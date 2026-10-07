const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(root,p),'utf8').replace(/^\uFEFF/,'');
const write = (p,s) => { fs.mkdirSync(path.dirname(path.join(root,p)),{recursive:true}); fs.writeFileSync(path.join(root,p),s,'utf8'); };
const json = p => JSON.parse(read(p));
const stamp = () => new Date().toISOString();
const files = (dir=root) => fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=> e.isDirectory()?files(path.join(dir,e.name)):[path.relative(root,path.join(dir,e.name)).replaceAll('\\','/')]);
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
const cmd = process.argv[2];
if(cmd==='init') {
 const roles = [
 ['DOC-01','Inventariere și structură','manager',['00_management/INVENTAR_INITIAL.md'],'Inventar existent verificat; structură de directoare creată'],
 ['DOC-02','Cercetare piață și UX','research_ux',['01_cercetare/piata_feedback_ux.md','07_surse/ux_sources.json','00_management/ux_events.jsonl'],'6 competitori; feedback documentat; 3 fluxuri; criterii UX'],
 ['DOC-03','Arhitectură Apple','apple_architecture',['03_arhitectura/01_arhitectura_apple.md','07_surse/apple_sources.json','00_management/apple_events.jsonl'],'Capabilități și platforme diferențiate; cerințe și teste propuse'],
 ['DOC-04','CAD imprimare și metrologie','cad_printing',[],'Formate clasificate; licențe; metrologie și imprimare; fixtures'],
 ['DOC-05','Integrare specificație și cercetare','manager',['02_specificatie/01_VIZIUNE_SI_SPECIFICATIE.md','05_validare/METODOLOGIE_CERCETARE_SI_TESTARE.md'],'Toate cele 3 module; cerințe măsurabile; statut experimental corect'],
 ['DOC-06','Prompt echipă și reluare','manager',['06_prompturi/PROMPT_MASTER.md','06_prompturi/PROMPT_RELUARE.md','00_management/PLAN_ECHIPA_SI_RELUARE.md'],'Roluri; obiective; loguri; checkpoint; audit; reluare'],
 ['DOC-07','Surse exemple și document unificat','manager',[],'Fișe locale; index; document lizibil; exemple etichetate'],
 ['DOC-08','Audit independent și remedieri','auditor_final',[],'Zero P0/P1 deschise pentru documentația acceptată'],
 ['DOC-09','Verificare și livrare','manager',[],'JSON valide; linkuri interne; SHA256; copie în proiect comparată']
 ];
 const tasks = roles.map((r,i)=>({id:r[0],title:r[1],owner:r[2],status:i<6?'in_review':'in_progress',inputs:['cererea_utilizatorului'],dependencies:i===0?[]:i<4?['DOC-01']:i===7?['DOC-02','DOC-03','DOC-04','DOC-05','DOC-06']:['DOC-01'],outputs:r[3],acceptance:r[4],audit:null,next_action:'Verificare documentară și integrare în livrare'}));
 tasks.push({id:'APP-P03',title:'Probe pe Mac Xcode și iPhone real',owner:'apple_architecture',status:'planned',inputs:['dosar_acceptat'],dependencies:['DOC-09'],outputs:[],acceptance:'5 probe executate pe dispozitive cu dovezi',audit:null,next_action:'Inventariază Mac/Xcode/iPhone disponibile; confirmă matrice dispozitive și toleranțe'});
 write('00_management/tasks.json',JSON.stringify({schema_version:'1.0',scope:'documentare curentă și primul pas de implementare',tasks},null,2)+'\n');
 write('00_management/STATUS.json',JSON.stringify({schema_version:'1.0',updated_at:stamp(),stage:'documentation_in_audit',implementation_status:'not_started',hardware_tests:'not_run',current_task:'DOC-08',next_action:'Auditează conținutul, remediază, regenerează livrabilele, verifică și copiază în proiect',checkpoint_policy:'Ultimul pas confirmat, fără garanție pentru munca nesalvată',network_target:'\\\\192.168.100.151\\site-uri\\3dscan.eva-org.com\\documentatie'},null,2)+'\n');
 const events=[['DOC-01','inventory','Directorul proiectului a fost gol; accesul UNC a funcționat după eroarea unității mapate'],['DOC-02','delegation','Agent cercetare UX pornit cu cerințe și folder separat'],['DOC-03','delegation','Agent Apple pornit cu cerințe și folder separat'],['DOC-04','delegation','Agent CAD pornit cu cerințe și folder separat'],['DOC-05','result','Specificația și metodologia au fost redactate; pragurile sunt propuneri'],['DOC-06','result','Prompturile și protocolul de reluare au fost redactate'],['DOC-08','delegation','Auditor independent pornit pentru conținut și coerență']];
 write('00_management/manager_events.jsonl',events.map((e,i)=>JSON.stringify({event_id:`MGR-${String(i+1).padStart(3,'0')}`,date:'2026-10-02',recorded_at:stamp(),timing:'reconstructed_from_session_history',actor:'manager',task_id:e[0],type:e[1],summary:e[2],evidence:tasks.find(t=>t.id===e[0])?.outputs||[],next_action:'Audit și integrare'})).join('\n')+'\n');
}
if(cmd==='event') {
 const entry={event_id:crypto.randomUUID(),timestamp:stamp(),actor:'manager',task_id:process.argv[3],type:process.argv[4],summary:process.argv[5],evidence:process.argv.slice(6),next_action:'Consultă STATUS.json'};
 fs.appendFileSync(path.join(root,'00_management/manager_events.jsonl'),JSON.stringify(entry)+'\n');
}
if(cmd==='build') {
 const order=['02_specificatie','01_cercetare','03_arhitectura','04_cad_printare','05_validare','00_management','06_prompturi','08_audit'];
 const chapters=files().filter(p=>p.endsWith('.md')&&!p.startsWith('09_livrabile/')&&!p.startsWith('07_surse/')&&p!=='README.md').sort((a,b)=>order.indexOf(a.split('/')[0])-order.indexOf(b.split('/')[0])||a.localeCompare(b));
 let merged='# Dosarul de cercetare și proiectare EVA 3D Scan\n\nVersiunea 1.0 · 2 octombrie 2026 · Documentație de proiectare, fără implementare sau rezultate experimentale.\n\n';
 merged+='## Rezumat\n\nProiectul propune trei componente: obiecte cu dimensiuni, măsurare temporară cu cote pe imagine și camere salvate care se pot uni în apartamente și case. Dosarul include 106 cerințe, arhitectura Apple, UX fundamentat în feedback, conversii CAD, pregătirea pentru imprimare 3D și un protocol de testare. Implementarea și măsurătorile experimentale rămân de realizat.\n\n';
 merged+='## Cuprins\n\n'+chapters.map((p,i)=>(i+1)+'. '+(read(p).match(/^#\s+(.+)/m)?.[1]||p)).join('\n')+'\n\n';
 for(const p of chapters) {const body=read(p).replace(/\]\(([^)]+)\)/g,(match,target)=>{if(/^(https?:|#|mailto:)/.test(target))return match;return ']('+path.posix.relative('09_livrabile',path.posix.normalize(path.posix.join(path.posix.dirname(p),target)))+')';});merged+='\n\n---\n\nSursa capitolului: `'+p+'`\n\n'+body+'\n';}
 const registries=files().filter(p=>p.startsWith('07_surse/')&&p.endsWith('_sources.json'));
 let sources=[];
 for(const p of registries){const j=json(p);sources.push(...(Array.isArray(j)?j:j.sources||[]));}
 write('07_surse/registru_unificat.json',JSON.stringify({generated_at:stamp(),records:sources.length,unique_urls:new Set(sources.map(s=>s.url)).size,sources},null,2)+'\n');
 const bibliography='# Bibliografia și fișele locale\n\n'+sources.map(s=>`## ${s.id} ${s.title}\n\n[Deschide sursa](${s.url})\n\n${s.summary||s.original_summary_ro||s.evidence_note||''}\n\nStare: ${s.verification||s.status||s.read_status||'vezi registrul'}. Acces: ${s.accessed_at||s.access_date||'2026-10-02'}.\n`).join('\n');
 write('07_surse/BIBLIOGRAFIE.md',bibliography);
 merged+='\n\n---\n\n'+bibliography;
 write('09_livrabile/DOSAR_COMPLET.md',merged);
 const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
 const inline=s=>esc(s).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2">$1</a>');
 let html='',table=false,code=false,nav=[],n=0;
 for(const l of merged.split(/\r?\n/)){
  if(l.startsWith('```')){if(table){html+='</tbody></table>';table=false;} html+=code?'</code></pre>':'<pre><code>';code=!code;continue;}
  if(code){html+=esc(l)+'\n';continue;}
  if(l.startsWith('|')){if(/^\|[\s:|\-]+$/.test(l))continue;if(!table){html+='<table><tbody>';table=true;}html+='<tr>'+l.split('|').slice(1,-1).map(c=>'<td>'+inline(c.trim())+'</td>').join('')+'</tr>';continue;}
  if(table){html+='</tbody></table>';table=false;}
  const h=l.match(/^(#{1,6})\s+(.+)/);if(h){const id='h'+(++n);html+=`<h${h[1].length} id="${id}">${inline(h[2])}</h${h[1].length}>`;if(h[1].length===1)nav.push(`<a href="#${id}">${inline(h[2])}</a>`);continue;}
  if(l==='---'){html+='<hr>';continue;}if(!l.trim())continue;
  html+='<p'+(/^[-*] |^\d+\. /.test(l)?' class="list"':'')+'>'+inline(l)+'</p>';
 }
 if(table)html+='</tbody></table>';if(code)html+='</code></pre>';
 write('09_livrabile/DOSAR_COMPLET.html',`<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>EVA 3D Scan · Dosar de proiectare</title><style>body{margin:0;color:#172c3e;background:#f2f5f7;font:16px/1.65 system-ui,Segoe UI,sans-serif}aside{position:fixed;inset:0 auto 0 0;width:260px;padding:24px;overflow:auto;background:#15364a;color:white}aside a{display:block;color:#d9eefa;text-decoration:none;font-size:13px;padding:7px 0}main{margin:24px 32px 80px 340px;max-width:1100px;background:white;padding:44px;border-radius:12px}h1{font-size:30px;line-height:1.25;margin-top:55px;color:#0d6274}h2{font-size:23px;margin-top:36px}h3{font-size:19px}table{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow:auto;margin:20px 0}td{border:1px solid #d3e0e6;padding:9px;vertical-align:top;min-width:70px}tr:first-child{background:#e4f0f3;font-weight:600}code{font-size:13px;background:#edf3f5;overflow-wrap:anywhere}pre{overflow:auto;background:#edf3f5;padding:16px}.list{margin-left:16px}a{color:#086b87;overflow-wrap:anywhere}hr{border:0;border-top:2px solid #c8dce5;margin:50px 0}@media(max-width:950px){aside{position:static;width:auto}main{margin:12px;padding:20px}}@media print{aside{display:none}main{margin:0;padding:0;max-width:none}body{background:white;font-size:10pt}h1{break-before:page}table{display:table;font-size:8pt}a{color:inherit}pre{white-space:pre-wrap}tr{break-inside:avoid}}</style><aside><h2>EVA 3D Scan</h2><p>Cercetare și proiectare<br>2 octombrie 2026</p>${nav.join('')}</aside><main>${html}</main></html>`);
 console.log(JSON.stringify({chapters:chapters.length,sources:sources.length,unique_urls:new Set(sources.map(s=>s.url)).size,words:merged.split(/\s+/).length}));
}
if(cmd==='validate') {
 const checks=[], fail=[];const all=files();
 for(const p of all.filter(p=>/\.jsonl?$/.test(p))){try{if(p.endsWith('.jsonl'))read(p).split(/\r?\n/).filter(Boolean).forEach(l=>JSON.parse(l));else json(p);checks.push('JSON '+p);}catch(e){fail.push(p+': '+e.message);}}
 for(const p of all.filter(p=>p.endsWith('.md')&&!p.startsWith('09_livrabile/'))){const t=read(p);if(t.includes('\uFFFD'))fail.push('Replacement character '+p);for(const m of t.matchAll(/\]\(([^)]+)\)/g)){if(/^(https?:|#|mailto:)/.test(m[1]))continue;const target=m[1].split('#')[0];if(target&&!fs.existsSync(path.resolve(root,path.dirname(p),target)))fail.push('Link missing '+p+' -> '+target);}}
 const tasks=json('00_management/tasks.json').tasks;const ids=new Set(tasks.map(t=>t.id));for(const t of tasks){for(const d of t.dependencies||[])if(!ids.has(d))fail.push('Missing dependency '+d);for(const o of t.outputs||[])if(!fs.existsSync(path.join(root,o)))fail.push('Missing output '+o);}
 const report={generated_at:stamp(),status:fail.length?'failed':'passed',scope:'JSON JSONL UTF8 linkuri relative dependențe și fișiere; nu verifică semantică hardware sau disponibilitate web viitoare',file_count:all.length,checks:checks.length,failures:fail};write('08_audit/VERIFICARE_AUTOMATA.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));if(fail.length)process.exitCode=1;
}
if(cmd==='manifest') {
 const items=files().filter(p=>p!=='MANIFEST_SHA256.json'&&p!=='LIVRARE_CONFIRMATA.json').sort().map(p=>({path:p,bytes:fs.statSync(path.join(root,p)).size,sha256:hash(p)}));write('MANIFEST_SHA256.json',JSON.stringify({generated_at:stamp(),excludes:['MANIFEST_SHA256.json','LIVRARE_CONFIRMATA.json'],files:items},null,2)+'\n');console.log('Manifest: '+items.length+' fișiere');
}
if(cmd==='verify') {
 const m=json('MANIFEST_SHA256.json');const bad=[];for(const f of m.files){if(!fs.existsSync(path.join(root,f.path))||hash(f.path)!==f.sha256)bad.push(f.path);}const tracked=new Set(m.files.map(x=>x.path));const extra=files().filter(p=>!tracked.has(p)&&!m.excludes.includes(p));console.log(JSON.stringify({status:bad.length||extra.length?'failed':'passed',checked:m.files.length,mismatches:bad,untracked:extra}));if(bad.length||extra.length)process.exitCode=1;
}
