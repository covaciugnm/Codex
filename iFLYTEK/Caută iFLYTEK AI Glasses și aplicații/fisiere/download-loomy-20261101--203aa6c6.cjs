'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),base=path.join(root,'collection-2026-11-01'),records=[];
(async()=>{
 await Promise.all([
 ['mac','Loomy-0.9.39-arm64.dmg'],['win','Loomy-Setup-0.9.39.exe'],['win&variant=secondary','Loomy-0.9.39-win.zip']
 ].map(async([p,n])=>{
  const url='https://loomy.xunfei.cn/api/download?platform='+p,r={url,kind:'installer',claimedVersion:'0.9.39',checkedAt:new Date().toISOString(),region:'China companion workflow; EU-specific edition unverified'};
  try{const res=await fetch(url,{signal:AbortSignal.timeout(180000)});r.httpStatus=res.status;r.finalUrl=res.url;r.contentType=res.headers.get('content-type');if(!res.ok)throw Error('HTTP '+res.status);const data=Buffer.from(await res.arrayBuffer());const valid=n.endsWith('.dmg')?data.subarray(-512,-508).toString()==='koly':n.endsWith('.exe')?data.subarray(0,2).toString()==='MZ':data.subarray(0,2).toString()==='PK';if(!valid)throw Error('Invalid installer format');r.bytes=data.length;r.sha256=crypto.createHash('sha256').update(data).digest('hex');r.file='applications/'+n;fs.writeFileSync(path.join(base,r.file),data);r.status='downloaded';}catch(e){r.status='unavailable';r.error=e.message;}records.push(r);fs.writeFileSync(path.join(base,'loomy-installers.json'),JSON.stringify(records,null,2)+'\n');console.log(r.status,n,r.bytes||'',r.error||'');
 }));
})().catch(e=>{console.error(e);process.exitCode=1});
