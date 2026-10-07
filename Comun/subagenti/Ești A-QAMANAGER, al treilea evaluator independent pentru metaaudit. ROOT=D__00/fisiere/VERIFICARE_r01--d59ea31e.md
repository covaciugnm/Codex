# ROM-001 — verificare nominală a calibrării editoriale r01

Evaluator: A-QAMANAGER — `01a0d0f3-8249-7d91-95f4-ef806130bebe`. Data verificării: `2026-09-24T08:26:16+03:00`.
Bază de autoritate: calificarea nominală r02 deja existentă, reutilizată conform mandatului; fără recalibrare proprie.

## Rezultat și întindere

A-GENRE, A-ORIGINALITY, A-STRUCTURE și A-EN: CALIFICAT, fiecare 11/11 (9 comune + 2 specializate). Total: 44/44 verdicturi, motive semantice și localizări valide. Nicio constatare de remediat; niciun exercițiu RETURN.

Acesta este controlul nominal al setului TEST deschis `rom001-r01`, nu test orb, audit G00, metaaudit G01 sau acceptare G02. Nu există contract de produs pentru această verificare; JSON-ul însoțitor folosește un format propriu de calificare. Nu s-a emis nicio notă productivă.

Regula aplicată: calificarea cere identitate/rol/independență concordante și toate cele 11 cazuri corecte, motivate și localizate efectiv. Un verdict greșit ori o probă invalidă ar întoarce exercițiul, nu cheia. `qualified:true` și numărătorile declarate au fost confruntate cu rezultatele calculate, nu folosite drept temei.

## Identități și închiderea execuțiilor

| Rol | ID nominal verificat | Răspuns final declarat la | Rezultat |
| --- | --- | --- | --- |
| A-GENRE | `01a0d1d0-67b7-7ea2-9e31-562bc344aaa7` | `2026-09-24T08:09:45.3115206+03:00` | CALIFICAT — 11/11 |
| A-ORIGINALITY | `01a0d1d0-690e-7871-b245-6817b004172f` | `2026-09-24T08:09:01+03:00` | CALIFICAT — 11/11 |
| A-STRUCTURE | `01a0d1d0-6cb7-7681-8010-b13b8b640dad` | `2026-09-24T08:09:54.8627055+03:00` | CALIFICAT — 11/11 |
| A-EN | `01a0d1d0-6f17-7c52-a5f8-a3c3178c2cb8` | `2026-09-24T08:09:01.5282651+03:00` | CALIFICAT — 11/11 |

Fotografia stabilă I03 păstrează cele 14 ID-uri distincte de la începutul controlului, dintre care cinci producători. Cele patru ID-uri de mai sus sunt UUID-uri valide, distincte între ele, de QA și de toți cei cinci producători. Rolul, `kind:auditor` și autorizarea concordă cu răspunsurile, mandatele și predările nominale. QA este înregistrat separat ca A-QAMANAGER/auditor, nu ca producător.

| Rol | Răspuns și fișă | Mandat | Predare | Închidere |
| --- | --- | --- | --- | --- |
| A-GENRE | I06; I07 | I08 | I09 | I10 |
| A-ORIGINALITY | I11; I12 | I13 | I14 | I15 |
| A-STRUCTURE | I16; I17 | I18 | I19 | I20 |
| A-EN | I21; I22 | I23 | I24 | I25 |

Pentru fiecare rol, `agent_id`, `role` și calea răspunsului din predare concordă; textul `previous_status.completed` din închidere este identic cu `message` din predare. Închiderea nu conține separat un câmp agent_id sau un timestamp certificat: atribuirea folosește numele nominal al fișierului și concordanța exactă cu predarea. `active:true` în registru exprimă autorizarea, nu faptul că execuția rulează. Nu pretind autentificare externă a infrastructurii.

## Stabilizarea contextului de registru

La controlul final inițial, hashul registrului live nu mai corespundea celui citit la început. Nu am tratat această divergență drept verificare reușită și nu am calificat noile roluri. La indicația managerului, am citit integral fotografia I03 și proveniența I26, create înaintea adăugării lotului B.

SHA-256 efectiv al fotografiei I03 este `85c2932b751598375a73e38a8732da602bfe6c894476c6d69497d019f6824806`: egal cu hashul registrului măsurat la început și cu cel declarat în I26. Aceasta confirmă identitatea de bytes cu contextul inițial prin SHA-256. Calea sursă, calea copiei și data declarată `2026-09-24T08:25:30.3363657+03:00` concordă în proveniență; data este metadată a managerului, nu o certificare externă.

La `2026-09-24T08:26:16+03:00`, registrul live avea 18 înregistrări, iar primele 14 coincideau integral cu fotografia. Pentru fiecare dintre cele patru ID-uri evaluate am reverificat unicitatea în registrul actual, rolul exact, `kind:auditor` și `active:true`; toate sunt păstrate. Cele patru înregistrări suplimentare nu au fost evaluate sau calificate. Registrul live este doar observație punctuală consemnată aici, nu intrare fixată la un hash evolutiv. Rezultatele celor 44 de cazuri nu se schimbă.

## Metodă și calcule

Am citit integral ambele seturi, cele patru fișe de rol și toate cele 44 de răspunsuri, manualul/politica, registrul, cele patru mandate și cele opt înregistrări de predare/închidere. Pentru fiecare răspuns am confruntat cheia, motivul și liniile efective citate, inclusiv trimiterile suplimentare la manual/fișă. Nu am repetat audituri de produs sau calibrări anterioare.

Controlul mecanic a verificat structura JSON fără chei duplicate, tipurile, exact C01–C09 plus două cazuri proprii fără omisiuni/duplicări, ID-urile, datele cu secunde/fus și numărătorile. Citirea semantică, nu simpla egalitate cu cheia, fundamentează rezultatele de mai jos. Am calculat inițial SHA-256 pentru 25 de intrări. Controlul de predare a detectat schimbarea registrului live, explicată și verificată separat mai jos; celelalte 24 de intrări au rămas neschimbate. Inventarul final fixează 26 de intrări: acele 24, fotografia registrului și proveniența ei.

- C01: 950 > 950 este fals; 950/100 = 9,50. Media sau criteriile 980 nu compensează criteriul neadmis.
- C08: 951 > 950 este adevărat; 951/100 = 9,51. PASS se referă exclusiv la stimulul cu toate celelalte condiții stipulate îndeplinite; nu cere 1000.
- C05: 2 × 2.000 = 4.000 cuvinte contabilizate pentru același bloc de 2.000; surplus duplicat 2.000. Nu este dat și nu inventez totalul eligibil al unui roman real.
- C07: {P01, P02, P03, P04} minus {P01, P02, P03} = {P04}: un paragraf omis.
- A-ORIGINALITY-S02: zece axe stipulate distincte — personaje, motivații, relații, obiective, loc, timp, cauzalitate, indicii, rezolvare, voce.
- Calcul nominal: 9 + 2 = 11 per rol; 4 × 11 = 44. Distribuția verdicturilor TEST: 33 RETURN + 4 PASS + 7 NU_E_DEFECT_IN_SINE = 44; acestea nu sunt verdicte asupra produsului sau retururi ale auditorilor.

## Cele 44 de rezultate QA

În tabele, verdictul este cel dat de auditor și confirmat prin cheie. CORECT înseamnă că verdictul, motivul și localizarea au trecut controlul nominal. Notația Ixx:Lx-Ly identifică intrarea din inventarul de mai jos și liniile fizice inclusive; probele suplimentare sunt de asemenea citite și indicate. NU_E_DEFECT_IN_SINE nu reprezintă PASS automat.

### A-GENRE — 01a0d1d0-67b7-7ea2-9e31-562bc344aaa7

Aplicarea brief-ului de gen și final; relevanța probelor de public. Domeniul fișei: G02, G03, G06, G09.

| Caz TEST | Verdict = cheie | Motiv QA independent | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică exact criteriul neadmis: 950 > 950 este fals; notele 980 nu îl compensează. | I06:L7-L11; I01:L12-L14 | CORECT |
| C02 | RETURN | Leagă aliasul Y de ID-ul producătorului X; aliasul nu elimină autoauditul. | I06:L13-L17; I01:L16-L18 | CORECT |
| C03 | RETURN | Separă amprenta veche A de versiunea curentă B și cere audit nou, nu transferul aprobării. | I06:L19-L23; I01:L20-L22 | CORECT |
| C04 | RETURN | Localizează lipsa capitolului C02 din C01–C03; sumarul nu este textul absent. | I06:L25-L29; I01:L24-L26 | CORECT |
| C05 | RETURN | Recunoaște dublarea scenei de 2.000 de cuvinte și cere remediere, renumărare și retest, fără total inventat. | I06:L31-L35; I01:L28-L30 | CORECT |
| C06 | RETURN | Confruntă Mara vie în V2 cu moartea definitivă din V1; nu inventează o excepție de canon. | I06:L37-L41; I01:L32-L34 | CORECT |
| C07 | RETURN | Identifică exact P04 fără corespondent DE și cere reverificare pe identificatori, nu pe volum. | I06:L43-L47; I01:L36-L38 | CORECT |
| C08 | PASS | Aplică 951 > 950 împreună cu toate condițiile stipulate; nu cere artificial 1000. | I06:L49-L53; I01:L40-L42 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Acceptă doar delimitarea onestă a selecției preliminare; exclude explicit PASS automat și aprobarea romanului. | I06:L55-L59; I01:L44-L46 | CORECT |
| A-GENRE-S01 | RETURN | Leagă RETURN de finalul optimist cerut prin brief și încălcat fără aprobare, nu de o interdicție a tragediei. | I06:L61-L65; I02:L4-L6 | CORECT |
| A-GENRE-S02 | RETURN | Respinge extrapolarea cererii de romance din manuale/joc sportiv fără legătură demonstrată; nu confundă succesul cu relevanța. | I06:L67-L71; I02:L7-L9 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate și probe valide; măsuri: niciuna.

### A-ORIGINALITY — 01a0d1d0-690e-7871-b245-6817b004172f

Distincția mecanism general/configurație recognoscibilă; matricea de diferențiere. Domeniul fișei: G03, G10; fără certificat juridic.

| Caz TEST | Verdict = cheie | Motiv QA independent | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Calculează corect minimul întreg 951; un criteriu 950 nu poate fi salvat de media celorlalte. | I11:L7-L11; I01:L12-L14; I04:L18-L18 | CORECT |
| C02 | RETURN | Identifică același ID X sub alias Y și cere evaluator distinct; schimbarea numelui nu produce independență. | I11:L13-L17; I01:L16-L18; I04:L20-L20 | CORECT |
| C03 | RETURN | Constată A ≠ B și cere audit nou; respinge explicit simpla înlocuire a hashului. | I11:L19-L23; I01:L20-L22; I04:L20-L20; I04:L25-L25 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03 și nu echivalează declarația sumarului cu proza. | I11:L25-L29; I01:L24-L26; I04:L70-L70 | CORECT |
| C05 | RETURN | Recunoaște dubla contabilizare a celor 2.000 de cuvinte; nu păstrează duplicatul pentru atingerea pragului. | I11:L31-L35; I01:L28-L30; I04:L58-L60 | CORECT |
| C06 | RETURN | Confruntă explicit moartea definitivă din V1 cu V2, fără înviere sau autorizare inventată. | I11:L37-L41; I01:L32-L34; I04:L30-L30; I04:L70-L70 | CORECT |
| C07 | RETURN | Identifică P04 omis și verificarea necesară P01–P04, indiferent de lungimea traducerii. | I11:L43-L47; I01:L36-L38; I04:L77-L77 | CORECT |
| C08 | PASS | Acceptă numai situația sintetică complet stipulată: 951 > 950, independență, versiune, zero constatări și controale îndeplinite. | I11:L49-L53; I01:L40-L42; I04:L18-L20 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Diferențiază acoperirea preliminară declarată de eșantionul ascuns; nu aprobă automat canonul ori romanul. | I11:L55-L59; I01:L44-L46; I12:L24-L24 | CORECT |
| A-ORIGINALITY-S01 | RETURN | Identifică configurația distinctivă a celor șapte întâmplări, relațiilor, indiciilor și finalului, păstrată sub nume noi; verdict editorial, nu juridic. | I11:L61-L65; I02:L10-L12; I04:L41-L43; I12:L21-L21 | CORECT |
| A-ORIGINALITY-S02 | NU_E_DEFECT_IN_SINE | Verifică cele zece axe stipulate ca diferite; motivul generic al scrisorii nu este singur defect, PASS automat sau garanție juridică. | I11:L67-L71; I02:L13-L15; I04:L37-L43; I12:L9-L9; I12:L21-L21 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate și probe valide; măsuri: niciuna.

### A-STRUCTURE — 01a0d1d0-6cb7-7681-8010-b13b8b640dad

Pregătirea și cauzalitatea climaxului; funcția structurală a scenei. Domeniul fișei: G05, G07, G08.

| Caz TEST | Verdict = cheie | Motiv QA independent | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică pragul strict pe fiecare criteriu: 950 nu trece; media și 980 pe alte criterii sunt nerelevante pentru această lipsă. | I16:L7-L11; I01:L12-L14; I04:L18-L18 | CORECT |
| C02 | RETURN | Urmărește ID-ul X, nu aliasul Y; cere refacere de către o execuție distinctă. | I16:L13-L17; I01:L16-L18; I04:L20-L20 | CORECT |
| C03 | RETURN | Recunoaște amprentele A/B ca versiuni diferite și cere audit pe fișierul și dependențele fixate. | I16:L19-L23; I01:L20-L22; I04:L20-L20; I04:L25-L25 | CORECT |
| C04 | RETURN | Localizează C02 absent; nu acceptă sumarul drept înlocuitor al capitolului. | I16:L25-L29; I01:L24-L26; I17:L24-L24 | CORECT |
| C05 | RETURN | Distinge repetarea textuală a scenei de proza nouă și cere remedierea redundanței plus renumărare. | I16:L31-L35; I01:L28-L30; I04:L58-L60 | CORECT |
| C06 | RETURN | Identifică ruptura V1/V2 a canonului Mara și refuză justificările absente din stimul. | I16:L37-L41; I01:L32-L34; I04:L30-L30 | CORECT |
| C07 | RETURN | Identifică omisiunea DE la P04 și necesitatea restabilirii corespondenței, nu o comparație de lungime. | I16:L43-L47; I01:L36-L38; I04:L77-L77 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai în cazul cu toate celelalte condiții stipulate îndeplinite; nu inventează prag 1000. | I16:L49-L53; I01:L40-L42; I04:L18-L20 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Limita declarată corespunde selecției preliminare; răspunsul nu o extinde la acceptarea etapelor ulterioare. | I16:L55-L59; I01:L44-L46; I04:L27-L27; I17:L24-L24 | CORECT |
| A-STRUCTURE-S01 | RETURN | Localizează lipsa pregătirii necunoscutului/cheii și ruptura dintre climax și alegerile protagonistului; o afirmație despre un indiciu absent nu remediază. | I16:L61-L65; I02:L16-L18; I04:L46-L50; I17:L9-L12 | CORECT |
| A-STRUCTURE-S02 | NU_E_DEFECT_IN_SINE | Urmărește dialog → schimbarea alianței/protecției → obligație → scena următoare; absența violenței nu anulează funcția cauzală. | I16:L67-L71; I02:L19-L21; I04:L48-L48; I17:L6-L6 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate și probe valide; măsuri: niciuna.

### A-EN — 01a0d1d0-6f17-7c52-a5f8-a3c3178c2cb8

Acord, referent, perspectivă și dialog eliptic idiomatic. Domeniul fișei: G06, G07, G09, G11; fără certificare de nativ uman.

| Caz TEST | Verdict = cheie | Motiv QA independent | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică neîndeplinirea strictă 950 > 950; celelalte note sau media nu justifică PASS. | I21:L7-L11; I01:L12-L14; I04:L18-L18 | CORECT |
| C02 | RETURN | Confruntă ID-ul autorului cu cel al semnatarului și identifică autoauditul sub alias. | I21:L13-L17; I01:L16-L18; I04:L20-L20 | CORECT |
| C03 | RETURN | Recunoaște versiunea veche A versus B curent și cere audit nou, fără transfer tacit al aprobării. | I21:L19-L23; I01:L20-L22; I04:L20-L20; I04:L25-L25 | CORECT |
| C04 | RETURN | Identifică lipsa concretă C02, deși sumarul pretinde predare completă. | I21:L25-L29; I01:L24-L26; I04:L70-L70 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte numărată dublu; cere remediere și reverificare, fără total de roman inventat. | I21:L31-L35; I01:L28-L30; I04:L58-L58; I04:L60-L60 | CORECT |
| C06 | RETURN | Identifică contradicția moarte definitivă V1/personaj viu V2 și nu inventează înviere ori schimbare autorizată. | I21:L37-L41; I01:L32-L34; I04:L30-L30; I04:L70-L70 | CORECT |
| C07 | RETURN | Localizează P04 omis din DE și cere verificare pe identificatori, independent de volumul de cuvinte. | I21:L43-L47; I01:L36-L38; I04:L75-L75; I04:L77-L77 | CORECT |
| C08 | PASS | Aplică 951 > 950 cu întregul pachet de condiții stipulate; nu adaugă cerința 1000. | I21:L49-L53; I01:L40-L42; I04:L18-L18; I04:L20-L20 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată fără a deduce acceptarea canonului integral sau a produsului. | I21:L55-L59; I01:L44-L46; I22:L24-L24 | CORECT |
| A-EN-S01 | RETURN | Localizează ambele dezacorduri Anna/have și He/were, plus pronumele masculin fără antecedent în perspectiva dată; nu inventează dialect. | I21:L61-L65; I02:L22-L24; I22:L6-L6; I22:L12-L12 | CORECT |
| A-EN-S02 | NU_E_DEFECT_IN_SINE | Recunoaște replica eliptică «Not tonight» ca idiomatică și autorizată de brief; lipsa verbului finit nu este singură defect sau PASS global. | I21:L67-L71; I02:L25-L27; I22:L6-L6; I22:L12-L12 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate și probe valide; măsuri: niciuna.

## Inventarul fix al intrărilor

Toate amprentele de mai jos sunt SHA-256 efectiv calculate pe bytes, nu preluate din `qualified:true`. I01/I02 sunt seturile; I06/I11/I16/I21 sunt răspunsurile finale. Restul fixează normele și proveniența nominală inspectată. Căile sunt legături absolute sub root-ul mandatului; JSON-ul conține aceeași mapare Ixx → path + sha256 și dimensiunea în bytes.

| Probă | Fișier inspectat | SHA-256 |
| --- | --- | --- |
| I01 | [06_REGISTRU/CALIBRARE/SET_TEST_r02.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/SET_TEST_r02.md>) | `968ac2a12660124cf1e5b6228038d929cfaf6cb9420531398190d01ea92d90ba` |
| I02 | [06_REGISTRU/CALIBRARE/ROM-001/SET_SUPLIMENTAR_r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/SET_SUPLIMENTAR_r01.md>) | `31ff8d6d1521a8e3a7edc594441cac3d95b45d9ec1a1349c20c1935bd84c9c38` |
| I03 | [06_REGISTRU/CALIBRARE/ROM-001/agents_at_A_check.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/agents_at_A_check.json>) | `85c2932b751598375a73e38a8732da602bfe6c894476c6d69497d019f6824806` |
| I04 | [00_CONDUCERE/MANUAL_ATELIER.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/00_CONDUCERE/MANUAL_ATELIER.md>) | `2502324b772ab5527ae214c6113416d39d8df9ae0f46a19a87b75899be46e7b2` |
| I05 | [00_CONDUCERE/policy.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/00_CONDUCERE/policy.json>) | `f28786cd4469679b06cc8dd04e49c0768d7a6447c84fa11c9f0f73dcb38adda4` |
| I06 | [06_REGISTRU/CALIBRARE/ROM-001/A-GENRE-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-GENRE-r01.json>) | `ab89793439aa8b704c555bb0acf921c247c00bf20143ef5f18603ad489fd6239` |
| I07 | [01_ECHIPA/A-GENRE.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-GENRE.md>) | `72d0c6152ab6d8a7a90423708afda135da0258e47adabf097f79e83fe2b0d46b` |
| I08 | [06_REGISTRU/PROMPTURI/ROM-001-A-GENRE-calibrare-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-GENRE-calibrare-r01.md>) | `28ab8ca95a0d6f7d28815e84bb07d1fcfa5bdbf9aeae836ded603f2ec5abcfc4` |
| I09 | [06_REGISTRU/ISTORIC/ROM-001-A-GENRE-calibrare-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-GENRE-calibrare-predare-r01.json>) | `ce72ca8cde736ad24eb1a5863e9f0770410d1803fbe9d1653e77ec2bbae1def7` |
| I10 | [06_REGISTRU/ISTORIC/ROM-001-A-GENRE-calibrare-inchidere-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-GENRE-calibrare-inchidere-r01.json>) | `c940e1a4e883f8d6e8a4f38fa89e2f8b8cf85e34a2833f1371f089053f6fb20d` |
| I11 | [06_REGISTRU/CALIBRARE/ROM-001/A-ORIGINALITY-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-ORIGINALITY-r01.json>) | `500cdda1f6c1dd98bf590c96d146897c588bbd90d2c528461600a080017c966a` |
| I12 | [01_ECHIPA/A-ORIGINALITY.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-ORIGINALITY.md>) | `a25f432bf8afc1c6e88e2f0d2c82717c0a6879482be423310105fff2bb51ed6a` |
| I13 | [06_REGISTRU/PROMPTURI/ROM-001-A-ORIGINALITY-calibrare-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-ORIGINALITY-calibrare-r01.md>) | `7ca0f635df6e8611870ebf7399dcacda47565836ed1347dac299f4f956df59fb` |
| I14 | [06_REGISTRU/ISTORIC/ROM-001-A-ORIGINALITY-calibrare-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-ORIGINALITY-calibrare-predare-r01.json>) | `e4998552499003413ad184ad5137e2358d79fc7077a7b6775a7f1e1aa0f30925` |
| I15 | [06_REGISTRU/ISTORIC/ROM-001-A-ORIGINALITY-calibrare-inchidere-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-ORIGINALITY-calibrare-inchidere-r01.json>) | `e11ab70f84fc3a7f1600511d8f8051f5278376bf381e3fc18d2f33b85e68fb04` |
| I16 | [06_REGISTRU/CALIBRARE/ROM-001/A-STRUCTURE-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-STRUCTURE-r01.json>) | `c3c5cdd70c3914ded56487a2bb19829d194842e1e1ad5079c928010534ca7c2f` |
| I17 | [01_ECHIPA/A-STRUCTURE.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-STRUCTURE.md>) | `2624182c60fdb71beec860552b10090bbc867910fc025248e9e5f22afef268b9` |
| I18 | [06_REGISTRU/PROMPTURI/ROM-001-A-STRUCTURE-calibrare-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-STRUCTURE-calibrare-r01.md>) | `d6d900b7e2979ebc885841b2b36d56c7160f707673a95fe107571460641ca79c` |
| I19 | [06_REGISTRU/ISTORIC/ROM-001-A-STRUCTURE-calibrare-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-STRUCTURE-calibrare-predare-r01.json>) | `4f86c6023dafcba74cfc1a924ce69733813bae04263af08547d58a24687c46bb` |
| I20 | [06_REGISTRU/ISTORIC/ROM-001-A-STRUCTURE-calibrare-inchidere-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-STRUCTURE-calibrare-inchidere-r01.json>) | `6ecbab3e9a33ae198663e3e845564a4053f194397c8d3cd389460b9e770516c1` |
| I21 | [06_REGISTRU/CALIBRARE/ROM-001/A-EN-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-EN-r01.json>) | `56ab181b64702650fe66889e0fbe8f69c1c9284daeac5d0e4af0d643be67a561` |
| I22 | [01_ECHIPA/A-EN.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-EN.md>) | `581b71ebc2aa2cccfd90957c671451258b7b647720963423010e2d12c00a7bce` |
| I23 | [06_REGISTRU/PROMPTURI/ROM-001-A-EN-calibrare-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-EN-calibrare-r01.md>) | `1b404ef083d4732dbc464edb75e5cf3334c5846ec4cd2a341f0bb08250a474ba` |
| I24 | [06_REGISTRU/ISTORIC/ROM-001-A-EN-calibrare-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-EN-calibrare-predare-r01.json>) | `cda559410a46f86e89c80a5a196527f4aa27cfbbacbc7c95312b62617fb0ee2f` |
| I25 | [06_REGISTRU/ISTORIC/ROM-001-A-EN-calibrare-inchidere-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-EN-calibrare-inchidere-r01.json>) | `d8254498959d32dd1db1417bec2654c02ecc129e94d92988652de8b0fb1766bb` |
| I26 | [06_REGISTRU/CALIBRARE/ROM-001/agents_at_A_check_provenance.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/agents_at_A_check_provenance.json>) | `baf62c5779a50a5ac11c9102503778c2d9035058e24a89642c454363b2ebcc84` |

## Limite și predare

- Set deschis, cu cheia disponibilă: nu este test orb, estimare statistică a performanței sau demonstrație de competență literară exhaustivă.
- Calificare nominală pentru exact cele patru ID-uri/roluri și grila verificată, aplicabilă prospectiv; nu califică retroactiv r01 și nu acceptă automat audituri productive viitoare.
- NU_E_DEFECT_IN_SINE nu înseamnă PASS automat. PASS din C08 privește doar cazul TEST și condițiile stipulate, nu un produs real.
- Nu au fost recitite manuscrise/surse web, repetate calibrări anterioare sau emise note productive, metaaudit G01, acceptare G02 ori certificat uman/juridic/de succes comercial.
- Identitățile sunt confirmate documentar prin fotografia stabilă și proveniența ei, mandate și predări/închideri, plus reverificare nominală punctuală în registrul live; nu pretind autentificare externă a infrastructurii. Înregistrările de închidere nu furnizează separat identitate sau dată certificată.
- Fișa/manualul și suplimentul au fost aplicate fără schimbarea politicii: fiecare criteriu productiv strict >950/1000 și zero constatări deschise; aceste condiții nu sunt evaluate aici pentru ROM-001.
- Au fost scrise exclusiv cele două fișiere VERIFICARE_r01; intrările și registrele nu au fost modificate. Arhivarea probelor fixe revine managerului și nu a fost executată de QA.

Politica și pragul nu au fost schimbate de supliment: pentru auditul productiv rămân fiecare criteriu strict >950/1000 și zero constatări deschise. Calificarea de aici nu dovedește îndeplinirea lor de ROM-001 și nu permite calificare retroactivă r01.

Nu rezultă măsuri corective pentru cele patru exerciții. Raportul nu solicită un auditor recursiv al QA. Înaintea predării, verificarea finală read-only controlează parsarea JSON-ului propriu, cele 44 de rezultate și ancorele, concordanța MD/JSON și hashurile efective; JSON-ul fixează hashul acestui MD, fără hash circular al propriului JSON în MD.

Livrabile: [VERIFICARE_r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_r01.md>) și [VERIFICARE_r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_r01.json>). Arhivarea va fi efectuată de manager cu probele fixe; QA nu a executat-o.
