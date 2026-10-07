import os,uuid,json,secrets
from pathlib import Path
from app.dracula import create_app
from app.db import session_scope
from app.security import create_access_token,hash_password
from sqlalchemy import text
assert os.environ.get('COMMERCE_MODE')=='demo'
app=create_app();app.testing=True;c=app.test_client()
with session_scope(role='admin',superadmin='on') as s:
    row=s.execute(text('SELECT id,email FROM identity.admin_users WHERE email=:e'),{'e':os.environ['ADMIN_SEED_EMAIL']}).first()
    token,_=create_access_token(subject=str(row.id),email=row.email,is_superadmin=False,roles={os.environ['DEFAULT_TENANT']:'owner'},extra={'mcp':False})
h={'Authorization':'Bearer '+token,'X-Requested-With':'XMLHttpRequest'}
r=c.get('/api/admin/v1/settings',headers=h);assert r.status_code==200,r.json
original=r.json
print('SETTINGS',list(original.keys()))
r=c.patch('/api/admin/v1/settings',headers=h,json={'languages':['ro','en','de','it']});assert r.status_code==200,r.json
try:
    r=c.put('/api/admin/v1/translations',headers=h,json={'entries':[{'key':'hero.title','values':{'it':'Eleganza.'}}]});assert r.status_code==200,r.json
    r=c.get('/api/dracula/bootstrap?lang=it');assert r.json['ui']['hero.title']=='Eleganza.' and r.json['locale']=='it'
    product=r.json['products'][0]
    r=c.patch('/api/admin/v1/products/'+product['id'],headers=h,json={'translations':{'it':{'name':'Zaino Business','slug':'rucsac-business'}}});assert r.status_code==200,r.json
    assert c.get('/api/dracula/bootstrap?lang=it').json['products'][0]['name']=='Zaino Business'
    print('PASS add language + DB UI and product translation + fallback')
finally:
    r=c.patch('/api/admin/v1/settings',headers=h,json={'languages':original['languages']});assert r.status_code==200,r.json
for path in ['dashboard','categories','media','themes','pages','dracula/inquiries']:
    r=c.get('/api/admin/v1/'+path,headers=h);assert r.status_code==200,(path,r.status_code,r.json)
print('PASS dashboard/categories/media/themes/pages/inquiries')
# Dedicated temporary UI QA admin, never uses or changes the owner's password.
email='ui-qa-'+uuid.uuid4().hex[:10]+'@example.com';password=secrets.token_urlsafe(24)
with session_scope(role='admin',superadmin='on') as s:
    uid=s.execute(text("INSERT INTO identity.admin_users(email,full_name,password_hash,status,must_change_password) VALUES(:e,'Automated UI QA',:p,'active',false) RETURNING id"),{'e':email,'p':hash_password(password)}).scalar_one()
    s.execute(text("INSERT INTO identity.admin_tenant_roles(admin_user_id,tenant_id,role) SELECT :u,id,'owner' FROM core.tenants WHERE slug=:slug"),{'u':uid,'slug':os.environ['DEFAULT_TENANT']})
path=Path('/app/data/.test-admin.json');path.write_text(json.dumps({'email':email,'password':password,'id':str(uid)}));path.chmod(0o600)
print('Temporary UI QA credentials stored privately; revoke after test.')
