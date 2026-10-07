# Agenții logici din aplicație și robot

Agenții de mai jos sunt componente software propuse. Nu sunt obligatoriu LLM-uri și nu au fiecare un fir de sistem dedicat. Un scheduler limitează joburile grele; actorii Swift pot proteja starea, iar nodurile ROS au contracte de mesaje. Rolurile echipei de dezvoltare sunt definite separat în FISE_DE_POST.

| Agent logic | Intrare | Activitate | Ieșire și criteriu | La degradare |
|---|---|---|---|---|
| CaptureCoordinator | Sesiune și capabilități | Distribuie observații sincronizate | observation_id unic, timp, intrinseci și calibrare | Oprește fluxul nevalid și anunță consumatorii |
| QualityMonitor | Tracking, expunere, depth, termic | Evaluează utilizabilitatea și bugetul | Stare și motiv pentru fiecare observație | Cere recaptură sau reduce sarcina |
| Detector | Cadre informative și zone prioritare | Propune clase și regiuni | Detecții cu scor și proveniență | Reduce frecvența, nu inventează obiecte |
| Segmenter | Regiuni și imagine | Estimează contururi și măști | Mască legată de același observation_id | Returnează unavailable la lipsă de suport |
| PoseEstimator | Model, RGB/depth și ipoteze | Estimează SE3 și rafinează | Pose cu model/frame/timp și incertitudine | Ambiguu sau invalid, nu certitudine zero |
| MultiObjectTracker | Detecții și pose recente | Asociază observații și extrapolează limitat | ID de instanță, lifecycle și ambiguity_status | Predicted/lost cu expirare |
| MapIntegrator | Geometrie validă și transformări | Actualizează structura persistentă | Delte versionate cu add/update/delete | Păstrează ultima revizie coerentă |
| LocalObstacleProcessor | Depth recent și TF | Produce ocupare locală și spațiu observat | Obstacole cu age_at_use și calitate | Zona devine necunoscută când expiră |
| CatalogManager | Evenimente validate | Menține identități și modele | Catalog tranzacțional și istoric | Reconciliere explicită după reset |
| ResourceScheduler | Cozi, termic și priorități | Alocă bugete limitate și aruncă date vechi | Plan de execuție și metrici | Suspendă rafinarea înaintea capturii utile |
| PersistenceWorker | Salvări explicite și joburi | Confirmă durabilitatea și idempotența | Checkpoint plus manifest | Reia operațiile neconfirmate fără dubluri |
| RobotBridge | Pachete autentificate | Validează schemă, timp, epocă și convertește | Topicuri ROS propuse în contract | Respinge și resincronizează |
| HealthSupervisor | Heartbeat și date utile | Evaluează stările de disponibilitate | READY/DEGRADED/INVALID după contract | Aplică politica locală de robot |
| SemanticAssistant opțional | Catalog aprobat de utilizator | Descrie și caută semantic | Text cu sursele obiectelor | Nu modifică pose sau controlul robotului |

## Prioritizare

Ordinea inițială propusă este: sănătate și prospețime, captură și transformări, obstacole locale dacă modul robotic este activ, obiecte prioritare, descoperire, rafinare și export. Frecvențele din capitole sunt ținte pentru măsurare. O prioritate mare nu justifică monopolizarea GPU și nici anulare forțată nesuportată de API.

Lista de obiecte și zone definește relevanța, nu obligația de a lansa un model neuronal pentru fiecare obiect la fiecare cadru. Detecția comună, reutilizarea caracteristicilor și urmărirea locală reduc costul. Numărul de lucrători grei este un parametru testat pe dispozitiv; numărul de obiecte nu devine automat număr de fire.

## Contract comun

Fiecare rezultat poartă identificatori, timp de captură și finalizare, proveniență, versiune și stare de incertitudine. Rezultatul nu poate schimba o revizie nouă dacă a calculat pe una veche fără reconciliere. Agentul consumator verifică aceleași condiții chiar dacă producătorul le-a verificat deja, deoarece rezultatul poate expira în coadă.

Succesul runtime se măsoară prin latență, corectitudine și resurse din experimentele EX-06 până la EX-12. Niciun agent logic nu primește criteriul vag „să fie inteligent” sau „100% precis”.
