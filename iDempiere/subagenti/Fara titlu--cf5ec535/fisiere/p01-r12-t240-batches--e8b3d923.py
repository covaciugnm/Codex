from pathlib import Path
import sys,json,hashlib,datetime,subprocess,shutil,os,time,concurrent.futures
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');P=R/'executie/R12_plan_delta'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(P/'A11_verdict_plan_delta_R12_v2.json')=='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
assert json.loads((P/'A11_verdict_plan_delta_R12_v2.json').read_text(encoding='utf-8-sig'))['decision']=='APROBAT_PLAN_10_DIN_10'
checks={'test_clasa_verifica_proba.py':'a42ccc6e7f232a45f9f8c6fed8686904d00774e2ad3a51a68444bd79dd5a9500','verifica_proba.py':'8352ebf2afa6175ae77582efc77166a0c071d2c3806926b7e0ae63da6fde6413'}
source=P/'Sources_lues/tools/teste/t240'
for n,h in checks.items():assert sha(source/n)==h
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
out=R/'executie/R12_fisiere/A08_T240'/('Supplement_'+stamp);out.mkdir(parents=True,exist_ok=False)
root=Path('D:/CodexWork')/('p01-r12-t240-batches-'+stamp);root.mkdir(exist_ok=False)
assert root.resolve().parent==Path('D:/CodexWork').resolve()
child=Path('D:/CodexWork/p01-r12-t240-child-v2.py');shutil.copyfile(child,out/child.name);shutil.copyfile(__file__,out/Path(__file__).name)
PY='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def run(mode):
 scratch=root/mode;scratch.mkdir();(scratch/'source').mkdir();(scratch/'tmp').mkdir();dest=out/mode;dest.mkdir()
 for n in checks:shutil.copyfile(source/n,scratch/'source'/n)
 env=os.environ.copy();env.update(TEMP=str(scratch/'tmp'),TMP=str(scratch/'tmp'),PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
 cmd=[PY,'-X','utf8','-I','-B','-u',str(child),str(scratch),mode];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
 try:
  try:p=subprocess.run(cmd,cwd=scratch,env=env,capture_output=True,timeout=60);stdout=p.stdout;stderr=p.stderr;rc=p.returncode;timeout=False
  except subprocess.TimeoutExpired as ex:stdout=ex.stdout or b'';stderr=ex.stderr or b'';rc=None;timeout=True
  elapsed=time.perf_counter()-t
  (dest/'stdout.txt').write_bytes(stdout);(dest/'stderr.txt').write_bytes(stderr)
  for f in scratch.glob('*.json*'):shutil.copyfile(f,dest/f.name)
  if mode=='cli_utf8':
   for f in (scratch/'tmp/utf8').glob('*'):shutil.copyfile(f,dest/f.name)
  rec={'mode':mode,'UTC_start':start,'elapsed_seconds':elapsed,'exit_code':rc,'timeout':timeout,'timeout_seconds':60,'command':cmd,'inputs_source_sha':checks,'scope':'Original CLI / selecție mutanți; niciun efect UI/DB/ERP.'}
  (dest/'Execution.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
  return rec
 finally:
  target=scratch.resolve();assert target.parent==root.resolve() and target.name==mode
  count=sum(1 for p in target.rglob('*') if p.is_file());shutil.rmtree(target)
  (dest/'Cleanup.json').write_text(json.dumps({'owned_absolute_target':str(target),'inside_workspace_verified':True,'files_before_cleanup':count,'removed':not target.exists(),'services_created':0,'ports_opened':0},ensure_ascii=False,indent=2),encoding='utf-8')
results=[]
try:
 results.append(run('cli_utf8'))
 # Disjoint mutation indices, two independent scratch roots; baseline already observed once.
 modes=['mutants_%d_%d'%(i,min(i+5,33)) for i in range(0,33,5)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for result in pool.map(run,modes):results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
finally:
 assert root.resolve().parent==Path('D:/CodexWork').resolve() and root.name.startswith('p01-r12-t240-batches-')
 shutil.rmtree(root)
 (out/'Cleanup_all.json').write_text(json.dumps({'root':str(root),'removed':not root.exists(),'source_hashes_unchanged':all(sha(source/n)==h for n,h in checks.items())},ensure_ascii=False,indent=2),encoding='utf-8')
(out/'Execution_all.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('OUTPUT '+str(out),flush=True)
