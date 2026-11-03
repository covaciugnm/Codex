import collections,gzip,hashlib,json,pathlib,shlex,subprocess
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');E=B/'executie';P=E/'R12_plan_delta';R=E/'R12_fisiere';O=R/'A12/Val_03';OLD=E/'delta/2026-11-02T23-39-09-646Z';NEW=E/'delta/2026-11-03T00-39-34-490Z';H='df85d33c1648ce2b2df130a60a05ef696e2e5480';S='1687cc8376902e7aa7163a883e07c7271bcae511'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p,pointer=None):
 b=p.read_bytes();r={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:r['pointer']=pointer
 return r
def save(p,x):
 assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def fhash(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
O.mkdir(parents=True,exist_ok=True)
commands=[]
for kind,args in [('named_tree_diff',['diff','--name-status',H+'..'+S]),('commit_metadata',['show','-s','--format=%H%n%T%n%P%n%aI%n%cI%n%s',H,S,'087b260117697895970a268fec6ccad4e1200e36']),('current_refs',['rev-parse','HEAD','refs/heads/master','refs/remotes/origin/master',H+'^{tree}'])]:
 command=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','saga-server@192.168.100.151',shlex.join(['git','-C','/home/saga-server/Documents/EvA-Contab']+args)]
 start=now();p=subprocess.run(command,capture_output=True,timeout=60);assert p.returncode==0,p.stderr.decode('utf-8','replace')
 commands.append({'kind':kind,'start':start,'end':now(),'command':command,'exit':p.returncode,'stdout':p.stdout.decode('utf-8','strict'),'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode('utf-8','strict'),'read_only':True})
diff=[]
for line in commands[0]['stdout'].splitlines():
 fields=line.split('\t');diff.append({'status':fields[0],'paths':fields[1:]})
git={'utc':now(),'candidate':H,'local_server_comparison_target':S,'commands':commands,'name_status_rows':diff,'counts':dict(collections.Counter(x['status'] for x in diff)),'method_limits':['Metadata and name-status only; no export or execution of1687 code.','Captured current refs are time-specific and different from the frozen df85 candidate. No ancestry/rebase inference from a shallow checkout.','No product test, checkout, reset, fetch or runtime mutation performed.']}
save(O/'Drift_server_metadata_0039.json',git)
a=load(OLD/'00_STATUS_TASKURI.json');b=load(NEW/'00_STATUS_TASKURI.json');ak={(r.get('proiect'),r['id']):(i,r) for i,r in enumerate(a)};bk={(r.get('proiect'),r['id']):(i,r) for i,r in enumerate(b)}
assert len(a)==len(b)==len(ak)==len(bk)==996 and set(ak)==set(bk)
changes=[];states=[]
for k,(i,x) in ak.items():
 j,y=bk[k];fs=[f for f in sorted(set(x)|set(y)) if x.get(f)!=y.get(f)]
 if fs:changes.append({'project':k[0],'id':k[1],'canonical':y.get('cod_capitol'),'old_pointer':'/'+str(i),'new_pointer':'/'+str(j),'before_state':x['stare_generala'],'after_state':y['stare_generala'],'changed_fields':fs,'values':[{'field':f,'before':x.get(f),'after':y.get(f),'before_sha256':fhash(x.get(f)),'after_sha256':fhash(y.get(f))} for f in fs]})
 if x.get('stare_generala')!=y.get('stare_generala'):states.append(k)
assert {(x['project'],x['id']) for x in changes}=={('P01','T240'),('P01','T343')} and not states
assert next(x for x in changes if x['id']=='T240')['changed_fields']==['observatii','ultima_actualizare']
assert next(x for x in changes if x['id']=='T343')['changed_fields']==['observatii','procent','ultima_actualizare']
delta_old=load(OLD/'Delta.json');delta_new=load(NEW/'Delta.json');capture_records=[]
for folder,d in [(OLD,delta_old),(NEW,delta_new)]:
 for r in d['files']:
  p=folder/r['name'];assert sha(p.read_bytes())==r['hash']
 capture_records.append({'capture':folder.name,'files':[ref(folder/r['name']) for r in d['files']],'capture_metadata':ref(folder/'Delta.json'),'github_master':d['github_master_at_capture'],'server_worktree_HEAD':d['server_worktree_head']})
assert delta_old['server_worktree_head']=='087b260117697895970a268fec6ccad4e1200e36' and delta_new['server_worktree_head']==S
assert delta_old['github_master_at_capture']==delta_new['github_master_at_capture']==H
aux=[]
for r in delta_new['files']:
 name=r['name']
 if name=='00_STATUS_TASKURI.json':continue
 eq=load(OLD/name)==load(NEW/name);beq=(OLD/name).read_bytes()==(NEW/name).read_bytes();assert eq and beq
 aux.append({'name':name,'before':ref(OLD/name),'after':ref(NEW/name),'semantic_equal':eq,'byte_equal':beq})
comp={'utc':now(),'comparison_base_capture':OLD.name,'current_capture':NEW.name,'old':ref(OLD/'00_STATUS_TASKURI.json'),'new':ref(NEW/'00_STATUS_TASKURI.json'),'comparison_key':['proiect','id'],'all':[996,996],'P01':[sum(r.get('proiect')=='P01' for r in a),sum(r.get('proiect')=='P01' for r in b)],'membership_added':[],'membership_removed':[],'state_changes':[],'changes':changes,'auxiliary_registries':aux,'github_master_at_both_captures':H,'server_worktree_heads':[delta_old['server_worktree_head'],S],'server_refs_separate_evidence':ref(O/'Drift_server_metadata_0039.json'),'generic_Delta_not_used_as_current_comparator':{'source':ref(NEW/'Delta.json'),'baseline_as_declared':delta_new['baseline'],'T352_new_final_vs_generic_base':True,'T352_new_final_vs_last_received_checkpoint':False},'historic_cohort_unchanged':{'tasks':652,'criteria':2619},'note':'Recomputed every field and member versus last received23:39 capture, not Nov1/Nov2initial. Dates absent remain undocumented; estimates and observations do not establish closure.'}
assert comp['P01']==[693,693];save(NEW/'Comparatie_ultimul_checkpoint.json',comp)
planp=P/'Plan_delta_R12_v2.json';plan=load(planp);gatep=P/'A11_verdict_plan_delta_R12_v2.json';gate=load(gatep)
assert sha(planp.read_bytes())=='4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276';assert sha(gatep.read_bytes())=='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4';assert plan['candidate']==H
focus_ids={'T355','T354','T331','T329','T330','T325','T366','T257','T58','T216','T343','T352','T240','T333','T326','T332','T341','T232'}
focus=[]
for alias in sorted(focus_ids):
 i,x=ak[('P01',alias)];j,y=bk[('P01',alias)];normative=['denumire','cod_capitol','capitol','descriere','cerere_proprietar','explicatii','documente_produse'];assert all(x.get(f)==y.get(f) for f in normative)
 focus.append({'alias':alias,'canonical':y.get('cod_capitol'),'state':y['stare_generala'],'before':ref(OLD/'00_STATUS_TASKURI.json','/'+str(i)),'after':ref(NEW/'00_STATUS_TASKURI.json','/'+str(j)),'normative_fields':[{'field':f,'equal':True,'value_sha256':fhash(y.get(f))} for f in normative],'all_fields_equal':x==y,'closure_date_inferred':None,'limit':'Equality of registry fields is not proof that every branch/worktree document or installed runtime is unchanged.'})
with gzip.open(P/'Dispatch_tehnic_integral_R12.jsonl.gz','rt',encoding='utf-8') as f:dispatch={r['path']:r for r in map(json.loads,f)}
tracep=E/'R11_fisiere/A05/Val_04/Raport_A05_native_Val04_v2.json';trace=load(tracep);assert trace['canonical_task']=='P01.C03.T0029' and trace['obligation']=='N05'
source_checks=[]
for i,r in enumerate(trace['source_trace']):
 path='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+r['file'];assert dispatch[path]['git_object']==r['oid'];p=B/r['source_artifact']['path'];assert sha(p.read_bytes())==r['source_artifact']['sha256']
 source_checks.append({'path':path,'fixed_R12_oid':r['oid'],'previous_reading_only':ref(tracep,'/source_trace/'+str(i)),'R12_execution_credit_from_this_comparison':0})
vp=R/'A11/Val03_preflight/Verdict_A11_aplicabilitate_R12_0039_v1.json';assert sha(vp.read_bytes())=='23e2a6d93d137c47cd81f6be930fbf67de4c26357a181d95f858af525e687824'
vs=list(vp.parent.glob('Sigiliu*.json'));assert len(vs)==1;assert sha(vs[0].read_bytes())=='62e6847c2dcd3eaa8595f082eb6092e7ed8c13d65f72a0e8439f796b48df5f1f'
comparison_source=ref(NEW/'Comparatie_ultimul_checkpoint.json')
checkp=R/'A11/Val02_loturi/Checklist_A11_dupa_loturi_Val02_v1.json';check=load(checkp)
areas=[{'area':'N05 WMS/BOM','owner':'A05','peer':'A03/A11','task':'T355','canonical':'P01.C03.T0029','required_route':'DialogNotaSetWms→AD_Process EVA_NotaSetWms→NotaSetWmsProces→ListaMaterialeWms→MPPProductBOM; PO.saveEx→ModelValidationEngine/EventManager→EvaNotaSetBomEvents','original_authority':ref(planp,'/priority_inherited/4'),'prior_native_mapping':ref(tracep),'latest_gate_action':ref(checkp,'/next_actions/1'),'unchanged_expected':'Serial and two concurrent transactions on the same recipe/version; quantity conservation before/after disassembly, rollback/retry and independent readback; G2 no duplicated accounting stock.','precondition':'Reconcile native build/schema/migrations and load exact candidate EVA handler/bundles; generic MProduct smoke is insufficient.','changed_claim_impact':'T343 lotB claim does not amend T355/BOM or close G1/G2/G3; T240 text claims do not prove native dialog.'},
 {'area':'DocAction / Fact_Acct','owner':'A03/A05','peer':'A04/A11','related_tasks':['T325','T329','T330','T366','T257','T58','T216'],'contract_sources':[ref(planp,'/remaining_contracts/'+str(i)) for i in [2,5,7,12,13,15]],'latest_gate_action':ref(checkp,'/next_actions/2'),'unchanged_expected':'Boxes and labor cost once in G1; no second accounting stock for reversible set; separate accounting schemes/currency, retry without duplicates, reversals and linked origin; full DocAction not a synthetic SQL substitute.','precondition':'Synthetic native clone, identified roles/client/org, open applicable period, identified schema/build and original methods.','changed_claim_impact':'T343 CO/IP authority conflict remains open; replacement of a tracker observation does not rescind the frozen CO|CO|CO oracle.'},
 {'area':'ZK / UX / normal access','owner':'A09/A08','peer':'A01/A11','related_tasks':['T240','T355','T333','T343'],'unassigned_application_source':'WSagaMasiniForm remains SHARED_NO_TASK_ASSIGNED','contract_sources':[ref(planp,'/remaining_contracts/0'),ref(planp,'/remaining_contracts/9'),ref(planp,'/remaining_contracts/16'),ref(planp,'/native_help_pipeline')],'latest_gate_action':ref(checkp,'/next_actions/3'),'unchanged_expected':'Real login/role and allowed/denied firm; native menu/form action with persistent effect; Mașini seven deadline fields through both editors, empty/valid/impossible, color and rollback; collector reports are not native UI proof.','new_T240_claim':'Text reaudit9/10 with one bis and29rows justified only by labels; no independent receipt of those rows, legal correctness, fixes or final L6.','limit':'The FNUASS statement is a quoted tracker claim only; no legal conclusion or proof on df85 is asserted. Disappearance of Mașini mention does not resolve its finding.'}]
sub={'schema':'eva.audit.r12.preflight0039/1','utc':now(),'candidate':H,'mode':'READ_ONLY_POPULATION_VERSION_CONTINUITY; NO_PRODUCT_EXECUTION','comparative_checkpoint':comparison_source,'captures':capture_records,'fixed_inventory':ref(P/'Manifest_A12_receptie_R12_v2.json'),'plan':ref(planp),'plan_gate':ref(gatep),'A11_independent_preflight':ref(vp),'A11_preflight_seal':ref(vs[0]),'population':{'total':996,'P01':693,'historic_completed_cohort':652,'historic_criteria':2619,'added_members':0,'removed_members':0,'changed_states':0,'changed_rows':2,'new_final_tasks_vs_last_received':0,'reopened_vs_last_received':0},'focus_requirement_equality':focus,'N05_source_identity_continuity':source_checks,'scope_impact':areas,
 'new_claims':[{'task':'T240','canonical':'P01.C14.T0001','classification':'DECLARED_REAUDIT_AND_FUTURE_REMEDIATION_NOT_ACCEPTED_CURRENT_CODE','claims':'9/10 text reaudit; D-240-119…121; RR87/88 future; officialL6 after integration','boundaries':'No state or normative requirement changed; no replacement/closure of Mașini from missing mention; no score transfer from9/10 to our audit.'},{'task':'T343','canonical':'P01.C10.T0025','classification':'DECLARED_OTHER_BRANCH_RESULT_NOT_ACCEPTED_CURRENT_CODE','claims':'t343-impl-b@2c5d3645a2d, copyd906cb0, LR1…5/X119resolved,55/55mutants,5/5UX,D-343-62; A10/A11stillrunning','boundaries':'Do not credit branch/copy results to df85, neither resolve prior findings nor infer accepted CO/IP amendment. Exact source/JAR, cases, origin and A11 receipt required.'}],
 'gate_applicability':{'A12_proposal':'APPLICABLE_ONLY_TO_PREVIOUSLY_APPROVED_FIXED_DF85_SCOPE_WITH_EXISTING_READINESS_GATES','A11_confirmation_already_received':ref(vp),'scope_or_population_plan_revision_required_for_df85':False,'server_local_HEAD1687_covered':False,'new_branch_claims_covered_as_accepted_implementation':False,'source_execution_condition':'Export/check every required source blob and candidate JAR from exact df85 identity; never compile/run the default server working tree1687 under a df85 label. Installed/native base has its own version identity and is not inferred from any Git ref.','native_readiness_condition':'Keep V02-N01 build/schema/migration reconciliation; LastBuildInfo placeholder and FailOnBuildDiffer=N do not establish compatibility. Enable original EVA handlers and verify them before N05.','normal_UI_condition':'Real authentication/role, client/org and native route needed; injected generic PO context has no RBAC/UI credit.','remaining_instruments':['R12-I01','R12-I04','R12-I10','R12-I14','R12-I15','R12-I16','R12-I17'],'instrument_condition':'Read-only or scratch-copy execution within approved contracts, exact source OID, destructive Git/file helpers confined to owned isolated copies.','T343_CO_IP':'CO|CO|CO remains until authoritative nominal amendment accepted; IP neither automatic PASS nor automatic defect.','full_contracts_still_open':17,'product_score':None},
 'versions':{'github_at_old_capture':H,'github_at_new_capture':H,'server_HEAD_at_old_capture':'087b260117697895970a268fec6ccad4e1200e36','server_HEAD_at_new_capture':S,'metadata_only_drift':ref(O/'Drift_server_metadata_0039.json'),'server_HEAD_never_asserted_equal_df85':True,'tree_or_ancestry_inference':'Only specified name-status diff and metadata; no automatic source export/test, no rebase inference.'},
 'history_and_resources':{'exact_completion_dates_absent':'Remain undocumented; no new date inferred from edit/estimate/progress or later observations.','past_wave_product_credit_changes':0,'A12_product_tests':0,'A12_processes_or_databases_started':0,'operational_writes':0,'previous_Masini_cleanup_limit':'Retained scratch after automatic review rejection; unchanged by this preflight.','previous_A05_state':'Stopped/portclosed/scratchremoved with retained native cache; no new laboratory touched.'}}
save(O/'Supliment_populatie_0039.json',sub)
# Perform continuity only after the new supplement, without rewriting earlier artifacts.
continuity=[]
for mp,expect,relative in [(R/'A12/Val_02/MANIFEST_R12_Val02.json','f169311d8a251f6f01cc47facdb20b74434a7afe0c9687c6792d587723decc5d',False),(R/'A11/Val02_registru/Sigiliu_A11_R12_Val02_registru_v1.json','a467fb0763d194b4f3f854f3d99ccfa49b8cb4059b1d3b370abb6c31c7122011',True),(vs[0],'62e6847c2dcd3eaa8595f082eb6092e7ed8c13d65f72a0e8439f796b48df5f1f',True)]:
 assert sha(mp.read_bytes())==expect;m=load(mp);verified=[]
 for rr in m['files']+([] if relative else m.get('inputs',[])):
  p=(B if str(rr['path']).startswith('executie/') or not relative else mp.parent)/rr['path'];assert sha(p.read_bytes())==rr['sha256'];verified.append(ref(p))
 continuity.append({'manifest_or_seal':ref(mp),'verified':verified,'count':len(verified),'all_hashes_match':True})
v2p=R/'A11/Val02_registru/Verdict_A11_R12_Val02_registru_v1.json';assert sha(v2p.read_bytes())=='e7f7d03f5198ac40e204943b7b9e16453d19494ae1d2fa58d5bbce4a53b1f6b4'
handoff=load(R/'A12/Val_02/Handoff_R12_Val02.json');qa=load(R/'A12/Val_02/QA_R12_Val02.json');assert qa['handoff']['sha256']==sha((R/'A12/Val_02/Handoff_R12_Val02.json').read_bytes());assert handoff['counts']['historic_tasks']==652 and handoff['counts']['historic_criteria']==2619 and handoff['counts']['current_partial_source_files']==13
save(O/'Continuitate_sigilii_Val02_dupa_preflight.json',{'utc':now(),'after_supplement':ref(O/'Supliment_populatie_0039.json'),'records':continuity,'A11_reception_authoritative':ref(v2p),'A12_pending_preserved_immutable':handoff['A11_wave_reception_pending'],'handoff_QA_SHA_compatible':True,'counts_preserved':handoff['counts'],'changes_to_prior_artifacts':0,'issues':[]})
def resolve(d,pointer):
 for t in pointer.lstrip('/').split('/') if pointer else []:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d
checks=set()
def scan(x):
 if isinstance(x,dict):
  if str(x.get('path','')).startswith('executie/') and 'sha256'in x:
   key=(x['path'],x['sha256'],x.get('pointer'))
   if key not in checks:
    p=B/x['path'];assert sha(p.read_bytes())==x['sha256'],str(p)
    if 'pointer'in x:resolve(load(p),x['pointer'])
    checks.add(key)
  for y in x.values():scan(y)
 elif isinstance(x,list):
  for y in x:scan(y)
for p in O.glob('*.json'):scan(load(p))
scan(comp)
save(O/'QA_preflight_0039.json',{'utc':now(),'comparison':comparison_source,'supplement':ref(O/'Supliment_populatie_0039.json'),'continuity':ref(O/'Continuitate_sigilii_Val02_dupa_preflight.json'),'nominal_rows_checked':996,'same_p01_population':693,'changed_rows':['T240','T343'],'state_changes':0,'normative_fields_of18_focus_tasks_unchanged':True,'six_auxiliary_registries_equal':True,'new_git_product_executions':0,'references_and_pointers_verified':len(checks),'issues':[],'quality_score':None})
(O/'build_preflight0039.py').write_bytes(pathlib.Path(__file__).read_bytes())
man={'utc':now(),'candidate':H,'kind':'PRE_EXECUTION_SUPPLEMENT_NOT_FULL_VAL03_AUDIT','files':[ref(p) for p in sorted(O.iterdir()) if p.is_file()],'external_output':comparison_source,'inputs':[ref(planp),ref(gatep),ref(vp),ref(vs[0]),ref(R/'A12/Val_02/MANIFEST_R12_Val02.json'),ref(v2p)],'no_self_reference':True,'no_test_coverage_added':True}
save(O/'MANIFEST_preflight_Val03_0039.json',man)
for r in man['files']+man['inputs']+[man['external_output']]:assert sha((B/r['path']).read_bytes())==r['sha256']
print(json.dumps({'comparison':comparison_source,'supplement':ref(O/'Supliment_populatie_0039.json'),'continuity':ref(O/'Continuitate_sigilii_Val02_dupa_preflight.json'),'manifest':ref(O/'MANIFEST_preflight_Val03_0039.json'),'drift_counts':git['counts'],'changes':[r['id'] for r in changes],'source_checks':len(source_checks),'references':len(checks)},ensure_ascii=False,indent=2))
