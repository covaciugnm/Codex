# Audit independent V2 — 2026-10-06

## Verdict: 10 / 10 pentru documentația de implementare

Pachetul îndeplinește toate cele zece criterii fixate în `auditor-preaudit.md`. Nu am constatări blocante deschise în documentația auditată. Recomand începerea implementării prin B01/R0, apoi corecțiile P0 și probele definite. Nota descrie completitudinea, coerența și verificabilitatea planului. Nu reprezintă certificarea performanței telefonului, a serverului sau a robotului și nu confirmă instalări ori teste hardware.

Rubrica nu a fost modificată pentru a obține nota. V1 a primit 5,5/10; lipsurile sale și observațiile suplimentare de revizie au fost corectate în V2. Licența comercială nu a fost criteriu de punctaj și nu a exclus opțiunile de cercetare, conform precizării utilizatorului.

## Identitatea exactă a pachetului

Am citit integral cele șapte documente și am reverificat pasajele modificate după comentariile de audit. Hash-urile următoare identifică octeții fișierelor locale înghețate. Publicarea în GitHub trebuie verificată față de acești octeți; o conversie de newline poate schimba hash-ul chiar fără schimbare semantică.

| Fișier | Octeți | SHA-256 |
|---|---:|---|
| PLAN_V2.md | 16561 | `DB8A63F1E97569B1D44D690FF5AE958877ECFA52D0D27F443B271B3F7870D1EF` |
| CONTRACTE_V2.md | 18691 | `76FA287FED75D54E411B2D5A8E1B73A8ABBB4F6F229B35C172A08EF261A72A7F` |
| EXECUTIE_TESTE_V2.md | 23302 | `17E05619D50161865AB200E028D007FBA030EB053149642A769628234B2F5D51` |
| 01-specialist-iphone-ios.md | 17202 | `A85649CC52F29552B36892DB69084ABB200266EED48473A0B79068D32BB6CBCF` |
| vision-robotics.md | 30065 | `2EB2C471C876F29016BC420F0B79FB0A743F949B68802686A234B97074E8234C` |
| 03-modele-voce-llm.md | 10605 | `CEDF087FC29E4E7F4AE3F970E2E2790C4BA1E50454A8CFFC567B4497131DBDF8` |
| 04-candidati-research.md | 6973 | `5757F5864F5D99D9E5D226FA4A24B42ED33146D4F200E374495711865761FE0F` |

PLAN_V1, audit-v1 și preaudit rămân documente istorice. Un eventual fișier final identic cu PLAN_V2 poate fi verificat prin același hash; dacă textul diferă, această aprobare nu se transferă automat modificării. Fișierele de index/publicare nu pot modifica prin rezumat semantica pachetului.

## Punctaj pe rubrica fixă

| ID | Scor | Dovezi și concluzie |
|---|---:|---|
| A1 Trasabilitate și actualitate | 1/1 | Data, commit-urile app/main și sursele sunt explicite. Documentele disting cod existent, propuneri, ipoteze și probe not_run. Precedența fișierelor rezolvă pragurile diferite din rapoartele inițiale. |
| A2 Hardware/iOS fezabil | 1/1 | Sunt tratate capture ownership, matrice runtime, montaj, camere, limitări MultiCam/background, termic, memorie, alimentare, iOS27/CoreAI/referenceobject/PCC și fallback. Nu se deduc RAM/fps din 1 TB. Compatibilitatea exactă este livrabil R0, nu rezultat inventat. |
| A3 Spațiu și timp | 1/1 | CONTRACTE definește SI, repere, sensul transformărilor, quaternion, conversie ARKit–optic, timpul capturii, clock mapping, epochs, incertitudine și invalidare. Ecuațiile, fixtures și testele T01/T04 fac verificabilă implementarea. |
| A4 Metode și evaluare | 1/1 | Matricele enumeră metode moderne și alternative cu surse, I/O, runtime, maturitate și condiții de activare. Baseline/challenger/combinații și regimurile buget egal/capacitate maximă evită superioritatea declarată fără date. Toate opțiunile research rămân eligibile tehnic. |
| A5 Memorie și multi-robot | 1/1 | ID-uri persistente, proveniență, map revision/epoch, ipoteze, server sequencer, assets atomice, snapshot/delta, tombstones, dedup și scenariul offline sunt definite. Alignment geometric, negative repetitive și evitarea dublei numărări sunt testate prin T02/T05/T08. |
| A6 Telefon–server–robot | 1/1 | Roluri și servicii, health/readiness, cozi, admission control, stocare, manifest, staging/canary și rollback sunt descrise. Dimensionarea se face aritmetic și apoi prin măsurare; parametrii necunoscuți au gate și owner. |
| A7 Integrare robotică | 1/1 | RobotProfile, URDF/XACRO/SRDF, TF, compatibilitate ROS, acțiuni tipate, anulare, precondiții și feedback sunt specificate. Watchdog/stop/echilibru rămân pe robot; motor enable cere probe distincte și toleranțe hardware. |
| A8 Persoane/voce/gesturi | 1/1 | STT, diarizare, speaker ID, fețe și asociere multimodală sunt separate; candidați RO/EN/TTS/embeddings concreți, fallback și versiuni de embeddings. T09–T11 includ negative, unknown/replay, zgomot și evaluare umană. |
| A9 Verificare și operare | 1/1 | T01–T15 au proceduri, ținte și artefacte; dataset/holdout, statistici, fault injection, soak și recovery sunt explicite. ACK local vs replicated și modelul de defect închid contradicția dintre RPO și zero pierderi. |
| A10 Roadmap și livrabile | 1/1 | B01–B17 au rol/dependență/livrabil/DoD; G0–G7 stabilesc ordinea. Testele unitare însoțesc corecțiile; calificarea completă C11/G6 nu mai blochează circular G1. Versiunile și auditurile se păstrează. |
| **Total** | **10/10** | **Zero constatări blocante documentare deschise.** |

## Închiderea constatărilor V1

- **AV1-01:** închis prin matricile specialiștilor, addendumurile 03/04 și comparația normativă. Nu se cere alegerea arbitrară a unui câștigător înainte de benchmark.
- **AV1-02:** închis prin CONTRACTE și T01/T04: schema conceptuală, ecuații, convenții, exemplu, invalidare și fixtures.
- **AV1-03:** închis prin protocolul de sincronizare, tranzacții și scenariul r01/r02, plus T02/T05/T08.
- **AV1-04:** închis prin verificarea noilor API-uri Apple și limitelor lor, împreună cu gates SDK/runtime.
- **AV1-05:** închis prin setul normativ T01–T15, precedență și distincția ținte pilot/toleranțe fizice.
- **AV1-06:** închis prin manifest, servicii, pașii staging/migrare/probe/canary/rollback și livrabilele runbook.
- **AV1-07:** închis prin RobotProfile, matrice ROS, task state machine, fencing și poarta simulator–robot.
- **AV1-08:** închis prin backlog, gates și trasabilitatea C→B→T.

## Observații suplimentare corectate înainte de înghețare

1. **Deduplicare:** același ID și conținut returnează ACK-ul inițial; același ID cu alt conținut este conflict. Dispare contradicția dintre retry idempotent și respingerea generică a duplicatelor.
2. **Partition și lease:** expirarea serverului nu dovedește oprirea fizică. Reatribuirea cere confirmare de stare stabilă sau fencing fizic verificabil; altfel resursa rămâne indisponibilă.
3. **Durabilitate:** ACK local garantează recuperare la crash cu disc intact; pierderea hostului poate avea RPO de cinci minute. ACK replicated cere confirmare într-un domeniu independent și este testat separat la pierderea unui domeniu.
4. **Ordinea etapelor:** G1 închide fundația și testele unitare asociate; C10 se califică G5 și C11 complet G6. Nu se amână întreaga infrastructură de teste până la final.
5. **Inventar ROS:** `ros2 doctor --report` poate include variabile de mediu. Runbook-ul cere allowlist și eliminarea valorilor sensibile înainte de arhivare; outputul brut nu se publică.

## Verificări primare independente

Am verificat prin surse primare, separat de rapoartele specialiștilor, punctele temporale cu impact mare:

- Modelul hardware și opțiunile relevante: [Apple specs](https://www.apple.com/iphone-18-pro/specs/).
- Limitele capturii și colaborării: [MultiCam hardwareCost](https://developer.apple.com/documentation/avfoundation/avcapturemulticamsession/hardwarecost), [ARKit collaboration](https://developer.apple.com/documentation/arkit/arworldtrackingconfiguration/iscollaborationenabled).
- Noul tracking de obiecte pe iOS și condițiile PCC: [referenceobject pe iOS](https://developer.apple.com/documentation/visionos/using-a-reference-object-with-arkit-in-ios), [PCC](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute), [iOS27/CoreAI](https://developer.apple.com/ios/whats-new/).
- Limita Vision 3D pentru persoana proeminentă: [Vision body poses](https://developer.apple.com/documentation/vision/identifying-3d-human-body-poses-in-images).
- Existența și cerințele selectate ale metodelor: [FoundationPose runtime](https://github.com/nvidia-isaac/foundation-pose-inference-library), [SAM3.1](https://github.com/facebookresearch/sam3), [VGGT-Omega](https://github.com/facebookresearch/vggt-omega), [GraspGenX](https://github.com/NVlabs/GraspGenX), [cuRoboV2](https://github.com/NVlabs/curobo), [YOLO26](https://github.com/ultralytics/yolo26).
- Checkpoint-uri concrete LLM/VLM și audio: [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B), [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), [Gemma4-31B-it](https://huggingface.co/google/gemma-4-31B-it), [Piper](https://github.com/OHF-Voice/piper1-gpl), [Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3), [pyannote community1](https://huggingface.co/pyannote/speaker-diarization-community-1).
- Actualitatea distribuției ROS și modificările documentate: [Lyrical Luth release](https://github.com/ros2/ros2_documentation/blob/rolling/source/Releases/Release-Lyrical-Luth.rst).

Aceasta este verificare documentară și eșantionare a afirmațiilor primare, nu reproducerea tuturor rezultatelor upstream sau auditarea fiecărei linii din dependențe. Problemele C01–C11 ale aplicației rămân constatări din analiza statică a commit-urilor indicate, fără reproducere runtime în acest audit.

## Ce rămâne de demonstrat în implementare

Inventarul serverului/robotului, disponibilitatea conturilor și modelelor, versiunile exacte descărcate, schemele generate, integrarea și benchmark-urile sunt livrabile explicite, nu goluri ascunse. Compatibilitatea simultană a camerelor, performanța termică, precizia metrică, identitatea persoanelor și succesul de manipulare rămân `not_run`. Metodele se promovează numai prin gates; niciuna nu a fost certificată drept cea mai capabilă pentru toate scenele.

Dosarul este pregătit pentru începutul implementării controlate. Activarea hardware și declararea performanțelor așteaptă dovezile cerute de același dosar.
