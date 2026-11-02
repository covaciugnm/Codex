'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),{spawnSync}=require('node:child_process');
const out=path.resolve(__dirname,'..'),repo=path.resolve(out,'..'),work=path.join(out,'.work'),local='D:/Codex-iflytek-apk-analysis-20261101',cache=path.join(local,'audit-existing-cache'),destination=path.join(local,'audit-materialized-sample-windows-safe-v1');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const bavvo=read(path.join(out,'versions/com.iflytek.bavvo/1.0.1222/bavvo-1.0.1222/manifest.json')),loomy=read(path.join(out,'versions/com.iflytek.loomy.mobile/0.0.8/Loomy-Android/manifest.json')),index=read(path.join(out,'baseline-release-index.json'));
const selected=[{...bavvo.entries.find(r=>r.storage==='cas'),component:'sample.apk',path:'new-object.bin'},{...loomy.entries.find(r=>r.storage==='existing'&&r.existing.storage==='git'),component:'sample.apk',path:'existing-git.bin'}];
const [hash,entry]=Object.entries(index).find(([,r])=>r.entry==='apktool.yml');selected.push({component:'sample.apk',path:'existing-release-zip.bin',sha256:hash,bytes:entry.bytes,storage:'existing',existing:entry});
const cacheFolder=path.join(cache,entry.release);fs.mkdirSync(cacheFolder,{recursive:true});const cached=path.join(cacheFolder,entry.asset);if(!fs.existsSync(cached))fs.copyFileSync(path.join(work,'baseline-release',entry.asset),cached);
// Warm exactly the small Git blob required by this fixture; materializer itself is tested local-only.
const git=spawnSync('git',['show','HEAD:'+selected[1].existing.path],{cwd:repo,encoding:null,maxBuffer:1024*1024,windowsHide:true});if(git.status!==0||sha(git.stdout)!==selected[1].sha256)throw Error('Cannot obtain fixture Git blob');
const fixture={schemaVersion:1,package:'audit.fixture',version:'1',variant:'representative-storage-sample',source:{note:'Audit fixture; sample objects from real version manifests, not an additional application'},entries:selected,outerEntries:[],decompilation:{components:[]}};
fs.writeFileSync(path.join(work,'audit-materialize-manifest.json'),JSON.stringify(fixture,null,2));
const tool=path.join(repo,'tools/materialize-apk-version-20261101.cjs'),args=[tool,'--manifest','.work/audit-materialize-manifest.json','--store-dir',local,'--cache-dir',cache,'--output',destination,'--local-only'];
const run=()=>spawnSync(process.execPath,args,{cwd:repo,encoding:'utf8',windowsHide:true,maxBuffer:1024*1024});
const corruptionTarget=path.join(destination,'raw/sample.apk/new-object.bin'),originalSample=fs.readFileSync(path.join(local,'cas',selected[0].sha256));
if(fs.existsSync(corruptionTarget))fs.writeFileSync(corruptionTarget,originalSample);
let r=run();if(r.status!==0)throw Error(r.stderr||r.stdout);const output=JSON.parse(r.stdout);for(const object of selected){const b=fs.readFileSync(path.join(destination,'raw/sample.apk',object.path));if(sha(b)!==object.sha256||b.length!==object.bytes)throw Error('Materialized mismatch');}
r=run();if(r.status!==0)throw Error('Idempotent materialization failed '+r.stderr);
fs.writeFileSync(corruptionTarget,Buffer.from('intentional audit corruption'));r=run();if(r.status===0)throw Error('Corrupted existing output accepted');fs.writeFileSync(corruptionTarget,originalSample);
const result={checkedAt:new Date().toISOString(),status:'PASS',sampleFiles:selected.length,storageCases:['CAS','existing Git blob','existing Release ZIP entry'],idempotentRerun:true,corruptedOutputRejected:true,outputSummary:output,limits:'Representative storage-resolution fixture; all 14 complete raw manifests were independently verified separately. This is not a full 14-version filesystem materialization.'};
fs.writeFileSync(path.join(__dirname,'materialization-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
