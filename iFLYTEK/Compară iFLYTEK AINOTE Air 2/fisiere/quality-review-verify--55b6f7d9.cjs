const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..'),dir=path.join(root,'imbunatatire-raspunsuri');
const read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const requests=read('analiza-solicitari.json'),requirements=read('cerinte-atomice.json'),methods=read('metode-imbunatatire.json'),experiments=read('plan-experimente.json'),claims=read('registru-afirmatii.json').claims;
const history=read('istoric-conversatie.json'),indicators=read('indicatori.json'),queue=read('coada-verificare.json'),manifest=read('manifest-intrari.json'),sources=read('surse-metodologice.json');
const functions=JSON.parse(fs.readFileSync(path.join(root,'catalog-parametri-functii/functii.json'),'utf8')),params=JSON.parse(fs.readFileSync(path.join(root,'catalog-parametri-functii/parametri.json'),'utf8'));
const auditState=require('./audit-state.cjs')(root),audit=auditState.current;
const exists=p=>fs.existsSync(p),hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const result={date:new Date().toISOString(),scope:'Integritatea raportului, derivarea indicatorilor și comportamentul paginii; fără teste hardware/cloud.',errors:[],checks:{},browser:null};
async function main(){
  assert.equal(requests.length,17); assert.equal(requirements.length,40);assert.equal(methods.length,18);assert.equal(experiments.length,9);
  const reqIds=new Set(requests.map(x=>x.id)),criteriaIds=new Set(requirements.map(x=>x.id)),methodIds=new Set(methods.map(x=>x.id)),expIds=new Set(experiments.map(x=>x.id)),sourceIds=new Set(sources.map(x=>x.id));
  assert.equal(criteriaIds.size,requirements.length);assert.equal(reqIds.size,requests.length);
  for(const q of requests){const t=history.turns.find(x=>x.id===q.turnId);assert(t,q.id);assert(q.finalMessageIds.length);for(const id of q.finalMessageIds)assert(t.messages.some(x=>x.id===id&&x.phase==='final_answer'&&!id.startsWith('call_')));for(const id of q.requirementIds)assert(criteriaIds.has(id));for(const id of q.methods)assert(methodIds.has(id));for(const id of q.experiments)assert(expIds.has(id));}
  const assigned=requests.flatMap(x=>x.requirementIds);assert.equal(assigned.length,requirements.length);assert.equal(new Set(assigned).size,requirements.length);
  for(const r of requirements){assert(reqIds.has(r.requestId));assert(requests.find(x=>x.id===r.requestId).requirementIds.includes(r.id));}
  for(const m of methods){assert(exists(path.join(dir,m.artifact)),m.id+' artifact');for(const id of m.sources)assert(sourceIds.has(id));}
  for(const e of experiments){assert.equal(e.status,'propus_neexecutat');for(const id of e.methods)assert(methodIds.has(id));for(const id of e.sources)assert(sourceIds.has(id));}
  for(const c of claims){assert(c.claim&&c.limit&&c.nextEvidence&&c.appliesTo);assert(c.evidence.length||c.urls.length);for(const id of c.requestIds)assert(reqIds.has(id));}
  for(const x of [...requests,...requirements,...claims,...read('evolutie-concluzii.json')])for(const f of x.evidence||[])assert(exists(path.join(root,f)),'evidence: '+f);
  const fIds=new Set(functions.map(x=>x.id)),pIds=new Set(params.map(x=>x.id));
  const flutter=functions.filter(x=>x.kind==='Flutter MethodChannel'),ble=functions.filter(x=>x.kind==='recepție BLE');
  const expected={K01:[flutter.filter(x=>x.outputParameterIds?.length).length,flutter.length],K02:[flutter.filter(x=>x.resultObservations?.length).length,flutter.length],K03:[params.filter(x=>x.javaType==='necunoscut').length,params.length],K04:[ble.filter(x=>x.outputParameterIds?.length).length,ble.length],K05:[ble.filter(x=>x.schemaPaths?.length).length,ble.length]};
  for(const m of indicators.metrics){assert.deepEqual([m.numerator,m.denominator],expected[m.id]);assert.equal(m.percent,Math.round(m.numerator/m.denominator*10000)/100);assert(m.limit&&m.unit&&m.source);}
  for(const g of queue.groups){assert.equal(g.count,g.items.length);assert.equal(new Set(g.items.map(x=>x.id)).size,g.count);if(g.id!=='channel-candidates')for(const item of g.items)assert((g.id==='unknown-types'?pIds:fIds).has(item.id));}
  const byId=Object.fromEntries(queue.groups.map(g=>[g.id,g]));
  for(const [group,original] of [['unknown-types',params.filter(x=>x.javaType==='necunoscut')],['flutter-output',flutter.filter(x=>!x.outputParameterIds?.length)],['flutter-result',flutter.filter(x=>!x.resultObservations?.length)],['ble-output',ble.filter(x=>!x.outputParameterIds?.length)],['ble-paths',ble.filter(x=>!x.schemaPaths?.length)]])assert.deepEqual(byId[group].items.map(x=>x.id).sort(),original.map(x=>x.id).sort());
  for(const f of manifest.files){assert.equal(hash(path.join(root,f.file)),f.sha256,'stale input: '+f.file);assert.equal(fs.statSync(path.join(root,f.file)).size,f.bytes);}
  const auditStatus=JSON.parse(fs.readFileSync(path.join(root,'audit-calitate/status.json'),'utf8'));assert.equal(auditStatus.matchesCurrentData,auditState.matchesCurrentData);assert.equal(auditStatus.round,audit.round);if(!auditState.matchesCurrentData)assert(indicators.maturity.some(x=>x.stage==='Audit independent al catalogului'&&x.state.includes('istoric')),'stale audit disclosed');
  const html=fs.readFileSync(path.join(dir,'INDEX.html'),'utf8'),embedded=JSON.parse(html.match(/<script id="review-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  assert.deepEqual(embedded.indicators,indicators);assert.deepEqual(embedded.queue,queue);assert.deepEqual(embedded.methods,methods);assert.deepEqual(embedded.experiments,experiments);assert.deepEqual(embedded.claims,claims);assert.equal(embedded.requests.length,requests.length);
  for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){const href=match[1];if(/^(https?:|#)/.test(href))continue;assert(exists(path.resolve(dir,decodeURIComponent(href.split('#')[0]))),'link: '+href);}
  for(const f of ['INDEX.html','../INDEX.html','../../INDEX.html','catalog-parametri-functii/INDEX.html','audit-calitate/INDEX.html']){const text=fs.readFileSync(path.join(root,f),'utf8'),match=text.match(/<p id="analiza-raspunsuri"[^>]*><a href="([^"]+)"/);assert(match,'navigation: '+f);assert.equal(path.resolve(path.dirname(path.join(root,f)),match[1]),path.join(dir,'INDEX.html'));}
  result.checks={requests:requests.length,requirements:requirements.length,methods:methods.length,experiments:experiments.length,claims:claims.length,metrics:indicators.metrics.length,queueGroups:queue.groups.length,inputHashes:manifest.files.length,matchingAuditedDatasets:auditState.checks.filter(x=>x.matches).length,auditRound:audit.round,auditMatchesCurrentData:auditState.matchesCurrentData,localEvidenceLinks:'passed',embeddedData:'passed'};
  const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
  const browser=await chromium.launch({channel:'msedge',headless:true});
  try{const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));const url=require('url').pathToFileURL(path.join(dir,'INDEX.html')).href;
    await page.goto(url);await page.waitForSelector('#requests-list>details');assert.equal(await page.locator('#requests-list>details').count(),17);await page.screenshot({path:path.join(dir,'preview-desktop.png'),fullPage:false});
    await page.fill('#request-search','firmware');assert((await page.locator('#requests-list>details').count())>0);assert((await page.locator('#requests-list>details').count())<17);await page.fill('#request-search','');
    await page.click('[data-tab="methods"]');await page.selectOption('#method-state','done');assert.equal(await page.locator('#methods-list>.card').count(),methods.filter(x=>x.status.startsWith('aplicat')).length);await page.selectOption('#method-state','planned');assert.equal(await page.locator('#methods-list>.card').count(),methods.filter(x=>!x.status.startsWith('aplicat')).length);
    await page.click('[data-tab="queue"]');assert.equal(await page.locator('#queue-list>tr').count(),20);await page.click('#next-page');assert.equal(await page.locator('#queue-page').textContent(),'2 / '+Math.ceil(byId['unknown-types'].count/20));await page.fill('#queue-search',byId['unknown-types'].items[0].id);assert.equal(await page.locator('#queue-list>tr').count(),1);await page.fill('#queue-search','');await page.selectOption('#queue-group','ble-output');assert.equal(await page.locator('#queue-count').textContent(),byId['ble-output'].count+' rezultate în această grupă');
    for(const tab of ['metrics','experiments','claims','sources'])await page.click('[data-tab="'+tab+'"]');
    const renderedHrefs=await page.locator('a[href]').evaluateAll(xs=>xs.map(x=>x.getAttribute('href')));const idsInPage=new Set(await page.locator('[id]').evaluateAll(xs=>xs.map(x=>x.id)));
    for(const href of renderedHrefs){if(/^https?:/.test(href))continue;if(href.startsWith('#')){const target=href.slice(1);assert(idsInPage.has(target)||/^M\d/.test(target),'anchor: '+href);continue;}assert(exists(path.resolve(dir,decodeURIComponent(href.split('#')[0]))),'rendered link: '+href);}
    await page.goto(url+'#S01');await page.waitForSelector('#S01[open]');assert(await page.locator('#panel-requests').isVisible());await page.locator('#S01 .answer summary').click();assert((await page.locator('#S01 .original').textContent()).length>500);
    await page.goto(url+'#E04');await page.waitForSelector('#E04[open]');assert(await page.locator('#panel-experiments').isVisible());
    await page.setViewportSize({width:390,height:844});
    const overflow=[];for(const tab of ['requests','methods','metrics','queue','experiments','claims','sources']){await page.click('[data-tab="'+tab+'"]');const tooWide=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);if(tooWide)overflow.push(tab);}
    await page.goto(url);await page.screenshot({path:path.join(dir,'preview-mobile.png'),fullPage:false});assert.deepEqual(overflow,[]);assert.deepEqual(errors,[]);
    result.browser={desktop:true,mobileWidth:390,mobileOverflow:overflow,javascriptErrors:errors,search:true,methodFilters:true,queuePagination:true,deepLinks:true,originalAnswers:true,localLinks:true};
  }finally{await browser.close();}
  result.passed=true;
}
main().catch(e=>{result.passed=false;result.errors.push(e.stack||String(e));process.exitCode=1;}).finally(()=>{fs.writeFileSync(path.join(dir,'validare.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));});
