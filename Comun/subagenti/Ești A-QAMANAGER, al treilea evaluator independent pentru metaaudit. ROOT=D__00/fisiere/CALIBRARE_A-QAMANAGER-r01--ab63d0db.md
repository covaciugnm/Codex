# Calibrare A-QAMANAGER — r01 — TEST

Statut: READY pentru un mandat nou. Fără aprobări de livrabil.

ROOT: `D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000`
Momentul inventarului: `2026-09-24T04:08:37.8724015+03:00`.
Evaluator: `A-QAMANAGER`; ID de execuție `01a0d0f3-8249-7d91-95f4-ef806130bebe`, citit din `CODEX_THREAD_ID` și regăsit în registrul inspectat.

Acest document consemnează pregătirea și șase cazuri sintetice marcate TEST. Nu este audit primar, metaaudit al unor rapoarte reale, lectură de roman sau aprobare editorială. Valorile și identificatorii simbolici din cazurile TEST nu sunt atribuiți niciunui roman, autor sau auditor real.

## 1. Ce am inspectat

Am citit integral cele șapte fișiere cerute, în UTF-8. Am calculat SHA-256 pentru octeții lor curenți, numai pentru identificarea materialelor de pregătire. Inventarul de mai jos nu reprezintă verificarea întregului bundle SYS-001.

| Fișier relativ la ROOT | Linii citite | SHA-256 observat |
| --- | ---: | --- |
| `00_CONDUCERE/MANUAL_ATELIER.md` | 90 | `292bd3c8946f9f423bf78ca68b72ed218ceda800376a4da3484b7f4a6fde130d` |
| `00_CONDUCERE/RUBRICI.md` | 222 | `10bc35a69450e7143a7d84354cbf4107da2fcb9e68f4eec195ba2e6942d06edd` |
| `00_CONDUCERE/PROTOCOL_ARHIVARE.md` | 48 | `6b609fd2136a802aceeab12c12569759a8437b193de7916efb300207763fdbe6` |
| `00_CONDUCERE/policy.json` | 8 | `c81555cebd890fccadb224a22bf5939948861a28ca01816abcf28f4a50333c41` |
| `06_REGISTRU/agents.json` | 55 | `7bdc7aff5dbdddfe76dfc47722655e42c05a9e03391dd72b23deed5ff243d446` |
| `06_REGISTRU/deliverables.json` | 382 | `0cc7eaba25b0c25e66856c6da228dd7be7903a27aa533f58cdb1fa74500e82cf` |
| `04_INSTRUMENTE/README.md` | 216 | `d0426ea6fe4ce159370ca06128190b53253d571d5bc8f5f4d12f344f81278a9a` |

Am verificat existența instrucțiunilor `AGENTS.md` în ROOT, în directorul de destinație și în directoarele părinte până la rădăcina D:; nu am găsit asemenea fișiere în aceste poziții. Fișierul de calibrare cerut nu exista înainte de redactare.

Politica citită fixează `threshold_exclusive: 950`, `score_scale: 1000`, minimum doi auditori independenți, toate criteriile peste prag și `require_meta_audit: true`. Nu există derogare prin medie sau prin decizia managerului.

Registrul citit conține patru producători și cinci auditori autorizați, inclusiv A-QAMANAGER. ID-ul acestei execuții corespunde înregistrării A-QAMANAGER cu `kind: auditor` și `active: true`; este diferit de celelalte opt ID-uri inspectate. Aceasta verifică o corespondență locală de identitate și rol, fără a certifica proveniența rapoartelor viitoare. Conform README, `active` reprezintă autorizare în registru, nu dovada că o execuție rulează.

În copia citită a `deliverables.json`, SYS-001, SEL-001 și RES-001 sunt la G00, cu `status: DEPUS-r01`, liste `audits: []` și fără câmp `meta_audit`. SEL-001 și RES-001 depind de SYS-001. Acestea sunt observații asupra registrului la momentul citirii; nu stabilesc dacă auditorii au între timp fișiere în lucru ori rapoarte neînscrise. Nu am căutat și nu am evaluat rapoartele lor.

## 2. Metoda calibrării TEST

Am aplicat regulile citite celor șase defecte cunoscute și am executat verificări minimale în memoria unei sesiuni PowerShell. Pragul a fost citit din politica reală; celelalte intrări ale cazurilor au fost sintetice. Hash-urile TEST au fost calculate efectiv din două șiruri UTF-8. Sursa TEST pentru localizare a fost o listă de trei linii în memorie.

Aceste verificări compară predicatele relevante pentru fiecare defect. Nu sunt rapoarte JSON complete, teste ale implementării gatekeeper sau o suită independentă de certificare. Identificatorul `TEST-AUTOR-1` este un simbol de exercițiu, nu un UUID înregistrat. Calea `TEST/sursa.md` desemnează exclusiv sursa virtuală a exercițiului; nu a fost creată pe disc.

Rezultatul efectiv al verificărilor în memorie: șase semnale de defect detectate din șase cazuri; sesiunea s-a încheiat fără eroare. Pentru fiecare caz, controlul indicat mai jos ar trebui să fie `false` într-o evaluare a acelei situații. Celelalte controale nu primesc implicit `true`.

### TEST-01 — Scor exact 950

Intrare sintetică: un raport pretinde `PASS`, iar un criteriu are scorul întreg `950`.

Semnale: comparația obligatorie `950 > 950` este falsă. 950 corespunde exact lui 9,50/10; pragul minim admis pentru un criteriu este 951. O medie peste prag, rotunjirea sau scorul altui auditor nu repară criteriul neeligibil.

Control afectat: `scoring = false`. Verdict obligatoriu în acest TEST: raportul cu PASS este invalid pentru acceptare; retur procedural, poarta rămâne închisă. Un raport care ar consemna corect RETURN la 950 nu ar fi invalid doar pentru nota mică.

Remediere obligatorie: constatare motivată și reevaluare justificată după remedierea demonstrată a problemei, dacă există. Nu se majorează scorul pentru a obține trecerea și nu se modifică raportul istoric.

Temei: `00_CONDUCERE/policy.json`, câmpul `threshold_exclusive`; `00_CONDUCERE/RUBRICI.md:L3-L5`; `00_CONDUCERE/MANUAL_ATELIER.md:L17-L20`.

### TEST-02 — Același ID pentru autor și auditor

Intrare sintetică: `author = TEST-AUTOR-1` și `reviewer = TEST-AUTOR-1`.

Semnale: egalitate exactă între identificatorul producătorului și cel al evaluatorului. Două etichete de rol, două rapoarte sau două nume afișate nu creează independență. Într-un raport real se compară UUID-urile și autorizarea din registru, nu doar denumirile rolurilor.

Control afectat: `independence = false`. Verdict obligatoriu în acest TEST: autoaudit invalid; raportul nu poate fi numărat între auditurile independente, iar poarta rămâne închisă.

Remediere obligatorie: un auditor distinct și autorizat verifică efectiv versiunea exactă și produce propriul raport. Schimbarea cosmetică a ID-ului într-un raport existent nu este remediere. A-QAMANAGER trebuie, la rândul său, să aibă ID diferit de orice producător și de auditorii livrabilului.

Temei: `00_CONDUCERE/MANUAL_ATELIER.md:L17-L20`; `04_INSTRUMENTE/README.md:L77` și `04_INSTRUMENTE/README.md:L122`.

### TEST-03 — Hash de versiune veche

Intrări sintetice, fără newline final:

- Octeți vechi: șirul UTF-8 `TEST versiune r01`; SHA-256 calculat: `4587b046343d3870bff514d7944f27990dd42ab3378ca48f4ab66e25eb1eb35a`.
- Octeți curenți: șirul UTF-8 `TEST versiune r02`; SHA-256 calculat: `6207e025831269058d753ba56fb498a760c954838ffc5de66e07a586f1df6158`.
- Raportul TEST pretinde că verifică versiunea curentă, dar păstrează prima amprentă.

Semnale: amprentele sunt diferite; un nume identic de fișier, un ID de versiune sau un PASS anterior nu stabilesc identitatea octeților. La metaaudit există două legături de verificat: artefactele față de manifest și audituri, apoi rapoartele JSON exacte față de `audit_files`.

Control afectat: `version = false`. Verdict obligatoriu în acest TEST: raportul este neaplicabil versiunii curente; retur procedural și poartă închisă. Un fișier acceptat anterior, dar modificat, devine NEVALIDAT conform manualului; se reevaluează și dependențele afectate.

Remediere obligatorie: verificarea efectivă a versiunii curente, raport nou și metaaudit al rapoartelor actuale. Nu se înlocuiește numai hash-ul fără recitire și reverificare; chiar reformatarea JSON schimbă octeții raportului. Versiunea istorică se păstrează.

Temei: `00_CONDUCERE/MANUAL_ATELIER.md:L22-L27`; `04_INSTRUMENTE/README.md:L76` și `04_INSTRUMENTE/README.md:L122`.

### TEST-04 — Constatare deschisă împreună cu PASS

Intrare sintetică: `verdict = PASS`, cu o constatare având `status = open`.

Semnale: verdictul de trecere contrazice existența constatării deschise, indiferent de severitate. Pentru auditul primar, README admite formal numai `closed` sau `resolved`, fără diferențiere de majuscule; declarația autorului că a corectat problema nu este dovadă de închidere.

Control afectat: `closure = false`. Verdict obligatoriu în acest TEST: PASS invalid, retur procedural și poartă închisă.

Remediere obligatorie: plan de măsuri legat de constatare, corecție trasabilă și retest documentat pe versiunea nouă, reverificat de auditor. Simplul schimb al etichetei în `closed` nu probează remedierea. Pentru un metaraport acceptabil, `findings` trebuie să fie lista goală; nu se șterg constatările reale pentru a satisface schema.

Temei: `00_CONDUCERE/RUBRICI.md:L3`; `00_CONDUCERE/PROTOCOL_ARHIVARE.md:L31-L34`; `04_INSTRUMENTE/README.md:L45` și `04_INSTRUMENTE/README.md:L124`.

### TEST-05 — Citare cu localizare inexistentă

Intrare sintetică: sursa virtuală `TEST/sursa.md` are exact trei linii: `# TEST`, `L2: probă sintetică.`, `L3: sfârșit TEST.`. Raportul o citează prin `TEST/sursa.md:L99-L100`.

Semnale: sursa există în colecția virtuală TEST, dar liniile 99–100 depășesc cele trei linii disponibile. Existența fișierului și sintaxa corectă a referinței nu dovedesc existența pasajului. Analog, o ancoră absentă sau un citat care nu apare la localizarea indicată nu poate susține concluzia.

Control afectat: `evidence = false`; justificarea scorurilor dependente ar necesita și reexaminarea `scoring`. Verdict obligatoriu în acest TEST: raport invalid din cauza probei nelocalizabile; retur procedural și poartă închisă, chiar dacă verificarea automată a formei referinței nu semnalează eroarea.

Remediere obligatorie: deschiderea sursei și versiunii exacte, verificarea existenței localizării, a citatului și a contextului; apoi refacerea concluziei și justificării prin dovezi reale. Nu se inventează o localizare înlocuitoare.

Temei: `00_CONDUCERE/MANUAL_ATELIER.md:L67-L70`; `04_INSTRUMENTE/README.md:L79`, care declară explicit că engine-ul nu certifică ancora, numărul liniilor sau adevărul afirmației.

### TEST-06 — Selecție preliminară prezentată ca lectură integrală

Intrare sintetică: evidența de acoperire declară `preliminary_selection`, iar raportul pretinde `integral` și folosește această pretenție pentru a susține încheierea lecturii relevante pentru G01.

Semnale: aria efectivă a examinării nu susține aria concluziei. O selecție, un eșantion sau un rezumat nu demonstrează lectură integrală. SEL-001 este anexă preliminară G00; chiar acceptarea ei nu înlocuiește verificările G01 și nu aprobă canonul integral ori romanul.

Control afectat: `coverage = false`; afirmația nesusținută afectează și `evidence`, iar punctajele bazate pe ea trebuie reexaminate. Verdict obligatoriu în acest TEST: raportul care pretinde lectura integrală este invalid; retur procedural și nicio trecere la G01 pe baza acestei pretenții.

Remediere obligatorie: restrângerea explicită a raportului la selecția examinată și la limitele ei. Pentru o concluzie de lectură integrală este necesară lectura efectivă a întregului corpus relevant și trasabilitatea acoperirii, într-un mandat separat. Nu se completează retroactiv o lectură fictivă.

Temei: `00_CONDUCERE/RUBRICI.md:L7`, secțiunile `SEL-001` de la linia 19 și `G01` de la linia 39; `00_CONDUCERE/MANUAL_ATELIER.md`, secțiunile 4 și 11.

## 3. Condiții pentru mandatul viitor de metaaudit real

Acest tabel este o listă de verificări de aplicat ulterior. Nu conține rezultate acordate unor rapoarte reale.

| Check obligatoriu | Verificare și dovezi necesare la mandatul real |
| --- | --- |
| `independence` | Identitățile reale, autorizarea și rolurile din registru; minimum doi auditori primari distincți, separați de producători. A-QAMANAGER are alt UUID decât producătorii și auditorii livrabilului. Concordanța locală observată acum se reverifică pe datele mandatului real. |
| `coverage` | Fiecare raport acoperă exact fișierele, criteriile și ponderile manifestului; se verifică și acoperirea efectivă a lecturii față de concluziile declarate, inclusiv limita G00/G01. |
| `evidence` | Referințe reale pentru fiecare criteriu și control; fișier, versiune, localizare și conținut deschise și verificate. Faptele sunt separate de opinii și de limitele examinării. |
| `scoring` | Numai întregi 0–1000, fiecare criteriu strict peste 950 la fiecare auditor; ponderi pozitive cu sumă exactă 100 și calcul ponderat reverificat. Se verifică justificarea editorială, nu numai calculul. Nicio notă literară nouă din partea metaauditorului. |
| `closure` | Nicio constatare primară deschisă; închideri susținute de măsuri și retest efectiv, pe versiunea relevantă. Metaraportul de trecere cere `findings: []`. |
| `version` | Corespondență exactă între fișiere, SHA-256 curente, manifest și fiecare audit; `audit_files` acoperă exact rapoartele primare cu hash-urile octeților lor actuali. Modificările și dependențele afectate se reverifică. |

Pentru acceptare, toate cele șase controale trebuie să existe o singură dată și să aibă literal boolean `true`, fiecare cu dovezi verificate; orice control suplimentar admis trebuie să îndeplinească aceleași condiții. Un control fals, lipsa unui raport sau un checksum depășit blochează poarta. Nu se emit rezultate favorabile pentru a umple schema.

Raportul invalid se returnează auditorului responsabil; A-QAMANAGER nu redactează în locul acestuia remedierea și nu rescrie verdictul istoric. Reauditul produce alt raport. Arhivarea și validarea sunt operații distincte, executabile numai în limitele mandatului aplicabil.

Temei: `00_CONDUCERE/RUBRICI.md:L219-L221`; `00_CONDUCERE/PROTOCOL_ARHIVARE.md:L22-L29` și `00_CONDUCERE/PROTOCOL_ARHIVARE.md:L36-L39`; `04_INSTRUMENTE/README.md:L106-L124`.

## 4. Limitări și închiderea pregătirii

- Am examinat documentele de procedură și registrele enumerate, nu romane, traduceri, dosare de canon, banca de repere, rapoarte primare sau întregul bundle SYS-001.
- Nu am emis note editoriale, audituri primare, metaraport JSON, PASS pentru livrabile sau modificări de statut. Cele șase rezultate sunt exclusiv recunoașteri ale unor defecte TEST cunoscute.
- Nu am inspectat implementarea gatekeeper și nu am rulat validatorul, arhivatorul ori suita de teste. Cele 151 de teste menționate în README sunt un rezultat raportat de acel document, nereprodus aici.
- Exercițiul în memorie nu dovedește robustețe pe rapoarte arbitrare, calitatea romanelor sau adevărul unor probe reale. Controalele semantice pentru citări și lectura integrală rămân necesare la mandatul real.
- Registrele și fișierele pot fi actualizate de ceilalți participanți după citire. Hash-urile de mai sus identifică observația locală; nu constituie snapshot atomic, semnătură digitală, timestamp certificat ori garanție împotriva falsificării de către un operator cu acces integral.
- Nu am creat agenți, nu am trimis mesaje auditorilor și nu am creat arhive sau fișiere TEST pe disc. Singura scriere autorizată în această rundă este `05_AUDIT/CALIBRARE_A-QAMANAGER-r01.md`; documentele și registrele inspectate nu au fost editate de mine.
- Rapoartele reale vor fi examinate numai după un mandat nou, pe identitățile, versiunile și dovezile disponibile atunci. Pregătirea de acum nu autorizează automat metaauditul sau deschiderea vreunei porți.

READY — calibrarea celor șase cazuri TEST este consemnată; aștept un mandat nou pentru rapoartele reale.

