# Addendum: candidați pentru comparația tehnică în cercetare

Data: 6 octombrie 2026. Completează raportul înghețat `vision-robotics.md`, fără a-l rescrie. La solicitarea utilizatorului, toate metodele relevante sunt eligibile în mod egal pentru evaluarea tehnică, inclusiv cele cu termeni necomerciali sau personalizați. Licența nu este criteriu de punctaj al performanței. Termenii, accesul la weights și dependențele se înregistrează drept metadate și condiții ale instalării efective. Nu s-au instalat ori testat aceste metode pe hardware-ul EVA.

„Cercetare” descrie maturitatea și dovezile disponibile; nu înseamnă excludere. „Activabil” înseamnă că artifactul este accesibil, interfața este integrată și testele sunt trecute. Un candidat poate câștiga tehnic și poate necesita încă muncă de integrare. Nici baseline-ul matur nu primește automat prioritate în rezultatul comparației.

## Candidați și condiții în care pot câștiga

| Candidat | Experiment și avantaj potențial | Condiția de câștig / activare |
|---|---|---|
| **MASt3R-SLAM** | SLAM dens cu priors3D, ca alternativă server la ARKit+reconstrucție geometrică; scene cu textură redusă și secvențe RGB arhivate | ATE/RPE metric mai mic, recuperare tracking mai bună și completitudine crescută în bugetul GPU. Pentru comparația metrică nu permitem rescalare Sim(3) care ascunde eroarea de scară. Integrare CUDA și proveniența corecțiilor obligatorii. [1] |
| **CoMo3R-SLAM** | Aliniere colaborativă a fluxurilor monoculare cu origini și scări independente; explicit challenger pentru doi/patru roboți | Depășește harta centralizată baseline la suprapunere redusă, false loop closures și trafic; se testează separat interior repetitiv, partition/rejoin și scene dinamice. Lucrare încă în review, exemplul upstream exterior nu validează locuința. [2] |
| **DA3 Large/Giant/Nested, variante1.1** | Comparăm întreaga scară de modele, inclusiv Nested care combină geometrie any-view cu estimare metrică | Câștig pe depth/pose/reconstrucție și robusteză, raportat la VRAM și latență. Variantele1.1 sunt preferate comparației cu vechile checkpoints depreciate. Rezultatele rămân estimări neurale distincte de depth măsurat. Termenii NC se documentează, nu elimină candidatul. [3] |
| **VGGT-Omega** | Reconstrucție multiview, recuperarea geometriei și relocalizare; comparație cu DA3 și RGB-D | Folosim checkpointul Reproduction din septembrie2026 pentru benchmark, iar varianta512 pentru experimentul practic conform indicațiilor autorilor. Câștig dacă geometria și pose-ul îmbunătățesc taskurile EVA, inclusiv datele greu observabile, la cost acceptat. Accesul gated se înregistrează. [4] |
| **FoundationPose original și runtime nou** | Aceeași familie evaluată în două implementări: originalul pentru paritate/cercetare/model-free; runtime CUDA/TensorRT pentru throughput și integrare multi-obiect | Comparăm aceleași intrări, weights și precizie când este posibil. Se raportează diferențele de renderer, preprocessing, registrare și tracking. Originalul câștigă dacă acuratețea ori flexibilitatea sunt mai bune; runtime-ul dacă reduce latența fără regresie relevantă. Licențele distincte sunt metadate. [5] |
| **Any6D și OrienPose** | Any6D: ancoră RGB-D unică pentru obiect necunoscut; OrienPose2026: referință unică și sinteză de vederi orientată | Set separat de obiecte fără CAD, ocluzii și schimbări mari de vedere; scor pe simetrii, scară, pose și succesul manipulării. OrienPose necesită calificarea artefactelor și codului înainte de activare. Nu presupunem că orice generare produce geometrie metrică suficientă. [6–7] |
| **Event6D** | Tracking din evenimente pentru mișcare rapidă/blur, dacă adăugăm cameră de evenimente | Experiment numai după existența senzorului și calibrarea spațiu/timp cu telefonul. Câștig prin reducerea tracking loss și erorii în mișcare rapidă; fluxul RGB iPhone nu substituie evenimentele. [8] |
| **SAM3.1, RF-DETR inclusiv Plus, YOLO26 toate dimensiunile** | Comparație între măști/open vocabulary/tracking și detecție rapidă; modelele mari pot servi serverul | Măsurăm clase comune și obiecte rare, mask quality, IDF1/HOTA și false merge. Nu extrapolăm fps TensorRT în fps iPhone. AGPL/PML/SAM License nu reduc scorul tehnic. [9] |
| **SAM3D, GraspGenX, cuRoboV2** | Formă necunoscută, grasp condiționat pe mâna reală și planificare pentru multe articulații | SAM3D câștigă la catalog/estimarea formei; geometria nevăzută cere confirmare pentru contact. GraspGenX câștigă pe succes fizic și adaptare gripper; cuRoboV2 pe fezabilitate, coliziuni și timp de planificare. Nu confundăm aceste rezultate cu validarea controlerului de echilibru. [10] |

## Protocol de comparație

ML/robotică păstrează candidații de mai sus într-un registru comun, fără filtrare pe utilizare comercială. Se fixează datele train/validation/test, resursele și criteriile înaintea probei finale. Evaluăm două regimuri: buget egal de resurse și capacitate maximă disponibilă; raportăm frontiera acuratețe–latență–energie–cost, nu un clasament care ascunde condițiile.

Fiecare metodă rulează pe replay și apoi în shadow. Comparăm baseline, candidat și combinație; serverul poate valida incertitudinile telefonului. Metodele care folosesc aceleași observații nu sunt considerate confirmări independente. Un model suplimentar intră în profilul activ când aduce un câștig măsurat ori acoperă un caz critic de eșec. Modelele scumpe pot câștiga profilul „inspecție precisă” fără să fie potrivite pentru flux continuu.

Auditorul verifică fidelitatea benchmarkului, trasabilitatea și condițiile de activare; nu elimină metode pentru simplul fapt că sunt necomerciale. Nota documentației rămâne separată de performanța hardware care urmează să fie măsurată.

## Surse primare deja cercetate

[1] https://github.com/rmurai0610/MASt3R-SLAM

[2] https://github.com/como3r-slam/como3r-slam

[3] https://github.com/ByteDance-Seed/Depth-Anything-3

[4] https://github.com/facebookresearch/vggt-omega

[5] https://github.com/NVlabs/FoundationPose și https://github.com/nvidia-isaac/foundation-pose-inference-library

[6] https://github.com/taeyeopl/Any6D

[7] https://openaccess.thecvf.com/content/CVPR2026/html/Liu_OrienPose_Orientation-Guided_Novel_View_Synthesis_for_Single-Image_Unseen_Object_Pose_CVPR_2026_paper.html

[8] https://openaccess.thecvf.com/content/CVPR2026/html/Kang_Event6D_Event-based_Novel_Object_6D_Pose_Tracking_CVPR_2026_paper.html

[9] https://github.com/facebookresearch/sam3 ; https://github.com/roboflow/rf-detr ; https://github.com/ultralytics/yolo26

[10] https://github.com/facebookresearch/sam-3d-objects ; https://github.com/NVlabs/GraspGenX ; https://github.com/NVlabs/curobo
