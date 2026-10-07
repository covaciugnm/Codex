import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {writeFile,readFile} from 'node:fs/promises';
import path from 'node:path';
import {useCases} from '../public/usecases-data.js';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..'),base=process.env.SITE_TEST_URL||'http://127.0.0.1:4160';
const report={started:new Date().toISOString(),status:'running',checks:[],errors:[]};
const browser=await chromium.launch({headless:true});
const pass=(type,extra={})=>report.checks.push({type,...extra,status:'passed'});
try{
 const context=await browser.newContext({viewport:{width:1440,height:1050},reducedMotion:'reduce'});const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 for(const lang of ['ro','en','de','fr','es','hu','bg']){
  const d=JSON.parse(await readFile(path.join(root,'content/locales',lang+'.json'),'utf8'));
  await page.goto(base+'/?lang='+lang);await page.waitForSelector('#customer-profile');const origin=await page.evaluate(()=>performance.timeOrigin);
  assert.equal(await page.locator('#customer-profile option').count(),7);
  assert.ok((await page.locator('label[for=customer-profile]').textContent()).includes(d['v2.customerLabel']));
  assert.ok((await page.locator('label[for=customer-problem]').textContent()).includes(d['v2.problemLabel']));
  for(const profile of ['architect','designer','builder','maker','property','creator','all']){
   await page.selectOption('#customer-profile',profile);
   const options=await page.locator('#customer-problem option').evaluateAll(es=>es.map(e=>e.value));
   assert.ok(options.length>=6);assert.equal(new Set(options).size,options.length);
   for(const id of options)assert.ok(useCases.some(item=>item.id===id));
   const selected=await page.inputValue('#customer-problem');assert.equal(await page.textContent('#customer-answer h2'),d['usecase.'+selected+'.title']);
   const item=useCases.find(x=>x.id===selected);assert.equal(await page.getAttribute('#customer-answer a','href'),item.module+'?lang='+lang);
   if(profile==='maker')assert.ok(options.every(id=>useCases.find(x=>x.id===id).category==='objects_print'));
   if(profile==='all')assert.equal(options.length,36);
   assert.equal(await page.evaluate(()=>performance.timeOrigin),origin);pass('profile-updates-relevant-problems',{lang,profile,count:options.length});
  }
  for(const item of useCases){
   await page.selectOption('#customer-problem',item.id);
   assert.equal(await page.textContent('#customer-answer h2'),d['usecase.'+item.id+'.title']);
   assert.equal(await page.textContent('#customer-answer p'),d['usecase.'+item.id+'.description']);
   assert.equal(await page.getAttribute('#customer-answer a','href'),item.module+'?lang='+lang);
   assert.equal(await page.getAttribute('#product-demo','data-mode'),item.module==='/measure'?'measure':item.module==='/spaces'?'space':'object');
   assert.equal(await page.evaluate(()=>performance.timeOrigin),origin);pass('problem-updates-result-and-module',{lang,id:item.id});
  }
 }
 await page.selectOption('#customer-profile','all');await page.selectOption('#customer-problem','furniture-fit');await page.locator('#customer-problem').focus();
 await page.evaluate(()=>dispatchEvent(new Event('online')));await page.waitForTimeout(500);
 assert.equal(await page.evaluate(()=>document.activeElement.id),'customer-problem');assert.equal(await page.inputValue('#customer-profile'),'all');assert.equal(await page.inputValue('#customer-problem'),'furniture-fit');pass('live-update-keeps-profile-problem-and-focus');
 await page.selectOption('#language','ro');await page.waitForFunction(()=>document.documentElement.lang==='ro');assert.equal(await page.inputValue('#customer-problem'),'furniture-fit');pass('language-keeps-selection');
 await page.click('#customer-answer a');assert.match(page.url(),/\/measure\?lang=ro/);await page.waitForSelector('#measurement-value');pass('selected-result-opens-correct-workflow');
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:width>800?1050:844});await page.goto(base+'/?lang=ro');await page.waitForSelector('#customer-profile');
  const first=await page.locator('#customer-profile').boundingBox(),second=await page.locator('#customer-problem').boundingBox();assert.ok(second.y>first.y+first.height);
  for(const profile of ['architect','designer','builder','maker','property','creator','all']){await page.selectOption('#customer-profile',profile);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);}
  await page.selectOption('#customer-profile','designer');await page.selectOption('#customer-problem','furniture-fit');await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:path.join(root,'docs/validation/customer-finder-'+width+'.png'),fullPage:true});pass('stacked-selectors-and-responsive-results',{width});
 }
 assert.deepEqual(report.errors,[]);report.status='passed';await context.close();
}catch(error){report.status='failed';report.errors.push(error.stack);process.exitCode=1;}finally{await browser.close();report.finished=new Date().toISOString();await writeFile(path.join(root,'docs/validation/customer-finder-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,errors:report.errors}));}
