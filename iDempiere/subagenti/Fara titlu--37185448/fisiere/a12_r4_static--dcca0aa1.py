from a12_r3_survey import *
import shlex,subprocess as sp,collections,concurrent.futures as cf,os
r4=E/'R4';pr=r4/'probe';repo=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');gd=Path('C:/Program Files/Git/usr/bin/grep.exe');assert gd.exists();ls=sp.check_output(['rg','--files',str(repo)]).decode('utf8',errors='replace').splitlines();by=collections.defaultdict(list)
for s in ls:pp=Path(s);by[pp.name.lower()].append(pp)
def resolve(token):
 tok=token.strip("'\";,()");tok=tok.replace('P/','').replace('B/','').replace('PV/','').replace('S/','');tok=tok.strip('/')
 if not tok or any(q in tok for q in '<>$*?{}')or not re.search(r'\.(java|py|tsx?|jsx?|xml|html|sh|tsv|sql|yaml|yml|properties|json|css)$',tok,re.I):return None
 cs=by.get(Path(tok).name.lower(),[]);hs=[v for v in cs if v.as_posix().lower().endswith('/'+tok.lower())];return hs[0] if len(hs)==1 else cs[0] if len(cs)==1 else None
items=[];slots=[];seen=set()
for f in (E/'R3/taskuri').glob('*.json'):
 w=rd(f);k=w['task']
 for c in w['operative_criteria_and_audit_criteria']+w['R3_new_criteria']:
  if c['current']['status']!='NEEXECUTAT':continue
  for cmd in re.findall(r'[\x60]([^\x60]{4,700})[\x60]',c['normative_content']):
   if not cmd.startswith(('grep ','rg ')):continue
   try:toks=shlex.split(cmd.replace(r'\|','|'))
   except ValueError:continue
   if '|'in toks:toks=toks[:toks.index('|')]
   if not toks or len(toks)<3:continue
   if any('<' in a or '$(' in a or a.startswith('-r')or a in ('-e','-f')for a in toks[1:]):continue
   j=1
   while j<len(toks) and toks[j].startswith('-'):
    if not re.fullmatch(r'-[niqclEFwoh]+',toks[j]):j=-1;break
    j+=1
   if j<=0 or j>=len(toks)-1:continue
   pat=toks[j]; file_args=toks[j+1:]; paths=[resolve(v)for v in file_args]
   if not all(paths)or len(pat)<3 or len(pat)>350:continue
   signatures=tuple(str(q)for q in paths)
   key=(c['id'],cmd,signatures)
   if key in seen:continue
   seen.add(key);opts=''.join(toks[1:j]);slots.append((k,c['id'],cmd,pat,opts,paths))
def act(z):
 k,r,cmd,pat,opts,paths=z;flags=[v for v in ('E','F','i','w')if v in opts];out=[]
 for path in paths:
  p=sp.run([str(gd),'-n',*['-'+v for v in flags],'--',pat,str(path)],capture_output=True,timeout=8);ll=p.stdout.decode('utf8',errors='replace').splitlines();out.append({'path':str(path.relative_to(repo)).replace('\\','/'),'sha256':sha(path),'exit':p.returncode,'matching_line_count':len(ll),'lines':[[z.split(':',1)[0],z.split(':',1)[1][:230]]for z in ll[:9]if ':'in z],'err':p.stderr.decode(errors='replace')[:150]})
 return {'task':k,'criterion':r,'oracle_command':cmd,'literal_pattern':pat,'flags':flags,'files':out,'scope':'Commande grep du plan sur fichiers non ambigus du Git figé. Le nombre de lignes n’est pas une exécution fonctionnelle ni un résultat historique.'}
with cf.ThreadPoolExecutor(max_workers=6)as execs:results=list(execs.map(act,slots))
wr(pr/'grep_criterii.json',results);print('checked',len(results),'cases',len(set(x['task']for x in results)))

