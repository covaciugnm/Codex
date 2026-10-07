import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');
const {chromium}=require('playwright');
const base=process.env.SITE_TEST_URL||'http://127.0.0.1:4160';
const root=path.resolve(import.meta.dirname,'..');
const output=path.join(root,'docs','validation');await mkdir(output,{recursive:true});
const report={started:new Date().toISOString(),base,checks:[],errors:[],browserErrors:[],hardwareAppTests:'not_run'};
const browser=await chromium.launch({headless:true});
const localeKeys=Object.keys(JSON.parse(await readFile(path.join(root,'content/locales/en.json'),'utf8')));
const routes=['/','/objects','/measure','/spaces','/uses','/people','/technology','/documentation','/about'];
const wait=async(page,lang)=>{await page.waitForSelector('#app:not([data-ssr]) main h1');await page.waitForFunction(l=>document.documentElement.lang===l,lang);};
try{
 for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
  const context=await browser.newContext({viewport,reducedMotion:'reduce'});const page=await context.newPage();page.on('pageerror',e=>report.browserErrors.push(e.message));
  for(const lang of ['en','de','fr','es','ro','hu','bg'])for(const route of routes){
   await page.goto(base+route+'?lang='+lang);await wait(page,lang);
   const result=await page.evaluate(keys=>({overflow:document.documentElement.scrollWidth>innerWidth+1,placeholders:/\{\{\w+\}\}/.test(document.body.innerText),missing:keys.filter(k=>document.body.innerText.includes(k)),broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src),heading:document.querySelector('h1').textContent}),localeKeys);
   assert.equal(result.overflow,false,`Overflow ${viewport.width} ${lang} ${route}`);assert.equal(result.placeholders,false);assert.deepEqual(result.missing,[],`Missing key ${lang} ${route}`);assert.deepEqual(result.broken,[]);
   report.checks.push({type:'route-locale-layout',viewport:viewport.width,lang,route,status:'passed'});
  }
  await page.goto(base+'/?lang=ro');await wait(page,'ro');await page.screenshot({path:path.join(output,`home-${viewport.width}.png`),fullPage:true});
  if(viewport.width===390){await page.click('#menu-button');assert.equal(await page.getAttribute('#menu-button','aria-expanded'),'true');await page.locator('#navigation [data-route="/objects"]').click();await page.waitForURL('**/objects?lang=ro');report.checks.push({type:'mobile-navigation',status:'passed'});}
  await context.close();
 }
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});const page=await context.newPage();page.on('pageerror',e=>report.browserErrors.push(e.message));await page.goto(base+'/?lang=ro');await wait(page,'ro');
 const origin=await page.evaluate(()=>performance.timeOrigin);
 for(const lang of ['en','de','fr','es','hu','bg','ro']){await page.selectOption('#language',lang);await wait(page,lang);assert.equal(await page.evaluate(()=>performance.timeOrigin),origin);}
 report.checks.push({type:'seven-languages-no-document-reload',status:'passed'});
 await page.route('**/api/content?lang=de',async r=>{await new Promise(resolve=>setTimeout(resolve,250));try{await r.continue();}catch{}});
 await page.selectOption('#language','de');await page.evaluate(()=>dispatchEvent(new Event('online')));await wait(page,'de');report.checks.push({type:'language-refresh-race',status:'passed'});
 await page.goto(base+'/?lang=ro');await wait(page,'ro');await page.evaluate(()=>history.pushState({},'','/objects?lang=ro'));await page.selectOption('#language','de');await page.goBack();await wait(page,'ro');await page.waitForTimeout(400);assert.equal(await page.evaluate(()=>document.documentElement.lang),'ro');report.checks.push({type:'language-back-race',status:'passed'});
 await page.goto(base+'/measure?lang=ro');await wait(page,'ro');await page.selectOption('#unit','mm');assert.match(await page.textContent('#measurement-value'),/1.?240 mm/);await page.selectOption('#unit','cm');assert.equal(await page.textContent('#measurement-value'),'124 cm');report.checks.push({type:'synthetic-unit-conversion',status:'passed'});await page.screenshot({path:path.join(output,'measure-desktop.png'),fullPage:true});
 await page.goto(base+'/technology?lang=en');await wait(page,'en');await page.click('[data-filter="cad"]');assert.equal(await page.locator('.format-card').count(),3);await page.click('[data-filter="print"]');assert.equal(await page.locator('.format-card').count(),2);report.checks.push({type:'format-filters',status:'passed'});
 for(const resource of ['/downloads/EVA-3D-Scan-dossier-ro.pdf','/downloads/cube-100mm.stl','/downloads/reference-cloud.ply','/downloads/room-4x3m.dxf','/assets/logo.svg']){const response=await page.request.get(base+resource);assert.equal(response.status(),200);assert.ok((await response.body()).length>100);report.checks.push({type:'download',resource,status:'passed'});}
 for(const privatePath of ['/docs/BACKEND.md','/.env','/server/config.mjs','/content/locales/en.json','/../.env','/api/admin']){const response=await page.request.get(base+privatePath);assert.equal(response.status(),404);report.checks.push({type:'private-route-blocked',resource:privatePath,status:'passed'});}
 const alias=await page.request.get(base+'/api/content?lang=sp');assert.equal((await alias.json()).locale,'es');report.checks.push({type:'spanish-alias',status:'passed'});
 if(process.env.TEST_LIVE_EDIT==='1'){
  await page.goto(base+'/?lang=ro');await wait(page,'ro');const original=(await(await page.request.get(base+'/api/content?lang=ro')).json()).messages['hero.title'];const marker=original+' [QA]';const sql=v=>`UPDATE content_messages SET value='${v.replaceAll("'","''")}' WHERE locale='ro' AND key='hero.title';`;const update=v=>execFileSync('docker',['compose','exec','-T','db','psql','-U','eva_site','-d','eva_site','-v','ON_ERROR_STOP=1','-c',sql(v)],{cwd:root,stdio:'pipe'});const before=await page.evaluate(()=>performance.timeOrigin);
  try{update(marker);await page.waitForFunction(v=>document.querySelector('h1')?.textContent===v,marker);assert.equal(await page.evaluate(()=>performance.timeOrigin),before);report.checks.push({type:'postgres-notify-live-update-without-reload',status:'passed'});}finally{update(original);await page.waitForFunction(v=>document.querySelector('h1')?.textContent===v,original);}
 }
 await context.close();assert.deepEqual(report.browserErrors,[]);report.status='passed';
}catch(e){report.status='failed';report.errors.push(e.stack);process.exitCode=1;}finally{await browser.close();report.finished=new Date().toISOString();await writeFile(path.join(output,'browser-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,errors:report.errors,browserErrors:report.browserErrors}));}
