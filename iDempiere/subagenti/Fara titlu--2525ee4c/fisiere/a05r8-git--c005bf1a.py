from pathlib import Path
import subprocess as sp, json, hashlib, re, datetime, sys, os, tarfile, io
base=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
out=base/'executie/R8_pregatire/A05'; w=Path('D:/CodexWork/a05r8')
out.mkdir(parents=True,exist_ok=True)
cut='6df998aee0e514d30856c461962afe99ebd0d113'
q=json.loads((base/'Coada_reverificari_P01.json').read_text(encoding='utf8'))
my=[i for i in q['rows'] if i['owner']=='A05' and i['category']=='FIXTURĂ_EXECUTABILĂ']
tasks=sorted(set(i['task'] for i in my))
taskfiles={t:json.loads((base/f'executie/R7/taskuri/Fisa_{t}.json').read_text(encoding='utf8')) for t in tasks}
dates={t:f['known_closure_dates'][0]['value'] if f['known_closure_dates'] else None for t,f in taskfiles.items()}
def remote(src):
 c=sp.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151','nice -n 10 python3 -'],input=src.encode('utf8'),capture_output=True,timeout=240)
 if c.returncode:raise RuntimeError(c.stderr.decode(errors='replace')[-650:])
 return c.stdout
def dump(f,x):f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
header="""import os,sys,re,subprocess as sp,hashlib,json,datetime,tarfile,io
os.chdir('/home/saga-server/Documents/EvA-Contab')
cut='6df998aee0e514d30856c461962afe99ebd0d113'
def git(*argv):return sp.check_output(['git','--no-optional-locks',*argv],stderr=sp.DEVNULL)
def g(*a):return git(*a).decode('utf8','replace').strip()
def blob(oid):return git('cat-file','blob',oid)
"""
if sys.argv[1]=='history':
 program=header+'dates='+repr(dates)+"""
tree=g('ls-tree','-r',cut,'--','Documentatie/echipa-2026-10-09','tools/teste').splitlines()
results={}; excerpts={}
for task,date in dates.items():
 matches=[s for s in tree if '/'+task+'-' in s or '/'+task.lower()+'/' in s or 'test/'+task.lower()+'/' in s]
 hist=g('log','--first-parent','-1','--format=%H|%cI','--before='+date,cut) if date else None
 hs=hist.split('|')[0] if hist else None
 def native(s):
  head,path=s.split('\t',1);return {'file':path,'oid':head.split()[2]}
 records=[native(s) for s in matches]
 results[task]={'date':date,'dated_master_snapshot':hs,'dated_commit_time':hist.split('|')[1] if hist else None,'inventory':records}
 # Select machine/evidence text files, excluding private credentials, raw HTTP/DB dumps. Private corpus used only for finding historical logs, never executed.
 for rec in records:
  path=rec['file'];name=path.rsplit('/',1)[-1]
  if not re.search(r'\.txt$|\.md$|\.log$',name,re.I):continue
  if not re.search(r'criter|rezult|audit|sintez|sumar|proba|^0[0-9]|mutant|Test(ListaPicking|Loturi|Fefo|T163|T33|T354)',name,re.I):continue
  if re.search(r'(secret|credential|token|parol|auth_|curl|env\.|login)',name,re.I):continue
  size=int(g('cat-file','-s',rec['oid']))
  if size>650000:continue
  text=blob(rec['oid']).decode('utf8','replace')
  # Only numeral criteria marker/status cites, not actual data, URLs, or secrets. Keep raw lengths, no full body.
  lines=[]
  for no,line in enumerate(text.splitlines(),1):
   matches=re.findall(r'(?<![A-Za-z0-9])(?:C-(?:[0-9]{1,2})(?![0-9.])|K-[0-9]{2}(?![0-9.])|RZ-[0-9]{1,2}\.[0-9]{1,2})',line)
   if not matches:continue
   # do not publish arbitrary raw historical content; include only normalized marks and location.
   states=list(dict.fromkeys(re.findall(r'(?<![\w])(?:OK|FAIL|VERDE|ROȘU|PASS|REFUZ|REPRODUS|NEEXECUTAT)(?![\w])',line,re.I)))
   lines.append([no,matches[:12],states[:5],hashlib.sha256(line.encode()).hexdigest()])
  if lines: excerpts[path]={'oid':rec['oid'],'bytes':size,'signals':lines}
print(json.dumps({'cutoff':cut,'tasks':results,'signals':excerpts},ensure_ascii=False))
"""
 o=json.loads(remote(program));dump(w/'history-corpus.json',o)
 hist={t:{k:v for k,v in j.items() if k!='inventory'} for t,j in o['tasks'].items()}
 dump(out/'Reper_istoric.json',{'scope':'Commit first-parent cel târziu la ora înscrisă în registru; commitul nu demonstrează ora testului și nu este ales după valabilitatea rezultatului. Inventar Git la cutoff (fișiere din dosar și tools/teste corespunzătoare).','tasks':{t:{**h,'files_at_cutoff':len(o['tasks'][t]['inventory'])} for t,h in hist.items()}})
elif sys.argv[1]=='statics':
 paths=['Documentatie/echipa-2026-10-09/T163-plus-minus-inventar/dovezi-02-plan/criterii_statice.sh','tools/teste/t333/criterii_schelet.sh']
 allowed={p:hashlib.sha256((w/Path(p).name).read_bytes()).hexdigest() for p in paths}
 prog=header+'allowed='+repr(allowed)+"""
res=[]
t163='9980254afc56f7a852e8b7c90dc6b3ba1d81f491'
t333=g('rev-parse','d6068a9fa9^{commit}')
for path,checked in allowed.items():
 safe=blob(g('rev-parse',cut+':'+path));assert hashlib.sha256(safe).hexdigest()==checked
 is163='T163-' in path
 hist=t163 if is163 else t333
 base=g('rev-parse',hist+'^')
 for tag,rev in [('historical',hist),('current',cut)]:
  oid=g('rev-parse',rev+':'+path)
  script=blob(oid);equal=hashlib.sha256(script).hexdigest()==checked
  # only byte-reviewed scripts run. Both scripts perform pure git reads. T333 derives cwd from $0; pass actual Git path to bash -c intentionally.
  cmd=['bash','-s','--',rev,base] if is163 else ['bash','-c',safe.decode(),'/home/saga-server/Documents/EvA-Contab/'+path,rev,base]
  run=sp.run(cmd,input=(script if is163 else None),capture_output=True,timeout=100) if equal else None
  res.append({'task':'T163' if is163 else 'T333','tag':tag,'rev':rev,'base':base,'path':path,'script_oid':oid,'sha256':checked,'executed':equal,'rc':run.returncode if run else None,'stdout':run.stdout.decode('utf8','replace') if run else None,'stderr':run.stderr.decode('utf8','replace') if run else None,'semantics':'For current aggregate base..cut includes unrelated later work; C-3 and C-10 do not attribute another task’s diff to this task. Historic base = parent of the named integration/skeleton witness.'})
print(json.dumps(res))
"""
 o=json.loads(remote(prog))
 for x in o:
  log=out/(x['task']+'_'+x['tag']+'_static.txt');log.write_text((x.pop('stdout') or '')+(x.pop('stderr') or ''),encoding='utf8');x['file']=log.name;x['sha256_output']=hashlib.sha256(log.read_bytes()).hexdigest()
 dump(out/'Executie_scripturi_originale.json',o)
elif sys.argv[1]=='guarddata':
 # Checked in Git; includes exact corpus that the original partner guard scans. Archive locally, never run any script from the corpus except the separately audited guard itself.
 prog=header+r"""
f=tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz'); root='Documentatie/echipa-2026-10-09'
paths=['idempiere/plugins/com.eva.ro.contab/test','idempiere/plugins/com.eva.ro.contab/src','tools/teste','scripts',root]
proc=sp.Popen(['git','cat-file','--batch'],stdin=sp.PIPE,stdout=sp.PIPE)
for line in git('ls-tree','-rz',cut,'--',*paths).split(b'\0'):
 if not line:continue
 tag,path=line.split(b'\t',1); p=path.decode('utf8');oid=tag.split()[-1]
 if p.startswith(root+'/') and 'dovezi' not in p:continue
 if not p.lower().endswith(('.java','.py','.sh','.js','.ts','.kt','.groovy','.sql','.permise')):continue
 proc.stdin.write(oid+b'\n');proc.stdin.flush();head=proc.stdout.readline().split();size=int(head[-1]);b=proc.stdout.read(size);proc.stdout.read(1)
 if b'..' in path.split(b'/') or p.startswith('/'):raise ValueError('unsafe git path')
 ti=tarfile.TarInfo(p);ti.size=size;f.addfile(ti,io.BytesIO(b))
proc.stdin.close();proc.wait();f.close()
"""
 a=remote(prog);tarpath=w/'guard_input.tgz';tarpath.write_bytes(a)
 print('guard tar',len(a))
 with tarfile.open(tarpath) as t:t.extractall(w/'guard-tree',filter='data')
 guard=w/'guard-tree/tools/teste/garda_parteneri_scriere.py';assert guard.read_bytes()==(w/'garda_parteneri_scriere.py').read_bytes()
 cp=sp.run([sys.executable,'-I',guard],capture_output=True,cwd=w/'guard-tree',timeout=150)
 public=cp.stdout.decode('utf8','replace').splitlines();summary=next(x for x in public if x.startswith('garda_parteneri_scriere:'))
 dump(out/'Garda_parteneri.json',{'rev':cut,'script_sha256':hashlib.sha256(guard.read_bytes()).hexdigest(),'corpus_sha256':hashlib.sha256(a).hexdigest(),'paths':sum(1 for x in (w/'guard-tree').rglob('*') if x.is_file()),'mode':'Original script, isolated Python; no --invata. Windows separator in os.path.relpath may diverge from slash whitelist; if nonzero see POSIX replay. This is static scanning, not capture of runtime HTTP.','rc':cp.returncode,'summary':summary,'remaining_lines':len(public)-1})
