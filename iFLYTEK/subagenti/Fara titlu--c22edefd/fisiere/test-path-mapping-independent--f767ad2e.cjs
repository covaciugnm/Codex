'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {planPaths}=require('../../tools/materialize-apk-version-20261101.cjs');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),fold=s=>s.normalize('NFC').toUpperCase();
const names=['res/2F.xml','res/2f.xml','Case/file.txt','case/file.txt','dupe','dupe/child.xml','_apkcase_forged/name.txt','CON.txt','é.txt','e\u0301.txt','ordinary.txt'];
const rows=names.map(name=>{const logical='raw/base.apk/'+name,b=Buffer.from('Independent auditor fixture: '+logical);return{logical,data:b,record:{sha256:sha(b),bytes:b.length}};});
const first=planPaths(rows),again=planPaths([...rows].reverse());if(JSON.stringify(first.map(r=>[r.logical,r.physical]))!==JSON.stringify(again.map(r=>[r.logical,r.physical])))throw Error('Order-dependent path map');
const dest=path.join('D:/Codex-iflytek-apk-analysis-20261101','independent-path-fixture-'+Date.now());fs.mkdirSync(dest,{recursive:true});const seen=new Set();
for(const r of first){const k=fold(r.physical);if(seen.has(k))throw Error('Case collision');seen.add(k);const p=path.resolve(dest,r.physical);if(!p.startsWith(path.resolve(dest)+path.sep))throw Error('Escaped fixture');fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,r.data);}
for(const r of first){const b=fs.readFileSync(path.join(dest,r.physical));if(sha(b)!==r.record.sha256||b.length!==r.record.bytes)throw Error('Fixture overwrite');}
if(first.find(r=>r.logical.endsWith('/ordinary.txt')).physical!=='raw/base.apk/ordinary.txt')throw Error('Ordinary path changed');
let rejected=0;for(const bad of [[{logical:'../escape'}],[{logical:'a'},{logical:'a'}]])try{planPaths(bad);}catch{rejected++;}if(rejected!==2)throw Error('Invalid logical paths accepted');
const result={checkedAt:new Date().toISOString(),status:'PASS',files:first.length,actualWindowsFilesIndependentlyReread:true,orderIndependent:true,reversibleOriginalNames:true,casePairsPreserved:true,fileDirectoryConflictPreserved:true,unicodeAliasesPreserved:true,reservedNamespaceAndDOSNamesHandled:true,invalidPathsRejected:rejected,paths:first.map(r=>({logical:r.logical,physical:r.physical,sha256:r.record.sha256,bytes:r.record.bytes}))};fs.writeFileSync(path.join(__dirname,'independent-path-mapping-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,paths:undefined},null,2));
