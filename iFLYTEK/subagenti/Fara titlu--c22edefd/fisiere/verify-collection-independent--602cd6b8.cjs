'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {zipEntries}=require('../../tools/inspect-android-archive.cjs');
const out=path.resolve(__dirname,'..'),repo=path.resolve(out,'..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const inventory=read(path.join(out,'file-inventory.json')),manifest=read(path.join(out,'manifest.json')),catalog=read(path.join(out,'sources/loomy-skill-catalog.json')),archives=read(path.join(out,'archive-entries.json'));
const previous=new Set();for(const [file,select] of [['iflytek-manifest-sha256.json',x=>x.files],['collection-2026-11-01/manifest.json',x=>x.records],['retailer-audit-2026-11-01/file-inventory.json',x=>x],['apk-analysis-2026-11-01/cas-index.json',x=>x.objects],['apk-analysis-2026-11-01/baseline-release-index.json',x=>Object.keys(x).map(sha256=>({sha256}))]])for(const r of select(read(path.join(repo,file))))if(r.sha256)previous.add(r.sha256);
const crcTable=Array.from({length:256},(_,n)=>{let c=n;for(let j=0;j<8;j++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0;});
function crc(b){let c=0xffffffff;for(const n of b)c=crcTable[(c^n)&255]^(c>>>8);return(c^0xffffffff)>>>0;}
let nestedCount=0,zipFiles=0;const payloads=new Map(),seen=new Set();let total=0;
function checkArchive(b,record){
 const es=zipEntries(b);let end=b.length-22;while(end>=0&&b.readUInt32LE(end)!==0x06054b50)end--;if(end<0)throw Error('Missing ZIP footer');let offset=b.readUInt32LE(end+16);if(es.length!==record.entries||record.items.length!==record.entries)throw Error('Archive entry count mismatch '+(record.file||'nested APK'));const expected=new Map(record.items.map(r=>[r.name,r]));let bytes=0;
 for(const e of es){const centralCRC=b.readUInt32LE(offset+16);offset+=46+b.readUInt16LE(offset+28)+b.readUInt16LE(offset+30)+b.readUInt16LE(offset+32);
  const data=e.read(),r=expected.get(e.name);if(!r||data.length!==r.bytes||sha(data)!==r.sha256||crc(data)!==centralCRC||centralCRC!==r.crc32)throw Error('Archive member mismatch '+e.name);expected.delete(e.name);bytes+=data.length;if(!e.name.endsWith('/'))zipFiles++;
  if(e.name.endsWith('.apk')){if(!r.nestedApk)throw Error('Missing nested APK evidence');checkArchive(data,r.nestedApk);nestedCount++;}
 }
 if(expected.size||bytes!==record.uncompressedBytes)throw Error('Incomplete ZIP inventory');
}
for(const r of inventory){const file=path.resolve(out,r.file);if(!file.startsWith(out+path.sep))throw Error('Unsafe inventory path');const b=fs.readFileSync(file);if(b.length!==r.bytes||sha(b)!==r.sha256)throw Error('Artifact integrity '+r.file);if(seen.has(r.sha256)||previous.has(r.sha256))throw Error('Duplicate artifact '+r.file);seen.add(r.sha256);total+=b.length;
 if(/\.(zip|xapk)$/.test(r.file)){const a=archives.find(x=>x.file===r.file);if(!a||a.sha256!==r.sha256)throw Error('Missing archive index');checkArchive(b,a);}
 if(r.file.startsWith('cli/'))payloads.set(r.file,b);
 if(r.file.endsWith('.pdf')&&b.subarray(0,5).toString()!=='%PDF-')throw Error('Invalid PDF');
}
const ids=new Set(),covered=[];for(const item of catalog.data.items){if(ids.has(item.skill_id))throw Error('Duplicate skill ID');ids.add(item.skill_id);const r=manifest.records.find(r=>r.url===item.download_url&&r.status!=='unavailable');if(!r)throw Error('Missing catalog skill '+item.skill_id);const f=inventory.find(f=>f.sha256===r.sha256);if(!f)throw Error('Catalog artifact missing');const a=archives.find(x=>x.file===f.file);if(!a?.items.some(e=>/(^|\/)SKILL\.md$/i.test(e.name)))throw Error('Skill missing metadata');covered.push({id:item.skill_id,version:item.latest_version,file:f.file,sha256:f.sha256});}
if(ids.size!==catalog.data.total||ids.size!==67)throw Error('Catalog count mismatch');
const historical=inventory.find(r=>r.file==='skills/transaas01-1.0.3.zip');if(!historical)throw Error('Missing historical skill');
const cli=[];for(const [name,b] of payloads){const magic=b.subarray(0,4).toString('hex');if(name.endsWith('.exe')){if(b.subarray(0,2).toString()!=='MZ'||b.readUInt16LE(b.readUInt32LE(60)+4)!==0x8664)throw Error('Wrong PE architecture');}else if(name.includes('linux')){if(magic!=='7f454c46'||b[4]!==2||b.readUInt16LE(18)!==62)throw Error('Wrong ELF architecture');}else {if(magic!=='cffaedfe'||b.readUInt32LE(4)!==(name.includes('arm64')?0x100000c:0x1000007))throw Error('Wrong Mach-O architecture');}
 const http=manifest.records.find(r=>r.file===name&&r.url.startsWith('http:')),https=manifest.records.find(r=>r.url===http?.url.replace('http:','https:'));if(!http||https?.sha256!==sha(b))throw Error('HTTP/HTTPS mismatch');
 const text=b.toString('latin1');if(!text.includes('go1.26.3')||!text.includes('8bc446660123751dae0f45a24fd99d8ded0eeb1a')||!text.includes('vcs.modified=true'))throw Error('Missing static Go metadata');cli.push({file:name,magic,sha256:sha(b),httpsVerifiedByRecordedHash:true});
}
const result={checkedAt:new Date().toISOString(),status:'PASS',uniqueArtifacts:seen.size,totalBytes:total,priorArtifactDuplicates:0,catalogSkills:ids.size,historicalSkills:1,topLevelArchives:archives.length,nestedApkArchives:nestedCount,zipMemberFilesIndependentlyVerified:zipFiles,pdfFiles:inventory.filter(r=>r.file.endsWith('.pdf')).length,cli,skills:covered};
fs.writeFileSync(path.join(__dirname,'collection-integrity-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,skills:undefined},null,2));
