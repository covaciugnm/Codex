PAGES=[]
def page(title,paras=(),headers=None,rows=(),widths=None,refs=(),after=()):
    PAGES.append(dict(title=title,paras=list(paras),headers=headers,rows=list(rows),widths=widths,refs=list(refs),after=list(after)))

page('Analiza iDempiere HR și SSM SU pentru România',[
'Raport de selecție și integrare pentru echipa proiectului iDempiere și EVA Accounting. Data cercetării: 8 octombrie 2026. Raportul compară baza iDempiere, extensiile HR internaționale, Frappe HR, Axelor HR, Apache OFBiz și platformele SSM.ro, SSMatic și SafeHub.',
'Recomandare: evaluați în paralel, prin aceleași scenarii de acceptanță, o familie HR nativă iDempiere și Frappe HR integrat cu iDempiere. SSM.ro este primul candidat pentru integrarea SSM/SU datorită API-ului public documentat. Alegerea finală rămâne condiționată de probele funcționale și localizarea românească.',
'Nu este demonstrată o soluție unică gratuită integral, stabilă în configurația voastră, cu salarizare românească, SSM/SU și integrare completă gata de utilizare. Licența fără cost nu elimină costurile de operare, adaptare, suport și semnare.',
],['Decizie','Opțiune de evaluat','Motiv'],[
['Păstrarea HR în iDempiere','Familia CDSoftware','Mai multe extensii HR native documentate; compatibilitatea publicată rămâne la versiunea 10.'],
['Alternativă nativă payroll','AMERPSOFT Personnel & Payroll','Actualizare declarată pentru 12; marcată în testare.'],
['HR independent','Frappe HR','Acoperire documentată pentru recrutare, prezență, concedii și payroll configurabil.'],
['HR independent în Java','Axelor HR','Candidat Java relevant; pregătirea payroll nu echivalează cu salarizare românească.'],
['Platformă Java pentru dezvoltare','Apache OFBiz','Bază extensibilă; experiența HR și localizarea cer evaluare tehnică.'],
['SSM/SU integrabil','SSM.ro','Ghid și API public; exportul complet al documentelor trebuie demonstrat.'],
], [0.23,0.28,0.49],['PL01','PL07','FR01','AX01','OF01','SS05'],[
'Dosarul este pregătit pentru consultare și evaluare. Nu constituie o instalare de aplicații, o validare a salarizării sau o certificare de conformitate SSM/SU.'
])

page('Metodă versiuni și niveluri de încredere',[
'Funcțiile sunt evaluate la nivel de familii și fluxuri. Inventarul tehnic al modelelor iDempiere este anexat separat. Activarea fiecărei ferestre și extensii în instalarea beneficiarului necesită un export local; această instalare nu a fost auditată.',
'D = documentat; P = parțial; E = extensie; C = configurare sau dezvoltare; NC = neconfirmat. NC nu înseamnă lipsă. Pentru furnizorii comerciali, declarațiile de pe site sunt separate de documentația tehnică și de testarea efectivă.'
],['Sistem','Baza de verificare','Limită importantă'],[
['iDempiere','Release 13 și codul aferent','Master și release-urile de dezvoltare nu sunt baza recomandării.'],
['CDSoftware','Pagini oficiale de catalog','Testat pe 10.0.0; absența unei mențiuni pentru 13 nu dovedește incompatibilitatea, dar cere probă.'],
['AMERPSOFT','README general și README modul','12 în README general; informații mai vechi în modul; Under Test.'],
['Frappe HR','Manual și release-uri v15/v16','Funcțiile diferă între ramuri; se fixează versiuni compatibile ale dependențelor.'],
['Axelor','Documentație HR inclusiv 8.5; release-uri 9.1.x','Nu se presupune identitate între manual și ediția instalată.'],
['OFBiz','Manual stable și release 24.09.07','Documentația stable se poate actualiza; arhiva păstrează copia consultată.'],
['SSM.ro','Manual operațional și API','Contractul stabilește accesul, semnăturile și condițiile comerciale.'],
['SSMatic și SafeHub','Prezentări și pagini comerciale','Manualele tehnice complete și API-urile generale nu au fost confirmate public.'],
],[0.18,0.34,0.48],['ID14','PL07','FR03','AX04','OF04','SS01','SM02','SH02'])

page('iDempiere organizare securitate și platformă',[
'Aceste funcții formează infrastructura comună a ERP-ului. Utilizarea lor pentru HR implică modelarea datelor și drepturilor specifice; o facilitate generică nu se contabilizează automat ca modul HR complet.'
],['Familie','Funcții și rezultate','Acoperire','Implicație pentru HR'],[
['Organizare','Tenant, organizații și structuri','D standard','Definește companiile și unitățile.'],
['Utilizatori','Conturi, contacte și roluri','D standard','Nu înlocuiește dosarul complet de personal.'],
['Acces','Drepturi pe ferestre, date și procese','D standard','Separarea datelor HR trebuie configurată și testată.'],
['Audit','Istoric și urmărirea modificărilor configurate','D standard','Se verifică exact ce câmpuri și acțiuni sunt înregistrate.'],
['Application Dictionary','Tabele, câmpuri, ferestre, taburi, validări','D standard','Bază pentru extensii; nu funcții juridice gata făcute.'],
['Workflow','Etape, activități și aprobări','D standard','Poate susține cereri și aprobări HR după configurare.'],
['Procese programate','Joburi și procesări periodice','D standard','Poate declanșa sincronizări și notificări.'],
['Comunicare','Email și procesare solicitări','D standard','Configurare și drepturi necesare.'],
['Documente','Atașamente și formate de tipărire','D standard','Nu dovedește arhivă electronică calificată.'],
['Extensibilitate','Pluginuri Java și OSGi','D standard','Avantaj pentru modulele native.'],
['Integrare','Importuri și servicii; REST extins prin plugin','D + E','API-ul se verifică pe versiunea instalată.'],
],[0.18,0.33,0.15,0.34],['ID02','ID03','ID04','ID05','PL15'])

page('iDempiere fluxuri comerciale și logistice',[],['Familie','Funcții','Documente principale','Relație cu HR'],[
['Parteneri','Clienți, furnizori, angajați, contacte','Fișe și adrese','Identificatori și date comune.'],
['CRM și solicitări','Cereri, responsabilități, urmărire','Request și activități','Poate gestiona solicitări interne configurate.'],
['Vânzări','Ofertare, comandă, livrare, facturare','Ofertă, comandă, aviz, factură','Facturarea serviciilor și a timpului.'],
['Achiziții','Necesar, ofertare furnizori, comandă','Requisition, RfQ, PO','Achiziții pentru personal și instruiri.'],
['Recepție și verificare','Recepții și corelarea facturilor','Recepție, factură, matching','Controlul cheltuielilor.'],
['Retururi','Retururi comerciale și corecții','RMA și documente asociate','Utilitate indirectă.'],
['Articole și servicii','Categorii, unități, atribute','Nomenclatoare','Poate înregistra EIP ca articole.'],
['Prețuri','Liste și reduceri','Versiuni de liste','Utilitate financiară.'],
['Depozite','Locații, intrări, ieșiri, transferuri','Mișcări și inventare','Predarea EIP individuală cere flux propriu.'],
['Trasabilitate','Atribute, loturi și serii','Înregistrări de trasabilitate','Nu echivalează cu autorizări profesionale.'],
['Reaprovizionare','Reguli de completare stoc','Necesar generat','Poate susține aprovizionarea EIP.'],
],[0.18,0.32,0.24,0.26],['ID02','ID03','ID04'])

page('iDempiere finanțe proiecte active și producție',[],['Familie','Funcții','Acoperire','Limită sau implicație'],[
['Contabilitate','Scheme, perioade, note și dimensiuni','D standard','Contabilizarea HR depinde de evenimentele și regulile implementate.'],
['Valute și taxe','Cursuri și configurări fiscale','D standard','Nu dovedește localizare românească integrală.'],
['Încasări și plăți','Bancă, casă și alocări','D standard','Exportul bancar concret se testează.'],
['Creanțe și datorii','Solduri și vechime','D standard','Poate gestiona decontări cu angajați.'],
['Costuri','Costuri produse și costuri suplimentare','D standard','Integrarea costului salarial pe centre se proiectează.'],
['Raportare','Rapoarte contabile configurabile','D standard','Indicatorii HR cer date și rapoarte specifice.'],
['Active fixe','Evidență și amortizare','D standard','Nu înlocuiește verificările tehnice obligatorii.'],
['Proiecte','Faze, activități și costuri','D standard','Legătură cu orele și cheltuielile personalului.'],
['Timp și cheltuieli','Ore de proiect și deconturi','D standard','Nu reprezintă pontaj complet cu ture.'],
['Resurse','Disponibilitate și alocare','D standard','Nu reprezintă solduri de concediu.'],
['Producție de bază','BOM, consumuri și producție','D standard','Nu se confundă cu o suită MRP/MES completă.'],
['Planificare industrială extinsă','Libero și alte extensii','E','Se inventariază separat de nucleu.'],
],[0.19,0.32,0.14,0.35],['ID02','ID03','ID04','ID09','ID10'])

page('Ce există deja în baza HR iDempiere',[
'Verificarea codului release 13 completează evaluarea funcțională inițială: iDempiere are structuri pentru poziții, atribuiri și remunerații. Sunt prezente și interfețe de model HR moștenite. Existența unei clase generate sau a unei tabele nu dovedește un proces de salarizare complet, disponibil și întreținut.',
'Anexa tehnică fixează commitul verificat și listează interfețele de model. Fragmentele HR au fost descărcate pentru verificare independentă.'
],['Structură','Ce dovedește sursa','Ce nu dovedește'],[
['C_BPartner și conturi angajat','Angajatul poate avea identitate de partener și conturi asociate.','Dosar HR complet sau CIM românesc.'],
['C_Job și C_JobCategory','Poziții și categorii de poziții.','Organigramă HR avansată gata configurată.'],
['C_JobAssignment','Atribuiri de persoane pe poziții și valabilitate.','Onboarding și toate schimbările contractuale.'],
['C_Remuneration','Nomenclator de remunerații.','Calcul net și obligații fiscale.'],
['C_JobRemuneration','Asocieri remunerație și poziție.','Un stat de plată legal pentru România.'],
['C_UserRemuneration','Evidență remunerație asociată persoanei.','Un motor complet de payroll.'],
['I_HR_Employee și I_HR_Department','Modele de date HR în codul bazei.','Meniu activ și flux utilizabil fără extensii.'],
['I_HR_Payroll, I_HR_Process și I_HR_Movement','Structuri de date salariale.','Executarea motorului și rapoartelor unei extensii.'],
['Expense Report','Ore de proiect și cheltuieli.','Prezență, ture și solduri de concediu.'],
],[0.28,0.36,0.36],['ID14','ID16','ID09','CODE001','CODE002','CODE003','CODE004','CODE005','CODE006','CODE007'],[
'Pentru inventarul exact al instanței: exportați meniurile, ferestrele, procesele, tabelele și lista pluginurilor. Scriptul SQL de lectură este inclus în anexă; nu a fost executat pe producție.'
])

page('Familia CDSoftware pentru iDempiere',[
'Familia este relevantă deoarece extinde direct ERP-ul existent. Sursele publice indică GPLv2 și testare pe 10.0.0 pentru cele cinci module documentate mai jos. Recomandarea este de evaluare, nu de instalare imediată în producție.'
],['Modul','Funcții documentate','Dependențe și limitări','Dovadă'],[
['Payroll','Angajați, departamente, poziții, concepte și perioade; multivalută și împrumuturi contabilizate.','Base și DetailNames; exemple pentru Panama.','PL01'],
['Attendance','Import TXT, formate HIKVISION, ture rotative și întârzieri.','Se verifică formatul concret al terminalelor și regulile locale.','PL02'],
['EmployeeTraining','Planificarea și urmărirea instruirilor.','Depinde de Payroll; nu dovedește SSM/SU românesc.','PL03'],
['EmployeeRecruitment','Recrutare și selecție.','Payroll și Training; descriere publică redusă.','PL04'],
['PayrollReport','Rapoarte cu coloane multiple și exporturi configurabile.','Payroll și Attendance.','PL05'],
['PerformanceEvaluation','Nume prezent în catalog.','Funcțiile, licența și compatibilitatea nu au fost confirmate individual.','PL06 / ID10'],
],[0.21,0.36,0.33,0.10],['PL01','PL02','PL03','PL04','PL05','PL06','ID10'],[
'Payroll Contract include definiții ale frecvenței salarizării; denumirea nu trebuie echivalată automat cu un contract individual de muncă. Verificarea pe versiunea țintă trebuie să includă build, 2Pack/migrări, reguli, rapoarte și contabilizare.',
'Paginile wiki cu descărcare refuzată rămân în registru cu starea lor reală. Linkurile Sources din paginile oficiale sunt puncte de intrare, nu arhive de cod declarate ca recuperate.'
])

page('Alte extensii și implementări internaționale',[],['Candidat','Dovada disponibilă','Situație','Utilitate pentru proiect'],[
['AMERPSOFT Personnel & Payroll','Repository, README și PDF','Versiunea 12 declarată în testare; licență de clarificat.','Alternativă nativă de payroll.'],
['Ingeint Payroll','Intrare în catalog','Disponibilitatea actuală a sursei și mentenanța sunt neconfirmate.','Contact cu mentenorul înainte de selecție.'],
['Ingeint Human Talent','Repository Java','Manual și release-uri insuficient documentate.','Explorare tehnică, nu soluție validată.'],
['Libero Payroll vechi','Pagina declară neîntreținerea','Istoric; înlocuit în catalog de Ingeint.','Referință, nu bază recomandată nouă.'],
['iDempiere Taiwan Mobile','Ofertă HR mobilă','Funcții declarate; licență, distribuție și proveniență de verificat.','Pistă pentru portal mobil și aprobări.'],
['Exvee ERP de la 17tek','Furnizor din Vietnam, bazat pe iDempiere','Ofertă comercială cu HR/payroll declarat.','Pistă globală; nu plugin gratuit verificat.'],
['ADempiere HR/Payroll','Proiect și release-uri distincte','Alt produs, chiar dacă există origine comună.','Portare sau studiu de implementare.'],
['Localization Romania','Traducere și plan de conturi','Pagină în progres, actualizare indicată în 2020.','Nu dovedește salarizare ori SSM.'],
],[0.23,0.27,0.27,0.23],['PL07','PL08','PL10','PL11','PL12','PL13','PL14','PL18','PL19'],[
'Nu se recomandă combinarea implicită a două motoare native de salarizare. AMERPSOFT utilizează tabele AMN_; armonizarea cu alt motor trebuie proiectată explicit. Java comun nu garantează compatibilitatea bazelor de date sau a API-urilor.'
])

page('Cum selectăm un plugin HR nativ',[
'Un plugin se acceptă după probe, nu numai după pagina de catalog. CDSoftware și AMERPSOFT sunt candidați de pilot. Informațiile publice nu justifică un clasament numeric de stabilitate sau procent de acoperire.'
],['Control','Ce se verifică','Criteriu de acceptanță'],[
['Licență','Fișierul licenței și dependențele exacte','Utilizarea și modificarea dorite sunt permise.'],
['Compatibilitate','Versiune iDempiere, Java, PostgreSQL/Oracle, OSGi','Build și instalare reproductibile într-un mediu de test.'],
['Migrare','Tabele, Application Dictionary, 2Pack, rollback','Migrarea nu pierde date și poate fi repetată controlat.'],
['Calcul','Reguli, rotunjiri, perioade, corecții','Rezultate comparate cu exemple românești validate.'],
['Contabilitate','Conturi, centre de cost, reversări','Totalurile și notele se reconciliază.'],
['Pontaj','Ture, noapte, lipsă pontare, import repetat','Fără dubluri și fără ore incorect alocate.'],
['Documente','Formate, versiuni și export','Documentele cerute se produc și rămân recuperabile.'],
['Mentenanță','Release-uri, probleme și răspunsul mentenorului','Există responsabilitate pentru update-uri și remedieri.'],
['Localizare','CIM, fiscalitate, D112, REGES, SSM/SU','Fiecare cerință are implementare sau integrare demonstrată.'],
],[0.19,0.40,0.41],['PL01','PL07','PL08','PL15'])

page('Cele trei aplicații HR profil și costuri',[],['Criteriu','Frappe HR','Axelor HR','Apache OFBiz'],[
['Tehnologie','Python și JavaScript','Java','Java și componente proprii'],
['Licență examinată','GPLv3 în sursă','AGPLv3','Apache 2.0'],
['Instalare proprie','Da','Da, Community','Da'],
['Tip de produs','Aplicație HR pe Frappe','Modul într-o suită ERP','Modul într-o platformă ERP'],
['Punct forte','Acoperire HR și self-service','HR în Java și extensibilitate','Bază Java și licență permisivă'],
['Compromis pentru iDempiere','Încă o platformă tehnică','Suprapunere ERP','Mai multă adaptare HR'],
['Payroll România','NC','NC','NC'],
['SSM/SU România','NC','NC','NC'],
['Costuri dincolo de licență','Hosting, integrare, suport și localizare','Aceleași; delimitați serviciile comerciale','Aceleași; dezvoltare proprie mai importantă'],
],[0.23,0.26,0.26,0.25],['FR02','FR13','AX02','AX11','AX12','AX14','OF05','OF06'],[
'Acest trio este o selecție pentru cerințele proiectului, nu un top absolut al tuturor produselor HR. Preferința Java justifică includerea Axelor și OFBiz; Frappe este reperul funcțional. Nu a fost identificat un candidat de pe Hugging Face care să schimbe selecția fundamentată pe repository-uri și manuale oficiale.'
])

page('Matrice HR administrare și recrutare',[],['Funcție','iDempiere bază','Frappe HR','Axelor HR','OFBiz'],[
['Identitate angajat','D, partener/contact','D','D','D'],
['Dosar personal extins','P și modele HR','D','D','D'],
['Poziții și atribuiri','D','D','D','D'],
['Departamente HR','Structură și modele; flux de verificat','D','D','D'],
['Contracte de muncă','C/E pentru flux complet','D/P; localizare','D; localizare','D/P'],
['CIM și acte RO','C','C','C','C'],
['Recrutare','E','D','D','D'],
['Interviuri și feedback','E','D','P; verificare','NC'],
['Onboarding și ieșire','E/C','D','P','NC'],
['Transfer și promovare','Atribuiri de bază; E/C','D','P','P'],
['Competențe și calificări','E/C','D','D','D'],
],[0.28,0.21,0.17,0.17,0.17],['ID16','FR04','FR05','FR01','AX06','AX07','OF01'],[
'D indică documentare la nivel de produs. Nu confirmă prezența în orice ediție sau versiune și nu confirmă forma legală românească a documentelor.'
])

page('Matrice HR timp dezvoltare și acces angajat',[],['Funcție','iDempiere bază','Frappe HR','Axelor HR','OFBiz'],[
['Concedii și cereri','E/C','D','D','D'],
['Politici și solduri','E/C','D','D','De verificat'],
['Check-in și prezență','E','D','De verificat','NC'],
['Terminale pontaj','E','Integrare documentată','NC','NC'],
['Ture','Resurse; E pentru HR','D','Planificări; P','NC'],
['Ore de proiect','D','D, cu dependențe','D','Project Manager'],
['Ore suplimentare','E/C','Versiune/configurare','D','NC'],
['Deconturi','D','D','D','Flux de verificat'],
['Evaluarea performanței','E','D','D','D'],
['Instruire','E','D','D','D'],
['Portal angajat','E/C','D','D','NC comparabil'],
['Mobil HR','E','PWA','Aplicație; ediția de verificat','NC'],
],[0.28,0.21,0.17,0.17,0.17],['ID09','FR01','FR06','AX01','AX09','AX13','OF01'])

page('Matrice HR salarizare și localizare',[],['Funcție','iDempiere bază','Frappe HR','Axelor HR','OFBiz'],[
['Remunerație de referință','D','D','D','D/P'],
['Motor salarial complet','Structuri; extensie de validat','D configurabil','Pregătire/export','De verificat'],
['Componente și formule','E pentru proces operațional','D','Bonusuri și pregătire','P/C'],
['Fluturaș din calcul','E','D','Nu se deduce din export','De verificat'],
['Procesare colectivă','E','D','Pregătire în lot','De verificat'],
['Contabilizare salarii','E și configurare','D cu contabilitatea configurată','Integrare payroll','C'],
['Bonusuri și beneficii','E','D','D','D/P'],
['Stat de plată RO','C/localizare','C/localizare','Integrare/localizare','C/localizare'],
['D112','NC','NC','NC','NC'],
['REGES-ONLINE','NC','NC','NC','NC'],
['Conformitate SSM/SU RO','NC','NC','NC','NC'],
],[0.26,0.24,0.18,0.18,0.14],['FR07','FR08','FR09','AX08','OF01','CODE004','CODE005','CODE006'],[
'Frappe are un circuit documentat de calcul și fluturași; aceasta nu validează fiscalitatea românească. Axelor documentează colectarea variabilelor și exportul payroll, inclusiv către soluții externe. Aceste două niveluri nu sunt echivalente.'
])

page('Evaluarea aplicațiilor HR pentru proiect',[
'Frappe HR este prima aplicație separată pe care aș testa-o: manualul acoperă un ciclu HR extins, iar API-ul permite integrarea. Beneficiul se confirmă numai dacă portalul și procesele reduc munca manuală suficient pentru a justifica a doua platformă.',
'Axelor este prima alternativă separată dacă Java devine cerință obligatorie. Verificați funcțiile efective ale ediției Community și costul migrărilor. Un export payroll nu trebuie prezentat ca înlocuitor al unei soluții românești de salarizare.',
'OFBiz este potrivit când echipa acceptă un proiect de dezvoltare și adaptare pe Java. Nu există în această analiză suficiente dovezi pentru a-l declara egal cu Frappe la pontaj mobil sau self-service HR.'
],['Aspect','Decizie recomandată'],[
['Prioritate funcțională HR','Frappe HR pe lista scurtă.'],
['Prioritate tehnologică Java','Axelor, apoi OFBiz, cu costul de integrare estimat separat.'],
['Prioritate aplicație unică','Pilot CDSoftware versus AMERPSOFT înaintea unui al doilea ERP.'],
['Prioritate payroll România imediat','Păstrarea sau integrarea unui motor local validat până la validarea celui nou.'],
['Prioritate gratuit integral','Nu există dovadă pentru un pachet complet care să elimine implementarea și serviciile.'],
],[0.34,0.66],['FR01','FR10','AX08','AX11','AX12','OF01','OF04'])

page('SSM și SU ce trebuie acoperit în România',[
'SSM înseamnă securitate și sănătate în muncă. SU include situațiile de urgență, iar PSI se referă la prevenirea și stingerea incendiilor. Un software ajută la evidență, instruire și documente; conformitatea depinde și de organizarea și măsurile efective din firmă.',
'Domeniul exact depinde de activitate, locuri de muncă, riscuri și obligațiile aplicabile. Tabelul este un cadru de evaluare a software-ului, nu lista exhaustivă a obligațiilor juridice ale unei firme.'
],['Arie','Ce trebuie demonstrat în aplicație','Ce rămâne activitate profesională'],[
['Organizare','Responsabili, puncte de lucru și documente','Stabilirea responsabilităților și resurselor.'],
['Riscuri','Evidențe, versiuni și măsuri','Evaluarea reală a riscurilor.'],
['Instruire','Tematici, participanți, test, semnături, scadențe','Instruirea efectivă și verificarea însușirii.'],
['Documente','Generare, aprobare, istoric și recuperare','Adecvarea conținutului la firmă.'],
['Medicina muncii','Aptitudini și expirări, acces restrâns','Examinări și decizii medicale.'],
['EIP','Necesar, predare și înlocuire','Alegerea și utilizarea adecvată.'],
['Incendii și urgențe','Planuri, instruiri și evidențe tehnice','Măsuri și exerciții efective.'],
['Incidente','Raportare și urmărire','Cercetarea și formalitățile legale aplicabile.'],
],[0.20,0.42,0.38],['LG01','LG02','LG03','LG05'],[
'Un modul SU nu obține automat autorizația ISU. Un generator de documente nu certifică automat conținutul. Formele legale în vigoare și fluxul semnăturilor se validează pentru implementarea concretă.'
])

page('Matrice SSM și SU instruire și documente',[
'În coloanele comerciale, «declarat» înseamnă prezentare a furnizorului. SSM.ro are suplimentar un manual operațional. O funcție neconfirmată rămâne întrebare de demonstrație, nu este marcată ca absentă.'
],['Funcție','SSM.ro','SSMatic','SafeHub'],[
['Companii și angajați','Documentat','Declarat','Declarat'],
['Grupe pe posturi și risc','Documentat','De verificat','Declarat'],
['Instruire SSM','Documentată','Declarată','Declarată'],
['Instruire SU','Documentată','Acoperire de verificat','Declarată'],
['Periodic și suplimentar','Documentat','De verificat','Declarat'],
['Materiale și teste','Documentat','Declarat','Declarat'],
['Generare documente','Documentată','Declarată','Șabloane declarate'],
['Șabloane proprii','DOCX și variabile','De verificat','Declarate'],
['Semnare electronică','Opțiuni documentate','Serviciu plătit','AES/OTP declarat'],
['Scadențe și notificări','Documentate','Declarate','Declarate'],
['Nesemnate','Raport API documentat','NC','De verificat'],
],[0.31,0.26,0.22,0.21],['SS01','SS02','SS03','SS07','SM01','SM02','SH01'])

page('Matrice SSM și SU operațiuni și integrare',[],['Funcție','SSM.ro','SSMatic','SafeHub'],[
['Evaluare completă de risc','Nu rezultă numai din generator','Generare declarată; metodologie de verificat','NC'],
['Aptitudini și medicina muncii','Acoperire de verificat','NC','Declarat'],
['EIP','Acoperire de verificat','NC','Declarat'],
['Incidente și near-miss','Registru accidente și incidente documentat','NC','Declarat'],
['Scadențe PRAM și ISCIR','Acoperire de verificat','NC','Declarat'],
['Import angajați','Documentat','De verificat','Excel declarat'],
['API public','Da','Neidentificat','Neidentificat general HR'],
['Microsoft 365','SSO Entra documentat','NC','Integrări declarate'],
['Export integral documente și dovezi','De verificat','De verificat','De verificat'],
['Cod public și self-host complet','Neidentificat','Neidentificat','Neidentificat'],
['Manual public detaliat','Da','Neidentificat comparabil','Neidentificat comparabil'],
],[0.31,0.26,0.22,0.21],['SS04','SS05','SS09','SSX021','SSX038','SM01','SH01'],[
'Evidența unui incident nu dovedește generarea dosarului complet de cercetare. Evidența unui stingător sau a unei scadențe nu înlocuiește verificarea tehnică. Integrarea Microsoft 365 nu dovedește automat API de sincronizare a dosarului HR.'
])

page('SSM ro funcții operaționale suplimentare',[
'Parcurgerea integrală a legăturilor interne ale ghidului a identificat funcții suplimentare față de prezentarea generală. Acestea întăresc candidatura SSM.ro, fără a transforma documentația în probă de funcționare pentru configurația beneficiarului.'
],['Modul','Funcții documentate','Condiție de evaluare'],[
['Registru accidente','Evenimente, persoane implicate, stări și exporturi de registre în Excel.','Nu echivalează automat cu dosarul complet de cercetare.'],
['Audituri și chestionare','Întrebări condiționale, fotografii, scoruri, măsuri, responsabili și termene.','Se testează modelul de audit și raportul cerut de firmă.'],
['Raportare HSE','Indicatori lunari, ținte, formule și export PDF/XLSX.','Structura și nivelul de configurare se verifică pe ediția aleasă.'],
['Arhivare M-Files','Transmitere automată sau manuală și maparea metadatelor.','Necesită configurarea serviciului extern.'],
['Arhivare IronMountain AE','Selectarea documentelor și urmărirea stărilor de arhivare.','Contract și credențiale ale serviciului extern.'],
['Arhivare Namirial','Arhivare a PDF-urilor eligibile și maparea metadatelor.','Servicii proprii Namirial; există limite pe procesare.'],
['SSO','OIDC în SaaS și SAML în modelul Enterprise, conform ghidului.','Configurarea se stabilește cu furnizorul și IdP-ul organizației.'],
],[0.23,0.43,0.34],['SSX020','SSX021','SSX023','SSX016','SSX017','SSX018','SSX038'],[
'Conectorii de arhivare documentați sunt o opțiune reală pentru păstrarea documentelor în alt serviciu. Ei nu dovedesc însă că API-ul public general oferă orice operațiune necesară sincronizării cu iDempiere sau Frappe.'
])
PAGES.insert(17,PAGES.pop())

page('SSM costuri și alegerea furnizorului',[],['Criteriu','SSM.ro','SSMatic','SafeHub'],[
['Model','Serviciu comercial','Ofertă gratuită pentru anumite funcții','Serviciu comercial'],
['Semnături','Condiții și tarife contractuale','Contra cost','Condiții contractuale'],
['Gratuit integral','Nu rezultă','Nu incluzând semnături','Nu rezultă'],
['Avantaj de evaluat','Manual și API public','Acces de bază gratuit declarat','Acoperire operațională declarată'],
['Necunoscut decisiv','Export API complet al documentelor','API, limite și tarif final','API general și condiții de acces'],
['Document comercial necesar','Ofertă pentru volumul real','Ofertă clară pentru semnături și limite','Ofertă pentru companii și utilizatori'],
],[0.25,0.26,0.25,0.24],['SS09','SS10','SM02','SH02'],[
'Nu sunt incluse valori de preț estimate sau un cost total inventat. Comparați aceeași populație de angajați, același număr de instruiri, același tip de semnătură, aceleași documente și aceeași perioadă.',
'Pentru contract solicitați: export la încetare, date și documente păstrate, formatul dovezilor de semnare, responsabilitatea pentru șabloane și schimbări legislative, acces API, limitări și timpi de suport. Acestea sunt criterii propuse de achiziție.'
])

page('Matrice documente HR și salarizare',[],['Document sau rezultat','iDempiere bază','HR sau plugin','Probă cerută'],[
['Fișă angajat','Date de bază','Dosar extins','Câmpuri, istoric și drepturi.'],
['CIM românesc','C/E','Șablon și logică locală','Document complet pentru cazul real.'],
['Act adițional','C/E','Configurare/localizare','Versionare și dată efectivă.'],
['Decizie HR','C/E','Configurare/localizare','Aprobare și emitere.'],
['Cerere concediu','E/C','Funcție HR','Cerere, aprobare și sold.'],
['Pontaj lunar','Ore proiect, P','Attendance + reguli','Ture, absențe și corecții.'],
['Stat de plată','E/localizare','Motor + localizare','Reconciliere cu calcul validat.'],
['Fluturaș','E','Frappe documentat','Legătură cu statul și acces angajat.'],
['D112','NC','NC în selecția analizată','Fișier și validare efectivă.'],
['REGES-ONLINE','NC','NC în selecția analizată','Flux și interfață actuală demonstrate.'],
['Notă contabilă salarii','După implementare','După configurare','Totaluri și reversare controlată.'],
],[0.24,0.20,0.26,0.30],['ID09','FR08','FR09','AX08','PL01','PL08'],[
'Un import denumit Revisal într-un manual nu este dovadă de integrare actuală REGES-ONLINE. Absența dovezii este marcată separat de posibilitatea de a construi un conector.'
])

page('Matrice documente SSM și SU',[],['Document sau evidență','Acoperire de urmărit','Ce se validează'],[
['Fișă individuală SSM','Platformă specializată','Tipuri de instruire, persoane și semnături.'],
['Fișă de instruire SU','Platformă specializată','Etape, tematică și responsabilități.'],
['Tematică și test','SSM.ro documentat; alții declară','Versiune, rezultat și dovada parcurgerii.'],
['Instrucțiuni proprii','Șabloane sau documente proprii','Adecvarea la locul de muncă.'],
['Evaluare de risc','Nu se deduce din generator','Metodologie, evaluator, riscuri și măsuri.'],
['Plan prevenire și protecție','Se cere exemplu concret','Trasabilitate față de riscuri.'],
['Decizii și desemnări','Generatoare/șabloane','Persoane, roluri și aprobări.'],
['Aptitudine medicală','Evidență și scadență','Acces strict la datele necesare.'],
['Predare EIP','Evidență sau dezvoltare','Articol, cantitate, persoană și dovadă.'],
['Plan evacuare/intervenție','Document specializat','Conținut specific amplasamentului.'],
['Dosar incident/accident','Acoperire completă NC','Nu se acceptă doar o fișă de incident.'],
['Arhivă semnată','Fișier final și dovezi','Recuperare și verificabilitate în afara platformei.'],
],[0.29,0.32,0.39],['SS03','SS09','SM01','SH01','LG01','LG02','LG03'])

page('Arhitecturi de integrare comparate',[
'Recomandarea de arhitectură este proiectată pentru acest caz, nu o funcție deja disponibilă. Alegeți un singur sistem principal pentru dosarul angajatului și un singur motor pentru calculul salarial.'
],['Variantă','Flux','Avantaj estimat','Cost sau risc'],[
['A HR nativ','iDempiere + o familie HR → conector → SSM/SU','Mai puține aplicații și identități','Compatibilizarea pluginurilor și localizare.'],
['B HR separat','Frappe HR ↔ conector ↔ iDempiere; HR ↔ SSM/SU','Funcții HR specializate','Sincronizare și două platforme de operat.'],
['C Java separat','Axelor HR ↔ conector ↔ iDempiere','Competențe Java reutilizabile','Suprapunere ERP și payroll extern/localizat.'],
['D Dezvoltare Java','OFBiz HR ↔ conector ↔ iDempiere','Control asupra dezvoltării','Mai mult efort de produs și integrare.'],
],[0.18,0.32,0.25,0.25],['FR10','FR11','AX10','PL15','PL16','SS05'],[
'Frappe are REST și webhook-uri. iDempiere are un plugin REST. Acestea permit construirea integrării, dar nu reprezintă un conector gata făcut pentru întregul circuit.',
'Implementarea propusă folosește identificatori stabili, coadă de evenimente, jurnal de erori, reluare fără dubluri și reconciliere. Nu se recomandă scrierea directă în tabelele celuilalt sistem pentru a ocoli regulile de business.'
])

page('Contractul de date pentru integrare',[],['Obiect','Sistem principal','Date minime','Comportament propus'],[
['Companie','iDempiere','ID, denumire, identificator fiscal','Se transmite structura necesară.'],
['Angajat','HR ales','ID stabil, marcă, nume, stare','Un singur proprietar al fiecărui câmp.'],
['Post și unitate','HR/iDempiere după acord','Cod, valabilitate, locație','Eveniment la schimbare.'],
['Grupă risc','SSM cu responsabil validare','Legătură post și profil risc','Nu se presupune egală cu funcția COR.'],
['Pontaj aprobat','HR','Perioadă, tip ore, cantitate','Versiuni și corecții explicite.'],
['Rezultat salarial','Motor localizat','Sume și centre de cost','Se postează numai rezultate aprobate.'],
['Stare instruire','SSM','Tip, dată, scadență, stare','API sau export, după capabilitate.'],
['Document final','SSM/arhivă','ID, tip, dată, referință, amprentă','PDF și dovezi unde sunt disponibile.'],
['Încetare','HR','Dată efectivă și stare','Dezactivare fără pierderea istoricului.'],
],[0.20,0.23,0.29,0.28],['SS04','SS05','SS07','SS08','FR10','PL16'],[
'În API-ul public SSM.ro sunt documentate operațiuni pentru contacte/angajați și raportul draft_signatures. Descărcarea tuturor PDF-urilor, istoricul complet al testelor și webhook-ul de finalizare rămân cerințe de demonstrat. Pentru SSMatic și SafeHub, un API general HR nu a fost confirmat public.'
])

page('Plan de implementare și probe de acceptanță',[],['Etapă','Activitate','Rezultat cerut'],[
['1 Inventar','Versiuni, pluginuri, date și procese actuale','Bază de comparație semnată intern.'],
['2 Licențe și surse','Repository-uri, dependențe și drepturi','Componentele pot fi folosite și întreținute.'],
['3 Mediu pilot','Instalare izolată și date sintetice','Build, restaurare și upgrade reproductibile.'],
['4 Date HR','Angajare, transfer, concediu, încetare','Istoric corect și acces pe roluri.'],
['5 Pontaj','Ture/noapte, absențe, import repetat','Cantități corecte și fără dubluri.'],
['6 Salarizare','Cazuri validate cu specialistul payroll','Sume și documente reconciliate.'],
['7 SSM/SU','Instruire, test, semnare, export','Dosar complet recuperabil.'],
['8 Integrare','Eroare, retry, actualizare, dezactivare','Reconciliere și jurnal operațional.'],
['9 Decizie','Comparație rezultate și cost total','Alegere justificată sau respingere.'],
['10 Producție','Migrare și operare controlată','Responsabili, backup și proceduri.'],
],[0.20,0.42,0.38],[],[
'Duratele și bugetele nu sunt estimate fără numărul de angajați, companii, locații, terminale și situațiile salariale. Anexa include formularul de cerințe și registrul de acceptanță pentru completare.'
])

page('Scenarii de test gata de folosit',[],['ID','Scenariu','Dovadă de succes'],[
['T01','Angajare și sincronizare repetată','Un singur angajat în fiecare sistem.'],
['T02','Schimbare de post și punct de lucru','Istoric păstrat; profil SSM revizuit.'],
['T03','Tură peste miezul nopții','Ore în perioada corectă.'],
['T04','Lipsă pontare și corecție aprobată','Corecție trasabilă, total corect.'],
['T05','Concediu și anulare','Sold restituit o singură dată.'],
['T06','Calcul salarial și corecție','Reconciliere cu setul validat.'],
['T07','Notă contabilă transmisă de două ori','O singură postare.'],
['T08','Instruire respinsă sau incompletă','Stare corectă și notificare.'],
['T09','Semnare de toate persoanele necesare','Document final și dovezi recuperabile.'],
['T10','API indisponibil','Reluare fără pierdere sau dublare.'],
['T11','Încetare și dezactivare acces','Acces retras, istoric păstrat.'],
['T12','Export la ieșirea din platformă','Fișiere utilizabile independent.'],
],[0.09,0.46,0.45],[],[
'Fiecare test se consemnează cu versiunea, datele sintetice, rezultatul obținut, dovada și responsabilul. Nu sunt incluse rezultate simulate drept teste executate.'
])

page('Ghid de lectură pentru cele trei aplicații HR',[],['Produs','Ordine recomandată','Ce clarifică','Descărcare'],[
['Frappe HR','Introducere → Employee → Recruitment → Shift → Payroll Setup → Payroll Entry','Fluxurile HR și diferența dintre configurare și localizare','FR01, FR04–FR09; fiecare pagină HTML are copie locală dacă recuperarea a reușit.'],
['Axelor','Index HR → Employee file → Hiring → Training → Payroll Preparation','Administrare, recrutare și export payroll','AX01, AX06–AX09; ediția și versiunea trebuie corelate.'],
['OFBiz','Manual utilizator, capitolul HR; apoi Project Manager și integrare','Acoperirea HR în contextul ERP','OF02 manual PDF; OF03 manual tehnic PDF.'],
],[0.15,0.34,0.29,0.22],['FR01','FR04','FR05','FR06','FR07','FR08','FR09','AX01','AX06','AX07','AX08','AX09','OF01','OF02','OF03'],[
'Legăturile din raport deschid sursele oficiale. INDEX.html din rădăcina dosarului deschide și copiile locale, cu filtrare după produs și stare. Linkurile de release sunt descărcări de software; nu sunt prezentate drept manuale.',
'Documentația originală rămâne în limba publicată. Analiza, explicațiile, indexurile, registrele și fișele de evaluare sunt în română.'
])

page('Ghid de lectură pentru SSM SU și extensii',[],['Produs','Material prioritar','Limită de acces'],[
['SSM.ro','Primii pași, generatoare, angajați, API și rapoarte','Manual public; condițiile de acces API sunt contractuale.'],
['SSMatic','Prezentarea și prețurile','Nu a fost identificat un manual tehnic public complet.'],
['SafeHub','Funcții și ofertă','Nu a fost identificat un manual tehnic public complet.'],
['CDSoftware','Paginile Payroll, Attendance, Training și Recruitment','Unele descărcări wiki sunt refuzate; marcate în registru.'],
['AMERPSOFT','README general, README modul, PDF','Documentația poate descrie versiuni diferite.'],
['iDempiere','Manual, inventar modele și surse release 13','Codul completează paginile wiki inaccesibile, fără a le înlocui integral.'],
],[0.19,0.46,0.35],['SS01','SS02','SS03','SS04','SS05','SS06','SS07','SS08','SM01','SM02','SH01','SH02','PL01','PL07','PL08','PL17','ID14'],[
'Materialele HTML sunt salvate ca versiuni text și tabele pentru citire offline. JavaScript-ul și imaginile externe sunt eliminate din aceste copii; interfețele demonstrative și capturile de ecran pot necesita sursa online. Originalul HTML este păstrat comprimat, inert, pentru proveniență.',
'Arhiva nu pretinde să conțină documentații private, toate limbile, toate versiunile istorice sau materiale inaccesibile. Registrul enumeră exact ce a fost recuperat și ce nu.'
])

page('Decizii rămase și recomandarea finală',[],['Decizie','Recomandare','Condiție'],[
['HR nativ sau separat','Pilot CDSoftware versus Frappe HR','Aceleași cazuri și date sintetice.'],
['Motor salarial','Un singur motor validat pentru România','Reconciliere cu payroll autorizat intern.'],
['Alternativă nativă','AMERPSOFT în evaluare separată','Licență, compatibilitate și raportare confirmate.'],
['SSM/SU','SSM.ro primul pentru integrare; ceilalți în demo comparabil','Export complet și circuit semnături demonstrate.'],
['Axelor/OFBiz','Păstrate pentru cerință Java sau dezvoltare amplă','Beneficiu suficient față de duplicarea ERP.'],
['Arhivare','Documente și dovezi recuperabile independent','Test de export și restaurare.'],
['Acceptanță finală','Pe dovezi, nu pe scoruri arbitrare','Teste, costuri și responsabilități asumate.'],
],[0.22,0.43,0.35],['PL01','PL07','FR01','AX01','OF01','SS05'],[
'Concluzia cercetării: există extensii HR reale pentru iDempiere și nu este necesară presupunerea că tot HR-ul trebuie construit de la zero. Diferența rămasă este între existența structurilor sau modulelor și un sistem complet, compatibil, localizat și testat pentru firma voastră.',
'Dosarul oferă documente, surse și instrumente de evaluare utilizabile imediat. Compatibilitatea de producție și conformitatea locală rămân rezultate ale implementării și validării, nu ale acestei cercetări documentare.'
])
