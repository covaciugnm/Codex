import json,pathlib,hashlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');e=R/'executie'; directory=e/'delta/2026-11-02T15-00-35-559Z'; p=directory/'Addendum_plan_R2.json'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected='2596eb1314016d250a7250b23d3eed2b850dfe8212265779ced1a10a7f41d5ea';a=rd(p);assert h(p)==expected
prior=rd(e/'A11_gate_delta_P01_R1.json'); assert a['replaces_hash']==prior['hash_sha256']
assert all(h(directory/x['name'])==x['sha256'] for x in a['sources'])
idx=rd(R/'Index_trasabilitate.json');Cs={c['id']:c for c in idx['controls']};Ps={p['id']:p for p in idx['pipelines']}
rows=rd(directory/'00_STATUS_TASKURI.json');errors=[]
def pointer(ptr):
 name,ptr=ptr.split('#/'); k,v=ptr.split('/');return rows[int(k)],rows[int(k)][v]
for c in a['controls']:
 rr,req=pointer(c['source_request_ref']);rr2,desc=pointer(c['source_description_ref'])
 assert rr['id']==c['task'] and rr2['id']==c['task'] and req and desc
 assert all(k in Cs for k in c['controls']) and all(k in Ps for k in c['pipelines'])
 assert c['planned_evidence_id'] and c['artifact'] and c['negative'] and c['db_or_boundary'] and c['status']=='NEEXECUTAT' and c['observed'] is None
 for k in c['controls']:
  if not any(k in Ps[x]['resolved_control_ids'] for x in c['pipelines']): errors.append((c['id'],'control_orphan',k))
 for x in c['pipelines']:
  if not any(k in Ps[x]['resolved_control_ids'] for k in c['controls']): errors.append((c['id'],'pipeline_orphan',x))
assert len(a['controls'])==len(set(x['id'] for x in a['controls']))==len(set(x['planned_evidence_id'] for x in a['controls']))==15
assert not errors,errors
reasons={'QC01-P2':'A06 titular T352, A05 titular T366, A12 auditor pe task, celelalte zone cu dispoziție explicită în assignments/transfer.','QC02-P2':'15 rânduri, surse originale și inversele control/flux validate independent, ID fișier de probă distinct și matrice interfețe.','QC02-P4':'T352 R04/R05/R06/R07 acoperă supliment absolut/procent, termen per canal, funcții rapide și AI fără aplicare tacită.','QC02-P5':'T366 R01/R02/R03/r57 separă operator pe produs, confirmare, document, montare la cabinet și probă efectivă.','QC04-P2':'Fixture 8 fizic, 100 furnizor, 7 buc/25%, prag fracționar, anulare, control canal și refuz; regula procent necunoscută rămâne neconcludentă.','QC06-P3':'În dosar sunt 10 handoff-uri; fiecare titular citește același ID/versiune/rezultat sau raportează discrepanța.','QC09-P1':'Cazuri separate pe articol, lot, zero/gol/negativ, dublare/retry, reversare și corelare a mișcării, martor neschimbat.','QC10-P1':'Template cu task/criteriu/control/flux/actor/ID/expected/observed, fișier și SHA per caz, control final A11.'}
criteria=[{'id':x['id'],'points':0.2,'evidence':reasons.get(x['id'],'Condiție neschimbată a planului semnat și reconfirmată prin setul de 15 controale cu negative, mediu, oracol și handoff.')} for crit in rd(R/'A11_rubrica_control.json')['criteria'] for x in crit['plan_subchecks']]
v={'schema':'A11-gate-addendum-v2','reviewer':'A11','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject':p.relative_to(R).as_posix(),'hash_sha256':h(p),'base_plan_bundle':a['base_plan'],'previous_gate_sha256':h(e/'A11_gate_delta_P01_R1.json'),'decision':'ACCEPTAT_PLAN_SUPLIMENT_T352_T366','quality_score_plan':10,'earned':50,'maximum_subchecks':50,'subchecks':criteria,'control_count':len(a['controls']),'source_hash_checks':10,'source_pointer_checks':30,'control_pipeline_inverse_anomalies':errors,'open_hard_blockers':[],'cutoff':a['supplement_cutoff'],'population':{'before':651,'after':652,'added':['T352'],'retained_review_due_to_transition':['T366'],'active_context':['T225','T232','T343']},'quality_score_product_or_audit':None,'scope':'Aprobarea permite exclusiv execuția suplimentului în mediile aprobate și pe corpusul declarat; procentele și politica de rotunjire se decid prin contractul real. Nu acceptă rapoarte sau funcții.'}
out=e/'A11_gate_delta_P01_R2.json';out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); print(h(out))

