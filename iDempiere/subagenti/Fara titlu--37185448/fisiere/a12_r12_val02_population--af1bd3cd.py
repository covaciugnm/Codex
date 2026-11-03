import json,pathlib,hashlib
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';O=E/'R12_fisiere/A12/Val_02'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p,pointer=None):
 b=p.read_bytes();r={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:r['pointer']=pointer
 return r
old=E/'delta/2026-11-02T23-15-23-444Z';new=E/'delta/2026-11-02T23-39-09-646Z';a=load(old/'00_STATUS_TASKURI.json');b=load(new/'00_STATUS_TASKURI.json');c=load(new/'Comparatie_ultimul_checkpoint.json')
assert c['hashes']==[sha((p/'00_STATUS_TASKURI.json').read_bytes()) for p in [old,new]]
ak={(r.get('proiect'),r['id']):(i,r) for i,r in enumerate(a)};bk={(r.get('proiect'),r['id']):(i,r) for i,r in enumerate(b)}
assert len(ak)==len(bk)==len(a)==len(b)==996 and set(ak)==set(bk)
changes=[]
for k,(i,x) in ak.items():
 j,y=bk[k];fields=[f for f in sorted(set(x)|set(y)) if x.get(f)!=y.get(f)]
 if fields:changes.append({'project':k[0],'alias':k[1],'old_source':ref(old/'00_STATUS_TASKURI.json','/'+str(i)),'new_source':ref(new/'00_STATUS_TASKURI.json','/'+str(j)),'fields':[{'name':f,'before':x.get(f),'after':y.get(f)} for f in fields]})
assert len(changes)==1 and changes[0]['alias']=='T240' and changes[0]['project']=='P01'
assert {x['name'] for x in changes[0]['fields']}=={'procent','observatii','ultima_actualizare'}
assert all(ak[k][1].get('stare_generala')==bk[k][1].get('stare_generala') for k in ak)
x=ak[('P01','T240')][1];y=bk[('P01','T240')][1]
assert x['procent']==96 and y['procent']==97 and x['stare_generala']==y['stare_generala']=='implementare'
assert y['cod_capitol']=='P01.C14.T0001'
data={'schema':'eva.audit.r12.population-supplement/2','utc':datetime.now(timezone.utc).isoformat(),'head':c['head'],'method':'READ_ONLY_METADATA_COMPARE; no product test, no tracker writes',
 'captures':[{'role':label,'source':ref(d/'00_STATUS_TASKURI.json'),'all_capture_files_rehashed':[ref(p) for p in sorted(d.iterdir()) if p.is_file()]} for label,d in [('previous',old),('latest',new)]],
 'comparison_source':ref(new/'Comparatie_ultimul_checkpoint.json'),
 'independent_comparison':{'keys':['proiect','id'],'records_before':len(a),'records_after':len(b),'p01_before':sum(r.get('proiect')=='P01' for r in a),'p01_after':sum(r.get('proiect')=='P01' for r in b),'added':[],'removed':[],'state_changes':[],'changes':changes},
 'task':{'alias':'T240','canonical':'P01.C14.T0001','state':'implementare','declared_progress':[96,97],'latest_edit_declared':y['ultima_actualizare'],'exact_completion_date':None,'date_status':'N/A_ACTIVE; estimated dates and last edit are not completion dates','cohort_membership':'OUTSIDE_HISTORIC_652','owner':'A08','planned_peer':'A09','independent_reviewer':'A11'},
 'new_claims':[{'claim':'RR texte + D-108…113, t240-impl-texte 5a6702ca869, JAR a5d48ce2…, 286/0; refs0 with args and rc2 without args','status':'DECLARED_OTHER_BRANCH_NOT_ACCEPTED_ON_DF85','action':'Require exact branch commit/full JAR hash, criteria, logs, implementation/installed distinction and A11 delta acceptance before credit; no automatic closure of Val01 or current helper findings.'},{'claim':'Targeted reaudit r2/86_, future master integration and official L6, then §37/§36','status':'PLANNED_OR_IN_PROGRESS_NOT_COMPLETED','action':'Keep original native screens/roles/RO-EN/capture/privacy/help contracts open; the helper component tests do not replace official native L6.'},{'claim':'Estimated close 10–14.11 (maximum23.11 20:00)','status':'ESTIMATE_NOT_A_DATE_OF_COMPLETION','action':'Do not invent closure or add T240 to historic652.'},{'claim':'T-NOU proposed WSagaMasiniForm dd.MM.yyyy+STRICT rejects dates (D-240-118)','status':'INVESTIGATION_SIGNAL_WITHOUT_CANONICAL_ASSIGNMENT','action':'Keep WSagaMasiniForm at SHARED_NO_TASK_ASSIGNED; attach its exact parser evidence only after A11 receipt. The T240 observation is provenance, not a new commercial task ID.'}],
 'plan_impact':{'technical_inventory_change':False,'cohort_change':False,'approved_method_still_applicable':True,'execution_credit_from_tracker':0,'candidate':'df85d33c1648ce2b2df130a60a05ef696e2e5480','business_tasks_or_criteria_created':0,'approved_plan':ref(E/'R12_plan_delta/Plan_delta_R12_v2.json'),'gate':ref(E/'R12_plan_delta/A11_verdict_plan_delta_R12_v2.json'),'native_contracts_still_open':17,'T343_CO_IP':{'status':'OPEN_NOMINAL_ORACLE_CONFLICT','previous_supplement':ref(E/'R12_plan_delta/A12/Supliment_populatie_2315.json'),'independent_receipt':ref(E/'R12_plan_delta/Receptie_A11_supliment_T343_2315_v1.json'),'oracle':'CO|CO|CO until nominal amendment received; IP is neither automatically accepted nor automatically a product defect'}},
 'invariants':{'total_records':996,'P01':693,'historic_tasks':652,'historic_criteria':2619,'technical_files':6728,'no_credit_transfer_from_R11':True,'previous_waves_unchanged':True},
 'resources':{'A12_product_processes_created':0,'A12_product_tests_executed':0,'A12_operational_writes':0},'score':None}
assert data['independent_comparison']['p01_before']==data['independent_comparison']['p01_after']==693
O.mkdir(parents=True,exist_ok=True);p=O/'Supliment_populatie_2339.json';assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(ref(p),ensure_ascii=False))
