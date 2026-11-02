"""Independent DB engine repeat of R1 against a disposable DB created by this script only."""
import os,pathlib,uuid,subprocess,tempfile,sys,hashlib,json,datetime
W=pathlib.Path(os.environ.get('A01_WORK',r'D:\CodexWork\eva_a01_r2_work'));W.mkdir(parents=True,exist_ok=True)
BASE=pathlib.Path(os.environ.get('A01_CASE_SOURCE',r'D:\CodexWork\a01_probe.py')); root=pathlib.Path(os.environ.get('A01_PG_ROOT',r'D:\CodexWork\p01-local-pg16'))
name='a01_r2_'+uuid.uuid4().hex[:16]; host='127.0.0.1'; port='56481'; user='audit_owner'; env={**os.environ,'PGPASSFILE':str(root/'pgpass.conf')}; psql=root/'pgsql/bin/psql.exe'
def sql(db,query):
 r=subprocess.run([str(psql),'-X','-q','-A','-t','-v','ON_ERROR_STOP=1','-h',host,'-p',port,'-U',user,'-d',db,'-c',query],env=env,capture_output=True,text=True,timeout=24);assert r.returncode==0,'PG SQL failed. No connection string or credentials logged.';return r.stdout.strip()
assert name.startswith('a01_r2_') and len(name)==23 and name[7:].isalnum(); assert sql('postgres',"SELECT count(*) FROM pg_database WHERE datname='"+name+"'")=='0'; sql('postgres','CREATE DATABASE '+name); made=True; recorded=[]
try:
 text=BASE.read_text(encoding='utf-8'); marker='from app.main import app'; assert text.count(marker)==1
 text=text.replace(marker,"os.environ['EVA_DATABASE_URL']='postgresql+psycopg://audit_owner@127.0.0.1:56481/"+name+"'\n"+marker)
 marker='Base.metadata.create_all(engine);';assert text.count(marker)==1
 text=text.replace(marker,"from sqlalchemy import text\nwith engine.begin() as early:\n early.execute(text('create table eva_idempiere_client_map (tenant_cui text, managing_uuid text, idempiere_client_id integer)'))\n"+marker)
 text=text.replace('isolated SQLite','isolated PostgreSQL 16.15').replace('single-process SQLite synthetic','single-process PostgreSQL 16.15 synthetic')
 dst=W/'repeat_pg_generated.py'; dst.write_text(text,encoding='utf-8');p=subprocess.run([sys.executable,'-B',str(dst)],env={**env,'A01_OUTPUT':str(W)},capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=210)
 (W/'postgres_attempt.log').write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,'Fixture stopped; review postgres_attempt.log locally.'
 recorded=[{'case':'anonymous registration joined B','observed':sql(name,"SELECT managing_uuid||'|'||role FROM iam_users WHERE email='uninvited@example.invalid'")},{'case':'canal B after revoked/inactive/service operations','observed':sql(name,"SELECT subdomain FROM commerce_stores WHERE channel_code='channel-B'")},{'case':'only one office document for idempotency collision, standalone SQL','observed':sql(name,"SELECT count(*) FROM office_documents WHERE filename IN ('A-only-canary.txt','B-requested.txt')")},{'case':'B requested document was never created','observed':sql(name,"SELECT count(*) FROM office_documents WHERE filename='B-requested.txt'")},{'case':'callback fake created one audit event','observed':sql(name,"SELECT count(*) FROM audit_events WHERE action='office.onlyoffice_callback' AND entity_id='canary-job'")},{'case':'epoch A vs B after logout-all / password change','observed':sql(name,"SELECT iam_user_uuid||'|'||token_epoch FROM iam_credentials WHERE iam_user_uuid IN ('Amgr','Bmgr') ORDER BY iam_user_uuid")}];
finally:
 if made:sql('postgres','DROP DATABASE '+name)
 assert sql('postgres',"SELECT count(*) FROM pg_database WHERE datname='"+name+"'")=='0'
fx=json.loads((W/'fixture_results.json').read_text(encoding='utf-8'));fx['postgres_independent_SQL']=recorded;fx['postgres_cleanup_verified']=True;fx['pg_version']=sql('postgres',"SELECT current_setting('server_version')");fx['harness_original_sha256']=hashlib.sha256(BASE.read_bytes()).hexdigest();fx['harness_generated_sha256']=hashlib.sha256(dst.read_bytes()).hexdigest();fx['meaning']='Fresh reproducible R2 ASGI+Flask replay on locally created PostgreSQL. Mock only iDempiere, egress denied, no writes to another database. Not an independent A11 signoff.';(W/'postgres_repeat.json').write_text(json.dumps(fx,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Executed',len(fx['checks']),'assertions and',len(fx['frontend']),'frontend cases. PostgreSQL cleanup confirmed.')
