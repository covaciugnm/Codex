from a12_r10_jvm import *
des=P10/'Zone_A09';des.mkdir(exist_ok=True);j.J=des;j.T8=Path('D:/CodexWork/a12-r10-local/jvm')
with ThreadPoolExecutor(max_workers=3)as px:res=list(px.map(j.go,[(t,n)for t in ['git','instalat']for n in ['TestT29Catalog','TestT204Documente','TestT204Ecrane']]))
f=des/'Suita_tiparituri.json';wr(f,{'utc':now(),'runs':res});print(sha(f),[(z['target'],z['suite'],z['exit'],z['traced'])for z in res])
