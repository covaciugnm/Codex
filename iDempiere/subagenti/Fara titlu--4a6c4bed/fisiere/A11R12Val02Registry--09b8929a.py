from pathlib import Path
import json,hashlib,gzip,datetime,sys,collections,functools,shutil
sys.stdout.reconfigure(encoding='utf8')
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';V=B/'A12/Val_02';P=R/'executie/R12_plan_delta';O=B/'A11/Val02_registru';O.mkdir(exist_ok=True)
@functools.lru_cache(None)
def raw(p):return Path(p).read_bytes()
def h(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def rows(p):return [json.loads(x) for x in gzip.decompress(raw(p)).decode('utf8').splitlines() if x]
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p),'bytes':len(raw(p))}
checks=[];refs=[]
def ck(name,ok,detail=None):checks.append({'check':name,'passed':bool(ok),'detail':detail});assert ok,(name,detail)
def resolve(x):
 p=R/x['path'];assert h(p)==x['sha256'],x
 if 'bytes' in x:assert len(raw(p))==x['bytes'],x
 z=j(p) if 'pointer' in x else None
 if 'pointer' in x:
  for part in x['pointer'].strip('/').split('/'):
   key=part.replace('~1','/').replace('~0','~');z=z[int(key)] if isinstance(z,list) else z[key]
 return z
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and x['path'].startswith('executie/') and 'sha256' in x:resolve(x);refs.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=V/'MANIFEST_R12_Val02.json';hp=V/'Handoff_R12_Val02.json'
ck('manifest expected',h(mp)=='f169311d8a251f6f01cc47facdb20b74434a7afe0c9687c6792d587723decc5d');ck('handoff expected',h(hp)=='609fe44a4d91fe936d91480d8477b3babc21ec16f0725d97d9faf71d0334672d')
manifest=j(mp);handoff=j(hp);walk(manifest)
ck('20 manifest unique entries',len(manifest['files'])==len({x['path'] for x in manifest['files']})==20)
for x in manifest['files']:
 if x['path'].endswith('.json'):walk(j(R/x['path']))
reg=rows(V/'Registru_6728_R12_Val02.jsonl.gz');prev=rows(B/'A12/Val_01/Registru_6728_R12_Val01.jsonl.gz');dispatch=rows(P/'Dispatch_tehnic_integral_R12.jsonl.gz');histreg=rows(R/'executie/R11_fisiere/A12/Val_04/Registru_6709_val_04.jsonl.gz')
rm={x['path']:x for x in reg};pm={x['path']:x for x in prev};dm={x['path']:x for x in dispatch};hm={x['path']:x for x in histreg}
ck('6728 identities unchanged',len(reg)==len(rm)==len(dm)==6728 and rm.keys()==dm.keys()==pm.keys() and len({x['id'] for x in reg})==6728)
ck('raw register SHA',hashlib.sha256(gzip.decompress(raw(V/'Registru_6728_R12_Val02.jsonl.gz'))).hexdigest()==handoff['register']['raw_sha256'])
fields=[('id','id'),('git_oid','git_object'),('git_mode','mode'),('owner','owner'),('planned_peer','peer'),('control','control'),('pipeline_candidates','pipeline_candidates'),('task_candidates','task_candidates')]
for path,x in rm.items():
 for a,b in fields:assert x[a]==dm[path][b],(path,a)
 assert x['candidate']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
 assert x['R11_reference_only']==pm[path]['R11_reference_only']
 assert x['axis']['whole_file_acceptance'] is None and x['file_verdict'] is None
 assert x['axis']['native_UI']==x['axis']['ERP_DB']=='UNVERIFIED_R12'
walk(reg);ck('all6728 routing8fields history whole/native unchanged',True)
events=j(V/'Evenimente_11_fisiere.json')['rows'];em={x['path']:x for x in events};changed={p for p in rm if rm[p]!=pm[p]};current={p for p,x in rm.items() if x['axis']['component_exercised']=='OBSERVED_ONLY_AT_LINKED_SCOPE'};old_current={p for p,x in pm.items() if x['axis']['component_exercised']=='OBSERVED_ONLY_AT_LINKED_SCOPE'}
ck('11 new rows exact and others unchanged',len(events)==len(em)==11 and changed==set(em) and len(current)==13 and len(old_current)==2 and current==old_current|set(em) and not old_current&set(em))
ck('116 historical no transfer',len({p for p,x in hm.items() if x['axis']['exercised']=='OBSERVED_ONLY_AT_LINKED_SCOPE'})==116 and all(x['R11_reference_only'] is None or x['R11_reference_only']['credit_transferred'] is False for x in reg))
a11=j(B/'A11/Val02_loturi/Verdict_A11_loturi_Val02_v1.json');a11file={x['file']['path']:x for x in a11['file_receptions']}
ck('new target identities equal independent reception',em.keys()==a11file.keys())
for p,e in em.items():
 rr=rm[p];s=raw(R/e['source']['path']);oid=hashlib.sha1(b'blob '+str(len(s)).encode()+b'\0'+s).hexdigest();assert oid==e['git_oid']==rr['git_oid'] and hashlib.sha256(s).hexdigest()==e['sha256']==a11file[p]['file']['sha256']
 assert resolve(e['independent_receipt'])==a11file[p] and e['independent_disposition']==a11file[p]['disposition'] and e['independent_limit']==a11file[p]['limit']
 assert e['whole_file_acceptance'] is None and e['whole_task_acceptance'] is None
 assert len(rr['current_evidence'])==1 and resolve(rr['current_evidence'][0]['source'])==e and resolve(rr['peer_receipts']['independent_A11'])==a11file[p]
ck('11 sourceOID sourceSHA receiptpointer scope exact',True)
maspath=next(p for p in em if p.endswith('WSagaMasiniForm.java'));ck('Masini class binding only unassigned',rm[maspath]['axis']['installed_binding']=='CLASS_BYTES_EQUAL_ONLY_NO_RUNNING_FORM_PROOF' and em[maspath]['canonical_task'] is None and not rm[maspath]['task_candidates'])
ck('6715 no current component scope',sum(x['axis']['component_exercised']=='UNVERIFIED_R12' for x in reg)==6715)
idx=j(V/'Index_invers_13_fisiere.json')['rows'];ck('13 inverse unique same paths',len(idx)==len({x['path'] for x in idx})==13 and {x['path'] for x in idx}==current)
for x in idx:
 y=rm[x['path']];ev=resolve(x['event_source']);assert ev['path']==x['path'] and ev['event_id']==x['event_id']
 assert (x['git_oid'],x['owner'],x['peer'],x['control'],x['pipelines'],x['tasks'])==(y['git_oid'],y['owner'],y['planned_peer'],y['control'],y['pipeline_candidates'],y['task_candidates'])
ck('forward inverse 13 exact multidimensional pairs',True)
cases=j(V/'Cazuri_nominale_133.json')['rows'];cm={x['id']:x for x in cases};ck('133 unique records per lot not unique tests',len(cases)==len(cm)==133 and collections.Counter(x['lot'] for x in cases)=={'A08':54,'A09':67,'Masini':12} and all(x['not_whole_product_PASS'] for x in cases))
linked=set()
for e in events:
 for rp in e['nominal_cases']:
  case=resolve(rp);assert case['id'] in cm;linked.add(case['id'])
  if e['audit_control'] and case['lot']=='A09':assert case['instrument']==e['audit_control']
ck('all133 connected nominally',linked==cm.keys())
a08raw=sum([j(B/'A08_Helper_rapoarte_lot02'/f)['cases'] for f in ['Results.json','Results_supplement01.json','Results_supplement02.json']],[])
a09raw=j(B/'A09_Helper_corpus_lot02/results.json')['results']+j(B/'A09_Helper_corpus_lot02/results_supplement01.json')['results']
ck('executor case IDs preserved', {x['producer_case_id'] for x in cases if x['lot']=='A08'}=={x['id'] for x in a08raw} and {x['producer_case_id'] for x in cases if x['lot']=='A09'}=={x['case'] for x in a09raw})
for x in cases:
 if x['lot'] in ['A08','A09']:
  rawcase=resolve(x['raw_result']) if 'pointer' in x['raw_result'] else j(R/x['raw_result']['path']);assert rawcase.get('id',rawcase.get('case'))==x['producer_case_id']
 else:
  assert len(x['observed'])==2
  for obs in x['observed']:
   rr=resolve(obs['source']);assert rr['actual']==obs['actual']
ck('133 raw results/evaluations linked without duplication',True)
matrix=j(V/'Matrice_taskuri_criterii_R12_Val02.json');hist=j(R/matrix['historic_cohort']['R11_matrix_reference_only']['path']);cons=j(V/'Conservare_652_fise_2619_criterii.json')
ck('6522619 historical preserved',len(hist['task_rows'])==652 and len(hist['criterion_rows'])==2619 and cons['tasks']==652 and cons['criteria']==2619 and len(cons['all_dossiers_rehashed'])==652)
td={x['task']:x for x in hist['task_rows']}
for x in cons['all_dossiers_rehashed']:
 orig=td[x['task']]['historical_dossier'];assert x['dossier']['path']==orig['file'] and x['dossier']['sha256']==orig['sha256'];assert x['no_current_credit_transferred'];assert h(R/orig['file'])==orig['sha256']
ck('652 actual dossiers rehashed',True)
ck('zero historic credit activeT240 separate',matrix['historic_criteria_newly_accepted']==matrix['historic_cohort']['current_R12_criterion_credit_from_this_wave']==0 and matrix['T240']['closed'] is False and matrix['T240']['canonical']=='P01.C14.T0001' and matrix['T240']['state']=='implementare' and matrix['T240']['exact_completion_date'] is None and len(matrix['T240']['component_event_ids'])==12)
ck('T343 oracle preserved', 'CO|CO|CO' in matrix['T343_CO_IP'])
fins=j(V/'Constatari_lot02.json')['rows'];ck('22 findings and limits unique',len(fins)==len({x['id'] for x in fins})==22)
disp={x['id']:x for x in a11['findings_disposition']}
for x in fins:
 d=x['disposition'].get('MASINI-DATE',x['disposition']);assert d==disp[d['id']]
hc11=next(x for x in fins if x['id'].endswith('HC11'));ck('HC11 reclassified not P2 automatic',hc11.get('effective_priority') is None and hc11['disposition']['A11_disposition']=='ADMIS_OBSERVATIE; RESPINS_DEFECT_P2_NECONDITIONAT')
zones=j(V/'Situatie_10_zone_R12_Val02.json')['rows'];ck('10 zones',len(zones)==len({x['owner'] for x in zones})==10)
for z in zones:
 pset={p for p,x in rm.items() if x['owner']==z['owner']};assert z['assigned_files']==len(pset) and z['current_partial_source_files']==len(pset&current) and z['new_partial_source_files']==len(pset&set(em)) and z['whole_zone_verdict'] is None
ck('zone aggregates recomputed',True)
infra=j(V/'Infrastructura_nativa_separata.json');native=j(B/'A11/Val02_loturi/Verdict_A11_A05_infrastructura_Val02_v1.json');ck('infrastructure separate no credit',infra['files_added_to6728']==infra['component_events_added_to13']==0 and infra['task_id_created'] is None and infra['observed_scope']==native['accepted'] and all(x in infra['limitations'] for x in native['rejected_extensions']))
ck('retained scratch explicit',j(V/'Resurse_si_restituire.json')['all_laboratory_folders_restituted'] is False)
ck('17 contracts7instruments scoresnull',matrix['all17_contracts_open'] and handoff['counts']['native_contracts_open']==17 and handoff['counts']['new_audit_tools_remaining']==7 and handoff['scores']=={'plan_received_separately':10,'execution_quality':None,'product':None})
out={'schema':'A11.R12.Val02.registry_checks.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[ref(mp),ref(hp)],'checks':checks,'all_passed':True,'reference_edges_rehashed_and_pointers_resolved':len(refs),'distinct_reference_files':len({x['path'] for x in refs}),'historical_dossiers_rehashed':652,'identity_equality':{'files':6728,'dimensions':len(fields),'changed_identity_or_routing':0,'unchanged_complete_rows_from_Val01':6717,'changed_evidence_rows':11},'numbers':{'current_component_sources':13,'historical_R11_component_sources_only':116,'historic_tasks':652,'historic_criteria':2619,'current_historic_criteria_credited':0,'whole_files':0,'whole_tasks':0,'contracts_open':17,'remaining_new_tools':7,'nominal_case_records':133},'method':{'path':str(Path(__file__)),'sha256':h(Path(__file__))},'product_executions':0}
p=O/'Control_A11_R12_Val02_registru_v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'output':ref(p),'checks':len(checks),'references':len(refs)},ensure_ascii=False))
