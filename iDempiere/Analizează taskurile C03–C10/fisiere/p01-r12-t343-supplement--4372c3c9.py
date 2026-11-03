from pathlib import Path
import sys,os,json,subprocess,shutil,hashlib,zipfile,datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A06_T343_instrumente_lot03';L=Path('D:/CodexWork/p01-r12-t343-tools-l03-v2');PY=Path(sys.executable)
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def unix(p):return '/'+p.drive[0].lower()+p.as_posix()[2:]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
env=dict(os.environ,AUDIT_ROOT=str(L),PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
probe=L/'post_canaries.py';outside=L.parent/'p01-r12-boundary-canary-never.txt';assert not outside.exists()
write(probe,'''import socket,os
from pathlib import Path
results=[]
def run(name,fn):
 try:fn();results.append((name,"FAILED"))
 except PermissionError:results.append((name,"BLOCKED"))
run("network",lambda:socket.socket())
run("outside_write",lambda:Path("D:/CodexWork/p01-r12-boundary-canary-never.txt").write_text("synthetic"))
run("process",lambda:os.system("echo synthetic"))
print(results)
assert all(x[1]=="BLOCKED" for x in results)
''')
p=subprocess.run([str(PY),'-I',str(L/'guard.py'),str(probe)],env=env,cwd=L,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert p.returncode==0 and not outside.exists()
canary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timing':'POST_EXECUTION_BOUNDARY_CHECK, not falsely backdated to preflight','rc':p.returncode,'stdout':p.stdout.decode('utf-8'),'stderr':p.stderr.decode('utf-8'),'guard_sha256':sha(L/'guard.py'),'outside_file_absent':not outside.exists(),'credit':'Harness only, no product criterion.'}
(O/'Post_canaries.json').write_text(json.dumps(canary,ensure_ascii=False,indent=2),encoding='utf-8')
case=L/'class_setup_from_original';assert not case.exists();case.mkdir();repo=case/'repo';shutil.copytree(L/'class_complete/repo',repo)
work=case/'work';(work/'out').mkdir(parents=True);suite=case/'suite';suite.mkdir()
stub=(L/'class_complete/suite/rulare_aud_b_r1.sh').read_text();needle='case "$AGG_MODE" in\n';assert needle in stub
stub=stub.replace(needle,'if [ "$s" = bl ]; then cat "$AUDIT_LOG_SOURCE" > "$log"; cat "$log"; exit 0; fi\n'+needle)
write(suite/'rulare_aud_b_r1.sh',stub)
orig=(O/'sources/test_clasa_lot_b_r1.sh').read_text();script=suite/'test_clasa_lot_b_r1.sh';write(script,orig.replace('R=/home/saga-server/Documents/EvA-Contab;','R='+unix(repo)+';'))
git='C:/Program Files/Git/cmd/git.exe';commit=subprocess.check_output([git,'-C',str(repo),'rev-parse','HEAD'],env=env,text=True).strip()
source=L/'runner_setup/work/out/probe.aud.txt';assert 'UCIS (ERROR ' in source.read_text()
env.update(AUDIT_CASE=str(case),EVA_T343B_LUCRU=unix(work),AGG_MODE='complete',AUDIT_LOG_SOURCE=unix(source))
launch='export PATH="'+unix(L/'shims')+':/mingw64/bin:/usr/bin:/bin"; exec bash "$@"'
args=['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc','-c',launch,'audit',str(script),commit,'SYNTHETIC_SITE_COMMIT']
p=subprocess.run(args,env=env,cwd=case,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
data={'id':'I16_setup_from_original_I15_BL','group':'I16_COMPARATOR','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'args':args,'rc':p.returncode,'stdout':p.stdout.decode('utf-8'),'stderr':p.stderr.decode('utf-8'),'input_original_I15_log_sha256':sha(source),'source_case':'I15_setup','output_logs':{x.name:x.read_text() for x in (work/'out').glob('*.txt')},'oracle':'BL log contains original I15 classifications UCIS(ERROR) from a real pytest setup error fixture. ext/panou runner outputs are synthetic complete controls. Expected no complete mutant reception.','limit':'Comparator composition, not real Docker/CESIRO1 tests; two other sets are synthetic controls.'}
assert p.returncode==0 and 'mutanti=OK' in data['stdout'] and 'UCIS (ERROR ' in data['stdout']
(O/'Supplement_case.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(O/'Supplement_fixture.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in case.rglob('*'):
  if f.is_file():z.write(f,f.relative_to(L).as_posix())
 z.write(probe,probe.name)
print(json.dumps({'case':data['id'],'rc':p.returncode,'setup_error_accepted_as_mutants_OK':True,'canaries':canary['stdout']},ensure_ascii=False))
