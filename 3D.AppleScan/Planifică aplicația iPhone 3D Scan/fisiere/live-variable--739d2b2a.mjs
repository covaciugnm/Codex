import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {execFileSync} from 'node:child_process';
import {writeFile} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');
const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..');
const base=process.env.SITE_TEST_URL||'http://127.0.0.1:4160';
const original=(await(await fetch(base+'/api/content?lang=ro')).json()).variables.docsPages;
const marker=Number(original)+1;
const update=value=>execFileSync('docker',['compose','exec','-T','db','psql','-U','eva_site','-d','eva_site','-v','ON_ERROR_STOP=1','-c',`UPDATE content_variables SET value='${JSON.stringify(value).replaceAll("'","''")}'::jsonb WHERE key='docsPages';`],{cwd:root,stdio:'pipe'});
const browser=await chromium.launch({headless:true});const page=await browser.newPage();
const report={started:new Date().toISOString(),type:'postgres-variable-live-update-without-reload',status:'failed'};
try {
 await page.goto(base+'/documentation?lang=ro');await page.waitForFunction(v=>document.body.textContent.includes(v+' de pagini'),original);
 const before=await page.evaluate(()=>performance.timeOrigin);
 try {update(marker);await page.waitForFunction(v=>document.body.textContent.includes(v+' de pagini'),marker);assert.equal(await page.evaluate(()=>performance.timeOrigin),before);report.status='passed';}
 finally {update(original);await page.waitForFunction(v=>document.body.textContent.includes(v+' de pagini'),original);report.restored=true;}
} catch(error){report.error=error.stack;process.exitCode=1;}
finally {await browser.close();report.finished=new Date().toISOString();await writeFile(path.join(root,'docs/validation/live-variable.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));}
