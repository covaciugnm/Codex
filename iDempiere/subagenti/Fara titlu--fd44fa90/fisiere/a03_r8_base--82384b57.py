from pathlib import Path as P
import os,subprocess as sp,hashlib,json,datetime,shlex,re,sys,concurrent.futures as ft
repo='/home/saga-server/Documents/EvA-Contab';sha='6df998aee0e514d30856c461962afe99ebd0d113'; D='Documentatie/echipa-2026-10-09';pref={}; 
def ssh(cmd,stdin=None,timeout=100):return sp.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',cmd],input=stdin,capture_output=True,timeout=timeout)
out=P('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R8_pregatire/A03');out.mkdir(exist_ok=True,parents=True); work=P('D:/CodexWork/a03-r8');work.mkdir(exist_ok=True)
def H(b):return hashlib.sha256(b).hexdigest()
def J(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
def UTC():return datetime.datetime.now(datetime.UTC).isoformat()
def get(path,rev=sha):
 r=ssh('cd '+repo+' && git show '+shlex.quote(rev+':'+path));assert r.returncode==0,(path,r.stderr[:150]);return r.stdout
def allfiles():
 p=work/'paths.txt'
 if not p.exists():
  r=ssh('cd '+repo+' && git ls-tree -r --name-only '+sha+' -- '+D+' tools/teste');assert r.returncode==0;p.write_bytes(r.stdout)
 return p.read_text(encoding='utf8').splitlines()
paths=allfiles()
for t in 'T58 T156 T159 T186 T256 T254 T03 T194 T11 T196'.split():
 l=[p for p in paths if '/'+t+'-' in p and not p.startswith('tools/')];pref[t]=l[0].split('/')[2]
def path(t,name):return D+'/'+pref[t]+'/'+name
def doc(path0):
 b=get(path0); return b.decode('utf8',errors='replace')
if __name__=='__main__':
 for t,p,pattern in [('T159','12_spec.md','generator_hardcodari|C-27|G =|reclasificate|3.6'),('T186','dovezi-20-plan/inventar_t186.py','utilizare|usage|sys.argv|arguments|consecint|20v_|mapare'),('T186','dovezi-20-plan/verifica_inventar_t186.py','utilizare|usage|sys.argv|arguments|20[a-z]_'),('T256','dovezi-02-plan/mutanti_sql_fixturi.sql','CREATE|DROP|INSERT|UPDATE|FROM |\\\\'),('T156','dovezi-02-plan/scripturi/t0_criterii.sh','git|ROOT|cd |mkdir|rm |mktemp'),('T159','dovezi-10/generator_hardcodari.py','utilizare|usage|ramase|cititori|chei-lipsa|git |cwd|subprocess'),('T186','36_test_clasa_r2.py','usage|sys.argv|LR-3|worktree')]:
  try: print(t,p,'\n','\n'.join(x[:280] for x in doc(path(t,p)).splitlines() if re.search(pattern,x,re.I))[:4200])
  except Exception as e:print(e)

