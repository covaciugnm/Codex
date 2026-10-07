# Conducere, echipă și reluarea lucrului

## Organizarea efectivă

În această etapă lucrează managerul/cercetătorul principal și trei agenți specialiști: Apple/percepție, robotică și metrologie/CAD. Limita sesiunii este de patru agenți simultan, inclusiv managerul. Rolurile de mai jos reprezintă specializări și responsabilități ale proiectului, nu persoane angajate sau calificări profesionale certificate. Un agent poate prelua pe rând mai multe roluri, păstrând separarea autorului de auditor pentru același livrabil.

Managerul efectuează sinteza cercetării, fixează scopul, arbitrează conflictele dintre contracte și păstrează registrul. Specialiștii scriu proiectul și probele. Auditorul de metrologie verifică cercetarea și robotica; specialistul de robotică verifică metrologia; managerul verifică iOS/date. Modificările cerute de audit sunt aplicate de autor, apoi reverificate. Acceptarea documentară cere închiderea tuturor constatărilor blocante și a criteriilor stabilite; nu echivalează cu acuratețe fizică perfectă.

## Fișe de rol pentru implementare

| Rol | Misiune și activități | Rezultat cuantificabil | Auditor și drept de blocare |
|---|---|---|---|
| Manager tehnic | Plan, dependențe, alocare, control schimbări | Fiecare sarcină are owner, intrări, ieșiri, criteriu și pas următor | Auditor de sistem verifică registrul și dovezile |
| Cercetător CV | Comparații, ablații, ipoteze falsificabile | Un raport reproducibil pentru fiecare candidat; set de evaluare separat | Metrolog verifică referințele și concluziile |
| Inginer iOS/Apple | Capture coordinator, capabilități, SwiftUI, ciclul de viață | Build pe SDK fixat; zero acces concurent necontrolat la cameră în testele definite | Inginer QA iOS poate bloca release-ul |
| Inginer viziune 6D | Marker, corespondențe, PnP, rafinare, simetrie | Erori translație/rotație și rată de pierdere pe fiecare profil | Cercetător CV independent de implementarea evaluată |
| Inginer mapare | Keyframe-uri, subhărți, fuziune, loop closure | Raport deriva/acoperire/timp și ablație pentru fuziune | Metrolog și robotician |
| Inginer ROS/robotică | Repere, URDF, timestamp-uri, consumatori | Toate lanțurile TF testate; datele expirate respinse în fault injection | Auditor de sistem robotic |
| Inginer Thor/GPU | Build reproducibil, profiling, memorie, termic | P50/P95/P99 și memorie/consum pentru fiecare profil ales | Inginer performanță independent |
| Inginer hardware/calibrare | Montaj, extrinseci, sincronizare, vibrație | Raport cu incertitudine și revalidare după remontare | Metrolog |
| Specialist CAD/imprimare | Export semantic, unități, mesh, verificări slicer | Fixtures importate în aplicațiile țintă; diferențe dimensionale în toleranța definită | Proiectant CAD independent |
| Metrolog/statistician | Referințe, domenii, eșantion, intervale de încredere | Fiecare afirmație metrică are populație, numitor și incertitudine | Auditor științific |
| UX/accesibilitate | Fluxuri pentru arhitect, designer, meșter și utilizator general | Succesul sarcinilor, erori și timpi observați în studiul de utilizare | Cercetător UX care nu a proiectat fluxul |
| Inginer date/securitate | Retenție, CAS, tranzacții, pairing, importuri | Zero date persistente neautorizate în testele live; respingere importuri invalide | Auditor securitate/date |
| QA/fiabilitate | Replay, întreruperi, regresii, CI | Rezultate nominale și negative cu versiuni și artefacte | Auditor de release |
| Auditor de release | Dovezi, licențe, defecte, limitări publicate | Nicio cerință declarată îndeplinită fără rezultat verificabil | Managerul poate retrimite, nu suprascrie constatarea |

Într-o implementare reală, rolurile cu validare fizică sau juridică cer persoane competente desemnate. Agenții pot pregăti codul, analiza și documentația; nu semnează certificări profesionale inexistente.

## Planul executabil și rezultatele așteptate

| Etapă | Obiectiv / activități | Rezultat și poartă | Reluare |
|---|---|---|---|
| P00 Inventar | Identifică telefonul, OS, Thor/carrier, accesorii, Xcode și referințele | 100% câmpuri obligatorii ale profilului completate; tuple software fixat | Completează numai câmpurile lipsă, verifică hash profil |
| P01 Contracte și replay | Implementează validatori, epoci, timestamp-uri, deduplicare | Probe pozitive/negative și corpus versionat; fără acceptarea datelor vechi | Reia de la testul nereușit, păstrează seed/input |
| P02 Captură iOS | Implementează moduri exclusive și buffere limitate | Build pe telefon, preflight și raport de sesiune 30 minute | Ultimul build și profil; datele live nepersistente se recapturează |
| P03 Calibrare | Măsoară scară, intrinseci/crop, extrinseci și ceas | Referințe independente, incertitudine și domeniu documentate | Se reia subprocedura invalidată; nu se reutilizează calibrare după remontare |
| P04 Obiect metric | Captură ghidată, reconstrucție, verificare dimensiuni | Pilotul și ulterior calificarea profilului obiecte | Joburi idempotente pe aceeași revizie și parametri |
| P05 Live/camere | Măsurare fără salvare, camere și unire | Pilot pe scenarii canonice; control de scară și derivă | Camere finalizate persistă; sesiunea activă poate necesita relocalizare |
| P06 Poziție 6D | Trei obiecte cu reper, apoi catalog fără reper | Raport eroare, succes, ambiguitate și latență pentru ambele variante | Ultima secvență și model; fără rezultate selectate manual |
| P07 Thor și hartă | Integrează fluxuri, harta statică/dinamică și prioritizarea | Bugete măsurate, cozi limitate, recuperare după căderea rețelei | Snapshot confirmat și revizii; nu se aplică delta cu bază greșită |
| P08 H1 demo | Vizualizează lanțul TF și mișcarea trunchiului din date sintetice | Toate transformările verificate; mesh-uri/licențe disponibile | URDF și configurație fixate; zero actuare în această etapă |
| P09 Robot propriu | Adaptează URDF, montaj, odometrie și consumatori | Probe repetate cu modelul real; gate separat pentru orice mișcare | Recalibrare și replay, fără a transfera presupuneri H1 |
| P10 Exporturi | STL/3MF/PLY/USDZ/DXF; DWG cu convertor calificat | Import independent, unități, cote, texturi și avertismente verificate | Artefact derivat din hash intrare și versiune convertor |
| P11 Calificare/release | Rulează planul statistic, regresii, UX și audit licențe | Toate criteriile profilului declarat trecute; defectele publicate | Nu se repetă doar cazurile favorabile; versiune nouă dacă se schimbă algoritmul |

Aceste etape sunt **planificate**, nu finalizate prin redactarea documentelor. Durata de calendar se estimează după P00 și un spike P02/P06. Bugetarea în săptămâni fără acces la hardware, echipă nominală și rezultate de spike ar crea o precizie falsă. Paralelizarea permisă: UI, fixtures/exporturi și replay după P01; calibrarea depinde de montaj; performanța finală depinde de pipeline-ul integrat.

## Protocolul jurnalelor

Fiecare agent scrie numai în jurnalul său JSONL; managerul nu rescrie istoricul altui agent. Înregistrarea conține timestamp UTC, task, eveniment, rezultat, artefacte și următorul pas. Pentru acceptare se păstrează amprentele SHA-256 ale intrărilor/ieșirilor. Când o sarcină e întreruptă, se notează ultimul pas confirmat, fișiere temporare și dacă reluarea este sigură. La reluare se verifică hashurile înainte de a continua.

Stările sarcinilor documentare sunt `in_progress`, `in_review`, `rework`, `accepted`. Pentru experimente: `planned`, `running`, `passed`, `failed`, `inconclusive`, `not_run`. Nu folosim procentul de progres ca dovadă de finalizare. Auditul păstrează R1 și eventualele revizii; o constatare închisă are remediu și reverificare. Fișierele JSON și probele sunt autoritative pentru rezultatele executate; PDF-ul este o vizualizare a unei versiuni fixate.

Jurnalele acestei etape sunt puncte de control scrise pe parcurs, nu un recorder al fiecărei operații interne de calcul. Pentru runtime-ul viitoarei aplicații se implementează jurnalizarea tranzacțională descrisă în capitolul de date. Manifestul detectează modificările după livrare, dar nu este semnătură criptografică a unei autorități independente.

## Procedura de reluare

1. Citește `STATUS.json`, acest plan și rapoartele din `06_audit`.
2. Rulează verificarea manifestului pentru versiunea livrată. Dacă diferă, inventariază modificările; nu presupune că raportul vechi validează fișiere noi.
3. Citește ultima înregistrare din jurnalul rolului și intrările/ieșirile sarcinii.
4. Reexecută numai verificările ale căror intrări s-au schimbat sau care au eșuat. O modificare de contract impune replay-ul consumatorilor afectați.
5. Salvează rezultatul și cere verificare unui rol diferit de autor. Actualizează starea numai după dovezi.
6. Rebuild documentul, regenerează manifestul și verifică livrarea. Păstrează versiunea anterioară pentru comparație.

## Prompt master pentru echipa de implementare

„Implementează EVA-3dScan pentru profilul iPhone 17 Pro Max + Jetson AGX Thor 128 GB, conform contractelor și deciziilor acestui dosar. Începe cu P00, verifică dovezile disponibile și completează lipsurile. H1 v1 este model demonstrativ; robotul propriu se integrează ulterior prin URDF-ul furnizat. Nu confunda proba sintetică cu validarea hardware. Pentru fiecare sarcină înregistrează scopul, dependențele, intrările cu hash, acțiunile, ieșirile, testele și pasul următor. Atribuie auditor independent. Remediază constatările și reverifică. Nu declara un prag metric, de latență sau de fiabilitate îndeplinit fără protocolul și rezultatele cerute. Menține modurile obiecte, măsurare live fără salvare și camere/apartamente, plus extensia robotică explicit activată. Respectă unitățile, reperele, epocile, licențele și retenția. Oprește promovarea spre utilizare fizică dacă datele nu sunt suficient de recente sau calibrarea este invalidă. Predă cod reproductibil, rapoarte și jurnal de reluare.”
