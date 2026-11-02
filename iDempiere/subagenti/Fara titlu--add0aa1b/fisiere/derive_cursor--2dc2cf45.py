from pathlib import Path
w=Path('D:/CodexWork/a06ex')
gate=(w/'gateway.py').read_text(encoding='utf8').replace('cesiro.sock','cursor.sock').replace("w/'port'","w/'portcursor'").replace('p01synthetic','p01cursor').replace('relay-settings.json','cursor-settings.json').replace('stop-relay','stop-cursor')
(w/'gateway-cursor.py').write_text(gate,encoding='utf8')
code=(w/'relay.py').read_text(encoding='utf8').replace('from p01_cesiro_contract_lab import create_real_api','from p01_cesiro_contract_lab import create_real_api,create_fixture,close_fixture').replace("slugs={t['slug'] for t in q['synthetic_tenants'].values()}","slugs={'canal-a','canal-b'}").replace("dest=here/'relay-local.json'","dest=here/'relay-cursor.json'").replace("key=secrets.token_urlsafe(24);",'''cx,db,role,T,O=create_fixture()
(here/'cursor-seed.json').write_text(json.dumps({'db':db,'tenant_ids':T,'order_ids':O},indent=2))
key=secrets.token_urlsafe(24);''').replace(" if request.method!='GET'",''' f=here/'fault-cursor.txt'
 if f.exists():
  mode=f.read_text().strip()
  if mode in ('429','500') and request.path.endswith('/orders'):return ('synthetic failure',int(mode))
  if mode=='partial' and request.path.endswith('/orders'):
   from flask import jsonify
   return jsonify({'items':[],'total':3,'pages':3,'page':1,'per_page':1})
  if mode=='truncated' and request.path.endswith('/orders'):return ('{"items":[',200)
  if mode=='timeout' and request.path.endswith('/orders'):
   import time
   time.sleep(1.5)
  if mode=='detail500' and request.path.endswith(str(O[1])):return ('synthetic detail failure',500)
 if request.method!='GET' ''').replace("Q checkout rows in synthetic PG a08_cesiro","isolated exercise 3+1 orders in its literal native schema").replace("'/sourcekey'","'/cursorkey'").replace('cesiro.sock','cursor.sock').replace("gate=here/'gateway.py'","gate=here/'gateway-cursor.py'").replace("w+'/gateway.py'","w+'/gateway-cursor.py'").replace('python3 gateway.py','python3 gateway-cursor.py').replace("if (here/'end-relay').exists()","""if (here/'advance-cursor').exists() and not (here/'advanced-cursor').exists():
    cx.execute("update sales.orders set updated_at='2026-11-02 10:00:03+00' where id=%s",(O[1],))
    (here/'advanced-cursor').write_text('done')
   if (here/'end-cursor').exists()""").replace(' if server is not None and server.poll() is None:server.terminate()',' if server is not None and server.poll() is None:server.terminate()\n close_fixture(cx,db,role)')
(w/'relay-cursor.py').write_text(code,encoding='utf8')

