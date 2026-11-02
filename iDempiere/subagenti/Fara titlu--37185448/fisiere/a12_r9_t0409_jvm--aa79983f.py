from a12_r9_orig import *
import a12_r8_jvm as harness
from concurrent.futures import ThreadPoolExecutor
harness.J=P9/'T04_suita';harness.J.mkdir(exist_ok=True);harness.T8=R9L/'suites';harness.T8.mkdir(exist_ok=True)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4)as px:run=list(px.map(harness.go,[(t,s)for s in ['TestCorelareComenzi','TestT22Ramburs']for t in ['git','instalat']]))
 fs=[];src=r7map['T04.09-R3-001']['source_row'];anchors=block(src['source_file'],src['sha_or_git_blob'],[36,68,273,274,275,280,281,285,286,287,288,289,290])
 for z in run:
  f=B/z['log']['file'];vv=f.read_text(encoding='utf8').splitlines();entries=[]
  for i,v in enumerate(vv,1):
   if not re.match(r'\s*(OK|FAIL)\s+',v)or not re.search(r'⇒.*(?:LEGAT_AUTO\|R5|DE_LAMURIT\|R5g)|R3: AWB-ul comenzii|linie.*NELEGAT|decontarea liniei|niciun candidat → NELEGAT|cauza.*comision|1 linie aceeași zi',v,re.I):continue
   entries.append({'line':i,'observed':v.strip(),'sha':hashlib.sha256(v.encode()).hexdigest(),'stack':vv[i].split('|',1)[1]if i<len(vv)and vv[i].startswith('ANCHOR')else None})
  fs.append({'target':z['target'],'suite':z['suite'],'jar_sha':z['jar_sha'],'java_source':z['file'],'source_sha':z['source_sha'],'log':z['log'],'exit_entire':z['exit'],'markers':entries})
 p=P9/'T04_09_reconcilieri.json';wr(p,{'utc':now(),'criterion':'T04.09-R3-001','origin':anchors,'criterion_recovered':'Când decontul lipsește, R04 rămâne DE_LAMURIT; un singur candidat potrivit și un grup neclar trebuie distinse. Fereastra și structura martorului cu 49 linii Wise trebuie probate separat.','retested':fs,'scope':'MotorCorelare R3 AWB/R5 decont/încasare/exceptie; nu este traseul în UI sau o importare bancară integrală cu postări R04.'});print(sha(p),[(q['suite'],q['target'],len(q['markers']))for q in fs])

