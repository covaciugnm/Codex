# SEO tehnic: pagini publice în șapte limbi

## Ce primește vizitatorul

Serverul livrează de la prima cerere titlul, descrierea și conținutul paginii în HTML. Conținutul vizibil este în `#app`, apoi aceeași aplicație JavaScript încarcă interacțiunile. Textele vin din bundle-ul PostgreSQL folosit și de frontend. Nu există pagini separate pentru roboți, text SEO ascuns sau o copie în `noscript`.

Rutele publice sunt `/`, `/objects`, `/measure`, `/spaces`, `/uses`, `/people`, `/technology`, `/documentation`, `/about`. Fiecare are versiuni `en`, `de`, `fr`, `es`, `ro`, `hu`, `bg`. Exemplu: `https://3dscan.eva-org.com/uses?lang=ro`.

Google recomandă HTML care poate fi procesat direct și linkuri cu `href` real. Randarea pe server permite descoperirea conținutului înainte ca robotul să execute JavaScript. Acest lucru ajută accesibilitatea conținutului, fără a garanta indexarea sau poziția în căutări. [Documentația Google pentru SEO și JavaScript](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).

## O singură structură, conținut din DB

| Rută | Prefixul textelor |
| --- | --- |
| `/` | `hero` |
| `/objects` | `object` |
| `/measure` | `measure` |
| `/spaces` | `spaces` |
| `/uses` | `uses` |
| `/people` | `people` |
| `/technology` | `tech` |
| `/documentation` | `docs` |
| `/about` | `about` |

Titlul SEO folosește `prefix.metaTitle` când există. Altfel, pagina principală folosește `meta.title`, iar celelalte pagini folosesc `prefix.title` și numele produsului. Descrierea folosește `prefix.metaDescription`; alternativa este introducerea paginii. Pentru pagina principală, introducerea vine din `campaign.heroIntro`, apoi `hero.description` sau `meta.description`.

Pagina `/uses` afișează toate perechile disponibile `usecase.<id>.title` și `usecase.<id>.description`. Fiecare articol este vizibil și are ancora `usecase-<id>`. Nu se generează automat zeci de pagini cu variații minime ale acelorași cuvinte. Paginile existente afișează introducerea, secțiunile relevante și limitele descrise în textele lor. Linkurile de navigare păstrează limba.

Șabloanele înlocuiesc `{{product}}`, `{{docsPages}}` și celelalte variabile din DB. Modificarea unui text, unei variabile sau a metadatelor folosește mecanismul existent de actualizare live; SSR citește aceeași versiune de date. Conținutul conturilor și proiectelor private nu intră în rendererul SEO.

## Canonical, hreflang și descoperire

Fiecare combinație rută/limbă are un canonical autoreferențial. Parametrii suplimentari nu intră în URL-ul canonical. `sp` se normalizează la `es`; o limbă necunoscută se normalizează la `en`. Cererile fără limbă primesc HTML în engleză, determinist, fără redirecționare după IP sau User-Agent. Frontendul poate aplica preferința utilizatorului și păstrează limba aleasă în URL.

Fiecare document are cele șapte alternative `hreflang`, inclusiv limba curentă, plus `x-default` către engleză. Alternativele sunt reciproce și folosesc URL-uri absolute. Google recomandă aceste relații pentru versiunile localizate; limba reală se determină și din conținutul paginii, nu doar din atribute. [Documentația Google pentru versiuni localizate](https://developers.google.com/search/docs/specialty/international/localized-versions).

`/sitemap.xml` conține exact 63 de URL-uri publice și alternativele lor. Nu sunt incluse API-uri, conturi sau proiecte. Nu se inventează date `lastmod`. `/robots.txt` indică sitemap-ul și exclude rutele de autentificare și proiecte. `/api/content` rămâne accesibil pentru randare. Protejarea datelor private este făcută de autentificare; robots.txt nu este un control de acces. Răspunsurile API pentru autentificare și proiecte au și `X-Robots-Tag: noindex, nofollow`.

Originea implicită este `https://3dscan.eva-org.com`. `PUBLIC_BASE_URL` poate indica o altă origine HTTP(S) explicită; sunt respinse credențialele, căile, query-ul și fragmentul. URL-ul nu se construiește din headerul Host trimis de client.

## Date structurate și securitate

JSON-LD descrie un `SoftwareApplication` pentru iOS, cu numele proiectului, categoria UtilitiesApplication, limba și starea de dezvoltare. Nu sunt declarate prețuri, oferte, recenzii, evaluări, linkuri de descărcare sau o lansare în magazin. Starea folosește proprietatea [Schema.org creativeWorkStatus](https://schema.org/creativeWorkStatus), moștenită de [SoftwareApplication](https://schema.org/SoftwareApplication).

Marcajul semantic nu promite un rezultat Google îmbogățit. Documentația Google cere informații suplimentare pentru eligibilitatea unor astfel de rezultate; proiectul nu inventează date pentru a le îndeplini. [Documentația Google SoftwareApplication](https://developers.google.com/search/docs/appearance/structured-data/software-app).

Textul din DB este escaped înainte de includerea în HTML sau atribute. În JSON-LD, caracterul `<` este codificat pentru a preveni închiderea injectată a elementului script. CSP include hash-ul exact al acestui bloc; nu este permis JavaScript inline arbitrar. Metadatele Open Graph și Twitter folosesc aceleași titluri și descrieri.

## Cache și erori

ETag-ul HTML include documentul randat și bundle-ul complet, deci depinde de limbă, metadate, mesaje și variabile. Un document neschimbat răspunde 304, inclusiv la HEAD. HTML-ul nu folosește ETag-ul static al șablonului. Schimbarea limbii sau a conținutului invalidează răspunsul vechi.

Dacă bundle-ul nu poate fi citit din DB, ruta publică răspunde 503, `Cache-Control: no-store` și `Retry-After: 30`. Nu se livrează o pagină goală cu status 200 sau un răspuns 304 care ascunde eroarea. Fișierele statice își păstrează cache-ul existent.

## Validare și limite

`npm test` include `tests/backend-seo.mjs`: verifică cele 63 de variante, canonical, hreflang, conținut SSR, JSON-LD și hash CSP, cache după modificări, HEAD, aliasul sp, escaparea textelor, sitemap-ul și funcționarea API-urilor de autentificare/proiecte. Testul PostgreSQL se activează separat prin mediul existent de integrare.

După schimbări de frontend, verificați și metadatele după navigare și schimbarea limbii fără reload. ID-urile SSR sunt `seo-canonical`, `seo-alternate-<lang>` și `seo-jsonld`. Rootul `#app` este marcat `data-ssr="true"`, astfel încât frontendul să poată păstra pagina inițială dacă reîncărcarea bundle-ului eșuează.

Nu s-au trimis sitemap-uri în Search Console și nu s-au făcut publicări sau cereri de indexare prin acest patch. Confirmarea indexării reale necesită acces la domeniul public și, opțional, la proprietatea Search Console.
