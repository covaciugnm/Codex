"""Coada de e-mailuri: `sales.outbox_emails`, cu retry și worker de fundal.

De ce coadă și nu trimitere directă din request: un server SMTP lent sau picat nu are
voie să blocheze plasarea unei comenzi. Mesajul se scrie în aceeași tranzacție cu
comanda — dacă tranzacția cade, nu rămâne un e-mail „fantomă"; dacă reușește, mesajul
pleacă în câteva secunde.

Corpul se stochează în `body_enc`, care e `bytea`. Pentru mesajele generate de aplicație
păstrăm un JSON UTF-8 cu `{subject, text, html, bcc}` — nu conțin secrete (parolele nu se
mai trimit niciodată prin e-mail; se trimite un link de setare).
"""
from __future__ import annotations

import json
import logging
import threading
import time
from typing import Any

from sqlalchemy import text

from ..config import get_settings
from ..db import session_scope, set_session_context
from .sender import resolve_settings, send_email

log = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
BACKOFF_SECONDS = (0, 60, 300)          # imediat, după 1 min, după 5 min
BATCH = 20


def enqueue(session, *, tenant_id: str, template: str, to_email: str, subject: str,
            text_body: str, html_body: str = "", locale: str = "ro",
            order_id: str | None = None, user_id: str | None = None,
            bcc: str = "", sensitive: bool = False) -> None:
    """Pune un mesaj în coadă, în tranzacția curentă."""
    payload = json.dumps(
        {"subject": subject, "text": text_body, "html": html_body, "bcc": bcc},
        ensure_ascii=False,
    ).encode("utf-8")
    session.execute(
        text(
            """
            INSERT INTO sales.outbox_emails
                   (tenant_id, order_id, user_id, template, to_email, subject,
                    body_enc, locale, sensitive, status, created_at)
            VALUES (CAST(:t AS uuid), CAST(:order_id AS uuid), CAST(:user_id AS uuid),
                    :template, :to_email, :subject, :body, :locale, :sensitive, 'pending',
                    -- clock_timestamp, nu now(): în aceeaşi tranzacţie now() e identic
                    -- pentru toate mesajele, iar workerul (ORDER BY created_at) le-ar
                    -- trimite în ordine aleatoare — „Bine ai venit" după confirmare
                    clock_timestamp())
            """
        ),
        {"t": tenant_id, "order_id": order_id, "user_id": user_id, "template": template,
         "to_email": to_email, "subject": subject[:500], "body": payload,
         "locale": locale, "sensitive": sensitive},
    )


def _claim(session, limit: int) -> list[Any]:
    """Ia din coadă mesajele de trimis și le marchează `sending` (fără curse între workeri)."""
    return session.execute(
        text(
            """
            UPDATE sales.outbox_emails
               SET status = 'sending', attempts = attempts + 1
             WHERE id IN (
                 SELECT id FROM sales.outbox_emails
                  WHERE status IN ('pending', 'failed')
                    AND attempts < :max_attempts
                    AND created_at > now() - interval '7 days'
                  ORDER BY created_at
                  LIMIT :limit
                  FOR UPDATE SKIP LOCKED
             )
            RETURNING id, tenant_id, to_email, subject, body_enc, attempts, template
            """
        ),
        {"limit": limit, "max_attempts": MAX_ATTEMPTS},
    ).all()


def process_outbox(limit: int = BATCH) -> dict[str, int]:
    """Trimite un lot. Întoarce `{trimise, esuate, ramase}`."""
    settings = get_settings()
    if not settings.postgres_enabled:
        return {"trimise": 0, "esuate": 0, "ramase": 0}

    sent = failed = 0
    with session_scope(role="admin", superadmin="on") as session:
        rows = _claim(session, limit)
        session.commit()                     # marcajul „sending" se vede imediat
        for row in rows:
            set_session_context(session, tenant_id=str(row.tenant_id))
            email_settings = resolve_settings(session, str(row.tenant_id))
            try:
                payload = json.loads(bytes(row.body_enc).decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                payload = {"subject": row.subject, "text": "", "html": ""}
            if not email_settings.configured:
                session.execute(
                    text(
                        """
                        UPDATE sales.outbox_emails
                           SET status = 'pending', attempts = GREATEST(0, attempts - 1), last_error = 'SMTP neconfigurat'
                         WHERE id = :id
                        """
                    ),
                    {"id": row.id},
                )
                continue
            result = send_email(
                email_settings,
                to=row.to_email,
                subject=payload.get("subject") or row.subject,
                text_body=payload.get("text") or "",
                html_body=payload.get("html") or "",
                bcc=payload.get("bcc") or "",
            )
            if result.ok:
                sent += 1
                session.execute(
                    text(
                        """
                        UPDATE sales.outbox_emails
                           SET status = 'sent', sent_at = now(), last_error = NULL
                         WHERE id = :id
                        """
                    ),
                    {"id": row.id},
                )
            else:
                failed += 1
                final = row.attempts >= MAX_ATTEMPTS
                log.warning("e-mail %s către %s a eșuat (%s/%s): %s", row.template,
                            row.to_email, row.attempts, MAX_ATTEMPTS, result.detail)
                session.execute(
                    text(
                        """
                        UPDATE sales.outbox_emails
                           SET status = CASE WHEN :final THEN 'failed' ELSE 'pending' END,
                               last_error = :error
                         WHERE id = :id
                        """
                    ),
                    {"id": row.id, "error": result.detail[:500], "final": final},
                )
        remaining = session.execute(
            text(
                """
                SELECT count(*) FROM sales.outbox_emails
                 WHERE status IN ('pending', 'failed') AND attempts < :max_attempts
                """
            ),
            {"max_attempts": MAX_ATTEMPTS},
        ).scalar() or 0
    return {"trimise": sent, "esuate": failed, "ramase": int(remaining)}


_worker_started = threading.Event()


def start_worker(interval: int = 30) -> None:
    """Pornește firul de fundal care golește coada (o singură dată per proces)."""
    if _worker_started.is_set():
        return
    settings = get_settings()
    if not settings.postgres_enabled:
        return
    _worker_started.set()

    def loop() -> None:
        # mică întârziere: nu concurăm cu pornirea aplicației
        time.sleep(10)
        while True:
            try:
                result = process_outbox()
                if result["trimise"] or result["esuate"]:
                    log.info("outbox: %s", result)
            except Exception:                 # noqa: BLE001 - firul nu are voie să moară
                log.exception("ciclul de trimitere a e-mailurilor a eșuat")
            time.sleep(interval)

    thread = threading.Thread(target=loop, name="outbox-worker", daemon=True)
    thread.start()
    log.info("worker outbox pornit (interval %ss)", interval)
