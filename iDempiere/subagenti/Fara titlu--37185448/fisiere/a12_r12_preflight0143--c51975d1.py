import collections,gzip,hashlib,html,json,pathlib,shlex,subprocess
from datetime import datetime,timezone

B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
E=B/'executie'; P=E/'R12_plan_delta'; R=E/'R12_fisiere'
O=R/'A12/Val_04'; PREV=R/'A12/Val_03'
OLD=E/'delta/2026-11-03T00-39-34-490Z'; NEW=E/'delta/2026-11-03T01-43-37-057Z'
H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
def now():return datetime.now(timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p,pointer=None):
    b=p.read_bytes();r={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
    if pointer is not None:r['pointer']=pointer
    return r
def save(p,x):
    assert not p.exists(),str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def fhash(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
def different_fields(a,b):return [k for k in sorted(set(a)|set(b)) if (k in a)!=(k in b) or a.get(k)!=b.get(k)]
def pointer(x,p):
    for k in p.removeprefix('#').split('/')[1:]:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
def find_refs(x):
    if isinstance(x,dict):
        if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:yield x
        for v in x.values():yield from find_refs(v)
    elif isinstance(x,list):
        for v in x:yield from find_refs(v)
def resolve(rr,origin):
    p=pathlib.Path(rr['path'])
    if p.is_absolute():return p
    if (B/p).exists():return B/p
    if (origin.parent/p).exists():return origin.parent/p
    raise AssertionError(('unresolved',origin,rr))

# Sources are read once; all new output is additive. No product program is run.
ad,bd=load(OLD/'Delta.json'),load(NEW/'Delta.json')
a,b=load(OLD/'00_STATUS_TASKURI.json'),load(NEW/'00_STATUS_TASKURI.json')
ak={(r.get('proiect'),r['id']):(i,r) for i,r in enumerate(a)}
bk={(r.get('proiect'),r['id']):(i,r) for i,r in enumerate(b)}
assert len(ak)==len(a)==996 and len(bk)==len(b)==997
assert set(bk)-set(ak)=={('P01','T386')} and not set(ak)-set(bk)
assert ad['github_master_at_capture']==bd['github_master_at_capture']==H
assert ad['server_worktree_head']=='1687cc8376902e7aa7163a883e07c7271bcae511'
assert bd['server_worktree_head']=='8c0695de36b50ede569c6d318715db0af11fcbff'
captures=[]
for folder,d in [(OLD,ad),(NEW,bd)]:
    files=[]
    for rr in d['files']:
        p=folder/rr['name'];r=ref(p);assert r['sha256']==rr['hash'],rr['name'];files.append(r)
    assert len(files)==7
    captures.append({'capture':folder.name,'metadata':ref(folder/'Delta.json'),'files':files,'github_master_at_capture':d['github_master_at_capture'],'server_worktree_HEAD_at_capture':d['server_worktree_head']})

changes=[];row_ledger=[];states=[];normchanges=[]
normative=['denumire','capitol','cod_capitol','descriere','cerere_proprietar','explicatii','documente_produse','decizii_deschise','fisier']
for key in sorted(set(ak)&set(bk)):
    i,x=ak[key];j,y=bk[key];fs=different_fields(x,y)
    row_ledger.append({'project':key[0],'id':key[1],'before_pointer':'/'+str(i),'after_pointer':'/'+str(j),'before_value_sha256':fhash(x),'after_value_sha256':fhash(y),'entire_row_equal':not fs,'changed_fields':fs,'state_source_field':'stare_generala','before_state':x.get('stare_generala'),'after_state':y.get('stare_generala')})
    if fs:changes.append({'project':key[0],'id':key[1],'canonical':y.get('cod_capitol'),'before':ref(OLD/'00_STATUS_TASKURI.json','/'+str(i)),'after':ref(NEW/'00_STATUS_TASKURI.json','/'+str(j)),'state_source_field':'stare_generala','before_state':x.get('stare_generala'),'after_state':y.get('stare_generala'),'changed_fields':fs,'values':[{'field':k,'before_present':k in x,'after_present':k in y,'before':x.get(k),'after':y.get(k)} for k in fs]})
    if x.get('stare_generala')!=y.get('stare_generala'):states.append(key)
    if set(fs)&set(normative):normchanges.append(key)
assert [x['id'] for x in changes]==['T240'] and changes[0]['changed_fields']==['observatii','procent','ultima_actualizare']
assert not states and not normchanges
assert ak[('P01','T352')][1]==bk[('P01','T352')][1]

aux=[];correspondence_add=[];corr_index=None
for rr in bd['files']:
    name=rr['name']
    if name=='00_STATUS_TASKURI.json':continue
    x,y=load(OLD/name),load(NEW/name)
    item={'name':name,'before':ref(OLD/name),'after':ref(NEW/name),'byte_equal':(OLD/name).read_bytes()==(NEW/name).read_bytes(),'semantic_equal':x==y}
    if name=='00_CORESPONDENTA_COD_CAPITOL.json':
        assert different_fields(x,y)==['coduri']
        xc={r['cod']:r for r in x['coduri']};yc={r['cod']:r for r in y['coduri']}
        assert len(xc)==len(x['coduri'])==353 and len(yc)==len(y['coduri'])==354
        assert set(yc)-set(xc)=={'P01.C10.T0030'} and not set(xc)-set(yc)
        assert all(xc[k]==yc[k] for k in xc)
        correspondence_add=[yc['P01.C10.T0030']]
        corr_index=next(i for i,r in enumerate(y['coduri']) if r['cod']=='P01.C10.T0030')
        item.update(added=correspondence_add,removed=[],existing_changes=[],counts=[353,354],added_source=ref(NEW/name,'/coduri/'+str(corr_index)))
    else:assert item['byte_equal'] and item['semantic_equal']
    if name in ['00_STATUS_RAMASE.json','00_STATUS_FINALIZATE.json']:
        # Exact equality proves no new T386 entry; recursively inspect IDs as well.
        def all_dicts(z):
            if isinstance(z,dict):
                yield z
                for v in z.values():yield from all_dicts(v)
            elif isinstance(z,list):
                for v in z:yield from all_dicts(v)
        ids=[r for r in all_dicts(y) if r.get('id')=='T386' or r.get('id_tehnic')=='T386' or r.get('cod_capitol')=='P01.C10.T0030']
        assert not ids
        item.update(T386_entries=0,interpretation='Derived registry unchanged. Absence of this new plan member is a snapshot synchronization gap, not proof of product deletion or a closed task.')
    aux.append(item)

manifest_expectations=[
 (PREV/'MANIFEST_R12_Val03.json','5f80d3973e34be94ce12aafdea307eec43aca359b42f2a0042c740e6c9db9a23'),
 (PREV/'MANIFEST_lectura_finala_Val03_v1.json','1b40caa6b7587badc3e304467ad0a4386c5a3f725f4c4b9c3f0efd107b530dfe'),
 (PREV/'SIGILIU_supliment_stari_Val03_v1.json','2a0c42fd6bc8ea2e11458a49792259c7f92c82a77e6217e997c343064a7dd38c'),
 (PREV/'Handoff_R12_Val03_v2.json','58c7de3c525c69af3dd41799eed8e485f682e577233ea47f9acef3d7bda15dbb'),
 (R/'A11/Val03_registru/Verdict_A11_R12_Val03_registru_v1.json','e284136e81d919cb5b8b6dec6ea5ade3af24a59a60ad80e89b4226752a859114'),
 (R/'A11/Val03_registru/Sigiliu_A11_R12_Val03_registru_v1.json','81595e4ecb34ca09e664d2fcf57f4d57e6e2e787e6ea2a6685b145cc153f5c61'),
 (E/'Publicare_R12_Val03/Final_2026-11-03T01-36-40Z/MANIFEST_PUBLICARE_FINAL.json','f9a6d8174592cc009f58c18755a1b30eb67789e5ad5e706d0a0ee6f4e83b8d19'),
 (R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json','3e6aff18819a2d88cd6de04b7ee71dbdd159b80ea7df5652524896306a9dd3ba'),
 (P/'Plan_delta_R12_v2.json','4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276'),
 (P/'A11_verdict_plan_delta_R12_v2.json','84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'),
 (R/'A11/Val04_preflight/Verdict_A11_aplicabilitate_R12_0143_v1.json','0c16fd002cb11ffb0acc5e374e5cc5ce2327c9007ca93d4e0326042a2a05fc4d')]
hashcache={};continuity=[]
for p,expected in manifest_expectations:
    assert ref(p)['sha256']==expected,(p,expected)
    checks=[]
    for rr in find_refs(load(p)):
        q=resolve(rr,p)
        if q not in hashcache:hashcache[q]=ref(q)
        got=hashcache[q];assert got['sha256']==rr['sha256'],(q,rr['sha256'],got['sha256'])
        if 'bytes' in rr:assert got['bytes']==rr['bytes'],q
        if rr.get('pointer') is not None:pointer(load(q),rr['pointer'])
        checks.append({'reference':rr,'hash_match':True,'pointer_checked':rr.get('pointer') is not None})
    continuity.append({'artifact':ref(p),'matches_expected_hash':True,'reference_checks':checks})

dispatchp=P/'Dispatch_tehnic_integral_R12.jsonl.gz';catalogp=P/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz'
with gzip.open(dispatchp,'rt',encoding='utf-8') as f:dispatch=[json.loads(l) for l in f]
assert len(dispatch)==len({r['path'] for r in dispatch})==6728
with gzip.open(catalogp,'rt',encoding='utf-8') as f:catalog_count=sum(1 for _ in f)
assert catalog_count==183469
routes=[r for r in dispatch if r['path'].endswith(('/corelare/CanalGrupe.java','/corelare/OperatiiCanale.java'))]
assert len(routes)==2 and all(r['owner']=='A06' and r['peer']=='A08' for r in routes)
plan=load(P/'Plan_delta_R12_v2.json');zonecheck=load(PREV/'Checklist_10_zone_Val03.json');a11check=load(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json')
assert len(zonecheck['rows'])==10 and len(zonecheck['contracts'])==17
assert all(r['status']=='OPEN' for r in zonecheck['contracts'])

# Metadata-only read. Explicit object names; no default worktree program or export.
commands=[]
for kind,args in [('captured_commits',['show','-s','--format=%H%n%T%n%P%n%aI%n%cI%n%s',H,ad['server_worktree_head'],bd['server_worktree_head']]),('T240_claim_commit_metadata',['show','-s','--format=%H%n%T%n%P%n%aI%n%cI%n%s','6354d62893e'])]:
    cmd=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','saga-server@192.168.100.151',shlex.join(['git','-C','/home/saga-server/Documents/EvA-Contab']+args)]
    t=now();p=subprocess.run(cmd,capture_output=True,timeout=30)
    commands.append({'kind':kind,'started_utc':t,'ended_utc':now(),'command':cmd,'exit':p.returncode,'stdout':p.stdout.decode('utf-8','replace'),'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode('utf-8','replace'),'read_only':True})
assert commands[0]['exit']==0
metadata={'utc':now(),'fixed_candidate':H,'server_HEAD_before':ad['server_worktree_head'],'server_HEAD_after':bd['server_worktree_head'],'commands':commands,'limits':['Commit existence/subject is metadata, not acceptance of T240 implementation, JAR or score.','No new code exported or executed; no fetch, checkout, reset or operational write.','No ancestry/rebase inference from shallow status. Captured GitHub master is distinct from server worktree HEAD.']}

i,newtask=bk[('P01','T386')];assert newtask['stare_generala']=='plan' and newtask['cod_capitol']=='P01.C10.T0030'
tasksref=ref(NEW/'00_STATUS_TASKURI.json','/'+str(i));corrref=ref(NEW/'00_CORESPONDENTA_COD_CAPITOL.json','/coduri/'+str(corr_index))
intake={'schema':'eva.audit.task_intake/1','utc':now(),'id':'T386','canonical':'P01.C10.T0030','state_source_field':'stare_generala','current_state':'plan','source':tasksref,'source_literal':newtask,'correspondence':corrref,'correspondence_literal':correspondence_add[0],
 'in_historic_completed_cohort':False,'historic_task_count_change':0,'historic_criteria_count_change':0,'completion_date':None,'dates_note':'serie and ultima_actualizare are registry metadata; no exact creation/closure transition is inferred.',
 'authority':{'request_kind':'RECONSTRUCTED_REQUEST_AS_EXPLICITLY_LABELLED_IN_REGISTRY','description_is_declared_objective':True,'original_owner_instruction_directly_verified':False,'original_documents_to_locate':['T316/02b_, D-316-11','T211 dovezi-107-R/08_q_a10_5.md','COORDONARE03.11.2026 00:15, C-eva-contab-92-15','eva-contab-b6 response03.11 00:29'],'19_rule_divergence_independently_verified':False,'estimated_10_13h_not_a_deadline_or_completion':True},
 'proposed_atomic_objectives_from_literal_description':[{'id':'INTAKE-T386-O1','text':'Decide and document the unique rules for campaigns and channel groups.','source_field':'descriere','missing_acceptance_oracle':'Enumerate the19 claimed differences and the authoritative resolution for each; no inferred numeric pass threshold.'},{'id':'INTAKE-T386-O2','text':'Make the B-2 writer methods delegate to existing CanalGrupe writers.','source_field':'descriere','native_reuse':'Reuse C_Campaign, EVA_CanalGrupa and existing CanalGrupe; prove callers and original/native table contracts before adding another writer.','missing_acceptance_oracle':'Exact caller coverage, behavior preservation, access/client/org and transactional ownership to be approved.'},{'id':'INTAKE-T386-O3','text':'Provide tests, mutants and revised A-9 reference.','source_field':'descriere','missing_acceptance_oracle':'Named suites/cases, semantic mutant effects and A-9 source/version comparator remain unverified.'}],
 'proposed_assignment':{'owner':'A06','peer':'A08','database_dependency':'A02','tenancy_dependency':'A01','independent_reviewer':'A11','basis':'Existing dispatch routes for CanalGrupe and OperatiiCanale plus the literal new task description. Assignment is not peer execution.','existing_routes':routes,'new_aliases_invented':False,'sealed_dispatch_modified':False},
 'future_case_contract_NOT_EXECUTED':{'actor':'Authenticated authorized channel administrator, plus forbidden other-client/organization actor; exact native role pending identification.','preconditions':'Identify source/bundle/migration at approved candidate; resolve19rules and one-writer authority; dedicated synthetic client/org/channel and legal native identifiers.','input':'Same campaign/group creation/link/unlink through both existing entry paths; duplicate request and concurrent request. Values/IDs must be specified before execution.','expected':'One authoritative writer with equivalent approved behavior, no duplicate links or cross-client changes; no automatic accounting/stock side effect implied.','negative':'Unknown group, forbidden role, other client/org, replay and failing mid-transaction; exact allowed differences require approved rule matrix.','observables':'Read C_Campaign/EVA_CanalGrupa and relevant link/AD audit rows before/after/rollback/retry on new connections; inspect UI feedback only when actually invoked.','postcondition':'Restore/delete only own fixtures and stop/release owned lab; no operational data writes.','status':'PLAN_INTAKE_ONLY; NOMINAL_ADDENDUM_AND_A11_APPROVAL_BEFORE_EXECUTION'},
 'product_tests':0,'implementation_verdict':None,'score':None}

focusids=['T355','T354','T331','T329','T330','T325','T366','T257','T58','T216','T343','T352','T240','T333','T326','T332','T341','T232']
focus=[]
for alias in focusids:
    i0,x=ak[('P01',alias)];i1,y=bk[('P01',alias)]
    focus.append({'alias':alias,'canonical':y.get('cod_capitol'),'current_state':y['stare_generala'],'state_source_field':'stare_generala','before':ref(OLD/'00_STATUS_TASKURI.json','/'+str(i0)),'after':ref(NEW/'00_STATUS_TASKURI.json','/'+str(i1)),'normative_fields':[{'field':k,'equal':(k in x)==(k in y) and x.get(k)==y.get(k),'value_sha256':fhash(y.get(k))} for k in normative],'entire_row_including_observations_and_progress_equal':x==y,'new_execution_credit':0})
assert all(q['equal'] for r in focus for q in r['normative_fields'])
areaeffects={
 'A01':'No existing normative change. T386 proposed channel writer must inherit client/org/role guards; no direct source mapping or execution added.',
 'A02':'RAMASE omits new plan member at this cutoff; record source synchronization limit. T386 table/writer authority must be traced; no native schema change established.',
 'A03':'DocAction, schemes, G1 values and unique boxes/labor cost remain open. New tracker observations supply no accounting evidence.',
 'A04':'Purchases/import/native receipt contracts unchanged; no new execution evidence.',
 'A05':'N05/T355 unchanged and prior bounded finding retained; G2 quantitative11from10 is not a physical count or G1 valuation. T386 membership does not close WMS.',
 'A06':'T386 intake proposed owner from dispatch. T343 all fields unchanged; CO/IP authority remains unresolved. G3 linked site/order double-subtraction and price-transition hypotheses remain unexecuted.',
 'A07':'Delivery/AWB/invoice/returns contracts unchanged; no new native pipeline evidence.',
 'A08':'T240 progress98 and other-commit/JAR/text score claims are unaccepted. Official L6 is still future. Proposed T386 peer is assignment only.',
 'A09':'Native ZK/roles/Mașini deadlines remain open. No UI health/scan/role credit from tracker updates.',
 'A10':'Server HEAD8c excluded from df85gate. T240 claimed6354/JAR require separate version reconciliation. Six retained scratch roots remain; no cleanup bypass.'}
zones=[{'owner':z['owner'],'assigned_files_unchanged':z['assigned_files'],'previous':ref(PREV/'Checklist_10_zone_Val03.json','/rows/'+str(j)),'preflight_disposition':areaeffects[z['owner']],'new_executions':0,'peer_complete_inferred':False} for j,z in enumerate(zonecheck['rows'])]

# Preserve file peer A08 and distinguish A11's domain cross-review A09/A02.
intake['proposed_assignment']['A11_domain_cross_review']=['A09','A02']
intake['proposed_assignment']['file_peer_A08_is_not_replaced_by_domain_cross_review']=True
intake['A11_nominal_intake_addendum']=ref(R/'A11/Val04_preflight/Verdict_A11_aplicabilitate_R12_0143_v1.json','/new_task_addendum')
intake['proposed_assignment']['contracts_from_A11']=['D01','D04','D10','D11']

# Write only after all independent input checks have succeeded.
O.mkdir(parents=True,exist_ok=True)
save(O/'Metadate_Git_0143.json',metadata)
save(O/'Comparatie_996_randuri_existente.json',{'utc':now(),'key':['proiect','id'],'before':ref(OLD/'00_STATUS_TASKURI.json'),'after':ref(NEW/'00_STATUS_TASKURI.json'),'rows':row_ledger,'added':[tasksref],'removed':[]})
comp={'schema':'eva.audit.checkpoint_comparison/2','utc':now(),'baseline_capture':OLD.name,'current_capture':NEW.name,'captures':captures,'comparison_key':['proiect','id'],'total':[996,997],'P01':[693,694],'added':[{'project':'P01','id':'T386','canonical':'P01.C10.T0030','state':'plan','state_source_field':'stare_generala','source':tasksref}],'removed':[],'existing_changes':changes,'state_changes':[],'normative_changes_among_existing':[],'all_shared_rows_compared':996,'all_shared_rows_ledger':ref(O/'Comparatie_996_randuri_existente.json'),'auxiliary_registries':aux,'versions':ref(O/'Metadate_Git_0143.json'),'historic_completed_cohort':{'tasks':652,'criteria':2619,'new_final_vs_last_checkpoint':0,'reopened_vs_last_checkpoint':0,'T352_entire_row_equal':True},'generic_delta_warning':{'source':ref(NEW/'Delta.json'),'its_comparison_base':bd['baseline'],'not_used_for_current_membership_or_finalization':True},'no_missing_completion_date_inferred':True,'product_tests':0}
save(NEW/'Comparatie_ultimul_checkpoint.json',comp)
save(O/'Fisa_intake_T386_v1.json',intake)
save(O/'Continuitate_sigilii_Val03.json',{'utc':now(),'mode':'Read-only integrity of original manifests, handoffv2, correction, independent receipt and publication','artifacts':continuity,'referenced_file_instances_checked':sum(len(x['reference_checks']) for x in continuity),'unique_reference_files':len(hashcache),'all_valid':True,'limits':'File identity and JSON-pointer validity are not product execution. Pending fields in old immutable files are governed by later independent receipt.','previous_sources_modified':0})
save(O/'Dispozitii_10_zone_preflight_Val04.json',{'utc':now(),'candidate':H,'rows':zones,'A11_checklist':ref(R/'A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'),'contracts':zonecheck['contracts'],'contracts_closed':0,'technical_inventory':{'dispatch':ref(dispatchp),'catalog':ref(catalogp),'dispatch_identities':6728,'whole_git_paths':183469,'new_source_exports_or_tests':0},'score':None})
sub={'schema':'eva.audit.r12.preflight0143/1','utc':now(),'candidate':H,'mode':'READ_ONLY_POPULATION_VERSION_CONTINUITY; NO_PRODUCT_EXECUTION','comparison':ref(NEW/'Comparatie_ultimul_checkpoint.json'),'previous_handoff':ref(PREV/'Handoff_R12_Val03_v2.json'),'previous_independent_receipt':ref(R/'A11/Val03_registru/Verdict_A11_R12_Val03_registru_v1.json'),'continuity':ref(O/'Continuitate_sigilii_Val03.json'),'new_member_intake':ref(O/'Fisa_intake_T386_v1.json'),'focus_requirement_equality':focus,'all_fields_definition':'entire_row_including_observations_and_progress_equal compares every present field; normative equality is a separate explicit predicate.','zones':ref(O/'Dispozitii_10_zone_preflight_Val04.json'),
 'new_claims':[{'task':'T240','canonical':'P01.C14.T0001','current_state':'implementare','source':changes[0]['after'],'observations_before':ak[('P01','T240')][1]['observatii'],'observations_after':bk[('P01','T240')][1]['observatii'],'classification':'DECLARED_TEXT_SCORE_AND_OTHER_COMMIT_JAR_NOT_ACCEPTED','accepted_tests_or_score':0,'limits':['10/10 refers to a declared text audit, not our independent product audit.','6354d62893e and aea8d6fe… do not identify the approved df85 code/bundle. Commit metadata is not implementation evidence.','Official native L6 button test is described as future; no execution accepted.','Estimated closure date is not an exact closure event; state remains implementare.','Disappearance or absence of Mașini details does not close its parser/UI finding.']}],
 'gate_applicability_proposal':{'plan':ref(P/'Plan_delta_R12_v2.json'),'approved_plan_gate':ref(P/'A11_verdict_plan_delta_R12_v2.json'),'status':'SUBMITTED_TO_A11; NO_SELF_APPROVAL','existing_fixed_df85_scope':'May remain applicable subject to independent A11 confirmation and existing native readiness checks; no normative changes to existing task rows.','new_T386':'New active plan intake outside652/2619. Its implementation audit requires nominal rules/oracles/source mapping and approved scope addendum; no automatic admission from shared source or chapter.','server_HEAD8c_covered':False,'claim_commit6354_covered':False,'no_credit_from_OID_identity':True,'cohort_expansion_for_completed_tasks_required':False,'native_preconditions':'Exact candidate export/JAR and registered original handler; native build/schema/seed calibration and role/context proof remain necessary. LastBuildInfo placeholder/FailOnBuildDiffer=N does not certify compatibility.','N05':'Prior native finding/limits retained; reversible components only, no recreation of consumed boxes or reversal of labor. G2 nonaccounting, CPP/CPA separate identities, G1 values not certified.','DocAction':'No new before/after facts, schemes, reversals, permissions or accounting balances measured.','ZK':'No native UI scenario executed; actual roles/menu/process must be measured separately.','T343_CO_IP':'Unchanged row and unresolved authority; no accepted amendment of frozen CO|CO|CO oracle.','all17_contracts_open':True,'product_score':None},
 'population':{'total':997,'P01':694,'added_active_plan_tasks':1,'removed':0,'existing_changed_rows':1,'existing_state_changes':0,'historic_final_tasks':652,'historic_criteria':2619,'newly_closed':0,'full_task_acceptances':0},
 'counts_preserved_NOT_new_coverage':{'bounded_evidence_sources':39,'original_component_or_method_paths':26,'comparators':7,'record_or_type_uses':2,'fixture_binding_metadata':4,'static_only_reads':31,'historic_R11_partial_sources_without_R12_transfer':116,'technical_identities':6728,'full_files':0,'full_tasks':0,'full_business_contracts':0},
 'resources':{'new_A12_product_tests':0,'new_A12_lab_or_product_processes':0,'operational_mutations':0,'six_preexisting_retained_scratch_roots':'Unchanged after automatic cleanup rejection; no bypass or claim of full restitution.','A05_previous_lab':'Closed in prior sealed handoff; this preflight does not operate PostgreSQL or native clone.'},'version_metadata':ref(O/'Metadate_Git_0143.json'),'exact_completion_dates_absent_remain_undocumented':True}
sub['gate_applicability_proposal']['independent_applicability_receipt']=ref(R/'A11/Val04_preflight/Verdict_A11_aplicabilitate_R12_0143_v1.json')
sub['gate_applicability_proposal']['status']='A11_CONFIRMED_LIMITED_DF85_APPLICABILITY; A12_SUPPLEMENT_RECEPTION_PENDING; CONCRETE_NEXT_PROTOCOLS_NOT_APPROVED_BY_THIS_DOCUMENT'
save(O/'Supliment_populatie_0143.json',sub)
save(O/'Handoff_preflight_Val04_v1.json',{'utc':now(),'candidate':H,'server_HEAD_at_capture':bd['server_worktree_head'],'previous':ref(PREV/'Handoff_R12_Val03_v2.json'),'previous_independent_receipt':ref(R/'A11/Val03_registru/Verdict_A11_R12_Val03_registru_v1.json'),'supplement':ref(O/'Supliment_populatie_0143.json'),'comparison':ref(NEW/'Comparatie_ultimul_checkpoint.json'),'intake':ref(O/'Fisa_intake_T386_v1.json'),'zones':ref(O/'Dispozitii_10_zone_preflight_Val04.json'),'A11_applicability':ref(R/'A11/Val04_preflight/Verdict_A11_aplicabilitate_R12_0143_v1.json'),'A11_A12_supplement_reception_pending':True,'new_product_execution_credit':0,'next_action':'A11 receives this supplement independently; parent dispatches only approved concrete next protocols. Preserve the 652/2619 cohort; any T386 execution first needs nominal scope authority.','score':None})

page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Val04 — verificarea capturii01:43</title><style>body{font:17px/1.55 system-ui;margin:auto;padding:24px;max-width:960px;color:#152334;background:#f6f8fb}a,code{overflow-wrap:anywhere}article{background:white;padding:22px;border:1px solid #d4dce4;border-radius:10px}.table{overflow-x:auto}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd5de;padding:8px;text-align:left}h1{font-size:1.7rem}</style><article><h1>Preflight Val04: un task nou în plan</h1><p>Comparăm captura03.11.2026 01:43:37 UTC cu ultima captură00:39:34 UTC. GitHub: <code>df85d33c1648ce2b2df130a60a05ef696e2e5480</code>. HEAD-ul separat al serverului este <code>8c0695de36b50ede569c6d318715db0af11fcbff</code> și nu primește acoperire.</p><div class="table"><table><tr><th>Indicator</th><th>Înainte</th><th>Acum</th></tr><tr><td>Total tracker / P01</td><td>996 /693</td><td>997 /694</td></tr><tr><td>Taskuri istorice / criterii</td><td>652 /2619</td><td>652 /2619</td></tr><tr><td>Stări existente schimbate / noi finalizări</td><td>—</td><td>0 /0</td></tr></table></div><p><strong>T386 /P01.C10.T0030 este în plan:</strong> unificarea scriitorilor campaniilor și grupelor canalelor. Primește fișă de intrare, nu verdict de implementare. Registrul principal și corespondența îl includ; registrele derivate RAMASE/FINALIZATE sunt neschimbate.</p><p><strong>T240 rămâne în implementare.</strong> Progres97→98 și observații noi despre un alt commit/JAR și un scor declarat pentru texte nu demonstrează execuția nativă sau finalizarea. T352 este identic cu ultima captură, deci nu este nou finalizat în acest interval.</p><p>Niciun test de produs nou. Cele39surse cu dovezi anterioare au niveluri diferite:26componente/trasee de metode,7comparatoare,2utilizări de tip și4fixture/binding/metadate. Niciun contract business integral închis; toate17rămân deschise.</p><ul><li><a href="Supliment_populatie_0143.json">Supliment nominal și limite</a></li><li><a href="Fisa_intake_T386_v1.json">Fișa de intrare T386</a></li><li><a href="Dispozitii_10_zone_preflight_Val04.json">Continuitatea celor10zone</a></li><li><a href="Continuitate_sigilii_Val03.json">Verificarea sigiliilor Val03</a></li><li><a href="Handoff_preflight_Val04_v1.json">Predarea pentru recepția A11</a></li><li><a href="../Val_03/index_final.html">Val03recepționat — versiunea anterioară imuabilă</a></li></ul><p>Propunerea de aplicabilitate este transmisă A11; această pagină nu acordă aprobare sau scor.</p></article></html>'''
page=page.replace('capturii01:43','capturii 01:43').replace('captura03.11.2026','captura 03.11.2026').replace('captură00:39:34','captură 00:39:34').replace('Progres97','Progres 97').replace('Cele39surse','Cele 39 surse').replace('26componente','26 componente').replace('7comparatoare','7 comparatoare').replace('2utilizări','2 utilizări').replace('4fixture','4 fixture').replace('toate17rămân','toate 17 rămân').replace('celor10zone','celor 10 zone').replace('Val03recepționat','Val03 recepționat').replace('Propunerea de aplicabilitate este transmisă A11; această pagină nu acordă aprobare sau scor.','A11 a menținut aplicabilitatea limitată a planului pentru df85 și a primit nominal T386 ca task în plan. Suplimentul A12 și protocoalele concrete următoare au recepții distincte; această pagină nu acordă scor sau credit de execuție.')
ip=O/'index_preflight.html';assert not ip.exists();ip.write_text(page,encoding='utf-8',newline='\n')
scriptp=O/'build_preflight0143.py';assert not scriptp.exists();scriptp.write_bytes(pathlib.Path(__file__).read_bytes())

outputs=list(O.iterdir());instances=0;pointers=0
for p in outputs+[NEW/'Comparatie_ultimul_checkpoint.json']:
    if p.suffix!='.json':continue
    for rr in find_refs(load(p)):
        q=resolve(rr,p);assert sha(q.read_bytes())==rr['sha256'],q
        if 'bytes' in rr:assert q.stat().st_size==rr['bytes']
        if rr.get('pointer') is not None:pointer(load(q),rr['pointer']);pointers+=1
        instances+=1
qa={'utc':now(),'all_input_expected_hashes_match':True,'capture_files_rehashed':14,'unique_existing_rows_compared':996,'new_members':1,'removed_members':0,'state_changes':0,'existing_normative_changes':0,'auxiliary_files_compared':6,'auxiliary_files_identical':5,'correspondence_only_new_entry':'P01.C10.T0030','focus_tasks':len(focus),'focus_normative_predicates':sum(len(x['normative_fields']) for x in focus),'reference_instances_checked':instances,'json_pointers_checked':pointers,'technical_routes_unique':6728,'catalog_paths':catalog_count,'historic_cohort':[652,2619],'ten_zone_rows':10,'contracts_open':17,'product_tests':0,'new_task_or_criterion_credit':0,'issues':[],'score':None}
save(O/'QA_preflight_0143.json',qa)
save(O/'MANIFEST_preflight_Val04_0143.json',{'utc':now(),'candidate':H,'files':[ref(p) for p in sorted(O.iterdir())]+[ref(NEW/'Comparatie_ultimul_checkpoint.json')],'inputs':[ref(p) for p,_ in manifest_expectations]+[ref(dispatchp),ref(catalogp),ref(PREV/'Checklist_10_zone_Val03.json')],'A11_receipt_pending':True,'no_self_reference':True,'no_previous_artifact_modified':True,'no_product_execution':True})
print(json.dumps({'manifest':ref(O/'MANIFEST_preflight_Val04_0143.json'),'handoff':ref(O/'Handoff_preflight_Val04_v1.json'),'supplement':ref(O/'Supliment_populatie_0143.json'),'intake':ref(O/'Fisa_intake_T386_v1.json'),'comparison':ref(NEW/'Comparatie_ultimul_checkpoint.json'),'QA':qa},ensure_ascii=False,indent=2))
