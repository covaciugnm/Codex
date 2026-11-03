import json,pathlib,hashlib
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');A=R/'executie/delta/2026-11-03T01-43-37-057Z';B=R/'executie/delta/2026-11-03T02-45-48-441Z'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
key=lambda x:(x.get('proiect'),x['id'])
a=j(A/'00_STATUS_TASKURI.json');b=j(B/'00_STATUS_TASKURI.json');am={key(x):x for x in a};bm={key(x):x for x in b}
out={'before':len(a),'after':len(b),'P01_before':sum(x.get('proiect')=='P01' for x in a),'P01_after':sum(x.get('proiect')=='P01' for x in b),'added':list(bm.keys()-am.keys()),'removed':list(am.keys()-bm.keys()),'changed':[],'auxiliary':[]}
for k in sorted(am.keys()&bm.keys(),key=str):
 if am[k]!=bm[k]:out['changed'].append({'key':k,'changes':{f:{'before':am[k].get(f),'after':bm[k].get(f)} for f in sorted(am[k].keys()|bm[k].keys()) if am[k].get(f)!=bm[k].get(f)}})
for p in A.glob('00_*.json'):out['auxiliary'].append({'name':p.name,'identical':p.read_bytes()==(B/p.name).read_bytes()})
print(json.dumps(out,ensure_ascii=False,indent=2))
