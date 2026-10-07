from pathlib import Path
root=Path(__file__).resolve().parents[1]/'outputs'
for folder,slug,port in [('dracula-design-office','dracula-design',4181),('dracula-food','dracula-food',4183)]:
 p=root/folder
 config=f'''# Real delivery: use ONLY after configuring this domain's authorized SMTP.
# Never combine with docker-compose.devmail.yml.
x-smtp: &smtp
  MAIL_CAPTURE_ONLY: "false"
  MAIL_WORKER: "false"
  SMTP_HOST: ${{SMTP_HOST:?Configure Dracula SMTP host}}
  SMTP_PORT: ${{SMTP_PORT:-587}}
  SMTP_SECURITY: ${{SMTP_SECURITY:-starttls}}
  SMTP_USER: ${{SMTP_USER:?Configure Dracula SMTP username}}
  SMTP_PASSWORD: ${{SMTP_PASSWORD:?Configure Dracula SMTP password}}
  SMTP_FROM: ${{SMTP_FROM:?Configure verified Dracula sender}}
  SMTP_REPLY_TO: ${{SMTP_REPLY_TO:?Configure Dracula reply address}}
  ORDER_NOTIFICATION_EMAIL: ${{ORDER_NOTIFICATION_EMAIL:?Configure shop notification recipient}}
services:
  backend:
    environment: *smtp
  mail-worker:
    image: {slug}-backend
    restart: unless-stopped
    depends_on:
      db: {{condition: service_healthy}}
    environment:
      <<: *smtp
      DATABASE_URL: postgresql+psycopg://eva_storefront:${{EVA_STOREFRONT_DB_PASSWORD}}@db:5432/{slug.replace('-','_')}
      ADMIN_DATABASE_URL: postgresql+psycopg://eva_admin_api:${{EVA_ADMIN_DB_PASSWORD}}@db:5432/{slug.replace('-','_')}
      DEFAULT_TENANT: {slug}
      STORAGE_BACKEND: postgres
      SECRETS_KEY: ${{SECRETS_KEY}}
      PUBLIC_BASE_URL: ${{PUBLIC_BASE_URL:?Configure public URL}}
      MAIL_WORKER_INTERVAL: "15"
    command: [python, email_worker.py]
'''
 (p/'docker-compose.smtp.yml').write_text(config,encoding='utf-8')
 doc=p/'ops/EMAIL.md'
 with doc.open('a',encoding='utf-8') as f:f.write('''
Overlay pregătit pentru livrare reală: `docker-compose.smtp.yml` (neactivat). Validează obligatoriu credențialele prin Compose. După configurarea `.env` și verificarea cozii: `docker compose -f docker-compose.yml -f docker-compose.smtp.yml config --quiet`, apoi `docker compose -f docker-compose.yml -f docker-compose.smtp.yml up -d --no-deps backend mail-worker`. Oprește Mailpit separat. Nu combina overlay-urile SMTP și devmail. Dacă folosești SMTP din admin, păstrează `.env` cu aceeași identitate verificată, ca rezervă și pentru pornirea workerului.
''')
print('Production SMTP overlays prepared, not enabled.')
