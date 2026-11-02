from a12_r7_ledger import *
from a12_r7_atomic import dev,suite_by
native=E/'R6_pregatire/ERP/UX/UX_15_forme_roluri.json';ux=rd(native);local_forms=defaultdict(list)
for q in ux['matrix']:
 for c in q['criteria']:local_forms[c['criterion']].append({'class':q['class'],'role':q['role'],'AD_Session_ID':q['role_session'],'strict_role_navigation_only':q['state']})
case_runs=rd(RP/'Cazuri_locale_nominale_79.json')['records'];ran=defaultdict(list)
for r in case_runs:ran[r['criterion']].append(r)
a03p=E/'R4_zone/A03/dovezi/Registru_incremental_01.json';a03={r['criterion_id']:r for r in rd(a03p)['claims']}
sq=rd(RP/'SQL/Matrice_SQL_reala_R7.json');sqlnames=defaultdict(list)
for name,item in sq['expectations_before_mutation'].items():
 for cid in item['criteria']:sqlnames[cid].append(name)
symptom={'T216-R2-001':'Transferul din cererea explicită «site→comenzi iDempiere» întâlnește refuzul V01 al importului cetății C (Q conține 2 linii DTO și zero linii salvate).','T216-R2-002':'Q nu devine C_Order din COMENZI+VALIDEZ. Din această Q nu se poate observa facturarea asociată.','T216-R2-005':'Pentru Q, lipsa C_Order și deci a facturii legate împiedică afișarea numărului acelei facturi pe site.','T216-R2-006':'Conversia→factură→plată pentru Q nu traversează validarea. Contraexemplul arată că înscrierea seller.cui în DTO înlătură numai V02.','T216-R2-007':'Validarea comenzii native din solicitarea atribuită acestui ID se oprește pentru Q la V01/V02; alte origini nu primesc această concluzie.'}
blocked_exact={q:s for q,s in symptom.items()if q in reg}
local_mixed={'T04.01-R3-001':('Simulator de platformă; mock easySales/C cu comanda sintetică Q, jurnal de scriere și trei răspunsuri','Compară identificatorul comenzii importate și pretenția «fără modificare la partener».'),
'T04.02-R3-001':('Fișier sintetic de ramburs și comisioane+importul și vizualizarea decontului; destinatarul real rămâne separat.','Pentru plată 5 și virament 3, reconciliază diferența 2 în fișa de decont și păstrează comanda.'),
'T04.03-R3-001':('Simulatorul original cu order/read și decont de contul A; urmărește tentativele de write.','Citirea datelor este permisă, iar operațiile de modificare nu trebuie să producă efect la contul extern. POST de citire din protocolul eMAG se tratează separat de scrierea comercială.'),
'T04.10-R3-001':('Identitate A/B și comenzi refuzate/admise prin simulatorul eMAG nominal, corp cu cheie nouă și replay.','Comenzile afișate/importate trebuie să aparțină contului selectat; accesul la sandbox-ul furnizorului rămâne un control separat.'),
'T17-R2-001':('Fixtura extrasului Smart Fintech și două conturi mock; fără transmisie de plăți în exterior.','Verifică importul și numai operațiunile permise prin contract; data, consimțământul și contractul real al băncii sunt o componentă separată.'),
'T22.14-R2-001':('Adapter Stripe la proxy de test, GET și POST/PUT/DELETE înregistrate separat.','Doar GET are drept să ajungă la adaptorul extern; verifică 0 scrieri și auditul refuzului.'),
'T212.05-R2-001':('Același contract GET pentru aliasul particular al canalului, cu trace la ruta nu doar numele părintelui.','POST/PUT/DELETE nu trebuie trimise; primirea unei sesiuni reale Stripe e o verificare externă separată.'),
'T351-R2-001':('Adapter de terminal și simulator fără încasare: citire propriu cont, mutanți de metodă; terminalul fizic și SDK extern nu sunt acoperite.','Conservă amânarea explicită din cerere; orice validare locală privește doar contractul observabil al adaptorului existent.'),
'T310-R3-001':('Două sesiuni deschid același beneficiar D107; prima schimbă rândul, a doua încearcă să salveze versiunea veche prin DialogBeneficiariD107.','Salvarea veche se refuză, valoarea primei sesiuni și numărul de rânduri persistă. Dovada instalării istorice r49 este o etapă distinctă.')}
r6t=rd(R6/'Dovezi_criterii.json')['evidence']
def fmt(x):return str(x)if x is not None else None
def intent_excerpt(c,src):
 table=src.get('original_table')or {}
 if src.get('constraint_from_own_row')and src.get('expected_structured'):return {'kind':'independent_table_fields','condition':src['constraint_from_own_row'],'expected':src['expected_structured'],'source':src['source_file'],'pointer':src['source_pointer_original']}
 if src.get('expected_structured'):return {'kind':'structured_target','condition':c['normative_content'],'expected':src['expected_structured'],'source':src['source_file'],'pointer':src['source_pointer_original']}
 literal=c['normative_content']
 # Capture the conditional relation exactly when the author specified a causal transition or output in the same clause.
 sides=re.split(r'\s*(⇒|→|->|=>)\s*',literal,maxsplit=1)
 if len(sides)==3 and len(sides[0])>=12 and len(sides[2])>=4:return {'kind':'author_explicit_transition','condition':sides[0],'expected':sides[2],'source':src['source_file'],'pointer':src['source_pointer_original']}
 if c['kind']in ['CRITERIU_FIȘĂ_C10','RZ_SURSĂ_C03']and (src.get('fixture_literals_verbatim') or src.get('native_entities_explicit')):return {'kind':'scope_and_expected_by_published_manual','condition':src.get('fixture_literals_verbatim')or src.get('native_entities_explicit'),'expected':literal,'source':src['source_file'],'pointer':src['source_pointer_original']}
 return None
def prep(c,src):
 x={};f=src.get('named_test_fixtures_in_source',[])
 if f:x['declared_test_names']=f
 if src.get('verified_symbol_entrypoints'):x['source_verified_methods']=src['verified_symbol_entrypoints'][:4]
 if src.get('versioned_paths_uniquely_resolved'):x['specific_versioned_paths']=src['versioned_paths_uniquely_resolved'][:4]
 if src.get('native_entities_explicit'):x['native_entities']=src['native_entities_explicit']
 if src.get('recipe_from_own_row'):x['author_recipe']=src['recipe_from_own_row']
 if src.get('roles_or_interfaces_named_in_source'):x['documented_roles']=src['roles_or_interfaces_named_in_source']
 if src.get('fixture_literals_verbatim'):x['literal_input_or_fixture']=src['fixture_literals_verbatim']
 if src.get('negative_inputs_verbatim'):x['negative_literals']=src['negative_inputs_verbatim']
 if src.get('environment_or_legacy_baseline'):x['historical_environment_baseline']=src['environment_or_legacy_baseline']
 return x
rows=[]
for cid,r in reg.items():
 c=todo[cid];w=meta[cid];s=r['entry_and_oracle_specific_to_case'];ref=s['source_file'];pt=s['source_pointer_original'];oc=intent_excerpt(c,s);p=prep(c,s); old=ann[cid]
 primary=r6t[c['source_evidence_id']];assert primary['sha_or_oid']==s['sha_or_git_blob']
 doc=histents.get(cid);native_case=local_forms.get(cid,[]);known=ran.get(cid,[]);aq=a03.get(cid,{});sqnames=sqlnames.get(cid,[])
 hist_authority=doc is not None and doc['question_type'] in ('method','disposition','plan','historical_delta','documentary')
 trace= list({v['suite']for v in known});scope=[];new_archive=[{'file':x['file'],'git_blob':x['blob_oid'],'line':x['line'],'relation':'fragment de document istoric recitit în R6; nu este probă runtime'}for x in old['historical_controls']]
 if cid in blocked_exact:
  category='ETAPĂ_BLOCATĂ_DE_DEFECT_REPRODUS_PE_O_ORIGINE'; basis={'direct_case':'Q-COM-01','evidence':'executie/R4_zone/A06/probe/probe-detaliu-proprietate.json','why_this_criterion':blocked_exact[cid],'branch_stops_before':['C_Order','C_Invoice','C_Payment'],'alternative':'Alte origini și comanda introdusă în ERP pot servi drept martor separat; nu înlocuiesc originea Q de pe C.'};method='Reia Q prin COMENZI+VALIDEZ cu 2 linii DTO și zero persistate; măsoară dacă apar C_Order, număr de factură și legături. Validează seller.cui prezent și absent.' 
 elif cid in local_mixed:
  category='FIXTURĂ_EXECUTABILĂ';route,benchmark=local_mixed[cid];basis={'individual_route':route,'criterion_boundary':benchmark,'distinct_external_dependency':r['resource_boundaries'],'source_declared':c['normative_content'],'quantity_is_explicit_test_fixture_not_new_owner_requirement':True};method=route+' '+benchmark
 elif cid in a03 and not str(aq['R4_classification']).startswith('NEEXECUTAT'):
  category='FIXTURĂ_EXECUTABILĂ';basis={'direct_run':aq['R4_classification'],'named_oracle':aq['R6_oracle'],'observed':aq['observed_and_expected'],'source_reports':aq['evidence_refs']};method=aq['method_and_actor']
 elif known or sqnames:
  category='FIXTURĂ_EXECUTABILĂ';basis={'direct_run_suites':trace+sqnames,'oracle_from_authored_requirement':oc,'verified_primary_fixture':p};method='Execută '+' / '.join(trace+sqnames)+' din SHA-ul sursă, pe fixtura nominală și JAR-urile distincte. Compară '+str((oc or{}).get('expected') or c['normative_content'])[:300]
 elif hist_authority:
  category='DISPOZIȚIE_SAU_DOCUMENT_ISTORIC';basis={'question_type':doc['question_type'],'direct_sources_and_constrained_ancestor_roots':doc['primary_root']+doc['documented_ancestor_roots'],'actual_records_reviewed':doc['candidate_docs_read'],'checkable_review_records':[{'path':x['path'],'sha':x['sha256'],'title':x['title'],'stamp':x['actual_lines_with_authored_decision'][0],'ancestry':x['authority']}for x in doc['documents_with_a_decision_line'][:2]],'historical_field':f'{ref} at {pt}'}
  method='Verifică în istoricul nominal '+ref+' (reper '+str(pt)+') dispoziția și revizia obiectului pentru «'+c['normative_content'][:120]+'». '+('Compară planul solicitat cu '+basis['checkable_review_records'][0]['path']+'.'if basis['checkable_review_records']else'Sunt necesare o urmă datată a deciziei și identitatea planului/ediției; o execuție în laborator nu le recreează.')
 elif oc and (s.get('executable_recipe_declared')or any(p.get(k)for k in ['source_verified_methods','native_entities','declared_test_names'])or native_case):
  category='FIXTURĂ_EXECUTABILĂ';basis={'authored_oracle':oc,'case_specific_entrypoints':p,'current_form_roles_seen':native_case,'missing_parameters_for_complete_path':r['missing_or_conditional']};method='Reproduce '+str(p.get('author_recipe')or p.get('source_verified_methods')or p.get('native_entities')or native_case)[:360]+'. Confruntă independent cu '+str(oc['expected'])[:320]+'.'
 elif oc and s.get('recipe_from_own_row')and s.get('environment_or_legacy_baseline')and s['source_pointer_original'] is not None:
  category='FIXTURĂ_EXECUTABILĂ';basis={'authored_oracle':oc,'fixture':s['environment_or_legacy_baseline'],'recipe':s['recipe_from_own_row'],'prerequisites_not_assumed':r['missing_or_conditional']};method='În '+str(s['environment_or_legacy_baseline'])[:145]+', execute «'+str(s['recipe_from_own_row'])[:260]+'» cu oracol «'+str(oc['expected'])[:190]+'».'
 else:
  category='ETALON_SAU_DATE_NERECUPERATE_DIN_SURSELE_CONTROLATE';basis={'target_sometimes_known':oc,'case_specific_entrypoint_if_any':p,'source_missing_fields':r['missing_or_conditional'],'nominal_annex_result':old['search_result'],'origin_approval_class':s['source_authority_class'],'what_is_missing_now':(['intrare sau date inițiale care permit evaluarea oracolului']if oc and not p else ['punct de acces, date ale fixturii ori valoare independentă: vezi dimensiunile lipsă nominal'] if oc else ['definiția concretă a rezultatului de acceptare și caz de refuz/verificare'])}
  method='Din «'+c['normative_content'][:180]+'», '+r['owner']+' are nevoie de '+', '.join((r['missing_or_conditional']or basis['what_is_missing_now'])[:2])+'. Compară '+ref+' la '+str(pt)+' și '+(new_archive[0]['file']+' la '+str(new_archive[0]['line']) if new_archive else 'istoricul documentelor nominale deja verificat')+'.'
 ext=r['resource_boundaries'];assert isinstance(ext['requires_external_or_hardware'],bool);rows.append({'criterion':cid,'task':w['task'],'canonical':w['canonical'],'owner':r['owner'],'source_row':{'text':c['normative_content'],'origin_type':c['kind'],'source_file':ref,'source_position':pt,'sha_or_git_blob':s['sha_or_git_blob'],'source_evidence_id':c['source_evidence_id']},'category':category,'individual_reasoning':basis,'case_method':method,'original_inputs_and_accepted_oracle':oc,'original_fixture_fields':p,'historical_reference_coverage':new_archive,'has_partial_external':ext['requires_external_or_hardware'],'external_part_if_any':ext.get('external_or_physical_part_only')or(ext.get('specific_boundary')if ext['requires_external_or_hardware']else[]),'local_work_still_available_without_external':(p.get('author_recipe')or p.get('source_verified_methods')or method),'actual_scope_run_this_round':trace+sqnames+([str(aq['R4_classification'])]if aq and not str(aq['R4_classification']).startswith('NEEXECUTAT')else[]),'independent_input_needed_from':'Titular '+r['owner']+' pentru clarificarea valorilor declarate în '+ref if category.startswith('ETALON')else None,'product_grade':None})
staticp=RP/'Masuratori_statice_nominale_R7.json'
static=defaultdict(list)
if staticp.is_file():
 for i,z in enumerate(rd(staticp)['rows']):static[z['criterion']].append({'file':staticp.relative_to(E).as_posix(),'sha':sha(staticp),'pointer':'/rows/'+str(i),'result':z['comparison'],'expected':z['expected_subcase'],'observed':z['observed_now']})
for item in rows:
 cid=item['criterion']
 if cid in static:
  item['actual_scope_run_this_round']+=['Măsurări Git sau JAR']
  item['R7_static_evidence']=static[cid]
 if cid in ('T58-R2-005','T58-R2-006'):
  ff=E/'R4_zone/A03/dovezi'/('T58_native_gate.json'if cid.endswith('005')else'T58_ZK.json')
  item['actual_scope_run_this_round']+=['REST nativ și refuz înainte de scriere'if cid.endswith('005')else'Formă ZK și buton dezactivat']
  item['R7_native_supplement']={'source':ff.relative_to(E).as_posix(),'sha':sha(ff)}
by=Counter(q['category']for q in rows);bext=Counter(q['category']for q in rows if q['has_partial_external']);assert len(rows)==1587 and sum(bext.values())==45
wr(RP/'Clasificare_nominala_1587.json',{'original_R6_sha':sha(R6/'A12_raport.json'),'classifier_basis':'Lectură par critère de la source primaire hachée, de la nature de la disposition, des champs de table (valeur/recette/fixtură), des essais nommément retrouvés et des anomalies dont le chemin a un témoin nominal. Un thème ou mot isolé n’établit pas la classe. Un seuil connu avec données de départ absentes reste identifié comme tel. Les parties extérieures sont orthogonales.','cohort':1587,'local_only':1542,'partial_external':45,'classification_counts':by,'partial_external_by_class':bext,'records':rows});print(by,bext)

