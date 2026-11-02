from pathlib import Path
import subprocess,socket,secrets,sys,os,logging,json,datetime,threading,contextlib,urllib.parse
def digest(b):import hashlib;return hashlib.sha256(b).hexdigest()
sys.path.insert(0,'D:/CodexWork');from p01_cesiro_contract_lab import create_real_api
from werkzeug.serving import make_server
from flask import request
here=Path('D:/CodexWork/a06ex');base=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/supliment_CESIRO1/probe');q=json.loads((base/'EX03_C_Q_raw.json').read_text());slugs={t['slug'] for t in q['synthetic_tenants'].values()};dest=here/'relay-local.json'
os.environ.update(PGPASSFILE='D:/CodexWork/p01-local-pg16/pgpass.conf',PGOPTIONS='-c default_transaction_read_only=on',DATABASE_URL='postgresql+psycopg://audit_owner@127.0.0.1:56481/a08_cesiro',ADMIN_DATABASE_URL='postgresql+psycopg://audit_owner@127.0.0.1:56481/a08_cesiro',NO_PROXY='127.0.0.1,localhost')
key=secrets.token_urlsafe(24);os.environ['EXTERNAL_API_KEYS_SHA256']=digest(key.encode())
app=create_real_api();events=[];logging.getLogger('werkzeug').setLevel(logging.ERROR)
@app.before_request
def guard():
 if request.method!='GET' or not request.path.startswith('/api/ext/v1/'):return ('denied',403)
 if request.path.endswith('/orders') or '/orders/' in request.path:
  if request.args.get('tenant') not in slugs:return ('fixture tenant only',403)
 if not (request.path.endswith('/health') or '/orders' in request.path):return ('fixture route only',403)
@app.after_request
def observe(res):
 data=res.get_json(silent=True) or {};ev={'path':request.path,'query':request.args.to_dict(),'http':res.status_code,'rows':[v.get('id') for v in data.get('items',[])] if isinstance(data,dict) and isinstance(data.get('items'),list) else [],'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 events.append(ev);dest.write_text(json.dumps({'origin':'Real CESIRO1 ext_bp with A08 Q checkout rows in synthetic PG a08_cesiro, restricted to A/B, synthetic key never exported to report, original endpoint SQL READ ONLY','events':events},indent=2),encoding='utf8');return res
w=(here/'remote.txt').read_text().strip();host='saga-server@192.168.100.151';opts=['-o','BatchMode=yes','-o','StrictHostKeyChecking=yes']
port=make_server('127.0.0.1',0,app);server=None;confirm=None
try:
 # The key is synthetic and is delivered in stdin only inside the exclusive test folder; never printed.
 subprocess.run(['ssh',*opts,host,'umask 077; cat > '+w+'/sourcekey'],input=key.encode(),check=True)
 pipe=subprocess.Popen(['ssh',*opts,'-o','ExitOnForwardFailure=yes','-N','-R',w+'/cesiro.sock:127.0.0.1:'+str(port.server_port),host],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 gate=here/'gateway.py';subprocess.run(['scp','-q',*opts,str(gate),host+':'+w+'/gateway.py'],check=True)
 server=subprocess.Popen(['ssh',*opts,host,'cd '+w+' && python3 gateway.py'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 import time
 for _ in range(8):
  if pipe.poll() is not None: raise AssertionError(str(pipe.stderr.read())[:350])
  time.sleep(.1)
 threading.Thread(target=port.serve_forever,daemon=True).start()
 print('Source bridge started for exact A08 test tenants on isolated ERP subnet',flush=True)
 try:
  for _ in range(1500):
   if (here/'end-relay').exists() or server.poll() is not None:break
   time.sleep(1)
 finally:
  port.shutdown()
finally:
 port.server_close()
 if 'pipe' in locals() and pipe.poll() is None:pipe.terminate()
 if server is not None and server.poll() is None:server.terminate()

