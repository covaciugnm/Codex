from pathlib import Path
import json,hashlib,gzip,datetime,sys,collections,functools
sys.stdout.reconfigure(encoding='utf8')
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');V=R/'executie/R12_fisiere/A12/Val_01';P=R/'executie/R12_plan_delta';O=R/'executie/R12_fisiere/A11/Val01';O.mkdir(exist_ok=True)
@functools.lru_cache(None)
def raw(p):return Path(p).read_bytes()
def h(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def rows(p):return [json.loads(x) for x in gzip.decompress(raw(p)).decode('utf8').splitlines() if x]
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p),'bytes':len(raw(p))}
checks=[];references=[]
def check(name,ok,detail=None):checks.append({'check':name,'passed':bool(ok),'detail':detail});assert ok,(name,detail)
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and x['path'].startswith('executie/') and 'sha256' in x:
   p=R/x['path'];assert h(p)==x['sha256'],x
   if 'bytes' in x:assert len(raw(p))==x['bytes'],x
   if 'pointer' in x:
    z=j(p)
    for part in x['pointer'].strip('/').split('/'):
     key=part.replace('~1','/').replace('~0','~');z=z[int(key)] if isinstance(z,list) else z[key]
   references.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=V/'MANIFEST_R12_Val01.json';hp=V/'Handoff_R12_Val01.json'
check('manifest_expected_SHA',h(mp)=='2d0e8529b61698031a132cf4bf8e72f17b8a9fbb03df2b0000e885dde38efe93')
check('handoff_expected_SHA',h(hp)=='ab1111fc909d039af8aeab5d262f84fbe7dce56290e1989b2d0f33af608b29ce')
manifest=j(mp);handoff=j(hp);walk(manifest)
for v in manifest['files']:
 if v['path'].endswith('.json'):walk(j(R/v['path']))
reg=rows(V/'Registru_6728_R12_Val01.jsonl.gz');dispatch=rows(P/'Dispatch_tehnic_integral_R12.jsonl.gz');old=rows(R/'executie/R11_fisiere/A12/Val_04/Registru_6709_val_04.jsonl.gz')
check('register_raw_SHA',hashlib.sha256(gzip.decompress(raw(V/'Registru_6728_R12_Val01.jsonl.gz'))).hexdigest()==handoff['register']['raw_sha256'])
rm={x['path']:x for x in reg};dm={x['path']:x for x in dispatch};om={x['path']:x for x in old}
check('6728_unique_paths_and_IDs',len(rm)==len(reg)==len(dm)==len(dispatch)==6728 and len({x['id'] for x in reg})==6728)
check('identity_set_equal_dispatch',rm.keys()==dm.keys())
fields=[('id','id'),('git_oid','git_object'),('git_mode','mode'),('owner','owner'),('planned_peer','peer'),('control','control'),('pipeline_candidates','pipeline_candidates'),('task_candidates','task_candidates')]
for path,row in rm.items():
 for a,b in fields:assert row[a]==dm[path][b],(path,a)
 assert row['candidate']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
walk(reg)
check('all_identity_routing_dimensions_equal',True,{'files':6728,'fields':[a for a,b in fields]})
check('old6709_plus19_new',len(om)==6709 and om.keys()<=rm.keys() and len(rm.keys()-om.keys())==19)
for p,rr in om.items():
 current=rm[p];history=current['R11_reference_only'];assert history and history['candidate']==rr['candidate'] and history['axes']==rr['axis'] and history['credit_transferred'] is False
 assert current['git_oid']==rr['git_oid'] and current['git_mode']==rr['git_mode'] and history['same_blob_mode'] is True
 assert history['source']['logical_path']==p
check('6709_historical_axes_exact_no_transfer',True)
check('19_new_have_no_history',all(rm[p]['R11_reference_only'] is None for p in rm.keys()-om.keys()))
historic_exercised={p for p,x in om.items() if x['axis']['exercised']=='OBSERVED_ONLY_AT_LINKED_SCOPE'}
new_exercised={p for p,x in rm.items() if x['axis']['component_exercised']=='OBSERVED_ONLY_AT_LINKED_SCOPE'}
check('116_history_only',len(historic_exercised)==116)
check('2_current_sources_exact',new_exercised=={'tools/teste/t240/test_clasa_verifica_proba.py','tools/teste/t240/verifica_proba.py'})
for p,x in rm.items():
 assert x['axis']['native_UI']==x['axis']['ERP_DB']==x['axis']['installed_binding']=='UNVERIFIED_R12'
 assert x['axis']['whole_file_acceptance'] is None and x['file_verdict'] is None
 assert x['peer_receipts']['A09_receipt_asserted'] is False
 if p not in new_exercised:assert not x['current_evidence'] and x['peer_receipts']['independent_A11'] is None and x['axis']['component_exercised']=='UNVERIFIED_R12'
 else:assert len(x['current_evidence'])==1 and x['peer_receipts']['independent_A11']['sha256']=='3d0bdd5cfc5010cf8cdd994a4c7d1ed2205f3d973250eb9592129cc5a55ea371'
check('all6728_native_unverified_full_none_no_invented_A09',True)
check('6726_remaining_not_defect_count',len(rm)-len(new_exercised)==6726)
matrix=j(V/'Matrice_taskuri_criterii_R12_Val01.json');hist=j(R/matrix['historic_cohort']['R11_matrix_reference_only']['path'])
check('652_tasks2619criteria_preserved',hist['task_population']==len(hist['task_rows'])==652 and hist['criterion_population']==len(hist['criterion_rows'])==2619)
check('unique_historical_tasks_and_criteria',len({x['task'] for x in hist['task_rows']})==652 and len({(x['task'],x['criterion']) for x in hist['criterion_rows']})==2619)
for t in hist['task_rows']:
 d=t['historical_dossier'];assert h(R/d['file'])==d['sha256'],t['task']
check('652_historical_dossiers_rehashed',True)
check('0_historic_current_criterion_credit',matrix['historic_cohort']['current_R12_criterion_credit_from_this_wave']==0)
active=matrix['active_tasks_outside_cohort'];check('active_T240_separate_unclosed',len(active)==1 and active[0]['task_alias']=='T240' and active[0]['canonical']=='P01.C14.T0001' and active[0]['state']=='implementare' and active[0]['whole_task_verdict'] is None)
events=j(V/'Evenimente_2_instrumente.json')['rows'];links=matrix['current_semantic_links'];check('2event_links_exact',len(events)==len(links)==2 and events==links and {x['path'] for x in events}==new_exercised)
check('T343_old_oracle_preserved',matrix['pending_T343']['new_criterion_ids_created']==0 and matrix['pending_T343']['unchanged_oracle']=='CO|CO|CO until nominal amendment received')
zones=j(V/'Situatie_10_zone_R12_Val01.json')['rows'];check('10zones_unique',len(zones)==len({x['owner'] for x in zones})==10)
for z in zones:
 owner=z['owner'];assigned={p for p,x in rm.items() if x['owner']==owner}
 assert z['assigned_files']==len(assigned) and z['files_component_exercised_R12']==len(assigned&new_exercised) and z['historical_R11_exercised_reference_only']==len(assigned&historic_exercised)
 assert z['native_files_exercised_R12']==0 and z['whole_zone_verdict'] is None
check('zone_counts_recomputed',True,{'assigned_total':sum(z['assigned_files'] for z in zones),'current':sum(z['files_component_exercised_R12'] for z in zones),'historical':sum(z['historical_R11_exercised_reference_only'] for z in zones)})
prod=j(R/'executie/R12_fisiere/A08_T240/Lot_01_final_v1/Raport_A08_T240_R12_lot01_v1.json');verdict=j(R/'executie/R12_fisiere/A11/T240_lot01/Verdict_A11_R12_T240_lot01_v1.json');findings=j(V/'Constatari_componente_T240.json')['rows']
check('five_findings_exact_base_fields',len(findings)==5 and all(all(fin.get(k)==v for k,v in original.items()) for original,fin in zip(prod['findings'],findings)))
for x,d in zip(findings,verdict['findings_disposition']):assert x['independent_disposition']==d
check('five_A11_dispositions_exact',True)
rec=j(V/'Reconciliere_cazuri_mutanti_si_limite.json');check('metrics_equal_producer',rec['counts']==prod['counts'])
check('no_unique_tests_total_no_score',rec['no_total_unique_tests_inferred'] is True and rec['grade'] is None)
check('fixture24_count_not_new_credit','13 distinct RO' in rec['fixture_count_erratum']['actual_executed'] and '24 rows' in rec['fixture_count_erratum']['actual_executed'] and rec['fixture_count_erratum']['test_count_is_not_screen_count'] is True)
check('17_contracts_and17instruments_open',matrix['all17_native_contracts_open'] and handoff['counts']['native_contracts_still_open']==17 and handoff['counts']['new_instruments_still_unexercised']==17)
check('scores_current_null',handoff['scores']=={'plan_received_separately':10,'execution_quality':None,'product':None})
out={'schema':'A11.R12.Val01.registry_checks.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[ref(mp),ref(hp)],'checks':checks,'all_passed':True,'reference_edges_rehashed_and_pointers_resolved':len(references),'distinct_reference_files':len({x['path'] for x in references}),'historical_dossiers_rehashed':652,'identity_equality':{'files':6728,'dimensions':len(fields),'changed_ID_or_path_or_OID_or_mode_or_routing':0},'numbers':{'current_component_sources':2,'historical_R11_component_sources_only':116,'historic_tasks':652,'historic_criteria':2619,'current_historic_criteria_credited':0,'whole_files':0,'whole_tasks':0,'contracts_open':17},'method':{'path':str(Path(__file__)),'sha256':h(Path(__file__))},'product_executions':0}
dst=O/'Control_A11_R12_Val01_v1.json';assert not dst.exists();dst.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'artifact':ref(dst),'checks':len(checks),'refs':len(references),'distinct_files':out['distinct_reference_files']},ensure_ascii=False))
