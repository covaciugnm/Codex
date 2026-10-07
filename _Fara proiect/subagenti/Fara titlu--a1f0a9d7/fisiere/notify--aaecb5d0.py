"""Legătura dintre evenimentele magazinului și e-mailurile trimise.

Un singur loc care știe „ce e-mail se trimite când", ca rutele să rămână curate.
Toate funcțiile scriu în coadă (`sales.outbox_emails`), în tranzacția primită —
niciuna nu vorbește direct cu serverul SMTP.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from sqlalchemy import text

from . import render
from .outbox import enqueue
from .sender import resolve_settings

log = logging.getLogger(__name__)


def _base_url() -> str:
    url = (os.environ.get("PUBLIC_BASE_URL") or "").strip()
    if url and "//" not in url:
        url = f"https://{url}"
    return url.rstrip("/") or "http://127.0.0.1:4181"


def _store_name(session, tenant_id: str) -> str:
    from .texts import bind_translations
    rows = session.execute(text("SELECT key, values FROM core.ui_translations WHERE tenant_id=CAST(:t AS uuid) AND key LIKE 'email.%'"), {"t":tenant_id}).all()
    bind_translations({row[0][6:]: row[1] for row in rows})
    row = session.execute(
        text(
            """
            SELECT coalesce(NULLIF(s.seller ->> 'public_name', ''),
                            NULLIF(t.display_name, ''), t.slug) AS name
              FROM core.tenants t
              LEFT JOIN core.tenant_settings s ON s.tenant_id = t.id
             WHERE t.id = CAST(:t AS uuid)
            """
        ),
        {"t": tenant_id},
    ).scalar()
    return str(row or "Dracula Design")


def _company(session, tenant_id: str) -> dict[str, Any]:
    """Datele de firmă pentru subsolul e-mailurilor.

    `core.tenant_settings.legal` ține adresa/telefonul/CUI-ul, `seller` numele
    comercial. Nimic hardcodat: dacă operatorul le schimbă din panou, se schimbă și
    în e-mailuri. IBAN-ul NU se citește de aici (stă în `core.tenant_secrets`) și
    nu are ce căuta într-o confirmare de comandă.
    """
    row = session.execute(
        text(
            """
            SELECT coalesce(s.legal, '{}'::jsonb) AS legal,
                   coalesce(s.seller, '{}'::jsonb) AS seller
              FROM core.tenant_settings s WHERE s.tenant_id = CAST(:t AS uuid)
            """
        ),
        {"t": tenant_id},
    ).first()
    if row is None:
        return {}
    legal = dict(row.legal or {})
    seller = dict(row.seller or {})
    legal.pop("iban", None)
    legal.pop("bank", None)
    return {
        "company_name": legal.get("company_name") or seller.get("legal_name") or "",
        "legal_name": seller.get("legal_name") or "",
        "cui": legal.get("cui") or seller.get("cui") or "",
        "registration": legal.get("registration") or "",
        "address": legal.get("address") or "",
        "phone": legal.get("phone") or "",
        "email": legal.get("email") or "",
    }


def _existing_tracking(session, order_id: str | None) -> dict[str, Any] | None:
    """AWB-ul comenzii, dacă a fost deja emis (rezumatul de pe `sales.orders`)."""
    if not order_id:
        return None
    try:
        row = session.execute(
            text("SELECT tracking_number, courier, tracking_url FROM sales.orders"
                 " WHERE id = CAST(:o AS uuid)"),
            {"o": order_id},
        ).first()
    except Exception:                                        # noqa: BLE001
        return None
    if row is None or not getattr(row, "tracking_number", ""):
        return None
    return {"tracking_number": row.tracking_number, "courier": row.courier or "",
            "tracking_url": row.tracking_url or ""}


def order_placed(session, *, tenant_id: str, order: dict[str, Any],
                 customer: dict[str, Any], shipping: dict[str, Any],
                 billing: dict[str, Any] | None = None,
                 locale: str = "ro", order_id: str | None = None,
                 user_id: str | None = None, paid: bool = False) -> None:
    """Confirmare către client + copie către magazin + WhatsApp.

    `paid=True` — comanda cu cardul, abia după încasare (webhook-ul Stripe): e-mailul
    spune „primită şi plătită", confirmarea WhatsApp arată „PLĂTITĂ online cu cardul”
    + „Total plătit”, iar copia magazinului e marcată PLĂTITĂ.
    """
    store = _store_name(session, tenant_id)
    company = _company(session, tenant_id)
    base_url = _base_url()
    # AWB-ul intră în confirmare DOAR dacă există deja (ex. AWB emis instant); altfel
    # pleacă în mesajul de expediere, imediat ce e emis.
    tracking = _existing_tracking(session, order_id)
    subject, text_body, html_body = render.order_confirmation(
        locale=locale, store=store, base_url=base_url, order=order,
        customer=customer, shipping=shipping, billing=billing, company=company,
        paid=paid, tracking=tracking,
    )
    to_email = str(customer.get("email") or "")
    if to_email:
        enqueue(session, tenant_id=tenant_id, template="order_confirmation",
                to_email=to_email, subject=subject, text_body=text_body,
                html_body=html_body, locale=locale, order_id=order_id, user_id=user_id)

    settings = resolve_settings(session, tenant_id)
    notify_to = settings.order_notification_email
    if notify_to:
        n_subject, n_text, n_html = render.order_notification(
            store=store, base_url=base_url, order=order, customer=customer,
            shipping=shipping, billing=billing, company=company,
        )
        if paid:
            n_subject = f"[PLĂTITĂ CU CARDUL] {n_subject}"
        enqueue(session, tenant_id=tenant_id, template="order_notification",
                to_email=notify_to, subject=n_subject, text_body=n_text,
                html_body=n_html, locale="ro", order_id=order_id)

    # Ordinea: confirmarea clientului, copia magazinului, apoi WhatsApp-ul (regula
    # proprietarului pentru fluxul card v2). Un mesaj scurt, în ACEEAȘI tranzacție. Funcția
    # își înghite singură orice eroare — o notificare nu are voie să rupă o vânzare.
    from ..notifications import order_placed as wa_order_placed

    wa_order_placed(session, tenant_id=tenant_id, order=order, customer=customer,
                    locale=locale, order_id=order_id, user_id=user_id,
                    shipping=shipping, paid=paid, tracking=tracking)

def order_status_changed(session, *, tenant_id: str, order_number: str, status: str,
                         to_email: str, name: str = "", locale: str = "ro",
                         order_id: str | None = None, user_id: str | None = None,
                         phone: str = "", tracking_number: str = "", courier: str = "",
                         tracking_url: str = "") -> None:
    # WhatsApp-ul pleacă și dacă nu avem adresă de e-mail (unele comenzi vechi n-au),
    # deci se face ÎNAINTEA verificării de mai jos.
    from ..notifications import order_status_changed as wa_status

    if phone:
        wa_status(session, tenant_id=tenant_id, order_number=order_number, status=status,
                  phone=phone, locale=locale, order_id=order_id, user_id=user_id,
                  tracking_number=tracking_number, courier=courier,
                  tracking_url=tracking_url)
    if not to_email:
        return
    store = _store_name(session, tenant_id)
    subject, text_body, html_body = render.order_status(
        locale=locale, store=store, base_url=_base_url(), number=order_number,
        status=status, name=name, company=_company(session, tenant_id),
        tracking={"tracking_number": tracking_number, "courier": courier,
                  "tracking_url": tracking_url},
    )
    enqueue(session, tenant_id=tenant_id, template=f"order_status_{status}",
            to_email=to_email, subject=subject, text_body=text_body,
            html_body=html_body, locale=locale, order_id=order_id, user_id=user_id)


def account_created(session, *, tenant_id: str, to_email: str, name: str = "",
                    locale: str = "ro", user_id: str | None = None) -> None:
    store = _store_name(session, tenant_id)
    subject, text_body, html_body = render.account_welcome(
        locale=locale, store=store, base_url=_base_url(), name=name,
        company=_company(session, tenant_id),
    )
    enqueue(session, tenant_id=tenant_id, template="account_welcome", to_email=to_email,
            subject=subject, text_body=text_body, html_body=html_body, locale=locale,
            user_id=user_id)


def account_ready(session, *, tenant_id: str, to_email: str, name: str = "",
                  locale: str = "ro", user_id: str | None = None,
                  existing: bool = False, phone: str = "",
                  order_id: str | None = None) -> None:
    """E-mailul trimis la prima comandă: „ai cont" sau „am adăugat comanda în contul tău"."""
    store = _store_name(session, tenant_id)
    subject, text_body, html_body = render.auto_account(
        locale=locale, store=store, base_url=_base_url(), name=name, existing=existing,
        company=_company(session, tenant_id),
    )
    enqueue(session, tenant_id=tenant_id,
            template="account_existing" if existing else "account_auto_created",
            to_email=to_email, subject=subject, text_body=text_body,
            html_body=html_body, locale=locale, user_id=user_id)
    # Doar pentru contul CREAT acum: „ai deja cont" nu e o veste, e o redundanță.
    if not existing and phone:
        from ..notifications import account_created as wa_account

        wa_account(session, tenant_id=tenant_id, phone=phone, email=to_email,
                   locale=locale, user_id=user_id, order_id=order_id)


def email_verification(session, *, tenant_id: str, to_email: str, token: str,
                       name: str = "", locale: str = "ro",
                       user_id: str | None = None) -> None:
    store = _store_name(session, tenant_id)
    subject, text_body, html_body = render.verify_email(
        locale=locale, store=store, base_url=_base_url(), token=token, name=name,
        company=_company(session, tenant_id),
    )
    enqueue(session, tenant_id=tenant_id, template="account_verify", to_email=to_email,
            subject=subject, text_body=text_body, html_body=html_body, locale=locale,
            user_id=user_id)


def password_reset(session, *, tenant_id: str, to_email: str, token: str,
                   name: str = "", locale: str = "ro",
                   user_id: str | None = None) -> None:
    store = _store_name(session, tenant_id)
    subject, text_body, html_body = render.password_reset(
        locale=locale, store=store, base_url=_base_url(), token=token, name=name,
        company=_company(session, tenant_id),
    )
    enqueue(session, tenant_id=tenant_id, template="password_reset", to_email=to_email,
            subject=subject, text_body=text_body, html_body=html_body, locale=locale,
            user_id=user_id, sensitive=True)


def password_changed_by_admin(session, *, tenant_id: str, to_email: str, name: str = "",
                              locale: str = "ro", user_id: str | None = None) -> None:
    store = _store_name(session, tenant_id)
    subject, text_body, html_body = render.password_changed_by_admin(
        locale=locale, store=store, base_url=_base_url(), name=name,
        company=_company(session, tenant_id),
    )
    enqueue(session, tenant_id=tenant_id, template="password_changed_by_admin",
            to_email=to_email, subject=subject, text_body=text_body, html_body=html_body,
            locale=locale, user_id=user_id)


def order_paid(session, *, tenant_id: str, order_number: str, to_email: str,
               name: str = "", locale: str = "ro", order_id: str | None = None,
               user_id: str | None = None, phone: str = "", total: float = 0.0,
               currency: str = "RON") -> None:
    """Confirmarea plăţii: e-mail clientului, copie magazinului, WhatsApp.

    Se apelează din webhook-ul Stripe, DUPĂ ce plata a fost înregistrată. Fiecare
    canal îşi înghite propriile erori: banii sunt încasaţi, iar o notificare ratată
    nu are voie să întoarcă tranzacţia care marchează comanda plătită.
    """
    from ..notifications import order_paid as wa_order_paid

    if phone:
        wa_order_paid(session, tenant_id=tenant_id, order_number=order_number,
                      phone=phone, locale=locale, order_id=order_id, user_id=user_id,
                      total=f"{total:.2f} {currency}")
    store = _store_name(session, tenant_id)
    company = _company(session, tenant_id)
    total_text = f"{total:.2f} {currency}"
    if to_email:
        subject, text_body, html_body = render.order_paid(
            locale=locale, store=store, base_url=_base_url(), number=order_number,
            total=total_text, name=name, company=company,
        )
        enqueue(session, tenant_id=tenant_id, template="order_paid", to_email=to_email,
                subject=subject, text_body=text_body, html_body=html_body,
                locale=locale, order_id=order_id, user_id=user_id)

    settings = resolve_settings(session, tenant_id)
    if settings.order_notification_email:
        enqueue(
            session, tenant_id=tenant_id, template="order_paid_shop",
            to_email=settings.order_notification_email,
            subject=f"Plată încasată {order_number} · {total_text}",
            text_body=(f"Comanda {order_number} a fost plătită online.\n"
                       f"Total: {total_text}\n"
                       f"Client: {name}"),
            html_body="", locale="ro", order_id=order_id,
        )


def refund_initiated(session, *, tenant_id: str, order_number: str, to_email: str,
                     amount: float, method: str = "stripe", name: str = "",
                     locale: str = "ro", order_id: str | None = None,
                     user_id: str | None = None, phone: str = "",
                     currency: str = "RON") -> None:
    """„Rambursarea a fost inițiată": e-mail + WhatsApp către client (în coadă)."""
    from ..notifications import refund_initiated as wa_refund

    amount_text = f"{float(amount):.2f} {currency}"
    if phone:
        wa_refund(session, tenant_id=tenant_id, order_number=order_number, phone=phone,
                  locale=locale, order_id=order_id, user_id=user_id, amount=amount_text,
                  method=method)
    if not to_email:
        return
    subject, text_body, html_body = render.order_refund(
        locale=locale, store=_store_name(session, tenant_id), base_url=_base_url(),
        number=order_number, amount=amount_text, method=method, name=name,
        company=_company(session, tenant_id),
    )
    enqueue(session, tenant_id=tenant_id, template="order_refund", to_email=to_email,
            subject=subject, text_body=text_body, html_body=html_body, locale=locale,
            order_id=order_id, user_id=user_id)
