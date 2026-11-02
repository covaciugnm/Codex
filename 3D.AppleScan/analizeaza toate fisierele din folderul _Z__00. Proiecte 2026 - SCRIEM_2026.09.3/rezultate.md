# Rezultate — analizeaza toate fisierele din folderul "Z:\00. Proiecte 2026 - SCRIEM\2026.09.30 Acțiunea 2.1 POCIDIF\" si acolo avem inceput de scris cerere de finantare in folderul "Z:\00. Proiecte 2026 - SCRIEM\2026.09.30 Acțiunea 2.1 POCIDIF\P1. Dancorproiect SRL" - analizeaza proiectul in starea actuala evalueaza ce exista si ce mai trebuie si ce exista care sunt problemele rezultate in urma evaluarii

Răspunsuri și rezultate disponibile în istoricul local; fără limită de lungime aplicată de export.

## Asistent

Voi inventaria integral dosarul, apoi voi citi documentele de program și materialele deja redactate pentru Dancorproiect. La final vă livrez o evaluare structurată: ce există, ce lipsește, neconcordanțe/riscuri și prioritățile de remediere. Încep cu structura, volumele și eventualele instrucțiuni locale din proiect.

## Asistent

Inventarul arată un dosar deja consistent: documentația oficială, analize tehnice, audit/eligibilitate, bugete, acte de firmă, acte de locație, anexe și 13 secțiuni MySMIS redactate separat. Următorul pas este controlul de conținut și de coerență transversală — în special între ghid, grila de evaluare, planul de afaceri, buget, proiecțiile financiare și câmpurile MySMIS.

## fileChange

````json
{
  "type": "fileChange",
  "id": "exec-92b3a85d-1f2b-4caf-875d-a12c6dcca9a1",
  "changes": [
    {
      "path": "Z:\\00. Proiecte 2026 - SCRIEM\\2026.09.30 Acțiunea 2.1 POCIDIF\\extract_project_content.ps1",
      "kind": {
        "type": "add"
      },
      "diff": "param(\n    [string]$Root = 'Z:\\00. Proiecte 2026 - SCRIEM\\2026.09.30 Acțiunea 2.1 POCIDIF',\n    [string]$Output = 'Z:\\00. Proiecte 2026 - SCRIEM\\2026.09.30 Acțiunea 2.1 POCIDIF\\_analysis_extract.txt'\n)\n\nAdd-Type -AssemblyName System.IO.Compression.FileSystem\n\nfunction Get-OpenXmlText([string]$Path) {\n    $zip = [System.IO.Compression.ZipFile]::OpenRead($Path)\n    try {\n        $strings = @()\n        $shared = $zip.Entries | Where-Object FullName -eq 'xl/sharedStrings.xml'\n        if ($shared) {\n            $reader = [IO.StreamReader]::new($shared.Open())\n            try { [xml]$xml = $reader.ReadToEnd() } finally { $reader.Dispose() }\n            $strings = @($xml.sst.si | ForEach-Object { ($_.InnerText -replace '\\s+', ' ').Trim() })\n        }\n\n        $entries = $zip.Entries | Where-Object {\n            $_.FullName -eq 'word/document.xml' -or\n            $_.FullName -like 'word/header*.xml' -or\n            $_.FullName -like 'word/footer*.xml' -or\n            $_.FullName -like 'xl/worksheets/sheet*.xml' -or\n            $_.FullName -eq 'xl/workbook.xml'\n        } | Sort-Object FullName\n\n        foreach ($entry in $entries) {\n            \"--- XML: $($entry.FullName) ---\"\n            $reader = [IO.StreamReader]::new($entry.Open())\n            try { [xml]$xml = $reader.ReadToEnd() } finally { $reader.Dispose() }\n            if ($entry.FullName -like 'word/*') {\n                $nodes = $xml.SelectNodes('//*[local-name()=\"p\"]')\n                foreach ($node in $nodes) {\n                    $text = (($node.SelectNodes('.//*[local-name()=\"t\"]') | ForEach-Object InnerText) -join '')\n                    if ($text.Trim()) { $text.Trim() }\n                }\n            } elseif ($entry.FullName -like 'xl/worksheets/*') {\n                $rows = $xml.SelectNodes('//*[local-name()=\"row\"]')\n                foreach ($row in $rows) {\n                    $cells = foreach ($cell in $row.SelectNodes('./*[local-name()=\"c\"]')) {\n                        $ref = $cell.r\n                        $formula = $cell.SelectSingleNode('./*[local-name()=\"f\"]')\n                        $valueNode = $cell.SelectSingleNode('./*[local-name()=\"v\"]')\n                        $inline = $cell.SelectSingleNode('.//*[local-name()=\"is\"]')\n                        $value = if ($inline) { $inline.InnerText } elseif ($valueNode) { $valueNode.InnerText } else { '' }\n                        if ($cell.t -eq 's' -and $value -match '^\\d+$' -and [int]$value -lt $strings.Count) { $value = $strings[[int]$value] }\n                        if ($formula) { \"$ref=$value [FORMULA: $($formula.InnerText)]\" } else { \"$ref=$value\" }\n                    }\n                    if ($cells) { \"ROW $($row.r): \" + ($cells -join ' | ') }\n                }\n            } else {\n                ($xml.InnerText -replace '\\s+', ' ').Trim()\n            }\n        }\n    } finally { $zip.Dispose() }\n}\n\n$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Force | Where-Object {\n    $_.Extension -in '.docx', '.xlsx' -and $_.Name -notlike '~$*'\n} | Sort-Object FullName\n\n& {\n    foreach ($file in $files) {\n        \"`n===== FILE: $($file.FullName.Substring($Root.Length + 1)) =====\"\n        try { Get-OpenXmlText $file.FullName } catch { \"[EXTRACTION ERROR] $($_.Exception.Message)\" }\n    }\n} | Set-Content -LiteralPath $Output -Encoding UTF8\n\nGet-Item -LiteralPath $Output | Select-Object FullName, Length, LastWriteTime\n"
    }
  ],
  "status": "completed"
}
````

## Asistent

Am confirmat un aspect important: dosarul conține două stări financiare diferite (modelul inițial de 4,210 mil. € și varianta revizuită de 4,301 mil. €), iar unele documente încă trimit la versiunea veche. De asemenea, din cele 13 fișiere MySMIS, doar „3.1 Activități” are conținut redactat; restul sunt în principal câmpuri goale și limite de caractere. Acum verific PDF-urile oficiale și probele societății/locației/CV-urilor.

## Asistent

Conversia PDF este încă în curs; documentele Word/Excel sunt deja indexate. Până acum, starea reală este mai puțin avansată decât sugerează formularea „proiectat ≈94/100”: acel scor este doar potențial, condiționat de probe care încă lipsesc. Dacă s-ar depune în forma actuală, chiar evaluarea internă îl marchează „RESPINS”.

## Asistent

Verificarea formulelor a scos la iveală o problemă mai gravă decât cele consemnate în rapoartele interne: fișierul „REVIZUIT” nu este utilizabil (grant 3,097 mil. €, depășire salarială și formule `#DIV/0!`). Nici „EVA_Buget_consolidat.xlsx” nu este curat: totalurile de bază sunt corecte manual, dar formulele pentru ponderea activității de bază și personalului propriu indică 0% / `#DIV/0!`. Voi sintetiza acum verdictul și ordinea de remediere.

## Asistent

Am analizat inventarul complet: 88 de fișiere utile — 53 DOCX, 18 XLSX, 14 PDF, 2 DOC și o arhivă ZIP — inclusiv ghidul oficial, anexele, actele firmei, documentele locației, CV-urile, materialele tehnice, bugetele și secțiunile MySMIS.

Verdict general: proiectul are o bază conceptuală bună, dar dosarul de finanțare nu este încă depunabil. În forma actuală, riscul realist este respingerea, nu doar depunctarea. Chiar evaluarea internă din dosar spune explicit „DACĂ S-AR DEPUNE AZI: RESPINS”.

## Ce există și este valoros

- Concept tehnic EVA bine conturat: robot humanoid utilitar, AI locală, viziune stereo, FPGA, Jetson, LiDAR, actuatori și pachete sectoriale.
- Memoriu tehnic relativ avansat, cu structură orientată spre grilă.
- Studiu de piață și analiză de competitori, inclusiv versiuni PDF.
- Rezumat executiv și documente tehnice privind camerele, procesarea și laboratorul.
- Roadmap TRL4–TRL6 și roadmap post-proiect TRL6–TRL9.
- Analize interne de eligibilitate, audit bugetar și simulare de punctaj.
- Listă detaliată de utilaje pentru producție, HPC și laborator.
- Hala de implementare este în proprietatea DANCOR-PROIECT SRL, 672 mp, Str. Emil Racoviță nr. 9, Alba Iulia, fără sarcini în extrasul analizat.
- Devize de amenajare a halei.
- Trei CV-uri existente.
- Structură de activități pe 24 luni.
- Template-uri pentru LOI, protocol pilot și cereri de ofertă.

Acestea reprezintă o fundație tehnică bună, dar nu un dosar de finanțare finalizat.

## Situația reală a cererii

Din cele 13 fișiere MySMIS, doar [3.1 Activități Proiect](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/mysmis/3.1 Activitati Proiect.docx>) conține text substanțial.

Celelalte 12 fișiere conțin aproape exclusiv denumirile câmpurilor și limitele de caractere:

- Capacitate solicitant;
- Localizare;
- Obiective;
- Justificare/context;
- Durabilitate;
- Riscuri;
- Grup-țintă;
- Principii orizontale;
- Metodologie;
- Maturitate;
- Descrierea investiției;
- Rezultate așteptate.

Prin urmare, cererea MySMIS este, în esență, aproximativ 10–15% redactată.

[Cererea de finanțare – schelet](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/4. Dosar depunere (de completat)/02 - Cerere de finantare (schelet Anexa 1).docx>) și [Planul de afaceri – schelet](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/4. Dosar depunere (de completat)/03 - Plan de afaceri (schelet Anexa 4).docx>) sunt doar schițe scurte, nu documente completate conform modelelor oficiale.

## Probleme critice de eligibilitate

### 1. Codul CAEN al proiectului nu este decis

Documentele oscilează între:

- 6210 – software la comandă;
- 2611/2612 – producție componente/subansamble electronice.

Cererea trebuie construită pe un cod CAEN eligibil unic și coerent cu investiția. Formularea actuală „6210 + pentru hardware 2611/2612” nu este suficientă.

Pentru grantul de până la 3 milioane euro, caracterul de produs hardware și producția realizată de beneficiar trebuie susținute fără ambiguități. Lipsesc:

- certificatul constatator actualizat CAEN Rev.3;
- dovada autorizării codului ales la locația de implementare;
- decizia fermă asupra codului 2611, 2612 sau 2630;
- corelarea codului cu fluxul efectiv de producție.

Aceasta este o condiție de tip „go/no-go”.

### 2. Statutul de firmă TIC este vulnerabil

Analizele interne menționează ca activitate principală codul 7022 – consultanță în afaceri și management. Trebuie demonstrat că DANCOR este efectiv întreprindere din domeniul TIC, nu doar că are un cod TIC secundar în obiectul de activitate.

### 3. Datele societății nu sunt complet reconciliate

Documentele interne menționează:

- administrator: Horvath Cosmina Victoria;
- asociați: Covaciu Cosmin Adrian și Benga Emil Gabriel.

Textul extras din actul constitutiv 2026 indică însă Covaciu Cosmin Adrian ca asociat unic. Trebuie verificată și uniformizată situația actuală ONRC: asociați, administrator, reprezentant legal și puteri de semnătură.

### 4. Nu există încă dovada capacității financiare

Bugetul presupune:

- cofinanțare eligibilă de aproximativ 1,301 milioane euro;
- finanțare prin credit pe 10 ani;
- necesar important de lichiditate în implementare.

Nu există în dosar:

- scrisoare de confort;
- ofertă sau aprobare de credit;
- contract de credit;
- extras de cont;
- hotărâre AGA privind proiectul și cofinanțarea.

Capitalul social foarte redus și dimensiunea actuală a firmei fac acest risc major.

### 5. Nu este efectuată verificarea completă a eligibilității financiare

Lipsesc sau nu sunt completate:

- calculul „întreprindere în dificultate” – Anexa 15;
- situațiile financiare pe ultimii doi ani organizate în dosar;
- declarația IMM completată;
- analiza întreprinderilor legate/partenere;
- inventarul ajutoarelor de minimis;
- confirmarea finanțărilor anterioare excluse;
- certificatele fiscale și cazierele necesare contractării.

## Probleme serioase în buget

Există trei versiuni financiare incompatibile.

| Fișier | Cost eligibil | Grant | Cofinanțare | Verdict |
|---|---:|---:|---:|---|
| ORIGINAL | 4.210.715 € | 3.000.000 € | 1.210.715 € | versiune veche, fragilă |
| REVIZUIT | 4.422.118 € | 3.097.010 € | 1.325.109 € | neconform și cu formule defecte |
| Consolidat | 4.300.850 € | 2.999.995 € | 1.300.855 € | cea mai apropiată de varianta de lucru, dar încă defectă |

### Fișierul „REVIZUIT” este neutilizabil

La recalcularea în Excel rezultă:

- grant 3.097.010 €, peste plafonul de 3 milioane;
- salarii de 51,1 €/oră, peste plafonul de 50 €/oră;
- formule `#DIV/0!`;
- pondere activitate de bază 0%;
- pondere personal propriu 0%;
- flux cumulat negativ în primii doi ani de durabilitate;
- dashboard cu rezultate contradictorii.

### Fișierul consolidat are totaluri bune, dar formule greșite

[EVA_Buget_consolidat.xlsx](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/3. Buget/EVA_Buget_consolidat.xlsx>) pare varianta care ar trebui păstrată, însă:

- ponderea activității de bază apare 0%;
- ponderea personalului propriu apare `#DIV/0!`;
- formulele de sumarizare trimit la coloane greșite;
- grantul este 2.999.995 €, nu exact 3.000.000 €;
- proiecțiile comerciale diferă de restul documentelor;
- creditul de 1,301 milioane euro este tratat ca și cum ar fi deja disponibil.

Valorile corecte calculate manual par a fi aproximativ:

- activitate de bază: 90%;
- personal propriu în activitatea de bază: 22%;
- minimis: 300.000 €.

Dar un evaluator va primi fișierul, nu calculul manual.

### Anexa 16 internă are, de asemenea, formule greșite

Formula pentru activitatea de bază include A0 și omite activitatea de introducere în piață A5. Formula personalului propriu folosește rândul A0, rezultând practic 0%. Așadar, Anexa 16 nu trebuie depusă în forma actuală.

### Proiecțiile financiare nu sunt unitare

Apar cel puțin două serii de venituri în perioada de durabilitate:

- 0,9 / 1,45 / 2,10 milioane euro;
- 1,2 / 1,8 / 2,6 milioane euro.

În consecință, apar și valori diferite pentru:

- RI: 18,4%, 18,8%, 21,7%;
- PI_D: aproximativ 0,68–0,79;
- fluxul de numerar.

Trebuie stabilit un singur scenariu financiar, realist și fundamentat prin preț × cantitate × clienți × contracte.

## Costurile halei nu sunt integrate în capacitatea financiară

Devizul detaliat arată:

- total lucrări: 781.666 €;
- surse proprii și „zonă gri”: 561.666 €;
- fotovoltaice/baterii – alt program: 150.000 €;
- mezanin opțional: 70.000 €.

Aceste costuri nu sunt integrate coerent în necesarul total de lichiditate și în proiecțiile financiare. Ghidul cere ca sustenabilitatea să ia în calcul toate costurile eligibile și neeligibile, nu numai cofinanțarea bugetului PoCIDIF.

Mai trebuie clarificate:

- TVA;
- renovările neeligibile;
- fundațiile utilajelor;
- branșamentul de circa 400 kVA;
- ventilația și exhaustarea ATEX;
- autorizarea PSI și de mediu;
- costurile reale de funcționare ale HPC, cuptoarelor și secției metalice.

## Riscul de supradimensionare tehnică

Linia de producție de 2,5 milioane euro include numeroase utilaje grele: CNC, strung, danturare, EDM, WAAM, binder jetting, cuptoare, metrologie etc.

Evaluatorul poate considera că proiectul este:

- preponderent o investiție în utilaje;
- supradimensionat pentru realizarea unui prototip TRL6;
- insuficient justificat față de volumul de producție prognozat;
- dificil de instalat și autorizat într-o hală de 672 mp;
- insuficient corelat cu capacitatea actuală a microîntreprinderii.

Este necesar un flux de producție clar:

`BOM robot → piese fabricate intern → utilaj folosit → timp/utilizare → capacitate anuală → cost unitar → volum de vânzări`

În lipsa acestei demonstrații, o parte importantă a utilajelor poate fi redusă sau declarată neeligibilă.

## Dovezi tehnice și comerciale lipsă

Memoriul tehnic este bine formulat, dar multe afirmații sunt încă declarative. Lipsesc:

- schema arhitecturii hardware/software;
- BOM complet;
- desene și specificații;
- fotografii/video/procese-verbale ale TRL4;
- rapoarte de test;
- dovada unui prototip parțial;
- plan de testare și validare;
- plan de certificare CE/EMC/siguranță;
- analiza riscurilor funcționale ale robotului;
- strategia reală de proprietate intelectuală;
- delimitarea cercetare industrială/dezvoltare experimentală.

Lipsesc integral:

- minimum trei LOI reale;
- protocolul pilot;
- clienții nominali;
- două oferte pentru fiecare cheltuială eligibilă;
- centralizatorul Anexa 7;
- fundamentarea prețului robotului și a abonamentelor.

Template-urile existente nu constituie dovezi.

## Echipa nu este încă demonstrată

Sunt trei CV-uri, dar bugetul presupune cinci specialiști tehnici, plus manager și responsabil financiar.

- CV-ul lui Bogdan Pintea arată experiență puternică în produs, AI, edge și business development.
- CV-urile Cristina Potra și Mihai Jalobeanu sunt în format slab indexabil; trebuie verificate manual/OCR și mapate punctual pe cerințele grilei.
- Nu există o matrice „persoană → rol → experiență → proiecte → studii → criteriu ETF”.
- Nu sunt identificate nominal toate cele cinci persoane bugetate.
- Nu este demonstrat care dintre ele sunt sau vor deveni personal propriu.
- Lipsesc actele de numire și declarațiile de conflict pentru echipa completă.

## Anexele administrative

În folderul „Anexe mysmis” există doar câteva modele, în mare parte necompletate. Lipsesc din dosarul Dancor sau nu sunt finalizate:

- Planul de monitorizare;
- Declarația IMM;
- Declarația TVA;
- declarația privind cumulul ajutoarelor;
- Anexa 15 – firmă în dificultate;
- hotărârea AGA;
- situațiile financiare organizate pentru depunere;
- bugetul oficial Anexa 6 final;
- centralizatorul Anexa 7;
- organigrama și actele echipei.

Există și o problemă de control al versiunilor: numerotarea declarației de cumul și a acordului de parteneriat diferă între ghid, denumirile fișierelor și checklistul intern. Înainte de completare trebuie stabilit setul oficial final de anexe și eliminate dublurile.

## Evaluare de maturitate

Estimarea mea:

- concept și poziționare: 70%;
- documentație tehnică narativă: 55–60%;
- documente comerciale/probe de piață: 10%;
- buget funcțional și reconciliat: 40%;
- cerere MySMIS: 10–15%;
- plan de afaceri conform anexei: 15–20%;
- anexe administrative: 20–25%;
- eligibilitate demonstrată: sub 40%;
- pregătire globală pentru depunere: aproximativ 30–35%.

Scorul intern „≈94/100” este un scor potențial, nu scorul stării actuale. În prezent nu poate fi susținut documentar.

## Ordinea recomandată de remediere

1. Decizie „go/no-go” pe CAEN, caracterul hardware și capacitatea reală de cofinanțare.
2. Certificat ONRC Rev.3 și autorizarea codului unic la hala din Emil Racoviță nr. 9.
3. Verificarea completă IMM, firme legate, minimis, firmă în dificultate și finanțări anterioare.
4. Alegerea unei singure versiuni de buget și repararea tuturor formulelor.
5. Introducerea renovării, TVA și costurilor neeligibile în necesarul financiar total.
6. Reducerea/justificarea tehnologică a liniei de producție prin BOM și flux de fabricație.
7. Obținerea ofertelor reale pentru fiecare poziție eligibilă.
8. Confirmarea nominală a echipei și verificarea CV-urilor.
9. Obținerea LOI-urilor și a protocolului pilot.
10. Finalizarea probelor TRL și a documentației de testare/certificare.
11. Scrierea integrală a Planului de afaceri și a câmpurilor MySMIS.
12. Reconcilierea finală: aceleași sume, rezultate, activități, indicatori și termene în toate documentele.

Concluzia esențială: merită continuat numai dacă DANCOR poate demonstra rapid codul CAEN hardware, producția proprie și finanțarea reală a unui efort total care poate depăși 1,8 milioane euro din surse proprii/credit, după includerea amenajării și a costurilor neeligibile. Altfel, proiectul trebuie redimensionat semnificativ.

## Asistent

L-am verificat doar la nivelul informațiilor existente în dosar, nu l-am putut confirma documentar definitiv.

Analiza internă afirmă că, pe baza unui certificat constatator din 06.06.2025, DANCOR avea ca activități secundare:

- 6201 → corespondent CAEN Rev.3: 6210;
- 6202/6203 → 6220;
- 6209 → 6290;
- 6311 → 6310.

Tot analiza spune că 6201 era autorizat „la terți”. Problema este că certificatul constatator respectiv nu se găsește efectiv în folder, iar actul constitutiv scanat nu dovedește autorizarea activității la locația proiectului. Existența codului în obiectul de activitate nu este același lucru cu autorizarea lui.

În plus, pentru componenta hardware, documentele indică faptul că 2611, 2612 și 2630 nu sunt confirmate; este menționat doar 2790, care nu apare în lista CAEN eligibilă a apelului.

Concluzie: codurile secundare TIC sunt plauzibile, dar neverificate oficial în forma actuală a dosarului. Este necesar un certificat constatator ONRC actualizat, CAEN Rev.3, care să confirme:

- lista activităților secundare;
- codul unic ales pentru proiect;
- autorizarea codului la hala din Str. Emil Racoviță nr. 9;
- existența/autorizarea 2611, 2612 sau 2630 dacă proiectul rămâne pe varianta hardware de 3 milioane euro.

## Asistent

Accesez dosarul firmei și verific în primul rând certificatul constatator, actele ONRC și codurile CAEN secundare/autorizate. Nu voi modifica nimic.

## Asistent

Am găsit documentele decisive, inclusiv certificatul constatator din 06.06.2025, unul din 11.03.2026 și dosarul ONRC din 15.06.2026. Le citesc acum comparativ, ca să disting între codurile înscrise în obiectul de activitate și cele efectiv autorizate la sediu/terți.

## Asistent

Am accesat folderul și am verificat documentele ONRC. Corectez concluzia anterioară:

- DANCOR are codul secundar 6201 – realizare software la comandă, corespondent CAEN Rev.3: 6210.
- Codul 6201 este și autorizat, dar numai pentru activități desfășurate „la terți”.
- Mai apar în obiectul secundar 6209 și activități corespunzătoare 6202/6203/6311, însă nu rezultă că toate sunt autorizate.
- Codul 2790 este secundar și autorizat la un „fond de comerț”, dar nu este eligibil pentru acest apel.
- Codurile hardware eligibile 2611, 2612 și 2630 nu apar în certificatul verificat.
- Activitatea principală rămâne 7022 – consultanță pentru afaceri și management.

Problema decisivă: hala din Str. Emil Racoviță nr. 9 a fost cumpărată în aprilie 2026, după certificatele analizate, și nu apare ca sediu secundar/punct de lucru cu activitate autorizată. Certificatul indică doar punctul de lucru din Sighișoara.

Prin urmare:

- pentru varianta software, 6210 există în fond, dar trebuie convertit/confirmat în CAEN Rev.3 și autorizat la noua locație;
- pentru varianta hardware de 3 milioane euro, trebuie adăugat și autorizat 2611, 2612 sau 2630 la hala din Alba Iulia;
- trebuie înregistrată hala ca punct de lucru/sediu secundar înaintea obținerii unui certificat constatator nou.

Certificatul recomandat pentru proiect trebuie emis după aceste operațiuni și să arate explicit:

1. CAEN Rev.3;
2. punct de lucru Str. Emil Racoviță nr. 9;
3. codul eligibil ales pentru proiect;
4. activitatea autorizată la acel punct de lucru.

## Asistent

Următoarea problemă critică este dovada capacității de cofinanțare și a lichidității.

Proiectul presupune aproximativ:

- 1.300.855 € cofinanțare eligibilă;
- circa 561.666 € pentru amenajarea halei și lucrări „zonă gri”;
- TVA și alte cheltuieli neeligibile;
- finanțarea temporară a cheltuielilor până la rambursarea grantului.

Bugetul presupune un credit pe 10 ani, dar în dosar nu există încă o aprobare bancară pentru această sumă.

Trebuie rezolvate imediat:

1. Stabilirea necesarului total de finanțare, inclusiv TVA, renovare și decalajul de rambursare.
2. Solicitarea la bancă a unei scrisori de confort/eligibilitate sau a unei oferte ferme de credit.
3. Pregătirea situațiilor financiare 2024–2025, balanței recente și extraselor de cont.
4. Verificarea gradului de îndatorare și a garanțiilor disponibile, inclusiv hala.
5. Hotărârea AGA privind proiectul, valoarea totală și asumarea cofinanțării.
6. Introducerea creditului, dobânzii și ratelor reale în fluxul de numerar.

Pragul de decizie este simplu: dacă banca nu confirmă o capacitate apropiată de necesarul total, proiectul trebuie redimensionat înainte de continuarea scrierii. După aceasta, următoarea problemă va fi repararea și unificarea bugetului.

## Asistent

Verific exact în ghid diferența dintre documentele cerute la depunere și cele cerute la contractare, apoi clarific și cum poate fi întins legal proiectul pe 24 de luni fără ca renovarea să afecteze eligibilitatea ajutorului regional.

## Asistent

Nu, scrisoarea de confort sau oferta fermă de credit nu este obligatorie la depunerea cererii.

Conform ghidului:

- la depunere este obligatorie Hotărârea AGA/Decizia asociatului unic, cu valoarea totală, cofinanțarea, cheltuielile neeligibile și sumele necesare până la rambursare;
- dovada efectivă a cofinanțării — extras de cont, linie sau contract de credit — se prezintă la contractare;
- termenul indicat este de 15 zile lucrătoare de la scrisoarea de demarare a contractării.

Totuși, recomand inițierea discuției cu banca acum, deoarece 15 zile la contractare pot fi insuficiente pentru aprobarea unui credit de aproximativ 1,3 milioane euro.

## Cum maximizăm finanțarea

Ținta poate fi:

- grant: maximum 3.000.000 €;
- investiție eligibilă: aproximativ 4.300.850 €;
- cofinanțare eligibilă: aproximativ 1.300.855 €;
- implementare: 24 luni, durata maximă standard.

Pentru grantul de 3 milioane euro trebuie menținută încadrarea ca produs hardware inovativ, cu producție realizată de DANCOR și cu suma peste 1,5 milioane justificată prin linia de producție.

Valoarea totală eligibilă poate fi chiar mai mare de 4,3 milioane euro, dar grantul rămâne plafonat la 3 milioane. Diferența suplimentară va fi suportată de firmă.

## Renovarea halei

Renovarea generală nu poate fi introdusă în grant doar pentru a maximiza investiția. Sunt, în principiu, neeligibile:

- tencuieli și finisaje generale;
- geamuri și uși;
- încălzirea generală;
- birouri, vestiare și grupuri sanitare;
- mezanin;
- reparații generale ale halei.

Pot fi analizate pentru includere doar costurile direct și inseparabil legate de instalarea/punerea în funcțiune a utilajelor, de exemplu:

- fundații speciale pentru utilaje;
- instalarea și configurarea echipamentelor;
- alimentări electrice dedicate;
- exhaustare ATEX specifică utilajului;
- racorduri tehnologice;
- punerea în funcțiune.

Ideal, aceste costuri trebuie să apară în ofertele furnizorilor ca parte a echipamentului/instalării. Eligibilitatea lor trebuie confirmată înainte de definitivarea bugetului.

## Calendar recomandat pentru 24 luni

- L1–L3: proiect tehnic, autorizații, documentații și lansarea achizițiilor;
- L2–L8: renovarea halei din surse proprii;
- L3–L10: proceduri și contractare echipamente;
- L7–L15: livrare și instalare linie de producție/HPC;
- L1–L18: cercetare industrială și dezvoltarea modulelor EVA;
- L10–L20: integrare, fabricație componente și prototip;
- L16–L22: testare, certificare preliminară și pilot;
- L18–L24: introducere în piață;
- L22–L24: audit tehnic și ultima cerere de rambursare.

Nu recomand amânarea tuturor achizițiilor spre final: cele 24 luni includ și realizarea cheltuielilor, livrarea, punerea în funcțiune și depunerea cererilor de rambursare.

De asemenea, pentru ajutorul de stat, nu trebuie făcute cheltuieli sau angajamente ferme aferente investiției eligibile înainte de depunerea cererii. Pentru lucrările legate direct de investiția regională, varianta prudentă este începerea după depunere și, ideal, după clarificarea eligibilității/contractare.

## Asistent

Atunci strategia financiară trebuie schimbată: eliminăm cofinanțarea voluntară introdusă doar pentru punctaj și solicităm intensitatea maximă permisă pentru fiecare cheltuială.

În bugetul actual există o linie de 250.000 € pentru cercetare contractuală, finanțată integral din surse proprii. Aceasta a fost introdusă pentru cele 5 puncte aferente cofinanțării suplimentare. Dacă obiectivul este cofinanțarea minimă, linia trebuie eliminată sau finanțată la intensitatea maximă permisă.

Varianta imediată, pe structura actuală:

- cost eligibil: aproximativ 4.050.850 €;
- grant solicitat: 3.000.000 €;
- cofinanțare eligibilă minimă: aproximativ 1.050.850 €;
- renovare, TVA și cheltuieli neeligibile: separat.

Principiile noului buget:

- ajutor regional: 70% grant / 30% contribuție;
- cercetare industrială: 80% grant dacă acceptăm condiția de diseminare/licențiere;
- dezvoltare experimentală: 60% grant dacă sunt îndeplinite condițiile majorării;
- minimis: 100%, maximum 300.000 €;
- nicio cheltuială eligibilă finanțată voluntar 100% din surse proprii;
- grant total exact 3.000.000 €;
- activitatea de bază minimum 80%;
- personalul tehnic propriu minimum 20% din grantul activității de bază.

Există însă un compromis: dacă solicităm strict cofinanțarea minimă, probabil pierdem cele 5 puncte de la criteriul 4.2. Scorul proiectat ar coborî aproximativ de la 94 la 89 de puncte, deci sub pragul de excelență de 92, dar peste pragul minim de 70.

Recomandarea mea este să reconstruim bugetul pe obiectivul declarat:

> grant maxim 3.000.000 €, contribuție eligibilă minimă, fără cheltuieli eligibile autofinanțate voluntar.

Ținta realistă imediată este o cofinanțare eligibilă de aproximativ 1,05 milioane euro. O reducere suplimentară ar necesita mutarea unei părți mai mari din buget din ajutor regional de 70% în cercetare industrială de 80%, dar numai dacă încadrarea tehnică poate fi apărată solid și linia de producție rămâne suficientă pentru justificarea plafonului hardware.

## Asistent

Voi verifica fiecare categorie pe trei axe: eligibilitatea legală, intensitatea corectă de ajutor și efectul asupra punctajului. Mă concentrez pe varianta cu grant de 3 milioane €, cofinanțare minimă și fără linii introduse artificial pentru punctaj. Verific separat linia de producție, HPC/laboratorul, salariile, minimis și formulele de control.

## Asistent

La verificarea preliminară, clasificarea generală a utilajelor și a HPC-ului este permisă de ghid, dar „100% corect” nu este încă adevărat: am identificat deja probleme la salarii, la justificarea unor utilaje și la formule. Verific și dacă specificațiile hardware folosite în fișe sunt actuale și ofertabile, deoarece fără aceasta nu putem susține rezonabilitatea prețurilor.

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-23298bae-82ab-4e1e-92bf-1a4244bb3256",
  "query": "site:nvidia.com Jetson AGX Thor Developer Kit official specifications availability price ...",
  "action": {
    "type": "search",
    "query": null,
    "queries": [
      "site:nvidia.com Jetson AGX Thor Developer Kit official specifications availability price",
      "site:nvidia.com H100 Tensor Core GPU official specifications L40S official",
      "site:amd.com VEK280 evaluation kit official specifications price",
      "site:nvidia.com DGX B200 official specifications"
    ]
  },
  "results": null
}
````

## Asistent

Verdictul este clar: bugetul nu este încă încadrat 100% corect și nu este pregătit pentru punctaj maxim. În plus, „cofinanțare minimă” și „punctaj maxim” sunt obiective incompatibile: criteriul 4.2 acordă 5 puncte numai dacă aportul propriu depășește minimul obligatoriu cu peste 5%.

## Varianta cu finanțare maximă și cofinanțare minimă

Pe structura actuală, varianta optimă este eliminarea cheltuielii de 250.000 euro pentru „cercetare contractuală”, prevăzută integral din surse proprii doar pentru majorarea cofinanțării.

| Componentă | Eligibil | Grant | Cofinanțare |
|---|---:|---:|---:|
| Linie de producție | 2.500.000 € | 1.750.000 € | 750.000 € |
| HPC și infrastructură AI | 506.850 € | 354.795 € | 152.055 € |
| Personal cercetare | 744.000 € | 595.200 € | 148.800 € |
| Ajutor de minimis | 300.000 € | 300.000 € | 0 € |
| **Total** | **4.050.850 €** | **2.999.995 €** | **1.050.855 €** |

Cofinanțarea eligibilă minimă rezultată este deci aproximativ **1,051 milioane euro**, la care se adaugă:

- TVA, dacă nu este eligibilă;
- renovările și lucrările neeligibile;
- cheltuielile până la rambursarea cererilor de plată;
- eventualele depășiri de preț.

Diferența de 5 euro până la plafonul de 3 milioane se corectează la definitivarea ofertelor.

Consecința de punctaj:

- maximum teoretic: aproximativ **95/100**, deoarece se pierd cele 5 puncte pentru cofinanțare suplimentară;
- raportat la evaluarea internă actuală, estimarea realistă este în jur de **89/100**, dacă restul neconformităților sunt rezolvate;
- pragul de excelență de 92 poate deveni dificil de atins cu cofinanțare strict minimă.

## 1. Linia de producție – încadrare parțial corectă

Fișierul analizat: [Linie productie robotica.xlsx](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/3. Buget/Linie productie robotica.xlsx>).

Încadrarea ca ajutor regional, la intensitatea de 70%, este în principiu posibilă pentru echipamentele care intră efectiv în fluxul de producție al robotului EVA.

Sunt relativ bine încadrate:

- CNC 5 axe;
- strung multifuncțional;
- mașină de danturat;
- debitare;
- scule și presetter;
- echipamente additive strict necesare pieselor robotului;
- echipamente de control dimensional și calitate.

Problemele identificate:

- Sunt prevăzute simultan WAAM/DED și Binder Jet, plus trei tipuri de cuptoare. Pentru volume de 3, 7–10 și 15–20 roboți, configurația poate fi considerată supradimensionată.
- Wire EDM, două rectificări, CMM, scanner și rugozimetru trebuie legate de repere concrete din BOM-ul robotului.
- „Sisteme auxiliare – 20.000 euro” este prea vag. Trebuie împărțit în echipamente distincte, cu cantități și oferte.
- Lipsesc calculul de capacitate, orele de funcționare, gradul de utilizare și analiza make-or-buy.
- Lipsesc layoutul halei și fluxurile pentru materii prime, pulberi metalice, tratament termic, prelucrări și control.
- Nu este demonstrat că hala de 672 m² permite instalarea sigură a tuturor echipamentelor, inclusiv zona ATEX, cuptoarele și laboratorul.
- Ventilația, puterea electrică, PSI, ATEX și amenajările necesare nu sunt integral bugetate sau delimitate între eligibil și neeligibil.

Recomandare: păstrați numai utilajele susținute printr-un tabel „reper robot – operație – utilaj – timp/ciclu – capacitate anuală”. Restul trebuie etapizat, externalizat sau foarte bine argumentat.

## 2. HPC și laboratorul AI – eligibil, dar cu probleme tehnice și de preț

Ghidul permite infrastructură HPC, GPU, AI, edge și stocare în categoria introducerii în producție. Totuși, trebuie demonstrat că sistemul este utilizat pentru industrializarea și exploatarea produsului, nu exclusiv pentru activități de cercetare.

Probleme:

- Configurația cu 4 noduri H100, 4 noduri L40S și 2 noduri RTX 6000 Ada poate părea redundantă fără un calcul de workload.
- Fișa H100 conține o eroare: aproximativ 989 TFLOPS reprezintă performanța TF32 indicată de NVIDIA, nu FP16 în forma înscrisă în proiect. Fișa trebuie corectată. [Specificațiile oficiale NVIDIA H100](https://www.nvidia.com/en-us/data-center/h100/)
- În 2026 există deja generația NVIDIA Blackwell/DGX B200. H100 nu devine neeligibil, dar trebuie justificat prin cost, disponibilitate, compatibilitate și TCO. [NVIDIA DGX B200](https://www.nvidia.com/en-us/data-center/dgx-b200/)
- AMD VEK280 este prezentat oficial ca evaluation kit, nefiind destinat producției de serie. Prețul oficial este de 6.995 USD/bucată, în timp ce bugetul prevede 18.000 euro/bucată. Diferența trebuie explicată prin accesorii, licențe și integrare sau redusă. [AMD VEK280](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/vek280.html)
- Jetson AGX Thor Developer Kit are un preț oficial indicativ de aproximativ 3.499 USD, iar proiectul prevede 10.000 euro/bucată. Trebuie separat kitul de dezvoltare de modulele destinate roboților și de serviciile de integrare. [NVIDIA Jetson Thor](https://www.nvidia.com/en-gb/autonomous-machines/embedded-systems/jetson-thor/)
- Nu există dimensionare: parametri model, volum dataset, ore de antrenare, grad de utilizare GPU, stocare anuală și comparație cu varianta cloud.
- Licențele de 7.850 euro trebuie detaliate pe produs, perioadă, număr de utilizatori și tratament contabil.

Pentru punctaj maxim, adăugați o anexă de dimensionare HPC și o comparație CAPEX versus cloud pentru 24–36 luni.

## 3. Laboratorul separat nu este inclus integral în bugetul consolidat

Fișierul cu dotări pentru secții și laborator conține aproximativ 570.000 euro, dar această sumă nu are spațiu distinct în bugetul consolidat.

Există și suprapuneri:

- CMM și scanner 3D apar și în linia de producție;
- rugozimetrul apare în mai multe liste;
- licențele CAD/CAE/EDA se pot suprapune cu licențele HPC;
- echipamentele de testare trebuie delimitate între laborator de cercetare și control de producție.

Trebuie creată o singură listă master, cu un cod unic pentru fiecare echipament. În forma actuală există risc de dublă bugetare.

## 4. Salariile nu sunt 100% conforme

Plafoanele din Anexa 9 sunt:

- categoria 1: maximum 50 euro/oră;
- categoria 2: maximum 35 euro/oră;
- categoria 3: maximum 25 euro/oră;
- categoria 4: maximum 15 euro/oră.

Evaluarea actuală:

| Funcție | Tarif calculat | Verdict |
|---|---:|---|
| Coordonator tehnic | ~49,4 €/oră | Acceptabil numai cu doctorat/experiență specifică de categoria 1 |
| Expert AI/ML | ~43,6 €/oră | Neconform dacă nu îndeplinește categoria 1 |
| Expert embedded | ~43,6 €/oră | Neconform dacă nu îndeplinește categoria 1 |
| Expert robotică/sector | ~29,1 €/oră | Posibil categoria 2, dar experiența „peste 3 ani” nu susține automat tariful |
| QA/securitate | ~14,5 €/oră | Poate intra la categoria 4 |

Bogdan Pintea ar putea susține categoria 1, având doctorat și experiență relevantă, dacă este nominalizat efectiv ca expert/coordonator și are relația contractuală eligibilă. Pentru ceilalți experți nu este demonstrată categoria salarială.

Important: experiența necesară pentru punctajul echipei nu este identică cu experiența necesară pentru plafonul salarial.

Dacă experții AI și embedded rămân în categoria 2, remunerația lor trebuie redusă la maximum aproximativ 35 euro/oră. Aceasta poate reduce cheltuiala salarială eligibilă și grantul cu circa 56.000–60.000 euro. Diferența trebuie acoperită prin:

- alte ore reale de cercetare ale unor specialiști eligibili;
- un expert suplimentar necesar și justificat;
- sau echipamente suplimentare, caz în care crește cofinanțarea.

Bugetul salarial trebuie reconstruit în lei, pornind de la:

- salariul brut și contribuțiile eligibile;
- numărul efectiv de ore productive;
- procentul de alocare în proiect;
- fișa postului;
- categoria din Anexa 9;
- activitățile și livrabilele fiecărei persoane.

## 5. Minimis – plafon utilizat integral, dar repartizarea este vulnerabilă

Cei 300.000 euro sunt utilizați integral:

- marketing: 120.000 euro;
- informare și publicitate: 30.000 euro;
- audit/securitate/GDPR: 60.000 euro;
- management: 90.000 euro.

Probleme:

- website-ul de produs de 22.000 euro și website-ul proiectului de 8.000 euro pot fi considerate suprapunere;
- 30.000 euro pentru publicitate obligatorie este ridicat;
- 60.000 euro pentru audit/securitate/GDPR trebuie împărțit în servicii și livrabile distincte;
- lipsesc sau nu au buget clar: accesibilitate, certificări, autorizări, proprietate intelectuală și pregătirea documentațiilor;
- plafonul de minimis este ocupat integral, deci nu mai există rezervă;
- trebuie verificat plafonul de minimis la nivel de întreprindere unică.

Aș redistribui o parte din publicitate și audit către:

- certificarea produsului;
- testare cybersecurity/penetration testing;
- accesibilitate;
- autorizări și conformitate;
- protecția proprietății intelectuale.

Această redistribuire nu schimbă cofinanțarea, dar îmbunătățește coerența și punctajul.

## Concluzie

Nu recomand depunerea pe listele actuale. Cele patru corecții obligatorii sunt:

1. Eliminarea cercetării contractuale de 250.000 euro dacă prioritatea este cofinanțarea minimă.
2. Refacerea salariilor pe categorii Anexa 9 și nominalizarea experților.
3. Unificarea liniei de producție, HPC și laboratorului într-o listă fără suprapuneri.
4. Obținerea a minimum două oferte comparabile pentru fiecare cheltuială, inclusiv servicii, și completarea centralizatorului din Anexa 7.

Până nu există ofertele și justificările tehnice, nu se poate acorda calificativul „100% corect”; în special, punctajul aferent fundamentării bugetului rămâne nesecurizat.

## Asistent

Reiau evaluarea pe versiunea modificată și o compar cu concluziile anterioare. Voi verifica întâi ce fișiere s-au schimbat, apoi bugetul, echipamentele/laboratoarele, salariile, cofinanțarea și documentele suport, iar la final îți dau o listă prioritizată de sarcini.

## Asistent

Am identificat modificările principale din 13 iulie: un buget nou „EVA_Buget_FINAL”, Anexa 16 și completări în secțiunile MySMIS privind capacitatea, localizarea, investiția, documentațiile și rezultatele. Acum verific dacă valorile și textele sunt corelate între ele, nu doar dacă fișierele au fost completate.

## Asistent

Prima corecție majoră este confirmată: cofinanțarea eligibilă a fost redusă la 942.857 euro, dar noul fișier are necorelări interne între lista de echipamente, buget și Anexa 16. Mai important, documentul „Activități proiect” a rămas pe vechiul scenariu de 4,300 milioane euro și contrazice bugetul final. Verific acum și temeiul exact pentru finanțarea integrală a echipamentelor CDI la 80%, deoarece aici este riscul financiar cel mai mare.

## Asistent

Am reverificat fișierele modificate la 13.07.2026. Proiectul este mai bine structurat, dar bugetul de 942.857 euro cofinanțare nu este încă defensabil în forma actuală. Riscul principal este trecerea întregului HPC și laboratorului la ajutor CDI 80%, deși pentru echipamentele CDI este eligibilă, de regulă, numai amortizarea aferentă utilizării în proiect.

## Ce s-a îmbunătățit

- A fost eliminată cercetarea contractuală de 250.000 euro finanțată integral din surse proprii.
- Grantul este fixat la 3.000.000 euro.
- A fost creată o listă unificată de echipamente.
- Au fost eliminate unele suprapuneri de metrologie.
- Patru experți tehnici sunt nominalizați.
- A fost actualizată [Anexa 16](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/4. Dosar depunere (de completat)/04 - Anexa 16 corelare + buget defalcat.xlsx>).
- Au fost completate parțial cinci secțiuni MySMIS.
- Cofinanțarea eligibilă teoretică a scăzut de la aproximativ 1,301 milioane euro la 942.857 euro.

## Probleme critice noi sau rămase

### 1. Cofinanțarea de 942.857 euro este construită pe o încadrare riscantă

În [EVA_Buget_FINAL.xlsx](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/3. Buget/EVA_Buget_FINAL.xlsx>) sunt încadrate la CDI 80%:

- clusterul HPC;
- kiturile Jetson și FPGA;
- laboratorul electronic;
- stațiile CAD/CAE/EDA;
- instrumentele de testare.

Conform documentelor oficiale, dacă echipamentele CDI nu sunt utilizate în proiect pe întreaga durată de viață, este eligibilă numai amortizarea corespunzătoare duratei proiectului. Prin urmare, nu se poate lua automat 80% din prețul integral de achiziție.

Propunerea mea este:

- HPC utilizat ulterior pentru producție/exploatarea produsului: ajutor regional 70%, preț integral;
- laborator strict CDI: ajutor CDI, dar numai amortizarea eligibilă;
- echipamente de control al producției: ajutor regional 70%;
- kituri de dezvoltare Jetson/VEK280: CDI/amortizare sau cheltuială neeligibilă, după utilizare.

Varianta prudentă, cu tot hardware-ul achiziționat integral pe ajutor regional, conduce din nou la o cofinanțare eligibilă de aproximativ **1,051 milioane euro**. Diferența față de scenariul actual este aproximativ 108.000 euro, dar această variantă este mult mai sigură.

### 2. Lista de echipamente nu se închide cu bugetul

| Element | Lista echipamente | Buget |
|---|---:|---:|
| Producție eligibilă | 2.130.000 € | 2.142.857 € |
| HPC + laborator eligibil | 766.850 € | 756.000 € |
| Faza 2 | 580.000 € | 577.993 € |

Diferențele sunt generate și prin valori introduse manual în formule. Nu există o corespondență exactă „echipament–valoare–tip ajutor–ofertă–activitate”.

### 3. Salariile nu sunt încă validate

Situația corectă este:

- Dr. Mihai Jalobeanu: categoria 1 este plauzibilă, cu documente justificative.
- Adrian Potra: experiența de peste 20 ani nu îi acordă automat categoria 1 dacă este doar expert. Pentru 43,6 euro/oră trebuie doctorat + peste 10 ani sau o încadrare reală ca director de proiect cu peste 15 ani.
- Cristina Potra: aceeași problemă.
- Bogdan Pintea: experiența de peste 15 ani nu este suficientă automat pentru categoria 1 dacă rolul este „expert business/sectorial”.
- QA/Security: apare categoria 2 cu doar peste 2 ani experiență. Tariful de 14,5 euro/oră se încadrează mai sigur în categoria 4.
- Responsabilul financiar nu este nominalizat.

Mai există necorelări de durată:

- salariile tehnice sunt bugetate 24 luni;
- Anexa 16 indică A1 în lunile L1–L20;
- documentul vechi de activități indică L1–L18;
- managementul este bugetat 18 luni, dar activitatea apare L1–L24.

### 4. Documentul „Activități proiect” a rămas pe bugetul vechi

[3.1 Activități Proiect](<Z:/00. Proiecte 2026 - SCRIEM/2026.09.30 Acțiunea 2.1 POCIDIF/P1. Dancorproiect SRL/mysmis/3.1 Activitati Proiect.docx>) conține în continuare:

- cercetare contractuală de 250.000 euro;
- producție de 2.500.000 euro;
- HPC regional de 506.850 euro;
- cost eligibil total 4.300.850 euro;
- cofinanțare 1.300.855 euro;
- vechiul calendar al activităților.

Afirmația din document că sumele coincid cu bugetul și Anexa 16 este, momentan, falsă.

### 5. Dashboardul are indicatori calculați diferit față de Anexa 16

Bugetul final arată:

- activitate de bază: 90%;
- personal propriu/bază: 22%.

Anexa 16 arată:

- activitate de bază: 94%;
- personal propriu/bază: 21,1%.

Anexa 16 include corect promovarea/go-to-market în activitatea de bază. Dashboardul trebuie corectat la 94% și 21,1%.

### 6. Capacitatea financiară prezentată este incompletă

Creditul de 942.857 euro acoperă numai cofinanțarea eligibilă din scenariul actual. Nu acoperă:

- Faza 2: aproximativ 580.000 euro;
- renovarea halei: până la 781.666 euro;
- TVA;
- decalajul până la rambursare;
- eventualele cheltuieli respinse;
- capitalul de lucru;
- dobânzile și comisioanele din implementare.

Necesarul total potențial poate depăși **2,3 milioane euro plus TVA și decalajul de rambursare**. Modelul financiar actual nu reflectă acest necesar.

### 7. Codul CAEN și locația nu sunt rezolvate

Noile texte declară:

> „6210 + 2611/2612”

Dar în documentele societății analizate anterior:

- 2611 și 2612 nu apar;
- hala Emil Racoviță nr. 9 nu apare încă drept punct de lucru autorizat;
- 6210 trebuie autorizat la locația proiectului;
- trebuie ales codul CAEN efectiv corespunzător fabricării robotului, fără a menționa în cerere coduri pe care societatea nu le are.

Fără certificat constatator actualizat, aceasta rămâne problemă de eligibilitate.

### 8. Secțiunile MySMIS sunt în mare parte goale

Au fost completate parțial secțiunile 1, 2, 11, 12 și 13. Au rămas practic necompletate:

- obiectivele;
- justificarea și relevanța;
- durabilitatea;
- riscurile;
- grupul-țintă;
- principiile orizontale;
- metodologia;
- maturitatea proiectului;
- analiza cererii și analiza opțiunilor.

Planul de afaceri și cererea de finanțare sunt încă doar schelete.

## Lista nouă de sarcini

### Prioritatea 0 – înainte de continuarea redactării

1. **Decizie definitivă privind încadrarea echipamentelor**

   Regional integral versus CDI prin amortizare, pentru fiecare poziție.

2. **Refacerea bugetului master**

   O singură listă cu cod unic, denumire, cantitate, ofertă, cost în lei/euro, tip ajutor, intensitate, grant, cofinanțare, activitate și lună de achiziție.

3. **Închiderea diferențelor numerice**

   Corectarea valorilor 2.130.000/2.142.857, 766.850/756.000 și 580.000/577.993.

4. **Recalcularea cofinanțării reale**

   Recomand scenariul prudent de aproximativ 1,051 milioane euro cofinanțare eligibilă, până când amortizarea CDI este demonstrată.

5. **Rezolvarea CAEN și a punctului de lucru**

   Act constitutiv, autorizare cod eligibil la Emil Racoviță nr. 9 și certificat constatator nou.

### Prioritatea 1 – eligibilitate și punctaj eliminatoriu

6. **Validarea fiecărui expert pe Anexa 9**

   Diplome, doctorat/master, experiență, rol, tarif și relație de muncă.

7. **Nominalizarea QA/Security și a responsabilului financiar**

   CV, diplome și declarații de conflict de interese.

8. **Plan concret de diseminare**

   Este necesar pentru justificarea intensității CDI de 80%: conferințe, publicații, registre open-access/open-source sau angajament de licențiere admis de ghid.

9. **Raportul expertului extern de inovare**

   Pentru noutate, comparație internațională și delimitarea cercetării industriale de dezvoltarea experimentală.

10. **Dovezi de maturitate**

   Prototip existent, fotografii, video, rapoarte de testare și demonstrarea nivelului de pornire.

11. **Scrisori de interes și protocol pilot**

   Minimum trei LOI din sectoare diferite și cel puțin un protocol de pilotare.

### Prioritatea 2 – tehnic și buget

12. **BOM complet al robotului EVA**

   Fiecare reper produs intern trebuie legat de utilajul solicitat.

13. **Calcul de capacitate**

   Ore/utilaj, ciclu de fabricație, număr de roboți/an, grad de utilizare și make-or-buy.

14. **Layout pentru hala de 672 m²**

   Utilaje, fluxuri, laborator, HPC, depozitare, zonă ATEX, cuptoare, căi de acces și evacuare.

15. **Bilanț de utilități**

   Putere electrică, răcire HPC, aer comprimat, ventilație, gaze, exhaustare și PSI.

16. **Minimum două oferte pentru fiecare cheltuială eligibilă**

   Nu numai pentru „echipamentele majore”; inclusiv servicii, audit, marketing, licențe și publicitate.

17. **Corectarea fișelor HPC**

   Specificația H100, prețurile Jetson/VEK280, configurația GPU și calculul de workload.

### Prioritatea 3 – documentația finală

18. **Înlocuirea tuturor valorilor vechi**

   Eliminarea din toate documentele a scenariului 4.300.850 euro/1.300.855 euro.

19. **Completarea Cererii și Planului de afaceri**

   Acestea sunt încă schelete și nu pot susține punctajul.

20. **Refacerea proiecțiilor financiare**

   Cu renovare, Faza 2, TVA, credit, dobândă, decalaj de rambursare, capital de lucru și scenarii de vânzări.

21. **Actualizarea checklistului**

   Checklistul încă menționează cofinanțarea de 1,3 milioane euro și marchează unele probleme drept rezolvate deși nu sunt.

22. **Principii orizontale și accesibilitate**

   Bugetul este zero, iar secțiunea MySMIS este goală. Sunt necesare măsuri verificabile, responsabil, calendar și cost.

23. **Control de versiune**

   Un singur dosar „VERSIUNE CURENTĂ”, iar variantele vechi numai în arhivă. În prezent, documentele active se contrazic.

Concluzia mea: versiunea este o îmbunătățire reală, dar nu aș valida încă „grant 3 milioane/cofinanțare 942.857 euro”. Prima sarcină trebuie să fie refacerea încadrării HPC/laboratorului și închiderea bugetului master; altfel toate textele MySMIS vor trebui rescrise din nou.

## Asistent

Verific exact separarea dintre ajutorul regional și ajutorul CDI, fiindcă mesajul amestecă două regimuri diferite. Regula amortizării există, dar nu se aplică automat utilajelor CNC și liniei de producție încadrate pe ajutor regional. Verific și duratele/codurile din HG 2139/2004 înainte să confirm cifrele.

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-da168be7-f87c-441c-8041-a30e4b33e526",
  "query": "site:legislatie.just.ro HG 2139/2004 catalog masini unelte prelucrarea metalelor durata 8 12 ani ...",
  "action": {
    "type": "search",
    "query": null,
    "queries": [
      "site:legislatie.just.ro HG 2139/2004 catalog masini unelte prelucrarea metalelor durata 8 12 ani",
      "site:eur-lex.europa.eu Regulation 651/2014 Article 25 instruments equipment depreciation regional investment aid eligible costs full assets Article 14",
      "site:monitoruloficial.ro HG 2139 2004 catalog durata functionare calculatoare periferice 2 4 ani"
    ]
  },
  "results": null
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-22b56cf5-52f4-4bdc-8323-71dae7d85f72",
  "query": "'Where such instruments and equipment are not used for their full life for the project'",
  "action": {
    "type": "findInPage",
    "url": null,
    "pattern": "Where such instruments and equipment are not used for their full life for the project"
  },
  "results": null
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-c0171e5e-e3cf-4689-87b6-7223b5f36bba",
  "query": "",
  "action": {
    "type": "other"
  },
  "results": null
}
````

## Asistent

Este parțial adevărat, dar concluzia finală este greșită deoarece amestecă ajutorul CDI cu ajutorul regional.

## Regula corectă

### 1. Echipamente încadrate pe ajutor CDI – 80%

Da, pentru instrumentele și echipamentele încadrate la cercetare industrială/dezvoltare experimentală:

> dacă nu sunt utilizate pe întreaga lor durată de viață în proiect, este eligibilă numai amortizarea aferentă perioadei efective de utilizare în proiect.

Aceasta rezultă atât din Ghid, cât și din art. 25 alin. (3) lit. b din Regulamentul 651/2014. [Regulamentul UE 651/2014, art. 25](https://eur-lex.europa.eu/eli/reg/2014/651)

Important: perioada eligibilă nu este automat 24 luni. Dacă echipamentul este livrat și pus în funcțiune în luna 5, poate fi amortizat în proiect numai pentru lunile 5–24.

### 2. Utilajele încadrate pe ajutor regional – 70%

Pentru CNC, strung, danturare, EDM, rectificare, WAAM, cuptoare și echipamentele liniei de producție, dacă sunt încadrate corect ca investiție inițială pentru introducerea în producție:

- costul eligibil este prețul integral de achiziție;
- grantul este 70%;
- cofinanțarea este 30%;
- nu se limitează eligibilitatea la amortizarea din cele 24 luni.

Ajutorul regional permite costurile investiției în active corporale și necorporale, cu obligația menținerii investiției minimum trei ani în cazul IMM-urilor. [Regulamentul UE 651/2014, art. 14](https://eur-lex.europa.eu/eli/reg/2014/651)

Prin urmare, afirmația:

> „Dacă vrei echipamente de prelucrare nu poți deduce decât ce folosești în cele 24 luni”

este falsă pentru utilajele încadrate pe ajutor regional.

## Exemplu CNC de 250.000 euro

### Încadrare corectă – ajutor regional 70%

- cost eligibil: 250.000 euro;
- grant: 175.000 euro;
- cofinanțare: 75.000 euro.

### Încadrare CDI 80%, durată de viață 8 ani

Dacă ar fi instrument CDI și ar fi utilizat exact 24 luni:

- amortizare eligibilă: 250.000 × 2/8 = 62.500 euro;
- grant: 62.500 × 80% = 50.000 euro;
- diferența de achiziție suportată de firmă: 200.000 euro.

De aceea utilajele liniei de fabricație trebuie păstrate pe ajutor regional, nu mutate la CDI pentru a obține aparent 80%.

## Duratele de amortizare

Afirmația privind calculatoarele este corectă:

- cod 2.2.9 – calculatoare și periferice: **2–4 ani**.

Pentru mașini și utilaje pentru prelucrarea metalului există mai multe poziții, frecvent cu durate de:

- 2.1.5.2: **8–12 ani**;
- alte categorii 2.1.5: 5–9, 6–10, 9–15 ani, în funcție de utilaj.

[Catalogul oficial din HG 2139/2004](https://legislatie.just.ro/Public/DetaliiDocumentAfis/58613)

Dar afirmația că roboții umanoizi se încadrează automat la „automatizări, 3–5 ani” nu este confirmată de Catalog:

- roboții umanoizi nu au poziție distinctă;
- încadrarea trebuie făcută după funcția reală;
- „instalații pentru comandă și reglare automată” – cod 2.2.8 – are în Catalog **8–12 ani**, nu 3–5;
- calculatoare și periferice au 2–4 ani;
- echipamentele tehnologice pot avea alte durate.

Încadrarea robotului trebuie stabilită printr-o notă contabilă/tehnică, nu aleasă exclusiv pentru minimizarea amortizării.

## Ce înseamnă pentru EVA

| Echipamente | Încadrare recomandată |
|---|---|
| CNC, strung, danturare, EDM, rectificări | Regional 70%, cost integral |
| WAAM, cuptoare, ATEX, postprocesare | Regional 70%, cost integral |
| CMM/scanner utilizate în controlul producției | Regional 70%, cost integral |
| HPC folosit ulterior în producție/exploatare | Preferabil regional 70%, cost integral |
| HPC dedicat exclusiv cercetării | CDI 80%, numai amortizarea eligibilă |
| Osciloscoape, VNA, cameră climatică, laborator CDI | CDI 80%, de regulă amortizare |
| Jetson/VEK280 developer kits | CDI/amortizare, dacă sunt instrumente de dezvoltare |
| Materialele și componentele consumate în prototip | Pot fi cheltuieli CDI directe, nu neapărat active amortizabile |

Concluzia corectă: contribuția nu devine enormă pentru linia de prelucrare, deoarece aceasta poate fi finanțată regional la cost integral. Problema de amortizare afectează în primul rând cei 756.000 euro mutați în noul buget la „echipamente CDI 80%”. Acolo trebuie refăcută încadrarea echipament cu echipament.

## Asistent

Verific exact dacă ghidul impune un procent minim pentru ajutorul CDI ca tip de ajutor sau doar pentru activitatea de bază și personalul tehnic propriu. Sunt trei noțiuni diferite și nu trebuie confundate în buget.

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-0f53895e-5772-4bed-83e2-a5c2e78bfa05",
  "query": "PoCIDIF Acțiunea 2.1 ghid solicitant 20% personal propriu activitatea de bază CDI minimum 80% ...",
  "action": {
    "type": "search",
    "query": null,
    "queries": [
      "PoCIDIF Acțiunea 2.1 ghid solicitant 20% personal propriu activitatea de bază CDI minimum 80%",
      "site:mysmis2021.gov.ro PoCIDIF 2.1 ghid activitatea de bază personal propriu 20%",
      "site:mcid.gov.ro PoCIDIF Acțiunea 2.1 ghid solicitant cercetare dezvoltare 20%"
    ]
  },
  "results": null
}
````

## Asistent

Nu există o limită minimă distinctă pentru „total cheltuieli CDI” sau pentru „echipamente CDI”. Există însă două praguri obligatorii care generează indirect cheltuieli CDI.

## Pragurile obligatorii

1. **Activitatea de bază:** minimum 80% din grantul total.

La grant de 3.000.000 euro:

- grant activitate de bază minimum: **2.400.000 euro**.

În activitatea de bază intră CDI, introducerea în producție și introducerea în piață.

2. **Activitățile tehnice realizate cu personal propriu:** minimum 20% din grantul activității de bază.

În bugetul EVA actual:

- grant activitate de bază: **2.820.000 euro**;
- minimum personal tehnic propriu: 20% × 2.820.000 = **564.000 euro grant**;
- personal tehnic prevăzut: **595.200 euro grant**;
- pondere: **21,1%**.

Deci suntem peste minimum, dar marja este numai:

- 31.200 euro grant;
- echivalent cu aproximativ 39.000 euro cheltuială salarială la intensitate de 80%.

Regula de 80%/20% este prevăzută în [Ghidul final PoCIDIF 2.1](https://www.smart.org.ro/wp-content/uploads/Ghid-Actiunea-2.1-PoCIDIF.pdf).

## Ce nu este obligatoriu

Nu este obligatoriu să avem:

- 756.000 euro echipamente CDI;
- HPC încadrat la CDI;
- laborator încadrat integral la CDI;
- un anumit procent minim de echipamente CDI;
- cercetare contractuală.

Putem avea, de exemplu:

- personalul tehnic propriu pe CDI;
- toate echipamentele cumpărate integral pe ajutor regional, dacă sunt destinate investiției inițiale și introducerii în producție;
- fără echipamente CDI sau numai cu amortizarea instrumentelor strict experimentale.

## Structura prudentă pentru EVA

Aș recomanda:

- linie producție: regional 70%;
- HPC utilizat pentru produs/producție: regional 70%;
- controlul calității producției: regional 70%;
- laborator strict experimental: CDI 80%, numai amortizarea;
- personal tehnic propriu: CDI 80%, minimum 564.000 euro grant;
- promovare/go-to-market: minimis, activitate de bază;
- management, publicitate și audit: activități conexe/minimis.

Aș păstra personalul tehnic la minimum **595.200 euro grant**, deoarece o reducere salarială de peste 31.200 euro grant ar coborî proiectul sub pragul de 20%.

Concluzia: nu avem obligația să menținem cei 756.000 euro de echipamente CDI. Putem să le mutăm justificat pe ajutor regional și să păstrăm componenta CDI în principal prin personalul tehnic propriu.

## Asistent

Poți utiliza următorul prompt:

```text
Analizează și restructurează integral bugetul proiectului „EVA – Empathic Virtual Assistant”, depus de DANCOR PROIECT SRL în cadrul PoCIDIF – Acțiunea 2.1.

OBIECTIV PRINCIPAL

Realizează un plan de mutare a echipamentelor din categoria „Ajutor CDI – cercetare industrială, intensitate 80%” în categoria „Ajutor regional pentru investiții – intensitate 70%”, astfel încât:

1. să obținem grantul maxim de 3.000.000 euro;
2. să minimizăm cofinanțarea proprie;
3. să evităm riscul ca prețul integral al echipamentelor CDI să fie declarat neeligibil, fiind acceptată numai amortizarea aferentă utilizării în proiect;
4. să păstrăm la CDI numai serverele, stațiile de calcul și laptopurile pentru care poate fi justificată legal și contabil o durată de amortizare de 24 luni;
5. toate celelalte echipamente să fie analizate pentru încadrare pe ajutor regional la valoarea integrală de achiziție.

CONTEXT ȘI REGULI

- Durata proiectului este de maximum 24 luni.
- Pentru echipamentele încadrate pe ajutor CDI, dacă nu sunt utilizate pe întreaga durată de viață în proiect, este eligibilă numai amortizarea corespunzătoare perioadei efective de utilizare în proiect.
- Calculatoarele și echipamentele periferice pot avea, conform HG 2139/2004, cod 2.2.9, o durată normală de funcționare de 2–4 ani.
- Utilizarea duratei de 2 ani trebuie justificată prin politica contabilă, nota de încadrare a mijlocului fix, data punerii în funcțiune și utilizarea efectivă în proiect.
- Nu considera automat toate componentele HPC ca având durata de 2 ani. Serverele GPU, laptopurile, stocarea, rețeaua, UPS-ul, rackurile, răcirea și licențele trebuie analizate separat.
- Pentru un echipament pus în funcțiune după luna 1 nu presupune automat eligibilitatea amortizării integrale în cele 24 luni.
- Echipamentele încadrate pe ajutor regional trebuie să reprezinte active noi, parte a unei investiții inițiale și să fie necesare introducerii în producție a robotului EVA.
- Ajutorul regional este de 70%, iar ajutorul CDI pentru cercetare industrială este de maximum 80%, numai dacă sunt îndeplinite condițiile suplimentare pentru această intensitate.
- Grantul activității de bază trebuie să reprezinte minimum 80% din grantul total.
- Grantul pentru activitățile tehnice realizate de personalul propriu trebuie să reprezinte minimum 20% din grantul activității de bază.
- Valoarea personalului tehnic prevăzută în prezent este 744.000 euro, cu grant de 595.200 euro.
- Ajutorul de minimis este 300.000 euro.
- Grantul total urmărit este exact 3.000.000 euro.
- Cofinanțarea trebuie minimizată, dar fără încadrări artificiale sau neconforme.

BUGETUL ACTUAL

- Echipamente producție, ajutor regional 70%:
  cost eligibil 2.142.857 euro;
  grant 1.500.000 euro;
  cofinanțare 642.857 euro.

- Echipamente CDI – HPC și laborator:
  cost eligibil 756.000 euro;
  grant calculat la 80%: 604.800 euro;
  cofinanțare 151.200 euro.

- Personal tehnic propriu CDI:
  cost eligibil 744.000 euro;
  grant 595.200 euro;
  cofinanțare 148.800 euro.

- Minimis:
  cost eligibil și grant 300.000 euro.

- Total actual:
  cost eligibil 3.942.857 euro;
  grant 3.000.000 euro;
  cofinanțare 942.857 euro.

ECHIPAMENTE CARE TREBUIE ANALIZATE

A. Cluster HPC:

1. nod GPU cu 4 × NVIDIA H100;
2. nod GPU cu 4 × NVIDIA L40S;
3. nod cu 2 × RTX 6000 Ada;
4. nod head/management;
5. stocare NVMe de aproximativ 100 TB;
6. rețea InfiniBand/200GbE;
7. kituri NVIDIA Jetson AGX Thor;
8. plăci FPGA AMD Versal VEK280;
9. rack, PDU, UPS și răcire;
10. licențe AI/MLOps și simulare;
11. eventuale laptopuri și stații mobile necesare echipei tehnice.

B. Laborator:

1. osciloscoape, analizoare logice și generatoare;
2. analizor de spectru și VNA;
3. surse programabile, sarcini electronice și multimetre;
4. stații de lipire/rework, reflow și microscop;
5. prototipare PCB;
6. cameră climatică și sistem de testare la vibrații;
7. mașină de încercări materiale și durimetru;
8. stații de proiectare și licențe CAD/CAM/CAE/EDA.

C. Producție:

1. CNC 5 axe;
2. strung CNC turn-mill;
3. mașină de danturat;
4. Wire EDM;
5. rectificări;
6. ferăstrău;
7. scule și presetter;
8. WAAM/DED;
9. Binder Jet;
10. cuptoare;
11. stație ATEX;
12. postprocesare;
13. CMM;
14. scanner 3D și rugozimetru;
15. sisteme auxiliare.

SCENARIUL SOLICITAT

1. Păstrează la ajutor CDI numai:

- serverele și nodurile de calcul care pot fi încadrate justificat la codul 2.2.9;
- laptopurile și stațiile de calcul care pot avea justificat o durată contabilă de 24 luni;
- numai amortizarea efectiv eligibilă pentru perioada dintre punerea în funcțiune și finalizarea proiectului;
- licențele strict CDI, tratate separat în funcție de natura lor contabilă și durata abonamentului.

2. Analizează mutarea pe ajutor regional a:

- infrastructurii HPC utilizate după proiect pentru antrenarea, actualizarea, validarea și operarea comercială a robotului EVA;
- stocării și infrastructurii de rețea;
- rackurilor, UPS-urilor și răcirii;
- echipamentelor laboratorului care vor fi folosite permanent pentru testarea, validarea și controlul calității produselor fabricate;
- tuturor utilajelor de producție și metrologie;
- stațiilor CAD/CAM/CAE folosite în fluxul permanent de proiectare și fabricație.

3. Pentru Jetson AGX Thor și AMD VEK280 stabilește separat dacă sunt:

- instrumente CDI supuse amortizării;
- componente ale prototipului;
- active regionale utilizate în procesul permanent de producție;
- sau cheltuieli care trebuie scoase din proiect.

4. Nu încadra automat la ajutor regional echipamentele folosite exclusiv pentru cercetare. Pentru fiecare poziție prezintă justificarea funcțională și riscul de neeligibilitate.

REZULTATE SOLICITATE

Livrează următoarele:

1. Un tabel „situație actuală versus situație propusă”, cu:

- echipament;
- valoare;
- încadrare actuală;
- încadrare propusă;
- cod de amortizare;
- durată de amortizare;
- lună estimată de punere în funcțiune;
- număr de luni utilizate în proiect;
- valoare eligibilă;
- intensitatea ajutorului;
- grant;
- cofinanțare;
- justificare;
- risc de neeligibilitate.

2. Un buget consolidat recalculat, cu:

- total ajutor regional;
- total CDI – personal;
- total CDI – amortizare echipamente;
- total minimis;
- grant total;
- cofinanțare totală;
- cheltuieli neeligibile;
- TVA;
- necesar de cash până la rambursare.

3. Minimum trei scenarii:

- Scenariul A – prudent: majoritatea hardware-ului pe ajutor regional;
- Scenariul B – echilibrat: serverele pe CDI prin amortizare, restul regional;
- Scenariul C – cofinanțare minimă: maximum posibil pe CDI, dar numai în limite legale și contabile.

4. Recomandă scenariul cu:

- cel mai mic risc de corecție financiară;
- grant exact 3.000.000 euro;
- cofinanțare minimă realistă;
- respectarea pragului de minimum 20% pentru personalul tehnic propriu.

5. Calculează dacă este realistă amortizarea integrală în 24 luni pentru fiecare server sau laptop. Nu accepta simpla alegere a duratei minime de 2 ani dacă echipamentul este pus în funcțiune după începerea proiectului.

6. Prezintă documentele justificative necesare:

- decizie privind politica contabilă;
- notă contabilă de încadrare;
- proces-verbal de punere în funcțiune;
- registrul mijloacelor fixe;
- plan de utilizare în proiect;
- fișă tehnică;
- două oferte;
- justificarea încadrării pe ajutor regional;
- justificarea caracterului de investiție inițială;
- justificarea utilizării productive după finalizarea proiectului.

7. Identifică toate modificările care trebuie propagate în:

- EVA_Buget_FINAL.xlsx;
- lista unificată de echipamente;
- Anexa 6 – buget defalcat;
- Anexa 7 – centralizator oferte;
- Anexa 16 – corelare buget-activități;
- activitățile proiectului;
- Cererea de finanțare;
- Planul de afaceri;
- proiecțiile financiare;
- descrierea investiției;
- capacitatea financiară și tehnică.

CONDIȚIE FINALĂ

Nu optimiza bugetul exclusiv matematic. Orice mutare între CDI și ajutor regional trebuie să fie susținută de funcția reală a echipamentului, tratamentul contabil, perioada de utilizare și activitatea din proiect.

Dacă grantul de 3.000.000 euro nu poate fi obținut cu cofinanțarea de 942.857 euro în condiții sigure, determină cofinanțarea minimă realistă și explică diferența.
```

## Asistent

Verific în ghidul final plafoanele cumulative, deoarece minimisul are atât plafonul european de 300.000 euro la nivel de întreprindere unică, cât și limite interne ale apelului pentru anumite categorii. Apoi separ cheltuielile eligibile de cele care doar par „servicii generale”.

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-7e4b35e3-3d2c-4fe2-bbc7-24ecdbbd6599",
  "query": "",
  "action": {
    "type": "other"
  },
  "results": null
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-0126e6c4-6e8f-4efe-8d5a-6b67af9d9d07",
  "query": "",
  "action": {
    "type": "other"
  },
  "results": null
}
````

## webSearch

````json
{
  "type": "webSearch",
  "id": "exec-d207d9a1-e442-453c-b0bb-8104ea0bf404",
  "query": "'3.4. Rata de cofinanțare'",
  "action": {
    "type": "findInPage",
    "url": null,
    "pattern": "3.4. Rata de cofinanțare"
  },
  "results": null
}
````

## Asistent

## Cofinanțarea pentru minimis

Intensitatea ajutorului de minimis este **100%**. Pentru o cheltuială eligibilă de minimis:

- cost eligibil: 100.000 euro;
- grant: 100.000 euro;
- cofinanțare eligibilă: **0 euro**.

Totuși, firma trebuie să poată suporta temporar plata până la rambursare și orice TVA deductibilă, depășire de preț sau cheltuială declarată neeligibilă. [Ghidul final, secțiunea 3.4](https://www.smart.org.ro/wp-content/uploads/Ghid-Actiunea-2.1-PoCIDIF.pdf)

## Cât poate fi ajutorul de minimis

Maximum:

> **300.000 euro pentru întreprinderea unică, într-o perioadă continuă de trei ani.**

Calculul se face la nivel de „întreprindere unică”, deci trebuie incluse și firmele legate/controlate, nu numai DANCOR PROIECT SRL.

Formula este:

**Minimis disponibil = 300.000 euro − ajutoarele de minimis primite de întreprinderea unică în ultimii trei ani.**

Dacă verificarea confirmă că DANCOR și firmele legate au primit zero minimis, proiectul poate utiliza integral **300.000 euro**. [Ghidul final, secțiunea 5.3.2](https://www.smart.org.ro/wp-content/uploads/Ghid-Actiunea-2.1-PoCIDIF.pdf)

Mai există o limită specială:

- consultanța de la categoria B.2;
- plus managementul intern de la categoria B.5;

nu pot depăși împreună 10% din valoarea maximă eligibilă aferentă proiectului și trebuie să rămână în plafonul total de 300.000 euro.

## Cheltuieli eligibile pe minimis

### 1. Informare, promovare și introducere în piață

- panouri, plăci, afișe și alte elemente obligatorii de vizibilitate;
- pagina proiectului;
- promovarea și comercializarea robotului EVA;
- realizarea website-ului comercial;
- platforme de marketing;
- listări marketplace;
- instrumente analytics;
- campanii digitale;
- colaborare și networking;
- participare la conferințe și evenimente;
- publicarea și diseminarea rezultatelor;
- registre open-access;
- programe gratuite sau open-source.

Promovarea/comercializarea și diseminarea rezultatelor sunt considerate activitate de bază.

### 2. Consultanță, avize și certificări

- elaborarea Cererii de finanțare;
- elaborarea Planului de afaceri;
- raportul expertului extern;
- consultanță pentru implementare și management;
- documentații pentru achiziții;
- asistență juridică aferentă achizițiilor;
- acorduri, avize și autorizații;
- certificarea produsului;
- obținerea, validarea și protejarea brevetelor;
- protecția altor active necorporale.

Consultanța pentru documentația de depunere și raportul expertului extern pot reprezenta excepția permisă anterior depunerii, cu respectarea exactă a condițiilor ghidului.

### 3. Instruire și formare

- instruirea utilizatorilor cărora le este destinat robotul;
- instruirea personalului beneficiarului care va asigura mentenanța;
- formare profesională specifică produsului dezvoltat.

Nu intră automat cursurile generale fără legătură directă cu EVA.

### 4. Audit tehnic și securitate

- auditul tehnic final;
- verificarea corespondenței rezultatului cu Cererea de finanțare;
- verificarea gradului de inovare;
- audit cybersecurity;
- penetration testing;
- protecția informațiilor;
- verificarea GDPR și a datelor personale.

Auditorul trebuie să aibă certificare profesională avansată recunoscută, precum CISA, CISM, CISSP, CCSP, CIPP/E, ISO 27001 Lead Auditor sau OSCP.

### 5. Management intern

- salariile managerului de proiect;
- salariile responsabilului financiar/achiziții;
- deplasările personalului de management;
- transportul bunurilor justificat de proiect;
- echipamente TIC numai pentru echipa de management.

Nu se pot deconta simultan aceleași activități prin management externalizat și management intern.

### 6. Accesibilitate

- display-uri și cititoare Braille;
- adaptarea interfețelor web;
- interfață accesibilă pentru robot;
- conținut multimedia accesibil;
- aplicații mobile accesibile;
- alte tehnologii asistive justificate.

### 7. Cheltuieli indirecte – maximum 7%

- contabilitate;
- recrutare;
- curățenie;
- telefon și internet;
- apă, energie, gaze și salubritate;
- servicii poștale și curierat;
- chirie;
- alte costuri indirecte necesare proiectului.

Acestea intră tot în plafonul de minimis de 300.000 euro și nu pot dubla cheltuieli directe deja bugetate.

## Ce nu putem muta pe minimis

În mod obișnuit, nu se pot muta pe minimis:

- CNC, strunguri și utilaje de producție;
- HPC și serverele tehnice;
- echipamentele laboratorului CDI;
- laptopurile experților tehnici;
- renovarea generală a halei;
- materiile prime pentru producție;
- salariile cercetătorilor și experților tehnici;
- dobânzile creditului;
- TVA deductibilă.

Excepțiile pentru echipamente sunt limitate la echipamente TIC destinate managementului și echipamente de accesibilitate.

## Situația EVA

Bugetul actual utilizează exact plafonul:

| Categorie | Valoare |
|---|---:|
| Promovare/go-to-market | 120.000 € |
| Informare și publicitate | 30.000 € |
| Management intern | 90.000 € |
| Audit/securitate/GDPR | 60.000 € |
| **Total minimis** | **300.000 €** |
| **Grant** | **300.000 €** |
| **Cofinanțare** | **0 €** |

Structura este permisă ca tipuri de cheltuieli, dar aș redistribui o parte din cei 30.000 euro de publicitate și 60.000 euro de audit către:

- certificarea robotului;
- accesibilitate;
- avize și autorizări;
- protecția proprietății intelectuale;
- testarea formală de securitate.

Astfel păstrăm grantul de 300.000 euro și cofinanțarea zero, dar construim un buget mai ușor de justificat și mai util proiectului.
