from lab import *
from t326_driver import env
import subprocess,pathlib,time
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-a05r8'
assert not int(sql("SELECT count(*) FROM adempiere.ad_scheduler WHERE isactive='Y'"))
working=W/'t354-data';working.mkdir(exist_ok=True)
env.update(T354_ID=AP,T354_PG=PG,T354_LUCRU=str(working))
d=W/'tools/teste/t354'
subprocess.run(['docker','exec',AP,'mkdir','-p','/tmp/t354mock/orders'],check=True)
subprocess.run(['docker','cp',str(W/'tools/teste/t203/MockSiteGet.java'),AP+':/tmp/t354mock/MockSiteGet.java'],check=True)
subprocess.run(['docker','exec','-d',AP,'sh','-c','cd /tmp/t354mock && exec java MockSiteGet.java 18354 /tmp/t354mock >/tmp/t354mock/mock.out 2>&1'],check=True)
time.sleep(2)
traces=[]
def go(label,cases):
 env.update(T354_DOAR=cases)
 try:
  run=subprocess.run(['python3','-I',str(d/'proba_a.py')],env=env,cwd=working,capture_output=True,text=True,timeout=220)
  raw=run.stdout+'\n'+run.stderr
  rec={'label':label,'start_cases':cases,'utc':now(),'rc':run.returncode,'lines':[x[:1600] for x in raw.splitlines() if x.startswith(('CRIT ','PROBA A','RAND P-','SystemExit:','AssertionError:','ValueError:','RuntimeError:','HTTP','POST ','PUT ','autentificare','alegerea ')) and 'password' not in x.lower() and 'Bearer ' not in x],'raw_sha256':digest(raw.encode()),'last_safe':raw.strip().splitlines()[-1][:400] if raw.strip() else ''}
 except subprocess.TimeoutExpired:rec={'label':label,'rc':'TIMEOUT_220'}
 traces.append(rec);save('native_t354.json',traces);print(label,rec['rc'],flush=True)
go('all scenarios original incl C2 and C10','')
if not any(x.startswith('CRIT C-2 ') for x in traces[0].get('lines',[])):
 for label,cases in [('C9','c9'),('C11','c11'),('C14','c14'),('C22','c3_c4_c22,c22')]:go(label,cases)
