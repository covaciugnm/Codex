'use strict';
// Read-only inspection of the previously archived XAPK; writes derived inputs to D: only.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {zipEntries}=require('./inspect-android-archive.cjs');
const repo=path.resolve(__dirname,'..'),work='D:/Codex-iflytek-decompilation-repair-20261101',hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function adler(b){let a=1,z=0;for(let start=0;start<b.length;start+=5552){const end=Math.min(b.length,start+5552);for(let i=start;i<end;i++){a+=b[i];z+=a;}a%=65521;z%=65521;}return((z<<16)|a)>>>0;}
function main(){
 const old=path.join(repo,'loomy-translate-skill-2026-11-01'),inventory=JSON.parse(fs.readFileSync(path.join(old,'file-inventory.json'))),entry=inventory.find(r=>r.file==='other-hardware/HeyCyan-1.0.173_20261017.xapk');if(!entry)throw Error('Archived HeyCyan entry missing');
 const source=path.join(old,entry.file),b=fs.readFileSync(source);if(b.length!==entry.bytes||hash(b)!==entry.sha256)throw Error('Archived XAPK checksum mismatch');
 const folder=path.join(work,'inputs/heycyan'),components=[],allDex=[];fs.mkdirSync(folder,{recursive:true});
 for(const a of zipEntries(b).filter(x=>x.name.toLowerCase().endsWith('.apk'))){if(a.name!==path.basename(a.name))throw Error('Unexpected nested APK path');const bytes=a.read(),apkSha256=hash(bytes),component={name:a.name,sha256:apkSha256,bytes:bytes.length,dex:[]};
  for(const d of zipEntries(bytes).filter(x=>/^classes(?:\d+)?\.dex$/.test(x.name))){const data=d.read();if(data.length<112||data.subarray(0,4).toString()!=='dex\n'||data.readUInt32LE(32)!==data.length)throw Error('Invalid DEX header');const p=path.join(folder,apkSha256,d.name);fs.mkdirSync(path.dirname(p),{recursive:true});if(fs.existsSync(p)){const prior=fs.readFileSync(p);if(prior.length!==data.length||hash(prior)!==hash(data))throw Error('Existing derived DEX differs');}else fs.writeFileSync(p,data);
   const r={path:d.name,sha256:hash(data),bytes:data.length,classDefinitions:data.readUInt32LE(96),dexSignatureSha1Valid:crypto.createHash('sha1').update(data.subarray(32)).digest().equals(data.subarray(12,32)),dexAdler32Valid:adler(data.subarray(12))===data.readUInt32LE(8),localPath:p};component.dex.push(r);allDex.push({...r,component:a.name});}
  components.push(component);
 }
 if(components.length!==20||!allDex.length)throw Error('Unexpected archived split/DEX coverage');
 const report={schemaVersion:1,generatedAt:new Date().toISOString(),generator:{file:'tools/prepare-heycyan-decompilation-20261101.cjs',sha256:hash(fs.readFileSync(__filename))},scope:'Other hardware; no compatibility claim for XF-AIGlasses-01',package:'com.glasssutdio.wear',version:'1.0.173_20261017',source:{file:entry.file,sha256:entry.sha256,bytes:entry.bytes,alreadyArchived:true},components,dexFiles:allDex.length,classDefinitions:allDex.reduce((n,r)=>n+r.classDefinitions,0),dexSetSha256:hash(Buffer.from(allDex.map(r=>r.component+'/'+r.path+':'+r.sha256).sort().join('\n'))),allDexHeaderChecksPassed:allDex.every(r=>r.dexSignatureSha1Valid&&r.dexAdler32Valid),decompilerExecution:false};
 fs.writeFileSync(path.join(work,'HEY-CYAN-INPUT.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({components:components.length,dexFiles:report.dexFiles,classDefinitions:report.classDefinitions,dexHeaderChecksPassed:report.allDexHeaderChecksPassed,dexSetSha256:report.dexSetSha256}));
}
if(require.main===module)main();
