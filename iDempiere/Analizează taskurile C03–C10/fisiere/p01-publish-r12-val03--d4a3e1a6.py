from pathlib import Path
import sys,json,hashlib,datetime,re,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
cfg=rd(Path(sys.argv[1]))
assert cfg['independent_lots_received'] and cfg['independent_register_received']
inputs={k:R/v['path'] for k,v in cfg['inputs'].items()}
for k,p in inputs.items():assert sha(p)==cfg['inputs'][k]['sha256'],(k,p)
hd=rd(inputs['handoff']);assert hd['head']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
assert cfg['counts']==hd['counts']
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
out=R/'executie/Publicare_R12_Val03'/('Final_'+stamp);out.mkdir(parents=True,exist_ok=False)
names=['Raport_audit.html','Audit_C03.html','Audit_C10.html','Stare_continuare_audit.json','Runda_11_stare.json','Runda_12_stare.json']
for name in names:shutil.copyfile(R/name,out/('anterior_'+name))
block=Path(cfg['html_block']).read_text(encoding='utf-8')
assert 'id="r12-lot03"' in block and 'REPLACE_' not in block
for name in names[:3]:
 p=R/name;s=p.read_text(encoding='utf-8');assert '<!--r12-lot03-->' not in s
 marker='</header>' if name=='Raport_audit.html' else '<!--r12-lot02-->'
 assert marker in s
 injection='<!--r12-lot03-->'+block+'<!--end-r12-lot03-->'
 s=s.replace(marker,marker+injection if name=='Raport_audit.html' else injection+marker,1)
 s=re.sub(r'<small>Actualizat [^<]*</small>','<small>Actualizat '+utc+' · candidat GitHub auditat R12 df85d33c1648ce2b2df130a60a05ef696e2e5480 · captură Git/populație la 2026-11-03 00:39 UTC. HEAD al copiei de lucru de pe server: 1687cc8376902e7aa7163a883e07c7271bcae511; nu este candidatul executat.</small>',s)
 p.write_text(s,encoding='utf-8')
checkpoint={'utc':utc,'head':hd['head'],'verdict':inputs['verdict'].relative_to(R).as_posix(),'verdict_sha256':sha(inputs['verdict']),'verdict_ref':ref(inputs['verdict']),'manifest':ref(inputs['manifest']),'handoff':ref(inputs['handoff']),'state':cfg['state'],'counts':cfg['counts'],'whole_execution_grade':None,'product_grade':None,'open_full_contracts':cfg['open_contracts'],'current_revision_axes':cfg['axes'],'independent_receipts':{k:ref(p) for k,p in inputs.items() if 'verdict' in k}}
for name in names[3:]:
 p=R/name;d=rd(p);d['utc']=utc
 if name=='Runda_11_stare.json':d['next_candidate']={'head':hd['head'],'state':'Runda_12_stare.json','last_component_receipt':checkpoint}
 else:
  previous=d.get('last_independent_checkpoint')
  if previous:d.setdefault('previous_R12_checkpoints',[]).append(previous)
  d['last_independent_checkpoint']=checkpoint
  d['current_nominal_handoff']=ref(inputs['handoff']);d['next_review_checklist']=ref(inputs['checklist']);d['component_execution_counts']=cfg['counts'];d['execution_state']=cfg['state']
  d['product_tests_executed_meaning']=cfg['coverage_meaning'];d['next']=cfg['next'];d['latest_resources']=cfg['resources'];d['active_resources']=cfg['resources'];d['external_dependency_indispensable']=False
  d['latest_population_supplement']=ref(inputs['population_supplement']);d['latest_population_delta']=ref(inputs['population_delta']);d['publication_state']=cfg['state'];d['revision_boundary']=cfg['revision_boundary']
  d['latest_native_N05']=cfg['native_N05']
  if name=='Stare_continuare_audit.json':
   d['generated_utc']=utc;d['registry']={**ref(inputs['handoff']),'file':inputs['handoff'].relative_to(R).as_posix()}
   d['latest_tracker']=inputs['population_delta'].relative_to(R).as_posix();d['primary_hash_meaning']='Candidatul GitHub df85 verificat la captură și înghețat pentru probe; distinct de copia de lucru a serverului1687. Nu afirmă HEAD sau deploy după captură.'
   d.setdefault('current_best_view',{})['R12_nominal']=inputs['handoff'].relative_to(R).as_posix()
   d.setdefault('next_candidate',{})['execution_state']=cfg['state'];d['next_review']=cfg['next']
   d['next_round']={'round':12,'work_state':'Runda_12_stare.json','candidate_code':hd['head'],'plan_quality':10,'gate':d.get('gate'),'stage':cfg['state'],'A12_current':inputs['handoff'].relative_to(R).as_posix(),'full_execution_grade':None,'remaining_contracts':cfg['open_contracts']}
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'Predare_publicare.json').write_text(json.dumps({'utc':utc,'received':checkpoint,'inputs':{k:ref(p) for k,p in inputs.items()},'files_pending_final_QA':[ref(R/n) for n in names],'previous_snapshots':[ref(p) for p in out.glob('anterior_*')]},ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copyfile(Path(__file__),out/'publisher.py');shutil.copyfile(Path(sys.argv[1]),out/'config.json');shutil.copyfile(Path(cfg['html_block']),out/'section.html')
print(out)
