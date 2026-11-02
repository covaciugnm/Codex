import json,pathlib,collections,concurrent.futures
F=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R5')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
r=rd(F/'A12_raport.json'); ev=rd(F/'Dovezi_criterii.json')['evidence']
def task(rec):
 j=rd(F/rec['file']);return [(c,j['task'])for c in j['operative_criteria_and_audit_criteria']+j['R3_new_criteria']+j['R4_new_criteria'] if c.get('R5_measured_scenarios')]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:ls=[x for line in pool.map(task,r['records'])for x in line]
print(len(ls))
for c,tid in ls[::10]:
 sc=c['R5_measured_scenarios'][0];print(c['id'],c['current']['status'],str(c['normative_content'])[:130],str(sc)[:320])
cs=collections.Counter(x[0]['kind']for x in ls);print(cs)

