# Contractele de date și execuție pentru EVA Robot

Data 6 octombrie 2026. Contract propus `eva.robot/1.0-draft`, normativ pentru implementarea din PLAN_V2. Nu reprezintă mesaje ROS IDL deja generate. Unitatea de compatibilitate este major version; schimbarea sensului unui câmp cere major nou. JSON Schema, Swift Codable și ROS IDL vor fi generate/testate împreună în R1.

## Identitate și proprietate

`site_id`, `robot_id`, `sensor_id`, `session_id`, `clock_id`, `map_id`, `map_epoch`, `calibration_id`, `model_id` sunt identificatori separați. `robot_id` se alocă la pairing, nu din numele comercial al telefonului. Sesiunea se schimbă la restart; `clock_id` la schimbarea originii ceasului; `map_epoch` când resetarea schimbă originea locală. `map_revision` este revizia globală a estimării și poate avansa fără resetarea originii. `sequence` crește per (robot,sensor,session,stream); `observation_id` UUID este unic global. Retrierea păstrează același observation_id.

Un track local primește (robot_id,session_id,local_track_id). `object_id` global apare numai după asociere acceptată. Aliasurile și operațiile de merge/split sunt evenimente reversibile; un ID nu se reutilizează pentru alt obiect. Persoanele au domeniu separat și acces controlat. Orice rezultat de server păstrează source observation IDs și model revision; nu devine observație independentă a aceleiași imagini.

## Unități repere și transformări

SI: metri, secunde, radiani. Quaternion `[x,y,z,w]` normalizat; matrice 4×4 în ordinea row-major pe fir. `T_A_B` transformă coordonate din B în A; compunere pe vectori coloană. Repere ROS de corp: X înainte, Y stânga, Z sus. Optic C: X dreapta, Y jos, Z înainte. Cameră ARKit A: X dreapta, Y sus, Z înapoi. Schimbarea A→C este `S=diag(1,-1,-1)`, rotație proprie, determinant +1. Transformarea lumii ARKit V către map M se estimează/calibrează; nu se deduce din simpla schimbare a axelor camerei.

Pentru observație exprimată în C: `T_M_O(t)=T_M_V(t) · T_V_A(t) · T_A_C · T_C_O(t)`, cu `T_A_C=diag(1,-1,-1,1)`. Alternativa prin robot: `T_M_O(t)=T_M_odomR(t) · T_odomR_baseR(t) · T_baseR_headR(q(t)) · T_headR_phoneR · T_phoneR_C · T_C_O(t)`. Se folosește exact un traseu autoritar și toate componentele dinamice la capture time. Două trasee independente se compară pentru diagnostic, nu se multiplică unul cu altul.

Arborele TF are un singur părinte și autoritate per copil. Estimatorul robotului publică odom→base, localizatorul map→odom, robot_state_publisher articulațiile, calibrarea legăturile fixe. Camera VIO pe gât mobil nu este direct odometrie a bazei: compensarea kinematică folosește q(t). Covarianța și corelațiile se propagă, iar IMU/VIO derivate din aceleași date nu se numără ca surse independente.

Publicăm observații cameră-local și, separat, starea obiectelor în map. Topicul și schema le disting. Valoarea world nu primește frame_id optic. Imaginea/depth sunt asociate cu rezoluție, K, distorsiune relevantă, depth_to_rgb și transformarea crop/resize; transformarea pentru orientarea ecranului nu se aplică orb în deproiecție.

## Timp și incertitudine

`capture_time_ns`, `receive_time_ns`, `process_finished_ns`, `estimate_time_ns` au semnificații distincte. Toate contoarele/timestamp-urile UInt64 sunt șiruri zecimale în JSON. ClockMapping conține `clock_id`, `robot_clock_id`, `a`, `b_ns`, intervalul de valabilitate, `uncertainty_ns` și numărul de eșantioane; conversia este `t_robot=a*t_phone+b`. Wall clock UTC se folosește pentru căutare/audit, nu pentru ordonare senzorială sau cursor sync.

Calibrare inițială: schimburi bidirecționale timestamped, filtrarea eșantioanelor cu RTT mare, regresie robustă pe drift și offset, reestimare periodică. Asimetria rețelei este o incertitudine, nu este anulată presupunând RTT/2 exact. Validare prin eveniment vizual/mișcare comună și referință independentă. Propunere pilot p95≤5 ms; limita pentru activarea mișcării se deduce din bugetul geometric. Exemplu calculat, nu măsurat: 60 grade/s×20 ms=1,2 grade; la 2 m rezultă ~42 mm abatere transversală.

La lipsa TF la t, se așteaptă cel mult TTL-ul fluxului; nu se substituie automat ultima transformare. Pentru pilot TTL percepție locală=100 ms, rezultat server pentru actualizarea locală=500 ms; schimbarea pragurilor este revizie de configurație. Rezultatul peste TTL poate intra în istoric/offline, nu în control. Transformarea de ceas expirată sau cu incertitudine peste buget interzice starea READY pentru sarcina dependentă.

Covarianța necunoscută este `null` cu `uncertainty_status=unavailable`. Zero nu înseamnă necunoscut. Dacă există model empiric, includem versiunea lui. Convenție internă SE3: perturbație dreaptă `T=T_hat Exp(delta_xi^)`, ordinea `[rho_x,rho_y,rho_z,phi_x,phi_y,phi_z]`, exprimată în cadrul copil. Conversia către perturbație stângă folosește Ad(T), iar către eroare ROS aditivă de poziție și rotație fixed-axis în părinte folosește Jacobianul diag(R,R), pentru parametrizarea declarată. Nu copiem aceeași matrice între convenții. Simetriile/mai multe ipoteze de orientare se păstrează explicit.

## Mesaj de observație exemplu

Valorile sunt fixture sintetice, nu măsurători ale proiectului. Quaternionul este valid deoarece exemplul presupune o țintă rigidă cu orientare măsurată; pentru detector 2D fără orientare se transmite null și rotation_valid=false.

```json
{
  "protocol": "eva.robot/1.0-draft",
  "site_id": "site-01", "robot_id": "r01", "sensor_id": "rear-rgbd",
  "session_id": "session-17", "stream_id": "object_observations",
  "sequence": "42", "observation_id": "obs-fixture-42",
  "clock_id": "clock-17", "capture_time_ns": "10000000000",
  "map_id": "floor-01", "map_epoch": "vio-17", "map_revision": "123",
  "calibration_id": "cal-07", "frame_id": "r01/camera_optical",
  "source_frame_id": "frame-1234", "local_track_id": "17:3", "object_id": null,
  "class": "mug", "class_score": 0.91,
  "pose": {"position_m": [0.1, 0.05, 1.2], "orientation_xyzw": [0, 0, 0, 1]},
  "position_valid": true, "rotation_valid": true,
  "dimensions_m": [0.08, 0.10, 0.08], "dimensions_status": "measured",
  "uncertainty_status": "unavailable", "covariance": null,
  "symmetry": "none", "state": "observed", "method": "fixture_marker",
  "model_id": "fixture-v1", "source_observation_ids": [],
  "assets": [{"kind": "rgb", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}]
}
```

Validatorul rejectează câmpuri necesare lipsă, numere nefinite, unități/reper necunoscut, quaternion nenormalizat când valid, depth invalid, dimensiuni negative, model/calibrare incompatibile și epoch expirat. Duplicatul cu același ID și același conținut primește ACK-ul rezultatului inițial fără reaplicare; același ID cu alt conținut este conflict. ID-urile demonstrative de mai sus sunt înlocuite de UUID în schema de producție. Scorul clasei nu este covarianță geometrică. Stările observed/predicted/occluded/lost sunt distincte de present/missing în memoria persistentă.

## WorldModel și sincronizare tranzacțională

Entități persistente: MapRevision, Submap, Calibration, Robot, Observation, ObjectInstance, ObjectAlias, ObjectStateEstimate, SpatialRelation, PersonProfile, Task, Asset, ChangeEvent. `ObjectStateEstimate` are parent observation IDs, valid_from/to, frame/map revision, pose validity, uncertainty și estimator version. Relațiile on/in/near/held_by includ obiectele capete, timp, metodă și încredere. Near se calculează din geometrie, on/in cer suport/conținere. Obiectele neobservate nu sunt declarate lipsă fără vizibilitate a volumului, adâncime validă și confirmări repetate.

Handshake: client autentificat trimite protocol/schema major, robot/site, app/OS build, capabilities, clock mappings, map epoch și ultimul change_seq aplicat. Serverul negociază versiunea și răspunde current revision, minimum retained change_seq și plan delta/snapshot. Un client incompatibil primește upgrade_required; datele lui pot fi arhivate brut fără fuziune.

Upload observation este append-only, deduplicat pe (site_id,observation_id). Comenzile de editare WorldModel includ expected base_revision și idempotency_key. Într-o tranzacție serializată per site/map, serverul validează baza, aplică schimbarea, alocă change_seq, scrie event și outbox, apoi commit. Răspunsul repetat la același idempotency key este același rezultat, fără aplicare duplicată. Un conflict primește 409 cu revision actuală; clientul reface asocierea, nu suprascrie orbește.

ACK declară `durability_level=local` după commit/fsync pe host și `replicated` numai după confirmarea jurnalului și assets necesare într-un domeniu de defect independent. La crash de proces/repornire cu disc intact, niciun ACK local nu se pierde. La pierderea hostului și a discului, profilul de backup local are RPO≤5min; zero pierderi se cere pentru ACK replicated în modelul de defect cu un singur domeniu pierdut. Dacă replica nu este disponibilă, nu emitem ACK replicated; clientul păstrează outbox-ul până la nivelul cerut. Backup zilnic cu jurnal incremental nu este prezentat ca garanție de zero pierderi la dezastru.

Assets: upload în staging content-addressed cu dimensiune/hash; verificare completă; apoi tranzacția publică manifestul reviziei care referă doar assets disponibile. Clientul descarcă în temporar, verifică hash și aplică baza+manifestul atomic, apoi avansează cursorul. Crash înainte de commit reia aceleași operații; assets nereferențiate se curăță după retenție, niciodată cât sunt cerute de o revizie activă/backup.

Delta conține intervalul contiguu (from_seq,to_seq], evenimente și hash de stare canonică. Duplicatele se ignoră; out-of-order se tamponează limitat; gap cere retransmisie. Dacă jurnalul nu mai reține gap-ul, se descarcă snapshot. Snapshot are map revision, last_seq, canonicalization version, manifest și hash; aplicarea este atomică. Rollback este eveniment compensator și revizie nouă, nu scăderea change_seq. Tombstone-urile rămân până la horizon-ul clienților; un client prea vechi primește snapshot înainte de a putea reintroduce date șterse.

Canonicalization: UTF-8, JSON keys sortate, array order semantic, fără NaN/Infinity, numere metric documentate cu reprezentare stabilă, timestamps UInt64 string; algoritmul și schema au versiune. În R1 folosim implementare unică și fixtures cross-language, nu hash pe serializări arbitrare Swift/Python/JS.

## Alinierea și reconcilierea mai multor roboți

1. Fiecare telefon produce submap metric și observații în origine proprie. Pentru pilot, o țintă fiducială calibrată oferă ancoră comună; o singură vedere frontală planară nu este suficientă pentru calificarea completă.
2. Place recognition produce candidați de loop closure. Corespondențe locale, RANSAC/estimare robustă și verificare geometrică RGBD resping false positives; verificare pe cadre independente înainte de acceptare. Gravitația/scara și distanțele de referință trebuie să fie coerente.
3. Optimizatorul creează propunere T_map_submap cu covarianță ori unavailable și lista constrângerilor. Acceptarea cere pragul de aliniere T05, fără contradicție cu ancorele acceptate; ambiguitatea păstrează hărțile separate.
4. Commit-ul transformării este revizie nouă. Odom local rămâne continuu; localizatorul tratează corecția map separat. Estimările de obiecte afectate se recalculează din observațiile originale.
5. Asocierea inter-robot folosește poziție cu incertitudine, clasă, dimensiuni, embeddings compatibile și relații. O potrivire ambiguă păstrează două ipoteze. Observațiile provenite din același cadru ori de la server sunt corelate și nu dublează certitudinea. Merge de obiecte păstrează aliasuri și poate fi anulat.
6. ARKit CollaborationData este transport auxiliar opac, cu compatibilitate OS explicit testată; critical fiabil, optional best effort. Maximum patru participanți este recomandare Apple pentru rezultate bune, nu capacitatea întregii flote. Mai mulți roboți folosesc submaps și server; niciun merge nu depinde exclusiv de un blob Apple nedecodabil.

Exemplu: r01 și r02 văd aceeași cană în origini diferite. Ambele observații se păstrează; numai după aliniere primesc același object_id. r02 offline observă cana mutată la 09:00 și revine la 10:05. Evenimentul primește change_seq nou la 10:05, indiferent de ora observației. Dacă r01 are observație mai recentă, istoricul se completează, dar starea curentă nu regresează automat. Dacă ceasurile nu permit ordonare sigură, ambele ipoteze rămân și se cere reobservare. Un reset r02 schimbă map_epoch, deci vechiul T_map_submap nu se aplică automat.

## Transport QoS și interfețe

MVP: telefon→gateway prin TLS pe TCP cu fluxuri separate pentru senzori/control/assets. Extindere QUIC/datagrams doar după măsurarea câștigului. JSON rămâne pentru diagnostic; imagini/depth sunt binare, fără base64 în calea live. Codec/depth precision se declară; preview comprimat nu devine automat intrare metrică.

| Flux propus | ROS/type conceptual | Politică inițială |
|---|---|---|
| /r01/camera/rgb, depth, camera_info | sensor_msgs/Image, CameraInfo | best effort/volatile, keep_last 2, rate și TTL profil; frame bundle IDs |
| /r01/phone/pose | eva_msgs/TimedPose cu uncertainty status | keep_last 5, TTL 100 ms; conversie la tip standard numai dacă validă |
| /r01/objects/observations | eva_msgs/ObjectObservationArray | bounded; observed vs predicted explicit |
| /r01/health | diagnostic_msgs/DiagnosticArray + state | 1 Hz propus; lease 3 s, fără a anula TTL-ul mai strict de percepție |
| /world/revisions | eva_msgs/WorldRevision | reliable, transient_local pentru ultima revizie; assets prin API |
| /r01/tasks/execute | eva_msgs/ExecuteTask action | reliable, ack, feedback, cancel și fencing |
| /tf, /tf_static, /joint_states | tipuri ROS standard | autorități unice, QoS standard verificat la integrare |

Map/control nu împart coada cu video; fiecare conexiune are byte/frame budgets. Consumatorul lent pierde întâi cadre vechi, apoi primește degraded/disconnect. Discovery/namespaces nu sunt autentificare. Certificates per robot, ACL per site și TLS/mTLS pentru gateway; traficul DDS este izolat/autorizat separat. USB-C nu garantează un endpoint IP: probă de transport pe cablu/hub/rețea înainte de alegerea lui ca primar.

## RobotProfile și executarea sarcinilor

Pachetul `robot-profile.zip` conține manifest.json (schema, robot model, urdf hash, units, ROS distro, controller interface versions, base/head/feet/gripper frames, calibration IDs), robot.urdf, surse XACRO, meshes cu hash, semantic.srdf, joint_limits.yaml, controllers.yaml și collision policy. Rezolvarea XACRO se face pe staging cu acces restrâns la pachet; iOS primește URDF rezolvat. Se verifică mesh-uri lipsă, unități, arbore, joint types/mimic, limite, inerții și collision geometry. Fișierul importat nu poate executa scripturi pe telefon. Conversia pentru viewer nu modifică geometria metrică a controlului.

Baseline nou: ROS 2 Lyrical LTS dacă driverul robotului și pachetele obligatorii sunt compatibile; pentru robot vendor pe Jazzy se păstrează Jazzy în control și se califică gateway tipat. Nu se presupune interoperabilitate DDS cross-distro. Matricea R0 trebuie să confirme ROS/Ubuntu/arch/driver/Nav2/MoveIt/ros2_control/RMW. URDF 1.2 din Lyrical oferă funcții noi, dar se exportă subsetul acceptat de toate parserele folosite; capsula nu este presupusă suportată în orice viewer. [Release Lyrical](https://github.com/ros2/ros2_documentation/blob/rolling/source/Releases/Release-Lyrical-Luth.rst).

Exemplu cerere: `{task_id, idempotency_key, robot_id, action:"pick_object", object_id, expected_world_revision, required_pose_age_ms, lease_id, fencing_token, deadline_robot_time_ns}`. Gateway răspunde accepted/rejected și motiv; executorul persistă starea accepted→planning→executing→verifying→succeeded/failed/cancelled. Feedback include step/progress, robot state și observații. Cancel returnează cancel_requested, apoi cancelled numai când controlerul confirmă starea fizică stabilă. Timeout nu se traduce în succes sau retry automat de prindere.

Un lease pentru obiect/sarcină este alocat tranzacțional de server și are fencing_token monoton; executorul respinge token vechi. La partition, expirarea impune oprire/aducere în stare stabilă conform contractului controlerului. Serverul nu reatribuie resursa până nu are confirmarea opririi/stării stabile ori un mecanism fizic de fencing verificabil; expirarea unui timer pe server nu dovedește că robotul izolat s-a oprit. Dacă nu există confirmare, resursa rămâne indisponibilă și se cere recuperare. Zonele înguste au rezervări; evitarea locală a persoanelor/roboților rămâne activă indiferent de planul flotei. Exactly-once în baza de date nu garantează exactly-once fizic: înainte de retry se verifică mâna, contactul și starea obiectului.

Poarta simulator→motor enable: RobotProfile validat; TF/timing/restart fault tests trecute; collision/self-mask tests; limite/stop/watchdog confirmate de responsabilul robotului; repetare pe banc; profil de viteză/calibrare și buget de eroare aprobate pentru hardware-ul real. Telefonul și LLM nu publică cupluri. Controlerul de echilibru decide reacția stabilă la percepție pierdută. Emergency stop fizic are cale independentă; vocea/gesturile sunt comenzi suplimentare.

## Probe sintetice obligatorii

12 fixtures: trei translații pe axe, trei rotații pe axe, compunere/inversă, schimbare de bază, cap mobil cu obiect fix, calibrare montaj, map correction fără salt odom, clock mapping cu drift. Toleranță numerică fixture double: 1e-6 m/rad. Testele nu substituie calibrarea fizică. Se adaugă 100 restarturi și 1000 mesaje duplicate/late/epoch invalide, toate cu reject/accept așteptat verificabil.

Surse de convenții: [REP 103](https://www.ros.org/reps/rep-0103.html), [REP 105](https://www.ros.org/reps/rep-0105.html), [Apple collaborative session](https://developer.apple.com/documentation/arkit/creating-a-collaborative-session), [MoveIt URDF/SRDF](https://moveit.picknik.ai/main/doc/examples/urdf_srdf/urdf_srdf_tutorial.html). Restul contractului este proiectarea propusă EVA, nu o capabilitate existentă a acestor biblioteci.
