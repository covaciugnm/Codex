import copy,gzip,hashlib,json,pathlib,sys
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');R=B/'executie/R12_fisiere';P=R/'A12/Val_03';O=R/'A12/Val_04/Increment_02_G3';N=R/'A05_G3_nativ_lot04';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
MEM={};CHECKS=[];INPUTS=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return MEM[p.name] if p.parent==O and p.name in MEM else p.read_bytes()
def load(p):return json.loads(read(p).decode('utf-8-sig'))
def ref(p,pointer=None):
 b=read(p);d={'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
 if pointer is not None:d['pointer']=pointer
 return d
def put(n,x):
 assert not (O/n).exists() and n not in MEM;MEM[n]=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8');return ref(O/n)
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
 if s.startswith('idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'):
  return N/'surse_df85'/s.split('src/com/eva/ro/contab/',1)[1]
 if (p.parent/q).exists() or p.parent==O and q.name in MEM:return p.parent/q
 if (N/q).exists():return N/q
 raise AssertionError((p,s))
def pointer(d,p):
 for k in p.lstrip('/').split('/') if p else []:d=d[int(k)] if isinstance(d,list) else d[k.replace('~1','/').replace('~0','~')]
 return d
def verify(p,h=None):
 rr=ref(p)
 if h:assert rr['sha256']==h,p
 for r in refs(load(p)):
  q=resolve(p,r['path']);assert sha(read(q))==r['sha256'],q
  if 'bytes' in r:assert len(read(q))==r['bytes']
  if 'pointer' in r:pointer(load(q),r['pointer'])
  CHECKS.append(r)
 INPUTS.append(rr);return load(p)
cfg=load(pathlib.Path(sys.argv[1]));assert cfg['head']==H and cfg['approved_native_receipt']
vr=B/cfg['receipt']['path'];v=verify(vr,cfg['receipt']['sha256'])
for r in cfg['additional_receipts']:verify(B/r['path'],r['sha256'])
verify(N/'MANIFEST_A05_G3_nativ_lot04_v1.json','4bd069621d27559943683fd7162bf906343b332c2f0af8aa316e346327b25410')
verify(N/'SIGILIU_supliment_QA_G3_v1.json','06892ba6906da7c1eaff0e2336bffb2b53c855184bd31b252814899d4f68aea4')
reportp=N/'Raport_A05_G3_nativ_lot04_v1.json';report=verify(reportp,'ef97e27d2fa2b0913156c9837e0af9e59073f07755c3ed51299dbc14e46f9f8e')
fp=N/'Fise_G3_final_v1.json';assert sha(read(fp))=='a05a418cd88b985540792896693fe26bad035e99babe18a8eb156a0e9fe50533';f=load(fp)
with gzip.open(P/'Registru_6728_R12_Val03.jsonl.gz','rt',encoding='utf-8') as z:D={r['path']:r for r in map(json.loads,z)}
assert len(f)==13 and len(D)==6728
classifications={s['path']:s['coverage_class'] for s in f};assert len(classifications)==13
counts=report['scope_counts'];assert counts['planned_families']==10 and counts['valid_python_readbacks']==41 and counts['initial_setup_only_readbacks']==1
orp=N/'Oracle_independent_G3_v1.json';oracle=load(orp);assert len(oracle['actual_java_outputs'])==16
case_rows=[]
for i,c in enumerate(report['cases']):
 j=next(j for j,a in enumerate(v['scenario_dispositions']) if a['id']==c['id'])
 case_rows.append({'scenario_id':c['id'],'producer_status':c['state'],'observed':c['detail'],'source':ref(reportp,'/cases/'+str(i)),'native_outputs':ref(orp,'/actual_java_outputs'),'oracle_source':ref(orp),'A11_disposition':v['scenario_dispositions'][j],'A11_receipt':ref(vr,'/scenario_dispositions/'+str(j)),'full_business_contract_acceptance':False,'limit':'Familiile de scenarii nu se confundă cu liniile CASE_G3, recitirile SQL sau predicatele A11. Statutul se interpretează în limitele recepției independente.'})
assert len(case_rows)==10 and len({c['scenario_id'] for c in case_rows})==10
caseref=put('Scenarii_G3_10.json',{'head':H,'rows':case_rows,'protocol_families':10,'CASE_G3_lines':16,'valid_python_readbacks':41,'initial_setup_readbacks':1,'total_readbacks':42,'independent_A11_metrics':cfg['A11_metrics'],'calibrations':report['errors_retained'],'calibration_is_not_product_failure':True,'raw_oracle':ref(orp),'native_receipt':ref(vr),'score':None})
pure={'FisaCanalCalcul.java','RegulaStocCanal.java','TabelaFisaCanal.java'}
effects={
 'RezervareStoc.java':'Citire originală a stocului și rezervărilor native comise; fără scriere a cititorului. Rezervările sunt create prin PO/API native în fixture, nu prin C_Order/DocAction.',
 'FisaCanalProces.java':'Sursa persistată este citită prin metodele originale sursa/stoc/surse.brut/stocArticol; fără doIt, AD_Process, publicare HTTP sau persistarea fișei rezultate.',
 'FisaCanalCalcul.java':'Calcul pur stocCalculat: plafonare la zero și floor în parametrii testați. Nu citește direct DB în această probă și nu persistă rezultate.',
 'RegulaStocCanal.java':'Calculul original cantitateOferita cu harta goală; fără query direct sau persistență. Celelalte reguli nu sunt validate.',
 'SetLista.java':'Traseu auxiliar pe produs non-BOM și cerere de componente absentă/zero; nu probează seturi cu componente, comenzi S1/S2 sau împărțirea stocului între seturi.',
 'TabelaFisaCanal.java':'reguliStoc pe canal null întoarce harta goală, fără query direct. Nu probează o configurație de canal activă.',
 'EvaWmsGardaEvents.java':'Handler original și filtre/topics observate în pregătirea fixturelor native; nu se certifică toate ramurile gardelor WMS.',
 'EvaStocEvents.java':'Binding și pregătire fixture după topicurile reale; fără credit nou pentru costare/postare sau toate ramurile handlerului.',
 'EvaAuditPostareEvents.java':'Binding auxiliar original; fără probă de Fact_Acct ori postare în acest lot.'}
runtime=[];static=[];overrides=[]
for i,s in enumerate(f):
 path=s['path'];name=pathlib.Path(path).name;d=D[path]
 loc=N/'surse_df85'/path.split('src/com/eva/ro/contab/',1)[1];bb=read(loc)
 assert d['git_oid']==s['oid']==hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest() and sha(bb)==s['sha256']
 # The reviewer provides authoritative nominal dispositions. No coverage inferred from stale state.
 nominal=cfg['source_dispositions'][path];assert nominal['coverage_class']==s['coverage_class']
 override={'path':path,'source':ref(fp,'/'+str(i)),'old_state_literal':s['state'],'effective_classification':s['coverage_class'],'generic_native_method_not_assigned_to_every_file':s['native_method'],'effective_method_scope':s['method_scope'],'persistent_effect_literal':s['persistent_effect'],'effective_effect':effects.get(name,'Numai constante sau lectură statică; nicio metodă ori citire DB creditată independent.'),'authoritative_native_method_and_effect':nominal['authoritative_native_method_and_effect'],'authority':ref(vr,nominal['pointer']),'routing_note':'Owner și peer nominali rămân cei din dispatch; A05 este executorul lotului. O responsabilitate de lot din raport nu modifică alocarea fiecărei surse.'}
 overrides.append(override)
 common={'path':path,'git_oid':s['oid'],'sha256':s['sha256'],'source':ref(loc),'owner':d['owner'],'planned_peer':d['planned_peer'],'control':d['control'],'pipeline_candidates':d['pipeline_candidates'],'task_candidates_preserved':d['task_candidates'],'task_mapping':s['task'],'producer_sheet':ref(fp,'/'+str(i)),'independent_receipt':ref(vr,nominal['pointer']),'planned_peer_performed_not_inferred':True,'coverage_class':s['coverage_class'],'method_scope':s['method_scope'],'actor':s['actor'],'entry_point':s['normal_path'],'requirement':s['requirement'],'positive':s['positive'],'counterexample':s['counterexample'],'persistent_effect':override['effective_effect'],'limits':[s['limit'],'Context User101/Role102/client11/org11 pregătit sintetic, fără autentificare UI sau dovadă completă de autorizare.','Identitatea sursei și montarea nu certifică toate funcțiile ori compatibilitatea integrală a buildului.'],'whole_file_accepted':False,'task_closed':False,'metadata_override':override}
 if s['coverage_class'] in ('LECTURA_STATICA','CONSTANTE_METADATE_FARA_CREDIT_EXECUTIE'):
  common.update(scope=s['coverage_class'],execution_credit=False,actual_reader='A05');static.append(common);continue
 assert s['coverage_class'] in ('METODA_ORIGINALA_APELATA_LIMITAT','TRASEU_TRANZITIV_LIMITAT','FIXTURE_BINDING')
 updates={}
 if s['coverage_class']=='FIXTURE_BINDING':
  # Never erase a stronger previous event. These three already had bounded fixture/binding evidence.
  assert d['axis']['component_exercised']=='NATIVE_FIXTURE_OR_BINDING_PARTIAL'
  updates={'component_exercised':d['axis']['component_exercised'],'installed_binding':'ORIGINAL_CLASS_BOUND_IN_ISOLATED_NATIVE_CLONE_ONLY'}
  method='NATIVE_FIXTURE_BINDING_PARTIAL'
 else:
  updates={'component_exercised':'NATIVE_ORIGINAL_METHOD_PARTIAL' if s['coverage_class']=='METODA_ORIGINALA_APELATA_LIMITAT' else 'NATIVE_TRANSITIVE_METHOD_PARTIAL'}
  if name in ('RezervareStoc.java','FisaCanalProces.java'):updates['ERP_DB']='ORIGINAL_NATIVE_DB_READBACK_PARTIAL'
  # Pure calculations receive no direct DB axis. SetLista retains earlier evidence without expanding its DB scope.
  method='ORIGINAL_NATIVE_DB_READER_PARTIAL' if name in ('RezervareStoc.java','FisaCanalProces.java') else 'ORIGINAL_NATIVE_TRANSITIVE_METHOD_PARTIAL'
 common.update(event_id=s['event_id'],actual_executor='A05',method_kind=method,execution_group='R12V04-G3-NATIVE-10-SCENARIOS',accepted_axis_updates=updates,native_reuse='PO/Trx și MStorageReservation native pentru fixture/comparator; fiecare fișier primește numai metoda și efectul descrise individual.',cases=caseref,scenario_scope=s['scenario'],evidence=s['evidence'])
 runtime.append(common)
assert len(runtime)==9 and len(static)==4 and len({r['path'] for r in runtime})==9
ov=put('Calificari_nominale_G3_13.json',{'head':H,'rows':overrides,'authority':ref(vr),'original_producer_sheets_unchanged':True,'purpose':'Câmpul state din plan și metoda/efectul generic din fișele executorului nu guvernează acoperirea finală. Dispoziția A11 și traseul nominal guvernează consolidarea.','new_execution_credit_from_correction':0})
cleanup=load(N/'Cleanup_final_v1.json');assert cleanup['pgStopped'] and cleanup['targetExistsAfter'] is False and cleanup['ownJvmProcesses']==0 and cleanup['listenersAfter']==0
resources={'cleanup_snapshot':ref(N/'Cleanup_final_v1.json'),'observed_in_cleanup':cleanup,'global_current_state_not_asserted':True,'retained_runtime_cache_and_harness':'Păstrate pasiv pentru reproducere; nu sunt servicii active. Cele șase rădăcini blocate anterior și PG al altor agenți au rămas neatinse.'}
findings={'existing_id':'R12-STOC-SO-PO-01','report':ref(reportp),'independent_receipt':ref(vr),'new_statistical_finding':False,'IsActive':'Diferență de politică nativă/EVA în fixture; fără defect nou sau validare a dreptului comercial.','confirmed_numeric_scope':'Stoc cantitativ înregistrat10, SO2 și PO0/5/15: nativ8; RezervareStoc8/3/−7; fișa canalului8/3/0. Nu sold valoric contabil și nu numărare fizică.'}
native={'head':H,'status':'PROBE NATIVE RECEPȚIONATE LIMITAT; FĂRĂ CONTRACT BUSINESS ÎNCHIS','independent_receipt':ref(vr),'producer_report':ref(reportp),'producer_manifest':ref(N/'MANIFEST_A05_G3_nativ_lot04_v1.json'),'runtime_events':runtime,'static_only_rows':static,'cases':caseref,'nominal_metadata_overrides':ov,'counts':{'EVA_source_sheets':13,'original_direct_method_sources':2,'transitive_method_sources':4,'fixture_binding_sources':3,'constants_without_execution_credit':2,'static_only_sources':2,'protocol_scenarios':10,'CASE_G3_lines':16,'valid_readbacks':41,'initial_setup_readbacks':1,'native_dependency_sources_outside_EVA_corpus':7,'A11_separate':cfg['A11_metrics']},'task_mapping':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','findings':findings,'finding_count_policy':'Constatarea SO/PO existentă este întărită nativ, nu dublată. Trei mecanisme frontend rămân separate și nu provin din acest test.','full_file_or_contract_acceptances':0,'resources':resources,'next_controls':cfg['next_controls'],'limits':report['limits']+cfg['extra_limits'],'native_first_recommendations':report['native_first_recommendation'],'public_summary_ro':'Proba nativă confirmă că cele două citiri EVA scad și cantitățile PO din disponibilul pentru vânzare. La stoc cantitativ înregistrat10 și SO2, creșterea PO de la0 la5 reduce EVA de la8 la3, în timp ce comparatorul nativ rămâne8. La PO15, RezervareStoc întoarce−7, iar calculul fișei canalului plafonează la0. Aceasta întărește constatarea SO/PO existentă; nu demonstrează C_Order/DocAction, UI, publicarea canalului ori soldurile valorice G1.','score':None}
nr=put('Curatoriat_G3_Val04.json',native)
MEM['build_increment_G3.py']=pathlib.Path(__file__).read_bytes();MEM['configuration_G3.json']=read(pathlib.Path(sys.argv[1]))
for n in list(MEM):
 if not n.endswith('.json'):continue
 for rr in refs(load(O/n)):
  if rr['path'] in D:
   if 'git_oid' in rr:assert rr['git_oid']==D[rr['path']]['git_oid']
   continue
  p=resolve(O/n,rr['path']);assert sha(read(p))==rr['sha256'],p
  if 'pointer' in rr:pointer(load(p),rr['pointer'])
  CHECKS.append(rr)
put('QA_increment_G3.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_identities':13,'original_methods_or_paths':6,'fixture_binding':3,'constants_or_static':4,'reference_instances_checked':len(CHECKS),'producer_scope_counts_kept_separate':True,'previous_SQL_evidence_not_erased':True,'issues':[],'score':None})
put('MANIFEST_increment_G3.json',{'utc':datetime.now(timezone.utc).isoformat(),'head':H,'files':[ref(O/n) for n in sorted(MEM)],'inputs':INPUTS,'not_final_Val04_registry':True,'no_self_reference':True})
O.mkdir(parents=True,exist_ok=True)
for n,b in MEM.items():assert not (O/n).exists();(O/n).write_bytes(b)
for n,b in MEM.items():assert (O/n).read_bytes()==b
print(json.dumps({'manifest':ref(O/'MANIFEST_increment_G3.json'),'native_curated':nr,'runtime_events':9,'static_rows':4,'cases':10,'CASE_lines':16},ensure_ascii=False))
