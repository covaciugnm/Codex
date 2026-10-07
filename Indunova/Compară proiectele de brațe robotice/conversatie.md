# Compară proiectele de brațe robotice

ID: `01a11201-d72a-7610-9332-5ab4240808d3`  
Proiect: Indunova  
Export UTC: 2026-10-07T14:10:54.540840+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Utilizator

analiza comparativa brat robotic - ce au ni ce nu au alti - care este cel mai complet si mai serios proiect si documentat - fa un tabel comparativ intre proiecte

Cel mai apropiat proiect open-source de Armold este Faze4, deoarece are tot 6 axe și reductoare cicloidale printate 3D.
Produsul tău — Armold, Sweep Dynamics:
https://www.sweepdynamics.com/products/8446143070242
Armold are, conform producătorului, sarcină utilă de 750 g, rază de lucru de 475 mm, repetabilitate de ±1 mm și greutate de 1,8 kg. www.sweepdynamics.com
1. Faze4 — cea mai apropiată soluție mecanică
https://github.com/Source-Robotics/Faze4-Robotic-arm
Include:
- Braț cu 6 axe și reductoare cicloidale printate 3D.
- Fișiere STL, plus STEP pentru discurile cicloidale.
- Lista componentelor, instrucțiuni de asamblare și documentație electronică.
- Software și fișiere URDF pentru reprezentarea robotului.
Este însă mult mai greu decât Armold: aproximativ 15 kg, cu circa 1.000 de componente, inclusiv șuruburi și rulmenți. github.com
Documentație:
https://faze4-robotic-arm-docs.readthedocs.io/
Licență: README menționează MIT, dar fișierul actual LICENSE conține CERN-OHL-S-2.0; există o neconcordanță care trebuie clarificată pentru utilizarea comercială. github.com
2. PAROL6 — alternativă pentru un braț de birou
https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm
Braț cu 6 axe, printat 3D. Proiectul oferă STL, lista componentelor, instrucțiuni, firmware, interfață de control, API Python și simulare ROS2/MoveIt. Licența declarată este GPLv3. github.com
Software de control:
https://github.com/Source-Robotics/PAROL-commander-software
3. Thor — alternativă cu aceeași sarcină maximă declarată
https://github.com/AngelLM/Thor
Braț cu 6 axe, sarcină maximă de 750 g, inclusiv gripperul, și înălțime întinsă de 625 mm. Oferă surse FreeCAD, STEP, STL, documentație și integrare ROS2/MoveIt2. Transmisia folosește roți dințate și curele. Licență CC BY-SA 4.0. github.com
Documentație:
https://thor.angel-lm.com/documentation
Aș începe cu Faze4 pentru mecanica cicloidală, iar cu PAROL6 pentru un proiect de braț robotic de birou cu software și instrucțiuni de construcție disponibile.


## Asistent

Voi verifica sursele oficiale și voi compara mecanica, performanțele declarate, fișierele disponibile și documentația, ca să distingem proiectul cel mai complet de cel mai apropiat de Armold.


## Asistent

PAROL6 are deja cel mai bine conturat traseu de la asamblare la control și calibrare, iar Thor se remarcă prin fișierele CAD editabile. La Armold, pagina produsului nu furnizează text tehnic accesibil verificării; voi marca explicit ce pot confirma și ce rămâne bazat pe datele din mesajul tău.


## Asistent

**Dintre cele patru, aș alege PAROL6 ca proiectul cel mai complet pentru construcție și utilizare practică. Thor este cel mai deschis pentru modificarea mecanicii, iar Faze4 este cel mai apropiat de Armold prin reductoarele cicloidale.** Pentru Armold nu am putut verifica suficientă documentație publică pentru a-l clasa corect alături de celelalte.

Am evaluat „seriozitatea” prin posibilitatea de a reproduce proiectul: fișiere, componente, asamblare, electronică, software, calibrare și limite tehnice explicate. Este o evaluare a documentației disponibile la **6 octombrie 2026**, nu rezultatul unor teste fizice.

**Comparația tehnică**

Valorile sunt declarate de autori/producători. „Neconfirmat” înseamnă că nu am găsit o dovadă suficientă în sursele verificate, nu că funcția lipsește obligatoriu.

| Criteriu | Armold — Sweep Dynamics | Faze4 | PAROL6 | Thor |
|---|---|---|---|---|
| **Număr de axe** | 6 | 6 | 6 | 6 |
| **Transmisie** | Reductoare cicloidale 26:1, control stepper CANBUS | Cicloidale pe J1–J5, curele pe unele axe; **planetar pe J6** | Reductoare planetare și curele | Roți dințate printate, fulii și curele GT2 |
| **Sarcină utilă** | 750 g | Neconfirmată în pagina tehnică verificată | **1 kg aproape de bază; 500 g în întregul spațiu de lucru** | Maximum 750 g, **inclusiv gripperul** |
| **Rază de lucru** | 475 mm | Dimensiuni ale segmentelor publicate; fără o valoare explicită verificată pentru rază | 400 mm cu gripperul standard | 625 mm reprezintă **înălțimea întinsă**, nu raza de lucru |
| **Repetabilitate** | ±1 mm, conform informației furnizate de tine; nereconfirmată | Neconfirmată | **0,1 mm în documentație; 0,2 mm pe pagina comercială** | Neconfirmată |
| **Greutate** | 1,8 kg, conform informației furnizate de tine; nereconfirmată | Aproximativ 15 kg | 5,5 kg în tabelul tehnic | Neconfirmată |
| **Particularitate** | Ansamblu compact și actuatoare cicloidale | Aproximativ 1.000 de componente, inclusiv șuruburi și rulmenți | Platformă de birou cu software și periferice documentate | Mecanică disponibilă inclusiv în formatul nativ FreeCAD |
| **Surse pentru comparație** | [Comunicarea producătorului](https://www.linkedin.com/company/sweep-dynamics) | [Proiect](https://github.com/Source-Robotics/Faze4-Robotic-arm), [transmisii și dimensiuni](https://faze4-robotic-arm-docs.readthedocs.io/en/latest/I_Robot_data.html) | [Specificații tehnice](https://source-robotics.github.io/PAROL-docs/page2_2/), [pagina comercială](https://source-robotics.com/products/parol6-robotic-arm) | [Proiect și specificații](https://github.com/AngelLM/Thor) |

**Comparația documentației și a lucrurilor pe care le primești efectiv**

| Criteriu | Armold | Faze4 | PAROL6 | Thor |
|---|---|---|---|---|
| **STL pentru imprimare** | Accesul și condițiile nu au putut fi verificate | Da | Da | Da |
| **CAD editabil** | Neconfirmat | STEP pentru discurile cicloidale; nu am confirmat CAD complet pentru braț | STEP separat, contra cost; **nu este open-source**, fără ansamblul complet | **FreeCAD + STEP**, publice |
| **Listă de componente — BOM** | Pachet public neconfirmat | Da | Da | Da, indicată în ghidul proiectului |
| **Instrucțiuni de asamblare** | Amploarea lor nu a putut fi evaluată | Manual PDF și documentație web | Manual, ghiduri video și pași de punere în funcțiune | Ghiduri, videoclipuri și instrucțiuni interactive indicate de proiect |
| **Electronică** | CANBUS anunțat; schemele și sursele publice neconfirmate | Fișiere PCB, cablare și cod de test | Placă dedicată, cablare și firmware documentate | Proiect PCB separat; opțiuni de plăci comerciale |
| **Control și programare** | Sweep Sync; promovat pentru utilizare fără programare | MATLAB și cod de test/dezvoltare | **Commander, programare de mișcări și API Python** | G-code; interfață Asgard |
| **ROS / MoveIt** | Integrare utilizabilă neconfirmată | URDF disponibil; secțiunea ROS a ghidului verificat este necompletată | ROS2/MoveIt2; simulare și instrucțiuni pentru conectarea hardware, cu rezervele de mai jos | ROS2 Humble, MoveIt2, Gazebo și Asgard web |
| **Calibrare și diagnosticare** | Neconfirmate public | Documentație cu acoperire inegală | **Homing, ajustări, teste ale componentelor și diagnosticare explicate** | Resurse de configurare disponibile; ghidul web nu a putut fi inspectat integral |
| **Limitarea principală** | Transparență tehnică insuficient verificabilă | Software mai experimental și secțiuni incomplete | CAD-ul STEP nu este deschis; unele specificații sunt neuniforme | Performanțe metrologice insuficient cuantificate în sursele consultate |

Pentru fișiere și construcție, comparația se bazează pe depozitele [Faze4](https://github.com/Source-Robotics/Faze4-Robotic-arm), [PAROL6](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm) și [Thor](https://github.com/AngelLM/Thor). Restricțiile CAD ale PAROL6 sunt precizate explicit pe [pagina fișierelor STEP](https://source-robotics.com/products/parol6-step-files).

Există câteva diferențe importante față de prezentarea inițială:

- **Faze4 are documentație multă, dar nu completă.** Autorul descrie codul de nivel înalt ca material pentru testare și dezvoltare proprie. Pagina include exemple MATLAB, însă secțiunea ROS este goală. Aș folosi proiectul în special pentru studierea mecanicii cicloidale. [Documentația software Faze4](https://faze4-robotic-arm-docs.readthedocs.io/en/latest/G_Code2.html)
- **PAROL6 documentează mai bine utilizarea efectivă.** Explică instalarea, încărcarea firmware-ului, homing-ul, reglarea pozițiilor și testarea componentelor. Acesta este principalul motiv pentru care îl pun primul pentru construcție și exploatare. [Punere în funcțiune](https://source-robotics.github.io/PAROL-docs/page3_2/), [software și API](https://source-robotics.github.io/PAROL-docs/page4/)
- **Suportul ROS2 trebuie evaluat separat.** PAROL6 are acum instrucțiuni pentru hardware real printr-un proiect suplimentar, dar README păstrează „Move PAROL6” nebifat; nu îl consider astfel validat integral. Thor publică un pachet care reunește planificarea, simularea și interfața web. [PAROL6 ROS2](https://github.com/Source-Robotics/PAROL6-ROS2-MOVEIT), [Thor ROS2](https://github.com/AngelLM/Thor-ROS)
- **Licențele nu sunt echivalente.** Faze4 păstrează contradicția dintre MIT în README și CERN-OHL-S-2.0 în LICENSE. PAROL6 publică sub GPLv3 codul, instrucțiunile/BOM și STL-urile, dar exclude STEP-urile. Thor declară CC BY-SA 4.0 pentru proiect. [Faze4 LICENSE](https://github.com/Source-Robotics/Faze4-Robotic-arm/blob/master/LICENSE), [PAROL6 licențiere](https://source-robotics.github.io/PAROL-docs/#licence), [Thor](https://github.com/AngelLM/Thor)

**Alegerea mea, în funcție de obiectiv:**

| Ce vrei să faci | Proiectul pe care l-aș alege | Motivul decisiv |
|---|---|---|
| Să construiești un braț și să ajungi la aplicații funcționale | **PAROL6** | Cel mai coerent ansamblu de instrucțiuni, control, calibrare și periferice |
| Să modifici geometria și să dezvolți mecanica proprie | **Thor** | Acces la sursele CAD native și STEP |
| Să studiezi sau să dezvolți reductoare cicloidale | **Faze4** | Arhitectura cea mai apropiată de Armold dintre proiectele analizate |
| Să alegi Armold pentru dimensiuni și greutate reduse | **Armold, condiționat de verificarea pachetului tehnic** | Concept atractiv, dar documentația publică verificată nu permite aceeași încredere în reproducere și integrare |

**Pentru un proiect propriu, aș lua PAROL6 drept reper pentru documentație și software, Thor pentru accesul la CAD și Faze4 pentru mecanica cicloidală.** Armold rămâne un reper de compactitate, însă nu pot susține, pe dovezile disponibile, că este cel mai complet sau cel mai bine documentat.
