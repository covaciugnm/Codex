from pathlib import Path
import subprocess,socket,hashlib,json,datetime,os,sys
ROOT=Path('D:/CodexWork/a05-r12-native-lab-20261103').resolve()
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
BIN=Path('D:/CodexWork/p01-local-pg16/pgsql/bin')
DATA=ROOT/'pgdata';SEED=Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump');PORT=56455
assert not DATA.exists()
assert hashlib.sha256(SEED.read_bytes()).hexdigest()=='54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4'
with socket.socket() as s:
 assert s.connect_ex(('127.0.0.1',PORT))!=0,'Port already occupied; refuse.'
env=dict(os.environ);env['PGPASSWORD']='A05SyntheticOnlyR12';env['PGCONNECT_TIMEOUT']='5'
steps=[];started=False
def run(name,args,input=None,timeout=60):
 r=subprocess.run([str(x)for x in args],capture_output=True,input=input,env=env,timeout=timeout)
 (OUT/(name+'.stdout.txt')).write_bytes(r.stdout);(OUT/(name+'.stderr.txt')).write_bytes(r.stderr)
 steps.append({'step':name,'exit':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()})
 if r.returncode:raise RuntimeError(name+': '+r.stderr.decode(errors='replace')[-2000:])
 return r.stdout
def sql(name,body):return run(name,[BIN/'psql.exe','-X','-qAt','-v','ON_ERROR_STOP=1','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','-d','idempiere'],body.encode())
try:
 passfile=ROOT/'synthetic_password.txt';passfile.write_text(env['PGPASSWORD'],encoding='ascii')
 run('pg_init',[BIN/'initdb.exe','-D',DATA,'-U','a05lab','--auth-host=scram-sha-256','--auth-local=scram-sha-256','--pwfile='+str(passfile),'--encoding=UTF8','--locale=C'])
 with (DATA/'postgresql.conf').open('a')as f:f.write("\nlisten_addresses='127.0.0.1'\nport=56455\nmax_connections=20\nshared_buffers='32MB'\nlogging_collector=off\nstatement_timeout='30s'\nidle_in_transaction_session_timeout='45s'\n")
 run('pg_start',[BIN/'pg_ctl.exe','-D',DATA,'-l',ROOT/'postgres.log','-w','start']);started=True
 run('pg_createdb',[BIN/'createdb.exe','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','idempiere'])
 sql('pg_create_native_role',"CREATE ROLE adempiere LOGIN PASSWORD 'A05SyntheticOnlyR12'; ALTER DATABASE idempiere OWNER TO adempiere; ALTER ROLE adempiere SET search_path=adempiere,pg_catalog;")
 run('pg_restore_seed',[BIN/'pg_restore.exe','--exit-on-error','--no-owner','--no-privileges','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','-d','idempiere',SEED],timeout=180)
 sql('pg_native_ownership',"GRANT ALL ON SCHEMA adempiere TO adempiere; GRANT ALL ON ALL TABLES IN SCHEMA adempiere TO adempiere; GRANT ALL ON ALL SEQUENCES IN SCHEMA adempiere TO adempiere; GRANT ALL ON ALL FUNCTIONS IN SCHEMA adempiere TO adempiere;")
 info=sql('pg_preflight_schema',"SELECT 'SYSTEM|'||version FROM adempiere.ad_system; SELECT 'CLIENT|'||ad_client_id||'|'||value FROM adempiere.ad_client ORDER BY ad_client_id; SELECT 'PROCESSOR|'||t.table_name FROM information_schema.tables t JOIN information_schema.columns c ON c.table_schema=t.table_schema AND c.table_name=t.table_name AND c.column_name='isactive' WHERE t.table_schema='adempiere' AND (t.table_name LIKE '%processor%' OR t.table_name LIKE '%scheduler%'); SELECT 'CLIENTCOL|'||column_name FROM information_schema.columns WHERE table_schema='adempiere' AND table_name='ad_client' AND (column_name LIKE '%mail%' OR column_name LIKE '%smtp%' OR column_name LIKE '%validat%'); SELECT 'MODELVALIDATOR|'||modelvalidationclass FROM adempiere.ad_modelvalidator;")
 print(info.decode())
except BaseException:
 if started:
  try:run('pg_stop_on_error',[BIN/'pg_ctl.exe','-D',DATA,'-m','fast','-w','stop'])
  except BaseException:pass
 raise
finally:
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cluster':str(DATA),'port':PORT,'seed_sha256':hashlib.sha256(SEED.read_bytes()).hexdigest(),'synthetic':True,'started':started,'steps':steps}
 (OUT/'PG_restore_preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'steps':steps,'started':started}))
