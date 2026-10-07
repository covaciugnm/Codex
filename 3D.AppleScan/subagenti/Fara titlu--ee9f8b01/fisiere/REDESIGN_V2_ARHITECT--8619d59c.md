# Redesign V2 — perspectiva arhitectului

Data: 2 octombrie 2026. Autor: agentul `architect_v2`.

Aceasta este o evaluare de rol simulată, bazată pe brief și textele propuse. Nu este un interviu cu un arhitect, o certificare sau o validare a preciziei aplicației. Nu au fost modificate fișiere de cod ori dicționare.

## Ce trebuie să înțeleg în primele 10 secunde

„Este o aplicație iPhone în dezvoltare. Pot explora cum aș documenta spațiul existent, aș verifica dimensiunile și aș reuni camerele într-un proiect. Văd un rezultat cotat, apoi aflu cum îl pot folosi la proiectare.”

Imaginea arhitectului atrage atenția; un plan lizibil cu două camere, o ușă și cote cu unități îmi explică produsul. Un ecran cu puncte colorate ori un telefon ținut în mână nu demonstrează singur utilitatea pentru releveu.

## Cele cinci întrebări prioritare

1. **Ce primesc după captură?** Vreau să văd un exemplu de plan/model cu cote și camere legate, înaintea listei de formate.
2. **Pot avea încredere în scară?** Trebuie explicate unitățile, dimensiunile de control și faptul că precizia EVA-3dScan nu este încă validată.
3. **Cum leg încăperile?** Vreau o schemă care arată poziția relativă a camerelor și verificarea trecerii dintre ele. „Camere conectate” trebuie să fie vizibil, nu doar un slogan.
4. **Cum continui în programul meu?** Disting între un model de referință, un desen CAD editabil și planșele de execuție. Vreau statutul formatelor lângă exemplu: planificat, condiționat de conversie, demonstrativ.
5. **Ce pot încerca acum?** Deschid o demonstrație sau un fișier exemplu; site-ul explică limpede că acesta este sintetic și aplicația este în dezvoltare.

## Flux concret propus

**Situație:** pregătesc renovarea unui apartament cu două camere și un hol.

| Pas | Intrare | Acțiune propusă în aplicație | Rezultat util | Probă necesară pe site |
|---|---|---|---|---|
| 1 | Spațiul existent și telefon compatibil | Captez camerele pe rând | Camere documentate în același proiect | Exemplu cu cel puțin două camere distincte |
| 2 | Dimensiuni măsurate independent | Compar cotele de control și verific unitățile | O referință a cărei scară o pot verifica | O cotă cu unitate și explicația controlului |
| 3 | Camerele și trecerile dintre ele | Revizuiesc legătura și poziția camerelor | Contextul apartamentului | Ușă sau trecere desenată între camere |
| 4 | Referința spațială verificată | Pregătesc datele pentru instrumentul de proiectare | Bază de lucru pentru releveu și renovare | Formatele planificate și un exemplu etichetat |

Acesta este fluxul urmărit de produs, nu o descriere a unor funcții iPhone deja testate. În site, cele patru rânduri pot deveni trei pași: **Scanezi camerele → Verifici cotele și scara → Revizuiești planul de lucru**.

## Cote, scară și limite

- Dimensiunile demonstrative trebuie să aibă unitate; exemplul „4 × 3 m” este inteligibil fără a cere citirea documentației.
- O valoare sintetică nu dovedește precizia capturii. Eticheta demonstrației trebuie să rămână lângă rezultat și lângă descărcare.
- O cotă verificată independent este mai utilă pentru înțelegerea fluxului decât un procent de „încredere” inventat.
- Arhitectul trebuie să poată distinge geometria capturată de deciziile de proiectare. Modelul capturat nu dovedește structura portantă, starea instalațiilor sau defecte ascunse.
- Exportul CAD/DWG trebuie prezentat ca funcție planificată sau conversie condiționată, conform stării reale. Nu presupunem că orice mesh devine automat un desen CAD curat și editabil.
- Nu sunt necesare avertismente repetate în fiecare card. Un statut vizibil și o explicație scurtă lângă rezultat susțin o prezentare clară.

## Revizuirea cheilor `v2.architect*`

| Cheie | Decizie | Text recomandat RO | Text recomandat EN |
|---|---|---|---|
| `v2.architect` | Păstrează | Arhitect | Architect |
| `v2.architectTitle` | Păstrează | Adu spațiul existent în proiectul tău. | Bring the existing space into your design. |
| `v2.architectNeed` | Mică simplificare | Pregătești o renovare? Înțelege dimensiunile camerelor, golurile de uși și ferestre și legătura dintre spații. | Planning a renovation? Understand room dimensions, door and window openings, and how spaces connect. |
| `v2.architectSteps` | Fă scara explicită | Scanezi camerele\|Verifici cotele și scara\|Analizezi planul camerelor conectate | Capture the rooms\|Check dimensions and scale\|Review the connected layout |
| `v2.architectDeliverable` | Înlocuiește „tema de proiectare”, prea abstract | O referință cotată a spațiului existent, de verificat și completat în proiectare. Exporturile CAD sunt planificate; desenele editabile și planșele de execuție necesită prelucrare și verificare. | A dimensioned reference of the existing space, ready to be checked and developed in your design. CAD exports are planned; editable drawings and construction documents require further processing and review. |

Motivul corecției principale: „pentru tema de proiectare” nu spune suficient de concret ce face arhitectul cu rezultatul. „Planșele de execuție editabile cer prelucrare suplimentară” poate sugera că aplicația produce deja astfel de planșe. Textul propus explică direct utilizarea referinței și munca necesară ulterior.

## Cinci criterii de acceptare pentru site

| ID | Criteriu cuantificabil | Verificare propusă |
|---|---|---|
| ARC-01 | Primul traseu pentru arhitect prezintă problema, trei pași și un rezultat concret | Inspecție DOM și captură la 390 px și 1440 px |
| ARC-02 | Exemplul vizual arată minimum două camere, o trecere și minimum o cotă cu unitate | Inspecție vizuală; eticheta „demonstrativ” este vizibilă |
| ARC-03 | Textul traseului include verificarea cotelor și a scării | Compararea textului randat cu dicționarele; aceeași semnificație în cele șapte limbi |
| ARC-04 | Formatele planificate și exemplul sintetic sunt identificate înainte sau imediat lângă descărcare | Click pe exemplu; titlu, etichetă și fișier concordante |
| ARC-05 | Traseul conduce în cel mult un click la pagina camerelor ori la o demonstrație relevantă; zero promisiuni numerice de precizie nevalidate | Test al linkului și audit al afirmațiilor |

Acestea sunt criterii pentru implementare și audit, nu teste executate de acest agent. Validarea cu arhitecți reali rămâne o etapă distinctă: cinci participanți, identificarea produsului după 10 secunde și explicarea rezultatului fără ajutor. Ținta propusă este minimum patru răspunsuri corecte din cinci; rezultatul nu a fost măsurat.

## Predare și reluare

Intrări citite: `docs/REDESIGN_V2_BRIEF.md`, `content/redesign-v2-source.json`. Livrabile: acest raport și `docs/redesign-v2-architect.jsonl`. Următorul pas: managerul decide textele finale, implementarea le integrează, auditorul verifică ARC-01–ARC-05 pe site-ul randat. Starea acestei evaluări: **finalizată**.
