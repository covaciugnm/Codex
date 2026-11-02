from lab import *
from t326_driver import env
dst=W/'t354-b';dst.mkdir(exist_ok=True)
env.update(T354_ID=AP,T354_PG=PG,T354_LUCRU=str(dst),T354_PLUG=str(W/'idempiere/plugins/com.eva.ro.contab'),T354_JAR_MD5='32162eb0b4111b27a1e98fa52c2e367a')
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-a05r8'
try:
 proc=subprocess.run(['python3','-I',str(W/'tools/teste/t354/proba_b.py'),str(dst/'ui'),str(dst/'journal')],capture_output=True,text=True,env=env,cwd=dst,timeout=175)
 log=proc.stdout+'\n'+proc.stderr
 v={'rc':proc.returncode,'sha_stdout_sha256':digest(log.encode()),'lines':[l[:1500] for l in log.splitlines() if l.startswith(('PAS ','PROBA B','RuntimeError:','AssertionError:','FileNotFoundError:','playwright.'))],'reason':log.strip().splitlines()[-1][:300]}
except subprocess.TimeoutExpired:
 v={'rc':'TIME_LIMIT_175','lines':[l[:1500] for l in (dst/'journal').read_text().splitlines() if l.startswith('PAS ')] if (dst/'journal').exists() else []}
save('t354_b_results.json',v)
