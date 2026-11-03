from pathlib import Path
import sys,os,json,hashlib,difflib,subprocess,zipfile,io,shutil,datetime
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
L=Path('D:/CodexWork/a10-r12-l03/shell')
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A10_Instrumente_ramase_lot03')
G='C:/Program Files/Git/cmd/git.exe';B='C:/Program Files/Git/bin/bash.exe'
PY='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
F='Documentatie/echipa-2026-10-09/T240-ajutor-ecrane-rest'
PL='idempiere/plugins/com.eva.ro.contab'
J='idempiere/plugins/com.eva.ro.saga.native/com.eva.ro.saga.native_13.0.0.jar'
def px(p):s=str(p).replace('\\','/');return '/'+s[0].lower()+s[2:] if len(s)>1 and s[1]==':' else s
def put(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s if isinstance(s,str) else json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {str(q.relative_to(p)).replace('\\','/'):{'sha256':sha(q),'bytes':q.stat().st_size} for q in sorted(p.rglob('*')) if q.is_file()}
def git(w,*args):
 r=subprocess.run([G,'-c','core.autocrlf=false','-c','core.hooksPath=NUL','-C',str(w),*args],capture_output=True,encoding='utf-8',errors='replace',timeout=30)
 if r.returncode:raise RuntimeError((args,r.returncode,r.stdout,r.stderr))
 return r.stdout.strip()
def commit(w,label):git(w,'add','.');git(w,'-c','user.name=Audit synthetic','-c','user.email=audit@example.invalid','commit','-qm',label);return git(w,'rev-parse','HEAD')
def init(w):w.mkdir(parents=True);git(w,'init','-q','-b','master');git(w,'config','core.autocrlf','false')
def jar(entries):
 x=io.BytesIO()
 with zipfile.ZipFile(x,'w',compression=zipfile.ZIP_STORED) as z:
  for k,v in entries:
   zi=zipfile.ZipInfo(k,date_time=(2020,1,1,0,0,0));z.writestr(zi,v)
 return x.getvalue()

DISPATCH=r'''from pathlib import Path
import sys,os,json,runpy,socket,subprocess
sys.dont_write_bytecode=True
root=Path(os.environ['AUDIT_CASE']).resolve()
def ck(p):
 if isinstance(p,int):return
 q=Path(os.fsdecode(p)).resolve()
 if not q.is_relative_to(root):raise PermissionError('OUTSIDE_FIXTURE:'+str(q))
def hook(e,a):
 if e.startswith('socket.') or e in ('subprocess.Popen','os.system'):raise PermissionError('NO_EXTERNAL')
 if e=='open' and ((isinstance(a[1],str) and any(c in a[1] for c in 'wax+')) or (isinstance(a[2],int) and a[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))):ck(a[0])
 if e in ('os.mkdir','os.rmdir','os.remove','os.chmod','os.utime'):ck(a[0])
 if e in ('os.rename','os.link','os.symlink'):ck(a[0]);ck(a[1])
sys.addaudithook(hook)
a=sys.argv[1:]
if a and a[0]=='-I':a=a[1:]
if a[0]=='-c':sys.argv=['-c']+a[2:];exec(compile(a[1],'<component -c>','exec'))
elif a[0]=='-':sys.argv=['-']+a[1:];exec(compile(sys.stdin.read(),'<original embedded Python>','exec'))
else:sys.argv=a;runpy.run_path(a[0],run_name='__main__')
'''

DEPENDENCY=r'''from pathlib import Path
import sys,os,json,hashlib
root=Path(os.environ['AUDIT_CASE']);cfg=json.loads((root/'config.json').read_text());name=Path(sys.argv[0]).name
def event(k):
 with open(root/'events.jsonl','a') as f:f.write(json.dumps({'child':name,'event':k,'args':sys.argv[1:]})+'\n')
event('called');w=root/'repo';work=root/'work';out=w/'Documentatie/echipa-2026-10-09/T240-ajutor-ecrane-rest/dovezi-80'
def code(key,default=0):return cfg.get(key,default)
if name=='garda_parteneri_scriere.py':
 def fisiere(args):
  for x in args:
   p=Path(x)
   if p.is_file():yield p
   elif p.is_dir():yield from (q for q in p.rglob('*') if q.is_file())
 if __name__=='__main__':
  files=list(fisiere([x for x in sys.argv[1:] if x!='--cai']));can=any('requests.post' in p.read_text(errors='replace') for p in files if p.suffix=='.py')
  print('0 apariții scanate — SYNTHETIC success-looking child stdout')
  if can:print('  NOU synthetic canary');sys.exit(1)
  sys.exit(code('partner_rc'))
elif name=='proba_buton.py':
 out.mkdir(exist_ok=True,parents=True);(out/'proba').mkdir(exist_ok=True)
 (out/'raport.tsv').write_text('ecran\tlimba\tstatus\nWOne\tro_RO\tDA\nWTwo\tro_RO\tDA\n',encoding='utf-8')
 for f in ['jurnal_proba.txt','perioade_bara.txt','revenire_ro.tsv']:(out/f).write_text('SYNTHETIC',encoding='utf-8')
 (out/'proba'/'observed.txt').write_text('SYNTHETIC DOM NOT EXECUTED')
 print('proba: success-looking output; fixture N=2, no UI');sys.exit(code('collector_rc'))
elif name=='verifica_proba.py':
 target=Path(sys.argv[1]);n=sum(1 for x in (target/'raport.tsv').read_text().splitlines()[1:] if '\tro_RO\t' in x)
 print(str(n)+'/2 conforme (synthetic oracle)')
 sys.exit(code('contra_rc',1) if target.name=='contra' else code('judge_rc'))
elif name in ['test_clasa_masca.py','test_clasa_fragmente_fraze.py','fragment_public.py']:
 print('0 în clar — SYNTHETIC stdout');sys.exit(code('privacy_rc'))
elif name=='foi_contact.py':
 dst=Path(sys.argv[2]);dst.mkdir(exist_ok=True,parents=True);(dst/'synthetic.txt').write_text('No image, no UI credit')
 print('SYNTHETIC last step');sys.exit(code('last_rc'))
'''

def common(c,cfg):
 w=c/'repo';bin=c/'bin';bin.mkdir();put(c/'config.json',cfg);put(c/'dispatch.py',DISPATCH)
 put(bin/'python3',f'#!/usr/bin/env bash\nexec "{px(PY)}" -I "{px(c/"dispatch.py")}" "$@"\n')
 # Deletion explicitly does not execute. Failures can be injected for the final cleanup.
 put(bin/'rm','#!/usr/bin/env bash\nprintf "rm-noop %s\\n" "$*" >> "$AUDIT_CASE/events.shell"\nif [[ "$AUDIT_RM_FAIL" = 1 && -d "$AUDIT_CASE/scratch" ]]; then exit 73; fi\nexit 0\n')
 for name in ['curl','wget','ssh','scp','psql','docker-compose','powershell','cmd']:
  put(bin/name,'#!/usr/bin/env bash\necho "BLOCKED external command" >&2\nexit 97\n')
 put(bin/'git',f'''#!/usr/bin/env bash
W="$PWD"; [[ "$1" == -C ]] && W="$2"
case "$W" in "$AUDIT_CASE"/*) ;; *) echo "GIT OUTSIDE FIXTURE" >&2; exit 96;; esac
exec '/c/Program Files/Git/cmd/git.exe' -c core.hooksPath=NUL -c core.autocrlf=false "$@"
''')
 put(bin/'docker','''#!/usr/bin/env bash
echo "docker-shim $*" >> "$AUDIT_CASE/events.shell"
case "$1" in
 network) echo "internal=${AUDIT_NETWORK:-true}"; exit "${AUDIT_DOCKER_RC:-0}";;
 exec) if [[ "$AUDIT_HASH_MISMATCH" == 1 ]]; then echo '00000000000000000000000000000000 synthetic.jar'; else md5sum "$AUDIT_CASE/work/jars/com.eva.ro.contab_13.0.0.jar"; fi;;
 logs) echo 'synthetic java.lang.FixtureException';;
 *) echo 'BLOCKED docker operation' >&2; exit 97;;
esac
''')
 put(w/'tools/teste/garda_parteneri_scriere.py',DEPENDENCY)
 put(w/'tools/teste/garda_date_personale.sh','#!/usr/bin/env bash\necho "SYNTHETIC guard success-looking stdout"\nexit "${AUDIT_SECRET_RC:-0}"\n')
 put(w/'tools/teste/verifica_rulator.sh','#!/usr/bin/env bash\necho "SYNTHETIC runner guard"\nexit "${AUDIT_RUNNER_RC:-0}"\n')
 put(w/'tools/teste/ruleaza_teste_saganative.sh','# fixture TestT232GardaConsola\n')
 # No actual remote/native child is copied into this fixture.
 put(c/'run.sh',f'''#!/usr/bin/env bash
export AUDIT_CASE='{px(c)}'
export PATH='{px(bin)}:/usr/bin:/bin'
export EVA_W='{px(w)}' EVA_T240_LUCRU='{px(c/'work')}' EVA_CERE_CONT='SYNTHETIC' EVA_T240_PID_SESIUNE='1'
export AUDIT_RM_FAIL='{cfg.get('rm_fail',0)}' AUDIT_SECRET_RC='{cfg.get('secret_rc',0)}' AUDIT_RUNNER_RC='{cfg.get('runner_rc',0)}'
export AUDIT_NETWORK='{cfg.get('network','true')}' AUDIT_HASH_MISMATCH='{cfg.get('hash_mismatch',0)}' AUDIT_DOCKER_RC='{cfg.get('docker_rc',0)}'
export AUDIT_PG_RC='{cfg.get('pg_rc',0)}' AUDIT_MASK_RC='{cfg.get('mask_rc',0)}' AUDIT_STOP_RC='{cfg.get('stop_rc',0)}' AUDIT_ACQUIRE_RC='{cfg.get('acquire_rc',0)}' AUDIT_RELEASE_RC='{cfg.get('release_rc',0)}' AUDIT_ACQUIRE_STDOUT='{cfg.get('acquire_stdout','SYNTHETIC_SLOT')}'
cd '{px(w)}' || exit 98
bash '{px(c/'comparator.sh')}' {cfg.get('args','')}
''')
 return w

def seal(c,id,cfg,original,modified,refs=None):
 put(c/'comparator.sh',modified)
 put(c/'source.diff',''.join(difflib.unified_diff(original.splitlines(True),modified.splitlines(True),fromfile='original Git OID source',tofile='synthetic comparator only')))
 if id=='I04':allowed=['QB path only']
 elif id=='I10':allowed=['R path only','SP path only']
 else:allowed=['five historical refs -> own synthetic commits (including echoed labels/file names)']
 put(c/'Case_preflight.json',{'id':id,'case':c.name,'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','approved_protocol_sha256':'13727927b40b797257ee4f483233638649df6bc9c205317759af093425379284','method':'COMPARATOR_ONLY','original_sha256':hashlib.sha256(original.encode()).hexdigest(),'comparator_sha256':sha(c/'comparator.sh'),'allowed_changes':allowed,'diff_sha256':sha(c/'source.diff'),'fixtures_and_shims':inv(c),'historical_ref_mapping':refs,'oracle_config':cfg,'limits':['delete no-op; no cleanup/retry-cleanliness credit','no real Docker/DB/ZK/privacy or partner detector','cooperative guards, not OS sandbox','Git merge-tree may write objects in own isolated repository']})
 put(c/'Inventory_before.json',inv(c))

def prep04(name,cfg):
 c=L/('I04_'+name);c.mkdir();w=c/'repo';init(w);cfg=dict(cfg,args='HEAD');common(c,cfg)
 put(w/(PL+'/test/fixtures/help/ecrane.tsv'),'WOne\tOne\nWTwo\tTwo\n');put(w/(PL+'/src/com/eva/ro/contab/ajutor/ManualEvA.java'),'// SYNTHETIC no actual UI\n')
 p=w/(PL+'/com.eva.ro.contab_13.0.0.jar');p.write_bytes(jar([('A.class',b'A')]))
 for f in ['proba_buton.py','verifica_proba.py','test_clasa_masca.py','test_clasa_fragmente_fraze.py']:put(w/('tools/teste/t240/'+f),DEPENDENCY)
 for f in ['fragment_public.py','foi_contact.py']:put(w/(F+'/dovezi-80/scripturi/'+f),DEPENDENCY)
 put(w/'tools/help/pregateste_cabinet_help.sh','''#!/usr/bin/env bash
echo "prepare $1" >> "$AUDIT_CASE/events.shell"
case "$1" in
 pg) mkdir -p "$EVA_T240_LUCRU/jars" "$EVA_T240_LUCRU/masca"; printf "J=%s/jars\\nNET=SYNTHETIC_NET\\nID=SYNTHETIC_ID\\n" "$EVA_T240_LUCRU" > "$EVA_T240_LUCRU/cabinet.stare"; exit "$AUDIT_PG_RC";;
 app) cp "$EVA_W/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar" "$EVA_T240_LUCRU/jars/";;
 mascheaza) echo 'synthetic phrases' > "$EVA_T240_LUCRU/masca/masca_fraze.txt"; exit "$AUDIT_MASK_RC";;
 opreste) echo 'synthetic stop requested'; exit "$AUDIT_STOP_RC";;
 *) exit 97;;
esac
''')
 put(c/'queue.sh','''#!/usr/bin/env bash
echo "queue $1" >> "$AUDIT_CASE/events.shell"
case "$1" in
 cere) [[ -z "$AUDIT_ACQUIRE_STDOUT" ]] || printf '%s\\n' "$AUDIT_ACQUIRE_STDOUT"; exit "$AUDIT_ACQUIRE_RC";;
 elibereaza) exit "$AUDIT_RELEASE_RC";;
 *) exit 97;;
esac
''')
 commit(w,'Synthetic I04 fixture')
 if cfg.get('existing_work'):put(c/'work'/'sentinel.txt','must remain intact')
 orig=(O/'sources/reteta_L6.sh').read_text();new=orig.replace('/home/saga-server/Documents/EvA-Contab/tools/status/coada_builduri.sh',px(c/'queue.sh'))
 seal(c,'I04',cfg,orig,new)

def prep10(name,cfg):
 c=L/('I10_'+name);c.mkdir();w=c/'repo';init(w);common(c,cfg)
 put(w/(F+'/dovezi-81/doc.txt'),'SYNTHETIC safe text');put(w/(F+'/81_test.md'),'SYNTHETIC header');put(w/'conflict.txt','base');commit(w,'I10 base')
 if cfg.get('conflict'):
  git(w,'branch','side');put(w/'conflict.txt','master');commit(w,'master');git(w,'checkout','-q','side');put(w/'conflict.txt','side');commit(w,'side')
 orig=(O/'sources/garzi.sh').read_text();new=orig.replace('R=/home/saga-server/Documents/EvA-Contab;',f'R={px(w)};')
 start='SP=/tmp/claude-1000/-home-saga-server-Documents-EvA-Contab/60bde47f-4e09-4e09-a1e8-ff784ce7b377/scratchpad/texte/garzi;'
 assert start in new;new=new.replace(start,f'SP={px(c/"scratch")};');seal(c,'I10',cfg,orig,new)

def prep01(name,cfg):
 c=L/('I01_'+name);c.mkdir();w=c/'repo';init(w);cfg=dict(cfg,args=f"'{px(w)}' '{px(c/'scratch')}'");common(c,cfg);(c/'scratch').mkdir()
 put(w/(PL+'/com.eva.ro.contab_13.0.0.jar'),'contab-synthetic');put(w/'Documentatie/echipa-2026-10-09/00_REGISTRU_BUILDURI_TESTE.jsonl','')
 folder='Documentatie/echipa-2026-10-09/T232-platforma-administrator';put(w/(folder+'/LOG_MODIFICARI.md'),'\n'.join('| date | actor | note | scope |' for _ in range(43)))
 for f in ['L1_integrare_suita_native_681970daa3c.txt','L1_portal_unittest_681970daa3c.txt','cabinet/L1_cabinet_rulare.txt']:put(w/(folder+'/dovezi-12/integrare/'+f),'start synthetic\nTOTAL synthetic\nrc suita 0\nREZULTAT synthetic\nstop synthetic\n')
 jp=w/J;jp.parent.mkdir(parents=True,exist_ok=True);base=[('A.class',b'BASE'),('B.class',b'B')];jp.write_bytes(jar(base));par=commit(w,'parent')
 put(w/'synthetic-note.txt','audit');a=commit(w,'audited');put(w/'synthetic-note.txt','validated');v=commit(w,'validated')
 mode=cfg.get('jar','normal');entries=base
 if mode=='changed':entries=[('A.class',b'CHANGED'),('B.class',b'B')]
 if mode=='missing_class':entries=[('A.class',b'BASE')]
 if mode=='duplicate_last_base':entries=[('A.class',b'MALFORMED_VARIANT'),('A.class',b'BASE'),('B.class',b'B')]
 if mode=='duplicate_last_variant':entries=[('A.class',b'BASE'),('A.class',b'MALFORMED_VARIANT'),('B.class',b'B')]
 if mode=='corrupt':jp.write_bytes(b'not ZIP')
 elif mode=='missing_jar':git(w,'rm','--',J)
 else:jp.write_bytes(jar(entries))
 put(w/'synthetic-note.txt','integrated');i=commit(w,'integration');git(w,'branch','t232-aud',a)
 # Independent oracle lists every member and digest; duplicates are never collapsed.
 oracle=[]
 for ref in [par,a,i]:
  r=subprocess.run([G,'-C',str(w),'show',ref+':'+J],capture_output=True)
  row={'commit':ref,'git_show_rc':r.returncode,'raw_sha256':hashlib.sha256(r.stdout).hexdigest()}
  try:
   with zipfile.ZipFile(io.BytesIO(r.stdout)) as z:row['members']=[{'name':n.filename,'crc':n.CRC,'sha256':hashlib.sha256(z.read(n)).hexdigest()} for n in z.infolist()]
  except Exception as e:row['error']=type(e).__name__
  oracle.append(row)
 put(c/'Jar_oracle.json',oracle)
 refs={'b1a127f4175':i,'01619179149':v,'934a1345228':a,'681970daa3c':par,'8acd3311a13':par}
 # Rename synthetic proof labels to mapped refs, consistent with comparator only.
 di=w/(folder+'/dovezi-12/integrare')
 for old in ['L1_integrare_suita_native_681970daa3c.txt','L1_portal_unittest_681970daa3c.txt']:
  put(di/old.replace('681970daa3c',par),(di/old).read_text())
 commit(w,'mapped proof fixture labels')
 orig=(O/'sources/verifica_integrare_L1.sh').read_text();new=orig
 for x,y in refs.items():new=new.replace(x,y)
 seal(c,'I01',cfg,orig,new,refs)

if sys.argv[1]=='prepare':
 L.mkdir(exist_ok=False)
 for name,cfg in [('normal',{}),('pg_fail',{'pg_rc':31}),('mask_fail',{'mask_rc':32}),('collector_fail',{'collector_rc':43}),('judge_fail',{'judge_rc':44}),('contra_false',{'contra_rc':0}),('privacy_fail',{'privacy_rc':47}),('network_false_hash_mismatch',{'network':'false','hash_mismatch':1}),('last_fail',{'last_rc':50}),('acquire_refused',{'acquire_rc':4,'acquire_stdout':''}),('acquire_error_stdout',{'acquire_rc':4}),('stop_release_fail',{'stop_rc':71,'release_rc':72}),('primary_and_cleanup_fail',{'collector_rc':43,'last_rc':50,'stop_rc':71,'release_rc':72}),('existing_work',{'existing_work':True})]:prep04(name,cfg)
 for name,cfg in [('normal',{}),('partner_fail',{'partner_rc':41}),('secret_fail',{'secret_rc':42}),('merge_conflict',{'conflict':True}),('cleanup_fail',{'partner_rc':41,'rm_fail':1})]:prep10(name,cfg)
 for name,cfg in [('normal',{}),('changed',{'jar':'changed'}),('missing_class',{'jar':'missing_class'}),('duplicate_last_base',{'jar':'duplicate_last_base'}),('duplicate_last_variant',{'jar':'duplicate_last_variant'}),('corrupt',{'jar':'corrupt'}),('missing_jar',{'jar':'missing_jar'}),('child_fail',{'partner_rc':41,'secret_rc':42,'runner_rc':43})]:prep01(name,cfg)
 put(L/'Preparation_manifest.json',{str(p.relative_to(L)):sha(p) for p in L.glob('*/Case_preflight.json')});print(json.dumps({'cases':27,'manifest':sha(L/'Preparation_manifest.json')}))
elif sys.argv[1]=='run':
 cases=[]
 for c in sorted(p for p in L.iterdir() if p.is_dir()):
  try:r=subprocess.run([B,'--noprofile','--norc',str(c/'run.sh')],cwd=str(c/'repo'),capture_output=True,encoding='utf-8',errors='replace',timeout=40);rc=r.returncode;stdout=r.stdout;stderr=r.stderr
  except subprocess.TimeoutExpired as e:rc='TIMEOUT';stdout=str(e.stdout);stderr=str(e.stderr)
  put(c/'stdout.txt',stdout);put(c/'stderr.txt',stderr)
  put(c/'Inventory_after.json',inv(c));cfg=json.loads((c/'config.json').read_text())
  row={'case':c.name,'rc':rc,'config':cfg,'stdout_sha256':sha(c/'stdout.txt'),'stderr_sha256':sha(c/'stderr.txt'),'case_preflight_sha256':sha(c/'Case_preflight.json'),'method':'COMPARATOR_WITH_EXPLICIT_SHIMS','resource_cleanup':'rm no-op; retained fixture artifacts; no lifecycle cleanliness credit'}
  put(c/'Outcome.json',row);cases.append(row);print(c.name,rc,flush=True)
 put(L/'Results.json',cases)
