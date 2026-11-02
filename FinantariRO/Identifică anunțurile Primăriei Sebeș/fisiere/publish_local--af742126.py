import shutil,hashlib,json,time
from pathlib import Path
S=Path(r'D:\Codex\iFLYTEK-audit\deliverable');D=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository\apk-protocol-audit-2026-11-01')
assert not D.exists(),'Destination already exists; inspect before changing it'
shutil.copytree(S,D);print('COPIED',str(D),flush=True)
items=json.loads((D/'SHA256SUMS.json').read_text(encoding='utf-8'))
for i,e in enumerate(items):
 p=D/e['path'];assert p.stat().st_size==e['bytes'];h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 assert h.hexdigest()==e['sha256'],e['path']
 if i%20==0:print('VERIFIED',i+1,'/',len(items),flush=True)
print('ALL HASHES VERIFIED',len(items),flush=True)
