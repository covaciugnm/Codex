from a12_r4_suites import *
from pathlib import Path
names=['TestScanareCod','TestScanareEcrane']
r=[]
with cf.ThreadPoolExecutor(max_workers=3)as px:
 r=list(px.map(rr,[(t,j,plug/'test'/(n+'.java'))for n in names for t,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]]))
wr(o/'scaner.json',r);print([(v['suite'],v['target'],v['run_exit'],v['summary'][-1:])for v in r])

