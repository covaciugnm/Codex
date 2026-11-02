/* Regenerare: node tools/quality-review-build.cjs. Nu modifică datele auditate ale catalogului. */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const root = path.resolve(__dirname, '..'), dir = path.join(root, 'imbunatatire-raspunsuri');
const inputFiles = new Set();
function read(file, json = true) { inputFiles.add(file); const s = fs.readFileSync(path.join(root, file), 'utf8').replace(/^\uFEFF/, ''); return json ? JSON.parse(s) : s; }
const local = f => read('imbunatatire-raspunsuri/' + f);
const history = local('istoric-conversatie.json'), requests = local('analiza-solicitari.json'), requirements = local('cerinte-atomice.json');
const methods = local('metode-imbunatatire.json'), experiments = local('plan-experimente.json'), claims = local('registru-afirmatii.json');
const evolution = local('evolutie-concluzii.json'), sources = local('surse-metodologice.json');
const functions = read('catalog-parametri-functii/functii.json'), params = read('catalog-parametri-functii/parametri.json');
const coverage = read('catalog-parametri-functii/acoperire.json'), schemas = read('catalog-parametri-functii/scheme.json');
const flutterAudit = read('catalog-parametri-functii/audit-flutter.json'), inv = read('inventar/summary.json');
const docs = read('documentatie/summary.json'), validation = read('catalog-parametri-functii/validare.json');
const firmware = read('firmware-analiza/audit.json'), sdk = read('../SDK_Experimental/sdk-manifest.json');
const sdkTest = read('../SDK_Experimental/test-results.txt', false), auditState=require('./audit-state.cjs')(root), audit=read('audit-calitate/'+auditState.current.folder+'/audit.json');
const independent = read('imbunatatire-raspunsuri/revizie-independenta.txt', false);
const deliveryReview = fs.existsSync(path.join(dir,'revizie-livrare.txt')) ? read('imbunatatire-raspunsuri/revizie-livrare.txt',false) : null;
read('imbunatatire-raspunsuri/model-raspuns.txt', false); read('imbunatatire-raspunsuri/dovada-air2-google-play-apk.txt', false);
const now = new Date().toISOString();
const write = (f,d) => fs.writeFileSync(path.join(dir,f), JSON.stringify(d,null,2)+'\n');
const countBy = (a,key) => a.reduce((o,x) => (o[x[key]]=(o[x[key]]||0)+1,o),{});
const flutter = functions.filter(x=>x.kind==='Flutter MethodChannel'), receive = functions.filter(x=>x.kind==='recepție BLE');
const has = (x,k) => Array.isArray(x[k]) && x[k].length>0;
const unresolvedStrings = flutterAudit.flatMap(x=>(x.unresolvedCandidates||[]).map((s,i)=>({id:'candidate:'+x.file+':'+i, name:typeof s==='string'?s:JSON.stringify(s), source:x.file, kind:'șir candidat, nu metodă confirmată'})));
const functionItem = x => ({id:x.id,name:x.name,kind:x.kind,source:x.source,line:x.line,href:'../catalog-parametri-functii/FUNCTII.html#'+x.id});
const parameterItem = x => ({id:x.id,name:x.name,scope:x.scope,javaType:x.javaType,functionIds:x.functionIds,href:'../catalog-parametri-functii/PARAMETRI.html#'+x.id});
const groups = [
  {id:'unknown-types',title:'Parametri cu tip necunoscut',priority:'P0',rule:'javaType === necunoscut',denominator:params.length,unit:'fișe parametru',items:params.filter(x=>x.javaType==='necunoscut').map(parameterItem),next:'Identifică producătorul și consumatorul valorii; confirmă tipul, unitatea și conversia. Nu completa după nume.'},
  {id:'flutter-output',title:'Flutter fără câmpuri output documentate',priority:'P1',rule:'kind Flutter MethodChannel și outputParameterIds gol',denominator:flutter.length,unit:'fișe Flutter',items:flutter.filter(x=>!has(x,'outputParameterIds')).map(functionItem),next:'Urmărește fiecare Result și callback. Separă void/ACK, eroare, rezultat delegat și schemă încă neextrasă.'},
  {id:'flutter-result',title:'Flutter fără observații Result',priority:'P1',rule:'kind Flutter MethodChannel și resultObservations gol',denominator:flutter.length,unit:'fișe Flutter',items:flutter.filter(x=>!has(x,'resultObservations')).map(functionItem),next:'Caută invocarea delegată, callbackul și ramura de dispatch. Poate fi o limită a extractorului.'},
  {id:'ble-output',title:'Recepții BLE fără câmpuri output',priority:'P0',rule:'kind recepție BLE și outputParameterIds gol',denominator:receive.length,unit:'fișe recepție',items:receive.filter(x=>!has(x,'outputParameterIds')).map(functionItem),next:'Stabilește dacă mesajul este fără payload, delegat sau neextras; păstrează separat modelul local.'},
  {id:'ble-paths',title:'Recepții BLE fără schemaPaths',priority:'P1',rule:'kind recepție BLE și schemaPaths gol',denominator:receive.length,unit:'fișe recepție',items:receive.filter(x=>!has(x,'schemaPaths')).map(functionItem),next:'Adaugă calea și condiția de profil numai din parser. Lipsa căilor nu înseamnă absența oricărei documentări.'},
  {id:'channel-candidates',title:'Șiruri de canal încă neclasificate',priority:'P2',rule:'audit-flutter[].unresolvedCandidates',denominator:null,unit:'ocurențe de șiruri',items:unresolvedStrings,next:'Clasifică metode/evenimente/enum/alte constante; nu le aduna la cele 443 funcții confirmate.'}
];
groups.forEach(g=>g.count=g.items.length);
const queue={generatedAt:now,scope:'Seturi suprapuse de verificare a extracției, nu defecte confirmate și nu un total de funcții lipsă.',groups};
write('coada-verificare.json',queue);
const ratio=(id,title,n,d,unit,meaning,limit,source)=>({id,title,numerator:n,denominator:d,percent:Math.round(n/d*10000)/100,unit,meaning,limit,source});
const messages=history.turns.flatMap(x=>x.messages);
const finals=messages.filter(x=>x.role==='assistant'&&x.phase==='final_answer'&&!x.id.startsWith('call_'));
const metrics=[
  ratio('K01','Flutter cu câmpuri output',flutter.filter(x=>has(x,'outputParameterIds')).length,flutter.length,'fișe Flutter','Prezența outputParameterIds în catalog.','Nu măsoară SDK complet; lipsa câmpurilor nu dovedește că funcția nu întoarce nimic.','catalog-parametri-functii/functii.json'),
  ratio('K02','Flutter cu observații Result',flutter.filter(x=>has(x,'resultObservations')).length,flutter.length,'fișe Flutter','Cel puțin o observație; există separat '+flutter.reduce((n,x)=>n+(x.resultObservations||[]).length,0)+' înregistrări de observație.','O observație poate fi o eroare sau expresie delegată, fără schemă completă.','catalog-parametri-functii/functii.json'),
  ratio('K03','Parametri cu tip necunoscut',groups[0].count,params.length,'fișe parametru','javaType exact necunoscut. Reducerea cere dovadă, nu presupuneri.','Tip cunoscut nu garantează semantică, interval, unitate sau obligativitate.','catalog-parametri-functii/parametri.json'),
  ratio('K04','Recepții BLE cu câmpuri output',receive.filter(x=>has(x,'outputParameterIds')).length,receive.length,'fișe recepție','Prezența câmpurilor extrase în selecția de recepții.','Selecția de 90 intrări nu este totalul răspunsurilor posibile ale firmware-ului.','catalog-parametri-functii/functii.json'),
  ratio('K05','Recepții BLE cu schemaPaths',receive.filter(x=>has(x,'schemaPaths')).length,receive.length,'fișe recepție','Prezența căilor explicite îmbogățite în catalog.','Este una dintre formele documentării recepțiilor; lipsa schemaPaths nu înseamnă absența documentării.','catalog-parametri-functii/functii.json')
];
const futureMetrics=[
  {id:'Q01',title:'Trasabilitatea afirmațiilor decisive',formula:'afirmații inventariate cu sursă aplicabilă + limită / afirmații decisive inventariate',status:'registru selectiv creat; universul complet al propozițiilor nu este inventariat',limit:'100% înseamnă trasabilitate în registru, nu adevăr universal.'},
  {id:'Q02',title:'Acoperirea cerințelor',formula:'distribuția criteriilor acceptate / parțiale / cu limită explicită / nelivrate',status:'40 criterii clasificate editorial; stările nu sunt însumate într-un scor',limit:'O întrebare de fezabilitate nu necesită implementarea unui produs necerut.'},
  {id:'Q03',title:'Defecte semantice pe eșantion',formula:'cazuri cu defect / cazuri revizuite, pe strat și severitate; neclarificate separat',status:'E09 propus, neevaluat încă',limit:'Selecția intenționată de cazuri critice nu produce automat o estimare pentru întregul APK.'},
  {id:'Q04',title:'Progres cu valoare pentru decizie',formula:'incertitudini critice închise prin dovezi / incertitudini critice planificate pentru runda curentă',status:'necalculat; următoarea rundă fixează traseele și criteriile înaintea testării',limit:'Mai multe fișiere sau teste nu sunt în sine beneficii.'},
  {id:'Q05',title:'Performanță audio și STT',formula:'WER pe corpus fix; latență p50/p95 pe condiție; cuvinte înțelese de utilizator separat',status:'E04–E06 propuse, fără rezultate pe dispozitiv',limit:'Repetarea aceleiași înregistrări nu adaugă vorbitori independenți; inteligibilitatea nu este WER.'},
  {id:'Q06',title:'Actualitatea dovezilor',formula:'intrări cu sursă/versiune schimbată sau depășită / intrări monitorizate',status:'manifest SHA-256 local generat; nu există monitorizare web automată',limit:'Hashul local nu dovedește că pagina web nu s-a schimbat.'}
];
const indicators={generatedAt:now,apkVersion:coverage.apkVersion,apkSha256:coverage.apkSha256,
  conversation:{turns:history.turns.length,completedRequests:requests.length,substantiveFinalAnswers:finals.length,userMessages:messages.filter(x=>x.role==='user').length,requirements:requirements.length,requirementStates:countBy(requirements,'assessment'),note:'Instantaneu istoric al analizei inițiale; indicatorii catalogului sunt recalculați separat. Raportul urmărește cele 17 solicitări anterioare. Prezența unui răspuns nu dovedește satisfacerea integrală a cererii.'},
  methods:{count:methods.length,states:countBy(methods,'status')},experiments:{count:experiments.length,states:countBy(experiments,'status')},
  claims:{count:claims.claims.length,scope:claims.scope},metrics,futureMetrics,
  quantities:{detailedFunctions:functions.length,parameters:params.length,schemas:schemas.length,sourceFiles:coverage.sources,dexClasses:inv.classes,dexMethods:inv.declaredMethods,nativeLibraries:inv.nativeLibraries,methodsNotDecompiled:inv.methodsNotDecompiled,javaFilesWithIssues:inv.javaFilesWithIssues,uniqueDocumentTexts:docs.uniqueDocuments,documentTextCharacters:docs.uniqueCharacters},
  maturity:[
    {stage:'Inventar DEX',state:'livrat',evidence:inv.classes+' clase / '+inv.declaredMethods+' metode',limit:'Structura include biblioteci și metode sintetice; nu reprezintă semantică integrală.'},
    {stage:'Catalog detaliat',state:'analiză statică selectivă',evidence:functions.length+' fișe funcții / '+params.length+' parametri',limit:'Granularitate diferită față de metodele DEX; nu calculăm un procent prin împărțire.'},
    {stage:'Documentație extrasă',state:'inventariată și sintetizată selectiv',evidence:docs.uniqueDocuments+' texte unice în indexul documentatie/summary.json',limit:'Nu include automat toate textele din toate arhivele și nu demonstrează lectură integrală.'},
    {stage:'SDK experimental',state:'compilat și testat offline',evidence:'v'+sdk.version+'; '+(sdkTest.match(/PASS (\d+) codec/)||[])[1]+' verificări codec/comenzi; simulare ABI recorder',limit:'Nu este un client BLE/audio autonom verificat.'},
    {stage:'Verificări catalog existente',state:'structură și regresii',evidence:validation.assertions+' aserțiuni raportate',limit:'Nu sunt '+validation.assertions+' funcții validate semantic sau pe ochelari.'},
    {stage:'Audit independent al catalogului',state:auditState.matchesCurrentData?audit.score+'/'+audit.maximum+' în domeniul declarat':'istoric; date modificate după evaluare',evidence:'runda '+audit.round,limit:audit.scope.coverageNote},
    {stage:'Integrare pe hardware / cloud',state:coverage.hardwareTested||coverage.cloudTested?'consultați sursa':'netestată în catalog',evidence:'hardwareTested='+coverage.hardwareTested+'; cloudTested='+coverage.cloudTested,limit:'Nu inventăm măsurători sau succes de conectare.'},
    {stage:'Imagine firmware',state:firmware.confirmedGlassesFirmwareImages+' imagini confirmate',evidence:firmware.archivesScanned+' arhive scanate în auditul firmware',limit:'Traseul OTA și fișierele de modele neuronale nu sunt imagine de firmware a ochelarilor.'}
  ]};
write('indicatori.json',indicators);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const data={requests:requests.map(q=>({...q,answers:history.turns.find(t=>t.id===q.turnId).messages.filter(x=>q.finalMessageIds.includes(x.id))})),requirements,methods,experiments,claims:claims.claims,evolution,sources,indicators,queue};
const downloads=['RAPORT.txt','analiza-solicitari.json','cerinte-atomice.json','registru-afirmatii.json','evolutie-concluzii.json','metode-imbunatatire.json','plan-experimente.json','indicatori.json','coada-verificare.json','manifest-intrari.json','istoric-conversatie.json','model-raspuns.txt','revizie-independenta.txt','dovada-air2-google-play-apk.txt','surse-metodologice.json'];
if(deliveryReview)downloads.push('revizie-livrare.txt');
if(fs.existsSync(path.join(dir,'validare.json')))downloads.push('validare.json');
let html=`<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Calitatea răspunsurilor · iFLYTEK</title><link rel="stylesheet" href="review.css"></head><body>
<header><div class="eyebrow">iFLYTEK · analiză la 30 octombrie 2026</div><h1>Răspunsuri mai precise.<br>Dovezi care pot fi verificate.</h1><p class="lead">${requests.length} solicitări și răspunsuri analizate, ${requirements.length} criterii explicite, ${methods.length} metode de îmbunătățire. Separăm calitatea explicației, acoperirea documentară și funcționarea demonstrată.</p><nav aria-label="Documentație"><a href="../INDEX.html">Catalog APK</a><a href="../catalog-parametri-functii/INDEX.html">Funcții și parametri</a><a href="../audit-calitate/INDEX.html">Auditul anterior</a><a href="RAPORT.txt">Raport TXT</a></nav></header>
<main><section class="notice" id="completare-air2"><b>Completare confirmată: Air 2 permite aplicații în versiunea descrisă de FAQ-ul UK.</b><p>Jurnalul oficial din 28.01.2025 descrie certificarea Google Play și instalarea APK, omise din comparația inițială. Se verifică regiunea și firmware-ul exemplarului. Aceasta nu confirmă integrarea cu ochelarii. <a href="https://uk.iflytek.com/en/pages/ainote-air2-faq">FAQ oficial</a> · <a href="dovada-air2-google-play-apk.txt">Dovadă și metodă de acces</a></p></section>
<div class="summary-grid"><article><strong>${requests.length}</strong><span>răspunsuri de fond</span></article><article><strong>${claims.claims.length}</strong><span>afirmații decisive urmărite</span></article><article><strong>${methods.length}</strong><span>metode cu criterii</span></article><article><strong>${experiments.length}</strong><span>experimente propuse, neexecutate</span></article></div>
<p class="scope">Analiză a istoricului și artefactelor disponibile, cu revizie independentă. Nu este o nouă verificare factuală exhaustivă a fiecărei propoziții. Scorul anterior 10/10 rămâne limitat la domeniul acelui audit; nu acordăm un scor global tuturor răspunsurilor.</p>
<nav class="tabs" aria-label="Secțiuni raport"><button data-tab="requests" aria-pressed="true">Solicitări</button><button data-tab="methods">Metode</button><button data-tab="metrics">Indicatori</button><button data-tab="queue">De verificat</button><button data-tab="experiments">Experimente</button><button data-tab="claims">Afirmații și evoluție</button><button data-tab="sources">Surse și fișiere</button></nav>
<section id="panel-requests" class="panel"><h2>Fiecare cerere, împreună cu răspunsul și îmbunătățirea</h2><p>„Parțial” descrie acoperirea, nu presupune o afirmație falsă. O întrebare despre fezabilitate nu impune construirea unei aplicații necerute.</p><label for="request-search">Caută în întrebări și analiză</label><input id="request-search" type="search" placeholder="Ex.: firmware, căști, Wi-Fi"><p id="request-count" class="small" role="status"></p><div id="requests-list"></div></section>
<section id="panel-methods" class="panel" hidden><h2>Metode și criterii de succes</h2><p>Prioritatea P0 privește o incertitudine care poate schimba decizia; P1 îmbunătățește fiabilitatea; P2 clasifică materialul auxiliar. Efortul este estimativ.</p><label for="method-state">Starea aplicării</label><select id="method-state"><option value="all">Toate</option><option value="done">Aplicate integral, selectiv sau parțial</option><option value="planned">Propuse / plan pregătit</option></select><p id="method-count" class="small" role="status"></p><div id="methods-list" class="cards"></div></section>
<section id="panel-metrics" class="panel" hidden><h2>Cantitatea are nevoie de unitate și numitor</h2><p>Acestea sunt numărători din catalogul actual. Nu sunt procente ale unui SDK, firmware sau protocol complet.</p><div id="metrics-list" class="cards"></div><h2>Starea rezultatelor</h2><div id="maturity-list"></div><h2>Indicatorii următoarei runde</h2><div id="future-list" class="cards"></div><h2>Criterii editoriale</h2><p id="requirement-states"></p><p class="small">Criteriile au fost descompuse retrospectiv pentru această analiză. Nu se prezintă drept praguri stabilite înaintea răspunsurilor istorice. Categoriile nu sunt însumate într-un scor de completitudine.</p></section>
<section id="panel-queue" class="panel" hidden><h2>Lista concretă de verificare</h2><p>Grupele se pot suprapune. O lipsă în extracție este o întrebare de investigat; nu dovedește o funcție defectă sau un rezultat absent.</p><label for="queue-group">Grupă</label><select id="queue-group"></select><label for="queue-search">Filtru ID / nume / clasă</label><input id="queue-search" type="search"><div id="queue-note"></div><p id="queue-count" role="status"></p><div class="table-scroll"><table><thead><tr><th>ID</th><th>Nume</th><th>Context / sursă</th></tr></thead><tbody id="queue-list"></tbody></table></div><div class="pager"><button id="prev-page">Înapoi</button><span id="queue-page"></span><button id="next-page">Înainte</button></div><p><a href="coada-verificare.json">Lista integrală JSON</a></p></section>
<section id="panel-experiments" class="panel" hidden><h2>De la incertitudine la probă</h2><p>Toate cele ${experiments.length} experimente sunt propuse și neexecutate. Datele deja cunoscute: ochelari deținuți, Android, actualizare firmware încă nedescărcată. E01 precedă testele pe dispozitiv; E02 → E03 → E04; E05/E06 evaluează utilitatea audio. E07 și E08 au dependențe proprii; E09 poate începe din corpusul local.</p><div id="experiments-list"></div></section>
<section id="panel-claims" class="panel" hidden><h2>Afirmații decisive și limite</h2><p>${esc(claims.scope)} O sursă statică poate susține implementarea observată; rezultatul pe dispozitiv cere altă dovadă.</p><div id="claims-list"></div><h2>Ce s-a schimbat și de ce</h2><div id="evolution-list"></div></section>
<section id="panel-sources" class="panel" hidden><h2>Surse primare pentru metode</h2><div id="sources-list"></div><h2>Revizie și reproducibilitate</h2><p><a href="revizie-independenta.txt">Revizia independentă</a> a recalculat indicatorii și a confirmat omisiunea Air 2. Istoricul complet al mesajelor vizibile este păstrat separat; nu include raționamente interne sau toate rezultatele instrumentelor.</p><p>Regenerare din directorul APK: <code>node tools/quality-review-build.cjs</code>. Verificare: <code>node tools/quality-review-verify.cjs</code>. Manifestul păstrează SHA-256 pentru intrări și dovezile locale utilizate; nu monitorizează automat paginile web.</p><ul class="downloads">${downloads.map(f=>'<li><a href="'+f+'">'+esc(f)+'</a></li>').join('')}</ul></section>
</main><footer>Generat ${esc(now)} · APK ${esc(coverage.apkVersion)} · <a href="model-raspuns.txt">Model de răspuns și sinteză actualizată</a></footer><script id="review-data" type="application/json">${JSON.stringify(data).replace(/</g,'\u003c')}</script><script src="review.js"></script></body></html>`;
if(fs.existsSync(path.join(root,'reverificare-detaliata/INDEX.html')))html=html.replace('<body>','<body><p id="reverificare-detaliata" style="padding:16px;background:#e5f2ed;border-left:4px solid #177963"><a href="../reverificare-detaliata/INDEX.html"><strong>Reverificare detaliată: RPK, produse, parametri și protocol</strong></a> · '+params.length+' parametri · '+groups[0].count+' tipuri încă necunoscute · dovezi și limite.</p>');
fs.writeFileSync(path.join(dir,'INDEX.html'),html);
const report=`ANALIZA SOLICITĂRILOR ȘI ÎMBUNĂTĂȚIREA RĂSPUNSURILOR
Generat: ${now}
APK analizat: ${coverage.apkVersion}; SHA-256 ${coverage.apkSha256}

DOMENIU
Au fost analizate ${requests.length} solicitări anterioare și ${finals.length} răspunsuri finale de fond, împreună cu clarificările și artefactele disponibile. Istoricul salvat are ${history.turns.length} ture și ${messages.filter(x=>x.role==='user').length} mesaje utilizator, inclusiv cererea actuală. Două întrebări asincrone marcate final_answer nu sunt răspunsuri de fond.
Aceasta este analiză editorială/documentară cu revizie independentă selectivă. Nu constituie reverificare factuală exhaustivă a tuturor produselor, fiecărei propoziții sau metode decompilate. Nu acordă un scor global. Auditul anterior 10/10 rămâne în domeniul declarat de acesta.

CONCLUZIE
Răspunsurile au avansat de la informații comerciale la implementare statică și documentație detaliată. Cea mai utilă îmbunătățire este legarea fiecărei concluzii de cerință, versiune, dovadă, limită și testul care o poate confirma. Cantitatea extrasă, sensul înțeles și funcționarea demonstrată se raportează separat.

COMPLETARE CONFIRMATĂ
FAQ-ul UK Air 2 descrie certificarea Google Play și instalarea locală APK în jurnalul din 28.01.2025. Acest aspect lipsea din comparația inițială. Se verifică regiunea/firmware-ul exemplarului; compatibilitatea cu aplicația ochelarilor rămâne nedemonstrată. Sursa: https://uk.iflytek.com/en/pages/ainote-air2-faq ; extras și limită de acces în dovada-air2-google-play-apk.txt.

CE ESTE APLICAT ACUM
- ${requirements.length} criterii legate de cele ${requests.length} cereri; stări: ${JSON.stringify(indicators.conversation.requirementStates)}. Acestea nu formează un procent unic de completitudine.
- ${claims.claims.length} afirmații decisive cu dovezi/limite; registru selectiv.
- ${evolution.length} intrări de evoluție: omisiune, eroare corectată, dovadă nouă, versiune sau limită încă deschisă.
- ${methods.length} metode: ${JSON.stringify(indicators.methods.states)}. „Aplicat parțial” sau „selectiv” nu înseamnă că toate criteriile viitoare sunt deja îndeplinite.
- Cozi exacte de verificare, manifest de intrări și pagină HTML cu căutare, filtre și legături la catalog.
- ${experiments.length} experimente definite; toate rămân propuse și neexecutate.

INDICATORI RECALCULAȚI
${metrics.map(m=>m.title+': '+m.numerator+'/'+m.denominator+' = '+m.percent+'% ('+m.unit+'). '+m.meaning+' Limită: '+m.limit).join('\n')}
Acestea sunt criterii de extracție cu numitori diferiți. Nu adunăm grupele care se suprapun. Nu împărțim 1107 fișe de funcții la 318284 metode DEX pentru a inventa acoperire semantică.

PRIORITĂȚI CU VALOARE PENTRU DECIZIE
1. Comparație uniformă Air 2/concurenți, cu aplicații, română STT separat de scris, regiune/firmware și cost verificat la decizie. Până atunci nu recalculăm un clasament comercial.
2. Clarificarea traseelor de baterie/versiune/start-stop audio: intrare, transport, parser, callback, efect. Exemple noi pentru auditor, nu doar repetarea cazurilor deja reparate.
3. Tipurile necunoscute și ieșirile neextrase se rezolvă cu sursă; semantica, unitățile și erorile se urmăresc separat de tip.
4. Pe configurația utilizatorului: identitate → captură legitimă a unui schimb read-only → client separat → microfon ochelari și ieșire în căști. Nicio etapă nu este presupusă funcțională.
5. Pentru audio: același corpus și condiții, erori STT, latență p50/p95 și inteligibilitate separate. Pentru firmware: întâi pachetul real cu proveniență, apoi arhitectura și analiza funcțiilor.

METODELE COMPLETE
${methods.map(m=>m.id+' · '+m.title+' ['+m.status+']\n'+m.method+'\nCriteriu: '+m.success+'\nArtefact: '+m.artifact).join('\n\n')}

EXPERIMENTE
${experiments.map(e=>e.id+' · '+e.title+' ['+e.status+']\nNecesită: '+e.requires+'\nAcceptare: '+e.acceptance+'\nLimită: '+e.limit).join('\n\n')}

Pagina de lucru: INDEX.html. Analiza fiecărei cereri: analiza-solicitari.json. Revizie: revizie-independenta.txt. ${deliveryReview?'Reverificarea livrării și închiderea clarificărilor L1/L2: revizie-livrare.txt. ':''}Regenerare: node tools/quality-review-build.cjs. Verificarea raportului nu înlocuiește testele pe dispozitiv.
`;
fs.writeFileSync(path.join(dir,'RAPORT.txt'),report);
// Fingerprint all direct inputs and local evidence; exclude output files to avoid self-reference.
for(const x of [...requests,...requirements,...claims.claims,...evolution]) for(const f of x.evidence||[]) inputFiles.add(f);
for(const f of ['tools/quality-review-build.cjs','tools/quality-review-verify.cjs','tools/audit-state.cjs','imbunatatire-raspunsuri/review.css','imbunatatire-raspunsuri/review.js']) if(fs.existsSync(path.join(root,f)))inputFiles.add(f);
// A small navigation addition to existing hubs. This function is idempotent.
for(const filename of ['INDEX.html','../INDEX.html','../../INDEX.html','catalog-parametri-functii/INDEX.html','audit-calitate/INDEX.html']){
  const absolute=path.join(root,filename),href=path.relative(path.dirname(absolute),path.join(dir,'INDEX.html')).replaceAll('\\','/');
  let s=fs.readFileSync(absolute,'utf8');
  const banner='<p id="analiza-raspunsuri" style="padding:16px;background:#e9f5ef;border-left:4px solid #24694f"><a href="'+href+'"><strong>Analiza tuturor solicitărilor și îmbunătățirea răspunsurilor</strong></a> · '+requests.length+' solicitări · '+methods.length+' metode · dovezi, limite și experimente.</p>';
  if(s.includes('id="analiza-raspunsuri"'))s=s.replace(/<p id="analiza-raspunsuri"[\s\S]*?<\/p>/,banner);
  else if(/<body[^>]*>/i.test(s))s=s.replace(/(<body[^>]*>)/i,'$1'+banner);
  else s=s.replace(/<\/style>/i,'</style>'+banner);
  fs.writeFileSync(absolute,s);
}
const entries=[...inputFiles].sort().map(file=>{const b=fs.readFileSync(path.join(root,file));return {file,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')};});
write('manifest-intrari.json',{generatedAt:now,base:'Directorul APK_Reconstituit_2026-10-30; căi relative la acesta',apkVersion:coverage.apkVersion,apkSha256:coverage.apkSha256,historyThread:history.threadId,files:entries,limit:'Hashuri ale dovezilor locale; fără afirmația că toate sursele web au fost descărcate integral sau sunt încă actuale.'});
console.log(JSON.stringify({requests:requests.length,requirements:requirements.length,methods:methods.length,claims:claims.claims.length,experiments:experiments.length,metrics:metrics.map(x=>({id:x.id,n:x.numerator,d:x.denominator})),queue:groups.map(x=>({id:x.id,n:x.count})),inputs:entries.length}));
