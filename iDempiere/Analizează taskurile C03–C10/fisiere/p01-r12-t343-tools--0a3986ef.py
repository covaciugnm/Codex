from pathlib import Path
import os,sys,json,hashlib,subprocess,shutil,gzip,difflib,datetime,zipfile
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A06_T343_instrumente_lot03'
L=Path('D:/CodexWork/p01-r12-t343-tools-l03-v2')
PY=Path(sys.executable);BASH=Path('C:/Program Files/Git/bin/bash.exe');GIT=Path('C:/Program Files/Git/cmd/git.exe')
HEAD='df85d33c1648ce2b2df130a60a05ef696e2e5480'
D='Documentatie/echipa-2026-10-09/T343-comenzi-site-mutate-in-program'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def unix(p):return '/'+p.drive[0].lower()+p.as_posix()[2:]
def contained(p):
 p=Path(p).resolve();assert p!=L.resolve() and p.is_relative_to(L.resolve());return p
def run(args,cwd,env=None,timeout=40):
 p=subprocess.run([str(x) for x in args],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 return {'args':[str(x) for x in args],'cwd':str(cwd),'rc':p.returncode,'stdout':p.stdout.decode('utf-8','replace'),'stderr':p.stderr.decode('utf-8','replace')}
assert not L.exists(),'unique owned scratch required'
L.mkdir();(O/'sources').mkdir(exist_ok=True);(O/'cases').mkdir(exist_ok=True)
rows=[json.loads(x) for x in gzip.open(R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf-8')]
sources=[]
for name in ['mutanti_aud_b_r1.py','rulare_aud_b_r1.sh','test_clasa_lot_b_r1.sh']:
 path=D+'/teste-auditor/b_r1/'+name;x=next(x for x in rows if x['path']==path);p=R/'executie/R12_plan_delta/Sources_lues'/path;data=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_object'];shutil.copyfile(p,O/'sources'/name);sources.append(dict(x,sha256=sha(p)))
put(O/'Sources.json',sources)
guard=r'''from pathlib import Path
import sys,os,runpy,socket,json
sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
root=Path(os.environ['AUDIT_ROOT']).resolve()
sys.dont_write_bytecode=True
def pathok(x):
 if isinstance(x,int):return
 p=Path(os.fsdecode(x)).resolve()
 if not p.is_relative_to(root):raise PermissionError('AUDIT_WRITE_OUTSIDE')
 protected=os.environ.get('AUDIT_EXPORT')
 if protected and p.is_relative_to(Path(protected).resolve()):raise PermissionError('AUDIT_EXPORT_IMMUTABLE')
def hook(e,a):
 if e.startswith('socket.') or e in ('subprocess.Popen','os.system'):raise PermissionError('AUDIT_EXTERNAL_DENIED')
 if e=='open':
  mode=a[1];flags=a[2]
  if (isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):pathok(a[0])
 if e in ('os.remove','os.rmdir','os.mkdir','os.chmod','os.utime'):pathok(a[0])
 if e in ('os.rename','os.link','os.symlink'):pathok(a[0]);pathok(a[1])
sys.addaudithook(hook)
if sys.argv[1]=='--pytest':
 sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');sys.argv=['pytest']+sys.argv[2:];runpy.run_module('pytest',run_name='__main__');raise SystemExit
target=Path(sys.argv[1]).resolve();args=sys.argv[2:]
if target.name=='mutanti_aud_b_r1.py' and args and args[0]=='aplica':
 exp=Path(args[2]).resolve();dest=Path(args[3]).resolve()
 if not exp.is_relative_to(root) or not dest.is_relative_to(root) or dest==root or exp==dest or exp.is_relative_to(dest):raise PermissionError('AUDIT_DESTRUCTIVE_TARGET_REFUSED')
sys.argv=[str(target)]+args;runpy.run_path(str(target),run_name='__main__')
'''
write(L/'guard.py',guard);shutil.copyfile(L/'guard.py',O/'guard.py')
shim=r'''from pathlib import Path
import os,sys,json,shutil,subprocess
sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
root=Path(os.environ['AUDIT_ROOT']).resolve();work=Path(os.environ['AUDIT_CASE']).resolve();cmd=sys.argv[1];args=sys.argv[2:]
def native(s):
 if len(s)>3 and s[0]=='/' and s[2]=='/' and s[1].isalpha():s=s[1].upper()+':'+s[2:]
 return Path(s).resolve()
def checked(s):
 p=native(s)
 if p==root or not p.is_relative_to(root):raise SystemExit('REFUSED OUTSIDE OWNED LAB')
 return p
with (work/'shim_events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'command':cmd,'args':args})+'\n')
if cmd in ('curl','wget','ssh','scp','powershell','pwsh'):raise SystemExit(90)
if cmd=='queue':
 if args[0]=='cere':
  if os.environ.get('QUEUE_REFUSE')=='1':raise SystemExit(10)
  print('SYNTHETIC_SLOT')
 raise SystemExit(0)
if cmd in ('ln','rm'):raise SystemExit(0) # cleanup/link integration explicitly not exercised
if cmd=='find':
 checked(args[0])
 if '-delete' in args:raise SystemExit(0) # destructive native find not invoked
 raise SystemExit(subprocess.run(['C:/Program Files/Git/usr/bin/find.exe']+args).returncode)
if cmd=='rsync':
 src=checked(args[-2]);dest=checked(args[-1]);assert dest==work/'work'/'exp'
 dest.mkdir(parents=True,exist_ok=True)
 for p in list(dest.iterdir()):
  assert p.resolve().is_relative_to(dest.resolve())
  if p.is_dir():shutil.rmtree(p)
  else:p.unlink()
 shutil.copytree(src,dest,dirs_exist_ok=True);raise SystemExit(0)
if cmd=='docker':
 assert args[0]=='exec'
 mid=args[args.index('-w')+1].split('/')[-1];mode=os.environ['DOCKER_CASE']
 selected='pass' if mid=='A00' and mode!='baseline_error' else ('setup' if mode=='baseline_error' else mode)
 row=json.loads((root/'pytest_results.json').read_text())[selected]
 sys.stdout.write(row['stdout']);sys.stderr.write(row['stderr']);raise SystemExit(row['rc'])
if cmd=='git':
 assert args[0]=='-C';checked(args[1]);assert args[2] in ('archive','rev-parse')
 raise SystemExit(subprocess.run(['C:/Program Files/Git/cmd/git.exe']+args).returncode)
raise SystemExit('UNKNOWN SHIM')
'''
write(L/'shim.py',shim);shutil.copyfile(L/'shim.py',O/'shim.py')
shims=L/'shims';shims.mkdir()
for cmd in ['queue','docker','rsync','ln','rm','find','git','ssh','scp','curl','wget','powershell','pwsh']:
 write(shims/cmd,'#!/usr/bin/env bash\nexec "'+PY.as_posix()+'" -I "'+(L/'shim.py').as_posix()+'" '+cmd+' "$@"\n')
write(shims/'python3','#!/usr/bin/env bash\n[ "${1:-}" = -I ] && shift\nexec "'+PY.as_posix()+'" -I "'+(L/'guard.py').as_posix()+'" "$@"\n')
baseenv=dict(os.environ,AUDIT_ROOT=str(L),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONIOENCODING='utf-8',TMP=str(L/'tmp'),TEMP=str(L/'tmp'),GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
(L/'tmp').mkdir()
protocol={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'files':sources,'gate':'R12v2 10/10 and A11 Val03 preflight23e2a6d93d137c47cd81f6be930fbf67de4c26357a181d95f858af525e687824','owner':'A06','peer':'A01/A11','task':'P01.C10.T0025','method':'Original I14; Bash I15/I16 with only hardcoded CB/R paths remapped. Real local Git and original partner scanner; Docker/queue/link/delete orchestration shims. Pytest phase outputs measured on local synthetic tests then replayed by Docker shim. No site implementation, Docker container, DB or partner API is executed.','boundary':'All paths resolved within unique own scratch; Python audit hook denies external writes/network/subprocess. Shell source inspected, all external-capable tool names shadowed. Not an OS sandbox. find-delete/rm/ln are recorded no-ops; resource lifecycle is not credited.','oracles':['Mutation target location and source export hash conservation, distinct outcomes missing/ambiguous/compile error.','A00 control vs assertion/setup/collection/no-tests; compilation/export errors separated from mutation kill.','Class aggregator fresh complete logs vs A00 only/duplicate, stale logs with runner failure, unexpected surviving mutant, no log and skipped mutants.'],'fixture_kind':'Wholly synthetic local repos, not a checkout falsely labeled CESIRO1.','new_product_test_scope':'Helpers only; dependency scanner execution adds no full-file credit.'}
put(O/'Protocol_sigillat_inainte_executie.json',protocol)
results=[]
def savecase(name,group,res,extra=None):
 res={'id':name,'group':group,**res,**(extra or {})};put(O/'cases'/(name+'.json'),res);results.append(res);put(O/'Results_in_progress.json',results)
def envcase(case):return dict(baseenv,AUDIT_CASE=str(case))
def guardrun(script,args,cwd,env):return run([PY,'-I',L/'guard.py',script,*args],cwd,env)
# Measured pytest exit semantics; these tests contain no application code.
pytest_results={}
fixtures={'pass':'def test_witness():\n    assert True\n','assert':'def test_witness():\n    assert False, "synthetic assertion"\n','setup':'import pytest\n@pytest.fixture\ndef broken():\n    raise RuntimeError("synthetic setup error")\ndef test_witness(broken):\n    pass\n','collect':'def test_bad(:\n    pass\n','empty':'# synthetic no test definitions\n'}
for mode,code in fixtures.items():
 case=L/('pytest_'+mode);case.mkdir();write(case/'test_witness.py',code)
 res=guardrun('--pytest',['-p','no:cacheprovider','--log-file='+str(case/'pytest.log'),'-q','-x',str(case/'test_witness.py')],case,envcase(case));pytest_results[mode]=res
put(L/'pytest_results.json',pytest_results);put(O/'Pytest_phase_oracles.json',pytest_results)
assert {k:v['rc'] for k,v in pytest_results.items()}=={'pass':0,'assert':1,'setup':1,'collect':2,'empty':5}
# I14 original mutation generator.
mut=O/'sources/mutanti_aud_b_r1.py'
for sel in [None,'ext','panou','bl','unknown']:
 case=L/('list_'+str(sel));case.mkdir();res=guardrun(mut,['list']+([] if sel is None else [sel]),case,envcase(case));savecase('I14_list_'+str(sel),'I14',res)
templates={
'baseline':('A00','def order_status_post():\n    n=1\n    if n != 1:\n        return False\n    return True\n'),
'valid':('A07','def order_status_post():\n    n=1\n    if n != 1:\n        return False\n    return True\n'),
'anchor_missing':('A07','def other():\n    if n != 1:\n        return False\n'),
'anchor_double':('A07','def order_status_post():\n    if n != 1:\n        pass\ndef order_status_post2():\n    return 1\n'),
'old_missing':('A07','def order_status_post():\n    return 1\n'),
'old_double':('A07','def order_status_post():\n    if n != 1:\n        pass\n    if n != 1:\n        pass\n'),
'old_next_function':('A07','def order_status_post():\n    return 1\ndef other():\n    if n != 1:\n        return False\n'),
'compile_failure':('A10','def order_status_post():\n    for pas in drum:\n        pass\n'),
'unknown_id':('AXX','def order_status_post():\n    return 1\n'),
'missing_tests':('A00','def order_status_post():\n    return 1\n'),
'retry_valid':('A07','def order_status_post():\n    n=1\n    if n != 1:\n        return False\n    return True\n')}
for label,(mid,code) in templates.items():
 case=L/('mut_'+label);case.mkdir();exp=case/'export';write(exp/'backend/app/api/external_orders.py',code);write(exp/'backend/app/__pycache__/inert.txt','cache')
 if label!='missing_tests':write(exp/'backend/tests/test_inert.py','# synthetic\n')
 dest=case/'output';dest.mkdir();write(dest/'old_sentinel.txt','old output')
 env=dict(envcase(case),AUDIT_EXPORT=str(exp));before={p.relative_to(exp).as_posix():sha(p) for p in exp.rglob('*') if p.is_file()}
 res=guardrun(mut,['aplica',mid,str(exp),str(dest)],case,env);after={p.relative_to(exp).as_posix():sha(p) for p in exp.rglob('*') if p.is_file()};assert before==after
 output=dest/'app/api/external_orders.py';savecase('I14_'+label,'I14',res,{'source_unchanged':True,'source_sha256':before,'output':output.read_text() if output.exists() else None,'old_sentinel_survived':(dest/'old_sentinel.txt').exists(),'pycache_copied':(dest/'app/__pycache__').exists()})
for label,args in [('unknown_command',['nonsense']),('no_arguments',[])]:
 case=L/('cli_'+label);case.mkdir();savecase('I14_'+label,'I14',guardrun(mut,args,case,envcase(case)))
for label in ['same_export','parent_export']:
 case=L/('guard_'+label);case.mkdir();exp=case/'export';write(exp/'backend/app/inert.py','# fixture\n');(exp/'backend/tests').mkdir();dest=exp if label=='same_export' else case
 res=guardrun(mut,['aplica','A00',str(exp),str(dest)],case,dict(envcase(case),AUDIT_EXPORT=str(exp)));assert 'AUDIT_DESTRUCTIVE_TARGET_REFUSED' in res['stderr'];savecase('BOUNDARY_'+label,'HARNESS_GUARD',res)

def initrepo(repo,site=False):
 repo.mkdir(parents=True)
 if site:
  write(repo/'backend/app/integrations/baselinker/shipping.py','def auto_issue():\n    rows = filtreaza_procesare_locala(session, tenant_id, rows)\n    return rows\n')
  write(repo/'backend/tests/test_inert.py','# synthetic\n')
  for p in ['database/README','docs/README','frontend/src/i18n/README']:write(repo/p,'synthetic\n')
 else:
  write(repo/D/'fixture.py','x = 1\n');write(repo/'tools/teste/t343b/fixture.py','x = 2\n')
 for a in [['init','-q'],['add','.'],['-c','user.name=SyntheticAudit','-c','user.email=audit@example.invalid','commit','-q','-m','synthetic fixture']]:
  x=run([GIT,'-C',repo,*a],repo,baseenv);assert x['rc']==0,x
 return run([GIT,'-C',repo,'rev-parse','HEAD'],repo,baseenv)['stdout'].strip()

def bashrun(script,args,case,env):
 launcher='export PATH="'+unix(shims)+':/mingw64/bin:/usr/bin:/bin"; exec bash "$@"'
 return run([BASH,'--noprofile','--norc','-c',launcher,'audit',script,*args],case,env,60)

# I15 original flow, only the queue absolute path changes.
for mode in ['assert','setup','collect','empty','pass','baseline_error','queue_refused','bad_export']:
 case=L/('runner_'+mode);case.mkdir();repo=case/'repo';commit=initrepo(repo,True);work=case/'work';(work/'out').mkdir(parents=True);(work/'exp').mkdir()
 write(work/'site.stare','PY=SYNTHETIC_PYTEST\n');write(work/'parole.env','PG_PW=synthetic\nSF_PW=synthetic\nADM_PW=synthetic\nSECRETS_KEY=synthetic\nJWT_SECRET=synthetic\nSECRET_KEY=synthetic\n')
 suite=case/'suite';suite.mkdir();shutil.copyfile(mut,suite/mut.name)
 orig=(O/'sources/rulare_aud_b_r1.sh').read_text();mapped=orig.replace('CB=/home/saga-server/Documents/EvA-Contab/tools/status/coada_builduri.sh','CB='+unix(shims/'queue'));assert mapped!=orig
 script=suite/'rulare_aud_b_r1.sh';write(script,mapped)
 write(O/'I15_path_only.diff',''.join(difflib.unified_diff(orig.splitlines(True),mapped.splitlines(True),fromfile='original',tofile='comparator')))
 env=dict(envcase(case),EVA_CERE_SESIUNE='synthetic',EVA_CERE_CONT='synthetic',EVA_SLOT_PID='12345',EVA_T343B_LUCRU=unix(work),EVA_T343B_COPIE=unix(repo),DOCKER_CASE='assert' if mode in ['queue_refused','bad_export'] else mode,QUEUE_REFUSE='1' if mode=='queue_refused' else '0')
 res=bashrun(script,['bl','NO_SUCH_COMMIT' if mode=='bad_export' else commit,'probe','tests/test_inert.py'],case,env)
 logs={p.name:p.read_text(encoding='utf-8',errors='replace') for p in (work/'out').glob('*.txt')};events=(case/'shim_events.jsonl').read_text() if (case/'shim_events.jsonl').exists() else ''
 savecase('I15_'+mode,'I15_COMPARATOR',res,{'logs':logs,'shim_events':events,'repo_commit':commit,'script_sha256':sha(script),'limit':'Docker, slot, rsync and links are local orchestration shims; no site/DB assertion; original mutator executed.'})

# I16 class aggregator with real Git archive and original scanner; runner is an explicit fixture.
runner_stub=r'''#!/usr/bin/env bash
set -u
s=$1; c=$2; e=$3; log="$EVA_T343B_LUCRU/out/$e.aud.txt"
case "$AGG_MODE" in
stale_fail|no_log_fail) echo "synthetic runner refused" >&2; exit 10;;
only_control) printf 'A00 CONTROL VERDE | synthetic\n' > "$log";;
duplicate_control) printf 'A00 CONTROL VERDE | synthetic\nA00 CONTROL VERDE | synthetic\n' > "$log";;
empty) : > "$log";;
unknown_live) printf 'A00 CONTROL VERDE | synthetic\nA99 REZULTAT VIU | synthetic\n' > "$log";;
not_run) printf 'A00 CONTROL VERDE | synthetic\nA01 NERULAT | synthetic\n' > "$log";;
*)
 printf 'A00 CONTROL VERDE | synthetic\n' > "$log"
 case "$s" in ext) ids='01 02 03 04 05 06 07 08 09 10';; panou) ids='11 12 13 14 15 16 17 18 19 20 23';; bl) ids='21 22';; esac
 for i in $ids; do printf 'A%s REZULTAT UCIS | synthetic assertion\n' "$i" >> "$log"; done;;
esac
cat "$log"
'''
for mode in ['complete','only_control','stale_fail','no_log_fail','duplicate_control','empty','unknown_live','not_run','skip']:
 case=L/('class_'+mode);case.mkdir();repo=case/'repo';commit=initrepo(repo,False);(repo/'.lucru/t343b-aud').mkdir(parents=True);shutil.copyfile(O/'garda_parteneri_scriere.py',repo/'tools/teste/garda_parteneri_scriere.py')
 work=case/'work';(work/'out').mkdir(parents=True);suite=case/'suite';suite.mkdir();write(suite/'rulare_aud_b_r1.sh',runner_stub)
 if mode=='stale_fail':
  for s in ['ext','panou','bl']:write(work/'out'/('clasa_'+s+'.aud.txt'),'A00 CONTROL VERDE | OLD_COMMIT_OLD_RUN\nA21 REZULTAT UCIS | OLD_COMMIT_OLD_RUN\n')
 orig=(O/'sources/test_clasa_lot_b_r1.sh').read_text();mapped=orig.replace('R=/home/saga-server/Documents/EvA-Contab;', 'R='+unix(repo)+';');assert mapped!=orig
 script=suite/'test_clasa_lot_b_r1.sh';write(script,mapped)
 write(O/('I16_'+mode+'_path_only.diff'),''.join(difflib.unified_diff(orig.splitlines(True),mapped.splitlines(True),fromfile='original',tofile='comparator')))
 env=dict(envcase(case),EVA_T343B_LUCRU=unix(work),AGG_MODE=mode)
 res=bashrun(script,[commit,'SYNTHETIC_SITE_COMMIT']+(['--fara-mutanti'] if mode=='skip' else []),case,env)
 logs={p.name:p.read_text() for p in (work/'out').glob('*.txt')};savecase('I16_'+mode,'I16_COMPARATOR',res,{'logs':logs,'repo_commit':commit,'script_sha256':sha(script),'limit':'Original partner scanner and Git archive; runner/logs synthetic dependency. No real T343 pipeline or mutant equivalence certified.'})
put(O/'Results.json',results)
put(O/'Post_execution_source_check.json',{'all_source_sha_unchanged':all(sha(O/'sources'/Path(x['path']).name)==x['sha256'] for x in sources),'head':HEAD})
# Preserve exact fixtures/harness before separately authorized cleanup.
with zipfile.ZipFile(O/'Fixture_and_harness.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in L.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(L).as_posix())
print(json.dumps({'output':str(O),'cases':len(results),'groups':{k:sum(x['group']==k for x in results) for k in sorted({x['group'] for x in results})},'result_rc':{x['id']:x['rc'] for x in results},'scratch_retained_until_review':str(L)},ensure_ascii=False))
