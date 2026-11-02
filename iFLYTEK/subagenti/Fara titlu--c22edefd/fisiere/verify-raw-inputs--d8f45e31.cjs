'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {zipEntries}=require('../../tools/inspect-android-archive.cjs');
const repo=path.resolve(__dirname,'../..'),out=path.resolve(__dirname,'..');
const inputRoot=process.env.IFLYTEK_AUDIT_INPUT_ROOT||'D:/Codex-iflytek-apk-analysis-20261101/inputs';
const casRoot=process.env.IFLYTEK_AUDIT_CAS_ROOT||'D:/Codex-iflytek-apk-analysis-20261101/cas';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const catalog=read(path.join(out,'catalog.json')),old=read(path.join(repo,'iflytek-manifest-sha256.json')).files,recent=read(path.join(repo,'collection-2026-11-01/manifest.json')).records;
const releases=read(path.join(__dirname,'release-inputs.json')).releases;
const expected=new Map(old.filter(r=>/\.(apk|xapk)$/i.test(r.path)).map(r=>[r.sha256,r.bytes]));
for(const r of recent.filter(r=>r.file&&/\.(apk|xapk)$/i.test(r.file)))expected.set(r.sha256,r.bytes);
for(const release of releases)for(const r of release.assets.filter(r=>/\.(apk|xapk)$/i.test(r.name)))expected.set(r.digest.replace('sha256:',''),r.size);
const known=new Map(old.map(r=>[r.sha256,r.bytes]));for(const r of recent)if(r.sha256)known.set(r.sha256,r.bytes);
const buildIndexPath=path.join(out,'baseline-release-index.json');if(fs.existsSync(buildIndexPath))for(const [h,r] of Object.entries(read(buildIndexPath)))known.set(h,r.bytes);
const files=fs.readdirSync(inputRoot),seen=new Set(),casChecked=new Set(),results=[];let logical=0;
for(const v of catalog.versions){
 const m=read(path.join(out,v.manifest));if(seen.has(m.source.sha256))throw Error('Duplicate input manifest');seen.add(m.source.sha256);
 const name=files.find(name=>name===m.variant+'.apk'||name===m.variant+'.xapk'||m.source.references.some(r=>r.asset===name));if(!name)throw Error('Missing input '+m.variant);
 const b=fs.readFileSync(path.join(inputRoot,name));if(sha(b)!==m.source.sha256||b.length!==m.source.bytes||expected.get(m.source.sha256)!==b.length)throw Error('Container mismatch '+name);
 const outer=zipEntries(b),outerMap=new Map(outer.map(e=>[e.name,e]));let count=0;
 for(const c of m.components){
  const cb=m.source.format==='XAPK'?outerMap.get(c.name).read():b;if(sha(cb)!==c.sha256||cb.length!==c.bytes)throw Error('Component mismatch');
  const es=zipEntries(cb).filter(e=>!e.name.endsWith('/')),mapped=m.entries.filter(r=>r.component===c.name);if(es.length!==c.entries||es.length!==mapped.length)throw Error('Component entry count mismatch');
  const em=new Map(mapped.map(r=>[r.path,r]));if(em.size!==mapped.length)throw Error('Duplicate logical file');
  for(const e of es){const data=e.read(),r=em.get(e.name);if(!r||r.sha256!==sha(data)||r.bytes!==data.length)throw Error('Logical entry mismatch '+name+':'+e.name);
   if(r.storage==='cas'&&!casChecked.has(r.sha256)){const object=fs.readFileSync(path.join(casRoot,r.sha256));if(sha(object)!==r.sha256||object.length!==r.bytes)throw Error('CAS mismatch '+r.sha256);casChecked.add(r.sha256);}
   else if(r.storage==='existing'&&known.get(r.sha256)!==r.bytes)throw Error('Unknown baseline reference '+r.sha256);
   count++;
  }
 }
 for(const r of m.outerEntries){const data=outerMap.get(r.path).read();if(sha(data)!==r.sha256||data.length!==r.bytes)throw Error('Outer entry mismatch');}
 if(count!==m.statistics.entries||count!==v.entries)throw Error('Version count mismatch');logical+=count;results.push({package:m.package,version:m.version,variant:m.variant,kind:m.kind,sha256:m.source.sha256,componentCount:m.components.length,verifiedLogicalFiles:count,status:'PASS'});
}
if(seen.size!==expected.size||[...expected.keys()].some(h=>!seen.has(h)))throw Error('Incomplete input coverage');
const result={checkedAt:new Date().toISOString(),expectedUniqueContainers:expected.size,verifiedUniqueContainers:seen.size,verifiedLogicalFiles:logical,verifiedNewCASObjects:casChecked.size,versions:results,status:'PASS',limits:'Raw inputs and extracted bytes checked; decompilation and final CAS remap/pack/materialization audited separately.'};
fs.writeFileSync(path.join(__dirname,'raw-input-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
