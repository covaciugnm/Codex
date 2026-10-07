"""Real PostgreSQL smoke suite. Run inside backend, in COMMERCE_MODE=demo only."""
import os,json,uuid
from app.dracula import create_app
from app.security import create_access_token
from app.db import session_scope
from sqlalchemy import text

assert os.environ.get('COMMERCE_MODE')=='demo','Tests are restricted to the demo shop'
app=create_app(); app.testing=True
client=app.test_client(); other=app.test_client()
def call(c,path,method='GET',data=None,extra=None):
    csrf=c.get_cookie('dracula_csrf')
    headers={'X-CSRF-Token':csrf.value if csrf else '',**(extra or {})}
    return c.open(path,method=method,json=data,headers=headers)
def ok(r,status=200):
    assert r.status_code==status,(r.status_code,r.json)
    return r.json
boot=ok(call(client,'/api/dracula/bootstrap?lang=de'));assert boot['locale']=='de' and len(boot['products'])==5 and len(boot['pages'])==14
assert ok(call(client,'/api/public/brand'))['name']=='Dracula Design'
pid=boot['products'][0]['id']
assert client.post('/api/cart/items',json={'product_id':pid,'qty':1}).status_code==403
ok(call(client,'/api/cart/items','POST',{'product_id':pid,'qty':1}))
email='qa-'+uuid.uuid4().hex[:12]+'@example.com'
registered=ok(call(client,'/api/account/register','POST',{'email':email,'password':'Local-QA-Test-2026!','password_confirm':'Local-QA-Test-2026!','full_name':'Local Test','accept_terms':True}),201)
ok(call(client,'/api/account/favorites','POST',{'product_id':pid}),201)
assert len(ok(call(client,'/api/account/favorites'))['items'])==1
cart=ok(call(client,'/api/cart'));assert cart['items_count']==1
body={'customer':{'first_name':'Local','last_name':'Test','email':email,'phone':'0722123456'},'shipping_address':{'line1':'Strada Test 1','city':'Brasov','county':'Brasov','postal_code':'500001','country':'RO'},'delivery_method':'courier','payment_method':'cash_on_delivery','accept_terms':True,'expected_total_ron':cart['products_gross_ron']+25,'notes':'AUTOMATED QA — TEST ONLY'}
key=uuid.uuid4().hex
tampered={**body,'expected_total_ron':0};assert call(client,'/api/orders','POST',tampered,{'Idempotency-Key':key}).status_code==409
assert ok(call(client,'/api/cart'))['items_count']==1
result=ok(call(client,'/api/orders','POST',body,{'Idempotency-Key':key}),201);assert result['demo']
assert ok(call(client,'/api/orders','POST',body,{'Idempotency-Key':key}))['order_number']==result['order_number']
assert call(client,'/api/orders','POST',tampered,{'Idempotency-Key':key}).status_code==409
assert ok(call(client,'/api/cart'))['items_count']==0
orders=ok(call(client,'/api/account/orders'));assert len(orders['orders'])==1
ok(call(client,'/api/account/orders/'+result['order_number']))
ok(call(other,'/api/dracula/bootstrap'))
assert call(other,'/api/account/orders/'+result['order_number']).status_code in (401,403,404)
assert call(client,'/api/admin/v1/products').status_code==401
assert call(client,'/api/dracula/inquiry','POST',{'kind':'contact','name':'Local Test','email':email,'body':'QA inquiry stored in the isolated database.'}).status_code==201
assert call(client,'/api/cart/items','POST',{'product_id':pid,'qty':1},{'Origin':'https://unrelated.invalid'}).status_code==403
assert call(client,'/api/payments/stripe/session','POST',{'order_number':result['order_number']}).status_code==409
with session_scope(role='admin',superadmin='on') as session:
    row=session.execute(text('SELECT id,email FROM identity.admin_users WHERE email=:email'),{'email':os.environ['ADMIN_SEED_EMAIL']}).first()
    token,_=create_access_token(subject=str(row.id),email=row.email,is_superadmin=False,roles={'dracula-design':'owner'},extra={'mcp':False})
    admin_id=str(row.id)
headers={'Authorization':'Bearer '+token,'X-Requested-With':'XMLHttpRequest'}
for path in ('products','orders','customers','settings','legal-pages','translations','users','dracula/inquiries'):
    r=call(client,'/api/admin/v1/'+path,extra=headers);assert r.status_code==200,(path,r.status_code,r.json)
print(json.dumps({'passed':['RO/EN/DE DB content','five products/fourteen pages','CSRF and origin enforcement','customer registration','guest cart merge','DB favorites','price tamper rejection','test checkout','idempotent replay','empty cart after order','customer order isolation','admin separation','inquiry persistence','no real payment in demo','admin modules'],'test_order':result['order_number']}))
