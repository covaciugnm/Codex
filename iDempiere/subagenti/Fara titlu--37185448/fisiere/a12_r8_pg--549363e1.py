from a12_r8_review import *
from a12_r6_exec import java,sec,base,plug,execute,repo
import os,sys,secrets,socket,tempfile,shutil,subprocess,time,threading
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
out=P/'SQL';out.mkdir(exist_ok=True);bin=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');testsql=E/'R5/sql_batch';targets=['TestT182D107Sql','TestT220CorelezSql','TestT227VerificareImportSql','TestT22CitiriSql','TestT22TrimitereSql']
def exe(args,**kwargs):return subprocess.run([str(z) for z in args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60,**kwargs)
def go():
 with tempfile.TemporaryDirectory(prefix='a12r8pg-',dir='D:/CodexWork/a12-r8-runs')as tmpdir:
  tmp=Path(tmpdir);pwd=secrets.token_hex(36);pf=tmp/'pwd-local';pf.write_text(pwd+'\n');data=tmp/'data'
  with socket.socket()as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
  r=exe([bin/'initdb.exe','-D',data,'-U','a12_r8','--username=a12_r8','--encoding=UTF8','--locale=C','--auth=scram-sha-256','--pwfile='+str(pf)]);assert r.returncode==0,r.stdout[-1200:];pf.unlink()
  r=subprocess.run([str(z)for z in [bin/'pg_ctl.exe','-D',data,'-l',tmp/'server.log','-o','-h 127.0.0.1 -p '+str(port),'start','-w']],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=70);assert r.returncode==0
  def db(n='postgres',autoc=False):return psycopg.connect(host='127.0.0.1',port=port,user='a12_r8',dbname=n,password=pwd,autocommit=autoc,connect_timeout=5)
  try:
   logs=[];suites=[]
   for nm in targets:
    for tag in ('git','instalat'):
     f=testsql/(tag+'_'+nm+'.sql');g=testsql/(tag+'_'+nm+'.generator.log')
     if not f.exists():suites.append({'suite':nm,'target':tag,'result':'ABSENT_GENERATED_SQL','diagnostics':source(g)});continue
     buf=f.read_text(encoding='utf8');original=n='a12r8_'+str(len(suites))
     with db(autoc=True)as cn:cn.execute('create database '+n+' template template0')
     try:
      rc=exe([bin/'psql.exe','-h','127.0.0.1','-p',str(port),'-U','a12_r8','-X','-qAt','-v','ON_ERROR_STOP=1','-d',n],input=buf.encode(),env=dict(os.environ,PGPASSWORD=pwd,PGCLIENTENCODING='UTF8'));q=out/(tag+'_'+nm+'.pglog');q.write_bytes(rc.stdout)
      val=rc.stdout.decode('utf8','replace').splitlines();markers=[{'line':i,'output':t}for i,t in enumerate(val,1)if re.match(r'^\s*(?:OK|FAIL)\s+',t)]
      suites.append({'suite':nm,'target':tag,'input_sql':source(f),'generation_log':source(g),'log':source(q),'exit':rc.returncode,'markers':markers,'errors':[s for s in val if 'ERROR:'in s]})
     finally:
      with db(autoc=True)as cn:cn.execute('drop database '+n)
   # two physical sessions; Java decision invokes deployed/Git implementations with the actual PG timestamps.
   td=Path('D:/CodexWork/a12-r8-runs/D107');td.mkdir(exist_ok=True);src=td/'AuditD107R8.java';src.write_text('''package com.eva.ro.contab.anaf; import java.sql.Timestamp; public class AuditD107R8 {public static void main(String[] a){System.out.println(D107Beneficiari.SQL_REVIZIE);System.out.println("conflict="+D107Beneficiari.inConflict(Timestamp.valueOf(a[0]),Timestamp.valueOf(a[1])));}}''',encoding='utf8')
   with db(autoc=True)as cn:
    cn.execute('create table eva_d107beneficiar(eva_d107beneficiar_id int primary key, ad_client_id int not null, updated timestamp not null, suma numeric not null)');cn.execute("insert into eva_d107beneficiar values(501,11,'2026-06-30 10:00',100),(502,12,'2026-06-30 10:00',999)")
   def j(tag,t0,t1):
    jar=sec/('cod-master-contab.jar'if tag=='git'else'com.eva.ro.contab_13.0.0.jar');dest=td/tag;dest.mkdir(exist_ok=True);cp=';'.join(map(str,[dest,jar,base,'D:/CodexWork/a05-support-jars/*','D:/CodexWork/eva-a01-java/lib/*']))
    if not (dest/'com/eva/ro/contab/anaf/AuditD107R8.class').exists():
     rr=execute([java/'javac.exe','-cp',cp,'-sourcepath','','-d',dest,src],td);assert rr.returncode==0,rr.stdout
    rr=execute([java/'java.exe','-cp',cp,'com.eva.ro.contab.anaf.AuditD107R8',str(t0),str(t1)],td);assert rr.returncode==0,rr.stdout;ls=rr.stdout.splitlines();return jar,ls[0],ls[-1]
   for tag in ('git','instalat'):
    with db(autoc=True)as cn:cn.execute("update eva_d107beneficiar set updated='2026-06-30 10:00',suma=100 where eva_d107beneficiar_id=501")
    with db()as a,db()as b:
     loaded=a.execute("select updated from eva_d107beneficiar where eva_d107beneficiar_id=501").fetchone()[0]
     jar,sqlj,ctrl=j(tag,loaded,loaded);assert ctrl=='conflict=false';statement=sqlj.replace('?','%s');assert statement.endswith('FOR UPDATE')
     b.execute("update eva_d107beneficiar set updated='2026-06-30 11:00',suma=230 where eva_d107beneficiar_id=501");jpid=a.info.backend_pid;vv=[]
     def read():vv.append(a.execute(statement,(501,11)).fetchone()[0])
     thread=threading.Thread(target=read);thread.start();wait=None
     with db(autoc=True)as cn:
      for i in range(30):
       wait=cn.execute('select wait_event_type,wait_event from pg_stat_activity where pid=%s',(jpid,)).fetchone()
       if wait and wait[0]=='Lock':break
       time.sleep(.04)
     b.commit();thread.join(8);assert vv;_,_,decision=j(tag,loaded,vv[0]);assert decision=='conflict=true' and wait and wait[0]=='Lock'
     foreign=a.execute(statement,(502,11)).fetchone();a.rollback()
     with db()as cn:end=cn.execute('select suma from eva_d107beneficiar where eva_d107beneficiar_id=501').fetchone()[0]
     logs.append({'target':tag,'jar_sha':sha(jar),'literal_SQL_from_binary':sqlj,'fixture':'501 firmă11 SUMA=100; 502 firmă12 SUMA=999','control_equal':ctrl,'actor_A_read':str(loaded),'actor_B_new_committed_amount':230,'A_wait_for_B':wait,'A_after_B':str(vv[0]),'deployed_conflict_method':decision,'other_tenant_read_is_none':foreign is None,'A_rolled_back':True,'end_amount':str(end),'scope':'SQL + metoda autentica inConflict; tranzacția de scriere B reală, ramura UI nu a fost apăsată.'})
  finally:
   stop=exe([bin/'pg_ctl.exe','-D',data,'-m','fast','stop','-w']);assert stop.returncode==0,stop.stdout
  wr(out/'Executii_SQL_r8.json',{'utc':now(),'postgres':exe([bin/'postgres.exe','--version']).stdout.decode().strip(),'network':'loopback-only; authenticated; ephemeral PG stopped and its generated directory removed by owner','suites':suites,'T310_two_sessions':logs,'product_mutations':0});print([(x['suite'],x['target'],x.get('exit'),len(x.get('markers',[])))for x in suites],logs[0]['deployed_conflict_method'])
if __name__=='__main__':go()

