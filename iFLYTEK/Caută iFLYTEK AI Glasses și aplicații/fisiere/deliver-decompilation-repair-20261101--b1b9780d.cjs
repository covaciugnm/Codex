'use strict';
// Data-only CAS packaging/restoration. Never runs an APK or generated Java.
const fs=require('node:fs'),fsp=fs.promises,path=require('node:path'),zlib=require('node:zlib');
const {Readable}=require('node:stream'),{pipeline}=require('node:stream/promises'),{spawnSync}=require('node:child_process');
const {header,fileHash}=require('./package-apk-analysis-20261101.cjs');
const {unpack}=require('./restore-apk-analysis-20261101.cjs');
const repo=path.resolve(__dirname,'..'),defaultRoot=path.join(repo,'decompilation-repair-2026-11-01');
const repository='covaciugnm/iFLYTEK',releaseTag='iflytek-decompilation-repair-2026-11-01';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
function objectMap(rows){
 if(!Array.isArray(rows))throw Error('Missing object list');const m=new Map();
 for(const r of rows){if(!r||!/^[a-f0-9]{64}$/.test(r.sha256)||!Number.isSafeInteger(r.bytes)||r.bytes<0||m.has(r.sha256))throw Error('Invalid/duplicate CAS object');m.set(r.sha256,r.bytes);}return m;
}
function priorObjects(root=repo){
 const m=new Map(),sources=['iflytek-manifest-sha256.json','collection-2026-11-01/manifest.json','retailer-audit-2026-11-01/file-inventory.json','apk-analysis-2026-11-01/cas-index.json','apk-analysis-2026-11-01/baseline-release-index.json','loomy-translate-skill-2026-11-01/file-inventory.json'];
 const add=(h,n)=>{if(m.has(h)&&m.get(h)!==n)throw Error('Inconsistent prior size');m.set(h,n);};
 const visit=v=>{if(!v||typeof v!=='object')return;if(/^[a-f0-9]{64}$/.test(v.sha256)&&Number.isSafeInteger(v.bytes)&&v.bytes>=0)add(v.sha256,v.bytes);for(const [k,x] of Object.entries(v))if(x&&typeof x==='object'){if(/^[a-f0-9]{64}$/.test(k)&&Number.isSafeInteger(x.bytes)&&x.bytes>=0)add(k,x.bytes);visit(x);}};
 for(const p of sources){const q=path.join(root,p);if(!fs.existsSync(q))throw Error('Missing prior inventory '+p);visit(read(q));}return m;
}
function checkedManifest(m){
 if(!m||m.schemaVersion!==1||m.repository!==repository||m.releaseTag!==releaseTag||!Array.isArray(m.packs))throw Error('Unexpected delivery manifest');
 const all=new Map(),names=new Set();let total=0;
 for(const p of m.packs){if(!/^cas-\d{4}-[a-f0-9]{16}\.tar\.gz$/.test(p.name)||names.has(p.name)||!/^[a-f0-9]{64}$/.test(p.sha256)||!Number.isSafeInteger(p.bytes)||p.bytes<0)throw Error('Invalid pack metadata');names.add(p.name);
  for(const [h,n] of objectMap(p.objects)){if(all.has(h))throw Error('Repeated pack object');all.set(h,n);total+=n;}}
 if(m.objects!==all.size||m.objectBytes!==total)throw Error('Pack totals mismatch');return all;
}
async function checkObject(store,h,n){const p=path.join(store,'cas',h),s=await fsp.stat(p);if(!s.isFile()||s.size!==n||await fileHash(p)!==h)throw Error('CAS integrity mismatch '+h);}
async function pack(root,store,options={}){
 const index=read(path.join(root,'cas-index.json')),objects=objectMap(index.objects),prior=options.prior||priorObjects();
 for(const [h,n] of objects){if(prior.has(h))throw Error('Previously archived object must be referenced, not repacked: '+h);await checkObject(store,h,n);}
 const groups=[];let rows=[],size=0;for(const [h,n] of [...objects].sort((a,b)=>a[0].localeCompare(b[0]))){if(rows.length&&size+n>256*1024*1024){groups.push(rows);rows=[];size=0;}rows.push({sha256:h,bytes:n});size+=n;}if(rows.length)groups.push(rows);
 const folder=path.join(store,'packs');await fsp.mkdir(folder,{recursive:true});
 const manifest={schemaVersion:1,repository,releaseTag,format:'POSIX ustar gzip; cas/<sha256>; mtime=0',objects:objects.size,objectBytes:[...objects.values()].reduce((a,b)=>a+b,0),packs:[]};
 for(let i=0;i<groups.length;i++){
  const list=groups[i],temp=path.join(folder,'part-'+String(i+1).padStart(4,'0')+'.tar.gz.partial');
  async function* tar(){for(const o of list){yield header('cas/'+o.sha256,o.bytes);for await(const b of fs.createReadStream(path.join(store,'cas',o.sha256)))yield b;const pad=(512-o.bytes%512)%512;if(pad)yield Buffer.alloc(pad);}yield Buffer.alloc(1024);}
  await pipeline(Readable.from(tar()),zlib.createGzip({level:6}),fs.createWriteStream(temp,{flags:'wx'}));
  const hash=await fileHash(temp),name='cas-'+String(i+1).padStart(4,'0')+'-'+hash.slice(0,16)+'.tar.gz',dest=path.join(folder,name);
  if(fs.existsSync(dest)){if(await fileHash(dest)!==hash)throw Error('Conflicting pack');await fsp.unlink(temp);}else await fsp.rename(temp,dest);
  manifest.packs.push({name,sha256:hash,bytes:(await fsp.stat(dest)).size,objects:list,downloadUrl:'https://github.com/'+repository+'/releases/download/'+releaseTag+'/'+name});
 }
 checkedManifest(manifest);const text=JSON.stringify(manifest,null,2)+'\n';await fsp.writeFile(path.join(root,'release-packs.json'),text);return manifest;
}
async function restore(root,store,options={}){
 const m=read(path.join(root,'release-packs.json')),expected=checkedManifest(m),index=objectMap(read(path.join(root,'cas-index.json')).objects);
 if(expected.size!==index.size||[...expected].some(([h,n])=>index.get(h)!==n))throw Error('CAS index differs from pack index');
 await fsp.mkdir(store,{recursive:true});let restored=0;
 for(const p of m.packs){let complete=true;for(const [h,n] of objectMap(p.objects)){try{await checkObject(store,h,n);}catch{complete=false;break;}}if(complete)continue;
  const folder=path.join(store,'packs'),file=path.join(folder,p.name);await fsp.mkdir(folder,{recursive:true});
  if(!fs.existsSync(file)){if(options.localOnly)throw Error('Missing local pack '+p.name);const r=spawnSync('gh',['release','download',releaseTag,'--repo',repository,'--pattern',p.name,'--dir',folder],{stdio:'inherit',windowsHide:true});if(r.status!==0)throw Error('Download failed');}
  if((await fsp.stat(file)).size!==p.bytes||await fileHash(file)!==p.sha256)throw Error('Pack checksum mismatch');restored+=await unpack(file,p,store);
 }
 for(const [h,n] of expected)await checkObject(store,h,n);return{verifiedObjects:expected.size,restoredObjects:restored,packs:m.packs.length};
}
async function main(){const args=process.argv.slice(2),get=(k,d)=>{const i=args.indexOf(k);return i<0?d:path.resolve(args[i+1]||'');};const root=get('--analysis-root',defaultRoot),store=get('--store-dir','D:/Codex-iflytek-decompilation-repair-20261101');
 if(args.includes('--pack')){const m=await pack(root,store);console.log(JSON.stringify({objects:m.objects,objectBytes:m.objectBytes,packs:m.packs.length}));}
 else if(args.includes('--restore'))console.log(JSON.stringify(await restore(root,store,{localOnly:args.includes('--local-only')})));
 else throw Error('Use --pack or --restore [--analysis-root DIRECTORY] [--store-dir DIRECTORY] [--local-only]');}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={objectMap,checkedManifest,priorObjects,pack,restore};
