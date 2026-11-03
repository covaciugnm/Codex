import pathlib,json,hashlib,re,datetime,zipfile,gzip
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');G=R/'executie/R12_fisiere/A05_G3_nativ_lot04';O=R/'executie/R12_fisiere/A11/Val04_loturi'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
checks=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'detail':d});assert b,(n,d)
ids=j(G/'Identitati_lectura_G3_v1.json');catalog={}
with gzip.open(R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf8') as f:
 for line in f:
  v=json.loads(line)
  if v['path'] in {x['path'] for x in ids['sources']}:catalog[v['path']]=v
for x in ids['sources']:
 p=G/'surse_df85'/x['path'].split('src/com/eva/ro/contab/')[1];b=p.read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 ck('source SHA/OID '+x['path'],sha(p)==x['sha256'] and oid==x['oid'] and catalog[x['path']]['git_object']==oid)
eva=pathlib.Path(ids['eva_jar']['path']);core=pathlib.Path(ids['native_core']['path']);ck('exact EVA JAR',sha(eva)==ids['eva_jar']['sha256']);ck('exact core JAR',sha(core)==ids['native_core']['sha256'])
zips={'com.eva.ro.contab':zipfile.ZipFile(eva),'org.adempiere.base':zipfile.ZipFile(core)}
for label in ['readiness_g3_v1','business_g3_v1','business_g3_v2','business_g3_v3']:
 t=(G/(label+'.stdout.txt')).read_text(encoding='utf-8-sig')
 ck(label+' seven denied canaries',len(re.findall('^CANARY_DENIED\\|',t,re.M))==7 and 'CANARY_ALLOWED|scratch_write' in t)
 ck(label+' only canary denials','BOUNDARY_DENIALS|7' in t)
 ck(label+' dormant before business',all(f'DORMANCY_BEFORE_PROBE|{name}|state=4|startlevel=50' in t for name in ['com.eva.ro.contab','org.adempiere.ui.zk','org.adempiere.server']))
 ck(label+' native connection','NATIVE_DB|org.compiere.db.DB_PostgreSQL|idempiere|127.0.0.1/32|56455' in t and 'NATIVE_SERVICE_LOCATOR|org.compiere.db.DB_PostgreSQL' in t)
 ck(label+' validators and hooks','org.idempiere.fa.model.ModelValidator' in t and all('HOOK_NULL|'+n in t for n in ['corelare.RezervareStoc.dublaSuma','corelare.FisaCanalProces.surseTest','corelare.SetLista.dublaCitiri']))
 ck(label+' no dormant bundle active at end',not any(re.search('^ACTIVE_END\\|'+re.escape(n)+'\\|',t,re.M) for n in ['com.eva.ro.contab','org.adempiere.ui.zk','org.adempiere.server']))
 for m in re.finditer(r'^CLASS_BINDING\|([^|]+)\|bundle=([^:|]+):[^|]+\|sha256=([0-9a-f]+)\|codeSource=',t,re.M):
  name,bundle,h=m.groups();entry=name.replace('.','/')+'.class';ck(label+' runtime bytecode '+name,hashlib.sha256(zips[bundle].read(entry)).hexdigest()==h)
for z in zips.values():z.close()
readiness=j(G/'Receptie_readiness_G3_v1.json')
for x in readiness['runtime']:ck('runtime cache '+x['path'],sha(pathlib.Path(x['path']))==x['sha256'])
schema=j(G/'Schema_G3_inainte_v1.json');ck('138 schema predicates',len(schema['checks'])==138 and not schema['failed'] and all(x['passed'] and x['ad_exists'] and (x['physical_exists'] or x['virtual']) for x in schema['checks']))
ck('neutralization counts',schema['rows']['counts']==[{'foreign_clients':0,'active_schedulers':0,'active_tokens':0,'unsafe_smtp':0}])
gate=j(R/'executie/R12_fisiere/A11/Val04_preflight/Addendum_A11_G3_F03_F01_v1.json')['utc']
ck('addendum before first continuation checkpoint',gate < j(G/'business_g3_v3.readback_01_G3-F01-product-sentinel.json')['utc'])
final=j(G/'Readback_final_G3_v1.json');ck('final readback readonly',final['read_only'] and final['rows']['session'][0]['readonly']=='on')
ck('local G3 lab absent',not pathlib.Path('D:/CodexWork/a05-r12-native-lab-g3-20261103').exists())
cleanup=j(G/'Cleanup_final_v1.json');ck('executor cleanup documented',cleanup['targetExistsAfter'] is False and cleanup['listenersAfter']==0 and cleanup['ownJvmProcesses']==0 and cleanup['pgStopped'] is True and cleanup['operationalWrites']==0)
p=O/'QA_A11_G3_binding_readiness_v1.json';assert not p.exists();p.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'schema_limit':'138 verificări de existență fizică/AD; nu verificare integrală a defaulturilor și editabilității. IsActive readonly observat separat în v2.','native_source_limit':'Cached source mai nouă, nu identică binarului. Core exact nu conține StorageValidatorProvider/IStorageValidator. Tracer null și drepturi comerciale neprobate.','resources_independent_snapshot':{'utc':'2026-11-03T02:18:00.7669121Z','targetExists':False,'listeners_56455':0,'ownJvmProcesses':0,'method':'Get-NetTCPConnection + Get-CimInstance Win32_Process și Test-Path numai citire, executate de A11; nicio oprire sau ștergere A11.'},'refs':[ref(G/n) for n in ['Schema_G3_inainte_v1.json','Receptie_readiness_G3_v1.json','Readback_final_G3_v1.json','Cleanup_final_v1.json']]},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'output':ref(p),'checks':len(checks)},ensure_ascii=False))
