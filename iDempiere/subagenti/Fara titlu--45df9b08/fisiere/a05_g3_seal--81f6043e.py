from pathlib import Path
from decimal import Decimal
import json,hashlib,datetime,re,shutil,html
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A05_G3_nativ_lot04'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,d):
 p=O/n;assert not p.exists();p.write_text(json.dumps(d,default=str,ensure_ascii=False,indent=2),encoding='utf8');return dict(path=p.relative_to(R).as_posix(),sha256=sha(p))
def ref(p):return dict(path=p.relative_to(R).as_posix(),sha256=sha(p))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();head='df85d33c1648ce2b2df130a60a05ef696e2e5480'
log2=(O/'business_g3_v2.stdout.txt').read_text(encoding='utf8');log3=(O/'business_g3_v3.stdout.txt').read_text(encoding='utf8')
assert 'G3_CASES_COMPLETE' in log3 and 'BOUNDARY_DENIALS|7' in log3 and 'HARNESS_CONTROLLED_EXIT|0' in log3
cleanup=read(O/'Cleanup_final_v1.json');assert cleanup['pgStopped'] and not cleanup['targetExistsAfter'] and cleanup['listenersAfter']==0
schema1=read(O/'Schema_G3_inainte_v1.json');schema2=read(O/'Schema_G3_dupa_v1.json')
for field in ['table','columns','physical','constraints','indexes','validators','roles','user_roles']:assert schema1['rows'][field]==schema2['rows'][field],field
capture_rows=[]
for version in [2,3]:
 for f in sorted(O.glob(f'business_g3_v{version}.readback_*.json')):
  d=read(f);rr=d['rows']['reservation'];stock=sum((Decimal(str(x['qtyonhand']))for x in d['rows']['stock'] if int(x['m_warehouse_id'])==d['warehouse']),Decimal(0))
  so=sum((Decimal(str(x['qty']))for x in rr if x['issotrx']=='Y'),Decimal(0));po=sum((Decimal(str(x['qty']))for x in rr if x['issotrx']=='N'),Decimal(0));eva=sum((Decimal(str(x['qty']))for x in rr if x['isactive']=='Y'),Decimal(0))
  assert d['rows']['session'][0]['readonly']=='on' and d['rows']['auxiliary'][0]['fixture_facts']==0
  capture_rows.append(dict(path=f.name,sha256=sha(f),version=version,case=d['case'],tag=d['tag'],product=d['product'],warehouse=d['warehouse'],stock=stock,SO=so,PO=po,EVA_reserved=eva,native_available_derived=stock-so,EVA_available_derived=stock-eva,EVA_channel_derived=max(0,int((stock-eva)//1)),reservation_rows=len(rr),readonly_pid=d['rows']['session'][0]['pg_backend_pid']))
assert len(capture_rows)==41
def cap(case):return next(x for x in capture_rows if x['case']==case)
for name,exp in {'G3-S01':('2','0','8','8'),'G3-C01':('2','5','8','3'),'G3-C02':('2','15','8','-7'),'G3-C03':('0','5','10','5'),'G3-F01-product-isolated':('2','0','8','8'),'G3-F03-POinactive-newPO':('2','5','8','8'),'G3-F03-bothInactive-newPO':('2','5','8','10'),'G3-F04-ASIall':('2','5','8','3'),'G3-F04-normalize':('2','0','8','8'),'G3-R01-rollback':('2','0','8','8'),'G3-R01-retry':('2','5','8','3'),'G3-S02':('2.25','0','8.50','8.50')}.items():
 c=cap(name);assert tuple(c[k]for k in ['SO','PO','native_available_derived','EVA_available_derived'])==tuple(map(Decimal,exp)),name
rollback_before=cap('before_rollback_invisible');rollback_after=cap('G3-R01-rollback');retry=cap('G3-R01-retry');assert rollback_before['reservation_rows']==rollback_after['reservation_rows']==1 and retry['reservation_rows']==2
rollback_uuid=re.search(r'newPOuuid=([^\r\n]+)',log3).group(1);final=read(O/'Readback_final_G3_v1.json');assert all(x['m_storagereservation_uu']!=rollback_uuid for x in final['rows']['reservations'])
oracle=write('Oracle_independent_G3_v1.json',dict(utc=utc,scope='Recalculare din41capturi SQL readonly, nu rerulare business și nu oracol A11',captures=capture_rows,rollback_uuid_absent_final=rollback_uuid,actual_java_outputs=[x for x in (log2+'\n'+log3).splitlines()if x.startswith('CASE_G3|')],limited_coverage='SQL stock−SO comparat semantic numai pe locatori eligibili; formule EVA originale executate separat. IsActive și ASI păstrate.'))
plan=read(O/'Fise_plan_G3_v1.json');six={'RezervareStoc.java','FisaCanalProces.java','FisaCanalCalcul.java','RegulaStocCanal.java','SetLista.java','TabelaFisaCanal.java'}
method_cases={'RezervareStoc.java':'G3-S01/C01/C02/C03/F01/F02/F03/F04/R01/S02','FisaCanalProces.java':'sursa/stoc/surse.brut/stocArticol pe aceleași cazuri; RandSursa real, non-BOM; fără doIt','FisaCanalCalcul.java':'stocCalculat; clamp C02 și floorS02; rezervă0/reguli{}','RegulaStocCanal.java':'cantitateOferita cu harta goală','SetLista.java':'esteSet pe non-BOM; cerereComponenta pe rânduri absente; fără componenteBOM','TabelaFisaCanal.java':'reguliStoc cu canal null → harta goală'}
rows=[]
for f in plan:
 n=Path(f['path']).name;f['event_id']='A05.R12.G3.NATIVE.'+n[:-5]+'.v1';f['head']=head;f['previous_evidence_preserved']='Val03 A06 SQL comparator rămâne separat; niciun eveniment/sursă vechi șters sau dublat ca fișier nou.'
 if n in six:
  f['coverage_class']='METODA_ORIGINALA_APELATA_LIMITAT' if n in {'RezervareStoc.java','FisaCanalProces.java'} else 'TRASEU_TRANZITIV_LIMITAT'
  f['result']='EXECUTAT_PE_CLONA_NATIVA; '+method_cases[n];f['scenario']=method_cases[n]
  f['persistent_effect']='Citește rezervările PO/API native comise;41recitiri readonly separate. Nicio scriere a cititorului sau publicare de canal demonstrată.'
 elif n in {'EvaWmsGardaEvents.java','EvaStocEvents.java','EvaAuditPostareEvents.java'}:
  f['coverage_class']='FIXTURE_BINDING';f['result']='Original EventHandler legat și topics/filters observate; PO fixture, fără credit integral pe ramurile handlerului.';f['scenario']='readiness și fixture warehouse/source'
 elif n in {'DomeniiT22.java','FluxTabele.java'}:
  f['coverage_class']='CONSTANTE_METADATE_FARA_CREDIT_EXECUTIE';f['result']='Constante citite; nu metode business testate';f['scenario']='metadata/filtre'
 else:
  f['coverage_class']='LECTURA_STATICA';f['result']='EvaActivator nu rulează integral; TipGestiune wildcard neexecutat';f['scenario']='proiectare/binding'
 f['evidence']=[ref(O/'business_g3_v2.json'),ref(O/'business_g3_v3.json'),oracle];f['task']='SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING';f['actor']='User101/Role102/client11/org11, context sintetic nativ, nu login';f['native_method']='PO.saveEx, MStorageReservation.add/getQty/getQtyAvailable, DB/Trx native';f['limit']+=' Nu DocAction/C_Order/UI/HTTP/persistența fișei/sets cu componente; nicio închidere task/fișier.'
 rows.append(f)
fiches=write('Fise_G3_final_v1.json',rows)
native=read(O/'Identitati_lectura_G3_v1.json')['native'];native_ref=write('Dependente_native_G3_v1.json',dict(scope='Dependențe native; NU fișiere noi din corpusul EVA',sources=native,actual_classes_binding=ref(O/'Receptie_readiness_G3_v1.json'),source_cache_difference='StorageValidatorProvider/IStorageValidator lipsesc din core13 recepționat; bytecode efectiv este autoritatea, nu sursa cache.',tracer_limit='Tracer null explicit. Tabela reală identificată ulterior este M_StorageReservationLog, nu M_ReservationTrace; delta acestei tabele NU a fost recitită. Nu se declară lipsa efectelor auxiliare în acea tabelă. Bytecode addQty nu cheamă tracer când null.'))
cases=[
 {'id':'G3-S01','state':'PASS_SCOPED','detail':'Stoc cantitativ înregistrat10, SO2, PO0 → native8 și EVA8.'},
 {'id':'G3-C01','state':'FAIL_PRODUCT_CONFIRMED_EXISTING_FINDING','detail':'PO5, SO2 constant → native8, RezervareStoc3 și FisaCanal3.'},
 {'id':'G3-C02','state':'FAIL_PRODUCT_CONFIRMED_EXISTING_FINDING','detail':'PO15, SO2 constant → native8, RezervareStoc−7, FisaCanal0.'},
 {'id':'G3-C03','state':'FAIL_PRODUCT_CONFIRMED_EXISTING_FINDING','detail':'FărăSO, PO5 → native10, EVA5.'},
 {'id':'G3-F01','state':'PASS_SCOPED','detail':'Depozit izolat prin același produs/altdepozit și produs izolat prin altprodus/acelașidepozit; ținta8 neschimbată. Prima fixture other modifica ambele dimensiuni și nu a fost suficientă singură.'},
 {'id':'G3-F02','state':'PASS_PARAMETER_BOUNDARY_ONLY','detail':'client1011 inexistent cu IDs realeclient11: sursa=null, EVA0; comparator nativ fărăclientparam returneazăSO2. Fără login/RBAC/IDOR acceptat.'},
 {'id':'G3-F03','state':'CHARACTERIZATION_CONFIRMED','detail':'IsActive readonly la modificarea PO existente. Addendum: PO noi inactive acceptate nativ; POinactive→EVA8/native8, ambelinactive→EVA10/native8. Nu demonstrează că fluxul comercial produce aceste rânduri.'},
 {'id':'G3-F04','state':'PASS_SCOPE_AND_SAME_FINDING','detail':'AttributeSet cu lot/instance și2ASI persistente: stock6/4,SO1/1,PO5L1; nativeavailableL1=5,L2=3,all8; EVA agregăASI și deducePO→3. Fără atribute, add normalizeazăASI0.'},
 {'id':'G3-R01','state':'PASS_SCOPED_ROLLBACK_RETRY','detail':'Trx necomisă vedePO5/EVA3; conexiunea separată nu vede rândulPO. Rollback îl elimină complet; UUID absent final. Retry produceexact1POQty5. Nu idempotență dupăcommit.'},
 {'id':'G3-S02','state':'PASS_SCOPED','detail':'Stock10.75/SO2.25→native8.50/RezervareStoc8.50/FisaCanal8.'}]
report={
 'utc':utc,'head':head,'owner':'A05','peer':['A06','A11'],'status':'PROBA NATIVĂ ÎNCHEIATĂ; CONSTATAREA PRODUSULUI RĂMÂNE DESCHISĂ; RECEPȚIA FINALĂ APARȚINE A11','finding_existing':'R12-STOC-SO-PO-01','new_duplicate_findings':0,'score_product':None,
 'summary':'Ambii cititori EVA originali scad cantitățile PO ca și cum ar fi rezervări de vânzare. Rezervările au fost create în tabela nativă prin PO/API native, fără tabelă substitut. Cu stoc cantitativ înregistrat10 și SO2, numai creșterea PO0→5→15 schimbă rezultatul EVA8→3→−7 (RezervareStoc) sau8→3→0 (fișa canalului); comparatorul nativ păstrează8.',
 'native_entry':'MStorageReservation.add(...,isSOTrx,...,tracer=null)→getCreate→PO.saveEx/cheie compusă→forUpdate→addQty original; inactive numai la PO nou, prin setter original înainte de saveEx.',
 'eva_entry':'FisaCanalProces.sursa din PO persistent→stoc/surse original→stocArticol→FisaCanalCalcul.stocCalculat→RegulaStocCanal.cantitateOferita; separat RezervareStoc.disponibil. Hook-uri null în aceeașiJVM, originalanonymousclassSHA verificat. Nu FisaCanalProces.doIt/AD_Process.',
 'cases':cases,'scope_counts':{'planned_families':10,'valid_python_readbacks':41,'initial_setup_only_readbacks':1,'scoped_EVA_method_sources':6,'other_EVA_source_fiches':7,'native_dependency_sources_not_corpus':7,'final_fixture_products_including_spares_failedsetup':14,'final_fixture_warehouses':12,'final_fixture_sources':12,'final_native_reservation_rows':23,'final_native_onhand_rows':13,'attribute_sets':1,'ASI':2,'global_facts_count':308,'fixture_facts':0,'fixture_order_lines':0,'fixture_site_lines':0},
 'readiness':ref(O/'Receptie_readiness_G3_v1.json'),'schema':{'before':ref(O/'Schema_G3_inainte_v1.json'),'after':ref(O/'Schema_G3_dupa_v1.json'),'checks':138,'meaning':'Existență AD/coloane consumate; metadata/physical/constraints/indexuri identice înainte/după. NU validare integrală editabilitate, build sau module. IsActive readonly a fost identificat la fixture și în metadata finală. LastBuildInfo placeholder nemodificat.'},
 'oracles':[oracle,ref(R/'executie/R12_fisiere/A11/Val04_loturi/Contraoracol_A11_G3_readback_v1.json')],
 'persistent_final':ref(O/'Readback_final_G3_v1.json'),'fiches':fiches,'native_dependencies':native_ref,
 'errors_retained':[{'attempt':'compile_v1','reason':'Harness missing throws SQLException; sursă/log salvate, no product.'},{'attempt':'business_g3_v1','reason':'Readback a cerut ID numeric inexistent; native key compusă+UUID. Zero rezervări/cazuri. Fixturea setup rămasă separată.'},{'attempt':'business_g3_v2 F03','reason':'PO nativ refuză schimbarea IsActive pe rând existent; vechiul oracol invalid. Cazurile anterioare păstrate, fără rerulare; addendum A11 permite numai PO nou inactive.'}],
 'native_first_recommendation':['Adaptează RezervareStoc.SQL_REZ_NATIVA și cititorul FisaCanalProces la semantica SO rezervat / PO comandat, folosind la maximum MStorageReservation.getQty(...,true) sau aceeași regulă nativă în adaptarea existentă.',
  'Nu înlocui automat cititorul: native getQty nu filtreazăAD_Client_ID/IsActive; ownership validat anterior și politica EVA IsActive explicită sunt obligatorii. Rândurile inactive demonstrate sunt fixture, nu flux comercial.',
  'ASI0 în getQty înseamnă toate loturile; păstrează agregarea G3 și specifică separat orice disponibil pe lot. getQtyAvailable filtrează locatori eligibili pentru rezervare, spre deosebire de sumă EVA; baseline aici are toți locatori eligibili.',
  'Păstrează diferența intenționată BigDecimal versus floor/clamp al canalului; nu crea tabele suplimentare de stoc și nu crea stoc contabil înG2.'],
 'remediation_checklist':[{'id':'G3-FIX01','check':'PO0/5/15 la SO2 și stoc10: cititorii vânzării rămân8; numai SO schimbărezervatul.'},{'id':'G3-FIX02','check':'SO0/PO5 păstrează disponibil10; QtyPO se raportează separat, fără scădere ca rezervareSO.'},{'id':'G3-FIX03','check':'Păstrează validarea ownership, client/produs/warehouse și IsActive; politica pentruinactive nu se schimbă incidental prin API.'},{'id':'G3-FIX04','check':'ASI0/toate și ASI specific, locator eligibil/neeligibil, BigDecimal/floor/clamp și reguli/rezervă se validează separat.'},{'id':'G3-FIX05','check':'Rollback: absența rândului PO nou și UUID; retry exacto dată dupărollback. Concurență/retrydupăcommit necesităprobe separate.'},{'id':'G3-FIX06','check':'Nu dubla cererea între linia site și rezervareaC_Order; testează ulterior fluxul original cu handler/DocAction explicit. Aici doar candidat static, nu defect confirmat.'}],
 'limits':['Nu C_Order/C_OrderLine/DocAction, publicare HTTP/UI/login sau persistarea fișei canalului.','Nu seturi S1/S2/CPP-CPA/G3 comun complet, gestiuniG2 multiple, costuri/cutii/manoperă ori Fact_Acct/postare.','CountFact_Acct308 și0rânduri fixture nu validează solduri contabile. Nu inventariere fizică: stocul cantitativ este înregistrat sintetic în laborator.','Native cache source și binary nu coincid integral; clasa/JAR exactă controleazăexecuția.','M_StorageReservationLog există, dar delta sa nu a fost capturată; tracer null și lipsa apelului în bytecode sunt singurele dovezi pentru această ramură, fără afirmație de zero efect persistent acolo.'],
 'cleanup':ref(O/'Cleanup_final_v1.json'),'operational_writes':0,'product_code_modified':False,'task_or_full_file_closed':0,
 'gates':[ref(R/'executie/R12_fisiere/A11/Val04_preflight/Verdict_A11_protocol_G3_nativ_v2.json'),ref(R/'executie/R12_fisiere/A11/Val04_preflight/Addendum_A11_G3_F03_F01_v1.json')]
}
report_ref=write('Raport_A05_G3_nativ_lot04_v1.json',report)
annex=write('Anexa_reproducere_G3_v1.json',dict(order=['VerificăHEAD/OID,poarta10/10șiaddendumA11; nouveau clone root și port56455 liber.','Restaureazăseed54d2...,max_locks_per_transaction1024;ownership doar schemaadempiere;neutralizează conectori/email/schedulers.','Rehash387JAR,compileazăgardă/harness;schema138prezențe+constraints și contextactor.','Canari7,OSGi/provideroriginal,EVA/UI/serverRESOLVED,startlevel50;3handlereoriginale,FixedAssetsY,3hooksnull.','MasterdataPOcommit/readback înainteMProduct.get;stocknativecommit;rezervăriSO/POoriginale;sourcePOactual.','Pythonrunner handshake readonly la fiecarecheckpoint;țineoperațiapânăsnapshot/ACK;operationalwrites0.','Modebusiness original conține încercarea vecheF03readonly; reproducerea nouă trebuie să folosească variantele inactivePO din business_continuation în locul vechiuluiF03. Continuation are IDs/Value legate de aceastărundă, nu reutilizabile pe altseed; nu rulaorbește.','ReciteșteDBfinal,schemadupă;sigileazărezultatele;închideJVM/OSGi,PG;ștergedoarrădăcinaproprievalidată.'],harness='harness/ include surse,probeJAR și scripts. Fiecare încercare păstrează propriile surse/loguri. Scripturile de continuare sunt dovezi, nu un installer de produs.',known_limits=report['limits'],resources='No active lab. Passive caches and harness retained. Other6rejectedcleanup scratch roots untouched.'))
h=O/'harness';h.mkdir(exist_ok=True)
for f in Path('D:/CodexWork/a05-g3-harness').glob('*'):
 if f.is_file()and f.suffix in ['.java','.jar']:shutil.copy2(f,h/f.name)
for f in Path('D:/CodexWork').glob('a05_g3_*.py'):shutil.copy2(f,h/f.name)
shutil.copy2(Path('D:/CodexWork/a05_g3_cleanup.ps1'),h/'a05_g3_cleanup.ps1')
table=''.join('<tr><td>'+html.escape(c['id'])+'</td><td>'+html.escape(c['state'])+'</td><td>'+html.escape(c['detail'])+'</td></tr>'for c in cases)
doc='<!doctype html><html lang="ro"><meta charset="utf-8"><title>Audit nativ G3 SO/PO</title><style>body{font:16px/1.5 system-ui;max-width:1200px;margin:32px auto;color:#17222a}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd5dd;padding:10px;text-align:left;vertical-align:top}h1{font-size:28px}.finding{border-left:6px solid #b32727;padding:12px;background:#fff0ed}</style><h1>Audit nativ G3: rezervări SO/PO</h1><p>HEAD '+head+'</p><p class="finding">'+html.escape(report['summary'])+'</p><p>10/10 este nota planului, nu conformitatea produsului. Proba folosește PO/API native. Nu execută comenzi C_Order, DocAction, interfața sau publicarea pe site.</p><table><tr><th>Caz</th><th>Rezultat</th><th>Dovadă și limită</th></tr>'+table+'</table><h2>Adaptarea funcțiilor native</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>'for x in report['native_first_recommendation'])+'</ul><h2>Limite și resurse</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>'for x in report['limits'])+'</ul><p>Clona proprie oprită și eliminată;0scrieri operaționale. Raportul și manifestulJSON păstrează toate identitățile,încercările și recitirile. Recepția finală aparține A11.</p></html>'
hf=O/'Raport_G3_nativ.html';assert not hf.exists();hf.write_text(doc,encoding='utf8')
files=[]
for f in sorted(O.rglob('*')):
 if f.is_file():files.append(dict(path=f.relative_to(O).as_posix(),bytes=f.stat().st_size,sha256=sha(f)))
manifest_ref=write('MANIFEST_A05_G3_nativ_lot04_v1.json',dict(utc=utc,head=head,files=files,report=report_ref,events='41valid Python readbacks +1setup; sixlimited method source events; all earlierSQL evidence preserved',cleanup=ref(O/'Cleanup_final_v1.json')))
print(json.dumps(dict(report=report_ref,manifest=manifest_ref,fiches=fiches,files=len(files)),ensure_ascii=False))
