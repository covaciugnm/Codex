# DECIZII_PROPUSE — ROM-001-G01 — r01

## 1. Identificare și regimul deciziilor

| Câmp | Valoare |
| --- | --- |
| ID livrabil G01 / componentă | ROM-001-G01 / DECIZII_PROPUSE |
| Versiune / statut document | r01 / DRAFT |
| Data | 24.09.2026, Europe/Bucharest |
| Autor / rol | P-EDITOR, producător separat de auditori |
| ID agent real | 01a0d1c4-17bb-7e03-93a3-e542824bc776, CODEX_THREAD_ID |
| ID sesiune observat | 01a07b90-9d07-7e72-8eb7-8439e985b9ba, CODEX_SESSION_ID |
| WorkID de portofoliu / dosar local | DB-047 / ROM-001 |
| Titlu / autoare catalogată | The Magenta Letters / Gabrielle St. Claire |
| Slug propus | magenta-letters, nepublicat, fără înregistrarea unei alte opere |
| Beneficiar al predării | P-MANAGER, pentru integrarea G01 |
| Proză EN nouă produsă / acceptată | 0 / 0; registrul nu se numără ca roman |

Fișierul păstrează numele cerut înainte de delegare. După răspunsul beneficiarului „Da, continuă și stabilește canonul prin decizii documentate și auditate.”, P-EDITOR își asumă alegeri editoriale pentru noul volum. Acestea nu sunt doar întrebări trimise beneficiarului și nu cer o a doua aprobare în limitele deja delegate. Documentul rămâne DRAFT: alegerea producătorului nu înseamnă acceptare G01 sau audit independent.

Dovadă citită integral: [APROBARE_BENEFICIAR_G01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/07_ROMANE/ROM-001/00_BRIEF/APROBARE_BENEFICIAR_G01.md>), SHA-256 47563b28103b26a6269b6315fcc147f0b516d5bf7fc4ee35dddd8c361cc5edc1. Mandatul anterior rămâne istoric, fără a i se completa retroactiv aprobări.

Componentă însoțitoare: [BRIEF_ROMAN_r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/07_ROMANE/ROM-001/00_BRIEF/BRIEF_ROMAN_r01.md>), același ID de livrabil, r01. §2 identifică intrările I-MAN, I-ROAD, I-ROL, I-CAN, I-MS, I-AP, I-RUB, I-ST, I-MOD, I-START, I-REG, I-FIND, I-U, I-ID și rapoartele managerului I-FISA/I-DREPT/I-MATR/I-AUX, întinderea lecturii și hash-urile calculate. §3 dă căile surselor H/HB/HP/HC/AC/A și convențiile P/L. Aceste referințe fac parte din intrările registrului; brief-ul nu este probă independentă pentru propriile sale afirmații.

Baza narativă efectiv citită de P-EDITOR este [CANON_EXISTENT.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/CANON_EXISTENT.md>), integral L1–L290, conținut intern r02, SHA-256 e5b6baada48e7d138ce841d6cc2283787984f22759c368322b269a3eb26ea4b0, acceptat ca selecție preliminară în pachetul G00 r03. P-EDITOR nu pretinde lectura întregului H și nu recitește auxiliarele în locul managerului. Probe H/HB/HP/HC/AC/A sunt raportate în I-CAN, cu completări explicit atribuite I-AUX, raportul managerului citit integral. Acestea urmează să fie integrate cu lectura integrală și verificate independent.

Reguli comune tuturor intrărilor:

- ASUMATĂ ÎN DRAFT înseamnă alegere efectivă a P-EDITOR, în autoritatea I-AP, destinată noului volum; nu înseamnă fapt unanim în H, constatare închisă sau PASS.
- DESCHIS înseamnă informație ori parametru care nu poate fi completat justificat înainte de integrarea probelor. Nu înseamnă că beneficiarul trebuie întrebat din nou.
- Pentru fiecare opțiune respinsă se păstrează proba concurentă. Nicio armonizare nu inventează o rudă, un al doilea obiect, un schimb de nume ori o scenă explicativă pentru a ascunde o inconsistență de redactare.
- Originalele, sursele, site-ul, strategia, programarea, registrele globale, contractele și auditurile nu sunt modificate. Alegerile documentează o continuitate asumată pentru noul volum; contradicțiile rămân vizibile în vechiul volum.
- Nu se aleg variante prin frecvența numelor și nici prin simplul fapt că o mențiune este ultima din carte.
- Orice probă suplimentară care infirmă baza alegerii cere revizie documentată înainte de depunerea fixă, nu o explicație inventată. După evaluare, o revizie primește versiune nouă.

## 2. Decizii de mandat și promisiune

### E01 — Operă, identitate de portofoliu și prioritate locală

**Probă:** I-AP autorizează The Magenta Letters; I-CAN §4.4 trimite la H P3981–P3984 și HC L684–L685. Constatarea verificată a managerului, transmisă de beneficiar (I-ID), identifică deja obiectul DB-047 din date_plan.json: același titlu, AMORIS/Isabella Morgan / Rue des Âmes, vol2, concept propus nescris, 60k, EN. Managerul raportează SITE_APP de la S: byte-identic capturii G00, fără id magenta-letters.

**Opțiuni:** A — utilizarea operei existente DB-047 cu dosarul local ROM-001; B — înregistrarea magenta-letters ca alt WorkID; C — schimbarea implicită a strategiei și programării.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Identitatea deja verificată previne dublarea aceleiași cărți. magenta-letters rămâne exclusiv slug propus nepublicat. Gabrielle St. Claire este autoarea catalogată; Isabella Morgan este personajul și numele ramurii.

**Impact nou:** master EN original minimum 50.000, țintă orientativă 65.000 în atelier, apoi RO/DE după EN acceptat. Estimarea strategică de 60k rămâne documentată separat. Mandatul acordă prioritate operațională locală pentru această producție.

**Efect asupra volumului vechi și portofoliului:** niciun fișier modificat; fără alt titlu, renumerotarea AMORIS, schimbarea strategiei ori reschedulare implicită.

**Dependență/test:** I-MATR/I-AUX, primite înainte de predare, localizează copia STRATEGIE_date_plan.json în 01_CANON/INTRARI_G01, obiect DB-047, și proveniența sa; documentează și comparația SITE_APP. P-MANAGER fixează aceste probe și hash-urile în depunere. În manifest trebuie să existe o singură operă DB-047, asociată dosarului ROM-001 și edițiilor sale. Nu se pretinde verificare directă a strategiei de către P-EDITOR.

### E02 — Promisiune de gen și limită de final

**Probă:** I-MAN §7 cere promisiune de gen și final compatibil; I-CAN §4.3–4.4 raportează cuplul căsătorit, Margaux's Story și promisiunea consimțământului.

**Opțiuni:** A — romance pentru adulți cu investigație epistolară și trecut istoric, final optimist; B — ficțiune despre iubire fără garanție de final romantic optimist.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Păstrează promisiunea relațională a continuării și oferă criteriu clar de verificare. Final HFN: reciprocitate și angajament credibile pentru arcul romantic central definit ulterior. O variantă fericită mai amplă este compatibilă; tragedia acelui arc sau cliffhanger-ul central nu sunt.

**Impact nou:** G03 va trebui să demonstreze un conflict central încheiat și satisfacție afectivă, fără a forța supraviețuirea ori reuniunea lui Margaux. Cititorul și tonul din brief sunt opțiuni editoriale, nu rezultate G02. Nu se stabilesc aici partenerul lui Margaux, intriga, antagonistul, scenele, POV sau două cronologii obligatorii.

**Efect asupra volumului vechi:** finalul Isabella–Alexandre, doliul și incertitudinea sarcinii se păstrează; nicio rescriere.

**Dependență/test:** lectura integrală și auditul de mandat G01 verifică compatibilitatea acestei promisiuni. Definirea ulterioară a arcului central trebuie să o respecte; cercetarea și premisele încep numai după porțile lor.

### E03 — Cuplul, plicul și separarea identităților

**Probă:** H P3553, P3839–P3841, P3860; P3882–P3892; P3932–P3955; separările de nume la I-CAN §4.2, L124–L126.

**Opțiuni:** A — continuitate a căsătoriei și acord specific pentru predare/deschidere/povestire; B — resetarea cuplului ori deschiderea plicului ca simplă convenție de investigație.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT, și aplicare a limitelor directe ale beneficiarului. Refuzul și păstrarea plicului sigilat trebuie respectate. Acordul pentru predare nu presupune acord pentru deschidere sau publicare; acestea sunt limite narative, nu o certificare juridică a drepturilor.

**Impact nou:** Isabella și Alexandre revin ca soți; sarcina rămâne la nivelul a trei teste și al speranței lor până la decizii narative ulterioare. Autorul/destinatarul/conținutul plicului și identitatea definitivă Margaux-din-mărturie/Margaux-Beaumont rămân necunoscute. Nicio rudenie Beaumont/Dubois, nicio unificare Margaux/Margot/Marguerite și nicio echivalare Alexandre/Alex Damian.

**Efect asupra volumului vechi:** se păstrează faptele finale și angajamentul etic, fără alterarea textului.

**Dependență/test:** nomenclatorul și registrul promisiunilor P-CANON trebuie să separe fapt, asociere de personaj, necunoscut și decizie. Închiderea poveștii noi nu poate cere încălcarea consimțământului ca soluție necesară.

### E04 — Perimetru de lucru și statut

**Probă:** I-MS, I-AP, I-ROAD G01–G06/G11/G17, I-RUB G01.

**Opțiuni:** A — integrarea documentelor G01 și controlul lor înainte de etapele dependente; B — utilizarea delegării drept aprobare a întregii porți.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Direcția și reconcilierea sunt delegate, dar acceptarea rămâne independentă. P-EDITOR produce numai cele două fișiere cerute în 00_BRIEF.

**Impact nou:** fără G02 research, G03 concepte sau G04 bible înainte de G01 acceptat; fără capitole înainte de G06 acceptat. Traducerile pornesc după G11. Fără scoruri, subagenți sau publicare.

**Efect asupra volumului vechi:** sursele sunt păstrate; nu se modifică site-ul sau artefactele de guvernanță.

**Dependență/test:** pachet integrat, versiune fixă, audit A-CANON/A-GOVERNANCE, metaaudit A-QAMANAGER și arhivare. Niciun verdict nu este emis de acest registru.

## 3. Reconcilieri H-C1–H-C9

### H-C1 — Anii și ancora temporală

**Probă:** I-CAN §4.5, L175: H P33–P42, scrisoare 15.10.1974 găsită după 51 de ani; P3816, reuniune în 2024; P3836–P3839, epilog la doi ani după descoperire; P3969, 57 de ani după 1968.

**Completare raportată de manager:** I-AUX indică HC L269 și SCORES L229–L242 cu epilog la un an. Această durată auxiliară este o a patra variantă; nu înlocuiește automat progresia din H. Alegerea A de mai jos exclude și importul ei ca durată certă.

**Opțiuni:** A — ancorarea descoperirii în 2025 și păstrarea progresiei de doi ani până în epilog; B — 2024 ca reper dominant al reuniunii, cu deplasarea descoperirii și recalcularea intervalelor; C — epilog tot în 2025 pentru a păstra cifra 57, abandonând progresia de doi ani.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT: descoperirea la 15.10.2025; epilog în decembrie 2027, prin corelarea cu H-C2. Aceasta este o alegere de normalizare, nu o cronologie integral probată în H. Păstrează ancora datată a obiectului inițial și progresia vieții cuplului. Reuniunea din prezent este ulterioară descoperirii, deci 2024 nu se transferă ca an al ei. În 2027 diferența calendaristică față de 1968 este 59 de ani; cifra 57 nu se preia pentru epilog.

**Impact nou:** continuarea trebuie să fie compatibilă cu starea din epilog; nu se fixează încă data începutului ROM-001, anul reuniunii, anul nunții sau alte date exacte. Calculul 1974 + 51 = 2025 este inferență; alegerea lui împotriva altor pasaje este decizie.

**Efect asupra volumului vechi:** 2024, 57 și salturile conflictuale rămân vizibile în H; nu se corectează originalul și nu se inventează o a doua reuniune.

**Dependență/test:** P-CANON livrează întreaga succesiune temporală. Managerul/editorul verifică toate ancorele, relația descoperire → reuniune → moarte → epilog și vârstele. Calendarul complet rămâne DESCHIS; dacă lectura integrală face soluția nesustenabilă, se revizuiește explicit înainte de audit.

### H-C2 — Luni, nuntă și aniversări

**Probă:** I-CAN §4.5, L176: H P8/P41, octombrie; P3631, sfârșit de noiembrie și „aproape un an”; P3786, februarie numită aniversarea găsirii; P3836/P3839, decembrie asociat aniversărilor; P3538, nuntă la 21 iunie.

**Opțiuni:** A — păstrarea lunii/datei scenelor explicit localizate și corectarea etichetelor aniversare pentru continuitate; B — mutarea descoperirii ori nunții ca să corespundă recapitulărilor târzii.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Aniversarea descoperirii este la 15 octombrie; data de zi/lună a nunții este 21 iunie. Decembrie rămâne luna epilogului, nu aniversarea exactă a nunții sau a descoperirii. Formularea „aproape un an” din noiembrie trebuie verificată ca durată aproximativă, fără a transforma automat noiembrie într-o altă lună.

**Impact nou:** nu se importă aniversarea în februarie și nu se inventează o ceremonie suplimentară pentru a salva recapitulările. Anul nunții și numărul exact de luni până la epilog rămân DESCHISE până la cronologia integrală. 2027 pentru epilog este alegerea H-C1, nu dovadă suficientă pentru deducerea tuturor celorlalte date.

**Efect asupra volumului vechi:** scenele și recapitulările incompatibile rămân neschimbate; decizia nu pretinde că nunta din H ar fi fost în decembrie.

**Dependență/test:** verificarea tuturor salturilor și aniversărilor în cronologia P-CANON; fiecare interval trebuie să corespundă datelor selectate. H-C1, H-C2 și H-C6 se închid numai împreună, pe o cronologie coerentă.

### H-C3 — Ceasul lui Antoine

**Probă:** I-CAN §4.5, L177: H P3729–P3733, ceasul pe trup la înmormântare; P3763–P3764/P3798, restituirea pentru îngropare; P3871/P3957, obiectul în apartamentul cuplului.

**Opțiuni:** A — ceasul este îngropat cu Antoine; B — ceasul rămâne moștenire în apartament. Acceptarea simultană ar cere un eveniment ori un obiect suplimentar care nu este probat.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Secvența explicită a înmormântării și gestul restituirii dau obiectului o închidere materială și afectivă clară. Motivul alegerii este acțiunea narată și funcția ei, nu numărul mențiunilor.

**Impact nou:** ceasul nu poate fi manipulat, transmis ori descoperit în apartament în prezentul continuării. Poate exista în amintirea personajelor numai în limitele faptelor selectate. Fără recuperare din mormânt, replică sau al doilea ceas inventat ca explicație.

**Efect asupra volumului vechi:** referințele de apartament rămân contradicții ale textului existent, explicit excluse din continuitatea obiectului în noul volum; sursa nu se editează.

**Dependență/test:** P-CANON verifică toate mențiunile, iar traseul obiectului trebuie să aibă o singură stare materială după înmormântare. Integrarea și auditul pot solicita revizuire dacă apare probă suplimentară.

### H-C4 — Locul primei descoperiri

**Probă:** I-CAN §4.5, L178: H P29–P32, plic pe birou lângă vază/sub ghid; P232/P3879, rememorare a găsirii în spatele biroului/golul sertarului. Noul plic este localizat separat la H P3882–P3892.

**Completare raportată de manager:** I-AUX identifică HP P85 cu un compartiment ascuns lângă cărți. Este o variantă de plan; decizia A nu o transferă în prima scenă din H.

**Opțiuni:** A — prima descoperire pe suprafața biroului, a doua în spațiul sertarului; B — prima descoperire în gol, prin prevalența recapitulărilor.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Scena primei descoperiri fixează acțiunea inițială; recapitulările nu primesc prioritate doar fiind mai târzii. Cele două plicuri au trasee distincte.

**Impact nou:** orice referință la prima scrisoare păstrează biroul/vaza/ghidul; camera 12 și spațiul sertarului aparțin descoperirii noului plic. Nu se deduce că primul plic a fost mutat între locuri de un personaj necunoscut.

**Efect asupra volumului vechi:** rememorările incompatibile nu sunt rescrise și nu sunt declarate coerente retrospectiv.

**Dependență/test:** P-CANON confirmă identitatea celor două obiecte și fiecare scenă de găsire; harta obiectelor nu le contopește.

### H-C5 — Jean-Paul, filiația și biografia familială

**Probă:** I-CAN §4.2/§4.5, L121/L179: H P256, Jean-Paul bunic/mecanic; P1651–P1656, tată și adresări „Mon fils”/„Papa”; P1778–P1782, Marie-Claire și carieră de profesor; H P1720/P1829, mama moartă când Alexandre avea 16 ani; HB P66–P67, ambii părinți morți când avea 12 ani.

**Opțiuni:** A — Jean-Paul tată/profesor, mama Marie-Claire moartă când Alexandre avea 16 ani; B — Jean-Paul bunic/mecanic și reconstruirea întregii filiații conform acelei mențiuni; C — biografia HB cu ambii părinți morți la 12 ani.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Relația tată–fiu este dramatizată prin adresări reciproce și context familial, cu consecințe în arcul lui Alexandre. Această funcție cauzală justifică alegerea, nu frecvența termenilor. HB este auxiliar de revizie anterior V2.

**Impact nou:** Jean-Paul este tatăl lui Alexandre și are cariera de profesor din ramura selectată; moartea lui rămâne. Marie-Claire este mama, moartă când fiul avea 16 ani. Nu se inventează adopție, tutelă, doi Jean-Paul sau un alt bunic mecanic pentru a distribui etichetele incompatibile. Datele de naștere și alte rude rămân necompletate.

**Efect asupra volumului vechi:** mențiunea bunic/mecanic și varianta HB rămân în surse; nu se modifică arborele prin rescrierea lor. Antoine nu devine bunicul lui Alexandre prin HP.

**Dependență/test:** nomenclatorul integral P-CANON verifică toate scenele familiale și moartea lui Jean-Paul. Biografia selectată trebuie să fie unică și compatibilă cu cronologia, fără rude adăugate ca remedii.

### H-C6 — Vârstele

**Probă:** I-CAN §4.5, L180: H P497 Antoine 80, P690 78, P3635 82; Catherine 73 la P2835 și 74 la P3783; HC L472 îi descrie pe amândoi ca aproximativ 76.

**Opțiuni:** A — preluarea tuturor numerelor literal, chiar dacă nu se potrivesc în timp; B — selectarea unei serii coerente de vârste din H după integrarea cronologiei; C — standardizarea ambilor la aproximativ 76 după HC.

**Recomandare și decizie de metodă:** B, ASUMATĂ ÎN DRAFT. HC nu arbitrează cifrele masterului. O vârstă trebuie legată de evenimentul și momentul la care este afirmată; o cifră izolată nu justifică o dată de naștere.

**Parametru DESCHIS:** această execuție nu selectează încă perechea de vârste definitive sau anii de naștere. Raportul preliminar nu furnizează succesiunea integrală necesară pentru a verifica dacă 80 → 82 și 73 → 74 se potrivesc cu duratele selectate. Regula de mai sus NU închide H-C6.

**Impact nou:** cifrele și datele de naștere nu intră în canonul de lucru ca certe până la completarea acestei decizii. Omiterea lor din proză nu elimină obligația de reconciliere din G01.

**Efect asupra volumului vechi:** toate vârstele rămân neschimbate în H/HC; nu se introduce o minciună despre vârstă pentru a explica o inconsistență.

**Dependență/test:** după DEP-01, P-EDITOR/P-MANAGER aleg cifrele în delegarea existentă și consemnează consecințele pentru 1974, prezent, reuniune, moarte și epilog. Până atunci H-C6 este blocaj documentar de închidere G01, nu cerere de aprobare suplimentară.

### H-C7 — Lisabona/Tokyo și continuarea anunțată

**Probă:** I-CAN §3/§4.5, L91/L181: AC P60–P62 și HP P113 propun Lisabona/O cafea la capătul lumii; HB P94–P103 adaugă jurnalul călătoriei lui Catherine din 1976; H P3932–P3984 și HC L684–L685 promit Margaux/1968/The Magenta Letters. I-AP și I-ID confirmă direcția.

**Completare raportată de manager:** I-AUX indică HC L379 cu perioada pre-May1968, deși registrul din H plasează șederea în vară/toamnă. Variantele sunt H — ședere în vară/toamnă — sau eticheta de jurnal pre-May; se adoptă în DRAFT informația registrului H pentru ședere. Eticheta auxiliară nu datează noul plic și nu fixează o intrigă despre evenimentele din mai. Efect nou: se păstrează 1968 și lunile efectiv probate; efect vechi: HC rămâne intact. Test: confruntarea integrală a registrului și a mențiunilor temporale de către P-CANON.

**Opțiuni:** A — continuarea promisă în finalul V2; B — preluarea planului Lisabona; C — mutarea la Tokyo după ordinea prezentării de serie de pe site.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT și conformă direcției autorizate. Finalul V2 și alegerea beneficiarului identifică aceeași operă. Itinerarele vechi nu sunt evenimente petrecute sau obligații de mutare în această continuare.

**Impact nou:** Parisul, hotelul și starea finală a cuplului sunt puncte de continuitate; nu se aprobă itinerar. 1968 și camera 14 sunt indicii documentate, nu plot. Nici Lisabona, nici Tokyo nu sunt importate automat. Posibila folosire ulterioară a unui loc cere alegere explicită în limitele premisei viitoare.

**Efect asupra volumului vechi și strategiei:** planurile rămân arhivate neschimbate; nu se șterg titluri, nu se mută sloturi și nu se rescrie prezentarea publică.

**Dependență/test:** managerul clasifică materialele auxiliare după versiune și funcție. Registrul promisiunilor separă teaserul efectiv de propunerile vechi.

### H-C8 — Camera 304/12 și Antoine Boucher/Mercier

**Probă:** I-CAN §4.5, L182: HP P87, camera 304; HP P93, Antoine Boucher, bunicul lui Alexandre; H P19, camera 12; H P150, Antoine Mercier.

**Completare raportată de manager:** I-AUX identifică HC L378/HCX P92 cu descoperirea noului plic în camera 14, diferită de H P3882–P3892. Opțiunile sunt camera 12 ca loc al descoperirii sau camera 14 din jurnal. Se adoptă în DRAFT camera 12 pentru găsire și camera 14 pentru adresă, pe baza scenei H și a inscripției distincte. Nu se inventează mutarea biroului. Efect nou: loc și adresă separate; efect vechi: jurnalele rămân neschimbate. Testul este traseul obiectului verificat de P-CANON.

**Opțiuni:** A — camera 12 și Antoine Mercier din H; B — camera 304 și genealogia din HP.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Se continuă masterul narativ identificat, nu planul anterior incompatibil. Numele lui Antoine și al lui Alexandre sunt conflicte separate.

**Impact nou:** camera 12 este cea a descoperirilor Isabellei; camera 14 este adresa noului plic și camera din registrul Margaux. Antoine este Mercier. Nu este introdus drept bunicul lui Alexandre și nu se deduce nicio filiație din numele Boucher.

**Efect asupra volumului vechi:** H și HP rămân neschimbate; varianta planului nu este prezentată ca episod pierdut sau identitate secretă.

**Dependență/test:** nomenclatorul, harta camerelor și proveniența HP/H sunt verificate integral. Orice informație genealogică suplimentară trebuie probată separat.

### H-C9 — Alexandre Boucher / Alexandre Dubois

**Probă:** I-CAN §4.2.1, L134–L138 și §4.5 L183: autoprezentări H P166/P860 cu Alexandre Boucher; formulele oficiantului H P3548/P3550 cu Alexandre Dubois; H P3553 pronunță căsătoria. I-FIND consemnează închiderea omisiunii documentare SEL-001-A-CANON-F01, fără a reconcilia H.

**Opțiuni:** A — Boucher pentru noul volum; B — Dubois pentru noul volum; C — evitarea numelui în proză, lăsând contradicția de canon nerezolvată.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Autoprezentarea identifică direct personajul în context profesional și relațional. Alegerea păstrează acea identitate și tratează forma concurentă din ceremonial drept inconsecvență editorială nepreluată în noua continuitate. Este o alegere explicită a producătorului; nu dovedește că Boucher este singurul nume din H sau un nume legal verificat. Frecvența și prioritatea ultimei mențiuni nu sunt argumente.

**Impact nou:** nomenclatorul de lucru folosește Alexandre Boucher și păstrează Dubois ca variantă conflictuală a sursei, nu alias al personajului. Isabella și Alexandre rămân același cuplu căsătorit; căsătoria nu este anulată de alegere. Nu se inventează rudenie cu Catherine/Guillaume, schimbare de nume, pseudonim, eroare explicată de personaj sau un al doilea Alexandre.

**Efect asupra volumului vechi:** ceremonia și autoprezentările rămân textual intacte. Divergența este documentată deschis; nu se raportează sursa ca reparată și nu se redeschide ori rescrie auditul istoric.

**Dependență/test:** P-CANON inventariază toate aparițiile și contextele, iar auditorii verifică identitatea unică și efectul alegerii asupra relațiilor. Omiterea numelui din viitoare scene nu ar fi închis H-C9; numai decizia integrată, justificată și auditată poate închide conflictul pentru continuare.

## 4. Clarificări H-N1–H-N2

### H-N1 — Profesii și stadiile proiectelor

**Probă:** I-CAN §4.5, L184: Catherine profesor pensionat de arhitectură, H P2835/P3809, dar predă la lycée la P3845/P3957; Alexandre specializat în Franța postbelică la P166, proiect medieval încheiat la P3841, aproape încheiat la P3872. I-CAN §4.2 raportează predarea parțială la Sorbona.

**Opțiuni:** A — păstrarea stării de profesor pensionat pentru Catherine și a proiectului medieval încheiat pentru Alexandre; B — preluarea predării curente la lycée și a proiectului încă neterminat; C — inventarea unor tranziții biografice pentru a lega toate variantele.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Profesia și pensionarea lui Catherine sunt identificate explicit; nu se introduce reangajare sau voluntariat fără probă. La Alexandre se selectează stadiul încheiat din descrierea situației de epilog, evitând regresia neexplicată la „aproape încheiat”. Motivul este o stare profesională finală coerentă, nu prevalența ultimei mențiuni.

**Impact nou:** Catherine rămâne profesor pensionat de arhitectură; predarea curentă la lycée nu este transferată ca fapt. Alexandre rămâne istoric, cu specializarea postbelică și predarea parțială raportate; proiectul medieval este încheiat la epilog în continuitatea selectată. O specializare și un proiect despre altă perioadă nu sunt declarate incompatibile prin ele însele; nu se inventează o schimbare de carieră pentru a le explica. Subiectul exact, publicarea și datele proiectului nu sunt completate.

**Efect asupra volumului vechi:** pasajele despre lycée și proiect aproape încheiat rămân vizibile în H. Nicio explicație nouă nu este strecurată retrospectiv în sursă.

**Dependență/test:** canonistul verifică toate mențiunile, succesiunea și eventualele tranziții deja existente. Dacă lectura integrală oferă o tranziție reală, aceasta este probă pentru revizuire, nu completare fictivă. Auditul distinge variația plauzibilă de contradicția efectivă.

### H-N2 — Numerotarea capitolelor și integralitatea textului

**Probă:** I-CAN §4.5, L185: H P1338 CHAPTER 10, apoi P1483 CHAPTER 12; HC L574 declară eliminarea capitolului 11, L592 eliminarea 25–27. I-CAN raportează 23 de titluri numerotate plus epilog, cu referințe HB la capitole vechi.

**Completare raportată de manager:** I-AUX indică SCORES L120–L126 pentru eliminarea capitolului 11 și constată că tabelele au 23 de capitole plus epilog, 24 de secțiuni, deși unele rezumate declară 25. Decizia A adoptă structura observată, fără a inventa secțiunea a 25-a. Diferența de numărătoare rămâne documentată în auxiliare, nu devine cerință de completare a romanului.

**Opțiuni:** A — păstrarea structurii observate și verificarea eliminărilor declarate; B — declararea automată a unui capitol lipsă și scrierea lui; C — renumerotarea H.

**Recomandare și decizie:** A, ASUMATĂ ÎN DRAFT. Un salt de etichetă, împreună cu o eliminare declarată în jurnal, nu demonstrează pierderea prozei. Integritatea narativă rămâne totuși de verificat prin lectura completă.

**Impact nou:** nu se scrie un capitol de completare a vechiului volum; referințele de probă rămân la P și la eticheta exactă din H. Numărul capitolelor ROM-001 se va decide la etapa de arhitectură; nici 23, nici 26 nu sunt obligatorii aici.

**Efect asupra volumului vechi:** zero renumerotări, inserări sau eliminări; se păstrează structura originală și jurnalul său.

**Dependență/test:** P-CANON verifică secvența întregului H, managerul verifică HC/HB și proveniența. Se raportează separat titlurile numerotate, epilogul și orice discontinuitate reală; nu se certifică integralitatea numai prin numărare.

## 5. Dependențe, grilă și predare

| Dependență | Ce trebuie integrat | Responsabil / limită |
| --- | --- | --- |
| Lectură H | acoperire integrală, nomenclator, cronologie, obiecte, promisiuni și constatări suplimentare | P-CANON; predarea nu este simulată de P-EDITOR |
| Auxiliare și proveniență | I-MATR/I-AUX/I-DREPT primite și citite; inventar și observații integrate în registru; probe de fixat în pachet | P-MANAGER; documente DRAFT, utilizare locală autorizată, limite comerciale separate pentru verificarea dinainte de G16/G17 |
| Identitate de operă | proba date_plan.json/DB-047, legătura ROM-001, metadate și comparația SITE_APP, localizate în I-MATR/I-AUX | P-MANAGER; raportarea managerului este utilizată, primarele nu sunt reverificate de P-EDITOR |
| Calendar și vârste | anul nunții, intervalele exacte, seria coerentă de vârste și recontrolul H-C1/H-C2/H-C6 | P-EDITOR/P-MANAGER după lectura integrală; nu necesită altă aprobare în delegarea dată |
| Depunere fixă | contract, manifest, amprentele celor două componente și ale întregului pachet G01 | P-MANAGER; P-EDITOR nu modifică registrele globale |
| Control independent | audit dublu, metaaudit și arhivare pe versiunea exactă | A-CANON, A-GOVERNANCE, A-QAMANAGER în execuții independente; fără rezultate anticipate |

Grila G01 rămâne neschimbată, fără scoruri de producător:

| Criteriu | Pondere | Acoperire în registru / verificare necesară |
| --- | --- | --- |
| acoperire | 25 | §1 și dependențele: probele raportate trebuie legate de lectura integrală și proveniența reală |
| canon | 30 | E02/E03, H-C1–H-C9 și H-N1: continuitate a relațiilor, obiectelor, faptelor și finalurilor |
| contradictii | 20 | fiecare intrare are alternative și dispoziție; parametrii DESCHIȘI se închid explicit înainte de acceptare |
| mandat | 15 | E01–E04: DB-047, vol2, gen/final, original EN minimum 50k, țintă 65k, apoi RO/DE, fără salt de etapă |
| trasabilitate | 10 | §1, probele localizate, I-AP, I-ID și amprentele intrărilor din brief; versiune fixă pentru ambii auditori |

Ponderile însumează 100; nu sunt note. Auditul fiecărui criteriu și închiderea constatărilor aparțin auditorilor. Metaauditul nu este redactat de P-EDITOR. Nicio intrare din registru nu este marcată ACCEPTATĂ sau PASS.

Stare de predare: decizii asumate în DRAFT, cu calendarul complet și H-C6 încă deschise. Identitatea DB-047 și delegarea sunt stabilite prin actualizările primite; nu se raportează un blocaj fictiv de permisiune. G01 rămâne NEACCEPTAT până la integrarea tuturor probelor, rezolvarea contradicțiilor, audit, meta și arhivare. Noul volum nu este scris sau finalizat.

Predarea privește numai [BRIEF_ROMAN_r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/07_ROMANE/ROM-001/00_BRIEF/BRIEF_ROMAN_r01.md>) și prezentul registru, în 00_BRIEF. Hash-urile finale sunt calculate după ultima editare și transmise managerului în raportul execuției; manifestul și fixarea pachetului se fac la integrare. Se așteaptă integrarea, fără pornirea etapelor următoare.
