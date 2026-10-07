# Plan integrat pentru EVA Robot cu iPhone și server colaborativ

Data 6 octombrie 2026, Europe/Bucharest. Versiunea2 pentru audit independent. Obiectiv: iPhone18 Pro Max1TB ca sistem perceptiv și interfață cognitivă pentru humanoid, cu scanare persistentă, poziții3D/6DoF, persoane, voce, gesturi, navigare, manipulare și memorie comună între roboți. Această etapă livrează planul implementabil; software-ul nou și performanțele fizice nu sunt declarate instalate/testate.

## Decizia principală

Construim un sistem pe trei niveluri. Telefonul captează și percepe local; calculatorul robotului menține TF, estimarea corpului, planificarea și controlul; serverul rulează modelele grele și memoria comună. Un singur coordonator al capturii distribuie RGB/depth/pose/timp tuturor consumatorilor. Datele au origine și prospețime verificabile. Procesarea server poate rafina observațiile și cere noi vederi, fără a înlocui automat un rezultat recent cu unul vechi.

Folosim maximum de metode relevante în cercetare, în două regimuri: buget egal pentru comparație eficientă și capacitate maximă cu serverul dimensionat pentru model. Varianta mai nouă sau mai mare nu este declarată câștigătoare înainte de benchmark. Modelele complementare pot coexista; schedulerul alege ce rulează continuu și ce rulează la cerere, ca percepția și vocea să nu se blocheze reciproc.

La cererea explicită a utilizatorului, licențele comerciale nu filtrează lista și nu intră în scorul tehnic. Includem research-only, necomercial, custom-license și servicii cu acces controlat. Condițiile de acces/utilizare sunt metadate și prerechizite pentru instalarea efectivă, nu motiv să omitem o tehnologie din analiză.

## Pachetul normativ și ordinea de citire

1. PLAN_V2.md: scop, alegeri, riscuri existente și ordinea implementării.
2. [CONTRACTE_V2.md](CONTRACTE_V2.md): schema spațiu/timp, mesaje, sincronizare, aliniere, RobotProfile și task execution.
3. [EXECUTIE_TESTE_V2.md](EXECUTIE_TESTE_V2.md): instalare, manifest, servicii, resurse, backlog B01–B17 și testele T01–T15.
4. [Raport iPhone iOS](01-specialist-iphone-ios.md), [raport viziune robotică](vision-robotics.md), [modele voce și LLM](03-modele-voce-llm.md), [extinderea candidaților research](04-candidati-research.md): surse primare, alternative și detalii comparative.

La diferențe, CONTRACTE prevalează pentru semantica datelor și EXECUTIE_TESTE pentru praguri/pași. Pentru eligibilitatea research prevalează cererea de mai sus și addendumul04. Rapoartele specialiștilor sunt păstrate ca dovezi ale cercetării; valorile lor inițiale de150ms/60min nu înlocuiesc țintele normative100ms local și3×2ore. PLAN_V1 și auditul5,5/10 sunt istorice, nu instrucțiuni concurente.

## Baza de cod și ce păstrăm

Aplicația analizată este [app la0e71d84](https://github.com/covaciugnm/3dscan.eva-org.com/tree/0e71d84abeb603db4daf81c5917bab58d36dd728); backend/documentație [main la98abc15](https://github.com/covaciugnm/3dscan.eva-org.com/tree/98abc15fbdc5b6ee8c746be637a8094db8e6be3b). Analiza statică precedentă a urmărit RobotPerceptionEngine/Telemetry/Bridge, InventoryModels/Matcher/Session/Sync, backend inventory, SpeechService, FaceRecognition/RobotFaceGreeter, LLMClient și testele Swift.

Păstrăm ARKit/VIO, detectorul curent drept baseline, inventarul și catalogul existent, ideea de context al vecinilor, fețele/STT/TTS, conectorii LLM, jurnalul NDJSON și backend PostgreSQL. Documentația robotică din2octombrie are deja principii utile TF/ceas/uncertitudine; le transformăm în contracte și teste executabile. Statusurile „build green” din documentație nu sunt probe de funcționare fizică obținute în acest audit.

## Corecțiile prioritare și trasabilitatea lor

| ID | Constatare statică | Task și test |
|---|---|---|
| C01 | Poziții world etichetate camera optical în telemetrie | B02/T01: frame contract și SE3 |
| C02 | phone pose timestamp la publicare în locul capturii | B02/T03/T04: capture time și clock mapping |
| C03 | Reset AR+sequence cu sessionID și obiecte vechi păstrate | B03/T01: session/map epoch și async generation |
| C04 | mergeNeural împrospătează timestamp fără poziția track-ului existent | B03/T06: update coerent și monoton |
| C05 | Hartă nouă după load fail; inventarul poate fi salvat fără aliniere | B04/T05: relocalization gate și revision |
| C06 | Nevăzut devine missing fără vizibilitate verificată | B04/T06: occlusion/unknown/absence separate |
| C07 | Cursor client-time și updated_at client pot omite upload offline târziu; erori assets absorbite | B05/T02/T15: server sequencer și asset transaction |
| C08 | Grosime/rotație aproximative; persistent object fără quaternion/reper versionat | B04/B08/T06: validity și provenance |
| C09 | TCP bridge fără auth/backpressure/error handling complet | B10/T03/T08: pairing/TLS/cozi/diagnostic |
| C10 | SFSpeechRecognizer nu impune requiresOnDeviceRecognition | B13/T09: politică local/server și locale gates |
| C11 | Testele Swift principale sunt șabloane | B16/T01–T15: suite domeniu/replay/hardware |

Surse de cod pentru verificare: [motorul](https://github.com/covaciugnm/3dscan.eva-org.com/blob/0e71d84abeb603db4daf81c5917bab58d36dd728/EVA-3DScan/Core/Robot/RobotPerceptionEngine.swift), [telemetria](https://github.com/covaciugnm/3dscan.eva-org.com/blob/0e71d84abeb603db4daf81c5917bab58d36dd728/EVA-3DScan/Core/Robot/RobotTelemetry.swift), [sync aplicație](https://github.com/covaciugnm/3dscan.eva-org.com/blob/0e71d84abeb603db4daf81c5917bab58d36dd728/EVA-3DScan/Core/Sync/InventorySyncService.swift), [sync server](https://github.com/covaciugnm/3dscan.eva-org.com/blob/98abc15fbdc5b6ee8c746be637a8094db8e6be3b/Site/server/inventory.mjs).

## Alegerea tehnologiilor pe telefon

Apple confirmă modelul și stocarea vizate în [specs](https://www.apple.com/iphone-18-pro/specs/). SDK/Xcode27 și API iOS27 se califică prin probes pe dispozitiv. Nu presupunem RAM, fps sau acces simultan la senzori din denumirea telefonului. Cei1TB sunt stocare, nu memorie de inferență.

| Funcție | Prima implementare de evaluat | Extindere și fallback |
|---|---|---|
| VIO/depth/captură | ARKit world tracking, sceneDepth/confidence, coordonator comun | smoothed depth pentru static/vizual; raw depth pentru dinamice după măsurare; oprește utilizarea tracking invalid |
| Camere și clădire | RoomPlan cu aceeași sesiune/origine și StructureBuilder | export geometric propriu+server; harta AR nu este singura memorie persistentă |
| Obiecte cunoscute6D | ARKit iOS27 trackingObjects/detectionObjects din CreateML | FoundationPose server și tracking geometric local |
| Detector/măști | baseline actual vs YOLO26n/s-seg și RF-DETR compact | export CoreML/CoreAI verificat numeric, model selectat pe holdout |
| Modele proprii | CoreML păstrat; CoreAI .aimodel drept challenger modern | operator/format/device support gates și fallback la ruta stabilă |
| Fețe | AuraFace existent/candidat vs SFace | alternative InsightFace research, prag open-set și necunoscut; FaceID database indisponibilă aplicației |
| STT | SpeechAnalyzer/SpeechTranscriber dacă locale există | FluidAudio Parakeet, Argmax/Whisper; server Parakeet RO |
| Speaker ID | embeddings și diarizare FluidAudio în benchmark | pyannote server; enrollment și asociere audio-video separată |
| TTS | AVSpeechSynthesizer cu voce RO/EN verificată | Piper/XTTS research pe server conform03; streaming și barge-in |
| Gesturi | Vision hand/body + clasificator temporal | model multi-person separat; depth pentru indicare3D |
| LLM local | Foundation Models local disponibil sau model CoreAI propriu | server VLM; PCC opțional după entitlement/quota/locale checks |
| Alte funcții | OCR/barcode, IMU timestamped, UWB auxiliar, haptics/display diagnostic | fiecare prin capability manifest; UWB nu furnizează singur6DoF |

Noul tracking iOS are working set de maximum10 fișiere .referenceobject cumulat, fără mix cu .arobject. Catalogul complet poate fi mare pe server, iar telefonul încarcă țintele relevante camerei/sarcinii. CoreAI și Foundation Models iOS27 sunt evaluate explicit; toolkit adapter26.0.0 incompatibil iOS27 nu este ales. PCC este opțiune de cloud Apple cu disponibilitate/cote, nu serverul de flotă. Detaliile și sursele sunt în raportul iOS.

Montajul trebuie să păstreze LiDAR posterior orientat spre scena utilă; dacă acesta privește înainte, ecranul/TrueDepth privesc înapoi. Camerele integrate se rotesc împreună. Nu deducem vedere360 simultană dintr-o hartă panoramică. MultiCam și combinațiile ARKit/TrueDepth se probează pe formate concrete; lipsa suportului duce la alternare declarată ori senzor extern pe robot. Mod foreground cu întreruperi gestionate și watchdog robot; background/lock nu garantează captură continuă.

## Metodele mai capabile pe server

| Sarcină | Stack de pornire | Research challengers și rol |
|---|---|---|
| Segmentare open-vocabulary | SAM3.1, detector local pentru fallback | RF-DETR mare/Plus și modele specializate; comparație pe obiectele EVA |
| Pose6D cunoscut | FoundationPose Inference Library | FoundationPose original/MegaPose, benchmark independent; RGBD+mask+CAD |
| Pose fără CAD | scanare multiview metrică apoi tracking | Any6D, OrienPose, FoundationPose model-free; ambiguitate/scară evaluate |
| Geometrie/reconstrucție | nvblox TSDF/ESDF sau RTAB-Map CPU | VGGT-Omega, DA3 inclusiv Large/Giant/Nested, SAM3D; măsurat vs inferat separat |
| Relocalizare/cooperare | hloc/LightGlue/ALIKED, geometric verification și pose graph | MASt3R-SLAM, CoMo3R-SLAM, Kimera-Multi ca experiment/port, Hydra scene graph |
| Prindere/planificare | MoveIt2 și grasps verificate pentru mâna reală | GraspGenX, cuRoboV2; nu înlocuiesc echilibrul biped |
| VLM/LLM | Qwen3.5-9B drept candidat compact | Qwen3.6-35B-A3B și Gemma4-31B-it, comparație independentă și resurse reale |
| Audio | Parakeet TDT0.6Bv3 RO/EN și pyannote community1 | metode din03 și variante premium accesibile; WER/DER/FAR pe zgomotul real |
| Senzori suplimentari | RGBD iPhone măsurat | Fast-FoundationStereo numai cu stereo calibrat; Event6D numai cu cameră de evenimente |

SAM3.1, runtime-ul FoundationPose, VGGT-Omega, DA3, GraspGenX și cuRoboV2 au surse primare actuale în raportul vision. Nu prezentăm stack-uri CUDA ca instalări iPhone gata făcute. Modelele mari cu cerințe32GB VRAM ori drivere specifice primesc worker compatibil; serverul existent nu este presupus capabil fără inventar. Suprafața generată de un model nu devine dovadă de contact/spațiu liber. Modelele nu sunt eliminate pentru lipsa licenței comerciale în acest proiect research; variantele includ pe cele restrictive în04.

Sursa pentru suportul limbii române și parametri Parakeet: [model card NVIDIA](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3). Diarizarea server este evaluată prin [pyannote community1](https://huggingface.co/pyannote/speaker-diarization-community-1). Existența limbii într-un model nu garantează precizia în camera robotului.

## Memoria comună și colaborarea

WorldModel unifică percepția live, inventarul, catalogul3D și contextul conversațional. Entitățile formează clădire→etaj→cameră→obiect, cu relații on/in/near/held_by, istoric, prospețime și identitate stabilă. Actuala asociere cu vecinii se extinde cu appearance embeddings, geometrie relațională, scor minim, diferență față al doilea candidat și asociere globală; matching-ul greedy nu este suficient pentru două scaune identice.

Două telefoane pornesc în origini separate. Serverul validează alinierea pe repere și corespondențe geometrice, apoi asociază observații la aceleași obiecte. Conflictele rămân ipoteze și cer reobservare; ultimul timestamp de telefon nu definește adevărul. Modificările offline primesc cursor server nou, indiferent de data capturii. Hărțile+assets+obiectele se aplică atomic, cu checksum și revision.

ARKit CollaborationData poate accelera alinierea locală; Apple recomandă până la4 participanți pentru rezultate bune. Nu este baza semantică permanentă și nu presupunem compatibilitate cross-iOS universală. Pentru mai multe telefoane, submaps și graph server păstrează identitatea. Object/task leases cu fencing împiedică doi roboți să revendice același obiect; lipsa confirmării că un robot izolat s-a oprit blochează reatribuirea, chiar dacă timerul server a expirat.

## De la cererea umană la acțiune

Scenariul de referință este „Adu cana de lângă monitor”. Sistemul identifică vorbitorul când are dovezi suficiente, transcrie, caută obiectul prin relațiile scenei, verifică identitatea și vechimea, planifică navigarea, reobservă cana și cere prinderea. Executorul validează pose, coliziuni, lease și feedback de contact, apoi confirmă rezultatul. O cerere ambiguă produce clarificare; un retry după timeout verifică efectul fizic înainte să repete comanda.

URDF/XACRO/SRDF și calibrarea se importă ca RobotProfile versionat, cu mesh-uri/limite/controlere și unități verificate. LLM primește tool-uri tipate, nu acces liber la actuatoare. Calculatorul robotului păstrează echilibrul și controlul; telefonul furnizează observații/intenții. Serverul comun poate coordona explorarea și sarcinile, însă evitarea locală și watchdog-ul nu depind de disponibilitatea lui.

## Etapele și rezultatele așteptate

| Poartă | Livrabil | Condiție de închidere |
|---|---|---|
| G0 | Inventar și manifest baseline | B01, compatibilitate și date necesare cunoscute |
| G1 | Corectitudine spațiu/timp/sync | C01–C07/C09 și partea de schemă C08, teste unitare/fixtures implementate odată cu fiecare corecție; C10 se califică G5, C11 complet se închide G6 |
| G2 | Un telefon și o cameră persistentă | capture owner, detector/6D bake-off, WorldModel și relocalizare |
| G3 | Doi apoi patru roboți colaboratori | map alignment, convergență, no false merge, ownership și isolation |
| G4 | Robot în simulator și pe banc | RobotProfile, TF, clock, watchdog și toleranțe fizice aprobate |
| G5 | Interacțiune și task complet | RO/EN, faces/voice/gestures, typed tools, demonstrația cană |
| G6 | Funcționare continuă și release | T01–T15, rollback, backup,3×2ore și raport eșecuri |
| G7 | Capacitate maximă de cercetare | B17, modele grele/alternative cu ablații și promovare bazată pe date |

B01–B17 din EXECUTIE_TESTE stabilesc rolurile, fișierele, dependențele și Definition of Done. Calendarul se estimează după inventar/spikes; nu promitem durate fără modelul robotului, server și echipa de implementare. Aceste date lipsă sunt intrări de G0, nu motive să lăsăm schema sau pașii neprecizați.

## Răspuns la auditul V1

| Constatare | Remediere V2 |
|---|---|
| AV1-01 metode/comparație | Matricele iOS/vision/03/04, baseline+challenger+I/O+hardware+source și metodologia Pareto |
| AV1-02 spațiu/timp | CONTRACTE: ecuații, axe, timestamp, uncertainty, exemplu mesaj, reject/dedup,12 fixtures |
| AV1-03 sync/map merge | CONTRACTE: handshake, sequencer, outbox/assets atomic, snapshot, conflicts, 2-phone example |
| AV1-04 Apple modern | iOS27/CoreAI/referenceobjects/PCC, availability și fallback în raport și plan |
| AV1-05 ținte | T01–T15 normative cu dataset, procedură, pass/fail și precedență față rapoarte |
| AV1-06 instalare | EXECUTIE_TESTE: inventory, manifest, servicii, profiles,8 pași, backup/rollback |
| AV1-07 robot/executor | CONTRACTE: RobotProfile, distro compatibility, action state machine, fencing și motor gate |
| AV1-08 roadmap | B01–B17 cu owner/deps/deliverable/DoD și G0–G7 |

## Limita verdictului și continuarea

Auditorul evaluează documentația și implementabilitatea ei, cu hash pentru fiecare fișier. Nota10/10 nu înseamnă că robotul a atins deja o precizie, autonomie sau fiabilitate. Build, install și probe hardware au status not_run până se atașează rezultate. Următoarea etapă după acceptarea dosarului este B01, apoi corecțiile P0, păstrând experimentele grele în staging.

Toate versiunile și auditurile se păstrează în folderul GitHub datat. Dacă execuția acestei etape se întrerupe din cauza usage, RELUARE.md indică artefactele, constatările și pasul următor; nu se marchează final un audit incomplet.
