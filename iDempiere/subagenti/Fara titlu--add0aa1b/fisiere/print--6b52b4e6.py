from readgit import *
d=json.loads((w/'hits.json').read_text(encoding='utf8'))
for k,items in d.items():
 print(k)
 for f in items:
  name=f['path'].split('/')[-1]
  if ((k=='T22-doc' and name.startswith(('74m_','96c_','76_'))) or (k=='T22-chan' and name.startswith(('71_','98_backend_','75k_'))) or (k=='T22-status' and name.startswith(('09_','74m_')))):
   for n,t in f['hits'][:6]:print(name,n,t[:470])

