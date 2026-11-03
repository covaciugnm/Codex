from pathlib import Path
import json,hashlib,sys,tempfile,shutil,subprocess,os,zipfile,datetime,gzip
sys.stdout.reconfigure(encoding='utf8')
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';O=B/'A11/Val02_loturi';O.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
plan=R/'executie/R12_plan_delta/Plan_delta_R12_v2.json';assert h(plan)=='4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276'
with gzip.open(R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf8') as f:catalog={x['path']:x for x in map(json.loads,f)}
sources={}
for folder in ['A09_Helper_corpus_lot02/sources','A08_Helper_rapoarte_lot02/Sources']:
 base=B/folder
 for f in base.rglob('*.py'):
  rel=f.relative_to(base).as_posix();raw=f.read_bytes();oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert oid==catalog[rel]['git_object']
  if rel in sources:assert sources[rel]==raw
  sources[rel]=raw
D='Documentatie/echipa-2026-10-09/T240-ajutor-ecrane-rest/dovezi-81'
N='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab'
HELP=N+'/ajutor/res/help';SCRIPTS={Path(p).name:p for p in sources}
guard=r'''from pathlib import Path
import sys,os,runpy,subprocess,json,socket
sys.stdout.reconfigure(encoding='utf8');sys.stderr.reconfigure(encoding='utf8');sys.dont_write_bytecode=True
root=Path(sys.argv[1]).resolve();source=Path(sys.argv[2]).resolve();args=sys.argv[3:];guard=Path(__file__).resolve();real_run=subprocess.run
allowed={str(p.resolve()) for p in root.rglob('*.py') if p.name!='guard.py'}
pending_command=None
def inside(p):
 try:return Path(p).resolve().is_relative_to(root)
 except (ValueError,TypeError,OSError):return False
def audit(event,a):
 if event.startswith('socket.') or event in ('os.system','os.exec','os.posix_spawn','ctypes.dlopen'):raise PermissionError('A11 network/exec denied')
 if event=='subprocess.Popen':
  exe,cmd,cwd,env=a
  actual_command=cmd if isinstance(cmd,str) else subprocess.list2cmdline(cmd)
  if pending_command is None or actual_command!=pending_command or (exe is not None and str(Path(exe).resolve()).lower()!=str(Path(sys.executable).resolve()).lower()):raise PermissionError('A11 unknown child denied')
 if event=='open':
  p,m,f=a;write=(isinstance(m,str) and any(c in m for c in 'wax+')) or (isinstance(f,int) and f&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if write and not isinstance(p,int) and not inside(p):raise PermissionError('A11 external write denied')
 if event in ('os.remove','os.rmdir','os.mkdir','shutil.rmtree') and not inside(a[0]):raise PermissionError('A11 external mutation denied')
sys.addaudithook(audit)
try:socket.socket();raise AssertionError('network guard')
except PermissionError:print('GUARD network OK',file=sys.stderr)
def observed_run(cmd,*a,**kw):
 global pending_command
 if not isinstance(cmd,list) or len(cmd)<3 or cmd[0]!=sys.executable or cmd[1]!='-I' or str(Path(cmd[2]).resolve()) not in allowed:raise PermissionError('A11 child whitelist')
 actual=[sys.executable,'-I','-X','utf8',str(guard),str(root),str(Path(cmd[2]).resolve())]+cmd[3:]
 pending_command=subprocess.list2cmdline(actual)
 try:cp=real_run(actual,*a,**kw)
 finally:pending_command=None
 with open(root/'children.jsonl','a',encoding='utf8') as f:f.write(json.dumps({'original_command':cmd,'wrapped_command':actual,'returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr},ensure_ascii=False)+'\n')
 return cp
subprocess.run=observed_run
sys.argv=[str(source)]+args
runpy.run_path(str(source),run_name='__main__')
'''
lab=Path(tempfile.mkdtemp(prefix='a11-r12-val02-helpers-',dir='D:/CodexWork')).resolve();assert lab.parent==Path('D:/CodexWork').resolve()
results=[]
def put(root,rel,text):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf8');return p
def base(name):
 d=lab/name;d.mkdir()
 for rel,raw in sources.items():f=d/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
 put(d,'guard.py',guard)
 put(d,D+'/00_progres.tsv','WA11Form\t1\tmanual\tcitit\n')
 put(d,N+'/setup/EvaMetadata.java','class EvaMetadata { String[][] x={{"Ecran A11", "WA11Form", "1"}}; }')
 put(d,'idempiere/plugins/com.eva.ro.saga.theme/src/com/eva/ro/saga/theme/EvaSagaMenuDef.java','menu("Audit"); item("Ecran A11", "Ecran A11");')
 put(d,N+'/form/WA11Form.java','class WA11Form { String titlu() {return "Titlu A11";} }')
 put(d,N+'/documente/res/etichete.tsv','A11\tEticheta\tLabel\n')
 put(d,'idempiere/plugins/com.eva.ro.contab/test/fixtures/help/ecrane.tsv','WA11Form\tTitlu A11\n')
 (d/HELP/'supliment').mkdir(parents=True,exist_ok=True)
 put(d,'Documentatie/help/00_PENTRU_CONSULTANT.md','Niciun verdict în fixture.\n')
 return d
def run(d,script,args,expected,oracle):
 src=d/SCRIPTS[script];cp=subprocess.run([sys.executable,'-I','-X','utf8',str(d/'guard.py'),str(d),str(src)]+list(map(str,args)),cwd=d,capture_output=True,text=True,encoding='utf8',timeout=20,env={**os.environ,'TMP':str(d),'TEMP':str(d),'PYTHONDONTWRITEBYTECODE':'1'})
 assert cp.returncode==expected,(d.name,cp.returncode,cp.stderr)
 for rel,raw in sources.items():assert (d/rel).read_bytes()==raw
 put(d,'stdout.txt',cp.stdout);put(d,'stderr.txt',cp.stderr)
 entry={'case':d.name,'source':SCRIPTS[script],'source_sha256':h(src),'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,'oracle':oracle,'source_unchanged':True,'children':[]}
 if (d/'children.jsonl').exists():entry['children']=[json.loads(l) for l in (d/'children.jsonl').read_text(encoding='utf8').splitlines()]
 results.append(entry);return entry
try:
 # Independent ZIP oracle retains every complete public path, never basename keys.
 for reverse in [False,True]:
  d=base('fragment_order_'+str(reverse));put(d,'mask.txt','lalele albastre\n');put(d,'scan.txt','lalele albastre')
  entries=[('pkg/ajutor/res/help/Same.tsv','lalele albastre'),('pkg/ajutor/res/help/supliment/Same.tsv','portocale verzi')]
  if reverse:entries.reverse()
  with zipfile.ZipFile(d/'public.jar','w') as z:
   for p,t in entries:z.writestr(p,t)
  e=run(d,'fragment_public.py',[d/'mask.txt',d/'public.jar',d/'scan.txt'],0 if reverse else 1,{'expected_full_path_public':True,'public_resource_count':2,'public_paths':[p for p,t in entries]})
  assert 'texte publice citite 1' in e['stdout']
 # Reference helper: same cited line, controlled exact-token location.
 for typ,txt,problems in [('exact','class A11Model {\n int A11_TOKEN;\n}\n',0),('moved','class A11Model {\n int other;\n int A11_TOKEN;\n}\n',1),('deleted','class A11Model {\n int other;\n}\n',0),('substring','class A11Model {\n int A11_TOKEN_EXTRA;\n}\n',0)]:
  d=base('refs_'+typ);put(d,'idempiere/plugins/A11Model.java',txt);v=put(d,'v.md','| rol | rol sintetic | A11Model.java:2 (A11_TOKEN ) | DA |\n')
  e=run(d,'refs_nemarcate.py',[v],0,{'exact_identifier_in_cited_line':typ=='exact','exact_identifier_anywhere':typ in ['exact','moved'],'missing_must_not_be_equivalent_to_valid':True})
  assert 'probleme '+str(problems) in e['stdout']
 # Parent-child behavior: isolated original dependencies; only invocation wrapped to guard and observe the child.
 manual='cap("Audit", "Primul", "WA11Form", "Text primar");\n'
 for typ in ['valid','missing','duplicate']:
  d=base('manual_'+typ)
  if typ!='missing':put(d,N+'/ajutor/ManualEvA.java',manual+('cap("Audit", "Al doilea", "WA11Form", "Text secundar");\n' if typ=='duplicate' else ''))
  if typ=='duplicate':
   e=run(d,'manual_cap.py',['WA11Form'],0,{'chapters_in_synthetic_source':2,'input_validity':'Violates one-chapter-per-screen invariant documented in native ManualEvA.java:2821; diagnostic/ambiguity boundary only.'});assert 'Al doilea' not in e['stdout']
  else:
   e=run(d,'construieste_lot.py',['1'],0,{'expected_child_success':typ=='valid','parent_must_not_assert_reading_after_failed_child':True});report=d/'Documentatie/echipa-2026-10-09/T240-ajutor-ecrane-rest/81_audit_texte_lot1.md';e['persistent_report']=report.read_text(encoding='utf8');e['persistent_report_sha256']=h(report)
   assert e['persistent_report'].count('| OK |')==2 and len(e['children'])==1
   assert e['children'][0]['returncode']==(0 if typ=='valid' else 1)
   if typ=='missing':assert 'FileNotFoundError' in e['children'][0]['stderr']
 # Extension provenance: a stray .txt must not be relabelled as a .tsv anchor.
 for ext in ['tsv','txt']:
  d=base('supplement_'+ext);put(d,HELP+'/supliment/proba.'+ext,'rol\tRol\t\n')
  e=run(d,'clase_corpus.py',['--detalii'],0,{'actual_extension':ext,'actual_path':'supliment/proba.'+ext});assert 'supliment/proba.tsv' in e['stdout'];e['diagnostic_path_exists']=(d/HELP/'supliment/proba.tsv').exists()
 # An unverified but syntactically present row is turned into OK without V.
 d=base('unread_missing_V');put(d,D+'/00_progres.tsv','WA11Form\t1\ttsv\tnecitit\n');put(d,HELP+'/WA11Form.tsv','rol\tRol A11\tA11 role\n')
 e=run(d,'construieste_lot.py',['1'],0,{'reading_event':False,'verification_V_exists':False,'expected_acceptance':'NEVERIFICAT'});report=d/'Documentatie/echipa-2026-10-09/T240-ajutor-ecrane-rest/81_audit_texte_lot1.md';e['persistent_report']=report.read_text(encoding='utf8');e['persistent_report_sha256']=h(report);assert '| OK | — |' in e['persistent_report']
 archive=O/'Probe_independente_helpers_Val02_v1.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(lab.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(lab).as_posix())
finally:
 assert lab.parent==Path('D:/CodexWork').resolve() and lab.name.startswith('a11-r12-val02-helpers-')
 shutil.rmtree(lab)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','plan':ref(plan),'method':'Fixture și oracole proprii. CLI byte-exact. Apelul Python copil este doar învelit de gardă și observat, cu returncode/stdout/stderr păstrate; codul produsului nu este modificat. Hook cooperativ, nu sandbox OS.','cases':results,'case_count':len(results),'archive':ref(archive),'cleanup':{'own_scratch_absent':not lab.exists(),'operational_writes':0,'services':0,'root_retained_masini_scratch_untouched':True},'method_source':{'path':str(Path(__file__)),'sha256':h(Path(__file__))},'full_native_product_credit':False}
dst=O/'Probe_independente_helpers_Val02_v1.json';assert not dst.exists();dst.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'output':ref(dst),'cases':len(results),'cleanup':out['cleanup']},ensure_ascii=False))
