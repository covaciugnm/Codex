# Exercițiu pe entry point actual, numai fixture efemeră, fără conexiuni de rețea.
import datetime,hashlib,json,os,runpy,socket,sys,tempfile
from pathlib import Path
here=Path(__file__).resolve().parent
base=Path('D:/CodexWork/eva-audit-p01-readonly-20261102/frontend/storefront')
sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(base)]
sys.dont_write_bytecode=True
work=Path(tempfile.mkdtemp(prefix='eva-a06-checkout-'));os.chdir(work)
def blocked(*a,**k):raise OSError('fixture network disabled')
socket.socket.connect=blocked;socket.socket.connect_ex=blocked;socket.create_connection=blocked
from app import cms
from app.factory import create_app
fx=runpy.run_path(str(base/'tests/test_audit_regressions.py'))['minimal_tenant']
translation=work/'seed/data/tenants/cesiro1/translations.json';translation.parent.mkdir(parents=True);translation.write_text('{}',encoding='utf8')
fx.__globals__['ROOT']=work/'seed';cms.DATA='D:/CodexWork/eva-audit-secondary-20261102/public-theme-fixture'
def run_case(idx,case,lines,repeat=None,collision=False):
 tenant=work/str(idx)/'tenants';cms.TENANTS=str(tenant);products=fx(tenant);cms._JSON_CACHE.clear()
 if collision:
  cat=tenant/'cesiro1/catalog.json';data=json.loads(cat.read_text(encoding='utf8'));data['products'][1]['sku']=data['products'][0]['id'];cat.write_text(json.dumps(data),encoding='utf8')
 app=create_app();app.testing=True;client=app.test_client()
 customer={'name':'Audit A06','phone':'+40722222222','email':'audit@example.test','country':'RO','address':'Strada Test 1','payment_method':'bank_transfer','customer_type':'individual'}
 observations=[]
 for qty in lines:
  res=client.post('/api/orders',query_string={'tenant':'cesiro1'},json={'items':[{'id':products['mapped']['id'],'qty':qty}],'customer':customer},headers={'X-Forwarded-For':f'198.51.100.{idx}','Idempotency-Key':str(repeat or idx)},base_url='https://cesiro1.eva-contab.ro')
  d=res.get_json() or {};oid=d.get('order_id') or d.get('id')
  vals=[json.loads(f.read_text(encoding='utf8')) for f in (tenant/'cesiro1').rglob('*.json') if oid and f.stem==oid]
  order=next((v for v in vals if 'items' in v),{});items=order.get('items',[])
  observations.append({'requested_id':products['mapped']['id'],'requested_qty':qty,'http':res.status_code,'id':oid,'business_state':d.get('order_status') or d.get('status'),'persisted_qty':items[0]['qty'] if items else None,'persisted_product_id':items[0]['id'] if items else None,'vat_rate':order.get('totals',{}).get('vat_rate'),'error':d.get('error')})
 return {'case':case,'observed':observations}
out=[run_case(1,'same key consecutive',[1,1],'same-operation'),run_case(2,'qty exceeds three in catalogue',[7]),run_case(3,'negative quantity',[-1]),run_case(4,'fractional quantity',[1.75]),run_case(5,'id of CPP collides with SKU of following CPA',[1],collision=True),run_case(6,'zero quantity',[0]),run_case(7,'ordinary positive qty',[2])]
data={'id':'A06-CHECKOUT-R2','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject':'Flask actual route, 7 cases / 8 HTTP requests. Mapped catalog product 3 units. Both articles fake. No ERP or marketplace calls.','results':out,'scopes':'Only /api/orders fixture and its own persisted JSON status; does not establish the state of C_Order/M_StorageReservation on any ERP.','source_sha':'6df998aee0e514d30856c461962afe99ebd0d113'}
(here/'checkout_cases.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
for r in out:print(r['case'],r['observed'])
