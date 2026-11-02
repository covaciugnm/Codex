import datetime,json,os,socketserver,socket,selectors,threading,pathlib,subprocess
w=pathlib.Path(__file__).resolve().parent;assert w.name.startswith('eva-contab-codex-ex05.');app=(w/'auditor-app').read_text().strip()
inspect=json.loads(subprocess.check_output(['docker','inspect',app]))[0];assert inspect['Config']['Labels']['eva.sesiune']=='eva-contab-codex-p01ex05r1'
net=next(iter(inspect['NetworkSettings']['Networks']));i=json.loads(subprocess.check_output(['docker','network','inspect',net]))[0];assert i['Internal'];gateway=i['IPAM']['Config'][0]['Gateway'];ap_ip=inspect['NetworkSettings']['Networks'][net]['IPAddress']
class Proxy(socketserver.BaseRequestHandler):
 def handle(self):
  if self.client_address[0]!=ap_ip:return
  with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as so:
   so.settimeout(12);so.connect(str(w/'cesiro.sock'))
   se=selectors.DefaultSelector();se.register(so,selectors.EVENT_READ,self.request);se.register(self.request,selectors.EVENT_READ,so)
   with se:
    while True:
     hits=se.select(12)
     if not hits:break
     for k,flags in hits:
      data=k.fileobj.recv(65536)
      if not data:return
      k.data.sendall(data)
class S(socketserver.ThreadingTCPServer):allow_reuse_address=True;daemon_threads=True
with S((gateway,0),Proxy) as s:
 (w/'port').write_text(str(s.server_address[1]))
 # Local alias confined to the disposable sandbox; internal bridge has no route to any partner.
 subprocess.run(['docker','exec','-u','0',app,'sh','-c','printf "%s\\n" "$1 p01synthetic" >>/etc/hosts','sh',gateway],check=True)
 (w/'relay-settings.json').write_text(json.dumps({'gateway':gateway,'app_ip':ap_ip,'private':i['Internal'],'exact_peer_only':True,'url':'http://p01synthetic:'+str(s.server_address[1])+'/api/ext/v1'}))
 s.timeout=1
 end=datetime.datetime.now()+datetime.timedelta(minutes=23)
 while not (w/'finish').exists() and not (w/'stop-relay').exists() and datetime.datetime.now()<end:s.handle_request()

