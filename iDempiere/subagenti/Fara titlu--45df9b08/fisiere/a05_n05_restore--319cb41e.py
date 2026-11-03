from pathlib import Path
import subprocess,socket,hashlib,json,datetime,os,sys
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
OUT=R/'executie/R12_fisiere/A05_N05_lot03'
gate=R/'executie/R12_fisiere/A11/Val03_preflight/Verdict_A11_protocol_N05_v2.json'
assert hashlib.sha256(gate.read_bytes()).hexdigest()=='d92aed9631986da6d1ec5652e114810f350a1ac49902e62e3b0b7ca226b36230'
ROOT=Path('D:/CodexWork/a05-r12-native-lab-n05-20261103').resolve();assert not ROOT.exists();ROOT.mkdir()
BIN=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');DATA=ROOT/'pgdata';SEED=Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump');PORT=56455
assert hashlib.sha256(SEED.read_bytes()).hexdigest()=='54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4'
with socket.socket() as s:assert s.connect_ex(('127.0.0.1',PORT))!=0,'Port occupied; refuse.'
env=dict(os.environ,PGPASSWORD='A05SyntheticOnlyR12',PGCONNECT_TIMEOUT='5');steps=[];started=False
def run(name,args,input=None,timeout=60):
 so=OUT/(name+'.stdout.txt');se=OUT/(name+'.stderr.txt');assert not so.exists()
 with so.open('wb')as a,se.open('wb')as b:r=subprocess.run([str(x)for x in args],stdout=a,stderr=b,input=input,env=env,timeout=timeout)
 steps.append({'step':name,'exit':r.returncode,'stdout_sha256':hashlib.sha256(so.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(se.read_bytes()).hexdigest()})
 if r.returncode:raise RuntimeError(name+': '+se.read_text(errors='replace')[-2000:])
 return so.read_bytes()
def sql(name,body):return run(name,[BIN/'psql.exe','-X','-qAt','-v','ON_ERROR_STOP=1','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','-d','idempiere'],body.encode())
try:
 pw=ROOT/'synthetic_password.txt';pw.write_text(env['PGPASSWORD'],encoding='ascii')
 run('pg_init',[BIN/'initdb.exe','-D',DATA,'-U','a05lab','--auth-host=scram-sha-256','--auth-local=scram-sha-256','--pwfile='+str(pw),'--encoding=UTF8','--locale=C'])
 with(DATA/'postgresql.conf').open('a')as f:f.write("\nlisten_addresses='127.0.0.1'\nport=56455\nmax_connections=25\nshared_buffers='32MB'\nlogging_collector=off\nstatement_timeout='30s'\nidle_in_transaction_session_timeout='45s'\n")
 run('pg_start',[BIN/'pg_ctl.exe','-D',DATA,'-l',ROOT/'postgres.log','-w','start']);started=True
 run('pg_createdb',[BIN/'createdb.exe','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','idempiere'])
 sql('pg_create_native_role',"CREATE ROLE adempiere LOGIN PASSWORD 'A05SyntheticOnlyR12'; ALTER DATABASE idempiere OWNER TO adempiere; ALTER ROLE adempiere SET search_path=adempiere,pg_catalog;")
 run('pg_restore_seed',[BIN/'pg_restore.exe','--exit-on-error','--no-owner','--no-privileges','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','-d','idempiere',SEED],timeout=180)
 # Metadata synchronization may ALTER TABLE: ownership must be native role, not only DML grants.
 sql('pg_native_ownership',"REASSIGN OWNED BY a05lab TO adempiere; GRANT ALL ON SCHEMA adempiere TO adempiere; GRANT ALL ON ALL TABLES IN SCHEMA adempiere TO adempiere; GRANT ALL ON ALL SEQUENCES IN SCHEMA adempiere TO adempiere;")
 before={};changes=[]
 with psycopg.connect(host='127.0.0.1',port=PORT,user='a05lab',password=env['PGPASSWORD'],dbname='idempiere')as conn:
  with conn.cursor()as c:
   c.execute('SET search_path=adempiere,pg_catalog')
   c.execute('SELECT ad_client_id,value FROM ad_client ORDER BY 1');before['clients']=c.fetchall();assert [x[0]for x in before['clients']]==[0,11]
   c.execute('SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1');before['validators']=c.fetchall()
   c.execute("SELECT table_name FROM information_schema.columns WHERE table_schema='adempiere' AND column_name='isactive' AND (table_name LIKE '%processor%' OR table_name LIKE '%scheduler%' OR table_name='rest_authtoken') ORDER BY table_name")
   for(t,)in c.fetchall():
    c.execute(psycopg.sql.SQL("UPDATE {} SET isactive='N' WHERE isactive='Y'").format(psycopg.sql.Identifier('adempiere',t)));changes.append({'table':t,'deactivated':c.rowcount})
   c.execute("UPDATE ad_client SET smtphost='127.0.0.1',smtpport=1,requestemail='synthetic@example.invalid',issmtpauthorization='N',isserveremail='N'")
   c.execute("UPDATE ad_user SET email=NULL,notificationtype='X'")
   c.execute("UPDATE ad_system SET isautoerrorreport='N',isallowstatistics='N',noprocessors=0,dbaddress='jdbc:postgresql://127.0.0.1:56455/idempiere'")
   c.execute('SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1');assert c.fetchall()==before['validators']
   c.execute('SELECT ad_client_id,modelvalidationclasses FROM ad_client ORDER BY 1');before['client_validators_preserved']=c.fetchall()
   c.execute('SELECT version,releaseno,lastbuildinfo,isfailonbuilddiffer,dbaddress FROM ad_system');before['system_after']=c.fetchall()
   c.execute('SELECT ad_role_id,ad_client_id,name,userlevel FROM ad_role ORDER BY 1');before['roles']=c.fetchall()
   c.execute('SELECT ad_user_id,ad_role_id,isactive FROM ad_user_roles ORDER BY 1,2');before['user_roles']=c.fetchall()
 (OUT/'Izolare_seed_v1.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target':str(ROOT),'port':PORT,'before_preserved':before,'deactivated':changes,'limit':'Clone-only readiness; no native or product process started. LastBuildInfo not altered.'},default=str,ensure_ascii=False,indent=2),encoding='utf8')
except BaseException:
 if started:
  try:run('pg_stop_on_error',[BIN/'pg_ctl.exe','-D',DATA,'-m','fast','-w','stop'])
  except BaseException:pass
 raise
finally:
 (OUT/'PG_restore_v1.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(ROOT),'port':PORT,'steps':steps,'started':started},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'started':started,'steps':len(steps),'root':str(ROOT)}))
