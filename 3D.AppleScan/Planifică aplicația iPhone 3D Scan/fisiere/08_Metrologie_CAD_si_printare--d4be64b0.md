# 8 Metrologie conversii CAD și imprimare 3D

## 8.1 Ce anume măsurăm

Înainte de alegerea algoritmului se definește măsurandul: distanța dintre două puncte identificabile, distanța dintre plane, gabaritul într-un reper sau suprafața unei regiuni. Diagonala cutiei aliniate cu axele scenei nu este dimensiunea intrinsecă a unui obiect rotit. Grosimea unui perete observat dintr-o singură parte nu este măsurată direct.

Se disting eroarea față de referință, repetabilitatea în condiții similare și incertitudinea rezultatului. Un set de scanări care se suprapun foarte bine poate împărtăși aceeași eroare de scară. În protocolul nostru, referințele pentru verificare sunt independente de datele folosite la ajustare. NIST recomandă raportarea componentelor incertitudinii, a metodei de evaluare și a factorului de acoperire când se raportează incertitudine extinsă. [NIST TN 1297](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty)

## 8.2 Bugetul de incertitudine propus

Modelul d=f(z,K,T,s,p) exprimă dependența unei distanțe de adâncime z, intrinseci K, transformări T, scară s și alegerea punctelor p. Într-o aproximare locală, u²(d)=JΣJᵀ, unde Σ include covarianțele intrărilor și corelațiile relevante. Aproximarea liniară se verifică prin simulare când geometria, ocluzia sau segmentarea produc neliniarități mari.

Componentele urmărite sunt zgomotul adâncimii, biasul pe material și distanță, înregistrarea RGB–depth, orientarea montajului, sincronizarea, deriva sesiunii, selecția punctelor, discretizarea plasei și cuantizarea exportului. O valoare confidence furnizată de un API nu devine direct milimetri sau covarianță. Relația trebuie calibrată experimental pe loturi distincte.

Pentru produs se poate comunica un interval estimat numai după verificarea acoperirii sale empirice. P95 al erorilor unui lot nu este intervalul de incertitudine individuală pentru fiecare captură. Dacă nu avem un model calificat, afișăm starea orientativă și cerem verificarea cotelor critice.

## 8.3 Scanări repetate și înregistrare

Pipeline-ul propus păstrează capturile brute eligibile, extrage cadre informative, aliniază perechi cu suprapunere suficientă, verifică corespondențele și optimizează transformările unui graf de poziții. Open3D oferă un exemplu de înregistrare multiplă bazată pe pose graph, cu tratament al legăturilor incerte. Folosirea acelui algoritm nu garantează eliminarea tuturor alinierilor greșite. [Open3D multiway registration](https://www.open3d.org/docs/release/tutorial/pipelines/multiway_registration.html)

Decizia de a accepta o aliniere folosește eroare reziduală, distribuția spațială a corespondențelor, suprapunere și observabilitate. Două suprafețe plane aproape identice pot permite deplasări slab constrânse. Nu se acceptă o corecție mare numai pentru că reduce o medie numerică pe o porțiune mică.

Se separă experimentul de densificare de cel de corectare metrică. Pentru o cameră scanată de trei ori raportăm: eroarea pe repere ținute deoparte, acoperirea, numărul de puncte, duplicarea pereților și variația între sesiuni. O îmbunătățire doar vizuală nu trece poarta dimensională.

## 8.4 Scara și modelele deja existente

La importul OBJ sau al altui model verificăm unitatea, dimensiunile cunoscute, axele, originea, transformările și materialele. Dacă unitatea nu este disponibilă explicit, cerem alegerea ei sau o referință identificată. Modelul păstrează separat geometria originală și transformarea de normalizare; procesarea nu rescrie discret coordonatele fără proveniență.

Pentru estimarea 6D, punctele și originea modelului au efect asupra interpretării poziției. Centrul unei cutii și un punct de prindere nu sunt interschimbabile. În catalog, frame_model definește geometria, iar frame_grasp poate descrie o priză proiectată și verificată separat. Nicio priză nu devine executabilă doar prin existența unui OBJ.

## 8.5 Matricea formatelor propuse

| Etapă | Format | Utilizare | Ce trebuie demonstrat |
|---|---|---|---|
| P0 | STL | Mesh pentru slicer | Scară convenită, triangulare, orientare și import |
| P0 | 3MF | Pachet pentru imprimare | Unități, obiecte și subset de proprietăți suportate |
| P0 | PLY | Nor sau plasă inspectabilă | Atribute, coordonate și convenția unităților |
| P0 | USDZ | Previzualizare și schimb în ecosistem Apple | Transformări, scară și texturi |
| P0 | DXF 2D plus JSON | Plan cotat și metadate | Entități, unități, cote implementate, reimport |
| P1 | OBJ și GLB/glTF | Modele vizuale și modele de referință | Materiale, axe, unitate externă unde necesar |
| P1 | E57 LAS/LAZ XYZ/PTS PCD | Schimb de nori de puncte | Subset de câmpuri, cuantizare, sistem de coordonate |
| P1 | DWG | Integrare CAD cerută de client | SDK/convertor licențiat, platformă și versiune |
| P2 | IFC STEP/BRep | Semantică BIM și geometrie inginerească | Reconstrucție și structurare suplimentare |
| P2 | AMF VRML 3DS | Compatibilitate după cerere | Destinații reale și pierderi documentate |

Tabelul reprezintă obiective, nu formate deja implementate. Specificația 3MF definește un format cu structură și extensii; compatibilitatea unui fișier trebuie testată pe subsetul ales și pe aplicația destinatară. [3MF Consortium](https://3mf.io/spec/)

Pentru DWG, ODA oferă Drawings SDK. Decizia comercială trebuie să verifice licența, distribuirea și platformele versiunii efectiv integrate; nu se presupune că simpla schimbare a extensiei DXF produce DWG. [ODA Drawings SDK](https://www.opendesign.com/products/drawings)

Un mesh scanat nu devine automat model parametric editabil. STEP/BRep cere reconstruirea suprafețelor și topologiei adecvate; IFC cere clasificare semantică și relații de clădire. Aceste extensii se califică separat de exportul geometric de bază.

## 8.6 Controlul imprimării

Fluxul propus este captură → control scară → curățare documentată → verificare geometrie → export → slicer → imprimare → măsurare. Se verifică muchii neetanșe, fețe degenerate, auto-intersecții, normale, grosimi minime și componente separate. Umplerea automată a unei găuri poate schimba funcția piesei; previzualizarea diferenței este obligatorie.

G-code depinde de imprimantă, firmware, material, duză sau tehnologie, temperaturi și profil. Dosarul nu propune G-code universal. Pentru fiecare probă fizică se păstrează versiunea slicerului, profilul, orientarea, suporturile, scara și identificarea materialului. Eroarea scanării, eroarea conversiei și eroarea imprimării se raportează separat.

Un lot propus de calificare include cel puțin 10 geometrii cu pereți, găuri, suprafețe curbe și îmbinări, fiecare în două orientări relevante pentru imprimanta aleasă. Numărul este un minim de pilot; nu susține singur toate materialele și tehnologiile. Pentru piese funcționale, toleranțele sunt impuse de utilizare și pot depăși posibilitățile capturii cu telefonul.

## 8.7 Pragurile dimensionale adoptate

L se exprimă în milimetri. Pentru obiecte rigide mate de 0,1–1 m, ținta P95 este max(5 mm, 0,01L); pentru live de 0,2–5 m, max(20 mm, 0,01L); pentru camere de 1–8 m, max(30 mm, 0,01L). Aceste praguri sunt propuse, moștenite din documentația anterioară și limitate la condițiile declarate.

Conversia numerică pe fixture exact are ținta max(0,01 mm, 10⁻⁵L), distinctă de eroarea capturii. Nu se folosește aliniere cu scară liberă la evaluarea exportului, deoarece ar ascunde o unitate greșită. Pentru loturi cu lungimi diferite se folosește r_i=e_i/tol(L_i), iar limita superioară CI95 pentru P95(r) trebuie să fie ≤1. Se cer și succes de captură ≥95% din încercările eligibile și limita inferioară CI95 ≥90%, cu gruparea pe obiect/cameră tratată explicit. Definiția completă se află în CRITERII_CANONICE. Lotul insuficient produce rezultat inconcludent, nu acceptare.

## 8.8 Trasabilitatea rezultatului

Fiecare raport dimensional conține identificatorul capturii, dispozitiv și OS, calibrare, referința independentă și incertitudinea ei, operator, mediu, versiunea algoritmului, pașii de procesare, unități și metrici. Dacă o cotă este corectată manual, valoarea observată și cea corectată rămân accesibile.

Un raport de export include hashul intrării și ieșirii, versiunea convertorului, subsetul, opțiunile, avertismentele și rezultatul reimportului. O fotografie a slicerului poate susține verificarea vizuală, dar nu înlocuiește măsurarea coordonatelor sau testul fizic. Auditorul poate reproduce parcursul din aceste artefacte fără explicații orale ale autorului.
