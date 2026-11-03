import collections,gzip,hashlib,json,pathlib,shutil,subprocess
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';O=E/'R12_plan_delta';A=O/'A12';V=A/'v2';V.mkdir(exist_ok=True)
H='df85d33c1648ce2b2df130a60a05ef696e2e5480';BASE='2fe90ed3f128c33dff7cf9f8674e664a70679390'
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
def rgz(p):
 with gzip.open(p,'rt',encoding='utf-8') as f:return [json.loads(l) for l in f]
def save(p,d):
 assert not p.exists(),str(p);p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def wg(p,rows):
 assert not p.exists();raw=('\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in rows)+'\n').encode();p.write_bytes(gzip.compress(raw,mtime=0));return dict(ref(p),raw_sha256=sha(raw))
livep=E/'delta/2026-11-02T22-49-25-027Z/00_STATUS_TASKURI.json';live=load(livep);old=load(E/'R11_plan_delta/A12_registru_693_stari_alias_v2.json')['rows'];oldmap={r['technical']:r for r in old}
doc=load(A/'Documentatie_562_clasificare.json');changes=[];maps={};source_reads=[]
for i,row in enumerate(doc['rows']):
 p=row['path'];task='T315' if '/T315-' in p else ('T316' if '/T316-' in p else None)
 if not task:continue
 ti,tr=next((j,r) for j,r in enumerate(live) if r.get('proiect')=='P01' and r['id']==task)
 prior=oldmap[task];canonical=prior['canonical'];assert canonical in tr['denumire'] or canonical==tr.get('cod_capitol')
 owner,peer=('A07','A03') if task=='T315' else ('A06','A08')
 old_role={k:row[k] for k in ('task_group','task','owner','peer')}
 cmd=['ssh','-o','BatchMode=yes','saga-server@192.168.100.151',f"git -C /home/saga-server/Documents/EvA-Contab cat-file blob {row['delta']['new_oid']}"]
 proc=subprocess.run(cmd,capture_output=True,check=True);raw=proc.stdout
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['delta']['new_oid']
 sp=V/'Sources_lues'/pathlib.PurePosixPath(p);sp.parent.mkdir(parents=True,exist_ok=True);assert not sp.exists();sp.write_bytes(raw)
 sr=dict(ref(sp),source_path=p,git_object=row['delta']['new_oid'],method='git cat-file blob read-only',executed=False);source_reads.append(sr)
 tref={'technical':task,'canonical':canonical,'title_as_declared':tr['denumire'],'state_as_declared':tr['stare_generala'],'last_edit_as_declared':tr.get('ultima_actualizare'),'exact_finish_date_as_declared':tr.get('finalizat_la'),'aliases_from_previous_verified_mapping':prior['alias_declared'],'source':dict(ref(livep),pointer=f'/{ti}'),'in_historic_652':prior['in_R10'],'R12_task_closure_credit':None}
 row.update(task_group=task,task=tref,owner=owner,peer=peer,read_for_plan=True,source=sr)
 maps[p]=row
 changes.append({'path':p,'old':old_role,'new':{k:row[k] for k in ('task_group','task','owner','peer')},'reason':'Exact dossier name and live P01 registry; original fallback SHARED_REGISTRY was too broad. Documentation only, no promoted executable or execution credit.','source':sr})
assert len(changes)==4
doc['limitation']='Clasificare nominală de plan; 31 bloburi total citite și verificate (27 inițiale + patru decizii T315/T316). Niciun instrument executat. Cele 546 artefacte neexecutabile nu primesc verdict semantic global.'
save(V/'Documentatie_562_clasificare_v2.json',doc)
save(V/'Corectie_nominala_T315_T316.json',{'head':H,'prior_manifest':ref(O/'Manifest_A12_receptie_R12.json'),'changes':changes,'scope':'Only four documentation assignments corrected; previous artifacts retained. No change to 6709 technical identities or 19 new tools.','new_product_execution':0})
save(V/'Manifest_4_sources_documentare.json',{'head':H,'mode':'READ_ONLY_PLAN','rows':source_reads})
cat=rgz(O/'Catalog_Git_integral_per_fisier_R12.jsonl.gz')
for r in cat:
 if r['path'] in maps:
  d=maps[r['path']];r.update(primary=d['owner'],peer=d['peer'],task_group=d['task_group'],read_for_plan=True)
catref=wg(O/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz',cat)
forward=rgz(A/'Matrice_forward_index_R12.jsonl.gz')
for r in forward:
 if r['path'] in maps:
  d=maps[r['path']];r.update(owner=d['owner'],peer=d['peer'],owner_peer=[d['owner']+'|'+d['peer']],technical_task=[d['task_group']],canonical_direct=[d['task']['canonical']],source=dict(ref(V/'Documentatie_562_clasificare_v2.json'),pointer='/rows/'+str(doc['rows'].index(d))))
assert len(forward)==7274
dims=['owner','peer','owner_peer','technical_task','canonical_direct','canonical_via_relation','control','peer_control','pipeline','control_pipeline','audit_control','disposition']
def vals(r,dim):
 v=r[dim]
 if dim=='control_pipeline':return [x['control']+'|'+x['pipeline'] for x in v]
 return [v] if isinstance(v,str) else v
ix={dim:collections.defaultdict(list) for dim in dims}
for r in forward:
 for dim in dims:
  for v in sorted(set(vals(r,dim))):ix[dim][v].append(r['path'])
inverse=[{'dimension':d,'value':v,'paths':sorted(p),'count':len(p)} for d in dims for v,p in sorted(ix[d].items())]
fr=wg(V/'Matrice_forward_index_R12_v2.jsonl.gz',forward);ir=wg(V/'Index_invers_R12_v2.jsonl.gz',inverse)
qr={}
for dim in dims:
 a={(r['path'],v) for r in forward for v in vals(r,dim)};b={(p,r['value']) for r in inverse if r['dimension']==dim for p in r['paths']};assert a==b
 qr[dim]={'expected_pairs':len(a),'observed_pairs':len(b),'missing':0,'extra':0,'exact_equality':True}
save(V/'QA_index_invers_R12_v2.json',{'head':H,'forward':fr,'inverse':ir,'dimensions':qr,'issues':[],'product_tests':0,'quality_grade':None})
summary=load(A/'Rezumat_inventar_dispatch_R12.json');summary['counts']['source_blobs_read_for_plan']=31;summary['catalog']=catref;summary['documentary_classification']=ref(V/'Documentatie_562_clasificare_v2.json');summary['correction']=ref(V/'Corectie_nominala_T315_T316.json')
for r in summary['changed_task_groups']:
 if r['group']=='SHARED_REGISTRY':r['changed_paths']=3
for task,owner,peer in [('T315','A07','A03'),('T316','A06','A08')]:
 matches=[d for d in maps.values() if d['task_group']==task];summary['changed_task_groups'].append({'group':task,'task':matches[0]['task'],'changed_paths':len(matches),'new_technical':0,'owner':owner,'peer':peer})
summary['utc']=datetime.now(timezone.utc).isoformat();summary['forward']=fr;summary['inverse']=ir;summary['index_qa']=ref(V/'QA_index_invers_R12_v2.json');summary['previous_summary']=ref(A/'Rezumat_inventar_dispatch_R12.json');summary['state']='FINAL_INVENTORY_FOR_PLAN_REVIEW_NO_PRODUCT_EXECUTION'
save(V/'Rezumat_inventar_dispatch_R12_v2.json',summary)
shutil.copyfile(pathlib.Path('D:/CodexWork/a12_r12_correct_dossiers.py'),V/'build_correction.py')
files=sorted(p for p in V.rglob('*') if p.is_file())+[O/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz']
manifest={'utc':datetime.now(timezone.utc).isoformat(),'head':H,'base':BASE,'status':'FINAL_R12_INVENTORY_DISPATCH_PLAN_ONLY','previous_immutable_manifest':ref(O/'Manifest_A12_receptie_R12.json'),'authoritative':{'summary':ref(V/'Rezumat_inventar_dispatch_R12_v2.json'),'catalog':catref,'dispatch':ref(O/'Dispatch_tehnic_integral_R12.jsonl.gz'),'inverse':ir,'forward':fr,'documentation':ref(V/'Documentatie_562_clasificare_v2.json'),'fiches':ref(A/'Index_19_fise.json'),'controls':ref(A/'Controale_audit_R12_I01_I19.json')},'artifacts':[ref(p) for p in files],'zero_product_tests':True,'no_self_reference':True}
save(O/'Manifest_A12_receptie_R12_v2.json',manifest)
assert all(sha((B/x['path']).read_bytes())==x['sha256'] for x in manifest['artifacts'])
print(json.dumps({'manifest':ref(O/'Manifest_A12_receptie_R12_v2.json'),'summary':ref(V/'Rezumat_inventar_dispatch_R12_v2.json'),'catalog':catref,'inverse':ir,'qa':ref(V/'QA_index_invers_R12_v2.json'),'task_changes':[{'path':x['path'],'owner':x['new']['owner'],'task':x['new']['task']['canonical']} for x in changes]},ensure_ascii=False,indent=2))
