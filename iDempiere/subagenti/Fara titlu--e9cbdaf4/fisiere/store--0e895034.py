import runpy,tempfile,socket,pathlib,shutil,json,sys,datetime
O=pathlib.Path(__file__).parent; E=O.parent
def rd(p): return json.loads(p.read_text(encoding='utf8'))
def wr(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/frontend/storefront');sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(src)]
calls=[]
def no(*args,**kwargs):calls.append('blocked');raise RuntimeError('offline fixture')
socket.socket.connect=no;socket.socket.connect_ex=no;socket.create_connection=no
from app import cms
from app.factory import create_app
with tempfile.TemporaryDirectory(prefix='a11-lot2-') as k:
 root=pathlib.Path(k);config=root/'seed/data/tenants/cesiro1/translations.json';config.parent.mkdir(parents=True);config.write_text('{}')
 fx=runpy.run_path(str(src/'tests/test_audit_regressions.py'))['minimal_tenant'];fx.__globals__['ROOT']=root/'seed'
 tenants=root/'tenants';cms.TENANTS=str(tenants);cms.DATA='D:/CodexWork/eva-audit-secondary-20261102/public-theme-fixture';p=fx(tenants);td=tenants/'cesiro1';other=tenants/'a11b';shutil.copytree(td,other)
 cat=td/'catalog.json';raw=rd(cat);first,second=raw['products'][:2];app=create_app();app.testing=True;c=app.test_client()
 customer={'name':'Synthetic A11','email':'fixture@example.test','address':'Synthetic Street','phone':'0700000000','country':'RO','payment_method':'bank_transfer','customer_type':'individual'}
 def order():
  res=c.post('/api/orders',base_url='https://cesiro1.eva-contab.ro',json={'customer':customer,'items':[{'id':first['id'],'qty':1}]});body=res.get_json();doc=rd(td/'orders'/(body['id']+'.json'));return {'http':res.status_code,'expected_product':first['id'],'stored_product':doc['items'][0]['id'],'stored_qty':doc['items'][0]['qty']}
 result={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':order()}
 second['sku']=first['id'];wr(cat,raw);cms._JSON_CACHE.clear();result['collision_after_id']=order()
 raw['products'][:2]=[second,first];wr(cat,raw);cms._JSON_CACHE.clear();result['reversed_catalog_order']=order()
 otherfile=other/'catalog.json';beforeA=cat.read_bytes();beforeB=rd(otherfile)
 body={'products':[{'id':'a11-new-canary','sku':'only-b','name':{'ro':'A11'},'price_ron':19,'slug':{'ro':'a11'}}]}
 r=app.test_client().post('/admin/api/tenants/a11b/import/json',base_url='https://cesiro1.eva-contab.ro',json=body);afterB=rd(otherfile)
 result['anonymous_cross_import']={'http':r.status_code,'cookies_sent':False,'target_ids_before':[x['id'] for x in beforeB['products']],'target_ids_after':[x['id'] for x in afterB['products']],'source_catalog_unchanged':cat.read_bytes()==beforeA,'source_host':'cesiro1','target':'a11b'}
 result['external_attempts']=calls
assert result['baseline']['stored_product']==first['id'] and result['collision_after_id']['stored_product']==second['id']
assert result['anonymous_cross_import']['target_ids_after']==['a11-new-canary']
wr(O/'A06_A08_storefront.json',result);print(result)

