from a12_r10_jvm import *
j.J=P10/'JVM_registre';j.J.mkdir(exist_ok=True);suites=['TestT201Registre','TestT201Ecrane','TestT220Corelez','TestT22Ramburs','TestT22Factura']
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3)as px:result=list(px.map(j.go,[(t,n)for n in suites for t in ['git','instalat']]))
 f=P10/'JVM_registre_corelare.json';wr(f,{'utc':now(),'runs':result});print(sha(f),[(z['suite'],z['target'],z['exit'])for z in result])
