import pathlib,json,hashlib,zipfile,re,collections,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere');B=R/'A05_N05_lot03';O=R/'A11/Val03_loturi'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((B/n).read_text(encoding='utf8'))
def ref(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
checks=[]
def ck(label,b):
 checks.append({'check':label,'ok':bool(b)})
 if not b:raise AssertionError(label)
def save(n,x):
 p=O/n;assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return ref(p)
m=load('MANIFEST_A05_N05_lot03_v1.json');ck('manifest fixed',sha((B/'MANIFEST_A05_N05_lot03_v1.json').read_bytes())=='1a194d28361afe9184e017f8efee7659618edb18f5ff1a671f9134f9adbc623f')
for e in m['files']:
 b=(B/e['path']).read_bytes();ck('artifact '+e['path'],sha(b)==e['sha256'] and len(b)==e['bytes'])
f=load('Fise_sursee_N05_v1.json');source_rows=[]
for e in f['files']:
 rel=e['path'].split('src/com/eva/ro/contab/',1)[1];p=B/'surse_df85'/rel;b=p.read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();ck('source '+rel,sha(b)==e['sha256'] and oid==e['oid'])
 scope='STATIC_ONLY' if not e['state'].startswith('EXECUȚIE') else ('FIXTURE_OR_BINDING_ONLY' if e['phase'].startswith('binding + fixture') or e['phase']=='fixture' else ('BINDING_AND_METADATA_ONLY' if e['phase'].startswith('binding + process') else 'TRANSITIVE_BUSINESS_PARTIAL'))
 source_rows.append({'path':e['path'],'oid':oid,'sha256':sha(b),'scope':scope,'phase':e['phase'],'methods':e['methods_in_scope'],'direct_class_binding_logged':e['direct_class_binding_logged'],'integral':False,'scope_note':e['control']})
runtime=load('Runtime_instalat_N05_v1.json');cache={}
for e in runtime['entries']:
 p=pathlib.Path(e['path']);b=p.read_bytes();ck('runtime '+p.name,sha(b)==e['sha256'] and len(b)==e['bytes']);cache[e['symbolic_name']]=p
eva=cache['com.eva.ro.contab'];core=cache['org.adempiere.base']
ck('EVA exact Git JAR',sha(eva.read_bytes())=='82099cd7f436a8fb4d532d8a46b83c62ae0e0176d86d9345c08598299d01d558')
ck('core exact native',sha(core.read_bytes())=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3')
bindings=[]
for version in ['business_v1','business_v2']:
 # V1 console was emitted with Windows legacy encoding. Match only ASCII provenance tokens;
 # preserve the original bytes/hash and never interpret mojibake as a product defect.
 rawlog=(B/(version+'.stdout.txt')).read_bytes()
 try:log=rawlog.decode('utf8')
 except UnicodeDecodeError:log=rawlog.decode('latin1')
 run=load(version+'.json')
 for n,h in run['sources'].items():ck('runner hash '+version+n,sha((B/(version+'.'+n)).read_bytes())==h)
 for name,bundle,h in re.findall(r'CLASS_BINDING\|([^|]+)\|bundle=([^|]+)\|sha256=([^|]+)',log):
  sym=bundle.split(':')[0];path=name.replace('.','/')+'.class'
  with zipfile.ZipFile(cache[sym]) as z:b=z.read(path)
  ck('loaded class '+version+name,sha(b)==h);bindings.append({'version':version,'class':name,'bundle':sym,'sha256':h})
 for prohibited in ['com.eva.ro.contab','org.adempiere.ui.zk','org.adempiere.server']:
  ck('dormant '+version+prohibited,'DORMANCY_BEFORE_PROBE|'+prohibited+'|state=4|startlevel=50' in log)
 ck('surrogate null '+version,'SURSE_TEST|NULL' in log);ck('boundary seven '+version,'BOUNDARY_DENIALS|7' in log)
 ck('provider original '+version,'NATIVE_SERVICE_LOCATOR|org.compiere.db.DB_PostgreSQL' in log)
 ck('factory native '+version,'PROCESS_BINDING|id=1000228|factory=com.eva.ro.contab.component.EvaProcessFactory|class=com.eva.ro.contab.corelare.NotaSetWmsProces|role_access=true' in log)
 ck('cleanup native '+version,'NATIVE_PROBE_CLEANUP|handlers_unbound|factory_unregistered|DB_closed' in log and 'FRAMEWORK_STOP|64' in log)
ck('run statuses v1 oracle-stop/v2 complete',load('business_v1.json')['exit']==1 and load('business_v2.json')['exit']==0)
schema=load('Reconciliere_schema_efectiva_v1.json');before=load('Schema_inainte_v1.json');after=load('Schema_dupa_v1.json')
oracle=load('Oracle_independent_N05_v1.json')
# Metadata schema snapshots carry the same named rows; run outputs and timestamps differ.
for k,v in oracle['schema_dictionary_access_stable'].items():
 ck('executor schema stable claim '+k,v)
 # Independently compare persisted dictionaries, not just boolean claims.
 ck('schema actual equality '+k,before['rows'][k]==after['rows'][k])
cleanup=load('Cleanup_final_v1.json');ck('cleanup target exact',cleanup['target']=='D:\\CodexWork\\a05-r12-native-lab-n05-20261103');ck('cleanup stopped',cleanup['pgStopped'] and cleanup['listenersAfter']==0 and cleanup['ownJvmProcesses']==0 and not cleanup['targetExistsAfter']);ck('cleanup directory absent independent filesystem check',not pathlib.Path(cleanup['target']).exists())
qa=save('QA_A11_N05_lot03_v1.json',{'count':len(checks),'checks':checks,'issues':[],'binding':bindings,'scope_counts':dict(collections.Counter(x['scope'] for x in source_rows))})
mapping=save('Matrice_A11_N05_sursee_v1.json',{'head':f['head'],'source_count':len(source_rows),'files':source_rows,'rule':'Doar sursele efectiv exercitate au PARTIAL, separate business/fixture/binding. Nimic integral; lecturile și încărcarea JAR nu se convertesc în criterii închise. Transitiv înseamnă corelare sursă+cale executată, nu acoperire instrumentală de linii/ramuri.'})
report=save('Verdict_A11_N05_lot03_v1.json',{
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','head':f['head'],'disposition':'ACCEPTAT defect N05 demonstrat în integrare nativă sintetică și controale limitate; recepția fluxului complet RESPINSĂ ca neîndeplinită',
 'executor_manifest':ref(B/'MANIFEST_A05_N05_lot03_v1.json'),'executor_report':ref(B/'Raport_A05_N05_lot03_v1.json'),'QA':qa,'source_matrix':mapping,'independent_counteroracle':ref(O/'Contraoracol_A11_N05_persistenta_v1.json'),
 'finding':{'identity':'N05 existent, extindere a dovezii de la JDBC/modele la proces+PO/handler originale; fără increment de defect unic','task':'P01.C03.T0029 (P01.T355)','priority':'P1 propus pentru integritatea evidenței WMS; impact contabil G1 nedemonstrat','observed':'Procesul ambalează2piese într-un set. Înaintea commitului, altă tranzacție salveazăQtyBOM3 prin MPPProductBOMLine.saveEx. După commit, procesul normal dezambalează3piese. Din10 piese inițiale rezultă11, confirmate de13rânduri de jurnal ale celor3fixturi și balanțele recalculare separat.','mechanism':'Lacătul firma+WMS al procesului nu este comun cu handlerul de editare BOM. SQL_FOLOSITA în T2 nu vede setul necomis. S02 dovedește că garda originală este activă în serial, deci constatarea nu se bazează pe omiterea acelei gărzi.','scope':'R01/C01 coordonează commitul prin overload managedTrx=false, aceeași clasă/factory/parametri/DB; nu s-a măsurat intercalarea din două sesiuni UI reale.'},
 'cases':{'S01':'ACCEPTAT: original ProceseEcran managedTrx=true;10→8+1set→10, stoc/jurnal persistente.','S02':'ACCEPTAT: refuz nominal după ambalare comisă; BOM2 rămâne.','N01_QTY':'ACCEPTAT: qty0 refuzat, fără delta WMS.','N02_STOC':'ACCEPTAT: necesar12/disponibil10 refuzat, fără delta WMS.','N03_ROL':'ACCEPTAT numai refuz nativ CannotAccessProcess, zero instanță; garda EVA R_DREPT neexecutată.','R01':'ACCEPTAT efecte WMS rollback+retry; AD_PInstance1002649/result1 persistă fără mișcări, deci nu atomicitate globală de metadate.','C01':'DEFECT CONFIRMAT în configurația sintetică documentată: PID/xid distincte READ COMMITTED, invizibilitate înaintea barierei, BOM3 comis, WMS11 persistat.'},
 'reuse_recommendation':['Adaptează procesul, handlerul PO, versiunile PP_Product_BOM și mecanismele native DB/Trx existente. Nu crea un motor WMS ori contabil paralel.','Coordonează citirea/folosirea BOM și editarea lui prin aceeași protecție per firmă+versiune; recitește starea sub protecție, păstrează până la commit/rollback. Verifică dacă imutabilitatea versiunii folosite permite modelul de business.','Ordine unică a blocărilor; la mutarea liniei protejează ambele versiuni ordonat. Include aceeași rețetă în G2.1/G2.2; lacătul exclusiv pe W nu este suficient.'],
 'important_limits':['Contextul actorului/rolului este injectat prin API nativ de laborator; nu login ori autorizare frontend completă.','Factory și4handler-e originale sunt legate programatic. EvaActivator/UI/server rămân dormant; nu întregul deployment operativ.','SurseTest=null și providerul nativ sunt verificate; helper-ele tranzitive nu au instrumentare exhaustivă de linii.','AD_Process1000228 aparține seedului GardenWorld. Identitățile operative nu se transferă.','LastBuildInfo placeholder și FailOnBuildDiffer=N nu sunt rezolvate; acceptare de schemă limitată, nu conformitate globală build/migrări.','NativeQty10, Fact_Acct0 pentru fixturi și count global308 neschimbat nu demonstrează postare, valori contabile globale nemodificate, costuri sau DocAction.','Parametrii sunt în ProcessInfo, AD_PInstance_Para0; nu se atribuie persistență parametrilor.','Sunt2identități de produs distincte per fixtură, nu dovada codurilor nereutilizabile permanent.','Rundele/încercările infra, activarea UI oprită și N03 oracle-stop rămân păstrate, fără credit de produs.'],
 'cleanup':'A05 a închis JVM/PG și port56455 și a șters doar propriul laborator validat; absența directorului este verificată independent. Cache/harness pasiv păstrat. Cele6rădăcini ale altor probe refuzate de aprobare rămân, fără declarație globală de cleanup.',
 'next_checklist':['Recepție A12 a matricei și a identităților:46lecturi nu sunt46execuții și nici46fișiere complete.','C01 pe remediere la noul OID/build, serial/control pozitiv și cauza exactă de refuz, apoi mai multe componente/BOM/G2, ambele ordini de commit, rollback ambele tranzacții, timeout/deadlock/retry.','Nativ DocAction/Fact_Acct:cutii/manoperă o singură dată G1,fără stoc contabil set dezasamblabil suplimentar G2,retur/parțial/anulare.','Frontend ZK cu rol real și traseu meniu→setări→comandă→pick→aviz; model de drepturi pe cabinet/firmă/canal.','CPP/CPA identități distincte nereutilizabile; G3CPP+CPAcapacitate comună/comenzi concurente; AWB/factură conform momentului configurat.','Păstrează toate17contractele deschise; recomandările nu constituie implementări.'],
 'open_contracts':17,'full_file_or_task_closures':0,'global_score':None})
seal=save('SIGILIU_A11_N05_lot03_v1.json',{'algorithm':'SHA256','immutable':True,'files':[report,qa,mapping,ref(O/'Contraoracol_A11_N05_persistenta_v1.json')],'executor_manifest':ref(B/'MANIFEST_A05_N05_lot03_v1.json')})
print(json.dumps({'report':report,'seal':seal,'QA_count':len(checks),'scope_counts':dict(collections.Counter(x['scope'] for x in source_rows))},ensure_ascii=False))
