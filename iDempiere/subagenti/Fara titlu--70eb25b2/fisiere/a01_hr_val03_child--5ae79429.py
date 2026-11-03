from pathlib import Path
import os,sys,json,hashlib,socket,inspect,collections
W=Path(os.environ['A01_WORK']).resolve(); MODE=sys.argv[1]; OUT=Path(os.environ['A01_OUTPUT'])
sys.dont_write_bytecode=True;sys.path[:0]=[str(W/'source/backend'),'D:/CodexWork/eva-a01-fixture-deps']
blocked=collections.Counter();selfs=[]
def guard(event,args):
 if event=='socket.bind':
  addr=args[1]
  if isinstance(addr,tuple) and addr[0]=='127.0.0.1' and addr[1]==0:selfs.append(args[0]);return
  blocked[event]+=1;raise PermissionError('HR fixture denied bind')
 if event=='socket.connect':
  addr=args[1]
  if isinstance(addr,tuple) and addr[:2]==('127.0.0.1',int(os.environ['PGPORT'])):return
  for s in selfs:
   try:
    if isinstance(addr,tuple) and addr[:2]==s.getsockname()[:2]:return
   except OSError:pass
  blocked[event]+=1;raise PermissionError('HR fixture denied nonlocal connection')
 if event=='socket.getaddrinfo' and args[0] not in ('127.0.0.1','::1'):
  blocked[event]+=1;raise PermissionError('HR fixture denied nonlocal DNS')
 if event in ('socket.sendto','subprocess.Popen','os.system','os.startfile'):
  blocked[event]+=1;raise PermissionError('HR fixture denied '+event)
 if event=='open' and not isinstance(args[0],int):
  flags=args[2] if isinstance(args[2],int) else 0
  if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
   p=Path(args[0]).resolve()
   if not p.is_relative_to(W) and str(p).lower() not in ('nul',os.devnull.lower()):
    blocked['write-outside-fixture']+=1;raise PermissionError('HR fixture denied external write')
sys.addaudithook(guard)
if MODE=='original':
 import pytest
 cases=[]
 class Listener:
  def pytest_runtest_logreport(self,report):
   r=report
   if r.when=='call' or (r.outcome!='passed' and r.when in ('setup','teardown')):cases.append({'id':r.nodeid,'stage':r.when,'outcome':r.outcome})
 nodes=['tests/test_hr_payroll.py::test_hrp_tenant_isolation','tests/test_hr_isolation.py::test_isolation_v1_employees','tests/test_hr_isolation.py::test_isolation_v2_employees']
 code=int(pytest.main(['-q','--log-file='+str(W/'pytest.log'),'-p','no:cacheprovider','--tb=short',*nodes],plugins=[Listener()]))
 OUT.write_text(json.dumps({'mode':MODE,'exit':code,'cases':cases,'blocked':dict(blocked)}),encoding='utf8');sys.exit(code)

import psycopg
from sqlalchemy import text,event
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db,SessionLocal,engine
from app import models,auth
from app.idempiere import readdb,tenant_authz
from app.hr_payroll.models import EvaHrEmployee
os.environ['EVA_ENV']='production'
init_db()
with engine.begin() as c:
 c.execute(text('create table if not exists eva_idempiere_client_map (managing_uuid text, tenant_cui text, idempiere_client_id integer, idempiere_org_id integer, idempiere_admin_role_id integer)'))
A='RO11111111';B='RO22222222';CAB_A='cabinet-a';CAB_B='cabinet-b'
with SessionLocal() as db:
 db.add_all([models.Tenant(tenant_cui=A,name='Synthetic A'),models.Tenant(tenant_cui=B,name='Synthetic B'),models.ManagingFirm(eva_uuid=CAB_A,cui='99000001',name='Synthetic Cabinet A',idmp_status='none'),models.ManagingFirm(eva_uuid=CAB_B,cui='99000002',name='Synthetic Cabinet B',idmp_status='none'),models.ManagedFirm(eva_uuid='mf-a',managing_uuid=CAB_A,tenant_cui=A,name='Synthetic A'),models.ManagedFirm(eva_uuid='mf-b',managing_uuid=CAB_B,tenant_cui=B,name='Synthetic B'),models.IamUser(eva_uuid='mgr-a',managing_uuid=CAB_A,name='Synthetic Manager A',email='a@example.invalid',role='manager'),models.IamUser(eva_uuid='mgr-b',managing_uuid=CAB_B,name='Synthetic Manager B',email='b@example.invalid',role='manager'),models.IamUser(eva_uuid='member-a',managing_uuid=CAB_A,name='Synthetic Reader',email='r@example.invalid',role='member'),models.FirmAccess(iam_user_uuid='member-a',managed_firm_uuid='mf-a',app='idempiere',permission='read')]);db.commit()
tokens={k:auth.make_token({'sub':uid,'role':role,'managing_uuid':cab,'email':uid+'@example.invalid','se':0},hours=1) for k,uid,role,cab in [('managerA','mgr-a','manager',CAB_A),('managerB','mgr-b','manager',CAB_B),('readerA','member-a','member',CAB_A)]}
client=TestClient(app,raise_server_exceptions=False);rows=[]
def snap():
 with psycopg.connect(os.environ['A01_GATEWAY_DSN']) as c:
  return {t:c.execute('select row_to_json(t) from '+t+' t order by row_to_json(t)::text').fetchall() for t in ('employees','eva_hr_employee','audit_events','idempotency_keys')}
def native_snap():
 with psycopg.connect(os.environ['A01_NATIVE_OWNER_DSN']) as c:return c.execute('select * from c_bpartner order by c_bpartner_id').fetchall()
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,default=str).encode()).hexdigest()
def call(id,method,path,who,tenant,payload=None,expected=None,headers=None,key=None):
 h={'X-Tenant-Cui':tenant,**(headers or {})}
 if who:h['Authorization']='Bearer '+tokens[who]
 if method=='POST':h['X-Idempotency-Key']=key or ('hr-val03-'+id).ljust(20,'0')
 before=digest(snap());nb=digest(native_snap())
 r=client.request(method,path,headers=h,json=payload)
 try:body=r.json()
 except ValueError:body={'text':r.text[:200]}
 after=digest(snap());na=digest(native_snap())
 row={'id':id,'method':method,'path':path,'actor':who,'tenant':tenant,'status':r.status_code,'expected_status':expected,'matches_expected':expected is None or r.status_code==expected,'body':body,'gateway_before':before,'gateway_after':after,'gateway_unchanged':before==after,'native_before':nb,'native_after':na,'native_unchanged':nb==na,'fresh_connection_verification':True}
 rows.append(row)
 if expected is not None:assert r.status_code==expected,(id,r.status_code,body)
 return r
P1='/api/v1/hr/employees';P2='/api/v1/hr/payroll/v2/employees'
for route,mark in [(P1,'V1'),(P2,'V2')]:
 for who,tenant,suffix in [('managerA',A,'A'),('managerB',B,'B')]:
  call(mark+'-create-'+suffix,'POST',route,who,tenant,{'marca':mark+'-'+suffix,'nume':'Synthetic '+mark+' '+suffix,'salariu_brut':6000},201)
 for who,tenant,own,foreign in [('managerA',A,'A','B'),('managerB',B,'B','A')]:
  r=call(mark+'-list-'+own,'GET',route,who,tenant,expected=200)
  records=r.json()['angajati' if mark=='V1' else 'salariati'];marks={x['marca'] for x in records}
  assert mark+'-'+own in marks and 'NATIVE:SAL:'+own in marks
  assert mark+'-'+foreign not in marks and 'NATIVE:SAL:'+foreign not in marks
  assert not any('ORGZERO' in m or 'OTHERCLIENT' in m or 'INACTIVE' in m for m in marks)
  assert all(x.get('cnp',x.get('cnp_mask',''))!='0000000000001' for x in records)
  rows[-1]['own_eva_and_native_present']=True;rows[-1]['foreign_org0_otherclient_inactive_absent']=True
 call(mark+'-foreign-read','GET',route,'managerA',B,expected=403)
 call(mark+'-foreign-write','POST',route,'managerA',B,{'marca':'FOREIGN-'+mark,'nume':'Forbidden'},403,headers={'X-Role':'hr','X-User-Role':'manager'})
 call(mark+'-anonymous-read','GET',route,None,A,expected=401,headers={'X-Role':'hr','X-User-Role':'manager'})
 call(mark+'-anonymous-write','POST',route,None,A,{'marca':'ANON-'+mark,'nume':'Forbidden'},401,headers={'X-Role':'hr'})
 call(mark+'-reader-own-list','GET',route,'readerA',A,expected=200)

call('V2-reader-spoof-role','POST',P2,'readerA',A,{'marca':'READER-V2','nume':'Forbidden'},403,headers={'X-Role':'hr','X-User-Role':'manager'})
call('V1-reader-default-policy','POST',P1,'readerA',A,{'marca':'READER-V1','nume':'Reader under default member-write policy'},201,headers={'X-Role':'hr'})
os.environ['EVA_IDM_MEMBER_WRITE']='0'
call('V1-reader-memberwrite-disabled','POST',P1,'readerA',A,{'marca':'READER-V1-DENY','nume':'Forbidden'},403,headers={'X-Role':'hr'})
os.environ.pop('EVA_IDM_MEMBER_WRITE')

for route,mark in [(P1,'V1'),(P2,'V2')]:
 def fail_commit(session):raise RuntimeError('SYNTHETIC_COMMIT_ABORT')
 event.listen(SessionLocal.class_,'before_commit',fail_commit)
 try:call(mark+'-rollback-injected','POST',route,'managerA',A,{'marca':'RETRY-'+mark,'nume':'Synthetic rollback'},500,key='hr-rollback-'+mark+'-key')
 finally:event.remove(SessionLocal.class_,'before_commit',fail_commit)
 assert rows[-1]['gateway_unchanged'] and rows[-1]['native_unchanged']
 r=call(mark+'-retry-after-rollback','POST',route,'managerA',A,{'marca':'RETRY-'+mark,'nume':'Synthetic rollback'},201,key='hr-rollback-'+mark+'-key')
 eid=r.json()['eva_uuid']
 r=call(mark+'-idempotent-replay','POST',route,'managerA',A,{'marca':'RETRY-'+mark,'nume':'Synthetic rollback'},201,key='hr-rollback-'+mark+'-key')
 assert r.json()['eva_uuid']==eid and rows[-1]['gateway_unchanged']
 table='employees' if mark=='V1' else 'eva_hr_employee'
 with psycopg.connect(os.environ['A01_GATEWAY_DSN']) as c:assert c.execute('select count(*) from '+table+' where marca=%s',('RETRY-'+mark,)).fetchone()[0]==1

direct=[]
readdb.set_active_client(11);readdb.set_active_db_host(None)
for label,orgs in [('none',None),('empty',[]),('A',[10101]),('B',[20202]),('unknown',[90909])]:
 got=readdb.list_employees_idempiere(org_ids=orgs);marks=[x['marca'] for x in got];direct.append({'case':label,'org_ids':orgs,'marks':marks})
 assert (marks==['NATIVE:SAL:'+label] if label in ('A','B') else marks==[])
readonly=False
try:
 with readdb._conn() as c:c.execute("insert into c_bpartner(c_bpartner_id) values(99999)")
except psycopg.errors.InsufficientPrivilege:readonly=True
assert readonly
with psycopg.connect(os.environ['A01_GATEWAY_DSN']) as c:
 rollback_before=c.execute('select count(*) from employees').fetchone()[0]
 c.execute("update employees set nume='SYNTHETIC_UNCOMMITTED' where marca='V1-A'");c.rollback()
with psycopg.connect(os.environ['A01_GATEWAY_DSN']) as c:
 rollback_after=c.execute('select count(*) from employees').fetchone()[0];unchanged_name=c.execute("select nume from employees where marca='V1-A'").fetchone()[0]
assert rollback_before==rollback_after and unchanged_name=='Synthetic V1 A'
assert all(r['native_unchanged'] for r in rows)
assert all(r['gateway_unchanged'] for r in rows if r['status'] in (401,403,500) or r['method']=='GET')
OUT.write_text(json.dumps({'mode':MODE,'requests':rows,'direct_native_sql':direct,'native_readonly_enforced':readonly,'postgres_rollback_fresh_connection':True,'tenant_context_unmodified':True,'jwt_signer_real_synthetic_secret':True,'erp_mirror':'original IDEMPIERE_MOCK=1; no native writes or live ERP effects','blocked':dict(blocked)},ensure_ascii=False,indent=2),encoding='utf8')
client.close();engine.dispose()
