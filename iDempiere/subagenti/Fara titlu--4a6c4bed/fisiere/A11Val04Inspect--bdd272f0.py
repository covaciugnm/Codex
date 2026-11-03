import json,pathlib,collections,hashlib
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
oldp=R/'executie/delta/2026-11-03T00-39-34-490Z'
newp=R/'executie/delta/2026-11-03T01-43-37-057Z'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
old=j(oldp/'00_STATUS_TASKURI.json');new=j(newp/'00_STATUS_TASKURI.json')
def key(x):return (x.get('proiect'),x['id'])
a={key(x):(i,x) for i,x in enumerate(old)};b={key(x):(i,x) for i,x in enumerate(new)}
assert len(a)==len(old) and len(b)==len(new)
print('COUNTS',len(old),len(new),sum(x.get('proiect')=='P01' for x in old),sum(x.get('proiect')=='P01' for x in new))
print('ADDED',json.dumps([b[k] for k in b.keys()-a.keys()],ensure_ascii=False,indent=2))
print('REMOVED',a.keys()-b.keys())
for k in a.keys()&b.keys():
 if a[k][1]!=b[k][1]:
  x,y=a[k][1],b[k][1];fields={f for f in x.keys()|y.keys() if x.get(f)!=y.get(f)}
  print('CHANGED',k,a[k][0],b[k][0],json.dumps({f:{'old':x.get(f),'new':y.get(f)} for f in fields},ensure_ascii=False,indent=2))
for p in oldp.glob('00_*.json'):
 q=newp/p.name
 print('HASH',p.name,hashlib.sha256(p.read_bytes()).hexdigest(),hashlib.sha256(q.read_bytes()).hexdigest(),p.read_bytes()==q.read_bytes())
plan=j(R/'executie/R12_plan_delta/Plan_delta_R12_v2.json')
print('PLAN_KEYS',list(plan))
for k,v in plan.items():
 if k in ['zones','contracts','pipeline_contracts','original_contracts']:
  for x in v:
   if isinstance(x,dict) and ('G3' in json.dumps(x,ensure_ascii=False) or x.get('id') in ['A06','D04']):print('PLAN_G3',k,json.dumps(x,ensure_ascii=False)[:12000])
