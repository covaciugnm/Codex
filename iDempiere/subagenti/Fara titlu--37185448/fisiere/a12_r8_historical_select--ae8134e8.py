from a12_r8_cases import *
fmap=[('T224-',r'21[ ×x]+5|21.*5 coloane|21 de comituri|21 comituri|21 rânduri'),('T213-',r'C_Campaign.{0,45}(canal|marketing)|campania de marketing|campania canalului'),('T204-',r'D1215.{0,80}T203|D-ORC-1.{0,130}retras'),('T314-',r'Blocat din cod|doar cheia VALIDATA|rânduri VALIDATA/RESPINSA|fișe VALIDATA|fișele VALIDATA'),('T216-',r'rendare.*(serie|număr)|serie.*afiș|documente în cont'),('T17-',r'SmartFin')]
for t,p in fmap:
 h=[]
 for z in a:
  if ('/'+t)not in z['file']or z['size']>130000 or(re.search(r'mutant.*/M|_M[0-9]',z['file'])):continue
  ls=txt(z).splitlines(); hits=[(i,v[:220])for i,v in enumerate(ls,1)if re.search(p,v,re.I)]
  if hits:h.append((z['file'].split('/',3)[-1],hits[:1]))
 h.sort(key=lambda v:(v[0].endswith('.md'),not ('verdict'in v[0]),v[0]));print(t,len(h));print(h[:5])

