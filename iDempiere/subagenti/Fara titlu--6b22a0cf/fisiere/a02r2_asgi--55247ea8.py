import contextlib,datetime,json,os,pathlib,secrets,sys,tempfile
from types import SimpleNamespace
from unittest.mock import patch
src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102');sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(src/'backend')];sys.dont_write_bytecode=True
out=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R2_zone/A02/probe_ASGI_produs.json');assert not out.exists()
with tempfile.TemporaryDirectory(prefix='eva-a02-route-') as td:
 os.environ.update(EVA_ENV='test',IDEMPIERE_MOCK='1',EVA_DATABASE_URL='sqlite:///'+str(pathlib.Path(td)/'fixture.db'),JWT_SECRET=secrets.token_hex(32),EVA_OFFICE_STORAGE=td,SAGA_JOBS_DIR=td)
 from fastapi import FastAPI
 from fastapi.testclient import TestClient
 from app.db import Base,SessionLocal,engine,get_db
 from app.routers import product_full as r
 app=FastAPI();app.include_router(r.router);app.dependency_overrides[r.current_user_optional]=lambda:SimpleNamespace(role='manager',name='fixture')
 Base.metadata.create_all(engine);cli=TestClient(app,raise_server_exceptions=False);state={'id':123,'Value':'FIX-PRIMARY','SKU':'ALIAS-A','UPC':'5940000000000'};writes=[];cases=[]
 class Transport:
  def update_product(self,id,fields):assert id==123;writes.append(dict(fields));state.update(fields);return id
 with contextlib.ExitStack() as bx:
  for owner,name,fn in [(r,'_ctx',lambda *a:{'tenant_cui':'FIX','ad_org_id':11,'ad_client_id':11}),(r,'_assert_product',lambda *a:{'tenant_cui':'FIX','ad_org_id':11,'ad_client_id':11}),(r,'_firm_product_client',lambda *a:Transport()),(r.svc,'resolve_product',lambda *a:{**state,'sku':state['Value']}),(r.svc,'sku_in_use',lambda *a:False),(r.svc,'log_critical',lambda *a,**kw:None),(r,'_record',lambda *a,**kw:None),(r,'get_product',lambda *a,**kw:{'id':123,**state})]:bx.enter_context(patch.object(owner,name,fn))
  for j,(key,body) in enumerate([('id-0012345678900000',{'sku_native':'ALIAS-B','reason':'fixture commercial'}),('id-0012345678900001',{'sku':'CHANNEL-SKU','reason':'fixture alias'}),('id-0012345678900001',{'sku':'CHANNEL-SKU','reason':'fixture alias'})]):
   before=dict(state);wc=len(writes);res=cli.patch('/eva/products/123',headers={'X-Idempotency-Key':key},json=body);cases.append({'case':j+1,'body':body,'status':res.status_code,'before':before,'after':dict(state),'write_delta':writes[wc:],'response':res.text[:200]})
 engine.dispose()
 ev={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':'EV-A02-R2-ASGI-SKU','route':'product_full.patch_product via FastAPI TestClient','scope':'Handler, validation, field mapping and idempotency store are real; authenticated fixture role and tenant resolution pinned. Outbound iDempiere adapter and final response reader are controlled doubles, no deployment claim. Independent native rename and reuse captured in A05/sandbox-product-identity.txt.','cases':cases}
 with out.open('x',encoding='utf8')as f:json.dump(ev,f,ensure_ascii=False,indent=2)
 print([(c['status'],c['write_delta'])for c in cases]);assert [c['status'] for c in cases]==[200,200,200] and len(writes)==2
