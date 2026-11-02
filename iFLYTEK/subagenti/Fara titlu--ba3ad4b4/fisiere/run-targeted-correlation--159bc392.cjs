'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {normalizeSmali}=require('./normalize-smali.cjs');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex'),fh=p=>hash(fs.readFileSync(p));
const planPath=path.join(__dirname,'TARGETED-CORRELATION-PLAN.json'),gatePath=path.join(__dirname,'../audit/TARGETED-CORRELATION-GATE.json'),gate=JSON.parse(fs.readFileSync(gatePath,'utf8')),plan=JSON.parse(fs.readFileSync(planPath,'utf8'));
if(gate.gate!=='G-TARGETED-CORRELATION'||gate.status!=='PASS'||gate.score!==10||fh(planPath)!==gate.planSha256)throw Error('Missing or stale targeted-correlation gate');
if(plan.inputs.length!==9||plan.targets.length!==2||plan.expectedClasses!==18||new Set(plan.inputs.map(x=>x.dexSetSha256)).size!==9)throw Error('Unexpected targeted scope');
const reference=JSON.parse(fs.readFileSync(path.join(__dirname,'reference-export-results.json'),'utf8')),refGate=JSON.parse(fs.readFileSync(path.join(__dirname,'../audit/CORRELATION-EXPORT-GATE.json'),'utf8'));
const run=path.join('D:/Codex-iflytek-decompilation-repair-20261101/correlation','targeted-'+Date.now());fs.mkdirSync(run,{recursive:true});fs.mkdirSync(path.join(run,'objects'));
const result={schemaVersion:1,gate:gate.gate,gateSha256:fh(gatePath),planSha256:fh(planPath),startedAt:new Date().toISOString(),run,scope:plan.stage,inputs:[],commands:[],comparisons:[],javaPromotionAllowed:false,status:'RUNNING'};
const sizeOf=p=>fs.readdirSync(p,{withFileTypes:true}).reduce((n,e)=>n+(e.isDirectory()?sizeOf(path.join(p,e.name)):fs.statSync(path.join(p,e.name)).size),0);
function tool(executable,args,timeoutMs,label){const started=Date.now(),r=cp.spawnSync(executable,args,{encoding:'utf8',timeout:timeoutMs,maxBuffer:8*1024**2,windowsHide:true}),log=path.join(run,label+'.log');fs.writeFileSync(log,(r.stdout||'')+(r.stderr||''));result.commands.push({executable,args,timeoutMs,label,elapsedMs:Date.now()-started,exitCode:r.status,error:r.error?.message||null,signal:r.signal||null,log,logSha256:fh(log)});if(r.error||r.status!==0||r.signal)throw Error(label+' failed');}
function compact(n){return {descriptor:n.descriptor,classSha256:n.classSha256,contextSha256:n.contextSha256,methodCount:n.methodCount,methods:n.methods.map(({normalized,...m})=>m)};}
try{
 const source=path.join(__dirname,'SmaliFingerprintExport.java'),normalizer=path.join(__dirname,'normalize-smali.cjs'),jar=reference.jar.file;
 if(reference.status!=='PASS'||fh(source)!==refGate.exporterSourceSha256||fh(normalizer)!==refGate.normalizerSha256||fh(jar)!==reference.jar.sha256)throw Error('Source/JAR/reference provenance mismatch');
 result.jar={file:jar,sha256:fh(jar)};result.exporterSourceSha256=fh(source);result.normalizerSha256=fh(normalizer);
 const classes=path.join(run,'classes');fs.mkdirSync(classes);tool('C:/Program Files/Java/jdk-21/bin/javac.exe',['-cp',jar,'-d',classes,source],60000,'compile');result.compiledExporterSha256=fh(path.join(classes,'SmaliFingerprintExport.class'));
 const descriptors=plan.targets.map(x=>x.descriptor),list=path.join(run,'descriptors.txt');fs.writeFileSync(list,descriptors.join('\n')+'\n');
 for(const p of plan.inputs){
  if(fs.statSync(p.input).size!==p.inputBytes||fh(p.input)!==p.inputSha256)throw Error('Input integrity mismatch '+p.variant);
  const r={...p,classes:[]};
  if(p.variant===plan.referenceReuse.variant){
   if(reference.input.sha256!==p.inputSha256)throw Error('Reference input mismatch');
   r.reused=true;r.referenceManifest='reference-export-results.json';r.referenceManifestSha256=fh(path.join(__dirname,'reference-export-results.json'));
   for(const descriptor of descriptors){const old=reference.classes.find(x=>x.descriptor===descriptor);if(!old||fh(old.file)!==old.smaliSha256||fs.statSync(old.file).size!==old.smaliBytes)throw Error('Existing reference mismatch');const n=normalizeSmali(fs.readFileSync(old.file,'utf8'));if(n.classSha256!==old.classSha256||n.contextSha256!==old.contextSha256)throw Error('Existing reference normalization mismatch');r.classes.push({...compact(n),file:old.file,smaliSha256:old.smaliSha256,smaliBytes:old.smaliBytes,reused:true});}
  }else{
   const output=path.join(run,p.dexSetSha256+'.ndjson');tool('C:/Program Files/Java/jdk-21/bin/java.exe',['-Xmx512m','-cp',classes+path.delimiter+jar,'SmaliFingerprintExport',p.input,output,'@'+list],plan.limits.maxWallMsPerInput,p.dexSetSha256.slice(0,12));
   const rows=fs.readFileSync(output,'utf8').trim().split(/\r?\n/).map(x=>JSON.parse(x)),s=rows.filter(x=>x.type==='summary'),all=rows.filter(x=>x.type==='class');
   if(s.length!==1||rows.at(-1)!==s[0]||!s[0].complete||s[0].classes!==2||s[0].inputSha256!==p.inputSha256||all.length!==2||new Set(all.map(x=>x.descriptor)).size!==2||all.some(x=>!descriptors.includes(x.descriptor)||x.validationErrors!==false))throw Error('Incomplete export '+p.variant);
   r.reused=false;r.export={file:output,sha256:fh(output),summary:s[0]};
   for(const c of all){const b=Buffer.from(c.smaliBase64,'base64');if(b.length!==c.smaliBytes||hash(b)!==c.smaliSha256)throw Error('Smali integrity mismatch');const n=normalizeSmali(b.toString('utf8'));if(n.descriptor!==c.descriptor)throw Error('Descriptor mismatch');const file=path.join(run,'objects',c.smaliSha256+'.smali');if(!fs.existsSync(file))fs.writeFileSync(file,b);else if(fh(file)!==c.smaliSha256)throw Error('Existing object corrupted');r.classes.push({...compact(n),file,smaliSha256:c.smaliSha256,smaliBytes:c.smaliBytes,dexEntry:c.dexEntry});}
  }
  result.inputs.push(r);if(sizeOf(run)>plan.limits.maxOutputBytesTotal)throw Error('Total disk budget exceeded');console.log('EXPORTED',p.variant,r.classes.length,r.reused?'reused':'new');
 }
 const base=result.inputs.find(x=>x.variant===plan.referenceReuse.variant);if(!base)throw Error('Reference group missing');
 for(const input of result.inputs)for(const target of plan.targets){const a=base.classes.find(x=>x.descriptor===target.descriptor),b=input.classes.find(x=>x.descriptor===target.descriptor);if(!a||!b)throw Error('Missing target class');for(const expected of target.targetMethods){const am=a.methods.find(x=>x.[CREDENTIAL_REDACTED]>x.[CREDENTIAL_REDACTED] classEqual=a.classSha256===b.classSha256,contextEqual=a.contextSha256===b.contextSha256,methodEqual=!!am&&!!bm&&am.sha256===bm.sha256;result.comparisons.push({referenceVariant:base.variant,targetVariant:input.variant,dexSetSha256:input.dexSetSha256,descriptor:target.descriptor,methodSignature:expected.signature,sameInput:input.variant===base.variant,classEqual,contextEqual,methodPresent:!!bm,methodEqual,reference:{classSha256:a.classSha256,contextSha256:a.contextSha256,methodSha256:am?.sha256,file:a.file},target:{classSha256:b.classSha256,contextSha256:b.contextSha256,methodSha256:bm?.sha256||null,file:b.file},classification:classEqual&&methodEqual?'identical-normalized-class-and-method-candidate':methodEqual?'method-equal-class-different-comparison-only':!bm?'target-method-absent-comparison-only':'method-different-comparison-only',javaPromotionAllowed:false});}}
 const nonSelf=result.comparisons.filter(x=>!x.sameInput);result.summary={logicalInputs:result.inputs.length,logicalClasses:result.inputs.reduce((n,x)=>n+x.classes.length,0),reusedClasses:result.inputs.filter(x=>x.reused).reduce((n,x)=>n+x.classes.length,0),newExports:result.inputs.filter(x=>!x.reused).reduce((n,x)=>n+x.classes.length,0),uniqueNewSmaliObjects:fs.readdirSync(path.join(run,'objects')).length,nonSelfComparisons:nonSelf.length,classAndMethodCandidates:nonSelf.filter(x=>x.classEqual&&x.methodEqual).length,methodEqualClassDifferent:nonSelf.filter(x=>!x.classEqual&&x.methodEqual).length,methodDifferent:nonSelf.filter(x=>!x.methodEqual).length,javaPatches:0};
 result.outputBytes=sizeOf(run);result.status='PASS';
}catch(e){result.status='FAIL';result.error=e.stack;process.exitCode=1;}
result.finishedAt=new Date().toISOString();fs.writeFileSync(path.join(__dirname,'targeted-correlation-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,summary:result.summary,error:result.error}));
