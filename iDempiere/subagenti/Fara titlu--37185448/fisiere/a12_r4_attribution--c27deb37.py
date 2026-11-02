from a12_r3_survey import * 
import subprocess as sp
r4=E/'R4';program="""import json,re,subprocess as sp,hashlib
g='6df998aee0e514d30856c461962afe99ebd0d113';r='/home/saga-server/Documents/EvA-Contab'
def run(*args):return sp.run(['git',*args],cwd=r,capture_output=True)
o={}
for k,ids in [('T33.06',['b125e03e1','e60a4aa4c']),('T33.07',['7cda5fa00','072bcc686','883e3ba28']),('T36.53',['bfc6cd5278','d3042a2b69']),('T27.34',['f0af10f15c94'])]:
 arr=[]
 for c in ids:
  x=run('show','--format=%H|%P|%s','--name-status',c);lines=x.stdout.decode(errors='replace').splitlines()
  arr.append({'reference':c,'exit':x.returncode,'commit_and_subject':lines[0] if lines else None,'number_changed':len([l for l in lines[1:] if l.strip()]),'changed_paths':[l for l in lines[1:]if l.strip()][:25],'ancestor_full_github':run('merge-base','--is-ancestor',c,g).returncode==0,'distinct_server_history':True})
 o[k]=arr
for k,rx in [('T33.06','P2 scripturi|P2 documentele'),('T33.07','P3 \\||P3 Q-5|P3 LOG_ISTORIC')]:
 p='Documentatie/echipa-2026-10-09/T33-igienizare-date-personale/03_backend_raport_P2_P3.md';b=run('show',g+':'+p).stdout;lines=b.decode(errors='replace').splitlines();o[k+'_authority']={'path':p,'blob':run('rev-parse',g+':'+p).stdout.decode().strip(),'lines_only_without_private_data':[[i,l.split('|')[1].strip(),l.split('|')[2].strip()]for i,l in enumerate(lines,1) if re.search(rx,l) and l.startswith('|')],'full_sha256':hashlib.sha256(b).hexdigest()}
for k in ['T36.54','T36.55']:
 p='Documentatie/echipa-2026-10-09/T36-defecte-00l-din-T32/40_manager_plan_transa_1.md';b=run('show',g+':'+p).stdout;lines=b.decode(errors='replace').splitlines();alias='B1' if k=='T36.54' else 'B3';o[k]={'path':p,'blob':run('rev-parse',g+':'+p).stdout.decode().strip(),'matching_exact_lot_rows':[[i,l[:600]] for i,l in enumerate(lines,1)if re.match(r'^\\| '+alias+r'(?: \\(| \\|)',l)],'full_sha256':hashlib.sha256(b).hexdigest()}
print(json.dumps(o,ensure_ascii=False))
""";q=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','python3 -'],input=program.encode(),capture_output=True,check=True,timeout=30);o=json.loads(q.stdout);wr(r4/'probe/commit_efect_si_alias.json',o);print({k:len(v)for k,v in o.items()})

