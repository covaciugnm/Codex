import json,os,runpy,subprocess,sys,socket,tempfile
from pathlib import Path
here=Path(__file__).resolve().parent;dest=Path('D:/CodexWork/a06r2/cases/ids-restart.json')
base=Path('D:/CodexWork/eva-audit-p01-readonly-20261102/frontend/storefront');deps=Path('D:/CodexWork/eva-audit-secondary-20261102/public-theme-fixture')
if len(sys.argv)==1:
 wd=Path(tempfile.mkdtemp(prefix='a06r2-ids-'));events=[]
 for scen in ('numeric-id','sku','ean','conflict','explicit-disagree','negative','fraction','zero','retry-one','retry-two'):
  proc=subprocess.run([sys.executable,str(__file__),str(wd),scen],capture_output=True,text=True,timeout=16)
  if proc.returncode: raise Exception(proc.stderr[-500:])
  events.append(json.loads(proc.stdout.strip().splitlines()[-1]))
 dest.write_text(json.dumps({'fixture':'One synthetic local catalog, independent Python/Flask worker restarted for every HTTP post, persistent tenant files shared, socket transport disabled, no vendor or ERP connections.','events':events},indent=2),encoding='utf8');print([(a['case'],a['out_id'],a['persisted_product'],a['persisted_qty']) for a in events]);sys.exit()
wd=Path(sys.argv[1]);sc=sys.argv[2];sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(base)];sys.dont_write_bytecode=True;os.chdir(wd)
def block(*a,**kw):raise OSError('Blocked network')
socket.socket.connect=block;socket.socket.connect_ex=block;socket.create_connection=block
from app import cms
from app.factory import create_app
ten=wd/'tenants';cms.TENANTS=str(ten);cms.DATA=str(deps)
if not ten.exists():
 fx=runpy.run_path(str(base/'tests/test_audit_regressions.py'))['minimal_tenant'];translation=wd/'seed/data/tenants/cesiro1/translations.json';translation.parent.mkdir(parents=True);translation.write_text('{}');fx.__globals__['ROOT']=wd/'seed';fx(ten)
 ck=ten/'cesiro1/catalog.json';cat=json.loads(ck.read_text(encoding='utf8'));first=cat['products'][0];first.update({'id':'10444','sku':'A-913','ean':'7222333444555'});second=cat['products'][1];second.update({'id':'B-0002','sku':'2727','ean':'10444'});ck.write_text(json.dumps(cat),encoding='utf8')
 cfgfile=ten/'cesiro1/storefront.json';cfg=json.loads(cfgfile.read_text(encoding='utf8'));cfg['idempiere']['last_stock_audit']['matched_skus']=['A913','2727'];cfgfile.write_text(json.dumps(cfg))
cms._JSON_CACHE.clear()
items={'numeric-id':{'id':2727},'sku':{'sku':'A-913'},'ean':{'ean':'7222333444555'},'conflict':{'id':10444},'explicit-disagree':{'id':'B-0002','sku':'A-913'},'negative':{'sku':'A-913','qty':-9},'fraction':{'sku':'A-913','qty':2.5},'zero':{'sku':'A-913','qty':0},'retry-one':{'sku':'A-913','qty':1},'retry-two':{'sku':'A-913','qty':1}}
item=items[sc];item.setdefault('qty',1);key='persistent-restart-91' if sc.startswith('retry-') else sc
customer={'name':'Fixture User','phone':'+40722222222','email':'fixture@example.test','country':'RO','address':'Test 1','payment_method':'bank_transfer'}
app=create_app();app.testing=True
res=app.test_client().post('/api/orders',query_string={'tenant':'cesiro1'},base_url='https://cesiro1.eva-contab.ro',json={'customer':customer,'items':[item]},headers={'Idempotency-Key':key})
resp=res.get_json() or {};oid=resp.get('order_id') or resp.get('id');docs=[json.loads(f.read_text()) for f in (ten/'cesiro1').rglob('*.json') if oid and f.stem==oid]
doc=next((v for v in docs if v.get('items')),{});saved=(doc.get('items') or [{}])[0]
print(json.dumps({'case':sc,'key':key,'submitted':item,'http':res.status_code,'out_id':oid,'business_state':resp.get('order_status') or resp.get('status'),'persisted_product':saved.get('id'),'persisted_qty':saved.get('qty'),'reason':resp.get('error')}))

