from a12_r7_pg_cui import *
import threading,time,uuid
n='a12r7lock_'+uuid.uuid4().hex[:12];assert re.fullmatch('a12r7lock_[a-f0-9]{12}',n)
with db('postgres',True)as p:p.execute('create database '+n+' template template0')
ktr='SELECT 1 FROM (SELECT pg_advisory_xact_lock(%s)) x'
def period(client,yyyy,mm):return client*1000000+yyyy*100+mm
def one(id_,keyb,abort=False,bypass=False):
 aa,bb=db(n),db(n);start=threading.Event();done=threading.Event();w=[]
 original=aa.execute('select txid_current(), pg_backend_pid()').fetchone();ka=period(11,2026,10);assert ka==11202610
 aa.execute(ktr,(ka,));aa.execute('insert into r7marks(run_id,client,yy) values (%s,%s,%s)',(id_,11,'202610'))
 def contender():
  try:
   idb=bb.execute('select txid_current(), pg_backend_pid()').fetchone();w.append(idb); start.set()
   if not bypass:bb.execute(ktr,(keyb,))
   after=bb.execute('select count(*) from r7marks where run_id=%s',(id_,)).fetchone()[0];bb.execute('insert into r7marks(run_id,client,yy) values(%s,11,%s)',(id_,str(keyb)));bb.commit();w.append(after)
  finally:done.set()
 th=threading.Thread(target=contender);th.start();assert start.wait(3)
 if keyb==ka and not bypass:
  lock=[]
  with db(n)as inspector:
   for _ in range(20):
    lock=inspector.execute('select wait_event_type,wait_event from pg_stat_activity where pid=%s',(w[0][1],)).fetchone()
    if lock and str(lock[1]).lower()=='advisory':break
    time.sleep(.025)
  blocked=not done.is_set() and bool(lock and str(lock[1]).lower()=='advisory')
 else:done.wait(1);blocked=not done.is_set()
 if abort:aa.rollback()
 else:aa.commit()
 th.join(4);assert done.is_set();aa.close();bb.close()
 with db(n)as c:count=c.execute('select count(*) from r7marks where run_id=%s',(id_,)).fetchone()[0]
 assert blocked==(keyb==ka and not bypass)
 return {'case':id_,'holder_key':ka,'contender_key':keyb,'same_instance_or_second_process':'PG backend processes have distinct PID and TxID','A':original,'B':w[0],'blocked_before_release':blocked,'A_action':'ROLLBACK'if abort else'COMMIT','B_sees_before_writing':w[1],'rows_final':count,'meaning':'Lacătul serializează; a doua tranzacție poate scrie după el. Prevenirea duplicării cere și garda de stare a operației.'}
try:
 with db(n)as c:c.execute('create table r7marks(run_id text,client int, yy text)');c.commit()
 tests=[one('same_org_month',period(11,2026,10)),one('different_month',period(11,2026,11)),one('different_client',period(12,2026,10)),one('holder_rollback',period(11,2026,10),True),one('bypass_lock',period(11,2026,10),False,True)]
finally:
 with db('postgres',True)as p:p.execute('drop database '+n)
def anchors(p,need):
 ls=p.read_text(encoding='utf8').splitlines();return {'file':p.relative_to(repo).as_posix(),'sha256':sha(p),'lines':[(k,l.strip())for k,l in enumerate(ls,1)if any(s in l for s in need)][:22]}
code=plug/'src/com/eva/ro/contab';srcs=[anchors(code/'form/JobFundal.java',['static synchronized boolean ocupaExclusiv','static final Set<String> IN_CURS','IN_CURS.add(', 'return k -> k.equals(bloc)']),anchors(code/'fiscal/InchidereLuna.java',['public static void lacatLuna','client * 1_000_000L','SELECT 1 FROM (SELECT pg_advisory_xact_lock(?)','lacatLuna(trxName','POARTA ANTI-DUBLARE']),anchors(code/'form/DialogReinchidere.java',['JobFundal.conflictBloc'])];ps=sp.check_output(['ssh','-o','BatchMode=yes',server,'docker ps --format "{{.Names}} {{.Image}}"']).decode();physical=[l for l in ps.splitlines()if l.split()[0]in ['eva-idempiere-cesiro','eva-idempiere-cesiro-ui','eva-postgres-cesiro']];assert len(physical)==3
a11f=E/'A11_reproduceri_R6/independent_jvm.json';wr(RP/'T03_topologie_si_lacat_PG.json',{'utc':datetime.now(UTC).isoformat(),'source_of_two_jvm_oracle':{'file':a11f.relative_to(E.parent).as_posix(),'sha':sha(a11f),'result':'Două JVM pot deține simultan cheia JobFundal. Un proces și două fire nu pot.'},'physical_observed_readonly':physical,'qualification':'Pe cabinetul CESIRO observat, containerul UI este alpine/socat, nu o a doua JVM iDempiere. Nu este inventarul tuturor cabinetelor/viitoarelor replici. JobFundal nu este o blocare distribuită. InchidereLuna.lacatLuna solicită tranzacție și ia un lacăt consultativ separat pe client/lună, pe anumite căi de validare și devalidare; acesta nu acoperă toate operațiile fiscale sau orice efect din etapa dinainte.','evidence_source':srcs,'actual_production_sql_literal':ktr.replace('%s','?'),'postgres_dedicated_fixture':tests,'fixture_dropped':True,'product_conclusion':'Doi deținători JVM sunt reproducibili; dublare reală Fact_Acct/GL_Journal în producție nu a fost demonstrată. Condiția statică 3 din minimum 5 rămâne un defect documentar de acoperire, nu un incident contabil confirmat.'});print([(r['case'],r['blocked_before_release'],r['B_sees_before_writing'],r['rows_final'])for r in tests])

