"""Run with pinned backend deps on PYTHONPATH / local TestClient only. No external socket permitted."""
import os, sys, json, tempfile, secrets, socket, uuid, hashlib, pathlib, datetime, time, shutil, concurrent.futures
from unittest.mock import patch
src=pathlib.Path(os.environ.get('A01_SOURCE',r'D:\CodexWork\eva-audit-p01-readonly-20261102'))
out=pathlib.Path(os.environ.get('A01_OUTPUT',r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\A01'))
out.mkdir(parents=True,exist_ok=True)
deps=pathlib.Path(os.environ.get('A01_DEPS',r'D:\CodexWork\eva-a01-fixture-deps'))
sys.path[:0]=[str(deps),str(src/'backend')]; sys.dont_write_bytecode=True
tmp=tempfile.TemporaryDirectory(prefix='eva-A01-fixture-'); wd=pathlib.Path(tmp.name)
os.environ.update(EVA_ENV='test',EVA_AUTH_ENFORCE='1',EVA_MFA_ENFORCE='1',IDEMPIERE_MOCK='1',EVA_DATABASE_URL='sqlite:///'+str(wd/'db.sqlite3').replace('\\','/'),EVA_OFFICE_STORAGE=str(wd/'office'),SAGA_JOBS_DIR=str(wd/'jobs'),EVA_JWT_SECRET=secrets.token_hex(32),ONLYOFFICE_JWT_SECRET=secrets.token_hex(32),EVA_COMMERCE_SERVICE_TOKEN=secrets.token_hex(32),EVA_ANAF_OAUTH_ZILNIC='0',EVA_TENANT_AUTHZ='strict')
attempted=[]; original_connect=socket.socket.connect
def blocknet(*a,**k):
 if sys._getframe(1).f_code is socket._fallback_socketpair.__code__: return original_connect(*a,**k)
 attempted.append('external-connect-denied'); raise OSError('A01 isolated fixture permits no network')
socket.socket.connect=blocknet; socket.create_connection=blocknet
from app.main import app
from app import auth
from app.db import Base,engine,SessionLocal
from app.models import IamUser,IamCredential,ManagingFirm,ManagedFirm,FirmAccess,CommerceStore,OfficeDocument,AuditEvent
from app.routers import cabinets
from fastapi.testclient import TestClient
Base.metadata.create_all(engine); cli=TestClient(app,raise_server_exceptions=False); pref='/api/v1'; obs=[]
def token(uid,role,mu,epoch=0):return auth.make_token({'sub':uid,'email':uid+'@example.invalid','role':role,'managing_uuid':mu,'se':epoch})
with SessionLocal() as s:
 for k in 'AB':
  s.add(ManagingFirm(eva_uuid='cab'+k,cui='RO7100000'+str('AB'.index(k)+1),name='cab-'+k,slug='cab'+k)); s.flush()
  for j,cui in enumerate(['RO91919191','RO8191919'+str('AB'.index(k)+1)]):s.add(ManagedFirm(eva_uuid=k+str(j),managing_uuid='cab'+k,tenant_cui=cui,name='firma-'+k+str(j)))
  for user,role in [('mgr','manager'),('tl','team_leader'),('mem','member')]:
   uid=k+user;s.add(IamUser(eva_uuid=uid,managing_uuid='cab'+k,email=uid.lower()+'@example.invalid',name=uid,role=role,team_leader_uuid=k+'mgr' if role=='member' else None));s.add(IamCredential(iam_user_uuid=uid,password_hash=auth.hash_password('FixturePasswordOr1ginal!')))
 s.add(CommerceStore(eva_uuid='channelB',channel_code='channel-B',tenant_cui='RO81919192',subdomain='B-before'))
 s.add(CommerceStore(eva_uuid='sharedB',channel_code='B-shared-canary',tenant_cui='RO91919191',subdomain='B-shared-canary'))
 s.commit()
am=token('Amgr','manager','cabA');bm=token('Bmgr','manager','cabB');al=token('Atl','team_leader','cabA'); member=token('Amem','member','cabA')
def request(code,method,route,user=None,data=None,headers=None,allowed=(),pick=None):
 trace='A01-'+code; h={'X-Trace-Id':trace,**(headers or {})};
 if user: h['Authorization']='Bearer '+user
 start=time.perf_counter();resp=cli.request(method,pref+route,headers=h,json=data);elapsed=round((time.perf_counter()-start)*1000,1)
 try:body=resp.json()
 except ValueError:body={}
 detail=pick(body) if pick and resp.status_code<400 else (body.get('error',{}).get('code') if isinstance(body,dict) else None)
 obs.append(dict(id=code,method=method,route=route,status=resp.status_code,expected_status=list(allowed),comparison='MATCH' if resp.status_code in allowed else 'DIFF',observed=detail,trace=resp.headers.get('X-Trace-Id'),ms=elapsed));return resp
def record(code,expected,actual):obs.append(dict(id=code,expected=expected,observed=actual,comparison='MATCH' if actual==expected else 'DIFF'))
def read_user(uid):
 with SessionLocal() as s:
  user=s.query(IamUser).filter_by(eva_uuid=uid).one();cred=s.query(IamCredential).filter_by(iam_user_uuid=uid).one();return {'cabinet':user.managing_uuid,'role':user.role,'active':user.active,'epoch':cred.token_epoch,'mfa':cred.mfa_enabled}
request('T01','GET','/auth/me',allowed=[401]); request('T02','GET','/auth/me',am,allowed=[200],pick=lambda b:b['user']['role']);request('T03','GET','/auth/me',am+'x',allowed=[401]);request('T04','GET','/auth/me',auth.make_refresh_token('Amgr'),allowed=[401]);request('T05','GET','/auth/me',auth.make_token({'sub':'Amgr'},hours=-1),allowed=[401]);request('T06','PUT','/stores/channel-B',data={'subdomain':'none'},headers={'X-User-Role':'super'},allowed=[401]);request('T07','GET','/managing-firms/cabB/users',am,headers={'X-User-Role':'super'},allowed=[403]);
for name,email in [('T08','missing@example.invalid'),('T09','amgr@example.invalid')]:request(name,'POST','/auth/login',data={'email':email,'password':'wrong'},allowed=[401]);
request('T10','GET','/stores/channel-B',am,allowed=[403]); request('T11','PUT','/stores/channel-B',member,{'subdomain':'A-overwrote-B'},allowed=[403,404],pick=lambda b:b.get('subdomain'))
with SessionLocal() as s:record('T12','B-before',s.query(CommerceStore).filter_by(channel_code='channel-B').one().subdomain)
request('T13','GET','/stores',am,allowed=[200],pick=lambda b:[x['channel_code'] for x in b['stores']]);record('T14',False,'B-shared-canary' in obs[-1]['observed']);
request('T15','POST','/users/Amem/access',member,{'managed_firm_uuid':'B1','app':'both','permission':'write'},allowed=[403,404],pick=lambda b:[b.get('permission'),b.get('managed_firm')]);
with SessionLocal() as s:record('T16',0,s.query(FirmAccess).filter_by(iam_user_uuid='Amem',managed_firm_uuid='B1').count())
request('T17','GET','/auth/can?tenant_cui=RO81919192&perm=write',member,allowed=[200],pick=lambda b:b.get('allowed'));record('T18',False,obs[-1]['observed']);
request('T19','DELETE','/users/Amem/access/B1',al,allowed=[403,404],pick=lambda b:b.get('removed'))
request('T20','POST','/auth/register',data={'name':'synthetic registration','email':'uninvited@example.invalid','password':'FixturePasswordOnly!','cui':'RO71000002'},allowed=[400,403,409],pick=lambda b:[b['user']['role'],b['user']['managing_uuid'],b['managing_firm']['name']]);
with SessionLocal() as s: record('T21',0,s.query(IamUser).filter_by(managing_uuid='cabB',email='uninvited@example.invalid',role='manager').count())
request('T22','POST','/auth/logout-all',am,allowed=[200],pick=lambda b:b.get('token_epoch'));request('T23','GET','/auth/me',am,allowed=[401]);request('T24','POST','/auth/refresh',data={'refresh_token':auth.make_refresh_token('Amgr',epoch=0)},allowed=[401]);request('T25','GET','/managing-firms/cabA/users',am,allowed=[401],pick=lambda b:b.get('count'));request('T26','PUT','/stores/channel-B',am,{'subdomain':'revoked-mutated-B'},allowed=[401],pick=lambda b:b.get('subdomain'));
request('T27','POST','/auth/password',bm,{'old_password':'FixturePasswordOr1ginal!','new_password':'NewFixturePasswordOnly!'},allowed=[200]);request('T28','GET','/auth/me',bm,allowed=[401],pick=lambda b:b['user']['role']);record('T29',1,read_user('Bmgr')['epoch']);
with SessionLocal() as s: u=s.query(IamUser).filter_by(eva_uuid='Atl').one();u.active='N';s.commit()
request('T30','GET','/auth/me',al,allowed=[401]);request('T31','PUT','/stores/channel-B',al,{'subdomain':'inactive-mutated-B'},allowed=[401],pick=lambda b:b.get('subdomain'));
request('T32','POST','/office/onlyoffice/callback',data={'key':'canary-job','status':2},allowed=[401]);request('T33','POST','/office/onlyoffice/callback',data={'key':'canary-job','status':2},headers={'Authorization':'Bearer invalid-fixture'},allowed=[401],pick=lambda b:b.get('error'));
with SessionLocal() as s:record('T34',0,s.query(AuditEvent).filter_by(action='office.onlyoffice_callback',entity_id='canary-job').count());
jobdir=pathlib.Path(cabinets._FIRMJOBS_DIR);jobdir.mkdir(parents=True,exist_ok=True);jid='Bfixture-owned';pathlib.Path(cabinets._firmjob_path(jid)).write_text(json.dumps({'job_id':jid,'cabinet':'cabB','state':'confirmed','log':['canary-B-job']}),encoding='utf-8');request('T35','GET','/admin/cabinets/firms/job/'+jid,member,allowed=[403,404],pick=lambda b:[b.get('cabinet'),b.get('log')]);
service=os.environ['EVA_COMMERCE_SERVICE_TOKEN'];request('T36','PUT','/stores/channel-B',service,{'subdomain':'svc-wrote'},allowed=[403,404],pick=lambda b:b.get('subdomain'));request('T37','DELETE','/users/Bmem/access/B1',service,allowed=[401,403],pick=lambda b:b.get('removed'));
with SessionLocal() as s: sec=auth.generate_totp_secret();cred=s.query(IamCredential).filter_by(iam_user_uuid='Bmem').one();cred.totp_secret=sec;cred.mfa_enabled='Y';s.commit()
bmem=token('Bmem','member','cabB');request('T38','POST','/auth/login',data={'email':'bmem@example.invalid','password':'FixturePasswordOr1ginal!'},allowed=[401]);request('T39','POST','/auth/mfa/enroll',bmem,allowed=[401,403,409],pick=lambda b:b.get('status'));record('T40','Y',read_user('Bmem')['mfa']);
from app.idempiere import perms
record('T41','member',perms.normalize_role('unknown-audit-role'));
newam=token('Amgr','manager','cabA',1); h={'X-Tenant-Cui':'RO91919191','X-Idempotency-Key':'same-idem-fixture-00001'};before={'filename':'A-only-canary.txt','content':'A-only-data','mime':'text/plain'};other={'filename':'B-requested.txt','content':'B-different','mime':'text/plain'};
d1=request('T42','POST','/office/documents',newam,before,h,[201],lambda b:b['eva_uuid']);d2=request('T43','POST','/office/documents',bm,other,h,[201,409],lambda b:b.get('eva_uuid'));record('T44',False,d1.json().get('eva_uuid')==d2.json().get('eva_uuid') and d1.status_code==201 and d2.status_code==201);
request('T45','GET','/office/documents',bm,headers={'X-Tenant-Cui':'RO91919191'},allowed=[200],pick=lambda b:[x['filename'] for x in b['documents']]);record('T46',False,'A-only-canary.txt' in (obs[-1]['observed'] or []));
request('T47','GET','/office/documents',newam,headers={'X-Tenant-Cui':'RO81919192'},allowed=[403]);request('T48','GET','/office/documents',newam,allowed=[400]);
def refresh_race(i): return cli.post(pref+'/auth/refresh',json={'refresh_token':auth.make_refresh_token('Amgr',epoch=0)}).status_code
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:record('T49',[401,401],list(pool.map(refresh_race,[1,2])));
request('T50','GET','/managing-firms/cabB/users',newam,headers={'X-Tenant-Cui':'RO81919192'},allowed=[403]);
request('T51','POST','/auth/refresh',data={'refresh_token':newam},allowed=[401]);
request('T52','POST','/office/documents',newam,{'filename':'../synthetic.html','mime':'text/html','content':'<b>fixture</b>'},{'X-Tenant-Cui':'RO91919191','X-Idempotency-Key':'fixture-upload-html-000001'},[201,400,415],lambda b:b.get('version'));
record('T54',False,perms.read_org0_allowed('C_Invoice',True));record('T55',False,perms.read_org0_allowed('M_Product',False)); record('T56',False,perms.read_org0_allowed('EVA_PrivateSynthetic',False));
from app.errors import EvaError
for cid,f in [('T57',lambda:perms.assert_can_docaction('member','C_Invoice','CO')),('T58',lambda:perms.filter_write_fields('C_Invoice',{'DocStatus':'CO'})),('T59',lambda:perms.assert_not_doc_generic_write('C_Invoice'))]:
 try:f();denied=False
 except EvaError:denied=True
 record(cid,True,denied)
class ProvisionStub:
 def raise_for_status(self):pass
 def json(self):return {'rest_url':'https://fixture.invalid','idempiere':'synthetic-container','postgres':'synthetic-db'}
boundary=[]
def provisioning(url,**kwargs):boundary.append({'operation':'POST /cabinets','slug':kwargs['json'].get('slug')});return ProvisionStub()
with patch.object(cabinets,'REGISTRY',str(wd/'registry'/'cabinets.json')),patch.object(cabinets.httpx,'post',provisioning):
 request('T60','POST','/cabinets',member,{'slug':'a01test','name':'synthetic','cui':'RO71000001'},allowed=[403],pick=lambda b:b.get('cabinet',{}).get('slug'));record('T61',0,len(boundary));record('T62',False,(wd/'registry'/'cabinets.json').exists());
from sqlalchemy import text,event
with SessionLocal() as s:
 s.execute(text('create table if not exists eva_idempiere_client_map (tenant_cui text, managing_uuid text, idempiere_client_id integer)'));s.commit()
def bench(size):
 with SessionLocal() as s:
  for i in range(size):
   k='perf'+str(i)
   if s.query(ManagedFirm).filter_by(eva_uuid=k).first():continue
   cui='RO67000'+str(i).zfill(3);s.add(ManagedFirm(eva_uuid=k,managing_uuid='cabB',tenant_cui=cui,name='fixture'));s.add(FirmAccess(iam_user_uuid='Btl',managed_firm_uuid=k,app='both',permission='read'));s.execute(text('insert into eva_idempiere_client_map values (:c,:m,:i)'),{'c':cui,'m':'cabB','i':1000000+i});
  s.commit()
 queries=[]
 def count(*a):queries.append(1)
 event.listen(engine,'before_cursor_execute',count);times=[];tot=[];claims=token('Btl','team_leader','cabB');
 try:
  for j in range(5):
   n=len(queries);prev=time.perf_counter();r=cli.get(pref+'/auth/me',headers={'Authorization':'Bearer '+claims});times.append(round((time.perf_counter()-prev)*1000,2));tot.append(len(queries)-n);assert r.status_code==200 and len(r.json()['access'])==size
 finally:event.remove(engine,'before_cursor_execute',count)
 return {'grants':size,'runs':5,'sql_per_request':tot,'elapsed_ms':times,'scope':'single-process SQLite synthetic /auth/me; production SLA is not defined'}
benchmarks=[bench(1),bench(60)]
with SessionLocal() as s:
 files=[{'filename':d.filename,'mime':d.mime,'path_stays_scoped':pathlib.Path(d.content_path).resolve().is_relative_to((wd/'office').resolve()),'size':pathlib.Path(d.content_path).stat().st_size} for d in s.query(OfficeDocument).all()]; record('T53',True,all(x['path_stays_scoped'] for x in files));
# Exercise Flask's real routes/decorators; substitute only the HTTP transport to the local ASGI client.
import importlib.util, urllib.request, urllib.error, urllib.parse, io
sys.path.insert(0,str(src/'frontend')); spec=importlib.util.spec_from_file_location('a01_fixture_front',src/'frontend'/'app.py');front=importlib.util.module_from_spec(spec); spec.loader.exec_module(front)
transport=[]; children=[]; screens=[]
def in_process(req,*args,**kwargs):
 url=req.full_url if hasattr(req,'full_url') else str(req); u=urllib.parse.urlsplit(url)
 if not url.startswith(front.EVA_API):raise OSError('unapproved upstream')
 hdr=dict(req.header_items()) if hasattr(req,'header_items') else {}; meth=req.get_method() if hasattr(req,'get_method') else 'GET'; resp=cli.request(meth,u.path+('?' + u.query if u.query else ''),headers=hdr,content=getattr(req,'data',None));transport.append({'path':u.path,'http':resp.status_code});
 if resp.status_code>=400:raise urllib.error.HTTPError(url,resp.status_code,'fixture',{'Content-Type':'application/json'},io.BytesIO(resp.content))
 return io.BytesIO(resp.content)
def no_child(args,*aa,**kw):children.append({'command':pathlib.Path(str(args[2])).name if len(args)>2 else 'unknown','tenant_arg_present':'--cui' in args,'explicit_cabinet':'--managing-uuid' in args,'dry_run':'--dry-run' in args});raise OSError('fixture interceptor: no processes or Docker started')
def screen(name,c,path,expected,**kw):
 r=c.get(path,base_url='http://acc.eva-org.com',**kw); body=r.get_data(as_text=True); screens.append({'id':name,'route':path,'HTTP':r.status_code,'expected_status':expected,'location':r.headers.get('Location'),'content_type':r.content_type,'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'visible_error_runner':'fixture interceptor' in body,'contains_done':'done' in body,'body_chars':len(body)});return r
with patch.object(front._urlreq,'urlopen',in_process),patch.object(front.subprocess,'Popen',no_child):
 anon=front.app.test_client(); screen('U01',anon,'/app/remote',[302]); screen('U02',anon,'/71000001/81919191/CanalA',[200,302]);
 anon.set_cookie('eva_token','invalid-fixture',domain='acc.eva-org.com');screen('U03',anon,'/app/remote',[302]);
 fm=front.app.test_client();fm.set_cookie('eva_token',member,domain='acc.eva-org.com');screen('U04',fm,'/app/adminer',[403]);
 screen('U05',fm,'/app/api/saga/bootstrap/stream?cui=RO81919192&name=Fixture&schema=saga_fixture',[403]);
 def interrupted(req,*args,**kwargs):
  if urllib.parse.urlsplit(req.full_url).path.endswith('/saga/cabinet-instance'):raise OSError('simulated upstream timeout')
  return in_process(req,*args,**kwargs)
 with patch.object(front._urlreq,'urlopen',interrupted):
  screen('U08',fm,'/app/api/saga/bootstrap/stream?cui=RO81919192&name=Fixture&schema=saga_fixture',[403,502,503]);
 from werkzeug.exceptions import NotFound
 for no,route in enumerate(['/71000001','/71000001/81919191','/71000001/81919191/CanalA'],9):
  try:match=front.app.url_map.bind('acc.eva-org.com').match(route)[0]
  except NotFound:match=None
  screens.append({'id':f'U{no:02}','route':route,'Flask_endpoint':match,'scope':'Route matcher only. External edge rewrites require separate evidence.'})
 with front.app.test_request_context('/webui',headers={'Cookie':'eva_idm_cab=cabb'}): screens.append({'id':'U06','operation':'_idm_upstream selecting foreign cabinet cookie, no connection', 'observed':front._idm_upstream(),'limitation':'Host resolution only. No evidence of native login or private records.'});
 # Warm /auth/me in frontend, revoke in backend, and compare portal guard without launching an action.
 cacheuser=token('Btl','team_leader','cabB'); fc=front.app.test_client();fc.set_cookie('eva_token',cacheuser,domain='acc.eva-org.com');
 with front.app.test_request_context('/app/remote',headers={'Cookie':'eva_token='+cacheuser}): warm=front._me_role_user()[0]
 rc=cli.post(pref+'/auth/logout-all',headers={'Authorization':'Bearer '+cacheuser}); realme=cli.get(pref+'/auth/me',headers={'Authorization':'Bearer '+cacheuser})
 with front.app.test_request_context('/app/remote',headers={'Cookie':'eva_token='+cacheuser}): post=front._me_role_user()[0]
 screens.append({'id':'U07','warm_role':warm,'logout HTTP':rc.status_code,'upstream_me_after_logout':realme.status_code,'role_cached_after_logout':post,'cache_configured_seconds':getattr(front,'_ME_CACHE_TTL',None)})
result={'sha':'6df998aee0e514d30856c461962afe99ebd0d113','timestamp_utc':datetime.datetime.now(datetime.UTC).isoformat(),'environment':'Complete imported FastAPI app through ASGI TestClient, real production auth/tenant guards with enforced switches, isolated SQLite, mock iDempiere, external network disabled. No conftest or tenant_context stub. Flask requests with real decorators, HTTP transported to same ASGI app. Process launch intercepted without Docker or machine access.','versions':{},'external_connect_attempts_blocked':len(attempted),'checks':obs,'frontend':screens,'frontend_transport':transport,'intercepted_child_processes':children,'provisioner_boundary':boundary,'benchmarks':benchmarks,'uploaded_files':files,'DB_cleanup':False}
from importlib.metadata import version
for n in ['fastapi','sqlalchemy','starlette','httpx','pydantic']:result['versions'][n]=version(n)
cli.close();engine.dispose();tmp.cleanup();result['DB_cleanup']=not wd.exists();
(out/'fixture_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('checks',len(obs),'DIFF',sum(x['comparison']=='DIFF' for x in obs),'cleanup',result['DB_cleanup']);
