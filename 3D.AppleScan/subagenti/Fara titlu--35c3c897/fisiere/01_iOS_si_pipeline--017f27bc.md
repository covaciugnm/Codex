# 1. Proiectul iOS și fluxul de percepție

**Versiune de proiectare:** V2, 2026-10-02. **Autor:** agentul proiectant iOS/CV. Acest document fixează alegeri pentru prima implementare. Fișierul Swift asociat este un contract de proiectare, nu o aplicație compilată. Nicio valoare de latență sau precizie nu este declarată măsurată pe telefon. Registrele și protocoalele V1 rămân istoric; aici detaliem implementarea propusă fără a le rescrie.

## 1.1. Configurația de bază și rezultatul livrabil

Alegem aplicație nativă Swift cu SwiftUI pentru navigație, ARKit pentru fluxul live și RoomPlan pentru camere. Pentru obiecte alegem captura ghidată Object Capture și reconstrucția RealityKit pe dispozitiv compatibil. Deployment target-ul propus este iOS 17.0, confirmat înainte de dezvoltare prin compilarea unui proiect minimal cu SDK final. Nu presupunem că orice telefon capabil să ruleze iOS 17 oferă toate funcțiile. O versiune minimă de OS este o condiție software, nu o listă de dispozitive calificate.

Baseline-ul de produs nu depinde de urmărirea `.referenceobject` asociată documentației noi iOS 27/Beta. Pentru poziția 6D implementăm întâi o referință cu marker și un traseu RGB-D restrâns la modele cunoscute. Această alegere produce un experiment verificabil pe API-uri deja existente și izolează facilitățile viitoare în spatele aceleiași interfețe. Faptul că un obiect a fost importat în format OBJ nu activează automat urmărirea sa.

Profilul hardware de referință este acum **iPhone 17 Pro Max**, confirmat disponibil de utilizator. Sunt necesare în continuare verificările runtime: LiDAR accesibil prin sceneDepth, world tracking și suport pentru RoomCaptureSession, ObjectCaptureSession și PhotogrammetrySession. iOS 17 este pragul de API propus, nu versiunea instalată presupusă; W00 înregistrează OS-ul real și fixează Xcode/SDK final care acceptă acest dispozitiv. Apple descrie captura ghidată și reconstrucția pe iOS și recomandă verificarea suportului dispozitivului. [I01 — Object Capture iOS](https://developer.apple.com/videos/play/wwdc2023/10191/), [I02 — suport ObjectCaptureSession](https://developer.apple.com/documentation/realitykit/objectcapturesession/issupported)

Fișa oficială iPhone 17 Pro Max confirmă A19 Pro, LiDAR și USB 3 cu rată nominală de până la 10 Gb/s; aceasta nu reprezintă debit de rețea garantat prin orice cablu. [I21 — specificații iPhone 17 Pro Max](https://support.apple.com/en-la/125091) Calculatorul extern declarat este NVIDIA Jetson AGX Thor 128 GB. Reconstrucția sau modelele grele pe Thor rămân opțiuni evaluate, nu transferuri automate din modul live. Modelul robotic demonstrativ este Unitree H1 v1; URDF-ul robotului personalizat va necesita integrare și calibrare separată.

iPhone 18 Pro Max este un dispozitiv viitor în parcul utilizatorului, nu un echipament testat în proiect. Migrarea păstrează formatul proiectului, dar creează device_id și calibration_id noi, rerulează manifestul de capabilități, memoria/termicul, calibrarea și testele de transport. Nu transferăm covarianțele sau extrinseca telefonului 17 către 18. Existența unor specificații publice nu închide această poartă experimentală.

Pe un telefon fără LiDAR putem implementa ulterior o ediție limitată pentru fotografiere/import/vizualizare. Ea nu se prezintă ca echivalentul ediției metrice și nu intră implicit în prima calificare. Interfața afișează funcția indisponibilă înaintea unei capturi lungi. Camera frontală pentru persoane este un profil separat, cu modele deformabile și protocol de consimțământ; nu o conectăm la baseline-ul rigid din această versiune.

## 1.2. De ce această structură tehnică

| Decizie | Alegere inițială | Alternativă analizată | Motiv și condiție de reevaluare |
|---|---|---|---|
| UI și integrare senzori | SwiftUI plus adaptoare native | Framework multiplatformă | Reducem punțile peste buffere/ciclul AR; reevaluăm pentru ecrane administrative comune |
| Camere | RoomPlan cu model intern EVA separat | Reconstrucție integral proprie | Obținem un baseline semantic; algoritmul propriu se compară ulterior pe geometrii dificile |
| Obiecte | Captură și reconstrucție în două faze | Reconstrucție densă permanentă | Protejăm bugetul termic al capturii și separăm erorile |
| Urmărire 6D | Marker/PnP, apoi rafinare RGB-D | Model greu de fundație pentru fiecare cadru | Baseline interpretabil și portabil; modelul greu rămâne experiment pe calculator extern |
| Catalog | Registru actor și obiecte imutabile | Dicționar global accesat din toate firele | Ordine explicită a actualizărilor și verificarea reviziilor |
| Stocare | SQLite local plus fișiere adresate prin hash | Un singur document JSON mare | Tranzacții mici, istoric și recuperare fără rescrierea întregului proiect |

Nu rulăm simultan Object Capture, RoomPlan și o sesiune ARKit proprie concurentă pentru aceeași cameră. `CaptureCoordinator` deține exclusiv modul activ. Pentru camere preia sesiunea permisă de RoomPlan și primește actualizări prin delegate; pentru live și robotică deține ARSession. Orice reutilizare a sesiunii existente prin inițializatorul RoomPlan este verificată pe SDK și profil, nu obținută prin schimbarea arbitrară a configurației unei sesiuni active.

## 1.3. Organizarea repository-ului și dependențelor

Repository-ul viitor este un monorepo cu `ios/EVA3DScanApp`, `Packages/EVADomain`, `EVACapture`, `EVAPerception`, `EVAStorage`, `EVAExport`, `EVARobotLink`, `Fixtures` și `Tests`. `EVADomain` conține identificatori, unități, mașini de stări și erori, fără import ARKit. `EVACapture` conține adaptoarele Apple. Pachetele de procesare primesc snapshoturi de date, nu acces direct la camera fizică. Codul de interfață nu deschide direct baza de date.

`EVAStorage` are o singură autoritate de scriere și expune operații de domeniu precum finalizarea capturii sau confirmarea exportului. `EVAExport` nu modifică modelul original; generează versiuni derivabile dintr-un hash de intrare. `EVARobotLink` convertește contractele interne în protocolul stabilit împreună cu proiectantul robotic. Dependența inversă din domeniu spre transport este interzisă, pentru ca modul fără rețea să rămână complet funcțional.

Un wrapper C/Objective-C++ izolează biblioteca de marker și operațiile geometrice care nu sunt convenabile în Swift. Pentru prima probă se fixează un commit AprilTag și o versiune OpenCV, se construiește un XCFramework pentru arhitecturile efectiv distribuite și se arhivează licențele. Nu adăugăm întregul ecosistem Open3D într-o aplicație mobilă numai pentru ICP; păstrăm Open3D ca referință offline, iar un solver restrâns va fi comparat numeric înainte de optimizarea cu Metal.

CI va avea trei niveluri: teste pure de domeniu pe host compatibil, build iOS cu SDK final și probe pe dispozitiv real. Simulatorul validează navigația și stările, dar nu constituie probă LiDAR. Fiecare build păstrează lockfile-urile, compilatorul, SDK-ul, commiturile wrapperelor și hashurile modelelor. O dependență nouă nu intră direct în release doar pentru că demo-ul rulează.

## 1.4. Manifestul capabilităților și preflight

La instalare și după actualizare de OS se rulează un preflight scurt: autorizație cameră, disponibilitatea configurației ARKit, sceneDepth, sceneReconstruction, RoomPlan, captură și reconstrucție Object Capture. Se înregistrează rezultatele boolean și eroarea distinctă dacă sesiunea de probă eșuează. Suportul RoomPlan este condiționat de LiDAR în documentația Apple. [I03 — RoomCaptureSession.isSupported](https://developer.apple.com/documentation/RoomPlan/RoomCaptureSession/isSupported)

Înainte de fiecare captură se verifică spațiul liber, starea termică, nivelul resurselor și existența unei calibrări corespunzătoare. O calibrare este invalidată dacă se schimbă camera, crop-ul relevant, modelul de adâncime sau montajul robotic; schimbarea limbii interfeței nu o invalidează. Se păstrează identificatorul imutabil al calibrării, nu numai numărul ei vizibil.

Profilul inițial de laborator cere rezervă liberă de minimum `max(2 GiB, 2 × estimarea intrărilor + estimarea rezultatului)`. Aceasta este o regulă conservatoare propusă, ajustabilă după măsurători, nu o cerință Apple. Dacă estimarea lipsește, se solicită segmentarea capturii și se limitează volumul acceptat, fără continuare până la umplerea discului. Cota de proiect este afișată în UI înaintea lansării reconstrucției.

## 1.5. Mașina de stări a sesiunii

Stările sunt `idle`, `checking`, `ready`, `capturing`, `suspended`, `finalizing`, `reviewing`, `saved`, `failed`. Tranzițiile sunt acțiuni validate de coordinator, nu texte deduse din existența unui fișier. `suspended` păstrează motivul: aplicație în fundal, tracking insuficient, termic, operator sau transport. `failed` păstrează un cod stabil și recuperabilitatea: reîncercare, recalibrare, relocalizare ori recaptură.

În modul obiecte, încheierea capturii trece în finalizing numai după verificarea inventarului de imagini și metadate disponibil. Reconstrucția este un job persistent separat. În modul camere, fiecare cameră are starea sa; încheierea uneia nu înseamnă încheierea proiectului de apartament. În live, oprirea conduce la ștergerea referințelor tranzitorii și idle, fără saved. O fotografie cotată salvată explicit este o operație distinctă și nu transformă retrospectiv toate cadrele în date persistente.

Întreruperea camerei în fundal este tratată ca eveniment normal, nu ca defect ascuns. Modelul de utilizare continuă cere aplicația activă și alimentare/termic adecvate; nu promitem captură normală nelimitată pe ecran blocat. [I04 — întreruperea camerei în fundal](https://developer.apple.com/documentation/avfoundation/avcapturesession/interruptionreason/videodevicenotavailableinbackground)

## 1.6. Identitatea observației și contractul bufferelor

Cheia de mesaj este `(device_id, session_id, stream_id, sequence)`. `sequence` și timpii în nanosecunde sunt serializați zecimal ca stringuri pentru a evita pierderea preciziei în intermediari JSON. `observation_id` identifică o captură sursă; `frame_id` numește exclusiv reperul geometric. `map_epoch`, `clock_epoch` și `session_id` se schimbă independent la resetarea reperului, discontinuitatea ceasului și restartul procesului.

Un `CapturedObservation` conține descriptorul imuabil și un token de buffer. Tokenul nu este o adresă de memorie transmisă în rețea. `FrameLeasePool` păstrează referințele reale CVPixelBuffer/Metal private și oferă lease-uri pe consumator. După ce ultimul lease este eliberat și operația GPU asociată este terminată, bufferul poate fi reutilizat. Anularea unei sarcini Swift nu permite reciclarea unui buffer încă folosit de accelerator.

Limitele inițiale ale profilului sunt: trei cadre distincte deținute simultan de aplicație, un cadru în așteptare la detector, un job greu 6D activ și maximum două operații GPU EVA aflate în lucru. Aceste limite privesc resursele controlate de EVA; ARKit/Core ML pot avea alocări interne suplimentare. La depășire se abandonează candidatul nou sau cel neînceput conform politicii, niciodată o resursă în uz. Numărul total de lease-uri nu poate depăși șase în profilul de bază.

Bugetul inițial de memorie controlată pentru buffere și tensori EVA este 192 MiB, verificat prin contabilizare înaintea alocării. Nu este o promisiune că întregul proces consumă atât. Instrumentarea urmărește separat footprint-ul real; dacă limita internă nu previne presiunea de memorie, profilul este redus. Acest design urmărește evitarea acumulării, conform practicilor Apple pentru cadre întârziate, fără a presupune că proprietățile AVFoundation sunt API ARKit. [I05 — TN2445](https://developer.apple.com/library/archive/technotes/tn2445/_index.html)

## 1.7. Programarea și anularea

`CaptureCoordinator` gestionează callbackurile și schimbările de mod. `PerceptionScheduler` este actorul care decide ce cadre sunt utile. `TrackRegistry` acceptă rezultate numai dacă epocile, calibrarea și versiunea modelului coincid cu starea așteptată. `PersistenceActor` nu rulează pe MainActor. Operațiile grele nu se execută în actorul de interfață și nu păstrează o tranzacție de bază de date deschisă pe durata inferenței.

Planificatorul rulează descoperirea la ținta inițială de 5 Hz, urmărește obiectul selectat la 15 Hz dacă există cadre și buget, iar randarea urmărește 30 Hz. Acestea sunt parametri de experiment, nu garanții ale API-urilor. Când o inferență depășește intervalul, nu lansăm automat o a doua pentru fiecare cadru ratat. Preferăm ultimul cadru eligibil și raportăm rata realmente atinsă.

Cu două sau patru joburi concurente putem obține throughput mai bun, dar și memorie mai mare sau latență mai slabă. Apple cere profilarea câștigului în scenariul real; de aceea baseline-ul pornește cu un job greu, iar 1/2/4 sunt variante de experiment. Anularea Swift este cooperativă; răspunsul tardiv este ignorat după verificarea epocii chiar când operația hardware nu poate fi întreruptă imediat. [I06 — Core ML asincron](https://developer.apple.com/videos/play/wwdc2023/10049/), [I07 — TaskGroup](https://docs.swift.org/latest/documentation/swift/taskgroup/)

## 1.8. Pipeline-ul 6D ales

Prima țintă este un obiect rigid cu scară verificată și marker fix calibrat față de model. Detectăm colțurile markerului, folosim intrinseci pentru imaginea efectiv procesată și estimăm poziția. Respingem unghiurile și distanțele în afara profilului, reproiecția prea mare și adâncimea incompatibilă. AprilTag oferă un baseline de marker; testul independent folosește alte referințe pentru a evita evaluarea circulară. [I08 — AprilTag](https://github.com/AprilRobotics/apriltag)

A doua etapă elimină markerul numai pentru un catalog mic calificat. Detectorul propune regiunea, segmentarea elimină fundalul, corespondențele model–imagine furnizează PnP inițial, iar RGB-D rafinează local. Pentru început folosim imagine redusă cu intrinseci transformate și maximum 2.000 de puncte geometric distribuite pe obiect. Numărul este un parametru inițial de cost; testele compară 1.000/2.000/4.000 puncte la aceeași secvență.

PnP estimează transformarea obiect–cameră, iar variantele au condiții diferite și pot produce soluții multiple. [I09 — OpenCV PnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html) Folosim o funcție robustă pentru corespondențe aberante și verificăm cheirality, acoperire spațială, reproiecție și consistență depth. Refinarea geometrică nu pornește dintr-o poziție arbitrară: ICP este local și nu identifică unic orientarea unui plan sau cilindru simetric. [I10 — ICP](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html)

Adâncimea se reproiectează numai după verificarea rezoluției, intrinsecielor și definiției geometrice. Pixelul invalid nu devine punct la origine. `confidenceMap` este o categorie de încredere, nu precizie în milimetri. În prima implementare eliminăm punctele de încredere joasă din ajustarea dimensională, păstrând procentul eliminat în raport. Această regulă poate scădea completitudinea și este evaluată ca atare. [I11 — sceneDepth](https://developer.apple.com/documentation/arkit/arframe/scenedepth), [I12 — confidenceMap](https://developer.apple.com/documentation/arkit/ardepthdata/confidencemap)

## 1.9. Catalog, incertitudine și fuziune

Catalogul separă modelul geometric, exemplarul fizic și trackul temporar. Starea transmisă este observed/predicted/occluded/lost/retired, iar ambiguity_status este none/pose/identity/both. La două exemplare identice păstrăm ipoteza de asociere ambiguă; nu inventăm identitate numai fiindcă meshurile sunt egale. Predicția nu actualizează timpul ultimei observații reale.

Transformarea `T_AO` mută puncte din obiect O în reperul A. Reprezentarea internă a incertitudinii folosește perturbația dreaptă `T=T_hat Exp(delta_xi)`, vector `[rho,phi]` în O, unități m²/rad²/m·rad pentru blocuri. Covarianța absentă are status unavailable. Conversia către pose ROS cu eroare aditivă de poziție și rotație infinitezimală în axe fixe folosește `diag(R,R)`; conversia către perturbație Lie stângă folosește adjointul complet. Cele două operații nu sunt confundate.

Încărcăm modelul OBJ numai după normalizarea unităților, definirea originii și axelor și validarea texturilor. Alegem metri intern și păstrăm transformarea față de sursă. Dimensiunea corectată manual are proveniență separată și nu dovedește precizia capturii. Un model importat prea mare sau cu căi externe de texturi este respins înaintea alocărilor costisitoare.

## 1.10. Camere și fluxul spre robot

RoomPlan produce o reprezentare parametrică utilă pentru camere și export USD; modelul intern EVA păstrează versiunea observațiilor și corecțiile distinct. [I13 — RoomPlan](https://developer.apple.com/documentation/roomplan) Unirea se face numai cu repere compatibile: sesiune AR comună menținută între camere sau relocalizare verificată. [I14 — multiroom](https://developer.apple.com/documentation/roomplan/scanning-the-rooms-of-a-single-structure)

Pentru robot alegem trei conexiuni TLS WebSocket separate — control, realtime și hartă — conform colegului de robotică. `URLSessionWebSocketTask` oferă transport peste TCP/TLS și mesaje text/binar; nu îl prezentăm ca datagramă și nu promitem lipsa blocării din cauza retransmisiilor. Dimensiunea maximă recepționată este limitată explicit înaintea decodării. [I15 — URLSessionWebSocketTask](https://developer.apple.com/documentation/foundation/urlsessionwebsockettask), [I16 — maximumMessageSize](https://developer.apple.com/documentation/foundation/urlsessionwebsockettask/maximummessagesize)

Adâncimea recentă pentru obstacole este separată de harta persistentă: Apple nu garantează că actualizările mesh reflectă mișcările mediului în timp real. [I17 — ARMeshAnchor](https://developer.apple.com/documentation/arkit/armeshanchor) Modurile live_ephemeral și robot_stream sunt diferite: primul nu transmite implicit mediul, iar al doilea cere alegerea explicită a robotului asociat și contractul de retenție. Partajarea este vizibilă permanent în UI.

## 1.11. Livrabile și porți de implementare

Stările canonice de obiect sunt aceleași ca în contractul de transport: `observed`, `predicted`, `occluded`, `lost`, `retired`. Adaptorul pentru un registru vechi cu `archived` nu îl convertește automat: îl mapează la `retired` numai dacă există retragere explicită; ambiguitatea rămâne în `ambiguity_status`. Pentru `lost` sau `occluded`, câmpul pose obligatoriu reprezintă ultima estimare și păstrează timpul ultimei capturi contributive; nu este dată proaspătă pentru mișcare. Heartbeat-ul anunță sănătatea actuală. Predicția are orizont mărginit și covarianță crescută, iar ieșirea din fereastra calificată duce la `lost`, fără extrapolare nelimitată.

Handshake-ul inițial folosește excepția control din schema wire: `clock_model_id=null`, timp și epoci zero, `calibration_id`/`frame_id=unbound`, numai pentru hello și schimbul de probe de ceas. Nu emite observații în această stare. Pentru depth, `camera_frame_id` denumește cadrul optic, `frame_id` este părintele, iar `camera_pose=T_parent_cameraoptical`. Ținta canonică P95 este 100 ms, distinctă de limita individuală de utilizare de 150 ms; acestea rămân criterii de calificare, nu latențe măsurate.

Adaptorul wire păstrează separat timpul original iPhone `sourceCaptureTimeNS` și timpul convertit în domeniul monoton Thor, transmis ca `capture_time_ns`. Conversia folosește `clock_model_id` și include incertitudinea; înaintea calificării modelului de ceas, fluxul nu furnizează observații utilizabile pentru mișcare. Identificatorii numerici UInt64/Int64 sunt șiruri zecimale pe transport, conform `transport.schema.json`. Metadatele depth transmit intrinsecii pentru rezoluția efectivă și convenția camerei definită în contractul robotic. RGB comprimat nu este activ în profilul wire inițial. Limitarea rezoluției transmisiei nu schimbă automat intrinsecii: adaptorul le recalculează și le verifică pe fixture.

Primul increment livrează shell-ul SwiftUI, simulatorul de cadre și manifestul de capabilități. Al doilea livrează captura live cu limite de buffere și probe de fundal. Al treilea livrează un proiect persistent de obiect și o cameră, apoi exportul verificat. Al patrulea adaugă markerul 6D; abia după compararea lui cu referințe independente se activează modelul fără marker. RobotBridge este inițial numai vizualizare și înregistrare autorizată, fără comenzi de actuatoare.

Fiecare increment are commit, build, profil hardware, teste rulate și defecte. Testele minime includ epuizare de lease-uri, rezultat întârziat după reset, intrinseci la resize, întoarcere din fundal, lipsă depth și model simetric. Acceptarea unei interfețe în document nu echivalează cu acceptarea codului. Precizia dimensională urmează profilurile canonice și protocolul statistic al proiectului; nici randarea fluentă, nici un scor de detector mare nu înlocuiesc acele măsurători.
