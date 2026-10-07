# 1. Sinteza cercetării și configurația de referință

## 1.1 Întrebarea tehnică

Putem folosi un iPhone montat rigid pe un humanoid pentru a măsura, reconstrui și urmări obiecte cunoscute, publicând continuu o hartă și poziții 6D către un calculator de bord? Da, ca sistem de percepție cu domeniu de funcționare delimitat. Fezabilitatea nu echivalează cu o precizie garantată, funcționare nelimitată sau autorizare pentru mișcarea robotului. Proiectul propus separă achiziția, estimarea, verificarea și consumul datelor de către robot.

Poziția 6D înseamnă trei coordonate de translație și trei grade de libertate de rotație. Un fișier OBJ oferă geometrie, dar poate să nu definească unitatea, originea convenabilă sau corespondența cu obiectul fizic. Importul trebuie să producă un model metric verificat, un reper explicit, o revizie și informații despre simetrie. Un bounding box nu rezolvă singur orientarea unui obiect simetric.

## 1.2 Configurația comunicată de beneficiar

| Element | Statut | Consecință pentru proiect |
|---|---|---|
| iPhone 17 Pro Max | Model disponibil declarat de beneficiar; acces fizic neefectuat în această etapă | Profilul principal de achiziție și prima calificare |
| iPhone 18 Pro Max | Migrare intenționată | Profil separat, calibrare și revalidare; fără copiere automată a rezultatelor de pe 17 |
| NVIDIA Jetson AGX Thor 128 GB | Calculator ales de beneficiar | Procesare locală accelerată; se confirmă modulul, carrier-ul, alimentarea și imaginea software înainte de instalare |
| Humanoid propriu | URDF va fi furnizat ulterior | Interfață de integrare independentă de modelul demonstrativ |
| Unitree H1 v1 | Model public pentru demonstrație | Verificarea reperelor și vizualizarea; modelul H1_2 este exclus din acest profil |

Pagina Apple pentru 17 Pro Max confirmă LiDAR, USB 3 de până la 10 Gb/s și Wi-Fi 7. Aceste specificații nu definesc rata susținută a aplicației sau eroarea metrică a scanării. [Apple: iPhone 17 Pro Max](https://support.apple.com/en-la/125091). Există o pagină oficială pentru generația 18 la data documentării; migrarea se bazează pe specificații confirmate și probe proprii. [Apple: iPhone 18 Pro](https://www.apple.com/de/iphone-18-pro/specs/).

Configurația T5000 publicată de NVIDIA include 128 GB de memorie și un domeniu de putere de 40–130 W. Valoarea maximă de calcul FP4 nu poate fi convertită în cadre pe secundă pentru pipeline-ul nostru. [NVIDIA: configurații Jetson](https://www.nvidia.com/en-eu/autonomous-machines/embedded-systems/jetson/back-to-school/). Înainte de achiziții suplimentare, inventarul trebuie să confirme dacă utilizatorul are kitul de dezvoltare sau un modul pe carrier personalizat.

## 1.3 Ce schimbă această etapă față de dosarul anterior

Dosarul anterior stabilește scopul, echipa, cerințele și protocoalele. Această extensie fixează o configurație, alege o primă implementare, definește contracte de date și produce probe numerice independente de hardware. Cele două dosare rămân separate pentru a conserva auditurile și amprentele fișierelor. Criteriile metrologice rămân ținte propuse, fără promovarea lor la performanțe demonstrate.

Ordinea recomandată este: date corecte și sincronizate → repere calibrate → obiect cunoscut cu reper vizual → urmărire fără reper în condiții controlate → mai multe obiecte → hartă statică și dinamică → integrare humanoid. Aceasta permite izolarea cauzei unei erori. O demonstrație care pornește simultan cu SLAM, segmentare generală, reconstrucție neurală și control locomotor ar face dificilă atribuirea erorilor.

## 1.4 Metoda de cercetare

Cercetarea managerului folosește documentația producătorilor, articole primare și depozitele autorilor. Fișele de surse disting pagină integrală, articol integral, rezumat și fișier sursă descărcat. Căutarea acoperă: capabilități iPhone, combinația JetPack/ROS, poziție 6D din model cunoscut, fuziune de scanări, metrologie, licențe și integrare URDF. Nu este declarată o revizuire sistematică exhaustivă a întregii literaturi.

Pentru fiecare decizie cerem: problema, alternativele, motivul alegerii, condițiile în care alegerea devine invalidă și un experiment care poate să o infirme. Afirmațiile furnizorilor despre performanță sunt separate de măsurători independente. Articolele despre generații anterioare de iPhone indică riscuri și metode de evaluare; nu furnizează automat cifre pentru 17 sau 18.

Există trei niveluri distincte de rezultat în dosar: **documentat** prin sursă verificată; **verificat offline** prin fișiere și calcule locale; **de verificat pe hardware**. Un test de matrice 4×4 nu demonstrează calibrarea fizică. Un JSON valid nu demonstrează latență de rețea. Un URDF parsabil nu demonstrează stabilitatea mersului.

## 1.5 Rezultatul minim convingător

Prima demonstrație trebuie să conțină trei obiecte rigide, asimetrice, mate, cu modele metrice și repere vizuale, într-o cameră delimitată. Telefonul este fixat mecanic; transformarea montajului este măsurată și verificată independent. Se afișează pentru fiecare obiect identificatorul, poziția, orientarea, vârsta ultimei observații și incertitudinea. La obturare, starea devine prezisă și apoi pierdută; interfața nu păstrează o precizie aparentă.

Aceeași înregistrare se redă offline pentru comparația algoritmilor. Se provoacă pierderea conexiunii, resetarea sesiunii AR, deplasarea unui obiect și rotația trunchiului H1. Rezultatul acceptabil este un raport reproductibil cu erori și eșecuri, nu doar un videoclip în care suprapunerile par plauzibile. Extinderea către obiecte fără repere este condiționată de această bază.

## 1.6 Ipoteze explicit deschise

Nu sunt încă măsurate: rezoluția și frecvența efectivă a adâncimii în configurația aleasă, întârzierile fluxurilor, comportamentul termic, rata conexiunii prin adaptor, consumul complet al robotului, stabilitatea montajului și distribuția erorilor. Niciun prag din proiect nu trebuie folosit drept specificație comercială înaintea calificării.

Sunt necesare ulterior un Mac cu Xcode compatibil, acces la telefoane și Thor, accesorii de montaj/alimentare/rețea, referințe dimensionale și un spațiu de probe. Dosarul pregătește aceste activități; nu afirmă că ele au fost executate în mediul Windows folosit pentru documentare.
