import pathlib,json,hashlib,gzip,datetime,collections,functools,sys
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';V=B/'A12/Val_04';P=B/'A12/Val_03';O=B/'A11/Val04_registru'
@functools.lru_cache(None)
def raw(p):return pathlib.Path(p).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def rows(p):return [json.loads(l) for l in gzip.decompress(raw(p)).decode('utf8').splitlines() if l]
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def write(p,d):assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[];refs=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'details':d});assert b,(n,d)
def resolve(x):
 p=pathlib.Path(x['path']);p=p if p.is_absolute() else R/p
 ck('hash '+x['path'],sha(p)==x['sha256'] and ('bytes'not in x or len(raw(p))==x['bytes']))
 z=j(p) if 'pointer' in x else None
 if 'pointer' in x:
  for part in x['pointer'].removeprefix('#').strip('/').split('/') if x['pointer'].removeprefix('#').strip('/') else []:
   k=part.replace('~1','/').replace('~0','~');z=z[int(k)] if isinstance(z,list) else z[k]
 refs.append(x);return z
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and (x['path'].startswith('executie/') or pathlib.Path(x['path']).is_absolute()):resolve(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=V/'MANIFEST_R12_Val04.json';hp=V/'Handoff_R12_Val04_v1.json';ck('manifest fixed',sha(mp)==sys.argv[1]);ck('handoff fixed',sha(hp)==sys.argv[2]);m=j(mp);h=j(hp);walk(m)
for e in m['files']:
 p=R/e['path']
 if p.suffix=='.json':walk(j(p))
for name in ['Increment_01_frontend/MANIFEST_increment_frontend.json','Increment_02_G3/MANIFEST_increment_G3.json']:
 z=j(V/name);walk(z)
 for e in z['files']:
  p=R/e['path']
  if p.suffix=='.json':walk(j(p))
reg=rows(V/'Registru_6728_R12_Val04.jsonl.gz');old=rows(P/'Registru_6728_R12_Val03.jsonl.gz');dispatch=rows(R/'executie/R12_plan_delta/Dispatch_tehnic_integral_R12.jsonl.gz');rm={x['path']:x for x in reg};pm={x['path']:x for x in old};dm={x['path']:x for x in dispatch}
ck('6728 exact identities',len(reg)==len(rm)==len(dm)==len(pm)==6728 and rm.keys()==dm.keys()==pm.keys())
fields=[('id','id'),('git_oid','git_object'),('git_mode','mode'),('owner','owner'),('planned_peer','peer'),('control','control'),('pipeline_candidates','pipeline_candidates'),('task_candidates','task_candidates')]
for p,x in rm.items():
 for a,b in fields:assert x[a]==dm[p][b],(p,a)
 assert x['candidate']=='df85d33c1648ce2b2df130a60a05ef696e2e5480' and x['R11_reference_only']==pm[p]['R11_reference_only']
 assert x['file_verdict'] is None and x['axis']['whole_file_acceptance'] is None and x['axis']['native_UI']=='UNVERIFIED_R12'
 assert x['current_evidence'][:len(pm[p]['current_evidence'])]==pm[p]['current_evidence']
walk(reg);ck('routing preserved and no previous evidence removed',True)
events=j(V/'Evenimente_Val04.json')['rows'];static=j(V/'Lecturi_statice_Val04.json')['rows'];em={x['path']:x for x in events};changed={p for p in rm if rm[p]!=pm[p]};statpaths={x['path'] for x in static}
ck('delta equals all new evidence paths',changed==set(em)|statpaths and len(events)==len(em)==11 and len(static)==13 and len(statpaths)==12)
delta=j(V/'Delta_integrala_Val04.json');ck('delta exact set',delta['changed_rows']==len(changed) and {x['path'] for x in delta['rows']}==changed and delta['new_identities']==0)
for e in events+static:
 p=R/e['source']['path'];buf=raw(p);ck('source OID '+e['path'],sha(p)==e['sha256']==e['source']['sha256'] and hashlib.sha1(b'blob '+str(len(buf)).encode()+b'\0'+buf).hexdigest()==e['git_oid']==rm[e['path']]['git_oid'])
 assert e['owner']==rm[e['path']]['owner'] and e['planned_peer']==rm[e['path']]['planned_peer']
ck('batch executors separate from dispatch owners',collections.Counter(e['actual_executor'] for e in events)=={'A08':2,'A05':9})
current={p for p,x in rm.items() if x['axis']['component_exercised']!='UNVERIFIED_R12'};previous={p for p,x in pm.items() if x['axis']['component_exercised']!='UNVERIFIED_R12'}
ck('39 previous partial retained, five new identities',len(previous)==39 and previous<=current and len(current)==44 and len(current-previous)==5)
idx=j(V/'Index_invers_surse_Val04.json');pairs={(x['path'],x['event_id']) for x in idx['rows']};forward={(p,e['event_id']) for p,x in rm.items() for e in x['current_evidence'] if 'event_id' in e}
for x in idx['legacy_Val01_pointer_resolution']:
 ev=resolve(x['event_source']);assert ev['path']==x['path'] and ev['event_id']==x['event_id'];oldproof=rm[x['path']]['current_evidence'][x['existing_forward_evidence_index']];assert all(oldproof[k]==v for k,v in x['existing_forward_proof'].items()) and ev['evidence']==x['existing_forward_proof'];forward.add((x['path'],x['event_id']))
ck('50 forward inverse pairs 44 paths',len(idx['rows'])==len(pairs)==50 and forward==pairs and {x[0] for x in pairs}==current)
for x in idx['rows']:
 e=resolve(x['event_source']);assert e['path']==x['path'] and e['event_id']==x['event_id'];y=rm[x['path']]
 assert (x['git_oid'],x['owner'],x['peer'],x['control'],x['pipelines'],x['tasks'])==(y['git_oid'],y['owner'],y['planned_peer'],y['control'],y['pipeline_candidates'],y['task_candidates'])
ck('forward inverse routing and nominal pointers',True)
metric=j(V/'Reconciliere_metrici_si_limite_Val04.json');groups=metric['current_exclusive_primary_levels'];claimed=set()
for k,x in groups.items():
 ck('exclusive metric '+k,x['count']==len(x['paths']) and not claimed&set(x['paths']));claimed.update(x['paths'])
ck('metric coverage set',claimed==current and metric['component_axis_distribution']==dict(collections.Counter(x['axis']['component_exercised'] for x in reg)))
ck('metric 33 original 5 comparator 2 type 4 binding', {k:x['count'] for k,x in groups.items()}=={'componenta_sau_traseu_metoda_originala':33,'comparator_shell':5,'tip_record':2,'fixture_binding_metadate':4})
ck('handoff metric equality',h['counts']==metric['counts'])
front=j(V/'Increment_01_frontend/Cazuri_frontend_10.json');native=j(V/'G3_checkpoint_nativ_Val04.json');nf=j(B/'A05_G3_nativ_lot04/Fise_G3_final_v1.json');nd=j(B/'A11/Val04_loturi/Verdict_A11_G3_nativ_lot04_v1.json');nm={x['path']:x for x in nd['source_dispositions']}
ck('native counts no inflation',native['counts']['protocol_scenarios']==10 and native['counts']['CASE_G3_lines']==16 and native['counts']['valid_readbacks']==41 and native['counts']['initial_setup_readbacks']==1)
for e in native['runtime_events']:
 assert e['path'] in nm and e['git_oid']==nm[e['path']]['oid'] and e['owner']==rm[e['path']]['owner']
ck('native nine event roles align A11',len(native['runtime_events'])==9 and len(native['static_only_rows'])==4)
for e in native['static_only_rows']:assert e['path'] in nm and nm[e['path']]['authoritative_state']=='STATIC_ONLY_NO_EXECUTION_CREDIT'
ck('static native has no runtime credit',True)
hist=j(V/'Conservare_652_fise_2619_criterii_Val04.json')
for x in hist['all_dossiers_rehashed']:resolve(x['dossier']);assert x['no_current_credit_transferred']
ck('652 dossiers 2619 criteria no transfer',len(hist['all_dossiers_rehashed'])==652 and sum(x['criteria_count_as_historic'] for x in hist['all_dossiers_rehashed'])==2619 and hist['current_new_credit']==0)
matrix=j(V/'Matrice_taskuri_criterii_R12_Val04.json');states={}
for x in matrix['current_rows']:
 t=resolve(x['source']);assert t['id']==x['alias'] and x['current_state']==t['stare_generala'] and x['progress_declared']==t.get('procent');states[x['alias']]=x['current_state']
ck('five frozen current task states',len(states)==5 and matrix['historic_criteria_newly_accepted']==0 and matrix['all17_contracts_open'])
ck('116 R11 references only',all(x['R11_reference_only'] is None or x['R11_reference_only']['credit_transferred'] is False for x in reg) and h['counts']['R11_reference_only']==116)
zones=j(V/'Checklist_10_zone_Val04.json');ck('ten owners and seventeen contracts',len(zones['rows'])==len({x['owner'] for x in zones['rows']})==10 and len(zones['contracts'])==17)
for z in zones['rows']:assert z['assigned_files']==sum(x['owner']==z['owner'] for x in reg) and z['whole_acceptances']==0
resources=j(V/'Resurse_si_restituire_Val04.json');ret=resources['prior_six_retained_roots']['retained_after_auto_review'];ck('six denied roots preserved',ret['count']==len(set(ret['roots']))==6 and resources['global_cleanup_not_claimed'])
O.mkdir(exist_ok=True);qa=O/'QA_A11_R12_Val04_registru_v1.json';write(qa,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'reference_instances':len(refs),'unique_reference_paths':len({x['path'] for x in refs}),'changed_rows':len(changed),'state_projection':states,'metric_groups':{k:x['count'] for k,x in groups.items()},'product_executions':0})
print(json.dumps({'QA':ref(qa),'checks':len(checks),'states':states,'metric_groups':{k:x['count'] for k,x in groups.items()}},ensure_ascii=False))
