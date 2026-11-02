from a12_r4_suites import *
from pathlib import Path
ids=['T03','T58','T159','T326','T186','T190','T201','T163','T330','T11','T329','T156','T191','T194','T325','T324','T323','T334','T157','T200','T203','T204','T205','T213','T214','T160','T158','T162','T164','T165','T166','T167','T168','T169','T171','T172','T173','T174','T175','T177','T178','T180','T181','T182','T183','T184','T185','T188','T189','T192','T193','T195','T196','T198','T199','T202','T206','T207','T209','T210','T219']
pat=re.compile('^Test('+'|'.join(ids)+')(?![0-9])');fs=[p for p in (plug/'test').glob('Test*.java') if pat.match(p.stem) and p.stat().st_size <120000 and 'static void main(' in p.read_text(encoding='utf8',errors='replace')]; prev={v['suite']for v in rd(o/'executii.json')};fs=[p for p in fs if p.stem not in prev]
if __name__=='__main__':
 rs=[]
 with cf.ThreadPoolExecutor(max_workers=5)as px:
  for i,v in enumerate(px.map(rr,[(t,j,p) for p in fs for t,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]])):
   rs.append(v)
   if i%10==0:wr(o/'progress2.json',{'done':len(rs),'expected':2*len(fs)})
 wr(o/'executii2.json',rs);print(len(fs),len(rs),sum(v['run_exit']is not None for v in rs),sum(v['run_exit']==0 for v in rs))

