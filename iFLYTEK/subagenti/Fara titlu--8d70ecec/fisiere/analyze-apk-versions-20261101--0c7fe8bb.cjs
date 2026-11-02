'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib');
const {zipEntries,inspect}=require('./inspect-android-archive.cjs');
const root=path.resolve(__dirname,'..'),out=path.join(root,'apk-analysis-2026-11-01'),work=process.env.IFLYTEK_APK_WORK_ROOT||path.join(out,'.work'),casRoot=process.env.IFLYTEK_APK_CAS_ROOT||path.join(out,'cas');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const write=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');};
const baseline=JSON.parse(fs.readFileSync(path.join(root,'iflytek-manifest-sha256.json'))).files;
const known=new Map();for(const r of baseline)if(!known.has(r.sha256))known.set(r.sha256,{path:r.path,storage:r.storage,asset:r.asset,release:r.storage==='release'?'iflytek-documentation-2026-10-31':undefined});
const recent=JSON.parse(fs.readFileSync(path.join(root,'collection-2026-11-01/manifest.json'))).records;
for(const r of recent)if(r.sha256&&r.file&&!known.has(r.sha256))known.set(r.sha256,{path:'collection-2026-11-01/'+r.file,storage:r.storage,asset:r.assetName,release:r.releaseTag});
const table=Array.from({length:256},(_,n)=>{let c=n;for(let j=0;j<8;j++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0;});
function crc(b){let c=0xffffffff;for(const v of b)c=table[(c^v)&255]^(c>>>8);return(c^0xffffffff)>>>0;}
function entries(b){const es=zipEntries(b);let end=b.length-22;while(b.readUInt32LE(end)!==0x06054b50)end--;let p=b.readUInt32LE(end+16);for(const e of es){e.crc32=b.readUInt32LE(p+16);p+=46+b.readUInt16LE(p+28)+b.readUInt16LE(p+30)+b.readUInt16LE(p+32);}return es;}
function object(b){const h=sha(b),existing=known.get(h);if(existing)return{sha256:h,bytes:b.length,storage:'existing',existing};const rel='cas/'+h;const target=path.join(casRoot,h);if(!fs.existsSync(target)){fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,b);}return{sha256:h,bytes:b.length,storage:'cas',cas:rel};}
function checked(e){const b=e.read();if(crc(b)!==e.crc32)throw Error('CRC mismatch '+e.name);return b;}
function safe(name){if(name.includes('\\')||name.startsWith('/')||name.split('/').includes('..')||/^[a-z]:/i.test(name))throw Error('Unsafe ZIP entry '+name);}
const inputs=[];
for(const r of recent.filter(r=>r.file&&/\.(apk|xapk)$/i.test(r.file))){const name=path.basename(r.file);inputs.push({local:process.env.IFLYTEK_APK_WORK_ROOT?path.join(work,'inputs',name):path.join(root,'collection-2026-11-01',r.file),name,kind:'vendor',references:[{path:'collection-2026-11-01/'+r.file,...known.get(r.sha256)}],expectedSha256:r.sha256,expectedBytes:r.bytes});}
for(const h of [...new Set(baseline.filter(r=>/\.apk$/i.test(r.path)).map(r=>r.sha256))]){const rows=baseline.filter(r=>r.sha256===h);const name=path.basename(rows[0].path),local=path.join(work,'inputs',rows[0].asset||name);inputs.push({local,name,kind:'vendor',references:rows.map(r=>({path:r.path,storage:r.storage,asset:r.asset,release:r.storage==='release'?'iflytek-documentation-2026-10-31':undefined})),expectedSha256:h});}
for(const [name,h] of [['iflytek-1.0.3899-full-rebuilt.apk','c10d5475f384d433884e44417126f1077478790241ab174bc5987a08a98f038c'],['iflytek-1.0.3899-romania40.apk','82aa11096fbd474f0669b5ca295e325fd0b0c45c2999360859d1bd93821a9aa8']])inputs.push({local:path.join(work,'inputs',name),name,kind:'derived-modified-not-vendor',references:[{storage:'release',release:'iflytek-apk-romania40-2026-10-31',asset:name}],expectedSha256:h});
const catalog={schemaVersion:1,date:'2026-11-01',scope:'All vendor and derived APK/XAPK containers identified in the repository and its releases',versions:[],baselineManifest:'iflytek-manifest-sha256.json',tool:'tools/analyze-apk-versions-20261101.cjs',notes:['Static unpacking only; no APK executed. Decompilation is not original source. CAS deduplicates by bytes across versions and existing repository files.']};
const jobs=[];
for(const input of inputs){
 const b=fs.readFileSync(input.local),hash=sha(b);if(input.expectedSha256&&hash!==input.expectedSha256)throw Error('Input mismatch '+input.name);if(input.expectedBytes&&b.length!==input.expectedBytes)throw Error('Input size mismatch '+input.name);
 const meta=inspect(input.local),pkg=meta.package||meta.manifest.package_name,version=meta.versionName||meta.manifest.version_name;
 const variant=input.name.replace(/\.(apk|xapk)$/,'');const relative='versions/'+pkg+'/'+version+'/'+variant;
 const m={schemaVersion:1,package:pkg,version,variant,kind:input.kind,source:{sha256:hash,bytes:b.length,format:meta.format,references:input.references},inspection:meta,outerEntries:[],components:[],entries:[],decompilation:{status:'pending'}};
 const outer=entries(b),components=[];
 if(meta.format==='XAPK')for(const e of outer){safe(e.name);const d=checked(e);if(e.name.endsWith('.apk')){m.outerEntries.push({path:e.name,bytes:d.length,sha256:sha(d),storage:'source-zip-entry',sourceSha256:hash});const temp=path.join(work,'components',sha(d)+'.apk');fs.mkdirSync(path.dirname(temp),{recursive:true});if(!fs.existsSync(temp))fs.writeFileSync(temp,d);components.push({name:e.name,buffer:d,local:temp});}else m.outerEntries.push({path:e.name,...object(d),crc32:e.crc32});}
 else components.push({name:'base.apk',buffer:b,local:input.local});
 for(const component of components){const es=entries(component.buffer),names=new Set(),dex=[];for(const e of es){safe(e.name);if(names.has(e.name))throw Error('Duplicate ZIP entry '+e.name);names.add(e.name);if(e.name.endsWith('/'))continue;const d=checked(e),record={component:component.name,path:e.name,crc32:e.crc32,...object(d)};m.entries.push(record);if(/^classes\d*\.dex$/.test(e.name))dex.push({path:e.name,sha256:record.sha256,bytes:d.length});}
 const dexSetSha256=sha(Buffer.from(dex.map(x=>x.path+':'+x.sha256).sort().join('\n')));
 const c={name:component.name,sha256:sha(component.buffer),bytes:component.buffer.length,entries:es.filter(e=>!e.name.endsWith('/')).length,directories:es.filter(e=>e.name.endsWith('/')).length,dex,dexSetSha256,resourceHandling:'All resources, binary XML, manifest and native libraries preserved byte-for-byte with SHA-256 and CRC32; no source code expected from resource-only split.'};m.components.push(c);if(dex.length)jobs.push({manifest:relative+'/manifest.json',component:component.name,dexSetSha256,input:component.local});
 }
 const stats={entries:m.entries.length,existingReferences:m.entries.filter(r=>r.storage==='existing').length,casReferences:m.entries.filter(r=>r.storage==='cas').length};m.statistics=stats;write(path.join(out,relative,'manifest.json'),m);catalog.versions.push({package:pkg,version,variant,kind:input.kind,sourceSha256:hash,manifest:relative+'/manifest.json',...stats});write(path.join(out,'catalog.json'),catalog);write(path.join(work,'decompile-jobs.json'),jobs);console.log('UNPACKED',pkg,version,variant,JSON.stringify(stats));
}
const hashes=new Set(catalog.versions.map(v=>v.sourceSha256));if(hashes.size!==inputs.length)throw Error('Unexpected duplicate input');
catalog.statistics={uniqueContainers:hashes.size,sourceReferences:inputs.reduce((n,x)=>n+x.references.length,0),logicalEntries:catalog.versions.reduce((n,x)=>n+x.entries,0),casObjects:fs.readdirSync(casRoot).length};write(path.join(out,'catalog.json'),catalog);console.log(JSON.stringify(catalog.statistics));
