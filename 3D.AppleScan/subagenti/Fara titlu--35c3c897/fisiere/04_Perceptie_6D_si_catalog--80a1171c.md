# 4. Percepția 6D, inventarul geometric și urmărirea obiectelor

**Statut:** metodologie propusă; algoritmii, seturile experimentale și pragurile robotice necesită implementare și calificare. Autor: agentul specialist Apple și percepție. Dimensiunile obiectului, eroarea poziției și eroarea orientării reprezintă mărimi diferite. Acceptarea uneia nu o demonstrează pe cealaltă.

## 4.1. Reprezentarea problemei

Poziția 6D a unui obiect rigid are trei componente de translație și trei grade de libertate de rotație. Folosim transformarea omogenă `T_AB`, care convertește coordonate din reperul B în reperul A. Pentru camera C, obiectul O și lumea W: `T_WO = T_WC T_CO`. Aceeași convenție trebuie să apară în cod, mesaje, teste și documente. Ordinea factorilor nu este interschimbabilă.

Transformarea rigidă aparține `SE(3)` și se scrie ca matrice cu blocul de rotație `R ∈ SO(3)`, translația `t ∈ R³` și ultimul rând `[0,0,0,1]`. Condițiile `RᵀR = I` și `det(R)=1` sunt teste numerice obligatorii. Pentru interpolare și stocare utilizăm cuaternioni normalizați; unghiurile Euler rămân o reprezentare de interfață cu ordinea axelor declarată. Semnele opuse ale aceluiași cuaternion nu reprezintă orientări fizice diferite.

Scara obiectului este parametrul separat `s`, fixat înaintea urmăririi metrice. Dacă permitem ajustarea liberă a scării pentru a potrivi un model, problema devine una de similitudine, nu estimare rigidă pură. O potrivire frumoasă realizată prin schimbarea scării poate ascunde o eroare dimensională și nu trebuie utilizată pentru a declara un export corect.

## 4.2. Nivelurile de înțelegere care trebuie separate

| Reprezentare | Răspunde la întrebarea | Nu demonstrează singură |
|---|---|---|
| Etichetă de clasă | Este probabil un scaun? | Care exemplar este |
| Dreptunghi 2D | Unde se află în imagine? | Adâncimea sau forma exactă |
| Mască de instanță | Ce pixeli aparțin obiectului vizibil? | Suprafața ascunsă |
| Cutie 3D | Ce volum aproximativ ocupă? | Orientarea semantică exactă |
| Model înregistrat 6D | Cum este orientat modelul față de cameră? | Identitatea unică dintre exemplare identice |
| Identitate persistentă | Este același exemplar ca ieri? | Că nu a fost înlocuit în afara câmpului vizual |

Vision oferă o cerere pentru măști de instanță de prim-plan. Aceasta reprezintă o componentă posibilă, nu o clasificare universală ori o soluție completă de urmărire 3D. [A14 — măști de prim-plan](https://developer.apple.com/documentation/vision/vngenerateforegroundinstancemaskrequest)

Designul interfeței trebuie să afișeze nivelul realmente disponibil. Un contur exact în imagine nu justifică eticheta „poziție 6D precisă”. Pentru obiectele fără model se poate furniza un centru și o cutie aproximativă; orientarea rămâne parțial observabilă sau necunoscută. Catalogul acceptă explicit valori lipsă, fără completarea cu zero care ar sugera măsurare validă.

## 4.3. Pregătirea unui model OBJ existent

Importul se execută într-o zonă de lucru separată. Se verifică parsarea, limitele de dimensiune, coordonatele finite, fețele degenerative, normalele, dependențele de materiale și existența texturilor. Modelul original este păstrat nemodificat, cu hash. Calea către texturi trebuie rezolvată în pachetul autorizat; un fișier de model nu poate cere citirea arbitrară a sistemului de fișiere.

Unitatea nu se deduce sigur numai din valorile coordonatelor. Utilizatorul sau manifestul de proveniență declară metri, milimetri ori altă unitate și furnizează cel puțin o dimensiune independentă. După conversia internă la metri se verifică trei dimensiuni și sensul axelor. Se definește un reper semantic stabil: de exemplu centrul bazei, axa verticală și direcția din față. Centrul cutiei geometrice nu trebuie confundat automat cu centrul de masă.

Se construiesc mai multe niveluri de detaliu, puncte eșantionate pe suprafață, descrieri vizuale și o listă a simetriilor cunoscute. Pentru fiecare versiune se păstrează transformarea dintre modelul original și cel normalizat. Un punct de prindere definit pe model trebuie să poată fi transformat înapoi verificabil. „Watertight” și rezoluția texturii se raportează separat de adecvarea modelului pentru identificare.

## 4.4. Trei căi algoritmice comparate

**Calea A — marker rigid.** Un AprilTag cu dimensiune măsurată și transformare calibrată față de obiect oferă o referință explicită. Implementarea oficială oferă suport pentru estimarea poziției markerului din parametrii camerei și mărimea etichetei. [A15 — AprilTag](https://github.com/AprilRobotics/apriltag) Propunem această cale drept bază experimentală pentru integrarea transformărilor. Ea nu este adevăr de referință independent dacă același marker și aceleași observații sunt folosite și de algoritmul evaluat.

**Calea B — corespondențe imagine–model.** Se găsesc puncte 2D și corespondentele 3D ale obiectului, apoi se estimează `T_CO`. OpenCV documentează PnP, variante cu soluții multiple și RANSAC pentru corespondențe aberante. Rezultatul transformă puncte din reperul obiectului în cel al camerei. [A16 — PnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html) În proiect se verifică reproiecția, numărul și distribuția punctelor, adâncimile pozitive și consistența cu observațiile noi.

**Calea C — RGB-D și înregistrare geometrică.** Pornind de la o ipoteză inițială, aliniem punctele modelului cu punctele observate în mască. ICP este o metodă de rafinare locală; Open3D documentează inițializarea și variantele point-to-point și point-to-plane. [A17 — ICP](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) Respingerile trebuie să includă suprapunere insuficientă și geometrii degenerative. Un reziduu mic pe o singură față plană nu fixează toate cele șase grade de libertate.

FoundationPose constituie un candidat de cercetare pentru estimare și urmărire pe baza modelelor ori a imaginilor de referință. Depozitul oficial are dependențe GPU/CUDA și pași proprii de configurare; nu reprezintă o bibliotecă iOS gata integrată. [A18 — FoundationPose](https://github.com/NVlabs/FoundationPose) Compararea pe calculatorul robotului este o ipoteză de arhitectură, cu audit separat pentru licența codului, greutăților și datelor. Viteza publicată într-un alt sistem nu este copiată ca performanță EVA.

## 4.5. Fuziune și estimarea incertitudinii

Propunem optimizarea unei sume de reziduuri de reproiecție, distanță geometrică și continuitate temporală, fiecare ponderat printr-un model de eroare. Ponderile se estimează pe lotul de calibrare și se îngheață înaintea evaluării finale. O funcție robustă limitează contribuția corespondențelor aberante, dar nu repară un model de obiect greșit.

Incertitudinea locală este reprezentată în convenția propusă prin perturbație dreaptă: `T_AO = T_hat_AO Exp(delta_xi^)`, cu `delta_xi=[rho_x,rho_y,rho_z,phi_x,phi_y,phi_z]`, exprimată în reperul local O al obiectului. `rho` se exprimă în metri și `phi` în radiani. Covarianța `Sigma_right=E[delta_xi delta_xiᵀ]` presupune eroare centrată; biasul estimat se păstrează separat. Blocurile translație–translație au unitatea m², rotație–rotație rad² și cele două blocuri mixte m·rad. Ordinea este fixată și în manifest; o matrice fără convenție este respinsă.

Conversia de ordinul întâi la perturbația stângă exprimată în A, `T_AO=Exp(delta_eta^) T_hat_AO`, folosește `delta_eta=Ad(T_hat_AO) delta_xi`, deci `Sigma_left=Ad(T_hat_AO) Sigma_right Ad(T_hat_AO)ᵀ`. Pentru ordinea `[rho,phi]`, `Ad(T)=[[R,[t]_x R],[0,R]]`. Schimbarea numai a reperului extern A prin multiplicare la stânga nu schimbă covarianța dreaptă exprimată în O; covarianța stângă se transformă prin adjointul schimbării de reper. Această distincție previne aplicarea aceleiași rotații mecanic oricărui tip de covarianță.

La popularea unei structuri ROS de pose, adaptorul aplică Jacobianul dintre coordonatele tangente declarate și parametrizarea de poziție/rotații a mesajului. Profilul inițial ROS adoptă eroare de poziție aditivă în A și rotații infinitezimale în jurul axelor fixe ale lui A: `delta_p=R rho`, `delta_theta=R phi`; rezultă `J_ROS=diag(R,R)` și `Sigma_ROS=J_ROS Sigma_right J_ROSᵀ`. Această matrice nu este `Ad(T)`: translația unei perturbații stângi SE(3) nu coincide cu diferența aditivă a pozițiilor, deoarece aceasta din urmă include și termenul rotației originii. Profilul nu definește covarianța diferențelor finite de unghiuri Euler; un consumator care folosește acea parametrizare cere alt Jacobian și versiune declarată.

Nu se copiază direct matricea din SE(3) doar fiindcă are 36 de valori. Învelișul EVA păstrează pentru reprezentarea originală `covariance_convention=right_local_object`, reperul O și starea `uncertainty_status`; reprezentarea convertită are `covariance_convention=ros_additive_position_fixed_axis_small_rotation`. Dacă modelul de eroare lipsește, matricea este opțională și statusul este `unavailable`; nu se furnizează matrice nulă interpretabilă drept certitudine.

Pentru erori corelate între poziția camerei și cea a obiectului, însumarea simplă a covarianțelor poate fi nejustificată. Propagarea conține termenii încrucișați ori o aproximare conservatoare justificată. Evaluarea empirică a acoperirii intervalelor este obligatorie; eticheta de încredere a detectorului nu este covarianță geometrică.

O singură covarianță gaussiană nu descrie satisfăcător două orientări plauzibile ale unui obiect simetric. În acest caz catalogul păstrează ipoteze multiple ori marchează axa neobservabilă. Pentru o cană, mânerul poate elimina o ambiguitate numai dacă este observat; pentru un cilindru fără textură, rotația în jurul axei poate rămâne nedeterminată. Alegerea arbitrară a unei orientări arată stabilitate fictivă.

## 4.6. Catalogul persistent și asocierea în timp

Modelul propus separă `asset_id` pentru tipul/modelul geometric, `instance_id` pentru exemplarul fizic și `track_id` pentru urmărirea temporară. Un nou `track_id` după ocluzie nu creează automat un nou obiect fizic. Invers, două scaune identice nu primesc aceeași identitate doar pentru că au același mesh.

O observație conține: identificator de sesiune și epocă, cadru, timp de captură, versiunea hărții, versiunea calibrării, modelul utilizat, mască/cutie, transformare, incertitudine, metodă, scoruri și motivul respingerii. Înregistrarea unui obiect conține starea curentă, ultima observație validă, istoricul și proveniența deciziilor de asociere.

Asocierea folosește simultan distanță spațială compatibilă cu timpul scurs, aspect, geometrie și restricții de exclusivitate. O reidentificare cu dovezi insuficiente intră în starea ambiguă, fără rescrierea istoricului. Pot fi cerute marcaje suplimentare pentru bunuri identice a căror identitate are importanță operațională. O schimbare făcută manual este înregistrată ca decizie a operatorului.

Starea canonică transmisă este `observed`, `predicted`, `occluded`, `lost` sau `retired`. Ambiguitatea este ortogonală vizibilității: `ambiguity_status` are valorile `none`, `pose`, `identity`, `both`, iar ipotezele alternative sunt păstrate dacă există. Eticheta UI `ambiguous` este afișată pentru ultimele trei valori fără să înlocuiască starea de vizibilitate. Eticheta locală `archived` se mapează la `retired` numai când reprezintă decizia explicită de retragere din inventarul activ; simpla copiere a proiectului în arhivă nu schimbă starea obiectelor. Autorul contractului ROS implementează aceleași câmpuri înaintea interoperabilității; transportul care nu le acceptă este incompatibil, nu pierde tăcut informația.

„Predicted” înseamnă extrapolare, cu vârsta și incertitudinea afișate. Nu afirmăm observarea unui obiect ascuns și nu deducem dispariția lui dintr-o singură detecție ratată. Expirarea unui track are alt efect decât ștergerea unui obiect din inventar.

## 4.7. Predicție, prioritizare și percepție activă

Predicția pe termen scurt poate utiliza un model de viteză aproximativ constantă, dar trebuie suspendată când intervin accelerații neobservate sau contact. Pentru obiectele manipulate de robot, kinematica gripperului poate furniza o constrângere, cu incertitudinea prinderii. Această constrângere este o sursă distinctă și nu trebuie contabilizată ca detecție vizuală suplimentară.

Percepția activă propusă alege o perspectivă care reduce ambiguitatea ori acoperă o suprafață necunoscută. Funcția de selecție poate combina creșterea estimată a informației, timpul de deplasare, consumul și constrângerile mișcării. Algoritmul trebuie comparat cu o succesiune fixă de perspective. Beneficiul cuantificabil este reducerea timpului până la o poziție acceptată, nu doar numărul mai mare de imagini.

Obiectele de interes apropiate de acțiunea robotului primesc prioritate. Obiectele statice îndepărtate sunt reverificate periodic. O zonă de interes reprezintă o regulă de programare a calculului, nu o cameră suplimentară. Descoperirea globală periodică rămâne necesară pentru a evita pierderea obiectelor nou intrate în scenă.

## 4.8. Experimente și criterii de interpretare

Pentru translație măsurăm `e_t = ||t_est − t_ref||`. Pentru rotație folosim unghiul geodezic `acos(clamp((trace(R_refᵀ R_est)−1)/2,−1,1))`. La obiectele simetrice raportăm și eroarea minimă peste transformările simetrice admise, păstrând vizibil faptul că orientarea completă nu este identificabilă. Eroarea de reproiecție în pixeli și eroarea metrică se raportează împreună, fără a le considera echivalente.

| Experiment propus | Lot și comparație | Rezultate obligatorii |
|---|---|---|
| PER-01, scală și repere | Fixture digital cunoscut plus referințe fizice independente | Unități, transformări inversabile, eroare de scară |
| PER-02, estimare statică | Pilot: 10 obiecte × 10 poziții; familii separate la calibrare și test | Eroare P50/P95, eșecuri din toate încercările, intervale de încredere |
| PER-03, simetrii și ocluzii | Obiecte asimetrice, repetate și simetrice; ocluzii etichetate | Rata ambiguităților detectate, orientări fals declarate sigure |
| PER-04, urmărire | Secvențe cu intrări, ieșiri și schimbări de poziție | Schimbări de identitate, fragmentări, timp de recapturare |
| PER-05, scanări repetate | O scanare versus fuziune multiobservație | Eroare pe repere nefolosite la optimizare și cost suplimentar |
| PER-06, incertitudine | Lot separat de cel folosit la reglaje | Acoperirea empirică a intervalelor și erori condiționate de scor |

Testul numeric suplimentar PER-07 verifică convenția de covarianță: se pornește de la o matrice pozitiv definită în reperul obiectului și o transformare cu rotație și translație nenule; se compară conversia prin adjoint cu diferențe finite și eșantionare de perturbații mici. Conversia tur–retur trebuie să recupereze matricea în toleranța numerică predeclarată, iar simetria și semidefinirea pozitivă trebuie păstrate. Un caz separat combină două observații identice, perfect corelate: estimatorul nu trebuie să înjumătățească artificial incertitudinea ca și cum ar fi independente. Testul este definit, nu executat în acest dosar.

Lotul pilot de 100 poziții nu constituie singur acceptare statistică. Dimensiunea lotului final se stabilește după variabilitatea observată, înaintea evaluării finale. Cadrele succesive ale aceluiași obiect sunt corelate; resamplingul trebuie realizat la nivel de obiect, traseu sau sesiune adecvat ipotezei. Raportarea milioanelor de pixeli ca milioane de probe independente ar produce certitudine artificială.

Pragurile de poziție 6D pentru manipulare vor fi stabilite din toleranța sarcinii și modelul de prindere în poarta robotică. Nu transferăm automat pragul de cinci milimetri din metrologia obiectelor asupra poziționării robotului. Auditorul acceptă documentul când metoda, referințele, numitorii și limitele sunt explicite; acceptarea aplicației rămâne condiționată de experimentele efective.
