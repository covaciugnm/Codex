from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'outputs'
for folder,slug,port,webport,logo in [('dracula-design-office','dracula-design',4182,4181,'dracula-design-logo-auriu.jpeg'),('dracula-food','dracula-food',4184,4183,'dracula-food-logo.jpeg')]:
    root=ROOT/folder
    mail=root/'backend/app/mail'
    p=mail/'sender.py'
    s=p.read_text(encoding='utf-8')
    s=s.replace('    env = _from_env()\n', '''    env = _from_env()
    # Explicit local-capture mode cannot be overridden by production DB settings.
    if os.environ.get("MAIL_CAPTURE_ONLY") == "true":
        return replace(env, host="mailpit", port=1025, security="none", user="", password="", source="local-capture")
''',1)
    p.write_text(s,encoding='utf-8')
    p=mail/'render.py';s=p.read_text(encoding='utf-8')
    s=s.replace('from html import escape','import os\nfrom html import escape')
    s=s.replace('BRAND = "#0f766e"','BRAND = "#681b24"').replace('ACCENT = "#f59e0b"','ACCENT = "#b89a64"')
    s=s.replace('("termeni-si-conditii",','("terms",').replace('("politica-de-confidentialitate",','("privacy",').replace('("politica-de-retur-si-garantie",','("returns",').replace('("contacteaza-ne",','("contact",')
    s=s.replace('return f"{_base(base_url)}/account"','return f"{_base(base_url)}/ro/account"')
    start=s.index('    base = _base(base_url)\n',s.index('def _order_url'))
    end=s.index('\n\n\ndef _lines',start)
    s=s[:start]+'    return _account_url(base_url)\n'+s[end:]
    s=s.replace('logo = f"{_base(base_url)}/static/email/logo_light.png"',f'logo = _abs_url(base_url, os.environ.get("EMAIL_LOGO_PATH", "/assets/brand/{logo}"))')
    s=s.replace('f\'<a href="{escape(base)}/legal/{quote(slug)}" \'','f\'<a href="{escape(base)}/{quote(locale)}/pages/{quote(slug)}" \'')
    s=s.replace('DEFAULT_CONTACT_EMAIL = "office@cesiro.ro"',f'DEFAULT_CONTACT_EMAIL = os.environ.get("SMTP_REPLY_TO") or os.environ.get("SMTP_FROM") or "contact@{slug}.com"')
    s=s.replace('url = f"{_base(base_url)}/?panel=account&verify={quote(token)}"','url = f"{_base(base_url)}/{quote(locale)}/account?verify={quote(token)}"')
    s=s.replace('url = f"{_base(base_url)}/reset-password?token={quote(token)}&lang={quote(locale)}"','url = f"{_base(base_url)}/{quote(locale)}/reset-password?token={quote(token)}"')
    p.write_text(s,encoding='utf-8')
    p=mail/'notify.py';s=p.read_text(encoding='utf-8').replace('or "https://cesiro-nou.eva-org.com"',f'or "http://127.0.0.1:{webport}"').replace('return str(row or "CESIRO")',f'return str(row or "{slug.replace("-"," ").title()}")')
    s=s.replace('def _store_name(session, tenant_id: str) -> str:\n','''def _store_name(session, tenant_id: str) -> str:
    from .texts import bind_translations
    rows = session.execute(text("SELECT key, values FROM core.ui_translations WHERE tenant_id=CAST(:t AS uuid) AND key LIKE 'email.%'"), {"t":tenant_id}).all()
    bind_translations({row.key[6:]: row.values for row in rows})
''')
    p.write_text(s,encoding='utf-8')
    p=mail/'texts.py';s=p.read_text(encoding='utf-8').replace('from __future__ import annotations','''from __future__ import annotations
from contextvars import ContextVar

_tenant_texts = ContextVar("dracula_mail_texts", default={})

def bind_translations(values):
    _tenant_texts.set(values)
''').replace('entry = TEXTS.get(key) or {}','entry = _tenant_texts.get().get(key) or TEXTS.get(key) or {}').replace('entry.get(locale) or entry.get("ro") or key','entry.get(locale) or entry.get("ro") or TEXTS.get(key, {}).get(locale) or TEXTS.get(key, {}).get("ro") or key')
    p.write_text(s,encoding='utf-8')
    (root/'backend/email_worker.py').write_text('''"""Dedicated queue consumer; no web server or factory startup required."""
import logging
import os
import time
from app.mail.outbox import process_outbox

logging.basicConfig(level=logging.INFO)
while True:
    try:
        result=process_outbox()
        if result["trimise"] or result["esuate"]:
            logging.info("Mail queue: %s",result)
    except Exception:
        logging.exception("Mail queue retry on next cycle")
    time.sleep(int(os.environ.get("MAIL_WORKER_INTERVAL", "5")))
''',encoding='utf-8')
    (root/'backend/seed_email_content.py').write_text('''"""Store editable email copy without replacing admin edits."""
import json
from sqlalchemy import text
from app.db import session_scope, set_session_context
from app.config import get_settings
from app.repositories.tenant_repo import get_tenant_id
from app.mail.texts import TEXTS

with session_scope(role="admin",superadmin="on") as session:
    tid=get_tenant_id(session,get_settings().default_tenant)
    set_session_context(session,tenant_id=tid)
    for key,values in TEXTS.items():
        session.execute(text("INSERT INTO core.ui_translations(tenant_id,key,values) VALUES(CAST(:t AS uuid),:k,CAST(:v AS jsonb)) ON CONFLICT DO NOTHING"),{"t":tid,"k":"email."+key,"v":json.dumps(values,ensure_ascii=False)})
print("Email translations prepared; existing content preserved.")
''',encoding='utf-8')
    compose=f'''# Explicit development overlay: all email remains in this stack's Mailpit.
x-local-email: &local-email
  MAIL_CAPTURE_ONLY: "true"
  MAIL_WORKER: "false"
  SMTP_HOST: mailpit
  SMTP_PORT: "1025"
  SMTP_SECURITY: none
  SMTP_USER: ""
  SMTP_PASSWORD: ""
  SMTP_FROM: no-reply@{slug}.com
  SMTP_REPLY_TO: contact@{slug}.com
  ORDER_NOTIFICATION_EMAIL: admin@{slug}.com
  EMAIL_LOGO_PATH: /assets/brand/{logo}
services:
  backend:
    environment: *local-email
  mailpit:
    image: axllent/mailpit:v1.31.1
    restart: unless-stopped
    environment:
      MP_DATABASE: /data/mailpit.db
      MP_MAX_MESSAGES: 1000
      MP_DISABLE_VERSION_CHECK: "true"
    ports:
      - "127.0.0.1:{port}:8025"
    volumes:
      - mail_capture:/data
    healthcheck:
      test: [CMD, wget, -q, --spider, http://127.0.0.1:8025/readyz]
      interval: 10s
      timeout: 3s
      retries: 6
  mail-worker:
    image: {slug}-backend
    restart: unless-stopped
    depends_on:
      db: {{condition: service_healthy}}
      mailpit: {{condition: service_healthy}}
    environment:
      <<: *local-email
      DATABASE_URL: postgresql+psycopg://eva_storefront:${{EVA_STOREFRONT_DB_PASSWORD}}@db:5432/{slug.replace('-','_')}
      ADMIN_DATABASE_URL: postgresql+psycopg://eva_admin_api:${{EVA_ADMIN_DB_PASSWORD}}@db:5432/{slug.replace('-','_')}
      DEFAULT_TENANT: {slug}
      STORAGE_BACKEND: postgres
      SECRETS_KEY: ${{SECRETS_KEY}}
      PUBLIC_BASE_URL: ${{PUBLIC_BASE_URL:-http://127.0.0.1:{webport}}}
      MAIL_WORKER_INTERVAL: "5"
    command: [python, email_worker.py]
    healthcheck:
      test: [CMD-SHELL, "kill -0 1"]
      interval: 15s
      timeout: 3s
      retries: 3
volumes:
  mail_capture:
    name: {slug.replace('-','_')}_mail_capture
'''
    (root/'docker-compose.devmail.yml').write_text(compose,encoding='utf-8')
    (root/'ops/start-devmail.sh').write_text('''#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 ops/prepare.py
docker compose -f docker-compose.yml -f docker-compose.devmail.yml config --quiet
docker compose -f docker-compose.yml -f docker-compose.devmail.yml build backend
docker compose -f docker-compose.yml -f docker-compose.devmail.yml run --rm --no-deps backend python seed_email_content.py
docker compose -f docker-compose.yml -f docker-compose.devmail.yml up -d --no-deps backend mailpit mail-worker
docker compose -f docker-compose.yml -f docker-compose.devmail.yml ps
''',encoding='utf-8')
    (root/'ops/EMAIL.md').write_text(f'''# Email — {slug}

Mesajele sunt capturate local cu `docker-compose.devmail.yml`. Fiecare site are propriul Mailpit, volum și worker; niciun mesaj capturat nu este retransmis extern. SMTP port 1025 nu este publicat. UI este numai pe server loopback: http://127.0.0.1:{port}.

Pornire: `sh ops/start-devmail.sh`. Pentru comenzile ulterioare de recreare folosește mereu `docker compose -f docker-compose.yml -f docker-compose.devmail.yml ...` cât modul de test rămâne activ. Capturarea are prioritate față de setările SMTP din admin.

De pe calculator: `ssh -N -L {port}:127.0.0.1:{port} saga-server@192.168.100.151`, apoi http://127.0.0.1:{port}. Nu publica interfața Mailpit prin Cloudflare; conține linkuri temporare de verificare/resetare.

Textele email sunt salvate în PostgreSQL, `core.ui_translations`, cu prefixul `email.` și pot fi traduse din admin. Antetul folosește logo-ul acestui site; footer-ul și linkurile duc la paginile Dracula.

## SMTP real

Nu sunt configurate credențiale SMTP Dracula. CESIRO are o configurație proprie, care nu a fost copiată. Pentru livrare reală sunt necesare host, port, TLS, utilizator/parolă, expeditor verificat pentru acest domeniu, Reply-To și destinatarul notificărilor interne. Pot fi salvate în admin (parola criptată) sau în `.env`; nu în surse. Sunt necesare înregistrările DNS ale furnizorului (SPF/DKIM și DMARC).

La trecerea la producție: oprește workerul de test; verifică și exclude eventualele mesaje demonstrative încă pending din outbox, setează URL-ul public și SMTP-ul verificat, elimină overlay-ul devmail și pornește workerul cu configurarea de producție. Verifică livrarea către o adresă autorizată înainte de activarea vânzărilor.

Documentație Mailpit: https://mailpit.axllent.org/docs/install/docker/
''',encoding='utf-8')
print('Email implementation written for both sites.')
