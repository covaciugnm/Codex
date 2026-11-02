import subprocess,pathlib,gzip,hashlib,re,sys,os,json
repo='D:/CodexWork/eva-audit-p01-src-20261101'; sha='6df998aee0e514d30856c461962afe99ebd0d113'; env={**os.environ,'GIT_NO_LAZY_FETCH':'1'};w=pathlib.Path('D:/CodexWork/a06-oracles')
roots='T22-flux-comenzi-cesiro-reconciliere-incasari T31-integrare-easysales T35-cadru-platforme-vanzari'.split()
def listing(roots):
 b=subprocess.check_output(['git','-C',repo,'ls-tree','-z','-r',sha,'--',*['Documentatie/echipa-2026-10-09/'+r for r in roots]],env=env)
 return [(v.split(b'\t')[1].decode(),v.split(b'\t')[0].split()[2].decode()) for v in b.split(b'\0') if v]
def get(path,oid):
 fn=pathlib.Path('D:/CodexWork');data=None
 for dirname in ('A12_evidence_20261102/blobs','a12-r8-archives','a12-r8-morearchive','a12-r8-spec-extra','a12-r8-preview'):
  cached=fn/dirname/(oid+'.gz')
  if cached.is_file():data=gzip.decompress(cached.read_bytes());break
 if data is None:
  proc=subprocess.run(['git','-C',repo,'cat-file','blob',oid],env=env,capture_output=True,timeout=3)
  if proc.returncode==0:data=proc.stdout
 if data is None:return None
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid
 return data
if __name__=='__main__':
 index={}
 for path,oid in listing(roots):
  if path.count('/')>3 or not path.endswith('.md'):continue
  if not re.search(r'(plan|spec|decizi|criter|propri|cerer|ecran|flux|proces|registr)',path.rsplit('/',1)[-1],re.I):continue
  try:d=get(path,oid)
  except Exception:continue
  if d is None:continue
  lines=d.decode('utf-8-sig',errors='replace').splitlines()
  hits=[(i,t) for i,t in enumerate(lines,1) if re.search(r'bulin|fereastr[ăa] nou|alt[ăa] firm|aceleiași firme|acces direct|alt cabinet|AD_Client_ID|ID-ul document|ID intern|fără trimiter|AD_Table_ID|record_id',t,re.I)]
  index[path]={'git_oid':oid,'sha256':hashlib.sha256(d).hexdigest(),'hits':hits}
 (w/'originals.json').write_text(json.dumps(index,ensure_ascii=False),encoding='utf8')
 print(len(index),sum(len(v['hits']) for v in index.values()))

