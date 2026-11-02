'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {out,hashes}=require('./audit-retailers-20261101.cjs');
const mp=path.join(out,'assets.json');const records=fs.existsSync(mp)?JSON.parse(fs.readFileSync(mp,'utf8')):[];
async function asset(url,name,scope,expectedIntegrity){const old=records.find(r=>r.url===url&&r.status!=='unavailable');if(old)return old;const r={url,scope,checkedAt:new Date().toISOString()};
 try{const res=await fetch(url,{signal:AbortSignal.timeout(900000)});r.statusCode=res.status;r.finalUrl=res.url;r.contentType=res.headers.get('content-type');if(!res.ok)throw Error('HTTP '+res.status);const data=Buffer.from(await res.arrayBuffer());if(/\.(?:zip|tgz|apk|xapk)$/.test(name)&&!data.subarray(0,2).equals(Buffer.from('PK'))&&!(data[0]===31&&data[1]===139))throw Error('Not a ZIP/APK/tar.gz');if(name.endsWith('.exe')&&data.subarray(0,2).toString()!=='MZ')throw Error('Not a Windows executable');if(name.endsWith('.dmg')&&data.subarray(-512,-508).toString()!=='koly')throw Error('Not a DMG');if(name.endsWith('.crx')&&data.subarray(0,4).toString()!=='Cr24')throw Error('Not a CRX');if(name.endsWith('.js')&&r.contentType?.includes('html'))throw Error('HTML instead of JavaScript');if(expectedIntegrity){const [algo,expected]=expectedIntegrity.split('-',2);const actual=crypto.createHash(algo).update(data).digest('base64');if(actual!==expected)throw Error('Registry integrity mismatch');r.registryIntegrityVerified=true;}
  r.bytes=data.length;r.sha256=crypto.createHash('sha256').update(data).digest('hex');const dup=hashes.get(r.sha256);if(dup){r.status='already-in-github';r.existing=dup;}else{r.file=name;r.status='downloaded';fs.mkdirSync(path.dirname(path.join(out,name)),{recursive:true});fs.writeFileSync(path.join(out,name),data);hashes.set(r.sha256,{path:'retailer-audit-2026-11-01/'+name});}
 }catch(e){r.status='unavailable';r.error=e.message;}
 const i=records.findIndex(x=>x.url===url);if(i>=0)records[i]=r;else records.push(r);fs.writeFileSync(mp,JSON.stringify(records,null,2)+'\n');console.log(r.status,name,r.bytes||'',r.error||'');return r;
}
module.exports={asset,records};
if(require.main===module)(async()=>{
 await asset('https://loomy.xunfei.cn/_next/static/chunks/3057-ba63193ab17adde0.js','resources/loomy-skills-3057.js','official-skills-code');
 await asset('https://loomy.xunfei.cn/_next/static/chunks/app/(public)/skills/page-9f3411dd0f8c1645.js','resources/loomy-skills-page.js','official-skills-code');
})().catch(e=>{console.error(e);process.exitCode=1});
