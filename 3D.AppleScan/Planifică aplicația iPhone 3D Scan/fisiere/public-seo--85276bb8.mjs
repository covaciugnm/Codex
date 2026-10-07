import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import path from 'node:path';
const origin='https://3dscan.eva-org.com';const report={started:new Date().toISOString(),origin,checks:[],note:'HTTP verification from the deployment server; Google indexation and ranking not measured.'};
try{
 for(const [route,lang] of [['/uses','ro'],['/people','en'],['/objects','de']]){const response=await fetch(origin+route+'?lang='+lang);assert.equal(response.status,200);const html=await response.text();assert.ok(html.includes(`href="${origin}${route}?lang=${lang}"`));assert.ok(html.includes(`lang="${lang}"`));assert.ok(html.includes('seo-jsonld'));assert.ok(!html.includes('noindex'));if(route==='/uses')assert.equal((html.match(/id="usecase-/g)||[]).length,36);report.checks.push({route,lang,status:response.status,ssr:true});}
 const robots=await fetch(origin+'/robots.txt');assert.equal(robots.status,200);assert.ok((await robots.text()).includes('Sitemap: '+origin+'/sitemap.xml'));report.checks.push({route:'/robots.txt',status:200});
 const sitemap=await fetch(origin+'/sitemap.xml');assert.equal(sitemap.status,200);const xml=await sitemap.text();assert.equal((xml.match(/<loc>/g)||[]).length,63);report.checks.push({route:'/sitemap.xml',status:200,urls:63});report.status='passed';
}catch(error){report.status='failed';report.error=error.stack;process.exitCode=1;}
report.finished=new Date().toISOString();await writeFile(path.resolve(import.meta.dirname,'../docs/validation/public-seo-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
