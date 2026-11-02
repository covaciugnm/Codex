from a12_r9_source882 import *
for k in ['T22.15-R3-001','T36.18-R3-001']:
 s=r7map[k]['source_row'];w=task(k.split('-')[0]);p=s['source_file'];o=s['sha_or_git_blob'];pnt=s['source_position'];z=point(parse(p,o),pnt)
 print(k,s,'canonical',w['canonical'],'title',w['title'],'root raw',[(j,str(w.get(j))[:250])for j in ['state_at_new_capture','source_literal','closure_date']]);print('hist block',str(z)[:1600])
 print('w keys',list(w)[:55]);print('neighbors from tree')
 def collect(x,path=()):
  if isinstance(x,list):
   for i,y in enumerate(x):yield from collect(y,path+(str(i),))
  if isinstance(x,dict):
   names=[(a,v)for a,v in x.items()if isinstance(v,str)and a in ['id','serie','task','denumire','titlu','cod']]
   if any(re.search(re.escape(k.split('-')[0])+r'(?![\d.])',v,re.I)for a,v in names): yield (path,names)
   for ky,y in x.items():
    if isinstance(y,(dict,list)):yield from collect(y,path+(ky,))
 for f in [B/'capturi/00_STATUS_TASKURI.json',B/'capturi/00_STATUS_FINALIZATE.json']:
  if f.exists():print('live',f.name,list(collect(rd(f)))[:4])

