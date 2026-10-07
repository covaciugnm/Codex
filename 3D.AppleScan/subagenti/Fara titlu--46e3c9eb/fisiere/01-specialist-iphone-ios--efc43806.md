# Raport specialist iPhone/iOS — 2026-10-06

Scop: plan pentru EVA 3DScan, telefonul ca senzor, memorie locală și coordonator al unui humanoid. Cercetare de documentație primară consultată la 6 octombrie 2026. Nu s-a instalat software, nu s-a compilat proiectul și nu s-a verificat telefonul fizic. „Verificat” înseamnă confirmat în sursa citată; performanțele și compatibilitatea simultană sunt de demonstrat prin implementare.

## 1. Hardware și API-uri actuale

Apple confirmă iPhone 18 Pro Max, varianta 1 TB, A20 Pro, iOS 27, camere posterioare 48 MP, camera frontală Center Stage 18 MP cu TrueDepth, LiDAR, giroscop și accelerometru. Pagina listează USB 3 până la 10 Gb/s, Wi-Fi 7 și UWB. Cei 1 TB reprezintă stocare, nu RAM sau memorie disponibilă procesului. Nu fixăm RAM ori un buget ANE din afirmații neconfirmate. [Specificații Apple](https://www.apple.com/iphone-18-pro/specs/).

Decizie: construim manifest de capabilități la runtime, cu model, versiune iOS/build, formate de captură, rezoluții/frecvențe, disponibilitate sceneDepth/sceneReconstruction/faceTracking, localizări STT/TTS/LLM și memorie disponibilă. Manifestul devine parte din fiecare raport de test și handshake cu serverul.

Noutăți importante față de un plan bazat doar pe iOS 26:

- iOS 27 introduce Core AI pentru modele proprii, cu execuție locală, controlul memoriei și trasee fără copiere. Foundation Models adaugă input multimodal și abstractizarea providerilor. Evaluăm aceste trasee, fără rescrierea automată a modelelor Core ML care funcționează. [Ghid Apple iOS 27](https://developer.apple.com/wwdc26/guides/ios/).
- ARKit aduce în iOS urmărirea obiectelor de referință antrenate: `detectionObjects` pentru obiecte în principal staționare și `trackingObjects` pentru obiecte mobile. Apple documentează accesul la poziții metrice și reutilizarea referințelor între iOS și visionOS. Acesta este un candidat de prim rang pentru obiectele cunoscute ale robotului, de comparat cu estimatoare externe 6DoF. [WWDC26 object tracking](https://developer.apple.com/videos/play/wwdc2026/283/).
- Toolkit-ul Foundation Models adapter **26.0.0 este explicit incompatibil cu iOS 27 și ulterior**. Nu îl selectăm pentru acest telefon. [Avertisment Apple](https://developer.apple.com/apple-intelligence/foundation-models-adapter/).

## 2. Captură unică și distribuirea senzorilor

Propunere de arhitectură: `SensorCoordinator` deține un ARSession principal și distribuie cadrele către module independente. FrameBundle trebuie să cuprindă `frameID`, `captureTime`, `clockEpoch`, RGB, intrinseci, rezoluție, transformarea camerei, sceneDepth, confidenceMap, calibrare și starea tracking-ului. Toate rezultatele derivate rețin identificarea cadrului original. Se reutilizează CVPixelBuffer/Metal textures; se limitează numărul cadrelor reținute și se evită conversiile JPEG pentru inferența locală.

Consumatori: urmărire/world model, detector/segmentator, fețe, mâini/corp, OCR/barcode, recorder și expeditor server. Cozi independente bounded/latest-only pentru date live; exportul și reconstrucția operează pe joburi persistente. Un consumator lent nu blochează captura. ARSession gestionează împreună senzorii de mișcare și camera; date IMU suplimentare Core Motion se publică doar cu timestamp-ul lor, fără inventarea unei corespondențe cu timpul trimiterii. [ARSession](https://developer.apple.com/documentation/arkit/arsession/).

Pentru RoomPlan se furnizează același ARSession. Capturile mai multor camere se reunesc cu StructureBuilder numai după confirmarea unui reper comun continuu sau relocalizat. [Multiroom și ARSession comun](https://developer.apple.com/documentation/roomplan/scanning-the-rooms-of-a-single-structure).

Nu presupunem acces simultan nelimitat la toate camerele:

- ARKit are configurație pentru world tracking plus user face tracking frontal; se verifică `supportsUserFaceTracking`. Aceasta nu demonstrează disponibilitatea tuturor fluxurilor RGB/depth brute. [Apple](https://developer.apple.com/documentation/arkit/combining-user-face-tracking-and-world-tracking).
- Pentru AVCaptureMultiCamSession se verifică `isMultiCamSupported`, seturile de dispozitive, formatele compatibile și costul configurației. Cost hardware >1 împiedică pornirea; system pressure >1 nu este sustenabil. [Seturi compatibile](https://developer.apple.com/documentation/avfoundation/avcapturedevice/discoverysession/supportedmulticamdevicesets), [hardwareCost](https://developer.apple.com/documentation/avfoundation/avcapturemulticamsession/hardwarecost), [systemPressureCost](https://developer.apple.com/documentation/avfoundation/avcapturemulticamsession/systempressurecost).
- Prototipul trebuie să testeze explicit coexistarea configurației ARKit alese cu orice sesiune AVFoundation suplimentară. Dacă nu este suportată, alternăm moduri sau adăugăm o cameră pe calculatorul robotului. Nu prezentăm alternarea drept observație simultană.
- Orientarea mecanică se decide înaintea suportului fizic: LiDAR este posterior. Dacă spatele telefonului privește înainte, ecranul și TrueDepth privesc înapoi. Camerele integrate sunt rigide între ele. Pan/tilt rotește telefonul întreg. O hartă panoramică acumulată nu oferă observație instantanee 360°.

## 3. Poziționare și 6DoF

Primar pe telefon: VIO ARKit, depth cu confidence gating, mesh local și RoomPlan pentru structura semantică. `sceneDepth` este baza propusă pentru obstacole dinamice; `smoothedSceneDepth` pentru vizualizare/fuziune statică, deoarece Apple îl definește ca mediere temporală. Această alegere trebuie verificată pentru întârziere și suprafețe mobile. [Scene depth netezit](https://developer.apple.com/documentation/arkit/arframe/smoothedscenedepth), [ARDepthData](https://developer.apple.com/documentation/arkit/ardepthdata).

Obiecte cunoscute: antrenare Create ML din model 3D/fotogrammetrie, ARKit reference object iOS27, benchmark 6DoF față de marker rigid și sistem de măsurare independent. Obiecte necunoscute: detector + mască pe instanță + depth robust în interiorul măștii + observații multiple; bounding box 2D cu adâncime centrală nu dovedește orientarea completă. Simetria trebuie reprezentată, iar orientarea necunoscută nu se transmite ca identitate sigură.

Limită documentată: maximum 10 fișiere `.referenceobject` cumulat în `detectionObjects` și `trackingObjects`, fără amestec `.arobject` vechi cu `.referenceobject` în aceeași sesiune. Urmărirea mobilă per-frame crește consumul. Propun catalog mare pe server, cu selectarea unui set activ mic în funcție de cameră și sarcină; schimbarea setului trebuie testată pentru continuitate. [Referințe ARKit pe iOS](https://developer.apple.com/documentation/visionos/using-a-reference-object-with-arkit-in-ios).

Pentru flotă: ARKit CollaborationData este un mecanism de aliniere locală între telefoane. Datele critical se transportă fiabil; optional pot folosi livrare nefiabilă. Acest schimb nu este o bază de date semantică și nu elimină serviciul central de hărți, obiecte și revizii. [Colaborare ARKit](https://developer.apple.com/documentation/arkit/creating-a-collaborative-session).

Apple recomandă colaborarea pentru cel mult patru participanți pentru cele mai bune rezultate. Pentru flotă mai mare, proiectăm grupuri locale și reconciliere server. Serializarea opacă impune teste de compatibilitate între versiunile iOS și fallback prin observații/metadate proprii, fără presupunerea decodării universale. [Limitele colaborării](https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration/iscollaborationenabled).

UWB/Nearby Interaction oferă măsurători relative de distanță și direcție, utile ca observații auxiliare între roboți. Nu oferă singur toate cele șase grade de libertate. Necesită parteneri compatibili, capabilități runtime și gestionarea indisponibilității. [Nearby Interaction](https://developer.apple.com/documentation/NearbyInteraction).

Serverul menține graful reperelor globale și reviziile; telefonul operează în propriul `local_world`. Mesajele includ `robot_id`, `session_id`, `map_id`, `map_epoch`, `calibration_id`, `capture_time`, `frame_id`, transformări și incertitudine. Rescrierea alinierii globale nu modifică retroactiv observațiile brute. Acestea sunt propuneri de implementare, nu API-uri Apple existente.

## 4. Inteligență pe telefon și pe server

Primar: păstrarea detectorului curent drept baseline; comparație cu modele compacte recente selectate de echipa vision, convertite în Core ML și/sau Core AI. Core AI primește `.aimodel`; Apple publică rețete Python și utilitare Swift în `coreai-models`. Integrarea documentată necesită Xcode 27/iOS 27. [Integrarea Core AI](https://developer.apple.com/documentation/CoreAI/integrating-on-device-ai-models-in-your-app-with-core-ai), [model în Foundation Models](https://developer.apple.com/documentation/foundationmodels/running-a-core-ai-model-in-a-foundation-models-session), [repo Apple](https://github.com/apple/coreai-models).

Criterii de selecție: precizie pe date EVA, latență p95/p99 în sarcină mixtă, memorie de vârf, consum/temperatură, operatori exportabili, licența codului și a greutăților. Un model mai nou nu primește automat prioritate. Rulăm temporar două metode pe cadrele de test sau în shadow mode pentru a măsura dezacordul; în producție păstrăm simultan numai ce aduce un câștig demonstrat.

Telefon: percepție cu reacție rapidă, VAD/STT/TTS, cache spațial, gesturi, identități locale, funcționare de bază fără rețea. Server: modele mari de viziune/limbaj, fuziune multirobot, reconstrucție și reidentificare costisitoare, antrenare/conversie modele, evaluare și distribuire de artefacte. Serverul răspunde cu observation/frame IDs și timpul capturii; un rezultat întârziat nu comandă mișcări ca și când ar fi actual.

LLM: Foundation Models local ca candidat pentru intenții, răspunsuri scurte și apeluri structurate. Se verifică disponibilitatea, limbile și erorile; suportul românei nu se presupune din limba interfeței iOS. Alternativă: model propriu exportat prin Core AI, apoi endpoint server pentru sarcini grele. Comenzile robotice trec prin executor determinist cu precondiții, limitări, progres și verificarea rezultatului. [Limbile Foundation Models](https://developer.apple.com/documentation/foundationmodels/supporting-languages-and-locales-with-foundation-models).

O a patra opțiune verificată este Private Cloud Compute prin Foundation Models pe iOS27: modelul PCC are context 32K în documentația actuală, necesită entitlement gestionat/eligibilitate și conexiune, plus cote zilnice. Îl includem în benchmark după obținerea accesului, cu fallback pentru indisponibilitate și quota reached. Nu îl tratăm ca infrastructură proprie de flotă sau dependență obligatorie pentru funcționarea robotului. [PCC în Foundation Models](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute).

## 5. Voce, identitate, gesturi

STT: SpeechAnalyzer + SpeechTranscriber + AssetInventory reprezintă traseul Apple de evaluat. Enumerăm `supportedLocales`/`installedLocales` pentru română și limbile cerute; lipsa suportului activează fallback. Menținem SFSpeechRecognizer numai cu politica on-device aplicată explicit dacă aceasta este cerută. [SpeechTranscriber](https://developer.apple.com/documentation/speech/speechtranscriber), [SpeechAnalyzer](https://developer.apple.com/documentation/Speech/SpeechAnalyzer).

Alternativă concretă de benchmark: FluidAudio (Swift/Core ML) oferă ASR Parakeet, VAD, diarizare, embeddings pentru identificarea vorbitorului și opțiuni TTS. AEC/denoise este prezentat ca beta. WhisperKit se redirecționează acum la `argmax-oss-swift`; pinning-ul se face pe repo/versiune actuală. Nici scorurile publicate de autori, nici suportul unui model nu demonstrează performanța românei în zgomotul robotului. [FluidAudio](https://github.com/FluidInference/FluidAudio), [Argmax](https://github.com/argmaxinc/argmax-oss-swift).

Implementare audio propusă: un singur AVAudioSession/AVAudioEngine, ring buffer timestamped, VAD, STT, diarizare și speaker embeddings, plus TTS cu referință pentru anularea ecoului și barge-in. Se separă „ce s-a spus”, „cine vorbește în acel interval” și „identitatea persoanei”. Asocierea față–voce folosește timp, urmărire vizuală și scor de ambiguitate, nu simpla prezență a unei fețe. O înregistrare redată din difuzor trebuie tratată în teste ca atac/replay, fără presupunerea că embeddingul dovedește persoană vie.

Fețe: Vision pentru detectare/landmarks plus model de embeddings evaluat; enrollment propriu, versiune model, prag open-set și necunoscut. Baza biometrică Face ID nu este disponibilă aplicației. [Apple Face ID](https://support.apple.com/en-ca/102381).

Gesturi: Vision hand/body pose plus clasificator temporal și proiecția direcției de indicare în scena 3D. Vision 3D body pose documentează o singură persoană proeminentă și poate folosi înălțime de referință dacă lipsește depth adecvat; nu îl prezentăm ca detector metric multi-person garantat. Pentru mai multe persoane: detectare/tracking pe instanțe și evaluarea unui model separat. [Vision 3D body](https://developer.apple.com/documentation/vision/identifying-3d-human-body-poses-in-images).

## 6. Continuitate și limite operaționale

Aplicația trebuie să trateze background/lock, apeluri, întreruperi audio, presiune termică și schimbarea rețelei. Documentația AVFoundation indică întreruperea camerei când aplicația trece în background. Modurile de background nu sunt o promisiune de captură robotică nelimitată cu ecranul blocat. [Camera în background](https://developer.apple.com/documentation/avfoundation/avcapturesession/interruptionreason/videodevicenotavailableinbackground).

Propun mod dedicat foreground, luminozitate redusă, menținere controlată a ecranului activ și watchdog pe calculatorul robotului. Alimentarea prin USB și răcirea se testează în montura finală; cablul/hub-ul trebuie să susțină simultan alimentarea și traseul de date ales. USB 10 Gb/s este plafonul portului, nu debitul aplicației garantat. Legătura telefon–robot prin Ethernet/USB se validează practic, nu se deduce automat din existența USB-C.

Trei profile propuse: navigare (prioritate VIO/depth), inspecție (prioritate rezoluție/6DoF), conversație (prioritate audio). Reducerea adaptivă a inferențelor secundare la încălzire trebuie să lase o stare explicită de capabilitate redusă. Jurnalele au cote, compresie, încărcare reluabilă și retenție; nu umplem automat 1 TB cu fluxuri brute.

## 7. Pași de implementare și probe de acceptare

1. Inventar pe dispozitiv + build Xcode27: manifest complet și exemple minime pentru fiecare combinație de camere/API. Livrabil: tabel suportat/nesuportat și raport termic; fără performanțe inventate.
2. SensorCoordinator + schema FrameBundle: replay determinist, cadru RGB/depth/pose identificabil, fără timestamp de procesare substituit capturii și fără rezultate din sesiuni expirate.
3. Poziționare și obiecte: teste staționar, cap rotit, occludere, lumină slabă, suprafețe lucioase, obiecte simetrice și două instanțe identice. Eroarea poziției/orientării se măsoară față de referință independentă; pragurile finale derivă din gripper, gabarit și distanța de oprire ale robotului.
4. Bake-off Core ML/Core AI/ARKit object tracking și audio: aceleași date și seed/config, median/p95/p99, RAM maxim, drift, WER română, diarization error, false accept/reject identități, succes de task și procent de fallback. Publicăm atât eșecurile, cât și câștigurile.
5. Test 2 telefoane în aceeași cameră: aliniere verificată, aceeași identitate obiect, schimb offline și reconciliere; un telefon mută originea/repornește fără să corupă harta celuilalt. Extindere ulterior la numărul țintă de roboți.
6. Soak test propus: minimum 2 ore în montura alimentată, cu sarcini mixte și condiții termice reprezentative; 30 cicluri background/foreground și pierdere/revenire rețea; verificăm recuperarea și jurnalizarea. Aceste numere sunt praguri inițiale de proiect, nu garanții Apple.
7. Distribuție: manifest de modele cu URL/revizie/hash, licență, format, dimensiune, versiune minimă iOS, metrici și rollback; semnătură/verificare înainte de activare. CI pe Mac și test hardware obligatoriu înainte de promovarea unui model.

Auditul poate acorda 10/10 completitudinii planului dacă toate deciziile și probele sunt trasabile. Nu poate certifica 10/10 performanța robotului înainte de măsurători pe hardware. Nu există o metodă demonstrabil „maximă” pentru orice scenă; planul trebuie să păstreze comparația continuă și înlocuirea controlată a metodelor.
