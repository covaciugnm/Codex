# Audit independent robotică și transport — R1

Data: 2026-10-02. Auditor: `doctoral_apple_perception`, în rol de auditor robotic independent de autorul `doctoral_robotics`. Domeniu: capitolele 06/07, Xacro, contractul ROS și registrul bibliografic robotic. Nu am modificat artefactele autorului. Auditul este documentar; nu certifică un robot, o rețea, o aplicație sau siguranța fizică.

## Verdict

**NEACCEPTAT pentru închiderea documentară: patru constatări deschise — două P1 și două P2.** Arhitectura separă corect percepția de controlul echilibrului și tratează explicit incertitudinea, resetările și datele persistente. Contractul de interfață conține însă ambiguități care trebuie eliminate înaintea implementării. „100%” va însemna toate criteriile de mai jos trecute și zero constatări documentare deschise, nu absența erorilor fizice viitoare.

Severitățile sunt de audit: P1 = defect contractual important ce poate altera observații/decizii; P2 = neconcordanță de specificație ce poate produce implementări incompatibile. Nu sunt prioritățile P0/P1/P2 ale produsului.

## Metodă și verificări efectuate

Am citit integral cele cinci artefacte. Xacro este XML bine format; conține o macrodefiniție cu parametri obligatorii, fără calibrare numerică inventată. JSON se parsează și descrie 12 topicuri. Nu am rulat expandarea Xacro, un compilator ROS, RViz sau un robot; acestea rămân verificări de implementare.

Am refăcut calculul debitului adâncimii: 256×192×4×15×8/10⁶ = 23,59296 Mbit/s. Exemplul temporal 60°/s × 0,020 s = 1,2° și aproximativ 42 mm la 2 m este consistent. Suma de bandă și distanța simplificată de frânare sunt aritmetic corecte, etichetate adecvat ca scenarii.

Surse primare reverificate în această rundă:

- [REP-120](https://raw.githubusercontent.com/ros-infrastructure/rep/master/rep-0120.rst): transformarea humanoidului către base_footprint nu este rigidă.
- [robot_state_publisher](https://raw.githubusercontent.com/ros/robot_state_publisher/rolling/README.md): model cinematic și joint_states; TF fix și mobil publicate separat.
- [ROS 2 Jazzy QoS](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Concepts/Intermediate/About-Quality-of-Service-Settings.rst): compatibilitate, istoric, durabilitate și evenimente; acestea nu constituie watchdog de aplicație.
- [ROS Clock and Time](https://raw.githubusercontent.com/ros2/design/gh-pages/articles/130_ros_time.md): timp de sistem, timp monoton și timp simulat; salturile cer tratament explicit.

## Grilă de criterii

| ID criteriu | Criteriu de acceptare documentară | Rezultat R1 | Evidență |
|---|---|---|---|
| RC01 | Transformări SE3, unități, autorități TF și montaj mobil/fix coerente | PASS | §6.2–6.4 și Xacro |
| RC02 | Calibrare și timp la captură distincte de recepție | PASS | §6.5 și §7.3 |
| RC03 | Regula formală de admitere respinge date viitoare/invalide și expirate | FAIL | ROB-A02 |
| RC04 | Fuziunea nu tratează sursele corelate sau covarianța necunoscută drept certe | PASS | §6.6 |
| RC05 | Hartă structurală separată de obstacole dinamice și spațiu necunoscut | PASS | §6.7–6.8 |
| RC06 | QoS limitat, prospețime la consum, fără promisiune hard realtime | PASS | §7.4 și profile JSON |
| RC07 | Identitatea mesajelor este unică între fluxuri | FAIL | ROB-A01 |
| RC08 | Duplicatele și conflictele hărții au identitate și conținut semantic neambigue | FAIL | ROB-A04 |
| RC09 | Stările catalogului se transmit fără pierdere între percepție și ROS | FAIL | ROB-A03 |
| RC10 | Reacția robotului nu confundă oprirea instantanee cu starea sigură | PASS | §6.8–6.9 |
| RC11 | Șabloanele și probele neexecutate sunt marcate explicit | PASS | Antete, `hardware_verified=false`, macro Xacro |
| RC12 | Sursele au proveniență și limite; nu se pretinde licențiere comercială validată | PASS | robotics_sources.json; pachete/codec încă decizii deschise |

Licențierea concretă a pachetelor și codec-urilor va necesita versiuni fixate și inventar de dependențe înaintea implementării/distribuției. În domeniul inspectat nu există afirmația falsă că acest audit de licențe a fost deja executat; nu o tratăm drept test trecut al produsului.

## Constatări și remedieri

### ROB-A01 — P1 — Coliziuni între fluxuri la deduplicare

**Evidență:** `01_capitole/07_Transport_si_harta_distribuita.md`, §7.2, declară număr de secvență independent pentru fiecare flux, dar cheia de deduplicare este perechea sesiune–secvență. În `04_contracte/ros_topics.json`, envelope are `stream_id`, fără regulă canonică de deduplicare.

**Contraexemplu:** RGB și depth din aceeași sesiune au fiecare `sequence=1`. Cheia descrisă este identică deși ambele mesaje sunt valide. Eliminarea unui duplicat poate elimina observația altui senzor.

**Remediere:** cheia trebuie să includă identitatea dispozitivului, sesiunea, fluxul și secvența. Specificați testul cu două fluxuri având aceeași secvență și un duplicat real în același flux. Actualizați proza și JSON.

### ROB-A02 — P1 — Formula de prospețime admite viitorul

**Evidență:** `04_contracte/ros_topics.json`, `admission.age_formula`, conține numai limita superioară a vârstei. §7.3 descrie intenția de a trata timpul aparent negativ drept problemă, dar nu formalizează condiția în contract.

**Contraexemplu calculat:** `age=-1 s`, `u=0,005 s`, `limit=0,1 s` trece inegalitatea existentă. O observație cu timp cu o secundă în viitor poate fi marcată proaspătă.

**Remediere:** precizați verificarea modelului temporal, a epocii, a valorilor finite, `u≥0` și limita admisă a incertitudinii. Introduceți limita inferioară `age≥-u` sau o regulă mai conservatoare explicită. Adăugați cazuri pentru viitor, expirare, overflow, valori invalide și model temporal expirat. O incertitudine estimată trebuie să aibă interpretare și prag, nu doar un număr arbitrar.

### ROB-A03 — P2 — Vocabularul de stare nu coincide cu percepția

**Evidență:** §7.7 și `topics[/eva/objects/state].states` folosesc `retired` și omit `ambiguous`. Capitolul 04 §4.6 definește `ambiguous` și `archived`. Regula din JSON solicită ambiguitate explicită, dar payloadul nu specifică valoarea sau câmpul.

**Remediere:** adoptați un vocabular canonic ori o mapare fără pierderi. Ambiguitatea poate fi câmp separat de starea de vizibilitate, dacă acest lucru este declarat; definiți și semantica `archived` versus `retired`. Adăugați verificarea round-trip dintre registrul de percepție și mesajul ROS.

### ROB-A04 — P2 — Hashul semantic al deltei este insuficient definit

**Evidență:** §7.6 vorbește despre cheia fragmentului și checksum; JSON cere `geometry_hash` și spune duplicate identificate prin key+hash. Nu este explicit dacă transformarea și revizia fac parte din hashul utilizat la detectarea conflictului.

**Contraexemplu:** două operații cu aceeași revizie și geometrie au transformări diferite. Hashul exclusiv al geometriei coincide; o implementare conformă interpretării înguste poate omite conflictul. DELETE nu are geometrie nouă, iar semantica câmpului obligatoriu nu este precizată.

**Remediere:** definiți cheia operației incluzând epoca, fragmentul și revizia; introduceți hash canonic al conținutului semantic, incluzând transformare, repere, operație și revizii. Păstrați `geometry_hash` drept componentă distinctă. Definiți DELETE și cazurile în care geometria este absentă. Adăugați testul de conflict produs numai prin schimbarea transformării.

## Condiții pentru R2

Autorul remediază numai documentele și contractele sale, referențiază fiecare ID și jurnalizează schimbarea. Auditorul recitește diferențele și caută regresii în cele 12 criterii. R1 rămâne arhivat ca probă a neconformităților reale; un verdict R2 îl poate înlocui operațional, fără a-l rescrie retrospectiv. Nu este necesar să existe hardware pentru închiderea acestor patru erori de specificație.
