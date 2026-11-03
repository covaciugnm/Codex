import collections,gzip,hashlib,json,pathlib,shutil
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';O=E/'R12_plan_delta';A=O/'A12'
HEAD='df85d33c1648ce2b2df130a60a05ef696e2e5480';BASE='2fe90ed3f128c33dff7cf9f8674e664a70679390'
def sha(b):return hashlib.sha256(b).hexdigest()
REF_CACHE={}
def ref(p):
 if p not in REF_CACHE:
  b=p.read_bytes();REF_CACHE[p]={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 return dict(REF_CACHE[p])
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def readgz(p):
 with gzip.open(p,'rt',encoding='utf-8-sig') as f:return [json.loads(s) for s in f]
def save(p,d):
 assert not p.exists(),str(p);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def writegz(p,d):
 assert not p.exists(),str(p);b=('\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in d)+'\n').encode();p.write_bytes(gzip.compress(b,mtime=0));return dict(ref(p),raw_sha256=sha(b))
for name in ['a12_r12_inventory.py','a12_r12_index.py']:
 dest=A/name;assert not dest.exists();shutil.copyfile(pathlib.Path('D:/CodexWork')/name,dest)
rows=readgz(O/'Dispatch_tehnic_integral_R12.jsonl.gz');by={r['path']:r for r in rows}
docs=load(A/'Documentatie_562_clasificare.json')['rows'];doc_by={r['path']:r for r in docs}
oldmap=load(E/'R11_plan_delta/A12_registru_693_stari_alias_v2.json')['rows'];canonical={r['technical']:r['canonical'] for r in oldmap}
task_src=ref(E/'R11_plan_delta/A12_registru_693_stari_alias_v2.json')
fiches=load(A/'Index_19_fise.json')['rows'];audit_control={r['path_in_git']:f'R12-I{i:02}' for i,r in enumerate(sorted(fiches,key=lambda x:x['path_in_git']),1)}
controls=[]
for meta in sorted(fiches,key=lambda x:x['path_in_git']):
 f=load(B/meta['path']);cid=audit_control[meta['path_in_git']]
 controls.append({'id':cid,'meaning':'Control de audit, nu cod de task comercial','file':meta['path_in_git'],'file_plan':meta,'task':f['task'],'owner':f['assignment']['owner'],'peer':f['assignment']['peer'],'linked_existing_control':f['assignment']['control'],'pipeline_candidates':f['assignment']['pipeline_candidates'],'objective':f['objective'],'actor':f['actor'],'fixture':f['fixture'],'positive_oracle':f['expected_oracle'],'negative_or_mutant':f['negative_or_mutant'],'before_after_retry':f['before_after_retry'],'postcondition':f['postcondition'],'limit':f['boundary'],'state':'PLAN_ONLY_AWAITING_A11','observed':None})
save(A/'Controale_audit_R12_I01_I19.json',{'head':HEAD,'rows':controls,'no_execution':True,'score':None})
forward=[]
for path in sorted(set(by)|set(doc_by)):
 if path in by:
  r=by[path]; tasks=r.get('task_candidates',[]);c=[r['control']] if r.get('control') else [];pc=[r['peer_control']] if r.get('peer_control') else [];p=r.get('pipeline_candidates',[])
  row={'path':path,'technical':True,'file_id':r['id'],'git_object':r['git_object'],'mode':r['mode'],'owner':r['owner'],'peer':r['peer'],'technical_task':tasks,'canonical_direct':[canonical[t] for t in tasks if canonical.get(t)],'canonical_via_relation':[],'control':c,'peer_control':pc,'pipeline':p,'control_pipeline':[{'control':x,'pipeline':y,'status':'CANDIDATE_FROM_DISPATCH_NO_EXECUTION'} for x in c for y in p],'audit_control':[audit_control[path]] if path in audit_control else [],'disposition':r['review_state'],'source':dict(ref(O/'Dispatch_tehnic_integral_R12.jsonl.gz'),logical_key=path),'association_mode':r.get('association_mode'),'unresolved_task_tokens':[t for t in tasks if t not in canonical]}
 else:
  r=doc_by[path];t=r.get('task');tasks=[t['technical']] if t else []
  row={'path':path,'technical':False,'file_id':None,'git_object':r['delta']['new_oid'],'mode':r['delta']['new_mode'],'owner':r['owner'],'peer':r['peer'],'technical_task':tasks,'canonical_direct':[t['canonical']] if t and t['canonical'] else [],'canonical_via_relation':[],'control':[],'peer_control':[],'pipeline':[],'control_pipeline':[],'audit_control':[],'disposition':'DOCUMENTARY_REVIEW_PENDING_CONSUMER_DIRECTION','source':dict(ref(A/'Documentatie_562_clasificare.json'),pointer='/rows/'+str(docs.index(r))),'association_mode':'DOSSIER_CONTEXT_NOT_CRITERION_COVERAGE','unresolved_task_tokens':[]}
 row['owner_peer']=[row['owner']+'|'+row['peer']]
 row['R12_product_execution_credit']=None
 forward.append(row)
assert len(forward)==7274 and sum(r['technical'] for r in forward)==6728
dimensions=['owner','peer','owner_peer','technical_task','canonical_direct','canonical_via_relation','control','peer_control','pipeline','control_pipeline','audit_control','disposition']
def values(row,dim):
 v=row[dim]
 if dim=='control_pipeline':return [x['control']+'|'+x['pipeline'] for x in v]
 return [v] if isinstance(v,str) else v
indices={k:collections.defaultdict(list) for k in dimensions}
for row in forward:
 for dim in dimensions:
  for value in sorted(set(values(row,dim))):indices[dim][value].append(row['path'])
inverse=[{'dimension':dim,'value':value,'paths':sorted(paths),'count':len(paths)} for dim in dimensions for value,paths in sorted(indices[dim].items())]
forward_ref=writegz(A/'Matrice_forward_index_R12.jsonl.gz',forward)
inverse_ref=writegz(A/'Index_invers_R12.jsonl.gz',inverse)
loaded_f=readgz(A/'Matrice_forward_index_R12.jsonl.gz');loaded_i=readgz(A/'Index_invers_R12.jsonl.gz')
qa_dims={}
for dim in dimensions:
 expected={(r['path'],key) for r in loaded_f for key in values(r,dim)}
 observed={(p,r['value']) for r in loaded_i if r['dimension']==dim for p in r['paths']}
 assert expected==observed,(dim,len(expected-observed),len(observed-expected))
 qa_dims[dim]={'expected_pairs':len(expected),'observed_pairs':len(observed),'missing':0,'extra':0,'exact_equality':True}
assert set(r['path'] for r in loaded_f if r['technical'])==set(by)
assert set(r['path'] for r in loaded_f)==set(by)|set(doc_by)
assert all(r['owner']!=r['peer'] for r in loaded_f)
assert len({r['audit_control'][0] for r in loaded_f if r['audit_control']})==19
save(A/'QA_index_invers_R12.json',{'utc':datetime.now(timezone.utc).isoformat(),'head':HEAD,'forward':forward_ref,'inverse':inverse_ref,'dimensions':qa_dims,'counts':{'technical':6728,'delta':565,'delta_documentary_not_technical':546,'union_paths':7274,'full_git_catalog_separate':183469,'new_audit_controls':19},'no_product_tests':True,'quality_grade':None,'issues':[]})
save(A/'Reception_index_R12.json',{'head':HEAD,'base':BASE,'status':'PLAN_ONLY_AWAITING_A11','inventory_manifest':ref(O/'Manifest_A12_inventar_dispatch_R12.json'),'forward':forward_ref,'inverse':inverse_ref,'qa':ref(A/'QA_index_invers_R12.json'),'audit_controls':ref(A/'Controale_audit_R12_I01_I19.json'),'canonical_mapping_source':task_src,'scope':'Indexul acoperă toate 6.728 fișiere tehnice și toate 565 delta, cu 546 documentare suplimentare distincte. Catalogul separat include toate cele 183.469 căi Git. Niciun task/control/pipeline nu primește acceptare din index.','candidate_semantics':'control_pipeline este relația planificată deja atribuită de dispatch; asocierea taskului candidată nu este cerință atomică demonstrată. canonical_via_relation rămâne gol: nu inventăm genealogie.','A11_val04_receipt':ref(E/'R11_fisiere/A11/Verdict_A11_R11_val04_v1.json'),'A11_checklist':ref(E/'R11_fisiere/A11/Checklist_A11_dupa_val04_v1.json'),'new_revision_no_automatic_credit':True,'limits':['546 documentare: actor/owner/peer atribuit, control și pipeline neconfirmate până la citire; nu fabricate','Nicio estimare de acoperire semantică; numai relații nominale numărate în QA','Cele 19 controale sunt audit R12-Ixx, nu taskuri P01 noi','Anexa A10 și planul director sunt suplimente independente de acest index']})
# Exact files and both earlier/final manifests remain outside their own digest calculation.
artifacts=[O/'Catalog_Git_integral_per_fisier_R12.jsonl.gz',O/'Dispatch_tehnic_integral_R12.jsonl.gz',O/'Manifest_A12_inventar_dispatch_R12.json']+sorted(p for p in A.rglob('*') if p.is_file())
manifest={'head':HEAD,'base':BASE,'utc':datetime.now(timezone.utc).isoformat(),'status':'FINAL_INVENTORY_DISPATCH_FOR_PLAN_REVIEW_ONLY','artifacts':[ref(p) for p in artifacts],'qa_inventory':ref(A/'QA_inventar_dispatch_R12.json'),'qa_inverse':ref(A/'QA_index_invers_R12.json'),'no_product_execution':True,'no_self_reference':True}
save(O/'Manifest_A12_receptie_R12.json',manifest)
assert all(sha((B/x['path']).read_bytes())==x['sha256'] for x in manifest['artifacts'])
print(json.dumps({'manifest':ref(O/'Manifest_A12_receptie_R12.json'),'index':inverse_ref,'forward':forward_ref,'qa':ref(A/'QA_index_invers_R12.json'),'pairs':qa_dims},ensure_ascii=False,indent=2))
