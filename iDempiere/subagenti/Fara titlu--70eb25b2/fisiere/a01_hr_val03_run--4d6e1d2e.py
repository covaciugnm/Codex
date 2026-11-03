from pathlib import Path
import sys,os,subprocess,socket,tempfile,shutil,json,hashlib,datetime,secrets
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
BASE=Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\R11_fisiere')
OUT=BASE/'HR_izolare_Val03'
if os.environ.get('A01_HR_RUN_LABEL'):OUT=OUT/os.environ['A01_HR_RUN_LABEL']
OUT.mkdir(exist_ok=True)
assert not (OUT/'execution_receipt.json').exists(), 'Use a fresh A01_HR_RUN_LABEL; existing evidence is immutable.'
BIN=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');SRC=Path('D:/CodexWork/a01-r11-hr-frozen');CHILD=Path('D:/CodexWork/a01_hr_val03_child.py')
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
gate=BASE.parent/'R11_plan_delta/A11_verdict_plan_delta_R11_v3.json';assert H(gate)=='57b63643abcea8fcb1c716465a9dcb86e9f89a59ec3940d42035df940db2dd14'
with tempfile.TemporaryDirectory(prefix='a01-hr-val03-',dir='D:/CodexWork') as td:
 w=Path(td).resolve();data=w/'pgdata';started=False
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC','PATHEXT','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE') if k in os.environ}
 env.update(PATH=str(Path(sys.executable).parent)+';'+env.get('SYSTEMROOT','C:/Windows')+'/System32',TEMP=str(w),TMP=str(w),TMPDIR=str(w),HOME=str(w),USERPROFILE=str(w),PYTHONIOENCODING='utf8',PYTHONDONTWRITEBYTECODE='1',PGHOST='127.0.0.1',PGPORT=str(port),PGUSER='a01_owner')
 try:
  p=subprocess.run([str(BIN/'initdb.exe'),'-D',str(data),'-A','trust','-U','a01_owner','--encoding=UTF8','--no-locale'],env=env,capture_output=True,timeout=60);(OUT/'initdb.log').write_bytes(p.stdout+b'\n'+p.stderr);assert p.returncode==0
  started=True
  with (OUT/'start.log').open('wb') as log:
   p=subprocess.run([str(BIN/'pg_ctl.exe'),'-D',str(data),'-l',str(w/'pg.log'),'-o',f'-h 127.0.0.1 -p {port}','-w','start'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=60)
  assert p.returncode==0
  dsn=f'host=127.0.0.1 port={port} user=a01_owner'
  with psycopg.connect(dsn+' dbname=postgres',autocommit=True) as c:
   c.execute('create database a01_native');c.execute('create database a01_gateway');c.execute('create role a01_readonly login')
  ddl='''
create table c_bpartner(c_bpartner_id integer primary key,value text,name text,description text,taxid text,ad_client_id integer,ad_org_id integer,isactive char(1),isemployee char(1));
create table ad_org(ad_org_id integer primary key,ad_client_id integer,value text,name text);
create table ad_orginfo(ad_org_id integer primary key,taxid text);
create table ad_role_orgaccess(ad_role_id integer,ad_org_id integer,isactive char(1));
create table m_warehouse(m_warehouse_id integer primary key,ad_client_id integer,ad_org_id integer);
insert into ad_org values(10101,11,'11111111','Synthetic A'),(20202,11,'22222222','Synthetic B');
insert into ad_orginfo values(10101,'11111111'),(20202,'22222222');
insert into ad_role_orgaccess values(50004,10101,'Y'),(50004,20202,'Y');
insert into m_warehouse values(30101,11,10101),(30202,11,20202);
insert into c_bpartner values
 (1,'NATIVE:SAL:A','Synthetic Native A','Fixture only','0000000000001',11,10101,'Y','Y'),
 (2,'NATIVE:SAL:B','Synthetic Native B','Fixture only','0000000000002',11,20202,'Y','Y'),
 (3,'NATIVE:SAL:ORGZERO','Synthetic Org0','Fixture only','0000000000003',11,0,'Y','Y'),
 (4,'NATIVE:SAL:OTHERCLIENT','Synthetic OtherClient','Fixture only','0000000000004',22,10101,'Y','Y'),
 (5,'NATIVE:SAL:INACTIVE','Synthetic Inactive','Fixture only','0000000000005',11,10101,'N','Y'),
 (6,'NATIVE:NOTSAL:OTHER','Synthetic Nonemployee','Fixture only','0000000000006',11,10101,'Y','N');
grant connect on database a01_native to a01_readonly;
grant usage on schema public to a01_readonly;
grant select on all tables in schema public to a01_readonly;
'''
  (OUT/'fixture_native.sql').write_text(ddl,encoding='utf8')
  with psycopg.connect(dsn+' dbname=a01_native',autocommit=True) as c:c.execute(ddl);version=c.execute('select version()').fetchone()[0]
  native_before=None
  with psycopg.connect(dsn+' dbname=a01_native') as c:native_before=c.execute('select * from c_bpartner order by c_bpartner_id').fetchall()
  results=[]
  for mode in os.environ.get('A01_HR_MODES','original,actors').split(','):
   run=w/mode;run.mkdir();(run/'scratch').mkdir();shutil.copytree(SRC,run/'source')
   ce={**env,'A01_WORK':str(run),'A01_OUTPUT':str(run/'result.json'),'A01_GATEWAY_DSN':dsn+' dbname=a01_gateway','A01_NATIVE_OWNER_DSN':dsn+' dbname=a01_native','TEMP':str(run/'scratch'),'TMP':str(run/'scratch'),'TMPDIR':str(run/'scratch'),'HOME':str(run),'USERPROFILE':str(run),'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','PYTHONSAFEPATH':'1','IDEMPIERE_MOCK':'1','IDEMPIERE_DB_HOST':'127.0.0.1','IDEMPIERE_DB_NAME':'a01_native','IDEMPIERE_DB_USER':'a01_readonly','IDEMPIERE_DB_PASS':'synthetic-unused-trust-auth','EVA_DATABASE_URL':f'postgresql+psycopg://a01_owner@127.0.0.1:{port}/a01_gateway','EVA_JWT_SECRET':secrets.token_hex(32),'EVA_ENV':'test','EVA_TENANT_AUTHZ':'strict','EVA_AUTH_ENFORCE':'0' if mode=='original' else '1','EVA_ANAF_OAUTH_ZILNIC':'0','EVA_OFFICE_STORAGE':str(run/'office')}
   p=subprocess.run([sys.executable,'-X','utf8','-I',str(CHILD),mode],cwd=run/'source/backend',env=ce,capture_output=True,timeout=120)
   (OUT/(mode+'.log')).write_bytes(p.stdout+b'\n'+p.stderr)
   if (run/'result.json').exists():shutil.copyfile(run/'result.json',OUT/(mode+'.json'))
   results.append({'mode':mode,'exit':p.returncode})
   print(mode,p.returncode,flush=True)
   if p.returncode:print(p.stderr.decode('utf8','replace')[-3500:],flush=True)
  with psycopg.connect(dsn+' dbname=a01_native') as c:native_after=c.execute('select * from c_bpartner order by c_bpartner_id').fetchall()
  assert native_after==native_before
 finally:
  if started:
   p=subprocess.run([str(BIN/'pg_ctl.exe'),'-D',str(data),'-m','fast','-w','stop'],env=env,capture_output=True,timeout=30);(OUT/'stop.log').write_bytes(p.stdout+b'\n'+p.stderr);assert p.returncode==0
   shutil.copyfile(w/'pg.log',OUT/'postgres.log')
assert not w.exists()
with socket.socket() as s:
 s.settimeout(.3);closed=s.connect_ex(('127.0.0.1',port))!=0
assert closed
(OUT/'execution_receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'2fe90ed3f128c33dff7cf9f8674e664a70679390','results':results,'native_rows_unchanged':native_before==native_after,'postgres_version':version,'temporary_directory_removed':True,'port_no_longer_listening':True,'fixture_kind':'Fresh PG16 cluster with minimal synthetic native-schema projection; not a full iDempiere runtime. App SQL unchanged; original tests keep SQLite and their original mocks; independent actor run uses gateway PostgreSQL and unmodified tenant_context.','source_manifest_sha256':H(SRC/'source_manifest.json'),'child_sha256':H(CHILD)},indent=2),encoding='utf8')
shutil.copyfile(CHILD,OUT/CHILD.name);shutil.copyfile(Path(__file__),OUT/Path(__file__).name);shutil.copyfile(SRC/'source_manifest.json',OUT/'source_manifest.json')
print('DONE',H(OUT/'execution_receipt.json'),flush=True)
