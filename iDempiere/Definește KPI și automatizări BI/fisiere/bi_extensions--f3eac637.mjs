export const industries = `
A|01|Agricultură|Randament t/ha; cost/ha; marjă/cultură; consum apă/ha; pierderi recoltă; necesar lucrări|Parcelă, cultură, sezon, fermă|Registru agricol, utilaje, cântare, meteo|Prognoză recoltă și alertă abateri de consum|Randament = producție recoltată / suprafață recoltată
A|014; 03|Zootehnie și acvacultură|Conversie furaje; producție/cap; mortalitate; spor în greutate; cost/kg; cicluri reproducție|Lot, specie, fermă, ciclu|Evidență efective, furaje, cântare|Alertă consum anormal și lot cu abatere|Conversie furaje = furaj consumat / spor masă, aceeași cohortă
A|02|Silvicultură|Cost/m³; randament exploatare; volum pe sortimente; utilizare utilaje; pierderi; trasabilitate lot|Parcelă, lot, sortiment|Exploatare, transport, documente proveniență|Reconciliere volum intrare–ieșire|Randament = volum valorificat / volum intrat
B|05–09|Extracție|Cost/tonă; recuperare; disponibilitate instalații; raport steril/util; energie/tonă; incidente|Zăcământ, schimb, instalație|Producție, laborator, mentenanță|Alertă oprire și cost peste plan|Cost/tonă = cost atribuibil / tone utile
C|10–12|Alimente și băuturi|Randament rețetă; pierderi; trasabilitate lot; stoc cu expirare; cost/kg; retururi calitate|Lot, rețetă, linie, SKU|MES, laborator, WMS, temperaturi|FEFO și alertă temperatură/expirare|Randament = cantitate conformă / cantitate teoretică
C|13–18; 31|Textile, lemn, mobilă, tipar|Consum normat versus real; randament debitare; rebut; cost/comandă; timp setare; marjă variantă|Comandă, material, variantă|BOM, operații, pontaj|Propunere reducere pierderi și replanificare|Randament debitare = material util / material consumat
C|19–23|Chimie, farmaceutice, materiale|Yield lot; consum specific; loturi blocate; energie/tonă; neconformități; timp eliberare lot|Rețetă, lot, reactor, test|MES, QMS, laborator|Alertă abatere proces și carantină conform regulilor validate|Yield = cantitate conformă / cantitate teoretică
C|24–30; 32–33|Metal, echipamente, automotive|OEE; PPM; cost unitar; first pass yield; OTIF; variație cost materiale|Linie, piesă, client, schimb|ERP, MES, QMS|Predicție defect și aprovizionare piese critice|OEE = disponibilitate × performanță × calitate
D|35|Energie și utilități energetice|Producție MWh; disponibilitate; consum propriu; pierderi rețea; marjă/MWh; dezechilibre|Centrală, punct, interval, contract|SCADA, contoare, contracte|Alertă dezechilibru și prognoză producție|Marjă/MWh = contribuție / MWh livrați
E|36–39|Apă, deșeuri, mediu|Apă nefacturată; cost/m³; energie/m³; reciclare; cost/tonă; incidente mediu|Zonă, rută, instalație|Contoare, cântare, dispecerat|Detectare pierderi și optimizare rute|Apă nefacturată = volum intrat în sistem − volum facturat; componente separate
F|41–43; 4100|Construcții|Marjă șantier; EAC; lucrări nefacturate; productivitate echipă; progres fizic; garanții reținute|Șantier, deviz, etapă|Devize, situații lucrări, pontaje|Alertă depășire cost și întârziere etapă|EAC = cost realizat + cost pentru restul lucrărilor
G|46|Distribuție B2B|Marjă/client; cost-to-serve; DSO; fill rate; rotație stoc; rebate furnizor|Client, agent, SKU, rută|ERP, CRM, WMS|Credit control și reaprovizionare|Fill rate = unități livrate inițial / unități solicitate
G|47|Retail fizic|Vânzări/m²; marjă/SKU; bon mediu; conversie vizitatori; pierderi inventar; disponibilitate la raft|Magazin, SKU, oră|POS, WMS, trafic|Alertă ruptură stoc și promoții sub marjă|Bon mediu = vânzări nete / bonuri eligibile
G|46–47, după bunuri și activitate|Comerț electronic|Conversie; abandon coș; CAC; marjă după livrare; retururi; valoare comandă|Canal, cohortă, produs|Magazin online, plăți, ERP, curier|Recuperare internă excepții plată și retur|Marjă/comandă include cost produs, plată, livrare și retur atribuit
H|49–53|Transport și logistică|Venit/km; cost/km; kilometri goi; grad încărcare; OTIF; cost/expediere|Vehicul, rută, client|TMS, GPS, combustibil|Replanificare rută și avertizare ETA|Marjă cursă = venit cursă − cost direct și alocat
H|52|Depozitare pentru terți|Ocupare locații; linii/oră; acuratețe picking; cost/palet; SLA; marjă/client|Depozit, zonă, client|WMS, pontaj, contracte|Echilibrare capacitate și identificare erori|Ocupare = locații ocupate / locații utilizabile
I|55; 5510|Hoteluri și cazare|Ocupare; ADR; RevPAR; GOPPAR; anulări; cost distribuție|Proprietate, tip cameră, canal|PMS, rezervări, ERP|Prognoză ocupare și propuneri tarif|RevPAR = venit camere / camere disponibile în perioada analizată
I|56; 5611; 5612|Restaurante și catering|Food cost; marjă preparat; bon mediu; rotație mese; risipă; cost personal/venit|Locație, preparat, interval|POS, rețete, rezervări|Propunere producție și aprovizionare după cerere|Food cost = cost ingrediente consumate / venit relevant fără TVA
J|58–60|Media și conținut|ARPU; audiență; retenție abonat; venit/conținut; grad vânzare publicitate; cost producție|Titlu, canal, abonament|Ad server, abonamente, producție|Alertă churn și optimizare programare|ARPU = venit relevant / utilizatori plătitori medii
J/K|582; 62–63|Software și SaaS|MRR; ARR; NRR; churn; CAC payback; marjă cloud|Produs, client, cohortă|Billing, CRM, telemetrie|Scor risc churn și control cost infrastructură|ARR = 12 × MRR doar pentru venit recurent comparabil; NRR exclude clienții noi
K|61|Telecom|ARPU; churn; disponibilitate rețea; utilizare capacitate; cost instalare; tichete/1000 clienți|Rețea, regiune, ofertă|Billing, OSS/BSS, NMS|Alertă degradare și prioritizare remediere|Disponibilitate = minute serviciu funcțional / minute eligibile
K|62; 6210; 6220|Servicii IT|Utilizare facturabilă; marjă proiect; backlog; SLA; timp livrare; defecte scăpate|Proiect, contract, echipă|Pontaje, proiecte, ticketing|Alertă depășire estimare și SLA|Utilizare = ore facturabile / ore disponibile definite
L|64–66|Financiar și asigurări|Cost/venit; restanțe portofoliu; pierderi credit; lichiditate; rată daune; retenție polițe|Produs, portofoliu, client|Core banking/asigurări, risc|Monitorizare abateri de portofoliu cu validare specialist|Rata daune = daune suportate / prime câștigate; metodologia sectorială obligatorie
M|68; 6812|Imobiliare și dezvoltare|Ocupare; NOI; rent collection; WAULT; cost/m²; precontractări|Activ, chiriaș, proiect|Contracte, property management, ERP|Alertă expirare chirie și cash-flow proiect|NOI = venit operațional proprietate − cheltuieli operaționale definite
N|69; 6920|Contabilitate, audit și juridic|Marjă/client; documente/operator; dosare incomplete; închidere la termen; WIP; depuneri acceptate|Client, specialist, obligație|Dosare, pontaje, documente, ERP|Listă documente lipsă și calendar de lucru|Marjă/client = onorariu − cost serviciu atribuibil
N|70–75; 7020|Consultanță, inginerie, cercetare|Utilizare; tarif realizat; marjă proiect; backlog; etape acceptate; venit/client|Proiect, specialist, serviciu|CRM, proiecte, pontaj|Alertă lucrări nefacturate și depășire buget|Tarif realizat = venit muncă / ore facturabile
O|77–82|Servicii suport și închirieri|Utilizare echipamente; venit/activ; cost/intervenție; SLA; acoperire ture; marjă contract|Activ, locație, contract|Contracte, programări, pontaj|Reînnoiri și planificare resurse|Utilizare închiriere = zile închiriate / zile disponibile
P|84|Administrație publică|Execuție buget; cost/serviciu; termen soluționare; cereri restante; achiziții în termen; satisfacție beneficiar|Program, serviciu, instituție|Buget, registratură, achiziții|Alertă termen și depășire angajamente|Execuție = cheltuieli efective / buget aprobat, pe bază definită
Q|85|Educație|Ocupare cursuri; retenție cursanți; absolvire; cost/cursant; încasare taxe; utilizare săli|Curs, cohortă, centru|SIS/LMS, programări, ERP|Alertă abandon și facturi restante|Absolvire = absolvenți / cohortă eligibilă
R|86–88|Sănătate și asistență socială|Timp așteptare; neprezentare; utilizare capacitate; cost/episod; deconturi respinse; satisfacție|Unitate, serviciu, plătitor|HIS, programări, ERP|Confirmare operațională programări și tratare deconturi respinse|Neprezentare = programări neprezentate / programări eligibile; datele clinice au acces separat
S|90–93|Cultură, sport și recreere|Ocupare eveniment; venit/loc; utilizare facilități; retenție membri; cost/eveniment; anulări|Eveniment, locație, abonament|Ticketing, rezervări, ERP|Prognoză cerere și alertă marjă eveniment|Ocupare = locuri vândute / locuri disponibile
T|94–96|Servicii personale și reparații|Utilizare programări; bon mediu; revenire clienți; first-time fix; cost lucrare; marjă serviciu|Locație, specialist, lucrare|Programări, service, POS|Rechemare service propusă și aprovizionare piese|First-time fix = lucrări rezolvate prima dată / lucrări închise
U|97–98|Gospodării private|Cost resurse; ore lucrate; respectare buget; consum; programări; lucrări restante|Activitate, perioadă|Pontaje și evidențe proprii|Alerte buget și programări|Pachet simplificat; relevanță redusă pentru BI comercial
V|99|Organizații extrateritoriale|Execuție buget program; cost/beneficiar; rezultate program; termene; angajamente; achiziții|Program, proiect, finanțator|Programe, buget, achiziții|Raportare către finanțator și monitorizare termene|Rezultate / resurse pe metodologia programului
`.trim().split('\n').map((s,i)=>{const [section,codes,industry,metrics,dimensions,data,automation,definition]=s.split('|');return {id:`IND-${String(i+1).padStart(2,'0')}`,section,codes,industry,metrics,dimensions,data,automation,definition};});

export const functions = [];
function group(category,priority,lines){for(const s of lines.trim().split('\n')){const [name,requirement,test]=s.split('|');functions.push({id:`F-${String(functions.length+1).padStart(3,'0')}`,category,name,requirement,test,priority});}}
group('Date și integrare','P0',`
Conectori ERP și contabilitate|API, baze de date și fișiere cu contract de date|Un document nou apare o singură dată cu ID sursă
Import incremental|Capturarea modificărilor și ștergerilor logice|Reîncărcarea nu dublează tranzacții
Orchestrare încărcări|Dependențe, reluări, istoric și ferestre de procesare|O sursă indisponibilă generează incident identificabil
Reconciliere la sursă|Totaluri și număr înregistrări pe firmă și perioadă|BI se potrivește cu extrasul ERP aprobat
Calitate date|Validare chei, tipuri, completitudine și relații|O factură fără client intră în coada de excepții
Istoric și versiuni|Păstrarea stării istorice a clienților, produselor și bugetelor|Raportul închis poate fi reprodus
Catalog și proveniență|Traseu sursă–transformare–indicator|Utilizatorul identifică sursa unui total
Monitorizare prospețime|Ora evenimentului și ora încărcării afișate separat|Încărcarea reușită cu date vechi nu apare ca proaspătă
`);
group('Definiții și control financiar','P0',`
Dicționar KPI|Definiții și responsabil aprobate, cu versiune|Venitul din AI este identic cu venitul din raport
Plan de conturi configurabil|Mapări locale și de grup, reguli pe perioade|Un cont nemapat este semnalat
Entități și consolidare|Firme, sucursale și eliminări intercompany|Vânzarea internă este eliminată o singură dată
Monede și cursuri|Curs tranzacție, raportare și scenariu|Raportul explică diferența de curs
Calendar și închidere|Perioade fiscale, zile lucrătoare și stări provizoriu/final|Raportul final rămâne reproductibil
Costuri și alocări|Baze de alocare transparente, cu reconciliere|Total cost alocat este egal cu baza distribuită
Solduri și rate corecte|Agregare specifică tipului de măsură|Soldul lunar nu însumează soldurile zilnice
Control ajustări|Explicație, autor și aprobare pentru orice ajustare managerială|EBITDA ajustat se reconciliază cu EBIT contabil
`);
group('Panouri și explorare','P0',`
Panou pe rol|CEO, CFO, contabil, vânzări, operațiuni și HR|Fiecare rol vede doar indicatorii și datele permise
Comparații și trend|Actual, buget, forecast și perioadă comparabilă|Utilizatorul identifică perioada și comparatorul
Drill-through|Total până la client, tranzacție și document|Suma detaliilor explică exact totalul selectat
Analiză ad-hoc|Dimensiuni și măsuri selectabile din modelul aprobat|Managerul răspunde unei întrebări noi fără dezvoltare
Filtre și bookmarks|Filtre persistente, vizibile și ușor de resetat|Exportul păstrează contextul filtrelor
Vizualizări potrivite|Tabele, waterfall, cohortă, hartă și distribuție după întrebare|Graficul păstrează unitățile și arată lipsurile
Mobile și accesibilitate|Ecran adaptat, contrast și navigare cu tastatura|KPI critice sunt lizibile pe telefon
Listă de excepții|Impact estimat, responsabil, termen, stare|Excepția poate fi atribuită și închisă verificabil
`);
group('AI conversațional și explicații','P1',`
Întrebări în română|Vocabular economic local și sinonime|Setul românesc de întrebări etalon este trecut
Răspuns cu proveniență|Metrică, perioadă, filtre, sursă și calcul vizibile|Utilizatorul poate reproduce suma răspunsului
Clarificarea ambiguității|Întrebări suplimentare pentru venit, profit sau client ambiguu|AI cere baza și perioada înainte de calcul
Răspunsuri verificate|Bibliotecă de întrebări și rezultate certificate|Întrebarea standard folosește definiția aprobată
Rezumat managerial|Abateri, factori asociați, implicații și acțiuni sugerate|Fiecare număr din rezumat se regăsește în date
Generare rapoarte|Vizualizări și calcule propuse de AI|Raportul se validează înainte de publicare
Documente și date împreună|Contracte și proceduri citate lângă datele ERP|Clauza citată este din versiunea contractuală corectă
Abținere și evaluare AI|Răspuns indisponibil când dovezile lipsesc|Întrebarea fără date nu produce cifre inventate
`);
group('Predicții și optimizare','P2',`
Forecast cerere|Sezonalitate, promoții și evenimente|Depășește o prognoză simplă pe date nefolosite la antrenare
Forecast numerar|Scadențe, comportament de plată și scenarii|Eroarea pe orizont este raportată săptămânal
Detectare anomalii|Praguri statistice și reguli de business|Alarmele au rată de fals pozitiv măsurată
Factori ai variației|Descompuneri și asocieri explicate|Corelația este etichetată și nu prezentată ca o cauză dovedită
Risc churn și neplată|Scoruri calibrate pe cohorte|Calibrarea și precizia sunt măsurate pe perioade noi
Simulare what-if|Preț, volum, curs, cost și personal|Ipotezele și efectele sunt reproductibile
Optimizare cu restricții|Stoc, rute și capacitate în limite aprobate|Soluția respectă capacitatea și limitele operaționale
Monitorizare modele|Drift, erori, versiune și retragere model|Modelul degradat revine la o regulă verificată
`);
group('Planificare și colaborare','P1',`
Bugete pe factori|Cantitate, preț, salarii, termene și investiții|Modificarea unui factor actualizează ieșirile relevante
Versiuni scenarii|Bază, favorabil și nefavorabil cu ipoteze proprii|Scenariile nu suprascriu realizatul
Write-back plan|Scriere în tabele de plan autorizate și versionate|Bugetul schimbat păstrează autorul și versiunea
Flux aprobare plan|Responsabili, termene, delegări și blocare|Versiunea aprobată nu se modifică fără revizie
Comentarii contextualizate|Comentariu legat de KPI, perioadă și filtre|Comentariul rămâne pe contextul original
Pachet ședință|Raport periodic cu explicații și decizii|Raportul poate fi refăcut la data de referință
Export Excel și PDF|Date filtrate, unități și metadate incluse|Exportul respectă drepturile și totalurile
Distribuție personalizată|Abonamente pe rol și canal autorizat|Destinatarul primește doar perimetrul permis
`);
group('Automatizări și acțiuni','P1',`
Motor de reguli|Eveniment, condiție, prag, fereastră și responsabil|Regula este testabilă pe date istorice
Fluxuri vizuale|Pași, condiții, aprobări și tratare erori|O eroare oprește numai pașii dependenți
Acțiuni prin API|Creare sarcini și propuneri ERP/CRM|Acțiunea produce ID și stare de confirmare
Idempotență|Cheie unică pe eveniment și acțiune|Reluarea nu produce o a doua comandă
Simulare înainte de activare|Mod de observare fără efect operațional|Operatorul vede acțiunile care s-ar fi executat
Aprobări și limite|Plafoane valorice, roluri și listă acțiuni permise|Acțiunea peste plafon așteaptă aprobarea
Escaladare și deduplicare|Agregare alerte, interval de liniște și SLA|Aceeași problemă nu generează avalanșă de mesaje
Rezultat și oprire|Verificare efect, jurnal și mecanism de suspendare|Administratorul oprește fluxul și vede execuțiile afectate
`);
group('Securitate și administrare','P0',`
Identitate unică|SSO și autentificare conform politicii|Revocarea utilizatorului oprește accesul
Acces pe rând și coloană|Separare firme, departamente și date sensibile|Utilizatorul nu obține date interzise prin AI sau export
Izolare clienți|Separare tenant și context pentru produs oferit terților|Testele nu detectează acces între clienți
Jurnal audit|Citire sensibilă, export, modificări și acțiuni|O acțiune se reconstruiește cu autor și rezultat
Politici de păstrare|Retenție, ștergere și arhivare configurate|Datele expirate urmează politica aprobată
Control date trimise către AI|Furnizor, regiune, conținut și utilizări documentate|Administratorul vede exact clasele de date transmise
Mediu test și producție|Publicare controlată și revenire la versiune|Schimbarea eronată poate fi retrasă
Continuitate serviciu|Backup, restaurare și plan de recuperare|Restaurarea este demonstrată pe o copie de test
`);
group('Performanță și cost','P0',`
SLA de răspuns|Ținte pe volum, concurență și complexitate|Se măsoară p95 la încărcarea agreată
Scalare|Cache, agregări și capacitate adaptată|Testul concurent păstrează SLA-ul
Observabilitate|Jurnale, metrici și urmărirea erorilor|Incidentul poate fi localizat la sursa lui
Control cost cloud și AI|Cost pe raport, întrebare și automatizare|Consum peste buget produce alertă
Utilizare conținut|Rapoarte nefolosite și KPI solicitați|Echipa poate retrage conținut redundant
Portabilitate|Export modele, definiții, date și configurații|Datele pot fi recuperate la încetarea contractului
API și embed|Integrare în ERP și portal cu identitate transmisă corect|Raportul integrat respectă același acces
Management versiuni CAEN|Revizie, corespondențe și pachete pe activități multiple|Firma cu două activități primește ambele pachete
`);
group('Localizare România','P1',`
e-Factura monitorizare|Stări, răspunsuri și diferențe față de ERP|Trimiterea nu este confundată cu validarea
SAF-T control|Mapări și verificări de completitudine și reconciliere|Erorile sunt afișate înaintea fluxului de depunere
TVA reconciliere|Jurnale și declarații comparate cu diferențe explicate|Diferența are documente și responsabil
e-Transport monitorizare|Identificatori și stări pentru transporturile eligibile|Excepția indică expedierea și datele lipsă
Calendar fiscal configurabil|Obligații după profil și reguli cu valabilitate|Schimbarea regulii păstrează istoricul
Formate și vocabular local|Lei, valute, diacritice, calendare și termeni contabili|Exportul și AI folosesc aceleași definiții
`);

export const automations = [];
function auto(domain,owner,lines){for(const s of lines.trim().split('\n')){const [trigger,action,level,proof]=s.split('|');automations.push({id:`A-${String(automations.length+1).padStart(3,'0')}`,domain,trigger,action,owner,level,proof});}}
auto('Conducere și financiar','CEO / CFO',`
Ora raportului zilnic și date reconciliate|Generează briefing cu 12 KPI, 5 excepții și acțiuni|L1|Raport legat de data și versiunea surselor
Abatere profit peste pragul propriu|Descompune variația și deschide sarcină la controlling|L2|Sarcină cu factori și sumă reconciliată
Numerar proiectat sub buffer|Produce scenarii de colectare și amânare plăți|L2|Scenarii cu ipoteze și solduri pe 13 săptămâni
Comandă depășește bugetul disponibil|Propune blocare sau excepție pentru aprobare|L3|Decizie aprobată și stare ERP confirmată
Cost recurent crește anormal|Identifică contractul și solicită verificare internă|L2|Cost verificat și cauză înregistrată
Indicator strategic sub țintă|Deschide plan de remediere cu responsabil și termen|L2|Plan și rezultat urmărit
`);
auto('Creanțe și datorii','Credit control / trezorerie',`
Factură client devine restantă|Pregătește notificarea și sarcina de colectare|L2|Ciornă și sarcină; trimiterea urmează politica autorizată
Promisiune de plată nerespectată|Escaladează la responsabilul de client|L2|Promisiune și încasări verificate
Expunere depășește limita de credit|Propune reținerea comenzii noi|L3|Aprobare și confirmarea stării comenzii
Extras bancar nou|Propune potriviri între tranzacții și facturi|L2|Potriviri cu diferențe explicate
Potrivire bancară exactă și regulă aprobată|Aplică alocarea prin fluxul autorizat|L3|Alocare unică, jurnal și reconciliere
Factură furnizor posibil duplicată|Oprește fluxul propus și trimite la verificare|L2|Dublura confirmată ori respinsă documentat
Scadențe apropiate și cash insuficient|Pregătește lot de plăți prioritizat|L2|Propunere de lot; autorizarea plății rămâne în sistemul financiar
Discount de plată eligibil|Compară beneficiul cu costul lichidității|L2|Calcul și recomandare aprobabilă
`);
auto('Contabilitate și fiscalitate','Contabil-șef',`
Zi de închidere lunară|Generează checklist din reconcilieri și documente lipsă|L2|Checklist cu responsabili și stări
Diferență subregistru–carte mare|Izolează documentele care explică diferența|L2|Total diferențe egal cu abaterea raportată
e-Factură fără confirmare|Reverifică starea după politica de reluare|L1|Răspuns API păstrat; fără retransmitere oarbă
e-Factură respinsă|Deschide sarcină cu eroarea și documentul sursă|L2|Corecție în sistemul sursă și răspuns nou
Document prezent fiscal dar absent în ERP|Propune verificare și înregistrare în coadă|L2|Confirmare apartenență și document justificativ
Factura ERP și fiscală au același identificator|Compară conținutul, păstrând ambele versiuni|L1|Hash, identificatori și diferențe arhivate
Fișier SAF-T generat|Rulează validări și reconcilieri|L1|Raport de erori și controale, fără depunere automată implicită
Diferență de TVA identificată|Construiește lista de documente de investigat|L2|Explicație și rezoluție aprobate
Certificat sau acces aproape de expirare|Creează sarcină de reînnoire|L2|Acces retestat după reînnoire
Document fiscal nou disponibil|Arhivează originalul și metadatele prin conector autorizat|L1|Integritate și posibilitate de regăsire verificate
`);
auto('Comercial și clienți','Vânzări / customer success',`
Oportunitate fără activitate|Creează sarcină pentru agent și sugerează pasul următor|L2|Activitate înregistrată sau motiv închidere
Ofertă sub marja minimă|Solicită excepție comercială|L3|Aprobare și marjă explicată
Client cu risc churn ridicat|Propune intervenție bazată pe semnale verificabile|L2|Acțiune și evoluție retenție măsurată
Contract se apropie de reînnoire|Creează dosar cu utilizare, marjă și propunere|L2|Decizie de reînnoire în CRM
Campanie depășește costul țintă|Propune modificare buget sau pauză|L3|Aprobare înaintea schimbării bugetului extern
Creștere retururi la produs|Leagă vânzări, loturi și reclamații pentru analiză|L2|Cauză verificată și acțiune atribuită
Tichet se apropie de limita SLA|Escaladează după severitate și responsabil|L2|Tichet preluat și termen confirmat
Vârf de cerere într-un canal|Actualizează prognoza și propune realocare stoc|L2|Plan verificat față de stoc și capacitate
`);
auto('Achiziții, stoc și logistică','Achiziții / logistică',`
Stoc proiectat sub necesar|Pregătește cerere de aprovizionare|L2|Cerere cu cerere estimată, lead time și stoc de siguranță
Cerere în limitele politicii aprobate|Trimite spre fluxul de comandă autorizat|L3|Comandă unică, aprobare și confirmare furnizor
Lot aproape de expirare|Propune FEFO, transfer sau campanie|L2|Plan și stoc afectat confirmate
Stoc fără mișcare|Propune reducere achiziții ori lichidare|L2|Valoare recuperabilă estimată și decizie
Întârziere furnizor|Propune alternativă și reevaluează promisiunile de livrare|L2|Impact pe comenzi calculat
ETA depășește termenul clientului|Creează excepție logistică și ciornă de informare|L2|Nou termen aprobat și expediere identificată
Vehicul sau rută subutilizată|Propune consolidarea curselor|L2|Capacitate, restricții și economii verificate
Transport eligibil cu date fiscale incomplete|Cere completarea câmpurilor și verificarea responsabilului|L3|Verificare în fluxul operațional înainte de expediere
`);
auto('Producție, active și proiecte','Operațiuni / PMO',`
OEE sub pragul liniei|Identifică pierderi de timp, viteză și calitate|L2|Sarcină cu pierderi reconciliate
Senzor sau model indică degradare|Propune inspecție de mentenanță|L2|Intervenție validată de tehnician
Mentenanță preventivă scadentă|Creează ordin de lucru conform planului aprobat|L3|Ordin unic și resurse rezervate
Lot cu rezultat neconform|Aplică fluxul de carantină validat|L3|Stare lot confirmată; eliberare doar prin rol autorizat
Consum peste normă|Deschide investigație BOM, măsurare sau pierdere|L2|Diferență explicată pe material
EAC depășește bugetul proiectului|Propune replanificare și solicitare de schimbare|L2|Nou scenariu și impact contractual
Etapă proiect acceptată|Pregătește propunerea de facturare|L2|Document acceptanță și bază de facturare atașate
Schimbare contract fără aprobare|Semnalează lucrările și impactul estimat|L2|Decizie comercială documentată
`);
auto('HR, energie și control','HR / mediu / control intern',`
Autorizație profesională aproape de expirare|Creează sarcină de reînnoire|L2|Certificat validat și dată actualizată
Ore suplimentare peste limita internă|Semnalează echipa și propune redistribuire|L2|Plan aprobat, fără decizii automate de personal
Consum energie anormal|Deschide inspecție pe echipament și interval|L2|Cauză verificată și economii ulterioare
Contract critic aproape de expirare|Escaladează către juridic și titularul contractului|L2|Decizie și termen de notificare confirmate
Conflict de atribuții detectat|Creează cerere de revizuire acces|L2|Revizuire documentată și test de acces
Acțiune audit restantă|Escaladează conform politicii|L2|Responsabil și nou termen aprobat
`);
auto('Platformă de date și AI','CIO / echipa BI',`
Sursă nu a fost actualizată în SLA|Marchează panoul ca întârziat și notifică responsabilul|L1|Timestamp eveniment și incident vizibile
Control financiar eșuează|Oprește publicarea indicatorului afectat și păstrează ultima versiune validă etichetată|L1|Diferență și perimetru afectat în jurnal
Întrebare AI fără date suficiente|Cere clarificare sau declară lipsa dovezii|L1|Fără sumă inventată în răspuns
Eroare model peste pragul validat|Propune retragerea modelului și fallback verificat|L2|Versiune și rezultat backtest păstrate
Cost AI/cloud peste buget|Limitează sarcini necritice conform politicii|L3|Consum și aplicarea limitei înregistrate
Flux a eșuat după scriere parțială|Verifică starea destinației înainte de reluare|L1|Acțiune fără duplicat și compensare dacă este aplicabilă
`);

export const needs = [
 ['Încredere în cifre','BARC','Prioritate acordată calității, securității și guvernanței','Definiții aprobate și reconcilieri automate','F-004; F-009','Sondajul susține tema; nu un clasament al celor zece produse.'],
 ['Viteză și adoptare','BARC2','Performanța este o problemă recurentă în evaluările utilizatorilor','Teste de concurență și p95 pe volumul firmei','F-065; F-066','Timpul acceptabil depinde de scenariu.'],
 ['Documente accesibile AI','BARC3','Datele nestructurate pot fi greu de descoperit și urmărit','Catalog, permisiuni și citarea versiunii documentului','F-031','Studiu pe eșantion global, fără extrapolare la toate firmele.'],
 ['Ușurință versus complexitate','G2','Extrasul recenziilor menționează învățarea și performanța Power BI, integrarea Qlik','Probe cu manageri, timp până la primul raport și cost total','F-017; F-065','Pagina directă a fost indisponibilă; folosit doar extrasul indexat, fără scoruri proprii.'],
 ['Cost și rapoarte explicabile','TRUST','Recenziile laudă vizualizarea Tableau și reclamă costuri, latență sau explicații insuficiente','Dicționar KPI, buget de cost și probe de volum','F-009; F-068','Unele recenzii sunt stimulate; experiențele diferă între versiuni.'],
 ['De la P&L la document','FDRILL','Un utilizator cere detaliul valorilor dintr-o matrice financiară','Drill-through reconciliat la tranzacții','F-019','Fir vechi, relevant pentru nevoie; soluțiile tehnice se verifică în versiunea actuală.'],
 ['Excel pentru analiză proprie','FEXCEL','Un utilizator din finance explică nevoia de date granulare și modelare iterativă','Export filtrat și explorare flexibilă cu definiții comune','F-020; F-047','Discuție calitativă, fără frecvență statistică.'],
 ['Adopția AI conversațional','FAI','Discuția cere experiențe reale de introducere a conversațiilor cu datele','Pilot cu set etalon și măsurarea utilizării','F-025; F-032','Nu se deduce o rată generală de succes.'],
 ['Duplicate e-Factura','FDUP','Utilizatorul descrie retransmiterea unei facturi corectate','Identificatori unici, versiuni și coadă de verificare','F-052; F-073','Relatarea nu stabilește tratamentul fiscal corect.'],
 ['Plăți fără document complet','FMISS','Utilizatorul reclamă facturi lipsă pentru plăți de ridesharing','Reconciliere bancă–document–sistem fiscal','F-004; F-073','Opiniile fiscale ale participanților nu sunt preluate ca reguli.'],
 ['Alerte SPV utile','FSPV','Autorul propune notificări, iar comentariile întreabă ce valoare adaugă peste notificările existente','Alertă cu acțiune, context, responsabil și deduplicare','F-024; F-055','Fir de validare comercială, potențial promoțional.'],
 ['Arhivare documente','FARCH','Utilizatorul nu mai găsește un document nedescărcat','Arhivare original și metadate, cu căutare','F-061; F-073','Nu folosim termenul invocat în forum drept termen legal verificat.'],
 ['Integrare cu contabilitatea','FERP','Discuția descrie dificultăți între e-Factura și programe contabile','Conector și reconciliere completă, monitorizare erori','F-001; F-004','Fir din 2023; conectorii existenți astăzi trebuie retestați.']
];

export const executive = [
 ['Venituri nete','FIN-01','Buget și an anterior comparabil','Ce segment explică abaterea?'],
 ['Marjă de contribuție','FIN-03','Buget și preț-volum-mix','Ce produse ori clienți reduc profitul?'],
 ['EBITDA managerial','FIN-04','Buget, an anterior și reconciliere EBIT','Este abaterea recurentă?'],
 ['Numerar utilizabil','CASH-01','Buffer minim aprobat','Ce plăți pot fi susținute?'],
 ['Minim cash în 13 săptămâni','CASH-05','Scenariu bază și nefavorabil','Când apare nevoia de finanțare?'],
 ['Creanțe restante','AR-02','Aging și concentrarea pe clienți','Cine trebuie contactat și pentru ce sumă?'],
 ['DSO','AR-05','Termene contractuale și trend','Se deteriorează încasarea?'],
 ['Portofoliu comenzi','SAL-02','Capacitate și termen promis','Ce venit este susținut de comenzi?'],
 ['Valoare și vechime stoc','INV-01','Stoc fără mișcare și cerere','Unde este blocat numerarul?'],
 ['OTIF ori SLA sectorial','LOG-01','Ținta contractuală','Care clienți sunt afectați?'],
 ['Buget disponibil','PLAN-07','Angajamente și realizat','Ce cheltuieli noi pot fi aprobate?'],
 ['Reconciliere și prospețime','DATA-01; DATA-02','Toleranță și SLA de date','Sunt cifrele utilizabile pentru decizie?']
];

export const roadmap = [
 ['Etapa 1: definiții și surse','Inventar surse, dicționar, responsabilități, acces, profil fiscal și CAEN','Aprobare definiții și reconciliere pe perioadă de referință'],
 ['Etapa 2: nucleu managerial','P&L, numerar, creanțe, datorii, vânzări și stoc; 12 KPI și drill-through','Cifre reconciliate, filtre corecte, acces și export validate'],
 ['Etapa 3: operațiuni și alerte','Pachet CAEN relevant, cozi de excepții și automatizări L1–L2','Fiecare alertă are responsabil, SLA și rezultat măsurabil'],
 ['Etapa 4: planificare și AI','Bugete, scenarii, prognoze și conversație în română','Set etalon trecut, abținere corectă și prognoze validate'],
 ['Etapa 5: acțiuni în sisteme','Automatizări L3 cu API, limite, aprobări și verificare rezultat','Reluări fără duplicate și mecanism de oprire testat']
];
