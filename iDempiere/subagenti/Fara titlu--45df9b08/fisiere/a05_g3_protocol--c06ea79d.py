from pathlib import Path
import json, hashlib, datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A05_G3_nativ_lot04'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):
 p=R/p;return dict(path=p.relative_to(R).as_posix(),sha256=sha(p))
def save(n,x):
 p=O/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8');return sha(p)
ident=json.loads((O/'Identitati_lectura_G3_v1.json').read_text(encoding='utf8'))
p={
 'schema':'A05.G3.native.protocol.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','state':'PROPUS A11; ZERO PG/RUNTIME/PRODUS EXECUTAT',
 'owner':'A05','peer':['A06','A11'],'requirement':'V03-N04 / D04 disponibilitate G3 comună; SO și PO native distincte',
 'task':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING',
 'finding_existing':'R12-STOC-SO-PO-01; extindere nativă a aceleiași constatări SQL, fără defect duplicat',
 'references':[
  ref('executie/R12_fisiere/A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json'),
  ref('executie/R12_fisiere/A11/Val03_loturi/Verdict_A11_G3_SQL_lot04_v1.json'),
  ref('executie/R12_fisiere/A06_Rezervari_nativ_lot04/MANIFEST_A06_rezervari_lot04.json'),
  ref('executie/R12_fisiere/A06_Rezervari_nativ_lot04/Clarificare_semantica_disponibil_v1.json'),
  ref('executie/R12_fisiere/A05_N05_lot03/MANIFEST_A05_N05_lot03_v1.json'),
  ref('executie/R12_fisiere/A05_N05_lot03/Anexa_reproducere_N05_v1.json'),
  ref('executie/R12_fisiere/A05_N05_lot03/Cleanup_final_v1.json'),
  ref('executie/R12_fisiere/A05_G3_nativ_lot04/Identitati_lectura_G3_v1.json')],
 'scope':{
  'included':'Rezervări reale în M_StorageReservation create de modelul nativ, apoi cititorii originali EVA și formula originală. Persistență nativă/SQL independent/rollback/retry. Nu tabelă substitut.',
  'not_included':['N05 neschimbat nu se rerulează','Nu DocAction, C_Order/C_OrderLine, pregătire/completare comandă sau Fact_Acct','Nu procesul FisaCanalProces.doIt/AD_Process integral; doar sursa și metoda stoc originale','Nu UI/login/API HTTP/site/click real','Nu dubla scădere site+comandă nativă în această poartă','Nu recepție D04 complet: concurență canale, seturi S1/S2, mai multe G1/G2 și G3 comun rămân deschise'],
  'preserved_architecture':'G2 necontabil; nicio creare de stoc contabil G2. CPP/CPA distincte; cod intern permanent independent SKU/EAN; cutii/manoperă o singură dată G1; G3 calculează capacitatea comună. Niciuna nu este recepționată automat de acest test.'},
 'G01_identity_schema':{
  'sources':'surse_df85: cat-file la OID exact; Git JAR OID4a5e399ebc671569098235c6ec6d151defd20be6 SHA82099cd7f436a8fb4d532d8a46b83c62ae0e0176d86d9345c08598299d01d558; working tree operațional exclus.',
  'native_core':ident['native_core'],
  'source_binary_difference':'Cache-ul surselor native conține StorageValidatorProvider/IStorageValidator și apeluri din addQty absente în JAR-ul core13 recepționat. Autoritate pentru execuție: javap și SHA clasei originale din JAR, salvate native_bytecode. Nu se adaugă sau simulează providerul lipsă; nu se prezintă sursa cache drept build identic.',
  'native_actual_add':'add(ctx, warehouse, product, ASI, diffQty, isSOTrx, trx, IReservationTracer): zero/null diff return true; normalizează ASI=0 când produsul nu are atribute de instanță; getCreate creează prin constructor/PO.saveEx; AdempiereDatabase.forUpdate; addQty actualizează Qty/Updated/UpdatedBy nativ, reload, apoi trace numai dacă tracer != null.',
  'tracer':'Se transmite null explicit, overload tipizat IReservationTracer. Este fixture PO/API nativ, fără document și fără înregistrare M_ReservationTrace. Se recitește schema/tabela de trace dacă există și se consemnează lipsa delta aferentă fixturei; niciun credit pentru tracer de comandă.',
  'seed':'GardenWorld-A07.dump SHA54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4, clienți0/11, seed sintetic; restaurare nouă, fără stocurile N05.',
  'build':'Releaseno13/version2026-03-09; LastBuildInfo placeholder și FailOnBuildDiffer=N păstrate și declarate. isBuildOK nu dovedește schema. Diferențele cache/core sunt limitate prin bytecode exact; orice mismatch pe câmp folosit oprește business.',
  'schema_tables':['AD_System','AD_Client','AD_Org','AD_User','AD_Role','AD_User_Roles','AD_Table','AD_Column','AD_ModelValidator','M_Product','M_Product_Category','C_UOM','C_TaxCategory','M_Warehouse','M_Locator','M_LocatorType','M_StorageOnHand','M_StorageReservation','M_AttributeSet','M_AttributeSetInstance','EVA_SursaSite','EVA_ComandaSite','EVA_ComandaSiteLinie','PP_Product_BOM','PP_Product_BOMLine'],
  'schema_acceptance':['Schema fizică/AD tipuri, coloane, null/default/PK/FK/indexuri pentru exact citirile/PO atinse; M_StorageReservation unicitate warehouse/product/ASI/IsSOTrx și coloane Qty/IsActive/AD_Client_ID/UpdatedBy.',
   'Confruntă I_M_StorageReservation, I_M_AttributeSet, I_M_AttributeSetInstance, I_M_LocatorType din core-ul exact plus coloanele consumate de EVA. Diferențe nefolosite rămân limită, nu schimbări artificiale.',
   'Schema sursei EVA și a tabelelor site/set citite de query trebuie să existe, chiar dacă nu conțin rânduri pentru fixture. Nu se înlocuiesc cu tabele reconstruite.',
   'Nu rula EvaMetadata automat și nu modifica schema ca să obții PASS. Lipsă dependentă → diagnoză și addendum A11 înainte de activare/modificare.'],
  'preconditions_before_business':['A11 aplicabilitate Val04 + gate concret10/10','Hash seed/core/EVA/cache neschimbat','Canari7 trecuți','Readiness schema/context/binding și revalidare în aceeași JVM cu business','Fixture PO validă, ownership real verificat și termeni T22/seturi zero confirmați independent']},
 'G03_normal_path_binding':{
  'actor':'GardenAdmin user101/role102, client11/org11. Context nativ ServerContext pe thread; este parametrizare de laborator, nu login sau recepție RBAC.',
  'fixture_path':'MProduct/MWarehouse/MLocator/MAttributeSet/MAttributeSetInstance.saveEx; MStorageOnHand.add pentru bază sintetică; MStorageReservation.add→getCreate→PO.saveEx și UPDATE nativ original. PO generic MTable.getPO pentru sursa EVA_SursaSite cu endpoint gol și toate trimiterile dezactivate.',
  'normal_reader_A':'Apelanții operaționali citesc RezervareStoc.disponibil(client,product,warehouse,excludedOrder,trx); testul apelează exact metoda publică, fără substituție SQL/suma.',
  'normal_reader_B':'FisaCanalProces.sursa(client,sourceId,trx) original citește PO persistent → stoc(ctx,client,RandSursa,canal,product,trx) original → surse original → stocCuSet→stocArticol→FisaCanalCalcul.stocCalculat→RegulaStocCanal.cantitateOferita. Harness folosește reflection numai pentru metodele package-private, nu modifică câmpuri/logică.',
  'configuration':'Sursă sintetică persistentă cu EVA_GestiuniStoc=ID-ul unic al depozitului, rezervă0, canal null (calea originală fără reguli), sursa unică A05G3..., scriere/fisă/stoc spre site=false. Nicio conexiune externă. RandSursa nu este o dublă injectată, ci rezultatul sursa original.',
  'raw_observation':'Se apelează surse(...).brut(product) din obiectul original pentru peGestiuni/rezervari/comenzi și se apelează separat stoc() original. Rezultatul formulei nu se deduce doar prin aritmetica harnessului.',
  'test_hooks_must_be_null':['RezervareStoc.dublaSuma','FisaCanalProces.surseTest','SetLista.dublaCitiri'],
  'class_binding':'CodeSource/bundle name+version/SHA resource .class pentru RezervareStoc,FisaCanalProces(+RandSursa+surse anonymous),FisaCanalCalcul,RegulaStocCanal,SetLista,TabelaFisaCanal și modelele native efectiv apelate. Bytecode în JAR confruntat cu metodele citite; fără recompilarea/înlocuirea originalelor.',
  'services':'OSGi/SCR/EventAdmin/AdempiereDatabase/Service.locator originale, ca bootstrap N05. EVA/UI/server/zk rămân RESOLVED, start-level50, fără EvaActivator întreg. Gardele originale relevante la warehouse/locator/sursă: EvaWmsGardaEvents și EvaStocEvents; se pot păstra EvaAuditPostareEvents ca gardă originală, fără credit de postare. Excluderile celorlalte28subscriptions se consemnează nominal din inventarul sigilat N05. Nu se activează handler BOM fără operații BOM și nu se omite o gardă a tabelei atinse.',
  'native_validators':'Păstrează FixedAssetsY efectiv activ, LiberoN, ProductPriceValidatorN; inventar și servicii IStorageValidator dacă prezente în alte bundle-uri, fără inventarea clasei absente în core. Aplicabilitatea exactă addQty este conform bytecode: nu apelează StorageValidatorProvider în acest build.',
  'native_normal_order_path_static_only':'MOrder/MOrderLine folosesc rezervări native în fluxurile lor, dar nu sunt invocate aici. Eticheta corectă este rezervări sintetice prin PO/API nativ, nu comandă SO/PO finalizată.'},
 'G05_persistence':{
  'fixture':'Familii separate main, product/warehouse-filter, active, ASI, rollback. ID-uri și UUID-uri native; prefix unic; niciun ID hardcodat din N05. Stoc de bază10 în locator eligibil pentru rezervare; produs stocabil non-BOM. Restul termenilor T22/seturi/rezervă/reguli sunt0, cu probe SQL în preflight și la fiecare caz.',
  'write_scope':'Numai fixture sintetică locală. PO/API originale creează/schimbă rezervele; SQL direct folosit numai readback/izolare seed/transfer ownership, nu INSERT/UPDATE business M_StorageReservation.',
  'snapshot':['M_StorageReservation: ID/UUID/client/org/product/warehouse/ASI/IsSOTrx/Qty/IsActive/Updated/UpdatedBy','M_StorageOnHand și locatori/type/eligible; M_Product și attribute set/instance','EVA_SursaSite fără secrete și dovada source reader; toate liniile site pentru fixture, cerereSet=0','M_ReservationTrace dacă prezent: delta fixture; C_Order/C_OrderLine/M_InOut/Fact_Acct fixture=0 și număr global separat ca invarianti, nu audit contabil','PID/xid/Trx/izolare și timestamp înainte/după native add, commit, rollback; rezultate native reader, EVA raw, EVA final'],
  'independent':'După commit, conexiune Python separată readonly citește rândurile după ID și cheile fixturei și calculează SO/PO separat; înainte de commit la R01 confirmă vechea stare vizibilă. Oracolul nu importă funcția de business și nu scrie în DB. Se păstrează rândurile brute și nu se declară persistență numai din rezultat JVM.',
  'no_cache_shortcut':'getQty face SQL; pentru PO reload sau instanță nouă după commit. După setIsActive se recitește rândul pe conexiune nouă. Context/MProduct cache pentru ASI controlat prin produs nou, nu patch cache.'},
 'G06_cases':[
  {'id':'G3-S01','type':'pozitiv','setup':'stock10, SO2 active, PO absent/0; T22/seturi0','expected':{'native_SO':'2','native_PO':'0','native_available':'8','EVA_raw_reserved':'2','RezervareStoc':'8','FisaCanal':'8'},'persistence':'SO row2 comis, native stock10; readers nu modifică rezerve/stock.'},
  {'id':'G3-C01','type':'contraexemplu','setup':'aceeași familie, SO rămâne2; PO0→5 prin add(diff5,false)','contract':'EVA disponibil pentru vânzare trebuie să rămână8','predicted_current':{'native_SO':'2','native_PO':'5','native_available':'8','EVA_raw_reserved':'7','RezervareStoc':'3','FisaCanal':'3'},'classification':'Dacă observat și readback confirmat: FAIL_PRODUCT_CONFIRMED al R12-STOC-SO-PO-01, nu PASS.'},
  {'id':'G3-C02','type':'contraexemplu plafonare','setup':'SO2 constant; PO5→15 prin add(diff10,false)','contract':'disponibil vânzare8','predicted_current':{'native_SO':'2','native_PO':'15','native_available':'8','EVA_raw_reserved':'17','RezervareStoc':'-7','FisaCanal':'0'},'limit':'Nu confunda plafonarea FisaCanal cu RezervareStoc, care nu plafonează.'},
  {'id':'G3-C03','type':'martor PO fără SO','setup':'familie separată stock10, SO absent/0, PO5 active','contract':'disponibil vânzare10','predicted_current':{'native_SO':'0','native_PO':'5','native_available':'10','EVA_raw_reserved':'5','RezervareStoc':'5','FisaCanal':'5'}},
  {'id':'G3-F01','type':'filtre depozit/produs','setup':'stock10/SO2/PO0 principal; rezervări SO4/PO7 pe alt produs și SO3/PO9 pe alt depozit cu produse valide; fără corupere client/FK','expected':'principal rămâne native8/EVA8; cheile secundare au propriile sume; selectarea depozitului exact prin sursa originală','persistence':'readback tuturor cheilor separate, nu numai count'},
  {'id':'G3-F02','type':'filtru client/ownership citire','setup':'rânduri toate owned client11; se verifică proprietatea produsului, warehouse, source, ASI. Cititor EVA primește un client pozitiv inexistent, cu IDs client11, în comparație cu11','expected':'EVA nu returnează cantitatea client11; sursa(clientGreșit,sourceId)=null. Stoc metoda internă evaluată cu config validă se etichetează apel de limită parametrizat, nu apel normal autorizat. Native getQty nu are client param și continuă să returneze suma acelorași IDs. Nu crea rânduri cross-client invalide.',
   'limit':'Nu probă de autentificare/izolare endpoint ori IDOR. getQty nu este înlocuitor securizat fără validarea ownership în apelant. Client0 este în afara contractului SetLista.firma și poate da Refuz(K_FIRMA) exact, documentat separat.'},
  {'id':'G3-F03','type':'IsActive caracterizare','setup':'familie stock10/SO2/PO5; PO.setIsActive(false).saveEx apoi SO.setIsActive(false).saveEx, commits separate','expected':'după PO inactive: EVA8, nativeSO2/nativePO5; după ambele inactive: EVA10, nativeavailable8. Confirmă flags/readback. Native getQty include inactive, EVA exclude.',
   'limit':'Nu declară defectul nativ și nu recomandă dezactivarea rezervărilor ca flux normal; este caracterizarea politicii la refolosire. Nu suprascrie cantități pentru rezultat.'},
  {'id':'G3-F04','type':'ASI agregat și exact','setup':'produs nou cu MAttributeSet.isInstanceAttribute=true, două MAttributeSetInstance native L1/L2, stock6/4, SO1/1 și PO5 numaiL1','expected':'getQtySO(ASI0)=2; PO(ASI0)=5; SO(L1)=1,SO(L2)=1; nativeavailable L1=5/L2=3/toate8. EVA agregă toateASI: brut rezervat7, disponibil3. Confirmă persistența ASI reale, nu valori inventate.',
   'normalization_negative':'Un produs separat fără attribute set, add cu un ASI existent în parametru trebuie să persiste peASI0 conform API; martor de normalizare, fără credit de urmărire lot end-to-end.',
   'limit':'ASI0 în getQty înseamnă toate, nu doar rândul0. EVA cititorii actuali nu au parametruASI; nu se prezintă compatibilitate lot/perlot.'},
  {'id':'G3-R01','type':'rollback/retry','setup':'familie nouă stock10/SO2/PO0; Trx explicită addPO5; înainte commit, aceeașiTrx citește PO5/EVA3, conexiunea readonly separată vedePO0/EVA8 derivat; PID/xid/izolare capturate','expected':'rollback→PO0, SO2, stock10, disponibil8; retry înTrx nouă addPO5+commit→exactPO5 și rezultateC01, fără dublare10; snapshot separat al eventualei secvențe ID consumate','limit':'Retry după rollback demonstrat, nu idempotență request duplicat după commit. Callback tracer null; fără metadate proces.'},
  {'id':'G3-S02','type':'floor formula reală','setup':'familie separată stock10.75/SO2.25/PO0, T22/seturi/rezervă0','expected':'nativeavailable8.50; RezervareStoc8.50; FisaCanal8 prin floor. Fără deducție că native și canal trebuie să aibă același tipnumeric.'}
 ],
 'native_first_recommendation':{
  'direction':'Reutilizează semantica și, dacă precondițiile permit, MStorageReservation.getQty(product,warehouse,ASI,true,trx) pentru rezervări de vânzare; păstrează în adaptarea EVA validarea firmei/produsului/gestiunii, politica IsActive și domeniulASI. Fără tabelă nouă de stoc.',
  'availability_limits':'getQtyAvailable folosește MStorageOnHand.getQtyOnHandForReservation care filtrează LocatorType.IsAvailableForReservation; EVA SQL_STOC adună toate pozițiile. Baseline cere tipNULL/eligibleY și inventar al locatorilor pentru egalitatea bazei. Testarea locatorului indisponibil și decizia politicii sunt separate; înlocuirea directă a întregii formule poate schimba sensul.',
  'open_deduction':'SQL FisaCanal pentru linii site nu exclude C_Order_ID; RezervareStoc SQL_REZ_T22 nu îl exclude. Risc de dublă scădere numai candidat static. Pentru dovadă e necesar fluxul original generare comandă+linie site corelată, stările înainte/după și rezervarea nativă aferentă. Acest flux cere protocol/handler inventory/gate nou; nu se introduce o linieSQL artificială și nu primește credit aici.'},
 'isolation_cleanup':{
  'new_lab':'D:/CodexWork/a05-r12-native-lab-g3-20261103','port':56455,'pg_start':'Numai după gate; verifică liber127.0.0.1:56455 și lipsa laboratorului. Dacă ocupat sau preexistent, oprire fără a atinge resurse străine.',
  'guard':'Gardă JDK21 N05 rehashuită: connect numai127.0.0.1:56455, writes numai propria rădăcină;7canari TCP remote/altport loopback/listen/UDP/exec/writeoutside/removeguard înainte de cod. Orice tentativă ulterioară oprește; nu relaxează către operațional.',
  'neutralization':'Seedonly clienți0/11; SMTP127.0.0.1:1, RESTtoken inactive, schedulere/procesoare off, statistici/autoerroroff; sursa EVA nouă fără endpoint și transmitereoff. Descriptor nativ exactloopback; UI/server/REST/scheduler inactive.',
  'runtime_reuse':'Reutilizează fișierele bootstrap/hashurile N05, nu clusterul sau fixturele șterse. Adaptare numaiharness și configurare nouă; originale JAR nemodificate; nicio probă N05 repetată.',
  'cleanup':'finally rollback/closeTrx; unbind handlers/services; DB.closeTarget/framework.stop/JVMexit; pg_ctl stop numaiclusterpropriu; verificăprocese/listener; copiazăloguri; valideazăcale absolută și reparsepoints înainte de Remove-Item-LiteralPath propria rădăcină. Refuzpolicy→păstrează+raportează, fără metodă alternativă. Cele6scratchuri refuzate rămân neatinse.'},
 'acceptance_and_stop':{
  'gate':'10/10 numaiprotocol independent înainte de restaurare/test. Până atunci numai citire/proiectare/compilare harness fără execuție produs.',
  'valid_defect':'Positivele și izolarea valide, schimbarea doarPO, SO/fizic/termeneauxiliareconstante, originalEVA returnează alt disponibil și rândurile nativeconfirmate independent → defectconfirmat.',
  'stop':['Missing/schema mismatch/role/context/service mismatch','Hook nonnull ori clasă/hash diferit','UI/serverACTIVE sau canar neconform','Fixture/refuz setup: păstreazăeroare, nu declaradefect','Excepție generică nu este PASS; rezultat numericneașteptat fără cauzănu primeștecredit','Poarta/populație/HEAD invalidată → fără produs pânăreaprobare'],
  'output':'Raport înromână, fiecarecaz+fiecaremetodă cuOID/nativeclassSHA,ownerA05/peerA06,A11,cerință,actor,normalvsfixture,pozitiv/contraexemplu,rezultat,efectpersistent,limită; manifest imuabil și cleanup; recepție A11 separată. 0taskuri/fișiere închise automat.'}
}
save('Protocol_G3_nativ_v1.json',p)
apis={'core':ident['native_core'],'source_binary_delta':p['G01_identity_schema']['source_binary_difference'],'tracer':p['G01_identity_schema']['tracer'],'reads':{'getQty':'(product,warehouse,ASI,isSOTrx,trx), no client or active; ASI0 all','getQtyAvailable':'(warehouse,product,ASI,trx), eligible native onhand minus getQty(...true)','EVA':'client and active; no IsSOTrx; no ASI argument'},'runtime_started':False}
save('Reconciliere_API_native_plan_v1.json',apis)
files=[]
for f in sorted(O.rglob('*')):
 if f.is_file():files.append(dict(path=f.relative_to(O).as_posix(),sha256=sha(f),bytes=f.stat().st_size))
ms=save('MANIFEST_protocol_G3_v1.json',dict(head=p['head'],product_executed=False,files=files))
print(json.dumps(dict(protocol_sha256=sha(O/'Protocol_G3_nativ_v1.json'),manifest_sha256=ms,files=len(files),runtime_started=False)))
