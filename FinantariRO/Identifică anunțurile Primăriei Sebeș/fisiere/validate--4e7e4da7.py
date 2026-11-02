import io,zipfile,sqlite3,json,hashlib,time,struct,traceback
from pathlib import Path
from loguru import logger
from androguard.core.dex import DEX
logger.disable('androguard')
R=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository')
O=Path(r'D:\Codex\iFLYTEK-audit\results'); cache=O/'independent-validation.json'
results=json.loads(cache.read_text()) if cache.exists() else {}
def digest(items):return hashlib.sha256('\n'.join(sorted(items)).encode()).hexdigest()
def check(b):
 h=hashlib.sha256(b).hexdigest()
 if h in results:return
 try:
  d=DEX(b);methods=[];fields=[];instructions=0;sampled=0
  for c in d.get_classes():
   for m in c.get_methods():
    methods.append(m.get_class_name()+'->'+m.get_name()+m.get_descriptor().replace(' ',''))
    if m.get_code() and (m.get_method_idx()%101==0):
     instructions+=sum(1 for _ in m.get_instructions());sampled+=1
   for f in c.get_fields():fields.append(f.get_class_name()+'->'+f.get_name()+':'+f.get_descriptor())
  results[h]=dict(classes=len(d.get_classes()),defined_methods=len(methods),defined_fields=len(fields),method_signature_digest=digest(methods),field_signature_digest=digest(fields),sampled_code_methods=sampled,sampled_instructions=instructions,parser='androguard 4.1.4')
 except Exception:results[h]={'error':traceback.format_exc()}
 cache.write_text(json.dumps(results,indent=2),encoding='utf-8'); print(h[:12],results[h],flush=True)
def component(z):
 for e in z.infolist():
  if e.filename.endswith('.dex'):check(z.read(e))
inputs=list((R/'collection-2026-11-01/applications').glob('*.apk'))+list((R/'collection-2026-11-01/applications').glob('*.xapk'))+[p for p in (R/'apk-analysis-2026-11-01/.work/inputs').glob('*.apk') if not p.name.startswith('iflytek-')]+list(Path(r'D:\Codex\iFLYTEK-audit\stable-inputs').glob('*.apk'))
for p in inputs:
 print('INPUT',p.name,flush=True)
 with zipfile.ZipFile(p) as z:
  if p.suffix=='.xapk':
   for e in z.infolist():
    if e.filename.endswith('.apk'):component(zipfile.ZipFile(io.BytesIO(z.read(e))))
  else:component(z)
