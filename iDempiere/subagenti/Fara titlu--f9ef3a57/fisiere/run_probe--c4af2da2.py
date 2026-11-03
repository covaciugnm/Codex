import pathlib,json,hashlib,datetime,shutil,subprocess,os,sys
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); OUT=R/'executie/R12_fisiere/A08_Catalog_paginare_lot05'; LAB=pathlib.Path('D:/CodexWork/a08-catalog-json-l05-20261103')
JAVA=pathlib.Path('C:/Program Files/Java/jdk-21/bin/java.exe');JAVAC=JAVA.with_name('javac.exe')
CORE=pathlib.Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar');GSON=pathlib.Path('D:/CodexWork/a05-r12-native-cache/com.google.gson_2.9.0.jar')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def raw(p):return p.read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def dump(p,x):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def inventory(root):return [{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
def invoke(name,args,timeout=60,env=None):
 start=now();result=subprocess.run([str(a) for a in args],cwd=LAB,env=env,capture_output=True,timeout=timeout)
 (LAB/'logs'/f'{name}.stdout.txt').write_bytes(result.stdout);(LAB/'logs'/f'{name}.stderr.txt').write_bytes(result.stderr)
 dump(LAB/'logs'/f'{name}.json',{'start':start,'end':now(),'command':[str(a) for a in args],'returncode':result.returncode,'stdout':ref(LAB/'logs'/f'{name}.stdout.txt'),'stderr':ref(LAB/'logs'/f'{name}.stderr.txt')});return result
protocol=load(OUT/'Protocol_paginare_JSON_v1.json'); gate=R/'executie/R12_fisiere/A11/Val05_preflight/Verdict_A11_protocol_paginare_JSON_v1.json'; additive=R/'executie/R12_fisiere/A11/Val05_preflight/Addendum_A11_paginare_RegistruLegal_v1.json'
assert sha(gate)=='7fe60023b98b13a319559cbe60b92b1fc034545ac784e3883c63e062c8955971';assert sha(additive)=='88f0d9a3365d6de6d9b4fef76726b8c940fb27474daf1507cb697552baa9608a'
phase=sys.argv[1]
if phase=='prepare_compile':
 assert not (LAB/'Preparation.json').exists()
 for p in ['classes','lib','fixture/tenants/valid','fixture/tenants/empty','fixture/tenants/absent','fixture/shared','fixture/media','logs','empty_sourcepath']: (LAB/p).mkdir(parents=True,exist_ok=True)
 for s in protocol['runtime']:assert sha(pathlib.Path(s['path']))==s['sha256']
 assert sha(CORE)=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'
 shutil.copyfile(GSON,LAB/'lib/gson.jar')
 sourceinfo=[];sources=[]
 for s in protocol['source_identities']:
  if s['role']=='STATIC_ROUTE_CONTEXT_ONLY':continue
  p=OUT/'Sources'/s['path'];assert sha(p)==s['sha256'];dest=LAB/'source'/s['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);sources.append(dest);sourceinfo.append(dict(s,local=ref(dest)))
 ad=load(OUT/'Addendum_dependenta_RegistruLegal_v1.json');s=ad['source'];p=R/s['path'];assert sha(p)==s['sha256'];dest=LAB/'source'/s['repository_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);sources.append(dest);sourceinfo.append(dict(s,local=ref(dest),role='ORIGINAL_COMPILE_DEPENDENCY_NOT_CALLED'))
 products=[{'id':'P'+str(i),'name':{'ro':'Produs '+str(i)+' țest'},'slug':{'ro':'produs-'+str(i)},'short_description':{'ro':'Descriere sintetică'},'description':{'ro':'Numai probă locală'},'price_ron':10*i,'sku':'SYNTH-'+str(i),'category_ids':['CAT1'],'categories':[{'ro':'Categorie'}],'is_in_stock':True,'images':[],'reviews':[],'attributes':[]} for i in range(1,4)]
 for tenant,ps in [('valid',products),('empty',[])]:dump(LAB/f'fixture/tenants/{tenant}/catalog.json',{'categories':[{'id':'CAT1','name':{'ro':'Categorie'},'children':[]}] if ps else [],'collections':[],'products':ps})
 (LAB/'fixture/canary.txt').write_text('A08_SYNTHETIC_ONLY',encoding='utf8');dump(LAB/'fixture/cases.json',protocol['cases'])
 policy='grant {\n permission java.io.FilePermission "'+LAB.as_posix()+'/-", "read";\n permission java.io.FilePermission "'+LAB.as_posix()+'", "read";\n permission java.util.PropertyPermission "*", "read";\n'+''.join(' permission java.lang.RuntimePermission "getenv.'+k+'";\n' for k in ['EVA_WEBSHOP_DATA','EVA_WEBSHOP_SHARED','EVA_WEBSHOP_MEDIA'])+'};\n'
 (LAB/'probe.policy').write_text(policy,encoding='utf8')
 compileargs=[JAVAC,'-encoding','UTF-8','-proc:none','-implicit:none','-sourcepath',LAB/'empty_sourcepath','-cp',str(LAB/'lib/gson.jar')+';'+str(CORE),'-d',LAB/'classes',*sources,LAB/'harness/AuditCatalogPagination.java',LAB/'harness/CatalogProductProbe.java']
 dump(LAB/'Preparation.json',{'utc':now(),'gate':ref(gate),'addendum':ref(additive),'sources':sourceinfo,'compile_classpath':[ref(LAB/'lib/gson.jar'),ref(CORE)],'runtime_classpath':[str(LAB/'classes'),str(LAB/'lib/gson.jar')],'core_runtime_present':False,'reflection_permissions':[],'harness':[ref(LAB/'harness/AuditCatalogPagination.java'),ref(LAB/'harness/CatalogProductProbe.java')],'runner':ref(pathlib.Path(__file__)),'policy':ref(LAB/'probe.policy'),'fixtures':inventory(LAB/'fixture'),'compile_command':[str(a) for a in compileargs],'initial_root_files':{'D:/CodexWork/AuditCatalogPagination.java':False,'D:/CodexWork/p01-run-catalog-json-l05.py':False},'product_executions_before':0})
 result=invoke('compile_v1',compileargs); print(json.dumps({'phase':phase,'compile_rc':result.returncode,'preparation':ref(LAB/'Preparation.json')},ensure_ascii=False));sys.exit(result.returncode)
elif phase=='run':
 runid=sys.argv[2]; assert not (LAB/'logs'/f'{runid}.json').exists();prep=load(LAB/'Preparation.json');before=inventory(LAB/'fixture');dump(LAB/'logs'/f'{runid}.before.json',{'utc':now(),'fixture':before,'sources':[ref(LAB/'source'/s.get('repository_path',s.get('path'))) for s in prep['sources']],'classes':inventory(LAB/'classes')})
 env={k:v for k,v in os.environ.items() if k in ['SystemRoot','SYSTEMROOT','WINDIR','COMSPEC']};env.update({'EVA_WEBSHOP_DATA':str(LAB/'fixture/tenants'),'EVA_WEBSHOP_SHARED':str(LAB/'fixture/shared'),'EVA_WEBSHOP_MEDIA':str(LAB/'fixture/media'),'TEMP':str(LAB/'logs'),'TMP':str(LAB/'logs')})
 args=[JAVA,'-Xmx128m','-Djava.awt.headless=true','-Dfile.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+(LAB/'probe.policy').as_uri(),'-Xlog:class+load=info:file=logs/'+runid+'.classload.log','-cp',str(LAB/'classes')+';'+str(LAB/'lib/gson.jar'),'AuditCatalogPagination',LAB]
 dump(LAB/'logs'/f'{runid}.admission.json',{'utc':now(),'command':[str(a) for a in args],'environment':env,'runtime_classpath':[str(LAB/'classes'),str(LAB/'lib/gson.jar')],'core_runtime_present':False,'policy':ref(LAB/'probe.policy'),'preparation':ref(LAB/'Preparation.json')})
 result=invoke(runid,args,env=env);after=inventory(LAB/'fixture');dump(LAB/'logs'/f'{runid}.after.json',{'utc':now(),'fixture':after,'fixtures_unchanged':after==before,'sources':[ref(LAB/'source'/s.get('repository_path',s.get('path'))) for s in prep['sources']],'classes':inventory(LAB/'classes')})
 print(json.dumps({'phase':phase,'id':runid,'rc':result.returncode,'fixtures_unchanged':after==before,'stdout_tail':result.stdout.decode('utf8',errors='replace')[-1800:],'stderr_tail':result.stderr.decode('utf8',errors='replace')[-1000:]},ensure_ascii=False));sys.exit(result.returncode)
else:raise ValueError(phase)
