const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process');
const {pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..'), cmd=process.argv[2];
const read=p=>fs.readFileSync(path.join(root,p),'utf8').replace(/^\uFEFF/,'');
const json=p=>JSON.parse(read(p));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const save=(p,v)=>fs.writeFileSync(path.join(root,p),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n','utf8');
const files=(d=root)=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(d,e.name)):[path.relative(root,path.join(d,e.name)).replaceAll('\\','/')]);
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const inline=s=>esc(s).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g,'<a href="$2">$1</a>');
if(cmd==='build'){
 const order=['README.md','00_control/ECHIPA_PLAN_SI_RELUARE.md',...files().filter(p=>/^(01_cercetare|02_proiect_tehnic)\/.*\.md$/.test(p)).sort(),...files().filter(p=>/^06_audit\/.*\.md$/.test(p)).sort(),'05_surse/BIBLIOGRAFIE.md'];
 let md='# EVA-3dScan — Proiect tehnic fundamentat\n\niPhone 17 Pro Max · Jetson AGX Thor 128 GB · Unitree H1 v1\n\n2 octombrie 2026. Cercetare, contracte și probe offline. Calificarea hardware rămâne de executat.\n\n';
 for(const p of order)if(fs.existsSync(path.join(root,p)))md+='\n\n'+read(p)+'\n';
 save('07_livrabile/PROIECT_TEHNIC.md',md);
 let code=false,table=false,n=0,html=[],nav=[];
 for(const line of md.split(/\r?\n/)){
  if(line.startsWith('```')){if(table){html.push('</table></div>');table=false;}code=!code;html.push(code?'<pre><code>':'</code></pre>');continue;}
  if(code){html.push(esc(line)+'\n');continue;}
  if(line.startsWith('|')){if(/^\|[\s:|\-]+\|$/.test(line))continue;if(!table){html.push('<div class="tw"><table>');table=true;}html.push('<tr>'+line.split('|').slice(1,-1).map(c=>'<td>'+inline(c.trim())+'</td>').join('')+'</tr>');continue;}
  if(table){html.push('</table></div>');table=false;}
  const h=line.match(/^(#{1,6}) (.+)$/);
  if(h){const id='s'+(++n);html.push(`<h${h[1].length} id="${id}">${inline(h[2])}</h${h[1].length}>`);if(h[1].length===1)nav.push(`<a href="#${id}">${esc(h[2])}</a>`);}
  else if(line.trim())html.push('<p>'+inline(line)+'</p>');
 }
 if(table)html.push('</table></div>');
 save('07_livrabile/PROIECT_TEHNIC.html',`<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EVA-3dScan · Proiect tehnic</title><style>body{margin:0;background:#edf2f5;color:#182d3e;font:16px/1.6 system-ui,Segoe UI,sans-serif}aside{position:fixed;inset:0 auto 0 0;width:270px;box-sizing:border-box;background:#14354a;color:#fff;padding:22px;overflow:auto}aside a{display:block;color:#d9f3f4;text-decoration:none;font-size:12px;padding:6px 0}main{margin-left:270px;padding:40px 5vw;background:white;max-width:1200px}h1{font-size:30px;line-height:1.25;color:#087c82;margin-top:55px}h2{font-size:23px;margin-top:35px}h3{font-size:19px}a{color:#07628c;overflow-wrap:anywhere}code{font-size:.85em;background:#edf3f6;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf3f6;padding:14px}.tw{overflow:auto}table{border-collapse:collapse;width:100%;font-size:12px}td{border:1px solid #ccd9df;padding:8px;vertical-align:top}tr:first-child{font-weight:600;background:#e8f4f3}@media(max-width:900px){aside{position:static;width:auto;max-height:220px}main{margin:0;padding:22px}}@page{size:A4;margin:17mm 14mm}@media print{aside{display:none}main{margin:0;padding:0;max-width:none}body{background:white;font-size:10pt;line-height:1.48}h1{break-before:page;font-size:22pt}h2{font-size:15pt}h3{font-size:12pt}h1,h2,h3{break-after:avoid}table{font-size:8pt}.tw{overflow:visible}tr{break-inside:avoid}pre{font-size:8pt}}</style><aside><h2>EVA-3dScan</h2><p>Proiect tehnic fundamentat</p>${nav.join('')}</aside><main>${html.join('\n')}</main></html>`);
 console.log(JSON.stringify({chapters:order.length,words:md.split(/\s+/).length}));
}
if(cmd==='render'){
 const browser=process.argv[3],profile=process.argv[4];if(!browser||!profile)throw Error('browser and external profile required');
 const source=path.join(root,'07_livrabile/PROIECT_TEHNIC.html'),pdf=path.join(root,'07_livrabile/PROIECT_TEHNIC.pdf');
 const result=cp.spawnSync(browser,['--headless','--disable-gpu','--no-first-run','--no-pdf-header-footer','--user-data-dir='+profile,'--print-to-pdf='+pdf,pathToFileURL(source).href],{encoding:'utf8',windowsHide:true,timeout:90000});
 if(!fs.existsSync(pdf)||fs.statSync(pdf).mtimeMs<fs.statSync(source).mtimeMs)throw Error(result.stderr||'PDF not refreshed');
 const bytes=fs.readFileSync(pdf);console.log(JSON.stringify({pages:(bytes.toString('latin1').match(/\/Type\s*\/Page\b/g)||[]).length,bytes:bytes.length}));
}
if(cmd==='validate'){
 const failures=[],all=files();let count=0;
 for(const p of all.filter(p=>/\.jsonl?$/.test(p))){try{if(p.endsWith('.jsonl'))read(p).split(/\r?\n/).filter(Boolean).forEach(l=>JSON.parse(l));else json(p);count++;}catch(e){failures.push(p+': '+e.message);}}
 for(const p of all.filter(p=>p.endsWith('.md')&&!p.startsWith('07_livrabile/'))){const text=read(p);if(text.includes('\uFFFD'))failures.push('UTF8 '+p);for(const m of text.matchAll(/\]\(([^)]+)\)/g)){if(/^(https?:|#)/.test(m[1]))continue;if(!fs.existsSync(path.resolve(root,path.dirname(p),m[1].split('#')[0])))failures.push('link '+p+' -> '+m[1]);}}
 if(fs.existsSync(path.join(root,'00_control/tasks.json'))){const ts=json('00_control/tasks.json').tasks,ids=new Set(ts.map(t=>t.id));if(ids.size!==ts.length)failures.push('duplicate tasks');const visiting=new Set(),done=new Set();function visit(id){if(visiting.has(id)){failures.push('task cycle '+id);return;}if(done.has(id))return;visiting.add(id);const t=ts.find(t=>t.id===id);for(const d of t.dependencies){if(!ids.has(d))failures.push('missing dependency '+d);else visit(d);}visiting.delete(id);done.add(id);}for(const t of ts){visit(t.id);if(!t.owner||!t.auditor||t.owner===t.auditor||!t.acceptance||!t.next)failures.push('incomplete task '+t.id);if(t.status==='accepted'){if(!t.evidence?.length)failures.push('no evidence '+t.id);for(const p of t.evidence||[])if(!fs.existsSync(path.join(root,p)))failures.push('missing evidence '+p);}}}
 if(fs.existsSync(path.join(root,'06_audit/REGISTRU.json'))){const a=json('06_audit/REGISTRU.json');for(const r of a.reviews){if(r.author===r.auditor)failures.push('self audit '+r.domain);if(!fs.existsSync(path.join(root,r.report)))failures.push('missing audit report '+r.domain);const findings=json(r.findings);if(a.status==='accepted'&&(r.status!=='accepted'||findings.some(f=>f.status!=='closed')))failures.push('open audit '+r.domain);}}
 const report={at:new Date().toISOString(),status:failures.length?'failed':'passed',json_files:count,failures,scope:'Document structure, links, task dependencies and audit closure. Not general JSON Schema, Swift compilation or physical validation.'};save('06_audit/structural_checks.json',report);console.log(JSON.stringify(report));if(failures.length)process.exitCode=1;
}
if(cmd==='manifest'){const excludes=['MANIFEST_SHA256.json','LIVRARE_CONFIRMATA.json'];save('MANIFEST_SHA256.json',{at:new Date().toISOString(),excludes,files:files().filter(p=>!excludes.includes(p)).sort().map(p=>({path:p,bytes:fs.statSync(path.join(root,p)).size,sha256:sha(fs.readFileSync(path.join(root,p)))}))});console.log('manifest saved');}
if(cmd==='verify'){const m=json('MANIFEST_SHA256.json'),mismatch=m.files.filter(f=>!fs.existsSync(path.join(root,f.path))||sha(fs.readFileSync(path.join(root,f.path)))!==f.sha256).map(f=>f.path),known=new Set(m.files.map(f=>f.path)),extra=files().filter(p=>!known.has(p)&&!m.excludes.includes(p));console.log(JSON.stringify({status:mismatch.length||extra.length?'failed':'passed',files:m.files.length,mismatch,extra}));if(mismatch.length||extra.length)process.exitCode=1;}
if(cmd==='event'){const entry={timestamp:new Date().toISOString(),actor:'manager',task:process.argv[3],event:process.argv[4],result:process.argv[5],artifacts:process.argv.slice(6),next:'Consultă STATUS.json și task register'};fs.appendFileSync(path.join(root,'08_jurnale/manager.jsonl'),JSON.stringify(entry)+'\n');console.log(JSON.stringify(entry));}
if(!['build','render','validate','manifest','verify','event'].includes(cmd))throw Error('Use build/render/validate/manifest/verify/event');
