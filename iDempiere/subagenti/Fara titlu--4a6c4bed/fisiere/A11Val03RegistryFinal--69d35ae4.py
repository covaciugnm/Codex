import pathlib,json,hashlib,copy,gzip,collections,datetime,functools
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';V=B/'A12/Val_03';O=B/'A11/Val03_registru'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf8'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def save(n,x):
 p=O/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return ref(p)
checks=[]
def ck(n,b):checks.append({'check':n,'ok':bool(b)});assert b,n
def resolve(x):
 p=R/x['path'];assert sha(p)==x['sha256'];
 if 'bytes' in x:assert p.stat().st_size==x['bytes']
 d=j(p)
 for v in x.get('pointer','').strip('/').split('/') if x.get('pointer','').strip('/') else []:d=d[int(v)] if isinstance(d,list) else d[v.replace('~1','/').replace('~0','~')]
 return d
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and x['path'].startswith('executie/') and 'sha256' in x:
   p=R/x['path'];ck('supplement ref '+x['path'],sha(p)==x['sha256'] and ('bytes' not in x or p.stat().st_size==x['bytes']))
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
base=j(O/'Control_A11_Val03_registru_baza_v1.json');ck('base QA fixed',sha(O/'Control_A11_Val03_registru_baza_v1.json')=='42876e242b4295a64e7e5bcbd4673d80d9d1ebd260e8ca3c0de4b6bb02b34de3')
ck('base manifest remains immutable',sha(V/'MANIFEST_R12_Val03.json')=='5f80d3973e34be94ce12aafdea307eec43aca359b42f2a0042c740e6c9db9a23')
ck('state seal fixed',sha(V/'SIGILIU_supliment_stari_Val03_v1.json')=='2a0c42fd6bc8ea2e11458a49792259c7f92c82a77e6217e997c343064a7dd38c')
ck('reading seal fixed',sha(V/'MANIFEST_lectura_finala_Val03_v1.json')=='1b40caa6b7587badc3e304467ad0a4386c5a3f725f4c4b9c3f0efd107b530dfe')
for n in ['SIGILIU_supliment_stari_Val03_v1.json','MANIFEST_lectura_finala_Val03_v1.json','Handoff_R12_Val03_v2.json','Matrice_taskuri_criterii_R12_Val03_corectata_v1.json']:walk(j(V/n))
old=j(V/'Matrice_taskuri_criterii_R12_Val03.json');new=j(V/'Matrice_taskuri_criterii_R12_Val03_corectata_v1.json');expected=copy.deepcopy(old);supp=j(V/'Supliment_stari_nominale_Val03_v1.json')
for i,x in enumerate(supp['overrides']):
 value=resolve(x['source']);ck('state exact '+x['alias'],value==x['value_after'] and x['source_field']=='stare_generala' and x['target_pointer']==f'/current_rows/{i}/current_state' and expected['current_rows'][i]['alias']==x['alias'] and expected['current_rows'][i]['current_state'] is None)
 expected['current_rows'][i]['current_state']=value
ck('only four matrix values changed',expected=={k:v for k,v in new.items() if k!='presentation_correction'})
oh=j(V/'Handoff_R12_Val03.json');nh=j(V/'Handoff_R12_Val03_v2.json');ck('handoff original fields preserved except schema/utc/matrix',all(nh[k]==v for k,v in oh.items() if k not in ['schema','utc','matrix']))
ck('counts unchanged',nh['counts']==oh['counts']);ck('26+7+2+4 exact',nh['cumulative_evidence_categories']=={'original_components_or_method_paths':26,'comparators':7,'transitive_type_record_usage_without_method_trace':2,'fixture_binding_or_metadata':4})
reg=[json.loads(x) for x in gzip.decompress((V/'Registru_6728_R12_Val03.jsonl.gz').read_bytes()).decode().splitlines()];rm={x['path']:x for x in reg};current={p for p,x in rm.items() if x['axis']['component_exercised']!='UNVERIFIED_R12'}
zones=j(V/'Checklist_10_zone_Val03.json')['rows'];ck('ten distinct owners',len(zones)==len({x['owner'] for x in zones})==10)
for z in zones:
 ps={p for p,x in rm.items() if x['owner']==z['owner']};ck('zone aggregate '+z['owner'],z['assigned_files']==len(ps) and z['current_partial_sources']==len(ps&current) and z['full_acceptance']==0)
cons=j(V/'Conservare_652_fise_2619_criterii.json');hist=resolve(cons['source_matrix']);ck('652tasks2619criteria actual matrix',len(hist['task_rows'])==652 and len(hist['criterion_rows'])==2619 and cons['current_new_credit']==0)
for n in ['Ipoteza_G3_dubla_scadere_NEEXECUTATA.json','Ipoteza_G3_promo_NEEXECUTATA.json']:
 x=j(V/n);ck('unexecuted hypothesis '+n,x['status']=='IPOTEZA_DE_AUDIT_NEEXECUTATA' and x['finding_confirmed'] is False and x['new_execution_credit']==0 and x['priority'] is None)
resources=j(V/'Resurse_si_restituire_Val03.json');ck('six retained roots',resources['retained_after_auto_review']['count']==len(set(resources['retained_after_auto_review']['roots']))==6 and not resources['all_laboratory_resources_returned'])
report=save('Verdict_A11_R12_Val03_registru_v1.json',{
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','candidate':oh['head'],'operational_server_HEAD_excluded':oh['server_HEAD_not_candidate'],
 'disposition':'RECEPȚIE LIMITATĂ ACCEPTATĂ pentru registrul Val03 împreună cu suplimentul de stări și handoffv2; fără notă globală ori închidere de produs',
 'base_manifest':ref(V/'MANIFEST_R12_Val03.json'),'authoritative_handoff':ref(V/'Handoff_R12_Val03_v2.json'),'presentation_manifest':ref(V/'MANIFEST_lectura_finala_Val03_v1.json'),'state_addendum':ref(V/'SIGILIU_supliment_stari_Val03_v1.json'),'base_control':ref(O/'Control_A11_Val03_registru_baza_v1.json'),
 'verification':{'technical_identities':6728,'identity_and_routing_dimensions':8,'changed_evidence_rows_only':57,'new_partial_scope_rows':26,'new_static_only':31,'partial_scope_rows_total':39,'old13rows_unchanged':True,'historic_dossiers_actually_rehashed':652,'historic_criteria_preserved':2619,'historic_R11_partial_sources_reference_only':116,'historic_credit_transferred':0,'forward_inverse_pairs':39,'reference_instances_resolved_in_base_QA':base['reference_instances'],'distinct_reference_paths_in_base_QA':base['distinct_reference_paths'],'manifest_output_files':25,'manifest_input_references':30,'distinct_manifest_input_paths':29},
 'metric_semantics':{'original_components_or_method_paths':26,'comparators':{'Bash':5,'SQL_sites_same_query':2,'total':7},'transitive_record_type_uses':2,'fixture_binding_metadata':4,'sum39_is_not_business_execution_or_whole_files':True,'sum35_excludes_fixture_binding_metadata':35,'all19newtools_have_only_bounded_observations':True,'full_new_tool_receipts':0},
 'cases':{'new_helper_SQL_case_identities':121,'A06':36,'A10':73,'G3_unique_fixtures':12,'G3_SQL_evaluations_not_unique_cases':24,'N05_scenarios_separate':7,'A11_independent_controls_not_added_to_executor_counts':True,'not_PASS_or_criteria_total':True},
 'state_correction':{'error_found_by_A11':'current_state projected from missing stare instead of stare_generala, yielding4null values.','accepted_additive_values':{'T232':'implementare','T240':'implementare','T343':'audit','T355':'închis'},'meaning':'States are declarations from the frozen source snapshot, not independent audit acceptance. Original matrix/manifest preserved; corrected reading/handoff linked.'},
 'N05':{'finding':'A05.R11.G2.BOM.1/N05 strengthened by original native process and PO handler at df85; same defect, not new count.','priority':'P1 proposed for quantitative WMS records; physical inventory and accounting value impact not measured.','source_levels':'46 read =29static +11methodpaths +2types +3fixture/binding +1metadata','historic_criteria':'T355-R2-001/-002 have limited observations/counterexample; -003 no idempotency credit from postrollback retry; -004 boxes/labor not exercised. None closed.','accounting':'G2 is non-accounting; recovery of reusable components does not automatically recreate consumed boxes or reverse labor. G1 cost/posting remains separate.'},
 'accepted_limits':['G3 SQL sites are comparators, not Java/native/PostgreSQL/channel persistence.','Two extra G3 hypotheses remain unexecuted and unconfirmed, with no priority or criterion credit.','Planned peer assignments do not assert those peers performed an audit; actual executor and independent A11 are explicit.','No UI/ZK full reception, no product10/10, no full source/task/contract closure.','Historical exact closure dates are not inferred where undocumented.','N05 lab returned; six retained roots remain after approval rejection, without a workaround.'],
 'checks_supplement':checks,'open_contracts':17,'full_files_accepted':0,'full_tasks_closed_by_this_wave':0,'global_score':None,
 'resume_checklist':ref(B/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'),
 'review_tool_calibration':'Local metadata verifier was adapted to declared schemas:25outputs/30references with1duplicate, static_support_only, whole-JSON references and G3 result-vector projection. These iterations wrote no base verdict and executed no product; no product defects inferred from verifier exceptions.',
 'product_executions_by_this_registry_review':0})
seal=save('SIGILIU_A11_R12_Val03_registru_v1.json',{'immutable':True,'algorithm':'SHA256','files':[report,ref(O/'Control_A11_Val03_registru_baza_v1.json')],'base_manifest':ref(V/'MANIFEST_R12_Val03.json'),'state_addendum':ref(V/'SIGILIU_supliment_stari_Val03_v1.json'),'presentation_manifest':ref(V/'MANIFEST_lectura_finala_Val03_v1.json')})
print(json.dumps({'report':report,'seal':seal,'supplement_checks':len(checks)},ensure_ascii=False))
