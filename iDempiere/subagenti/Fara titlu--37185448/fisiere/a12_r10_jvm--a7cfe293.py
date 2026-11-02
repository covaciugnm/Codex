from a12_r10_base import *
import a12_r8_jvm as j
from concurrent.futures import ThreadPoolExecutor
j.J=P10/'JVM';j.J.mkdir(exist_ok=True);j.T8=Path('D:/CodexWork/a12-r10-local/jvm');j.T8.mkdir(exist_ok=True)
suites=['TestT227VerificareImport','TestT35Stoc','TestT211Garda','TestT22FisaCanal','TestT28Meniu','TestT22Ajutor','TestComparatieSaga','TestComparatieSagaEcran','TestT22VanzariOnline']
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3)as px:result=list(px.map(j.go,[(t,n)for n in suites for t in ['git','instalat']]))
 f=P10/'JVM_original.json';wr(f,{'utc':now(),'runs':result});print(sha(f),[(z['suite'],z['target'],z['exit'])for z in result])

