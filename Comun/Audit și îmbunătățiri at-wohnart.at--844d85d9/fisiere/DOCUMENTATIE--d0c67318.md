# Dracula Book — www.dracula-book.com · Documentație de operare (platformă, din 24–28.09.2026)

Magazin pe platforma EVA Storefront (copie a motorului cesiro.com, FĂRĂ datele Cesiro),
stack Docker separat `draculabook` în acest folder. Site-ul static vechi: backup la
https://dracula-book.com/index1/ + `docker-compose.static-vechi.yml` / `.env.static-vechi` /
`DOCUMENTATIE-site-static-vechi.md`; copie completă în `../_backup-dracula-book-20260924`.

## Servicii (`docker compose ps`)
| Serviciu | Rol | Port local |
|---|---|---|
| db | Postgres 16, volum `dracula_pgdata` (NICIODATĂ `down -v`) | 127.0.0.1:5440 |
| backend | Flask/gunicorn: magazin + API admin | 127.0.0.1:4130 |
| web | nginx: `/admin/` (React), proxy backend, `/citire-api/` → reader, `/index1/`, `/carti/` | 127.0.0.1:4131 |
| reader | cititorul online (PDF → imagini cu filigran), SQLite `reader/data/reader.db` | intern |
| tunnel | Cloudflare tunnel „dracula-book.com" → http://web:80 | — |

Comenzi: `docker compose up -d --build <serviciu>` · migrații: `docker compose --profile tools run --rm migrate`
· după migrare pe bază nouă: `docker compose restart backend` (seed tenant + admin).

## Conturi
- Admin: https://dracula-book.com/admin — `covaciu.gnm@gmail.com` (parola în .env: ADMIN_SEED_PASSWORD).
- Clienți: login/cont în dreapta sus; același cont dă acces și la „Citește online" (abonamente).
  Parola clienților: minimum 10 caractere. Confirmarea adresei: link din e-mail (/?verify=…).
- Admin comenzi cititor (aprobare plăți): https://dracula-book.com/citire-api/admin?p=<READER_ADMIN_PASS>.

## E-mail
SMTP prin mailcow eva-org.com (`SMTP_HOST=mail.eva-org.com`, rezolvat intern prin `extra_hosts`
→ 192.168.100.151; certificatul autosemnat mailcow e adăugat în `certs/ca-bundle.pem`, folosit prin
`SSL_CERT_FILE`). Expeditor noreply@eva-org.com. Căsuță de test: dracula@eva-org.com.
Coada: `sales.outbox_emails` (status sent/failed).

## Modificări față de motorul cesiro (în acest folder)
- Poze de produs PE LIMBĂ: coloana `catalog.product_images.locales` (migrarea 0049); în admin
  (Produse → Imagini) file RO/EN/DE/HU/BG/EL + bife pe fiecare poză; fără bifă = comună.
  Magazinul arată pozele limbii curente + cele comune. Variantele WebP se regenerează automat
  la încărcare/ștergere/reordonare.
- Rută `/media/<tenant>/…` pentru fișierele încărcate din panou; `/citeste` (pagina cititorului);
  link „Citește online" în antet; culori/favicon Dracula (`static/themes/dracula.css`).
- Reparații: migrarea 0002 pe bază nouă; confirmarea e-mailului (RLS) — reparată și pe cesiro.com;
  contorul de produse din categorii la editarea unui singur produs.
- Cititor: token de pagină legat de cont, blocare hotlink, limită 20 pag/min și 300/oră per cititor,
  filigran cu e-mail + rând de urmărire (cont, carte, pagină, dată), blocare copiere/printare/salvare.
- Scripturi de populare: `_scripts/seed_dracula.py`, `seed_legal.py`, `seed_covers.py`.
