import sys,os,tempfile,subprocess,threading,datetime,json,hashlib,urllib.request,http.client,socket,time,shutil,re
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
W=Path(r'D:\CodexWork\a01-r11-frozen');rule=W/'new/proxy/traefik/propuneri-t232/_erp-admin-blocat.yml';apply=W/'new/proxy/traefik/propuneri-t232/aplica.sh';traefik=Path(r'D:\CodexWork\p01-traefik-3.1.7\traefik.exe');gitbash=Path(r'C:\Program Files\Git\bin\bash.exe');assert traefik.is_file() and gitbash.is_file();real=[];h=lambda b:hashlib.sha256(b).hexdigest()
class Upstream(BaseHTTPRequestHandler):
 def log_message(self,*a): pass
 def do_GET(self):
  real.append({'case':self.headers.get('X-A01-Trace',''),'host':self.headers.get('Host',''),'path':self.path});body=b'fixture-control-200';self.send_response(200);self.send_header('content-length',str(len(body)));self.end_headers();self.wfile.write(body)
def freeport():
 with socket.socket() as ss:ss.bind(('127.0.0.1',0));return ss.getsockname()[1]
def bashsim():
 with tempfile.TemporaryDirectory(prefix='a01-r11-simul-') as folder:
  target=Path(folder)/'target';target.mkdir();(target/'unchanged.yml').write_text('# canary');dv=Path(folder)/'evidence';env={**os.environ,'EVA_T232_DYN_TINTA':target.as_posix(),'EVA_T232_DOVEZI':dv.as_posix()};path=apply.absolute().as_posix();posix='/'+path[0].lower()+path[2:];before=[(p.name,h(p.read_bytes())) for p in target.iterdir()];r=[];
  for args in [['--simulare'],['--simulare'],['--unsupported']]:
   p=subprocess.run([str(gitbash),posix,*args],env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=12);r.append({'args':args,'exit':p.returncode,'output':p.stdout+p.stderr});
  after=[(p.name,h(p.read_bytes())) for p in target.iterdir()];return {'rows':r,'before':before,'after':after,'unchanged':before==after,'evidence_dir_created':dv.exists(),'production_apply_called':False}
def runner(use_rule):
 up=ThreadingHTTPServer(('127.0.0.1',0),Upstream);threading.Thread(target=up.serve_forever,daemon=True).start();port=freeport();
 with tempfile.TemporaryDirectory(prefix='a01-r11-traefik-') as folder:
  root=Path(folder);dyn=root/'dynamic';dyn.mkdir();seed=dyn/'erp-positive.yml';seed.write_text('http:\n  routers:\n    fixture-default:\n      rule: "PathPrefix(`/`)"\n      entryPoints: [web]\n      priority: 1\n      service: allowed-fixture\n  services:\n    allowed-fixture:\n      loadBalancer:\n        servers:\n          - url: "http://127.0.0.1:'+str(up.server_port)+'"\n',encoding='utf8');
  if use_rule:shutil.copyfile(rule,dyn/rule.name)
  log=root/'access.jsonl';static=root/'traefik.yml';static.write_text('entryPoints:\n  web:\n    address: "127.0.0.1:'+str(port)+'"\nproviders:\n  file:\n    directory: "'+dyn.as_posix()+'"\n    watch: false\nlog:\n  level: ERROR\naccessLog:\n  format: json\n  filePath: "'+log.as_posix()+'"\n',encoding='utf8');std=root/'diag.log';f=std.open('wb');proc=subprocess.Popen([str(traefik),'--configFile='+str(static)],cwd=root,stdout=f,stderr=f,creationflags=subprocess.CREATE_NO_WINDOW);rows=[]
  def req(label,host,path,ip='127.0.0.2',headers=None):
   conn=http.client.HTTPConnection('127.0.0.1',port,timeout=4,source_address=(ip,0));before=len(real);conn.request('GET',path,headers={'Host':host,'X-A01-Trace':label,**(headers or {})});r=conn.getresponse();data=r.read();loc=r.getheader('Location');conn.close();return {'case':label,'host':host,'raw_path':path,'client_ip':ip,'http':r.status,'redirect':loc,'business_upstream_hits':real[before:],'body_sha256':h(data)}
  try:
   for n in range(80):
    try:req('readiness','neutral.fixture','/ready');break
    except (OSError,http.client.HTTPException):time.sleep(.07)
   else:raise RuntimeError('no local ingress; '+std.read_text(errors='replace')[:450])
   host='erp-synthetic.eva-org.com';cases=[('osgi',host,'/osgi'),('monitor',host,'/idempiereMonitor'),('server',host,'/server'),('osgi-child',host,'/osgi/system/console'),('encoded',host,'/%2e%2e/osgi'),('matrix',host,'/..;/osgi'),('webui-normal',host,'/webui/zkau/web/js/zk.wpd'),('normal-similar-prefix',host,'/serverless-fixture'),('normal-dotdot-in-name',host,'/webui/assets/a..b.css'),('java-subhost','cesiro-java-dev.eva-org.com','/osgi'),('not-covered-host','neutral.fixture','/osgi'),('other-domain','erp-synthetic.other.invalid','/server'),('repeat-denial',host,'/osgi')];
   for case,hos,pa in cases:rows.append(req(case,hos,pa))
   rows.append(req('forged-forwarded-for',host,'/osgi',headers={'X-Forwarded-For':'127.0.0.1'}));rows.append(req('trusted-source-localhost-not-403',host,'/osgi',ip='127.0.0.1'))
  finally:
   proc.terminate();proc.wait(timeout=8);f.close();up.shutdown();up.server_close()
  logs=[json.loads(l) for l in (log.read_text(encoding='utf8').splitlines() if log.exists() else []) if l.strip()];
  for row in rows:
   matches=[v for v in logs if v.get('RequestHost')==row['host'] and v.get('DownstreamStatus')==row['http'] and (v.get('RequestPath')==row['raw_path'] or urllib.parse.unquote(v.get('RequestPath',''))==urllib.parse.unquote(row['raw_path']))];row['candidate_router_names_in_access_log']=list(dict.fromkeys(v.get('RouterName') for v in matches));
  return {'rule_in_local_provider':use_rule,'rule_hash_in_provider':h((dyn/rule.name).read_bytes()) if use_rule else None,'diag':std.read_text(errors='replace')[:600],'static_config_sha256':h(static.read_bytes()),'raw_log_count':len(logs),'access_rows':[{'path':v.get('RequestPath'),'host':v.get('RequestHost'),'http':v.get('DownstreamStatus'),'router':v.get('RouterName'),'service':v.get('ServiceName'),'origin_status':v.get('OriginStatus')} for v in logs],'rows':rows,'production_mount_observed':False}
res={'utc':datetime.datetime.now(datetime.UTC).isoformat(),'traefik_binary_sha256':h(traefik.read_bytes()),'binary_version':subprocess.run([str(traefik),'version'],capture_output=True,text=True,timeout=4).stdout,'rule_source_sha256':h(rule.read_bytes()),'unapplied_control':runner(False),'applied_local_copy_only':runner(True),'simulation':bashsim(),'scope':'Two temporary standalone loopback Traefik v3.1.7 instances, sequential, no cabinet, remote daemon or production changes. The genuine proposal is loaded only in the second temporary provider; the source range 127.0.0.1 is exercised with local source 127.0.0.2 negative+127.0.0.1 positive. TLS and the production topology are not tested.'};(W/'traefik-results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('denial/allowed',[(x['case'],x['http'],len(x['business_upstream_hits'])) for x in res['applied_local_copy_only']['rows']]);print('simulation',res['simulation']['unchanged'],[(q['args'],q['exit']) for q in res['simulation']['rows']])
