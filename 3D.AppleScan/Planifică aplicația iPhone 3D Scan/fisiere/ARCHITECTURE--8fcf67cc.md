# Arhitectura site-ului

## O singură structură pentru toate limbile

`public/index.html` este intrarea comună. `public/app.js` conține structura celor șapte pagini. Nu există variante HTML separate pentru en/de/fr/es/ro/hu/bg. Routerul schimbă secțiunea cu History API, iar parametrul `lang` păstrează aceeași pagină atunci când limba se schimbă. `sp` se normalizează la `es`.

La pornire, browserul solicită un singur bundle al limbii. Acesta conține mesajele, variabilele și revizia. Dicționarul este reutilizat pentru navigare și pentru limbile deja încărcate. Cererile depășite se anulează; intenția de limbă este urmărită separat de limba deja randată. Navigarea înapoi și evenimentele de reconectare nu suprascriu alegerea curentă.

## Actualizări rapide

PostgreSQL păstrează câmpurile traduse. Triggerele actualizează revizia numai la modificări reale și emit NOTIFY după commit. Backendul invalidează cache-ul și transmite un eveniment SSE. Browserul cere bundle-ul curent și înlocuiește textele în pagina existentă. Nu este necesară generarea a șapte site-uri sau o reîncărcare de document.

Toate valorile text sunt escape-uite înainte de introducerea în HTML. Administrarea se face prin scripturile serviciului `content`; nu există endpoint public de editare. Traducerile au fost redactate în această sesiune și verificate structural; o revizie lingvistică de către vorbitori nativi rămâne recomandată înainte de o campanie comercială.

## Rulare

Docker Compose pornește PostgreSQL 17 și aplicația Node 22. Serviciul de migrare se termină înainte de pornirea aplicației. Contul runtime are numai citire și accesul necesar ascultării evenimentelor. Baza de date nu expune port pe gazdă, iar aplicația este legată la loopback 4160. Accesul public necesită configurarea domeniului și a reverse proxy-ului separat.

Aplicația servește numai `public/`. Fișierele originale de cercetare din `Aplicație`, cheile `.deploy`, sursele, scripturile și jurnalele sunt în afara rădăcinii publice. În `public/downloads` sunt copiate explicit PDF-ul de prezentare și exemplele sintetice.

## Performanță

Nu există framework frontend, fonturi externe, scripturi de analiză sau CDN. JavaScript și CSS sunt servite local, imaginile sunt WebP, iar imaginile de sub primul ecran sunt încărcate întârziat. ETag permite revalidare fără transferul repetat al fișierelor. Datele folosesc și cache în backend, și cache de dicționare în browser.

Rapoartele măsurate precizează condițiile testului. Timpii măsurați pe server local nu reprezintă o garanție pentru telefoane lente sau conexiuni mobile.

## Reluare

Consultați README, raportul auditorului, starea din `docs/STATUS.json` și jurnalele `*-events.jsonl`. Nu reinițializați volumul PostgreSQL la update. Migrațiile deja aplicate au checksum și nu se editează; se adaugă migrații noi. `ops/start.sh` păstrează `.env` existent. Datele persistente și configurația secretă necesită backup administrativ separat de cod.
