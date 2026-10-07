"""Generate this shop's secrets once. Never reads another store's environment."""
import os,secrets,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
env=root/'.env'
if env.exists():
    print('Existing .env kept unchanged.')
else:
    values={'POSTGRES_PASSWORD':secrets.token_hex(32),'EVA_STOREFRONT_DB_PASSWORD':secrets.token_hex(32),'EVA_ADMIN_DB_PASSWORD':secrets.token_hex(32),'SECRET_KEY':secrets.token_hex(32),'JWT_SECRET':secrets.token_hex(32),'SECRETS_KEY':secrets.token_urlsafe(32),'ADMIN_SEED_EMAIL':'owner@dracula.local','ADMIN_SEED_PASSWORD':secrets.token_urlsafe(24),'PUBLIC_BASE_URL':'http://127.0.0.1:4181','BIND_ADDRESS':'127.0.0.1','SHOP_PORT':'4181','COMMERCE_MODE':'demo','COMMERCE_READY':'false','COOKIE_SECURE':'false','STRIPE_ENABLED':'false','MAIL_WORKER':'false'}
    fd=os.open(env,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w',encoding='utf-8') as f:f.write('\n'.join(k+'='+v for k,v in values.items())+'\n')
    print('Created private .env. Admin credentials are ADMIN_SEED_EMAIL / ADMIN_SEED_PASSWORD; password change is required at first login.')
for folder in ['data','data/media_cache','data/tenants/dracula-design','backups']:(root/folder).mkdir(parents=True,exist_ok=True)
registry=root/'data/theme_registry.json'
if not registry.exists():
    registry.write_text(json.dumps({'themes':[{'id':'dracula_exclusive','name':{'ro':'Dracula Exclusiv','en':'Dracula Exclusive','de':'Dracula Exklusiv'},'template':'dracula','description':{'ro':'Colecția Dracula Design','en':'The Dracula Design collection','de':'Die Dracula Design Kollektion'},'colors':{'primary':'#090909','accent':'#b89a64'},'layout_order':['hero','products','signature','universe']}]},ensure_ascii=False),encoding='utf-8')
