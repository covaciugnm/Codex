'use strict';
// Experimental decompiler-only change. Never edits the original JAR or promotes APK output.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {zipEntries}=require('./inspect-android-archive.cjs');
const repo=path.resolve(__dirname,'..'),meta=path.join(repo,'decompilation-repair-2026-11-01/jadx-null-const'),work='D:/Codex-iflytek-decompilation-repair-20261101/jadx-null-const',jar='D:/Codex-iflytek-apk-analysis-20261101/jadx/lib/jadx-1.5.6-all.jar',java='C:/Program Files/Java/jdk-21/bin/java.exe',javac='C:/Program Files/Java/jdk-21/bin/javac.exe';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex'),read=p=>JSON.parse(fs.readFileSync(p)),write=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');},relative='jadx/core/dex/visitors/typeinference/TypeUpdate.java';
const fixture=`package jadx.core.dex.visitors.typeinference;
import jadx.api.JadxArgs;
import jadx.api.JadxDecompiler;
import jadx.core.dex.nodes.RootNode;
import jadx.core.dex.nodes.MethodNode;
import jadx.core.dex.nodes.ClassNode;
import jadx.core.dex.nodes.InsnNode;
import jadx.core.dex.instructions.InsnType;
import jadx.core.dex.instructions.args.ArgType;
import jadx.core.dex.instructions.args.InsnArg;
import jadx.core.dex.instructions.args.RegisterArg;
import jadx.core.dex.instructions.args.SSAVar;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;
import java.io.File;
import java.util.List;
public class NullConstGuardFixture {
  static String run(RootNode root, MethodNode context, boolean result, ArgType current, ArgType candidate) throws Exception {
    TypeUpdate update = new TypeUpdate(root);
    TypeUpdateInfo info = new TypeUpdateInfo(context, TypeUpdateFlags.FLAGS_EMPTY, root.getArgs());
    InsnNode insn = new InsnNode(InsnType.CONST, 1);
    InsnArg literal = InsnArg.lit(0, candidate);
    insn.addArg(literal);
    if (result) {
      RegisterArg assignment = InsnArg.reg(0, current);
      SSAVar variable = new SSAVar(0, 0, assignment);
      variable.setType(current);
      if (!assignment.getType().equals(current)) throw new IllegalStateException("Fixture SSA type setup failed");
      insn.setResult(assignment);
    }
    Method listener = TypeUpdate.class.getDeclaredMethod("sameFirstArgListener", TypeUpdateInfo.class, InsnNode.class, InsnArg.class, ArgType.class);
    listener.setAccessible(true);
    try { return String.valueOf(listener.invoke(update, info, insn, literal, candidate)); }
    catch (InvocationTargetException e) { return e.getCause().getClass().getSimpleName(); }
  }
  public static void main(String[] args) throws Exception {
    JadxArgs configuration = new JadxArgs();
    configuration.setInputFiles(List.of(new File(args[0])));
    configuration.setThreadsCount(1);
    try (JadxDecompiler reader = new JadxDecompiler(configuration)) {
      reader.load(); // Metadata from this generated fixture class only; no APK input/getCode.
      MethodNode context = null;
      for (ClassNode cls : reader.getRoot().getClasses())
        if (cls.getRawName().equals("jadx.core.dex.visitors.typeinference.NullConstGuardFixture"))
          for (MethodNode mth : cls.getMethods())
            if (mth.getMethodInfo().getName().equals("run")) context = mth;
      if (context == null) throw new IllegalStateException("Fixture method context missing");
      RootNode root = reader.getRoot();
      System.out.println("IFLYTEK_FIXTURE_RESULT {\\\"missingFloat\\\":\\\"" + run(root, context, false, ArgType.INT, ArgType.FLOAT) + "\\\",\\\"matchingInt\\\":\\\"" + run(root, context, true, ArgType.INT, ArgType.INT) + "\\\",\\\"conflictFloatToInt\\\":\\\"" + run(root, context, true, ArgType.INT, ArgType.FLOAT) + "\\\",\\\"matchingFloat\\\":\\\"" + run(root, context, true, ArgType.FLOAT, ArgType.FLOAT) + "\\\"}");
    }
  }
}
`;
async function prepare(){
 const url='https://raw.githubusercontent.com/skylot/jadx/v1.5.6/jadx-core/src/main/java/jadx/core/dex/visitors/typeinference/TypeUpdate.java',response=await fetch(url);if(!response.ok)throw Error('Official source unavailable '+response.status);const original=Buffer.from(await response.arrayBuffer()),text=original.toString('utf8'),needle='\t\tInsnArg changeArg = isAssign(insn, arg) ? insn.getArg(0) : insn.getResult();\n\t\tif (updateInfo.hasUpdateWithType(changeArg, candidateType)) {';
 if(!text.startsWith('package jadx.core.dex.visitors.typeinference;')||text.split(needle).length!==2)throw Error('Unexpected exact upstream source shape');
 const patched=text.replace(needle,'\t\tInsnArg changeArg = isAssign(insn, arg) ? insn.getArg(0) : insn.getResult();\n\t\tif (changeArg == null) {\n\t\t\tLOG.warn("IFLYTEK_EXPERIMENTAL_NULL_CONST_TARGET method={} opcode={} offset={}",\n\t\t\t\t\tupdateInfo.getMth() == null ? "<fixture>" : updateInfo.getMth().getMethodInfo().getRawFullId(),\n\t\t\t\t\tinsn.getType(), insn.getOffset());\n\t\t\treturn CHANGED;\n\t\t}\n\t\tif (updateInfo.hasUpdateWithType(changeArg, candidateType)) {');
 const originalFile=path.join(work,'source/original',relative),patchedFile=path.join(work,'source/patched',relative),fixtureFile=path.join(work,'source/fixture-v2/jadx/core/dex/visitors/typeinference/NullConstGuardFixture.java');for(const [p,b] of [[originalFile,original],[patchedFile,patched],[fixtureFile,fixture]]){fs.mkdirSync(path.dirname(p),{recursive:true});if(fs.existsSync(p)&&!fs.readFileSync(p).equals(Buffer.from(b)))throw Error('Existing source bytes differ; use a fresh versioned source path');fs.writeFileSync(p,b);}
 const jarBytes=fs.readFileSync(jar),expected=read(path.join(repo,'apk-analysis-2026-11-01/toolchain.json')).jadx.jarSha256;if(hash(jarBytes)!==expected)throw Error('Original JAR mismatch');const entry=zipEntries(jarBytes).find(e=>e.name==='jadx/core/dex/visitors/typeinference/TypeUpdate.class');if(!entry)throw Error('Original class missing');const classBytes=entry.read(),folder=path.join(work,'preflight-v2'),ref=(file)=>{const b=fs.readFileSync(file);return{file,sha256:hash(b),bytes:b.length};};
 const plan={schemaVersion:1,gateId:'G-JADX-NULL-CONST-PREFLIGHT-V2',classification:'EXPERIMENTAL-DECOMPILER-CHANGE-NOT-APK-REPAIR',status:'PROPOSED-NOT-EXECUTED',upstream:{url,tag:'v1.5.6',retrievedAt:new Date().toISOString(),sha256:hash(original),bytes:original.length,licenseUrl:'https://github.com/skylot/jadx/blob/v1.5.6/LICENSE'},originalJar:{file:jar,sha256:expected,bytes:jarBytes.length,typeUpdateClassSha256:hash(classBytes)},sources:{original:ref(originalFile),patched:ref(patchedFile),fixture:ref(fixtureFile)},change:{scope:'Only sameFirstArgListener, registered for CONST',behavior:'If target operand is absent, keep the current update and skip propagating into a nonexistent operand, with explicit warning. Existing result/constraints remain unchanged.',warning:'IFLYTEK_EXPERIMENTAL_NULL_CONST_TARGET method=<raw-full-id> opcode=<type> offset=<raw-jadx-offset>',risk:'May relax an inference constraint and emit wrong Java. Unit success or lower error count is not semantic acceptance.'},limits:{compileTimeoutMs:60000,fixtureTimeoutMs:30000,totalTimeoutMs:270000,heap:'512MB per fixture JVM',maximumOutputBytes:10485760},runFolder:folder,commands:[
  {name:'compile-fixture',executable:javac,args:['--release','17','-proc:none','-encoding','UTF-8','-cp',jar,'-d',path.join(folder,'fixture-classes'),fixtureFile],timeoutMs:60000},
  {name:'compile-control',executable:javac,args:['--release','17','-proc:none','-encoding','UTF-8','-cp',jar,'-d',path.join(folder,'control-classes'),originalFile],timeoutMs:60000},
  {name:'compile-patched',executable:javac,args:['--release','17','-proc:none','-encoding','UTF-8','-cp',jar,'-d',path.join(folder,'patched-classes'),patchedFile],timeoutMs:60000},
  ...['original','control','patched'].map(name=>({name:'fixture-'+name,executable:java,args:['-Xmx512m','-Djava.io.tmpdir='+path.join(folder,'tmp'),'-Duser.home='+path.join(folder,'home'),'-cp',[path.join(folder,'fixture-classes'),...(name==='original'?[]:[path.join(folder,name+'-classes')]),jar].join(path.delimiter),'jadx.core.dex.visitors.typeinference.NullConstGuardFixture',path.join(folder,'fixture-classes/jadx/core/dex/visitors/typeinference/NullConstGuardFixture.class')],timeoutMs:30000}))],compiler:{executable:javac,version:'javac 21.0.6',releaseTarget:17,expectedClassMajorVersion:61},originalDistributedClassMajorVersion:classBytes.readUInt16BE(6),fixtureClassInput:'Generated fixture class metadata only; no getCode calls and no APK input',expected:{original:{missingFloat:'NullPointerException',matchingInt:'SAME',conflictFloatToInt:'REJECT',matchingFloat:'SAME'},control:{missingFloat:'NullPointerException',matchingInt:'SAME',conflictFloatToInt:'REJECT',matchingFloat:'SAME'},patched:{missingFloat:'CHANGED',matchingInt:'SAME',conflictFloatToInt:'REJECT',matchingFloat:'SAME'}},apkInputIncluded:false,codePromotionAllowed:false};
 write(path.join(meta,'PREFLIGHT-V2-PLAN.json'),plan);console.log(JSON.stringify({file:path.join(meta,'PREFLIGHT-V2-PLAN.json'),sha256:hash(fs.readFileSync(path.join(meta,'PREFLIGHT-V2-PLAN.json'))),upstreamSha256:hash(original)}));
}
function files(folder){const result=[];for(const e of fs.readdirSync(folder,{withFileTypes:true})){const file=path.join(folder,e.name);if(e.isDirectory())result.push(...files(file));else{const b=fs.readFileSync(file);result.push({file,sha256:hash(b),bytes:b.length,...(file.endsWith('.class')?{classMajorVersion:b.readUInt16BE(6)}:{})});}}return result;}
function run(){const planFile=path.join(meta,'PREFLIGHT-V2-PLAN.json'),plan=read(planFile),gate=read(path.join(repo,'decompilation-repair-2026-11-01/audit/GATES.json')).gates.find(g=>(g.id||g.gate)===plan.gateId);if(!gate||gate.status!=='PASS'||gate.score!==10||gate.planSha256!==hash(fs.readFileSync(planFile))||gate.runnerSha256!==hash(fs.readFileSync(__filename)))throw Error('Exact independent preflight gate missing');for(const r of [plan.originalJar,...Object.values(plan.sources)]){const b=fs.readFileSync(r.file);if(hash(b)!==r.sha256||b.length!==r.bytes)throw Error('Experimental input changed');}if(fs.existsSync(plan.runFolder))throw Error('Fresh experiment directory required');for(const p of [plan.runFolder,path.join(plan.runFolder,'tmp'),path.join(plan.runFolder,'home')])fs.mkdirSync(p,{recursive:true});fs.writeFileSync(path.join(plan.runFolder,'RUNNER-SNAPSHOT.cjs'),fs.readFileSync(__filename));fs.writeFileSync(path.join(plan.runFolder,'PLAN-SNAPSHOT.json'),fs.readFileSync(planFile));for(const [name,r] of Object.entries(plan.sources))fs.writeFileSync(path.join(plan.runFolder,'SOURCE-'+name+'.java'),fs.readFileSync(r.file));const startedAt=new Date().toISOString(),start=Date.now(),runs=[];let failure=null;
 for(const command of plan.commands){const effectiveTimeoutMs=Math.min(command.timeoutMs,plan.limits.totalTimeoutMs-(Date.now()-start));if(effectiveTimeoutMs<=0){failure='Total timeout';break;}const commandStart=Date.now(),r=cp.spawnSync(command.executable,command.args,{cwd:plan.runFolder,encoding:'utf8',timeout:effectiveTimeoutMs,maxBuffer:plan.limits.maximumOutputBytes,windowsHide:true,env:{...process.env,JADX_CACHE_DIR:path.join(plan.runFolder,'cache'),JADX_CONFIG_DIR:path.join(plan.runFolder,'config'),JADX_TMP_DIR:path.join(plan.runFolder,'tmp')}}),elapsedMs=Date.now()-commandStart,log=path.join(plan.runFolder,command.name+'.log'),logBytes=Buffer.from((r.stdout||'')+(r.stderr||''));fs.writeFileSync(log,logBytes);const result={...command,effectiveTimeoutMs,elapsedMs,exitCode:r.status,error:r.error?.message||null,signal:r.signal,log:{file:log,sha256:hash(logBytes),bytes:logBytes.length}};runs.push(result);if(r.status!==0||r.error||r.signal){failure='Compilation/fixture process failed';break;}
  if(command.name.startsWith('fixture-')){const match=/^IFLYTEK_FIXTURE_RESULT (.+)$/m.exec(r.stdout||'');if(!match){failure='Fixture result missing';break;}try{result.result=JSON.parse(match[1]);}catch{failure='Fixture JSON invalid';break;}const expected=plan.expected[command.name.slice(8)];if(JSON.stringify(result.result)!==JSON.stringify(expected)){failure='Fixture differs from exact expected behavior';break;}}
 }
 const artifacts=files(plan.runFolder),controlFiles=artifacts.filter(r=>r.file.startsWith(path.join(plan.runFolder,'control-classes')+path.sep)).map(r=>path.relative(path.join(plan.runFolder,'control-classes'),r.file)).sort(),patchedFiles=artifacts.filter(r=>r.file.startsWith(path.join(plan.runFolder,'patched-classes')+path.sep)).map(r=>path.relative(path.join(plan.runFolder,'patched-classes'),r.file)).sort();if(!failure&&JSON.stringify(controlFiles)!==JSON.stringify(patchedFiles))failure='Control/patched auxiliary class sets differ';if(!failure&&artifacts.some(r=>r.classMajorVersion&&r.classMajorVersion!==plan.compiler.expectedClassMajorVersion))failure='Unexpected compiled target Java version';if(!failure&&artifacts.reduce((n,r)=>n+r.bytes,0)>plan.limits.maximumOutputBytes)failure='Post-run artifact size acceptance check exceeded';const report={schemaVersion:1,status:failure?'FAIL':'PASS',classification:'EXPERIMENTAL-TOOL-PREFLIGHT-ONLY',planSha256:hash(fs.readFileSync(planFile)),generatorSha256:hash(fs.readFileSync(__filename)),startedAt,finishedAt:new Date().toISOString(),elapsedMs:Date.now()-start,runs,artifacts,controlAuxiliaryFiles:controlFiles,patchedAuxiliaryFiles:patchedFiles,failure,apkInputIncluded:false,codePromotionAllowed:false};write(path.join(meta,'PREFLIGHT-V2-RESULTS.json'),report);console.log(JSON.stringify({status:report.status,failure,runs:runs.length,elapsedMs:report.elapsedMs}));if(failure)process.exitCode=1;
}
if(require.main===module)(async()=>{if(process.argv.includes('--prepare'))await prepare();else if(process.argv.includes('--run'))run();else throw Error('Use --prepare or --run');})().catch(e=>{console.error(e);process.exitCode=1;});
