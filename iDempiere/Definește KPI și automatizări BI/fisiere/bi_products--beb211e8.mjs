export const products = [];
export const capabilities = [];
function vendor(name,fit,limitation,presentation,help,lines){
 products.push({name,fit,limitation,presentation,help});
 for(const s of lines.trim().split('\n')){const [capability,evidence,status='Documentat',condition='Validare ediție, regiune și acces în ofertă']=s.split('|');capabilities.push({platform:name,capability,evidence,status,condition});}
}
vendor('Microsoft Power BI / Fabric + Copilot','BI financiar și operațional în ecosistem Microsoft; model semantic și integrare largă','Copilot cere capacitate eligibilă; Pro/PPU singure nu ajung. Unele experiențe sunt preview. Româna se testează explicit; documentația are restricții multilingve.','PBIP','PBI',`
Întrebări despre model și rapoarte|PBI
Creare și modificare rapoarte cu AI|PBI
Generare interogări DAX|PBI
Rezumate în raport și abonamente|PBI
Descrieri pentru măsuri|PBI
Pregătire model, instrucțiuni și răspunsuri verificate|PBI2
Căutare între rapoarte și modele|PBI|Preview pentru experiența standalone|Capacitate și setări tenant
Asistență AI la modelare web|PBI|Preview|Drept de scriere și model pe capacitate eligibilă
`);
vendor('Tableau Cloud + Tableau Agent / Pulse','Explorare vizuală și monitorizare personalizată de metrici','Pulse este documentat pentru Cloud. Agent in Pulse, corelațiile și forecast-ul premium țin de Tableau+. Verificați diferențele Cloud/Server/Desktop.','TABP','TAB',`
Asistență la creare vizualizări|TAB
Creare și explicare câmpuri calculate|TAB
Asistență pentru pregătirea datelor și descrieri|TAB
Metrici urmărite de fiecare utilizator|PULSE
Digesturi prin email și Slack|PULSE
Întrebări conversaționale pe grupuri de metrici|PULSEQ|Documentat, premium|Tableau+ și activare la nivel de site
Citarea metricilor în răspuns|PULSEQ
Metrici corelate și prognoze Pulse|PULSEP|Documentat, premium|Disponibilitate Tableau+
`);
vendor('Qlik Cloud Analytics + Answers / Predict / Automate','Analize asociative, date și documente în același context, automatizări','Experiența agentică Answers diferă de varianta legacy. Insight Advisor nu se utilizează simultan în tenantul cu experiența agentică; modulele și capacitatea se verifică separat.','QLIK2','QLIK',`
Conversație pe date structurate din aplicații|QLIK
Răspunsuri din baze de cunoștințe documentare|QLIK
Citarea surselor utilizate|QLIK
Asistenți cu date și documente curate|QLIK
Acțiuni prin automatizări conectate asistentului|QLIK|Documentat, configurabil|Conectori, drepturi și automatizări pregătite
Explorare și vizualizare asociativă|QLIK3
Modele predictive fără cod|QLIK3|Documentat în Qlik Predict|Entitlement și limite de consum de confirmat
Integrare AI prin mecanisme de conectare Qlik|QLIK2|Documentat în ghid de evaluare|Verificare a conectorului și a drepturilor efective
`);
vendor('Google Looker + Gemini','Definiții comune în LookML, analytics integrat în aplicații și ecosistem Google','Looker și Looker Studio sunt produse distincte. Gemini necesită activare; agenții de dashboard pot fi preview. Costul warehouse și licențele se includ în evaluare.','LOOKP','LOOK',`
Întrebări în limbaj natural pe Explores|LOOK2
Agenți de date cu instrucțiuni proprii|LOOK2
Context din maximum cinci Explores pe agent|LOOK2|Documentat|Limita se reconfirmă pentru ediția ofertată
Întrebări verificate pentru contextul agentului|LOOK2
Analize avansate prin Python în conversație|LOOK
Generare expresii și asistență LookML|LOOK
Personalizare vizualizări prin limbaj natural|LOOK
API și integrare în aplicații pentru conversații|LOOKP|Prezentare oficială|Validare drepturi, autentificare și costuri API
`);
vendor('Amazon Quick / Quick Sight','BI pe AWS combinat cu agenți, cercetare și fluxuri între aplicații','Documentația actuală folosește Amazon Quick; materiale mai vechi spun QuickSight sau Quick Suite. Componentele suitei nu sunt echivalente cu licența BI de bază.','AWSP','AWS',`
Dashboarduri și analytics prin Quick Sight|AWS
Seturi de date, conexiuni structurate și SPICE|AWS
Agenți cu instrucțiuni și surse configurate|AWS
Spaces pentru documente, dashboarduri și context comun|AWS
Quick Flows pentru sarcini repetitive|AWS2
Quick Automate pentru procese cu intervenție umană|AWS
Quick Research pentru rapoarte cu surse|AWS
Conectori OpenAPI/MCP și extensii în aplicații|AWS|Documentat, configurabil|Validare autentificare, acțiuni și drepturi pe destinație
`);
vendor('SAP Analytics Cloud + Joule','BI plus planificare financiară și operațională, în special în ecosistem SAP','Funcțiile depind de licență, platformă și centru de date. Predicția pe modele de planning are restricții; funcții din alte produse SAP pot apărea în prezentări.','SAPP','SAP',`
Întrebări de business prin Just Ask|SAP2
Comparare actual versus forecast în interogări|SAP2
Analytical Insights prin Joule|SAP
Smart Insights pentru explicații|SAP
Smart Predict pentru scenarii predictive|SAP
Predicții în planificare pe serii temporale|SAP3|Documentat cu restricții|Planning Predictive nu acoperă toate tipurile de model
Versiuni, bugete și simulări what-if|SAPP2|Prezentare oficială|Licență de planificare și drepturi corespunzătoare
Conținut de business și scenarii de risc Compass|SAPP|Prezentare oficială|Module și disponibilitate confirmate în probă
`);
vendor('Oracle Analytics Cloud + AI Assistant','Pregătire, analiză și vizualizare în mediul Oracle și surse mixte','OAC, Oracle Analytics Server și produsele EPM au perimetre diferite. Crearea de data flows cu AI este indicată ca preview în catalogul consultat.','ORAP','ORA3',`
Întrebări conversaționale prin AI Assistant|ORA
Agenți cu context și surse de business|ORA
Explain pentru a investiga o coloană sau măsură|ORA2
Contextual insights pentru vizualizări|ORA3
Interacțiune AI pentru explorare și vizualizare|ORA3
Pregătirea și îmbogățirea datelor|ORAP|Prezentare oficială
Fluxuri de date create cu asistent AI|ORA3|Preview|Verificare disponibilitate și limitări
Colaborare și analiză pe surse cloud sau hibride|ORAP|Prezentare oficială|Nu implică paritate între toate edițiile
`);
vendor('IBM Cognos Analytics + agentic AI','Raportare enterprise, distribuție și control centralizat','Funcțiile diferă între ofertele Cognos. AI on-premises presupune serviciu instalat și configurat; watsonx BI este prezentat ca add-on distinct.','IBMP','IBM',`
Rapoarte multipagină în PDF, Excel, HTML și CSV|IBMP
Dashboarduri interactive și explorare|IBMP
Asistent pentru întrebări și vizualizări|IBMP
Agenți specializați pentru lucru cu rapoarte|IBM
Recomandare rapoarte și rezumare|IBMP|Prezentare oficială|Confirmare ediție, model și activare
Forecast cu intervale și detalii statistice|IBM2
Driver analysis pentru factori predictivi|IBM3|Documentat cu restricții|Poate folosi eșantionare; filtrele nu sunt suportate pe vizualizarea descrisă
Extindere conversațională prin watsonx BI|IBM4|Add-on|Licență și integrare separate
`);
vendor('ThoughtSpot + Spotter','Analiză prin conversație și integrare de analytics în produse','Versiunile Spotter au diferențe. Unele planuri noi îl includ, iar planurile embedded sau legacy pot cere add-on. Prezentările despre acțiuni trebuie demonstrate în tenant.','TSP2','TS',`
Întrebări și răspunsuri pe modelul de date|TS
Întrebări multiple și sugestii de aprofundare|TS
Explicarea câmpurilor și formulelor|TS
Pregătirea vocabularului și contextului de business|TS
Monitorizare KPI și alerte email/Slack|TS2
SpotterModel pentru modele semantice|TS3|Documentat în portal|Confirmare versiune și entitlement
SpotterViz pentru Liveboards și SpotterCode pentru dezvoltare|TS3|Documentat în portal|Module distincte de confirmat
Acțiuni către aplicații și embed|TSP|Prezentare oficială|Necesită conectori, drepturi și validare în probă
`);
vendor('Zoho Analytics + Ask Zia','BI pentru echipe care vor analytics, pregătire și rapoarte asistate într-un pachet accesibil de evaluat','GenAI este documentat pentru Premium/Enterprise. Zia Insights indică engleză, spaniolă și franceză; româna nu trebuie presupusă. Configurația LLM și datele transmise contează.','ZOHOP','ZOHO',`
Rapoarte și dashboarduri create prin conversație|ZOHO
Pipeline-uri, formule și interogări sugerate|ZOHO3
Rezumate narative și vizuale|ZOHO2
Analize trend, sezonalitate și anomalii|ZOHO2
Forecasting și clusterizare|ZOHO3
Key Driver Analysis și explorare diagnostică|ZOHO2
Data stories și acțiuni de export/distribuție|ZOHO
Integrarea Ask Zia în aplicații și configurare LLM|ZOHO|Documentat, configurabil|Permisiuni, plan și opțiuni de partajare date
`);

export const criteria = [
 ['Corectitudinea financiară și trasabilitatea',20,'Reconciliere pe perioadă închisă și navigare până la document'],
 ['Integrarea cu ERP și sursele firmei',15,'Probe de import, actualizare, ștergere logică și recuperare după eroare'],
 ['Securitate și izolare',15,'Teste negative pe rând, coloană, AI, export și clienți diferiți'],
 ['Utilitate managerială și utilizare',10,'CEO/CFO rezolvă scenariile fără ajutor de dezvoltare'],
 ['AI în română și verificabilitate',10,'Set de întrebări etalon, clarificări, citări și abținere'],
 ['Automatizări și acțiuni',10,'Aprobare, idempotență, audit și verificare destinație'],
 ['Planificare și particularități sectoriale',5,'Buget, scenarii și cinci cazuri specifice industriei'],
 ['Performanță și disponibilitate',5,'p95 la concurența și volumul contractate'],
 ['Cost total pe 3 ani',5,'Autori, cititori, AI, capacitate, conectori, implementare și mentenanță'],
 ['Portabilitate și administrare',5,'Export definiții/date, versionare, operare și ieșire din contract']
];
export const acceptance = [
 ['Reconciliere','Diferență zero la baza monetară agreată sau toleranță de rotunjire justificată','Pe firmă, cont, perioadă și monedă; documente duplicate sau lipsă explicate'],
 ['Acces','Zero dezvăluiri neautorizate în probe','Teste prin dashboard, AI, API, export și distribuție'],
 ['Răspuns panou','Țintă inițială p95 ≤ 3 secunde','Propunere, nu benchmark de produs; volum și concurență stabilite în pilot'],
 ['Prospețime','Financiar zilnic; operațional 5–15 minute unde este util','Propuneri; acceptate numai dacă sursa și costul susțin nevoia'],
 ['AI critic','100% corect pe setul financiar critic aprobat','Set finit de test; nu înseamnă garanție pentru orice întrebare'],
 ['AI general','Țintă inițială ≥ 95% pe setul etalon general','Separat se măsoară refuzurile corecte, erorile și costul'],
 ['Automatizări','Zero duplicate la reluări și verificare a rezultatului','Simulare timeout după scriere, erori API, anulare și reexecutare'],
 ['Forecast','Rezultat mai bun decât prognoza simplă pentru orizontul util','Test pe perioade nefolosite la antrenare, cu WAPE și bias'],
 ['Utilitate','Timp redus pentru pregătirea și explicarea raportului','Comparație înainte/după, cu costul complet al operării'],
 ['Preț și disponibilitate','Ofertă scrisă cu module, regiune, limite și funcții preview','Prețurile și scorurile comerciale nu au fost inventate în acest catalog']
];
