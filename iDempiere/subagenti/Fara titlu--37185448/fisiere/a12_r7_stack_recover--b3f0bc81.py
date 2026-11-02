from a12_r7_pg_cui import *
from collections import defaultdict,Counter
from functools import lru_cache
from difflib import SequenceMatcher
import unicodedata,base64
sr=rd(RP/'stack_exec.json');traces={}
def norm(l):
 s=l.split(' · ',1)[-1]if ' · 'in l else l; s=re.sub(r'^\s*(?:ok|fail)\s+', '',s,flags=re.I)
 return ' '.join(re.findall('[a-z0-9]+',''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if unicodedata.category(c)!='Mn')))
for v in sr:
 p=RP/v['log']; assert sha(p)==v['sha'];t=[]
 for i,line in enumerate(p.read_text(encoding='utf8').splitlines(),1):
  if not line.startswith('ANCHOR:'):continue
  body,*frames=line.split('|');msg=base64.b64decode(body.removeprefix('ANCHOR:')).decode('utf8');fs=[]
  for f in frames:
   m=re.fullmatch(r'([^:]+):(\d+):(.*)',f)
   if m and m[1]==v['suite']+'.java':fs.append((int(m[2]),m[3]))
  t.append({'decoded':msg.strip(),'label':norm(msg),'frames':fs,'trace_line':i})
 traces[(v['suite'],v['target'])]=(v,t)
e6=rd(E/'R6/Dovezi_criterii.json')['evidence'];records=rd(E/'R6_pregatire/A12/Oracole_487_EV5.json')['rows'];todo=[v for v in records if v['numeric_basis'].startswith('CONDIȚIE')]
jms=rd(E/'R5/probe/executii_corelate.json')['records']
def source_excerpt(p,i):
 ls=p.read_text(encoding='utf8').splitlines()
 lo=i-1;hi=i
 while lo>i-7 and lo>0 and not re.search(r'(?:(?:chk|t|ok|test|caz|egal|check|compar|verif|eq|assert)\s*\()|^\s*(?:if|try)\s*[\({]',ls[lo],re.I):lo-=1
 while hi<min(len(ls),i+8)and ';'not in ls[hi-1] and '});'not in ls[hi-1]:hi+=1
 return {'file':p.relative_to(repo).as_posix(),'sha':sha(p),'stack_line_exact':i,'range':[lo+1,hi],'source_condition':'\n'.join(ls[lo:hi])}
out=[]
for old in todo:
 eid=old['r5_id'];rawsrc=e6[eid]['source'];n=Path(rawsrc).stem.removeprefix('git_').removeprefix('instalat_');target='git'if Path(rawsrc).name.startswith('git_')else'instalat';v,t=traces[n,target];label=norm(old['observation']);ranked=sorted([(SequenceMatcher(None,label,k['label'],autojunk=False).ratio() if not (k['label'].startswith(label)and len(label)>19)else 1.0,idx)for idx,k in enumerate(t)],reverse=True);score,idx=ranked[0]if ranked else(0,-1)
 exact=idx>=0 and label==t[idx]['label'];top=[t[tt]for sc,tt in ranked if abs(sc-score)<.000001]
 if top and all(r['frames']==top[0]['frames'] for r in top)and (score>=0.73 and (exact or score==1.0 or score-(next((sc for sc,tt in ranked if sc<score-.000001),0))>=0.048)):
  hit=t[idx];f=repo/v['test_source'];fs=hit['frames'];anchors=[]
  if len(fs)>1:
   # Last caller near main identifies the actual suite section; preceding frames resolve the individual subassertion.
   for ln,meth in fs[1:]:
    ex=source_excerpt(f,ln);ex['method']=meth;anchors.append(ex)
  elif fs:anchors=[source_excerpt(f,fs[0][0])]
  outcome='PREDICAT_CONDIȚIE_EXECUTATĂ'if len(fs)>1 and fs[0][1]not in ('t','test','caz','sectiune','sec')else'GRUP_DE_ASERȚIUNI_APEL_IDENTIFICAT'
  children=[]
  if outcome.startswith('GRUP')and fs:
   for child in t:
    fc=child['frames']
    if len(fc)>=3 and fc[-1]==fs[-1]and child['decoded']!=hit['decoded']:
     src=source_excerpt(f,fc[1][0]);children.append({'asserted':child['decoded'],'source_line':src['stack_line_exact'],'expression':src['source_condition'],'raw_pointer':child['trace_line']})
   if not children:outcome='GRUP_IDENTIFICAT_FĂRĂ_VECTORI_INDIVIDUALI_ACCEPTAȚI'
  new={'code_state':outcome,'test_source':v['test_source'],'test_source_sha':v['sha_source'],'target':target,'jar_sha':v['jar_sha'],'trace_log':v['log'],'log_sha':v['sha'],'trace_line':hit['trace_line'],'r7_actual':hit['decoded'],'r5_actual':old['observation'],'capture_match':round(score,4),'stack_exact':fs,'source_anchors':anchors,'child_assertions':children,'limit':'Cadrul executat identifică apelul proiectului și condiția explicită sau grupul. Nu creează o probă de produs nativ sau contabil.'}
 else:new={'code_state':'ASERȚIUNE_NEREIDENTIFICATĂ_FĂRĂ_CREDIT','trace_log':v['log'],'log_sha':v['sha'],'maximum_label_match':round(score,4),'source':v['test_source'],'source_sha':v['sha_source'],'alternatives':[(round(sc,3),t[ix]['decoded'][:155])for sc,ix in ranked[:3]],'limit':'Domeniul testului rămâne cognoscibil, dar rândul statistic din R5 nu se echivalează cu predicatul individual în lipsa unei identificări univoce.'}
 out.append({'evidence':eid,'criterion':old['criterion'],'formerly_missing':True,'comparison':new})
assert len(out)==148;wr(RP/'148_predicate_prin_stack.json',{'source_immutable_R6':sha(E/'R6_pregatire/A12/Oracole_487_EV5.json'),'input_count':len(out),'statistics':Counter(z['comparison']['code_state']for z in out),'rows':out});print(Counter(z['comparison']['code_state']for z in out),[(z['criterion'],z['comparison'].get('maximum_label_match'))for z in out if 'NEREIDENTIFICAT' in z['comparison']['code_state']][:18])

