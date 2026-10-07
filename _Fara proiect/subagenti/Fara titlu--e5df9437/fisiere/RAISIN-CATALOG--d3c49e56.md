# Catalogul celor 17 produse cu stafide

Sursa editorială: `food/raisin-drafts.json`. Manifestul SKU și imaginilor:
`food/raisin-import-manifest.json`.

Produsele DF-003–DF-012 aparțin categoriei „Stafide naturale și soiuri”;
DF-013–DF-019 aparțin categoriei „Stafide aromatizate și infuzate”.
Fiecare produs are texte RO, EN și DE în PostgreSQL și status `draft`.
Prețul tehnic 0, `needs_price_review=true`, stocul 0 și `is_in_stock=false`
nu reprezintă date comerciale confirmate. Produsele nu apar în magazinul public.

Import pe server, fără reconstruirea sau oprirea magazinului:

```sh
cd /home/saga-server/site-uri/dracula-food
docker compose run --rm -T --no-deps \
  -v /home/saga-server/site-uri/dracula-food:/import:ro \
  migrate python /import/backend/import_raisin_drafts.py --root /import
```

La instalarea inițială se poate adăuga `--verify`, care verifică exact 17 produse
draft, 2 produse publicate, 51 de traduceri și distribuția 10/7. Nu folosiți această
opțiune după publicarea sau modificarea intenționată a catalogului.

Importul poate fi repetat: nu rescrie prețuri, stocuri, categorii, traduceri,
imagini deja alese, conturi sau comenzi. Imaginile se atașează numai dacă fișierul
corespunzător există în `backend/public/assets/produse` și produsul nu are deja o
imagine. Aceeași comandă atașează imaginile generate ulterior. Pentru servirea
fișierelor noi, includeți-le în imaginea backend la următorul deployment.

Verificare efectuată pe server: import inițial cu 17 inserări, a doua rulare cu
0 inserări; 17 draft + 2 publicate; 51 traduceri; 10/7 categorii. Conturile și
comenzile au rămas identice, verificate prin hash în tranzacția importului.
Endpointul public `/api/dracula/bootstrap` continuă să returneze doar nucile și
alunele. Raportul ultimei rulări: `food/raisin-import-report.json`.
