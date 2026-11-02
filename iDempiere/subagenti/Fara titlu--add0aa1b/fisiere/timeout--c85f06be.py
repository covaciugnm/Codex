import concurrent.futures,http.server,threading,time,sys,json,hashlib,datetime,subprocess,os,secrets
from pathlib import Path
w=Path(__file__).resolve().parent;s=Path('D:/CodexWork/eva-audit-secondary-20261102')
e=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/supliment_CESIRO1/probe')
evidence=e/'EX04-evidence';basefile=e/'EX04.json';digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
calls=[];gate=threading.Event()
class Receiver(http.server.BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if not self.path.startswith('/api/ext/v1/orders'):self.send_error(404);return
  calls.append({'method':'GET','path':self.path,'when':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  gate.wait(205)
class S(http.server.ThreadingHTTPServer):daemon_threads=True
server=S(('127.0.0.1',0),Receiver);t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
def one(k):
 jar=s/('cod-master-contab.jar' if k=='git' else 'com.eva.ro.contab_13.0.0.jar');cp=';'.join([str(w/('classes-'+k)),str(jar),str(s/'org.adempiere.base_13.0.0.202603090043.jar'),str(s/'org.adempiere.base.process_13.0.0.202603090043.jar'),'D:/CodexWork/a05-support-jars/*','D:/CodexWork/eva-a01-java/lib/*'])
 beg=time.monotonic()
 x=subprocess.run(['C:/Program Files/Java/jdk-21/bin/java.exe','-Dstdout.encoding=UTF-8','-Duser.timezone=UTC','-cp',cp,'com.eva.ro.contab.corelare.Ex04Wire',f'http://127.0.0.1:{server.server_port}/api/ext/v1','canal-a','2026-11-02 00:00:00','2026-11-03 00:00:00','null'],env={**os.environ,'EX04_FIXTURE_KEY':secrets.token_urlsafe(15)},timeout=201,encoding='utf8',text=True,capture_output=True)
 return {'jar':k,'jar_sha256':digest(jar),'elapsed_s':round(time.monotonic()-beg,2),'java_returncode':x.returncode,'result':x.stdout.strip().splitlines()}
try:
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:res=list(ex.map(one,['git','installed']))
finally:gate.set();server.shutdown();server.server_close()
payload={'schema':'eva.audit.EX04.timeout.addendum','base_EX04_sha256':digest(basefile),'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case':'CURSOR-01, timeout','expected':'configured Java HTTP request timeout (~180s), no successful list or swallowed empty page','execution':'Two concurrent original Java clients call an isolated loopback listener which accepts TCP and deliberately sends no headers/body. No partners, no source or ERP writes. This steps past native Java network stack and connector; no new native PreiaDinSite execution in this timed scenario. Its throw/checkpoint handling on 429/500/truncation is in separate evidence.','results':res,'http_accepts':calls,'cleanup':'Listener and both Java process handles closed.','quality_score':None}
assert len(calls)==2 and all(o['elapsed_s']>=178 and any('HttpTimeoutException' in l for l in o['result']) for o in res),res
file=e/'EX04_timeout_addendum.json';assert not file.exists();file.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf8');print(file.name,digest(file),res,flush=True)

