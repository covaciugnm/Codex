import json,pathlib,collections
E=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie');F=E/'R4'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
d=rd(F/'Dovezi_criterii.json');cc=collections.Counter((x['level'],x['source'].split('/')[0]) for k,x in d['evidence'].items() if k.startswith('EV4-')); print('EV4',sum(cc.values()),cc.most_common(12))
x=rd(F/'Registru_1868.json');a=x['records'][0];print('act',list(a));print({k:str(a[k])[:210] for k in ['action_id','requires_external_or_hardware','resource_split','individual_dependency','designated_entry_and_evidence','steps'] if k in a})
r=rd(F/'A12_raport.json');names=['T259','T257','T07.03','T08.03','T10.04','T10.06','T36.53','T352','T366'];keys={}
for t in names:
 c=rd(F/'taskuri'/('Fisa_'+t+'.json')); cs=c['operative_criteria_and_audit_criteria']+c['R3_new_criteria']+c['R4_new_criteria']
 print(t,[(x['id'],x['current']['status'])for x in cs if x in c['R4_new_criteria'] or (t in ['T257','T259','T352','T366'] and x in c['R3_new_criteria'])]);keys[t]=[x['current'].get('observed') for x in c['R4_new_criteria']]
print('external',collections.Counter(type(z['requires_external_or_hardware']).__name__ for z in x['records']));print('task',r['findings_requiring_decision'][:2])

