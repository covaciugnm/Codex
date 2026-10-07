# Protocol de arhivare, audit și remediere
## Principiul obligatoriu
Tot procesul de lucru observabil se păstrează: cerințe și instrucțiuni, versiuni ale planurilor și textelor, surse și trimiteri, mandate de agenți, mesaje finale, rapoarte de audit, respingeri, planuri de măsuri, rezultate de test/retest și decizii. Nu se salvează raționamente interne ascunse ale modelelor, parole, tokenuri sau date personale fără necesitate.

## Structura locală
00_CONDUCERE — mandat, roadmap, politică, status și decizii.
01_ECHIPA — fișe de post pentru toate rolurile.
02_DOCUMENTARE — cercetare, canon preliminar și surse.
03_MODELE — formulare pentru livrabile, audit, remediere și predare.
04_INSTRUMENTE — verificare automată, arhivare și teste.
05_AUDIT — rapoarte reale, niciodată precompletate cu note de trecere.
06_REGISTRU — agenți reali, livrabile, rubrici, rulări și indexuri.
07_ROMANE — câte un dosar separat per WorkID, cu subfolderele etapelor.
08_ARHIVA — depuneri/snapshot-uri separate pentru fiecare rundă.
09_ELIBERARE_LOCALA — numai pachete finale aprobate; fără sincronizare automată cu site-ul.

## Identificare
Exemple: ROM-001-G05-v001 pentru plan; ROM-001-C07-EN-v003 pentru proză; AUD-ROM-001-C07-EN-v003-A-EN-r02 pentru audit. Un ID de versiune nu se reutilizează pentru alt conținut. ID-urile agenților sunt cele întoarse de instrumentul de execuție, nu nume inventate. Aliasul uman ajută orientarea, nu dovedește identitatea.

Datele includ fus orar sau UTC. O rundă primește un ID unic, de exemplu 20260924T010000Z-r01. Arhivatorul refuză suprascrierea unei runde existente. Registrele curente sunt indexuri de lucru; snapshot-urile lor păstrează situația exactă la fiecare depunere.

## Flux la fiecare depunere
1. Autorul închide versiunea, inventariază toate fișierele și produce checksum-urile.
2. Managerul arhivează snapshot-ul BEFORE_AUDIT, cu mandatul, intrările și manifestul.
3. Doi auditori diferiți citesc exact versiunea depusă și produc rapoarte separate, cu surse/localizări, criterii, scoruri și constatări.
4. Managerul QA face metaauditul: identități, independență, acoperire, probe, calcul și verdict; orice raport invalid se returnează auditorului, nu se cosmetizează.
5. Validatorul recalculează hash-urile, condițiile, dependențele și pragurile; rezultatul său se salvează chiar când este respins.
6. Se arhivează snapshot-ul AFTER_AUDIT cu rapoartele, metaauditul și rezultatul verificării.
7. Dacă este retur, se deschide un plan de măsuri cu ID-uri legate de constatări; se produce versiune nouă și se reia fluxul. Dacă trece, se arhivează decizia ACCEPTAT și abia apoi se autorizează etapa următoare.

## Planul de măsuri
Fiecare constatare are: ID, livrabil/versiune, auditor, localizare, severitate, obiectiv ratat, probă, cauză, acțiune, responsabil, termen, rezultat așteptat, test de închidere, dovadă realizată și auditor care reverifică. „Corectat” spus de autor nu închide problema. Închiderea cere un retest pe versiunea nouă.

Se păstrează și măsurile respinse, încercările nereușite și motivele. Dacă se schimbă agentul, noul agent primește mandatul și dosarul de erori, nu începe de la o variantă cosmetizată a istoriei.

## Rapoarte și rezultate
Un raport care a spus RETURN rămâne RETURN în arhivă. Reauditul este alt raport, nu editarea notei vechi. Planul poate avea o vedere curentă, dar fiecare stare depusă se arhivează separat. Rezultatele automate indică testele executate, data, comanda/procedura, fișierele și rezultatul real; fixture-urile sintetice sunt marcate TEST.

Mesajele agenților care spun „gata” nu substituie existența fișierului și auditul său. Se salvează dovada locală și se verifică înainte de raportare. Nu se trece automat de la „planificat” la „publicat”.

## Integritate și recuperare
Amprentele detectează schimbarea raportată la snapshot și permit verificarea copiei. Nu sunt semnătură digitală a unui terț și nu transformă discul într-o arhivă WORM. Cine controlează tot discul poate altera și fișierele, și indexurile; această limită se comunică explicit.

Se recomandă o copie de siguranță versionată pe un suport separat după fiecare etapă acceptată și înainte de transfer. Configurarea ei, destinația și eventualele costuri se aprobă separat; în acest proiect nu se presupune că există deja backup extern. Se testează recuperarea unei runde într-un director temporar, fără suprascrierea atelierului.

## Retenție și eliberare
Nu se șterg surse, rapoarte de respingere sau versiuni pentru a „curăța” scorurile. Eventuala politică de retenție se decide explicit, ținând cont de drepturi și confidențialitate. Pentru publicare se păstrează dosarul complet local; către site pleacă numai pachetul final necesar livrării, nu toate rapoartele interne.

## Supliment r02 — Contract, probe și conservarea eșecurilor
Auditul fixează nu numai fișierele produsului, ci și contractul de intrare și versiunile dependențelor. Fiecare sursă locală folosită ca dovadă este declarată cu hash și inclusă în captura verificabilă. Schimbarea unui master EN sau a unei probe impune reevaluarea raportului dependent; aprobarea separată a noii surse nu este suficientă.

Schema exactă și modul de conservare a eșecurilor sunt documentate în 04_INSTRUMENTE/README.md. O rundă RETURN cauzată de hashuri neconforme trebuie păstrată prin calea explicită de conservare a eșecului: manifestul declarat, bytes disponibili și hashurile observate, lipsurile, rapoartele și rezultatul original. Manifestul vechi nu este «reparat» pentru a pretinde că descria acei octeți. Captura eșecului nu acordă aprobare și nu se confundă cu un snapshot coerent acceptat. Se păstrează refuzul de suprascriere și se verifică indexul.

## Supliment r02 — Istoric recuperat și captură preventivă
Dosarul 06_REGISTRU/ISTORIC/RECONCILIERE_ISTORIC_r02.md identifică mandatele, clarificările, predările, rapoartele și limitele recuperării inițiale. Primele runde nu sunt rescrise pentru a pretinde că aveau mesaje salvate ulterior. Materialul recuperat primește o captură suplimentară cu ID nou, dată și hash. Rezumatele rămân explicit rezumate. Nu se inventează ore, mesaje, aprobări sau ieșiri de instrument indisponibile.

În sesiunile viitoare, mandatul integral se salvează înainte de delegare; răspunsul final exact imediat la primire; documentele, constatările, măsurile și rezultatele în fiecare rundă. Coordonatorul verifică inventarul complet înainte de arhivare. Recipisa de creare a arhivei apare după captură și se păstrează separat pentru următoarea rundă; indexul nu se autohashează. O lacună materială deschide constatare și blochează acceptarea, nu este ascunsă sub eticheta «totul salvat».

## Regula r03 — probe din arhive anterioare

Nu declarați căi din 08_ARHIVA în evidence_files sau supplemental_evidence_files ale rapoartelor curente: arhivatorul interzice ingestia arhivelor vechi. Pentru verificarea unui index anterior folosiți o copie plată, byte-identică, păstrată în afara 08_ARHIVA, cu proveniență și SHA-256; declarați copia în contract sau în propriul supliment. Menționarea unei arhive în text nu o transformă în probă arhivabilă.

Rapoartele r02 originale care au provocat OBS-MANAGER-002 rămân păstrate; revizia de ambalare v02 folosește copii plate fără schimbarea concluziilor semantice. Într-o rundă nouă se verifică atât validarea porții, cât și arhivarea și recuperarea efectivă înaintea autorizării etapei următoare.
