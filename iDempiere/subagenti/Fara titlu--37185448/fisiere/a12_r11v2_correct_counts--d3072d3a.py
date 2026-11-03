from a12_r11x_base import *
import copy,shutil
V=A/'Val_02';old=V/'Handoff_val_02.json';m=read(V/'Matrice_criterii_task_probe.json');rep=read(old)
ct=sum(bool(x['R11_cases'])for x in m['criterion_rows']);tt=sum(bool(x['R11_direct_cases'])for x in m['task_rows']);assert (ct,tt)==(12,5)
actual_crit={x['criterion']for x in m['nominal_links']};actual_tasks={x['task']for x in m['nominal_links']};assert len(actual_crit)==ct and len(actual_tasks)==tt
before={k:rep['counts'][k]for k in ['criteria_with_direct_partial_observation','tasks_with_direct_observation']}
rep['counts']['criteria_with_direct_partial_observation']=ct;rep['counts']['tasks_with_direct_observation']=tt
rep['utc']=now();rep['revision']='VAL02_V2_CORRECTION_NUMERATOR';rep['supersedes_summary_only']={'source':ref(old),'corrected_fields':before,'reason':'Numărul cheilor de defaultdict creștea prin citirea pozițiilor fără probă. Numărătorul corect folosește numai listele de cazuri ne-goale, independent din matricea serializată. Rândurile de fișier și matricea nu sunt schimbate.'}
out=V/'Handoff_val_02_v2.json';save(out,rep)
q=read(V/'Verificare_val_02.json');q['utc']=now();q['report']=ref(out);q['additional_crosscheck']={'explicit_links':len(m['nominal_links']),'distinct_criteria':len(actual_crit),'distinct_tasks':len(actual_tasks),'nonempty_task_rows':tt,'nonempty_criterion_rows':ct,'all_task_file_hashes_verified':652,'prior_summary_count_issue':'superseded_by_v2; no change to any underlying evidence or task verdict'}
qa=V/'Verificare_val_02_v2.json';save(qa,q)
script=Path(__file__);shutil.copyfile(script,V/'metoda'/script.name)
fm=V/'MANIFEST_val_02_v2.json';save(fm,{'utc':now(),'head':head,'effective_report':ref(out),'effective_QA':ref(qa),'prior_manifest':ref(V/'MANIFEST_val_02.json'),'supersession':'Manifest v2 și Handoff v2 sunt ediția de predare; vechile cifrele de sumar sunt păstrate în Handoff_val_02.json pentru trasabilitatea corecției.','files':[ref(p)for p in sorted(V.rglob('*'))if p.is_file()and p!=fm],'self_reference':False})
for e in read(fm)['files']:assert sha(B/e['path'])==e['sha256']
print('MANIFEST',ref(fm),'REPORT',ref(out),'QA',ref(qa),'COUNTS',rep['counts'])

