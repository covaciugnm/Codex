# 2. Alegerea algoritmilor și argumentele cercetării

## 2.1 Modelul geometric înaintea inteligenței artificiale

Notăm T_A_B transformarea care exprimă coordonate din B în A. Pentru obiectul O observat de camera C într-o cameră fizică W, T_W_O = T_W_C · T_C_O. Pe robot trebuie cunoscut și lanțul cinematic dintre camera montată și reperul robotului, evaluat la momentul expunerii. Multiplicarea unor estimări corecte la momente diferite poate produce o poziție greșită.

Înregistrarea modelului OBJ începe cu unitatea și scara. Un cub modelat cu latura numerică 100 poate însemna 100 mm sau 100 m. O dimensiune cunoscută poate fixa scara, însă o altă dimensiune trebuie păstrată pentru verificare independentă. Nu ajustăm ulterior scara liber pentru a ascunde erorile în comparația cu referința. OBB-ul este calculat și versionat în reperul modelului; un AABB recalculat în cameră poate crește doar pentru că obiectul s-a rotit.

PnP estimează transformarea obiect–cameră din corespondențe 3D–2D și intrinseci. Implementarea OpenCV folosește convenția camerei x spre dreapta, y în jos, z înainte; conversia spre ARKit/ROS trebuie explicită. Punctele aproape coliniare, corespondențele greșite și unele configurații plane pot produce soluții instabile sau ambigue. [OpenCV: solvePnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).

Decizia proprie: demonstratorul începe cu AprilTag atașat rigid și transformare tag–obiect măsurată. Reperul nu este obiectul; poziția lui trebuie compusă cu transformarea calibrată. Se folosesc intrinseci pentru fluxul efectiv, nu valori copiate dintr-un alt crop. AprilTag oferă detecție și estimarea poziției reperelor în implementarea publică. [AprilRobotics](https://github.com/AprilRobotics/apriltag). Dacă reperul este prea mic, oblic sau obturat, algoritmul declară observație indisponibilă.

## 2.2 Alternative pentru obiecte cunoscute

| Candidat | Date necesare | Rol propus | Principalul risc | Experiment de selecție |
|---|---|---|---|---|
| Reper vizual + PnP | Reper dimensionat, intrinseci, extrinsec tag–obiect | Bază măsurabilă pentru integrare | Obturare și calibrare fizică | Eroare vs unghi/distanță și comparație cu referința |
| Puncte vizuale + PnP/RANSAC + rafinare RGB-D | Model cu puncte/aspect și corespondențe | Prima variantă fără reper | Textură slabă, repetitivă, iluminare | Aceleași secvențe cu/fără textură și lumină variabilă |
| ICP point-to-plane local | Adâncime, model, inițializare apropiată | Rafinare și urmărire locală | Minime locale, simetrie, suprafețe plane | Perturbarea controlată a inițializării și obturărilor |
| FoundationPose | Model CAD sau imagini de referință, RGB-D, inițializare potrivită | Experiment de cercetare pe Thor | Licență, latență, portare, memorie | Reproducere cu greutățile disponibile și hardware-ul nostru |
| BundleSDF | Obiect rigid necunoscut, RGB-D și mască inițială | Studiu pentru catalogare/reconstrucție | Derivă, cost și mișcare insuficientă | Secvență nouă, geometrie și traiectorie de referință |

FoundationPose propune un cadru pentru estimarea și urmărirea 6D a obiectelor noi, cu acces la modele sau imagini de referință. Articolul justifică evaluarea candidatului, nu garantează compatibilitatea noastră cu Thor sau performanța pe obiecte casnice. [Wen et al., FoundationPose](https://arxiv.org/html/2312.08344v2). Autorii precizează în depozit că greutățile publice diferă de cele ale lucrării. [README oficial](https://raw.githubusercontent.com/NVlabs/FoundationPose/main/readme.md).

Licența originală NVlabs limitează utilizarea la cercetare/evaluare necomercială. Prin urmare, acest cod nu este o dependență implicită a aplicației comerciale. Orice distribuție alternativă ori SDK se verifică separat, inclusiv greutățile și dependențele. [Licența FoundationPose, §3.3](https://raw.githubusercontent.com/NVlabs/FoundationPose/main/LICENSE).

BundleSDF tratează urmărirea și reconstrucția online a unui obiect rigid necunoscut din RGB-D, pornind de la o mască. În această etapă a fost consultat rezumatul primar; nu preluăm cifre de performanță și nu îl alegem drept componentă obligatorie. [Wen et al., BundleSDF](https://arxiv.org/abs/2303.14158).

## 2.3 Simetrii și identitate

Pentru un cilindru fără textură, rotația în jurul axei poate fi neobservabilă. Ieșirea corectă este o clasă de orientări echivalente sau un statut de ambiguitate. Nu forțăm o orientare numerică stabilă doar pentru a umple șase câmpuri. Evaluarea rotației minimizează distanța pe grupul de simetrie declarat; pentru obiecte deformabile modelul rigid devine invalid.

Identitatea instanței este diferită de clasa semantică. Două căni identice pot avea aceeași clasă și geometrii foarte apropiate, dar identificatori distincți. La interschimbare sub obturare completă, sistemul poate pierde identitatea chiar dacă detectează corect două căni. Înregistrăm asocierea incertă, folosim istoricul și cerem confirmare în aplicațiile unde identitatea contează. Nu prezentăm reidentificarea drept proprietate garantată a unui detector.

## 2.4 Hartă și reconstrucție continuă

TSDF este potrivit pentru integrarea suprafețelor din adâncime și extragerea unui mesh. ESDF reprezintă distanța față de obstacole și poate alimenta planificarea. Voxblox descrie construirea incrementală ESDF din TSDF; demonstrația sa nu este un benchmark pentru telefonul ori humanoidul nostru. [Oleynikova et al., Voxblox](https://arxiv.org/abs/1611.03631). Principiul fuziunii depth-to-model și al urmăririi locale are o bază în KinectFusion. [Microsoft Research](https://www.microsoft.com/en-us/research/publication/kinectfusion-real-time-dense-surface-mapping-tracking/).

Decizia proprie: trei reprezentări au cicluri de viață diferite. Harta statică persistă și este revizuită după aliniere; obiectele mobile au stări și covarianțe; stratul local de obstacole păstrează observații recente și expiră. Un scaun mutat nu trebuie integrat simultan în două locuri din harta statică. Zona pe care camera nu o vede rămâne necunoscută, chiar dacă ultimul mesh era gol acolo.

„Scanare continuă” înseamnă procesare incrementală cu cozi limitate și selecție de cadre. Nu înseamnă păstrarea permanentă a tuturor imaginilor la frecvența maximă. Cadrele importante se aleg după mișcare, acoperire, informație geometrică și calitate; cadrele aproape identice cresc costul fără să ofere informație independentă. La suprasarcină se reduc rezoluția, frecvența detecției și numărul obiectelor prioritare; se păstrează prioritar timestamp-urile și semnalele de sănătate.

## 2.5 De ce repetarea scanării nu garantează dimensiunea corectă

Un model simplificat este z_i = d + b + ε_i, unde d este dimensiunea reală, b eroarea sistematică, iar ε_i variația aleatoare. Media reduce variația independentă; b rămâne. Pentru zgomot cu varianță σ² și corelație egală ρ, varianța mediei este σ²[1+(N−1)ρ]/N. La N=10 și ρ=0,8, abaterea standard devine aproximativ 0,906σ, nu 0,316σ. Este o ilustrare matematică, nu o estimare a corelației iPhone.

Reluările ajută dacă adaugă perspective, închid bucle și îmbunătățesc acoperirea. Pot agrava modelul dacă alinierea este greșită sau obiectele s-au deplasat. Procedura păstrează scanările brute aprobate, estimarea rigidă, reziduurile și punctele de control. Înainte de fuziune verificăm scara, orientarea, suprapunerea și consistența reperelor. Datele respinse rămân identificabile în raport, fără a fi ascunse din numitorul succesului.

Un studiu primar ISPRS pe dispozitive Apple mai vechi evaluează separat precizia locală, corectitudinea globală și acoperirea suprafeței. Această separare este relevantă pentru proiect: o suprafață netedă local poate aparține unei camere deformate global. Studiul nu califică iPhone 17/18. [Díaz-Vilariño et al., 2022](https://isprs-archives.copernicus.org/articles/XLIII-B4-2022/303/2022/isprs-archives-XLIII-B4-2022-303-2022.pdf).

Lucrarea Pix4D din 2024 descrie folosirea reperelor AutoTags pentru compensarea derivei și combinarea scanărilor. Am consultat pagina primară și rezumatul; descărcarea integrală prin instrumentul web a eșuat. O folosim pentru a motiva experimentul cu repere, fără a atribui cifre de precizie. Autorii sunt afiliați furnizorului, fapt relevant în interpretare. [Strecha et al., 2024](https://isprs-archives.copernicus.org/articles/XLVIII-2-2024/415/2024/).

## 2.6 Cercetarea doctorală propusă

Contribuțiile încă nedemonstrate pot fi formulate ca ipoteze falsificabile: H1 selecția cadrelor după informație reduce traficul fără degradarea semnificativă a erorii; H2 reperele și punctele de control reduc deriva inter-sesiune; H3 separarea obiectelor dinamice reduce fantomele din harta statică; H4 ordonarea adaptivă a urmăririi menține vârsta observațiilor prioritare sub bugetul definit; H5 un profil de incertitudine calibrat detectează degradarea înaintea unei măsurări eronate acceptate.

Pentru fiecare ipoteză folosim aceeași colecție de scene, split de dezvoltare separat de evaluare, ablație în care eliminăm numai mecanismul testat, timp total și consum măsurate, intervale de încredere și raportarea eșecurilor. Nu optimizăm pe setul de calificare. O lipsă de diferență sau un rezultat negativ este acceptabil științific și poate simplifica produsul. Publicarea unei contribuții originale cere aceste experimente și evaluare de specialitate; nivelul de detaliu al documentului nu le înlocuiește.
