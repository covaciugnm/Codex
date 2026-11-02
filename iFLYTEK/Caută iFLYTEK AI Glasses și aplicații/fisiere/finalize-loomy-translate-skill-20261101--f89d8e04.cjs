'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {zipEntries}=require('./inspect-android-archive.cjs');
const {out,records,known,save}=require('./collect-loomy-translate-skill-20261101.cjs');
const repo=path.resolve(__dirname,'..'),rel='loomy-translate-skill-2026-11-01',release='iflytek-loomy-skills-2026-11-01';
const previousFiles=fs.existsSync(path.join(out,'file-inventory.json'))?new Map(JSON.parse(fs.readFileSync(path.join(out,'file-inventory.json'),'utf8')).map(r=>[r.file,r.sha256])):new Map();
const previousArchives=fs.existsSync(path.join(out,'archive-entries.json'))?new Map(JSON.parse(fs.readFileSync(path.join(out,'archive-entries.json'),'utf8')).map(r=>[r.file,r])):new Map();
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const table=Uint32Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
function crc(b){let n=0xffffffff;for(let i=0;i<b.length;i++)n=table[(n^b[i])&255]^(n>>>8);return(n^0xffffffff)>>>0;}
function checkZip(b){const es=zipEntries(b);let p=b.length-22;while(p>=0&&b.readUInt32LE(p)!==0x06054b50)p--;if(p<0)throw Error('Missing ZIP directory');p=b.readUInt32LE(p+16);const names=new Set(),items=[];for(const e of es){const expected=b.readUInt32LE(p+16);p+=46+b.readUInt16LE(p+28)+b.readUInt16LE(p+30)+b.readUInt16LE(p+32);if(names.has(e.name))throw Error('Repeated ZIP name '+e.name);names.add(e.name);const data=e.read();if(crc(data)!==expected)throw Error('CRC mismatch '+e.name);items.push({name:e.name,bytes:data.length,sha256:sha(data),crc32:expected,...(e.name.endsWith('.apk')?{nestedApk:checkZip(data)}:{})});}return{entries:items.length,uncompressedBytes:items.reduce((n,e)=>n+e.bytes,0),items};}
const old='other-hardware/HeyCyan-latest.xapk',renamed='other-hardware/HeyCyan-1.0.173_20261017.xapk';
for(const r of records)if(r.file===old){if(fs.existsSync(path.join(out,old)))fs.renameSync(path.join(out,old),path.join(out,renamed));r.file=renamed;}
for(const r of records){
 if(r.status==='already-in-github'&&r.existing?.path?.startsWith(rel+'/'))r.status='reused-in-collection';
 if(r.bytes===0&&r.statusCode===200){r.status='empty-response';r.note='Empty HTTP response; not a usable login document.';delete r.existing;}
 if(r.file?.startsWith('extracted/')){r.status='contained-in-new-archive';r.storage='zip-entry';r.archiveFile='skills/transaas01-1.0.4.zip';r.entry=r.file.slice('extracted/transaas01-1.0.4/'.length);}
}
const archives=[],files=[],seen=new Set();
for(const r of records.filter(r=>r.status==='downloaded'&&r.file)){
 const p=path.join(out,r.file),b=fs.readFileSync(p);if(b.length!==r.bytes||sha(b)!==r.sha256)throw Error('Artifact hash mismatch '+r.file);if(seen.has(r.sha256))throw Error('Unclassified duplicate artifact');seen.add(r.sha256);
 const pointer=known.get(r.sha256);if(pointer?.inventory)throw Error('Artifact already indexed in GitHub '+r.file);
 if(r.file.startsWith('cli/')){const magic=b.subarray(0,4).toString('hex');if(!['4d5a9000','cffaedfe','7f454c46'].includes(magic))throw Error('Unexpected CLI format');r.formatVerified=true;}
 if(/\.(zip|xapk)$/.test(r.file)){const cached=previousArchives.get(r.file),canReuse=r.zipCrcVerified&&previousFiles.get(r.file)===r.sha256&&cached&&cached.entries===cached.items?.length;const a=canReuse?cached:checkZip(b);r.zipCrcVerified=true;archives.push({...a,file:r.file,sha256:r.sha256});}
 r.storage=r.file.startsWith('cli/')||b.length>25000000?'release':'git';if(r.storage==='release'){r.release=release;r.asset=path.basename(r.file);r.downloadUrl='https://github.com/covaciugnm/iFLYTEK/releases/download/'+release+'/'+r.asset;}
 files.push({file:r.file,bytes:r.bytes,sha256:r.sha256,storage:r.storage,source:r.url,...(r.downloadUrl?{downloadUrl:r.downloadUrl,asset:r.asset,release:r.release}:{})});
}
for(const r of records)if(r.status==='reused-in-collection'){const target=files.find(x=>x.sha256===r.sha256);if(!target)throw Error('Unresolved collection duplicate '+r.url);r.existing={inventory:rel+'/file-inventory.json',path:rel+'/'+target.file,storage:target.storage,asset:target.asset,release:target.release,downloadUrl:target.downloadUrl};}
save();fs.writeFileSync(path.join(out,'file-inventory.json'),JSON.stringify(files,null,2)+'\n');fs.writeFileSync(path.join(out,'archive-entries.json'),JSON.stringify(archives,null,2)+'\n');
fs.writeFileSync(path.join(out,'.gitignore'),'extracted/\ncli/\nother-hardware/*.xapk\nskills/beautiful-html-1.0.0.zip\n');
const catalog=JSON.parse(fs.readFileSync(path.join(out,'sources/loomy-skill-catalog.json'),'utf8'));
const summary={catalogSkills:catalog.data.items.length,downloadedSkillArchives:files.filter(r=>r.file.startsWith('skills/')).length,cliBinaries:files.filter(r=>r.file.startsWith('cli/')).length,releaseAssets:files.filter(r=>r.storage==='release').length,downloadedArtifacts:files.length,totalBytes:files.reduce((n,r)=>n+r.bytes,0),httpsCliCrosschecks:records.filter(r=>r.category==='official-transaas-HTTPS-crosscheck'&&r.status==='reused-in-collection').length};
fs.writeFileSync(path.join(out,'verification-summary.json'),JSON.stringify(summary,null,2)+'\n');console.log(summary);
