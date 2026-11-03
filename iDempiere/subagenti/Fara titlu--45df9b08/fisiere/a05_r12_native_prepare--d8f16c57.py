from pathlib import Path
import subprocess,json,hashlib,datetime,shlex,zipfile,tarfile,io
ROOT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
OUT=ROOT/'executie/R12_fisiere/A05_Nativ_lot02'
OUT.mkdir(parents=True,exist_ok=True)
CACHE=Path('D:/CodexWork/a05-r12-native-cache')
CACHE.mkdir(exist_ok=True)
SSH=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151']
def remote(args):
 r=subprocess.run(SSH+[shlex.join(args)],capture_output=True,timeout=60)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r.stdout
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
observed=remote(['docker','ps','--format','{{.Names}} {{.Image}}']).decode()
relevant=[l for l in observed.splitlines() if any(x in l for x in ['eva-test-p01-t343-','eva-test-p01-t316-','eva-test-p01-t213-','eva-idempiere-cesiro '])]
data=remote(['docker','exec','eva-idempiere-cesiro','find','/opt/idempiere/plugins','-maxdepth','1','-type','f','-name','*.jar','-printf','%f\t%s\n']).decode()
rows=[{'name':n,'bytes':int(s)} for n,s in [l.split('\t')for l in data.splitlines()]]
rows.sort(key=lambda r:r['name'])
image=remote(['docker','inspect','-f','{{.Image}}','eva-idempiere-cesiro']).decode().strip()
j={'utc':utc,'method':'Citire metadata/binare; nicio operație asupra laboratoarelor altor executori.','remote_container':'eva-idempiere-cesiro','image':image,'other_active_labs_untouched':relevant,'files':rows,'bytes':sum(r['bytes']for r in rows),'root_mode':'READ_ONLY'}
(OUT/'Inventar_runtime_readonly.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
print({'count':len(rows),'bytes':j['bytes'],'postgres':[r for r in rows if 'postgres' in r['name']],'image':image})
