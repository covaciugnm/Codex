import pathlib,json,collections
e=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
r=e/'R2'
rep=read(r/'A12_raport.json');d=read(r/'Dovezi_criterii.json');E=d['evidence']; cnt=collections.Counter();ex={}; refs=collections.Counter()
for f in rep['records']:
 j=read(r/f['file'])
 for c in j['operative_criteria_and_audit_criteria']:
  key=(c['kind'],c['current']['status']);cnt[key]+=1
  if key not in ex:ex[key]=[f['task'],c['normative_content'][:128],str(c['current']['observed'])[:120],c['current']['evidence_ids'][:2]]
for k,n in cnt.most_common():
 if 'NEEXEC' not in k[1]:print(n,k,ex[k])
for eid,v in E.items():refs[(v['level'],v['source'].split('/')[0] if '/' in v['source'] else v['source'][:16])]+=1
print(refs.most_common(15))
for z in ['A06','A07','A08','A09']:
 p=read(e/(z+'_raport.json')); print(z,p['counts'],p['limits'][:1] if 'limits' in p and isinstance(p['limits'],list) else '')
 print('eidx',type(p['evidence_index']),str(p['evidence_index'])[:470]);print('control1',list(p['controls'][0]),'pipe',list(p['pipelines'][0]))

