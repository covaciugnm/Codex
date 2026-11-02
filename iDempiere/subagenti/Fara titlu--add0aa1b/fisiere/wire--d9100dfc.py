import sys,os,secrets,hashlib,datetime,json,subprocess,threading,logging,warnings
from pathlib import Path
sys.path.insert(0,'D:/CodexWork');from p01_cesiro_contract_lab import create_fixture,create_real_api,close_fixture
from werkzeug.serving import make_server
from flask import request,make_response
import requests
w=Path('D:/CodexWork/a06ex');sec=Path('D:/CodexWork/eva-audit-secondary-20261102');out=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/supliment_CESIRO1/probe/EX04-evidence');out.mkdir(exist_ok=True)
def save(name,d): (out/name).write_text(json.dumps(d,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
origins={'git':'cod-master-contab.jar','installed':'com.eva.ro.contab_13.0.0.jar'}
def cp(k):
 dest=w/('classes-'+k);dest.mkdir(exist_ok=True);return ';'.join([str(dest),str(sec/origins[k]),str(sec/'org.adempiere.base_13.0.0.202603090043.jar'),str(sec/'org.adempiere.base.process_13.0.0.202603090043.jar'),'D:/CodexWork/a05-support-jars/*','D:/CodexWork/eva-a01-java/lib/*'])
java=Path('C:/Program Files/Java/jdk-21/bin')
for k in origins:
 subprocess.run([java/'javac.exe','-encoding','UTF-8','-cp',cp(k),'-d',str(w/('classes-'+k)),str(w/'Ex04Wire.java')],check=True)
cx,db,role,T,O=create_fixture();key=secrets.token_urlsafe(24);os.environ['EXTERNAL_API_KEYS_SHA256']=hashlib.sha256(key.encode()).hexdigest();app=create_real_api();server=None;events=[];mode='normal';log=[];logging.getLogger('werkzeug').setLevel(logging.ERROR)
@app.before_request
def anomaly():
 if request.path.endswith('/orders'):
  if mode=='429':return ('throttled',429)
  if mode=='500':return ('synthetic error',500)
  if mode=='malformed':return make_response('{"items":[',200)
  if mode=='valid_partial':return make_response('{"items":[],"total":3,"pages":3,"page":1,"per_page":1}',200)
@app.after_request
def record(r):
 if request.path.startswith('/api/ext'):
  v=r.get_json(silent=True) if r.mimetype=='application/json' else None
  log.append({'path':request.path,'query':dict(request.args),'mode':mode,'http':r.status_code,'metadata':({k:v.get(k) for k in ['total','page','pages','per_page']} if isinstance(v,dict) else {})})
 return r
def invoke(k,label,tenant,fromdate='2026-11-02 00:00:00',until='2026-11-03 00:00:00',since='null',ref=None):
 args=[java/'java.exe','-Dstdout.encoding=UTF-8','-Duser.timezone=UTC','-cp',cp(k),'com.eva.ro.contab.corelare.Ex04Wire',base,tenant,fromdate,until,since]
 if ref:args.append(ref)
 x=subprocess.run(args,env={**os.environ,'EX04_FIXTURE_KEY':key},encoding='utf8',text=True,capture_output=True,timeout=11)
 if x.returncode!=0:raise RuntimeError(x.stderr[:400])
 rows=[s.split('\t')[1:] for s in x.stdout.splitlines() if s.startswith('ROW\t')];end=next(s.split('\t')[1:] for s in x.stdout.splitlines() if s.startswith('RESULT\t'))
 item={'jar':k,'case':label,'tenant':tenant,'row_count':len(rows),'rows':rows,'result':end,'requests':[s.split('\t',1)[-1] for s in x.stdout.splitlines() if s.startswith('HTTP\t')],'detail':[s for s in x.stdout.splitlines() if s.startswith('DETAIL\t')]};events.append(item);return item
try:
 server=make_server('127.0.0.1',0,app);threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/api/ext/v1'
 def raw_page(tenant,page,size=1,since=None):
  p={'tenant':tenant,'page':page,'per_page':size}
  if since:p['updated_since']=since
  rr=requests.get(base+'/orders',params=p,headers={'Authorization':'Bearer '+key},timeout=4);row=rr.json();return {'page':page,'status':rr.status_code,'total':row.get('total'),'pages':row.get('pages'),'ids':[v['id'] for v in row.get('items',[])]}
 # Preserve authenticated original responses for isolated native replay. Only fake tenant/customer data.
 for tenant,slug,ids in [(T[0],'canal-a',O[:3]),(T[1],'canal-b',O[3:])]:
  for scope,path in [('orders','/orders'),('tenants','/tenants'),('health','/health')]+[(str(x),'/orders/'+str(x)) for x in ids]:
   params={'tenant':slug,'per_page':0,'items':0} if scope=='orders' else {'tenant':slug};rr=requests.get(base+path,params=params,headers={'Authorization':'Bearer '+key},timeout=5);assert rr.status_code==200
   save('raw-'+slug+'-'+scope+'.json',rr.json())
 pages=[raw_page('canal-a',i) for i in (1,2,3)];bp=raw_page('canal-b',1)
 for k in origins:
  for slug in ('canal-a','canal-b'):invoke(k,'full-window',slug,ref=O[0] if slug=='canal-a' else O[3])
  invoke(k,'restart-same-snapshot','canal-a')
  invoke(k,'inclusive-tie','canal-a',since='2026-11-02 10:00:00')
  invoke(k,'same-day-final-exclusive','canal-a',until='2026-11-02 23:59:59')
  for fault in ('429','500','malformed','valid_partial'):
   mode=fault;invoke(k,fault,'canal-a')
  mode='normal';invoke(k,'recovery','canal-a')
 # New version of 102 is deliberately after the previous cursor, identity stable in an unchanged date window.
 cx.execute("update sales.orders set updated_at='2026-11-02 10:00:03+00' where id=%s",(O[1],))
 late=[invoke(k,'late-version','canal-a',since='2026-11-02 10:00:02') for k in origins]
 # Offset consumer: demonstrate insertion between p1 and p2. Race belongs to external API page consumer, connector normally asks all rows.
 first=raw_page('canal-a',1);cx.execute("update sales.orders set created_at='2026-11-02 10:00:04+00' where id=%s",(O[1],));second=raw_page('canal-a',2);third=raw_page('canal-a',3)
 data={'timestamp':now(),'source_code':'6df998aee0e514d30856c461962afe99ebd0d113','fixture_database':db,'fixture_role':'read-only per API transaction; fixture owner inserts synthetic events independently','tenant_refs':list(T),'order_ids':O,'origins':origins,'baseline_pages':pages,'B_page':bp,'changed_order_during_offset_paging':{'pages':[first,second,third],'observed_ids':sum([p['ids'] for p in [first,second,third]],[])},'java':events,'wire':log,'transport':'Original Flask ext_bp and original SursaCesiro1.get on fresh Java process over loopback HTTP. Mutants injected before blueprint for errors/truncated body only. Business rollback and persistence require ERP probe; optional pagination and updated_since not sent by normal PreiaDinSite.comenzi.','cleanup':None}
finally:
 if server:server.shutdown();server.server_close()
 close_fixture(cx,db,role)
if 'data' in locals():
 data['cleanup']='Dedicated fixture DB and role removed in finally.';save('wire.json',data);print([(v['jar'],v['case'],v['row_count'],v['result'][0]) for v in events]);print(pages,bp)

