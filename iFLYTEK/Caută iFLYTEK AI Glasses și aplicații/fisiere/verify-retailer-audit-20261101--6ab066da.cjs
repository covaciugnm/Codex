'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..','retailer-audit-2026-11-01');
(async()=>{
 const records=JSON.parse(fs.readFileSync(path.join(root,'file-inventory.json'),'utf8'));let verified=0;
 for(const r of records){const p=path.resolve(root,r.file);if(!p.startsWith(root+path.sep))throw Error('Unsafe path');
  if(!fs.existsSync(p)&&r.storage==='release'&&process.argv.includes('--restore')){
   const {spawnSync}=require('node:child_process');const result=spawnSync('gh',['release','download','iflytek-retailer-software-2026-11-01','--repo','covaciugnm/iFLYTEK','--pattern',path.basename(r.file),'--dir',path.dirname(p)],{stdio:'inherit'});if(result.status!==0)throw Error('Download failed');
  }
  if(!fs.existsSync(p))throw Error('Missing '+r.file+'; use --restore for release assets');
  const b=fs.readFileSync(p),h=crypto.createHash('sha256').update(b).digest('hex');if(b.length!==r.bytes||h!==r.sha256)throw Error('Integrity mismatch '+r.file);verified++;
 }
 console.log('Verified '+verified+' files, SHA-256 and size.');
})().catch(e=>{console.error(e);process.exitCode=1;});
