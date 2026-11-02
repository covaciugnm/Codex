from pathlib import Path
import subprocess as sp, os, re, json, hashlib, datetime, concurrent.futures
root=Path('D:/CodexWork/eva-audit-p01-readonly-20261102'); plug=root/'idempiere/plugins/com.eva.ro.contab'
git='D:/CodexWork/eva-audit-p01-src-20261101';cut='6df998aee0e514d30856c461962afe99ebd0d113'
out=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R8_pregatire/A05')
scratch=Path('D:/CodexWork/a05r8');jd=Path('C:/Program Files/Java/jdk-21/bin');deps=Path('D:/CodexWork/eva-audit-secondary-20261102')
for d in (scratch,out,out/'JVM',scratch/'classes',scratch/'tmp'):d.mkdir(parents=True,exist_ok=True)
allow='TestT163ArticoleDiverse TestT163Ecran TestT36TexteChei TestListaPicking TestListaPickingEcran TestLoturi TestLoturiEcrane TestFefo TestT40L2Motor TestT40L2Straturi TestT354Disponibil TestT354Set TestRegulaLegaturaWms TestT331Oglinda TestT327Etichete TestT323Pozitii TestT333Acces TestT337Confirmare TestT339Motor TestT339ValidareWms TestT339Ecran TestListaAmplasare TestImportFapticLocatieLot TestT29Catalog TestT29Tiparire TestT29Acoperire TestT29ColoanaFizica TestT29Perioade TestScanareCod TestApiMobilInventar TestApiMobilInventarCitiri TestNotaSetWms TestNotaSetWmsEcran TestConfirmarePickVal TestBonConsumLot'.split()
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def gj(*args):return sp.check_output(['git','-C',git,*args],env={**os.environ,'GIT_NO_LAZY_FETCH':'1'}).decode('utf8','replace').strip()
def dump(f,j):f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def bo(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def run(cmd,timeout=42):
    env={**os.environ,'PATH':str(jd)+';'+os.environ['PATH']}
    q=sp.run(cmd,cwd=plug,env=env,capture_output=True,timeout=timeout);return q.returncode,(q.stdout+q.stderr).decode('utf8','replace')
classpath=';'.join(map(str,[scratch/'classes',deps/'com.eva.ro.contab_13.0.0.jar',deps/'org.adempiere.base_13.0.0.202603090043.jar',deps/'org.adempiere.base.process_13.0.0.202603090043.jar','D:/CodexWork/a05-support-jars/*','D:/CodexWork/eva-a01-java/lib/*']))
pol=scratch/'offline.policy'
# SecurityManager is enabled on JDK 21 for the fork only. No SocketPermission; read-only outside private temp. No external executable except audited local javap.
pol.write_text('''grant {
permission java.io.FilePermission "<<ALL FILES>>","read,readlink";
permission java.io.FilePermission "D:/CodexWork/a05r8/tmp/-","write,delete";
permission java.io.FilePermission "C:/Program Files/Java/jdk-21/bin/javap.exe","execute";
permission java.lang.RuntimePermission "*";
permission java.lang.reflect.ReflectPermission "*";
permission java.util.PropertyPermission "*","read,write";
permission java.util.logging.LoggingPermission "control";
permission java.security.SecurityPermission "*";
permission java.awt.AWTPermission "*";
permission java.sql.SQLPermission "*";
permission javax.management.MBeanPermission "*","*";
};''',encoding='utf8')
def one(name):
    f=plug/'test'/(name+'.java'); b=f.read_bytes(); ident=bo(b); p=f.relative_to(root).as_posix();gitid=gj('rev-parse',cut+':'+p);assert ident==gitid,(name,ident,gitid)
    s=b.decode();pkg=re.search(r'^package ([\w.]+);',s,re.M);cl=(pkg.group(1)+'.' if pkg else '')+name
    build,logs=run([jd/'javac.exe','-encoding','UTF-8','-cp',classpath,'-sourcepath',plug/'test','-d',scratch/'classes',f])
    code=None
    if not build:
        code,tail=run([jd/'java.exe','-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dline.separator=\n','-Djava.security.manager','-Djava.security.policy=='+pol.as_posix(),'-Djava.io.tmpdir='+(scratch/'tmp').as_posix(),'-cp',classpath,cl]);logs+=tail
    artifact=out/'JVM'/(name+'.txt');artifact.write_text(logs,encoding='utf8')
    return {'suite':name,'file':p,'java_blob_oid':gitid,'sha256_src':sha(f),'build':build,'exit':code,'log':'JVM/'+artifact.name,'sha256_log':sha(artifact),'ok_lines':len(re.findall(r'^\s*ok\s',logs,re.I|re.M)),'fail_lines':len(re.findall(r'^\s*fail\s',logs,re.I|re.M)),'summary':logs.splitlines()[-8:]}
if __name__=='__main__':
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with concurrent.futures.ThreadPoolExecutor(2) as ex:
        result=[]
        for name,row in zip(allow,ex.map(one,allow)):
            result.append(row); print(name,row['build'],row['exit'],row['ok_lines'],row['fail_lines'],flush=True);dump(out/'JVM_index_progres.json',{'started':started,'cutoff':cut,'installed_jar':sha(deps/'com.eva.ro.contab_13.0.0.jar'),'runner':'JDK 21; local methods in installed test JAR, verified test source, no SocketPermission; relative working dir plugin subtree; no ERP UI/DB impersonated','suites':result})
