from readgit import *
from collections import defaultdict
criteria={'T22-status':r'C05.*C18|26.*bulin|36.*rând|verde.*ro[șs]u','T22-doc':r'Action=Zoom|Record_UU|Record_ID|zoom|fereastr[ăa] nou|refuz.*document|document.*alt[ăa] firm','T22-chan':r'suprascri|valoar.{1,45}nativ|valoarea.{0,15}efectiv|valoarea.{0,15}efectiv|proprietar.{0,35}câmp|nativ.{0,25}canal|fi[șs]a individual.{0,20}articol','T35-active':r'alt[ăa] firm|inactiv|neperm|[Ss]criere permis[ăa]|fiș[aă] dezactivat|poart[aă]|cheie.*masc|T35 L1'}
# inspect top pinned documents, cache entries only, without network.
ls=listing(roots)
out=defaultdict(list)
for path,oid in ls:
 if path.count('/')!=3 or not path.endswith('.md'):continue
 try:d=get(path,oid)
 except Exception:continue
 if not d:continue
 lines=d.decode('utf8','replace').splitlines()
 for k,pat in criteria.items():
  if ('/T35-' in path)!=k.startswith('T35') or (not '/T22-' in path and not '/T35-' in path):continue
  hh=[(n,t) for n,t in enumerate(lines,1) if re.search(pat,t,re.I)]
  if hh:out[k].append({'path':path,'oid':oid,'sha256':hashlib.sha256(d).hexdigest(),'hits':hh})
(w/'hits.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf8')
for k,rr in out.items():print(k,len(rr),sum(len(x['hits']) for x in rr));print([(x['path'].split('/')[-1],len(x['hits'])) for x in rr if len(x['hits'])>=3][:15])

