from a03_r8_jvm import *
from a03_r8_pg import run,pg
import shutil,tempfile,secrets
def pol():
 old=policy.read_text(encoding='utf8')
 p=work/'R8.policy';p.write_text(old+'\ngrant {permission java.io.FilePermission "D:/CodexWork/a03-r8/-","read,write,delete";permission java.lang.RuntimePermission "setIO";permission java.lang.reflect.ReflectPermission "newProxyInPackage.com.eva.ro.saga.core";permission java.io.FilePermission "C:/Users/User/.cache/codex-runtimes/-","read";};\n',encoding='utf8');return p
def setup_run():
 jjdk=pol(); env={**os.environ,'JAVA_HOME':str(jdk.parent),'PATH':str(jdk)+';'+os.environ['PATH']};t=work/'tmp';t.mkdir(exist_ok=True)
 for lab,n in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
  cp=os.pathsep.join(str(p) for p in [work/lab,P('D:/CodexWork/a03-r4-runtime')/lab,sec/n,work/'git-saga.jar',sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',P('D:/CodexWork/a05-support-jars/*'),P('D:/CodexWork/eva-a01-java/lib/*'),plug/'src',saga/'src']);rs=[]
  for name in ['TestT29ImportSetari','TestT159LotD','TestA83Butoane','TestPornireContab']:
   cwd=saga if name=='TestT29ImportSetari' else plug
   rr=sp.run([jdk/'java.exe','-Xmx512m','-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+jjdk.as_uri(),'-Djava.io.tmpdir='+str(t),'-cp',cp,name],env=env,cwd=cwd,capture_output=True,timeout=60)
   b=rr.stdout+rr.stderr;f=out/'log'/('retry-'+lab+'-'+name+'.txt');f.write_bytes(b);lines=b.decode('utf8',errors='replace').splitlines()
   rs.append({'test':name,'jar':n,'jar_sha256':H((sec/n).read_bytes()),'rc':rr.returncode,'file':str(f.relative_to(out)),'sha256':H(b),'summary':[l for l in lines if 'REZULTAT' in l or 'Exception in thread' in l][:3]});print(rs[-1]['test'],rs[-1]['rc'],rs[-1]['summary'],flush=True)
  J(out/('JVM_reexecutii_'+lab+'.json'),{'utc':UTC(),'policy_sha256':H(jjdk.read_bytes()),'network_granted':False,'results':rs})
def testpg():
 pol0=pol(); store=work/'testsql';store.mkdir(exist_ok=True);dep=store/'deps';dep.mkdir(exist_ok=True)
 for d in [P('D:/CodexWork/a05-support-jars'),P('D:/CodexWork/eva-a01-java/lib'),sec]:
  for p in d.glob('*.jar'):
   if p.name.startswith('cod-master') or 'com.eva.ro.contab' in p.name or 'frontend' in p.name:continue
   q=dep/p.name
   if not q.exists():
    try:os.link(p,q)
    except OSError:shutil.copyfile(p,q)
 f=plug/'test/sql/TestT256D394Sql.java';c=sp.run([jdk/'javac.exe','-proc:none','-encoding','UTF-8','-d',store,f],capture_output=True);assert c.returncode==0,c.stderr
 pgbase=pg/'pgsql/bin/pg_ctl.exe';opts=[str(pgbase),'-D',str(pg/'data')];status=sp.run(opts+['status'],capture_output=True);assert status.returncode==3,'cluster occupied; coordinate before use'
 sr=sp.run(opts+['-o','-h 127.0.0.1 -p 56481','-l',str(pg/'log.txt'),'-w','start'],stdout=sp.DEVNULL,stderr=sp.DEVNULL,cwd=work);assert sr.returncode==0
 try:
  rows=[]
  for lab,n in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
   loc=store/lab;loc.mkdir(exist_ok=True);shutil.copyfile(sec/n,loc/'com.eva.ro.contab_13.0.0.jar')
   rr=sp.run([jdk/'java.exe','-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+pol0.as_uri(),'-cp',store,'TestT256D394Sql',loc,dep],cwd=work,capture_output=True,timeout=60);assert rr.returncode==0,rr.stderr.decode(errors='replace')[-1800:];sql=rr.stdout
   assert b'CREATE TABLE' in sql and b'SELECT CASE WHEN' in sql
   db='p01_a03r8j_'+secrets.token_hex(5);assert re.fullmatch('p01_a03r8j_[0-9a-f]{10}',db)
   cr=run(('CREATE DATABASE '+db+" TEMPLATE template0 ENCODING 'UTF8';").encode());assert cr.returncode==0,cr.stderr
   try:r=run(sql,db)
   finally:cl=run(('DROP DATABASE '+db+';').encode());assert cl.returncode==0,cl.stderr
   b=r.stdout+r.stderr;fout=out/'log'/(lab+'-T256-SQL-binary.txt');fout.write_bytes(b);(out/'log'/(lab+'-T256-SQL-generated.sql')).write_bytes(sql)
   ls=b.decode('utf8',errors='replace').splitlines();rows.append({'source_test':str(f.relative_to(root)),'test_sha256':H(f.read_bytes()),'origin':lab,'jar':n,'jar_sha256':H((sec/n).read_bytes()),'sql_sha256':H(sql),'evidence_sql':str(fout.with_name(lab+'-T256-SQL-generated.sql').relative_to(out)),'stdout_sha256':H(b),'evidence_log':str(fout.relative_to(out)),'psql_rc':r.returncode,'checks':[x for x in ls if re.match('^(OK |FAIL )',x)],'db_released':cl.stdout.decode().strip()})
 finally:st=sp.run(opts+['-m','smart','-w','stop'],capture_output=True,cwd=work); assert st.returncode==0,st.stderr
 J(out/'T256_SQL_din_JAR.json',{'utc':UTC(),'engine':'PostgreSQL 16.15, dedicated fresh UTF8 databases, cluster restarted and stopped after final trial. Fixture generated in the JVM with actual production SQL (no native document posting or ANAF submission).','sha':sha,'results':rows})
 print([(r['origin'],r['psql_rc'],len(r['checks']),sum(x.startswith('FAIL ') for x in r['checks'])) for r in rows])
if __name__=='__main__':globals()[sys.argv[1]]()

