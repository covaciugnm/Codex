from a12_r3_survey import *
import subprocess as sp, urllib.request as ur, hashlib, datetime
R4=E/'R4';o=R4/'probe';script="""import subprocess as sp,pathlib,json,hashlib,re
sha='6df998aee0e514d30856c461962afe99ebd0d113';root='/home/saga-server/Documents/EvA-Contab'
def run(a):return sp.run(a,cwd=root,capture_output=True)
def git(*a):return run(['git',*a])
res={}
n='f0af10f15c94';pr=git('show','--format=%H %P %s','--name-status',n);res['T27.34_commit']={'exit':pr.returncode,'lines':pr.stdout.decode(errors='replace').splitlines()[:80]}
for k,rexp in [('T33.06','T33-P2'),('T33.07','T33-P3'),('T36.66','T36-L6|T36:L6|anexa_audit_etichete'),('T43.01','T43b'),('T43.02','T43c')]:
 out=git('grep','-n','-I','-E',rexp,sha,'--','Documentatie/echipa-2026-10-09/T33*','Documentatie/echipa-2026-10-09/T36*','Documentatie/echipa-2026-10-09/T43*');ll=out.stdout.decode(errors='replace').splitlines();valid=[l for l in ll if not re.search('bearer|password|parola|token[:=]',l,re.I)]
 res[k]={'exit':out.returncode,'all_hit_count':len(ll),'examples':[l[:550]for l in valid[:15]]}
for k,p in [('T33.history','/home/saga-server/.claude/projects/-home-saga-server/9ed2b82a-2adc-47c8-93bf-ff63f91ee1be/subagents/agent-af33ee828fc1401d6.jsonl')]:
 f=pathlib.Path(p)
 if not f.is_file():res[k]={'source_present':False};continue
 with f.open(encoding='utf8')as st:
  one=next((l for i,l in enumerate(st,1)if i==200),'')
 safe={}; s=json.loads(one) if one else {}; serialized=json.dumps(s,ensure_ascii=False)
 for al in ['T33-P2','T33-P3']:
  mm=re.search(re.escape(al),serialized,re.I);safe[al]={'present':mm is not None,'bounded_text':(serialized[max(0,mm.start()-45):mm.end()+100]if mm else None)}
 res[k]={'source_present':True,'line':200,'whole_line_sha256':hashlib.sha256(one.encode()).hexdigest(),'aliases':safe}
front='eva-contab-frontend';loc='/repo/frontend/data/saga_import_map.json';j=run(['docker','exec',front,'sha256sum',loc]);res['frontend_map']={'exit':j.returncode,'hash':j.stdout.decode(errors='replace').split()[:1],'error':j.stderr.decode(errors='replace')[:160]}; 
for p in ['frontend/data/saga_import_map.json','frontend/portal/eva_saga_import_map.html','tools/saga-import-map/gen_saga_map.py','tools/teste/cabinet_test_jar_montat.sh']:
 b=git('show',sha+':'+p);res[p]={'exit':b.returncode,'sha256':hashlib.sha256(b.stdout).hexdigest() if not b.returncode else None,'size':len(b.stdout)}
print(json.dumps(res,ensure_ascii=False))
""";x=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','python3 -'],input=script.encode(),capture_output=True,timeout=85,check=True);r=json.loads(x.stdout);wr(o/'aliasuri_si_frontend.json',r)
print({k:(v.get('exit'),v.get('all_hit_count'),v.get('source_present'),v.get('hash'))for k,v in r.items()});print(r['T27.34_commit']['lines'][:3])

