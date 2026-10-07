# 3. Hardware, decizii și limite de integrare

## 3.1 Ce prelucrează fiecare dispozitiv

iPhone furnizează imaginile, adâncimea disponibilă, intrinseci, poziția AR și starea urmăririi. Aplicația gestionează capturarea, ghidajul, măsurarea locală și păstrarea datelor autorizate. Thor execută înregistrarea modelelor, detecția mai costisitoare, urmărirea mai multor obiecte, integrarea hărții și interfața ROS. Autoritatea estimării trebuie definită pentru fiecare reper: două sisteme SLAM nu publică independent aceeași transformare map–odom.

Un proces central distribuie observații imuabile către lucrători cu cozi limitate. Un lucrător de detecție rulează mai rar, unul de urmărire folosește cele mai recente observații, iar reconstrucția consumă keyframe-uri. Prioritizarea ține cont de vârsta observației, regiunea de interes și importanța obiectului. Numărul de fire nu este egal cu numărul de obiecte și nici cu numărul de modele GPU rezidente. Proiectul pornește cu grupuri măsurate de sarcini, nu cu câte o copie a modelului pentru fiecare obiect.

## 3.2 Buget de transfer calculat, nu măsurat

Exemplu de dimensionare: RGB NV12 la 1280×720, 30 Hz, are 1280×720×1,5×30 = 41.472.000 octeți/s. Adâncimea float32 la 256×192, 30 Hz adaugă 5.898.240 octeți/s; confidence uint8 adaugă 1.474.560 octeți/s. Totalul ipotetic este 48.844.800 octeți/s, adică aproximativ 390,76 Mb/s înainte de framing, TLS și alte metadate. Rezoluțiile și frecvențele sunt ipoteze de buget; se citesc din fluxurile reale.

Compresia video poate reduce traficul RGB, însă introduce întârziere, dependențe între cadre și artefacte. Pentru poziție metrică se păstrează relația exactă dintre imagine, crop, intrinseci și adâncime. Compresia cu pierderi a adâncimii necesită calificare separată. Un flux comprimat de exemplu la 12 Mb/s nu reprezintă o predicție a encoderului; fiecare profil salvează rata, latența și erorile efectiv observate.

O coadă de 30 de cadre la 30 Hz poate adăuga aproximativ o secundă la coadă chiar dacă algoritmul produce rezultate fluent. Pentru urmărire, un rezultat recent este preferabil acumulării nelimitate. Coada live elimină cadre vechi înaintea procesării, iar procesarea de arhivă are un canal și un buget distinct. Exemplul de calcul nu fixează profilurile finale de transport descrise de echipa de robotică.

## 3.3 Conectivitate și alimentare

USB 3 pe telefon nu dovedește existența unei interfețe de rețea iPhone–Jetson gata de utilizare. Candidatul principal este un adaptor USB-C–Ethernet compatibil cu telefonul și alimentare simultană, conectat la rețeaua locală a robotului. Se verifică accesoriul concret, rutarea aplicației, negocierea linkului și încărcarea sub sarcină. Wi-Fi este alternativa pentru dezvoltare și mobilitate în condiții controlate; jitter-ul și pierderile se măsoară.

Nu cumpărăm accesorii doar după viteza declarată. Testul de intrare urmărește 30 de minute de flux, deconectare/reconectare, trecerea termică între stări, nivelul bateriei și timpul captură–consum. Un cablu cu date insuficiente, un adaptor care reduce alimentarea sau un conector tensionat mecanic poate domina fiabilitatea sistemului. Alegerea finală se înregistrează prin producător, model, revizie, firmware și rezultate.

Puterea disponibilă pentru Thor nu include automat telefonul, adaptoarele, stocarea și răcirea. Bilanțul robotului trebuie să includă vârfurile și pierderile convertoarelor. Un exemplu pur aritmetic de 100 W timp de o oră înseamnă 100 Wh înainte de pierderi; autonomia reală necesită profilul întregului robot. Răcirea și vibrația se verifică pe montaj, nu doar pe banc.

## 3.4 Montajul pe H1 și transferul către robotul propriu

Am descărcat URDF-ul H1 și licența depozitului la commit-ul `5994d4faef0a9cadd3287f8de0199a67eeb2a259`. Parsarea XML identifică 25 de linkuri, 24 de articulații, dintre care 19 revolute, cu rădăcina pelvis. Fișierul și proveniența sunt în `05_surse/instantanee`. Nu au fost descărcate mesh-urile; URDF-ul referă 21 de URI-uri distincte pentru acestea. Snapshotul este suficient pentru auditul topologiei, nu un pachet de simulare autonom. [Unitree, commit fixat](https://github.com/unitreerobotics/unitree_ros/tree/5994d4faef0a9cadd3287f8de0199a67eeb2a259).

În model, `torso_link` este legat prin articulația revolută `torso_joint`. Un telefon prins de trunchi nu are transformare constantă față de pelvis atunci când trunchiul se rotește. Se adaugă un link de montaj fix față de torso și se compune cinematica la timestamp-ul observației. Masa și inerția suportului se vor măsura; nu adăugăm valori fabricate la modelul dinamic.

Depozitul Unitree are un istoric de integrare ROS 1/Gazebo. Nu declarăm că întregul pachet funcționează direct în ROS 2 Jazzy. Refolosim descrierea, păstrăm licența BSD cu trei clauze și pregătim un adaptor cu resource paths valide. Depozitul nu constituie un controller de mers gata de utilizat. [README Unitree](https://github.com/unitreerobotics/unitree_ros), [licență fixată](https://raw.githubusercontent.com/unitreerobotics/unitree_ros/5994d4faef0a9cadd3287f8de0199a67eeb2a259/LICENSE).

Pentru robotul propriu, contractul de predare cere: URDF/Xacro și mesh-uri cu unități/licențe, root link, joint limits, frecvența și timestamp-ul joint_states, identificarea IMU, montajul telefonului, sursa odometriei și cadrul de siguranță existent. Un test de compatibilitate verifică numele reperelor și lanțurile, iar calibrarea se reface. Schimbarea robotului nu este o înlocuire de nume de fișier.

## 3.5 Compatibilitate software

Pagina curentă NVIDIA descrie familia JetPack 7 și JetPack 7.2. Documentația versionată Isaac ROS 4.1 oferă o matrice pentru Thor/JetPack 7.0 și ROS 2 Jazzy. Alegem pentru primul experiment un ansamblu explicit compatibil din matrice; actualizarea la 7.2 are propriul test. Nu combinăm automat ultimele versiuni ale tuturor componentelor. [JetPack](https://developer.nvidia.com/embedded/jetpack), [Isaac ROS 4.1](https://nvidia-isaac-ros.github.io/v/release-4.1/repositories_and_packages/isaac_ros_mapping_and_localization/index.html).

Registrul build-ului va fixa imaginea de sistem, driverele, CUDA, TensorRT, ROS, compilatorul, digest-urile containerelor, modelele și licențele. În această etapă nu există o imagine instalată și testată pe Thor. Valoarea `candidate` în registru este intenționată. În iOS, versiunea minimă declarată a aplicației nu înseamnă că fiecare funcție este prezentă pe toate dispozitivele: verificările de capabilități decid ce moduri sunt disponibile.

## 3.6 Registru de decizii de arhitectură

| ID | Decizie propusă | Alternative evaluate | Motiv | Condiție de reconsiderare |
|---|---|---|---|---|
| ADR-01 | iPhone pentru achiziție și UX; Thor pentru operații costisitoare | Totul local pe telefon; procesare cloud | Separă sarcina termică și păstrează procesarea lângă robot | Profilul local îndeplinește singur toate țintele cu consum mai mic |
| ADR-02 | Reper vizual + model metric în prima demonstrație | Detector general + model neural imediat | Face identificabile scara, extrinsecii și erorile temporale | După calificare, variantă fără repere evaluată pe același set |
| ADR-03 | FoundationPose numai experiment de cercetare | Dependență comercială obligatorie | Restricția licenței originale | Licență adecvată verificată pentru distribuția efectivă |
| ADR-04 | Harta statică, obiecte dinamice, obstacole recente separat | Un mesh global unic | Actualizări și expirări diferite | Numai dacă un model unificat demonstrează aceleași garanții observabile |
| ADR-05 | Protocol cu epoci și revizii; deduplicare explicită | Mesaje de stare fără istoric | Reconectarea nu trebuie să reactiveze date vechi | Nicio eliminare fără probă echivalentă de recuperare |
| ADR-06 | Ansamblu software fixat și verificat | Actualizare automată la latest | Reproductibilitatea defectelor și benchmark-urilor | Migrare controlată cu replay și verificare hardware |
| ADR-07 | H1 ca model demonstrativ, apoi adaptor robot propriu | Dependențe înglobate în tot sistemul | Permite schimbarea cinematicii fără rescrierea percepției | URDF-ul propriu relevă alte cerințe de timestamp/cadru |
| ADR-08 | Validare metrică independentă de fuziune | Compararea exclusivă scanare–scanare | Două scanări pot avea aceeași eroare sistematică | Nicio înlocuire fără referință cu incertitudine documentată |

## 3.7 Registrul riscurilor prioritare

R-01: eroare sistematică de scară; detector: verificare dimensională independentă; răspuns: invalidarea profilului metric și repetarea calibrării. R-02: montaj flexibil; detector: reziduu variabil cu vibrația/postura; răspuns: reproiectarea mecanică. R-03: ceasuri nealiniate; detector: incertitudine temporală crescută și eroare dependentă de viteză; răspuns: expirarea rezultatelor și recalibrarea sincronizării.

R-04: supraîncălzire; detector: starea termică plus latență/throughput; răspuns: reducerea încărcării, apoi oprire controlată a modului dacă limitele persistă. R-05: identități interschimbate; detector: conflict între geometrie, traseu și context; răspuns: ambiguitate explicită. R-06: suprafețe transparente/lucioase; detector: adâncime inconsistentă și acoperire insuficientă; răspuns: avertizare în flux și metodă alternativă calificată.

R-07: licențe incompatibile; detector: inventar software/model fără drepturi confirmate; răspuns: blocarea distribuției componentei respective. R-08: consumator robotic care ignoră vechimea; detector: teste de fault injection; răspuns: contract respins, fără trecere la mișcare. Fiecare risc are un proprietar în fișele de rol; în implementare se adaugă frecvența observată și costul, fără scoruri numerice inventate înaintea probelor.
