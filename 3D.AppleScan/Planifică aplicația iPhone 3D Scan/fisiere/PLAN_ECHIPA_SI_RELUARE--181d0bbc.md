# Planul echipei și procedura de reluare

## Echipa și limitele sesiunii

Managerul este agentul principal. Au fost pornite trei roluri de specialitate în paralel, folosind toate cele patru locuri disponibile, inclusiv managerul. Rolul de auditor final se execută după eliberarea unui loc și revizuiește livrabilele celorlalte roluri. Nu există agenți umani certificați implicați: descrierile reprezintă responsabilități de lucru ale agenților AI.

| Rol | Responsabilitate | Livrabil | Criteriu de încheiere |
|---|---|---|---|
| Manager | Scop, integrare, cerințe, registru, reluare, arbitraj | Specificație, plan, prompt, index, registre | Fiecare livrabil are proprietar, stare, dovezi și pas următor |
| Cercetare și UX | Concurenți, GitHub relevant, recenzii, forumuri, fluxuri | Studiu comparativ, feedback, UX, surse | Afirmații importante susținute și observații anecdotice etichetate |
| Apple | Hardware, API, arhitectură, captură, limite | Capitol tehnic și matrice capabilități | Fără promisiuni neconfirmate despre API sau precizie |
| CAD și imprimare | Formate, unități, DWG, point cloud, slicere, metrologie | Matrice formate, pipeline, protocol | Export și conversie diferențiate; pierderi și licențe explicate |
| Auditor final | Coerență, lipsuri, linkuri, trasabilitate, afirmații | Raport cu constatări și verdict | Zero constatări P0/P1 nerezolvate în documentația acceptată |

Managerul decide ordinea și integrarea. Specialistul decide recomandarea tehnică din aria sa. Auditorul poate respinge un livrabil; autorul îl repară, iar auditorul verifică din nou. Managerul nu închide o problemă critică prin schimbarea etichetei. „100% mulțumit” este operaționalizat ca îndeplinirea tuturor criteriilor documentare convenite; nu reprezintă garanție de perfecțiune a software-ului.

## Etapele proiectului aplicației

Toate etapele de implementare de mai jos sunt planificate, fără rezultate executate în sesiunea de documentare.

| Pas | Obiectiv și activități | Responsabil | Rezultat cuantificabil și poartă | Dependență |
|---|---|---|---|---|
| P00 | Inventariere și organizare | Manager | 1 inventar, 1 registru, 1 index, 0 fișiere existente suprascrise | Acces la director |
| P01 | Cercetare și sinteză | UX, Apple, CAD | Minimum 6 competitori, 12 observații de feedback dacă disponibile, surse pentru afirmații decisive | P00 |
| P02 | Cerințe și UX | Manager, UX | 3 fluxuri complete; fiecare P0 cu test și proprietar | P01 |
| P03 | Probe de fezabilitate Apple | Apple | 5 probe reale: depth, obiect, măsurare, cameră, unire; log pe fiecare telefon | Mac, Xcode, iPhone |
| P04 | Model de date și recuperare | Apple, QA | 50 întreruperi injectate, zero proiecte finalizate corupte | P03 |
| P05 | Obiecte cu cote | Apple, CAD | Captură, referință, cote, versiuni, export; benchmark dimensional pe clase | P03–P04 |
| P06 | Măsurare temporară | Apple, UX | 50 sesiuni fără persistență media și fără upload, 20 anulări foto | P03 |
| P07 | Camere și unire | Apple, UX | 10 proiecte cu 3–8 camere, originale păstrate, erori de aliniere raportate | P04 |
| P08 | Exporturi și CAD | CAD | Fiecare format anunțat trece fixture, import, scară, cote și pierderi | P05/P07 |
| P09 | Imprimare și metrologie | CAD, QA | Loturi și eșantioane conform protocolului; raport digital separat de piesa fizică | P08, imprimante |
| P10 | UX, accesibilitate și robustețe | UX, QA | 20 participanți în evaluarea propusă; zero blocaje critice; raport pe dispozitiv | P05–P09 |
| P11 | Audit și pilot | Auditor, manager | Zero P0/P1 deschise; pilot limitat cu rezultate și consimțăminte de test | P10 |
| P12 | Lansare și urmărire | Manager, echipă | Note de versiune, matrice suport, procedură incident și restaurare verificate | P11 |

Estimare de planificare, fără angajament contractual: probe 2–4 săptămâni; nucleu 8–12; exporturi și metrologie 4–8; pilot și stabilizare 4–6. Unele activități se suprapun. Efortul depinde de dispozitive, echipa umană, licențe și rezultatele cercetării; intervalele nu sunt un deviz verificat. Agenții AI nu înlocuiesc accesul la hardware și măsurarea fizică.

## Registrul canonic

`tasks.json` este registrul sarcinilor acestui dosar. `STATUS.json` arată ultimul checkpoint și pasul următor. Jurnalele `*_events.jsonl` păstrează evenimentele rolurilor; managerul menține `manager_events.jsonl`. Rapoartele din `08_audit` sunt istoricul auditului. Manifestul SHA-256 permite identificarea modificărilor după înghețarea unei livrări.

Stările permise sunt `planned`, `in_progress`, `in_review`, `changes_requested`, `accepted`, `blocked`. Acceptarea documentației nu schimbă starea implementării. Un rezultat `not_run` sau `blocked` nu poate fi redenumit `passed` fără dovezi.

Fiecare sarcină conține ID, titlu, proprietar, intrări, dependențe, rezultat așteptat, criterii, fișiere, stare, audit și următoarea acțiune. Fiecare eveniment conține ID unic, moment ISO 8601 sau data când ora nu a fost înregistrată, actor, sarcină, tip, rezumat, dovezi și pas următor. Evenimentele reconstruite din istoricul sesiunii sunt etichetate `reconstructed`; nu primesc ore inventate.

## Protocol obligatoriu înainte de lucru

1. Citește README, STATUS, registrul sarcinilor, ultima versiune a manifestului și auditul final.
2. Rulează verificatorul documentației. Pentru o versiune livrată verifică hashurile înainte de editare și păstrează raportul.
3. Alege o sarcină cu dependențe satisfăcute. Înregistrează `task_started` înainte de editare, cu proprietar unic și fișierele asumate.
4. Nu permite scrierea simultană în același fișier. Agenții lucrează în folderele atribuite. Managerul integrează secvențial.
5. La fiecare rezultat verificabil adaugă un eveniment și actualizează starea. Un draft existent după crash rămâne `in_progress`, nu devine implicit complet.

## Checkpoint și reluare după întrerupere

La sfârșitul fiecărei sarcini și înaintea unei operații lungi, scrie: ce s-a finalizat, ce fișiere există, ce verificări au trecut, ce a eșuat, ce surse au fost citite, ce rămâne și prima acțiune exactă. Pentru operațiile viitoare automate se folosesc fișier temporar, flush și rename în același volum. Copierea pe SMB nu este presupusă atomică; se verifică manifestul și un marcaj de livrare creat ultimul.

După întrerupere, compară registrul cu fișierele și jurnalele. Dacă lipsește evenimentul de finalizare, verifică efectul înainte de repetarea operației. Dacă rezultatul este incomplet, păstrează-l drept draft și reia de la ultimul pas confirmat. Pentru descărcări și conversii folosește cheie de idempotentă derivată din hashul intrării, versiunea adaptorului și opțiuni. Nu dubla plăți sau joburi externe.

Fiecare audit are ID, versiunea documentelor, criteriile verificate, dovada, severitatea, responsabilul remedierii și retestarea. Dacă o observație rămâne deschisă, ea se transferă explicit în STATUS și în următoarea iterație.

## Limitele continuității

Acest mecanism permite reluarea la ultimul checkpoint confirmat. Nu poate reconstrui raționamentul nesalvat sau o operație executată între două checkpointuri. Protecția reală împotriva pierderii necesită backup versionat în altă locație și verificarea restaurării. Copia locală și copia de rețea oferite aici au hashuri comparate, dar nu constituie singure un sistem complet de backup automat.

## Regula de finalizare

Un document este acceptat când existența, lizibilitatea, referințele, cerințele, contradicțiile și limitările au fost auditate. O aplicație este acceptată numai după execuția testelor pe dispozitive reale. Cercetarea continuă prin sarcini noi; documentele acceptate nu se rescriu fără jurnal și versiune nouă.
