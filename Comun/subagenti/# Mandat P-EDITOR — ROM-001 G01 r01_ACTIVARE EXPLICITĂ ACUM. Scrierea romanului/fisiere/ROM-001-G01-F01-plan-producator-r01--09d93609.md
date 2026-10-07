# ROM-001-G01-A-CANON-F01 — plan de măsuri al producătorului

Versiune plan: r01. Statut: DRAFT — PREGĂTIRE DE REMEDIERE.
Autor: P-EDITOR, ID real 01a0d1c4-17bb-7e03-93a3-e542824bc776, verificat în CODEX_THREAD_ID.
Data: 24.09.2026, Europe/Bucharest.
Proiect: ROM-001; WorkID DB-047; livrabil afectat ROM-001-G01.
Finding tratat: ROM-001-G01-A-CANON-F01, OPEN.
Stare comunicată la activare: RETURN primar G01 r01; metaaudit în curs. Nu se deduce aici un rezultat ulterior al QA.

## 1. Autoritate și separarea etapelor

Mandatul curent autorizează numai lectura, analiza și acest plan. Unicul fișier în care scrie P-EDITOR acum este:
06_REGISTRU/MASURI/ROM-001-G01-F01-plan-producator-r01.md.

Contractul r01, produsele r02, sursele și rapoartele sunt înghețate. Nicio componentă r03 nu este autorizată în acest turn. Acest plan nu este produs corectat, închidere de finding, nouă depunere, audit ori G02; nu conține proză de roman și nu acordă scoruri.

Condiția comună G pentru orice activitate viitoare de modificare: managerul confirmă închiderea și arhivarea rundei r01, inclusiv tratarea rezultatului metaauditului, apoi transmite activarea explicită a reviziei și limitele ei. Sunt necesare ambele condiții. Închiderea rundei nu înseamnă închiderea findingului F01 și nici acceptarea G01. Delegarea anterioară pentru canon nu înlocuiește G.

Planul păstrează manualul, rubricile și separarea producție/audit deja citite. Măsuri suplimentare ale QA pot cere un plan distinct/revizuit; nu sunt anticipate drept verdict cunoscut. P-EDITOR nu rescrie un raport primar returnat de QA și nu înlocuiește auditorul care a emis constatarea.

## 2. Intrări identificate și întinderea verificării actuale

Rădăcina exactă a căilor relative:
D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000.

SHA-256 calculate asupra octeților locali în această pregătire:

| Alias | Cale relativă exactă | SHA-256 |
| --- | --- | --- |
| M | 06_REGISTRU/PROMPTURI/ROM-001-G01-P-EDITOR-plan-producator-pregatire-r01.md | 606fa7d85677ed352f74e7878e94241927e3198a6ec33f922e9bd725976381ab |
| A | 05_AUDIT/ROM-001-G01/r01/A-CANON.md | 516b1d5e499b0ab78a1456508f462d148160b6e629300cd715bca665f10efefc |
| I | 06_REGISTRU/MASURI/ROM-001-G01-F01-intake-r01.md | bcddeb54b6a83130fe7f447a795a4b8fad4104aa6042d1b9036628ae8d97d5ab |
| B | 07_ROMANE/ROM-001/00_BRIEF/BRIEF_ROMAN_r02.md | fb26a4a6bdfa76da4d0a66cc8fac9b75677ee2f299e014cc3de666978c9e78c7 |
| D | 07_ROMANE/ROM-001/00_BRIEF/DECIZII_CANON_r02.md | 6ee676184ae2d21bbdffb57459158e18fae35ffb0ec3f2a7d7de4533d0b2b4a4 |
| O | 07_ROMANE/ROM-001/00_BRIEF/CANON_OPERATIONAL_r02.md | a5a9ff52b30f110d362e4b2175a17fe924d8a34d11c89efeb407d5025db54abc |
| F | 07_ROMANE/ROM-001/01_CANON/r01/CANON_FACTUAL.md | 0635d163992d0c63d0b1d815df000816f8b9320c84e33c732cb899dd6eebd3ab |
| H | 02_DOCUMENTARE/INTRARI_REFERINTA/H.docx | a9940d5776380cb40b105429f6976219440f3ea74fb8ebc1d1b4481e9da068c3 |
| K | 06_REGISTRU/CONTRACTE/ROM-001-G01-r01.json | 07110637be555cb455727593ebdf9ef88de1f27c12b5a389f53e79544bd6cebe |

M, A, I, B, D, O și F au fost citite integral în această pregătire. Din K au fost consultate identificarea rundei, lista celor 11 artefacte, rolurile de audit și referința politicii; nu se pretinde o nouă verificare a tuturor celor 126 evidence sau a arhivei complete.

Control direct H: P128–P160, P1366, P1380–P1385 și P1409, exact 41 de paragrafe distincte, afișate integral și citite. Metodă: word/document.xml, //w:body//w:p, concatenare .//w:t, eliminarea spațiilor periferice și a paragrafelor goale, numerotare de la 1. Corpul a fost enumerat mecanic până la P3984 numai pentru indexare; aceasta NU este lectură integrală a H. Nu s-au extras fișiere pe disc. Lectura integrală anterioară H rămâne atribuită P-CANON.

Au fost confruntate direct O L92 și F L92; contextul F L88–L98 este inclus în lectura integrală F. Celelalte localizări H pentru personajele de control sunt preluate explicit prin F, nu declarate recitite direct aici.

Control mecanic de identificare: cele 11 artefacte din K au hashurile din contract, fără diferențe la pregătire. Au fost fixate în memorie amprente pentru 16 fișiere distincte: cele 11 plus M, A, I, H și K. Nu s-au modificat intrările și nu s-a produs un manifest nou. Acest control nu dovedește corectitudinea semantică a produsului și nu substituie auditul.

Controlul separat de afiliere P-CANON: PENDING la punctul de verificare 24.09.2026 11:09:12 +03:00; în directoarele 06_REGISTRU/MASURI și 07_ROMANE/ROM-001/01_CANON nu era disponibil un fișier F01/afiliere diferit de intake. Nu îi inventez calea, hashul, conținutul sau rezultatul. Integrarea lui este prevăzută la M2, fără a amâna predarea acestui plan.

## 3. Defect observabil, cauză de proces și corecție propusă

### 3.1. Confruntarea probelor

| Localizare verificată | Observație relevantă | Consecință pentru măsură |
| --- | --- | --- |
| O L92, coloana F | Patru persoane grupate — Laurent, Marcel, Odette, Rousseau — urmate de patru descrieri. A doua îl asociază pe Marcel cu „personal/interlocutor al hotelului”. Referința este generică: conform CANON_FACTUAL. | Afilierea este introdusă în sinteză ca fapt, nu motivată ca alegere D. Rândul trebuie dezambiguizat în produsul viitor. |
| F L92 | Marcel Fontaine este arhivar/intermediar; numele complet este legat de H P1366. Partner-ul din P160 nu este identificat, iar vârsta are variante. | Sursa invocată de O nu susține afilierea hotelieră. Nu există aici o lacună care cere inventarea unui al doilea post. |
| H P128–P160 | Marcel este specialistul în registre ale secolului XX, consultă dosare și registrul hotelier în cadrul arhivelor. P156 introduce separat hotelul/Besson în întrebarea Isabellei. | Subiectul documentelor — hotelul — nu este instituția persoanei care le consultă. Registre hoteliere ≠ angajare la hotel. |
| H P1366 | Marcel Fontaine se prezintă ca provenind de la arhive. | Identificare explicită nume–cadru instituțional. |
| H P1380–P1385 | Apelul stabilește accesul la arhivă; personajele se deplasează acolo și sunt întâmpinate de Marcel. | Confirmă cadrul arhivelor, fără a-i atribui o a doua funcție. Varianta de vârstă din P1385 rămâne tratată separat prin H-C6. |
| H P1409 | Marcel își atribuie găsirea fotografiei în catalogarea curentă și consemnează proveniența în catalog. | Proveniența probei trebuie păstrată la arhive/Marcel, nu transferată hotelului. Declarația diegetică despre utilizare nu devine certificare juridică externă. |

Efectul erorii: un romancier sau un rezumat derivat poate muta sursa/custodele documentării în personalul hotelului și poate atribui greșit autoritatea accesului. Acesta este un defect nou de sinteză F→O, nu una dintre contradicțiile H rezolvate prin cele 22 de decizii. Findingul curent nu trebuie confundat cu SEL-001-A-CANON-F01, menționat istoric la H-C9.

### 3.2. Cauză de proces, fără inferențe psihologice

Transformarea mai multor fișe factuale în liste paralele, într-un singur rând, a pierdut legătura explicită dintre persoană, rol, instituție și probă. O a adăugat afilierea hotelieră în coloana F, deși F păstrează rolul corect. Trimiterea generică la întregul CANON_FACTUAL nu a făcut asocierea verificabilă la nivelul fiecărei persoane.

Responsabilitatea producerii sintezei este P-EDITOR. Bariera de confruntare granulară F→O nu a împiedicat regresia observabilă; verificarea de integrare este al doilea punct de control al P-MANAGER. Nu susțin că știu dacă o verificare anume a fost omisă mental, dacă un agent a uitat sau câtă atenție a acordat. Cauza documentabilă privește reprezentarea și controlul ieșirii, nu stări interne, incidentul de limită sau presupuse intenții. F/H nu trebuie schimbate pentru a justifica O.

### 3.3. Direcția corecției — încă neexecutată

După G, propun ca nomenclatorul să folosească identificări explicite, de preferat un rând pentru fiecare persoană afectată, cu rol, instituție/cadru și localizare F/H atașate aceleiași persoane. Pentru Marcel, ținta de corectitudine este Marcel Fontaine — arhivar/intermediar al arhivelor — F L92 și cele 41 de paragrafe H verificate; nu personal hotelier. Referentul Dr Fontaine nu se unifică cu Marcel fără probă: separarea fișelor nu pretinde că H ar demonstra imposibilitatea identității lor.

Se vor explicita numele în rezumatele în care forma scurtă poate confunda referenții: în special Jean-Michel Rousseau pentru custodia scrisorilor și Sophie Rousseau pentru jurnalism/articol. Contextul, nu înlocuirea globală a numelui Rousseau, decide referentul. Instituția neprobată se marchează neprecizată; nu se inventează un angajator sau o titulatură juridică a arhivelor.

Corecția nu schimbă vârsta lui Marcel din H-C6, calendarul, familia lui Alexandre, ceasurile, consimțământul, sarcina sau alte alegeri H-C1–H-C16/H-N1–H-N6. Nu adaugă o decizie H-C17 și nu convertește această remediere factuală într-o nouă reconciliere. Orice problemă mai largă necesită probă, impact, justificare și caz separat adus managerului/QA, fără corecție tăcută.

## 4. Planul de activități și responsabilități

Toate rândurile de mai jos sunt activități viitoare. Niciuna nu este executată prin redactarea acestui plan. G este condiția din §1; nu constituie o autorizare acordată de P-EDITOR.

| ID | Activitate / responsabil | Livrabil ori urmă cerută după autorizare | Statut și dependență |
| --- | --- | --- | --- |
| M1 | P-MANAGER închide/arhivează runda r01 potrivit QA și transmite activarea explicită, limitele și intrările reviziei. | Referințe reale la rezultat/meta, arhivare, contractul înghețat și mesaj/mandat nou. | NEEXECUTATĂ în acest plan; condiție prealabilă, nu rezultat pretins. |
| M2 | P-EDITOR citește și integrează controlul de afiliere predat de P-CANON; P-MANAGER clarifică eventualele diferențe față de F/H. | Identificare cale/versiune/hash, întinderea lecturii și mapare la F01. Controlul rămâne suport factual, nu audit. | NEEXECUTATĂ; integrare PENDING, după G și disponibilitatea documentului. |
| M3 | P-EDITOR produce CANON_OPERATIONAL_r03.md separat de O r02, cu corespondențe neechivoce în §3 și propagare în rezumatele relevante ale aceleiași componente. | O r03 DRAFT + diferențe localizate: fiecare modificare legată de F01 și de probă. Niciun rând afectat reparat prin post suplimentar sau identitate inventată. | NEEXECUTATĂ; numai după G și tratarea intrărilor M2. |
| M4 | P-EDITOR produce BRIEF_ROMAN_r03.md și DECIZII_CANON_r03.md separat de B/D r02; aliniază versiunile, trimiterile și contextul de revizie. | Trei componente r03 coerente; D păstrează semantic toate cele 22 de dispoziții. Detaliile sunt în §5. | NEEXECUTATĂ; numai după G, în aceeași revizie controlată cu M3. |
| M5 | P-EDITOR aplică testele §6 pe octeții finali propuși; P-MANAGER face confruntarea de integrare. | Evidență de diferențe și rezultate de producție, cu fișier/linie/referent/probă pentru fiecare apariție și verificare 22/22 semantică. Calea/versiunea raportului separat vor fi stabilite în activare. | NEEXECUTATĂ; după G și M3–M4; nicio valoare de succes completată acum. |
| M6 | P-MANAGER fixează inventarul tuturor rezumatelor/handoffurilor active și coordonează propagarea; fiecare producător revizuiește numai propriile fișiere autorizate. P-EDITOR verifică propriile trei componente și predarea sa. | Listă exhaustivă active/istorice, fișiere cu și fără apariții, fiecare ocurență clasată și rezumate noi coerente. Documentele înghețate rămân istoric, nu sunt suprascrise. | NEEXECUTATĂ; după G; modificările fișierelor altor responsabili cer mandatele lor, nu sunt autorizate de acest plan. |
| M7 | P-MANAGER fixează noua depunere, contractul și manifestul corespunzător, cu sprijin P-SYSTEMS în propriul mandat. | Căi/versiuni și SHA-256 reale ale celor trei r03 și ale tuturor intrărilor; context stabil al reviziei; runda veche păstrată. | NEEXECUTATĂ; după G și controalele de producție. P-EDITOR nu creează contract/manifest. |
| M8 | Auditorii nominali separați retestează pe contractul nou; QA face metaauditul; managerul consemnează/arhivează potrivit rezultatelor. | Rapoarte independente și decizie de poartă numai prin workflow; eventuale măsuri suplimentare. | NEEXECUTATĂ; nu este atribuție sau verdict al producătorului și nu este anticipată. |

## 5. Coerența celor trei componente propuse r03

Director propus, doar după autorizare: 07_ROMANE/ROM-001/00_BRIEF/.

| Componentă viitoare | Modificări strict propuse | Ce trebuie păstrat |
| --- | --- | --- |
| CANON_OPERATIONAL_r03.md | Revizie r03 în titlu/metadate; nomenclator neechivoc și citări individuale; referințe funcționale către B r03/D r03; identificarea F01 și a originii r02; dezambiguizare controlată a rezumatelor de custodie/intermediere. | F/H r01 ca surse istorice, etichetele F/D/I și toate cele 22 de alegeri, inclusiv vârsta lui Marcel. |
| DECIZII_CANON_r03.md | Revizie r03 și trimiteri către B/O r03; notă de revizie factuală F01 în afara celor 22 de dispoziții; eventuale nume explicite numai dacă un rezumat propriu este ambiguu, fără schimbare de referent. | Identificatorii, probele concurente, alegerea, motivul, excluderile și testele H-C1–H-C16/H-N1–H-N6, semantic neschimbate. |
| BRIEF_ROMAN_r03.md | Revizie r03; lista celor trei componente și trimiterile reciproce actualizate; secțiune de revizie care identifică F01, B/D/O r02 drept părinți, intrările noi și întinderea lecturii; DRAFT fără acceptare anticipată. | DB-047/ROM-001, autor/agent, mandat EN≥50k/țintă65k, RO/DE ulterior, promisiunea de gen și limitele de continuitate. |

Reguli de versiune și trasabilitate:

- r01 este versiunea rundei contractuale auditate; r02 sunt versiunile componentelor depuse în ea; r03 ar fi versiunile produselor remediate. P-EDITOR nu inventează numărul viitorului contract.
- Fiecare trimitere funcțională dintre componentele active va ținti r03. Referințele la r02 care explică istoricul/părintele rămân r02 și sunt etichetate istoric; nu se execută o înlocuire globală oarbă. F r01, H și celelalte surse păstrate nu sunt rebotezate r03.
- În B r03 se va adăuga un grup distinct de intrări de revizie, fără reutilizarea ambiguă a identificatorilor I01–I32: mandatul/activarea nouă; raportul A și intake-ul I; acest plan în forma predată; B/D/O r02 cu hashurile din §2; controlul P-CANON; rezultatul QA și dovada închiderii/arhivării rundei; contextul stabil furnizat de manager.
- Intrările existente se referențiază prin calea/versiunea/hashul real. Cele încă inexistente sau neprimite nu primesc hash, dată, autoritate ori statut inventat. La activare se fixează explicit setul de intrări și se citesc noile instrucțiuni relevante integral.
- Contextul istoric CONTEXT_INTEGRARE_r02 rămâne istoric. Noile stări QA/depunere nu sunt deduse din el sau din hashurile unor registre live vechi.
- Amprentele finale ale r03 se calculează după ultimul edit și se predau managerului pentru manifestul separat. Nu se creează un ciclu de auto-hashuri între B/D/O; trimiterile reciproce identifică versiunile, manifestul fixează octeții.
- Raportul viitor de modificări va separa corecția factuală F01, dezambiguizările echivalente, metadatele/trimiterile și orice propunere ieșită din scop. Ultima categorie nu se implementează fără caz și autorizare distincte.

## 6. Teste și rezultate măsurabile propuse

Statut comun T1–T8: NEEXECUTATE pe produsul remediat; nu există r03 în acest mandat. Cifrele din coloana rezultat sunt ținte de verificare, nu rezultate obținute sau scoruri.

| Test | Metodă / cazuri obligatorii | Rezultat măsurabil cerut înaintea redepunerii |
| --- | --- | --- |
| T1 — transfer F→O | Confruntare a noii O §3 cu F L88–L98 și H P128–P160/P1366/P1380–P1385/P1409. Pentru fiecare persoană afectată: nume, rol, instituție/cadru, sursă exactă și limită. | Toate corespondențele afectate documentate individual; zero afiliere hotelieră neprobată pentru Marcel; zero rol nou introdus. |
| T2 — identități învecinate | Marcel Fontaine distinct de Dr Fontaine; fără echivalare automată cu Henri Delacroix. Sylvie Laurent managera hotelului, Besson recepție/custodie, Odette martoră. Jean-Michel Rousseau fost camarad/custode de scrisori, distinct de jurnalista Sophie Rousseau. Baza actuală: F L88–L98; H pentru Marcel este direct citit, celelalte citări H sunt prin F și se vor confrunta în controlul de afiliere. | Zero confuzie de persoane/instituții; numele comun nu creează identitate/rudenie. Custodia personală a scrisorilor nu este redenumită post în arhive sau la hotel. |
| T3 — toate aparițiile și toate rezumatele active | Căutare Marcel, Fontaine, Dr Fontaine/Dr. Fontaine, Jean-Michel și variante de separator, Rousseau, Sophie, Laurent, Besson, Odette; verificare în context, inclusiv rânduri colective, abrevieri și pronume relevante. Inventarul pornește de la cele 11 artefacte K și de la lista exhaustivă a rezumatelor/handoffurilor active fixată de manager pentru noua depunere. | 11/11 artefacte de bază consemnate, inclusiv cele fără rezultat; N/N rezumate/handoffuri active identificate în inventarul real și citite; fiecare ocurență clasată, zero ocurențe active neanalizate. N se fixează din inventar, nu este inventat acum. |
| T4 — actual versus istoric | Clasificare: afirmație operațională activă / citat al erorii sau raport de remediere / probă istorică înghețată. Verificare a predării textuale a P-EDITOR și a rezumatelor ce pot fi consumate în continuare. | Zero afirmații active care atribuie hotelul/Dr Fontaine lui Marcel sau custodia lui Jean-Michel jurnalistei Sophie. Mențiunile istorice ale erorii rămân etichetate, nu sunt șterse pentru a obține artificial zero rezultate la căutare. |
| T5 — conservarea reconcilierilor | Comparație r02→r03 pentru toate H-C1–H-C16/H-N1–H-N6, inclusiv subcazurile; diferență semantică citită de P-EDITOR și de manager, nu numai existența titlurilor/ID-urilor. | 22/22 ID-uri păstrate și confruntate; zero schimbări semantice neautorizate; fiecare diferență încadrată în F01 sau metadate/trimiteri. Vârsta Marcel, calendarul și cele două ceasuri neschimbate. |
| T6 — versiuni și intrări | Verificarea celor trei titluri/metadate r03, a trimiterilor B↔D↔O, a localizărilor recalculate și a intrărilor de revizie. | Exact trei componente editoriale r03 coerente; zero referințe funcționale reziduale către r02 prezentat drept produs activ; zero hashuri fictive sau nepotrivite. Istoricul r02 rămâne accesibil ca istoric. |
| T7 — integritate și confinare | Hashuri înainte/după pentru părinții r02, F/H, contract și alte intrări înghețate; inventarul exact al scrierilor autorizate pentru noua etapă. | Zero modificări ale surselor/r02/rapoartelor/contractului r01; zero editări site/strategie; zero proză/G02 și zero subagenți. Orice abatere oprește depunerea și este raportată. |
| T8 — evidență de predare | Recitire finală, raportul de diferențe și rezultatele de producție, hashuri după ultimul edit; verificarea că fișierele depuse sunt chiar cele testate. | Fiecare test are intrare și rezultat observabil; niciun rezultat completat doar din intenție. Predarea nu declară finding închis, G01 acceptat sau QA favorabil. |

Lista contractuală inițială pentru T3: B, D, O, REGISTRU_DREPTURI_r01.md, TRASABILITATE_DEPUNERE_r01.md, F, CRONOLOGIE_OBSERVATA.md, CONTRADICTII.md, JURNAL_LECTURA.md, MATRICE_SURSE_r01.md și LECTURA_AUXILIARE_MANAGER_r01.md, la căile exacte din K. Managerul va arăta care sunt înlocuite în noua depunere și care rămân surse păstrate. Nu se omite un fișier pentru că nu conține Marcel și nu se confundă lista celor 11 cu totalitatea handoffurilor active.

Dacă un rezumat/handoff înghețat conține eroarea, se păstrează originalul și se propune, prin responsabilul său și după autorizare, un nou rezumat care îl înlocuiește explicit pentru lucru. P-EDITOR nu repară registrele sau mesajele istorice ale altora. O căutare fără rezultate nu înlocuiește lectura semantică a corespondențelor.

## 7. Rezultat de producție versus acceptare

Rezultat de producție urmărit, încă neobținut: trei componente r03 DRAFT coerente, nomenclator fără afilierea eronată, toate rezumatele active verificate, 22 de dispoziții conservate semantic și integritate demonstrată. Producătorul poate declara numai executarea și rezultatele propriilor controale după ce acestea au avut loc.

Închiderea F01 necesită depunere nouă și retest independent pe contractul nou, nu acest plan ori acordul informal asupra corecției. Conform cadrului păstrat: fiecare criteriu trebuie să depășească strict 950, zero findinguri deschise, audituri și metaaudit valide, plus arhivare/decizie de poartă. Nu este acordată nicio notă și nu este anticipată acceptarea. Rezultatele unui alt auditor nu compensează constatarea deschisă.

QA poate cere alte măsuri sau o revizie de raport primar. Producătorul va trata cererea printr-un caz explicit și prin mandatul următor, fără a rescrie raportul auditorului și fără a altera semantic cele 22 de decizii sub eticheta F01.

## 8. Predarea actuală și scrieri oprite

Efectuat acum: lectura integrală a celor șapte intrări textuale indicate, lectura directă a celor 41 de paragrafe H, confruntarea O L92/F L92, identificarea contractuală și pregătirea acestui plan. Nu au fost executate M1–M8 sau T1–T8 pe un produs remediat.

Rămân OPEN findingul și neacceptat G01. Controlul separat P-CANON este PENDING la punctul de verificare declarat; nu pretind rezultat sau integrare. Nu pretind închiderea/arhivarea rundei, verdict QA ori activarea r03.

Unica scriere este acest plan. B/D/O r02, F, H, rapoartele, contractul, registrele existente, site-ul și strategia rămân nemodificate de P-EDITOR. După verificarea finală read-only și calcularea hashului planului, scrierile se opresc la predare. Nu se continuă automat cu r03. Hashul final se comunică în predare, fără auto-hash în corp.
