import json,os,io,base64
from pathlib import Path
from sqlalchemy import text
from app.dracula import create_app
from app.db import session_scope
from app.security import create_access_token
app=create_app();app.testing=True;c=app.test_client()
assert os.environ.get('COMMERCE_MODE')=='demo'
with session_scope(role='admin',superadmin='on') as s:
 row=s.execute(text('SELECT id,email FROM identity.admin_users WHERE email=:e'),{'e':os.environ['ADMIN_SEED_EMAIL']}).first()
 token,_=create_access_token(subject=str(row.id),email=row.email,is_superadmin=False,roles={os.environ['DEFAULT_TENANT']:'owner'},extra={'mcp':False})
h={'Authorization':'Bearer '+token,'X-Requested-With':'XMLHttpRequest'}
png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
r=c.post('/api/admin/v1/media/upload',headers=h,data={'file':(io.BytesIO(png),'qa.png')});assert r.status_code==201,r.json
media=r.json
if 'item' in media:media=media['item']
assert c.get(media['url']).status_code==200,media
assert c.delete('/api/admin/v1/media/'+media['id'],headers=h).status_code in (200,204)
print('PASS admin media upload, public image response, deletion')
path=Path('/app/data/.test-admin.json')
if path.exists():
 data=json.loads(path.read_text())
 with session_scope(role='admin',superadmin='on') as s:
  s.execute(text("UPDATE identity.admin_users SET status='disabled' WHERE id=:id AND email=:e"),{'id':data['id'],'e':data['email']})
  s.execute(text('UPDATE identity.admin_sessions SET revoked_at=now() WHERE admin_user_id=:u AND revoked_at IS NULL'),{'u':data['id']})
 path.unlink()
 print('Temporary QA administrator disabled and sessions revoked.')
