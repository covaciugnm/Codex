# 1 Cadrul științific și obiectivele cercetării

## 1.1 Rezumat

EVA 3dScan este propusă ca aplicație iPhone pentru capturarea geometriei, estimarea dimensiunilor și întreținerea unei reprezentări spațiale a obiectelor și încăperilor. Extensia robotică folosește telefonul montat rigid ca sursă de observații pentru un calculator ROS 2. Problema centrală este combinarea utilității pentru persoane cu trasabilitatea geometrică, temporală și operațională necesară unui robot.

Lucrarea definește ce trebuie construit, ce rămâne cercetare și cum se decide acceptarea. Ipoteza de lucru este că o arhitectură cu fluxuri distincte pentru geometria persistentă, obstacolele recente și identitățile obiectelor poate oferi o utilizare mai eficientă a resurselor decât procesarea completă a fiecărui cadru. Această ipoteză va fi testată; nu se afirmă că a fost demonstrată.

Sistemul nu are o singură măsură de calitate. O plasă cu aspect plăcut poate avea scară incorectă; un detector precis poate produce rezultate prea vechi; un tracker fluid poate păstra identitatea greșită; o hartă globală coerentă poate ascunde obstacole apărute recent. Evaluarea se face simultan pe eroare geometrică, acoperire, rată de succes, latență, consum, interpretarea utilizatorului și recuperabilitate.

## 1.2 Întrebări de cercetare

RQ1 întreabă în ce condiții scanările repetate reduc eroarea dimensională față de o singură trecere. Se compară aceeași referință independentă, materiale și iluminări, păstrând toate eșecurile. O scădere a zgomotului fără reducerea biasului nu este interpretată ca rezolvare a acurateței.

RQ2 examinează contribuția unui model anterior OBJ/USDZ, a adâncimii și a texturii la estimarea 6D. Se evaluează obiecte asimetrice și simetrice, identificarea categoriei și distingerea exemplarelor. Un rezultat corect doar până la o simetrie geometrică trebuie declarat astfel.

RQ3 testează dacă programarea adaptivă a procesării în funcție de mișcare, incertitudine și importanță reduce energia și latența fără o degradare inacceptabilă a urmăririi. Comparația include un program fix la același buget de calcul, nu doar un baseline intenționat lent.

RQ4 examinează stabilitatea hărții distribuite iPhone–robot la pierderi de pachete, reconectări, drift temporal și relocalizare. Corectitudinea include absența rezultatelor aplicate în cadrul de referință greșit, chiar dacă interfața pare fluidă.

RQ5 testează dacă utilizatorii înțeleg diferența dintre măsurare orientativă, rezultat verificat, poziție prezisă și ultima poziție observată. Nu este suficient ca un specialist să înțeleagă legenda.

RQ6 investighează limitele telefonului pentru percepția unui humanoid: vizibilitatea picioarelor și a podelei, vibrații, mișcarea capului, temperatură și întreruperi. Rezultatul poate fi o delimitare justificată a utilizărilor, inclusiv respingerea unor scenarii.

## 1.3 Contribuții propuse și limitele originalității

Contribuția propusă C1 este un contract comun de observații și obiecte care păstrează unitatea, cadrul, timpul și proveniența între aplicație, export și robot. C2 este un mecanism de alocare a resurselor evaluat experimental pe sarcini concurente. C3 este un protocol unitar care urmărește erorile de la captură până la export și decizia robotică. C4 este o interfață care expune incertitudinea fără a bloca activitățile uzuale.

Acestea sunt contribuții candidate. Originalitatea necesită o revizuire sistematică extinsă a literaturii, comparație cu metodele publicate și rezultate reproductibile. Folosirea ARKit, RoomPlan, ICP sau ROS 2 în aceeași aplicație nu constituie, singură, contribuție doctorală. Dosarul este o bază de proiect și de protocol, nu o certificare academică.

## 1.4 Obiectivele cuantificabile

O1 cere definirea completă a celor trei moduri inițiale, fiecare cu date de intrare, stări, rezultat, erori și test de acceptare. O2 cere ca fiecare cerință din registru să aibă cel puțin un experiment sau un control documentar asociat. O3 cere ca fiecare sarcină să aibă proprietar, auditor diferit, dependențe și dovadă de rezultat.

O4 cere ca toate mesajele de percepție persistente să poată fi atribuite unei sesiuni și versiuni de hartă și ca rezultatele expirate să nu înlocuiască observații mai noi. O5 cere caracterizarea experimentală a profilurilor metrice și de latență din criteriile canonice. O6 cere recuperarea tuturor rezultatelor deja confirmate ca salvate, verificată prin identificatori și hashuri.

Pentru documentul prezent sunt măsurabile acoperirea cerințelor, integritatea registrelor, consistența legăturilor, închiderea constatărilor și identitatea copiei livrate. Pentru produs, aceleași registre păstrează statusul planificat până la efectuarea testelor. Niciun procent de satisfacție al auditorului nu înlocuiește rezultatele acestora.

## 1.5 Metoda de documentare

Sursele primare prioritare sunt documentațiile Apple și ROS, specificațiile formatelor, proiectele oficiale și publicațiile despre evaluare. Pentru fiecare sursă se consemnează afirmația susținută, nivelul accesului, data consultării și limitele. O pagină găsită într-un motor de căutare nu este declarată citită integral.

Feedbackul clienților din documentația precedentă rămâne o sursă exploratorie pentru probleme și vocabular, nu un eșantion reprezentativ de piață. Planul include interviuri și teste noi, cu numitor și criteriu de succes stabilite anterior. Nu se fabrică citate de clienți sau validări ale cererii comerciale.

## 1.6 Modelul formal al sistemului

La momentul t, starea este S(t) = {M, X, O, Q, V}, unde M reprezintă geometria persistentă, X traiectoriile și transformările, O catalogul obiectelor, Q calitatea și incertitudinea, iar V versiunile și proveniența. Observația Z(t) include imagine, adâncime când există, intrinseci, transformări, timestamp și starea trackingului.

Actualizarea F nu este definită numai de algoritmul geometric: S(t+1) = F(S(t), Z(t), politica de resurse, contractul de consistență). În cazul unei observații incompatibile temporal sau geometric, F trebuie să o respingă ori să o trimită în carantină. Repararea implicită prin schimbarea scării, originii sau identității ar face rezultatul imposibil de auditat.

Costul de proiectare poate fi exprimat J = w₁E_geometrie + w₂E_identitate + w₃Latență + w₄Energie + w₅Risc. Ponderile nu sunt universale. Pentru proiectare de mobilier domină fidelitatea geometrică; pentru robot domină prospețimea observației și condițiile sigure de utilizare. Se preferă o frontieră de compromisuri măsurată, nu un singur scor care ascunde eșecurile.

## 1.7 Rezultatele pe care lucrarea le permite

După închiderea porții documentare se poate începe implementarea instrumentată, fără a reinventa rolurile, contractele sau criteriile. După pilot se pot revizui bugetele pe baza variației observate. După calificare se pot formula promisiuni limitate la dispozitivele și condițiile testate. Extinderea domeniului de utilizare reîncepe evaluarea relevantă și nu moștenește automat aprobarea profilului anterior.
