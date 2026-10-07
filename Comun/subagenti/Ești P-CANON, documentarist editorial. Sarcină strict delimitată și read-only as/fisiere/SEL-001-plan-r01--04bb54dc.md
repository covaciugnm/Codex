# SEL-001 — plan de măsuri r01

Data: 24.09.2026, Europe/Bucharest. Autor de lucru: P-CANON.

**Stare a măsurilor: PLANIFICAT.** Obiect: selecția preliminară SEL-001 / G00. Audit de origine: `SEL-001-A-CANON-r01`, verdict **RETURN**, finding `SEL-001-A-CANON-F01`, severitate `major`, status de audit `open`.

Acest mandat produce numai planul de măsuri. Nu modifică `02_DOCUMENTARE/CANON_EXISTENT.md`, manuscrisul H, auditurile, schema, manifestul sau arhivele. Versiunea r01 rămâne înghețată pentru metaaudit. Editarea unei versiuni noi a documentului de selecție poate începe numai după arhivarea procesului r01 și un mandat separat explicit. G01 rămâne blocat; alegerea numelui de familie nu este autorizată.

Rădăcina tuturor căilor relative de mai jos: `D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/`.

## 1. Intrări și versiuni identificabile

JSON-ul și MD-ul A-CANON r01 au fost citite integral pentru acest plan. JSON-ul conține **un singur finding**; MD-ul dezvoltă același F01. Există deci o singură măsură editorială, cu pași de implementare și retestare, nu mai multe constatări inventate din aceeași probă. Scorurile auditorului nu sunt recalculate sau înlocuite aici; nu sunt anticipate scoruri r02.

| Intrare / probă | Identificare exactă |
| --- | --- |
| Mandatul acestui plan | `06_REGISTRU/PROMPTURI/P-CANON-plan-r01.md`; SHA-256 `3ba9ffea37f4bc3205ad5d45a42a78462cf963f072a034b0d0102a8970be4316`. Concordă cu mandatul disponibil în conversație. |
| Auditul structurat | `05_AUDIT/SEL-001/A-CANON-r01.json`; 5.434 octeți; SHA-256 `66aa22455424a2f9f361531a472829a8f3aab543f731a0306f6565875c72c1cd`. `schema_version: 1`, `audit_id: SEL-001-A-CANON-r01`, verdict `RETURN`, `findings[0].id: SEL-001-A-CANON-F01`. |
| Probele auditorului | `05_AUDIT/SEL-001/A-CANON-r01.md`; 26.582 octeți; SHA-256 `c4e491128bebc2d71838a9fae20b2aa47db6e0171a15514ba42af24324579fd6`. Secțiunile cu ancore `#proba-identitate`, `#integritate`, `#handoff`. |
| Produsul evaluat, încă înghețat | `02_DOCUMENTARE/CANON_EXISTENT.md`; 48.900 octeți; SHA-256 `0c64e4cc13bed895a0105a582afca2c85905f69cc90e3ce34774446f2e87ad72`. Acesta este și hashul declarat de audit și de obiectul SEL-001 din registrul consultat. |
| Snapshotul BEFORE_AUDIT | `08_ARHIVA/SEL-001/r01-before-audit/index.json`; SHA-256 `f75949648ddb122738b07861bb8a45f17b0210ab7358f5a12fc3dc90a0406596`, egal cu `index.sha256` citit. Copia produsului este `sources/02_DOCUMENTARE/CANON_EXISTENT.md` în acest snapshot. |
| Sursa identității, H | Original: `D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Hotelul_din_Rue_des_Ames_FINAL_v2.docx`. Copie: `08_ARHIVA/INTRARI_CANON/20260924-r01/H.docx`. SHA-256 `a9940d5776380cb40b105429f6976219440f3ea74fb8ebc1d1b4481e9da068c3`; 269.789 octeți conform indexului. Hashul copiei a fost recalculat pentru acest plan; original/copie sunt declarate identice de auditor. |
| Indexul surselor canonice | `08_ARHIVA/INTRARI_CANON/20260924-r01/index.json`; SHA-256 `cc71a0c05c80ce0f8e7006baf29901c6ae17cd082bb2233fbfc90135c23c1b9f`. Identifică H, originalul, copia și digestul. |
| Contractul r01 și dependența | Obiectul SEL-001 din `06_REGISTRU/deliverables.json` cere `A-GOVERNANCE`, `A-CANON`, dependența `SYS-001` și etapa G00. Copia istorică a registrului: `08_ARHIVA/SEL-001/r01-before-audit/sources/06_REGISTRU/deliverables.json`, digest **declarat în indexul citit** `0cc7eaba25b0c25e66856c6da228dd7be7903a27aa533f58cdb1fa74500e82cf`. Acest digest nu este atribuit registrului curent, care poate avea modificări concurente. |
| Reguli de proces | `00_CONDUCERE/PROTOCOL_ARHIVARE.md`, SHA-256 `6b609fd2136a802aceeab12c12569759a8437b193de7916efb300207763fdbe6`; `00_CONDUCERE/policy.json`, SHA-256 `c81555cebd890fccadb224a22bf5939948861a28ca01816abcf28f4a50333c41`. Citite integral. |

Amprentele intrărilor de control au fost citite/recalculate în această pregătire, cu un control la 24.09.2026, 04:22:24 +03:00; verificarea copiei H a urmat. Nu se pretinde reexecutarea în acest mandat a întregului control de 69 de intrări sau a tuturor surselor executat de auditor. Nici existența snapshotului BEFORE_AUDIT, nici hashurile lui nu dovedesc că procesul AFTER_AUDIT r01 este deja arhivat.

## 2. Măsura editorială pentru findingul unic

| Câmp | Măsură |
| --- | --- |
| ID măsură | `SEL-001-A-CANON-F01-M01` — identificator local al măsurii, nu finding nou. |
| Finding / audit / versiune | `SEL-001-A-CANON-F01` / `SEL-001-A-CANON-r01` / SEL-001 r01, hash `0c64e4cc13bed895a0105a582afca2c85905f69cc90e3ce34774446f2e87ad72`. |
| Stare | **PLANIFICAT**. Findingul rămâne `open`; verdictul r01 rămâne `RETURN`. |
| Obiectiv ratat | Separarea consecventă a faptului documentat de identitatea nereconciliată a unui protagonist central, chiar în intervalul citat de raport. |
| Localizare afectată | Produs r01: L108–L119, tabelul personajelor; L151–L164, registrul contradicțiilor; efect asupra L229–L249, recomandare/predare G01. Auditor: MD `#proba-identitate`. Localizările sunt ale r01; pentru r02 se recalculează. |
| Cauză constatabilă | Raportul asociază numele „Alexandre Boucher” cu dovada căsătoriei din H P3538–P3556, dar nu înregistrează forma „Alexandre Dubois” din același interval. H-C5 descrie alt conflict, tată/bunic; H-C8 descrie Antoine Boucher/Mercier. Aceste două înregistrări nu acoperă numele partenerului Isabellei. Omisiunea rezultă din documente; nu se inventează o cauză psihologică, un istoric al lecturii sau o intenție a producătorului. |
| Probă | H P166 și P860: „Alexandre Boucher”; H P3548 și P3550: „Alexandre Dubois”; H P3553: pronunțarea căsătoriei. Excerptele și numărătoarea apar în auditul MD identificat prin hash, `#proba-identitate`. |
| Corecție concretă viitoare | Într-o versiune nouă **a documentului de selecție**, modificați rândul personajului astfel încât să numească Alexandre și să indice explicit variantele Boucher/Dubois, cu toate cele patru localizări și statutul de nume nereconciliat. Păstrați căsătoria ca fapt documentat separat, cu P3553 și contextul P3538–P3556. Adăugați în registrul contradicțiilor un conflict distinct al numelui lui Alexandre și includeți-l nominal în predarea G01. Verificați toate formulările din selecție care ar putea prezenta Boucher drept numele definitiv; aliniați-le fără ștergerea dovezilor vreuneia dintre variante. |
| Formulare de lucru propusă | „Alexandre — nume de familie nereconciliat: Boucher în H P166/P860, Dubois în H P3548/P3550. Căsătoria cu Isabella Morgan este documentată separat prin H P3553, în contextul P3538–P3556. Alegerea formei canonice rămâne blocaj explicit G01.” Acesta este un text propus în plan, neintrodus în produs. |
| Limite ale corecției | Nu se editează manuscrisul H. Nu se înlocuiește mecanic Boucher cu Dubois sau invers. Nu se deduc rudenii cu Catherine/Guillaume Dubois, schimbare legală de nume, pseudonim, un al doilea Alexandre ori altă explicație neprobată. Nu se confundă acest conflict cu Antoine Boucher/Mercier. |
| Responsabil implementare | **P-CANON**, după mandat separat. Producătorul SEL-001 r01 este înscris în registru ca `01a0d0d7-e865-7b71-9707-be8786099512`; aceasta este o identitate consemnată, nu certificarea automată a unei alocări runtime viitoare. Dacă alocarea se schimbă, coordonatorul o înregistrează în runda nouă. |
| Responsabil proces | Coordonatorul / P-MANAGER: arhivarea r01, mandatul ulterior, înghețarea r02, manifestul noii depuneri și solicitarea auditurilor independente. P-SYSTEMS răspunde de interfața tehnică r02, separat de acest plan editorial. |
| Auditor de retest | Rol **A-CANON**, alocat independent de coordonator; al doilea rol cerut este **A-GOVERNANCE**, urmat de **A-QAMANAGER** pentru metaaudit. Identitatea A-CANON r01 din audit este `01a0d0ee-a42b-7182-af79-92a1d6a9dafb`; nu se presupune automat aceeași alocare r02. |
| Termen | După arhivarea și păstrarea verificabilă a procesului r01, inclusiv RETURN și metaauditul, **și după mandat separat de editare**; înainte de depunerea r02 și de orice scriere de roman. Nu este inventată o dată-limită calendaristică. |
| Impact | Se corectează exactitatea clasificării în SEL-001/G00 și se face vizibil blocajul de identitate în G01. Probele titlului Magenta, plicului și căsătoriei nu sunt infirmate de F01. Nu se validează prin aceasta recomandarea globală, dependența SYS-001, canonul integral, un plot, manuscrisul, traducerile sau publicarea. |
| Rezultat așteptat | Noua selecție consemnează toate variantele probate, separă căsătoria de nume și transmite conflictul concret în G01, cu trasabilitate către F01 și r01. Nu se anticipează acceptarea ori scorul auditorilor. |
| Dovadă realizată / rezultat actual | **Nicio remediere implementată; niciun test de închidere executat sau declarat trecut.** Există acest plan și probele auditorului. Viitorul diff, noul hash, reauditurile și metaauditul nu există ca rezultate ale prezentului mandat. |

## 3. Teste de închidere propuse — toate PLANIFICAT

| Test | Procedură și criteriu observabil de închidere | Responsabil / dovadă viitoare |
| --- | --- | --- |
| F01-T1 — reproducerea probei | Verificați hashul H de referință. Reextrageți `word/document.xml`, cu namespace `w`, selecția `//w:body//w:p`, concatenarea `.//w:t` și eliminarea paragrafelor fără text; numerotare de la 1. Confirmați Boucher la P166/P860 și Dubois la P3548/P3550. Citiți contextual P3538–P3556 și P3553 pentru căsătorie. Diferența de hash sau numerotare se raportează; nu se ajustează proba ca să coincidă artificial. | P-CANON pentru documentarea implementării; A-CANON reproduce independent. Dovadă: rezultat real cu hashul sursei, metoda, paragrafele, data și executantul. Stare **PLANIFICAT**. |
| F01-T2 — corecția coerentă | În produsul nou, ambele nume și cele patru localizări apar explicit ca variante nereconciliate. Căsătoria este separată de problema numelui. Tabelul personajelor, registrul contradicțiilor și predarea G01 consemnează același conflict. O înlocuire simplă a numelui sau o explicație inventată determină neînchiderea. | P-CANON; verificare independentă A-CANON. Dovadă: localizări recalculate în versiunea nouă și diff față de produsul r01 arhivat. Stare **PLANIFICAT**. |
| F01-T3 — limitele corecției | Recontrolați că H și produsul r01 arhivat au hashurile anterioare; examinați diff-ul selecției. Nicio schimbare de manuscris, alegere arbitrară Boucher/Dubois, promovare a G01 sau rescriere a RETURN r01. | Coordonator și A-GOVERNANCE, cu verificarea de conținut A-CANON. Dovadă: comparații reale de hash și diff; nu declarația producătorului. Stare **PLANIFICAT**. |
| F01-T4 — noua depunere și retestarea independentă | După înghețarea r02, verificați inventarul, hashurile produsului, contractului, dependențelor și probelor, versiunea de schemă aplicabilă și independența alocărilor. Obțineți rapoarte r02 reale A-CANON/A-GOVERNANCE și metaauditul exact al acelei runde. Închiderea F01 se bazează pe retestul independent, nu pe acest plan; acceptarea globală rămâne supusă tuturor condițiilor și dependențelor. | Coordonator, P-SYSTEMS pentru instrumente, auditorii desemnați și A-QAMANAGER. Dovadă: noua depunere, audituri/metaaudit/validare și arhivarea lor, toate legate de versiunile exacte. Stare **PLANIFICAT**. |

## 4. Dependențe de proces pentru compatibilitatea r02

Această secțiune preia cerințele explicite ale utilizatorului adresate P-SYSTEMS și cerința de trasabilitate din auditul A-CANON. **Nu reprezintă findings suplimentare atribuite A-CANON și nu implementează schema SYS-001.** Planul SYS-001 și probele auditorului de sisteme trebuie tratate de responsabilul respectiv. Prezentul plan nu pretinde că a verificat toate acele probe și nu acceptă schema tehnică în locul auditorilor.

| Dependență pentru noua depunere | Cerință și probă de verificare viitoare | Responsabil / stare |
| --- | --- | --- |
| Contract/dependențe/probe legate de hashuri | Contractul r02 trebuie să fie identificabil prin hash și să păstreze rolurile, criteriile, politica și dependența SYS-001 aferente exact acelei depuneri. Referințele probelor trebuie să lege sursa identificată prin hash de localizarea reală, nu numai de o cale schimbabilă. Se verifică și versiunea exactă și rezultatul aplicabil al dependenței; simplul ID SYS-001 nu dovedește acceptarea. Hashurile r02 se calculează după existența și înghețarea fișierelor, nu se inventează acum. | P-SYSTEMS și coordonator; verificare A-GOVERNANCE/A-QAMANAGER. **PLANIFICAT**. |
| Păstrarea RETURN/HASH și a manifestului istoric | Se arhivează r01, JSON și MD, metaauditul și rezultatele reale de validare, inclusiv RETURN și orice rezultat HASH existent sau viitor. Se păstrează manifestul evaluat și digestul așteptat împreună cu digestul observat în caz de diferență. Nu se „repară” manifestul r01 pentru a face o respingere să dispară. R02 are o depunere nouă, cu legătură explicită la r01. **Pentru A-CANON r01 este documentat RETURN; acest plan nu atribuie un verdict HASH neconsemnat acelui audit.** | Coordonator/P-SYSTEMS; control independent A-QAMANAGER. **PLANIFICAT**. |
| Detectarea Setext | Instrumentele viitoare trebuie să detecteze titlurile Markdown Setext, inclusiv sublinierile `===` și `---`, cu probe și teste conforme cazurilor auditorului de sisteme; nu numai titluri care încep cu `#`. Se disting titlurile reale de separatoare și de textul din blocuri de cod. Acesta este un criteriu de interfață cerut de utilizator, nu rezultatul unui test executat aici. | P-SYSTEMS; verificare A-SYSTEMS. **PLANIFICAT**. |
| Rapoarte reale r02 și schema declarată | A-CANON r01 are `schema_version: 1` și trebuie păstrat ca document istoric exact. Existența sa nu autorizează acceptarea implicită a v1 pentru r02. Schema nouă trebuie declarată și validată explicit; compatibilitatea/migrarea, dacă există, trebuie documentată, fără rescrierea auditului istoric. Se testează integrarea cu rapoarte r02 emise efectiv de auditori, fără note precompletate, verdicturi convertite sau simple fixture-uri prezentate drept audituri reale. Un raport vechi incompatibil nu primește acceptare tacită. | P-SYSTEMS, coordonator și auditori pentru propriile rapoarte; metaaudit A-QAMANAGER. **PLANIFICAT**. |

Acceptarea acestui plan, eventuala corectare a F01 sau un rezultat tehnic bun nu închid automat G01. Lectura integrală și reconcilierea canonului rămân lucrări ulterioare, iar alegerea dintre Boucher și Dubois rămâne nerezolvată.

## 5. Ordine și închidere a mandatului de planificare

1. Coordonatorul finalizează metaauditul r01 pe versiunea înghețată și păstrează întregul rezultat al rundei într-o arhivă nouă verificată, inclusiv RETURN, fără suprascrierea r01-before-audit. **PLANIFICAT în acest plan; execuția altui agent nu este presupusă.**
2. După arhivare, se primește un **mandat separat de editare**. Fără el, P-CANON nu execută M01 și nu actualizează manifestul. **PLANIFICAT.**
3. Se implementează M01 numai în noua versiune a selecției, se execută verificările de autor și se depune r02 în condițiile tehnice explicit stabilite. **PLANIFICAT.**
4. Auditorii independenți și metaauditorul evaluează runda nouă; rezultatele reale și eventualele noi RETURN se păstrează. **PLANIFICAT.**

Sunt acoperite **1/1 findings din A-CANON-r01.json**, prin măsura `SEL-001-A-CANON-F01-M01`. Aceasta este o verificare a corespondenței planului cu lista primită, nu un scor, un audit de acceptare sau închiderea findingului.

La predarea acestui fișier, produsul r01 trebuie să rămână la SHA-256 `0c64e4cc13bed895a0105a582afca2c85905f69cc90e3ce34774446f2e87ad72`. Nu se înregistrează acest plan în lista `files` a manifestului istoric pentru a-i schimba retrospectiv obiectul. Indexarea/arhivarea planului ca document ulterior aparține coordonatorului și trebuie să păstreze această proveniență.

Mandatul separat de recuperare a mesajelor observabile permite numai un supliment în `06_REGISTRU/ISTORIC/P-CANON-mesaje-observabile-r01.md`; nu constituie autorizație de editare SEL-001 sau de schimbare a arhivelor vechi. Predarea planului este completă ca planificare; implementarea și testele de închidere rămân **PLANIFICAT**.
