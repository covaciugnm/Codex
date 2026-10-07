# Viziune, poziționare și cooperare multi-robot — 6 octombrie 2026

Raport al specialistului viziune/robotică. Domeniu: recomandări pentru EVA-3DScan, telefon montat pe humanoid, calculatorul robotului și server comun. Cercetare prin surse primare accesate la 2026-10-06. Nu s-au instalat modele, nu s-a modificat aplicația și nu s-au executat benchmarkuri pe hardware-ul utilizatorului. Performanțele și compatibilitatea fizică rămân criterii de validat, nu rezultate obținute.

## Decizia propusă

Păstrăm ARKit drept odometrie vizual-inerțială locală pe iPhone; construim geometria metrică din RGB-D măsurat; adăugăm pe server segmentare cu vocabular deschis, estimare 6DoF, relocalizare și optimizare de hartă. Memoria comună are observații imuabile, identități persistente și revizii server. Controlul rapid al robotului rămâne pe calculatorul său, cu feedback de la articulații și senzori.

Folosirea maximă a resurselor înseamnă selectarea adaptivă a mai multor metode complementare și măsurarea beneficiului fiecăreia. Nu încărcăm simultan toate modelele în memoria telefonului. Două modele antrenate similar nu reprezintă automat două confirmări independente.

## Registrul metodelor disponibile și selecția

| Componentă | Alegere propusă | Challenger / fallback | Disponibilitate, licență și efort |
|---|---|---|---|
| Odometrie telefon | ARKit world tracking + depth/confidence, un singur proprietar al ARSession | Relocalizare server și repere fizice; comparație cu RTAB-Map | API Apple pe telefon; verificare runtime a fiecărei capabilități. Nu tratăm harta AR ca format universal multi-robot |
| Structura locuinței | RoomPlan MultiRoom + geometrie AR, aceeași origine validată | Reconstrucție RGB-D server | Apple permite ARSession personalizată; relocalizarea ulterioară cere păstrarea hărții. Sursă [A1] |
| Geometrie navigabilă | TSDF/ESDF prin nvblox dacă există GPU NVIDIA | RTAB-Map + reprezentare volumetrică CPU adecvată | nvblox Apache-2.0, CUDA; nu este port iOS gata făcut. [V1] |
| Detectare/segmentare locală | Benchmark YOLO26 n/s-seg convertit Core ML, păstrând modelul actual ca referință | RF-DETR Nano/Small pentru portare evaluată separat | YOLO26 are export CoreML și AGPL/comercial; RF-DETR are cod Apache și modele cu termeni diferențiați; conversia nu garantează ANE/fps. [V2–V3] |
| Segmentare semantică server | SAM 3.1 pentru text, exemple vizuale și tracking de instanțe | Detector local și măști existente; model compact când serverul nu este disponibil | Actualizare oficială 27.03.2026; CUDA, Python >=3.12, PyTorch >=2.7; checkpoint cu acces aprobat și SAM License. Nu propunem acest model ca port iOS imediat. [V4] |
| 6DoF obiect cunoscut, telefon | ARKit iOS27 `.referenceobject` și `trackingObjects`, model creat în Create ML | FoundationPose server, tracking geometric local limitat | API Apple documentat pentru iOS27; maximum10 fișiere referenceobject/session combinat cu detectionObjects, fără mix cu vechiul arobject; gate SDK/runtime și test termic. [A3] |
| 6DoF obiect cunoscut, server | FoundationPose Inference Library, pe RGB-D + mască + CAD | MegaPose drept comparator independent | Runtime NVIDIA nou, C ABI și multi-obiect, cod Apache; weights separat. FoundationPose original are altă licență. MegaPose Apache. [V5–V7] |
| 6DoF obiect fără CAD | Scanare multiview metrică și apoi tracking pe modelul rezultat | Any6D cu ancoră RGB-D; FoundationPose model-free | Any6D disponibil ca cercetare CUDA; dependențe și weights multiple de verificat separat. Nu este promisiune de poziție absolută corectă din orice fotografie. [V8] |
| Reconstrucție neurală server | VGGT-Omega și DA3 ca experimente pentru completare/relocalizare | Reconstrucție geometrică RGB-D măsurată | VGGT-Omega are checkpoint separat recomandat pentru benchmark din septembrie 2026; weights cu acces aprobat. DA3 Small/Base și Metric-Large sunt Apache; Large/Giant/Nested au termeni NC. [V9–V10] |
| Model 3D generativ obiect | SAM 3D Objects, opțional, arhivare și ipoteze de formă | Scanare fizică multiview | Setup oficial cere Linux și GPU NVIDIA cu cel puțin 32 GB VRAM; SAM License, acces la weights. Suprafețele nevăzute sunt inferate. [V11] |
| Relocalizare între roboți | Keyframe retrieval + verificare geometrică hloc/LightGlue/ALIKED + graph optimization | Fiduciale de cameră și aliniere operator; RTAB-Map | LightGlue cod/weights Apache; ALIKED BSD. SuperPoint are termeni diferiți, nu moștenește automat Apache. [V12] |
| Context spațial | WorldModel propriu versionat; Hydra ca adaptor/comparator scene graph | Relații geometrice deterministe | Hydra este ROS2 implicit și testat upstream pe Ubuntu24.04/Jazzy; BSD-2-Clause, cod de cercetare. [V13] |
| Prindere | GraspGenX pe server/robot GPU + verificare cinematică și coliziuni | Grasps parametrizate pentru primele obiecte/gripper | Lansare cod/weights 01.06.2026, condiționare pe configurația mâinii; cod Apache, checkpoints NVIDIA Open Model License. [V14] |
| Generare mișcare | MoveIt 2 + executor robot, cuRoboV2 ca accelerator/challenger | Planificator CPU deja integrabil în MoveIt | cuRoboV2 API diferit de v1, CUDA/PyTorch/Warp, Apache; bibliotecă de mișcare, nu controler universal de mers. [V15] |

Se verifică licența exactului fișier de weights, a codului și a dependențelor tranzitive. Alegerea unei familii cu licență permisivă nu aprobă toate dimensiunile ori toate modelele sale. RF-DETR Plus XL/2XL detecție este PML; documentații mai vechi despre segmentare au etichete diferite, de aceea manifestul versiunii efectiv descărcate este obligatoriu.

### Matrice operațională pentru calificare (completare AV1-01)

Toate rândurile sunt disponibile upstream/documentate, dar necalificate pe EVA. „Gate” înseamnă task obligatoriu înainte de descărcarea/promovarea variantei respective, cu owner ML/DevOps pentru licențe și conversie, owner iOS pentru API/capabilități. Chiar o licență identificată se înregistrează cu hash la checkpoint-ul ales.

| Metodă, sursă | Input → output | Cod | Weights/assets | Destinație/maturitate | Criteriu de selecție |
|---|---|---|---|---|---|
| ARKit/RoomPlan [A1–A3] | Camere/senzori + referință opțională → camera pose/depth/mesh/room/object anchor | Framework proprietar Apple SDK | Modele sistem Apple; referenceobject propriu antrenat Create ML, drepturi asset de verificat | Nativ iOS; noul tracking necesită iOS27/SDK corespunzător | Baseline dacă suportat; tracking object ales când local/offline și catalogul activ încape în10 referințe; măsurare deriva/termic |
| YOLO26 n/s [V2] | RGB → boxes/masks/clase, după task | AGPL-3.0 sau enterprise | Aceeași alegere de licențiere pentru modelul oficial, documentată pe artifact | Server disponibil; export CoreML documentat, ANE real nevalidat | Cel mai bun succes local sub buget susținut, fără regresie față baseline; obligațiile licenței îndeplinite |
| RF-DETR N/S [V3] | RGB → boxes/masks conform checkpointului | Apache pentru rfdetr; Plus PML | Apache-designated N/S; exact seg checkpoint gate; XL/2XL detection PML | Server PyTorch/ONNX; port CoreML experimental | Challenger dacă măști/obiecte mici îmbunătățesc metricile suficient pentru costul de memorie |
| SAM3.1 [V4] | RGB/video + text/points/exemplar → măști/scoruri/track IDs locale | SAM License | SAM License, download gated | Server CUDA, implementare publică; fără port iOS oficial verificat | Server pentru concepte noi și tracking greu; păstrat dacă crește recall fără false merge și respectă deadline |
| FoundationPose nou [V5–V6] | RGB+depth metric+K+mask+mesh/referințe → SE3 object-to-camera + score | Apache runtime; renderer opțional nvdiffrast are licență separată | NVIDIA Open Model License pentru ruta oficială nvidia/foundationpose; snapshot gate | NVIDIA CUDA/TensorRT; producție EVA nevalidată | Primul candidat server pt6D datorită runtime integrabil; promovează numai pe BOP/task metric și time budget |
| MegaPose [V7] | RGB, CAD și detecții, depth dacă pipeline ales → pose6D/ipoteze | Apache-2.0 | Checkpoint exact și dependențe de download: gate separat; licența repo nu ajunge | Cercetare GPU, comparator | Comparator reproductibil când licențele artefactelor se confirmă; păstrat dacă acoperă eșecuri FoundationPose |
| Any6D [V8] | O ancoră RGB-D și query → pose6D/scară | Licența efectivă și componenta FoundationPose: gate | FoundationPose/SAM2/InstantMesh fiecare cu gate separat | Cercetare CUDA; nu candidat release până la gate | Obiecte fără CAD, dacă depășește scanare+tracking pe setul separat, inclusiv simetrii |
| DA3 [V10] | Imagini una/multiple, pose opțional → depth/confidence/camera; outputs depind de model | Apache-2.0 | Small/Base/Metric-Large/Mono-Large Apache; Large/Giant/Nested CC BY-NC4 | Server; port compact iOS nevalidat | Completare/diagnostic, niciodată transformarea automată a adâncimii inferate în măsurare; variantă licențiată pt scop |
| VGGT-Omega [V9] | Mai multe imagini → intrinseci/extrinseci/depth/confidence | Licență custom în LICENSE: gate de aprobare utilizare | Acces gated și termeni exactului checkpoint: gate | GPU CUDA, cercetare; benchmark checkpoint Sept2026 | Doar dacă îmbunătățește reconstrucția/recuperarea comparativ cu geometria măsurată și intră în VRAM |
| SAM3D [V11] | RGB+mask → geometrie/textură/layout generate | SAM License | SAM License, acces gated | Linux/NVIDIA>=32GB upstream, batch | Catalog vizual/ipoteze; suprafețele generate nu sunt acceptate automat pt coliziuni și contact |
| hloc/LightGlue/ALIKED [V12] | Keyframes/features + hartă3D → matches și pose camera cu verificare | hloc BSD-3, LightGlue Apache, ALIKED BSD-3; exact deps gate | LightGlue Apache; detector exact gate; SuperPoint restrictiv | Server CPU/GPU; integrare matură upstream, EVA nevalidat | Relocalizare dacă trece setul de negative repetitive; matching în sine nu este acceptare loop closure |
| nvblox/RTAB-Map/Hydra [V1,V13,V22] | RGB-D, K, odometrie, semantice opțional → TSDF/ESDF, graph/map | Apache/BSD-3/BSD-2 respectiv | N/A pentru baza geometrică; rețele semantice separat | Linux ROS2; nvblox CUDA, fallback CPU RTAB-Map | Alege GPU pentru buget online; fallback CPU dacă hardware absent; Hydra dacă scene graph justifică integrarea |
| GraspGenX [V14] | Point cloud/mesh + descriere gripper → grasp candidates6D și scoruri | Apache-2.0 | NVIDIA Open Model License; assets gripper verificare separată | Server/robot GPU, cercetare disponibilă | Dacă gripperul real este reprezentat corect și succesul fizic depășește grasps simple fără cost inacceptabil |
| cuRoboV2 [V15] | Robot model+joint states+obstacole+goal → traiectorie | Apache-2.0 | Nu weights universal; assets robot cu licențe proprii | CUDA/PyTorch/Warp, integrare APIv2 necesară | Dacă accelerează planificarea cu validări collision/joint/torque; executor și echilibru rămân separate |

Înainte de promovare, toate gate-urile rândului se închid într-un model manifest semnat. Challenger-ele nerezolvate rămân dezactivate; un astfel de gate nu blochează baseline-ul disponibil și licențiat.

### Alternative recente evaluate, dar fără promovare automată

- **MASt3R-SLAM:** comparator server pentru SLAM neural; licență necomercială și ecosistem CUDA. Nu înlocuiește din start VIO metric local. [V16]
- **CoMo3R-SLAM:** implementare colaborativă nouă, lucrare încă în review, exemplu exterior cu două fluxuri și dependențe MASt3R. Rămâne experiment de laborator, nu fundamentul inițial al flotei. [V17]
- **Kimera-Multi:** arhitectură relevantă pentru verificarea loop closures și optimizare distribuită, dar repo consultat cere ROS Noetic/Ubuntu20.04 și spune că exemplul disponibil nu rezolvă comunicația intermitentă între masters. Folosim ideile și benchmarkul, nu promitem instalare directă ROS2. [V18]
- **Fast-FoundationStereo:** util doar dacă avem pereche stereo sincronizată, rectificată și calibrată. Nu presupunem că două camere accesibile ale telefonului furnizează automat un stereo robotic utilizabil. [V19]
- **Event6D:** metodă 2026 interesantă pentru tracking rapid, dar necesită cameră de evenimente. Nu există motiv să o includem în profilul telefonului fără acest senzor. [V20]
- **OrienPose:** lucrare/cod public 2026 pentru obiecte necunoscute din referință unică; candidat de cercetare după auditul efectiv al weights/licenței și comparație pe date EVA. Nu substituie geometria observată. [V21]

Niciuna dintre aceste alegeri nu este declarată universal „cea mai bună”. Recomandarea este o listă verificată de metode disponibile, cu competiție pe datele și hardware-ul proiectului.

**Actualizare importantă față de ARKit vechi:** documentația Apple actuală permite pe iOS27 referințe antrenate în Create ML și tracking al obiectelor mobile la frecvența formatului video selectat. Pentru obiecte staționare folosim detectionObjects, iar trackingObjects se activează pentru țintele active, deoarece crește consumul. Catalogul aplicației poate avea multe obiecte, dar sesiunea încarcă un working set de maximum10 fișiere referenceobject, ales după cameră și sarcină. ARObjectAnchor.isTracked controlează validitatea observației; un anchor păstrat nu dovedește vizibilitate curentă. Comparăm această cale nativă cu FoundationPose pe aceleași obiecte, fără să afirmăm deja superioritatea uneia. [A3]

## Contractul metric și temporal obligatoriu

Fiecare pachet de senzor trebuie să conțină `robot_id`, `device_id`, `session_id`, `clock_epoch`, `map_id`, `map_revision`, `calibration_id`, `frame_id`, `capture_time_monotonic`, timestamp convertit în ceasul robotului cu incertitudine, `sequence`, intrinseci și transformări. RGB, depth, confidence, masca și pose-ul trebuie legate la aceeași captură. Nu reconstruim metric din MP4 fără aceste metadate.

Propunere TF pentru robotul R: `building_map -> R/odom -> R/base_link -> ... -> R/head_link -> R/iphone_mount -> R/iphone_camera_optical`. Fiecare muchie are un singur publisher autoritar. `map->odom` admite corecțiile globale, `odom->base_link` trebuie să rămână continuu. Mișcarea capului se obține din articulații măsurate la timpul capturii, nu din ultima comandă trimisă servo-ului. Convențiile urmează REP103/105. [R1–R2]

Transformarea ARKit->ROS se implementează și testează explicit; nu etichetăm coordonate world drept optical. Un reset AR produce o nouă epocă a originii. O observație din epoca veche nu poate fi combinată cu noua hartă fără o transformare validată.

Un obiect are pose SE(3), simetrii cunoscute, validitatea orientării, dimensiuni măsurate/estimate, covarianță definită prin convenție, proveniență și vârstă. Un cilindru simetric poate avea yaw neobservabil; nu se inventează precizie prin quaternion identitate. În modelul EVA, incertitudinea necunoscută are câmp explicit; nu se presupune că `-1` este convenție universală pentru orice mesaj ROS.

ARKit și o reconstrucție server din aceleași imagini nu sunt senzori statistic independenți. Păstrăm identificatorii observațiilor comune; fuziunea evită numărarea dublă. Pentru estimări cu corelație necunoscută folosim selecție conservatoare ori metodă explicită, precum covariance intersection, verificată separat.

## Două sau mai multe telefoane în aceeași cameră

1. Telefonul se autentifică într-un `site_id` și primește identitate de robot și drepturi pe cameră; fiecare păstrează harta locală până la aliniere.
2. Se încearcă alinierea pe repere vizuale cunoscute sau prin keyframe retrieval și verificare geometrică robustă, cu minim de suprapunere măsurat. Asemănarea semantică „aceeași canapea” nu este suficientă.
3. Serverul păstrează `T_building_localmap`, covarianță, dovezi și revizie. Alinierea insuficient observabilă rămâne pending; nu contaminează harta comună.
4. Observațiile sunt evenimente imuabile cu UUID și origine. ID-ul track-ului local este separat de ID-ul instanței persistente. Asocierea globală verifică geometria, aspectul, dimensiunile, timpul și relațiile.
5. Două rapoarte contradictorii produc ipoteze/cerere de reobservare. Nu facem media a două căni distincte și nu lăsăm ultimul timestamp al telefonului să decidă adevărul fizic.
6. Serverul atribuie un cursor monoton de schimbări. Offline, telefoanele păstrează outbox; upload idempotent, replay, tombstones și conflicte bazate pe revizie. Hărțile și obiectele fac parte din snapshot-uri compatibile.
7. Întreruperea legăturii nu oprește percepția locală. Datele comune îmbătrânesc explicit. Misiunile care cer rezervarea unui obiect sau a unei uși folosesc lease și fencing token; după pierderea autorității nu se continuă operația exclusivă.
8. O cerere către robotul A nu poate acționa robotul B: namespace și ACL per robot, `target_robot_id`, autorizare la executor, chei separate. `ROS_DOMAIN_ID` este separare de descoperire, nu autentificare.

Apple oferă schimb de ARWorldMap/CollaborationData pentru experiențe comune, util ca accelerator între iPhone-uri. Transportul îl implementează aplicația; API-ul nu furnizează singur inventar semantic, consens, versiuni persistente și reguli de conflict. [A2]

Memoria server: PostgreSQL existent pentru metadate/evenimente, obiecte blob cu hash pentru hărți și media, index de descriptori cu versiunea embeddingului; graf de relații inițial în schema existentă, fără a impune o bază de graf suplimentară înainte de necesitate. Operațiile `merge_id` și `split_id` trebuie reversibile și auditate.

## Transport și procesare server

Păstrăm trei canale logice: observații efemere recente; tranzacții de hartă/inventar; comenzi și feedback. Pentru fluxurile vizuale contează deadline și prospețime, cu cozi limitate. Pentru mapări contează livrare fiabilă, hash, confirmare și reluare. Setările QoS ROS trebuie compatibile publisher/subscriber; datele de senzori pot utiliza best-effort/volatile cu coadă scurtă, hărțile reliable/transient-local, cu versionare în aplicație. [R3]

Dimensionare exemplificativă, calculată, nu măsurată: RGB 1280×720×3×30 = 82,94 MB/s necomprimat/telefon; depth 256×192×2×15 = 1,47 MB/s înainte de confidence/metadate. Pentru N telefoane se multiplică și se adaugă overhead. Rezoluțiile sunt exemple pentru calcul, nu specificații declarate ale iPhone-ului. Video comprimat se trimite adaptiv, plus keyframes de calitate și depth lossless/quantizat documentat; MP4 vizual nu devine sursa metrică unică.

Servicii propuse: `sensor-gateway`, `world-model`, `map-builder`, `semantic-inference`, `pose-estimator`, `grasp-planner`, `model-registry`, `replay-evaluator`. Coada fiecărui job are lease, heartbeat, număr de încercări, backoff, anulare și idempotency key. Rezultatul păstrează versiunile inputului și ale modelului; un rezultat pentru o hartă veche nu suprascrie orb noua revizie.

Serverul confirmă, rafinează și reproiectează observațiile către telefon; trimite motivul dezacordului și poate cere o vedere suplimentară. Telefonul păstrează distinct observația locală și revizia fuzionată. Obiectele ascunse rămân neobservate; absența se afirmă numai după verificarea zonei vizibile.

## Profiluri de resurse și instalare ulterioară

Nu este cunoscut inventarul serverului real. Înainte de alegerea definitivă se colectează OS, CPU/RAM, GPU/VRAM, driver, arhitectură x86/ARM, stocare, rețea și sarcini existente. Se măsoară simultan numărul de roboți, rezoluția și p95/p99 latența. Bugetele de mai jos sunt propuneri de laborator, nu minime universale.

- **Profil telefon:** VIO/depth/local tracking continuu; un detector compact; descriptor și recunoaștere la cerere; înregistrare cu retenție. Modelele mai grele se descarcă doar când sunt selectate și licențiate. Se testează temperatură și presiunea memoriei timp de minimum o oră.
- **Profil fără GPU NVIDIA:** servicii, sincronizare, replay și geometrie CPU; percepție locală telefon; joburi grele amânate. Sistemul rămâne util fără SAM3/FoundationPose CUDA.
- **Profil laborator GPU 24–48 GB:** zonă de experiment propusă pentru inferență server, batching controlat și mai multe modele încărcate selectiv. SAM3D are cerință upstream de minimum32 GB; un GPU24 GB nu o satisface. Concurența completă poate cere GPU-uri separate și se dimensionează prin măsurare.
- **Profil flotă:** separarea serviciilor de control/metadata de lucrările GPU; cote per robot, admission control, prioritizare după deadline și observabilitate. Numărul de telefoane suportate nu se promite înaintea probei de încărcare.

Pași de instalare în faza de implementare:

1. Fixare matrice OS–ROS–CUDA–driver și manifest de commituri/weights SHA256/licențe. ROS2 Lyrical există din mai2026; pentru Hydra baseline-ul verificat upstream este Jazzy/Ubuntu24.04. Alegerea celei mai noi distribuții depinde de toate driverele și pachetele robotului. [R4]
2. Mediu separat de site-ul existent, cu volume versionate, backup/restaurare testate și conturi de servicii. Nu actualizăm driverul serverului de producție pentru un singur experiment fără verificarea celorlalte workload-uri.
3. Containere distincte pentru dependențe incompatibile. SAM3 și FoundationPose nou nu împart obligatoriu aceeași imagine. Pentru FoundationPose nou upstream indică driver>=580, CUDA13.2/TensorRT10.16 și compatibilitate x86 CC>=7.5 sau Thor/JetPack7; aceasta nu validează automat alte Jetson-uri. [V5]
4. Reproducerea exemplului oficial al fiecărui candidat; apoi adaptor comun cu input/output metric, timeout, schema și test de paritate. Conversiile CoreML/ONNX/TensorRT se compară numeric cu modelul original.
5. Evaluare pe setul EVA separat de datele de antrenare. Activare shadow: candidatul produce rezultate fără a schimba mișcarea robotului. Promovare doar după criterii îndeplinite și rollback testat.
6. Pentru fiecare serviciu se livrează Dockerfile/lockfile, configurare, cerințe, model card, comenzi start/stop/health, backup, runbook de incident și procedură downgrade. Parametrii exactului server se completează după inventar; nu inventăm comenzi hardware universale.

## Teste de acceptare propuse și experimente

Toate valorile numerice de mai jos sunt ținte inițiale de proiect, nu rezultate și nu specificații Apple. Pentru mers/manipulare, limitele finale se derivă din viteză, frânare, gabarit, prindere și incertitudine; dacă acestea nu sunt cunoscute, execuția fizică nu este validată.

| Test / măsură | Metodă și criteriu propus |
|---|---|
| Reper/timp/reset | Replay sintetic și real cu telefon mobil/obiect fix; zero amestecări de epoci, zero timestamp-uri atribuite procesării; transformări numerice și normalizare quaternion |
| Localizare cameră | Traseu cu ground truth independent; raport ATE/RPE în metri și grade, SE(3) fără rescalare care ascunde drift metric; țintă inițială p95 poziție <=5cm pentru inventar în camera de test |
| Relocalizare și map merge | Minimum20 încercări, schimbări de lumină și două camere asemănătoare; >=95% relocalizări corecte în10s și zero false merge în setul negativ; nereușita este explicită |
| Identități obiecte | Minimum30 instanțe, incluzând perechi identice și mutări; IDF1/HOTA, false merge/split, erori de poziție și rezultatele pe fiecare categorie, nu doar media |
| 6DoF | Dataset CAD și necunoscut separat; BOP ADD-S/VSD ori echivalent pentru simetrii, eroare translație/orientație; manipularea cere eroare sub toleranța gripperului, nu prag universal |
| Calitatea geometriei | Distanțe față de măsurători independente, grosimea pereților, completitudine; suprafețe măsurate și generate etichetate distinct; unknown space nu devine automat liber |
| Mai mulți roboți | 2 apoi4 telefoane, fiecare cu origine inițială diferită; neconectare60s, reorder, duplicate, restart server și observații contradictorii; convergență la aceeași revizie și zero comenzi încrucișate |
| Prospețime | p50/p95/p99 end-to-end captură–consum, cadru expirat și incertitudine de ceas; țintă inițială p95<150ms pentru telemetria locală, validată față de robot; semantic server<1s pentru căutare nesigură de timp |
| Stabilitate | >=60min cu încărcare reprezentativă; fără OOM/crash, cozi limitate și tranziție predictibilă la profil redus; degradarea termică raportată |
| Prindere | Minimum20 repetări pentru fiecare combinație critică obiect–mână; raport succes și interval de încredere, coliziuni și scăpări; oprire imediată la defecte de transformare sau feedback |
| Ablație | Baseline actual vs fiecare model separat vs combinație; câștig de succes, latență, energie, VRAM și trafic. Două modele se păstrează în producție numai dacă îmbunătățesc ansamblul |

În scene de test includem reflexii, sticlă, suprafețe negre, obiecte mici, ocluzii, persoane în mișcare, obiecte ținute în mână, camere repetitive și rotații rapide ale capului. Vizualizarea frumoasă nu este dovadă de precizie metrică.

## Roadmap al acestui subsistem

**V0 — Fundație corectă:** contracte/timp/TF, reset și sync server monotonic; replay și dataset; niciun upgrade de model nu ocolește această etapă.

**V1 — Un telefon, o cameră:** model compact măsurat pe telefon, scene graph minimal, harta persistentă și criterii de relocalizare; benchmark server SAM3.1/FoundationPose și fallback.

**V2 — Memorie de echipă:** două telefoane, aliniere, evenimente imuabile, identități globale reversibile, conflicte și testele offline; apoi patru telefoane.

**V3 — Robot în buclă:** model robot/calibrare, state estimator, planificator și executor în simulare, apoi hardware; obiecte și gripper limitate inițial pentru măsurarea succesului.

**V4 — Capacități avansate:** obiecte necunoscute, reconstruire neurală, GraspGenX/cuRoboV2, observație activă și distribuirea sarcinilor; promovare din shadow doar pe rezultate.

Livrabile pentru fiecare etapă: ADR cu decizia și alternativele, schema/protocol, manifest software, set de teste și rezultate, runbook, demonstrație și lista limitărilor. Review10/10 al documentului poate confirma că planul este complet și verificabil; nu poate certifica prin text performanța încă nemăsurată a robotului.

## Surse primare consultate

- [A1] Apple RoomPlan MultiRoom/custom ARSession: https://developer.apple.com/videos/play/wwdc2023/10192/
- [A2] Apple colaborare AR: https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration/iscollaborationenabled și https://developer.apple.com/documentation/arkit/creating-a-multiuser-ar-experience
- [A3] Apple object tracking iOS27: https://developer.apple.com/documentation/visionos/using-a-reference-object-with-arkit-in-ios și https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration/trackingobjects și https://developer.apple.com/documentation/visionos/implementing-object-tracking-in-your-app
- [V1] nvblox: https://github.com/nvidia-isaac/nvblox și https://nvidia-isaac.github.io/nvblox/
- [V2] YOLO26: https://github.com/ultralytics/yolo26 și https://www.ultralytics.com/license
- [V3] RF-DETR: https://github.com/roboflow/rf-detr și https://roboflow.com/licensing
- [V4] SAM3/3.1: https://github.com/facebookresearch/sam3 și https://github.com/facebookresearch/sam3/blob/main/LICENSE
- [V5] FoundationPose runtime: https://github.com/nvidia-isaac/foundation-pose-inference-library
- [V6] FoundationPose original/weights: https://github.com/NVlabs/FoundationPose și https://huggingface.co/nvidia/foundationpose
- [V7] MegaPose: https://github.com/megapose6d/megapose6d și https://github.com/megapose6d/megapose6d/blob/master/LICENSE
- [V8] Any6D: https://github.com/taeyeopl/Any6D și https://openaccess.thecvf.com/content/CVPR2025/html/Lee_Any6D_Model-free_6D_Pose_Estimation_of_Novel_Objects_CVPR_2025_paper.html
- [V9] VGGT-Omega: https://github.com/facebookresearch/vggt-omega
- [V10] Depth Anything3: https://github.com/ByteDance-Seed/Depth-Anything-3
- [V11] SAM3D: https://github.com/facebookresearch/sam-3d-objects și https://github.com/facebookresearch/sam-3d-objects/blob/main/doc/setup.md
- [V12] Localizare: https://github.com/cvg/Hierarchical-Localization și https://github.com/cvg/LightGlue
- [V13] Hydra: https://github.com/MIT-SPARK/Hydra
- [V14] GraspGenX: https://github.com/NVlabs/GraspGenX
- [V15] cuRoboV2: https://github.com/NVlabs/curobo
- [V16] MASt3R-SLAM: https://github.com/rmurai0610/MASt3R-SLAM
- [V17] CoMo3R-SLAM: https://github.com/como3r-slam/como3r-slam
- [V18] Kimera-Multi: https://github.com/MIT-SPARK/Kimera-Multi
- [V19] Fast-FoundationStereo: https://github.com/NVlabs/Fast-FoundationStereo
- [V20] Event6D: https://openaccess.thecvf.com/content/CVPR2026/html/Kang_Event6D_Event-based_Novel_Object_6D_Pose_Tracking_CVPR_2026_paper.html
- [V21] OrienPose: https://openaccess.thecvf.com/content/CVPR2026/html/Liu_OrienPose_Orientation-Guided_Novel_View_Synthesis_for_Single-Image_Unseen_Object_Pose_CVPR_2026_paper.html
- [V22] RTAB-Map ROS2: https://github.com/introlab/rtabmap_ros/tree/ros2
- [R1] REP103: https://reps.openrobotics.org/rep-0103/
- [R2] REP105: https://reps.openrobotics.org/rep-0105/
- [R3] ROS2 QoS: https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst
- [R4] ROS2 distribuții: https://github.com/ros2/ros2_documentation/blob/rolling/source/Releases.rst
