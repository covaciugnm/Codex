# Site EVA 3D Scan

Site de prezentare și documentare a proiectului iPhone EVA 3D Scan. Aplicația de scanare este în dezvoltare; site-ul prezintă cerințele și conceptul, iar exemplul de măsurare este sintetic.

## Ce include

- Pagina principală, obiecte, măsurare live, camere și clădiri, tehnologie, documentație și identitate EVA.
- Șapte limbi: en, de, fr, es, ro, hu, bg. `sp` este alias pentru `es`.
- O singură structură de pagini; dicționarele și variabilele schimbă conținutul fără reîncărcarea documentului.
- PostgreSQL cu texte editabile, revizii, cache, ETag și actualizare live prin Server-Sent Events.
- PDF-ul de cercetare în română, trei exemple sintetice descărcabile și siglă SVG.
- Docker Compose, volume persistente, citire pentru conținutul public și permisiuni dedicate funcțiilor de cont/proiect existente și servicii separate pentru operații administrative.

## Pornire

Pe server Linux cu Docker, din acest folder:

```sh
bash ops/start.sh
```

La prima pornire scriptul generează două parole diferite în `.env`, fără să le afișeze. Nu comite acest fișier. Site-ul este legat numai la `127.0.0.1:4160`; PostgreSQL nu expune un port pe gazdă. Pentru acces public, reverse proxy-ul domeniului trebuie să trimită către acest port și să permită SSE fără buffering. Pornirea serviciului nu configurează singură DNS sau HTTPS.

## Texte și traduceri fără rebuild

```sh
docker compose run --rm content node scripts/set-content.mjs --lang ro --key hero.title --value 'Titlul nou'
```

Modificarea este păstrată în PostgreSQL și transmisă paginilor deschise după commit. Reporniți aplicația fără a pierde textele. Fișierele JSON sunt sursa inițială de import, nu pagini HTML duplicate. Un import explicit reaplică valorile JSON; folosiți-l intenționat.

```sh
docker compose run --rm content node scripts/import-content.mjs
```

Variabilele comune (`product`, `languages`, `modules`, `docsPages`) sunt păstrate în PostgreSQL și se actualizează live, fără rebuild sau redeploy. Valorile CLI folosesc JSON: numerele și boolean-ele se scriu direct; textele trebuie să includă ghilimelele JSON.

```sh
docker compose run --rm content node scripts/set-variable.mjs --key docsPages --value 89
docker compose run --rm content node scripts/set-variable.mjs --key product --value '"EVA 3D Scan"'
```

Modificările variabilelor folosesc aceeași revizie, invalidare cache și notificare live ca textele. Repornirea păstrează valorile editate. Valorile implicite din configurație sunt folosite doar pentru cheile lipsă din DB.

## Testare și documente

`npm test` rulează verificările backend locale. `bash ops/verify.sh` execută și testele PostgreSQL, apoi testele de browser când Playwright și Chromium sunt disponibile. `PLAYWRIGHT_PACKAGE` poate indica un package.json al mediului de test care are Playwright instalat. Acesta este un instrument de test, nu o dependență a site-ului public.

Consultați `docs/BACKEND.md`, `docs/TRANSLATIONS.md`, `docs/BRAND.md`, `docs/AUDIT_SITE.md` și rapoartele din `docs/validation`. Fișierele interne și jurnalele nu sunt servite de aplicație.

## Organizarea proiectului

Documentația de cercetare originală și arhiva sunt în folderul vecin `Aplicație`. Fișierele operaționale existente `.codex`, `.deploy`, `ops` și `.gitignore` ale proiectului rădăcină au fost păstrate. Cheile de deploy nu au fost copiate în Site sau în imaginea Docker.

## Identitate și redesign

Marca curentă este **EVA-3dScan**. Prima pagină explică trei module și include cinci imagini de campanie într-un carusel, cu siglă animată. Ghid: `docs/IDENTITATE_EVA-3dScan.md`. Livrare și verificări: `docs/REDESIGN_LIVRAT.md`. Audit: `docs/AUDIT_REDESIGN.md`. Iconița pentru aplicație are copie în `../Aplicație/Identitate EVA-3dScan`.

## Navigare după client și problemă

Site public: https://3dscan.eva-org.com/?lang=ro. Prima pagină are două selectoare: șase profiluri plus proiect personal, apoi problema relevantă din catalogul de 36 utilizări. Nouă pagini, șapte limbi, 454 chei/localizare, texte dinamice în PostgreSQL și randare inițială pentru indexare.

Raport curent: docs/REDESIGN_CLIENTI_LIVRAT.md. Specificație: docs/CUSTOMER_FOCUS.md. Audit: docs/AUDIT_REDESIGN_V2.md.
