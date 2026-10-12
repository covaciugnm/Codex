const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
(async()=>{const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});const p=await b.newPage({viewport:{width:1440,height:1000}});let errors=[];p.on('pageerror',e=>{errors.push(e.message);console.log('PAGEERROR',e.message)});
await p.goto('http://127.0.0.1:8765/');await p.screenshot({path:'portal/preview-home.png',fullPage:true});assert.equal(await p.locator('.portal-card').count(),3);
for(const section of ['executori','insolventa']){
 await p.goto('http://127.0.0.1:8765/'+section+'/');assert.equal(await p.locator('.listing').count(),24);await p.locator('#next').click();assert.match(await p.locator('#pageinfo').textContent(),/^2/);
 const auto=section==='executori'?'Auto, moto și ambarcațiuni':'Auto';await p.selectOption('#category',auto);assert(await p.locator('#autoFilters').isVisible());assert(!(await p.locator('#propertyFilters').isVisible()));
 await p.fill('#yearMin','2015');await p.locator('#yearMin').dispatchEvent('change');await p.selectOption('#currency','RON');await p.fill('#priceMax','50000');await p.locator('#priceMax').dispatchEvent('change');
 const ids=await p.locator('[data-id]').evaluateAll(a=>a.map(x=>x.dataset.id));assert(ids.length>0);assert(await p.evaluate(ids=>ids.every(id=>{let x=LISTINGS.find(x=>x.id===id);return x.year>=2015&&x.currency==='RON'&&x.price<=50000}),ids));
 await p.locator('[data-id]').first().click();await p.locator('dialog').waitFor({state:'visible'});assert((await p.locator('dialog .external-links a').first().getAttribute('href')).startsWith('https://'));await p.keyboard.press('Escape');
 await p.selectOption('#category','Imobiliare');assert(await p.locator('#propertyFilters').isVisible());assert.equal(await p.locator('#yearMin').inputValue(),'');await p.locator('#reset').click();
 await p.fill('#query','zzzznotfound987');assert.equal(await p.locator('.listing').count(),0);assert(await p.locator('.empty').isVisible());await p.locator('#reset').click();
 await p.selectOption('#sort','low');assert.match(await p.locator('#filterMessage').textContent(),/Alege RON/);await p.selectOption('#currency','EUR');const prices=await p.locator('[data-id]').evaluateAll(a=>a.map(el=>LISTINGS.find(x=>x.id===el.dataset.id).price));assert(prices.every((v,i)=>!i||v>=prices[i-1]));
 await p.locator('#reset').click();await p.screenshot({path:'portal/preview-'+section+'.png',fullPage:false});await p.setViewportSize({width:390,height:844});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:'portal/preview-'+section+'-mobile.png',fullPage:false});await p.setViewportSize({width:1440,height:1000});
 await p.goto('file:///D:/ANABI%20-%20Licitatii/'+section+'/index.html');assert.equal(await p.locator('.listing').count(),24);
}
assert.deepEqual(errors,[]);await b.close();console.log('PASS: portal links, catalogs, categories, dependent filters, numeric ranges, currency sorting, pagination, details, empty states, responsive and local file access.');})().catch(e=>{console.error(e);process.exit(1)});


