# RES-001 r03 — Rezultatul aplicațiilor preliminare

P-RESEARCH · 24.09.2026 · DRAFT în staging, neintegrat.  
Stare: PATRU APLICAȚII PRELIMINARE EXECUTATE; RETEST INDEPENDENT ÎNCĂ NECESAR.  
Nu sunt acordate scoruri, nu se emite acceptare de audit și nu se închide F-RES-SOURCES-001.

## Mandat și verdictul r02 preluat exact

Am citit planul r01, rezultatul r02, jurnalul de teste A-SOURCES r02, raportul final MD și JSON-ul r02, precum și CANON_EXISTENT și copiile locale necesare identificării. Raportul final era disponibil în timpul acestui mandat; nu a fost modificat.

Audit A-SOURCES r02: **02226da7-e236-4904-9aa6-d441708dcaf7**; auditor **01a0d0ee-a56e-7140-b26d-e212cb9c7fb8**; `reviewed_at=2026-09-24T05:36:34.8551667+03:00`. Verdict: **RETURN**. F-RES-SOURCES-001: **open**. GOV-RES-01: **closed**, exclusiv în domeniul procedural precizat de auditor. Aceste valori provin din E13:L3–L5 și câmpurile JSON E14, nu sunt judecăți sau închideri P-RESEARCH.

Planul E10:L117 cere aplicații pe WorkID-uri reale din NOIR, AURORA, MYTHICA și AMORIS; E11:L78 consemna că nu fuseseră executate. Jurnalul E12:L106–L112 semnalează și lipsa copiilor INTRARI_REFERINTA din probele contractuale RES. R03 adaugă aplicațiile preliminare și lista de probe locale; nu rescrie rezultatul r02 și nu îl redenumește retrospectiv drept test îndeplinit.

## Ce am executat

Au fost create exclusiv:

1. [APLICATII_WORKID_REALE.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r03_staging/APLICATII_WORKID_REALE.md>).
2. [REZULTAT_APLICATII_r03.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r03_staging/REZULTAT_APLICATII_r03.md>) — acest raport.

Am identificat patru valori existente din `BOOKS.id`, am verificat corespondența lor cu `shelf`/`saga`, titlurile și atribuirea afișată, apoi am aplicat câmpurile procedurii din banca r02. „WorkID” este explicit identificatorul de catalog, nu un ID nou și nu o mapare pretins verificată într-un alt registru.

| Colecție / WorkID real | Localizare aplicație | Acțiune / prezentare | Două opere distincte | Relații cu alte serii |
| --- | --- | --- | --- | --- |
| NOIR / `marienburg` | [Cazul 1, L18–L32](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r03_staging/APLICATII_WORKID_REALE.md:18>) | BM-011 / BM-008 | R6 Chinatown / R4 The Maid | nu se invocă |
| AURORA / `sunrise` | [Cazul 2, L34–L48](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r03_staging/APLICATII_WORKID_REALE.md:34>) | BM-009 / BM-016 | R5 The Obsession / R8 What Remains of Edith Finch | nu se invocă |
| MYTHICA / `crown` | [Cazul 3, L50–L64](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r03_staging/APLICATII_WORKID_REALE.md:50>) | BM-014 / BM-018 | R7 Hamilton / R9 Maus | nu se invocă |
| AMORIS / `hotelul` | [Cazul 4, L66–L80](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r03_staging/APLICATII_WORKID_REALE.md:66>) | BM-002 / BM-003 | R1 Guernsey / R2 The Last Letter from Your Lover | nu se invocă |

Fiecare fișă conține identificare și probe, ramă minim documentată, alegerea celor două mecanisme, transformare exploratorie de acțiune, POV/ordine/voce/ritm/dezvăluire, efect ipotetic, excluderi distincte și necunoscute pentru G01. Ținta tuturor este minimum 50.000 de cuvinte de proză EN într-o producție viitoare autorizată, cu RO/DE ulterior și separat. Nu se pretinde realizarea acestei lungimi.

Nu lipsește niciunul dintre cele patru identificatoare de catalog. Lipsurile rămase sunt consemnate punctual: autor personal neidentificat pentru NOIR în sursele folosite; atribuire Armin Vale în catalog versus Cesiro Horeca în N.docx pentru MYTHICA. Pentru toate, versiunea narativă de referință și compatibilitatea integrală necesită verificare G01. E05 este un revision log vechi, iar E06 o bible de dezvoltare cu limite raportate în E08; nu au fost promovate la canon integral.

## Controale de autor efectiv realizate

| Control | Operație / observație |
| --- | --- |
| Identificatori reali | Căutare în segmentul BOOKS al copiei SITE_APP, fără executarea JavaScript-ului: câte o singură înregistrare pentru marienburg/noir/noirvol, sunrise/aurora/cycle, crown/mythica/crowns și hotelul/amoris/isabella. Titlurile și denumirile au fost confruntate cu CAT. |
| Ancorare și lipsuri | Lectura metadatelor relevante, a ambelor indexuri și a raportului CANON_EXISTENT; lectura E05 și a membrului E06; numai P1–P5 din E07. Autorul absent și atribuirea contradictorie au fost păstrate, fără inventarea unei soluții. |
| Aplicarea procedurii | Patru fișe redactate și recitite integral; fiecare acoperă toate câmpurile cerute, separat pe WorkID. Variantele de prezentare nu cer personaj, calendar sau lume din altă colecție. |
| Mecanisme / surse | Fiecare ID selectat există o singură dată în bancă; perechile trimit fiecare la două opere distincte. Banca r02 păstrează exact 18 ID-uri unice și nouă opere, fără operații noi sau schimbări ale indicatorilor lor. |
| Întindere | Aproximativ 357, 382, 358 și 385 de cuvinte pe caz înaintea transformării citărilor în linkuri; numărătoare orientativă a textului vizibil, nu scor. Nu se repetă sinopsisurile celor nouă opere și nu se adaugă cercetare de piață. |
| Probe / integritate | Am calculat SHA-256 pentru fișierele enumerate mai jos. SITE_APP, CAT, Z și N coincid ca hash/mărime cu index_origine; HBT coincide cu SUPLIMENT_r02. Membrul bible are hash separat, indicat în aplicații. |
| Independență editorială | Catalogul descrie cadrul minim; nu dovedește canon integral. Propunerile sunt marcate exploratorii, conexiunile sunt neinvocate, excluderile sunt separate pentru fiecare operă. Nu s-au transferat scene recognoscibile. |
| Domeniu de scriere | Numai cele două fișiere noi r03, prin apply_patch. Produsele r02, planul, rezultatul istoric, sursele, auditurile, registrele, contractele, site-ul, arhivele și manuscrisele existente nu au fost editate. |

Prima identificare și această verificare sunt documentare. Nu reprezintă validarea independentă a probelor de canon, un test de originalitate a unui roman sau executarea de către autor a retestului rezervat auditorului.

## Lista EXACTĂ a copiilor pentru evidence_files RES r03

ROOT: `D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000`.

Cele **șapte fișiere E01–E07** de mai jos sunt setul exact din INTRARI_REFERINTA necesar acestor aplicații: cinci copii de conținut și două indexuri de proveniență. Main trebuie să le includă explicit în spațiul de probe al RES r03, cu hashurile indicate. Existența lor în SEL, într-o dependență sau într-o arhivă nu înlocuiește includerea în RES.

| ID | Cale ROOT-relativă exactă | SHA-256 | Utilizare / localizare |
| --- | --- | --- | --- |
| E01 | [02_DOCUMENTARE/INTRARI_REFERINTA/SITE_APP.js](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/SITE_APP.js>) | `b3e62c3b0b84487a9b77da18f36b01b8b97e16cb7e92bba04976d83a0c0d4636` | SITE_APP: BOOKS L20–L24, L41–L56, L98–L115; descrieri L130–L144. Identificatori, titluri, autori afișați, colecții/saga, cadru de catalog. |
| E02 | [02_DOCUMENTARE/INTRARI_REFERINTA/CAT.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/CAT.md>) | `43dc2f09fd1ab09cda944283364cc03ed1942085f17d89f3a5a5c9d9e17025fb` | CAT: L14, L24, L42, L48, L71, L74, L86–L87. Coroborare titlu/colecție/saga; fără adoptarea scorurilor și declarațiilor de publicare. |
| E03 | [02_DOCUMENTARE/INTRARI_REFERINTA/index_origine.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/index_origine.json>) | `cc71a0c05c80ce0f8e7006baf29901c6ae17cd082bb2233fbfc90135c23c1b9f` | Index: L6–L10, L55–L60, L69–L80. Proveniența și amprentele SITE_APP, N, Z, CAT. |
| E04 | [02_DOCUMENTARE/INTRARI_REFERINTA/SUPLIMENT_r02.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/SUPLIMENT_r02.json>) | `674c647af05517635b04d2a384df21902d30956b5c4245e32d66726eccd65114` | Supliment: L13–L18. Proveniența, data capturii și amprenta HBT. |
| E05 | [02_DOCUMENTARE/INTRARI_REFERINTA/HBT.txt](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/HBT.txt>) | `1a44c0f32fa866fe1e171a013204ec17930c5cff74535ca1429cf41d151f5b31` | HBT: L1–L3, L111–L120. Statut de revision log și plan anterior Lisabona, nu canon reconciliat. |
| E06 | [02_DOCUMENTARE/INTRARI_REFERINTA/Z.zip](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/Z.zip>) | `22736278789db9e58e551013675e759ff68dff3a709d488e05e1b49cad98140c` | ZIP, membrul series-bible/01-core-premise.md: L40–L47, L76–L94. Ramă de dezvoltare fantasy/politică/prezentare, condiționată de limitele E08. |
| E07 | [02_DOCUMENTARE/INTRARI_REFERINTA/N.docx](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/INTRARI_REFERINTA/N.docx>) | `c77846fdc094d5800735ab8bdc7a1a3f62248a313f5cf2ae6e757e8baef22039` | N.docx: P1–P5, explicit P3. Titlu, saga și atribuirea internă diferită de catalog. |

Nu sunt necesare pentru aceste patru aplicații alte copii din INTRARI_REFERINTA. Nu se solicită ingestia recursivă a directorului ori a arhivelor. Pentru ZIP se include fișierul Z.zip întreg și se folosește membrul exact indicat; nu este necesară crearea unei extracții text separate.

### Probe locale de context care trebuie să fie și ele în pachetul RES

Setul complet de probe citate este **E01–E14**, nu numai cele șapte copii. Main va păstra/adăuga explicit următoarele șapte intrări de context; E09 poate rămâne în `files` ca produs r02 inclus în bundle, fără duplicarea aceleiași căi în `evidence_files`. Restul intră în `evidence_files` dacă nu sunt deja acoperite explicit de contractul RES r03. Nu am modificat contractul.

| ID | Cale ROOT-relativă exactă | SHA-256 | Utilizare / localizare |
| --- | --- | --- | --- |
| E08 | [02_DOCUMENTARE/CANON_EXISTENT.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/CANON_EXISTENT.md>) | `e5b6baada48e7d138ce841d6cc2283787984f22759c368322b269a3eb26ea4b0` | CANON_EXISTENT: L5–L7, L75–L91, L106, L171–L187, L217–L244, L260–L277. Limite G00/G01 și contradicții raportate; document citit integral. |
| E09 | [02_DOCUMENTARE/BANCA_MECANISME_EXTINSA.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/BANCA_MECANISME_EXTINSA.md>) | `355b298ad718562a37717b0deadf1413d0e1c00a77765f9d9c08e8e53d444490` | Banca r02: L34–L149 pentru surse/ID-uri; L157–L182 pentru procedură. Exact 18 mecanisme, nouă opere; fără rescriere. |
| E10 | [06_REGISTRU/MASURI/RES-001-plan-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/MASURI/RES-001-plan-r01.md>) | `9fc4922b7e8f58017f0d85f5843d23c6c8251639279be61bc521b4e877153146` | Plan: L117 și L121. Testul pe WorkID-uri reale și condițiile de închidere; starea PLANIFICAT rămâne istorică. |
| E11 | [06_REGISTRU/MASURI/RES-001-rezultate-r02.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/MASURI/RES-001-rezultate-r02.md>) | `8f48ead0e6679e0e93d1909d787caa48c1833999b2f822bd7ea91cd46888566f` | Rezultat r02: L77–L78, L137–L141. Delimitarea testului procedural și a celui real neexecutat atunci. |
| E12 | [05_AUDIT/RES-001/A-SOURCES-r02-tests.txt](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/RES-001/A-SOURCES-r02-tests.txt>) | `9b855faaca1b7db9a35d018a9d55e205cf1c7cc6643dfd792d76ffde458adf54` | Jurnal A-SOURCES: L89–L112, în special secțiunea T02b la L106. Lipsa aplicațiilor reale și a copiilor în pachetul RES r02. |
| E13 | [05_AUDIT/RES-001/A-SOURCES-r02.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/RES-001/A-SOURCES-r02.md>) | `d3f5200d2bd747e47c97facec4d532ef2f24721b8eb0a3148a4f5c6bba493e51` | Audit MD r02: L3–L5 și secțiunea Retestul constatărilor r01. Verdict și stare atribuite auditorului. |
| E14 | [05_AUDIT/RES-001/A-SOURCES-r02.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/RES-001/A-SOURCES-r02.json>) | `cb8247f4984dfae73e3232a48f06dafe6cefc032c1dd5885034589945156f6eb` | Audit JSON r02: $.audit_id, $.verdict, $.findings[0].status (F-RES-SOURCES-001), $.findings[1].status (GOV-RES-01), $.reviewed_at. |

Acestea sunt fișiere existente și incluzibile. Nu se citează un site live sau un fișier exterior ROOT drept substitut al lor. Căile originale din indexuri explică proveniența; probele efective sunt copiile enumerate. Mențiunile despre manuscrise din E08 rămân afirmații atribuite raportului, nu citări primare noi care ar pretinde o lectură neexecutată.

## Identitatea aplicațiilor și păstrarea r02

Fișier nou `02_DOCUMENTARE/r03_staging/APLICATII_WORKID_REALE.md`: **108 linii**, **21.884 octeți**, SHA-256 `75a7b1f229c9995a32f153a897bfa0a33b166fc85b4f7fecc1c5c8f1ddab2d17`.

Pentru păstrarea produselor integrate r02, amprentele de control sunt:

- `02_DOCUMENTARE/BANCA_MECANISME_EXTINSA.md`: `355b298ad718562a37717b0deadf1413d0e1c00a77765f9d9c08e8e53d444490`.
- `02_DOCUMENTARE/REPERE_SI_MECANISME.md`: `6413b6d1b2a93bc17a049538521fa9893a79788477c6a741eaa9a0273d338a01`.

Planul r01 păstrează starea PLANIFICAT; rezultatul r02 rămâne istoric. Prezentul raport nu își înscrie o amprentă circulară; Main o va calcula la depunerea versiunii efective. Hashurile identifică octeții, nu certifică autenticitatea, calitatea ori acceptarea.

## Ce rămâne pentru auditor și Main

1. Main include cele două produse r03 și toate probele enumerate în pachetul RES, cu amprente recalculate. Nu este declarată deja realizată această includere.
2. Auditorul independent verifică identificarea documentară, parcurge efectiv aplicațiile pe cele patru WorkID-uri, confruntă sursele, separarea acțiune/prezentare, limitele și condițiile T02. Decide dacă probele satisfac retestul convenit; producătorul nu declară acel test închis.
3. Identificarea, cadrul minim și propunerile exploratorii nu închid G01. Reconcilierea atribuirilor, bible/master și continuității necesită intrări și decizii separate înaintea scrierii.
4. Main va integra și reîngheța numai după arhivarea r02, conform mandatului. Nu s-au executat integrarea, arhivarea, un audit nou, metaauditul ori modificări ale registrelor.

F-RES-SOURCES-001 rămâne deschis până la decizia autorității independente. GOV-RES-01 este consemnat closed numai prin atribuirea exactă către A-SOURCES r02. Nu se acordă note și nu se proclamă canon validat, plot aprobat, proză scrisă sau succes comercial.
