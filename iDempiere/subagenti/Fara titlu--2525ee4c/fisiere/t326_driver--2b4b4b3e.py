from lab import *
import shutil
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-a05r8'
net=cmd(['docker','inspect','--format','{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}',AP]);assert cmd(['docker','network','inspect','-f','{{.Internal}}',net])=='true'
assert rows("select ad_client_id,name from adempiere.ad_client order by 1")==[['0','System'],['11','GardenWorld']]
assert sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
working=W/'t326-data';working.mkdir(exist_ok=True)
env={**os.environ,'T326_PG':PG,'T326_ID':AP,'T203_PG':PG,'T203_ID':AP,'T162_URL':ROOT,'T162_U':'GardenAdmin','T162_P':'GardenAdmin','T326_LUCRU':str(working),'T326_ZK':'0','T326_JAR':'r57-installed-current','T203_DOV':str(working),'NO_PROXY':'*','no_proxy':'*'}
if __name__=='__main__':
 stages=[('p0','pregatire'),('p0','s1s2s4'),('lot','u5'),('lot','f1'),('lot','doua'),('lot','fara_stoc'),('lot','suma_val'),('lot','pick'),('lot','s6'),('lot','u7')]
 traces=[]
 for prog,step in stages:
  script=W/'tools/teste/t326'/('pas0.py' if prog=='p0' else 'proba_lot_a.py')
  rec={'case':step,'utc':now(),'source_sha256':digest(script.read_bytes()),'input':'synthetic staged site record/body, internal loopback GET only; no claim resumed checkout or historical JAR.'}
  try:
   xp=subprocess.run(['python3','-I',str(script),step],capture_output=True,text=True,env=env,cwd=working,timeout=140)
   raw=xp.stdout+'\n'+xp.stderr
   # Include preselected assertion lines for audit only; transport token never logged.
   lines=[x[:1150] for x in raw.splitlines() if x.startswith(('RAND ','# mock:','# P01.','SystemExit:','AssertionError:','ValueError:','KeyError:','FileNotFoundError:','RuntimeError:','alegerea rolului','autentificare','POST ','GET ')) and 'token' not in x.lower() and 'password' not in x.lower()]
   rec.update(rc=xp.returncode,lines=lines,raw_sha256=digest(raw.encode()),tail_safe=(raw.strip().splitlines()[-1][:280].replace('GardenAdmin','actor') if xp.returncode not in (0,1) and raw.strip() else ''))
  except subprocess.TimeoutExpired:rec.update(rc='TIMEOUT')
  traces.append(rec);save('native_t326.json',traces);print(step,rec.get('rc'),len(rec.get('lines',[])),flush=True)
  if step in ('pregatire','s1s2s4') and (rec.get('rc')!=0 or not rec.get('lines')):break
