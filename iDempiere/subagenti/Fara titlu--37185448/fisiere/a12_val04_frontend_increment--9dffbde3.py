import collections,gzip,hashlib,json,pathlib
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');R=B/'executie/R12_fisiere';O=R/'A12/Val_04/Increment_01_frontend';P=R/'A12/Val_03';A=R/'A08_Storefront_catalog_lot04';S=R/'A08_Catalog_lectura_statica_lot04';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
MEM={};INPUTS=[];CHECKS=[];CACHE={}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return MEM[p.name] if p.parent==O and p.name in MEM else p.read_bytes()
def load(p):return json.loads(read(p).decode('utf-8-sig'))
def ref(p,pointer=None):
 b=read(p);d={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:d['pointer']=pointer
 return d
def put(n,x):
 assert n not in MEM and not (O/n).exists();MEM[n]=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode();return ref(O/n)
def refs(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:yield x
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
def resolve(p,s):
 q=pathlib.Path(s)
 if q.is_absolute():return q
 if s.startswith('executie/'):return B/q
 direct=p.parent/q
 if direct.exists() or (direct.parent==O and direct.name in MEM):return direct
 matches=[root/q for root in (A,S,R,B) if (root/q).exists()]
 assert len(matches)==1,('referinta nerezolvata/univoca',p,s,matches)
 return matches[0]
def point(d,p):
 for k in p.lstrip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def verify(p,expected=None):
 rr=ref(p)
 if expected:assert rr['sha256']==expected,p
 for r in refs(load(p)):
  q=resolve(p,r['path']);b=read(q);assert sha(b)==r['sha256'],q
  if 'bytes' in r:assert len(b)==r['bytes'],q
  if 'pointer' in r:point(load(q),r['pointer'])
  CHECKS.append(r)
 INPUTS.append(rr);return load(p)

verify(P/'MANIFEST_R12_Val03.json','5f80d3973e34be94ce12aafdea307eec43aca359b42f2a0042c740e6c9db9a23')
verify(P/'Handoff_R12_Val03_v2.json','58c7de3c525c69af3dd41799eed8e485f682e577233ea47f9acef3d7bda15dbb')
verify(R/'A11/Val03_registru/Verdict_A11_R12_Val03_registru_v1.json','e284136e81d919cb5b8b6dec6ea5ade3af24a59a60ad80e89b4226752a859114')
verify(R/'A12/Val_04/MANIFEST_preflight_Val04_0143.json','80d766c3c38cbcb925c4c9cc38cc660b12252da2f4bec15af42c5895d6c9199f')
verify(R/'A11/Val04_preflight/Verdict_A11_receptie_preflight_A12_0143_v1.json','dedbc15a0d3b58fc0ede5f9b277a3823cd1d472a9ac732109e7a05d0cd442a2d')
verify(A/'Handoff_A08_lot04_v1.json','c01caf69a1aa1c7c428a18ca38ff40e80bedef5eae3bb26d992f1947da212030')
for n in ['MANIFEST_A08_catalog_lot04_v1.json','MANIFEST_corectii_A08_v2.json','MANIFEST_lectura_A08_v3.json'] :verify(A/n)
vpath=R/'A11/Val04_loturi/Verdict_A11_catalog_lot04_v1.json';v=verify(vpath,'ef3cdaaa2b99a4ffd8bd8a636c2f7e7fc6903793fcd79cd87dee5dce2e8de5e9')
verify(R/'A11/Val04_loturi/Sigiliu_A11_catalog_lot04_v1.json','7a3d7fd6c607529922f7c9acec8d49ced7766fb119a6fbd2c10a36e3be859371')
verify(S/'SIGILIU_lectura_statica_v2.json','7d3c70215edb11730c365be4890d0543b1b94122b6e5502e53b75bfceb95a7b4')
verify(S/'MANIFEST_lectura_statica_v1.json')
sp=R/'A11/Val04_loturi/Peer_A11_catalog_lectura_statica_v2.json';sv=verify(sp,'15651cfd3f1729d93548f9a1933186b214c209714754dfe1aa4c2b433ae3d7dc')
with gzip.open(P/'Registru_6728_R12_Val03.jsonl.gz','rt',encoding='utf-8') as f:reg={x['path']:x for x in map(json.loads,f)}
assert len(reg)==6728
f=load(A/'Fise_7_cai_A08_v2.json');sr=load(S/'Raport_lectura_statica_v2.json');report=load(A/'Raport_A08_catalog_lot04_v2.json');runp=A/'Run_2026-11-03T02-00-34Z/Rezultate.json';run=load(runp)
assert run['executed_blobs']==1 and run['script_path_identities']==2 and len(run['cases'])==10
assert run['script_modified'] is False and v['counts']['executor_case_identities']==10
verify(runp);verify(runp.parent/'MANIFEST_RUN.json')
cases=[]
for i,c in enumerate(run['cases']):
 assert c['id'] not in [x['producer_id'] for x in cases]
 cases.append({'case_id':'R12V04-A08-'+c['id'],'producer_id':c['id'],'source':ref(runp,'/cases/'+str(i)),'oracle_literal':c['oracle'],'action':c['action'],'observed_status':c['status'],'observed':{'requests':c['requests'],'snapshots':c['snapshots'],'page_errors':c['page_errors']},'method':'Script original nemodificat, DOM sintetic și răspunsuri HTTP locale controlate; fără API/ERP real.','actor':'Vizitator public sintetic, fără autentificare.','independent_receipt':ref(vpath),'acceptance_limit':'Oracolul negativ poate respinge starea măsurată fără a defini suficient o remediere completă. Pentru N04/N05 se cere explicit ultimul filtru = cererea = produsele sau refuz vizibil coerent; negarea unei singure stări rele nu este suficientă.','whole_criterion_accepted':False})
cref=put('Cazuri_frontend_10.json',{'head':H,'rows':cases,'executor_cases':10,'independent_A11_witnesses_separate':5,'path_multiplication_forbidden':True,'no_product_execution_by_A12':True})
events=[];static=[]
for i,s in enumerate(f):
 path=s['path'];d=reg[path];p=A/'Sources'/path;b=read(p)
 assert d['git_oid']==s['git_oid']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() and sha(b)==s['sha256']
 assert d['planned_peer']==s['peer_catalog']=='A06'
 j=next(j for j,z in enumerate(v['source_dispositions']) if z['path']==path)
 assert v['source_dispositions'][j]['oid']==s['git_oid']
 common={'path':path,'git_oid':s['git_oid'],'sha256':s['sha256'],'source':ref(p),'owner':d['owner'],'planned_peer':d['planned_peer'],'control':d['control'],'pipeline_candidates':d['pipeline_candidates'],'task_candidates_preserved':d['task_candidates'],'task_mapping':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','producer_sheet':ref(A/'Fise_7_cai_A08_v2.json','/'+str(i)),'actual_executor':'A08','independent_receipt':ref(vpath,'/source_dispositions/'+str(j)),'planned_peer_performed_not_inferred':True,'functional_controls':['A08-P02','A08-C19','D10'],'provenance_only':['A08-C27'],'not_executed':['A08-P07'],'whole_file_accepted':False,'task_closed':False}
 if s['role']=='original_component_to_execute':
  common.update(event_id='R12V04-A08-CATALOG-'+str(len(events)+1),method_kind='ORIGINAL_JS_METHODS_SYNTHETIC_DOM_ONE_SHARED_BLOB',actor=s['actor'],requirement=s['requirement'],entry_point=s['normal_route'],native_reuse='Adaptarea funcției de catalog existente și a contractului API; niciun motor paralel propus.',positive_case_ids=s['positive_cases'],counterexample_case_ids=s['counterexample_cases'],effect='Numai DOM și stare JS efemeră; fără persistență ERP/DB.',limits=v['limits'],cases=cref,case_links=[ref(O/'Cazuri_frontend_10.json','/rows/'+str(j)) for j in range(10)],execution_group='R12V04-A08-BLOB-b901bec7b36c35589c4040d82586f2681db9d7e0',case_count_shared_not_additive=10)
  events.append(common)
 else:
  common.update(scope='STATIC_ROUTE_CONTEXT_ONLY',execution_credit=False,reading_limit=s['reading_limit'],normal_path=s['normal_route']);static.append(common)
for i,s in enumerate(sr['entries']):
 path=s['path'];d=reg[path];p=S/'Sources'/path;b=read(p)
 assert d['git_oid']==s['git_oid']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() and sha(b)==s['sha256']
 j=next(j for j,z in enumerate(sv['source_dispositions']) if z['path']==path)
 static.append({'path':path,'git_oid':s['git_oid'],'sha256':s['sha256'],'source':ref(p),'owner':d['owner'],'planned_peer':d['planned_peer'],'control':d['control'],'pipeline_candidates':d['pipeline_candidates'],'task_candidates_preserved':d['task_candidates'],'task_mapping':s['task'],'scope':'BOUNDED_STATIC_SUPPORT_ONLY','read_ranges':s['intervale_citite'],'whole_source_read':s['fisier_integral_citit'],'observation':s['observatie'],'requirement':s['cerinta'],'normal_path':s['cale_normala'],'limits':s['limite'],'producer_sheet':ref(S/'Raport_lectura_statica_v2.json','/entries/'+str(i)),'actual_reader':'root/A08','independent_receipt':ref(sp,'/source_dispositions/'+str(j)),'planned_peer_performed_not_inferred':True,'execution_credit':False,'whole_file_accepted':False})
assert len(events)==2 and len({x['git_oid'] for x in events})==1 and len(static)==9 and len({x['path'] for x in static})==8
er=put('Evenimente_frontend_2_cai_un_blob.json',{'head':H,'rows':events,'executor_cases':10,'unique_original_blobs_exercised':1,'path_identities':2,'case_multiplication_forbidden':True,'independent_component_witnesses_separate':5,'no_UI_ZK_API_ERP_DB_acceptance':True})
st=put('Lecturi_statice_9_asocieri_8_cai.json',{'head':H,'rows':static,'associations':9,'distinct_paths':8,'overlap':'WebshopServlet are context de traseu A08 și lectură punctuală separată; o singură identitate de cale.','hypothesis':sr['ipoteza'],'independent_static_peer':ref(sp),'confirmed_runtime_findings':0,'execution_credit':0})
findings=[]
for i,x in enumerate(report['findings']):
 j=next(j for j,y in enumerate(v['dispositions']) if y['finding']==x['id'])
 findings.append({'id':x['id'],'producer':ref(A/'Raport_A08_catalog_lot04_v2.json','/findings/'+str(i)),'original_observation':x,'effective_A11':v['dispositions'][j],'independent_receipt':ref(vpath,'/dispositions/'+str(j)),'distinct_mechanism_not_per_file':True,'whole_task_acceptance':False,'counterexample_is_not_a_pass':True})
put('Constatari_frontend_calificate.json',{'rows':findings,'mechanisms':3,'two_paths_do_not_double_findings':True,'scope':'Componente JS în condițiile declarate; erorile simulate nu probează defecte backend.','fix_acceptance_requirements':v['required_next_tests'],'score':None})
put('Checkpoint_increment_frontend.json',{'utc':datetime.now(timezone.utc).isoformat(),'head':H,'status':'LOT RECEPȚIONAT LIMITAT; REGISTRUL FINAL VAL04 AȘTEAPTĂ G3 ȘI RECEPȚIA SA','events':er,'static':st,'cases':cref,'frontend_receipt':ref(vpath),'static_receipt':ref(sp),'resources':{'executor':report['resources'],'A11':v['resources'],'A12_product_tests':0,'six_retained_roots_untouched':True},'historic_cohort_unchanged':[652,2619],'technical_identities_unchanged':6728,'full_file_or_task_acceptances':0,'contracts_open':17,'score':None})
put('build_increment_frontend.py.reference.json',{'local_source':'D:/CodexWork/a12_val04_frontend_increment.py','sha256':sha(pathlib.Path(__file__).read_bytes()),'purpose':'Construcție și verificare de documente; fără execuții de produs.'})
MEM['build_increment_frontend.py']=pathlib.Path(__file__).read_bytes()
checked=0
for n in list(MEM):
 if not n.endswith('.json'):continue
 for rr in refs(load(O/n)):
  if rr['path'] in reg:
   assert rr.get('git_oid')==reg[rr['path']]['git_oid']
   assert 'source' in rr and rr['source']['sha256']==rr['sha256']
   checked+=1;continue
  p=resolve(O/n,rr['path']);assert sha(read(p))==rr['sha256'],p
  if 'pointer' in rr:point(load(p),rr['pointer'])
  checked+=1
put('QA_increment_frontend.json',{'utc':datetime.now(timezone.utc).isoformat(),'references_checked':checked,'input_reference_instances_rehashed':len(CHECKS),'verified_source_associations':11,'verified_unique_source_paths':10,'runtime_path_identities':2,'runtime_blobs':1,'executor_case_identities':10,'static_associations':9,'static_unique_paths':8,'issues':[],'score':None})
put('MANIFEST_increment_frontend.json',{'utc':datetime.now(timezone.utc).isoformat(),'head':H,'files':[ref(O/n) for n in sorted(MEM)],'inputs':INPUTS,'not_final_Val04_registry':True,'no_self_reference':True})
O.mkdir(parents=True,exist_ok=True)
for n,b in MEM.items():assert not (O/n).exists();(O/n).write_bytes(b)
for n,b in MEM.items():assert (O/n).read_bytes()==b
print(json.dumps({'manifest':ref(O/'MANIFEST_increment_frontend.json'),'checkpoint':ref(O/'Checkpoint_increment_frontend.json'),'event_paths':len(events),'static_paths':len({x['path'] for x in static}),'cases':10,'issues':[]},ensure_ascii=False))
