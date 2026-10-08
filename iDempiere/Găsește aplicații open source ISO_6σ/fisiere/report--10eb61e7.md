# Analiza soluțiilor de management al calității pentru Eva Accounting și iDempiere

Raport pentru conducere și echipa IT • 8 octombrie 2026 • versiunea 1.0

## 1 Concluzia și decizia propusă

Pentru cerința de integrare completă cu iDempiere, recomandăm dezvoltarea unui modul QMS nativ peste componentele existente în EVA, completat cu R pentru analiza statistică Six Sigma. Aceasta este o soluție de construit, nu un produs complet deja disponibil. Codul consultat confirmă iDempiere 13, HR AMERPSOFT și un registru propriu de documente emise. Reutilizarea lor reduce duplicarea angajaților, firmelor și documentelor. [P01] [P02] [P03] [P07]

Pentru o aplicație QMS externă, prima opțiune de evaluat este OCA Management System pe Odoo Community. Are cea mai apropiată acoperire documentată de manual, audituri și neconformități dintre candidații comparați. ERPNext este alternativa pentru inspecții și procese operaționale, dar presupune încă un ERP. BookStack este potrivit pentru redactarea manualului; Logilite DMS este o extensie documentară iDempiere cu compatibilitate 13 neverificată; R este motor statistic, nu QMS. [O01–O10] [E02–E06] [B01–B08] [D01–D04] [R01–R05]

| Prioritate de evaluare | Soluție | Rolul real | Limita decisivă |
|---|---|---|---|
| 1 | OCA Management System | QMS modular și manual de calitate | Conectorul EVA trebuie dezvoltat |
| 2 | ERPNext și Frappe HR | Inspecții, obiective, acțiuni și instruire | Două ERP-uri și două modele de persoane |
| 3 | BookStack | Manual și proceduri accesibile în browser | Aprobările QMS și competența cer dezvoltare |
| 4 | Logilite DMS | Gestiune documentară în iDempiere | Nu este QMS complet; portarea pe 13 trebuie probată |
| 5 | R qcc și SixSigma | SPC, capabilitate și analize Six Sigma | Fără manual, HR sau fluxuri CAPA |

Ordinea reprezintă adecvarea funcțională pentru cerință, nu un benchmark de viteză. Nu s-au măsurat performanțe, concurență sau timpi de răspuns. Niciuna dintre cele cinci variante nu are, în dovezile consultate, un conector gata de instalat care să garanteze integrarea completă cu EVA. Nu recomandăm achiziția ori implementarea pe baza unei promisiuni de integrare de 100% înaintea testelor din capitolul 13.

## 2 Domeniul analizei și interpretarea gratuității

Raportul compară software disponibil cu sursă deschisă, autogăzduire și fără taxă obligatorie de licență pentru componentele analizate. Gratuitatea licenței nu elimină costurile de implementare, servere, actualizări, securizare și suport. Edițiile cloud comerciale și modulele proprietare nu sunt presupuse incluse. Licența exactă trebuie păstrată pentru fiecare versiune instalată și pentru dependențele sale.

Integrare completă înseamnă aici: identitate unică a persoanelor, separarea firmelor și cabinetelor, trasabilitate de la procedură la instruire și rezultat, documente aprobate și istoric, sincronizare verificabilă și scriere în ERP prin mecanismele lui. SSO singur nu reprezintă integrare HR. Un link către o pagină nu reprezintă control al reviziilor.

Analiza este documentară și include inspecție de cod. Nu s-au instalat aplicațiile, nu s-au accesat baza de date ori serviciile de producție și nu s-a validat configurația instalată. Funcțiile marcate ca existente sunt susținute de documentație sau cod, nu de un test de acceptanță în mediul EVA. Nu presupunem că o funcție nedocumentată este imposibilă.

| Simbol | Semnificație |
|---|---|
| N | Funcție nativă documentată în componenta analizată |
| C | Configurare sau modelare folosind funcții existente |
| A | Modul suplimentar open source sau componentă separată |
| D | Dezvoltare ori integrare necesară |
| U | Neconfirmat în sursele consultate |
| — | În afara rolului aplicației |

Combinațiile arată condiții diferite, nu niveluri de performanță. De exemplu U/D înseamnă că funcția nu este confirmată și trebuie bugetată ca dezvoltare până la o demonstrație. Matricele sunt detaliate în fișa fiecărui produs; sursele sunt identificate în text și în registrul final. Registrul acoperă toate sursele folosite sau încercate în această analiză, nu toate paginile existente pe internet.

## 3 Ce există efectiv în EVA

Referința analizată este repository-ul privat cesiroproduction/Eva-Accounting, commit 1c039193e0c1626cb03fb8ca37f9980a1703fd0c. Constatările descriu această versiune a codului. Documentele istorice din repository nu confirmă singure starea producției.

| Componentă | Dovadă | Implicație pentru QMS |
|---|---|---|
| iDempiere 13 | README și imaginile 13 din compose | Pluginul trebuie compilat și testat pentru 13 |
| Interfață principală ZK | Plugin com.eva.ro.contab; backend și frontend descrise ca dormant | Interfața QMS nativă este o extensie firească |
| HR AMERPSOFT | AMN_Employee și AMN_Contract; istoric HR_Employee și HR_Movement | AMN și C_BPartner trebuie să rămână surse de identitate |
| Punte HR | PunteAMN folosește C_BPartner_ID și context AD_Client | Mapare per firmă și verificare de idempotență |
| Utilizatori | AD_User pentru acces și contacte | Angajatul și contul de autentificare sunt concepte distincte |
| Registru SSM | EVA_SsmEvidenta cu Salariat și Responsabil text | Numele text nu este o cheie sigură pentru trasabilitate |
| Documente emise | EVA_DocEmis, hash SHA256, sursă, partener, snapshot și HTML atașat | Componentă reutilizabilă pentru dovada documentului emis |
| Scrieri ERP | Reguli pentru PO, procese native și REST | Fără scrieri SQL directe ale conectorului în tabelele de business |

Surse pentru tabel: [P01–P08]. README conține și descrieri mai vechi despre gateway și aplicații web; alegerea arhitecturii trebuie raportată la pluginul ZK curent și confirmată în mediul de test, nu dedusă din secțiuni istorice.

### 3.1 Persoana și contul de acces

WAngajatiForm leagă C_BPartner de AMN_Employee și de nomenclatoarele AMN pentru post și locație; AD_User este folosit pentru contacte. PunteAMN conține un filtru care exclude partenerii cu utilizator având parolă, pentru a evita conturile tehnice. Dacă se adaugă conturi QMS pentru angajați, trebuie testat dacă această regulă îi exclude din fluxul punții. Este un risc observat în cod, nu o afirmație că producția are deja acest defect. [P04] [P05]

QMS trebuie să stocheze identificatorul angajatului și al partenerului, separat de utilizatorul care a aprobat sau înregistrat evenimentul. Plecarea unui angajat dezactivează accesul și alocările viitoare, dar păstrează instruirile, semnăturile interne și responsabilitățile istorice.

### 3.2 Ce nu dovedește registrul documentelor

RegistruDocumente produce documente cu serie, număr, sursă, stare și hash; codul include protecții pentru anumite modificări și anulare. Acest lucru nu dovedește existența aprobării manualului, a unei revizii controlate de procedură, a confirmării nominale de citire ori a semnăturii electronice calificate. Un hash verifică integritatea față de o valoare de referință; nu dovedește singur autorul și momentul semnării. [P07]

EVA_PartenerID și referințele sursă trebuie validate ca relații în schema efectivă. Câmpul Salariat din SSM este text, astfel că raportarea după nume poate confunda persoane și nu poate substitui relația AMN_Employee/C_BPartner. [P06] [P07]

## 4 Matricea funcțiilor

### 4.1 Manualul și controlul documentelor

| Funcție efectivă | OCA | ERPNext | BookStack | DMS | R |
|---|---|---|---|---|---|
| Șablon de manual de calitate | N | C | C | U | — |
| Proceduri și instrucțiuni | N | N | N | C | — |
| Editare prin browser | N | N | N | U | — |
| Revizii ale documentului | A | C | N | N | D |
| Afișarea ultimei versiuni aprobate | A | D | D | U | — |
| Aprobare de document pe roluri | A | C | D | U | — |
| Citire nominală a unei revizii | D | D | D | D | — |
| Dovadă arhivată la emitere | D | D | D | U/D | D |
| Semnătură electronică calificată | U | U | U | U | — |

OCA necesită în special document_page_approval pentru controlul aprobării paginilor. BookStack are istoric de revizii și permisiuni, dar acestea nu echivalează cu aprobarea QMS și distribuția controlată. „Revizii” la DMS se referă la DMS_Version; comportamentul exact pe iDempiere 13 nu a fost testat. [O03] [O07] [E02] [B01–B08] [D02] [D03]

### 4.2 Audituri și îmbunătățire

| Funcție efectivă | OCA | ERPNext | BookStack | DMS | R |
|---|---|---|---|---|---|
| Audituri ale sistemului | N | U/D | D | U/D | — |
| Neconformitate cu responsabil | N | U/D | D | U/D | — |
| Analiza cauzelor | N | C | D | U/D | C |
| Acțiuni corective | N | N | D | U/D | — |
| Termen și responsabil de acțiune | N | C | D | U/D | — |
| Urmărirea eficacității | A | C/D | D | U/D | D |
| Analiza de management | N | C | D | U/D | — |
| Risc operațional și registru dedicat | U/D | U/D | D | U/D | C |
| Registru metrologie și scadențe | U/D | U/D | D | U/D | — |

Quality Action și Quality Review din ERPNext nu sunt presupuse echivalente cu o suită completă de audit ISO și CAPA. Pentru OCA, câmpurile și modulele suplimentare trebuie selectate împreună, nu deduse din simpla instalare a mgmtsystem_quality. [O02] [O04] [O05] [O08] [O09] [E04] [E05]

### 4.3 HR și competențe

| Funcție efectivă | OCA | ERPNext | BookStack | DMS | R |
|---|---|---|---|---|---|
| Componentă HR în ecosistem | A | A | — | — | — |
| Departament pe neconformitate | A | D | — | U/D | — |
| Evenimente și rezultate de instruire | U/A | A | D | D | — |
| Conector AMN_Employee gata de utilizare | U | U | U | U | U |
| Relație cu persoana din EVA | D | D | D | C/D | D |
| Competență pentru revizie și operație | D | D | D | D | — |
| Dezactivare sincronizată | D | D | D | C/D | — |
| Păstrarea postului istoric în dovezi | D | D | D | D | — |

mgmtsystem_nonconformity_hr adaugă legătura cu departamentul, nu un conector pentru AMERPSOFT. Frappe HR este un proiect separat și oferă Employee, Training Event și Training Result. Identitatea și drepturile EVA cer integrare în toate variantele externe. [O06] [E07–E10] [P03–P06]

### 4.4 Rezultate și Six Sigma

| Funcție efectivă | OCA | ERPNext | BookStack | DMS | R |
|---|---|---|---|---|---|
| Obiective de calitate | N | N | D | U/D | C |
| Inspecții de intrare și ieșire | U/D | N | — | U/D | — |
| Legături cu documente ERP proprii | A/C | N | — | C/D | D |
| Legare la lot și operație din EVA | D | D | D | D | D |
| Grafice SPC | U/D | U/D | — | — | N |
| Capabilitate proces | U/D | U/D | — | — | N |
| Gage R and R | U/D | U/D | — | — | N |
| Analiză înainte și după acțiune | C/D | C/D | D | D | C |
| Decizie de acceptare în EVA | D | D | D | D | D |

În coloana R, N înseamnă funcții de calcul în pachete, nu ecrane și fluxuri instalabile pentru operatori. Parametrii, selecția loturilor, validarea datelor și integrarea sunt dezvoltări distincte. [E03] [E06] [R01–R05]

### 4.5 Integrare și exploatare

| Funcție efectivă | OCA | ERPNext | BookStack | DMS | R |
|---|---|---|---|---|---|
| API în platformă | N | N | N | U | A |
| Evenimente către aplicații externe | D/A | N | N | D | D |
| Aceeași platformă iDempiere | D | D | D | N/C | D |
| Respectarea modelului exact de firme EVA | D | D | D | C/D | D |
| Conector complet EVA documentat | U | U | U | U | U |
| Licență open source pentru varianta evaluată | N | N | N | N | N |

API disponibil nu înseamnă mapare de business gata făcută. Webhook-urile Frappe și BookStack nu rezolvă automat autentificarea, reîncercarea, ordinea mesajelor sau separarea firmelor. În R, API-ul se poate construi cu plumber. [O13] [E11–E14] [B05] [B07] [R05]
## 5 OCA Management System pe Odoo Community

### 5.1 Funcții și module efective

OCA publică un ansamblu de module, nu un executabil QMS autonom. Pentru această analiză a fost consultată ramura 18.0. Modulul mgmtsystem_quality este AGPL 3; distribuția finală trebuie să păstreze licențele individuale și dependențele. Odoo Community poate fi autogăzduit; funcții din Enterprise nu sunt incluse în recomandare. [O01] [O02] [O11] [O12]

| Modul | Ce face efectiv | Ce mai trebuie pentru EVA |
|---|---|---|
| document_page_quality_manual | Structură de manual de calitate | Adaptarea proceselor și aprobarea conținutului firmei |
| mgmtsystem_quality | Reunește funcții de sistem al calității | Selectarea și configurarea modulelor |
| mgmtsystem_nonconformity | Descriere, origine, responsabil, cauze, analiză și plan de acțiune | Mapare lot, operație, persoană și firmă EVA |
| mgmtsystem_audit | Evidența auditurilor sistemului | Program și checklist adaptate standardului aplicabil |
| mgmtsystem_nonconformity_hr | Asociere de departament | Angajat AMN și istoric de post |
| document_page_approval | Aprobare de pagini și acces la versiunea aprobată | Dovezi nominale de citire și instruire |
| mgmtsystem_action_efficacy | Urmărirea eficacității acțiunii | Indicatori calculați din rezultatele EVA |
| mgmtsystem_review | Analize de management | Indicatori și documente justificative |
| mgmtsystem_nonconformity_product | Legătură cu produsul | Mapare cu M_Product și lotul din EVA |

Surse: [O02–O10]. Manualul disponibil este un punct de pornire; nu este dovada acoperirii unei ediții de standard sau a conformității firmei. O neconformitate poate avea referință la o comandă ori sarcină, dar referința liberă trebuie înlocuită sau completată cu identificatori pentru trasabilitate.

### 5.2 Integrare propusă

EVA rămâne sursa pentru firme, persoane, produse, documente și rezultate. Odoo primește copii minimale și chei externe, fără a deveni al doilea sistem de salarizare sau de stocuri. Conectorul va utiliza API-ul Odoo/RPC și API-ul ori procesele iDempiere. Codul RPC al Community este o dovadă tehnică; condițiile comerciale ale serviciilor Odoo găzduite nu trebuie confundate cu autogăzduirea Community. [O12] [O13] [I01–I04]

Neconformitatea poate fi administrată în OCA, dar starea lotului trebuie modificată în EVA printr-un proces validat. La aprobarea procedurii se arhivează în EVA o reprezentare stabilă cu hash și identificator de revizie. Identificatorii Odoo nu se folosesc ca identificatori ai angajaților EVA.

### 5.3 Verdict

Este candidatul extern cel mai potrivit pentru manual, audituri și neconformități. Dezavantajul principal este exploatarea a două platforme și construirea legăturilor cu AMN, documentele și rezultatele. Nu există în dovezile consultate o extensie OCA care să rezolve direct această integrare EVA. Descărcare și documentație: [O01–O14].

## 6 ERPNext și Frappe HR

### 6.1 Funcții efective

ERPNext este un ERP open source, GPL 3, cu funcții de calitate. Frappe HR este separat; includerea lui trebuie decisă explicit pentru a nu duplica salarizarea AMN. Instalarea poate folosi proiectul frappe_docker și versiuni compatibile fixate împreună. [E01] [E07] [E13]

| Funcție | Comportament documentat | Limita pentru cerința EVA |
|---|---|---|
| Quality Procedure | Proceduri de calitate structurate | Manualul complet și controlul distribuției se configurează |
| Quality Goal | Obiective și indicatori | Rezultatele EVA trebuie importate |
| Quality Review | Revizuirea obiectivelor și urmărire periodică | Nu dovedește întregul proces de analiză ISO |
| Quality Action | Acțiuni legate de probleme și îmbunătățire | CAPA și închiderea bazată pe eficacitate trebuie modelate |
| Quality Inspection | Parametri, criterii și inspecții de intrare sau ieșire | Legături native cu documentele ERPNext, nu automat EVA |
| Employee în Frappe HR | Fișa angajatului | Copie subordonată identității AMN |
| Training Event și Training Result | Evenimente și rezultate de instruire | Revizia procedurii și competența pe operație necesită extensie |

Surse: [E02–E10]. Nu am confirmat în modulele analizate un registru complet de audituri ISO, metrologie ori neconformități echivalent OCA; acestea se tratează ca cerințe de modelare/dezvoltare, nu ca funcții cumpărate implicit.

### 6.2 Integrare și exploatare

Frappe expune documentele prin REST, cu autentificare și permisiuni. API v2 este documentat pentru versiuni mai noi ale platformei; conectorul trebuie scris pentru versiunea aleasă. Webhook-urile pot transmite evenimente și pot include o semnătură HMAC; sursa consultată pentru ele este documentație v14 și trebuie reverificată pe versiunea instalată. [E11] [E12] [E14]

Propunerea este ca ERPNext să primească o cerere de inspecție cu cheia lotului EVA, să înregistreze măsurătorile și să returneze rezultatul validat. EVA execută acceptarea sau blocarea lotului. Nu se sincronizează contabilitatea și stocurile între două ERP-uri doar pentru a activa funcțiile de calitate. Evenimentele de HR includ strict identificatorul, numele necesar, departamentul, postul și starea activă.

### 6.3 Verdict

Potrivit dacă inspecțiile operaționale cântăresc mai mult decât manualul și auditurile. Mai puțin atractiv dacă obiectivul dominant este utilizarea unei singure platforme iDempiere. API-ul bun reduce efortul de transport al datelor, dar nu elimină modelarea, validarea și mentenanța integrării. Descărcare, Docker și documentație: [E01–E14].

## 7 BookStack pentru manual și proceduri

BookStack este o aplicație documentară sub licență MIT. Oferă organizare în cărți, capitole și pagini, editare în browser, căutare, revizii, roluri și permisiuni. Este potrivit pentru redactarea și consultarea manualului de calitate. Nu trebuie prezentat ca o suită ISO sau Six Sigma. Repository-ul GitHub consultat indică și mutarea dezvoltării către Codeberg; la instalare se urmează sursa oficială curentă. [B01–B03] [B08] [B09]

### 7.1 Ce face și ce nu face

| Cerință | Acoperire | Consecință |
|---|---|---|
| Manual navigabil | Cărți, capitole, pagini și căutare | Implementare documentară rapidă |
| Istoric editorial | Revizii ale paginilor | Util pentru comparații; nu substituie aprobarea |
| Acces diferențiat | Roluri și permisiuni | Configurare pentru autori, cititori și firme |
| Identitate | Integrare OIDC și alte mecanisme documentate | SSO trebuie corelat cu identitatea HR |
| Aprobare QMS | Flux dedicat neconfirmat | Se construiește în EVA |
| Citire și competență nominală | Funcție QMS neconfirmată | Înregistrare separată per revizie și angajat |
| Audituri și CAPA | În afara rolului de bază | Nu se reduc la pagini cu text |
| Statistică și loturi | În afara rolului de bază | Legături și rezultate gestionate în EVA |

### 7.2 Integrare propusă

API-ul REST poate extrage conținut și metadate; evenimentele se pot transmite prin webhook. OIDC oferă autentificare centralizată, dar nu sincronizează automat AMN_Employee. Evităm bazarea integrării pe personalizări fragile de interfață: documentația „hacking” nu este un contract stabil de API. [B04–B07]

Pentru controlul documentelor, BookStack poate fi spațiul de redactare. Aprobarea în EVA fixează o revizie și o copie arhivată. Angajatului i se atribuie acea revizie, iar confirmarea se înregistrează în QMS. Modificarea ulterioară a paginii nu schimbă dovada istorică. O integrare care deschide doar pagina curentă nu satisface această cerință.

Verdict: opțiune bună pentru ergonomia manualului, ca parte a unui QMS construit în EVA. Nu recomandăm cumpărarea de complexitate suplimentară dacă editorul și registrul EVA pot acoperi deja necesarul. Instalare și documentație: [B01–B10].

## 8 Logilite DMS pentru iDempiere

### 8.1 Dovezi și compatibilitate

Logilite DMS este o extensie de document management pentru iDempiere. Catalogul consultat o prezintă sub GPL v2 și menționează iDempiere 11. Repository-ul și README-ul arată componente DMS și DMS_Version, pași de instalare și migrare. Nu am validat o distribuție funcțională pentru iDempiere 13. [D01–D04]

| Aspect | Constatat | Necunoscut sau de testat |
|---|---|---|
| Integrare în iDempiere | Plugin în ecosistem | Compatibilitate reală cu EVA 13 |
| Documente și versiuni | Entități și migrații DMS | Comportament complet al drepturilor și reviziilor |
| Surse disponibile | Repository și ramuri publice | Build reproductibil cu dependențele actuale |
| Audit, CAPA și instruire | Nu sunt demonstrate ca suită | Dezvoltare QMS suplimentară |
| API propriu | Nu este suficient documentat în materialul consultat | Expunere prin plugin sau REST compatibil |
| Manual PDF | Link identificat | Acces automat blocat; nu fundamentează funcții în raport |

Catalogul și PDF-ul au răspuns 403 la reverificarea automată. Informația de catalog din lectura web anterioară se păstrează cu această rezervă; detaliile verificabile din repository sunt dovezi mai puternice. Ramurile mai vechi nu dovedesc incompatibilitate cu 13, dar nici nu permit declararea compatibilității. [D01] [D05]

### 8.2 Verdict și probă necesară

Avantajul este apropierea de platforma existentă. Riscul este costul de portare și suprapunerea cu EVA_DocEmis. Înainte de adoptare: build pe un mediu separat iDempiere 13, inventarul tabelelor și migrațiilor, verificarea licențelor și a accesului între firme, test de versiuni și restaurare. Nu se rulează scripturile de migrare direct în producție.

DMS poate înlocui sau completa stratul documentar numai dacă aduce beneficii demonstrate. Nu rezolvă automat procedurile aprobate, instruirile, neconformitățile și analiza rezultatelor. Descărcare și documentație: [D01–D05]; dezvoltare plugin iDempiere: [I05] [I06].

## 9 R cu qcc și SixSigma

R este recomandat ca serviciu de analiză pentru QMS-ul nativ. qcc oferă grafice de control, CUSUM, EWMA, Pareto și analize de capabilitate. SixSigma oferă instrumente pentru analiza și îmbunătățirea proceselor, inclusiv Gage R and R. Licențele publicate pentru pachetele consultate sunt GPL de la versiunea 2. Paginile CRAN consultate indică qcc 2.7 și SixSigma 0.11.1; acestea sunt referințe pentru reproducibilitate, nu o promisiune de activitate recentă. [R01–R04]

### 9.1 Contractul de date

| Intrare obligatorie după metodă | De ce este necesară |
|---|---|
| Caracteristică și unitate | Evitarea amestecării măsurătorilor incompatibile |
| Lot, operație și moment | Trasabilitate și ordinea observațiilor |
| Subgrup și plan de eșantionare | Alegerea graficului și estimarea variației |
| Limite de specificație | Calculul capabilității când este aplicabil |
| Instrument, operator și repetare | Studiu de măsurare Gage R and R |
| Valori lipsă, corecții și excluderi | Calcul verificabil fără selecție ascunsă |
| Versiunea metodei și parametrilor | Reproducerea analizei istorice |

Limitele de control nu sunt limite de specificație. Cp/Cpk nu trebuie prezentate automat ca dovadă că un proces este stabil sau că toate ipotezele metodei sunt îndeplinite. Serviciul trebuie să returneze avertismente pentru date insuficiente, unități amestecate ori ipoteze nevalidate; interpretarea este responsabilitatea persoanei desemnate.

### 9.2 Integrare propusă

Un serviciu R construit cu plumber primește setul minim de măsurători și parametri și returnează indicatori, grafice, avertismente, versiunea pachetelor și hash-ul setului analizat. Identificatorii tehnici sunt suficienți; datele salariale nu au rol în calcul. Autentificarea, limitarea cererilor, jurnalizarea, izolarea și publicarea rezultatelor trebuie implementate în serviciu. [R05]

Rezultatul se atașează unei analize în EVA. Acceptarea lotului sau închiderea acțiunii se face printr-un proces autorizat din QMS, nu automat deoarece un indicator depășește un prag. Pachetele nu oferă manual de calitate, HR, aprobări, audituri sau administrarea neconformităților. Instalare și manuale: CRAN și repository-urile [R01–R06]; fișele CRAN includ legăturile către manualele de referință și materialele disponibile.

## 10 Alternative care nu intră în selecția strictă

FlinkISO promovează module de QMS gratuite, dar comparația oficială free versus paid indică un serviciu API plătit pentru crearea formularelor personalizate, la 80 USD pe lună în pagina consultată. Acesta este API-ul de creare de formulare, nu trebuie confundat cu toate API-urile de integrare de date. Instalarea documentată implică înregistrare și cheie. Licența exactă a pachetului descărcabil nu a fost verificată suficient pentru a recomanda fără rezerve varianta ca 100% open source și gratuită pentru personalizarea necesară EVA. [F01–F03]

FlinkISO rămâne o opțiune de reevaluat dacă se acceptă limitele ediției gratuite ori costul personalizării. Afirmațiile furnizorului despre module gratuite nu au fost testate. Manualul general F04 a fost inaccesibil la reverificare și nu susține funcții în matrice.

Hugging Face poate găzdui modele care ajută la redactarea sau căutarea în proceduri. Un model lingvistic nu asigură registrul de revizii, aprobările, HR și dovada rezultatelor. Exemplul H01 a fost identificat, dar accesul automat a eșuat; nu este folosit pentru a recomanda o soluție QMS. Datele de calitate nu trebuie să depindă de răspunsuri generate pentru a păstra dovada unei decizii.
