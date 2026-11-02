'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..'),out=path.join(root,'apk-analysis-2026-11-01'),work=process.env.IFLYTEK_APK_WORK_ROOT||path.join(out,'.work'),casRoot=process.env.IFLYTEK_APK_CAS_ROOT||path.join(out,'cas');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const baseline=read(path.join(root,'iflytek-manifest-sha256.json')).files,known=new Map(baseline.map(r=>[r.sha256,{path:r.path,storage:r.storage,asset:r.asset,release:r.storage==='release'?'iflytek-documentation-2026-10-31':undefined}]));
function object(b){const h=sha(b),existing=known.get(h);if(existing)return{sha256:h,bytes:b.length,storage:'existing',existing};const cas='cas/'+h,p=path.join(casRoot,h);if(!fs.existsSync(p))fs.writeFileSync(p,b);return{sha256:h,bytes:b.length,storage:'cas',cas};}
function canReuseReport(file,dexSetSha256){
 if(process.argv.includes('--force')||!fs.existsSync(file))return false;
 try{const r=read(file);if(r.dexSetSha256!==dexSetSha256||!['decompiled','partial-decompilation'].includes(r.status)||!r.javaFiles||!Array.isArray(r.entries)||!Array.isArray(r.logs)||r.logs.length===0||r.entries.filter(e=>typeof e.path==='string'&&e.path.endsWith('.java')).length!==r.javaFiles)return false;
 for(const e of [...r.entries,...r.logs])if(typeof e.path!=='string'||!/^[a-f0-9]{64}$/.test(e.sha256)||!Number.isSafeInteger(e.bytes)||e.bytes<0||!['cas','existing'].includes(e.storage)||(e.storage==='existing'&&(!e.existing||!e.existing.storage)))return false;
 const checked=new Set();for(const entry of [...r.entries,...r.logs])if(entry.storage==='cas'&&!checked.has(entry.sha256)){if(!/^[a-f0-9]{64}$/.test(entry.sha256))return false;checked.add(entry.sha256);const p=path.join(casRoot,entry.sha256);if(!fs.existsSync(p))return false;const b=fs.readFileSync(p);if(b.length!==entry.bytes||sha(b)!==entry.sha256)return false;}return true;}catch{return false;}
}
const prefix='iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Reconstituit_2026-10-30/';
function enumerate(p,relative=''){const result=[];for(const e of fs.readdirSync(p,{withFileTypes:true})){const r=relative?relative+'/'+e.name:e.name;const q=path.join(p,e.name);if(e.isDirectory())result.push(...enumerate(q,r));else result.push({path:r,...object(fs.readFileSync(q))});}return result;}
async function main(){
 const catalog=read(path.join(out,'catalog.json')),jobs=read(path.join(work,'decompile-jobs.json'));
 const official=catalog.versions.find(v=>v.sourceSha256==='73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2');if(!official)throw Error('Baseline official APK missing');
 const baselineDex=read(path.join(out,official.manifest)).components[0].dexSetSha256,groups=new Map();for(const j of jobs){if(!groups.has(j.dexSetSha256))groups.set(j.dexSetSha256,[]);groups.get(j.dexSetSha256).push(j);}
 for(const [dexHash,list] of groups){
  const rel='decompilation/'+dexHash+'/manifest.json',dest=path.join(out,rel);let report;
  if(dexHash===baselineDex){
   const files=baseline.filter(r=>r.path.startsWith(prefix+'reconstituit/jadx/app/src/main/java/')||(r.path.startsWith(prefix+'reconstituit/jadx/')&&/\/(?:build\.gradle|settings\.gradle|gradle\.properties)$/.test(r.path)));
   report={schemaVersion:1,dexSetSha256:dexHash,status:'reused-existing-partial-decompilation',tool:'JADX 1.5.6 baseline',exitCode:3,knownJadxErrors:301,originalSource:false,notes:['Existing baseline decompilation retained with its limitations; raw DEX is independently mapped in each version. Flutter native Dart AOT is not reconstructed as original Dart source.'],entries:files.map(r=>({path:r.path.slice(prefix.length),sha256:r.sha256,bytes:r.bytes,storage:'existing',existing:{path:r.path,storage:r.storage,asset:r.asset}})),logs:baseline.filter(r=>r.path.startsWith(prefix+'inventar/')&&/jadx/.test(r.path)).map(r=>({path:r.path,sha256:r.sha256,bytes:r.bytes,storage:'existing',existing:{path:r.path,storage:r.storage,asset:r.asset}}))};
  }else if(canReuseReport(dest,dexHash)){report=read(dest);console.log('REUSE JOB',dexHash,report.status);
  }else{
   const job=list[0],target=path.join(work,'jadx-output',dexHash),tmp=path.join(work,'java-temp');fs.mkdirSync(target,{recursive:true});fs.mkdirSync(tmp,{recursive:true});
   const java=process.env.IFLYTEK_JAVA||'C:/Program Files/Java/jdk-21/bin/java.exe',jar=path.join(work,'jadx/lib/jadx-1.5.6-all.jar');
   const args=['-Xmx4g','-Djava.io.tmpdir='+tmp,'-cp',jar,'jadx.cli.JadxCLI','--config','none','--no-res','--show-bad-code','-j','2','-d',target,job.input];
   const startedAt=new Date().toISOString(),log=path.join(work,'jadx-'+dexHash+'.log');console.log('JADX START',dexHash,job.input);const fd=fs.openSync(log,'w');
   const code=await new Promise((resolve,reject)=>{const child=cp.spawn(java,args,{stdio:['ignore',fd,fd],windowsHide:true,env:{...process.env,JADX_CACHE_DIR:path.join(work,'jadx-cache'),JADX_CONFIG_DIR:path.join(work,'jadx-config'),JADX_TMP_DIR:tmp}});child.on('error',reject);child.on('close',resolve);});fs.closeSync(fd);
   const entries=enumerate(target),javaFiles=entries.filter(r=>r.path.endsWith('.java')).length;
   report={schemaVersion:1,dexSetSha256:dexHash,status:code===0?'decompiled':'partial-decompilation',tool:'JADX 1.5.6',toolSha256:sha(fs.readFileSync(jar)),toolArchiveSha256:sha(fs.readFileSync(path.join(work,'jadx-1.5.6.zip'))),java:'Java 21.0.6',exitCode:code,startedAt,finishedAt:new Date().toISOString(),originalSource:false,command:{executable:java,args:args.map(a=>a.replace(work,'${WORK}'))},notes:['Static DEX decompilation only. Original project, comments and names may be absent or inaccurate. Resources and native libraries are preserved in raw version manifests; --no-res avoids a second resource copy. Flutter Dart AOT is not original Dart source. Nonzero exit codes and unsupported methods remain visible.'],javaFiles,entries,logs:[{path:'jadx.log',...object(fs.readFileSync(log))}]};
   if(javaFiles===0)report.status='failed-no-java-output';
   console.log('JADX DONE',dexHash,'exit',code,'javaFiles',javaFiles);
  }
  write(dest,report);
  for(const j of list){const p=path.join(out,j.manifest),m=read(p);m.decompilation.components=m.decompilation.components||[];m.decompilation.components=m.decompilation.components.filter(c=>c.component!==j.component);m.decompilation.components.push({component:j.component,dexSetSha256:dexHash,manifest:rel,status:report.status});m.decompilation.status='complete-with-documented-limitations';write(p,m);}
 }
 for(const v of catalog.versions){const p=path.join(out,v.manifest),m=read(p);if(!m.components.some(c=>c.dex.length)){m.decompilation={status:'not-applicable-no-dex'};write(p,m);}v.decompilationStatus=m.decompilation.status;}
 catalog.decompilation={uniqueDexSets:groups.size,baselineDexSet:baselineDex,completedAt:new Date().toISOString()};write(path.join(out,'catalog.json'),catalog);
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={canReuseReport};
