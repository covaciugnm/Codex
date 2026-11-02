'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {zipEntries}=require('./inspect-android-archive.cjs');
const repo=path.resolve(__dirname,'..'),root=path.join(repo,'apk-analysis-2026-11-01');
const option=(name,fallback)=>{const i=process.argv.indexOf(name);return i<0?fallback:process.argv[i+1];};
const store=path.resolve(option('--store-dir',root)),cache=path.resolve(option('--cache-dir',path.join(store,'existing-cache'))),localOnly=process.argv.includes('--local-only');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const zipCache=new Map(),gitBlobCache=new Map();
function safe(root,name){if(!name||name.includes('\\')||name.startsWith('/')||name.split('/').includes('..')||/^[a-z]:/i.test(name))throw Error('Unsafe logical path '+name);const p=path.resolve(root,name);if(!p.startsWith(path.resolve(root)+path.sep))throw Error('Path escape');return p;}
function download(release,asset){if(!release||!asset||asset!==path.basename(asset))throw Error('Invalid release pointer');const folder=path.join(cache,release),p=path.join(folder,asset);if(fs.existsSync(p))return p;if(localOnly)throw Error('Missing cached release '+p);fs.mkdirSync(folder,{recursive:true});const r=cp.spawnSync('gh',['release','download',release,'--repo','covaciugnm/iFLYTEK','--pattern',asset,'--dir',folder],{stdio:'inherit',windowsHide:true});if(r.status!==0)throw Error('Release download failed');return p;}
function gitRef(e){if(e.gitBlobSha1){if(!/^[a-f0-9]{40}$/.test(e.gitBlobSha1))throw Error('Invalid stable Git object ID');return e.gitBlobSha1;}return'HEAD:'+e.path;}
function existing(e){
 if(e.storage==='release-zip-entry'){
  const p=download(e.release,e.asset);let map=zipCache.get(p);if(!map){const b=fs.readFileSync(p);if(hash(b)!==e.archiveSha256)throw Error('Existing ZIP hash mismatch');map=new Map(zipEntries(b).map(x=>[x.name,x]));zipCache.set(p,map);}const entry=map.get(e.entry);if(!entry)throw Error('Missing existing ZIP entry '+e.entry);return entry.read();
 }
 if(e.storage==='release')return fs.readFileSync(download(e.release||'iflytek-documentation-2026-10-31',e.asset));
 if(!e.path)throw Error('Missing existing Git path');if(gitBlobCache.has(e.path))return gitBlobCache.get(e.path);const local=safe(repo,e.path);if(fs.existsSync(local)){const b=fs.readFileSync(local);if(!e.gitBlobSha1||crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')===e.gitBlobSha1)return b;}
 const result=cp.spawnSync('git',['show',gitRef(e)],{cwd:repo,encoding:null,maxBuffer:1024*1024*1024,windowsHide:true,env:{...process.env,...(localOnly?{GIT_NO_LAZY_FETCH:'1'}:{})}});if(result.status!==0)throw Error('Existing Git object unavailable '+e.path);return result.stdout;
}
function resolve(r){let b;if(r.storage==='cas')b=fs.readFileSync(path.join(store,'cas',r.sha256));else if(r.storage==='existing')b=existing(r.existing);else throw Error('Unsupported storage '+r.storage);if(b.length!==r.bytes||hash(b)!==r.sha256)throw Error('Logical object mismatch '+r.sha256);return b;}
function put(base,name,r){const p=safe(base,name),b=resolve(r);fs.mkdirSync(path.dirname(p),{recursive:true});if(fs.existsSync(p)){const old=fs.readFileSync(p);if(old.length!==r.bytes||hash(old)!==r.sha256)throw Error('Existing output differs '+p);}else fs.writeFileSync(p,b);return 1;}
const fold=s=>s.normalize('NFC').toUpperCase();
function planPaths(rows){
 const siblings=new Map(),seenLogical=new Set();
 for(const row of rows){
  const parts=row.logical.split('/');if(!row.logical||row.logical.includes('\\')||parts.some(s=>!s||s==='.'||s==='..'))throw Error('Unsafe logical materialization path '+JSON.stringify(row.logical));
  if(seenLogical.has(row.logical))throw Error('Duplicate logical materialization path '+row.logical);seenLogical.add(row.logical);
  for(let i=0;i<parts.length;i++){const parent=parts.slice(0,i).join('/'),key=parent+'\0'+fold(parts[i]);if(!siblings.has(key))siblings.set(key,new Set());siblings.get(key).add(JSON.stringify([parts[i],i===parts.length-1?'file':'directory']));}
 }
 const physicalNodes=new Map(),planned=[];
 for(const row of rows){const parts=row.logical.split('/'),mapped=[];
  for(let i=0;i<parts.length;i++){
   const segment=parts[i],parent=parts.slice(0,i).join('/'),prefix=parts.slice(0,i+1).join('/'),kind=i===parts.length-1?'file':'directory';
   const conflict=siblings.get(parent+'\0'+fold(segment)).size>1;
   const deviceStem=segment.split('.')[0].replace(/[. ]+$/,'');
   const invalid=/[<>:"|?*\x00-\x1f]/.test(segment)||/[. ]$/.test(segment)||/^(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|CLOCK\$|COM[1-9¹²³]|LPT[1-9¹²³])$/i.test(deviceStem)||/^_apkcase_/i.test(segment)||segment.length>180;
   const readable=segment.replace(/[^A-Za-z0-9._-]/g,'_').slice(0,80)||'entry';
   const physical=conflict||invalid?'_apkcase_'+hash(Buffer.from(JSON.stringify([prefix,kind])))+'_'+readable:segment;
   mapped.push(physical);const key=fold(mapped.join('/')),identity=JSON.stringify([prefix,kind]),prior=physicalNodes.get(key);
   if(prior&&prior!==identity)throw Error('Physical path collision: '+prior+' versus '+identity+' at '+mapped.join('/'));physicalNodes.set(key,identity);
  }
  planned.push({...row,physical:mapped.join('/')});
 }
 return planned.sort((a,b)=>a.logical<b.logical?-1:a.logical>b.logical?1:0);
}
function preloadGit(records){
 const entries=[...new Map(records.filter(r=>r.storage==='existing'&&r.existing.storage==='git').map(r=>[r.existing.path,r])).values()];if(!entries.length)return;
 for(const r of entries){safe(repo,r.existing.path);if(/[\r\n]/.test(r.existing.path))throw Error('Unsupported Git path');}
 const result=cp.spawnSync('git',['cat-file','--batch'],{cwd:repo,input:entries.map(r=>gitRef(r.existing)).join('\n')+'\n',encoding:null,maxBuffer:1024*1024*1024,windowsHide:true,env:{...process.env,...(localOnly?{GIT_NO_LAZY_FETCH:'1'}:{})}});
 if(result.status!==0)throw Error('Git batch preload failed: '+String(result.stderr).slice(0,200));const b=result.stdout;let offset=0;
 for(const r of entries){const end=b.indexOf(10,offset);if(end<0)throw Error('Incomplete Git batch header');const header=b.subarray(offset,end).toString('utf8'),match=/^[a-f0-9]{40,64} blob (\d+)$/.exec(header);if(!match)throw Error('Git blob unavailable '+r.existing.path);const size=Number(match[1]);offset=end+1;if(offset+size>=b.length||b[offset+size]!==10)throw Error('Incomplete Git batch object');const value=b.subarray(offset,offset+size);if(size!==r.bytes||hash(value)!==r.sha256)throw Error('Git batch SHA-256 mismatch '+r.existing.path);gitBlobCache.set(r.existing.path,value);offset+=size+1;}
 if(offset!==b.length)throw Error('Unexpected Git batch trailing bytes');console.log('Preloaded and verified',entries.length,'Git objects.');
}
async function main(){
 const name=option('--manifest');if(!name)throw Error('Usage: --manifest versions/package/version/variant/manifest.json --output DIRECTORY [--store-dir DIRECTORY] [--cache-dir DIRECTORY] [--local-only]');
 const manifest=safe(root,name),m=JSON.parse(fs.readFileSync(manifest,'utf8')),destination=path.resolve(option('--output',path.join(store,'materialized',m.package,m.version,m.variant)));
 if(destination===repo||destination===root||destination===store)throw Error('Choose a separate materialization directory');
 const codeReports=!process.argv.includes('--raw-only')?(m.decompilation.components||[]).map(c=>({component:c.component,report:JSON.parse(fs.readFileSync(safe(root,c.manifest),'utf8'))})):[];
 const rows=m.entries.map(r=>({kind:'raw',component:r.component,path:r.path,logical:'raw/'+r.component+'/'+r.path,record:r}));
 for(const r of m.outerEntries||[])if(r.storage!=='source-zip-entry')rows.push({kind:'xapk-sidecar',component:null,path:r.path,logical:'xapk/'+r.path,record:r});
 for(const c of codeReports){for(const r of c.report.entries||[])rows.push({kind:'decompiled',component:c.component,path:r.path,logical:'decompiled/'+c.component+'/'+r.path,record:r});for(const r of c.report.logs||[])rows.push({kind:'log',component:c.component,path:r.path,logical:'logs/'+c.component+'/'+r.path.replace(/.*\//,''),record:r});}
 const planned=planPaths(rows),pathMap={schemaVersion:1,mapping:'windows-safe-v1',package:m.package,version:m.version,variant:m.variant,sourceSha256:m.source.sha256,paths:planned.map(r=>({kind:r.kind,component:r.component,path:r.path,logical:r.logical,physical:r.physical,sha256:r.record.sha256,bytes:r.record.bytes}))};
 const mapFile=path.join(destination,'PATH-MAP.json'),mapText=JSON.stringify(pathMap,null,2)+'\n';
 if(fs.existsSync(destination)&&fs.readdirSync(destination).length){if(!fs.existsSync(mapFile)||fs.readFileSync(mapFile,'utf8')!==mapText)throw Error('Choose a fresh output directory: existing files lack the same PATH-MAP.json. No existing files were changed.');}
 fs.mkdirSync(destination,{recursive:true});if(!fs.existsSync(mapFile)){fs.writeFileSync(mapFile+'.partial',mapText);fs.renameSync(mapFile+'.partial',mapFile);}
 if(process.argv.includes('--preload-git'))preloadGit(rows.map(r=>r.record));
 let raw=0,decompiled=0,sidecars=0;
 for(const r of planned){put(destination,r.physical,r.record);if(r.kind==='raw')raw++;else if(r.kind==='xapk-sidecar')sidecars++;else decompiled++;}
 fs.mkdirSync(destination,{recursive:true});fs.writeFileSync(path.join(destination,'SOURCE-MANIFEST.json'),JSON.stringify(m,null,2)+'\n');
 console.log(JSON.stringify({package:m.package,version:m.version,variant:m.variant,destination,raw,decompiled,sidecars,mappedPaths:planned.filter(r=>r.logical!==r.physical).length,pathMap:'PATH-MAP.json',verified:'Every materialized file SHA-256 and size verified; original logical names preserved reversibly in PATH-MAP.json.'},null,2));
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={resolve,safe,existing,planPaths};
