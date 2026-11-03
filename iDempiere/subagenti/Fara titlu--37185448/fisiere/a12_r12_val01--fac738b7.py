import collections,copy,gzip,hashlib,html,json,pathlib,sys
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';P=E/'R12_plan_delta';R=E/'R12_fisiere'
OUT=R/'A12/Val_01';H='df85d33c1648ce2b2df130a60a05ef696e2e5480';OLD='2fe90ed3f128c33dff7cf9f8674e664a70679390'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
CACHE={}
def ref(p,pointer=None):
 if p not in CACHE:
  b=p.read_bytes();CACHE[p]={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 d=dict(CACHE[p])
 if pointer is not None:d['pointer']=pointer
 return d
def save(p,d):
 assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def gzrows(p,rows):
 assert not p.exists();b=('\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in rows)+'\n').encode();p.write_bytes(gzip.compress(b,mtime=0));return dict(ref(p),raw_sha256=sha(b))
def resolve(d,pointer):
 for token in pointer.strip('/').split('/') if pointer else []:
  token=token.replace('~1','/').replace('~0','~');d=d[int(token)] if isinstance(d,list) else d[token]
 return d
assert len(sys.argv)==3,'Usage: builder A11_verdict_absolute A11_seal_absolute'
vp=pathlib.Path(sys.argv[1]);sp=pathlib.Path(sys.argv[2]);v=load(vp);seal=load(sp)
assert H in json.dumps(v,ensure_ascii=False),'Missing candidate in independent receipt'
assert v['decision']=='ADMIS_CA_DOVEZI_COMPONENTĂ_LIMITATE_CU_CONSTĂTĂRI_DESCHISE'
assert 'c4fdf5311d70f9dcbdbb37c24db802021065b34162accc98525dd40ad4514c4d' in json.dumps(v,ensure_ascii=False),'Independent receipt must bind this manifest'
assert sha(vp.read_bytes()) in json.dumps(seal),'Independent seal must bind exact verdict'
mp=R/'A08_T240/Lot_01_final_v1/MANIFEST_A08_T240_R12_lot01_v1.json';rp=mp.parent/'Raport_A08_T240_R12_lot01_v1.json'
assert sha(mp.read_bytes())=='c4fdf5311d70f9dcbdbb37c24db802021065b34162accc98525dd40ad4514c4d'
assert sha(rp.read_bytes())=='b787ebbacdbed52aa5dfb3ac8b61d4e2ad331d043b489306b110986afbe5aa69'
m=load(mp);report=load(rp);assert m['head']==report['head']==H
verified_refs=[]
for x in m['files']+m['external_independent_witnesses']:
 p=B/x['path'];assert sha(p.read_bytes())==x['sha256'],str(p);verified_refs.append(ref(p))
assert len(report['sources'])==2 and report['native_UI_or_ERP_executed'] is False
assert report['whole_task_verdict'] is None and report['whole_file_verdict'] is None
with gzip.open(P/'Dispatch_tehnic_integral_R12.jsonl.gz','rt',encoding='utf-8') as f:dispatch={r['path']:r for r in map(json.loads,f)}
with gzip.open(E/'R11_fisiere/A12/Val_04/Registru_6709_val_04.jsonl.gz','rt',encoding='utf-8') as f:historical={r['path']:r for r in map(json.loads,f)}
source_by={s['path']:s for s in report['sources']}
for s in report['sources']:
 p=B/s['local_evidence']['path'];b=p.read_bytes();assert sha(b)==s['sha256']==s['local_evidence']['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['git_oid']==dispatch[s['path']]['git_object'];assert s['path'] not in historical
baseline=report['counts'];assert baseline['original_cases']==baseline['original_cases_passed']==46
assert baseline['mutants_declared']==baseline['mutants_exercised_in_batches']==33
assert {r['index'] for r in report['mutants']}==set(range(33))
assert all(r['status']=='UCIS' and len(r['case_results'])==46 and r['witnesses'] for r in report['mutants'])
assert len(report['cases_A08'])==20 and len({r['case_id'] for r in report['cases_A08']})==20
assert report['execution']['timeout_retained'] is True
assert not OUT.exists(),'Immutable wave directory already exists'
OUT.mkdir(parents=True)
rows=[]
hist_ref=ref(E/'R11_fisiere/A12/Val_04/Registru_6709_val_04.jsonl.gz')
for path,d in sorted(dispatch.items()):
 old=historical.get(path);is_new=path in source_by
 if old:assert (old['git_oid'],old['git_mode'])==(d['git_object'],d['mode'])
 row={'id':d['id'],'path':path,'git_oid':d['git_object'],'git_mode':d['mode'],'candidate':H,'owner':d['owner'],'planned_peer':d['peer'],'control':d['control'],'pipeline_candidates':d.get('pipeline_candidates',[]),'task_candidates':d.get('task_candidates',[]),'scope':'CURRENT_R12','axis':{'read':'OBSERVED_IN_SIGNED_COMPONENT_PACKAGE' if is_new else 'NO_NEW_CREDIT_IN_THIS_WAVE','component_exercised':'OBSERVED_ONLY_AT_LINKED_SCOPE' if is_new else 'UNVERIFIED_R12','native_UI':'UNVERIFIED_R12','ERP_DB':'UNVERIFIED_R12','installed_binding':'UNVERIFIED_R12','whole_file_acceptance':None},'current_evidence':[dict(ref(rp,'/sources/'+str(report['sources'].index(source_by[path]))),scope='Original CLI baseline, original functions in bounded mutant batches and nominal independent synthetic cases; no native UI/ERP',independent_reception=ref(vp))] if is_new else [],'R11_reference_only':{'candidate':OLD,'source':dict(hist_ref,logical_path=path),'same_blob_mode':True,'axes':old['axis'],'credit_transferred':False} if old else None,'peer_receipts':{'planned':d['peer'],'A09_receipt_asserted':False,'independent_A11':ref(vp) if is_new else None},'file_verdict':None}
 rows.append(row)
reg=gzrows(OUT/'Registru_6728_R12_Val01.jsonl.gz',rows)
events=[]
for s in report['sources']:
 cid='R12-I18' if s['path'].endswith('test_clasa_verifica_proba.py') else 'R12-I19'
 ev={'event_id':'R12V01-'+cid,'path':s['path'],'git_oid':s['git_oid'],'sha256':s['sha256'],'task_alias':'T240','task_canonical':'P01.C14.T0001','task_state':'implementare','within_historic_completed_cohort':False,'audit_control':cid,'actor':report['shared_profile']['actor'],'native_method':report['shared_profile']['native_method'],'fixture_observed':report['shared_profile']['context'],'positive_and_counterexample':ref(rp,'/shared_profile/counterexample_policy'),'persistent_effect':report['shared_profile']['persistent_effect'],'scope':report['shared_profile']['execution_scope'],'result':'COMPONENT_MEASUREMENTS_WITH_FINDINGS_AND_LIMITS','whole_task_or_file_acceptance':None,'evidence':ref(rp,'/sources/'+str(report['sources'].index(s))),'independent_reception':ref(vp),'limits':report['limitations']}
 events.append(ev)
save(OUT/'Evenimente_2_instrumente.json',{'head':H,'rows':events,'counting':'Two distinct sources, not two completed functions or native screens.'})
findings=[]
for i,f in enumerate(report['findings']):
 row=copy.deepcopy(f);row.update(source=ref(rp,'/findings/'+str(i)),independent_reception=ref(vp),count_once_by=f['id'],canonical_task='P01.C14.T0001',task_state='implementare',corrective_code_changes_in_this_audit=False)
 matches=[x for x in v['findings_disposition'] if x['finding'].split(' / ')[0]==f['id']]
 assert len(matches)==1
 row['independent_disposition']=matches[0]
 findings.append(row)
save(OUT/'Constatari_componente_T240.json',{'head':H,'rows':findings,'no_automatic_promotion':'Kinds and severity proposals are preserved from the producer. Independent verdict is separate and authoritative for acceptance; no all-findings-equal or whole-task score.'})
reconciliation={'head':H,'producer':ref(rp),'independent_reception':ref(vp),'counts':baseline,'scope':report['shared_profile'],'attempts':report['execution'],'environment_correction':report['environment_correction'],'performance':report['performance'],'no_total_unique_tests_inferred':True,'fixture_count_erratum':{'plan_and_source_docstring':'A12 initial I18 plan/source docstring describe12 screens','actual_executed':'13 distinct RO screen identities plus10 EN TEXTE and1 EN Perioade=24 rows,46 cases','source':ref(rp,'/shared_profile/context'),'meaning':'Different descriptive count; preserve original plan and executed fixture separately. No extra native screen credit.','test_count_is_not_screen_count':True},'case_sets':{'A08_cases':{'count':20,'source':ref(rp,'/cases_A08')},'A08_original_CLI_UTF8':{'count':1,'source':ref(rp,'/findings/3')},'A11_independent_CLI':{'count':19,'sources':report['independent_witnesses']},'mutants':{'count':33,'batches':7,'case_evaluations':1518,'source':ref(rp,'/mutants'),'not1518_unique_tests':True}},'grade':None}
save(OUT/'Reconciliere_cazuri_mutanti_si_limite.json',reconciliation)
matrix={'head':H,'historic_cohort':{'tasks':652,'criteria':2619,'R11_matrix_reference_only':ref(E/'R11_fisiere/A12/Val_04/Matrice_criterii_task_probe_val04.json'),'R11_receipt':ref(E/'R11_fisiere/A11/Verdict_A11_R11_val04_v1.json'),'current_R12_criterion_credit_from_this_wave':0},'active_tasks_outside_cohort':[{'task_alias':'T240','canonical':'P01.C14.T0001','state':'implementare','source':ref(E/'delta/2026-11-02T23-15-23-444Z/00_STATUS_TASKURI.json','/831'),'events':['R12V01-R12-I18','R12V01-R12-I19'],'audit_controls':['R12-I18','R12-I19'],'component_requirement':'Existing validator rules R1–R11 and declared C-12 context; no complete native help criterion accepted','source_requirements':report['sources'],'findings':[r['id'] for r in findings],'whole_task_verdict':None}],'pending_T343':{'supplement':ref(P/'A12/Supliment_populatie_2315.json'),'independent_reception':ref(P/'Receptie_A11_supliment_T343_2315_v1.json'),'unchanged_oracle':'CO|CO|CO until nominal amendment received','new_criterion_ids_created':0},'current_semantic_links':events,'all17_native_contracts_open':True}
save(OUT/'Matrice_taskuri_criterii_R12_Val01.json',matrix)
zone_rows=[]
for zone in [f'A{i:02}' for i in range(1,11)]:
 owned=[r for r in rows if r['owner']==zone]
 zone_rows.append({'owner':zone,'assigned_files':len(owned),'files_component_exercised_R12':sum(r['axis']['component_exercised']!='UNVERIFIED_R12' for r in owned),'native_files_exercised_R12':0,'new_current_evidence':'A08 T240 component' if zone=='A08' else 'No new execution credited in this checkpoint','historical_R11_exercised_reference_only':sum(r['R11_reference_only'] is not None and r['R11_reference_only']['axes']['exercised']!='UNVERIFIED' for r in owned),'whole_zone_verdict':None})
save(OUT/'Situatie_10_zone_R12_Val01.json',{'head':H,'rows':zone_rows,'native_contracts_open':17})
counts={'technical_files':6728,'historic_files_unchanged':6709,'new_tools':19,'current_R12_source_files_component_exercised':2,'remaining_files_without_R12_component_execution_in_this_wave':6726,'historical_R11_exercised_reference_only':116,'historical_116_transferred_credit':0,'native_UI_or_ERP_files_exercised':0,'historic_tasks':652,'historic_criteria':2619,'historic_criteria_newly_credited_by_this_wave':0,'active_task_T240_closed':False,'full_file_verdicts':0,'full_task_verdicts':0,'native_contracts_still_open':17}
counts['new_instruments_still_unexercised']=17
assert sum(r['axis']['component_exercised']!='UNVERIFIED_R12' for r in rows)==2
assert sum(r['R11_reference_only'] is not None and r['R11_reference_only']['axes']['exercised']!='UNVERIFIED' for r in rows)==116
srcs=''.join('<tr><td>'+html.escape(e['audit_control'])+'</td><td>'+html.escape(e['path'])+'</td><td>Componentă sintetică; UI/ERP neexecutat</td></tr>' for e in events)
frows=''.join('<tr><td>'+html.escape(f['id'])+'</td><td>'+html.escape(f['subject'])+'</td><td>'+html.escape(f['kind'])+'</td></tr>' for f in findings)
page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R12 · Val 01 · T240</title><style>body{font:16px/1.5 system-ui;max-width:1100px;margin:32px auto;padding:0 16px;color:#172534;background:#f5f7fa}h1,h2{line-height:1.2}p,td,code,a{overflow-wrap:anywhere}.table{overflow-x:auto;background:white;padding:12px;border-radius:8px}table{border-collapse:collapse;width:100%}td,th{text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid #ddd}code{font-size:14px}.note{border-left:4px solid #246d86;padding:12px;background:#e7f2f5}</style><h1>R12 · Val 01: validatorul probelor de ajutor</h1>'''
page+='<p>Revizie fixată: <code>'+H+'</code>. Două instrumente existente au fost exercitate la nivel de componentă. T240 — <strong>P01.C14.T0001</strong> — rămâne în implementare.</p><p class="note">Cele 116 fișiere exercitate în R11 sunt istoric separat. Nu au primit automat credit R12. Nu au fost executate interfața nativă, baza ERP sau cele 17 contracte complete.</p>'
page+='<h2>Execuții și limite</h2><p>46/46 cazuri originale; 33/33 mutanți detectați în 7 loturi disjuncte. Încercarea integrală s-a oprit la 60 secunde și rămâne timeout, fără credit de rulare integrală. Cele 1.518 evaluări ale mutanților reutilizează aceleași 46 cazuri.</p><p>20 cazuri proprii A08, un caz CLI UTF8 și 19 martori A11 se păstrează separat. Fixture-ul executat are 13 identități RO și 24 rânduri; descrierea inițială de 12 ecrane este consemnată ca diferență documentară.</p><div class="table"><table><tr><th>Control</th><th>Fișier</th><th>Domeniu</th></tr>'+srcs+'</table></div>'
page+='<h2>Constatări nominale</h2><div class="table"><table><tr><th>ID</th><th>Subiect</th><th>Încadrare</th></tr>'+frows+'</table></div><p>Recepția independentă și limitele fiecărui caz sunt legate în raportul JSON. Nu există notă de conformitate globală sau închidere de task.</p><p><a href="Handoff_R12_Val01.json">Handoff și surse</a> · <a href="Matrice_taskuri_criterii_R12_Val01.json">Matrice nominală</a> · <a href="Reconciliere_cazuri_mutanti_si_limite.json">Numărători și limite</a></p></html>'
(OUT/'index.html').write_text(page,encoding='utf-8',newline='\n')
handoff={'schema':'eva.audit.r12.a12.wave/1','utc':datetime.now(timezone.utc).isoformat(),'head':H,'current_master_after_latest_capture':'Not asserted; frozen candidate only','latest_preflight':ref(P/'A12/Supliment_populatie_2315.json'),'approved_plan':ref(P/'Plan_delta_R12_v2.json'),'gate':ref(P/'A11_verdict_plan_delta_R12_v2.json'),'authoritative_inventory':ref(P/'Manifest_A12_receptie_R12_v2.json'),'previous_received_wave':ref(E/'R11_fisiere/A12/Val_04/MANIFEST_val_04.json'),'producer_manifest':ref(mp),'producer_report':ref(rp),'producer_QA':ref(mp.parent/'QA_lot01_v1.json'),'independent_verdict':ref(vp),'independent_seal':ref(sp),'counts':counts,'register':reg,'matrix':ref(OUT/'Matrice_taskuri_criterii_R12_Val01.json'),'events':ref(OUT/'Evenimente_2_instrumente.json'),'findings':ref(OUT/'Constatari_componente_T240.json'),'cases':ref(OUT/'Reconciliere_cazuri_mutanti_si_limite.json'),'zones':ref(OUT/'Situatie_10_zone_R12_Val01.json'),'scores':{'plan_received_separately':10,'execution_quality':None,'product':None},'resources':{'A12_new_product_services':0,'A12_new_product_tests':0,'producer_cleanup':report['cleanup'],'A12_local_preparation_file':'D:/CodexWork/a12_r12_val01_base.json; inert metadata, not an executed product artifact'},'limitations':report['limitations']+['Planned peer A09 remains distinct from the actual independent A11 receipt; no A09 signature is invented.','Historic652 task dossiers and2619criteria preserved by sealed references, no unsupported new current-HEAD credit.'],'A11_wave_reception_pending':True,'source_manifest_hashes_reverified':len(verified_refs)}
save(OUT/'Handoff_R12_Val01.json',handoff)
# Resolve every emitted local artifact reference, hash, and RFC6901 pointer; JSONL logical keys are explicit.
checks={};errors=[]
def scan(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x and str(x['path']).startswith('executie/'):
   p=B/x['path'];key=(str(p),x['sha256'],x.get('pointer'))
   if key not in checks:
    try:
     assert sha(p.read_bytes())==x['sha256']
     if x.get('pointer') is not None:resolve(load(p),x['pointer'])
     checks[key]=True
    except Exception as e:errors.append({'ref':x,'error':str(e)})
  for y in x.values():scan(y)
 elif isinstance(x,list):
  for y in x:scan(y)
for p in OUT.glob('*.json'):scan(load(p))
for r in rows:scan(r)
scan(v);scan(seal);scan(report)
assert not errors,errors[:2]
qa={'utc':datetime.now(timezone.utc).isoformat(),'handoff':ref(OUT/'Handoff_R12_Val01.json'),'register':reg,'counts':counts,'all_source_sha_and_git_blob_verified':True,'all89_producer_manifest_artifacts_stable':len(m['files'])==89,'producer_and_independent_receipts_kept_separate':True,'mutant_indices_unique_complete':True,'no_original_full_program_success_inferred':True,'no_historical_credit_transferred':True,'local_references_and_pointers_verified':len(checks),'issues':errors,'quality_score':None}
save(OUT/'QA_R12_Val01.json',qa)
(OUT/'build_val01.py').write_bytes(pathlib.Path(__file__).read_bytes())
manifest={'utc':datetime.now(timezone.utc).isoformat(),'head':H,'status':'A12_CHECKPOINT_FOR_INDEPENDENT_RECEPTION','files':[ref(p) for p in sorted(OUT.iterdir()) if p.is_file()],'inputs':[ref(mp),ref(rp),ref(vp),ref(sp),ref(P/'Manifest_A12_receptie_R12_v2.json'),ref(P/'Plan_delta_R12_v2.json'),ref(P/'A11_verdict_plan_delta_R12_v2.json')],'no_self_reference':True}
save(OUT/'MANIFEST_R12_Val01.json',manifest)
for x in manifest['files']+manifest['inputs']:assert sha((B/x['path']).read_bytes())==x['sha256']
print(json.dumps({'manifest':ref(OUT/'MANIFEST_R12_Val01.json'),'handoff':ref(OUT/'Handoff_R12_Val01.json'),'qa':ref(OUT/'QA_R12_Val01.json'),'counts':counts},ensure_ascii=False,indent=2))
