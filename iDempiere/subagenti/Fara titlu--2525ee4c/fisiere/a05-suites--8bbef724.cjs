const fs=require('fs'),p=require('path'),cp=require('child_process'),cr=require('crypto');
const o='Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/A05';
const root='D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab';
const secondary='D:/CodexWork/eva-audit-secondary-20261102';
const deps='D:/CodexWork/a05-support-jars'; const classes='D:/CodexWork/a05-compiled-20261102';const j='C:/Program Files/Java/jdk-21/bin/';
const run=(exe,args)=>cp.spawnSync(exe,args,{cwd:root,encoding:'utf8',timeout:16000,maxBuffer:8e6,windowsHide:true,env:{...process.env,PATH:j+';'+process.env.PATH}});
const suites='TestRegulaLegaturaWms TestT354Set TestT354Disponibil TestT331Oglinda TestScanareCod TestApiMobilInventar TestApiMobilInventarCitiri TestListaPicking TestFefo TestT323Pozitii TestT327Etichete TestT339ValidareWms TestConfirmarePickVal TestNotaSetWms'.split(' ');
const all=[];for(const test of suites){
 const src=p.join(root,'test',test+'.java'),data=fs.readFileSync(src,'utf8'),des=data.match(/^package ([^;]+);/m);
 const jvmCp=[classes,secondary+'/com.eva.ro.contab_13.0.0.jar',secondary+'/org.adempiere.base_13.0.0.202603090043.jar',secondary+'/org.adempiere.base.process_13.0.0.202603090043.jar',deps+'/*'].join(';'); const build=run(j+'javac.exe',['-encoding','UTF-8','-cp',jvmCp,'-d',classes,src]); const t=build.status===0?run(j+'java.exe',['-Dline.separator=\n','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',jvmCp,(des?des[1]+'.':'')+test]):null;
 const raw=[build.error,build.stdout,build.stderr,t?.error,t?.stdout,t?.stderr].filter(Boolean).join('\n'); let logs=p.join(o,'suite');fs.mkdirSync(logs,{recursive:true});fs.writeFileSync(p.join(logs,test+'.txt'),raw,'utf8'); const item={test,compile_exit:build.status,run_exit:t?.status??null,ok:(raw.match(/^\s*OK\s/gm)||[]).length,fail:(raw.match(/^\s*FAIL\s/gm)||[]).length,diagnostic:raw.split(/\r?\n/).filter(x=>/error:|Exception|Error:|^FAIL/.test(x)).slice(0,4),sha256:cr.createHash('sha256').update(raw).digest('hex')};all.push(item);console.log(JSON.stringify(item));
}fs.writeFileSync(p.join(o,'suite-results.json'),JSON.stringify(all,null,2),'utf8');
