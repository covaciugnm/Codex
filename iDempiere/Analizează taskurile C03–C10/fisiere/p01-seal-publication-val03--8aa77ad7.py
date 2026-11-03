from pathlib import Path
import sys,json,hashlib,datetime,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=Path(sys.argv[1]);Q=Path(sys.argv[2]);cfg=json.loads(Path(sys.argv[3]).read_text(encoding='utf-8-sig'))
assert O.is_relative_to(R/'executie/Publicare_R12_Val03')
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
for k,x in cfg['inputs'].items():assert sha(R/x['path'])==x['sha256'],k
q=rd(Q);assert q['passed']
for x in q['links']:assert sha(R/x['file'])==x['sha256']
resource=rd(Path('D:/CodexWork/p01-r12-val03-resource-check.json'))
assert not resource['native_n05_lab_exists'] and not resource['listeners_56455'] and not resource['native_n05_java']
assert len(resource['retained_after_automatic_rejection'])==6
assert all(x['exists'] for x in resource['retained_after_automatic_rejection'])
shutil.copyfile(Path('D:/CodexWork/p01-r12-val03-resource-check.json'),O/'Control_resurse_final.json')
visual={'utc':utc,'review':'Root inspected new N05, SQL and A10 reading views and final main report screenshots. Document QA includes desktop/mobile, local links, duplicate IDs and existing C03/C10 task filtering. No product UI execution is implied.','qa_current':ref(Q),'earlier_reading_QA':[ref(R/p) for p in cfg['reading_qa']],'limits':'Screenshot samples and automated width/link checks do not certify every paragraph or product UX. All original signed reports retained.'}
(O/'Verificare_vizuala.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2),encoding='utf-8')
names=['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json','Runda_12_stare.json']
for name in names[3:]:
 p=R/name;d=rd(p);d['latest_publication_QA']=ref(Q);d['latest_resource_check']=ref(O/'Control_resurse_final.json');d['latest_publication_manifest']=(O/'MANIFEST_PUBLICARE_FINAL.json').relative_to(R).as_posix();d['utc']=utc
 if name!='Runda_11_stare.json':
  assert d['last_independent_checkpoint']['counts']==cfg['counts']
  assert d['external_dependency_indispensable'] is False
 if name=='Stare_continuare_audit.json':d['generated_utc']=utc
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for name in names:shutil.copyfile(R/name,O/name)
for name in ['p01-publish-r12-val03.py','p01-seal-publication-val03.py','p01-r12-qa-val03.py']:
 shutil.copyfile(Path('D:/CodexWork')/name,O/name)
manifest={'utc':utc,'state':cfg['state'],'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','accepted_inputs':cfg['inputs'],'qa':ref(Q),'public_files':[ref(R/n) for n in names],'snapshots_and_publication_sources':[ref(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='MANIFEST_PUBLICARE_FINAL.json'],'full_task_closures':0,'contracts_open':cfg['open_contracts'],'next_action':cfg['next'],'retained_scratch':resource['retained_after_automatic_rejection'],'external_dependency_indispensable':False}
m=O/'MANIFEST_PUBLICARE_FINAL.json';assert not m.exists();m.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
refs=manifest['public_files']+manifest['snapshots_and_publication_sources']+list(cfg['inputs'].values())+[manifest['qa']]
assert all(sha(R/x['path'])==x['sha256'] for x in refs)
print(json.dumps({'manifest':str(m),'sha256':sha(m),'public_files':len(names),'verified_refs':len(refs),'qa_passed':True},ensure_ascii=False))
