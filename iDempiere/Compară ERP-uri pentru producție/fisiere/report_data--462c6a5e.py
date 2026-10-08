from pathlib import Path
import json

PAGES=[]
def page(title,lead=''):
    p={'title':title,'blocks':[]};PAGES.append(p)
    if lead:p['blocks'].append(('p',lead))
    return p
def p(text):PAGES[-1]['blocks'].append(('p',text))
def h(text):PAGES[-1]['blocks'].append(('h',text))
def table(head,rows,widths=None):PAGES[-1]['blocks'].append(('t',{'head':head,'rows':rows,'widths':widths}))

page('Managementul producției în EVA și iDempiere','Raport de decizie pentru management și echipa tehnică | 8 octombrie 2026 | Versiunea 1.0')
h('Decizia recomandată')
p('Recomand evaluarea prioritară a Logilite Manufacturing 2 pe o copie de test iDempiere 13, păstrând EVA drept sistem contabil și operațional principal. Este calea cu cea mai bună potrivire arhitecturală identificată: manifestul curent al pluginului declară versiunea 13, iar sursele includ ordine de fabricație, MRP, CRP și colectarea costurilor. Aceste dovezi justifică un pilot, nu instalarea directă în producție. [SRC_mfg2] [V01]')
p('ERPNext este prima alternativă externă pentru acoperirea funcțională integrată a producției. Alegerea sa devine justificată dacă pilotul nativ nu trece criteriile de cost, trasabilitate și operare sau dacă experiența de lucru în secție contează mai mult decât păstrarea unei singure platforme. Integrarea presupune dezvoltarea unui conector și delimitarea strictă a responsabilității asupra stocului. [E01–E08]')
table(['Prioritate','Soluție','Motiv și condiție'],[
['Nativ','iDempiere 13 + EVA + MFG2','Prima opțiune de integrare; necesită compilare, verificarea dependențelor ZK și probe tranzacționale.'],
['Extern 1','ERPNext','Flux amplu de la BOM la operații și consumuri; cost suplimentar pentru integrarea a două ERP-uri.'],
['Extern 2','Tryton','Module oficiale coerente și control asupra modelului; configurare și interfață de secție de evaluat.'],
['Extern 3','Odoo Community','MRP, centre de lucru și mentenanță în codul liber; Quality și PLM comerciale nu intră în evaluare.'],
['Extern 4','Apache OFBiz','Motor de fabricație și MRP, potrivit echipei Java; integrare și ergonomie cu efort ridicat.'],
['Extern 5','Dolibarr','BOM și ordine de producție pentru fluxuri simple; acoperire avansată mai redusă în dovezile analizate.']],[55,125,315])
p('Clasamentul extern este o apreciere tehnică pentru această cerință, nu un top universal și nici un benchmark. EVA are deja producție de bază; înlocuirea ei fără inventarierea comportamentelor existente ar pierde valoare. Raportul separă funcțiile incluse, modulele oficiale de activat, extensiile și dezvoltările necesare.')
p('Rezultatul este documentar și include inspecție de cod la commit-uri identificate. Nu au fost executate teste funcționale pe o instanță ERP și nu a fost modificată producția. Responsabilitatea recomandării privește interpretarea dovezilor și proiectarea pilotului; aprobarea lansării revine beneficiarului după probele de acceptanță.')

page('Domeniul și regulile comparației')
p('Sunt comparate cinci aplicații externe open-source autogăzduite, nucleul iDempiere 13, extensiile publice relevante și codul EVA. „100% free” înseamnă aici zero taxă obligatorie de licență pentru componentele libere selectate. Nu înseamnă zero cost de server, implementare, migrare, instruire, securizare sau suport. Edițiile SaaS și modulele comerciale nu sunt presupuse incluse.')
table(['Cod','Înțeles în matrice'],[
['N','Funcție inclusă în distribuția/codul ediției evaluate; poate necesita activare și configurare.'],
['M','Modul oficial liber separat, de instalat/activat; utilizat în special pentru structura modulară Tryton.'],
['C','Se modelează prin funcții existente, cu limitări; nu este o funcție specializată echivalentă.'],
['A','Extensie comunitară suplimentară identificată; compatibilitatea și licența distribuției se verifică separat.'],
['D','Dezvoltare sau integrare specifică necesară pentru cerința exactă.'],
['U','Neconfirmat în dovezile consultate. Nu reprezintă dovada absenței absolute.'],
['N*','Cod existent, cu limită concretă explicată în raport; nu înseamnă validare funcțională.']],[45,450])
h('Criterii eliminatorii înainte de punctaj')
p('Licență liberă verificabilă pentru configurația propusă; posibilitate de instalare proprie; cod și versiune identificabile; lipsa unei dependențe proprietare obligatorii pentru scenariul pilot; export de date și backup; separarea firmelor; reversarea controlată a documentelor. O soluție care nu îndeplinește aceste condiții nu devine acceptabilă printr-un scor mediu bun.')
h('Ce înseamnă implicit')
p('Pentru ERPNext, OFBiz, Dolibarr și Odoo se evaluează funcțiile din codul liber al produsului, chiar dacă trebuie activate module. Pentru Tryton se arată explicit modulele oficiale suplimentare. Pentru iDempiere, existența unei tabele PP_* sau a unei ferestre în dicționar nu dovedește existența motorului complet MRP. Pentru EVA, existența codului nu dovedește ce JAR este instalat în fiecare cabinet.')
h('Limita inventarului complet')
p('Catalogul urmărește întregul lanț definit în acest raport: date tehnice, cerere, planificare, execuție, stoc, calitate, cost, mentenanță, oameni, raportare și integrare. Nu poate garanta inventarierea tuturor pluginurilor private sau a tuturor extensiilor publicate vreodată. Registrul documentațiilor consemnează exact corpusul consultat și descărcările nereușite; acestea nu sunt prezentate ca documentație locală completă.')

page('Versiunile și proveniența dovezilor')
p('Versiunile sunt repere de audit, nu afirmații că fiecare ramură este cea mai nouă versiune stabilă. Pentru implementare se fixează release-ul, commit-ul, dependențele și schema bazei de date. Documentațiile „latest” pot evolua independent de cod; o funcție nouă din manual trebuie confruntată cu versiunea instalată.')
table(['Componentă','Referința inspectată','Dovada principală'],[
['EVA','1c039193e0c1626cb03fb8ca37f9980a1703fd0c','README și codul ecranelor de producție; ramura implicită fix/116-remediere-izolare-multifirma.'],
['iDempiere','release-13 / 0bbc4fa5df2e','MProduction, ProductionCreate, Doc_Production, modele BOM și quality.'],
['MFG2 Logilite','master / 7f353732ba27','Manifest: 13.0.0; JavaSE-17; cerințe ZK 10.3.0. Compatibilitate declarată, netestată aici.'],
['Libero Shepetko','master / b2adfea08d50','Manifest: 14.0.0; README încă menționează 8.2.0. Nu se instalează master pe 13 fără evaluare.'],
['Asset Maintenance','master / 73fd87291e0e','Wiki declară 2.1.0.3 pentru 13; sursa și manualele sunt în biblioteca locală.'],
['ERPNext','version-16 / 7474d9e78627','DocTypes BOM, Work Order, Job Card și Production Plan; manualul oficial.'],
['Tryton','Documentația oficială latest','Module production, routing, work, outsourcing și supply; versiunea de instalare se fixează în pilot.'],
['Odoo Community','19.0 / 9ec2b55d3fa3','addons/mrp, maintenance și mrp_subcontracting; nu Enterprise.'],
['Apache OFBiz','release24.09 / 0749c835f0f3','Manualul stable și API-urile de producție/MRP.'],
['Dolibarr','23.0 / 11abdaed08a9','Modulele BOM și MO; codul mo.class.php și bom.class.php.']],[100,170,225])
p('Commit-urile complete și arborii sursă sunt păstrați în fișierele de proveniență. Pentru proiectele externe, licențele declarate sunt ERPNext GPL-3.0, Tryton GPL-3.0-or-later, OFBiz Apache-2.0, Dolibarr GPL-3.0-or-later și Odoo Community LGPL-3.0. iDempiere și pluginurile Libero/MFG2 analizate declară GPLv2. Se păstrează licența fiecărui fișier și modul; această identificare nu este o opinie juridică privind o combinație de cod derivat.')

page('Ce există deja în EVA')
p('EVA este un plugin OSGi de contabilitate românească peste iDempiere 13. README descrie cabinetul ca instanță separată și firma ca AD_Client. Interfața curentă este ZK; backend-ul și frontend-ul mai vechi sunt descrise ca dormante. Arhitectura propusă se raportează la această stare, nu la descrierile istorice rămase mai jos în README. [V01]')
table(['Categorie','Funcția identificată','Dovadă la commit-ul auditat'],[
['Documente','Bon de predare cu produs finit, cantitate, dată, gestiune și componente','WSagaProductieForm, scrieDocument, liniile 2200–2337.'],
['Rețetă','Citește PP_Product_BOM și PP_Product_BOMLine; multiplică consumurile după cantitatea produsă','idReteta și aplicaReteta, 1152–1238.'],
['Consum','Componente manuale sau din rețetă; gestiune separată pe linie','WSagaProductieForm; WSagaBonConsumForm.'],
['Ciclu document','Salvare ciornă; validare prin MProduction.processIt(Complete); anulare prin Void','scrieDocument la 2328; devalideaza la 1563.'],
['Dezmembrare','Subclasă a ecranului de producție; inversează sensul produsului și al componentelor','WSagaDezmembrariForm și cârligele din clasa de bază.'],
['Cost orientativ','Preț prestabilit, propunere din consumuri și manoperă; avertizare la manoperă','pretPropus, costReteta și gardaManopera.'],
['Analitic','Legătură C_Activity la document','WSagaProductieForm, 2254.'],
['Raport','Situație producție cu produse/consumuri, gestiune, cantități, preț și valoare; arată și ciorne','WSagaSituatieProductieForm, 75–149.'],
['Tipărire','Bonuri și consumuri individuale sau grupate; numere și serii','Butoanele BP și variante din WSagaProductieForm.'],
['Protecție','Verificare AD_Client pe document și poartă de perioadă la salvare/validare','scrieDocument, 2208–2230.']],[78,213,204])
p('Aceste capabilități justifică păstrarea fluxului simplu de producție și a documentelor existente. Nu am identificat în fișierele inspectate un planificator complet de operații, o interfață de pontaj pe operație, un motor APS pentru cuptoare sau un OEE industrial complet. Acestea rămân U/D, nu sunt declarate absente în întreaga instalație.')

page('Limite tehnice EVA care influențează integrarea')
p('Constatările următoare rezultă din cod static. Nu afirmă că există deja erori în datele de producție. Ele stabilesc probele și lucrările necesare înaintea introducerii fabricației avansate. [V02–V06]')
table(['Constatare','Implicație','Acțiune de acceptanță'],[
['Alegerea rețetei','idReteta ia prima rețetă activă fără ordonare și fără selecție explicită a reviziei/valabilității.','Două BOM active pentru același produs: selectare deterministă, revizie și data de aplicare salvate pe ordin.'],
['Preț și manoperă în Description','Convenții text P= și M= folosite pentru reafișare; tipul dezmembrării este tot un prefix text.','Migrare în câmpuri tipizate și păstrarea textului istoric; nu se bazează integrarea pe traducerea descrierii.'],
['Costul curent','costUnitar selectează primul cost pozitiv după created; nu selectează explicit toate dimensiunile costului.','Test pe mai multe scheme/elemente/organizații; costul istoric al documentului se citește din evidențele tranzacției.'],
['Raportul de producție','JOIN la M_Cost doar după produs și client; poate multiplica rânduri când există mai multe înregistrări.','Set de date cu mai multe dimensiuni M_Cost; verificare cantitate și valoare fără dublare.'],
['Valoare de raport vs contabilitate','Raportul folosește costul curent și include ciorne; nu demonstrează valoarea contabilă istorică.','Separare indicatori planificați/nevalidați de costul postat și reconciliere cu Fact_Acct.'],
['Loturi în ecranul inspectat','scrieDocument nu setează explicit ASI pe liniile construite în secvența inspectată.','Probe cu lot obligatoriu; genealogie intrare–ieșire, selecție lot și carantină.'],
['BOM tehnic','asiguraBom creează un artefact pentru cerința motorului; nu este automat rețeta tehnologică aprobată.','Excludeți artefactele tehnice din planificare; definiți BOM master și revizia consumată.'],
['Două motoare de fabricație','M_Production și PP_Order/CostCollector pot produce ambele mișcări dacă sunt legate greșit.','O singură cale autoritativă de consum și recepție pentru fiecare ordin.']],[95,200,200])
p('Prioritate propusă: selecția BOM, dimensiunile costului și evitarea dublei postări sunt P0 pentru pilot; loturile devin P0 dacă trasabilitatea este obligatorie. Tipizarea câmpurilor este P1 înaintea conectorului de producție. Nu se modifică acest cod în cadrul prezentului raport.')

page('Nucleul iDempiere relevant pentru producție')
p('iDempiere 13 are producție simplă și componente ERP care o susțin. Codul actual utilizează PP_Product_BOM/PP_Product_BOMLine în MProduction; descrierea exclusiv prin vechiul M_Product_BOM ar fi inexactă pentru reperul auditat. Un BOM multinivel nu implică automat planificare MRP completă. [SRC_idempiere]')
table(['Categorie','Componente native','Funcții și limită'],[
['Articole și unități','M_Product, categorii, C_UOM, conversii','Materii prime, semifabricate, produse, servicii; disciplina unităților trebuie configurată.'],
['Structură tehnică','PP_Product_BOM, PP_Product_BOMLine','Componente și cantități, validări și explorarea structurii; aprobarea inginerească se proiectează separat.'],
['Producție','M_Production, M_ProductionLine, M_ProductionPlan','Generare linii, consum/recepție, completare și anulare; nu echivalează cu un MES pe operații.'],
['Cerere și reaprovizionare','C_Order, M_Requisition, M_Replenish','Comenzi, cereri, praguri și generare producție; nu se confundă cu APS.'],
['Stoc','M_Warehouse, M_Locator, M_Transaction, stoc și alocări','Depozite, locații, mișcări, inventar și legătură cu documentele.'],
['Trasabilitate','M_AttributeSetInstance, lot, serie, M_ProductionLineMA','Atribute și alocări de material; genealogia și blocările de lot se probează cap-coadă.'],
['Calitate de bază','M_QualityTest, M_QualityTestResult','Teste și rezultate asociate; nu sunt o suită CAPA/SPC/ISO completă.'],
['Cost și contabilitate','M_Cost, M_CostDetail, Doc_Production, Fact_Acct','Evaluare și postare în ERP; configurarea conturilor și dimensiunilor este esențială.'],
['Oameni și proiecte','C_BPartner, AD_User, S_Resource, C_Project','Identități, resurse și proiecte; calificarea pe operație cere legături explicite.'],
['Control și integrare','AD_Role, AD_Workflow, procese, webservices, OSGi','Permisiuni, extensibilitate și servicii; REST-ul uzual bxservice este o extensie distinctă.']],[87,172,236])
p('Procese identificate în arborele release-13: ProductionCreate, ProductionProcess, M_Production_Run, OrderCreateProduction, OrderLineCreateProduction, ProjectGenProduction, ReplenishReportProduction, BOMVerify și IndentedBOM. M_ProductionPlan nu este echivalentul unui master production schedule cu capacitate finită.')

page('Fabricație avansată nativă prin Libero și MFG2')
p('Cele două proiecte împart o origine tehnică și exportă pachete org.libero. Nu se recomandă instalarea lor simultană: trebuie verificată suprapunerea modelelor, validatoarelor, proceselor și a înregistrărilor din dicționar. MFG2 este candidatul inițial pentru EVA 13, deoarece manifestul său actual indică explicit această familie. [SRC_mfg2] [SRC_libero]')
table(['Categorie','Clase și concepte găsite în MFG2','Ce trebuie demonstrat'],[
['Ordine de fabricație','MPPOrder, MPPOrderBOM, MPPOrderBOMLine','Lansare, îngheț BOM, cantități parțiale, închidere și anulare.'],
['Necesar materiale','MPPMRP, MRP, MRPUpdate, WMRPDetailed','Cerere netă, stoc, recepții, timpi de aprovizionare și relansare fără duplicate.'],
['Capacități','CRP, CRPReasoner, WCRP, WCRPDetail','Calendare și încărcare pe resurse; nu se presupune optimizare APS globală.'],
['Rute și operații','MPPOrderWorkflow, MPPOrderNode, RoutingService','Succesiune, durate, resurse și colectarea execuției.'],
['Consum și recepție','OrderReceiptIssue, WOrderReceiptIssue','Ieșiri materiale și intrări finite, loturi și recepții parțiale.'],
['Cost fabricație','MPPCostCollector, MPPOrderCost, CostEngine, Doc_PPCostCollector','Materiale, resurse și abateri; concordanță cu schema contabilă EVA.'],
['Distribuție','DD_Order, DistributionRunOrders','Transferuri între locații/organizații; nu un WMS complet implicit.'],
['Rapoarte BOM','PrintBOM, CostBillOfMaterial, BOMVerify','Structură, cost și verificare; comparația istorică se validează separat.'],
['Lot de încărcare','I_PP_Order_BatchCharge și X_PP_Order_BatchCharge','Doar model identificat; nu dovedește planificator de încărcare cuptor.'],
['Extensii mentenanță','CreateForecastLine4eAM, CreateMOFromForecastLine4eAM','Dependențe și flux complet de verificat; nu se asumă CMMS complet.']],[95,210,190])
p('Manifestul MFG2 include cerințe pentru Java 17 și ZK 10.3.0. Build-ul EVA și distribuția iDempiere 13 trebuie confruntate exact cu acestea. Un Bundle-Version egal cu 13 nu este dovadă suficientă pentru rezolvarea tuturor dependențelor. README-urile vechi de 7.1/8.2 sunt depășite față de manifest; am păstrat ambele dovezi.')

page('Extensii iDempiere pentru planificare și execuție')
p('Inventarul următor reunește extensiile publice relevante identificate. „Istoric” descrie reperul public consultat, nu o concluzie că proiectul este abandonat. Actualizarea binarelor, licenței și compatibilității este condiție de selecție. [I01–I10] [I19]')
table(['Extensie','Funcții','Statut pentru EVA 13'],[
['Libero Manufacturing','MRP, ordine, rute, materiale, capacități și costuri în familia Libero.','Sursa master inspectată declară 14; alegeți o revizie compatibilă sau portare.'],
['Logilite MFG2','Reorganizare/extindere Libero, procese MRP/CRP și colectori de cost.','Manifest 13; prima variantă de pilot nativ.'],
['BOMDrop Configurator','Componente obligatorii, opționale, variante și grupuri; transfer în documente.','Extensie istorică; nu este configurator industrial complet/PLM.'],
['AutoBOMOrder','Expansiune BOM în liniile comenzii de vânzare.','Istoric 4.1; modificați doar după analizarea efectelor pe documente.'],
['CopyBOMToProduct','Copiere structură BOM către alt produs.','Istoric 7.1; verificați ce oferă deja nucleul pentru a evita dublarea.'],
['Beluga copyBOM','Copiere rețetă existentă pentru articole similare.','GPLv2, versiune publicată 1.0.0; compatibilitate de verificat.'],
['Sales Forecasting','Perioade și previziuni de vânzare pentru planificare.','Wiki indică 4.1/5.1; nu este forecast instalat implicit.'],
['Purchasing Forecast','Transformă cererea în propuneri/comenzi de achiziție, cu termene și necesar net.','Istoric 2.1/3.0; verificare pe 13.'],
['TOC Buffer Management','Praguri dinamice de reaprovizionare și istoric de buffer.','Wiki 6.2, binar 7.1; nu este certificare DDMRP.'],
['TargetCostBOMReport','Cantități, acumulare cost și comparație între două date.','Documentat pentru 10 și Libero; licența/revizia livrată de verificat.']],[120,205,170])
p('Nu confundați pluginul LPE cu un motor de planificare: pagina consultată descrie localizarea fiscală pentru Peru. Numele scurt nu constituie dovadă funcțională. Nici un tablou Kanban nu înlocuiește calculul necesarului material sau capacitatea utilajelor.')

page('Extensii iDempiere conexe producției')
table(['Extensie','Funcții utile','Limita decisivă'],[
['Asset Maintenance','Planuri de întreținere, contoare, sarcini standard, cereri și ordine de intervenție.','Wiki declară 13; verificare sursă, joburi și resurse în pilot. [I02]'],
['Kanban Dashboard','Stări, priorități, mutare carduri, filtre, swimlanes și limitare WIP în carduri.','Configurație peste documente; nu reprezintă capacitate tehnologică în minute. [I04]'],
['Libero Warehousing','Flux outbound dependent de familia Libero.','Wiki ALPHA și inbound incomplet; condițiile distribuției comerciale nu sunt clarificate. [I11]'],
['Red1 WMS','Handling units și locații disponibile, în ecosistemul de depozitare.','BETA/versiuni istorice; integrarea 13 și licența pachetului exact de verificat. [I12]'],
['Scale Connector','Citire de cântare/senzori prin serviciu și RS-232.','Wiki pentru 3.1; nu dovedește integrare OPC UA/MQTT și nici rețetar de proces. [I13]'],
['Multiple ASI Editor','Editare/alocare a atributelor și loturilor, candidat pentru simplificarea introducerii.','Funcțiile exacte și compatibilitatea nu sunt confirmate prin cod în acest raport. [I14]'],
['CopyWFNodes','Utilitar de copiere a nodurilor workflow.','Candidat pentru configurare; nu se punctează ca MES. [I15]'],
['BPM Process Configurator','Configurare de procese în ecosistem.','Necesită fișă tehnică și test; nu se atribuie funcții MRP fără probă. [I16]'],
['Logilite DMS','Gestiune documentară pentru instrucțiuni și atașamente.','Revizie tehnică aprobată și legare la operație trebuie probate. [I17]'],
['TMS','Transport, relevant pentru aprovizionare și livrare.','Sistem conex; nu este motor de producție. [I18]'],
['REST bxservice','Acces la modele și procese pentru integrare.','Conectorul de business, idempotenta și reconcilierea nu vin automat. [I90]']],[112,205,178])
p('Suita de bază poate fi completată cu JasperReports, BI, atașamente, HR AMERPSOFT și localizarea românească EVA. Acestea sunt componente de suport; nu se numără ca module de fabricație avansată. Nu recomand instalarea tuturor extensiilor: se selectează cel mai mic ansamblu care trece scenariul pilot.')
p('Pentru extensiile cu pagini wiki inaccesibile la descărcare, registrul păstrează URL-ul și eroarea HTTP. Codul public și manualele din repository, când au fost disponibile, sunt alternative locale. Nu este corect ca o fișă de sinteză să fie etichetată manual oficial complet.')

page('ERPNext ca alternativă externă')
p('Configurația evaluată este ERPNext din familia version-16, autogăzduit cu Frappe, fără abonament obligatoriu pentru codul GPL. Punctul forte este continuitatea dintre BOM, Production Plan, Work Order, Job Card și tranzacțiile de stoc. Acesta este motivul priorității sale între soluțiile externe, nu simplul număr de module. [E01–E08] [SRC_erpnext]')
table(['Categorie','Funcții efective','Condiție pentru EVA'],[
['Inginerie','BOM multinivel, operații, costuri planificate, instrumente BOM.','Mapare revizii, unități și variante; păstrarea identității produsului.'],
['Planificare','Production Plan, necesar de materiale, subansamble și comenzi de fabricație.','Cererea provine din EVA; nu se generează achiziții în două sisteme.'],
['Execuție','Job Card, operații, timpi, cantități și Workstation.','Persoana EVA/AMN trebuie mapată distinct de utilizator.'],
['Materiale','Transfer către WIP, consum și recepție de produse prin Stock Entry.','Alegerea unui singur registru de stoc autoritativ este obligatorie.'],
['Calitate','Quality Inspection și componente de management al calității.','Regula de blocare/eliberare a lotului în EVA cere integrare.'],
['Subcontractare','Fluxuri dedicate de subcontractare și materiale furnizate.','Contract și bunuri la terți reconciliate cu evidența EVA.'],
['Mentenanță','Asset Maintenance și loguri asociate activelor.','Nu se presupune optimizare comună producție–mentenanță.'],
['Integrare','REST Frappe și webhooks.','Mapare, reluări, ordinea evenimentelor și monitorizare de construit.']],[92,204,199])
h('Limitele care contează')
p('Planificarea resurselor documentată nu garantează un APS global pentru cuptoare cu loturi mixte, matrițe, uscătoare și schimbări de glazură. Rețetele procentuale cu umiditate, bilanț de masă și randamente pe faze trebuie demonstrate într-un prototip. O funcție din documentația curentă se verifică în versiunea fixată, înainte să fie punctată ca livrabil.')
p('Integrarea externă nu înseamnă copierea modulului Python în OSGi. ERPNext rămâne serviciu separat, cu propria bază de date și propriile cicluri de upgrade. Pentru EVA, avantajul funcțional trebuie să depășească efortul de operare și reconciliere al celei de-a doua platforme.')

page('Tryton ca alternativă modulară')
p('Tryton este o opțiune liberă modulară. Funcționalitatea rezultă din activarea unui ansamblu de module oficiale; instalarea serverului gol nu reprezintă instalarea producției. Documentația diferențiază explicit producția de rutare, execuție, timp și subcontractare. [T01–T10]')
table(['Modul oficial','Funcții efective','Observație de integrare'],[
['production','BOM cu intrări și ieșiri; ordine și mișcări de stoc.','Permite modelarea mai multor ieșiri; costul de repartizat se verifică.'],
['production_routing','Operații ordonate și rute asociate BOM.','Importați codurile și reviziile rutei, nu doar denumirile.'],
['production_work','Centre de lucru, cicluri, durate și cost pe oră/ciclu.','Potrivire bună pentru execuție structurată; ergonomia se testează.'],
['production_work_timesheet','Pontaj asociat lucrărilor.','Legătura cu HR EVA este dezvoltare separată.'],
['production_outsourcing','Serviciu furnizor pe rută, comandă de achiziție și cost asociat.','Trebuie stabilit cine creează achiziția financiară.'],
['production_split','Împărțire ordin în cantități și rest.','Nu reprezintă automat genealogia completă a loturilor.'],
['stock_supply_production','Necesar de producție din niveluri de stoc și cereri existente.','Păstrați un singur mecanism de reaprovizionare.'],
['sale_supply_production','Cerere de producție din vânzare.','Evenimentele de anulare/modificare trebuie sincronizate.'],
['stock_lot și quality','Loturi și mecanisme de inspecție/control documentate separat.','Calitatea pe operație și blocarea lotului se probează exact.']],[133,190,172])
p('Centrele de lucru au costuri și durate, dar aceasta nu dovedește automat optimizare finită multicriterială sau un panou MES industrial. Modulele oficiale pot fi extinse coerent; se plătește însă efortul de implementare, nu o licență. Familia exactă Tryton și dependențele se fixează împreună la începutul pilotului.')
p('Tryton este alternativa a doua când echipa preferă o platformă modulară Python/PostgreSQL și poate configura interfața de producție. Nu identific în corpus un conector complet Tryton–EVA disponibil gata de instalat. API-ul și clientul de scripting sunt baze tehnice, nu o mapare contabilă.')

page('Odoo Community și separarea de Enterprise')
p('Evaluarea folosește codul public Odoo 19.0. Acesta conține mrp_workcenter.py, mrp_workorder.py, maintenance și mrp_subcontracting. Prin urmare, afirmația generală „Community nu are centre de lucru, operații sau mentenanță” ar fi greșită pentru reperul inspectat. [SRC_odoo]')
table(['Inclus în codul liber inspectat','Funcția','Limită'],[
['mrp','BOM, ordine de fabricație, operații și centre de lucru.','Configurația exactă și ecranele se verifică în Community curat.'],
['mrp work orders','Înregistrări de lucru, durate și planificarea pe calendare.','Nu se atribuie implicit aplicația Enterprise Shop Floor sau vizualizarea comercială de planificare.'],
['mrp workcenter','Capacități, calendare și câmp oee.','Formula observată în cod nu este automat OEE industrial A × P × Q.'],
['mrp_subcontracting','Flux de subcontractare.','Necesită modulele dependente și configurarea logisticii.'],
['maintenance','Echipamente și cereri de mentenanță.','Predicția defectelor și integrarea IoT rămân alte cerințe.'],
['stock și stock_account','Stoc, loturi, mișcări și valorizare în platformă.','Nu trebuie să devină al doilea registru financiar autoritativ.'],
['Module OCA','Extensii comunitare, inclusiv în ecosistemul calității.','Nu sunt implicit instalate; fiecare are versiune, licență și dependențe proprii.']],[145,180,170])
p('Quality, PLM și funcțiile comerciale de Shop Floor nu se presupun incluse în Community. Pagina oficială de ediții oferă context comercial; pentru detaliile de mai sus dovada decisivă este codul liber. O variantă Community + OCA rămâne posibilă, dar este o configurație diferită care trebuie auditată individual.')
h('OEE necesită o definiție comună')
p('În mrp_workcenter.py, calculul inspectat folosește timpul productiv și timpul blocat. Pentru indicatorul industrial solicitat trebuie definite disponibilitatea, performanța și calitatea, cu numitorii și excluderile convenite. Nu se compară procente provenite din formule diferite doar fiindcă au aceeași etichetă.')
p('Odoo Community este o opțiune solidă dacă echipa are deja competențe Odoo și acceptă selecția extensiilor. Nu îl pun înaintea ERPNext pentru obiectivul de acoperire integrată gratuită fără a demonstra explicit completările pentru calitate și operarea secției.')

page('Apache OFBiz și Dolibarr')
h('Apache OFBiz')
p('OFBiz include concepte de BOM, rute, sarcini și production run, împreună cu MRP și calculul costului. API-urile inspectate descriu generarea operațiilor și a materialelor, schimbarea stării și anularea ordinului. Acoperirea justifică selecția sa pentru o echipă Java, dar utilizarea aceluiași limbaj nu îl transformă într-un plugin iDempiere. Modelele de persistență și servicii diferă. [F01] [F04] [F05]')
p('Recomand o integrare prin servicii pentru cazul în care OFBiz este ales, nu copierea entităților în baza EVA. Avantajul este flexibilitatea; dezavantajul este efortul de configurare, interfață și mentenanță. APS avansat, QMS complet și genealogia exactă cer probe separate. Licența Apache-2.0 este permisivă, dar rămân obligațiile de atribuire și verificare a dependențelor.')
h('Dolibarr')
p('Dolibarr include modulele BOM și Manufacturing Orders în distribuție; trebuie activate de administrator. Este un candidat rezonabil pentru asamblare sau transformare simplă, cu o bază ERP accesibilă. Denumirea MRP din prezentarea modulului nu dovedește un motor industrial complet de calcul net al necesarului și capacităților. [D01] [D02] [SRC_dolibarr]')
p('Nu sunt confirmate în corpus o planificare APS completă, un MES cu operații și timpi comparabil cu ERPNext sau un QMS industrial complet în distribuția de bază. Extensiile din marketplace nu intră automat în categoria gratuită. Pentru EVA, încă un ERP cu producție simplă aduce un avantaj insuficient dacă reproduce doar funcțiile existente.')
table(['Scenariu','OFBiz','Dolibarr'],[
['Producție multietapă','Candidat tehnic; pilot pe rute și cost.','Necesită demonstrarea extensiilor necesare.'],
['Asamblare simplă','Posibil, cu efort de configurare.','Potrivire funcțională mai simplă.'],
['Integrare în EVA','Serviciu separat și mapare.','Serviciu separat și mapare.'],
['Motiv de alegere','Echipă Java, personalizare amplă.','Simplitate și flux limitat.'],
['Motiv de respingere','Buget redus pentru implementare/UX.','Necesitate de fabricație avansată imediată.']],[110,190,195])

MATRICES=[]
def cat(name,source,items,note=''):
    MATRICES.append({'category':name,'sources':source,'rows':items,'note':note})
# Columns: ERPNext, Tryton, Odoo CE, OFBiz, Dolibarr, iDempiere core, EVA inspected.
cat('Date tehnice și produse','E02 E06 E07 T01 T02 SRC_odoo SRC_idempiere V02',[
('Articole și unități de măsură','N M N N N N N'),('Conversii de unități','N M N N C N C'),('BOM și componente','N M N N N N N'),('BOM multinivel','N M N N C N C'),('Semifabricate stocate','N M N N N N C'),('Variante de produs','N M N C N C C'),('Selecție revizie BOM pe ordin','N C C C U C D'),('Aprobare inginerească formală PLM','C D A D U D D')], 'În EVA, rețeta activă este preluată fără selecție explicită de revizie; C la multinivel nu dovedește o explozie recursivă completă în ecranul propriu.')
cat('Cerere și planificare de materiale','E03 E24 T07 T08 F04 SRC_odoo I09 I10 SRC_mfg2',[
('Producție la comandă','N M N N C N C'),('Producție pentru stoc','N M N N N N N'),('Plan agregat din comenzi','N M C N U A U'),('Calcul necesar net de materiale','N M N N U A U'),('Propuneri de aprovizionare','N M N N C N C'),('Praguri de reaprovizionare','N M N N N N C'),('Forecast pentru cerere','N M A C U A U'),('Pegging complet cerere ofertă auditat','C C C C U A U')], 'N la MRP nu înseamnă APS și nu garantează toate politicile de lotizare. Rezultatele se testează la modificarea cererii și la rerulare.')
cat('Operații și capacități','E06 E07 E08 E09 T02 T03 F01 SRC_odoo SRC_mfg2',[
('Rute tehnologice','N M N N U A U'),('Centre de lucru și utilaje','N M N N U C U'),('Calendare de resurse','N C N C U C U'),('Durate și cost pe operație','N M N N U A U'),('Vizibilitate încărcare capacități','N C N C U A U'),('Ordine de lucru pe operație','N M N N U A U'),('Optimizare APS globală finită','D D D D U D D'),('Secvențiere cuptor după glazură','D D D D D D D')], 'CRP în plugin și planificarea pe calendare nu sunt echivalente cu optimizarea globală a tuturor resurselor constrânse.')
cat('Execuție și material în curs','E04 E05 E16 T01 T03 F05 SRC_odoo SRC_idempiere V02',[
('Lansare ordin de fabricație','N M N N N N N'),('Consum efectiv de materiale','N M N N N N N'),('Recepție produse finite','N M N N N N N'),('Transfer către stoc WIP','N M N C C C C'),('Raportare producție parțială','N C N N N C C'),('Pontaj pe operație','N M N N U A U'),('Înregistrare opriri utilaj','N C N C U A U'),('Execuție offline cu sincronizare','D D D D D D D')], 'În EVA sunt confirmate bonurile, nu un ciclu complet al ordinului cu operații și raportări multiple de progres.')
cat('Stocuri și trasabilitate','E16 E17 T09 D03 D04 SRC_odoo SRC_idempiere V02',[
('Depozite și locații','N M N N N N N'),('Lot și serie','N M N N N N U'),('Termen de expirare','N M N C N N U'),('Rezervare materiale','N M N N C N U'),('Consum pe lot explicit în UI','N M N C N N D'),('Genealogie lot intrare ieșire','N M N C C C D'),('Split și reunire cu istoric','C M C C U C D'),('Carantină cu interdicție consum','C M C C D C D')], 'Loturile din nucleu nu dovedesc că ecranul EVA propriu le colectează. Un depozit numit Carantină fără regulă de blocare nu satisface ultima cerință.')
cat('Rebuturi și producție de proces','E02 E04 E30 E31 T01 SRC_odoo SRC_mfg2 V02 V04',[
('Rebut sau pierdere declarată','N C N C C C C'),('Produse secundare','N M N C C C C'),('Dezmembrare','N C N C C C N'),('Reprelucrare cu ordin legat','C C C C U C D'),('Randament planificat efectiv','N C N C U A U'),('Rețetă procentuală pe substanță uscată','D D D D D D D'),('Bilanț masă cu umiditate','D D D D D D D'),('Cost energie pe șarjă cuptor','D D D D D D D')], 'BOM cu cantități proporționale nu este automat rețetar de proces. Ultimele trei cerințe sunt scenarii industriale de construit și testat.')
cat('Calitate și conformitate operațională','E13 E14 T10 SRC_idempiere SRC_odoo I17',[
('Teste de calitate și rezultate','N M A C U N U'),('Inspecție la recepție','N M A C U C U'),('Inspecție pe operație','N C A C U A U'),('Blocare și eliberare lot','C M A C D D D'),('Plan de eșantionare industrial','C C A D U D D'),('Neconformitate și CAPA completă','C D A D U D D'),('SPC și capabilitate proces','D D A D U D D'),('Instrucțiune aprobată pe revizie','C C A C C A D')], 'Funcțiile quality de bază nu certifică ISO și nu echivalează cu un sistem QMS complet. OCA este extensie, nu Odoo Community implicit.')
cat('Costuri și contabilitate','E02 E04 T01 T03 F01 F05 SRC_idempiere SRC_odoo V02 V03',[
('Cost materiale în produs','N M N N N N N*'),('Cost manoperă planificat','N M N N C C N*'),('Cost efectiv pe operație','N M N N U A U'),('Regie în cost fabricație','C C C C C C C'),('Evidență WIP și închidere','N M N C U A U'),('Analiză abateri standard efectiv','C C C C U A U'),('Cost istoric pe document','N M N C C N D'),('Reconciliere cu contabilitate RO EVA','D D D D D C C')], 'N* în EVA arată date și propuneri existente; fluxul exact de capitalizare se verifică. Raportul curent nu substituie costul istoric postat.')
cat('Subcontractare și logistică','E15 T05 F01 D07 SRC_odoo I11 I12',[
('Operație externalizată','N M N C C C D'),('Materiale la subcontractor','N C N C C C C'),('Cost serviciu în producție','N M N C C C D'),('Recepție parțială de la terț','N C N C C N C'),('Necesar transport','C C C C C A U'),('Picking pentru producție','N M N C C C C'),('Handling units paleți','C M C C U A U'),('Connector complet WMS EVA','D D D D D D D')], 'Modulele warehouse și manufacturing nu livrează automat o integrare verificată cu WMS-ul ales pentru EVA.')
cat('Mentenanță și oameni','E20 T03 T04 SRC_odoo I02 V01',[
('Registru de utilaje','N M N N C N C'),('Plan mentenanță preventivă','N D N C U A U'),('Contor ore sau cicluri','C C C C U A U'),('Ordin de intervenție','N D N C U A U'),('Angajat asociat lucrării','N M N N C C D'),('Pontaj real versus standard','N M N C U A U'),('Competență obligatorie pe operație','D D D D D D D'),('Integrare AMN și cost orar EVA','D D D D D D D')], 'AMN existent în EVA poate furniza identitatea și costuri aprobate; datele salariale nominale nu trebuie replicate inutil în secție.')
cat('Indicatori și management','E11 E12 F01 T03 SRC_odoo I04 I19 V03',[
('Situație cantitativă producție','N M N N N N N'),('Plan versus realizat','N C N C C A C'),('Timpi pe operație','N M N N U A U'),('Rebut pe cauză și operație','C C C C U D D'),('OEE industrial A × P × Q','C D C D U D D'),('Cost pe ordin și articol','N M N N C A C'),('Kanban vizual configurabil','N C N C C A U'),('Data mart comun EVA producție','D D D D D D D')], 'Eticheta OEE nu garantează aceeași formulă. Raportarea managerială trebuie să excludă ciornele din indicatorii realizați și să păstreze proveniența.')
cat('Administrare și integrare','E90 E91 I90 V01 SRC_odoo F02 T90',[
('Roluri și permisiuni','N N N N N N N'),('Separare firme și organizații','N M N C A N N'),('API sau servicii de extensie','N N N N N N N'),('Conector EVA gata verificat','U U U U U U U'),('Idempotentă integrare cap coadă','D D D D D D D'),('Export și backup autogăzduit','N N N N N N N'),('Română integrală verificată','U U U U U U U'),('Operare fără taxe de licență selectate','N N N N N N N')], 'API existent nu garantează izolare corectă între cabinete și AD_Client. Interfața în română se verifică pentru toate ecranele din scenariu.')

for k in range(0,len(MATRICES),2):
    page('Matrice funcțională '+str(k//2+1),'E = ERPNext; T = Tryton; O = Odoo Community; F = OFBiz; D = Dolibarr; I = iDempiere nucleu; V = EVA inspectată. Codurile sunt definite în capitolul metodologic.')
    for catdata in MATRICES[k:k+2]:
        h(catdata['category'])
        table(['Funcție','E','T','O','F','D','I','V'],[[name]+status.split() for name,status in catdata['rows']],[250,35,35,35,35,35,35,35])
        p(catdata['note']+' Surse: '+catdata['sources']+'.')

page('Evaluarea ponderată și sensibilitatea deciziei')
p('Scorurile de mai jos sunt judecăți de proiectare pe o scară 1–5, nu măsurători de performanță. 5 înseamnă potrivire foarte bună pentru criteriu, 1 efort/risc mare. Formula este suma ponderii × scor / 5. Incertitudinea compatibilității nu poate fi compensată de scor: MFG2 rămâne condiționat de probele eliminatorii.')
SCORES=[['EVA + MFG2',5,4,3,3,5,3,4],['ERPNext',2,5,4,4,4,4,3],['Tryton',2,4,4,3,4,4,3],['Odoo Community',2,4,3,4,4,4,3],['OFBiz',2,4,3,2,5,3,2],['Dolibarr',2,2,2,4,4,4,4]]
WEIGHTS=[30,25,10,10,10,10,5]
table(['Criteriu','Pondere','Interpretare'],[['Integrare cu EVA',30,'Date, procese native, evitarea dublării registrelor'],['Producție integrată',25,'BOM, MRP, rute, execuție și cost'],['Trasabilitate și calitate',10,'Loturi, controale și blocări'],['Operare în secție',10,'Interfață și efort de configurare anticipat'],['Control software liber',10,'Autogăzduire și dependențe'],['Mentenabilitate',10,'Coerență tehnică și verificabilitate'],['Efort inițial',5,'Scor mai mare înseamnă efort relativ mai mic']],[145,60,290])
table(['Soluție','I','P','Q','UX','L','M','Ef','Total'],[[r[0]]+r[1:]+[f'{sum(a*b for a,b in zip(r[1:],WEIGHTS))/5:.1f}'] for r in SCORES],[160,38,38,38,38,38,38,38,69])
p('Sensibilitate: dacă integrarea nativă scade de la 30% la 10%, iar acoperirea producției crește de la 25% la 45%, ERPNext ajunge la 83,0 și MFG2 la 80,0. Ordinea se inversează. Dacă MFG2 nu rezolvă dependențele și corectitudinea contabilă, este eliminat indiferent de total. Scorul de UX este anticipat, cu încredere scăzută până la observația operatorilor.')
p('Recomandarea asumată este deci contextuală: MFG2 pentru integrare în EVA; ERPNext pentru completitudine externă. Nu recomand două piloturi complete în paralel de la început. Mai întâi un test nativ scurt, cu criterii de oprire, apoi alternativa externă dacă testul nu trece.')

page('Arhitectura recomandată pentru integrarea nativă')
p('EVA și iDempiere rămân sistemul autoritativ pentru firme, produse, parteneri, stocuri și contabilitate. MFG2 adaugă planificarea și execuția avansată în aceeași platformă. Un plugin EVA Manufacturing adaptează ecranele, regulile industriale și rapoartele. Numele pluginului este propunere de proiect, nu componentă existentă.')
table(['Strat','Responsabilitate','Regulă'],[
['EVA existentă','Contabilitate RO, documente, cabinete, firme, HR și flux simplu','Se păstrează documentele și seriile istorice.'],
['MFG2','MRP, CRP, PP_Order, operații și colectori de cost','Selectați un singur furnizor de modele/procese pentru aceste tabele.'],
['EVA Manufacturing propus','Rețete aprobate, raportare secție, legături HR și particularități de proces','Extensie prin servicii și validatoare; fără fork inutil al nucleului.'],
['Calitate și mentenanță','Inspecții, loturi blocate și disponibilitate utilaj','Regulile sunt executate la lansare și consum, nu doar în UI.'],
['BI','Indicatori și istorice','Doar citire; nu repară stocuri sau costuri prin SQL.']],[120,195,180])
h('Relația dintre M_Production și PP_Order')
p('Se păstrează M_Production pentru fluxurile simple existente. Pentru ordinele gestionate prin MFG2, consumul și recepția urmează mecanismul validat al PP_Order/PP_Cost_Collector. Bonurile tipărite EVA pot deveni reprezentări ale documentelor rezultat. Nu se creează și o producție M_Production duplicată pentru aceleași cantități. O cheie de legătură explicită identifică sursa și documentul contabil rezultat.')
h('Separarea pe cabinet și firmă')
p('Niciun identificator numeric nu este global între instanțele cabinetelor. Cheia canonică trebuie să conțină instanța, AD_Client și identificatorul entității; AD_Org este păstrat unde este relevant. Toate serviciile verifică tenantul din sesiune față de documentul încărcat. Un planificator de grup nu poate amesteca stocul firmelor fără un flux intercompany explicit.')
h('Upgrade și rollback')
p('JAR-uri fixate prin hash, target platform fixată, migrații de dicționar versionate, backup restaurat în staging și test de reversare. Rollback-ul unui plugin cu migrare de schemă nu se reduce la ștergerea JAR-ului; se stabilește compatibilitatea datelor și strategia de revenire înainte de pilot.')

page('Arhitectura alternativă cu ERPNext')
p('Dacă varianta nativă nu trece pilotul, ERPNext poate gestiona planul și operațiile, iar EVA păstrează contabilitatea legală și documentele financiare. Problema principală este controlul stocului. Trebuie ales explicit dacă stocul operațional se ține în ERPNext și se oglindește în EVA sau dacă fiecare mișcare se confirmă în EVA înaintea progresului execuției.')
table(['Obiect','Sistem autoritativ propus','Sens'],[
['Firmă și identitate cabinet','EVA','EVA → integrare → ERPNext'],
['Produs și unitate','EVA','EVA → ERPNext; extensii tehnologice cu proprietar definit'],
['BOM și rută aprobate','Un singur sistem, stabilit în pilot','Revizie înghețată la lansare; fără editare bidirecțională liberă'],
['Comandă client','EVA','Cerere și modificări → planificator'],
['Operație și timp','ERPNext','Rezultate → EVA și BI'],
['Consum și produs finit','Eveniment unic de execuție','Un eveniment poate genera documente în ambele sisteme, cu reconciliere'],
['Contabilitate și fiscalitate','EVA','Stare de postare → integrare'],
['Angajat','EVA/AMN','Doar datele necesare și drepturile operaționale']],[110,215,170])
p('Nu există o tranzacție distribuită implicită între cele două ERP-uri. Se folosește outbox în sistemul sursă, inbox cu cheie unică în destinație, reîncercări și reconciliere. La căderea conexiunii, operatorul vede „în așteptarea confirmării”; nu primește succes contabil înaintea confirmării. Compensarea se face prin documente de reversare, nu prin ștergerea istoricului.')
h('Decizia care trebuie luată înainte de dezvoltare')
p('Pentru pilot recomand ca EVA să rămână registrul autoritativ de stoc și cost. Evenimentul operațional se confirmă în EVA, apoi se marchează sincronizat. Orice stoc local ERPNext necesar motorului său este oglindă controlată; diferențele blochează închiderea ordinului. Dacă această limită împiedică fluxurile native ERPNext, se reevaluează arhitectura înainte de extindere, în loc de a ascunde două adevăruri contabile.')

page('Modelul de date și contractul de integrare')
table(['Entitate','Cheie minimă și conținut','Control obligatoriu'],[
['Produs','cabinet_id, client_id, product_uuid, cod, UOM','Codul de articol nu este cheie globală; conversii exacte.'],
['BOM revizie','bom_uuid, revision, valid_from/to, aprobat_de, hash','Revizie imuabilă după lansare; compoziție și unități.'],
['Ordin','order_uuid, produs, cantitate, UOM, BOM revizie, termen','Legătură cerere și prioritate; stare validată server-side.'],
['Operație','operation_uuid, secvență, resursă, standard, instrucțiune','Calendar, precedențe, competențe și blocări.'],
['Lot','lot_uuid, articol, sursă, cantitate, stare, expirare','Unicitate și genealogie; segregare lot respins.'],
['Eveniment execuție','event_uuid, sequence, occurred_at, received_at, actor','Idempotentă și ordine; dată de business separată de timpul tehnic.'],
['Cost','cost_event_uuid, monedă, element, sumă, bază repartizare','Dimensiuni și document contabil; fără rotunjiri binare.'],
['Calitate','inspection_uuid, specificație revizie, rezultat, decizie','Cine eliberează lotul și când; istoric nemodificabil.']],[90,230,175])
h('Exemplu de mesaj propus')
p('Tip: production.operation.completed, schema_version=1. Envelope: event_id UUID, source_instance, AD_Client_UU, AD_Org_UU, aggregate_id, aggregate_version, occurred_at UTC, correlation_id. Payload: operație, cantitate bună, rebut, UOM, început/sfârșit, resursă și loturile intrare/ieșire. Costul monetar se transmite ca șir zecimal cu monedă, nu float. Exemplul este un contract de proiectare, nu un endpoint deja existent.')
h('Comenzi și erori')
p('Comenzi propuse: release-order, report-consumption, report-output, record-scrap, close-order și reverse-event. Fiecare are cheie idempotentă și versiune a agregatului. Repetarea aceleiași comenzi cu același conținut returnează același rezultat; același ID cu alt conținut se respinge. Erorile de validare nu se reîncearcă automat, iar erorile temporare intră în coadă cu backoff și limită.')
p('Scrierile în EVA trec prin PO/procese/servicii native. SQL direct se folosește numai pentru citire sau migrații controlate de schemă, conform regulilor proiectului. Finalizarea documentelor nu se simulează prin actualizarea coloanei DocStatus.')

page('Scenariul industrial de validare')
p('Scenariul următor este propus pentru producție ceramică, relevant contextului CESIRO, dar neconfirmat ca proces efectiv al fabricii. Cantitățile și duratele sunt date sintetice de test. Nu sunt plan de producție, norme tehnologice sau parametri recomandați pentru utilaje.')
table(['Etapă','Ce trebuie modelat','Dovada așteptată'],[
['Pregătire materii prime','Rețetă, loturi, masă umedă/uscată, apă și substituții aprobate','Bilanț pe unități compatibile și rețetă fixată.'],
['Formare','Matriță, utilaj, ciclu, schimb și operator','Consum, cantitate, timp și rebut cu cauză.'],
['Uscare','Lot intermediar, durată și resursă','WIP identificabil și randament pe etapă.'],
['Glazurare','Lot glazură, culoare, consum și schimbări','Trasabilitate lot și rețetă de finisaj.'],
['Ardere','Șarjă, încărcare, compatibilități și ciclu','Mai multe ordine într-o șarjă fără pierderea genealogiei.'],
['Sortare','Calitate, defect, rebut/reprelucrare și clasă','Lot blocat până la decizie; diferențiere rezultate.'],
['Ambalare','Articol comercial, set, ambalaj și etichetă','Consum ambalaj și relație produs–lot–livrare.']],[90,225,180])
h('Exemplu de control cantitativ')
p('Ordin test: 1.000 bucăți lansate; 930 bune, 50 rebut și 20 în curs. În unitatea de numărare a pieselor, 1.000 = 930 + 50 + 20. Acest control nu se aplică direct masei materialelor, unde apa evaporată și pierderile tehnologice au altă ecuație. Pentru fiecare bilanț se păstrează aceeași unitate și aceeași frontieră de proces.')
h('Cost și șarjă')
p('Cost bun = materiale consumate + manoperă acceptată + regie repartizată + servicii externe + energie alocată, ajustat pentru tratamentul rebutului și coproductelor aprobat de contabilitate. Pentru cuptor, regula de repartizare poate folosi masa, volumul sau timp/capacitate echivalentă; alegerea se justifică și se versionează. Nu se presupune că o simplă împărțire la numărul de bucăți este corectă pentru produse diferite.')
p('Dacă acest scenariu este obligatoriu, niciun candidat nu primește calificativ „complet implicit” înainte de demonstrarea șarjei mixte, randamentului și genealogiei. Aceste teste pot schimba clasamentul mai mult decât numărul de meniuri disponibile.')

page('Planul de acceptanță și condițiile de oprire')
table(['Test','Execuție','Criteriu de trecere'],[
['T01 Build','Compilare MFG2 pe target EVA 13 fixat','Zero bundle unresolved; servicii și formulare încărcate.'],
['T02 Dicționar','Instalare pe bază clonată și reluare migrare','Fără duplicate/conflicte; backup restaurabil.'],
['T03 BOM','Două revizii și un BOM multinivel','Revizia corectă și cantități exacte; ciclurile se resping.'],
['T04 MRP','Cerere 100, stoc 20, recepție fermă 30','Necesar 50 înainte de politici; rerularea nu dublează ordine.'],
['T05 Capacitate','Două ordine concurente pe aceeași resursă','Supraîncărcare vizibilă sau replanificare explicabilă.'],
['T06 Parțial','Consum și recepție în două tranșe','Sold ordin și stoc coerente; fără dublare.'],
['T07 Lot','Două loturi intrare și două rezultate','Urmărire în ambele sensuri până la livrare.'],
['T08 Calitate','Lot blocat și încercare de consum','Refuz în serviciu și UI; eliberare numai autorizată.'],
['T09 Cost','Material, manoperă, regie, mai multe M_Cost','Fără multiplicare; cost și contabilitate reconciliate.'],
['T10 Anulare','Document postat, apoi reversare','Stoc, cost și note contabile reversate corect.'],
['T11 Izolare','Același cod în două firme și două cabinete','Zero citiri/scrieri cross-tenant.'],
['T12 Retransmisie','Același eveniment trimis de zece ori','Un singur efect de business și răspuns determinist.'],
['T13 Cădere','Întrerupere după salvare înainte de răspuns','Reluare fără pierdere sau dublare.'],
['T14 Perioadă','Consum cu data în perioadă închisă','Respins conform regulilor EVA.'],
['T15 Restaurare','Backup și restore pe mediu gol','Date, documente și legături intacte, raport verificat.'],
['T16 Operator','Flux complet efectuat de utilizatori desemnați','Fără pași ascunși; erori inteligibile și trasabilitate.']],[55,220,220])
p('Pragurile cantitative se calculează în precizia configurată a UOM și monedei. Pentru pilot se propun minimum trei familii de produse și două schimburi, dacă există. Volumul, concurența și timpul de răspuns acceptat se stabilesc din datele reale, nu se inventează un benchmark.')
p('Oprire: imposibilitatea izolării firmelor, dublarea postărilor, lipsa reversării, pierderea genealogiei obligatorii sau imposibilitatea restaurării. Acestea sunt condiții eliminatorii, chiar dacă demonstrația interfeței pare satisfăcătoare.')

page('Etape de implementare și model de cost')
table(['Etapă','Rezultat','Efort orientativ în zile om'],[
['0 Inventar','Versiuni instalate, JAR-uri, dicționar, flux și date curate','3–5'],
['1 Fezabilitate nativă','Build și instalare MFG2, probe T01–T04','5–10'],
['2 Pilot de business','BOM, rute, loturi, cost și reversări','10–20'],
['3 Adaptare EVA','UI, câmpuri tipizate, documente și drepturi','15–30'],
['4 Validare și lansare','Migrare controlată, instruire, restore și reconciliere','10–20'],
['Total inițial nativ','Fără APS ceramică, IoT complex sau QMS complet','43–85']],[95,290,110])
p('Intervalele sunt estimări de planificare ale autorului, cu încredere redusă înaintea etapei 0. Nu reprezintă ofertă sau termen contractual. Varianta externă adaugă integrarea celor două sisteme; buget preliminar separat pentru conector: 20–40 zile om, plus administrarea platformei. Nu se adună automat la totalul nativ, deoarece variantele au lucrări diferite.')
h('Formula de buget')
p('TCO pe trei ani = implementare + migrare + instruire + infrastructură + mentenanță + upgrade + costul intern al operării și incidentelor. Costul de licență poate fi zero în configurația liberă, în timp ce celelalte componente rămân pozitive. Folosiți tariful intern sau oferta furnizorului înmulțită cu zilele om, fără a confunda zilele om cu durata calendaristică.')
h('Responsabilități propuse')
p('Sponsorul aprobă obiectivul și bugetul; responsabilul de producție validează rutele și normele; contabilitatea aprobă tratamentul costurilor și reconcilierea; IT fixează versiunile, backupul și integrarea; calitatea aprobă blocările și genealogia; operatorii validează ergonomia. Acestea sunt roluri propuse, nu persoane deja desemnate.')
h('Livrabilul de ieșire din pilot')
p('Versiuni și hash-uri, configurație exportată, set anonim de date, rezultate pentru fiecare test, diferențe față de cerință, costul estimat revizuit, procedură de restaurare și decizia semnată de responsabili. Dacă MFG2 eșuează din cauze disproporționate de adaptare, se rulează același set de teste în ERPNext, păstrând criteriile comparabile.')

page('Riscuri și decizia finală')
table(['Risc','Măsură','Responsabil propus'],[
['Documentație depășită','Confruntare README/wiki cu manifest și cod; versiuni fixate.','IT'],
['Plugin incompatibil cu EVA','Build pe target exact și instalare doar în staging.','IT'],
['Cost contabil greșit','Reconciliere pe elemente, dimensiuni și documente istorice.','Contabilitate + IT'],
['Lot fără genealogie','Trasabilitate de la recepție la livrare și test de retragere.','Calitate'],
['Date tehnice slabe','Curățare BOM/UOM, aprobarea reviziilor și normelor.','Producție'],
['Două registre de stoc','Sistem autoritativ explicit, idempotentă și reconciliere.','Arhitect integrare'],
['Licență ambiguă a extensiei','Verificarea distribuției și dependențelor înainte de includere.','IT + responsabil juridic'],
['Funcții comerciale presupuse gratuite','Test pe ediția liberă curată, fără module Enterprise.','Responsabil produs'],
['Adopție slabă în secție','Probe cu operatori, scanare și mesaje în română.','Producție'],
['Instalare excesivă de pluginuri','Minimul necesar pentru test; un singur motor de fabricație.','IT']],[130,270,95])
p('Propun aprobarea unei etape limitate de fezabilitate pentru EVA + MFG2, cu buget și termen stabilite pe baza inventarului real. Alegerea pentru integrarea nativă este MFG2; alegerea externă cu cea mai bună acoperire generală în această analiză este ERPNext. Tryton rămâne alternativa modulară, Odoo Community alternativa cu ecosistem larg, OFBiz varianta pentru personalizare Java, iar Dolibarr varianta pentru producție simplă.')
p('Nu recomand migrarea contabilității românești din EVA doar pentru a obține un modul de producție. Nu recomand nici construirea de la zero a întregului MRP înainte de a testa pluginul nativ existent. Recomandarea se schimbă dacă testele de izolare, cost, loturi sau operare nu trec ori dacă fabrica cere implicit funcții de proces pe care niciun candidat nu le demonstrează.')
p('Acest raport nu declară integrarea realizată sau aplicațiile validate în producție. El oferă inventarul, dovezile, diferențele și criteriile necesare pentru o decizie verificabilă. Publicarea documentației în GitHub nu constituie aprobarea unei schimbări în producție.')

EVA_SHA='1c039193e0c1626cb03fb8ca37f9980a1703fd0c'
BASE='https://github.com/cesiroproduction/Eva-Accounting/blob/'+EVA_SHA+'/'
SOURCES_EVA=[
('V01','Arhitectura EVA','README.md'),
('V02','Producție EVA','idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/form/WSagaProductieForm.java'),
('V03','Raport producție EVA','idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/form/WSagaSituatieProductieForm.java'),
('V04','Dezmembrări EVA','idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/form/WSagaDezmembrariForm.java'),
('V05','Bon consum EVA','idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/form/WSagaBonConsumForm.java'),
('V06','Registru documente EVA','idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/documente/RegistruDocumente.java')]
