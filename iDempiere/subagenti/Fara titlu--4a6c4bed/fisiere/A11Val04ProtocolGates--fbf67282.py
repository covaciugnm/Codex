import pathlib,json,hashlib,gzip,zipfile,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';O=B/'A11/Val04_preflight';G=B/'A05_G3_nativ_lot04';F=B/'A08_Storefront_catalog_lot04'
def raw(p):return p.read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
def oid(p):b=raw(p);return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def write(p,d):assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
checks=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'details':d});assert b,(n,d)
gp=G/'Protocol_G3_nativ_v2.json';fp=F/'Protocol_A08_catalog_v1.json';g=j(gp);f=j(fp)
ck('G3 protocol exact',sha(gp)=='7e214b85565bb51185511b8788a0c5ad4da1bba3b3b92e8995d38598ed201e99')
ck('frontend protocol exact',sha(fp)=='f04a2c9de4abe00b7bbf541e0526e71a89196d2a8ca2f74bb79fb1a9dd99c688')
mp=G/'MANIFEST_protocol_G3_v1.json';ck('G3 base manifest',sha(mp)=='fdcae522550e57a8d1466fe7e294bb66c478ea6d3a6b0d1d61a91f06aafab4a3')
for x in j(mp)['files']:
 p=G/x['path'];ck('manifest '+x['path'],sha(p)==x['sha256'] and len(raw(p))==x['bytes'])
gi=j(G/'Identitati_lectura_G3_v1.json');fi=j(F/'Identitati_v1.json')
cat={}
want={x['path'] for x in gi['sources']}|{x['path'] for x in fi}
with gzip.open(R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf8') as z:
 for ln in z:
  x=json.loads(ln)
  if x['path'] in want:cat[x['path']]=x
ck('catalog20paths',len(cat)==len(want)==20)
for x in gi['sources']:
 p=G/'surse_df85'/x['path'].split('/src/com/eva/ro/contab/')[1]
 ck('G3 source '+x['path'],sha(p)==x['sha256'] and oid(p)==x['oid'] and x['oid'] in str(cat[x['path']]))
for x in fi:
 p=F/'Sources'/x['path'];ck('frontend source '+x['path'],sha(p)==x['sha256'] and oid(p)==x['git_oid'] and x['git_oid'] in str(cat[x['path']]))
ck('two identical JS copies one blob',raw(F/'Sources'/f['identities'][0]['path'])==raw(F/'Sources'/f['identities'][1]['path']))
for item in [gi['eva_jar'],gi['native_core']]:
 p=pathlib.Path(item['path']);ck('binary '+p.name,sha(p)==item['sha256'] and ('oid' not in item or oid(p)==item['oid']))
with zipfile.ZipFile(gi['eva_jar']['path']) as z:
 for x in gi['sources']:ck('EVA class '+x['class_entry'],hashlib.sha256(z.read(x['class_entry'])).hexdigest()==x['class_sha256'])
with zipfile.ZipFile(gi['native_core']['path']) as z:
 for x in gi['native']:
  ck('native sourcecache '+pathlib.Path(x['source_cache_path']).name,sha(pathlib.Path(x['source_cache_path']))==x['source_sha256'])
  ck('native class presence '+x['class_entry'],(x['class_entry'] in z.namelist())==x['class_present'])
  if x['class_present']:ck('native class bytes '+x['class_entry'],hashlib.sha256(z.read(x['class_entry'])).hexdigest()==x['class_sha256'])
for x in g['references']:ck('G3 anchor '+x['path'],sha(R/x['path'])==x['sha256'])
ck('10 unique G3 cases',len(g['G06_cases'])==len({x['id'] for x in g['G06_cases']})==10)
ck('10 unique frontend cases',len(f['cases'])==len({x['id'] for x in f['cases']})==10)
ck('frontend functional correction explicit',f['mapping']['functional']==['A08-P02','A08-C19','D10'] and f['mapping']['not_executed']==['A08-P07'])
pre=O/'Verdict_A11_aplicabilitate_R12_0143_v1.json';ck('population gate fixed',sha(pre)=='0c16fd002cb11ffb0acc5e374e5cc5ce2327c9007ca93d4e0326042a2a05fc4d')
nf=G/'Fise_plan_G3_v1.json';ck('G3 nominal plans',sha(nf)=='675eb97f4349d84853cd3c9e003c002a502c27108fd5f32bd7329a4b2b9f3a66')
qa=O/'QA_A11_identitati_protocoale_Val04_v1.json';write(qa,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'product_executions':0,'method':'Local rehash/source Git blob identity/catalog comparison and ZIP class inspection; no classes loaded or application executed. Native source cache explicitly differs from core13; actual bytecode reviewed.'})
grows=[
 ('G01','Identitate și proveniență',['df85 și poarta populației fixate','13 surse Git originale/OID și catalog verificate','EVA JAR și clase individuale originale verificate','Core13 exact și diferența față de surse cache declarată','Sursa/bytecode/runtime/context nu sunt echivalate']),
 ('G02','Obiectiv și nivel',['SO/PO distincte pentru disponibilul de vânzare','D04/V03-N04 și același defect SQL existent','Fără transfer N05 sau dublare defect','Fără DocAction/C_Order/Fact_Acct','Task nominal încă neatribuit și zero închidere']),
 ('G03','Actor și legare',['Context GardenAdmin de laborator explicit','ServerContext și proprietatea fixturei verificate înainte de business','Servicii native OSGi/DB originale','EVA/UI/server RESOLVED și inventar handler relevant','Hook-uri null și clase încărcate cu SHA']),
 ('G04','Schemă și pregătire',['Seed sintetic nou și hash verificat','Schema fizică/AD/PK/FK/indici necesari reconciliați înainte business','LastBuildInfo/FailOnBuildDiffer nu probează schemă','Fără auto-migrare ca să obțină PASS','Refuz schema/serviciu/context divergente']),
 ('G05','Cale originală și oracol',['MStorageReservation.add/getCreate/saveEx originale','Ordine argumente product/warehouse explicită','RezervareStoc.disponibil original cu SQL neschimbat','Sursa EVA persistată/citită original și stoc/surse/formulă originale','Termeni T22/seturi/reguli zero confirmați']),
 ('G06','Martori și contraexemple',['SO2/PO0 pozitiv','PO5 și PO15 doar factor schimbat','PO fără SO separat','Depozit/produs/client parametrizat fără rânduri interclient invalide','IsActive/ASI/floor diferențe caracterizate']),
 ('G07','Persistență și tranzacție',['Readback conexiune separată readonly','Rânduri brute chei și argumente jurnalizate','Rollback cere zero rând PO, nu doar sumă zero','Retry postrollback un singur rând, fără pretenție idempotență postcommit','Niciun efect contabil dedus din counts']),
 ('G08','Izolare și resurse',['Cluster loopback propriu port56455 numai dacă liber','GardăJDK și7canari înainte produs','Schedulere/endpoints/tokenuri neutralizate','finally închideTrx/JVM/PG și verifică procese/port','Cleanup refuzat se păstrează, fără ocolire']),
 ('G09','Interpretare și nativ',['getQtySO nu include PO','Native getQty fără client/IsActive nu se substituie orbește','ASI0 toate și normalizare ASI verificată prin persistare','LocatorType rezervabil condiționează baza comparabilă','Schema/cache/source mismatch rămâne limită documentată']),
 ('G10','Recepție și limite',['Predicțiile de defect nu sunt PASS de produs','10 scenarii și subevaluări numărate distinct','Fișe pe metode/binding/lectură distincte','PeerA06 repartizat nu pretins executat','RecepțieA11 după probe;17contracte rămân deschise'])]
frows=[
 ('F01','Identitate',['df85 și poarta populației fixate','7 căi originale cu SHA/OID/catalog','2 căi JS identice reprezintă un singur blob','Script integral fără expunerea IIFE/modificări','Template și servlet doar citire']),
 ('F02','Obiectiv și mapare',['P02/C19/D10 funcțional','Subcontrol starefiltru/cerere/rezultate explicit','C27 proveniență numai','P07 reconciliere ERP neexecutat','Task SHARED fără atribuire inventată']),
 ('F03','Actor și intrare',['Vizitator public fără sesiunea utilizatorului','Context nou per scenariu','Selectori din templatele originale','Click/submit reale','Valoare input fixture plus Enter; debounce declarat în afara acestei subprobe']),
 ('F04','Oracol',['Produse cu identități sintetice distincte pe A/B/C','Captură cereri page/category/q','Titlu/filtru/carduri și lipsa răspunsului coerente','Mesaj de eroare separat de zero produse','Concurență blocată ori ultima intenție satisfăcută']),
 ('F05','Pozitive',['Paginare2 apoi3','Categorie secvențialăA/B','Zero rezultate legitim apoi recuperare','Dubluclick doar cererea înzbor','RecuperareC după succes separată de blocaj permanent']),
 ('F06','Negative',['Abortfetch','JSONinvalid','HTTP500JSON','CategorieB în timpulA','CăutareB în timpulA']),
 ('F07','Determinism',['CerereA ținută pending cu barieră explicită','Al doilea eveniment înaintea eliberăriiA','Așteptare finală bounded și log toate cererile','No hiddenIIFEcall sau patchloading','Nu număra aceeași recuperare în două cazuri']),
 ('F08','Izolare',['HTTP(S)interceptate, restabort','Host sintetic audit.invalid','Fără cont/comenzi/retur/date reale','Contexte/browser închise finally','LocalStorage efemer separat de DB']),
 ('F09','Calificare',['SimularefrontierăHTTP dar JSoriginal','Fără APIJava/Python real','Fără disponibilG3ERP sau UI ZK','ScreenshotDOMfuncțional fără designresponsive pretins','Întregfișiernevalidat chiar dacă încărcatintegral']),
 ('F10','Raport și resurse',['10 scenarii, evaluări/retrydistincte','Source/runner/DOM/capturi/hash păstrate','Calibrareharness separată de produs','Recomandareadapteazăfetch/stareexistentă','Recepțieindependentă ulterioară;17contractedeschise'])]
def rubric(rows):return [{'category':c,'name':n,'subchecks':[{'id':c+'.'+str(i+1),'check':t,'accepted_for_protocol':True} for i,t in enumerate(v)]} for c,n,v in rows]
common={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','candidate':'df85d33c1648ce2b2df130a60a05ef696e2e5480','prior_population_gate':ref(pre),'identity_QA':ref(qa),'method':'Independent reading and identity checks only; protocol acceptance authorizes exact bounded execution with runtime prerequisites. It is not evidence that runtime prerequisites or product cases have already passed.','quality_score_protocol':10,'subchecks_satisfied':50,'subchecks_total':50,'product_score':None,'full_audit_score':None,'whole_file_or_task_closed':0,'open_contracts':17,'product_executions_by_reviewer':0,'operational_writes':0}
go={**common,'protocol':ref(gp),'rubric':rubric(grows),'decision':'ACCEPTAT10/10 pentru protocolul limitat G3 nativ. Se poate restaura clona proprie și efectua preflightul; business numai după toate condițiile G01/G03/isolation satisfăcute și consemnate.',
 'mandatory_conditions':['Nu reutiliza working tree8c0695de sau fixturile N05. Surse/JAR df85 și core exact.','Toate scrierile de produs și ownership ale fixturilor trec prin PO/API native. Sintagma transfer ownership din protocol se limitează la permisiuni ale laboratorului și neutralizarea seedului; nu autorizează mutarea produselor/depozitelor între clienți prin SQL direct.','F02 cu client inexistent este probă de limită a cititorului, nu autentificare/IDOR validată. Sursa citită pentru client greșit trebuie separată de configvalidă parametrizată.','Record de invocare cu numele fiecărui argument; produs și warehouseID distincte pentru control. ASI adevărat și AttributeSet valid; readback și normalizareaASI0 separate.','RândulPO creat necomis trebuie să lipsească integral din conexiunea separată și dupărollback; ID/UUID consumat nu trebuie reciclat.','Hook-uri null înainte/după și termenii auxiliari0 verificate în fiecarecaz; orice abatere oprește/nuconfirmăcauzalitatea.','Inventar nominal al handlerelor/validatorilor relevanți și schema efectivă înaintebusiness. Nicio gardă relevantă omisă pentru a forța succes.','Constatarea nouă poate extinde R12-STOC-SO-PO-01; nu crește numărul unic de defecte pentru aceeași cauză.','Nu folosi postrollbackretry drept idempotență dupăcommit; Fact_Acct/DocAction și canalcomplet rămân neexecutate.'],
 'source_scope':{'EVA_source_paths_read':13,'source_cache_native':7,'native_classes_present':5,'native_classes_absent':2,'nominal_source_plans':ref(nf),'prospective_case_identities':10,'actual_execution_credit':0}}
fo={**common,'protocol':ref(fp),'rubric':rubric(frows),'decision':'ACCEPTAT10/10 pentru protocolul limitat al catalogului JS original pe DOM sintetic. Execuția poate începe cu aceste condiții, fără test pe site operațional.',
 'method_amendment':'Precizarea executorului A08 este acceptată: valoarea inputului se pregătește ca fixture fără eveniment input, apoi Enter real produce submit; astfel debounce280ms nu creează o cerere suplimentară ascunsă. Logul declară această pregătire și faptul că interacțiunea de tastare/debounce nu este exercitată. Nu se modifică scriptul/IIFE.',
 'mandatory_conditions':['Păstrează evenimentul click/Enter real; nu apela funcțiafetchProductsprin hook adăugat și nu reseta artificial state.loading.','DOMminimal include mesajele/etichetele necesare din contractul de template (sau text sintetic non-gol explicit); pozitivulS03 confirmă mesajulzero valid. Lipsa accidentală a labelului înfixture nu se impută produsului.','S01include gridinițial/page1 declarat; verifică page2/page3, cardID și cantități, fără APIreal.','N04/N05 folosesc barieră: cerereA capturată, evenimentB, eliberareA. Înregistrează toate cererile și așteaptă bounded dupăB; un timeout alharnessului nu este singur dovadă de defect.','S05 recuperareC poate avea două subtrasee, dar rămâne o identitateprotocol; dacă un subtraseu este folositcaassert înN04/N05, nu dubla executările în statistici.','DOM/capturi trebuie să arate filtru/titlu/IDproduse distincte și erorileJavaScript; browserulascuns seînchide înfinally.','C27reprezintă numai identitateblob/template; nu versiuneactivă de site dovedită. P07 rămâneNEEXECUTAT, înciuda repartizării istorice.','Dacă ambele căiJS suntcreditate, trebuie indicate caaceeași execuție peblobequal, nu douăfișiere rulate separat. Template/servlet lectura fărăcreditruntime.','Nu concluziona defect globalERP/API/securitydin aceste răspunsurisintetice; severitatea secalifică pentru componentă/condiții.'],
 'source_scope':{'source_paths_verified':7,'original_JS_blob_to_execute':1,'equal_JS_paths':2,'static_context_paths':5,'prospective_case_identities':10,'actual_execution_credit':0}}
for name,out in [('G3_nativ_v2',go),('frontend_catalog_v1',fo)]:
 p=O/('Verdict_A11_protocol_'+name+'.json');write(p,out);seal=O/('SIGILIU_A11_protocol_'+name+'.json');write(seal,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(p),ref(qa)],'immutable':True});print(json.dumps({'verdict':ref(p),'seal':ref(seal)},ensure_ascii=False))
runner=O/'Runner_A11_protocoale_Val04_v1.py';assert not runner.exists();runner.write_bytes(pathlib.Path(__file__).read_bytes());print('QA',json.dumps(ref(qa)),len(checks))
