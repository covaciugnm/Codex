import sys,collections
from a12_val05_common import *
F=R/'A08_Catalog_paginare_lot05';Q=O/'Increment_01_paginare'
cfg=load(pathlib.Path(sys.argv[1]));assert cfg['head']==H and cfg['A11_received']
checks=[];inputs=[]
for rr in cfg['inputs']:
    p=B/rr['path'];_,cc=verify(p,rr['sha256']);checks+=cc;inputs.append(ref(p))
vp=B/cfg['receipt']['path'];v,cc=verify(vp,cfg['receipt']['sha256']);checks+=cc
manifest,cc=verify(F/'MANIFEST_A08_paginare_lot05_v1.json','b8d60193a2429057dcd860813141c578c29e2234d0c3225c4efb686fe724cad7');checks+=cc
report,cc=verify(F/'Raport_A08_paginare_lot05_v3.json','4b44bf0d258639747e9c2976f1340cbdcc2cf7a3f3d732e63aa344144a19050d');checks+=cc
fp=F/'Fise_16_surse_paginare_v2.json';sheets=load(fp)['rows'];assert len(sheets)==16
prior,D=read_prior();runtime=[];support=[];classifications=[]
rp=F/'Rezultate_paginare_v1.json';results=load(rp)
assert len(results['rows'])==16 and len({r['id'] for r in results['rows']})==16
assert collections.Counter(r['contract_result'] for r in results['rows'])=={'PASS_LIMITED':10,'FAIL_CONTRACT':6}
classmap={
 'ORIGINAL_COMPONENT_PARTIAL':('ORIGINAL_JAVA_METHOD_COMPONENT_PARTIAL','ORIGINAL_JAVA_DIRECT_METHOD_PARTIAL'),
 'ORIGINAL_TRANSITIVE_PATH_PARTIAL':('ORIGINAL_JAVA_TRANSITIVE_PATH_PARTIAL','ORIGINAL_JAVA_TRANSITIVE_PATH_PARTIAL'),
 'ORIGINAL_DIAGNOSTIC_PATH_PARTIAL':('ORIGINAL_JAVA_DIAGNOSTIC_PARTIAL','ORIGINAL_JAVA_DIAGNOSTIC_PARTIAL'),
 'ORIGINAL_VALUE_TYPE_PARTIAL':('ORIGINAL_VALUE_TYPE_USE_PARTIAL','ORIGINAL_VALUE_TYPE_PARTIAL'),
 'ORIGINAL_FIXTURE_BINDING_PARTIAL':('ORIGINAL_FIXTURE_BINDING_PARTIAL','ORIGINAL_CONFIGURATION_BINDING_PARTIAL')}
for i,s in enumerate(sheets):
    path=s['path'];d=D[path];src=B/s['source']['path'];bb=src.read_bytes()
    assert s['git_oid']==d['git_oid']==hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()
    assert sha(bb)==s['source']['sha256'];assert s['owner_catalog']==d['owner'] and s['planned_peer_catalog']==d['planned_peer']
    disp=cfg['source_dispositions'][path]
    assert disp['coverage_level']==s['coverage_level']
    common={'path':path,'git_oid':d['git_oid'],'sha256':sha(bb),'source':ref(src),'owner':d['owner'],'planned_peer':d['planned_peer'],'control':d['control'],'pipeline_candidates':d['pipeline_candidates'],'task_candidates_preserved':d['task_candidates'],'task_mapping':'SHARED_NO_TASK_ASSIGNED','producer_sheet':ref(fp,'/rows/'+str(i)),'independent_receipt':ref(vp,disp['pointer']),'actual_executor':'A08','planned_peer_performed_not_inferred':True,'requirement':s['requirement'],'actor':s['actor'],'entry_point':s['normal_route'],'method_scope':s['methods_in_scope'],'positive':s['positive'],'counterexample':s['counterexample'],'persistent_effect':s['persistent_effect'],'limits':[s['limits'],'Nici HTTP, UI, OSGi, DB ori utilizator autenticat nu sunt executate de acest lot.','Compilarea și încărcarea clasei sunt separate de apelul unei metode și nu certifică toate ramurile.'],'whole_file_accepted':False,'task_closed':False,'coverage_class':s['coverage_level'],'granular_levels':{'compiled':s['compiled'],'class_loaded':s['observed_class_loaded'],'direct_method_call':s['direct_method_call_in_harness'],'call_evidence_type':s['method_evidence_type'],'database_persistence':False,'fixture_files_unchanged':True,'HTTP_or_UI_executed':False},'A11_qualifications':disp.get('qualifications',[])}
    classifications.append(copy.deepcopy(common))
    if s['coverage_level'] not in classmap:
        assert s['coverage_level'] in ['COMPILE_ONLY_NO_METHOD_CREDIT','STATIC_CONTEXT_ONLY']
        common.update(scope=s['coverage_level'],execution_credit=False,actual_reader='A08');support.append(common);continue
    axis,method=classmap[s['coverage_level']]
    common.update(event_id='R12V05-PAGINATION-'+d['id'],method_kind=method,execution_group='R12V05-A08-PAGINATION-16-CASES',accepted_axis_updates={'component_exercised':axis,'read':'OBSERVED_AT_LINKED_SCOPE'},cases=ref(rp),scenario_scope=s['events'],evidence=ref(fp,'/rows/'+str(i)))
    runtime.append(common)
assert len(runtime)==7 and len(support)==9
assert sum(s['compiled'] for s in sheets)==12 and sum(s['observed_class_loaded'] for s in sheets)==7
assert sum(s['direct_method_call_in_harness'] for s in sheets)==4
case_rows=[]
for i,c in enumerate(results['rows']):
    case_rows.append({'id':c['id'],'entry':c['entry'],'fixture':c['fixture'],'input':c['input'],'expected':c['expected'],'observed_outcome':c['actual']['outcome'],'observed':{k:w for k,w in c['actual'].items() if k!='full_result'},'status':c['contract_result'],'proof':ref(rp,'/rows/'+str(i)),'whole_acceptance':False})
Q.mkdir(parents=True,exist_ok=True)
save(Q/'Cazuri_paginare_16.json',{'head':H,'rows':case_rows,'executor_cases':16,'independent_A11_calls_separate':6,'calibration_attempts':report['preparation_attempts'],'calibrations_not_cases_or_product_failures':True,'independent_receipt':ref(vp),'score':None})
save(Q/'Calificari_nominale_16_surse.json',{'head':H,'rows':classifications,'compiled_sources':12,'loaded_classes_sources':7,'direct_method_sources':4,'transitive_or_diagnostic_sources':3,'compile_only_sources':5,'static_context_sources':4,'A11_receipt':ref(vp),'whole_acceptances':0})
finding=load(F/'Constatare_paginare_v1.json')
assert finding['id']=='R12-CATALOG-JSON-PAGINATION-01' and finding['mechanism_count']==1
curated={'head':H,'status':'COMPONENTA_JAVA_RECEPȚIONATA_LIMITAT','independent_receipt':ref(vp),'producer_manifest':ref(F/'MANIFEST_A08_paginare_lot05_v1.json'),'producer_report':ref(F/'Raport_A08_paginare_lot05_v3.json'),'runtime_events':runtime,'support_rows':support,'source_classifications':ref(Q/'Calificari_nominale_16_surse.json'),'cases':ref(Q/'Cazuri_paginare_16.json'),'counts':{'source_sheets':16,'compiled_original_sources':12,'method_or_type_or_binding_sources':7,'original_component_sources':2,'transitive_sources':2,'diagnostic_sources':1,'value_type_sources':1,'fixture_binding_sources':1,'compile_only_without_runtime_credit':5,'static_context_sources':4,'executor_cases':16,'conforming_limited_cases':10,'nonconforming_cases':6,'index_exceptions':4,'wrong_first_page_repetitions':2,'finding_mechanisms':1,'finding_sites':2,'independent_A11_calls_separate':6,'full_acceptances':0},'findings':{'source':ref(F/'Constatare_paginare_v1.json'),'id':finding['id'],'promotes_prior_static_candidate':finding['promotes_candidate'],'unique_mechanism_count':1,'A11_receipt':ref(vp),'limit':'Excepție sau pagină greșită la metoda originală; nu HTTP500 și nu cauza erorilor simulate frontend Val04.'},'resources':{'executor_cleanup':ref(F/'Cleanup_final_v1.json'),'retained_root':'D:/CodexWork/a08-catalog-json-l05-20261103','rejection':'blocked by policy','own_JVM_remaining':0,'retained_A11_root':'D:/CodexWork/a11-catalog-oracle-l05-20261103','no_cleanup_bypass':True},'task_mapping':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','full_file_or_contract_acceptances':0,'limits':report['limits']+cfg.get('extra_limits',[]),'next_controls':cfg['next_controls'],'public_summary_ro':'Paginarea catalogului JSON a fost executată prin cele două metode originale, pe trei produse sintetice. Șase dintre cele 16 cazuri arată același mecanism de depășire a intervalului int: patru excepții de index și două repetări ale primei pagini. Proba nu a apelat servletul, HTTP, sursa DB ori UI. Corecția propusă adaptează aritmetica cititorului existent, fără un catalog paralel.','score':None}
save(Q/'Curatoriat_paginare_Val05.json',curated)
for p in list(Q.glob('*.json')):
    _,cc=verify(p);checks+=cc
save(Q/'QA_increment_paginare.json',{'utc':now(),'source_identities_verified_oid_sha_dispatch':16,'runtime_or_type_or_binding_sources':7,'compile_only':5,'static_context':4,'cases':16,'references_checked':len(checks),'peer_assignment_not_inferred_completed':True,'no_task_criteria_accepted':True,'issues':[],'score':None})
shutil_source=pathlib.Path(__file__);(Q/'build_increment_paginare.py').write_bytes(shutil_source.read_bytes());(Q/'configuration_paginare.json').write_bytes(pathlib.Path(sys.argv[1]).read_bytes());(Q/'a12_val05_common.py').write_bytes(pathlib.Path(__file__).with_name('a12_val05_common.py').read_bytes())
save(Q/'MANIFEST_increment_paginare.json',{'utc':now(),'head':H,'files':[ref(p) for p in sorted(Q.iterdir())],'inputs':inputs+[ref(vp),ref(F/'MANIFEST_A08_paginare_lot05_v1.json')],'no_self_reference':True,'not_final_Val05_registry':True,'no_new_A12_product_execution':True})
print(json.dumps({'manifest':ref(Q/'MANIFEST_increment_paginare.json'),'curated':ref(Q/'Curatoriat_paginare_Val05.json'),'runtime':7,'support':9,'cases':16},ensure_ascii=False,indent=2))
