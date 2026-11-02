const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const path=require('path');
const assert=require('assert/strict');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1100}});
 const page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const base='https://wordpress.alba-vision.ro';
 const response=await page.goto(base+'/',{waitUntil:'networkidle',timeout:60000});
 assert.equal(response.status(),200);
 await page.waitForFunction(()=>document.querySelectorAll('.domain-card').length>100);
 const jsonResponse=await context.request.get(base+'/_domain-status.json');
 assert.match(jsonResponse.headers()['cache-control'],/no-store/);
 const data=await jsonResponse.json();
 const list=page.locator('.domain-card');
 assert.equal(await list.count(),data.domains.length);
 const names=await list.evaluateAll(nodes=>nodes.map(n=>n.dataset.domain));
 const sorted=[...names].sort(new Intl.Collator('ro',{sensitivity:'base',numeric:true}).compare);
 assert.deepEqual(names,sorted);
 for(const name of ['cesiro.ro','cesiro.com','model.bonna.ro','alo-drone.ro','red.red-robot.ro','wordpress.alba-vision.ro','task.eva-org.com'])assert(names.includes(name));
 for(const [category,count] of [['mirror',9],['spree_products',4],['local_products',14],['not_cloned_ro',2],['not_cloned_com',8]]){
   await page.selectOption('#category-filter',category);assert.equal(await list.count(),count);
 }
 await page.click('#reset-filters');
 for(const [filter,field] of [['#docker-filter','docker'],['#response-filter','http']]){
   for(const value of ['yes','no']){
     await page.selectOption(filter,value);
     const expected=data.domains.filter(r=>r[field][field==='docker'?'exists':'responds']===(value==='yes')).length;
     assert.equal(await list.count(),expected);
   }
   await page.selectOption(filter,'all');
 }
 await page.selectOption('#ip-filter','91.188.227.120');
 assert((await list.count())>=10);
 await page.click('#reset-filters');
 await page.selectOption('#account-filter','cesiro.ro');assert.equal(await list.count(),15);
 await page.click('#reset-filters');
 await page.fill('#search','cesiro.com');
 let card=page.locator('.domain-card[data-domain="cesiro.com"]');
 await card.locator('summary').first().click();
 assert(await card.getAttribute('open')!==null);
 const before=await card.textContent();assert(before.includes('5.286'));assert(before.includes('cesiro1-admin-1'));
 await page.click('#refresh');await page.waitForFunction(()=>!document.querySelector('#refresh').disabled);
 card=page.locator('.domain-card[data-domain="cesiro.com"]');
 assert(await card.getAttribute('open')!==null);assert.equal(await page.inputValue('#search'),'cesiro.com');
 await page.click('#reset-filters');
 await page.screenshot({path:path.join(__dirname,'live-desktop.png'),fullPage:false});
 await page.setViewportSize({width:393,height:852});
 await page.fill('#search','innovationecosystem.red-robot.ro');
 await list.first().locator('summary').first().click();
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
 await page.screenshot({path:path.join(__dirname,'live-mobile.png'),fullPage:true});
 assert.equal(errors.length,0,errors.join('\n'));
 const slugs='bonna calphalon cesiro old-cesiro fisher-price ghirardelli go-pro leapfrog melissa-doug ninja-kitchen opticosmetics set-farfurii tarte-cosmetics'.split(' ');
 const storefronts=[];
 for(let i=0;i<slugs.length;i+=4){
   await Promise.all(slugs.slice(i,i+4).map(async s=>{const r=await context.request.get(base+'/'+s+'/',{timeout:30000});storefronts.push({slug:s,status:r.status()});assert.equal(r.status(),200,s);}));
 }
 const report={tested_at:new Date().toISOString(),url:base,domains:data.domains.length,generated_at:data.generated_at,ui_errors:errors,storefronts,result:'PASS'};
 fs.writeFileSync(path.join(__dirname,'live-report.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
