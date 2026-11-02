from pathlib import Path
import sys,os,json,tempfile,datetime,uuid,hashlib,threading,urllib.parse,urllib.request,urllib.error,ssl,contextlib,io,socket,logging,posixpath
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from unittest.mock import patch
W=Path(r'D:\CodexWork\a01-r11-frozen');ver=sys.argv[1];root=W/ver;frontend=root/'frontend';oldbackend=Path(r'D:\CodexWork\eva-audit-p01-readonly-20261102\backend');deps=Path(r'D:\CodexWork\eva-a01-fixture-deps');sys.path[:0]=[str(deps),str(oldbackend)];sys.dont_write_bytecode=True;tmp=tempfile.TemporaryDirectory(prefix='a01-r11-local-auth-');os.environ.update(EVA_ENV='test',EVA_AUTH_ENFORCE='1',IDEMPIERE_MOCK='1',EVA_DATABASE_URL='sqlite:///'+str(Path(tmp.name)/'auth.db').replace('\\','/'),EVA_JWT_SECRET=uuid.uuid4().hex*2,EVA_ANAF_OAUTH_ZILNIC='0',NO_PROXY='127.0.0.1,localhost')
from app.main import app as gateway
from app.models import ManagingFirm,IamUser,IamCredential
from app.db import Base,engine,SessionLocal
from app import auth
from fastapi.testclient import TestClient
from importlib import util
sys.path.insert(0,str(frontend));spec=util.spec_from_file_location('fixture_portal_'+ver,frontend/'app.py');portal=util.module_from_spec(spec);spec.loader.exec_module(portal);Base.metadata.create_all(engine);be=TestClient(gateway,raise_server_exceptions=False);tokens={}
with SessionLocal() as s:
 for p,role,epoch in [('a','member',0),('b','manager',0),('revoked','member',1)]:
  m='caba' if p!='b' else 'cabb';
  if not s.query(ManagingFirm).filter_by(eva_uuid=m).first():s.add(ManagingFirm(eva_uuid=m,name='fixture-'+m,cui='RO113' if m=='caba' else 'RO114',slug=m));s.flush()
  s.add(IamUser(eva_uuid=p,name='fixture-'+p,email=p+'@example.invalid',managing_uuid=m,role=role));s.add(IamCredential(iam_user_uuid=p,password_hash=auth.hash_password('fixture-pass-'+p),token_epoch=epoch));tokens[p]=auth.make_token({'sub':p,'role':role,'email':p+'@example.invalid','managing_uuid':m,'se':0})
 s.commit()
wire=[];authcalls=[];current={'case':'-'};ports={};
class Receiver(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_HEAD(self):self.do_GET()
 def do_POST(self):self.do_GET()
 def do_GET(self):
  path=urllib.parse.urlsplit(self.path).path;cab=self.server.audit_cab;wire.append({'case':current['case'],'host':cab,'raw_request_target':self.path,'method':self.command,'session_cookie_forwarded':bool(self.headers.get('Cookie')),'body_bytes':len(self.rfile.read(int(self.headers.get('Content-Length','0')))),'query':urllib.parse.urlsplit(self.path).query});
  if path=='/webui/redirect-inside': status,loc=302,'/webui/zkau/web/js/zk.wpd'
  elif path=='/webui/redirect-outside':status,loc=302,'/osgi/synthetic-marker'
  elif path=='/webui/redirect-other':status,loc=302,'http://localhost:'+str(ports['cabb'])+'/synthetic-marker'
  else:status,loc=200,None
  body=('fixture:'+cab+':'+path).encode();self.send_response(status);self.send_header('Content-Type','text/plain');self.send_header('Content-Length',str(len(body)));self.send_header('Set-Cookie','JSESSIONID=fixture; Path=/webui; Secure; HttpOnly');
  if loc:self.send_header('Location',loc)
  self.end_headers();
  if self.command!='HEAD':self.wfile.write(body)
servers=[]
for cab in ['caba','cabb','shared']:
 s=ThreadingHTTPServer(('127.0.0.1',0),Receiver);s.audit_cab=cab;ports[cab]=s.server_port;servers.append(s);threading.Thread(target=s.serve_forever,daemon=True).start()
orig_open=urllib.request.urlopen
def transport(req,**kwargs):
 u=urllib.parse.urlsplit(req.full_url); 
 if req.full_url.startswith(portal.EVA_API):
  r=be.request(req.get_method(),u.path+('?'+u.query if u.query else ''),headers=dict(req.header_items()));authcalls.append({'case':current['case'],'path':u.path,'status':r.status_code});
  if r.status_code>=400:raise urllib.error.HTTPError(req.full_url,r.status_code,'fixture',r.headers,io.BytesIO(r.content))
  return io.BytesIO(r.content)
 cab={'eva-idempiere-caba':'caba','eva-idempiere-cabb':'cabb'}.get(u.hostname,'shared');port=ports[cab];url=urllib.parse.urlunsplit(('http','127.0.0.1:'+str(port),u.path,u.query,''));wire.append({'case':current['case'],'mapped_at_transport_only':True,'upstream_selected':u.hostname,'validated_path':u.path});loc=urllib.request.Request(url,data=req.data,headers=dict(req.header_items()),method=req.get_method());return orig_open(loc,timeout=3)
cases=[];logio=io.StringIO();handler=logging.StreamHandler(logio);portal.app.logger.addHandler(handler)
def run(id,actor,cab,path,method='GET',headers=None,seedsession=True):
 current['case']=id;client=portal.app.test_client();
 if actor:client.set_cookie('eva_token',tokens[actor],domain='acc.eva-org.com')
 if cab:client.set_cookie('eva_idm_cab',cab,domain='acc.eva-org.com')
 if seedsession: client.set_cookie('JSESSIONID','fixture-session',domain='acc.eva-org.com',path='/webui' if path.startswith('/webui') else '/idmp')
 before=len(wire);r=client.open(path,method=method,base_url='http://acc.eva-org.com',headers={'X-Trace-Id':id,**(headers or {})},data=b'fixture-post' if method=='POST' else None);data=r.get_data();events=wire[before:];actual=[ev for ev in events if not ev.get('mapped_at_transport_only')];rec={'case':id,'actor':actor or 'anon','cookie_cab':cab,'path':path,'method':method,'response_status':r.status_code,'redirect':r.headers.get('Location'),'Cache-Control':r.headers.get('Cache-Control'),'cookies_forwarded_by_portal':[v.split('=',1)[0]+' '+v.split(';',1)[-1] for v in r.headers.getlist('Set-Cookie')],'visible_refusal':data==b'ADMIN_REFUZ','auth_results':[e['status'] for e in authcalls if e['case']==id and e['path'].endswith('/auth/me')],'wire':events,'actual_receiver_count':len(actual),'actual_receiver_hosts':[e['host'] for e in actual],'actual_receiver_paths':[e['raw_request_target'] for e in actual]};cases.append(rec)
with patch.object(portal._urlreq,'urlopen',transport):
 for prefix in ['/webui','/idmp']:
  p=prefix.strip('/');
  for key,pa in [('normal','/zkau/web/js/zk.wpd?theme=ro&x=1'),('traversal','/%2e%2e/osgi/system/console%23/..%2F..%2F..%2Fwebui%2Fz'),('matrix','/%2e%2e%3B/osgi'),('double','/%252e%252e%252fosgi'),('encoded-separator','/a%2Fb.js'),('invalidUTF8','/%ff%fe'),('dots-in-name','/a..b.js'),('valid-utf8','/tem%C4%83.css'),('redirect-inside','/redirect-inside'),('redirect-outside','/redirect-outside'),('redirect-other','/redirect-other')]:
   run(p+'-'+key,'a','caba',prefix+pa)
  run(p+'-normal-repeat','a','caba',prefix+'/zkau/web/js/zk.wpd?theme=ro&x=1');run(p+'-denied-repeat','a','caba',prefix+'/%252e%252e%252fosgi');run(p+'-legit-post','a','caba',prefix+'/zkau',method='POST');run(p+'-actor-B','b','cabb',prefix+'/styles.css');run(p+'-actor-A-targets-B','a','cabb',prefix+'/styles.css');run(p+'-no-session',None,'caba',prefix+'/styles.css');run(p+'-revoked','revoked','caba',prefix+'/styles.css');run(p+'-spoof-role',None,'caba',prefix+'/styles.css',headers={'X-User-Role':'super'})
 for id,route in [('cui-root','/RO113'),('cui-company','/RO113/RO114'),('cui-channel','/RO113/RO114/eMag'),('download-traversal','/downloads/..%2Fportal%2Feva_users.html')]:run(id,'a','caba',route)
 from pathlib import Path
 docs=Path(tmp.name)/'docs';docs.mkdir();(docs/'public-fixture.txt').write_text('specific public fixture',encoding='utf8')
 with patch.object(portal,'DOWNLOADS',str(docs)):
  run('public-document-positive',None,None,'/downloads/public-fixture.txt');run('public-document-negative',None,None,'/downloads/..%2Fauth.db')
 run('protected-login-screen-cache',None,None,'/app/login')
 if ver=='new':
  with patch.object(portal,'cale_webui_permisa',return_value=True),patch.object(portal,'cale_trimisa_in_webui',return_value=True):run('double-guard-mutant','a','caba','/webui/../osgi/admin')
portal.app.logger.removeHandler(handler);[s.shutdown() for s in servers];[s.server_close() for s in servers];be.close();engine.dispose();tmp.cleanup();response={'version':ver,'source_sha256':hashlib.sha256((frontend/'app.py').read_bytes()).hexdigest(),'utc':datetime.datetime.now(datetime.UTC).isoformat(),'level':'Original Flask route, decorator, cookie selection, actual gateway strict /auth/me on synthetic SQLite, urllib HTTP + redirect behavior and real HTTP listeners on loopback only. Transport maps fake cabinet host to local listener; no real iDempiere. _idm_proxy and _idm_upstream are not replaced.','cases':cases,'log_ADMIN_REFUZ_count':logio.getvalue().count('ADMIN_REFUZ'),'events':len(wire),'mutation_note':'Only the named double-guard-mutant case substitutes both validators in memory.','cleanup':True};(W/('portal-'+ver+'.json')).write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(ver,len(cases),[(x['case'],x['response_status'],x['actual_receiver_paths']) for x in cases if x['case'] in ('webui-traversal','webui-redirect-outside','webui-invalidUTF8','webui-actor-A-targets-B','webui-no-session','double-guard-mutant')])
