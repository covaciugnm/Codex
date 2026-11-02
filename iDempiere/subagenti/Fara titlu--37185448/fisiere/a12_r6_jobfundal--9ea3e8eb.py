from a12_r6_exec import *
from uuid import uuid4
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
dbname='a12_job_'+uuid4().hex[:15]; assert re.fullmatch(r'a12_job_[a-f0-9]{15}',dbname)
def connect(db,auto=False):return psycopg.connect(host='127.0.0.1',port=56481,user='audit_owner',dbname=db,connect_timeout=6,autocommit=auto)
code='''package com.eva.ro.contab.form;
import java.io.*;import java.util.concurrent.*;import java.util.function.Predicate;
public class JobR6 {
 public static void main(String[] p) throws Exception {
 String mode=p[0];int client=11; String block=JobFundal.cheieBloc(client);String month="11|inch|2026-10";
 String[] keys={"same".equals(mode)?block:block,"same".equals(mode)?block:month};boolean[] got=new boolean[2];
 CyclicBarrier start=new CyclicBarrier(2);CountDownLatch done=new CountDownLatch(2);
 for(int ix=0;ix<2;ix++){final int i=ix;new Thread(()->{try{start.await();Predicate<String> conflict=i==0?JobFundal.conflictBloc(client):JobFundal.conflictScriere(client);got[i]="bypass".equals(mode)||JobFundal.ocupaExclusiv(keys[i],conflict);}catch(Exception e){throw new RuntimeException(e);}finally{done.countDown();}}).start();}
 done.await();System.out.println("RESULT "+got[0]+" "+got[1]);System.out.flush();
 if(new BufferedReader(new InputStreamReader(System.in)).readLine()==null)System.exit(3);
 if(!"bypass".equals(mode)){int winner=got[0]?0:1; int loser=1-winner;Predicate<String> conflict=loser==0?JobFundal.conflictBloc(client):JobFundal.conflictScriere(client);boolean repeat=JobFundal.ocupaExclusiv(keys[loser],conflict);JobFundal.elibereaza(keys[winner]);boolean after=JobFundal.ocupaExclusiv(keys[loser],conflict);if(after)JobFundal.elibereaza(keys[loser]);System.out.println("RELEASE "+repeat+" "+after);System.out.flush();}
 }}'''
p=E6/'JobR6.java';p.write_text(code,encoding='utf8')
def go(t,j,db,m,phase):
 dest=T/('jobr6_'+t);dest.mkdir(exist_ok=True);cp=';'.join(map(str,[dest,j,base,'D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*']));cc=execute([java/'javac.exe','-encoding','UTF-8','-sourcepath','','-cp',cp,'-d',dest,p],T);assert cc.returncode==0,cc.stdout
 cmd=[java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-cp',cp,'com.eva.ro.contab.form.JobR6',m]
 before=connect(db);a,b=connect(db),connect(db);choices=[a,b];rows=[];seq='select txid_current(), pg_backend_pid(), (select count(*) from audit_marker where scenario=%s)'
 for c in choices:rows.append(c.execute(seq,(phase,)).fetchone())
 assert rows[0][0]!=rows[1][0]and rows[0][1]!=rows[1][1]and rows[0][2]==rows[1][2]==0
 proc=sp.Popen(list(map(str,cmd)),cwd=T,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,encoding='utf8');result=proc.stdout.readline().strip()
 if not result.startswith('RESULT'):raise RuntimeError(str((result,proc.stderr.read()[:500])))
 got=[(v=='true')for v in result.split()[1:]];assert sum(got)==(2 if m=='bypass'else 1)
 for i,c in enumerate(choices):
  if got[i]:c.execute('insert into audit_marker(scenario,actor) values(%s,%s)',(phase,i))
  if phase.endswith('_rollback')and got[i]:c.rollback()
  else:c.commit()
 seen=before.execute('select count(*) from audit_marker where scenario=%s',(phase,)).fetchone()[0];before.commit()
 proc.stdin.write('committed\n');proc.stdin.flush();tail=proc.stdout.read().strip();ret=proc.wait(timeout=15);assert ret==0
 if m!='bypass':assert tail=='RELEASE false true',tail
 n=0
 if phase.endswith('_rollback'):
  # Re-reservation after release by the same JVM granted the actual second attempt above; persist only its fixture effect.
  retry=connect(db);retry.execute('insert into audit_marker(scenario,actor) values(%s,%s)',(phase,1 if got[0]else 0));retry.commit();retry.close()
 final=before.execute('select actor from audit_marker where scenario=%s order by actor',(phase,)).fetchall()
 assert seen==(0 if phase.endswith('_rollback')else sum(got));assert len(final)==(2 if m=='bypass'else 1)
 for c in [a,b,before]:c.close()
 return {'target':t,'jar_sha':sha(j),'scenario':phase,'two_pg_sessions_before':rows,'simultaneous_after_barrier':got,'witness_rows_after_first_two_trx':seen,'attempt_while_first_held_and_retry_after_release':tail or None,'final_rows':final,'limit':'Scrierea din audit_marker aparține adaptorului de probă în baza izolată; nu închide în iDempiere o perioadă și nu demonstrează concurența între două JVM.'}
if __name__=='__main__':
 with connect('postgres',True)as x:x.execute('create database '+dbname+' template template0')
 try:
  with connect(dbname)as x:x.execute('create table audit_marker(scenario text not null, actor int not null)');x.commit()
  out=[]
  for tag,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]:
   for m,purpose in [('same','same_key'),('cross','cross_key'),('cross','cross_rollback'),('bypass','mutant_bypass')]:out.append(go(tag,j,dbname,m,tag+'_'+purpose))
 finally:
  with connect('postgres',True)as x:x.execute('drop database '+dbname)
 wr(E6/'T03_concurenta_JobFundal.json',{'inputs':sha(p),'criterion':'T03-R2-039','test_input':'Doi actori sincronizați cu o barieră JVM, două conexiuni PostgreSQL deschise înainte de concurs. Fiecare are PID și tranzacție distincte. Fără unicitate în tabelul martor. Execuție simultană pentru aceeași cheie și pentru bloc vs lună. Caz cu rollback + reîncercare și mutant de bypass.','assertion':'Same/cross: un deținător, un rând; retry cât deține primul e refuzat; după release acceptat. Rollback: 0, după retry 1. Bypass: 2, martorul detectează lipsa gărzii.','production_static_oracle':{'measured':[0,3],'expected':['0','≥5'],'second_condition_match':False},'rows':out,'physical_cabinet_stage':'NU_A_EXECUTAT_INCHIDERE_REALĂ_FISCALĂ','ephemeral_postgres_dropped':True})
 print([(v['target'],v['scenario'],v['witness_rows_after_first_two_trx'],len(v['final_rows']))for v in out])

