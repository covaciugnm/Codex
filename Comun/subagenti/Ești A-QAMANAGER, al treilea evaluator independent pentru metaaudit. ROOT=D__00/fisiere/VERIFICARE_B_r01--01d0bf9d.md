# ROM-001 — verificare nominală a calibrării editoriale, lot B, r01

Evaluator: A-QAMANAGER — `01a0d0f3-8249-7d91-95f4-ef806130bebe`. Data: `2026-09-24T08:41:26+03:00`.
Calificarea QA r02 existentă este reutilizată conform mandatului, fără recalibrare sau audit recursiv.

## Rezultat și întindere

Cele șase roluri sunt CALIFICAT, fiecare 11/11: nouă cazuri comune și două proprii. Total: 66/66 verdicturi, motive semantice și localizări valide. Nicio constatare de remediat și niciun rol RETURN.

Acesta este controlul nominal al lotului B, set TEST deschis `rom001-b-r01`, nu test orb, audit G00/G01/G02, metaaudit de produs ori acceptare de etapă. Nu există contract de produs pentru această verificare; JSON-ul însoțitor este un raport propriu de calificare. Nu au fost emise note productive, iar lotul A rămâne nemodificat.

Regula: CALIFICAT numai cu identitate/rol/autorizare/independență concordante și 11/11 răspunsuri corecte, motivate și localizate efectiv. Un singur caz greșit sau o probă invalidă ar întoarce exercițiul rolului, cu măsură concretă, fără schimbarea cheii. `qualified:true` și numărătorile declarate au fost comparate cu rezultatul QA calculat, nu folosite ca temei.

## Identități și autorizare

| Rol | ID nominal verificat | Data răspunsului declarat | Verdict QA |
| --- | --- | --- | --- |
| A-CHARACTER | `01a0d1df-4125-7c52-9c87-042d9cbaaedf` | `2026-09-24T08:26:29.0895096+03:00` | CALIFICAT — 11/11 |
| A-FACT | `01a0d1df-4217-7a01-92af-667005fddae6` | `2026-09-24T08:25:07+03:00` | CALIFICAT — 11/11 |
| A-RO | `01a0d1df-4d33-7841-9275-e3fd290768c0` | `2026-09-24T08:25:04+03:00` | CALIFICAT — 11/11 |
| A-DE | `01a0d1df-5136-7653-8989-034c9c8daaf7` | `2026-09-24T08:25:04+03:00` | CALIFICAT — 11/11 |
| A-TRANSLATION | `01a0d1e2-5845-7401-ba0d-8d4ec267681c` | `2026-09-24T08:28:36.0996029+03:00` | CALIFICAT — 11/11 |
| A-PRODUCTION | `01a0d1e2-59ed-7e23-8a75-cdd3413f413f` | `2026-09-24T08:28:27.6584314+03:00` | CALIFICAT — 11/11 |

Contextul fix este B03, `agents_at_B_check.json`: 20 de identități unice, dintre care cinci producători. Cele șase ID-uri sunt UUID-uri valide, distincte între ele, de A-QAMANAGER și de fiecare producător înregistrat. Fotografia confirmă rolul exact, `kind:auditor` și `active:true`, în concordanță cu răspunsurile și predările nominale.

La `2026-09-24T08:37:08+03:00`, am verificat și [registrul live](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/agents.json>): fiecare dintre cele șase ID-uri apare o singură dată și păstrează același rol, tip de auditor și autorizare. Observația este punctuală; hashul registrului live nu este fixat drept context permanent. `active:true` nu certifică automat calificarea și nu înseamnă că execuțiile închise continuă să ruleze.

| Rol | Răspuns | Fișă de rol | Mandat | Predare și închidere |
| --- | --- | --- | --- | --- |
| A-CHARACTER | B06 | B07 | B08 | B09 |
| A-FACT | B10 | B11 | B12 | B13 |
| A-RO | B14 | B15 | B16 | B17 |
| A-DE | B18 | B19 | B20 | B21 |
| A-TRANSLATION | B22 | B23 | B24 | B25 |
| A-PRODUCTION | B26 | B27 | B28 | B29 |

Toate cele șase înregistrări de predare au `agent_id`, `role` și `close_result.previous_status.completed`, cu calea exactă a răspunsului. Pentru A-FACT/A-RO/A-DE există și `message` separat: egalitatea cu textul din închidere este verificată. Pentru A-CHARACTER/A-TRANSLATION/A-PRODUCTION nu există `message` separat; nu pretind această comparație. Ele includ `recorded_at:2026-09-24 05:33:27 UTC`, adică 08:33:27 +03:00, ca metadată locală a consemnării, nu certificat extern al orei de închidere. În celelalte trei nu inventez o dată `recorded_at` absentă.

## Verificări executate și calcule

Am citit integral ambele seturi, toate cele șase fișe, toate cele 66 de răspunsuri, manualul/politica, fotografia de registru, cele șase mandate și șase predări/închideri. Fiecare motiv a fost confruntat semantic cu stimulul și regula, nu doar comparat textual cu cheia. Au fost citite toate localizările invocate, inclusiv probele suplimentare A-TRANSLATION din manual și fișă. Nu există eșantionare în interiorul celor 66 de cazuri.

Controlul mecanic a verificat structura JSON, lipsa cheilor duplicate, tipurile, exact C01–C09 plus cele două ID-uri proprii, datele cu secunde/fus, identitățile, concordanța predării și numărătorile. Au fost calculate SHA-256 pentru 29 de intrări fixe. Rapoartele lotului A sunt doar protejate împotriva modificării prin comparație de hash, nu reauditate.

- C01: 950 > 950 este fals; 950/100 = 9,50. Media nu compensează criteriul.
- C08: 951 > 950 este adevărat; 951/100 = 9,51. PASS aparține doar stimulului cu toate celelalte condiții îndeplinite, fără prag nou de 1000.
- C05: 2 × 2.000 = 4.000 contabilizate pentru același bloc de 2.000; surplus duplicat 2.000. Nu inventez totalul eligibil al unui roman.
- C07: {P01, P02, P03, P04} minus {P01, P02, P03} = {P04}: un paragraf omis.
- A-FACT-S01: 1900 ≠ 1890; diferență de zece ani în stimulul fictiv, fără cercetare web.
- A-RO-S02: codurile au fost verificate efectiv: Ş/U+015E și ţ/U+0163 au sedilă; Ș/U+0218 și ț/U+021B au virgulă dedesubt. Identificatorii diferiți nu satisfac aceeași convenție.
- A-DE-S01: «hadn't … yet» exprimă comunicare încă neefectuată, «schon gesagt» comunicare deja efectuată. Fluența nu repară inversarea.
- A-TRANSLATION-S01: Nora → Paul devine Paul → Nora, iar 18:40 devine 08:40, cu zece ore diferență între orele stipulate. Sunt două abateri la P12.
- A-PRODUCTION-S01: fișier de zero octeți în stimul; nu a fost deschis sau regenerat un PDF real.
- Calificare: 6 × (9 + 2) = 66/66. Verdictele TEST se distribuie în 51 RETURN + 6 PASS + 9 NU_E_DEFECT_IN_SINE = 66; acestea nu sunt retururi ale auditorilor sau verdicte asupra romanului.

## Cele 66 de rezultate nominale

În coloana «Verdict = cheie» este răspunsul auditorului, confirmat independent. CORECT înseamnă verdict, motiv și localizare valide. Bxx identifică intrarea fixă din inventar; :Lx-Ly indică liniile fizice inclusive. Sunt indicate răspunsul, cazul complet și localizările efectiv citate. NU_E_DEFECT_IN_SINE nu este PASS automat.

### A-CHARACTER — 01a0d1df-4125-7c52-9c87-042d9cbaaedf

Motivație, autonomie, schimbare și cost cauzal; etape ale fișei G04/G08. Fără diagnostice reale.

| Caz TEST | Verdict = cheie | Motiv QA | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică criteriul exact 950: 950 > 950 este fals; celelalte note 980 și media nu compensează. | B06:L7-L11; B01:L12-L14; B01:L13-L13 | CORECT |
| C02 | RETURN | Confruntă ID-ul X al autorului cu același ID sub alias Y; schimbarea aliasului nu elimină autoauditul. | B06:L13-L17; B01:L16-L18; B01:L17-L17 | CORECT |
| C03 | RETURN | Identifică amprenta veche A versus B curent și cere audit nou; aprobarea nu se transferă între versiuni. | B06:L19-L23; B01:L20-L22; B01:L21-L21 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03; sumarul nu furnizează textul lipsă. | B06:L25-L29; B01:L24-L26; B01:L25-L25 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte contabilizată dublu și cere remediere plus renumărare/retest, fără total de roman inventat. | B06:L31-L35; B01:L28-L30; B01:L29-L29 | CORECT |
| C06 | RETURN | Confruntă moartea definitivă din V1 cu Mara vie în V2; nu inventează explicație sau schimbare autorizată. | B06:L37-L41; B01:L32-L34; B01:L33-L33 | CORECT |
| C07 | RETURN | Localizează omisiunea DE/P04 și cere aliniere/completare pe identificatori, nu echivalarea numărului de cuvinte. | B06:L43-L47; B01:L36-L38; B01:L37-L37 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai împreună cu toate condițiile stipulate îndeplinite; nu impune artificial 1000. | B06:L49-L53; B01:L40-L42; B01:L41-L41 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată în limitele cerute, fără PASS automat asupra produsului sau canonului integral. | B06:L55-L59; B01:L44-L46; B01:L45-L45 | CORECT |
| A-CHARACTER-S01 | RETURN | Localizează inversarea deciziei Norei fără eveniment, informație ori alegere motivată. Necesitatea climaxului nu este motivație; nu inventează una. | B06:L61-L65; B02:L4-L6; B02:L5-L5 | CORECT |
| A-CHARACTER-S02 | NU_E_DEFECT_IN_SINE | Leagă noua decizie de informația verificată, conflictul interior și costul pe pagină; schimbarea motivată nu este automat contradicție sau PASS global. | B06:L67-L71; B02:L7-L9; B02:L8-L8 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate, autorizare și probe valide; măsuri: niciuna.

### A-FACT — 01a0d1df-4217-7a01-92af-667005fddae6

Afirmații materiale probate și delimitarea perspectivei ficționale; etapa fișei G10. Fără avize de specialitate inventate.

| Caz TEST | Verdict = cheie | Motiv QA | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică criteriul exact 950: 950 > 950 este fals; celelalte note 980 și media nu compensează. | B10:L7-L11; B01:L12-L14; B01:L13-L13; B01:L14-L14 | CORECT |
| C02 | RETURN | Confruntă ID-ul X al autorului cu același ID sub alias Y; schimbarea aliasului nu elimină autoauditul. | B10:L13-L17; B01:L16-L18; B01:L17-L17; B01:L18-L18 | CORECT |
| C03 | RETURN | Identifică amprenta veche A versus B curent și cere audit nou; aprobarea nu se transferă între versiuni. | B10:L19-L23; B01:L20-L22; B01:L21-L21; B01:L22-L22 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03; sumarul nu furnizează textul lipsă. | B10:L25-L29; B01:L24-L26; B01:L25-L25; B01:L26-L26 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte contabilizată dublu și cere remediere plus renumărare/retest, fără total de roman inventat. | B10:L31-L35; B01:L28-L30; B01:L29-L29; B01:L30-L30 | CORECT |
| C06 | RETURN | Confruntă moartea definitivă din V1 cu Mara vie în V2; nu inventează explicație sau schimbare autorizată. | B10:L37-L41; B01:L32-L34; B01:L33-L33; B01:L34-L34 | CORECT |
| C07 | RETURN | Localizează omisiunea DE/P04 și cere aliniere/completare pe identificatori, nu echivalarea numărului de cuvinte. | B10:L43-L47; B01:L36-L38; B01:L37-L37; B01:L38-L38 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai împreună cu toate condițiile stipulate îndeplinite; nu impune artificial 1000. | B10:L49-L53; B01:L40-L42; B01:L41-L41; B01:L42-L42 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată în limitele cerute, fără PASS automat asupra produsului sau canonului integral. | B10:L55-L59; B01:L44-L46; B01:L45-L45; B01:L46-L46 | CORECT |
| A-FACT-S01 | RETURN | Confruntă S1/1900 cu narațiunea/1890 pentru același pod și infirmă pretinsa verificare exactă; nu inventează surse, avize sau cercetare web. | B10:L61-L65; B02:L10-L12; B02:L11-L11; B02:L12-L12 | CORECT |
| A-FACT-S02 | NU_E_DEFECT_IN_SINE | Distinge credința greșită a personajului de faptele asumate narativ: bariera, informația corectă și consecința infirmă credința, nu demonstrează singure defect al autorului. | B10:L67-L71; B02:L13-L15; B02:L14-L14; B02:L15-L15 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate, autorizare și probe valide; măsuri: niciuna.

### A-RO — 01a0d1df-4d33-7841-9275-e3fd290768c0

Sens contextual, terminologie și diacritice românești; etape ale fișei G12/G14. Completitudinea numerică nu este suficientă.

| Caz TEST | Verdict = cheie | Motiv QA | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică criteriul exact 950: 950 > 950 este fals; celelalte note 980 și media nu compensează. | B14:L7-L11; B01:L12-L14; B01:L13-L13; B01:L14-L14 | CORECT |
| C02 | RETURN | Confruntă ID-ul X al autorului cu același ID sub alias Y; schimbarea aliasului nu elimină autoauditul. | B14:L13-L17; B01:L16-L18; B01:L17-L17; B01:L18-L18 | CORECT |
| C03 | RETURN | Identifică amprenta veche A versus B curent și cere audit nou; aprobarea nu se transferă între versiuni. | B14:L19-L23; B01:L20-L22; B01:L21-L21; B01:L22-L22 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03; sumarul nu furnizează textul lipsă. | B14:L25-L29; B01:L24-L26; B01:L25-L25; B01:L26-L26 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte contabilizată dublu și cere remediere plus renumărare/retest, fără total de roman inventat. | B14:L31-L35; B01:L28-L30; B01:L29-L29; B01:L30-L30 | CORECT |
| C06 | RETURN | Confruntă moartea definitivă din V1 cu Mara vie în V2; nu inventează explicație sau schimbare autorizată. | B14:L37-L41; B01:L32-L34; B01:L33-L33; B01:L34-L34 | CORECT |
| C07 | RETURN | Localizează omisiunea DE/P04 și cere aliniere/completare pe identificatori, nu echivalarea numărului de cuvinte. | B14:L43-L47; B01:L36-L38; B01:L37-L37; B01:L38-L38 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai împreună cu toate condițiile stipulate îndeplinite; nu impune artificial 1000. | B14:L49-L53; B01:L40-L42; B01:L41-L41; B01:L42-L42 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată în limitele cerute, fără PASS automat asupra produsului sau canonului integral. | B14:L55-L59; B01:L44-L46; B01:L45-L45; B01:L46-L46 | CORECT |
| A-RO-S01 | RETURN | Identifică library → librărie ca falsă echivalență în contextul explicit al bibliotecii de împrumut; nu inventează servicii ale unei librării. | B14:L61-L65; B02:L16-L18; B02:L17-L17; B02:L18-L18 | CORECT |
| A-RO-S02 | RETURN | Identifică exact Ş/U+015E și ţ/U+0163 cu sedilă versus Ș/U+0218 și ț/U+021B cu virgulă; citibilitatea aproximativă nu îndeplinește ghidul, cere corecție și retest. | B14:L67-L71; B02:L19-L21; B02:L20-L20; B02:L21-L21 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate, autorizare și probe valide; măsuri: niciuna.

### A-DE — 01a0d1df-5136-7653-8989-034c9c8daaf7

Sens, idiom, registru și respectarea ghidului de nume; etape ale fișei G13/G15. Un eșantion nu substituie lectura integrală cerută.

| Caz TEST | Verdict = cheie | Motiv QA | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică criteriul exact 950: 950 > 950 este fals; celelalte note 980 și media nu compensează. | B18:L7-L11; B01:L12-L14; B01:L13-L13; B01:L14-L14 | CORECT |
| C02 | RETURN | Confruntă ID-ul X al autorului cu același ID sub alias Y; schimbarea aliasului nu elimină autoauditul. | B18:L13-L17; B01:L16-L18; B01:L17-L17; B01:L18-L18 | CORECT |
| C03 | RETURN | Identifică amprenta veche A versus B curent și cere audit nou; aprobarea nu se transferă între versiuni. | B18:L19-L23; B01:L20-L22; B01:L21-L21; B01:L22-L22 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03; sumarul nu furnizează textul lipsă. | B18:L25-L29; B01:L24-L26; B01:L25-L25; B01:L26-L26 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte contabilizată dublu și cere remediere plus renumărare/retest, fără total de roman inventat. | B18:L31-L35; B01:L28-L30; B01:L29-L29; B01:L30-L30 | CORECT |
| C06 | RETURN | Confruntă moartea definitivă din V1 cu Mara vie în V2; nu inventează explicație sau schimbare autorizată. | B18:L37-L41; B01:L32-L34; B01:L33-L33; B01:L34-L34 | CORECT |
| C07 | RETURN | Localizează omisiunea DE/P04 și cere aliniere/completare pe identificatori, nu echivalarea numărului de cuvinte. | B18:L43-L47; B01:L36-L38; B01:L37-L37; B01:L38-L38 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai împreună cu toate condițiile stipulate îndeplinite; nu impune artificial 1000. | B18:L49-L53; B01:L40-L42; B01:L41-L41; B01:L42-L42 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată în limitele cerute, fără PASS automat asupra produsului sau canonului integral. | B18:L55-L59; B01:L44-L46; B01:L45-L45; B01:L46-L46 | CORECT |
| A-DE-S01 | RETURN | Confruntă hadn't … yet cu schon gesagt: negația și stadiul acțiunii sunt inversate. Fluența gramaticală nu restabilește sensul. | B18:L61-L65; B02:L22-L24; B02:L23-L23; B02:L24-L24 | CORECT |
| A-DE-S02 | NU_E_DEFECT_IN_SINE | Păstrarea Camille Duret respectă ghidul; germanizarea Kamilla Dürer ar introduce o obligație absentă. Nu deduce aprobarea restului limbii sau integralității. | B18:L67-L71; B02:L25-L27; B02:L26-L26; B02:L27-L27 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate, autorizare și probe valide; măsuri: niciuna.

### A-TRANSLATION — 01a0d1e2-5845-7401-ba0d-8d4ec267681c

Fidelitate și integralitate pe versiunea exactă a sursei; etape ale fișei G12–G15. Auditorul nu este traducătorul/corectorul ediției.

| Caz TEST | Verdict = cheie | Motiv QA | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică criteriul exact 950: 950 > 950 este fals; celelalte note 980 și media nu compensează. | B22:L7-L11; B01:L12-L14; B01:L13-L13; B04:L17-L20 | CORECT |
| C02 | RETURN | Confruntă ID-ul X al autorului cu același ID sub alias Y; schimbarea aliasului nu elimină autoauditul. | B22:L13-L17; B01:L16-L18; B01:L17-L17; B04:L13-L13; B04:L20-L20 | CORECT |
| C03 | RETURN | Identifică amprenta veche A versus B curent și cere audit nou; aprobarea nu se transferă între versiuni. | B22:L19-L23; B01:L20-L22; B01:L21-L21; B04:L20-L20; B04:L25-L25 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03; sumarul nu furnizează textul lipsă. | B22:L25-L29; B01:L24-L26; B01:L25-L25 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte contabilizată dublu și cere remediere plus renumărare/retest, fără total de roman inventat. | B22:L31-L35; B01:L28-L30; B01:L29-L29; B04:L57-L60 | CORECT |
| C06 | RETURN | Confruntă moartea definitivă din V1 cu Mara vie în V2; nu inventează explicație sau schimbare autorizată. | B22:L37-L41; B01:L32-L34; B01:L33-L33; B04:L30-L30 | CORECT |
| C07 | RETURN | Localizează omisiunea DE/P04 și cere aliniere/completare pe identificatori, nu echivalarea numărului de cuvinte. | B22:L43-L47; B01:L36-L38; B01:L37-L37; B23:L6-L12; B04:L77-L77 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai împreună cu toate condițiile stipulate îndeplinite; nu impune artificial 1000. | B22:L49-L53; B01:L40-L42; B01:L41-L41; B04:L18-L20 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată în limitele cerute, fără PASS automat asupra produsului sau canonului integral. | B22:L55-L59; B01:L44-L46; B01:L45-L45 | CORECT |
| A-TRANSLATION-S01 | RETURN | Identifică la P12 ambele abateri: Nora → Paul devine Paul → Nora și 18:40 devine 08:40. Apropierea numărătorilor nu probează fidelitatea. | B22:L61-L65; B02:L28-L30; B02:L29-L29; B23:L6-L12; B04:L75-L77 | CORECT |
| A-TRANSLATION-S02 | RETURN | Leagă ținta aprobată de EN-v1, nu de EN-v2 cu final nou; cere evaluarea impactului, remediere și retest cu istoric păstrat, fără ID-uri de paragraf inventate. Extinderea la ambele traduceri este susținută de manual L77. | B22:L67-L71; B02:L31-L33; B02:L32-L32; B04:L20-L20; B04:L25-L25; B04:L75-L77; B23:L9-L12 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate, autorizare și probe valide; măsuri: niciuna.

### A-PRODUCTION — 01a0d1e2-59ed-7e23-8a75-cdd3413f413f

Deschidere, conținut, ediție și navigare; etape ale fișei G16/G17. Nu confirmă publicarea fără probă de acces.

| Caz TEST | Verdict = cheie | Motiv QA | Localizări verificate | Rezultat QA |
| --- | --- | --- | --- | --- |
| C01 | RETURN | Identifică criteriul exact 950: 950 > 950 este fals; celelalte note 980 și media nu compensează. | B26:L7-L11; B01:L12-L14; B01:L13-L13; B01:L14-L14 | CORECT |
| C02 | RETURN | Confruntă ID-ul X al autorului cu același ID sub alias Y; schimbarea aliasului nu elimină autoauditul. | B26:L13-L17; B01:L16-L18; B01:L17-L17 | CORECT |
| C03 | RETURN | Identifică amprenta veche A versus B curent și cere audit nou; aprobarea nu se transferă între versiuni. | B26:L19-L23; B01:L20-L22; B01:L21-L21 | CORECT |
| C04 | RETURN | Localizează C02 absent din predarea C01–C03; sumarul nu furnizează textul lipsă. | B26:L25-L29; B01:L24-L26; B01:L25-L25 | CORECT |
| C05 | RETURN | Recunoaște scena identică de 2.000 de cuvinte contabilizată dublu și cere remediere plus renumărare/retest, fără total de roman inventat. | B26:L31-L35; B01:L28-L30; B01:L29-L29 | CORECT |
| C06 | RETURN | Confruntă moartea definitivă din V1 cu Mara vie în V2; nu inventează explicație sau schimbare autorizată. | B26:L37-L41; B01:L32-L34; B01:L33-L33 | CORECT |
| C07 | RETURN | Localizează omisiunea DE/P04 și cere aliniere/completare pe identificatori, nu echivalarea numărului de cuvinte. | B26:L43-L47; B01:L36-L38; B01:L37-L37 | CORECT |
| C08 | PASS | Aplică 951 > 950 numai împreună cu toate condițiile stipulate îndeplinite; nu impune artificial 1000. | B26:L49-L53; B01:L40-L42; B01:L41-L41 | CORECT |
| C09 | NU_E_DEFECT_IN_SINE | Recunoaște acoperirea preliminară declarată în limitele cerute, fără PASS automat asupra produsului sau canonului integral. | B26:L55-L59; B01:L44-L46; B01:L45-L45 | CORECT |
| A-PRODUCTION-S01 | RETURN | Identifică PDF-ul de 0 octeți și imposibilitatea deschiderii; existența numelui nu demonstrează testarea/conținutul. Nu pretinde deschiderea unui pachet real. | B26:L61-L65; B02:L34-L36; B02:L35-L35 | CORECT |
| A-PRODUCTION-S02 | RETURN | Localizează textul german din ediția RO și cuprinsul DE către EN. Hashurile valide fixează și bytes greșiți, fără a certifica limba/ediția/navigarea; nu inventează teste productive. | B26:L67-L71; B02:L37-L39; B02:L38-L38 | CORECT |

Verdict nominal: CALIFICAT — 11/11. Identitate, autorizare și probe valide; măsuri: niciuna.

## Inventarul fix al intrărilor

Amprentele sunt SHA-256 calculate efectiv pe bytes. B01/B02 sunt seturile; B03 este fotografia de registru; cele șase fișiere de răspuns sunt B06/B10/B14/B18/B22/B26. JSON-ul conține aceeași mapare Bxx → cale/hash și dimensiunea în bytes. Căile de mai jos sunt absolute sub root-ul mandatului. Nu se fixează hashul registrului live.

| Probă | Fișier inspectat | SHA-256 |
| --- | --- | --- |
| B01 | [06_REGISTRU/CALIBRARE/SET_TEST_r02.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/SET_TEST_r02.md>) | `968ac2a12660124cf1e5b6228038d929cfaf6cb9420531398190d01ea92d90ba` |
| B02 | [06_REGISTRU/CALIBRARE/ROM-001/SET_SUPLIMENTAR_B_r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/SET_SUPLIMENTAR_B_r01.md>) | `84cb08309fdc6c29bd433a12b17635f7eb99734750a323780b6cab9ebe23f8ba` |
| B03 | [06_REGISTRU/CALIBRARE/ROM-001/agents_at_B_check.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/agents_at_B_check.json>) | `9eb4f8b4a4a7189e943fadcdcf7b74677fad93944d0152e464ab17b8b9f70e9c` |
| B04 | [00_CONDUCERE/MANUAL_ATELIER.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/00_CONDUCERE/MANUAL_ATELIER.md>) | `2502324b772ab5527ae214c6113416d39d8df9ae0f46a19a87b75899be46e7b2` |
| B05 | [00_CONDUCERE/policy.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/00_CONDUCERE/policy.json>) | `f28786cd4469679b06cc8dd04e49c0768d7a6447c84fa11c9f0f73dcb38adda4` |
| B06 | [06_REGISTRU/CALIBRARE/ROM-001/A-CHARACTER-b-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-CHARACTER-b-r01.json>) | `c0d42b8bd21d51731f2664db55db46ded8ecafa5d1ad7059512ac55954edbde6` |
| B07 | [01_ECHIPA/A-CHARACTER.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-CHARACTER.md>) | `7cc64af6bf82afaa72f353c91bfc15566267e4ac66b2046058f86031cb458c22` |
| B08 | [06_REGISTRU/PROMPTURI/ROM-001-A-CHARACTER-calibrare-b-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-CHARACTER-calibrare-b-r01.md>) | `94634cf14b4f69ef3f20a10b9a40fd3716233f334debaf28027ff3f869b35c89` |
| B09 | [06_REGISTRU/ISTORIC/ROM-001-A-CHARACTER-calibrare-b-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-CHARACTER-calibrare-b-predare-r01.json>) | `e6ef54310ebb04b13a13cef557f7c84b98c3061074e3f64cc18dd0133911b585` |
| B10 | [06_REGISTRU/CALIBRARE/ROM-001/A-FACT-b-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-FACT-b-r01.json>) | `eb3763a3c2d3692edb43ccb66c760c2865cbbd97ac82d4077ffcbadd19e86289` |
| B11 | [01_ECHIPA/A-FACT.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-FACT.md>) | `8f8312fae8ee0a1f4510a6f8ea1afc971f554892b9938f54a9463f1570ba9fae` |
| B12 | [06_REGISTRU/PROMPTURI/ROM-001-A-FACT-calibrare-b-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-FACT-calibrare-b-r01.md>) | `617f4116ef234e95518ed3c888530f40e6a2cadb76d32b77bb0e0ee7e4ed7165` |
| B13 | [06_REGISTRU/ISTORIC/ROM-001-A-FACT-calibrare-b-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-FACT-calibrare-b-predare-r01.json>) | `2adf4d7611d02e5e2559ac2c68ce23076e3c34d4801a2d47b45b50575ae75f45` |
| B14 | [06_REGISTRU/CALIBRARE/ROM-001/A-RO-b-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-RO-b-r01.json>) | `9696f8d2d0fcc70ae83ef11bbc8732c1ae668a33a0f46db576e147e8d5788353` |
| B15 | [01_ECHIPA/A-RO.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-RO.md>) | `66ca4c30e05256695343e91fed515eb345e199a06e1ac5140ae9eb8b64ce6d87` |
| B16 | [06_REGISTRU/PROMPTURI/ROM-001-A-RO-calibrare-b-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-RO-calibrare-b-r01.md>) | `5a05cd55a88d9c843ee7fd0ddad520851a8180d6df0dd24e72d16ba353f1a743` |
| B17 | [06_REGISTRU/ISTORIC/ROM-001-A-RO-calibrare-b-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-RO-calibrare-b-predare-r01.json>) | `535a5180ca04dbf03eea3ceba3a659ee92135376d6626d0a3f5ec8cd8a524a53` |
| B18 | [06_REGISTRU/CALIBRARE/ROM-001/A-DE-b-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-DE-b-r01.json>) | `13d3c7c369fe969007fba6d0e0f744fabd4dc7ade87f0f9c9c2bc60af63af518` |
| B19 | [01_ECHIPA/A-DE.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-DE.md>) | `2197fb2d212bac118b986ef1a589ab560215a910776089ebe7b3a8944e434851` |
| B20 | [06_REGISTRU/PROMPTURI/ROM-001-A-DE-calibrare-b-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-DE-calibrare-b-r01.md>) | `b2105a77c755e26d8d99dc3df5ba034eef8fda9e14f94a68f019f98394a60ea7` |
| B21 | [06_REGISTRU/ISTORIC/ROM-001-A-DE-calibrare-b-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-DE-calibrare-b-predare-r01.json>) | `0ab8b661570fee93f31d89b18c2998e92494a76823b5f816428539cfbb06b5a2` |
| B22 | [06_REGISTRU/CALIBRARE/ROM-001/A-TRANSLATION-b-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-TRANSLATION-b-r01.json>) | `72f5b905d85b3e4f4df85e8c6e50fa0a1709ae4935967dbb6bfe585f688beaf8` |
| B23 | [01_ECHIPA/A-TRANSLATION.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-TRANSLATION.md>) | `0a576290e92eddf62ebff8378a3744da07bd4091c022102d93a5120ce7dc1946` |
| B24 | [06_REGISTRU/PROMPTURI/ROM-001-A-TRANSLATION-calibrare-b-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-TRANSLATION-calibrare-b-r01.md>) | `d3c17495f25c56c3f6c92bee203d099cc9c78440e3106b948901417703a4369d` |
| B25 | [06_REGISTRU/ISTORIC/ROM-001-A-TRANSLATION-calibrare-b-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-TRANSLATION-calibrare-b-predare-r01.json>) | `659f5d19fa9d83c593df49ab0403f90af1dc31f3f43505136b0b871f91324b2b` |
| B26 | [06_REGISTRU/CALIBRARE/ROM-001/A-PRODUCTION-b-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/CALIBRARE/ROM-001/A-PRODUCTION-b-r01.json>) | `036fc226f320c997238726f1d66eeb17aaf4cd388a5ecf0919932ea1014e4262` |
| B27 | [01_ECHIPA/A-PRODUCTION.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/01_ECHIPA/A-PRODUCTION.md>) | `6dd41897bed1396b325113dea2dbc03b2750660da6e22abd645d36106f7e1151` |
| B28 | [06_REGISTRU/PROMPTURI/ROM-001-A-PRODUCTION-calibrare-b-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/PROMPTURI/ROM-001-A-PRODUCTION-calibrare-b-r01.md>) | `5e0dae89864b922c4a2d1ade2b768344515f5b78274c4c4df873d62ff681f6cf` |
| B29 | [06_REGISTRU/ISTORIC/ROM-001-A-PRODUCTION-calibrare-b-predare-r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/ISTORIC/ROM-001-A-PRODUCTION-calibrare-b-predare-r01.json>) | `bcad0bdaa71f17fa3120229b344db7cf1fc2fa958b9dc3e3b1dcc43bab6ac42e` |

## Limite și predare

- Set cu cheie deschisă: demonstrează aplicarea regulilor la aceste cazuri, nu test orb, performanță statistică sau competență literară exhaustivă.
- Calificarea este nominală pentru cele șase ID-uri/roluri și grila rom001-b-r01 verificată; nu este certificare umană, lingvistică nativă, medicală, juridică sau garanție comercială.
- NU_E_DEFECT_IN_SINE nu înseamnă PASS automat. PASS în C08 privește numai condițiile TEST stipulate, nu un produs real.
- Calificarea nu acceptă etape sau audituri productive viitoare și nu califică retroactiv r01. G00/G01/G02, lotul A și calificarea proprie QA nu au fost reauditate în acest control.
- Identitățile și închiderile sunt confirmate documentar prin fotografia fixă, mandate și înregistrările locale; nu pretind autentificare externă a infrastructurii. Registrul live a fost verificat punctual pentru aceleași șase autorizări, fără hash permanent al lui.
- Toate 66 de motive și localizări au fost inspectate; în afara exercițiului nu au fost citite manuscrise, cercetate surse web, deschise ediții/PDF-uri ori testate traduceri reale.
- Politica rămâne neschimbată: fiecare criteriu productiv strict >950/1000 și zero constatări deschise pentru acceptare. Nicio notă productivă nu a fost emisă aici.
- Au fost scrise exclusiv VERIFICARE_B_r01.md și VERIFICARE_B_r01.json. Arhivarea cu probele fixe revine managerului; QA nu a efectuat-o.

Nu rezultă măsuri corective pentru cele șase exerciții. Calificarea nu pornește automat o etapă și nu validează o ediție, traducere sau manuscris.

Verificarea finală read-only controlează MD/JSON, cele 66 de rezultate și ancorele, hashurile intrărilor fixe, concordanța datelor și păstrarea neschimbată a celor două rapoarte A. JSON-ul fixează hashul acestui MD; MD-ul nu conține hashul propriului JSON.

Livrabile: [VERIFICARE_B_r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_B_r01.md>) și [VERIFICARE_B_r01.json](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/05_AUDIT/ROM-001-CALIBRARE/VERIFICARE_B_r01.json>). Managerul va arhiva probele fixe; QA nu a efectuat arhivarea.

