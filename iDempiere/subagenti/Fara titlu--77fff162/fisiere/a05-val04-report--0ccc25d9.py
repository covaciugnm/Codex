from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import zipfile

root=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
out=root/'executie/R11_fisiere/A05/Val_04'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
evidence=read(out/'Provenienta_si_probe.json')
prior=root/'executie/R11_fisiere/A05/WMS_proba_tranzactii_G2.json'
assert sha(prior)=='c89d6edd8c54b09fba9f46d661a223cb9e23aa0de3b004b3b33d98ecc28a1653'
trace=[
    {'file':'form/DialogNotaSetWms.java','anchor':'private void inregistreaza()',
     'role':'Frontend ZK: extrage gestiunea, setul, cantitatea, locatorul și versiunea; apelează JobFundal.pornesteProces.',
     'positive':'Trimiterea celor 6 parametri către procesul existent este identificată în cod.',
     'counterexample':'Butonul dezactivat și cheia jobului sunt locale operației/sesiunii; nu există aici blocare comună cu editarea BOM.'},
    {'file':'setup/EvaMetadata.java','anchor':'private static void ensureNotaSetWms',
     'role':'Configurarea AD_Process pentru procesul EVA_NotaSetWms.',
     'positive':'Citirea independentă a AD_Process: ID 1000242 activ, classname NotaSetWmsProces.',
     'counterexample':'Prezența metadatei nu demonstrează lansare cu rolul sau gestiunea unui utilizator real.'},
    {'file':'corelare/NotaSetWmsProces.java','anchor':'protected String doIt()',
     'role':'Backend nativ SvrProcess: drept, firmă, pereche gestiuni, lacăt pe G2, plan recitit, înregistrare în tranzacție.',
     'positive':'Lacătul este luat înaintea planeaza; BAZA.piese apelează ListaMaterialeWms.IMPLICIT.',
     'counterexample':'Cheia lacătului este firmă+gestiune; handlerul editării BOM nu solicită această cheie. 2 G2 pe aceeași rețetă au și ele chei distincte.'},
    {'file':'wms/ListaMaterialeWms.java','anchor':'ListaMaterialeWms IMPLICIT',
     'role':'Citește modelul nativ MPPProductBOM și liniile active, păstrând firma și trx.',
     'positive':'Versiune explicită: constructor MPPProductBOM(ctx,bom,trx); nu se folosește cache static get(bom).',
     'counterexample':'getLines al obiectului nou efectuează Query fără for-update; cache-ul m_lines al obiectului nu ține aceeași rețetă între procese distincte.'},
    {'file':'corelare/SetLista.java','anchor':'SQL_RANDURI',
     'role':'Citirea/validarea definiției setului și a liniilor pe client/BOM.',
     'positive':'Citirile parametrizate ale definiției sunt consumate înaintea planului de mișcări.',
     'counterexample':'Validarea unei definiții corecte nu rezervă versiunea împotriva altui scriitor.'},
    {'file':'wms/NotaSetWms.java','anchor':'cheieLacat',
     'role':'Reguli de notă și chei de serializare ale operațiilor G2.',
     'positive':'Reutilizează mecanismul existent pg_advisory_xact_lock și mișcările native EVA existente.',
     'counterexample':'Protecția per gestiune nu este aceeași cu protecția per versiune BOM pe toate gestiunile.'},
    {'file':'wms/StocWms.java','anchor':'SQL_LACAT',
     'role':'Chei ordonate de stoc, rânduri EVA_StocWms și jurnal EVA_MiscareWms cu locator și BOM.',
     'positive':'Cheile stocului sunt blocate înainte de scrierile lotului; locator/BOM se păstrează în rândurile PO.',
     'counterexample':'Lacătul unui rând de stoc nu obligă salvarea PP_Product_BOMLine să citească după commitul primei ambalări.'},
    {'file':'wms/ModelWms.java','anchor':'STOC',
     'role':'Nume de tabele/coloane utilizate de stocul WMS.',
     'positive':'Tabelele EVA_StocWms și EVA_MiscareWms sunt active în AD și au coloanele locator, warehouse și BOM.',
     'counterexample':'În schema inspectată nu există un trigger non-intern pe cele 4 tabele care să serializeze editarea BOM cu aceste scrieri.'},
    {'file':'component/EvaNotaSetBomEvents.java','anchor':'protected void doHandleEvent',
     'role':'Adaptor de eveniment PO; citește stocul pozitiv pe client/versiune în trx al PO și emite refuz.',
     'positive':'Garda serială rămâne activă logic: stoc pozitiv → refuz; aceleași clase ca în proba precedentă și JAR montat.',
     'counterexample':'SELECT count(*) nu vede rândul neconfirmat al primei ambalări și nu dobândește lacătul versiunii.'},
    {'file':'EvaActivator.java','anchor':'evenimenteNotaSetBom.bindEventManager',
     'role':'Înregistrează handlerul în EventManager; există și dezînregistrarea la stop.',
     'positive':'Clasa montată este identică cu clasa din JAR Git, inclusiv calea de înregistrare.',
     'counterexample':'Bytecode identic nu dovedește că bindEventManager a reușit într-un anumit classloader activ; blocul catch și alte bundle-uri rămân de verificat în clonă.'}
]
records=[]
for row in trace:
    relative='src/com/eva/ro/contab/'+row['file']
    source=next(x for x in evidence['sources'] if x['file'].endswith(relative))
    path=out/'surse'/relative
    lines=path.read_text(encoding='utf8').splitlines()
    anchors=[i+1 for i,line in enumerate(lines) if row['anchor'] in line]
    records.append({**source,**row,'source_artifact':ref(path),'anchor_lines':anchors,
       'canonical_task':'P01.C03.T0029','requirement':'O versiune PP_Product_BOM folosită de stoc G2 nu poate fi modificată astfel încât dezambalarea să producă alte cantități.',
       'method':'LECTURĂ DE COD / BYTECODE + METADATE ÎN CITIRE, fără repetarea probei JDBC.',
       'normal_path':'DialogNotaSetWms → AD_Process EVA_NotaSetWms → NotaSetWmsProces → ListaMaterialeWms → MPPProductBOM → StocWms; editare prin PO → ModelValidationEngine → EvaNotaSetBomEvents.',
       'result':'Calea și delimitarea lacătelor identificate. Compatibil cu defectul de concurență deja reprodus pe componentă; nu dovedește salvarea PO concurentă integrală.',
       'persistent_effect':'Nicio scriere operațională. Proba persistentă rămâne exclusiv martorul anterior JDBC; această completare nu îi mărește domeniul.',
       'limit':'Nici ZK complet, nici PO.saveEx în OSGi, nici Fact_Acct nu au fost executate în acest supliment.',
       'whole_file_accepted':False})

native_dir=Path('D:/CodexWork/eva-audit-secondary-20261102')
trx=native_dir/'native/org.adempiere.base/src/org/compiere/util/Trx.java'
trx_copy=out/'surse_native/org/compiere/util/Trx.java'
trx_copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(trx,trx_copy)
native_jar=native_dir/'org.adempiere.base_13.0.0.202603090043.jar'
code=subprocess.check_output(['C:/Program Files/Java/jdk-21/bin/javap.exe','-classpath',str(native_jar),'-p','-c','org.compiere.util.Trx'])
trx_copy.with_suffix('.javap.txt').write_bytes(code)
with zipfile.ZipFile(native_jar) as archive:
    trx_class_sha=hashlib.sha256(archive.read('org/compiere/util/Trx.class')).hexdigest()
native_addendum={'file':'org.adempiere.base/src/org/compiere/util/Trx.java','source_commit':'da0730aec42f3e9f5f671e81a70ff71e24d5e534','source_sha256':sha(trx),'mounted_class_sha256':trx_class_sha,'source_anchor_line':233,'finding':'Trx cere DB.createConnection(false, Connection.TRANSACTION_READ_COMMITTED). Această ramură corespunde ipotezei martorului anterior; nu este o măsurare a unei sesiuni operaționale.'}

report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':evidence['head'],'executor':'A05 / a05_native_val04','peer':'A03; recepție independentă cerută A11','canonical_task':'P01.C03.T0029','obligation':'N05','status':'EXTINDERE PARȚIALĂ A DOVEZII; FĂRĂ RECEPȚIE NATIVĂ INTEGRALĂ',
 'conclusion':'Cursa BOM are o cale de apel în procesul instalat, iar verificările native inspectate nu furnizează lacătul comun lipsă. Aceasta întărește plauzibilitatea operațională a defectului anterior, dar reproducerea completă PO/OSGi și efectul G1/G3 rămân deschise.',
 'new_evidence':{'github_sources_read':10,'official_native_sources_and_bytecode':7,'mounted_classes_equal':8,'read_only_queries':6,'native_method_cases':4,'complete_native_PO_saves':0,'complete_ZK_runs':0,'Fact_Acct_cases':0},
 'source_trace':records,'native_source_records':evidence['native_sources']+[native_addendum],
 'proofs':[ref(out/name) for name in ['Provenienta_si_probe.json','Citiri_native_metadata.json','Constrangeri_native_metadata.json','Comparatie_clase_montate.json','Classpath_native_unic.json','Native_boundary_stdout.txt','Native_boundary_stderr.txt','A05NativeBomBoundary.java']],
 'prior_component_proof':ref(prior),
 'native_findings':[
   'AD_Process 1000242 este activ și indică NotaSetWmsProces; verificarea este în cabinetul CESIRO, nu în toate cabinetele.',
   'Nu sunt triggere PostgreSQL non-interne pe PP_Product_BOM/BOMLine/EVA_StocWms/EVA_MiscareWms și nu sunt AD_Table_ScriptValidator pe cele două tabele BOM în cabinetul inspectat. Nu se deduce absența altor validatori Java/OSGi.',
   'PO.save rulează beforeSave și apoi ModelValidationEngine; acesta trimite sincron evenimentul și colectează mesajele de eroare. Garda EVA este legată de mecanismul nativ, nu doar de ecran.',
   'MPPProductBOM.getLines folosește Query pe BOM/client/linii active și cache per obiect, fără lacăt comun cu scriitorul. ListaMaterialeWms construiește model nou pentru versiunea explicită.',
   'MPPProductBOMLine.beforeSave nativ verifică semnul co-produsului și Line. Cantități normale 2 și 3 trec metoda; co-produs pozitiv refuzat, negativ permis. Testul folosește gettere sintetice și Unsafe pentru a evita inițializarea PO; nu este PO.saveEx.',
   'afterSave nativ poate actualiza nivelul produsului și starea IsVerified în condiții proprii; nu a fost executat și nu se presupune lipsit de efecte sau blocări colaterale.'
 ],
 'native_bootstrap_attempt':{'result':'Constructorul normal MPPProductBOMLine se oprește în POInfo.loadInfo/DB.prepareStatement: No Database Connection / NullPointerException.','network':'JVM cu checkConnect/checkListen refuzate; zero încercări de conectare observate.','scope':'Limită de pregătire a laboratorului standalone, nu defect al aplicației și nu dependență externă indispensabilă. Nu s-a început tranzacție și nu s-a salvat PO.'},
 'next_native_fixture':[
   'Pornește runtime OSGi nativ izolat cu bundle DB, datasource și EventAdmin configurate; folosește seed GardenWorld și bundle EVA exact identificat, fără date operaționale.',
   'Creează două roluri native, o firmă sintetică, două G2 cu locatori proprii, aceeași versiune de rețetă și stoc inițial în piese; verifică binding-ul procesului și handlerului în acel runtime.',
   'Sincronizează două tranzacții PO prin barieră: ambalarea după citirea rețetei și editarea QtyBOM prin PO.saveEx; citește după commit din conexiune nouă. Include serial, rollback, versiune diferită și două G2.',
   'Pentru comparator, refolosește blocarea tranzacțională nativă a rândului PP_Product_BOM sau mecanismul existent advisory, cu aceeași identitate client+BOM în ambii scriitori și ordine deterministă. Nu aplica modificarea în produs.',
   'Probează separat G1: cutii/manoperă o singură dată și Fact_Acct real. Nu considera corectarea conservării G2 drept validare a costurilor sau G3.'
 ],
 'cleanup':evidence['cleanup'],'execution_grade':None,'product_grade':None,'independent_acceptance':None}
dest=out/'Raport_A05_native_Val04.json';assert not dest.exists()
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copyfile(__file__,out/Path(__file__).name)
manifest={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':evidence['head'],'report':ref(dest),'artifacts':[ref(p) for p in sorted(out.rglob('*')) if p.is_file()],'immutable':True,'native_complete':False}
target=out/'MANIFEST_A05_Val04.json';assert not target.exists();target.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'report_sha256':sha(dest),'manifest_sha256':sha(target),'anchors_missing':[r['file'] for r in records if not r['anchor_lines']],'artifacts':len(manifest['artifacts'])},ensure_ascii=False))
