import pathlib,json,hashlib,gzip,datetime,collections,functools
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';V=B/'A12/Val_03';O=B/'A11/Val03_registru';O.mkdir(exist_ok=True)
@functools.lru_cache(None)
def raw(p):return pathlib.Path(p).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def rows(p):return [json.loads(x) for x in gzip.decompress(raw(p)).decode('utf8').splitlines() if x]
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
checks=[];refs=[]
def ck(name,b,detail=None):
 checks.append({'check':name,'ok':bool(b),'detail':detail})
 if not b:raise AssertionError((name,detail))
def resolve(x):
 p=pathlib.Path(x['path']);p=p if p.is_absolute() else R/p
 assert sha(p)==x['sha256'],x
 if 'bytes' in x:assert len(raw(p))==x['bytes'],x
 z=j(p) if 'pointer' in x else None
 if 'pointer' in x and x['pointer'] not in ('','/'):
  for part in x['pointer'].strip('/').split('/'):
   key=part.replace('~1','/').replace('~0','~');z=z[int(key)] if isinstance(z,list) else z[key]
 return z
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and 'sha256' in x and (x['path'].startswith('executie/') or pathlib.Path(x['path']).is_absolute()):resolve(x);refs.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=V/'MANIFEST_R12_Val03.json';hp=V/'Handoff_R12_Val03.json';ck('manifest fixed',sha(mp)=='5f80d3973e34be94ce12aafdea307eec43aca359b42f2a0042c740e6c9db9a23');ck('handoff fixed',sha(hp)=='b3845967556f029921617297e3e38913d27d3954f82cfbd12f5f4325412e2958')
m=j(mp);h=j(hp);walk(m)
ck('manifest25outputs30inputreferences29distinct',len(m['files'])==len({x['path'] for x in m['files']})==25 and len(m['inputs'])==30 and len({x['path'] for x in m['inputs']})==29)
for e in m['files']:
 if e['path'].endswith('.json'):walk(j(R/e['path']))
reg=rows(V/'Registru_6728_R12_Val03.jsonl.gz');prev=rows(B/'A12/Val_02/Registru_6728_R12_Val02.jsonl.gz');dispatch=rows(R/'executie/R12_plan_delta/Dispatch_tehnic_integral_R12.jsonl.gz');rm={x['path']:x for x in reg};pm={x['path']:x for x in prev};dm={x['path']:x for x in dispatch}
ck('6728 identical identities',len(reg)==len(rm)==len(dm)==6728 and rm.keys()==dm.keys()==pm.keys() and len({x['id'] for x in reg})==6728)
fields=[('id','id'),('git_oid','git_object'),('git_mode','mode'),('owner','owner'),('planned_peer','peer'),('control','control'),('pipeline_candidates','pipeline_candidates'),('task_candidates','task_candidates')]
for p,x in rm.items():
 for a,b in fields:assert x[a]==dm[p][b],(p,a)
 assert x['candidate']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
 assert x['R11_reference_only']==pm[p]['R11_reference_only']
 assert x['axis']['whole_file_acceptance'] is None and x['file_verdict'] is None and x['axis']['native_UI']=='UNVERIFIED_R12'
walk(reg);ck('routing8dimensions history and no whole/UI credit',True)
ev=j(V/'Evenimente_9_surse_si_2_lecturi.json');ne=j(V/'Evenimente_N05_17_si_29_lecturi.json');print('EVENT_KEYS',ev.keys(),ne.keys())
events=ev['rows']+ne['rows'];static=ev['static_support_only']+ne['static_only'];em={x['path']:x for x in events};sm={x['path']:x for x in static};changed={p for p in rm if rm[p]!=pm[p]}
current={p for p,x in rm.items() if x['axis']['component_exercised']!='UNVERIFIED_R12'};old={p for p,x in pm.items() if x['axis']['component_exercised']!='UNVERIFIED_R12'}
ck('26 new partial +31static exact57delta',len(events)==len(em)==26 and len(static)==len(sm)==31 and changed==set(em)|set(sm) and not set(em)&set(sm))
ck('39 partial levels and13prior unchanged',len(current)==39 and len(old)==13 and not old&set(em) and current==old|set(em) and all(rm[p]==pm[p] for p in old))
for e in events+static:
 s=e['source'];p=R/s['path'];buf=raw(p);oid=hashlib.sha1(b'blob '+str(len(buf)).encode()+b'\0'+buf).hexdigest();assert oid==e['git_oid']==rm[e['path']]['git_oid'];assert sha(p)==e.get('sha256',s['sha256'])==s['sha256']
ck('57 sourceSHA/OID independent',True)
for p in sm:assert rm[p]['axis']['component_exercised']=='UNVERIFIED_R12'
ck('31readings unexercised',True)
ac=collections.Counter(rm[p]['axis']['component_exercised'] for p in current);print('AXES',dict(ac))
ck('levels exact',ac=={'OBSERVED_ONLY_AT_LINKED_SCOPE':13,'ORIGINAL_COMPONENT_PARTIAL':2,'SHELL_COMPARATOR_PARTIAL':5,'SQL_COMPARATOR_PARTIAL':2,'NATIVE_BUSINESS_METHOD_PARTIAL':11,'NATIVE_TRANSITIVE_VALUE_TYPE_USE':2,'NATIVE_FIXTURE_OR_BINDING_PARTIAL':4})
native_receipt=j(B/'A11/Val03_loturi/Matrice_A11_N05_sursee_v1.json');nm={x['path']:x for x in native_receipt['files']}
for e in ne['rows']+ne['static_only']:
 a=nm[e['path']];assert e['git_oid']==a['oid'] and e.get('sha256',e['source']['sha256'])==a['sha256']
 if e['path'] in em:
  assert e['phase']==a['phase'] and e['methods_in_scope']==a['methods'];assert not e['whole_file_accepted'] and not e['task_closed'];assert resolve(e['producer_dossier'])['path']==e['path']
ck('46N05 dispositions align independent matrix',True)
idx=j(V/'Index_invers_surse_Val03.json')['rows'];ck('39inverse unique',len(idx)==len({x['path'] for x in idx})==39 and {x['path'] for x in idx}==current)
for x in idx:
 y=rm[x['path']];e=resolve(x['event_source']);assert e['path']==x['path'] and e['event_id']==x['event_id'];assert (x['git_oid'],x['owner'],x['peer'],x['control'],x['pipelines'],x['tasks'])==(y['git_oid'],y['owner'],y['planned_peer'],y['control'],y['pipeline_candidates'],y['task_candidates'])
ck('forward inverse metadata exact',True)
cases=j(V/'Cazuri_nominale_121.json')['rows'];ck('121 unique 36+73+12',len(cases)==len({x['id'] for x in cases})==121 and collections.Counter(x['id'].split(':')[0] for x in cases)=={'A06':36,'A10':73,'G3':12})
print('CASE_FIELDS',cases[0].keys(),cases[-1].keys())
for c in cases:
 r=resolve(c['source']) if 'pointer' in c['source'] else j(R/c['source']['path']);expected_raw=r['two_sql_results'] if c['id'].startswith('G3:') else r
 assert expected_raw==c['observed'],c['id'];assert not c['whole_criterion_credit']
ck('121raw result pointers',True)
nc=j(V/'Cazuri_N05_7_scenarii.json');print('NATIVE_CASE_KEYS',nc.keys());ck('7native cases',len(nc['rows'])==len({x['id'] for x in nc['rows']})==7)
cons=j(V/'Conservare_652_fise_2619_criterii.json');print('CONS_KEYS',cons.keys())
for x in cons['all_dossiers_rehashed']:
 assert sha(R/x['dossier']['path'])==x['dossier']['sha256'];assert x['no_current_credit_transferred']
ck('652actual dossiers rehash',len(cons['all_dossiers_rehashed'])==652 and cons['tasks']==652 and cons['criteria']==2619)
historical=rows(R/'executie/R11_fisiere/A12/Val_04/Registru_6709_val_04.jsonl.gz');ck('116history no transfer',sum(x['axis']['exercised']=='OBSERVED_ONLY_AT_LINKED_SCOPE' for x in historical)==116 and all(x['R11_reference_only'] is None or x['R11_reference_only']['credit_transferred'] is False for x in reg))
mat=j(V/'Matrice_taskuri_criterii_R12_Val03.json');ck('nohistoric criteria accepted',mat['historic_criteria_newly_accepted']==0 and mat['all17_contracts_open'])
crit=j(V/'N05_Matrice_4_criterii_istorice.json');ck('4historic criteria observations only',len(crit['rows'])==4 and crit['criteria_added']==0 and crit['criteria_closed']==0 and not crit['supersedes_historical_dossier'])
for c in crit['rows']:
 orig=resolve(c['historical_source']);assert not c['criterion_integrally_accepted'];print('CRITERION',c['criterion_id'],c['new_observation_status'])
resources=j(V/'Resurse_si_restituire_Val03.json');print('RESOURCES',resources)
states=[]
for x in mat['current_rows']:
 orig=resolve(x['original_row']);states.append({'task':x['alias'],'base_matrix':x['current_state'],'authoritative_stare_generala':orig['stare_generala']})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':h['head'],'manifest':ref(mp),'handoff':ref(hp),'checks':checks,'reference_instances':len(refs),'distinct_reference_paths':len({x['path'] for x in refs}),'identity_dimensions':8,'technical_identities':6728,'source_levels':dict(ac),'prior_partial_sources':13,'new_partial_sources':26,'static_sources':31,'changed_evidence_rows':57,'cases':{'helper_SQL_identities':121,'native_scenarios':7,'no_total_PASS_sum':True},'states_need_additive_correction':states,'status':'INDEPENDENT_CHECKS_COMPLETE_EXCEPT_REQUIRED_STATE_ADDENDUM','product_executions':0}
p=O/'Control_A11_Val03_registru_baza_v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('OUTPUT',json.dumps(ref(p)),len(checks),len(refs))
