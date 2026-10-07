import {createRequire} from 'node:module';
import {writeFile} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');const {chromium}=require('playwright');
const base='http://127.0.0.1:4160';const times=[];let bytes=0;
for(let i=0;i<30;i++){const begin=performance.now();const r=await fetch(base+'/api/content?lang=ro');if(!r.ok)throw Error('API unavailable');const body=await r.text();times.push(performance.now()-begin);bytes=Buffer.byteLength(body);}
times.sort((a,b)=>a-b);const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1440,height:1000}});
await page.addInitScript(()=>{window.lcpValues=[];new PerformanceObserver(list=>{for(const e of list.getEntries())window.lcpValues.push(e.startTime);}).observe({type:'largest-contentful-paint',buffered:true});});
await page.goto(base+'/?lang=ro');await page.waitForSelector('main h1');await page.waitForTimeout(800);
const metrics=await page.evaluate(()=>({navigation_ms:performance.getEntriesByType('navigation')[0].duration,lcp_ms:window.lcpValues.at(-1),resources:performance.getEntriesByType('resource').filter(r=>r.responseEnd>0).map(r=>({name:new URL(r.name).pathname,encoded_bytes:r.encodedBodySize,duration_ms:r.duration}))}));
await browser.close();const report={created:new Date().toISOString(),scope:'One local-server browser sample and 30 sequential API requests, no WAN or CPU throttling; not field Core Web Vitals',api:{requests:30,p50_ms:times[14],p95_ms:times[28],response_bytes:bytes},browser:metrics};await writeFile(path.resolve(import.meta.dirname,'../docs/validation/performance.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
