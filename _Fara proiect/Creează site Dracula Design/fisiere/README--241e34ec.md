# Dracula Design Office

Magazin privat pentru dracula-design.com. Frontend propriu Dracula; administrația și modelul PostgreSQL provin din codul local CESIRO. Fotografiile și sigla sunt cele furnizate.

## Acces

- Magazin: http://127.0.0.1:4181/
- Admin: http://127.0.0.1:4181/admin/
- Administrator test: admin@dracula-design.com
- Client test: client@dracula-design.com
- Parola este cea solicitată în conversație, nu este inclusă în cod.

Adresele locale funcționează cât timp tunelul SSH este deschis. Pentru redeschidere rulează ops/preview-ssh.ps1. Portul 4183 este rezervat proiectului independent Food.

## Server

Folder: /home/saga-server/site-uri/dracula-design (S:\dracula-design).

Pornește: sh ops/start.sh. Verifică: docker compose ps.

Servicii: PostgreSQL 16, migrații Alembic, Flask/Gunicorn, React/Nginx. Volum DB: dracula_design_pgdata. PostgreSQL nu are port public. Secretele sunt generate în .env pe server; nu provin din CESIRO. Nu folosi docker compose down -v dacă vrei să păstrezi baza.

Food are propriul proiect Compose, PostgreSQL, volum, rețea, secrete, conturi și tunel Cloudflare. Nu există date comune între magazine.

## Conținut în DB

- Produse: cele cinci piese, traduceri, prețuri, stocuri și imagini.
- Traduceri: textele publice hero.*, collection.*, product.*, checkout.* etc.; etichetele admin au prefix admin.*.
- Pagini legale: 14 pagini de companie, contact, termeni, confidențialitate, ștergere date, retur/garanție, retragere, livrare, plăți, cookies, reclamații, FAQ, Impressum și accesibilitate.
- Solicitări: formularele de contact, retragere, reclamații și date personale.
- Setări: limbile active, moneda, compania, brandingul și livrarea.

RO/EN/DE sunt inițiale. Setări → Cod limbă nouă permite adăugarea altor limbi; apoi se completează traducerile. Schema nu are listă închisă de limbi. Textele lipsă folosesc limba implicită. Reîncarcă panoul dacă un editor era deja deschis când ai adăugat limba.

Paginile acceptă variabile din datele companiei: {{company_name}}, {{address}}, {{cui}}, {{registration}}, {{email}}, {{phone}}. Seedul nu suprascrie datele deja editate la repornire.

Frontend: backend/public. Admin: frontend. API propriu: backend/app/dracula.py. Migrație proprie: 0053; migrațiile CESIRO anterioare sunt păstrate.

## Testare și lansare

Prețurile, stocurile, taxele și livrarea sunt demonstrative. Comenzile sunt salvate cu is_test=true. Cardurile și integrările comerciale nu efectuează plăți sau livrări în demo. Conturile, favoritele, coșul și comenzile folosesc PostgreSQL real.

Pentru vânzări rămân de configurat: prețuri/stocuri, taxe, țări/tarife/termene livrare, date juridice complete, contact, SMTP și procesator. Adresa Dracula-Castel (Castelul-Dracula) este cea furnizată, nu o adresă poștală completă validată. Paginile juridice sunt drafturi marcate în previzualizare.

Backendul include Stripe Checkout și webhook semnat. Activarea cere cheile proprii și testare cu procesatorul. Nu au fost testate încasări reale. Recuperarea parolei/verificarea emailului folosesc coada de mesaje, iar livrarea emailurilor necesită SMTP. Workerii de integrări externe sunt opriți implicit.

Cloudflare: vezi ops/CLOUDFLARE.md. Overlay-ul este pregătit, dar tunelul dedicat necesită token și rutele domeniului din contul Cloudflare. Nu se reutilizează tunelul CESIRO.

## Verificări

Build TypeScript/React în Docker; desktop și mobil 390px; RO/EN/DE; cont nou; transfer coș vizitator; favorite; comandă; validare preț server; idempotency; acces numai la comenzile proprii; CSRF/origin; separarea clienților de admin; modulele admin. Adăugarea limbii italiene și salvarea traducerilor în DB au fost testate, apoi limba dezactivată.

Suitele backend/test_integration.py și backend/test_admin.py rulează numai în demo, creează date QA și nu fac plăți. Administratorul temporar creat de test_admin.py trebuie dezactivat după verificare.

## Backup și imagini

sh ops/backup.sh creează dump PostgreSQL în backups. Salvează separat data, .env privat și sursele. Verifică restaurarea într-un proiect separat înaintea oricărei operațiuni distructive.

Originalele sunt organizate pe server în 01-brand, 02-produse, 03-colectii, 04-atmosfera și 99-duplicate. inventar-imagini.csv păstrează corespondența și hashurile. Duplicatul a fost păstrat. Folderul dist este prima previzualizare statică, nu magazinul cu DB care rulează în Docker.
