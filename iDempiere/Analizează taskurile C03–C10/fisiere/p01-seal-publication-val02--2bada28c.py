from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/Publicare_R12_Val02/Final_2026-11-03T00-17-56Z'
Q=R/'executie/Publicare_R12_Val02/QA_2026-11-03T00-17-57Z/QA.json'
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
expected={
'executie/R12_fisiere/A11/Val02_registru/Verdict_A11_R12_Val02_registru_v1.json':'e7f7d03f5198ac40e204943b7b9e16453d19494ae1d2fa58d5bbce4a53b1f6b4',
'executie/R12_fisiere/A12/Val_02/MANIFEST_R12_Val02.json':'f169311d8a251f6f01cc47facdb20b74434a7afe0c9687c6792d587723decc5d',
'executie/R12_fisiere/A12/Val_02/Handoff_R12_Val02.json':'609fe44a4d91fe936d91480d8477b3babc21ec16f0725d97d9faf71d0334672d',
'executie/R12_fisiere/A11/Val02_loturi/Verdict_A11_loturi_Val02_v1.json':'8066bd2f33396d748693dcbe280826e9b73c1a2912935223c500f3afbe92a53f',
'executie/R12_fisiere/A11/Val02_loturi/Verdict_A11_A05_infrastructura_Val02_v1.json':'0394c3fe54710e905723d3c66faed4a222c1d21249b35efa5874c764af5079e8',
'executie/R12_fisiere/A11/Val02_registru/Checklist_A11_dupa_R12_Val02_v1.json':'d6b503999b979b6c330e9a604c708d315a9e0247ccea973cbcc379889a8c497c'}
assert all(sha(R/p)==s for p,s in expected.items())
q=rd(Q);assert q['passed']
for x in q['links']:assert sha(R/x['file'])==x['sha256']
resource=rd(O/'Control_resurse_final.json');assert not resource['owned_matching_processes'] and not resource['native_test_port_listeners']
assert resource['masini_scratch_exists']
visual={'utc':utc,'review':'Root inspected mobile and desktop main report screenshots and mobile views of three executor reports. Text is readable, no clipped page width; tabular content and source paths remain accessible.','qa_current':ref(Q),'earlier_QA':[ref(R/'executie/Publicare_R12_Val02/QA_2026-11-02T23-59-34Z/QA.json'),ref(R/'executie/Publicare_R12_Val02/QA_2026-11-02T23-58-59Z/QA.json')],'note':'Earlier QA failure for helper mobile layout is preserved; additive CSS-only views passed the rerun. No signed executor artifact was rewritten.'}
(O/'Verificare_vizuala.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2),encoding='utf-8')
names=['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json','Runda_12_stare.json']
for name in names[3:]:
 p=R/name;d=rd(p);d['latest_publication_QA']=ref(Q);d['latest_resource_check']=ref(O/'Control_resurse_final.json');d['latest_publication_manifest']=(O/'MANIFEST_PUBLICARE_FINAL.json').relative_to(R).as_posix();d['utc']=utc
 if name!='Runda_11_stare.json':
  assert d['last_independent_checkpoint']['counts']['current_partial_source_files']==13
  assert d['last_independent_checkpoint']['counts']['full_task_verdicts']==0
  assert d['external_dependency_indispensable'] is False
 if name=='Stare_continuare_audit.json':d['generated_utc']=utc
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
for name in names:shutil.copyfile(R/name,O/name)
for name in ['p01-publish-r12-val02.py','p01-publish-r12-val02-config.json','p01-seal-publication-val02.py','p01-r12-qa-val02.py']:
 shutil.copyfile(Path('D:/CodexWork')/name,O/name)
manifest={'utc':utc,'state':'R12 Val02 component and registry receipt; complete audit open','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','accepted_inputs':[ref(R/p) for p in expected],'qa':ref(Q),'public_files':[ref(R/n) for n in names],'snapshots_and_publication_sources':[ref(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='MANIFEST_PUBLICARE_FINAL.json'],'full_task_closures':0,'contracts_open':17,'next_action':'Use independent checklist; code/business native tests have priority, tools remain separate. Preserve all rounds. Read-only operations and synthetic clones.','retained_scratch':'D:/CodexWork/p01-r12-masini-dates; automatic cleanup rejected; no running service','external_dependency_indispensable':False}
m=O/'MANIFEST_PUBLICARE_FINAL.json';assert not m.exists();m.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(sha(R/x['path'])==x['sha256'] for x in manifest['snapshots_and_publication_sources'])
print(json.dumps({'manifest':str(m),'sha256':sha(m),'public_files':len(names),'verified_publication_artifacts':len(manifest['snapshots_and_publication_sources']),'qa_passed':True},ensure_ascii=False))
