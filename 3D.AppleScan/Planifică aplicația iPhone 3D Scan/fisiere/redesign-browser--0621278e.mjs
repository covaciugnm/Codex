import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {writeFile} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..'),base='http://127.0.0.1:4160';
const report={started:new Date().toISOString(),checks:[],errors:[]};const browser=await chromium.launch({headless:true});
try{
 const context=await browser.newContext({viewport:{width:1440,height:1050},reducedMotion:'reduce'});const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 for(const lang of ['ro','en','de','fr','es','hu','bg']){
  await page.goto(base+'/?lang='+lang);await page.waitForSelector('.clear-module');assert.equal(await page.locator('.clear-module').count(),3);assert.match(await page.textContent('h1'),/iPhone/);
  const time=await page.evaluate(()=>performance.timeOrigin);
  for(let i=0;i<5;i++){await page.click(`[data-slide="${i}"]`);await page.waitForFunction(()=>{const i=document.querySelector('#campaign-frame img');return i?.complete&&i.naturalWidth>0;});assert.equal(await page.getAttribute(`[data-slide="${i}"]`,'aria-pressed'),'true');assert.equal(await page.evaluate(()=>performance.timeOrigin),time);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);report.checks.push({type:'campaign-slide',lang,slide:i+1,status:'passed'});}
 }
 await page.goto(base+'/?lang=ro');await page.waitForSelector('.clear-module');await page.screenshot({path:path.join(root,'docs/validation/redesign-desktop.png'),fullPage:true});
 await page.click('[data-slide="1"]');await page.screenshot({path:path.join(root,'docs/validation/redesign-face.png'),fullPage:false});assert.equal(await page.locator('.speech-bubble').count(),1);
 await page.locator('#carousel-next').focus();await page.evaluate(()=>dispatchEvent(new Event('online')));await page.waitForTimeout(350);assert.equal(await page.evaluate(()=>document.activeElement.id),'carousel-next');assert.equal(await page.textContent('#carousel-toggle'),'▶');report.checks.push({type:'refresh-preserves-focused-control-and-pause',status:'passed'});
 await page.mouse.move(0,0);assert.deepEqual(report.errors,[]);
 await page.setViewportSize({width:390,height:844});await page.goto(base+'/?lang=ro');await page.waitForSelector('.clear-module');await page.screenshot({path:path.join(root,'docs/validation/redesign-mobile.png'),fullPage:true});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);report.checks.push({type:'mobile-layout',status:'passed'});
 for(const route of ['/api/auth/me','/api/projects'])assert.equal((await page.request.get(base+route)).status(),401);report.checks.push({type:'existing-auth-and-project-routes-preserved',status:'passed'});
 assert.equal((await page.request.get(base+'/assets/eva-app-icon-1024.png')).status(),200);
 const svg=await page.request.get(base+'/assets/eva-mark-animated.svg');assert.match(svg.headers()['content-security-policy'],/script-src 'none'/);const html=await page.request.get(base);assert.match(html.headers()['content-security-policy'],/style-src 'self'/);assert.doesNotMatch(html.headers()['content-security-policy'],/unsafe-inline/);report.checks.push({type:'svg-isolated-style-policy-and-app-icon',status:'passed'});
 await context.close();
 const motion=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'no-preference'});const mp=await motion.newPage();mp.on('pageerror',e=>report.errors.push(e.message));
 await mp.goto(base+'/?lang=ro');await mp.waitForSelector('#carousel-toggle');await mp.click('[data-slide="0"]');await mp.locator('#carousel-toggle').focus();await mp.keyboard.press('Enter');assert.equal(await mp.textContent('#carousel-toggle'),'Ⅱ');await mp.waitForTimeout(6800);assert.equal(await mp.getAttribute('[data-slide="1"]','aria-pressed'),'true');report.checks.push({type:'explicit-keyboard-play-with-focus',status:'passed'});
 await mp.keyboard.press('Enter');const selected=await mp.locator('[data-slide][aria-pressed=true]').getAttribute('data-slide');await mp.waitForTimeout(6800);assert.equal(await mp.locator('[data-slide][aria-pressed=true]').getAttribute('data-slide'),selected);report.checks.push({type:'pause-stops-autoplay',status:'passed'});
 await mp.goto(base+'/assets/eva-mark-animated.svg');assert.equal(await mp.locator('.beam').evaluate(e=>getComputedStyle(e).animationName),'scan');await mp.emulateMedia({reducedMotion:'reduce'});assert.equal(await mp.locator('.beam').evaluate(e=>getComputedStyle(e).animationName),'none');report.checks.push({type:'svg-animation-and-reduced-motion',status:'passed'});
 await motion.close();assert.deepEqual(report.errors,[]);report.status='passed';
}catch(error){report.status='failed';report.errors.push(error.stack);process.exitCode=1;}finally{await browser.close();report.finished=new Date().toISOString();await writeFile(path.join(root,'docs/validation/redesign-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,checks:report.checks.length,errors:report.errors}));}
