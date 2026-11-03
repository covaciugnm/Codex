from pathlib import Path
import json,hashlib,datetime,subprocess,sys,shutil,os,time,platform
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
P=R/'executie/R12_plan_delta'
PY=Path('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
GATE=P/'A11_verdict_plan_delta_R12_v2.json'
GATE_SHA='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
PLAN_SHA='4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(GATE)==GATE_SHA
gate=json.loads(GATE.read_text(encoding='utf-8-sig'))
assert gate['decision']=='APROBAT_PLAN_10_DIN_10'
assert PLAN_SHA in GATE.read_text(encoding='utf-8-sig')
assert sha(P/'Plan_delta_R12_v2.json')==PLAN_SHA
source=P/'Sources_lues/tools/teste/t240'
checks={'test_clasa_verifica_proba.py':('a42ccc6e7f232a45f9f8c6fed8686904d00774e2ad3a51a68444bd79dd5a9500','c724af2418577941ad264325c9ce401febe530a3'),'verifica_proba.py':('8352ebf2afa6175ae77582efc77166a0c071d2c3806926b7e0ae63da6fde6413','a2da8099f1f63e30c2107ae06df29ebf538698be')}
for n,(h,oid) in checks.items():
 b=(source/n).read_bytes();assert sha(source/n)==h;assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
out=R/'executie/R12_fisiere/A08_T240'/stamp;out.mkdir(parents=True,exist_ok=False)
scratch=Path('D:/CodexWork')/('p01-r12-t240-'+stamp)
scratch.mkdir(exist_ok=False)
assert scratch.resolve().parent==Path('D:/CodexWork').resolve()
own=scratch.resolve();(scratch/'source').mkdir();(out/'source').mkdir()
for n in checks:
 shutil.copyfile(source/n,scratch/'source'/n);shutil.copyfile(source/n,out/'source'/n)
child=Path('D:/CodexWork/p01-r12-t240-child.py');shutil.copyfile(child,out/child.name);shutil.copyfile(Path(__file__),out/Path(__file__).name)
records=[];cleanup={};runtime={'python':sys.version,'platform':platform.platform(),'os_name':os.name}
def run(mode,timeout=60):
 env=os.environ.copy();env.update(TEMP=str(scratch/'tmp'),TMP=str(scratch/'tmp'),PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
 command=[str(PY),'-X','utf8','-I','-B',str(child),str(scratch),mode]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
 try:
  p=subprocess.run(command,cwd=scratch,env=env,capture_output=True,timeout=timeout);rc=p.returncode;stdout=p.stdout;stderr=p.stderr;timed_out=False
 except subprocess.TimeoutExpired as ex:
  rc=None;stdout=ex.stdout or b'';stderr=ex.stderr or b'';timed_out=True
 (out/(mode+'.stdout.txt')).write_bytes(stdout);(out/(mode+'.stderr.txt')).write_bytes(stderr)
 result=scratch/('result_'+mode+'.json')
 if result.exists():shutil.copyfile(result,out/result.name)
 records.append({'mode':mode,'command':command,'UTC_start':start,'elapsed_seconds':time.perf_counter()-t,'exit_code':rc,'timed_out':timed_out,'timeout_seconds':timeout,'stdout':mode+'.stdout.txt','stderr':mode+'.stderr.txt'})
 return rc
try:
 rc=run('original')
 if rc==0:run('original_full',60)
 else:run('selected')
 # Each independent case starts in its own folder; original candidates remain byte-identical.
 run('independent',60)
 for f in scratch.glob('I*_report.tsv'):shutil.copyfile(f,out/f.name)
 (out/'Execution.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','gate_sha':GATE_SHA,'plan_sha':PLAN_SHA,'runtime':runtime,'records':records,'sources':checks,'limitations':['Python audit hook este gard de proces pentru sursele inspectate, nu sandbox OS.','Suita originală și martorii independenți sunt nivel componentă. Nu există UI/ERP/native posting executat.','Numele NU: ... este probat pe filesystem-ul efectiv; nu se presupune refuzul OS înaintea execuției.']},ensure_ascii=False,indent=2),encoding='utf-8')
finally:
 assert scratch.resolve()==own and own.parent==Path('D:/CodexWork').resolve() and own.name.startswith('p01-r12-t240-')
 before=sum(1 for p in own.rglob('*') if p.is_file());shutil.rmtree(own)
 cleanup={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_absolute_target':str(own),'inside_workspace_verified':True,'files_before_cleanup':before,'removed':not own.exists(),'services_created':0,'ports_opened':0,'source_hashes_after':{n:sha(source/n) for n in checks},'source_hashes_unchanged':all(sha(source/n)==h for n,(h,oid) in checks.items())}
 (out/'Cleanup.json').write_text(json.dumps(cleanup,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(out),'records':records,'cleanup':cleanup},ensure_ascii=False))
