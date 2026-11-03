from pathlib import Path
import sys,hashlib,json,datetime,subprocess,os,shutil,socket,re,zipfile
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
OUT=R/'executie/R12_fisiere/A05_Nativ_lot02'
CACHE=Path('D:/CodexWork/a05-r12-native-cache').resolve()
LAB=Path('D:/CodexWork/a05-r12-native-lab-20261103').resolve()
HEAD='df85d33c1648ce2b2df130a60a05ef696e2e5480'
GIT=Path('D:/CodexWork/eva-audit-p01-src-20261101')
sha=lambda b:hashlib.sha256(b).hexdigest()
oid=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def write(name,value):
 p=OUT/name;assert not p.exists(),name;p.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str),encoding='utf8');return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
assert sha((R/'executie/R12_plan_delta/A11_verdict_plan_delta_R12_v2.json').read_bytes())=='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
source_rows=[]
env=dict(os.environ);env['GIT_NO_LAZY_FETCH']='1';env['GIT_OPTIONAL_LOCKS']='0'
for path in ['tools/help/pregateste_cabinet_help.sh','tools/status/containere_test.sh']:
 result=subprocess.run(['git','-C',str(GIT),'rev-parse',HEAD+':'+path],capture_output=True,env=env,timeout=20);assert result.returncode==0
 key=result.stdout.decode().strip();result=subprocess.run(['git','-C',str(GIT),'cat-file','blob',key],capture_output=True,env=env,timeout=20);assert result.returncode==0
 data=result.stdout;assert oid(data)==key;target=OUT/'surse_git'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 source_rows.append({'path':path,'oid':key,'sha256':sha(data),'owner':'A05/A10','peer':['A03','A10','A11'],'role':'helper de pregătire / lifecycle, citit ca referință','normal_entry':'tools/help/pregateste_cabinet_help.sh pg|app|mascheaza|stare|opreste → containere_test.sh cere/declara/stare/elibereaza','requirement':'N08: reutilizare mecanisme existente fără a clona date operaționale sau a porni servicii pe server','control':'identitate Git verificată; parametrul DUMP implicit q31 și resursele Docker sunt incompatibile cu limita locală/sintetică a acestui lot','positive':'lectură completă și verificare OID; mecanismele de registry/autostop nu sunt executate pe server','negative':'implicitul q31 nu a fost lansat; nici stările/laboratoarele altor executori nu au fost modificate','result':'LECTURĂ_STATICĂ; NU_EXECUȚIE_HELPER','persistent_effect':'zero efect de produs; copie hashuită în raport','limit':'Nu este audit complet al helperului și nu primește credit de execuție la df85.'})
native_root=Path('D:/CodexWork/eva-audit-secondary-20261102/native/org.adempiere.base/src')
for path in ['org/adempiere/base/Service.java','org/adempiere/base/ds/DynamicServiceLocator.java','org/adempiere/base/BaseActivator.java','org/compiere/db/Database.java','org/compiere/db/CConnection.java','org/compiere/util/DB.java','org/compiere/Adempiere.java','org/compiere/model/MProduct.java','org/adempiere/base/event/AbstractEventHandler.java','org/compiere/model/MJournal.java','org/compiere/model/MJournalLine.java','org/compiere/acct/Doc.java']:
 data=(native_root/path).read_bytes();target=OUT/'surse_native'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 source_rows.append({'path':'native/org.adempiere.base/src/'+path,'oid_computed':oid(data),'sha256':sha(data),'owner':'A05','peer':['A03','A10','A11'],'role':'sursă nativă de documentare / binding cu binar13 separat','source_reference':'release-13/cache anterior; commit raportat anterior da0730aec42f3e9f5f671e81a70ff71e24d5e534, fără echivalență integrală presupusă cu buildul instalat','normal_entry':'OSGi BaseActivator → Service.locator → AdempiereDatabase → CConnection/DB → PO.saveEx; DocAction/Fact_Acct sunt doar pași viitori','requirement':'N08 pregătire clonă nativă; N05 WMS rămâne deschis','positive':'clasele native din binar core13 folosite în bootstrap/PO, fără înlocuirea Service.locator sau logica PO','negative':'fixture incompletă respinsă; rollback și Value duplicat refuzat prin PO real','result':'INFRASCTRUCTURĂ/PO_GENERIC, CU LIMITĂ DE BUILD; MJournal/MJournalLine/Doc/handler doar lectură','persistent_effect':'doar M_Product în GardenWorld sintetic; fără documente ori note financiare în acest lot','limit':'Nu conferă citire completă/exercițiu fiecărei clase și nici recepție WMS/DocAction/Fact_Acct.'})
write('Trasabilitate_fisiere_N08.json',{'candidate':HEAD,'scope':'Inventariere și lectură separate de execuție; nicio închidere fișier/task','files':source_rows})
# Independent oracle: new Python/psycopg connection after JVM has exited; it does not invoke the Java harness or its assertions.
out=(OUT/'bootstrap_attempt5_po.stdout.txt').read_text(encoding='utf8')
prefix=re.search(r'PO_COMMIT_READBACK\|prefix=([^|]+)',out).group(1)
readback={'utc':now(),'method':'Conexiune Python psycopg nouă, read-only, după ieșirea JVM; independentă față de aserțiile PO, nu recepție A11','prefix':prefix,'queries':[]}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',application_name='a05-independent-readback')as c:
 with c.cursor()as q:
  q.execute('SET TRANSACTION READ ONLY');q.execute('SET search_path=adempiere,pg_catalog')
  qs={
   'products':("SELECT m_product_id,value,description,ad_client_id,ad_org_id FROM m_product WHERE value LIKE %s ORDER BY m_product_id",(prefix+'%',)),
   'rollback':("SELECT count(*) FROM m_product WHERE value=%s",(prefix+'_ROLLBACK',)),
   'duplicate':("SELECT count(*) FROM m_product WHERE value=%s",(prefix+'_CPP',)),
   'build':("SELECT version,lastbuildinfo,isfailonbuilddiffer FROM ad_system",()),
   'clients':("SELECT ad_client_id,value FROM ad_client ORDER BY ad_client_id",()),
   'schedulers':("SELECT count(*) FROM ad_scheduler WHERE isactive='Y'",()),
   'native_sessions':("SELECT count(*) FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid() AND backend_type='client backend'",())}
  vals={}
  for name,(sql,params)in qs.items():q.execute(sql,params);vals[name]=q.fetchall();readback['queries'].append({'name':name,'sql':sql,'params':params,'rows':vals[name]})
  assert len(vals['products'])==2
  assert int(vals['rollback'][0][0])==0 and int(vals['duplicate'][0][0])==1
  assert vals['products'][0][2]=='A05 retry after rollback succeeded'
  assert int(vals['schedulers'][0][0])==0 and int(vals['native_sessions'][0][0])==0
  readback['oracle']='PASS pentru efect PO generic și lipsa sesiunilor native rămase'
write('Recitire_independenta_PO.json',readback)
# Preserve all harness revisions relevant to the successful lot and bootstrap diagnostics.
for name in ['a05_r12_native_prepare.py','a05_r12_copy_runtime.py','a05_r12_copy_ant.py','a05_r12_run_bootstrap.py','a05_r12_pg_restore.py','a05_r12_pg_resume.py','a05_r12_pg_isolation.py','a05_r12_build_po.py','a05_r12_close_lot.py','A05OsgiProbe.java','A05NativePoProbe.java']:
 source=Path('D:/CodexWork')/name;target=OUT/'harness'/name;target.parent.mkdir(exist_ok=True);target.write_bytes(source.read_bytes())
for name in ['bootstrap-attempt1.stdout.txt','bootstrap-attempt1.stderr.txt']:
 shutil.copyfile(CACHE/name,OUT/name)
shutil.copyfile(LAB/'postgres.log',OUT/'Postgres_laborator.log')
binary_rows=[]
for p in sorted(CACHE.glob('*.jar')):
 data=p.read_bytes();binary_rows.append({'path':str(p),'oid_computed':oid(data),'sha256':sha(data),'bytes':len(data)})
write('Cache_binar_reutilizabil.json',{'kind':'cache de surse/binare, fără proces ori serviciu activ; păstrat pentru reproducerea controlată','owner':'A05','peer':['A03','A10','A11'],'requirement':'N08 - closure real OSGi/provider','normal_entry':'instalare dormant, activare explicită subset nativ','positive':'manifest/SHA și origine binară; Service.locator/PO real','negative':'nu se copiază configurații operaționale și nu se instalează pluginurile com.eva.*, SSO/Hazelcast/server/REST în execuția finală','limit':'Inventar≠lectură fișier≠test; cache nu este build curent complet EVA','files':binary_rows})
# Stop and remove only this exact owned local laboratory. No remote mutation is performed.
assert LAB.parent==Path('D:/CodexWork').resolve() and LAB.name=='a05-r12-native-lab-20261103'
cmd=['D:/CodexWork/p01-local-pg16/pgsql/bin/pg_ctl.exe','-D',str(LAB/'pgdata'),'-m','fast','-w','stop']
with (OUT/'Cleanup_pg.stdout.txt').open('wb')as so,(OUT/'Cleanup_pg.stderr.txt').open('wb')as se:r=subprocess.run(cmd,stdout=so,stderr=se,timeout=30)
assert r.returncode==0
with socket.socket()as s:port_closed=s.connect_ex(('127.0.0.1',56455))!=0
assert port_closed
shutil.copyfile(LAB/'postgres.log',OUT/'Postgres_laborator_final.log')
shutil.rmtree(LAB);assert not LAB.exists()
archive=CACHE/'native-bundles.tar';assert archive.resolve().parent==CACHE;archive.unlink()
cleanup={'utc':now(),'pg_ctl_exit':r.returncode,'port56455_closed':port_closed,'scratch_absent':not LAB.exists(),'outside_canary_absent':not Path('D:/CodexWork/a05-canary-outside-denied.txt').exists(),'native_sessions_before_stop':0,'osgi_framework_stop_event':64,'jvm_exit':0,'shared_pg_data_untouched':'D:/CodexWork/p01-local-pg16/data','remote_labs_untouched':True,'operational_writes':0,'retained':'Raport, surse/harness și cache read-only de JAR-uri pentru reutilizare; arhiva duplicată eliminată.'}
write('Cleanup_final.json',cleanup)
report={
 'schema':'A05.R12.N08.native-readiness.lot02.v1','utc':now(),'candidate':HEAD,'owner':'A05/A10','peer':['A03','A10','A11'],
 'plan_gate':{'path':'executie/R12_plan_delta/A11_verdict_plan_delta_R12_v2.json','sha256':'84e3735906d868f2153bc6b71c8b0e0e7a0211367ba4d3df5f8509d008d1f2a4'.replace('c8b0','c71c8f0')},
 'verdict':'PROGRES PARȚIAL N08: clonă sintetică restaurată, bootstrap real OSGi/Service.locator și PO generic cu persistență; fără recepție produs10/10',
 'native_origin':{'container':'eva-idempiere-cesiro','operation':'doar citire metadata/binare viaSSH docker exec find/tar/grep; fără Docker start/stop/run pe server','core_sha256':'86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3','postgres_provider_sha256':'77859a33a552b575d3401f2c5739117155d4a93ba54e216592f710763647b0f6','seed_sha256':'54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4'},
 'sequence':[
  {'phase':'inventariere/lectură','result':'402JAR-uri native/terțe copiate fără configurații; Ant director preluat separat, intrări păstrate byte-identic.'},
  {'phase':'bootstrap1','result':'Refuz rezolvare: Ant lipsea din lista top-level JAR. Nu s-a substituit serviciul.'},
  {'phase':'bootstrap2','result':'Resolve reușit; inițializare Java javax.print eșuată. Nu este defect de produs, ci configurație de launcher incompletă.'},
  {'phase':'bootstrap3','result':'Config osgi.compatibility.bootdelegation=true confirmată read-only în runtime; provider nativ și Service.locator reale. Bundle-uri lazy suplimentare observate, excluse din proba finală.'},
  {'phase':'restorePG1','result':'Captura pipe a pg_ctl peWindows a rămas moștenită de postgres. Clusterul propriu pornise; oprit explicit. Campo started=false din prima fișă reprezintă stadiul scriptului, NU absența procesului.'},
  {'phase':'restorePG2','result':'Descriptorii reali de fișier au eliminat blocajul; restaurare strictă --exit-on-error, fără stderr; doar clienții0/11.'},
  {'phase':'PO1','result':'saveEx real ajunge în DB; fixture respinsă pentru C_TaxCategory_ID lipsă. Fixture corectată, fără modificarea produsului.'},
  {'phase':'PO2','result':'saveEx/commit/readback; rollback0rânduri; duplicat Value refuzat; retry persistent; recitire independentă prin conexiune nouă.'},
  {'phase':'cleanup','result':'JVM0; FrameworkEvent.STOPPED64; poolDB închis; cluster oprit, port închis, director eliminat.'}],
 'canaries':{'denied':7,'allowed':'scriere scratch + conexiune nativă127.0.0.1:56455','controls':['TCP extern','port loopback nepermis','listen','UDP','process exec','scriere în afara scratch','înlăturarea SecurityManager'],'limit':'Gardă de instrumentare JVM21, nu sandbox OS/hypervisor sau probă de rezistență contra codului ostil; doar cod autorizat. Nicio denegare suplimentară față de canari în proba finală.'},
 'generic_po':{'native_method':'BundleActivator→SCR/EventAdmin→org.adempiere.base→Database.getDatabase→Service.locator→DB_PostgreSQL→Hikari→POInfo→MProduct.saveEx→ModelValidationEngine→tranzacție nativă','actor':'GardenWorld Admin, AD_User_ID101, AD_Role_ID102, client11/org11; rol verificat DB. Context injectat prinAPI de laborator, nu sesiune UI/login auditată.','normal_case':'două M_Product cu Value distincte, commit și recitire','counterexample':'Value duplicat refuzat, rollback și0rânduri suplimentare','persistent_effect':'două rânduri demo și descrierea retry confirmate independent, apoi întregul cluster eliminat','result':'PASS_LIMITAT_GENERIC_PO'},
 'build_limit':{'AD_System_Version':'2026-03-09','core':'13.0.0.202603090043','LastBuildInfo':'${env.ADEMPIERE_VERSION} 20080428-1232','IsFailOnBuildDiffer':'N','native_isBuildOK':True,'meaning':'isBuildOK=true este permisiv din flag, NU dovadă de egalitate build. Nu am rescris LastBuildInfo pentru a transforma nepotrivirea în PASS. Necesită reconciliere migrări/schema pentru recepția integrală.'},
 'no_credit':['CPP/CPA sunt exclusiv sufixe de fixture; două M_Product_ID distincte nu dovedesc identitate permanentă, nereutilizare după ștergere/dezactivare ori separare SKU/EAN.','Modelvalidators configurate dezactivate în baseline generic; handler EvaNotaSetBomEvents nu a fost activat, deci N05 WMS rămâne deschis.','NotaSetWmsProces/AD_Process, WMS G1/G2/G3, cutii/manoperă, concurs BOM, disponibilitate canale nu au fost executate aici.','DocAction și Fact_Acct nu au fost executate; sursele MJournal/MJournalLine/Doc citite doar pentru pașii următori.','Fără frontend/UX/dispozitiv în acest lot; fără închideri task/fișier/criteriu și fără notă globală10/10.'],
 'next_internal_steps':['A11 verifică manifestul și recitirea; A12 înregistrează doar progres infrastructură N08.','Reconciliere seed/schema/migrări și LastBuildInfo cu build13 exact, fără schimbarea artificială a criteriului.','Activare bundle EVA exactdf85 cu OID/SHA, serviciile/handler-ele originale și permisiuni nominale; verificare AD_Process și EventManager real.','Proces normal EVA_NotaSetWms plus MPPProductBOMLine.saveEx serial/concurent și recitire pe tranzacție nouă; contraexemplu de conservare pentru N05.','DocAction/Fact_Acct separat, inclusiv G1 cutii/manoperă exacto dată, două scheme și rollback/retry; nu transfera creditul generic.','Identitate permanentă CPP/CPA, ne-reutilizare, SKU/EAN, G1/G2multiple și G3 rămân checklisturi de produs distincte.'],
 'outside_dependency_required':False,'cleanup':cleanup,'metrics':{'new_business_file_acceptances':0,'task_closures':0,'contract_closures':0,'generic_native_po_smoke_scenarios':4,'canary_denials':7,'complete_backend_frontend_audit':False}}
report['plan_gate']['sha256']='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
write('Raport_A05_N08_Nativ_lot02.json',report)
protocol={'purpose':'Reproducere numai locală, pe clonă sintetică; NU executa implicit helperul q31 și NU porni serverul operațional.','preconditions':['plan aprobat și inventar de execuții/porturi; director unic propriu, niciun laborator străin reutilizat','seedSHA54d2a646… și cachebinarymanifest verificate','JDK21, PostgreSQL16, portloopback liber; niciun configoperational copiat'],
 'steps':['Creează director propriu și inițializeazăPG cu rol sintetic; pg_ctl stdout/stderr către fișiere reale peWindows.','Restaurare --exit-on-error și verificare clienți/roluri/schema; oprește procesoare, schedulere, email și conectori ai fixturei.','Rulează canarii înainte de clasele native, frameworkstorage/user.home/AdempiereHome în scratch; refuz orice socket în afara DSN exact.','InstaleazăDormant closure nativă verificată; excludeweb/server/REST/SSO/Hazelcast/EVAplugin până la planul lor. Configureazăbootdelegation confirmată; porneșteSCR/EventAdmin/core/provider.','Confirmă serviciul PostgreSQL prin Service.locator real; nu îl înlocui prinreflection sau stub.','Verificăbuild real și diferența LastBuildInfo; pe acesta doar creditgenericPO cu limite, nu recepțieintegrală.','FoloseșteharnessulPO original păstrat, saveEx/commit/rollback/duplicate/retry, oracolpsycopgseparat.','Opreșteframework/pool, terminăJVM, opreștePG; reciteșteport/sesiuni și eliminănumairectorulpropriu dupăvalidarecale.'],
 'harness':'harness/ și po_v2.A05NativePoProbe.java; scripturile păstrate au nume și portul lotului pentru trasabilitate. Pentru rerulare se creează un NOU lot/namespace, nu se suprascriu acestea.','note':'Frameworkul nativ are executori statici; launcherul finalizează controlat JVM după FrameworkEvent.STOPPED, fără a înlătura garda în timpul probei.'}
write('Protocol_reproducere_nativa.json',protocol)
entries=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file():entries.append({'path':str(p.relative_to(OUT)).replace('\\','/'),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
manifest=write('MANIFEST_A05_Nativ_lot02.json',{'schema':'A05.R12.native_lot02.manifest.v1','sealed_utc':now(),'head':HEAD,'owner':'A05','peer':['A03','A10','A11'],'result':'PARȚIAL_INFRASCTRUCTURĂ_PO_GENERIC; RECEPȚIE_INDEPENDENTĂ_PENDING','entries':entries,'files':len(entries),'business_file_closures':0,'task_closures':0,'cleanup':cleanup})
print(json.dumps({'manifest':manifest,'report_sha256':sha((OUT/'Raport_A05_N08_Nativ_lot02.json').read_bytes()),'cleanup':cleanup},ensure_ascii=False))
