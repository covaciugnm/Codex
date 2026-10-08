# Fara titlu

ID: `01a0fc36-5616-78c3-ad4a-537083aa5d7e`  
Proiect: 3D.AppleScan  
Export UTC: 2026-10-08T14:13:28.280906+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Backend implementat în `Site/`.

- API content, ETag/304, fallback EN, alias `sp→es`, SSE.
- PostgreSQL persistent, migrații, seed inițial protejat, import tranzacțional și editare CLI.
- Docker Node22 + PostgreSQL17.11; app nonroot/read-only, port loopback4160, DB fără port public.
- Fișiere HTTP limitate la `public/`; sursele, documentația și secretele nu sunt servite.
- Testele HTTP trec; toate cele 7 seed-uri au câte 94 mesaje valide.
- Test PostgreSQL pregătit, necesită `TEST_DATABASE_URL`; Docker local nu rulează.
- Documentație: `docs/BACKEND.md`; jurnal: `docs/backend-events.jsonl`.

Contract: `{locale,revision,variables,messages}`; `revision` este string; variabilele includ `docsPages:89`.

## Asistent

Hardening și ETag gata; testele locale trec.

**Deploy**
```sh
docker compose up -d --build app
```

**Teste PostgreSQL reale**
```sh
docker compose run --rm -e TEST_PG=1 -v "$PWD/tests:/app/tests:ro" content npm test
```

App folosește numai rolul `eva_site_runtime`, cu SELECT și LISTEN. `migrate` și `content` păstrează operațiile privilegiate. Necesar: `PGAPP_PASSWORD` distinct, minimum 24 caractere. `.env` existent neatins.

ETag include întreg bundle, inclusiv variables; testul pentru schimbare configurație cu revizie DB identică trece. Documentația și jurnalul sunt actualizate.

## Asistent

Gata:

- `content` are `/tmp` tmpfs pentru teste.
- Fișierele statice au ETag, Last-Modified și răspuns 304 înainte de citirea conținutului.
- HEAD returnează metadate fără payload.
- Testele verifică 200→304, HEAD și invalidarea după modificarea unui fișier cu aceeași dimensiune.

Testele locale trec. Copiază `compose.yaml`, `server/http.mjs`, `tests/backend-http.mjs`; documentația și jurnalul sunt actualizate.

## Asistent

Variabilele comune sunt acum editabile în PostgreSQL fără rebuild.

- Migrarea `002` păstrează valorile existente.
- Modificările actualizează revizia, cache-ul și browserul prin SSE.
- Runtime are numai SELECT.
- CLI acceptă JSON scalar, maximum 16 KiB.
- README, documentația și testele sunt actualizate; testele locale trec.

```sh
docker compose run --rm content node scripts/set-variable.mjs --key docsPages --value 89
docker compose run --rm content node scripts/set-variable.mjs --key product --value '"EVA 3D Scan"'
```

Migrarea `001`, `.env`, volumul și frontendul au rămas intacte. Sunt pregătite testele PostgreSQL extinse pentru rularea remote.

## Asistent

Remediere gata:

- Migrarea `003` limitează numerele la intervalul finit JavaScript.
- Datele existente invalide opresc migrarea cu cheia problematică; nimic nu este modificat automat.
- API respinge defensiv valorile nefinite.
- Teste adăugate pentru `±1e999`, `±Number.MAX_VALUE` și păstrarea datelor invalide la eșecul migrării.

**3 teste locale trec.** Integrarea PostgreSQL așteaptă rularea remote. Migrațiile `001` și `002` sunt intacte.

## Asistent

SEO backend gata:

- SSR pentru 9 pagini × 7 limbi, din bundle-ul DB.
- Canonical, hreflang, Open Graph, JSON-LD și sitemap cu 63 URL-uri.
- ETag dependent de conținut și limbă; DB indisponibil → 503.
- Autentificarea și proiectele păstrate.
- **7 teste trecute**, integrarea PostgreSQL omisă local.

Fișiere: `server/seo.mjs`, `server/http.mjs`, `tests/backend-seo.mjs`, fixture-ul `backend-http.mjs`, `docs/SEO_TEHNIC.md`.

Documentația include [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) și [hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions). Frontendul trebuie să sincronizeze metadatele la navigare și schimbarea limbii, conform mappingului transmis.
