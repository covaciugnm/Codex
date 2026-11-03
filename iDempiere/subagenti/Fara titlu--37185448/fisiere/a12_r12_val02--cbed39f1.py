import copy,collections,gzip,hashlib,html,json,pathlib,sys
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';R=E/'R12_fisiere';P=E/'R12_plan_delta';O=R/'A12/Val_02';PRE=R/'A12/Val_01';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
CACHE={}
def ref(p,pointer=None):
 if p not in CACHE:
  b=p.read_bytes();CACHE[p]={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 d=dict(CACHE[p])
 if pointer is not None:d['pointer']=pointer
 return d
def save(p,x):
 assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def rows(p):
 with gzip.open(p,'rt',encoding='utf-8') as f:return [json.loads(x) for x in f]
def write_rows(p,x):
 b=('\n'.join(json.dumps(y,ensure_ascii=False,separators=(',',':')) for y in x)+'\n').encode();assert not p.exists();p.write_bytes(gzip.compress(b,mtime=0));return dict(ref(p),raw_sha256=sha(b))
def resolve(x,p):
 for t in p.lstrip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');x=x[int(t)] if isinstance(x,list) else x[t]
 return x
def check_manifest(p,expected=None,relative=True):
 if expected:assert sha(p.read_bytes())==expected,str(p)
 m=load(p);verified=[]
 entries=m['files'] if isinstance(m.get('files'),list) else m['entries']
 for v in entries:
  q=(p.parent if relative else B)/v['path'];assert q.is_file(),str(q);assert sha(q.read_bytes())==v['sha256'],str(q);verified.append(ref(q))
 return m,verified
assert len(sys.argv)==2,'Supply sealed receipt config JSON, no test execution is performed.'
config=load(pathlib.Path(sys.argv[1]));assert config['head']==H
assert not (O/'Handoff_R12_Val02.json').exists(),'Published checkpoint is immutable'
before_manifest,before_verified=check_manifest(PRE/'MANIFEST_R12_Val01.json','2d0e8529b61698031a132cf4bf8e72f17b8a9fbb03df2b0000e885dde38efe93',False)
for v in before_manifest['inputs']:assert sha((B/v['path']).read_bytes())==v['sha256']
prior_receipt=R/'A11/Val01/Verdict_A11_R12_Val01_v1.json';assert sha(prior_receipt.read_bytes())=='b702325e3259a69af59f7f51cad36026bd7f1649019b37881c917c1356a1df6e'
prior=rows(PRE/'Registru_6728_R12_Val01.jsonl.gz');dispatch={x['path']:x for x in prior};assert len(prior)==len(dispatch)==6728
lots={
 'A08':{'directory':R/'A08_Helper_rapoarte_lot02','manifest':'MANIFEST_A08_lot02.json','sha':'3dc9c882d755754b6ab7982d32dd8fb5f7e965d0fec99e10f242e82668012141','report':'Raport_A08.json'},
 'A09':{'directory':R/'A09_Helper_corpus_lot02','manifest':'MANIFEST_SHA256.json','sha':'23f5fa497a8f07b3b7654ccdd8de3227a6657a149cf94ce3aff3172d17de5018','report':'rezumat_predare.json'},
 'Masini':{'directory':R/'A09_Date_Masini_lot02','manifest':'MANIFEST_SHA256.json','sha':'ff071b46603712874805c53a024d5d4f8fccf7fedd5fb988dfb338d17f5059db','report':'Fisa_Masini_date.json'}}
proof_inputs=[];verified_artifacts=[];independent_seals_verified={}
for key,l in lots.items():
 mp=l['directory']/l['manifest'];m,vr=check_manifest(mp,l['sha']);assert m['head']==H;l['verified']=len(vr);verified_artifacts+=vr;l['report_path']=l['directory']/l['report'];l['report_data']=load(l['report_path']);assert l['report_data']['head']==H
 receipt=config['receipts'][key];vp=B/receipt['path'];sp=B/receipt['seal_path'];assert sha(vp.read_bytes())==receipt['sha256'];assert sha(sp.read_bytes())==receipt['seal_sha256'];v=load(vp);assert receipt['sha256'] in json.dumps(load(sp),ensure_ascii=False);assert l['sha'] in json.dumps(v,ensure_ascii=False),'Receipt must identify producer manifest';l['receipt_path']=vp;l['receipt']=v;l['seal_path']=sp
 if sp not in independent_seals_verified:
  _,ir=check_manifest(sp,receipt['seal_sha256']);independent_seals_verified[sp]=len(ir);verified_artifacts+=ir
 proof_inputs.append({'lot':key,'manifest':ref(mp),'report':ref(l['report_path']),'independent_verdict':ref(vp),'independent_seal':ref(sp),'artifact_count_rehashed':len(vr),'receipt_scope':receipt['scope'],'required_limits':receipt['limits']})
sources=[];events=[];findings=[];dependencies=[];case_ledger=[]
def verify_source(s,local):
 d=dispatch[s['path']];raw=local.read_bytes();assert sha(raw)==s['sha256'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==s['git_object']==d['git_oid'];assert s.get('mode',d['git_mode'])==d['git_mode'];return d,ref(local)
def add_event(s,local,lot,details,pointer,event_id):
 d,lref=verify_source(s,local);assert d['axis']['component_exercised']=='UNVERIFIED_R12';assert s['path'] not in [x['path'] for x in events];sources.append({'source':s,'local':lref,'dispatch_id':d['id'],'lot':lot});l=lots[lot]
 matches=[(i,r) for i,r in enumerate(l['receipt']['file_receptions']) if r['file']['path']==s['path']]
 assert len(matches)==1;ri,rd=matches[0];assert rd['file']['git_object']==s['git_object'] and rd['file']['sha256']==s['sha256'];assert rd['whole_file_accepted'] is False and rd['product_or_task_closed'] is False
 ev={'event_id':event_id,'path':s['path'],'git_oid':s['git_object'],'sha256':s['sha256'],'owner':d['owner'],'planned_peer':d['planned_peer'],'control':d['control'],'pipeline_candidates':d['pipeline_candidates'],'task_candidates_preserved':d['task_candidates'],'source':lref,'producer':ref(l['report_path'],pointer),'independent_receipt':ref(l['receipt_path'],'/file_receptions/'+str(ri)),'independent_disposition':rd['disposition'],'independent_scope':rd['scope'],'independent_limit':rd['limit'],'scope':'PARTIAL_COMPONENT_ONLY','whole_file_acceptance':None,'whole_task_acceptance':None,**details};events.append(ev)
 return ev
a08=lots['A08']['report_data'];assert a08['summary']['case_count']==54 and a08['summary']['top_level_cli_invocations']==58
assert len(a08['dossiers'])==5
a08cases=load(lots['A08']['directory']/'Case_index.json');a08effects=load(lots['A08']['directory']/'Effects_before_after.json')
assert len(a08cases)==54 and len({x['id'] for x in a08cases})==54
assert sum(len(x['steps']) for x in a08cases)==58
for i,c in enumerate(a08cases):
 ef=next(j for j,x in enumerate(a08effects) if x['case']==c['id']);rp=lots['A08']['directory']/c['result'];assert sha(rp.read_bytes())==c['result_sha256']
 case_ledger.append({'id':'A08:'+c['id'],'producer_case_id':c['id'],'lot':'A08','expected':c['expected'],'observed':c['observed'],'steps':c['steps'],'raw_result':ref(rp),'oracle_source':ref(lots['A08']['directory']/'Case_index.json','/'+str(i)),'effect_source':ref(lots['A08']['directory']/'Effects_before_after.json','/'+str(ef)),'not_whole_product_PASS':True})
for i,d in enumerate(a08['dossiers']):
 s=d['source'];local=lots['A08']['directory']/'Sources'/s['path']
 add_event(s,local,'A08',{'audit_control':d['control'],'executor':'A08','task_alias':'T240','canonical_task':'P01.C14.T0001','task_state':'implementare','requirement':d['requirements'],'actor':d['actor'],'entry_point':d['normal_path'],'native_method':d['native_idempiere'],'frontend_UX':d['frontend_UX'],'backend':d['backend'],'database':d['db_tables'],'positive_negative_cases':d['cases'],'expected_observed_source':ref(lots['A08']['directory']/'Case_index.json'),'persistent_effect':d['effects'],'limits':d['limits'],'source_dossier':ref(lots['A08']['report_path'],'/dossiers/'+str(i))},'/dossiers/'+str(i),'R12V02-'+d['control'])
for i,f in enumerate(a08['findings']):findings.append({'id':f['id'],'producer_claim':f,'producer':ref(lots['A08']['report_path'],'/findings/'+str(i)),'independent_receipt':ref(lots['A08']['receipt_path']),'disposition':config['receipts']['A08'].get('finding_dispositions',{}).get(f['id'],'Retain original claim qualified by independent receipt; no whole-product acceptance'),'count_once_by':f['id']})
a09cases=[]
for name in ['results.json','results_supplement01.json']:
 doc=load(lots['A09']['directory']/name)
 for i,c in enumerate(doc['results']):
  a09cases.append(c)
  case_ledger.append({'id':'A09:'+c['case'],'producer_case_id':c['case'],'lot':'A09','instrument':c['instrument'],'expected':{'exitcode':c['expected_exitcode'],'assertions':c['checks'],'interpretation':'These named assertions are producer observations against the declared finite fixture; matched does not mean whole-product conformant.'},'observed':{'exitcode':c['exitcode'],'stdout':c['stdout'],'stderr':c['stderr'],'oracle_matches':c['oracle_matches']},'input_effect':{'changed_inputs':c['changed_inputs'],'created_files':c['created_files']},'raw_result':ref(lots['A09']['directory']/name,'/results/'+str(i)),'not_whole_product_PASS':True})
assert len(a09cases)==67 and len({x['case'] for x in a09cases})==67
for p in sorted((lots['A09']['directory']/'fise').glob('*.json')):
 d=load(p);s=d['source'];local=lots['A09']['directory']/'sources'/s['path']
 ev=add_event(s,local,'A09',{'audit_control':d['instrument'],'executor':d['executor'],'task_alias':'T240','canonical_task':'P01.C14.T0001','task_state':'implementare','requirement':d['requirement'],'actor':d['actor'],'entry_point':d['normal_entry'],'native_method':d['native_method_or_NA'],'pipeline_description':d['pipeline'],'consumers':d['consumers'],'positive':d['positive_cases'],'counterexamples':d['counterexample_cases'],'expected_observed':d['observed_cases'],'persistent_effect':d['stages']['persistent_effect'],'limits':[d['limit'],'No complete-file, task, native UI/ERP or historical criterion acceptance'],'source_dossier':ref(p)},None,'R12V02-'+d['instrument']);ev['producer']=ref(p)
for i,f in enumerate(load(lots['A09']['directory']/'constatari.json')):findings.append({'id':'A09.R12.HC.'+f['id'],'original_id':f['id'],'producer_claim':f,'producer':ref(lots['A09']['directory']/'constatari.json','/'+str(i)),'independent_receipt':ref(lots['A09']['receipt_path']),'disposition':config['receipts']['A09'].get('finding_dispositions',{}).get(f['id'],'Retain original classification and independent limitations; no whole-product acceptance'),'count_once_by':'A09.R12.HC.'+f['id']})
md=lots['Masini']['report_data'];ms={'path':md['file'],'git_object':md['oid'],'sha256':md['sha256']};assert md['canonical_task'] is None and not dispatch[md['file']]['task_candidates']
mev=add_event(ms,lots['Masini']['directory']/'WSagaMasiniForm.java','Masini',{'audit_control':None,'executor':md['executor'],'task_alias':None,'canonical_task':None,'task_state':None,'task_mapping':'SHARED_NO_TASK_ASSIGNED','T240_link_kind':'Observation provenance only, no canonical task attribution','requirement':md['requirement'],'actor':md['actor'],'entry_point':'parseData private method by exact original source/JAR reflection','native_method':md['native_method'],'positive':md['positive'],'counterexamples':md['counterexample'],'expected_observed':ref(lots['Masini']['directory']/'Cases_normalized.json'),'normal_path_static_only':md['normal_path'],'persistent_effect':md['persistent_effect'],'installed_binding':md['installed_binding'],'limits':md['limits'],'source_dossier':ref(lots['Masini']['report_path'])},None,'R12V02-MASINI-DATE-01')
case=load(lots['Masini']['directory']/'Cases_normalized.json');assert len(case)==2 and all(len(x['cases'])==12 and x['valid_rejected']==5 and x['invalid_or_empty_as_expected']==7 for x in case)
for i,c in enumerate(case[0]['cases']):
 other=case[1]['cases'][i];assert (c['case'],c['input'],c['expected'])==(other['case'],other['input'],other['expected'])
 case_ledger.append({'id':'Masini:'+str(c['case']),'producer_case_id':c['case'],'lot':'Masini','input_rendered':c['input'],'input_native_kind':'JAVA_NULL' if i==11 else 'JAVA_STRING','expected':c['expected'],'observed':[{'execution':x['execution'],'actual':x['cases'][i]['actual'],'matches_expected':x['cases'][i]['product_matches_expected'],'source':ref(lots['Masini']['directory']/'Cases_normalized.json',f'/{j}/cases/{i}')} for j,x in enumerate(case)],'persistent_effect':'NONE; parser only, no PO save or SQL','not_whole_product_PASS':True})
peer_mp=R/'A01_Peer_Masini_lot02/MANIFEST_SHA256.json';peer_m,peer_refs=check_manifest(peer_mp,'ebe721e9d4377d2e2de60487f7c30c114796089bf10ac29f83c07411f3089a50')
peer_p=peer_mp.parent/'Peer_A01_Masini_lot02.json';assert sha(peer_p.read_bytes())=='d5f7084b086b050e1c8fff6b9f5b7066f8662f21d50accfd5b5f616c557a0ff4'
scopep=lots['Masini']['directory']/'Scope_restant_Masini_v1.json';assert sha(scopep.read_bytes())=='38a12764a2adcc9e37c59cc7a1e6fcde0516f1b28cf32da99dc40dd6c88bbd13'
mev['peer_A01_semantic_only']={'manifest':ref(peer_mp),'report':ref(peer_p),'new_executions':0,'cases_clarification':'5 valid dates rejected;4 invalid calendar/format inputs and3 empty/space/Java null. Input null is not the literal string null.','compiled_class_vs_JAR':'Recompiled-source class SHA differs from Git-JAR class; finite results agree. Only Git-JAR versus extracted installed class is byte-equal.'}
mev['remaining_axes_not_executed']=ref(scopep)
verified_artifacts+=peer_refs
findings.append({'id':md['finding_id'],'producer_claim':{'requirement':md['requirement'],'observed':md['result'],'priority_proposal':md['priority'],'normal_path_static_only':md['normal_path'],'recommendation':md['recommendation'],'closure_checklist':md['closure_checklist']},'producer':ref(lots['Masini']['report_path']),'independent_receipt':ref(lots['Masini']['receipt_path']),'disposition':config['receipts']['Masini'].get('finding_dispositions',{}),'count_once_by':md['finding_id'],'canonical_task':None})
for f in findings:
 if f.get('original_id')=='HC11':
  f['effective_classification']='OBSERVATION_ON_AMBIGUOUS_INPUT_VIOLATING_NATIVE_SINGLE_CHAPTER_INVARIANT';f['effective_priority']=None;f['producer_P2_and_defect_label_superseded_by_A11']=True
  f['effective_recommendation']='Detect and refuse ambiguous input while preserving one chapter per screen; do not multiply chapters or assert a P2 defect for a valid native input.'
assert len(events)==11 and len(set(x['path'] for x in events))==11
assert len(sources)==11 and len(findings)==22
assert len(case_ledger)==133 and len({x['id'] for x in case_ledger})==133
save(O/'Cazuri_nominale_133.json',{'head':H,'rows':case_ledger,'counts_by_lot':{'A08':54,'A09':67,'Masini_unique_inputs':12},'scope':'133 case identities are a traceability index, not133 successful product tests; 12 Mașini inputs each have two observations.'})
for ev in events:
 keys=ev.get('positive_negative_cases') or (ev.get('positive',[])+ev.get('counterexamples',[]) if ev['event_id']!='R12V02-MASINI-DATE-01' else [])
 lot='Masini' if ev['event_id']=='R12V02-MASINI-DATE-01' else ('A08' if ev['executor']=='A08' else 'A09')
 ev['nominal_cases']=[ref(O/'Cazuri_nominale_133.json','/rows/'+str(i)) for i,c in enumerate(case_ledger) if c['lot']==lot and (lot=='Masini' or c['producer_case_id'] in keys)]
 assert ev['nominal_cases'],ev['event_id']
 if lot=='A08':
  peerp=lots['A08']['directory']/'Peer_reception_scope.json';pd=load(peerp)
  ev['technical_peer_limited']={'reviewer':'A09','scope_source':ref(peerp),'cases_for_this_event':sorted(set(keys)&set(pd['scope'])),'source_identity_review_only_beyond_these_cases':True,'not_full_54_case_receipt':True}
 elif lot=='A09':
  peerp=lots['A08']['directory']/'Peer_A08_pentru_A09.json';pd=load(peerp)
  ev['technical_peer_limited']={'reviewer':'A08','source':ref(peerp),'cases_for_this_event':sorted(set(keys)&{x['id'] for x in pd['cases']}),'new_product_runs':0,'not_full_67_case_receipt':True}
dependencies=[{'origin':'A08','source':ref(lots['A08']['directory']/'Dependencies_exercised.json'),'scope':'Functions invoked as dependencies; fisa/manual_cap share direct events; no extra file count.'},{'origin':'A09','source':ref(lots['A09']['directory']/'Dependency_sources.json'),'scope':'Existing inventory/verifica_help functions only, no extra file execution claim or main coverage.'},{'origin':'Masini','source':ref(lots['Masini']['directory']/'Caller_source.json'),'scope':'WSagaCrudForm caller static read only; saveEx/commit not executed in Mașini test.'}]
old_events=load(PRE/'Evenimente_2_instrumente.json')['rows'];assert len(old_events)==2
all_events=old_events+events;assert len({x['path'] for x in all_events})==13 and len({x['event_id'] for x in all_events})==13
assert {x['path'] for x in old_events}.isdisjoint(x['path'] for x in events)
save(O/'Evenimente_11_fisiere.json',{'head':H,'rows':events,'source_identities':sources,'dependencies_without_automatic_credit':dependencies,'no_whole_file_task_or_contract_acceptance':True})
save(O/'Constatari_lot02.json',{'head':H,'rows':findings,'previous_findings_reference_only':ref(PRE/'Constatari_componente_T240.json'),'counting':'22 nominal new finding/limit records; not22 confirmed product defects; individual disposition from A11 is authoritative. Do not count one finding again for every affected file.','semantic_overlap':'H03/H07 cover distinct absent/substr reference behaviors; HC04 and earlier F05 describe different consumers of provenance checks; their common remedy does not create duplicate task claims.','score':None})
updated=[];event_by={x['path']:x for x in events};delta=[]
for oldrow in prior:
 row=copy.deepcopy(oldrow);ev=event_by.get(row['path'])
 if ev:
  row['axis']['read']='OBSERVED_IN_SIGNED_COMPONENT_PACKAGE';row['axis']['component_exercised']='OBSERVED_ONLY_AT_LINKED_SCOPE'
  if ev['event_id']=='R12V02-MASINI-DATE-01':row['axis']['installed_binding']='CLASS_BYTES_EQUAL_ONLY_NO_RUNNING_FORM_PROOF'
  evidence={'event_id':ev['event_id'],'source':ref(O/'Evenimente_11_fisiere.json','/rows/'+str(events.index(ev))),'scope':ev['scope'],'independent_reception':ev['independent_receipt']}
  row['current_evidence'].append(evidence);row['peer_receipts']['independent_A11']=ev['independent_receipt'];row['executor_for_current_event']=ev['executor']
  delta.append({'path':row['path'],'git_oid':row['git_oid'],'before_axis':oldrow['axis'],'after_axis':row['axis'],'evidence':evidence})
 updated.append(row)
reg=write_rows(O/'Registru_6728_R12_Val02.jsonl.gz',updated)
save(O/'Delta_11_fisiere.json',{'head':H,'previous':ref(PRE/'Registru_6728_R12_Val01.jsonl.gz'),'rows':delta,'new_file_identities':0,'new_partial_execution_events':11,'unchanged_rows':6717,'unchanged_mode_OID_owner_peer_control_task':True})
assert all((a['id'],a['path'],a['git_oid'],a['git_mode'],a['owner'],a['planned_peer'],a['control'],a['task_candidates'],a['R11_reference_only'])==(b['id'],b['path'],b['git_oid'],b['git_mode'],b['owner'],b['planned_peer'],b['control'],b['task_candidates'],b['R11_reference_only']) for a,b in zip(prior,updated))
assert sum(x['axis']['component_exercised']!='UNVERIFIED_R12' for x in updated)==13
assert sum(x['R11_reference_only'] is not None and x['R11_reference_only']['axes']['exercised']!='UNVERIFIED' for x in updated)==116
assert all(x['axis']['native_UI']=='UNVERIFIED_R12' and x['axis']['ERP_DB']=='UNVERIFIED_R12' and x['file_verdict'] is None for x in updated)
all_tools={x['path'] for x in updated if x['R11_reference_only'] is None};assert len(all_tools)==19;assert len(all_tools & {x['path'] for x in all_events})==12
index=[]
for e in all_events:
 d=dispatch[e['path']];index.append({'path':e['path'],'event_id':e['event_id'],'git_oid':e['git_oid'],'owner':d['owner'],'peer':d['planned_peer'],'control':d['control'],'pipelines':d['pipeline_candidates'],'tasks':d['task_candidates'],'event_source':ref(O/'Evenimente_11_fisiere.json','/rows/'+str(events.index(e))) if e in events else ref(PRE/'Evenimente_2_instrumente.json','/rows/'+str(old_events.index(e)))})
save(O/'Index_invers_13_fisiere.json',{'head':H,'rows':index,'key':['path','event_id'],'forward_inverse_pairs_equal':True,'criteria_accepted':0})
pair_checks={}
for dimension,key in [('owner','owner'),('peer','planned_peer'),('control','control'),('pipeline','pipeline_candidates'),('task','task_candidates')]:
 expected=set();actual=set()
 for e in all_events:
  value=dispatch[e['path']][key];values=value if isinstance(value,list) else [value]
  for val in values:expected.add((e['path'],e['event_id'],json.dumps(val,ensure_ascii=False,sort_keys=True)))
 for row in index:
  value=row[{'owner':'owner','peer':'peer','control':'control','pipeline':'pipelines','task':'tasks'}[dimension]];values=value if isinstance(value,list) else [value]
  for val in values:actual.add((row['path'],row['event_id'],json.dumps(val,ensure_ascii=False,sort_keys=True)))
 assert expected==actual,dimension;pair_checks[dimension]={'equal':True,'forward_pairs':len(expected),'inverse_pairs':len(actual),'missing':[],'extra':[]}
assert {(x['path'],x['event_id']) for x in index}=={(x['path'],x['event_id']) for x in all_events}
pair_checks['path_event']={'equal':True,'forward_pairs':13,'inverse_pairs':13}
historic=load(PRE/'Matrice_taskuri_criterii_R12_Val01.json')['historic_cohort'];assert historic['tasks']==652 and historic['criteria']==2619
hm=B/historic['R11_matrix_reference_only']['path'];assert sha(hm.read_bytes())==historic['R11_matrix_reference_only']['sha256'];hd=load(hm)
assert hd['task_population']==len(hd['task_rows'])==652 and hd['criterion_population']==len(hd['criterion_rows'])==2619
historical_dossiers=[]
for r in hd['task_rows']:
 p=B/r['historical_dossier']['file'];assert sha(p.read_bytes())==r['historical_dossier']['sha256']
 historical_dossiers.append({'task':r['task'],'canonical':r['canonical'],'dossier':ref(p),'criteria_count_as_historic':r['R10_criteria_count'],'no_current_credit_transferred':True})
assert sum(x['criteria_count_as_historic'] for x in historical_dossiers)==2619
save(O/'Conservare_652_fise_2619_criterii.json',{'source_matrix':ref(hm),'tasks':652,'criteria':2619,'all_dossiers_rehashed':historical_dossiers,'criterion_rows_sha256':sha(json.dumps(hd['criterion_rows'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'source_versions_preserved':True,'exact_dates_not_inferred':True,'current_new_credit':0})
matrix={'head':H,'historic_cohort':historic,'previous_matrix':ref(PRE/'Matrice_taskuri_criterii_R12_Val01.json'),'previous_wave_receipt':ref(prior_receipt),'current_source_event_count':13,'new_current_events':11,'historic_criteria_newly_accepted':0,'T240':{'alias':'T240','canonical':'P01.C14.T0001','state':'implementare','cohort':'OUTSIDE_HISTORIC_652','latest_snapshot':ref(E/'delta/2026-11-02T23-39-09-646Z/00_STATUS_TASKURI.json','/831'),'exact_completion_date':None,'component_event_ids':[x['event_id'] for x in all_events if x['path'] in all_tools],'events_are_audit_controls_not_new_commercial_criteria':True,'closed':False},'unassigned_Masini':{'path':ms['path'],'canonical':None,'mapping':'SHARED_NO_TASK_ASSIGNED','event_id':mev['event_id'],'registry_observation_T240_is_not_assignment':True},'population_supplement':ref(O/'Supliment_populatie_2339.json'),'T343_CO_IP':'Previous nominal oracle conflict remains open; CO|CO|CO until an accepted amendment.','index':ref(O/'Index_invers_13_fisiere.json'),'all17_contracts_open':True}
save(O/'Matrice_taskuri_criterii_R12_Val02.json',matrix)
reconcile={'head':H,'counting_unit':'Unique source path+OID for files; case ID/CLI/evaluation/independent witness are distinct metrics, no global sum of passes','Val01_reference':ref(PRE/'Reconciliere_cazuri_mutanti_si_limite.json'),'A08':{'cases':54,'top_level_CLI_invocations':58,'targets':5,'pipeline_cases_already_in54':['P_moved','P_deleted'],'reference':ref(lots['A08']['report_path'],'/summary'),'independent_receipt':ref(lots['A08']['receipt_path'])},'A09':{'cases':67,'targets':5,'by_instrument':lots['A09']['report_data']['case_count_by_instrument'],'fresh_repeats_already_in_cases':5,'matched_expected_observations_not_product_passes':67,'reference':ref(lots['A09']['report_path']),'independent_receipt':ref(lots['A09']['receipt_path'])},'Masini':{'unique_cases':12,'executions':2,'case_evaluations':24,'valid_dates_false_rejected_each':5,'invalid_empty_expected_each':7,'source_and_JAR_not24_unique_inputs':True,'reference':ref(lots['Masini']['directory']/'Cases_normalized.json'),'independent_receipt':ref(lots['Masini']['receipt_path'])},'guard_limit':'Python audit hooks and JDK SecurityManager are cooperative guards for inspected programs, not general OS isolation or proof of native business behavior.','new_tools_remaining':7,'native_UI_proofs_from_components':0,'native_business_contract_closures':0,'source_file_deduplication':{'prior2':2,'new_helpers':10,'new_existing_product_source':1,'current_total':13,'historical_R11_reference_only':116,'auto_transferred':0},'producer_and_independent_metrics_separate':True,'independent_limits':{k:config['receipts'][k]['limits'] for k in lots}}
reconcile['independent_A11_metrics_separate']={'source':ref(lots['A08']['receipt_path'],'/metrics'),'helper_CLI':12,'Masini_evaluations':8,'Mașini_valid_rejected':3,'Mașini_negative':5,'native_guard_canaries':7,'mechanical_identity_checks':2218,'no_sum_with_executor133_as_unique_tests':True,'native_PO_not_rerun_by_A11':True}
reconcile['Mașini_negative_detail']={'invalid_calendar_or_format':4,'empty_space_or_java_null':3,'copied_source_display_null':'Java null, not string literal null'}
save(O/'Reconciliere_metrici_si_limite.json',reconcile)
infra={'status':'NOT_INCLUDED_UNTIL_SEALED_RECEIPT','no_file_or_contract_credit':True,'task_id_created':None,'native_business_contracts_open':17}
if config.get('native_infrastructure'):
 ni=config['native_infrastructure'];mp=B/ni['manifest_path'];assert sha(mp.read_bytes())==ni['manifest_sha256'];nm,nvr=check_manifest(mp,ni['manifest_sha256'],ni.get('paths_relative',True));rp=B/ni['report_path'];assert sha(rp.read_bytes())==ni['report_sha256'];vp=B/ni['receipt_path'];sp=B/ni['seal_path'];assert sha(vp.read_bytes())==ni['receipt_sha256'];assert sha(sp.read_bytes())==ni['seal_sha256'];assert ni['manifest_sha256'] in json.dumps(load(vp),ensure_ascii=False);assert ni['receipt_sha256'] in json.dumps(load(sp),ensure_ascii=False)
 ap=mp.parent/'MANIFEST_reproducere_v1.json';am,av=check_manifest(ap,'3458ac7087d803a865400e4b8f4fbe1467e8e44683d00483be5a1014b8f1294e');assert am['immutable_primary_manifest']['sha256']==ni['manifest_sha256']
 infra={'status':'RECEIVED_GENERIC_NATIVE_INFRASTRUCTURE_ONLY','producer_manifest':ref(mp),'producer_report':ref(rp),'independent_receipt':ref(vp),'independent_seal':ref(sp),'artifacts_rehashed':len(nvr),'reproduction_appendix_manifest':ref(ap),'reproduction_appendix_artifacts':av,'observed_scope':ni['observed_scope'],'limitations':ni['limits'],'cleanup':ni['cleanup'],'no_file_or_contract_credit':True,'files_added_to6728':0,'component_events_added_to13':0,'task_id_created':None,'native_business_contracts_open':17};proof_inputs.append({'lot':'A05_native_infrastructure','manifest':ref(mp),'report':ref(rp),'independent_verdict':ref(vp),'independent_seal':ref(sp)});verified_artifacts+=nvr+av
save(O/'Infrastructura_nativa_separata.json',infra)
resources={'A12':{'product_tests_run':0,'product_services_created':0,'product_databases_created':0,'operational_writes':0,'only_read_rehash_and_artifact_build':True},'A08':{'source':ref(lots['A08']['directory']/'Cleanup_final.json'),'reported':load(lots['A08']['directory']/'Cleanup_final.json')},'A09_helpers':{'sources':[ref(lots['A09']['directory']/p) for p in ['cleanup.json','cleanup_supplement01.json']],'reported_scratch_removed':True},'Masini':{'source':ref(lots['Masini']['directory']/'Cleanup.json'),'reported':load(lots['Masini']['directory']/'Cleanup.json'),'must_not_claim_full_restitution':True,'explanation':'Automatic approval review rejected scratch deletion with reason blocked by policy; zero active owned Java processes, copied binaries/classes/harness directory retained.'},'A05_native':infra.get('cleanup','Await sealed independent cleanup receipt; A12 does not touch PG'),'all_laboratory_folders_restituted':False}
save(O/'Resurse_si_restituire.json',resources)
zones=[]
for z in [f'A{i:02}' for i in range(1,11)]:
 zr=[x for x in updated if x['owner']==z];zones.append({'owner':z,'assigned_files':len(zr),'current_partial_source_files':sum(x['axis']['component_exercised']!='UNVERIFIED_R12' for x in zr),'new_partial_source_files':sum(x['path'] in event_by for x in zr),'actual_executors_new':dict(collections.Counter(e['executor'] for e in events if e['owner']==z)),'full_file_acceptance':0,'whole_zone_verdict':None,'separate_infrastructure':ref(O/'Infrastructura_nativa_separata.json') if z=='A05' else None})
save(O/'Situatie_10_zone_R12_Val02.json',{'head':H,'rows':zones,'all17_contracts_open':True,'owner_is_preserved_from_dispatch_not_changed_to_executor':True})
counts={'technical_files':6728,'previous_partial_source_files':2,'new_partial_source_files':11,'current_partial_source_files':13,'remaining_without_current_component_evidence':6715,'new_audit_tools':19,'new_audit_tools_exercised_partial':12,'new_audit_tools_remaining':7,'historical_R11_exercised_reference_only':116,'historical_auto_transfer':0,'new_native_UI_component_proofs':0,'new_Masini_PO_transactions':0,'native_infrastructure_separate_from_file_counts':infra['status'],'historic_tasks':652,'historic_criteria':2619,'historic_criteria_newly_accepted':0,'full_file_verdicts':0,'full_task_verdicts':0,'native_contracts_open':17}
counts.update({'application_source_with_parser_exercised':1,'audit_helper_sources_partially_exercised_cumulative':12,'UI_ZK_scenarios_executed_in_these_lots':0,'generic_native_PO_infrastructure_scenarios':4 if config.get('native_infrastructure') else 0,'complete_business_contracts':0,'counting_boundary':'Application parser execution, synthetic offline helpers and generic native PO infrastructure are separate; no blanket claim of zero ERP code executed.'})
visual=E/'Publicare_R12_Val02/Manifest_vizualizare_rapoarte.json';vd=load(visual)
for r in vd['entries']:
 assert sha((B/r['source']).read_bytes())==r['source_sha256'];assert sha((B/r['view']).read_bytes())==r['view_sha256']
save(O/'Surse_si_receptii.json',{'head':H,'lots':proof_inputs,'source_artifact_records_rehashed':len(verified_artifacts),'actual_receipts_not_inferred_from_planned_peers':True,'previous_reception':ref(prior_receipt),'presentation_only_manifest':ref(visual),'presentation_adds_product_credit':False})
handoff={'schema':'eva.audit.r12.a12.wave/2','utc':datetime.now(timezone.utc).isoformat(),'head':H,'current_master_after_capture_not_asserted':True,'mode':'ADDITIVE_FROM_VAL01; NO_PRODUCT_TESTS_BY_A12','previous_manifest':ref(PRE/'MANIFEST_R12_Val01.json'),'previous_receipt':ref(prior_receipt),'approved_plan':ref(P/'Plan_delta_R12_v2.json'),'gate':ref(P/'A11_verdict_plan_delta_R12_v2.json'),'counts':counts,'population':ref(O/'Supliment_populatie_2339.json'),'register':reg,'delta':ref(O/'Delta_11_fisiere.json'),'events':ref(O/'Evenimente_11_fisiere.json'),'findings':ref(O/'Constatari_lot02.json'),'matrix':ref(O/'Matrice_taskuri_criterii_R12_Val02.json'),'inverse_index':ref(O/'Index_invers_13_fisiere.json'),'reconciliation':ref(O/'Reconciliere_metrici_si_limite.json'),'sources_and_receipts':ref(O/'Surse_si_receptii.json'),'native_infrastructure':ref(O/'Infrastructura_nativa_separata.json'),'resources':ref(O/'Resurse_si_restituire.json'),'zones':ref(O/'Situatie_10_zone_R12_Val02.json'),'A11_wave_reception_pending':True,'scores':{'plan_received_separately':10,'execution_quality':None,'product':None},'limits':['T240 stays implementare, not in historic652; branch5a670/JAR claims not accepted on df85.','Masini SHARED_NO_TASK_ASSIGNED; caller/static/class binding do not prove actual UI/PO save.','All17 full contracts remain open, including T343 CO/IP authority issue.','A05 generic PO infrastructure does not validate WMS G1/G2/G3 or any of the13 candidate-file events.','One scratch directory retained after automatic deletion rejection; no blanket claim that resources were fully returned.']}
save(O/'Handoff_R12_Val02.json',handoff)
tr=''.join('<tr><td>'+html.escape(e.get('audit_control') or 'Mașini · fără task atribuit')+'</td><td>'+html.escape(e['path'])+'</td><td>'+html.escape(e['executor'])+'</td></tr>' for e in events)
page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R12 Val02</title><style>body{font:16px/1.5 system-ui;max-width:1100px;margin:32px auto;padding:0 16px;color:#183041;background:#f7f9fb}p,td,code,a{overflow-wrap:anywhere}.table{overflow-x:auto}table{border-collapse:collapse;width:100%;background:white}th,td{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd}.note{border-left:4px solid #37788d;padding:12px;background:#e8f3f7}</style><h1>R12 · Val02 — componente și infrastructură separată</h1>'''
page+='<p>Revizie fixată <code>'+H+'</code>. Registrul păstrează 6.728 fișiere: două componente din Val01 și 11 surse noi au probe parțiale, în total <strong>13</strong>. Cele 116 fișiere R11 rămân istoric fără transfer automat.</p><p class="note">T240 — P01.C14.T0001 — rămâne în implementare. Cele 652 fișe și 2.619 criterii istorice sunt păstrate; niciun task, fișier integral sau contract nativ nu este închis.</p><h2>Ce a fost verificat</h2><p>A08: 54 cazuri, 58 invocări CLI pentru cinci instrumente. A09: 67 cazuri pentru alte cinci instrumente. La Mașini: 12 intrări în două execuții; cinci date valide sunt refuzate în fiecare. Sunt măsurători distincte, nu un total de teste de produs trecute.</p><div class="table"><table><tr><th>Control</th><th>Sursă exactă</th><th>Executor</th></tr>'+tr+'</table></div><h2>Limite și următorii pași</h2><p>Salvarea Mașini și interfața ZK nu au fost executate de acest lot; identitatea clasei instalate este separată. Instrumentele de ajutor au constatări nominale și limite de proveniență, numitori și euristici; se propune adaptarea celor existente.</p><p>Bootstrapul nativ A05 este consemnat separat și nu închide contractele WMS. Conflictul T343 CO/IP rămâne deschis. Afirmațiile despre ramura T240 5a670… nu sunt acceptate pe această revizie.</p><p>Directorul scratch Mașini a rămas după refuzul automat al ștergerii («blocked by policy»); raportul indică zero procese Java proprii. Nu se declară restituirea integrală a tuturor directoarelor.</p><p><a href="Handoff_R12_Val02.json">Predare și hashuri</a> · <a href="Matrice_taskuri_criterii_R12_Val02.json">Matrice nominală</a> · <a href="Constatari_lot02.json">Constatări cu recepție independentă</a> · <a href="Resurse_si_restituire.json">Resurse</a></p></html>'
assert not (O/'index.html').exists();(O/'index.html').write_text(page,encoding='utf-8',newline='\n')
checks={};errors=[]
def scan(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x and str(x['path']).startswith('executie/'):
   p=B/x['path'];key=(str(p),x['sha256'],x.get('pointer'))
   if key not in checks:
    try:
     assert sha(p.read_bytes())==x['sha256'],str(p)
     if x.get('pointer') is not None:resolve(load(p),x['pointer'])
     checks[key]=True
    except Exception as ex:errors.append({'reference':x,'error':str(ex)})
  for y in x.values():scan(y)
 elif isinstance(x,list):
  for y in x:scan(y)
for p in O.glob('*.json'):scan(load(p))
for r in updated:scan(r)
for l in lots.values():scan(l['report_data']);scan(l['receipt'])
assert not errors,errors[:4]
assert all(sha((B/x['path']).read_bytes())==x['sha256'] for x in before_manifest['files'])
qa={'utc':datetime.now(timezone.utc).isoformat(),'head':H,'handoff':ref(O/'Handoff_R12_Val02.json'),'register':reg,'counts':counts,'source_hashes_and_Git_blobs_verified':11,'unique_new_targets':11,'unique_cumulative_targets':13,'invariant_rows_6728':True,'unchanged_prior_wave_manifest_rehashed':ref(PRE/'MANIFEST_R12_Val01.json'),'forward_inverse_pairs_equal':pair_checks,'source_artifacts_rehashed':len(verified_artifacts),'local_references_and_JSON_pointers_verified':len(checks),'all17_contracts_open':True,'zero_current_credit_for_historical116':True,'errors':errors,'score':None}
save(O/'QA_R12_Val02.json',qa)
(O/'build_val02.py').write_bytes(pathlib.Path(__file__).read_bytes());(O/'build_population2339.py').write_bytes(pathlib.Path('D:/CodexWork/a12_r12_val02_population.py').read_bytes())
save(O/'build_receipt_configuration.json',config)
manifest={'utc':datetime.now(timezone.utc).isoformat(),'head':H,'status':'A12_ADDITIVE_CHECKPOINT_FOR_INDEPENDENT_RECEPTION','files':[ref(p) for p in sorted(O.iterdir()) if p.is_file()],'inputs':[ref(PRE/'MANIFEST_R12_Val01.json'),ref(prior_receipt),ref(P/'Plan_delta_R12_v2.json'),ref(P/'A11_verdict_plan_delta_R12_v2.json')]+[x[k] for x in proof_inputs for k in ['manifest','report','independent_verdict','independent_seal']],'no_self_reference':True}
save(O/'MANIFEST_R12_Val02.json',manifest)
for x in manifest['files']+manifest['inputs']:assert sha((B/x['path']).read_bytes())==x['sha256']
print(json.dumps({'manifest':ref(O/'MANIFEST_R12_Val02.json'),'handoff':ref(O/'Handoff_R12_Val02.json'),'qa':ref(O/'QA_R12_Val02.json'),'counts':counts},ensure_ascii=False,indent=2))
