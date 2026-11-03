import json,pathlib,hashlib,gzip,datetime,functools
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';V=B/'A12/Val_04';O=B/'A11/Val04_preflight'
@functools.lru_cache(None)
def raw(p):return pathlib.Path(p).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf8-sig' if False else 'utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def vh(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
checks=[];refs=[];pointers=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'details':d});assert b,(n,d)
def resolve(x):
 p=pathlib.Path(x['path']);p=p if p.is_absolute() else R/p
 assert sha(p)==x['sha256'],x
 if 'bytes'in x:assert len(raw(p))==x['bytes'],x
 refs.append(x)
 if 'pointer' not in x:return None
 z=j(p)
 for k in x['pointer'].removeprefix('#').split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');z=z[int(k)] if isinstance(z,list) else z[k]
 pointers.append(x);return z
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:resolve(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=V/'MANIFEST_preflight_Val04_0143.json';sp=V/'Supliment_populatie_0143.json';hp=V/'Handoff_preflight_Val04_v1.json'
ck('fixed final manifest',sha(mp)=='80d766c3c38cbcb925c4c9cc38cc660b12252da2f4bec15af42c5895d6c9199f')
ck('fixed supplement',sha(sp)=='d1f2cddc17a71cce255175e4f0e8ee4168a8bedd0280b03a669e304712bb57fd')
ck('fixed handoff',sha(hp)=='fd5adca6125ce132ac16f8454bde2bc4686a191738fe1af42079a57fb1c95de2')
m=j(mp);walk(m)
for x in m['files']:
 if x['path'].endswith('.json'):walk(j(R/x['path']))
ck('11outputs14inputs all resolved',len(m['files'])==len({x['path'] for x in m['files']})==11 and len(m['inputs'])==14)
c=j(V/'Comparatie_996_randuri_existente.json');old=j(R/c['before']['path']);new=j(R/c['after']['path']);key=lambda x:(x.get('proiect'),x['id'])
ck('996common unique 997after',len(old)==996 and len(new)==997 and len(c['rows'])==996 and len({(x['project'],x['id']) for x in c['rows']})==996)
for x in c['rows']:
 a=old[int(x['before_pointer'][1:])];b=new[int(x['after_pointer'][1:])]
 assert key(a)==key(b)==(x['project'],x['id'])
 assert vh(a)==x['before_value_sha256'] and vh(b)==x['after_value_sha256']
 fs=[k for k in sorted(a.keys()|b.keys()) if (k in a)!=(k in b) or a.get(k)!=b.get(k)]
 assert fs==x['changed_fields'] and (a==b)==x['entire_row_equal']
 assert a['stare_generala']==b['stare_generala']==x['before_state']==x['after_state']
ck('996row hashes states pointers fields exact',True)
s=j(sp);f=s['focus_requirement_equality'];ck('18focus rows162predicates',len(f)==18 and sum(len(x['normative_fields']) for x in f)==162)
for x in f:
 a=resolve(x['before']);b=resolve(x['after']);assert a['id']==b['id']==x['alias'];assert b['stare_generala']==x['current_state']
 for n in x['normative_fields']:assert n['equal'] and a.get(n['field'])==b.get(n['field']) and vh(b.get(n['field']))==n['value_sha256']
 assert (a==b)==x['entire_row_including_observations_and_progress_equal'];assert x['new_execution_credit']==0
ck('focus predicates independently recomputed',True)
fi=j(V/'Fisa_intake_T386_v1.json');ck('T386 intake literal and canonical exact',resolve(fi['source'])==fi['source_literal'] and resolve(fi['correspondence'])==fi['correspondence_literal'] and fi['canonical']=='P01.C10.T0030' and fi['current_state']=='plan')
ck('T386 nohistory noexecution nocredit',not fi['in_historic_completed_cohort'] and fi['historic_task_count_change']==fi['historic_criteria_count_change']==fi['product_tests']==0 and fi['score'] is None and fi['completion_date'] is None)
dp=R/'executie/R12_plan_delta/Dispatch_tehnic_integral_R12.jsonl.gz';ds={x['path']:x for x in map(json.loads,gzip.decompress(raw(dp)).decode().splitlines())}
for x in fi['proposed_assignment']['existing_routes']:assert x==ds[x['path']]
ck('two routes unmodified A08peer retained',len(fi['proposed_assignment']['existing_routes'])==2 and fi['proposed_assignment']['peer']=='A08' and fi['proposed_assignment']['A11_domain_cross_review']==['A09','A02'])
z=j(V/'Dispozitii_10_zone_preflight_Val04.json');ck('10 zones noexecution',len(z['rows'])==10 and len({x['owner'] for x in z['rows']})==10 and all(x['new_executions']==0 and not x['peer_complete_inferred'] for x in z['rows']))
for x in z['rows']:
 p=resolve(x['previous']);assert x['assigned_files_unchanged']==p['assigned_files']
ck('zone assignedcounts preserved',True)
meta=j(V/'Metadate_Git_0143.json')
for x in meta['commands']:assert hashlib.sha256(x['stdout'].encode()).hexdigest()==x['stdout_sha256'];assert x['exit']==0 and x['read_only']
ck('git metadata command text hashes only',len(meta['commands'])==2)
out={'schema':'A11.R12.Val04.A12.preflight.receipt.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','method':'Read-only local metadata; all996 common rows and162normative predicates independently recomputed; all manifest/reference/pointers rehashed/resolved; no executor build script executed and no product test. Git command output is evidence supplied by A12, not repeated remote A11 execution.',
 'manifest':ref(mp),'supplement':ref(sp),'handoff':ref(hp),'checks':checks,'reference_instances_checked':len(refs),'pointer_instances_checked':len(pointers),'unique_reference_paths':len({x['path'] for x in refs}),
 'decision':'ACCEPTAT LIMITAT: recepție nominală a preflightului și intakeT386, nu recepție de implementare.',
 'dispositions':['Captura nouă997/694 și taskT386plan se adaugă nominal; cohorta652/2619 și dispatch6728 rămân distincte.','Toate996stările existente sunt egale; T240 observații/progres98/data sunt afirmații noi, nu dovezi de închidere/implementare la df85.','A08 rămâne peer planificat al fișierelor din dispatch; A09/A02 sunt cross-review de domeniu propus. Repartizarea nu este review efectuat.','Listele Rămase/Finalizate sunt vechi și neschimbate, deci intake-ul principalT386 este păstrat explicit.','Commit6354 există conform metadata read-only, dar nu este candidatul probelor și nu primește transfer de credit; GitHubdf85 și server8c0695de rămân identități separate.','Mențiunea alertă disc din subjectul commitului operațional nu este măsurare actuală A11 și nu autorizează curățare ori mutații operaționale. Laboratoarele locale au propriul preflight.','39=26+7+2+4 și116istorice R11 păstrează nivelurile;17contracte deschise;zero integral.','Înainte de noua execuție G3/frontend, protocolul concret și eventualele amendamente de oracol vor primi recepție separată.'],
 'resources':'Nicio resursă operațională, DB, browser sau proces de produs creat; cele6rădăcini cu ștergere refuzată rămân neatinse.','product_score':None,'audit_global_score':None,'operational_writes':0,'product_executions':0}
op=O/'Verdict_A11_receptie_preflight_A12_0143_v1.json';assert not op.exists();op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rp=O/'Runner_A11_receptie_preflight_A12_0143_v1.py';assert not rp.exists();rp.write_bytes(pathlib.Path(__file__).read_bytes())
seal=O/'SIGILIU_A11_receptie_preflight_A12_0143_v1.json';assert not seal.exists();seal.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(op),ref(rp)],'immutable':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'verdict':ref(op),'seal':ref(seal),'refs':len(refs),'pointers':len(pointers)},ensure_ascii=False))
