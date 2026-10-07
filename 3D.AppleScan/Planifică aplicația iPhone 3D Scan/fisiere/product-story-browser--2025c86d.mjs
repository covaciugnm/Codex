import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {writeFile,readFile} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');
const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..'),base=process.env.SITE_TEST_URL||'http://127.0.0.1:4160';
const report={started:new Date().toISOString(),checks:[],errors:[],csp:[],status:'running',scope:'Website interactions; no human interviews or iPhone accuracy tests'};
const browser=await chromium.launch({headless:true});
const passed=(type,extra={})=>report.checks.push({type,...extra,status:'passed'});
try{
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 await page.addInitScript(()=>document.addEventListener('securitypolicyviolation',e=>console.error('CSP_VIOLATION '+e.violatedDirective)));
 page.on('console',m=>{if(m.text().startsWith('CSP_VIOLATION'))report.csp.push(m.text());});
 for(const lang of ['ro','en','de','fr','es','hu','bg']){
  const dictionary=JSON.parse(await readFile(path.join(root,'content/locales',lang+'.json'),'utf8'));
  await page.goto(base+'/?lang='+lang);await page.waitForSelector('.product-pitch h1');
  assert.equal(await page.textContent('h1'),dictionary['hero.title']);
  const origin=await page.evaluate(()=>performance.timeOrigin);
  for(const mode of ['object','measure','space']){
   await page.click('[data-demo="'+mode+'"]');
   assert.equal(await page.getAttribute('#product-demo','data-mode'),mode);
   assert.equal(await page.locator('[data-demo][aria-pressed=true]').count(),1);
   assert.ok((await page.textContent('#demo-outcomes')).includes(dictionary['v2.'+mode+'Result']));
   assert.ok((await page.textContent('.phone-viewport')).includes(mode==='object'?'100 mm':mode==='measure'?'4.00 m':'8.00 m'));
   assert.equal(await page.evaluate(()=>performance.timeOrigin),origin);
   passed('mode-updates-visual-and-outcome',{lang,mode});
  }
  for(const role of ['architect','designer','builder','maker','property','creator']){
   await page.click('[data-profession="'+role+'"]');
   assert.equal(await page.textContent('.role-copy h3'),dictionary['v2.'+role+'Title']);
   assert.equal(await page.locator('.role-copy li').count(),3);
   assert.equal(await page.locator('.role-proof svg').count(),1);
   assert.equal(await page.locator('[data-profession][aria-pressed=true]').count(),1);
   assert.ok((await page.textContent('.sample-disclosure')).length>35);
   assert.equal(await page.evaluate(()=>performance.timeOrigin),origin);
   passed('role-updates-needs-steps-result',{lang,role});
  }
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  const text=await page.textContent('main');assert.doesNotMatch(text,/v2\.[a-zA-Z]|\{\{\w+\}\}/);
 }
 await page.goto(base+'/?lang=ro');await page.waitForSelector('.product-pitch');
 await page.locator('[data-demo="measure"]').focus();await page.keyboard.press('Enter');
 await page.evaluate(()=>dispatchEvent(new Event('online')));await page.waitForTimeout(500);
 assert.equal(await page.evaluate(()=>document.activeElement.dataset.demo),'measure');
 assert.equal(await page.getAttribute('#product-demo','data-mode'),'measure');
 await page.click('[data-profession="designer"]');await page.evaluate(()=>dispatchEvent(new Event('online')));await page.waitForTimeout(500);
 assert.equal(await page.evaluate(()=>document.activeElement.dataset.profession),'designer');
 passed('keyboard-and-refresh-preserve-selection-focus');
 const origin=await page.evaluate(()=>performance.timeOrigin);await page.selectOption('#language','de');await page.waitForFunction(()=>document.documentElement.lang==='de');
 assert.equal(await page.getAttribute('[data-profession="designer"]','aria-pressed'),'true');
 assert.equal(await page.getAttribute('#product-demo','data-mode'),'space');assert.equal(await page.evaluate(()=>performance.timeOrigin),origin);
 passed('locale-change-keeps-demo-and-role-without-reload');
 await page.locator('.questions-list summary').first().click();assert.equal(await page.locator('.questions-list details').first().getAttribute('open'),'');
 await page.evaluate(()=>dispatchEvent(new Event('online')));await page.waitForTimeout(500);
 assert.equal(await page.locator('.questions-list details').first().getAttribute('open'),'');assert.equal(await page.evaluate(()=>document.activeElement.dataset.faq),'1');
 assert.ok((await page.locator('.questions-list details').first().textContent()).length>100);passed('faq-opens-and-survives-live-refresh');
 const download=await page.request.get(base+'/downloads/room-4x3m.dxf');assert.equal(download.status(),200);assert.match(await download.text(),/SECTION/);passed('real-synthetic-dxf-download');
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:width>800?1050:844});await page.goto(base+'/?lang=ro');await page.waitForSelector('.product-pitch');
  for(const mode of ['object','measure','space']){await page.click('[data-demo="'+mode+'"]');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);}
  for(const role of ['architect','designer','builder']){await page.click('[data-profession="'+role+'"]');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);}
  await page.click('[data-demo="object"]');await page.click('[data-profession="designer"]');await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:path.join(root,'docs/validation/product-v2-'+width+'.png'),fullPage:true});
  passed('responsive-all-modes-roles',{width});
 }
 await page.setViewportSize({width:1440,height:1050});await page.goto(base+'/?lang=ro');await page.waitForSelector('.product-pitch');
 await page.locator('.product-stage').screenshot({path:path.join(root,'docs/validation/product-v2-stage.png')});
 await page.click('[data-profession="designer"]');await page.locator('.professional-section').screenshot({path:path.join(root,'docs/validation/product-v2-designer.png')});
 await page.click('[data-profession="builder"]');await page.locator('.professional-section').screenshot({path:path.join(root,'docs/validation/product-v2-builder.png')});
 assert.equal(await page.locator('.phone-scanline').evaluate(e=>getComputedStyle(e).display),'none');passed('reduced-motion-respected');
 const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(base+'/?lang=ro');
 assert.match(await staticPage.textContent('main'),/referință cotată a spațiului existent/);assert.match(await staticPage.textContent('main'),/fără salvare automată/);passed('server-rendered-product-content-without-javascript');await nojs.close();
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.csp,[]);report.status='passed';await context.close();
}catch(error){report.status='failed';report.errors.push(error.stack);process.exitCode=1;}finally{await browser.close();report.finished=new Date().toISOString();await writeFile(path.join(root,'docs/validation/product-v2-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,errors:report.errors,csp:report.csp}));}
