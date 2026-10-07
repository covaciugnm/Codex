# Instalare roadmap și calificare EVA Robot

Data 6 octombrie 2026. Specificație de implementare pentru PLAN_V2. Toate țintele numerice sunt cerințe inițiale propuse, nu rezultate obținute. Acest fișier prevalează asupra pragurilor diferite din rapoartele specialiștilor. Scripturile/serviciile numite ca livrabile trebuie construite în taskurile de mai jos; nu sunt prezentate drept fișiere deja existente.

## Domeniul cercetării

Cererea utilizatorului din 6 octombrie include toate opțiunile tehnice, inclusiv research-only, necomerciale, custom-license și servicii comerciale. Licența comercială nu este criteriu de scor și nu elimină un candidat. Condițiile de acces, entitlement, descărcare și utilizare se consemnează în manifest înaintea experimentului; un model fără acces se marchează blocked_access, nu se declară inferior. Limitările fizice și lipsa unui senzor rămân criterii tehnice.

## Inventarul obligatoriu R0

Owner DevOps: OS/arch, CPU, RAM, GPU model/VRAM/driver, CUDA disponibil, disc și IOPS, rețea, servicii existente și ferestre de operare. Owner iOS: model/build iOS, Xcode/SDK/build Mac, provisionare, API capability matrix, senzori și profile captură/audio, cote disc și memorie observată. Owner robot: model/firmware/ROS, SDK, articulații/encodere/IMU/contacte, gripper, URDF/SRDF, controlere, viteze și mecanism stop. Inventarul real nu a fost furnizat încă; taskurile dependente nu presupun un GPU/robot fictiv.

Comenzi read-only pentru inventar, executate ulterior pe hostul adecvat, individual:

```bash
uname -a
cat /etc/os-release
lscpu
free -h
lsblk
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
docker version
docker compose version
ros2 doctor --report
```

Lipsa nvidia-smi înseamnă că profilul CUDA rămâne neconfirmat; nu declanșează automat instalarea unui driver. Pe Mac se rulează `xcodebuild -version`, `xcodebuild -showsdks` și `xcodebuild -list` în checkout-ul aplicației; schemele/destinațiile reale se folosesc ulterior în build/test/archive. Inventarul arhivat folosește allowlist de metadate. `ros2 doctor --report` poate include variabile de mediu: outputul brut nu se publică în GitHub, se elimină tokenuri/parole/valori sensibile înainte de arhivare și se verifică rezultatul. La final R0 produce `deployment-lock.json`, `hardware.json`, `capabilities.json` și matricea de compatibilitate.

## Manifestul reproductibil

Fiecare release identifică app/backend commit, Xcode și SDK build, OS/arch, ROS distro și RMW, versiuni pachete, CUDA/TensorRT/PyTorch, containere prin digest, model repository/revision/weights SHA256, conversie/export flags, schema, calibrări și profile de resurse. Se păstrează license-code și license-weights ca metadate separate, precum și starea accesului. Nu se folosește latest în release. O schimbare model sau preprocesare produce model_id nou.

Exemplu de structură pentru viitorul manifest; null marchează intrare R0 necompletată, deci nu este un lockfile deployabil:

```json
{
  "manifest_schema": "eva.deployment/1",
  "environment": "staging",
  "app_commit": "0e71d84abeb603db4daf81c5917bab58d36dd728",
  "backend_commit": "98abc15fbdc5b6ee8c746be637a8094db8e6be3b",
  "xcode_build": null, "ios_build": null, "ros_distro": null,
  "images": [{"service": "pose-estimator", "digest": null}],
  "models": [{"id": "foundationpose-candidate", "upstream_revision": null,
    "weights_sha256": null, "license_code": "record exact artifact",
    "license_weights": "record exact artifact", "access_status": "not_requested",
    "format": null, "memory_peak_bytes_measured": null}],
  "calibration_ids": [], "qualification_report": null
}
```

R0 automatizează rezolvarea versiunilor și calculează hash-uri după download verificat. Publicarea unui release este refuzată dacă vreun artifact activ are pin/hash/compatibility absent. Challenger-ele neactivate pot păstra unknown; acestea nu blochează cercetarea cu metodele accesibile.

## Servicii și persistență

| Serviciu propus | Dependențe și stocare | Interfață și health | Resurse/politică |
|---|---|---|---|
| sensor-gateway | identități/certificate, registry; fără media durabilă implicit | TLS443 extern; /healthz liveness, /readyz schema/auth/queue | CPU; cozi limitate pe robot; ACL și admission |
| world-model | PostgreSQL existent, event/outbox, object metadata | API intern; ready după DB+migrații | CPU/RAM rezervate; autoritate revision per map |
| asset-store | storage S3-compatible sau filesystem adapter versionat | URL-uri autorizate/checksum; ready read/write staging | volume separate; retenție și backup |
| job-queue | PostgreSQL jobs/outbox inițial, fără broker suplimentar obligatoriu | API intern, lease/heartbeat/retry | job claim atomic; backoff și dead-letter |
| semantic-inference | SAM3.1/detector models | request ID+frame ID; ready model warmed | GPU, coadă cu deadlines; instance state separat per robot |
| pose-estimator | FoundationPose/MegaPose/Any6D adapters | RGBD/K/mask/model→pose hypotheses | GPU; respinge input incomplet/stale |
| map-builder | nvblox/RTAB-Map, keyframes, graph | submap/revision API | GPU/CPU profil, fără block pe local controller |
| speech-person | Parakeet/pyannote sau adaptoare telefon | audio timestamped→segments/IDs | GPU/CPU; stream/session isolation |
| llm-service | model VLM/LLM + bounded world retrieval | structured tools, schema validation | GPU separabil; nu primește drept de actuare |
| robot-adapter | ROS, TF, robot profile, state estimator | actions+feedback; ready numai cu TF/time/profile valide | robot local; watchdog separat |
| model-registry/evaluator | manifest, artifacts, replay datasets | release/canary/rollback metadata | batch; nu consumă resurse rezervate live |

Porturile interne se alocă în compose-ul de implementare și nu se publică pe host; API-ul gateway este singura intrare propusă pentru telefoane. PostgreSQL/Triton/vLLM rămân private. Namespaces și rate limits sunt per robot/site. Triton poate servi modele stateless cu batching și versiuni explicite; stateful tracking cere sequence/session isolation. vLLM rămâne opțiune pentru modelele pe care le suportă la versiunea pinned; memoria KV/vision/cache se măsoară separat de weights. [Triton repository](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html), [batching](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html), [vLLM serve](https://docs.vllm.ai/en/stable/cli/serve/).

Nu adăugăm obligatoriu Neo4j/Kafka/Kubernetes: PostgreSQL, storage și containere sunt suficiente pentru primul pilot; se scalează când profilul măsurat justifică. Worker-ul video existent primește lease, heartbeat, retry, timestampuri și rezultate per instanță. Lipsa modelului este blocked_dependency, nu eșec definitiv al tuturor joburilor; crash permite reclaim după expirarea lease-ului.

## Dimensionare și operare

Profile propuse pentru laborator, nu promisiuni de throughput: S0 CPU pentru control/storage/replay și modele locale pe telefon; S1 NVIDIA24–48GB pentru experimente executate selectiv; S2 două sau mai multe GPU cu separarea percepției online de LLM/reconstrucție. SAM3D are cerință upstream >=32GB VRAM; profil24GB îl execută pe alt worker sau rămâne fără acel experiment. FoundationPose runtime nou cere matrice driver/CUDA specifică din raportul vision; nu modernizăm toate serviciile la aceeași imagine implicit.

Calcul de bandă exemplificativ: RGB1280×720×3×30=82,94MB/s/telefon; depth256×192×2×15=1,47MB/s/telefon, fără confidence/overhead. Pentru4 telefoane RGB brut ar fi331,78MB/s (~2,65Gb/s), deci keyframe selection/compresie/depth codec și măsurarea rețelei sunt obligatorii. Aceste rezoluții sunt exemple de dimensionare, nu specificații promise de captura iPhone.

Calcul weights: P miliarde parametri × bytes/param este numai limita ideală de stocare a greutăților; adăugăm KV, activări, encoder vizual, scratch și concurență. MoE memorie depinde de total weights, nu doar parametrii activi. Admission control măsoară peak VRAM pentru input maxim și rezervă inițial20% headroom; refuză/reprogramează joburi când bugetul nu permite. Fiecare robot are cotă; sarcinile batch cedează prioritate percepției.

Telefon: profil navigare cu VIO/depth prioritar, inspecție cu 6D prioritar, conversație cu audio prioritar. Primele ținte de scheduling sunt propuneri de test: VIO la rata suportată, depth15Hz dacă disponibil, detector5–10Hz, face2Hz, gesture5–10Hz, modele grele la cerere. Schedulerul reduce module secundare la termic serious/memory pressure și raportează degradarea; critical invalidează capabilitățile afectate. Frecvențele nu sunt garanții și pot fi ajustate numai cu măsurarea TTL/gap.

Storage: quota per robot/session, ring buffer și retenție. Exemplu buget de pornire pentru telefon: max50GB modele/cache și max100GB recordings, păstrând minimum20% disc liber; ajustare în R0 după utilizarea existentă. Nu se rezervă automat întregul1TB. Live metrics/logs nu includ implicit audio/biometrie brută. Backup metadate zilnic plus jurnal incremental, target pilot RPO≤5min și RTO≤60min; la crash cu disc intact ACK local se recuperează integral; la pierderea hostului/discului ACK local are RPO≤5min, iar ACK replicated cere zero pierderi la defectul unui singur domeniu independent; raw streams neconfirmate au politică de pierdere declarată. Ștergerea profilurilor personale se propagă către cache-uri/dispozitive și are retenție backup documentată.

## Pașii de instalare și revenire

1. **Build reproductibil:** checkout commiturile de bază, branch de implementare separat pentru app/backend; xcodebuild list→resolve dependencies→test→archive pe Mac; colcon build/test pentru mesaje/adaptoare pe OS selectat. Numele schemei și ros distro se iau din inventar, nu din presupuneri. CI stochează logs/test report/manifest.
2. **Staging izolat:** creare `compose.robot.yaml` cu profile core, vision, pose, speech, llm, research; volume și rețea distincte de site. Serviciile R0/R1 livrează Dockerfile și lockfile per mediu incompatibil. Download weights cu versiuni/hash și acces valid, fără activare automată în producție.
3. **Migrare:** backup DB+assets și test de restaurare în staging; adăugare tabele/events/revision și câmpuri nullable fără ștergerea vechilor date; backfill marchează legacy_unknown pentru orientare/reper neconfirmat. Dual-read/adaptor preview→v1 până toți clienții sunt compatibili. Nu atribuim arbitrar covarianță sau epoch datelor vechi.
4. **Probe independente:** upstream example pentru fiecare model; test de paritate original→CoreML/CoreAI/ONNX/TensorRT cu aceleași intrări; health nu este ready până modelul și schema sunt verificate. Se fixează digestul imaginii, modelul și raportul înainte de canary.
5. **Contract/replay:** fixtures T01–T04, import/export și sincronizare, fără actuare. Validăm că schimbarea byte layout/normalizării imaginii nu alterează coordonatele sau etichetele.
6. **Shadow/canary:** un telefon și apoi doi/patru; candidatul compară rezultate cu baseline fără comenzi robot. Promovare pe metricile de mai jos și review al eșecurilor, nu doar pe media scorurilor.
7. **Robot:** simulator apoi banc cu motor enable controlat de owner robot; profil viteză și toleranțe semnate. Se păstrează stop independent și watchdog. După calificare, demonstrație end-to-end pe setul de taskuri înghețat.
8. **Rollback:** dezactivare feature flag, oprire consum de rezultate candidate, anulare/rezolvare a sarcinilor în curs, revenire model/container/app la release manifest precedent compatibil. Schema DB folosește expand/contract; rollback nu șterge evenimentele și nu scade revision. Dacă incompatibil, read-only și restaurare în mediu separat, reconciliere și nou snapshot. Se verifică recuperarea cu fault injection înainte de release.

Livrabile runbook: `scripts/inventory`, `scripts/verify-manifest`, `scripts/smoke`, `scripts/replay`, `scripts/backup-restore-test`, `scripts/rollback`, cu platforma/shell declarate și exit codes; aceste scripturi se implementează la B01/B15. Comenzile docker compose config/pull/up și start-model se rulează doar pe compose validat, cu profilul și proiectul staging explicit. Nu se furnizează o comandă universală care să instaleze drivere/ștergă volume pe serverul necunoscut.

## Setul de date și criteriile normative

Owner QA îngheață dataset/config înainte de comparație: minimum6 camere (inclusiv două asemănătoare), 30 instanțe de obiecte cu10 perechi similare, 10 persoane cu sesiuni diferite, trasee repetate, iluminare normală/scăzută, reflexii/sticlă/ocluziune și zgomot real de robot. Separare pe cameră/obiect/persoană/sesiune între ajustare și test; nu se folosesc cadre vecine ca exemple independente. Pentru înrolare/test persoane identitatea se păstrează conform protocolului biometric, dar sesiunile sunt distincte; se adaugă persoane neînrolate ca negative. Ground truth se măsoară independent (repere rigide calibrate, distanțe și orientări), nu cu același model evaluat. Annotatorul nu vede rezultatul candidatului la etichetare.

p95/p99 se calculează pe probe end-to-end valide și se raportează separat toate eșecurile/drop/timeout. Pentru rate se raportează numărător/numitor și interval Wilson95%; pentru erori/latency, bootstrap pe sesiune/obiect, nu pe cadre corelate. Pragurile următoare definesc PASS pilot pe ratele punctuale dacă nu se precizează CI; ele nu certifică domenii netestate. Orice schimbare ulterioară se preregistrează și se folosește un nou holdout. Un sistem care trece doar media, dar eșuează într-o condiție critică declarată, nu este promovat pentru acea condiție.

| ID | Procedură și țintă pilot | Artefact / owner |
|---|---|---|
| T01 Spațiu/timp | 12 fixtures din CONTRACTE, eroare numerică≤1e-6 m/rad; 100 restarturi; 1000 mesaje invalid/late/duplicate: zero acceptări greșite | fixtures+CI / ROS+iOS |
| T02 Sincronizare offline | 1000 operații din2/4 clienți, delay/reorder/duplicate, offline60s, crash la fiecare etapă commit; zero pierderi de operații ACK, convergență la același hash după drain; p95≤10s după reconectare pentru backlog1000 evenimente mici pe LAN testat | logs/snapshot hashes / backend |
| T03 Transport/prospețime | 3 sesiuni×30min; local capture→consum p95≤100ms, p99≤200ms raportat chiar dacă respins; date>TTL nu sunt folosite; ≥95% ferestre de1s au observații locale valide; gap maxim≤500ms în profil nominal | traces/clock calibration / platform |
| T04 Ceas/calibrare | p95 eroare clock≤5ms pe referință comună; 30 poziții calibrare+10 ținte holdout și5 remontări; eroare spațială camera→robot p95≤20mm și2grade în volumul pilot declarat | calibration report / robot |
| T05 Localizare/aliniere | 40 încercări revenire și100 negative între camere similare; ≥95% relocalizări corecte≤10s, zero false merge în set; aliniere map p95≤50mm/3grade pe repere holdout; ATE/RPE fără rescalare ascunsă | trajectories+negative set / mapping |
| T06 Obiecte/6D | 30 instanțe×10 vederi independente; poziție p95≤30mm, orientare≤5grade pentru asimetrice; simetrii cu BOP metric echivalent; IDF1≥0.90 și zero false persistent merge în setul cu perechi similare; validitatea separată pentru necunoscut | poses/masks/ID report / ML |
| T07 Detector/segmentare | baseline și fiecare challenger pe același holdout; mAP/maskIoU/recall pe categorii; noninferioritate mAP în limita0.5 puncte procentuale și recall pentru obiectele taskului≥90%; conversie/export schimbă metricile cu cel mult0.5pp | ablation+parity / ML+iOS |
| T08 Flotă și ownership | 2 apoi4 roboți, origine diferită, reset unilateral, partition60s și lease expiry; 100 conflicte: zero comenzi cross-robot, zero execuții concurente exclusive și zero false merge; >4 doar după probă suplimentară de capacitate | event/task traces / distributed |
| T09 Audio/STT | minimum500 enunțuri RO și500 EN, sesiuni noi, quiet și SNR10dB+zgomot robot; WER≤15% quiet/≤25% noisy și intenție+slot corect≥95%; speech-end→text-final p95≤1s local sau≤2s server; suport locale verificat runtime | corpus/WER/latency / audio |
| T10 Identitate persoane | minimum1000 încercări impostor și200 genuine pe sesiuni separate pentru față și voce; limita superioară Wilson95% FAR≤1%, FRR punctual≤10%; diarization DER≤15% pe set cu vorbire suprapusă raportată separat; unknown/replay testat | scores/thresholds / people |
| T11 Gesturi/TTS | 4 gesturi×100 exemple+60min negative: recall≥95%,≤1 fals trigger/oră; indicare obiect corect≥90%. TTS RO/EN:100 enunțuri, inteligibilitate transcrisă de oameni≥95% cuvinte, first-audio p95≤500ms local/≤1.5s server, barge-in stop p95≤300ms | human eval/audio logs / interaction |
| T12 Stabilitate | 3×2ore în montura alimentată, sarcini mixte,30 întreruperi foreground/audio/rețea; zero crash/OOM, toate cozile sub plafon, ultima oră nu arată creștere monotonă neexplicată a memoriei; degradarea termică vizibilă și datele nevalide respinse | instruments/metrics / iOS+QA |
| T13 Sarcini robot | după gate motor: minimum20 repetări per combinație critică obiect/gripper și50 sarcini navigate-find-pick-place; succes≥90%, zero coliziuni neplanificate în test; orice astfel de coliziune redeschide gate; toleranțele reale impuse de robot pot fi mai stricte decât T06 | simulator+banc+video / robot |
| T14 LLM | 200 cereri cu ambiguitate/OCR adversarial/obiect lipsă; schema tools validă100%, zero acțiuni în afara permisiunii; plan corect≥90%, toate referințele object_id existente sau cerere clarificare; anulare/retry nu dublează efectul | eval cases/task traces / LLM |
| T15 Recovery/deploy | restore DB+assets verificat la hash, RPO≤5min/RTO≤60min în profil declarat; downgrade/upgrade canary și crash job reclamation; zero pierderi ACK local la crash cu disc intact; disaster cu pierderea hostului/discului: local ACK RPO≤5min, replicated ACK zero la un singur domeniu pierdut; manifest fără pins active lipsă | recovery report / DevOps |

T03=100ms local prevalează asupra propunerii150ms din raportul vision; semantica server pentru căutare are țintă p95≤1s și nu alimentează controlul dacă depășește TTL500ms. T12=3×2ore prevalează asupra recomandării60min. T04/T06 sunt exploratorii pentru pilot, nu aprobarea de mers/prindere. Owner robot stabilește buget final după viteză, gripper și gabarit înainte de T13; în lipsa lui T13 rămâne BLOCKED_HARDWARE, iar pașii software pot continua.

Promovarea unui model cere toate gate-urile relevante, lipsa regresiilor critice, paritate de conversie și rollback. Dintre modelele care trec, alegerea folosește succes task și analiza Pareto precizie/latency/memorie/energie. Evaluăm baseline, fiecare metodă singură și combinația; păstrăm două metode în runtime numai când combinația aduce câștig măsurabil ori acoperă eșecuri diferite. Variantele research mari nu sunt penalizate pe licență, dar trebuie să încapă în worker și să respecte rolul online/offline atribuit.

## Backlog executabil

Owner-ii sunt roluri care vor primi persoane la kickoff; nu atribuim fictiv responsabilitatea unui utilizator. Estimările de efort se fac după R0 și spikes; secvența și dependențele de mai jos sunt ferme, termene calendaristice nu sunt promise fără capacitatea echipei.

| ID | Rol și dependențe | Fișiere/subsistem vizat și livrabil | Definition of Done |
|---|---|---|---|
| B01 R0 inventar | DevOps+iOS+robot; start | manifests și compatibility matrix, baseline build | Toate intrările active pin/hash, acces și hardware măsurat; T15 setup |
| B02 Contracte | ROS+iOS; B01 | eva_msgs/schema+fixtures+adaptor RobotTelemetry | C01/C02, T01/T04; schema cross-language |
| B03 Lifecycle | iOS; B02 | RobotPerceptionEngine reset/generation/time/mergeNeural | C03/C04, T01 fără stale overwrites |
| B04 Persistență locală | iOS+mapping; B02 | InventoryModels/RoomInventorySession/InventoryLiveView | C05/C06/C08, map gate și state validity; T05/T06 |
| B05 Sync | backend+iOS; B02 | Site/server/inventory.mjs, SQL migration, InventorySyncService | C07, event cursor/assets atomic, T02/T15 |
| B06 Capture/audio owner | iOS; B03 | CaptureCoordinator/AudioCoordinator + capability manifest | No competing camera owners; tests interruptions T03/T12 |
| B07 Model adapters | ML+iOS; B01/B06 | detector/segmentation/CoreAI/CoreML parity+registry | toate variantele comparative documentate; T07/T12 |
| B08 6D/geometrie | ML+mapping; B04/B07 | ARKit refs, FoundationPose etc, uncertainty and depth masks | T06; inferat vs măsurat etichetat |
| B09 Memorie semantică | backend+ML; B04/B05/B08 | WorldModel, relation graph, ID merge/split și retrieval | T05/T06; istoric/proveniență și identități stabile |
| B10 Bridge ROS | ROS+platform; B02/B06 | RobotBridge TLS/backpressure + gateway + health/TTL | C09 și T01/T03; două subscribers fără blocare |
| B11 RobotProfile | robot; B01/B10 | URDF/XACRO/SRDF package validator, simulator | import exact metric și TF fără părinți dubli; T04 |
| B12 Flotă | distributed+mapping; B05/B09/B10 | map alignment, leases/fencing, dedup/rejoin | T02/T05/T08, fără namespace cross-talk |
| B13 Interacțiune | audio+people; B06/B09 | STT/TTS/voiceID/face/gesture candidates și fusion | C10, T09/T10/T11; unknown și limbă fallback |
| B14 LLM/executor | LLM+robot; B09/B11/B13 | typed tools+task state machine+scene retrieval | T14 și anulare/lease tests; fără tool torque |
| B15 Operare | DevOps+QA; B05/B07/B10 | staging compose, scripts, backup/rollback, model delivery | T15; health/readiness, job reclaim și observabilitate |
| B16 Calificare | QA+robot+auditor; B08–B15 | freeze holdout, test suite, end-to-end demo | C11; T01–T15, explicații toate fail/blocked |
| B17 Cercetare extinsă | ML; B07/B15 | DA3/VGGT/CoMo3R/Any6D/SAM3D/GraspGenX/cuRoboV2 spikes | aceleași metrici și resurse; promovare numai cu dovadă |

Ordine recomandată: B01→B02; apoi B03/B04/B05; B06–B11; B12/B13/B15; B14/B16. B17 poate rula pe server izolat în paralel după B07/B15. Controlul fizic rămâne după gate B11/T13, indiferent de stadiul interfeței conversaționale. Fiecare task produce cod, migrare dacă necesar, test report, ADR și runbook actualizat; un screenshot sau status „build green” singur nu închide taskul.

## Închiderea auditului documentar

10/10 înseamnă că sursele, alternativele, contractele, pașii, probele și responsabilitățile sunt suficient de clare pentru implementare. Starea fizică rămâne not_run până există rezultate. Fișierele auditate se identifică prin SHA256; modificarea lor cere revizie și re-audit. Auditul V1, constatările și răspunsul V2 se păstrează în GitHub, fără ștergere retroactivă.
