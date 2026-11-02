from a12_r8_review import *
from functools import lru_cache
R8=E/'R8';P9=E/'R9_pregatire/A12';P9.mkdir(parents=True,exist_ok=True);r8=rd(R8/'Registru_reexecutare_R8.json')['all_rows'];r8map={x['criterion']:x for x in r8};r7=rd(E/'R7_pregatire/A12/Clasificare_nominala_1587.json')['records'];r7map={x['criterion']:x for x in r7};r7reg={r['criterion']:r for r in rd(E/'R7/Registru_reexecutare_R7.json')['records']};q177=[x for x in r8 if x['in_467']and x['R8_status']=='NEEXECUTAT'];other=[x for x in r8 if x['R8_status']=='NEEXECUTAT'];ext=[r for r in other if r7map[r['criterion']]['has_partial_external']];no=[r for r in other if r7map[r['criterion']]['category'].startswith('ETALON')];a11=rd(E/'A11_control_A12_R8.json')
@lru_cache(maxsize=700)
def task(k):return rd(R8/'taskuri'/('Fisa_'+k+'.json'))
def cget(k,id):return next(c for c in criteria(task(k))if c['id']==id)
if __name__=='__main__':
 print('q',len(q177),len(other),len(ext),len(no));print('by-own',collections.Counter(x['owner']for x in q177));print('by-task',collections.Counter(x['task']for x in q177));print('A11',str(a11['semantic_adjudication'])[:4600]);print('R8 state',collections.Counter(v['R8_status']for v in r8 if v['in_467']))
 for row in q177[:4]:
  src=r7map[row['criterion']];o=r7reg[row['criterion']];print(row['criterion'],row['normative_text'][:220]);print({k:o[k]for k in ['entry_and_oracle_specific_to_case','R6_case_next_action','resource_boundaries']})

