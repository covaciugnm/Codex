from a12_r10_publish import *
for n in ['A03','A04','A05','A07','A08','A09','A06','A01','A10']:
 d=rd(B/(n+'_plan.json')); ps=d.get('pipelines',d.get('pipeline_catalog',d.get('pipeline',d.get('pipelineuri',[]))));cs=d.get('controls',d.get('checklists',d.get('controale',[])))
 print('ZONE',n,'pipes',[(q.get('id',q.get('pipeline_id')),q.get('title',q.get('business_outcome',q.get('nume','')))[:50])for q in ps]);print('keys',list(cs[0])if cs else'none')
 for q in cs:
  id=q.get('id',q.get('control_id'));title=next((q[k]for k in ['title','name','control','nume','obiectiv','scope','objective','risk']if isinstance(q.get(k),str)),'')
  pi=q.get('pipelines',q.get('pipeline',q.get('pipeline_ids',q.get('pipeline_id'))))
  print(id,title[:61],pi)
print('IFC',[(z['id'],z['from'],z['to'],z['contract'])for z in rd(B/'Matrice_interfete.json')['contracts']])

