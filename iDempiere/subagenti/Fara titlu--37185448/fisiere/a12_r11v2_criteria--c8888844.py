from a12_r11x_base import *
rt=read(E/'R10/Registru_reexecutare_R10.json')['rows']
for task in ['T216','T224','T355','T331','T171','T201','T257','T232','T232.01']:
 print('\n',task)
 for i,r in enumerate(rt):
  if r['task']==task:print(i,r['criterion'],r['text'][:300])
for z in ['A03','A08']:
 for f in (O/z).glob('Fisa_*.json'):
  j=read(f);x=j.get('dispatch',j.get('file',{}));print(z,f.name,x.get('task_candidates',x.get('related_tasks',[])))

