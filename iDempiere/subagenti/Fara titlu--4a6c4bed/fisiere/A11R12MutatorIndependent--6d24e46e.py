import ast,contextlib,ctypes,datetime,hashlib,io,json,msvcrt,os,runpy,shutil,socket,sys,zipfile
from pathlib import Path
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
SRC=R/'executie/R12_plan_delta/Sources_lues/Documentatie/echipa-2026-10-09/T343-comenzi-site-mutate-in-program/teste-auditor/b_r1/mutanti_aud_b_r1.py'
LAB=Path('D:/CodexWork/a11-r12-mutator-20261103-v2').resolve()
OUT=R/'executie/R12_fisiere/A11/Val03_loturi'
assert not LAB.exists();LAB.mkdir();OUT.mkdir(exist_ok=True)
raw=SRC.read_bytes();assert hashlib.sha256(raw).hexdigest()=='981ab0bce02027c618237ee9111a4c45a6ca81bed24ffbb05f804af1104b3ebd'
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='a98bd78c02e971f1bb14e29d1e647bb27936eeb6'
copy=LAB/'mutanti_original.py';copy.write_bytes(raw)
guard_on=True
def within(p):
 if isinstance(p,int):
  try:
   buf=ctypes.create_unicode_buffer(32768)
   fun=ctypes.windll.kernel32.GetFinalPathNameByHandleW
   fun.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32];fun.restype=ctypes.c_uint32
   size=fun(msvcrt.get_osfhandle(p),buf,32768,0)
   if not 0<size<32768:return False
   p=buf.value.removeprefix('\\\\?\\')
  except (OSError,ValueError):return False
 try:return Path(p).resolve().is_relative_to(LAB)
 except (TypeError,ValueError):return False
def guard(event,args):
 if not guard_on:return
 if event in ('socket.connect','socket.connect_ex','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.posix_spawn','os.spawn','os.exec'):raise PermissionError('A11 deny '+event)
 if event=='open':
  p,mode,flags=args
  writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
  if writing and not within(p):raise PermissionError('A11 write outside scratch')
 if event in ('os.remove','os.rmdir','os.mkdir','os.chmod','os.utime','shutil.rmtree') and not within(args[0]):raise PermissionError('A11 mutation outside scratch')
 if event in ('os.rename','os.link','os.symlink') and (not within(args[0]) or not within(args[1])):raise PermissionError('A11 link outside scratch')
sys.addaudithook(guard);sys.dont_write_bytecode=True
ns=runpy.run_path(str(copy),run_name='a11_component_only')
canaries=[]
try:
 try:Path('D:/CodexWork/a11-outside-denied-marker.txt').write_text('never created');canaries.append(False)
 except PermissionError:canaries.append(True)
 with socket.socket() as sk:
  try:sk.connect(('127.0.0.1',9));canaries.append(False)
  except PermissionError:canaries.append(True)
 bodies={
 'positive_target':"def order_status_post(n):\n    if n != 1:\n        return 'deny'\n    return 'ok'\n\ndef unrelated(n):\n    return n\n",
 'wrong_next_function':"def order_status_post(n):\n    return 'unchanged'\n\ndef unrelated(n):\n    if n != 1:\n        return 'deny'\n    return 'ok'\n",
 'ambiguous_two_in_target':"def order_status_post(n):\n    if n != 1:\n        print('first')\n    if n != 1:\n        return 'deny'\n    return 'ok'\n",
 'negative_no_anchor':"def unrelated(n):\n    if n != 1:\n        return 'deny'\n    return 'ok'\n"}
 cases=[]
 def structures(text):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
 for name,before in bodies.items():
  case=LAB/name;exp=case/'export';dest=case/'destination';p=exp/'backend/app/api/external_orders.py';p.parent.mkdir(parents=True);(exp/'backend/tests').mkdir(parents=True);p.write_text(before,encoding='utf-8')
  src_hash=hashlib.sha256(p.read_bytes()).hexdigest();stdout=io.StringIO();stderr=io.StringIO()
  with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):rc=ns['aplica']('A07',exp,dest)
  after=(dest/'app/api/external_orders.py').read_text(encoding='utf-8');a=structures(before);b=structures(after)
  changes=[n for n in set(a)|set(b) if a.get(n)!=b.get(n)]
  target=[n for n in ast.walk(ast.parse(after)) if isinstance(n,ast.FunctionDef) and n.name=='order_status_post']
  guard_ifs=[ast.dump(n.test,include_attributes=False) for f in target for n in ast.walk(f) if isinstance(n,ast.If)]
  cases.append({'id':name,'entry':'original aplica(A07, export, destination), not CLI','rc':rc,'stdout':stdout.getvalue(),'stderr':stderr.getvalue(),'before':before,'after':after,'changed_function_names':changes,'target_if_predicates_after':guard_ifs,'export_unchanged':hashlib.sha256(p.read_bytes()).hexdigest()==src_hash,'independent_oracle':'AST function ownership and number of predicate replacements, not source substring alone'})
 assert all(canaries) and all(x['export_unchanged'] for x in cases)
 assert cases[0]['rc']==0 and cases[0]['changed_function_names']==['order_status_post']
 assert cases[1]['rc']==0 and cases[1]['changed_function_names']==['unrelated']
 assert cases[2]['rc']==0 and len(cases[2]['target_if_predicates_after'])==2 and cases[2]['target_if_predicates_after'][0]=='Constant(value=False)' and cases[2]['target_if_predicates_after'][1]!='Constant(value=False)'
 assert cases[3]['rc']==2 and not cases[3]['changed_function_names']
finally:guard_on=False
archive=OUT/'Fixture_A11_mutator_lot03_v1.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(LAB.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(LAB))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'A11 independent','candidate':'df85d33c1648ce2b2df130a60a05ef696e2e5480','source':str(SRC),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':'a98bd78c02e971f1bb14e29d1e647bb27936eeb6','cases':cases,'unique_cases':4,'guard_canaries':{'outside_write_denied':canaries[0],'loopback_connect_denied':canaries[1]},'guard_scope':'Cooperative Python audit hook; not OS sandbox; inspected original helper only. No subprocess or network permitted.','artifact':{'path':str(archive),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},'finding':'Ancorarea este textuală și nu se oprește la limita funcției: A07 poate schimba altă funcție cu rc0. Ambiguitatea textului după ancoră este acceptată și se schimbă prima apariție. Nu demonstrează invaliditatea vreunui mutant executat pe CESIRO1 real.','native_first':'Întărește mutatorul existent cu limite AST ale funcției/numitor exact și hash/diff al țintei; nu construi un alt validator de produs.','persistent_effect':'Numai fișierele sintetic copiate; exportul inițial rămas identic. Nicio DB/serviciu operațional.','cleanup':'Scratch de eliminat separat prin PowerShell cu cale absolută verificată; arhiva păstrată intenționat.'}
p=OUT/'Proba_A11_mutator_lot03_v1.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cases':len(cases),'guard_canaries':canaries,'scratch':str(LAB)},ensure_ascii=False))
