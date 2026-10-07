# Preaudit independent — 2026-10-06

Obiect: calitatea planului de implementare EVA-3DScan pentru iPhone, humanoid, server și colaborare între roboți. Acest document fixează rubrica înainte de auditarea rezultatului. Nu certifică produsul sau performanța hardware. Nu s-au instalat pachete și nu s-au executat teste pe telefon/robot.

## Rubrică fixă: 10 criterii × 1 punct

Fiecare criteriu primește 0, 0,5 sau 1 punct. 1 înseamnă complet și verificabil pentru un plan; 0,5 înseamnă prezent dar cu lacune concrete; 0 înseamnă absent/contradictoriu. Pentru 10/10 trebuie 1 la toate criteriile și zero constatări blocante deschise. O constatare blocantă împiedică declarația de pregătire indiferent de suma numerică. Scopul este obținerea unui plan pregătit de implementare, nu obținerea obligatorie a unei note prin schimbarea rubricii.

| ID | Criteriu | Dovezi cerute pentru 1 punct |
|---|---|---|
| A1 | Trasabilitate și actualitate | Dată 2026-10-06, branch/commit de bază, surse primare pentru afirmațiile temporale, separarea existent/propunere/experiment. |
| A2 | Hardware/iOS fezabil | API-uri și availability reale, matrice captură, limite simultaneitate/background/termic/memorie, strategii fallback; fără inferarea RAM/performanței din 1 TB stocare. |
| A3 | Corectitudine spațiu și timp | Frames/axe/unități, timestamp captură, sincronizare, calibrare, map/session epochs, covarianță/validitate, recovery, teste cu rezultate așteptate. |
| A4 | Selecție metode și evaluare | Metode actuale comparate cu baseline, runtime țintă, intrări/ieșiri, licențe și greutăți, benchmark de promovare; nicio afirmație de superioritate absolută fără probe. |
| A5 | Memorie și multi-robot | ID-uri și proveniență, aliniere hărți, conflicte, versiuni, offline/reconectare, deduplicare, coerență obiecte-hartă, teste cu cel puțin doi roboți. |
| A6 | Împărțire telefon–server–robot | Responsabilități, servicii/interfețe, resurse de măsurat, instalare etapizată și reproducibilă, limite rețea și degradare independentă de server. |
| A7 | Integrare robotică executabilă | Profil URDF/XACRO/SRDF, kinematic TF, gateway ROS2, navigation/manipulation, comenzi structurate, validare și watchdog/oprire pe controler robot. |
| A8 | Persoane, voce și gesturi | STT/TTS, diarizare vs identificare, identitate multimodală, incertitudine, limbi/fallback, seturi de teste, date biometrice și retenție configurabilă. |
| A9 | Verificare și operare | Replay, teste negative, criterii numerice marcate ca ținte, observabilitate, soak, recuperare, rollback și evidențe cerute înainte de activare. |
| A10 | Roadmap și livrabile | Priorități/dependențe/roluri, pași reproductibili, intrări necunoscute cu responsabili/gates, Definition of Done, versiuni și audituri arhivate exact. |

## Constatări factuale independente

La data auditului, pagina oficială Apple confirmă modelul iPhone 18 Pro Max, opțiunea 1 TB, A20 Pro, LiDAR și USB 3 până la 10 Gb/s. Acestea nu dovedesc debitul disponibil aplicației sau performanța susținută a mai multor modele ML. Sursa: [Apple technical specifications](https://www.apple.com/iphone-18-pro/specs/). Lansarea publicată de Apple este 9 septembrie 2026: [Apple Newsroom](https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/).

ARKit collaboration transportă informații despre suprafețe, poziții și anchors. Apple recomandă practic până la patru participanți pentru rezultate bune și avertizează că deserializarea datelor între versiuni iOS diferite poate eșua. Nu echivalează cu baza de date semantică persistentă sau cu un protocol general de fuziune ROS. Sursa: [isCollaborationEnabled](https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration/iscollaborationenabled).

MultiCam trebuie evaluat pe configurația reală: hardwareCost > 1 împiedică pornirea; costul de presiune și sarcina aplicației cer degradare adaptivă. Sursa: [hardwareCost](https://developer.apple.com/documentation/avfoundation/avcapturemulticamsession/hardwarecost), [systemPressureCost](https://developer.apple.com/documentation/avfoundation/avcapturemulticamsession/systempressurecost). Aceste API-uri nu demonstrează automat compatibilitatea între orice configurație ARKit și orice sesiune AVFoundation.

Foundation Models actual include în iOS 27 opțiuni Private Cloud Compute și furnizori de modele, nu doar modelul local. Disponibilitatea, entitlement-ul și limita contextului trebuie verificate pentru backend-ul ales; nu se generalizează limita locală la toate modelele. Surse: [Foundation Models](https://developer.apple.com/documentation/FoundationModels), [WWDC26](https://developer.apple.com/videos/play/wwdc2026/241/), [generating content](https://developer.apple.com/documentation/FoundationModels/generating-content-and-performing-tasks-with-foundation-models).

Articolul PCC precizează iOS 27, context 32K, entitlement administrat, disponibilitate și cote zilnice. Acesta este o opțiune condiționată, nu un serviciu nelimitat sau disponibil offline: [PCC integration](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute). Unele pagini simbol păstrează marcaj Beta; versiunea SDK și funcționarea pe build-ul final trebuie confirmate înainte de promovare.

Documentația nouă Apple descrie `.referenceobject` pentru iOS, cu `trackingObjects` pentru obiecte mobile și `detectionObjects` pentru cele predominant statice, maximum zece fișiere însumate și fără amestec cu vechiul `.arobject`. Trebuie evaluată alături de metodele server-side; o afirmație că ARKit iOS oferă exclusiv vechea detecție statică este depășită: [Using a reference object with ARKit in iOS](https://developer.apple.com/documentation/visionos/using-a-reference-object-with-arkit-in-ios).

## Riscuri care trebuie închise în plan

1. Blocante înainte de mișcare: reper world etichetat camera, timestamp emis în loc de captură, restart fără map epoch și fără invalidarea rezultatelor vechi.
2. Blocante pentru memorie: lipsă relocalizare poate compara coordonate din origini diferite; lipsă observație nu dovedește obiect lipsă; cursor client-time poate pierde uploaduri offline târzii.
3. 6D: quaternion implicit și dimensiuni estimate nu sunt măsurători complete; starea validității și incertitudinii trebuie expusă robotului.
4. Multi-robot: aceeași cameră fizică nu înseamnă același reper; fuziunea necesită transformare verificată și incertitudine, control de proveniență și evitarea numărării duble a aceleiași dovezi.
5. Nicio metodă de cercetare, scor public sau demonstrație vizuală nu justifică numirea ei „cea mai bună” pe acest ansamblu fără benchmark local, licență și buget de resurse.
6. Instalațiile pe server/telefon sunt o etapă ulterioară explicită, cu inventar hardware/OS/conturi și rollback; documentarea unei instalări nu trebuie raportată ca instalare efectuată.

## Procedura auditului final

Auditorul citește fișierele concrete, înregistrează numele și hash-ul SHA-256 al fiecăruia, notează criteriile și constatări cu severitate/loc/corecție. Fiecare re-audit citește versiunea corectată și păstrează raportul anterior. Raportul final precizează exact ce a fost auditat, ce a fost verificat primar și ce rămâne test de implementare. Un 10/10 posibil descrie exclusiv completitudinea și coerența documentației pentru implementare.
