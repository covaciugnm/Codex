# Audit independent R1 — cercetare și robotică
Data: 2026-10-02. Auditor: auditor_final. Autorii documentelor: manager și doctoral_robotics.

## Verdict
**Remedieri necesare.** Trei neconcordanțe inițiale sunt remediate și verificate; trei necesită închiderea explicită a contractului. Acesta este un audit al proiectului tehnic, fără validare pe iPhone, Thor, robot, ROS, TLS sau rețea. Capitolul de metrologie scris de auditor este exclus din verdict și are reviewer separat. Hardware/decizii/management încă în redactare sunt rezervate R2.

## Perimetru și criterii
Au fost citite integral cercetare01/02, proiect tehnic03/04, schema JSON, exemplele, mesajele ROS propuse, profilurile și testele contractului. Criteriile sunt:
1. Fiecare performanță este identificată drept măsurată, calculată sau ipoteză; nicio extrapolare de precizie de la alt telefon.
2. Unități SI, direcție SE(3), cadre optic/body, convenție covarianță și timestampuri compatibile.
3. Pornirea/reconectarea se pot descrie fără dependență circulară; map epochs, revizii, tombstones, hash și snapshot au semantică explicită.
4. Schema, profilurile și exemplele descriu același protocol; mesaje incompatibile trebuie respinse.
5. Pragurile V1 rămân trasabile, iar bugetele calculate nu sunt prezentate ca percentile măsurate.
6. Sursele primare susțin afirmațiile decisive; licențele și lipsa experimentelor sunt vizibile.

## Constatări
### CR-01 — P1: Bootstrap ceas circular
Statut: **remediated_verified_R1**.

Contractul inițial cerea clock_model_id și timestamp convertit pentru hello/probe înainte de existența unui model.

Dovezi: `03_contracte/transport.schema.json:729`, `04_validare/robot_contract_checks.cjs:61`.

Remediere cerută: Excepție strictă pentru control bootstrap, sentinele explicite, interdicție pentru observații fără model.

Verificare: Schema modificată și 24/24 probe relansate independent; hello null acceptat, observație null respinsă.

### CR-02 — P1: Depth fără identificarea cadrului optic
Statut: **remediated_verified_R1**.

camera_pose nu identifica separat camera frame și transformarea parent-child.

Dovezi: `03_contracte/transport.schema.json:653`, `02_proiect_tehnic/03_robot_transport_si_harta.md:27`.

Remediere cerută: camera_frame_id obligatoriu, T_parent_camera explicit, Image/CameraInfo în optic.

Verificare: Câmp obligatoriu adăugat; probă numerică independent relansată în suita24.

### CR-03 — P1: Țintă P95 inconsistentă cu V1
Statut: **remediated_verified_R1**.

Bugetul propus150ms înlocuia ținta canonicăP95≤100ms fără decizie.

Dovezi: `02_proiect_tehnic/04_integrare_operare_si_bugete.md:58`.

Remediere cerută: P95≤100ms separat de cutoff individual150ms.

Verificare: Textul58 și profilul au ținta100 și cutoff150 distincte; nu există claim de măsurare.

### CR-04 — P1: Modelul afin negociat nu are mesaj de publicare
Statut: **open_author_notified**.

Telefonul trebuie să convertească timpul prin a,b/model_id/validitate, dar control nu definește transportul coeficienților și acceptarea modelului.

Dovezi: `03_contracte/transport.schema.json:575`, `03_contracte/transport.schema.json:608`, `02_proiect_tehnic/03_robot_transport_si_harta.md:33`.

Remediere cerută: Definirea publicării, domeniilor/unităților, epocii, intervalului valid și confirmării modelului; fixture și respingeri pentru model absent/expirat. Tokenul se transmite prin HTTP Authorization protejatTLS, nu în handshakeTLS.

Verificare: În așteptarea patchului autorului.

### CR-05 — P2: Mesh delta acceptă payload RGB
Statut: **open_reproduced**.

Înlocuirea geometry.encoding cu rgb_hevc_annex_b și recalcularea semantic_hash sunt acceptate de schema și validator, deși RGB nu e activ v1.

Dovezi: `03_contracte/transport.schema.json:140`, `04_validare/robot_contract_checks.cjs:29`, `06_audit/robot_independent_R1_results.json`.

Remediere cerută: Restrângerea geometry la eva_mesh_le_v1 în upsert și snapshot, teste negative pentru depth/RGB.

Verificare: Probă independentă acceptedWrongEncoding=true. Nu demonstrează vulnerabilitate de runtime; demonstrează contract contradictoriu.

### CR-06 — P2: Timestamp pentru predicted insuficient precizat
Statut: **open_author_notified**.

Pose extrapolată și ultima observație pot avea momente diferite; contractul are un singur capture_time_ns.

Dovezi: `02_proiect_tehnic/04_integrare_operare_si_bugete.md:64`, `03_contracte/eva_interfaces.msg.txt`.

Remediere cerută: Fie v1 predicted păstrează ultima pose nemodificată și timestampul ei, fie două momente explicite cu gate pe ultima observație și transformare la timpul pose.

Verificare: În așteptarea deciziei explicite a autorului.

## Rezultate pozitive
- Relansarea independentă a specificației executabile în VM a trecut **24/24** cazuri. Fișierele de rezultate ale autorului nu au fost rescrise; rezultatul propriu este robot_independent_R1_results.json.
- Conversia optic→body este o rotație proprie, compunerea/inversa SE(3), ordinea reviziilor, ștergerea cu tombstone și limitele int64/uint64 sunt acoperite în suita sintetică. Verificarea covarianței este limitată la rotația unui exemplu diagonal.
- Aritmetica debitului depth256×192×4×15=2.949.120B/s, bugetele stocării și formula ilustrativă de oprire sunt coerente. Rezerva rețelei și resurseleCPU/GPU sunt etichetate ipoteze.
- JCS și SHA256 sunt proiectate pentru identitate semantică; documentul nu confundă hashul cu autentificarea. Testele nu sunt declarate certificare generală JSON Schema/JCS.
- Snapshotul cu barieră, aplicarea atomică și tombstones păstrează separat starea incompletă. Probele100.000delta/100întreruperi/1.000epoch/60min sunt criterii viitoare, nu rezultate pretinse.
- Mișcarea este dezactivată implicit; indicatorii de percepție sunt consultativi, fără certificare de siguranță.

## Verificări de surse
Consultare independentă a paginilor primare, 2026-10-02:
- [Apple iPhone17ProMax](https://support.apple.com/en-la/125091): LiDAR, WiFi7 și USB3 până la10Gb/s susțin specificația conectivității, fără să demonstreze precizia/frecvența scanării.
- [Apple iPhone18Pro](https://www.apple.com/de/iphone-18-pro/specs/): pagina oficială era accesibilă; existența ei nu califică profilul viitor.
- [Licența NVlabs FoundationPose](https://raw.githubusercontent.com/NVlabs/FoundationPose/main/LICENSE): secțiunea3.3 restrânge utilizarea la cercetare/evaluare necomercială. Încadrarea drept baseline de cercetare este corectă.
- [README FoundationPose](https://raw.githubusercontent.com/NVlabs/FoundationPose/main/readme.md): secțiuneaNotes explică diferența antrenării pentru weights publice; rezultatele articolului nu pot fi atribuite automat instalării propuse.
- [ROS Jazzy](https://www.openrobotics.org/blog/2024/5/ros-jazzy-jalisco-released) și [Isaac ROS4.1](https://nvidia-isaac-ros.github.io/v/release-4.1/repositories_and_packages/isaac_ros_mapping_and_localization/index.html) au fost consultate; compatibilitatea declarată nu echivalează cu instalarea sau compilarea proiectului.

Nu a fost reprodus fiecare rezultat din articole și nu a fost efectuat un audit juridic. BundleSDF/raportPix4D sunt delimitate în text după nivelul de acces, fără a pretinde citirea unei descărcări eșuate.

## Reproducere și reluare
Rularea independentă: node06_audit/replay_robot_R1.cjs din directorul documentației, cu Node24.18.0. Scriptul execută probele autorului în memorie și salvează numai rezultatul auditorului; proba suplimentară modifică encoding și recalculează hashul. O tentativă inițială node-e a eșuat la quoting înainte de executarea probelor; rularea din fișier a rezolvat problema și este singura bază numerică a verdictului.

Pentru R2: revedeți CR-04/05/06, relansați testele, verificați hardware/decizii/management după stabilizare și creați hashurile snapshotului acceptat. Nu suprascrieți constatările istorice și nu transformați acceptarea documentară în acceptare hardware.

