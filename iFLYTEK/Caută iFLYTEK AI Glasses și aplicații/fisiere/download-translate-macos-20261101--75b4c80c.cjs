'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
(async()=>{for(const arch of ['arm64','x64']){
 const url='https://saas-public-cdn-ioss.iflytranslate.com/desktop/iflytek-translate-saas-1.0.9-mac-'+arch+'.dmg';
 const head=await fetch(url,{method:'HEAD'}),size=Number(head.headers.get('content-length')),expected=head.headers.get('content-md5');if(!head.ok||!size)throw Error('HEAD failed');
 const b=Buffer.alloc(size),chunk=4*1024*1024;let cursor=0,done=0;
 async function worker(){while(cursor<size){const start=cursor;cursor+=chunk;const end=Math.min(start+chunk,size)-1;let ok=false;
  for(let attempt=0;attempt<4&&!ok;attempt++)try{const res=await fetch(url,{headers:{Range:'bytes='+start+'-'+end},signal:AbortSignal.timeout(90000)});if(res.status!==206||res.headers.get('content-range')!=='bytes '+start+'-'+end+'/'+size)throw Error('Invalid range response');const data=Buffer.from(await res.arrayBuffer());if(data.length!==end-start+1)throw Error('Truncated range');data.copy(b,start);ok=true;done+=data.length;console.log(arch,Math.round(done/size*100)+'%');}catch(e){if(attempt===3)throw e;}
 }}await Promise.all(Array.from({length:6},worker));
 if(b.subarray(-512,-508).toString()!=='koly')throw Error('Invalid DMG');if(expected&&crypto.createHash('md5').update(b).digest('base64')!==expected)throw Error('CDN MD5 mismatch');
 fs.writeFileSync(path.join(__dirname,'../retailer-audit-2026-11-01/software/iflytek-translate-mac-'+arch+'.dmg'),b);console.log('Saved',arch,size);
}})().catch(e=>{console.error(e);process.exitCode=1});
