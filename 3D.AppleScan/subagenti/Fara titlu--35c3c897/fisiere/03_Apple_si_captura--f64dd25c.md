# 3. Platforma Apple, achiziția și integritatea măsurării

**Statut:** propunere de arhitectură și protocol de cercetare, 2 octombrie 2026. Autor: agentul specialist Apple și percepție. Niciun rezultat fizic sau performanță a aplicației native nu este declarat măsurat în acest capitol. Criteriile dimensionale și de recuperare din dosarul anterior `3dscan-documentatie/05_validare/CRITERII_CANONICE.md` au prioritate. Suportul unei funcții într-un SDK nu constituie implementarea ei în EVA-3dScan.

## 3.1. Întrebarea de cercetare și granițele platformei

Investigăm dacă un dispozitiv mobil poate furniza simultan observații geometrice utile pentru măsurare, un catalog de obiecte și percepție pentru un robot, menținând întârzieri, consum și incertitudine controlabile. Ipoteza de lucru este că reutilizarea aceleiași capturi reduce transferurile de memorie și costul energetic față de mai multe fluxuri independente. Ipoteza trebuie comparată experimental, nu dedusă din numărul de procesoare disponibile.

Cele trei produse de captură sunt distincte: obiect cotat și exportabil; măsurare live fără păstrarea mediului; proiect persistent cu camere și relații între ele. Extensia robotică introduce o a patra configurație de funcționare, cu politici explicite pentru transport și persistență. O sesiune live fără salvare nu devine implicit sesiune de înregistrare doar pentru că software-ul produce diagnostice. Diagnosticele implicite trebuie să excludă imaginile, harta și identitatea persoanelor.

Camera și LiDAR-ul măsoară numai ce este observabil. Suprafețele ascunse, reflexive, transparente, foarte întunecate sau aflate în mișcare cer clasificarea rezultatului drept incomplet ori în afara domeniului calificat. Algoritmul poate completa vizual un model, dar completarea trebuie separată de suprafața măsurată. Robotul nu trebuie să trateze o completare geometrică drept observație a spațiului liber.

## 3.2. Matrice de capabilități, nu listă comercială de telefoane

Înaintea primei capturi se generează un manifest cu modelul dispozitivului, versiunea și buildul OS, versiunea aplicației, SDK-ul utilizat la compilare, formatele video acceptate, verificările API și rezultatul unei capturi de probă. Disponibilitatea în compilare și disponibilitatea la execuție sunt două porți separate. Un răspuns pozitiv la `isSupported` nu este o certificare dimensională.

| Funcție propusă | Verificare obligatorie | Ieșire posibilă | Comportament dacă lipsește |
|---|---|---|---|
| Urmărirea camerei | Suportul configurației ARKit și starea sesiunii | Transformare cameră–lume | Captură 2D sau funcție indisponibilă, explicată |
| Adâncime posterioară | `supportsFrameSemantics(.sceneDepth)` și existența datelor | Adâncime și încredere | Fără promisiune de nor metric LiDAR |
| Reconstrucția suprafețelor | Suportul `sceneReconstruction` al configurației | Fragmente de mesh | Algoritm alternativ validat sau dezactivare |
| Captură ghidată de obiecte | `ObjectCaptureSession.isSupported` | Imagini și metadate pentru reconstrucție | Captură foto separată, dacă este implementată |
| Reconstrucție fotogrammetrică | `PhotogrammetrySession.isSupported` | Model reconstruit | Procesare pe Mac compatibil, cu acord pentru transfer |
| Scanarea camerelor | `RoomCaptureSession.isSupported` | Structură parametrică de cameră | Modul camere dezactivat |
| Urmărire nativă nouă de obiecte | SDK, OS, format și probă pe dispozitiv | Ancore de obiect | Marker sau algoritm propriu evaluat |

Apple cere verificarea suportului înaintea creării `ObjectCaptureSession`; lipsa suportului poate produce eroare la execuție. Captura ghidată și reconstrucția prin `PhotogrammetrySession` sunt faze diferite. [A01 — ObjectCaptureSession](https://developer.apple.com/documentation/realitykit/objectcapturesession), [A02 — verificarea capturii](https://developer.apple.com/documentation/realitykit/objectcapturesession/issupported), [A03 — verificarea reconstrucției](https://developer.apple.com/documentation/realitykit/photogrammetrysession/issupported)

Pentru RoomPlan, verificarea publicată de Apple leagă suportul de prezența LiDAR. Nu deducem aceeași disponibilitate pentru camera frontală TrueDepth sau pentru orice model cu sufix comercial similar. [A04 — RoomCaptureSession.isSupported](https://developer.apple.com/documentation/RoomPlan/RoomCaptureSession/isSupported)

## 3.3. Separarea capturii și reconstrucției unui obiect

Fluxul propus are șapte stări persistente: proiect inițiat, obiect definit, captură începută, captură încheiată, reconstrucție în curs, control geometric, export verificat. Fiecărei tranziții i se asociază un identificator, artefacte de intrare, parametri și motivul eșecului, dacă există. Nu acceptăm un model doar pentru că procesul de reconstrucție a terminat fără excepție.

În captură verificăm acoperirea angulară, claritatea, expunerea, procentul de fundal, stabilitatea obiectului și existența unei referințe de scară independente. Pentru obiecte rigide mate de 0,1–1 m se păstrează ținta canonică P95 a erorii absolute cel mult `max(5 mm, 0,01 × L)`. Este o țintă propusă pe domeniul calificat, nu precizia fiecărui pixel sau a fiecărei capturi. Acceptarea finală cere și limita superioară a intervalului de încredere de 95% pentru P95 sub prag.

Un obiect subțire, o suprafață lucioasă ori o piesă cu toleranță industrială mică poate produce un model vizual convingător și totuși necorespunzător dimensional. Fișa de rezultat separă aspectul texturii, completitudinea suprafeței, eroarea dimensională și posibilitatea de fabricație. Un mesh închis algoritmic nu dovedește că partea inferioară a obiectului a fost scanată.

Pentru economie de calcul se propun o reconstrucție preliminară pentru ghidaj și una finală după captură. Se păstrează parametrii și versiunea algoritmului, astfel încât o reconstrucție ulterioară să poată fi comparată cu prima fără rescrierea intrărilor originale. Dublarea spațiului necesar în această etapă intră în calculul capacității, nu este ascunsă de dimensiunea mică a exportului final.

## 3.4. Achiziția RGB–adâncime și calibrarea

`sceneDepth` trebuie activat prin semantica configurației și poate lipsi pe dispozitive sau configurații nesuportate. `confidenceMap` conține niveluri de încredere ale cadrului, influențate inclusiv de reflectivitate și lumină. Aceste niveluri nu reprezintă automat o abatere standard în milimetri. [A05 — sceneDepth](https://developer.apple.com/documentation/arkit/arframe/scenedepth), [A06 — confidenceMap](https://developer.apple.com/documentation/arkit/ardepthdata/confidencemap)

Protocolul propus verifică asocierea dintre imagine, adâncime, calibrare și transformarea camerei pentru fiecare cadru. Pentru reproiecție folosim o matrice intrinsecă aferentă rezoluției efective. Dacă o imagine este decupată, rotită sau redimensionată, transformarea pixelilor se compune explicit; simpla utilizare a aceleiași matrice pentru orice rezoluție este incorectă. Pixelii fără adâncime validă rămân necunoscuți, nu sunt transformați în puncte la origine.

Într-un model pinhole convențional, un pixel omogen `u` și adâncimea axială `z` dau punctul `p_C = z K⁻¹u`. În implementare se verifică definiția valorii furnizate de API și convenția reperului; dacă valoarea este distanță de-a lungul razei, formula trebuie normalizată. Testul obligatoriu folosește un plan frontal și unul înclinat, la distanțe independente cunoscute. Transformarea în lumea sesiunii este apoi `p_W = T_WC p_C`. Aceasta este formularea matematică a proiectului, nu cod verificat pe un telefon.

Se evaluează separat adâncimea curentă și cea netezită temporal. Netezirea poate îmbunătăți aspectul, dar fluxul pentru obstacole mobile trebuie judecat după întârziere și artefacte de mișcare, nu după imaginea mai plăcută. Modelul de eroare include biasul distanței, unghiul de incidență, temperatura, materialul și eroarea de aliniere temporală. O medie din observații corelate nu reduce eroarea precum media unor măsurări independente.

## 3.5. Camere, scanări repetate și repere comune

Apple permite combinarea camerelor când acestea au un spațiu comun compatibil: prin aceeași sesiune AR menținută între capturi sau prin relocalizare dintr-o hartă salvată. În al doilea caz trebuie așteptată revenirea urmăririi la starea normală înaintea continuării. [A07 — capturedStructure(from:)](https://developer.apple.com/documentation/roomplan/structurebuilder/capturedstructure%28from%3A%29)

Propunerea de cercetare nu suprapune mecanic pereți până când rezultatul pare drept. Fiecare tur produce observații și constrângeri; optimizarea poate corecta deriva, dar nu inventează cote independente. Se rezervă repere de control nefolosite la aliniere. Raportul diferențiază reziduul de ajustare de eroarea pe aceste repere. Un rezultat cu reziduu mic poate avea în continuare scară greșită.

Modelele de cameră trebuie să păstreze atât geometria observată, cât și cea regularizată pentru desen. Dacă un perete este ajustat la un unghi de 90°, regula, abaterea înainte și după, precum și motivul se înregistrează. Caracterul parametric al produsului nu autorizează tratarea oricărei camere ca dreptunghi perfect. Pentru camere rămâne ținta canonică `P95 ≤ max(30 mm, 0,01 × L)` în domeniul 1–8 m.

Documentația Apple curentă descrie și structuri cu etaje. Proiectul EVA păstrează însă capturarea și unirea robustă între niveluri reale în prioritatea de produs P2, conform criteriilor canonice; existența API nu elimină validarea proprie. [A08 — scanarea unei structuri](https://developer.apple.com/documentation/roomplan/scanning-the-rooms-of-a-single-structure)

## 3.6. Reconstrucție statică și obstacole dinamice

`ARMeshAnchor` subdivide mediul în fragmente actualizate pe măsura rafinării. Apple precizează explicit că reacția meshului la schimbările fizice nu este concepută ca reprezentare în timp real a acelor mișcări. [A09 — ARMeshAnchor](https://developer.apple.com/documentation/arkit/armeshanchor)

În consecință propunem trei straturi cu politici distincte: structură persistentă, observații locale recente și obiecte mobile urmărite. Un scaun mutat nu trebuie să rămână simultan în harta statică și în stratul dinamic fără o regulă de reconciliere. „Eliminat din hartă”, „neobservat” și „confirmat absent prin observație nouă” sunt evenimente diferite. Zona neobservată nu devine liberă prin expirarea unei detecții.

Resetarea originii AR creează un nou `map_epoch`; restartul procesului creează un nou `session_id`, iar discontinuitatea ceasului creează un nou `clock_epoch`. Termenul local `session_epoch` desemnează numai cheia compusă `(session_id, map_epoch, clock_epoch)`, fără a înlocui aceste trei câmpuri în transport. Rezultatele vechi nu sunt aplicate direct peste noul reper. Dacă relocalizarea furnizează o corespondență validată, se înregistrează transformarea dintre epoci și versiunea hărții; altfel se solicită o nouă aliniere. În timpul ambiguității, exportul de poziții către robot este marcat indisponibil, chiar dacă previzualizarea camerei continuă. Restartul nu presupune obligatoriu hartă nouă: o hartă persistentă poate fi recuperată numai după validarea relocalizării.

## 3.7. API nou pentru obiecte: pistă condiționată

La consultare, documentația Apple pentru `.referenceobject` pe iPhone/iPad indică iOS 27 sau ulterior, maximum zece fișiere în total pentru detecție și urmărire și incompatibilitatea amestecării cu `.arobject` în aceeași sesiune. Urmărirea mobilă consumă mai mult decât detecția obiectelor în principal staționare. O pagină asociată `trackingObjects` este etichetată Beta. [A10 — obiecte de referință în iOS](https://developer.apple.com/documentation/visionos/using-a-reference-object-with-arkit-in-ios), [A11 — trackingObjects](https://developer.apple.com/documentation/arkit/argeotrackingconfiguration/trackingobjects)

Decizia de arhitectură este izolarea acestui furnizor în spatele unei interfețe comune. Nu condiționăm prima versiune stabilă de disponibilitatea sa și nu extrapolăm facilitățile visionOS la iOS. Înainte de utilizare comercială se verifică SDK-ul instalat, disponibilitatea simbolurilor, condițiile distribuției și comportamentul pe hardware real. Importarea unui OBJ rămâne o etapă diferită de construirea unui obiect de referință antrenat și de obținerea unei poziții în imagine.

## 3.8. Continuitate, energie și protocol de acceptare

Captura în fundal este restricționată în scenariul obișnuit iOS; o aplicație de percepție nu poate promite operare nelimitată după blocarea telefonului. [A12 — întreruperea camerei în fundal](https://developer.apple.com/documentation/avfoundation/avcapturesession/interruptionreason/videodevicenotavailableinbackground) RoomPlan documentează erori pentru temperatură excesivă, configurație invalidă și pierderea urmăririi. [A13 — erori RoomPlan](https://developer.apple.com/documentation/roomplan/roomcapturesession/captureerror)

| Sarcină | Activitate și artefact | Rezultat cuantificabil propus | Auditor |
|---|---|---|---|
| APPLE-01 | Manifest pe fiecare combinație hardware/OS susținută | 100% funcții publicate au verificare runtime și probă documentată | Auditor Apple |
| APPLE-02 | Calibrare RGB–adâncime pe planuri și repere | Eroare raportată pe distanță, unghi și material; niciun prag inventat după test | Auditor metrologie |
| APPLE-03 | 10 probe pilot de întrerupere, apoi lotul canonic de 50 | Zero pierderi ale artefactelor confirmate; limitele API opace declarate | Auditor fiabilitate |
| APPLE-04 | Scanări de cameră repetate și repere independente | Raport înainte/după, eșecuri incluse, pragul canonic testat | Auditor geometrie |
| APPLE-05 | Sesiuni continue în trei condiții termice definite în protocol | Timpi, temperatură/stare termică, consum și opriri înregistrate | Auditor performanță |

Datele deja confirmate ca salvate trebuie recuperate integral. Ținta de cel mult cinci secunde de pierdere între checkpointuri privește numai fluxurile serializabile controlate de aplicație. Starea internă opacă Object Capture sau RoomPlan nu este declarată recuperabilă exact. Reluarea documentației este exactă la sarcină și artefact; reluarea unei capturi fizice poate necesita repetarea etapei. Aceste două contracte nu trebuie confundate.
