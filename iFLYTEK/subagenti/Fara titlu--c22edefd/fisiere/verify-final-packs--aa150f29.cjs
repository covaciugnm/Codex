'use strict';
// Independent streaming verification: does not unpack packs or reuse the restore parser.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib');
const root=path.resolve(__dirname,'..'),repo=path.resolve(root,'..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const packDir=process.env.IFLYTEK_AUDIT_PACK_DIR||path.join(root,'packs');
const hashFile=async p=>{const h=crypto.createHash('sha256');for await(const b of fs.createReadStream(p))h.update(b);return h.digest('hex');};
const previous=read(path.join(repo,'iflytek-manifest-sha256.json')).files,recent=read(path.join(repo,'collection-2026-11-01/manifest.json')).records,extra=read(path.join(root,'baseline-release-index.json'));
const retailers=read(path.join(repo,'retailer-audit-2026-11-01/file-inventory.json'));
const oldHashes=new Set([...previous,...recent,...retailers].map(r=>r.sha256).filter(Boolean));for(const h of Object.keys(extra))oldHashes.add(h);
const oldSizes=new Map(previous.map(r=>[r.sha256,r.bytes])),oldPaths=new Map(previous.map(r=>[r.path,r]));
for(const r of recent)if(r.sha256&&Number.isSafeInteger(r.bytes)){oldSizes.set(r.sha256,r.bytes);if(r.file)oldPaths.set('collection-2026-11-01/'+r.file,r);}
for(const r of retailers){oldSizes.set(r.sha256,r.bytes);oldPaths.set('retailer-audit-2026-11-01/'+r.file,r);}
for(const [h,r] of Object.entries(extra))oldSizes.set(h,r.bytes);
const index=read(path.join(root,'cas-index.json')),manifest=read(path.join(root,'release-packs.json')),catalog=read(path.join(root,'catalog.json'));
const indexed=new Map();for(const o of index.objects){if(indexed.has(o.sha256)||oldHashes.has(o.sha256))throw Error('Duplicate new/baseline content '+o.sha256);indexed.set(o.sha256,o.bytes);}
const refs=new Set(),decomp=new Set();let logicalRefs=0;
function checkRecords(records){for(const r of records||[]){if(r.storage==='cas'){if(indexed.get(r.sha256)!==r.bytes)throw Error('CAS reference missing/wrong size');refs.add(r.sha256);logicalRefs++;}else if(r.storage==='existing'){
 if(oldSizes.get(r.sha256)!==r.bytes)throw Error('Unknown/wrong existing reference');const e=r.existing;if(!e)throw Error('Missing baseline pointer');
 if(e.storage==='release-zip-entry'){const x=extra[r.sha256];if(!x||x.entry!==e.entry||x.archiveSha256!==e.archiveSha256||x.asset!==e.asset)throw Error('Wrong baseline ZIP pointer');}
 else {const x=oldPaths.get(e.path);if(!x||x.sha256!==r.sha256||x.bytes!==r.bytes)throw Error('Wrong baseline file pointer');}
 }else if(r.storage!=='source-zip-entry')throw Error('Unaccounted storage');}}
for(const v of catalog.versions){const m=read(path.join(root,v.manifest));if(m.decompilation.status==='pending')throw Error('Pending version');checkRecords(m.entries);checkRecords(m.outerEntries);for(const c of m.decompilation.components||[])decomp.add(c.manifest);}
for(const p of decomp){const d=read(path.join(root,p));checkRecords(d.entries);checkRecords(d.logs);if(!d.entries.length)throw Error('Empty decompilation report');if(d.originalSource!==false)throw Error('Missing decompilation disclaimer');}
if(refs.size!==indexed.size||[...indexed.keys()].some(h=>!refs.has(h)))throw Error('Orphan/missing CAS index object');
const seen=new Set(),results=[];
async function verifyPack(pack){
 const p=path.join(packDir,pack.name);if(fs.statSync(p).size!==pack.bytes||await hashFile(p)!==pack.sha256)throw Error('Pack digest mismatch '+pack.name);
 const expected=new Map(pack.objects.map(o=>[o.sha256,o.bytes]));if(expected.size!==pack.objects.length)throw Error('Repeated object in pack index');
 let buffer=Buffer.alloc(0),current=null,padding=0,zeroBlocks=0,count=0,bytes=0;
 for await(const chunk of fs.createReadStream(p).pipe(zlib.createGunzip())){
  buffer=Buffer.concat([buffer,chunk]);
  while(buffer.length){
   if(padding){const n=Math.min(buffer.length,padding);buffer=buffer.subarray(n);padding-=n;if(padding)break;continue;}
   if(!current){if(buffer.length<512)break;const header=buffer.subarray(0,512);buffer=buffer.subarray(512);if(header.every(n=>n===0)){zeroBlocks++;continue;}if(zeroBlocks)throw Error('TAR data after footer');
    let sum=0;for(let i=0;i<512;i++)sum+=i>=148&&i<156?32:header[i];const checksum=parseInt(header.subarray(148,156).toString().replace(/\0/g,'').trim(),8);if(sum!==checksum)throw Error('TAR checksum failure');
    const name=header.subarray(0,100).toString().split('\0')[0],size=parseInt(header.subarray(124,136).toString().replace(/\0/g,'').trim(),8);if(!/^cas\/[a-f0-9]{64}$/.test(name)||header[156]!==48)throw Error('Unexpected TAR member');const h=name.slice(4);if(expected.get(h)!==size||indexed.get(h)!==size||seen.has(h))throw Error('Unlisted/repeated TAR object');current={sha256:h,size,remaining:size,hash:crypto.createHash('sha256')};
   }
   const n=Math.min(current.remaining,buffer.length);current.hash.update(buffer.subarray(0,n));buffer=buffer.subarray(n);current.remaining-=n;if(current.remaining)break;
   if(current.hash.digest('hex')!==current.sha256)throw Error('Object SHA mismatch');seen.add(current.sha256);expected.delete(current.sha256);padding=(512-current.size%512)%512;bytes+=current.size;count++;current=null;
  }
 }
 if(current||padding||buffer.length||zeroBlocks<2||expected.size)throw Error('Incomplete TAR pack');return{name:pack.name,objects:count,objectBytes:bytes,sha256:pack.sha256,status:'PASS'};
}
(async()=>{for(const p of manifest.packs)results.push(await verifyPack(p));if(seen.size!==indexed.size||[...indexed.keys()].some(h=>!seen.has(h)))throw Error('Incomplete pack coverage');if(manifest.objects!==seen.size||manifest.objectBytes!==results.reduce((n,r)=>n+r.objectBytes,0))throw Error('Wrong aggregate pack metadata');
const result={checkedAt:new Date().toISOString(),status:'PASS',versions:catalog.versions.length,decompilationGroups:decomp.size,uniqueNewObjects:seen.size,logicalNewObjectReferences:logicalRefs,duplicateContentAgainstBaseline:0,packs:results};fs.writeFileSync(path.join(__dirname,'final-pack-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
