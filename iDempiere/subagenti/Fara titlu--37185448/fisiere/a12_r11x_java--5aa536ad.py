from a12_r11x_base import *
import re,zipfile
from concurrent.futures import ThreadPoolExecutor
C=LOCAL/'idempiere/plugins/com.eva.ro.contab'; S=LOCAL/'idempiere/plugins/com.eva.ro.saga.native'; jar=C/'com.eva.ro.contab_13.0.0.jar'; sqlite=S/'lib/sqlite-jdbc.jar'
scratch=W/'jvm';scratch.mkdir(exist_ok=True); out=A/'jvm';out.mkdir(exist_ok=True);sec=Path('D:/CodexWork/eva-audit-secondary-20261102');base=next(sec.glob('org.adempiere.base_*.jar'));java=Path('C:/Program Files/Java/jdk-21/bin');dep6=Path('D:/CodexWork/a12-r6-preprobes/deps')
policy=scratch/'isolated.policy'; policy.write_text('grant { permission java.io.FilePermission "<<ALL FILES>>","read"; permission java.io.FilePermission "'+scratch.as_posix()+'/-","read,write,delete"; permission java.util.PropertyPermission "*","read,write"; permission java.lang.reflect.ReflectPermission "*"; permission java.lang.RuntimePermission "*"; permission java.util.logging.LoggingPermission "control"; permission java.sql.SQLPermission "setLog"; permission java.security.SecurityPermission "getProperty.*"; permission java.io.SerializablePermission "*";};',encoding='utf8')
def cp(dst,j):return ';'.join(map(str,[dst,j,S/'com.eva.ro.saga.native_13.0.0.jar',sqlite,base,next(sec.glob('org.adempiere.base.process_*.jar')),str(dep6)+'/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',C/'src']))
names=['TestComparatieSaga','TestComparatieSagaEcran','TestT201Registre','TestT201Ecrane','TestT257Repostare']
def cmd(args,wd,timeout=95):
 try:return sp.run([str(k)for k in args],cwd=wd,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=timeout,encoding='utf8',errors='replace',creationflags=getattr(sp,'CREATE_NO_WINDOW',0))
 except sp.TimeoutExpired as e:return sp.CompletedProcess(args,124,(e.output or b'').decode('utf8','replace')+' TIMEOUT')
def run_one(name,j=jar,tag='candidate',neg=None):
 dst=scratch/(tag+'_'+name);dst.mkdir(exist_ok=True);src=C/'test'/(name+'.java');s=src.read_text(encoding='utf8');pkg=re.search(r'^package ([\w.]+);',s,re.M);fq=(pkg[1]+'.'if pkg else'')+name;classpath=cp(dst,j);cc=cmd([java/'javac.exe','-J-Xmx220m','-g:lines,source','-encoding','UTF-8','-proc:none','-cp',classpath,'-sourcepath',C/'test','-d',dst,src],C)
 app=[java/'java.exe','-Xmx250m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(scratch),'-Dline.separator=\n','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',classpath,fq]
 if neg:app+=neg
 rr=cmd(app,C)if cc.returncode==0 else None
 txt=cc.stdout+(rr.stdout if rr else'');f=out/(tag+'_'+name+'.log');f.write_text(txt,encoding='utf8');marks=[{'line':i,'text':line.strip()}for i,line in enumerate(txt.splitlines(),1)if re.search(r'^\s*(OK|FAIL)\s',line)]
 return {'suite':name,'target':tag,'jar_sha':sha(j),'fqcn':fq,'git_file':src.relative_to(LOCAL).as_posix(),'git_oid':d[src.relative_to(LOCAL).as_posix()]['git_object'],'test_sha256':sha(src),'propagate_runtime':False,'fixture_variable':neg,'compile':cc.returncode,'process_return':rr.returncode if rr else None,'markers_ok':sum(m['text'].startswith('OK')for m in marks),'markers_failed':sum(m['text'].startswith('FAIL')for m in marks),'summary':[t for t in txt.splitlines()if t.strip().startswith(('REZULTAT','Rezultat','TOTAL'))][-3:],'markers':marks,'log':ref(f)}
if __name__=='__main__':
 remote='docker exec eva-idempiere-cesiro cat /opt/idempiere/plugins/com.eva.ro.contab_13.0.0.jar';rr=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151',remote],capture_output=True,timeout=90);assert rr.returncode==0
 mounted=scratch/'cesiro-contab.jar';mounted.write_bytes(rr.stdout)
 with zipfile.ZipFile(mounted)as z:assert z.testzip() is None
 with ThreadPoolExecutor(max_workers=3)as ex:result=list(ex.map(lambda q:run_one(*q),[(n,j,t)for n in names for j,t in [(jar,'candidate'),(mounted,'mounted_copy')]]))
 f=A/'JVM_Banca_si_registre_01.json';save(f,{'utc':now(),'head':head,'gate':ref(gate),'git_sources':ref(A/'Sources_banca_DB_candidate.json'),'candidate_jar':sha(jar),'mounted_CESIRO_jar':sha(mounted),'limits':'Warm JVM executed the exact candidate and mounted bytes separately, using test classes rebuilt from the Git candidate. Mounted_copy is an isolated JVM; the operational ERP was not invoked. Sources and fixtures came from candidate. Cases with failing assertions or environment classifications stay visible.','runs':result});print(ref(f));print([(x['suite'],x['target'],x['compile'],x['process_return'],x['markers_ok'],x['markers_failed'])for x in result])

