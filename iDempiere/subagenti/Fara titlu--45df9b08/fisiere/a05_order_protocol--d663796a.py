from pathlib import Path
import json, hashlib, datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A05_Comanda_rezervare_lot05'
H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):
 f=R/p
 return dict(path=p,sha256=sha(f))
refs=[ref(p) for p in [
 'executie/R12_fisiere/A11/Val04_loturi/Checklist_A11_dupa_R12_Val04_v1.json',
 'executie/R12_fisiere/A11/Val04_loturi/Verdict_A11_G3_nativ_lot04_v1.json',
 'executie/R12_fisiere/A05_G3_nativ_lot04/MANIFEST_A05_G3_nativ_lot04_v1.json',
 'executie/R12_fisiere/A05_G3_nativ_lot04/Cleanup_final_v1.json',
 'executie/R12_fisiere/A05_Comanda_rezervare_lot05/Identitati_plan_comanda_v1.json',
 'executie/R12_fisiere/A05_Comanda_rezervare_lot05/Identitati_plan_comanda_supliment_v1.json']]
P=dict(schema='A05.DocAction.site.reservation.protocol.v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=H,
 state='PROPUNERE SPRE A11; NICIO CLONĂ RESTAURATĂ, NICIUN RUNTIME SAU TEST DE PRODUS PORNIT',owner='A05',peer=['A06','A11'],
 requirement='V04-N02: transferul cererii site către rezervarea nativă; verificarea ipotezei deducerii duble',
 task='SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING',references=refs)
P['concluzie_lectura']={
 'ipoteza':'Cititorii scad separat rezervarea nativă și cererea site. Lipsa filtrului C_Order_ID nu dovedește singură deducere dublă pe fluxul normal.',
 'protectie_identificata':'GeneratorDocumente.emite creează C_Order CO și M_InOut. În faza de culegere IP cu PC deschis scrie C_Order_ID și M_InOut_ID pe aceeași linie site, în aceeași tranzacție. RezervareStoc.SQL_REZ_T22 și FisaCanalProces.surse.brut exclud linia cu M_InOut_ID nenul. La finalizarea cu factură, legăturile și cantitatea rezervată zero sunt scrise împreună.',
 'distinctie':'Linia site cu numai C_Order_ID este o stare artificială până la identificarea unui apelant care o comite. Protocolul nu o fabrică și nu o folosește ca dovadă de defect. C_Order există temporar în tranzacția generatorului înaintea avizului, dar linia site încă nu este legată atunci.',
 'criteriu_de_infirmare':'Pentru cazul executat, dacă înainte există numai cerere site2, iar după commit numai rezervare SO2, iar disponibilul EVA rămâne8 din stoc10 și nu există stare parțială vizibilă extern, ipoteza se infirmă limitat pe această integrare. Nu se infirmă universal pentru alte apelante, importuri, anulări sau restaurări.',
 'constatare_anterioara':'R12-STOC-SO-PO-01 rămâne confirmată separat. În lotul nou PO=0; nu se repetă direct proba PO/API SO/PO ca și cum ar fi caz nou.'}
P['scop_si_frontiere']={
 'A':'MOrder/MOrderLine native, processIt(DocAction.ACTION_Prepare/Complete/Void) → DocumentEngine → MOrder.reserveStock → fabrica nativă IReservationTracerFactory → MStorageReservation și MStorageReservationLog. Fără linie site în familia A.',
 'B':'GeneratorDocumente.emite original, cu DTO sintetic valid și linie EVA persistentă, până la M_InOut IP + confirmare PC deschisă. Exercită ambele DocAction native și legarea originală a liniei. Se cere gate explicit pentru B, separat de A.',
 'C_neautorizat_prin_acest_plan':'PanouFluxComenzi/DialogConfirmComanda → JobFundal → ProceseEcran → ValideazaComenzi.VALIDEZ/AUTO/CONFIRM → GET Detalii → validări → emiteVal → GeneratorDocumente.emite → ListaCulegere și starea antetului. Nu se execută aici. Un viitor endpoint HTTP local sintetic, client/parser originale și gardă dedicată cer protocol și gate noi; niciun hook Detalii înlocuit.',
 'limite_B':['DTO este frontiera explicită: nu sunt probate preluarea externă, maparea, V01–V18 integral, drepturile de operație sau autentificarea.',
 'GeneratorDocumente nu actualizează antetul site IN_CULEGERE și nu cheamă ListaCulegere.genereazaIzolat; acestea sunt în ValideazaComenzi.emiteVal și rămân neexecutate.',
 'Nu se confirmă PC, nu se livrează CO, nu se facturează și nu se postează Fact_Acct. Dacă avizul ajunge CO sau factura este creată contrar fixturei, se oprește și se face rollback; nu se creditează o extindere accidentală.',
 'FisaCanalProces.stoc și surse sunt metode originale apelate; doIt, jurnalul fișei, publicarea și UX nu sunt executate.'],
 'arhitectura':'G1 contabilă este singura gestiune nativă a fixturei; G2 necontabilă nu primește stoc contabil nou. Cutii/manoperă o singură dată, identități permanente CPP/CPA distincte și capacitate G3 comună rămân contracte deschise; produsul simplu al fixturei nu le recepționează.'}
P['G01_izolare_identitate_schema']={
 'gate':'Mai întâi verdict A11 concret10/10 pe A și B. Aprobarea planului R12 sau a lotului G3 nu autorizează automat noul runtime.',
 'lab':'Rădăcină nouă D:/CodexWork/a05-r12-native-lab-order-20261103, numai dacă absentă; port127.0.0.1:56455 numai dacă liber și rezervat exclusiv de root. Nu reutiliza niciun laborator anterior sau cele șase directoare cu cleanup respins.',
 'runtime':'PG16.15, JDK21, Equinox/SCR/EventAdmin/AdempiereDatabase/Service.locator originale. EVA/UI/server rămân RESOLVED la start-level50. Fără EvaActivator întreg, REST, ZK activ, scheduler sau procesor contabil.',
 'seed':{'path':'D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump','sha256':'54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4','content':'Seed sintetic GardenWorld clienți0/11; fără dump operațional.'},
 'core':{'path':'D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar','sha256':'86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'},
 'eva':{'path':'D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar','oid':'4a5e399ebc671569098235c6ec6d151defd20be6','sha256':'82099cd7f436a8fb4d532d8a46b83c62ae0e0176d86d9345c08598299d01d558'},
 'cache':'Rehash integral al celor387 JAR-uri față de manifestul recepționat. Exporturile noi numai git cat-file la df85; working tree operațional nu este identitate de probă.',
 'build':'Păstrează limita LastBuildInfo placeholder / FailOnBuildDiffer=N din seed; nu falsifica informația. Nucleu13/version2026-03-09. Schema și AD sunt verificate nominal pentru toate câmpurile/metodele consumate; existența unei migrări sau isBuildOK nu este dovadă globală de compatibilitate.',
 'canari':'Înainte de orice clasă business: refuz TCP extern, alt port loopback, listen, UDP, exec, scriere în afara rădăcinii, înlocuire gardă; permis doar fișier propriu și conexiune PGloopback. Repetă bindingul și canarii în aceeași JVM cu business. Scrieri numai în lab, niciun apel extern.',
 'neutralizare':'DSNlocal, SMTP127.0.0.1:1, emailuri/tokenuri neutralizate, toate procesoarele și trimiterile externe inactive, endpoints surse nule. Inventar înainte/după plus servicii, threads, socketuri și procese. Nu transfera ownership global și nu modifica metadate operaționale.',
 'schema_minima':['AD_System','AD_Client','AD_Org','AD_OrgInfo','AD_User','AD_Role','AD_User_Roles','AD_Table','AD_Column','AD_ModelValidator','AD_Sequence','C_DocType','C_Order','C_OrderLine','C_OrderTax','C_OrderLineMA','M_InOut','M_InOutLine','M_InOutConfirm','M_InOutLineConfirm','M_StorageReservation','M_StorageReservationLog','M_StorageOnHand','M_Locator','M_LocatorType','M_Warehouse','M_Product','M_ProductPrice','M_PriceList','M_PriceList_Version','C_UOM','C_Tax','C_TaxCategory','C_BPartner','C_BPartner_Location','C_Location','C_PaymentTerm','C_Period','C_PeriodControl','C_Currency','EVA_SursaSite','EVA_ComandaSite','EVA_ComandaSiteLinie','PP_Product_BOM','PP_Product_BOMLine','EVA_PerecheWms','EVA_StocWms','EVA_MiscareWms','Fact_Acct'],
 'schema_acceptance':'Confruntă PG types/null/default/PK/FK/indexuri și AD editabilitate/mandatory/reference cu I_*/X_* din JAR și SQL df85; incluzând câmpurile C_DocType și toate coloanele M_StorageReservationLog. Inventariază și tabelele auxiliare ale handlerelor. Lipsa unei dependențe oprește etapa, fără ensureTables/EvaMetadata sau migrare improvizată; addendum înainte de remediere.'}
P['G03_actor_binding']={
 'actor':'GardenAdmin AD_User101, AD_Role102, AD_Client11, AD_Org11; toate identitățile active și relațiile se recitesc. #AD_Language=en_US, ServerContext nativ pe thread. Parametrizare de laborator, fără credit login, R_DREPT sau UI.',
 'native_validators':'FixedAssets ID50004 Y păstrat și efectiv activ; Libero ID50000 N și ProductPriceValidator N conform seed. Listează nominal fiecare validator/serviciu. Nu dezactiva un validator pentru a forța trecerea.',
 'handlers_activi':['EvaWmsGardaEvents: PO comenzi/linii/warehouse/source și DOC_BEFORE_PREPARE C_Order/M_InOut',
 'EvaCanalB2BEvents: PO C_Order/C_OrderLine și DOC_BEFORE_PREPARE; fixture fără campanie B2B, fără scutire artificială',
 'EvaSetLinieEvents: DOC_BEFORE_PREPARE C_Order/M_InOut; produs non-BOM; markerul SetLista.emitere este setat numai de generatorul original în B',
 'EvaLunaViitoareEvents: PO_AFTER_NEW/CHANGE C_Order și M_InOut, păstrate citirile native ale perioadei și jurnalul alarmei',
 'EvaStocEvents: warehouse/settings și DOC_BEFORE_COMPLETE M_InOut; Culegere.laLivrare decide SARI_MOTOR pentru PC deschis, fără înlocuirea logicii',
 'EvaLotExpiratEvents: DOC_BEFORE_PREPARE M_InOut; fixture fără lot, handler activ',
 'EvaWmsOglindaEvents: DOC_AFTER_COMPLETE M_InOut, legat chiar dacă IP nu trebuie să-l activeze; absența mișcărilor WMS se recitește',
 'EvaAuditPostareEvents: legat, nu credit de postare; orice încercare de postare în afara scopului oprește lotul'],
 'excluderi_nominale':'EvaValidareWmsEvents și EvaAmplasareEvents protejează reversări/void/reactivate M_InOut, care nu sunt invocate în B; EvaValidareProdusEvents protejează alt flux; EvaNotaSetBomEvents fără BOM; EvaAnaliticPartenerEvents exclusiv contabilizare; ceilalți handleri se confruntă cu inventarul EvaActivator și tabelele lor înaintea runtime. Orice eveniment relevant descoperit se adaugă original, cu sursă/hash/schema și preflight. Nu executa B dacă inventarul nu este complet.',
 'binding':'CodeSource, Bundle-SymbolicName/version, SHA256 al fiecărui .class original încărcat; compară JAR Git/core, nu doar numele clasei. EventManager original și lista de abonamente efective înainte/după; servicii factory originale, fără mock ori wrapper de business.',
 'hooks':'RezervareStoc.dublaSuma, FisaCanalProces.surseTest, SetLista.dublaCitiri trebuie null înainte și după. Niciun hook al handlerelor nu se scrie; câmpurile care au implementare implicită nenulă, precum EvaLunaViitoareEvents.lunaInchisa, rămân funcțiile originale și sunt identificate ca atare, nu pretinse null.',
 'tracer':'Core.getReservationTracerFactory original: serviciu real sau fallback original DefaultReservationTracerFactory, care creează ReservationLogTracer. Loghează clasa/fabrica efectivă; nu se transmite tracer null de harness, rezervarea este creată exclusiv de MOrder. trace original folosește același trx și creează M_StorageReservationLog cu OldQty/DeltaQty/NewQty, AD_Table_ID C_OrderLine, Record_ID, DocNo, LineNo, client/org/warehouse/product/ASI/IsSOTrx.',
 'readers':'RezervareStoc.disponibil(client,product,warehouse,excludedSiteOrder,trx); FisaCanalProces.sursa(client,sourceId,trx) → stoc/surse.brut → stocArticol → FisaCanalCalcul.stocCalculat → RegulaStocCanal. Reflection doar pentru acces package-private, fără modificări. TabelaFisaCanal canalnull = cale fără reguli; nu query direct. MStorageReservation.getQty(product,warehouse,ASI,isSO,trx) vs getQtyAvailable(warehouse,product,ASI,trx): loghează ordinea și ID-uri distincte.'}
P['G04_fixture']={
 'families':'Produse/depozite/surse distincte pentru A01, A02, B01, B02, B03. Prefix A05V05 unic și UUID native; niciun ID din loturile anterioare. Stoc cantitativ înregistrat în laborator10, produs simplu non-BOM, IsStockedY, ProductTypeI, ASI0 fără atribute de instanță, locator activ eligibil Availability. PO0, site/seturi suplimentare0.',
 'native_setup':'PO native MProduct/MWarehouse/MLocator/MStorageOnHand, MSequence/MDocType, MBPartner/MBPartnerLocation/MLocation, MPriceList/Version/ProductPrice și MTax dacă seedul nu oferă un candidat univoc adecvat. Numai setter/saveEx; nu SQL business INSERT/UPDATE. Datele de bază se comit și recitesc înaintea cache-urilor native. Poate fi refolosit un candidat seed sintetic exact, cu criteriile și ID-ul păstrate în readiness.',
 'doc_order':'C_DocType activ al client11 (sau0 când nativ admite), DocBaseTypeSOO, DocSubTypeSO=SO, IsSOTrxY, IsAutoGenerateInOutN, fără generare automată de factură, secvență validă. C_Order IsSOTrxY, client11/org11, warehouse al familiei, BP/locații reale, moneda/lista și termenul valide, PaymentRule potrivit, datele identice fixturedate într-o perioadă verificată deschisă. DocType/DocTypeTarget explicite. Nu presupune că Complete implică CO: se citesc stările și ProcessMsg.',
 'doc_shipping_B':'C_DocType MMS IsSOTrxY, IsPickQAConfirmY, IsShipConfirmN, IsSplitWhenDifferenceN, secvență validă. Noul tip sintetic are toate flagurile recitite înaintea generatorului. Generatorul trebuie să producă M_InOut IP cu PC deschis, QtyDelivered0; orice alt rezultat oprește etapa și se rollback.',
 'tax_date_currency':'În preflight rezolvă și salvează fixturedate, C_Period/Control, client/org calendar, C_Tax național univoc cu rata exactă întreagă pentru ContabUtil.taxaPentruCota, listă/monedă și UOM. Preferă taxă0 națională existentă univocă; altfel creează PO sintetic valid, fără alterarea taxelor existente. Nicio alegere arbitrară min(id) într-o mulțime ambiguă. Taxa se comite înainte de generator deoarece cititorul original folosește conexiune fără trx.',
 'bp':'Partener PF sintetic creat prin PO, Value egal cheiePf a DTO și locație activă facturare/livrare, client11, termeni/price list; credit suficient sau NoCreditCheck configurat nativ și consemnat. Se verifică alegerea aceluiași BP de GeneratorDocumente.partener. Zero date personale reale.',
 'source':'EVA_SursaSite prin MTable.getPO, sursă unică A05V05..., org11, warehouse explicit unic, EVA_GestiuniStoc același ID, rezerva0, canalnull, APIurlnull, toate trimiterile false. Acestea sunt precondiții ale cititorului, nu recepție a setărilor din UX.',
 'site_line_B':'EVA_ComandaSite și EVA_ComandaSiteLinie prin PO generic original. Antet client11/org11, sursa exactă, IDextern sintetic unic, nrcomandă egal DTO, stare DE_APROBAT. Linie nr10, produs al familiei, Qty2, stare REZERVAT, CantitateRezervata2, pret și total coerente cu DTO, cota fracție rate/100, fără C_Order_ID/M_InOut_ID/C_Invoice_ID. Câmpurile obligatorii din AD sunt validate înainte de save; nu se ignoră refuzuri. Schema lor reală, fără tabele reconstruite.',
 'dto_B':{'Partener':'pj=false, cui=null, cheiePf exact BP.Value, nume/adresă sintetice, localitate/țară din fixture',
 'Linie':'idLinie=ID persistent creat, produs=ID fixture, cantitate2, pretBrutLei10, cotaLegala=taxa aleasă, stocabiltrue, tipSerienull, serii[], componente[]',
 'ComandaDeEmis':'client11, sursa/nrComanda identice antetului, data/dataFactura=fixturedate, moneda egal ISO currency lista, curs1, partener/linie originale, transport0, discount0, metodaPlata declarată, primulValtrue, descriereLivrare sintetică, livrarePartialafalse',
 'Setari':'org11, gestiune proprie, docComanda SO verificat, docLivrare MMS PC verificat, docFactura ARI valid din seed pentru identitate dar neutilizat, listaPret/termenPlata valide, articolTransport0/articolDiscount0 deoarece valorile sunt0'},
 'terms':'Separat la fiecare checkpoint: site demand filtrat, reserve Qty, cerereComponenta pentru ambele filtre, rezerva sursă și reguli. În A site/seturi0; în B cerereSite2 înainte și0 după legare, componente/seturi0, PO0, activeY, ASI0. Nu cere native available să coincidă cu EVA înaintea transferului: native10 și EVA8 sunt corecte atunci.',
 'filter_scope':'Ownership real client/org/product/warehouse verificat prin FK/PO/readback. Parametrii aceleiași familii pe toate citirile, ASI0 înseamnă agregare. Acest lot nu recredită filtrele IsActive/ASI/multiplewarehouse testate în G3 și nu probează RBAC prin schimbarea clientului.'}
P['G05_oracol_persistenta']={
 'transaction':'Trx nativ nou pentru fiecare tranziție; MOrder.processIt și saveEx în același trx. Fără managedTrx de SvrProcess: nu se invocă proces AD sau MPInstance pentru A/B. GeneratorDocumente.emite folosește savepoint intern în trx extern. Comitere/rollback doar la harnessul de laborator, explicit și logat.',
 'readback':'Conexiune Python separată readonly, cu timestamp/PID/xid/izolare și snapshot pentru fiecare barieră înainte de commit și după commit/rollback. Nu importă calculul din EVA; păstrează rândurile brute, apoi verifică invarianți independenți. JVM loghează trxName/backendPID/xid și toate ID-urile/documentno înainte de ACK; Python nu scrie DB.',
 'tables':['C_Order/C_OrderLine: ID,UUID,DocStatus,DocAction,Processed,IsSOTrx,DocType/Target,warehouse/BP/price/currency/dates,QtyOrdered/Reserved/Delivered/Invoiced',
 'M_StorageReservation: cheia warehouse/product/ASI/IsSOTrx,UUID,Qty,IsActive,client/org,Updated/By; SO și PO separat',
 'M_StorageReservationLog: ID/UUID,AD_Table_ID,Record_ID,DocNo,LineNo,OldQty,DeltaQty,NewQty,SO/PO,client/org/product/warehouse/ASI și trx temporal',
 'EVA_ComandaSite și EVA_ComandaSiteLinie: ID/UUID,stări,cantități,source,documentlinks înainte/după; antetul rămâne neactualizat de generator, consemnat ca frontieră',
 'M_InOut/Line/Confirm/LineConfirm: ID/UUID/status/type/targetqty/movementqty/confirmedqty/C_OrderLine; existența PC deschis și lipsa facturii',
 'Stoc M_StorageOnHand, M_Transaction, M_CostDetail, Fact_Acct, C_Invoice, EVA_StocWms/EVA_MiscareWms și jurnalele handlerelor: delta pe fixture; count global doar invariant suplimentar, nu recepție contabilă'],
 'log_oracle':'Nu prelua limita nemăsurată din G3 drept zero. Capturează baseline M_StorageReservationLog înainte de fiecare caz. La reserve +2: documentul și linia trebuie să explice DeltaQty2 și Old+Delta=New, iar suma deltelor să explice variația rezervei. La complete după prepare nu se acceptă a doua creștere. La void Delta−2 și sumă0; la rollback rândurile business și logurile acelei tranzacții dispar/revin baseline. Numărul exact se consemnează și se motivează din tracer, fără presupuneri de0.',
 'invariants':'Stoc cantitativ înregistrat10 neschimbat, QtyDelivered0, PO0, Fact_Acct/M_Transaction/M_CostDetail ale fixturei fără efect de livrare/postare în scop. DocumentNo/AD_Sequence pot consuma numere la rollback; se măsoară separat, nu se pretinde restaurare a secvențelor. Un rând rezervare existent poate rămâne cu Qty0 după void; nu se cere ștergerea lui. La crearea într-un trx rollback trebuie să dispară rândul nou, nu doar Qty să fie0.',
 'failure':'Orice mismatch al oracolului oprește cazul; se păstrează încercarea, stack exact, stare și snapshot. Nu catch generic interpretat ca PASS, nu set_ValueNoCheck/SQL forțat, nu relaxarea așteptării după rezultat. Ajustarea justificată a fixturei cere addendum A11.'}
cases=[]
def case(i,title,setup,actions,expected,limit):
 cases.append(dict(id=i,title=title,actor='AD_User101 / role102 / client11 / org11',setup=setup,normal_path=actions,positive_and_counterexample=expected,persistence='Snapshot Python separat înainte/după fiecare tranzacție și loguri native nominale',limit=limit,state='NEEXECUTAT'))
case('O01','Momentul rezervării native și lipsa unei a doua rezervări la Complete','Familie A01; stoc10, site0, SO0/PO0; C_Order standardSO cu o linieQty2.',
 'PO saveEx DR commit → processIt(Prepare),saveEx → barieră readonly externă → commit → obiect nativ nou → processIt(Complete),saveEx → commit.',
 'DR: QtyReserved0 și EVA10. În trx după Prepare: IP,QtyReserved2,SO2,log+2; extern înainte de commit încă DR/SO0. După commit IP/SO2/EVA8. După Complete CO/QtyReserved2/SO2/EVA8, fără plus2 nou în log; stock10,delivered0.',
 'Cale nativă programatică reală DocAction; nu AD_Process, UI sau comanda site. Nu deduce stări din numele acțiunii.')
case('O02','Rollback al comenzii native și retry cu stare persistentă','Familie A02; comandă DR cu linieQty2 comisă; stoc10,SO0,site0.',
 'processIt(Complete),saveEx în Trx nou → stare CO/SO2/log în trx → martor extern DR/SO0 → rollback → readback → reîncarcă MOrder nou → Complete/saveEx/commit.',
 'Rollback păstrează DR/QtyReserved0 și baseline log; niciun rând rezervare nou persistent. Retry produce o singură comandă/linie efectivă CO și SO2, log+2 exact explicat; nu reutilizează PO cu cache al tranzacției anulate.',
 'Controlul retry este pe aceeași comandă DR nativă; nu idempotența întregului import sau generator.')
case('O03','Anularea nativă eliberează rezerva comenzii fără livrare','Comanda A01 CO validă, fără M_InOut/C_Invoice.',
 'MOrder nou → processIt(Void),saveEx → barieră externă → commit → cititori originali EVA.',
 'În trx VO și QtyReserved0/SO0; extern înainte de commit CO/SO2; dupăcommitVO/SO0/EVA10. Log legat de aceeași linie explică Delta−2, NewQty0, stock10. Poate rămâne rând rezervareQty0; se recitește.',
 'Anulare native order-only. Anularea unui val site cu PC și eliberarea liniei EVA nu sunt această probă.')
case('B01','Transferul normal din cererea site în rezerva nativă până la PC','Familie B01; stoc10; antet DE_APROBAT/linie REZERVAT Qty2/Rezerve2 fără legături; DocType MMS PC permis.',
 'Citește EVA înainte → GeneratorDocumente.emite original cu DTO fixat → inspectează Rezultat și obiectele în Trx → barieră independentă înaintecommit → commit → cititori/readback.',
 'Înainte: nativeavailable10,site2,EVA8. La întoarcere: C_OrderCO,SO2,M_InOutIP,PCdeschis,linie C_Order_ID+M_InOut_ID populate împreună,invoice0,siteTerm0,EVA8,stock10. Extern înaintecommit vede baseline site2/noOrder/noReservation și EVA8. Dupăcommit vede SO2/siteTerm0/EVA8. Ipoteza dublei deduceri se infirmă limitat dacă toate sunt adevărate; niciun order-only comis artificial.',
 'Integrarea metodei originale până la culegere, nu procesul complet VALIDEZ; antetul și ListaCulegere sunt în afara apelului. Nu presupune global că toate fluxurile sunt sigure.')
case('B02','Rollback al integrării generatorului și retry după recitire','Familie B02 identică B01, antet/linie comise înainte.',
 'GeneratorDocumente.emite până la IP/PC în Trx1 → citire în trx și externă → rollback integral → snapshot → DTO reconstituit cu ID linie persistentă → Trx2 emite/commit.',
 'Dupărollback site2 rămâne fără legături,SO0,noOrder/noInOut/noConfirm/noLog al încercării,stock10,EVA8. Retry are exact un set persistent de C_Order/line și M_InOut/PC al noii execuții, SO2,siteTerm0,EVA8. Numerele consumate la rollback se declară separat.',
 'Reîncercare după rollback integral; nu apel duplicat după succes comis, care are gardele sale în ValideazaComenzi.')
case('B03','Refuzul configurației de aviz după comanda nativă și rollback la savepoint','Familie B03; stoc10/linieQty2; tip MMS sintetic cu PickQA=Y și ShipConfirm=Y, Split=N, verificat prin PO readback.',
 'În Trx extern ia snapshot → GeneratorDocumente.emite; originalul creează/completă comanda, apoi refuzCombinatie aruncă Refuz înaintea primei salvări de aviz → recitește în trx după rollback savepoint → commit doar starea baseline.',
 'Excepție exactă GeneratorDocumente.Refuz și mesaj Etichete.t(Culegere.K_SHIP_CONFIRM, starea DR a noului aviz) conform ramurii originale; liniiRefuzate conține doar linia fixture. Niciun C_Order/Line/rezerve/log/aviz nou persistente; linia site fără legături și disponibil8. Alte excepții sunt eșec de setup, nu PASS. Momentul creării order înainte refuz se documentează din calea originală și loguri dacă observabil, fără a inventa un snapshot intermediar.',
 'Contraexemplu pentru garda generatorului la configurație incompatibilă; nu susține că validatorul exterior permite această configurare în UX. Fără refacere internă a operației.')
P['G06_cazuri']=cases
P['criterii_gate_si_stop']=[
 'G01 identități: HEAD df85, SHA core/EVA/cache/seed și surse; fără runtime operațional folosit ca sursă implicită.',
 'G02 izolare: port/root proprii libere, șapte canari, DSNlocal, schedulere/email/API inactive, servicii active limitate; nu start produs înainte de gate.',
 'G03 actor/servicii: context valid, Service.locator real, validators păstrați, handler-ele relevante toate legate și codeSource verificat în JVM business.',
 'G04 schemă: coloane native și EVA consumate, AD/PK/FK/editabilitate, M_StorageReservationLog; LastBuildInfo limită declarată, orice mismatch dependent oprește etapa.',
 'G05 fixture: DOCTYPE SO/MMS și flags exacte, perioadă/taxă/currency/BP univoce, masterdata comisă, stock10/SO0/PO0, hook-uri neatinse și cereri auxiliare zero.',
 'G06 stări: A măsoară DR/IP/CO/VO și momentul rezervării; B cere IP+PCdeschis, fără factură/livrare/postare; rezultat diferit se rollback și investighează.',
 'G07 persistență: snapshot extern înainte/după commit/rollback și log native nominal; return JVM singur nu este probă persistentă.',
 'G08 contraexemple: rollback/retry, Void și refuz configurație exact; fără catch generic sau SQL business manual.',
 'G09 concluzie: ipoteza poate fi infirmată pentru B01/B02; nu se numește defect un order-only creat artificial. SO/PO defect existent rămâne separat.',
 'G10 livrare: fișe per cale/OID/metodă/event_id, scenarii distincte și repetări separate, manifest imuabil, cleanup cu root absent/port închis/JVMzero, recepție independentă A11.']
P['obligatii_separate']=[
 'Procesul AD EVA_ValideazaComenzi, actor/drepturi/confirmare umană, GET la frontiera HTTP locală sintetică, parser/client originale și starea antetului/ListaCulegere; protocol nou înaintea serviciului.',
 'Confirmarea PC, anularea PC/valului, cantități parțiale, livrare CO, retururi, factură după configurare și Fact_Acct; fiecare are handlers/date/rollback proprii.',
 'Concurența a două comenzi site, idempotența după succes comis, import/replay și reconcilierea datelor istorice cu linkuri incomplete.',
 'G3 shared capacity CPP/CPA/seturi, multiple G1/G2 și canale, SKU/EAN versus identitate internă permanentă; aceste cazuri simple nu le acoperă.',
 'Native-first: păstrează MOrder/DocAction/reserveStock/tracer și legătura atomică cu avizul; dacă se găsește defect, adaptează contractul/cititorul și ownership-ul existente, fără stoc contabil G2 nou. Nu înlocui automat query-ul EVA cu getQty nativ, care are politică IsActive diferită.'
]
P['artefacte_si_cleanup']={
 'required':['Inventar resurse înainte/după','Reconciliere schemă și metadate nominale','Readiness/canari/binding în JVM business','Harness original-call și scriptul readback independent','Loguri complete pentru fiecare încercare','Oracol cazuri nominale și invarianți','Fișe surse cu OID/owner/peer/metodă/cerință/actor/traseu/pozitiv/contraexemplu/efect/limită','Raport român cu verdict limitat','MANIFEST și SHA','Cleanup final'],
 'cleanup':'Închide toate Trx/JVM/framework, oprește numai PG propriu, verifică PID/port/servicii, rezolvă calea exactă în D:/CodexWork și verifică lipsa reparse înainte de Remove-Item -LiteralPath pe rootul nou. Nu șterge/opri resursele altora sau directoarele cu refuz anterior. Dacă auto-review refuză, nu ocoli; păstrează și declară exact.',
 'score':'10/10 este doar poarta protocolului dacă A11 o acordă. Niciun scor de produs și nicio sursă executată doar pentru că este inventariată.'}
f=O/'Protocol_Comanda_rezervare_v1.json'; assert not f.exists(); f.write_text(json.dumps(P,ensure_ascii=False,indent=2),encoding='utf8')
# O fișă pentru fiecare sursă citită; toate sunt încă în etapa plan.
all_sources=[]
for n in ['Identitati_plan_comanda_v1.json','Identitati_plan_comanda_supliment_v1.json']:
 all_sources+=json.loads((O/n).read_text(encoding='utf8'))['sources']
fiches=[]
for s in all_sources:
 n=s['path'].rsplit('/',1)[-1]
 if n=='GeneratorDocumente.java': role='METODA ORIGINALĂ PROPUSĂ B01/B02/B03'; methods='emite → emiteFaraSavepoint → MOrder/MInOut DocAction → Culegere.SQL_LEGA_FAZA1'; scenarios=['B01','B02','B03']
 elif n in ['RezervareStoc.java','FisaCanalProces.java','FisaCanalCalcul.java','RegulaStocCanal.java','SetLista.java','TabelaFisaCanal.java']:
  role='CITITOR/CALCUL ORIGINAL PROPUS, LIMITAT LA PRODUS SIMPLU'; methods='disponibil / sursa / stoc / surse.brut / stocArticol / stocCalculat / cerereComponenta / reguliStoc după clasa exactă'; scenarios=[c['id'] for c in cases]
 elif n.endswith('Events.java'): role='HANDLER DE ANALIZAT/LEGAT CONFORM LISTEI NOMINALE, NU CREDIT BUSINESS'; methods='initialize/doHandleEvent numai dacă originalul este în lista activă; altfel lectură de aplicabilitate'; scenarios=['READINESS']
 elif n in ['Culegere.java','OrdineCulegere.java','ContabUtil.java']: role='TRASEU TRANZITIV PROPUS ÎN B'; methods='Culegere.inOperatie/steaguriTip/refuzCombinatie/dupaComplete/laLivrare; OrdineCulegere.PeVal; ContabUtil.taxaPentruCota, după clasă'; scenarios=['B01','B02','B03']
 else: role='LECTURĂ STATICĂ A FRONTIEREI SAU CONSTANTELOR'; methods='Apelant/schema/domenii; fără apel runtime creditat implicit'; scenarios=['PLAN']
 fiches.append(dict(**s,event_id='VAL05_PLAN_'+n,role=role,methods=methods,requirement=P['requirement'],actor='Context sintetic GardenAdmin în viitoarea probă; deocamdată numai lectură',normal_path=methods,native_method='MOrder.processIt/DocumentEngine/reserveStock; MInOut.processIt pentru etapa B; dependențe, nu credit pentru fișierul EVA',scenarios=scenarios,positive='Conform protocolului, NEEXECUTAT',counterexample='Conform protocolului, NEEXECUTAT',persistent_effect='NEEXECUTAT',limit='O fișă de plan nu este un fișier testat; fișele finale vor delimita metode apelate, transitive, fixture/binding și lectură.'))
ff=O/'Fise_plan_comanda_v1.json'; assert not ff.exists(); ff.write_text(json.dumps(dict(head=H,count=len(fiches),fiches=fiches),ensure_ascii=False,indent=2),encoding='utf8')
txt='''PROTOCOL VAL05 — COMANDĂ NATIVĂ ȘI REZERVAREA COMENZII SITE

Document de proiectare, neexecutat. Se cere verdictul A11 înaintea laboratorului.

1. Întrebarea
Poate fi scăzută aceeași cerere de două ori după ce comanda site devine C_Order?
Lectura arată că generatorul leagă în aceeași tranzacție și M_InOut_ID, iar ambii
cititori EVA exclud liniile cu aviz legat. Nu considerăm un defect demonstrat.

2. Probele propuse
A: comanda standard SO nativă, pregătire, completare, rollback, retry și anulare.
B: GeneratorDocumente.emite original, DTO sintetic și linie site persistentă,
până la aviz IP cu confirmare PC deschisă. Se urmărește trecerea de la cerere
site2 la rezervare nativă2, cu disponibil8 din stocul înregistrat10.
Contraexemplul B03 cere refuzul configurației incompatibile a avizului și
rollback la savepoint fără documente, rezerve sau loguri reziduale.

3. Ce nu se confundă
Apelul generatorului nu include GET, validările exterioare, drepturile de
operație, starea antetului sau ListaCulegere. Acestea rămân o etapă separată.
Linia cu numai C_Order_ID nu este creată artificial pentru a confirma ipoteza.
M_StorageReservationLog se măsoară acum explicit înainte și după fiecare pas.
Native getQty nu înlocuiește automat politica EVA privind IsActive.

4. Recepția
Protocolul JSON este autoritatea detaliată: șase scenarii, gate separat A/B,
fișe per sursă și oracol independent cu citiri înainte/după commit/rollback.
Nu există încă niciun rezultat de produs, serviciu activ sau laborator creat.
'''
ft=O/'Explicatie_protocol_comanda_v1.txt'; assert not ft.exists(); ft.write_text(txt,encoding='utf8')
files=[]
for x in sorted(O.rglob('*')):
 if x.is_file(): files.append(dict(path=x.relative_to(O).as_posix(),sha256=sha(x),bytes=x.stat().st_size))
mf=O/'MANIFEST_PLAN_Comanda_v1.json'; assert not mf.exists(); mf.write_text(json.dumps(dict(head=H,state='PLAN_NEEXECUTAT',files=files),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(protocol_sha256=sha(f),fiches_sha256=sha(ff),manifest_sha256=sha(mf),sources=len(fiches),cases=len(cases),runtime_started=False),ensure_ascii=False))
