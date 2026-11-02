"""Real source blueprint + readonly PostgreSQL fixture. No network connection except loopback PostgreSQL."""
from p01_cesiro_contract_lab import *
import logging,io,socket,re,contextlib,tempfile
from sqlalchemy import text
from flask import request
from unittest.mock import patch
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cx,db,role,tenants,orders=create_fixture(); api=None; observations=[]; wire=[]; logstream=io.StringIO(); lh=logging.StreamHandler(logstream); logging.getLogger().addHandler(lh)
 net=socket.socket.connect
 def restricted(sock,address):
  if not isinstance(address,tuple) or address[0] not in ('127.0.0.1','localhost','::1'):raise OSError('EX02: external socket denied')
  return net(sock,address)
 app=create_real_api(); cli=app.test_client(); keys=[secrets.token_hex(32) for _ in range(2)]; h=lambda s:hashlib.sha256(s.encode()).hexdigest(); os.environ['EXTERNAL_API_KEYS_SHA256']=','.join(h(k) for k in keys)
 @app.before_request
 def wh():wire.append({'endpoint':request.endpoint,'method':request.method,'path':request.path,'host':request.host,'Origin':request.headers.get('Origin'),'request_id':request.headers.get('X-Trace-Id')})
 def case(label,endpoint,expected,headers=None,host='canal-a.test',method='GET',export=False):
  hdr={'X-Trace-Id':label,**(headers or {})};r=cli.open('/api/ext/v1'+endpoint,method=method,base_url='https://'+host,headers=hdr);v=r.get_json(silent=True) or {};raw=r.get_data(as_text=True);items=v.get('items',[]); observation={'id':label,'path':endpoint,'method':method,'host':host,'Origin':hdr.get('Origin'),'http':r.status_code,'expected_http':expected,'status_matches':r.status_code in expected,'response_tenant':v.get('tenant'),'order_id':v.get('id'),'list_tenants':sorted({x.get('slug') or x.get('tenant') for x in items if (x.get('slug') or x.get('tenant'))}),'private_B_marker_in_response':'CONTACT-B7' in raw,'private_A_marker_in_response':'CONTACT-A7' in raw,'foreign_child_canary':'EX02-B-child-of-A' in raw,'sensitive_field_markers_found':[x for x in ('EX02-private-ip','EX02-private-token','EX02-private-password') if x in raw], 'access_control_allow_origin':r.headers.get('Access-Control-Allow-Origin'),'error':v.get('error'),'content_type':r.content_type,'response_bytes':len(r.data),'body_sha256':hashlib.sha256(r.data).hexdigest(),'export_request':export};observations.append(observation);return v
 try:
  # Owner setup deliberately creates an inconsistent association; these rows are synthetic, not production.
  cx.execute("UPDATE sales.orders SET customer=customer||%s::jsonb WHERE id=%s",(json.dumps({'nested':{'ip':'EX02-private-ip','auth_token':'EX02-private-token','password':'[CREDENTIAL_REDACTED]'}}),orders[3]))
  cx.execute("INSERT INTO sales.shipments(tenant_id,order_id,tracking_number,provider,package_status) VALUES(%s,%s,%s,%s,%s)",(tenants[1],orders[0],'EX02-B-child-of-A','fixture','created'))
  snap=lambda:{t:cx.execute('SELECT tenant_id::text,count(*) FROM sales.'+t+' GROUP BY 1 ORDER BY 1').fetchall() for t in ['orders','order_items','shipments']};s0=snap()
  api=importlib.import_module('app.api.external_orders');from app import theme_preview
  from app import cms
  with tempfile.TemporaryDirectory(prefix='EX02-theme-registry-') as folder,patch.object(cms,'DATA',folder):
   (Path(folder)/'theme_registry.json').write_text(json.dumps({'themes':[{'id':'preview-theme'}]}),encoding='utf8');tkn,_=theme_preview.make_token('preview-theme',tenants[0],'actor-admin-synthetic'); preview={'own_valid':theme_preview.load_token(tkn,tenants[0]) is not None,'foreign_refused':theme_preview.load_token(tkn,tenants[1]) is None,'tampered_refused':theme_preview.load_token(tkn+'x',tenants[0]) is None,'expired_refused':theme_preview.load_token(tkn,tenants[0],max_age=-1) is None}
  with patch.object(socket.socket,'connect',restricted):
   a,b=keys; ka={'X-Api-Key':a};kb={'Authorization':'Bearer '+b}; hostile={'Origin':'https://unrelated.fixture','X-Tenant-Cui':'RO-SAME-FIXTURE','X-Tenant':'canal-a','X-Channel':'canal-a','X-User-Role':'comisionar'}
   case('Q01-anonymous','/tenants',[401]);case('Q02-invalid-key','/orders?tenant=canal-a',[401],{'X-Api-Key':'invalid'});case('Q03-service-key-A-and-Origin','/tenants',[200],{**ka,**hostile});case('Q04-order-A-same-ref','/orders/ORD101?tenant=canal-a',[200],ka);case('Q05-keyA-selects-B-and-cleans-markers','/orders/ORD101?tenant=canal-b',[200],{**ka,**hostile});case('Q06-keyB-selects-A-on-host-B','/orders/ORD101?tenant=canal-a',[200],kb,host='canal-b.test');case('Q07-internal-B-UUID-in-A-filter','/orders/'+orders[3]+'?tenant=canal-a',[404],ka);case('Q08-unknown-UUID-in-A-filter','/orders/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa?tenant=canal-a',[404],ka);case('Q09-global-order-list','/orders?per_page=0',[200],ka);case('Q10-reference-no-tenant','/orders/ORD101',[200],ka);case('Q11-unknown-tenant','/orders?tenant=no-such-tenant',[404],ka);case('Q12-Bearer-priority-invalid','/tenants',[401],{**ka,'Authorization':'Bearer unauthenticated'});case('Q13-Bearer-priority-valid','/tenants',[200],{'X-Api-Key':'invalid',**kb});case('Q14-POST-no-write','/orders',[405],ka,method='POST');case('Q15-DELETE-no-write','/orders/ORD101',[405],ka,method='DELETE');case('Q16-no-export-route','/orders/export.csv',[404],ka,export=True);case('Q17-OPTIONS-preflight','/orders',[200,204],hostile,method='OPTIONS');
   cli.set_cookie('eva_preview',tkn,domain='canal-a.test');cli.set_cookie('session','synthetic-support-or-commissioner-cookie',domain='canal-a.test');case('Q18-support-cookie-only','/orders?tenant=canal-a',[401],hostile);case('Q19-preview-as-API-key','/orders?tenant=canal-a',[401],{'Authorization':'Bearer '+tkn,**hostile});case('Q20-preview-as-cookie-plus-global-key','/orders/ORD101?tenant=canal-b',[200],ka)
   import threading,urllib.request,urllib.error
   from werkzeug.serving import make_server
   access_logger=logging.getLogger('werkzeug');oldlevel=access_logger.level;access_logger.setLevel(logging.INFO);server=make_server('127.0.0.1',0,app);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();actual_wire=[]
   try:
    for u,key in [('/orders/ORD101?tenant=canal-b',a),('/orders?q=EX02-LOG-POSITIVE&tenant=canal-a',a),('/tenants','invalid-only')]:
     req=urllib.request.Request('http://127.0.0.1:'+str(server.server_port)+'/api/ext/v1'+u,headers={'X-Api-Key':key,'Origin':'https://wire.fixture','X-Trace-Id':'EX02-WIRE'})
     try:
      with urllib.request.urlopen(req,timeout=5) as res:status=res.status;body=res.read()
     except urllib.error.HTTPError as exc:status=exc.code;body=exc.read()
     actual_wire.append({'path':u,'HTTP':status,'contains_private_order_canary':b'CONTACT-B7' in body})
   finally:server.shutdown();thread.join(3);server.server_close();access_logger.setLevel(oldlevel)
   os.environ['EXTERNAL_API_KEYS_SHA256']=h(b);case('Q21-removed-keyA','/orders?tenant=canal-a',[401],ka);case('Q22-other-key-stays-global','/orders/ORD101?tenant=canal-a',[200],kb);os.environ['EXTERNAL_API_KEYS_SHA256']='';case('Q23-API-disabled','/orders',[503],kb)
  with api._read_only_session() as sx:
   api._begin_read_only(sx); ro=sx.execute(text("SELECT current_setting('transaction_read_only'),rolbypassrls FROM pg_roles WHERE rolname=current_user")).one(); blocked=None
   try:sx.execute(text("UPDATE sales.orders SET total_ron=total_ron WHERE FALSE"))
   except Exception as exc:blocked=getattr(getattr(exc,'orig',None),'sqlstate',None)
   finally:sx.rollback()
  s1=snap();logs=logstream.getvalue();logcheck={'capture_source':'Python logging from actual loopback Werkzeug HTTP requests plus original blueprint/session in TestClient. Production reverse proxy, PostgreSQL, browser logs and ERP consumer are unobserved.','real_loopback_cases':actual_wire,'captured_records_or_lines':len(logs.splitlines()),'public_query_scanner_positive':'EX02-LOG-POSITIVE' in logs,'canary_in_capture':{m:m in logs for m in ['CONTACT-A7','CONTACT-B7','EX02-B-child-of-A','EX02-private-token','EX02-private-password']},'credential_in_capture':any(x in logs for x in keys+[tkn]),'capture_sha256':h(logs)};assert logcheck['public_query_scanner_positive']
  result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':'EX02/Q-COM-01','read_only_projection':{'database_transaction_read_only':ro[0],'role_bypassrls':ro[1],'no_op_write_denial_SQLSTATE':blocked,'snapshot_business_before_after_equal':s0==s1,'before':s0,'after':s1},'auth_cases':observations,'request_envelope':wire,'logs':logcheck,'preview_token':preview,'source_refs':['backend/app/api/external_orders.py','backend/app/db/session.py','backend/app/theme_preview.py','database/migrations/sql/0029_shipments.sql'],'origin':'Two stores/canale synthetic with a separate technical test key per label, but both keys are authorized globally by the actual blueprint. CUI crossover headers and Origin are untrusted request values, not demonstrated identity. No human session credentials minted; cookie negative tests only.','limitations':'No issuer, expiry or per-key store policy in technical key registry. Revocation by hash removal verified. Receiver logs outside test are unobserved. No inferred commissioner authorization or public reachability.'}
  assert all(x['status_matches'] for x in observations);assert ro[0]=='on' and blocked in ('25006','42501') and s0==s1;assert all(preview.values());assert not any(logcheck['canary_in_capture'].values()) and not logcheck['credential_in_capture'];assert not any(x['sensitive_field_markers_found'] for x in observations)
 finally:
  logging.getLogger().removeHandler(lh)
  from app.db import engine
  for e in engine._engines.values():e.dispose()
  close_fixture(cx,db,role)
  with psycopg.connect(dbname='postgres',user='audit_owner',autocommit=True) as adm:clean=adm.execute('SELECT (SELECT count(*) FROM pg_database WHERE datname=%s),(SELECT count(*) FROM pg_roles WHERE rolname=%s)',(db,role)).fetchone()
 assert clean==(0,0);result['cleanup']={'own_DB_after':clean[0],'own_role_after':clean[1]};target=out/'EX02_variant_A01.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8');print('variant',len(observations),'checks',ro,blocked,clean,'canaries in captured log',sum(logcheck['canary_in_capture'].values()))
if __name__=='__main__':main()
