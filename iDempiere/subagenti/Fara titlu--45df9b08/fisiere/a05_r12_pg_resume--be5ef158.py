from pathlib import Path
import subprocess,socket,hashlib,json,datetime,os
ROOT=Path('D:/CodexWork/a05-r12-native-lab-20261103').resolve()
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
BIN=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');DATA=ROOT/'pgdata';SEED=Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump');PORT=56455
assert DATA.is_dir() and not(DATA/'postmaster.pid').exists()
env=dict(os.environ);env['PGPASSWORD']='A05SyntheticOnlyR12';env['PGCONNECT_TIMEOUT']='5'
steps=[];started=False
def run(name,args,input=None,timeout=60):
 name='v2_'+name
 stdout=OUT/(name+'.stdout.txt');stderr=OUT/(name+'.stderr.txt');assert not stdout.exists()
 with stdout.open('wb')as so,stderr.open('wb')as se:
  r=subprocess.run([str(x)for x in args],stdout=so,stderr=se,input=input,env=env,timeout=timeout)
 steps.append({'step':name,'exit':r.returncode,'stdout_sha256':hashlib.sha256(stdout.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(stderr.read_bytes()).hexdigest()})
 if r.returncode:raise RuntimeError(name+': '+stderr.read_text(errors='replace')[-2000:])
 return stdout.read_bytes()
def sql(name,body):return run(name,[BIN/'psql.exe','-X','-qAt','-v','ON_ERROR_STOP=1','-h','127.0.0.1','-p',str(PORT),'-U','a05lab','-d','idempiere'],body.encode())
try:
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
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cluster':str(DATA),'port':PORT,'seed_sha256':hashlib.sha256(SEED.read_bytes()).hexdigest(),'synthetic':True,'started':started,'steps':steps,'previous_attempt':'Capture pipe inherited by Windows postgres process; native pg_ctl had returned. Own cluster stopped explicitly and restarted with real file descriptors.'}
 (OUT/'PG_restore_preflight_v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'steps':steps,'started':started}))
