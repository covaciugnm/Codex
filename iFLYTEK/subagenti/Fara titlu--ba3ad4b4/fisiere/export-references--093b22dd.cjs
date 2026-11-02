'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {normalizeSmali}=require('./normalize-smali.cjs');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex'),fileHash=p=>hash(fs.readFileSync(p));
const gateFile=path.join(__dirname,'../audit/CORRELATION-EXPORT-GATE.json'),gate=JSON.parse(fs.readFileSync(gateFile,'utf8')),smoke=JSON.parse(fs.readFileSync(path.join(__dirname,'smoke-results.json'),'utf8'));
if(gate.gate!=='G-CORRELATION-REFERENCE-EXPORT'||gate.verdict!=='PASS'||gate.score!==10)throw Error('Missing approved reference-export gate');
const approved=['Lcom/google/android/material/carousel/CarouselStrategyHelper;','Lcom/google/android/material/shadow/ShadowDrawableWrapper;','La/b;','Lcom/google/android/gms/internal/auth/P1;','LK6/d;','LA4/d;'];
if(JSON.stringify([...gate.allowedDescriptors].sort())!==JSON.stringify([...approved].sort()))throw Error('Unexpected reference-export scope');
const run=path.join('D:/Codex-iflytek-decompilation-repair-20261101/correlation','references-'+Date.now());fs.mkdirSync(run,{recursive:true});
const result={schemaVersion:1,gate:gate.gate,gateFile,gateSha256:fileHash(gateFile),startedAt:new Date().toISOString(),run,requested:approved,commands:[],status:'RUNNING',scope:'Read-only static Smali reference export, no Java equivalence claim or patch'};
function tool(executable,args,timeoutMs,label){const start=Date.now(),r=cp.spawnSync(executable,args,{encoding:'utf8',timeout:timeoutMs,maxBuffer:8*1024**2,windowsHide:true}),log=path.join(run,label+'.log');fs.writeFileSync(log,(r.stdout||'')+(r.stderr||''));result.commands.push({executable,args,timeoutMs,label,elapsedMs:Date.now()-start,exitCode:r.status,error:r.error?.message||null,signal:r.signal||null,log,logSha256:fileHash(log)});if(r.error||r.status!==0||r.signal)throw Error(label+' failed');}
try{
 const source=path.join(__dirname,'SmaliFingerprintExport.java'),normalizer=path.join(__dirname,'normalize-smali.cjs'),input=smoke.input.file,jar=smoke.jar.file;
 if(fileHash(source)!==gate.exporterSourceSha256||fileHash(normalizer)!==gate.normalizerSha256||fileHash(input)!==gate.sourceComponentSha256||fileHash(jar)!==smoke.jar.expectedSha256)throw Error('Approved input/tool/source SHA mismatch');
 result.input={file:input,sha256:fileHash(input),bytes:fs.statSync(input).size};result.jar={file:jar,sha256:fileHash(jar)};result.exporterSourceSha256=fileHash(source);result.normalizerSha256=fileHash(normalizer);
 const list=path.join(run,'descriptors.txt');fs.writeFileSync(list,approved.join('\n')+'\n');const classes=path.join(run,'classes');fs.mkdirSync(classes);
 tool('C:/Program Files/Java/jdk-21/bin/javac.exe',['-cp',jar,'-d',classes,source],60000,'compile');
 result.compiledExporterSha256=fileHash(path.join(classes,'SmaliFingerprintExport.class'));
 const output=path.join(run,'references.ndjson');
 tool('C:/Program Files/Java/jdk-21/bin/java.exe',['-Xmx512m','-cp',classes+path.delimiter+jar,'SmaliFingerprintExport',input,output,'@'+list],gate.limits.maxWallMs,'export');
 const records=fs.readFileSync(output,'utf8').trim().split(/\r?\n/).map(x=>JSON.parse(x)),summaries=records.filter(x=>x.type==='summary'),all=records.filter(x=>x.type==='class');
 if(summaries.length!==1||records.at(-1)!==summaries[0]||!summaries[0].complete||summaries[0].classes!==6||summaries[0].inputSha256!==gate.sourceComponentSha256||all.length!==6||new Set(all.map(x=>x.descriptor)).size!==6||all.some(x=>!approved.includes(x.descriptor)||x.validationErrors!==false))throw Error('Invalid or incomplete reference export');
 result.classes=[];for(const c of all){const b=Buffer.from(c.smaliBase64,'base64');if(b.length!==c.smaliBytes||hash(b)!==c.smaliSha256)throw Error('Invalid Smali hash');const n=normalizeSmali(b.toString('utf8'));if(n.descriptor!==c.descriptor)throw Error('Descriptor mismatch');const name=c.descriptor.slice(1,-1).replace(/[^A-Za-z0-9_.-]/g,'_')+'-'+hash(Buffer.from(c.descriptor)).slice(0,8)+'.smali',file=path.join(run,name);fs.writeFileSync(file,b);result.classes.push({descriptor:c.descriptor,dexEntry:c.dexEntry,file,smaliSha256:c.smaliSha256,smaliBytes:c.smaliBytes,classSha256:n.classSha256,contextSha256:n.contextSha256,methodCount:n.methodCount,methods:n.methods.map(({normalized,...m})=>m)});}
 const sizeOf=p=>fs.readdirSync(p,{withFileTypes:true}).reduce((n,e)=>n+(e.isDirectory()?sizeOf(path.join(p,e.name)):fs.statSync(path.join(p,e.name)).size),0);result.outputBytes=sizeOf(run);if(result.outputBytes>gate.limits.maxOutputBytes)throw Error('Output budget exceeded');result.output={file:output,sha256:fileHash(output),summary:summaries[0]};result.status='PASS';
}catch(e){result.status='FAIL';result.error=e.stack;process.exitCode=1;}
result.finishedAt=new Date().toISOString();fs.writeFileSync(path.join(__dirname,'reference-export-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,run,classes:result.classes?.map(x=>({descriptor:x.descriptor,methods:x.methodCount,file:x.file})),error:result.error}));
