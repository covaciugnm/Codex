import pathlib,json,hashlib,datetime,collections,re
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');G=R/'executie/R12_fisiere/A05_G3_nativ_lot04';O=R/'executie/R12_fisiere/A11/Val04_loturi'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
def write(p,d):assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[];references=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'detail':d});assert b,(n,d)
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):
   q=pathlib.Path(x['path']);p=q if q.is_absolute() else R/q if x['path'].startswith('executie/') else G/'surse_df85'/x['path'].split('src/com/eva/ro/contab/')[1] if x['path'].startswith('idempiere/') else G/q
   ck('reference '+x['path'],sha(p)==x['sha256'] and ('bytes' not in x or p.stat().st_size==x['bytes']));references.append(ref(p))
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=G/'MANIFEST_A05_G3_nativ_lot04_v1.json';rp=G/'Raport_A05_G3_nativ_lot04_v1.json';fp=G/'Fise_G3_final_v1.json'
for p,h in [(mp,'4bd069621d27559943683fd7162bf906343b332c2f0af8aa316e346327b25410'),(rp,'ef97e27d2fa2b0913156c9837e0af9e59073f07755c3ed51299dbc14e46f9f8e'),(fp,'a05a418cd88b985540792896693fe26bad035e99babe18a8eb156a0e9fe50533')]:ck('sealed '+p.name,sha(p)==h)
for p in [mp,rp,fp,G/'QA_autoverificare_G3_v1.json']:walk(j(p))
ck('156 immutable artifacts',len(j(mp)['files'])==156 and len({x['path'] for x in j(mp)['files']})==156)
d=j(rp);f=j(fp);protocol=j(G/'Protocol_G3_nativ_v2.json');oracle=j(G/'Oracle_independent_G3_v1.json');final=j(G/'Readback_final_G3_v1.json')['rows']
ck('10 unique protocol cases',len(d['cases'])==len({x['id'] for x in d['cases']})==10 and {x['id'] for x in d['cases']}=={x['id'] for x in protocol['G06_cases']})
actual=[]
for v in [2,3]:actual.extend(x for x in (G/f'business_g3_v{v}.stdout.txt').read_text(encoding='utf-8-sig').splitlines() if x.startswith('CASE_G3|'))
ck('16 actual observations distinct from ten scenarios',len(actual)==16 and actual==oracle['actual_java_outputs'])
ck('41 valid plus one setup snapshot',len(oracle['captures'])==41 and sum(len(j(G/f'business_g3_v{v}.json')['readbacks']) for v in [2,3])==41 and len(j(G/'business_g3_v1.json')['readbacks'])==1)
ck('valid observation exit semantics',j(G/'business_g3_v1.json')['exit']==1 and j(G/'business_g3_v2.json')['exit']==1 and j(G/'business_g3_v3.json')['exit']==0)
ck('no case on initial setup',not re.search('^CASE_G3\\|',(G/'business_g3_v1.stdout.txt').read_text(encoding='utf-8-sig'),re.M))
for key,n in [('products',14),('warehouses',12),('sources',12),('reservations',23),('stock',13),('attribute_set',1),('attribute_instance',2)]:ck('final raw count '+key,len(final[key])==n)
ck('auxiliary final counts',final['auxiliary']==[{'order_lines':0,'site_lines':0,'fixture_facts':0,'global_fact_count':308}])
ck('rolled back UUID absent',all(x['m_storagereservation_uu']!=oracle['rollback_uuid_absent_final'] for x in final['reservations']))
ck('IsActive updateability explicit',next(x for x in final['reservation_metadata'] if x['columnname']=='IsActive')['isupdateable']=='N')
ck('trace log presence not zero delta',any(x['table_name']=='m_storagereservationlog' for x in final['trace_table']) and any('delta sa nu a fost capturată' in x for x in d['limits']))
before=j(G/'Schema_G3_inainte_v1.json');after=j(G/'Schema_G3_dupa_v1.json')
for key in ['table','columns','physical','constraints','indexes']:ck('schema unchanged '+key,before['rows'][key]==after['rows'][key])
ck('13 unique source dispositions',len(f)==len({x['path'] for x in f})==13)
cc=collections.Counter(x['coverage_class'] for x in f);ck('6 methods 3 binding 2 constants 2 static',cc=={'METODA_ORIGINALA_APELATA_LIMITAT':2,'TRASEU_TRANZITIV_LIMITAT':4,'FIXTURE_BINDING':3,'CONSTANTE_METADATE_FARA_CREDIT_EXECUTIE':2,'LECTURA_STATICA':2})
counter=O/'Contraoracol_A11_G3_readback_v1.json';binding=O/'QA_A11_G3_binding_readiness_v1.json';ck('A11 own oracle',sha(counter)=='af929b5b9d91da2dec6b7f67fd1b5eccf1dfee4452777e0f51421d5ab3f01756' and len(j(counter)['checks'])==192);ck('A11 binding QA',sha(binding)=='5853332a4633f255685f4a8c880eabf3ad024933d5e9b73cf61b4b8edcc02115' and len(j(binding)['checks'])==524)
native_by_name={
 'RezervareStoc':'DB/Trx native; SQL_STOC, SQL_REZ_NATIVA, SQL_REZ_T22; SetLista pentru termenul gol. MStorageReservation a scris fixturea, nu acest cititor.',
 'FisaCanalProces':'PO persistent EVA_SursaSite și DB/Trx; sursa/stoc/surse/brut/stocArticol. Nu doIt, AD_Process, jurnal sau publicare.',
 'FisaCanalCalcul':'Calcul pur stocCalculat pe valorile primite; fără query ori PO.saveEx direct.',
 'RegulaStocCanal':'Calcul pur cantitateOferita cu reguli goale; fără query ori PO.saveEx direct.',
 'SetLista':'Interogări originale pentru non-BOM și colecții absente; fără alocare efectivă pe componente sau seturi S1/S2.',
 'TabelaFisaCanal':'reguliStoc cu canal null întoarce Map.of înaintea query-ului; fără citirea ori persistarea regulilor de canal.',
 'EvaWmsGardaEvents':'Inițializare/abonare EventManager originală, context de fixture; nu recepție integrală a ramurilor de gardă.',
 'EvaStocEvents':'Inițializare/abonare originală; nu postare, costare sau credit pentru ramura eventuală de modificare a depozitului.',
 'EvaAuditPostareEvents':'Inițializare/abonare originală; fără AD_PInstance ori postare executată în G3.',
 'DomeniiT22':'Constante de referință; fără execuție independentă creditată.',
 'FluxTabele':'Constante de nume; fără execuție independentă creditată.',
 'TipGestiune':'Lectură statică; ramura wildcard neexecutată.',
 'EvaActivator':'Lectură statică a legăturilor; activatorul integral nu a pornit.'}
dispositions=[]
for x in f:
 name=pathlib.PurePosixPath(x['path']).stem;level=x['coverage_class'];method=level in ['METODA_ORIGINALA_APELATA_LIMITAT','TRASEU_TRANZITIV_LIMITAT'];bind=level=='FIXTURE_BINDING'
 dispositions.append({'path':x['path'],'oid':x['oid'],'sha256':x['sha256'],'authoritative_state':'NATIVE_METHOD_PARTIAL' if method else 'NATIVE_BINDING_PARTIAL' if bind else 'STATIC_ONLY_NO_EXECUTION_CREDIT','accepted_coverage_class':level,'method_scope':x['method_scope'],'authoritative_native_method_and_effect':native_by_name[name],'full_file_accepted':False,'owner':'A05','planned_peer':'A06','actual_peer':'A11 independent limited receipt','input_fiche_state_is_stale':True})
for name in ['A11G3Counteroracle.py','A11G3Bindings.py','A11G3Receipt.py']:
 p=O/('Runner_'+name);write_check=not p.exists();ck('new runner '+name,write_check);p.write_bytes(pathlib.Path('D:/CodexWork',name).read_bytes())
qa=O/'QA_A11_G3_manifest_reconciliation_v1.json';write(qa,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'reference_instances':len(references),'unique_reference_paths':len({x['path'] for x in references}),'metadata_corrections':'Starea moștenită de plan și câmpul native_method generic sunt calificate explicit în verdict; nu modificăm fișele sigilate.'})
out={'schema':'A11.R12.Val04.G3.receipt.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','head':d['head'],'report':ref(rp),'manifest':ref(mp),'fiches':ref(fp),'qa':ref(qa),'binding_qa':ref(binding),'counteroracle':ref(counter),'next_checklist':ref(O/'Checklist_A11_dupa_R12_Val04_v1.json'),
 'decision':'RECEPȚIE LIMITATĂ ACCEPTATĂ: dovada nativă întărește constatarea SO/PO deja existentă. Nu reprezintă recepție integrală de G3, fișier, task, frontend/backend sau produs.',
 'finding':{'id':'R12-STOC-SO-PO-01','status':'CONFIRMAT_PE_API_PO_NATIVE_SI_CITITORI_ORIGINALI; NEREZOLVAT','new_duplicate_findings':0,'cause':'Ambele citiri EVA însumează Qty pentru rezervările native active fără a separa IsSOTrx. PO sunt astfel deduse din disponibilul pentru vânzare.','critical_witness':'Același stoc cantitativ 10 și același rând SO=2, cu UUID și cantitate neschimbate. PO 0→5→15 produce nativ 8→8→8; RezervareStoc 8→3→−7 și FisaCanal 8→3→0.','persistence':'Rezervările există după commit în tabela nativă și sunt recitite pe conexiuni readonly distincte. Valorile EVA sunt rezultate ale cititorilor; nu s-a persistat sau publicat fișa canalului.','native_first':'Adaptează cititorii existenți la semantica MStorageReservation pentru rezervările SO. Păstrează explicit ownership/client, IsActive, ASI, politica locatorului, floor/clamp și termenii auxiliari. Fără tabelă nouă de stoc și fără înlocuire oarbă cu getQtyAvailable.'},
 'scenario_dispositions':d['cases'],
 'counts':{'protocol_scenarios':10,'successful_observation_lines':16,'valid_readonly_snapshots_v2_v3':41,'initial_setup_only_snapshot':1,'final_readback_is_separate':True,'A11_numeric_comparisons':13,'A11_counteroracle_predicates':192,'A11_binding_predicates':524,'EVA_sources':13,'limited_methods':6,'fixture_binding':3,'constants_no_execution_credit':2,'static_only':2,'whole_files_accepted':0,'tasks_accepted':0},
 'source_dispositions':dispositions,
 'authoritative_metadata_clarifications':['Toate cele 13 fișe au rămas cu state=LECTURA_PENTRU_PROTOCOL_FARA_EXECUTIE din plan. Pentru recepție se folosesc dispozițiile nominale din acest verdict și result/coverage_class, nu acel literal vechi. Nu se rescriu fișele.','native_method și persistent_effect generice nu se propagă ca execuție directă pentru toate fișierele. Calc în FisaCanalCalcul/RegulaStocCanal este pur; TabelaFisaCanal pe canal null nu face query.','A06 este peer planificat; nu există o recenzie A06 nouă revendicată de acest lot. Recenzia efectivă aici este A11.','Mesajele intermediare care au indicat 17 linii CASE_G3 erau greșite. Logurile și oracolul sigilat au corect 16 (6+10). Nu se schimbă numărul de 10 scenarii.'],
 'rejected_extrapolations':['F02 nu validează login, RBAC, IDOR sau izolarea între doi clienți reali; folosește client inexistent și ownership sintetic.','F03 este caracterizare de politică: PO nou permite N înainte de saveEx; setterul pe rând persistent este readonly. Nu este defect nou și nu dovedește un flux comercial de inactivare.','Rollback/retry nu este idempotență după commit; UUID nou după anulare confirmă tocmai o creare nouă.','Nu DocAction/C_Order, costuri, Fact_Acct validat, UI, API/publicare ori canale concurente. Count global 308 și zero facts pentru fixture nu sunt solduri contabile.','Nu recepție integrală de seturi, CPP/CPA, perechi G1/G2 sau capacitate comună.','Nu delta zero demonstrată pentru M_StorageReservationLog: nu s-a măsurat delta acestei tabele.'],
 'calibrations':{'executor':['Compilare harness: throws SQLException absent, fără execuție produs.','business_v1: oracol de cheie numerică inexistentă, înainte de rezervări; setup păstrat.','business_v2 F03: așteptare eronată de modificare IsActive pe rând readonly; cazurile precedente rămân valide, continuarea are addendum anterior.'], 'A11':['Verificatorul de metadata a folosit inițial cheia oid în loc de git_object, apoi aștepta dict în loc de lista counts. Două opriri înaintea fișierului QA, corectate numai în cititorul de metadata; zero execuții de produs. Un print diagnostic pe Windows cp1252 a eșuat înainte de afișare și a fost reluat cu UTF-8.','Prima versiune de runner metadata este păstrată separat. Contraoracolul Decimal a trecut la prima execuție.']},
 'reproducibility_limit':'Harnessul de continuare păstrează ID/Value din această rundă, iar modul business include vechiul F03. În runda următoare se reconstruiesc fixturele și se descoperă identitățile nou create; nu se rulează orbește continuarea pe alt seed. Aceasta limitează reutilizarea automată, nu infirmă probele sigilate.',
 'resources':{'executor_cleanup':ref(G/'Cleanup_final_v1.json'),'A11_independent_check':j(binding)['resources_independent_snapshot'],'passive_caches_and_harness_retained':True,'previous_six_denied_cleanup_roots_untouched':True,'A11_operational_writes':0,'global_zero_residue_claim':False},
 'open_contracts':17,'product_score':None,'global_audit_score':None}
vp=O/'Verdict_A11_G3_nativ_lot04_v1.json';write(vp,out)
seal=O/'SIGILIU_A11_G3_nativ_lot04_v1.json';write(seal,{'utc':out['utc'],'immutable':True,'files':[ref(vp),ref(qa),ref(binding),ref(counter),*[ref(O/('Runner_'+n)) for n in ['A11G3Counteroracle.py','A11G3Bindings.py','A11G3Receipt.py']],ref(O/'Runner_A11G3Bindings_calibrare_v1.py')]})
print(json.dumps({'verdict':ref(vp),'seal':ref(seal),'checks':len(checks)},ensure_ascii=False))
