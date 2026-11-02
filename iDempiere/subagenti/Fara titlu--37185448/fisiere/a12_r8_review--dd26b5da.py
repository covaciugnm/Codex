from a12_r3_survey import rd,wr,sha,B,E,D,Path,collections,json,re
from datetime import datetime,UTC
R7=E/'R7';P=E/'R8_pregatire/A12';P.mkdir(parents=True,exist_ok=True)
def criteria(w):return sum([w[k]for k in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
def now():return datetime.now(UTC).isoformat()
def source(p):return {'file':p.relative_to(B).as_posix(),'sha256':sha(p)}
def r7w(k):return rd(R7/'taskuri'/('Fisa_'+k+'.json'))
if __name__=='__main__':
 a=rd(E/'A11_control_A12_R7.json')
 for k in ['semantic_adjudication','remaining_reaudit','hard_blockers']:print(k,json.dumps(a[k],ensure_ascii=False,indent=1)[:9000])
 tr=rd(E/'R7_pregatire/A12/Clasificare_nominala_1587.json')['records'];reg={r['criterion']:r for r in rd(R7/'Registru_reexecutare_R7.json')['records']}
 print(list(tr[0]),list(reg.values())[0].keys())
 for k in ['T216','T354']:
  w=r7w(k)
  for c in criteria(w):
   if c['id']in ['T216-R2-002','T216-R2-005','T216-R2-006','T354-R2-021','T354-R2-027']:print(c['id'],c['normative_content'],c['current'],[(x['evidence'],x['result'])for x in c['R7_new_scenarios']])
 print(tr[0].get('category'),collections.Counter(x['category']for x in tr));print([(x['owner'],x['criterion'],x.get('case_method')) for x in tr[:1]])

