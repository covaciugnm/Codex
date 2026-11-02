from pathlib import Path
import os,json,shutil,collections,concurrent.futures
import persoane_copy_20261031 as m
from categorii import categoria
audit=m.A/'Repartizare pe persoane';audit.mkdir(exist_ok=True)
rows=m.records(m.L/'copies.jsonl'); seen=set();jobs=[]
for r in rows:
 p=Path(r.get('target','')); sha=r.get('sha256')
 if not sha or not p.is_relative_to(m.D):continue
 parts=p.relative_to(m.D).parts
 if len(parts)!=2 or parts[0][0].isdigit() or p in seen:continue
 seen.add(p); cat=categoria(Path(r['source']).stem)
 q=p.parent/cat/p.name
 jobs.append((p,q,sha))
def copy(job):
 p,q,h=job
 try:
  q.parent.mkdir(parents=True,exist_ok=True)
  if q.exists():
   if m.digest(q)!=h:raise ValueError('Destinatie existenta cu alt continut')
   state='existent'
  else:
   if m.digest(p)!=h:raise ValueError('Sursa nu corespunde jurnalului')
   with p.open('rb') as src,q.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
   if m.digest(q)!=h:raise ValueError('Verificare SHA esuata')
   os.utime(q,(p.stat().st_mtime,p.stat().st_mtime));state='copiat'
 except Exception as e:state='eroare: '+str(e)
 return dict(sursa=str(p),destinatie=str(q),sha256=h,stare=state)
counts=collections.Counter();print('De verificat in categorii:',len(jobs),flush=True)
with (audit/'Jurnal categorii.jsonl').open('a',encoding='utf-8') as f,concurrent.futures.ThreadPoolExecutor(8) as pool:
 for i,r in enumerate(pool.map(copy,jobs),1):
  counts[r['stare']]+=1;f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush()
  if i%100==0:print(i,dict(counts),flush=True)
print('Incheiat',dict(counts),flush=True)
