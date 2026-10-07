# 5. Concurență, latență, energie și contracte de execuție

**Statut:** proiect de implementare și evaluare; nicio frecvență nu reprezintă performanță deja demonstrată. Autor: agentul specialist Apple și percepție. Acest capitol definește agenții software ai fluxului de percepție. Ei sunt diferiți de agenții de dezvoltare și auditorii documentației.

## 5.1. Obiectivul optimizării

Scopul nu este folosirea simultană a tuturor firelor disponibile, ci obținerea informației utile înainte de expirarea ei, cu memorie și energie controlate. Putem avea o aplicație care procesează multe cadre pe secundă și totuși livrează rezultate vechi din cauza cozilor. Prin urmare măsurăm vârsta observației când este consumată, nu numai durata unei inferențe izolate.

Fie `t_capture` timpul capturii și `t_use` timpul în care rezultatul devine disponibil consumatorului. Latența capăt-la-capăt este `L = t_use − t_capture`, după conversia ceasurilor într-un reper comun. Dacă sincronizarea are incertitudine, raportul include această incertitudine. Diferența brută dintre două ceasuri de pe dispozitive diferite nu este o măsurare validă a latenței.

Numărul de obiecte din catalog și numărul de operații active sunt parametri independenți. Un catalog de o mie de obiecte poate avea numai cinci obiecte vizibile și două prioritare. Pornirea unui fir sau a unei inferențe grele pentru fiecare înregistrare ar consuma resurse fără informație nouă. „Agent per obiect” înseamnă în această arhitectură o stare logică și o politică, nu un proces complet ori un model lingvistic separat.

## 5.2. Flux unic și responsabilități

Se propune un producător de cadre și consumatori cu rate diferite. Datele sunt referite prin identificatori și proprietate controlată a bufferelor. Algoritmii nu modifică imaginea comună; rezultatele sunt mesaje separate. Transformările și versiunile sunt citite din același snapshot al cadrului.

| Agent software propus | Intrări | Responsabilitate | Ieșire și limită |
|---|---|---|---|
| CaptureCoordinator | Sesiune Apple, configurare | Produce pachete consistente și semnalează întreruperi | Cadru, adâncime, calibrare, timp; fără procesare grea în callback |
| DiscoveryWorker | Cadre selectate | Detectează obiecte noi și verifică zone neexplorate | Candidați; coadă cu ultimul cadru eligibil |
| PoseWorkerPool | Candidați, modele, adâncime | Estimează și rafinează poziții | Rezultate versionate; număr limitat de operații |
| TrackRegistry | Rezultate acceptate | Menține identități și stări temporale | Catalog consistent; fără acces GPU în secțiunea critică |
| MapIntegrator | Observații geometrice | Actualizează fragmentele și elimină contradicțiile | Revizii și evenimente de hartă |
| TransportWorker | Rezultate și revizii | Trimite date după politica fiecărui flux | Mesaje, confirmări, contoare de pierderi |
| Recorder | Evenimente eligibile | Persistă numai datele autorizate | Checkpointuri și jurnal recuperabil |
| HealthSupervisor | Timpi, memorie, temperatură | Modifică bugetul și declară degradarea | Stare de sănătate și decizii motivate |

Aceste denumiri sunt componente proiectate, nu clase existente în aplicație. Proprietatea fiecărei structuri mutable se atribuie explicit. Fuziunea hărții are un singur punct de publicare a reviziilor, pentru a evita rezultate incompatibile publicate de lucrători concurenți.

## 5.3. Swift Tasks, actors și fire reale

Swift permite organizarea lucrului în sarcini și grupuri de sarcini; execuția simultană efectivă este decisă de sistem. Actorii izolează starea mutable, iar anularea este cooperativă. [A19 — concurență Swift](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html) Această bază nu produce automat priorități de timp real ori preempțiune imediată a unui calcul GPU.

Propunem un actor pentru registrul de urmărire, unul pentru deciziile de programare și un serviciu separat de persistență. Calculele grele se execută în afara actorului de interfață. În interiorul actualizării unui registru, orice `await` este tratat ca punct în care starea poate deveni diferită înaintea continuării; după suspendare se revalidează revizia și epoca.

Un grup de sarcini așteaptă încheierea copiilor; cererea de anulare nu garantează că o operație externă s-a oprit imediat. [A20 — TaskGroup](https://docs.swift.org/latest/documentation/swift/taskgroup/) Din acest motiv, abandonarea rezultatului întârziat și oprirea calculului sunt două mecanisme diferite. Putem respinge rezultatul expirat chiar dacă accelerarea hardware își termină operația curentă.

Core ML oferă predicție asincronă și utilizare concurentă, dar câștigul depinde de model și de resursele utilizate. [A21 — integrarea Core ML asincronă](https://developer.apple.com/videos/play/wwdc2023/10049/) Arhitectura nu rezervă arbitrar o parte a Neural Engine fiecărui agent. Se compară limite de 1, 2 și 4 operații grele concurente pe fiecare configurație hardware; se alege varianta cu latență și energie mai bune în sarcina reală, chiar dacă are mai puține operații paralele.

## 5.4. Memorie limitată și eliminarea cadrelor învechite

Apple documentează că păstrarea prea îndelungată a bufferelor de captură poate provoca pierderea cadrelor și recomandă tratarea explicită a cadrelor întârziate în fluxurile AVFoundation. [A22 — TN2445](https://developer.apple.com/library/archive/technotes/tn2445/_index.html) Acest principiu inspiră proiectarea noastră; opțiunile concrete AVFoundation nu sunt presupuse automat disponibile în ARKit.

Contractul propus pentru fluxul live folosește o coadă de adâncime unu pentru așteptarea detecției și un set mic de buffere aflate efectiv în lucru. Sosirea unui cadru nou poate înlocui cadrul încă nepreluat. Nu înlocuiește un buffer deținut de GPU. Limita exactă a poolului se stabilește după măsurarea memoriei totale, incluzând texturi, adâncime, modele și copii introduse de framework.

Recorderul persistent are alt contract: dacă înregistrarea tuturor cadrelor este cerută explicit, nu putem pretinde simultan „fără pierderi” și „memorie fixă” în fața unui disc lent nelimitat. Se definește debitul susținut, o limită de coadă și o reacție vizibilă la depășire: scăderea ratei, pauză sau segment de înregistrare incomplet. Fiecare cadru pierdut primește motiv și interval temporal; numărătoarea nu dispare la export.

Un rezultat acceptabil conține `observation_id`, `frame_id`, `capture_time_ns`, `session_id`, `map_epoch`, `clock_epoch`, `map_revision`, `calibration_id`, `model_version` și `object_id`, dacă este aplicabil. Regula de publicare verifică epocile și compatibilitatea reviziilor. Un rezultat mai vechi nu rescrie starea curentă; poate intra într-o optimizare istorică explicită, care produce o revizie nouă, fără a falsifica timpul observației.

Tabelul următor este adaptorul canonic către contractul ROS din capitolul 07. Numele istorice locale sunt aliasuri de implementare, nu câmpuri concurente cu semantică diferită.

| Concept local | Câmp canonic de transport | Regulă |
|---|---|---|
| Numărul imaginii/cadrului | `observation_id` și `sequence` în flux | Unic prin device/session/stream/sequence; nu se pune în header.frame_id |
| Reper geometric | `frame_id` / ROS `header.frame_id` | Nume al reperului în care sunt coordonatele |
| `session_epoch` istoric | `(session_id,map_epoch,clock_epoch)` | Cheie compusă locală; toate componentele se transportă separat |
| Restart de proces | `session_id` nou | Nu implică automat hartă nouă dacă aceasta este recuperată și relocalizată |
| Resetarea originii/referinței spațiale | `map_epoch` nou | Nu se amestecă transformări fără aliniere explicită |
| Discontinuitatea ceasului | `clock_epoch` nou | Se invalidează modelul de conversie și se resincronizează |
| `calibration_revision` istoric | `calibration_id` | ID imutabil al manifestului de calibrare; orice schimbare produce ID nou |
| `model_revision` istoric | `model_version` plus hash în manifest | Leagă rezultatul de algoritm/greutăți exacte |
| `map_revision` | Revizie în interiorul `map_epoch` | Un număr egal în altă epocă nu indică aceeași hartă |
| `ambiguous` în interfață | `ambiguity_status` alături de `state` | `none/pose/identity/both`; starea observat/pierdut nu este distrusă |
| `archived` pentru obiect retras explicit | `state=retired` | Arhivarea simplă a unui fișier nu retrage obiectul |

Adaptorul refuză formatul care nu poate conserva aceste informații. Sunt propuse cinci probe APP-IF-01…05: restart cu hartă recuperată; resetare AR fără restart; salt de ceas fără schimbare de hartă; observații reordonate din două fluxuri cu același sequence; round-trip pentru obiect observat cu identitate ambiguă și pentru retragere explicită. Fiecare probă cere zero pierderi de câmpuri și zero confuzii între numărul observației și reperul ROS. Aceste probe sunt neexecutate până la implementare.

## 5.5. Programarea după utilitate și termen

Propunem trei clase de lucru: observații apropiate necesare mișcării; urmărirea obiectelor selectate; reconstrucție și arhivare care pot aștepta. Termenele se stabilesc din sarcina robotului, iar o operație cu termen ratat este raportată ca atare. O prioritate mare acordată de aplicație nu este garanție de timp de răspuns a sistemului de operare.

Un algoritm inițial de selecție poate ordona lucrul după urgență, vechimea ultimei observații și riscul incertitudinii. Se introduce însă și o perioadă maximă de reverificare pentru a evita înfometarea obiectelor cu prioritate mică. Într-un experiment, aceeași secvență este procesată cu ordonare FIFO, programare periodică și programare adaptivă. Beneficiul se măsoară prin latență P95/P99, rata termenelor ratate și rata de identificare corectă.

Frecvențele orientative pentru prototip sunt 30–60 Hz pentru poziția camerei când configurația permite, 10–30 Hz pentru obstacole recente, 5–20 Hz pentru obiectele prioritare și 1–5 Hz ori la schimbare pentru fragmentele de hartă. Nu sunt praguri de acceptare și nici suport uniform al tuturor iPhone-urilor. Disponibilitatea efectivă a cadrelor este măsurată și declarată separat de frecvența cerută.

## 5.6. Energie și degradare controlată

Monitorizarea include starea termică, bateria, conectarea alimentării, memorie, debit de rețea, latență și numărul de buffere. Alimentarea externă nu elimină încălzirea; poate modifica regimul termic. Carcasa robotului, poziția telefonului și ventilația fac parte din condițiile experimentului.

Ordinea propusă de reducere a sarcinii este: amânarea reconstrucției finale, reducerea frecvenței de descoperire globală, reducerea rezoluției inferenței și a numărului de obiecte prioritare, apoi suspendarea funcțiilor incompatibile cu bugetul rămas. Nicio reducere nu este tăcută: mesajul de sănătate indică profilul actual și funcțiile indisponibile. Modificarea profilului nu resetează contoarele, pentru a nu ascunde degradarea.

Pentru un flux către robot, termenul de expirare se transmite împreună cu observația. Robotul decide dacă o poate utiliza, ținând cont de viteza sa și de sarcină. Componenta telefonului nu declară independent că mersul este sigur. Echilibrul și controlul actuatoarelor rămân în subsistemul robotic dedicat.

## 5.7. Protocol de performanță reproductibil

Un raport complet declară dispozitivul, OS, buildul aplicației, modelul ML și hashul, rezoluțiile, numărul de obiecte, dimensiunea hărții, profilul energetic, temperatura ambientală și modalitatea de alimentare. Se separă pornirea rece, încălzirea modelului și regimul susținut. Măsurarea numai după eliminarea cadrelor dificile nu este admisă.

| Sarcină | Experiment propus | Criteriu documentar și ieșire |
|---|---|---|
| PERF-01 | 1/2/4 lucrători pe aceeași secvență | Tabel comparabil cu latență P50/P95/P99, memorie și energie |
| PERF-02 | 30 minute pentru fiecare profil inițial selectat | Curbe temporale, opriri, schimbări termice; zero intervale omise |
| PERF-03 | Consumator intenționat lent și rafale de cadre | Limita cozilor respectată și pierderi explicate |
| PERF-04 | Rezultate sosite invers, anulări și resetări | Zero aplicări ale rezultatelor din epoci incompatibile |
| PERF-05 | Întrerupere la salvare și reluare | Artefacte confirmate intacte; pierderea eligibilă măsurată canonic |
| PERF-06 | Rețea lentă, întreruptă și reconectată | Vârsta datelor, resincronizare și marcarea fluxului expirat |

Cele 30 de minute sunt durata inițială propusă pentru experimentele susținute ale acestui capitol, nu garanție de operare nelimitată. Durata finală de calificare se stabilește după cazul de utilizare. Înaintea unei campanii se publică protocolul și condițiile de oprire; schimbarea parametrilor produce o versiune nouă, fără înlocuirea rezultatelor vechi.

## 5.8. Jurnalizare și recuperarea lucrului

Fiecare operație persistentă are `task_id`, intrări cu hash, versiune de algoritm, stare, progres confirmat, ieșiri și următoarea acțiune. Stările propuse sunt `queued`, `running`, `checkpointed`, `completed`, `failed`, `cancelled` și `needs_recapture`. `completed` este publicat numai după verificarea ieșirilor și confirmarea scrierii durabile conform contractului de stocare.

Jurnalul operațional include evenimentele de început, schimbare de stare, checkpoint, eroare și încheiere. Nu presupunem că fiecare instrucțiune poate fi jurnalizată fără cost. Se definește granularitatea astfel încât ultima etapă confirmată să poată fi identificată, iar o operație întreruptă să fie reexecutabilă fără dublarea rezultatelor. Idempotenta este verificată prin injectarea aceleiași cereri de două ori.

După repornire, sistemul validează manifestul, integritatea artefactelor și versiunile necesare. Lucrul cu stare `running` fără proces activ devine de recuperat, nu este prezentat ca reușit. Un nou model ML sau o nouă calibrare nu continuă transparent o etapă care presupunea versiunea veche. Se păstrează legătura dintre rezultat și configurația exactă utilizată.

Auditorul de performanță acceptă planul doar dacă există limite de coadă, politici de expirare, condiții termice și probe de suprasarcină explicite. Auditorul de fiabilitate verifică separat salvarea și reluarea. Acceptarea documentului confirmă că aceste verificări sunt definite; rezultatele lor rămân neexecutate până la existența implementării și a echipamentelor.
