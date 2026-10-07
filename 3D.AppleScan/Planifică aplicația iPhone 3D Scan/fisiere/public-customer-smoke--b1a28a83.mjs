import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {writeFile} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..');const report={started:new Date().toISOString(),origin:'https://3dscan.eva-org.com',status:'running',checks:[],errors:[]};
const browser=await chromium.launch({headless:true});
try{const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});page.on('pageerror',e=>report.errors.push(e.message));
 const response=await page.goto(report.origin+'/?lang=ro');assert.equal(response.status(),200);await page.waitForSelector('#customer-profile');
 assert.equal(await page.locator('#customer-profile option').count(),7);report.checks.push('public HTTPS loads the final customer interface');
 await page.selectOption('#customer-profile','designer');await page.selectOption('#customer-problem','furniture-fit');assert.equal(await page.getAttribute('#customer-answer a','href'),'/measure?lang=ro');report.checks.push('public customer → problem → measurement link');
 await page.selectOption('#customer-profile','all');assert.equal(await page.locator('#customer-problem option').count(),36);report.checks.push('all 36 problems available publicly');
 await page.selectOption('#customer-profile','designer');await page.selectOption('#customer-problem','furniture-fit');await page.screenshot({path:path.join(root,'docs/validation/customer-public.png'),fullPage:false});
 assert.deepEqual(report.errors,[]);report.status='passed';
}catch(error){report.status='failed';report.errors.push(error.stack);process.exitCode=1;}finally{await browser.close();report.finished=new Date().toISOString();await writeFile(path.join(root,'docs/validation/public-customer-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));}
