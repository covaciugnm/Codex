import pathlib,json,hashlib,secrets,uuid
O=pathlib.Path(__file__).parent;E=O.parent;D=E/'supliment_CESIRO1/probe'
src=(D/'EX03_C.py').read_text(encoding='utf-8-sig').split('run=uuid.uuid4().hex')[0];exec(compile(src,'A11-shared-harness-only','exec'))
from flask import Flask
from app.api.external_orders import ext_bp
app=Flask('a11-ex02');app.register_blueprint(ext_bp);client=app.test_client()
r=json.loads((D/'EX03_C_Q_raw.json').read_text(encoding='utf8'));a,b=[r['synthetic_tenants'][k]for k in ['A','B']];order_a=r['cases'][0]['db'];order_b=r['cases'][-1]['db'];os.environ['EXTERNAL_API_KEYS_SHA256']=hashlib.sha256(key.encode()).hexdigest(); hd={'X-Api-Key':key}
nid=str(uuid.uuid4());marker='A11-A-child-for-B-'+nid[:8]
def trace(who,order,headers):
 rr=client.get('/api/ext/v1/orders/'+order['id'],base_url='http://fixture.local',query_string={'tenant':who['slug']},headers=headers);return {'http':rr.status_code,'marker_visible':marker in rr.get_data(as_text=True)}
before=trace(b,order_b,hd);assert before['http']==200 and not before['marker_visible']
with cx() as c:
 assert c.execute('select current_database() name, inet_server_addr()::text ip').fetchone()=={'name':'a08_cesiro','ip':'127.0.0.1/32'}
 c.execute('insert into sales.shipments(id,tenant_id,order_id,order_number,tracking_number) values(%s,%s,%s,%s,%s)',(nid,a['id'],order_b['id'],order_b['order_number'],marker))
try:
 yes=trace(b,order_b,hd);foreign=trace(a,order_b,hd);unauth=trace(b,order_b,{}); legit=trace(a,order_a,hd)
 assert yes=={'http':200,'marker_visible':True} and foreign['http']==404 and not foreign['marker_visible'] and unauth['http'] in [401,403] and not unauth['marker_visible'] and legit=={'http':200,'marker_visible':False}
finally:
 with cx() as c:
  c.execute('delete from sales.shipments where id=%s and tracking_number=%s',(nid,marker));assert c.execute('select count(*) n from sales.shipments where id=%s',(nid,)).fetchone()['n']==0
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'implementation':'Sealed installed CESIRO1 external_orders blueprint with Flask TestClient, synthetic K, PostgreSQL a08_cesiro. Cross-child actual inserted fixture strictly scoped then removed. No production calls.','reversed':'Opposite A-child/B-parent to previous B-child/A-parent. A genuine global service credential is allowed to see its scoped header; the wrong child should not be returned.','before':before,'positive_bad_child':yes,'foreign_header':foreign,'no_key':unauth,'legitimate_other_parent':legit,'cleanup':True}
(O/'EX02_A11_child.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(out)

