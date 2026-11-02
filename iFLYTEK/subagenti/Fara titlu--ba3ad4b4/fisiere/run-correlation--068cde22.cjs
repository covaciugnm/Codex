'use strict';
// This approved preflight runner deliberately supports only the one-class smoke.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {normalizeSmali}=require('./normalize-smali.cjs');
const repo=path.resolve(__dirname,'../..'),oldWork='D:/Codex-iflytek-apk-analysis-20261101',work='D:/Codex-iflytek-decompilation-repair-20261101/correlation';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex'),fileHash=p=>hash(fs.readFileSync(p));
if(process.argv.length!==3||process.argv[2]!=='--smoke')throw Error('Only explicitly approved --smoke is supported; no bulk export or Java patching');
const run=path.join(work,'smoke-'+Date.now());fs.mkdirSync(run,{recursive:true});
const evidence={schemaVersion:1,date:new Date().toISOString(),gate:'G-CORRELATION-PREFLIGHT',scope:'One-class static API smoke; no bulk export, no donor Java, no APK execution',run,limits:{compileTimeoutMs:60000,smokeTimeoutMs:60000,jvmHeap:'512m',threads:1,outputLimitBytes:5*1024**3},commands:[],status:'RUNNING'};
function runTool(executable,args,timeoutMs,label){const start=Date.now();const r=cp.spawnSync(executable,args,{encoding:'utf8',timeout:timeoutMs,maxBuffer:8*1024**2,windowsHide:true});const log=path.join(run,label+'.log');fs.writeFileSync(log,(r.stdout||'')+(r.stderr||''));const record={label,executable,args,timeoutMs,elapsedMs:Date.now()-start,exitCode:r.status,error:r.error?.message||null,signal:r.signal||null,log,logSha256:fileHash(log)};evidence.commands.push(record);if(r.error||r.status!==0||r.signal)throw Error(label+' failed: '+(r.error?.message||r.status));return r;}
try{
 const input=path.join(oldWork,'components/1ecd3388f4749f4863fc1731adfce27e6530d7d842d548c83bf36dda1fb2d939.apk'),jar=path.join(oldWork,'jadx/lib/jadx-1.5.6-all.jar');
 const expectedInput='1ecd3388f4749f4863fc1731adfce27e6530d7d842d548c83bf36dda1fb2d939',expectedJar='fe3e12c45acf75f92369685fd02d1d7a7323385dc725680a9b98a0dac0ea554b';
 evidence.input={file:input,bytes:fs.statSync(input).size,sha256:fileHash(input),expectedSha256:expectedInput};evidence.jar={file:jar,bytes:fs.statSync(jar).size,sha256:fileHash(jar),expectedSha256:expectedJar};
 if(evidence.input.sha256!==expectedInput||evidence.jar.sha256!==expectedJar)throw Error('Input or JAR SHA mismatch');
 const fixtures=JSON.parse(fs.readFileSync(path.join(__dirname,'fixture-results.json'),'utf8'));
 if(fixtures.failed!==0||fixtures.passed<22||fixtures.implementationSha256!==fileHash(path.join(__dirname,'normalize-smali.cjs'))||fixtures.testSha256!==fileHash(path.join(__dirname,'test-normalize-smali.cjs')))throw Error('Fixtures missing, failed or stale');evidence.fixtures={cases:fixtures.cases,passed:fixtures.passed,sha256:fileHash(path.join(__dirname,'fixture-results.json'))};
 const source=path.join(__dirname,'SmaliFingerprintExport.java'),classes=path.join(run,'classes');fs.mkdirSync(classes);evidence.exporterSourceSha256=fileHash(source);
 const java='C:/Program Files/Java/jdk-21/bin/java.exe',javac='C:/Program Files/Java/jdk-21/bin/javac.exe';runTool(java,['--version'],10000,'java-version');
 runTool(javac,['-cp',jar,'-d',classes,source],60000,'compile');
 const output=path.join(run,'smoke-output.ndjson'),descriptor='Lcom/iflytek/bavvo/MainActivity;';
 runTool(java,['-Xmx512m','-cp',classes+path.delimiter+jar,'SmaliFingerprintExport',input,output,descriptor],60000,'smoke');
 const records=fs.readFileSync(output,'utf8').trim().split(/\r?\n/).map(x=>JSON.parse(x)),summaries=records.filter(x=>x.type==='summary'),exported=records.filter(x=>x.type==='class');
 if(summaries.length!==1||records.at(-1)!==summaries[0]||!summaries[0].complete||summaries[0].classes!==1||summaries[0].inputSha256!==expectedInput||exported.length!==1||exported[0].descriptor!==descriptor||exported[0].validationErrors!==false)throw Error('Incomplete or unexpected API output');
 const raw=Buffer.from(exported[0].smaliBase64,'base64');if(raw.length!==exported[0].smaliBytes||hash(raw)!==exported[0].smaliSha256)throw Error('Smali integrity mismatch');
 const normalized=normalizeSmali(raw.toString('utf8'));if(normalized.descriptor!==descriptor)throw Error('Normalized descriptor mismatch');
 fs.writeFileSync(path.join(run,'MainActivity.smali'),raw);fs.writeFileSync(path.join(run,'MainActivity.normalized.smali'),normalized.normalized);fs.writeFileSync(path.join(run,'MainActivity.fingerprint.json'),JSON.stringify(normalized,null,2)+'\n');
 evidence.baksmaliOptions={debugInfo:false,sequentialLabels:true,implicitReferences:false,parameterRegisters:false,localsDirective:false,codeOffsets:false,accessorComments:false,normalizeVirtualMethods:false,registerInfo:0,allowOdex:false,deodex:false};
 evidence.output={file:output,sha256:fileHash(output),summary:summaries[0],descriptor,rawSmaliSha256:hash(raw),classSha256:normalized.classSha256,contextSha256:normalized.contextSha256,methodCount:normalized.methodCount,methods:normalized.methods.map(({normalized,...m})=>m),fingerprintFile:path.join(run,'MainActivity.fingerprint.json')};
 const sizeOf=p=>fs.readdirSync(p,{withFileTypes:true}).reduce((n,e)=>n+(e.isDirectory()?sizeOf(path.join(p,e.name)):fs.statSync(path.join(p,e.name)).size),0);evidence.outputBytes=sizeOf(run);if(evidence.outputBytes>evidence.limits.outputLimitBytes)throw Error('Output disk limit exceeded');
 evidence.status='PASS';
}catch(e){evidence.status='FAIL';evidence.error=e.stack;process.exitCode=1;}
evidence.finishedAt=new Date().toISOString();fs.writeFileSync(path.join(__dirname,'smoke-results.json'),JSON.stringify(evidence,null,2)+'\n');console.log(JSON.stringify({status:evidence.status,run,methodCount:evidence.output?.methodCount,error:evidence.error}));
