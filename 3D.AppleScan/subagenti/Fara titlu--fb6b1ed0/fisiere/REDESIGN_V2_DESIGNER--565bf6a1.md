# Redesign EVA-3dScan — perspectiva designerului de interior

Data: 2 octombrie 2026. Agent: `designer_v2`. Stare: evaluarea de conținut și structură încheiată; implementarea și testarea vizuală rămân în responsabilitatea echipei principale.

Aceasta este o evaluare de rol simulată, nu un interviu cu un designer, un studiu de utilizabilitate sau o validare a preciziei aplicației.

## Materiale citite

- `docs/REDESIGN_V2_BRIEF.md`: ierarhie, fluxuri, criterii și statutul produsului.
- `content/redesign-v2-source.json`: textele propuse în română și engleză, inclusiv toate cheile `v2.designer*`.
- `public/app.js`: structura home existentă. La momentul inspecției, noul layout V2 nu era încă implementat aici.

## Ce vreau să înțeleg înainte să folosesc aplicația

1. **Ce primesc după vizita la client?** Vreau să văd camera existentă și dimensiunile relevante, nu doar o fotografie frumoasă sau o animație de scanare. Exemplul trebuie să arate un rezultat pe care îl pot consulta ulterior.
2. **Pot verifica dacă încape mobilierul?** Vreau să înțeleg legătura dintre lățimea obiectului, spațiul disponibil și trecere. Dimensiunile unui obiect și dimensiunile camerei trebuie prezentate împreună într-un caz concret.
3. **Ce verific eu la fața locului?** Golurile, distanțele și cotele importante trebuie confirmate înainte de comandarea mobilierului. Nu solicit o precizie numerică inventată; solicit o explicație vizibilă despre cotele de control.
4. **Cum continui proiectarea și cum discut cu clientul?** Site-ul trebuie să distingă rezultatul scanării de amenajarea creată ulterior. Formatul disponibil sau planificat și următorul instrument folosit trebuie explicate lângă exemplu.
5. **Ce se salvează și ce telefon îmi trebuie?** Vreau să știu că proiectul de camere este un flux salvat, diferit de măsurarea temporară, și unde găsesc cerințele hardware. Stadiul în dezvoltare trebuie să fie clar înainte să caut instalarea.

## Povestea de utilizare

**Situație:** un cuplu dorește o amenajare nouă a livingului și vrea să păstreze o piesă de mobilier.

**Pasul 1 — spațiul existent.** Designerul capturează camera, golurile și contextul. Pe site se vede o încăpere identificabilă și reprezentarea ei digitală demonstrativă.

**Pasul 2 — piesa care trebuie păstrată.** Obiectul este asociat cu dimensiunile sale. Exemplul evidențiază o cotă relevantă și spațiul liber din jur, fără a afirma că produsul detectează automat toate obstacolele.

**Pasul 3 — proiectarea.** Designerul folosește referința în instrumentul ales, verifică amplasarea și discută varianta cu clientul. Designul nou este o etapă realizată de designer. Site-ul nu trebuie să sugereze generarea automată a amenajării sau o verificare automată garantată a circulației.

**Livrabilul concret explicat:** camera existentă și dimensiunile relevante, ca referință pentru amplasarea mobilierului și discuția cu clientul. Exemplele de pe site sunt sintetice; livrarea efectivă din aplicație rămâne planificată.

## Recomandări pentru textele V2

| Cheie | Evaluare / text recomandat |
|---|---|
| `v2.designer` | Păstrează „Designer de interior”. |
| `v2.designerTitle` | Păstrează „Încape ideea în cameră?”. Leagă imediat o intenție de o problemă concretă. |
| `v2.designerNeed` | Textul curent despre mobilier și spațiul de trecere este relevant. Nu îl extinde cu promisiuni despre randări sau stiluri generate automat. |
| `v2.designerSteps` | „Scanezi camera existentă\|Verifici dimensiunile mobilierului\|Compari amplasarea în proiect”. „Înregistrezi” este prea general, iar „spații libere” devine mai clar când este legat de amplasare. |
| `v2.designerDeliverable` | „Camera existentă și dimensiunile relevante, ca referință pentru amplasarea mobilierului și discuția cu clientul. Amenajarea se dezvoltă apoi în instrumentul de proiectare ales.” |

Echivalent recomandat în engleză pentru pași: “Capture the existing room\|Check furniture dimensions\|Compare placement in the design”. Pentru rezultat: “The existing room and relevant dimensions, as a reference for furniture placement and client discussions. Develop the interior proposal in your chosen design tool.”

## Ce trebuie văzut în layout

- Păstrează imaginea aprobată cu designerul și cuplul. Alătură un rezultat vizibil: planul camerei, conturul unui mobilier și o cotă. Personajele oferă context; rezultatul arată utilitatea.
- Arată traseul „camera existentă → dimensiuni → amplasare”, cu trei etichete scurte și legibile. Nu ascunde pașii într-un carusel care se schimbă singur.
- Delimitează exemplul de design de fotografia cu maistrul și reparațiile. Designerul răspunde la amplasare și discuția cu clientul; maistrul la intervenții și lucrare.
- Folosește un CTA către fluxul de camere sau cazul relevant din catalog. Un link către dosarul tehnic poate fi secundar.
- Pe mobil, ordinea recomandată este problemă, rezultat vizual, trei pași, CTA. Evită un bloc lung de text înainte de primul rezultat.

## Cinci criterii de acceptare

| ID | Criteriu măsurabil | Verificare cerută |
|---|---|---|
| DES-01 | Zona designer numește camera existentă, mobilierul și un rezultat folosibil; are exact un traseu principal cu trei pași. | Inspecție text / DOM în toate cele șapte limbi. |
| DES-02 | Imaginea designerului cu cuplul este păstrată, iar rezultatul ilustrativ include cel puțin un contur de cameră, un obiect și o cotă lizibilă. | Capturi desktop și mobil; marcaj de exemplu sintetic lângă vizual. |
| DES-03 | Un CTA executabil duce către pagina de camere sau un caz de amenajare; linkul are destinația corectă și funcționează cu tastatura. | Click, Tab și Enter în browser. |
| DES-04 | Zero afirmații că aplicația produce automat designul, garantează încadrarea mobilierului ori a validat o precizie numerică. | Audit al textului și al etichetelor vizuale din zona designer. |
| DES-05 | La 390 px și 1440 px, întrebarea, vizualul, pașii și CTA sunt lizibile, fără suprapuneri sau derulare orizontală; reparațiile sunt distincte de amenajare. | Capturi și test de layout; verificarea celor două scene. |

## Decizie și reluare

Direcția brief-ului este potrivită pentru designer, cu ajustarea pașilor și a livrabilului de mai sus. Prioritatea este dovada vizuală a rezultatului. Nu aprob aici implementarea, deoarece fișierul inspectat încă prezenta structura veche.

Următorul pas: echipa principală integrează formulările și rezultatul ilustrativ, apoi auditorul verifică DES-01–DES-05 pe pagina randată. Nu este necesară o altă cercetare externă pentru această evaluare restrânsă a materialelor deja disponibile.
