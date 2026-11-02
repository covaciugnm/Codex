from pathlib import Path
import os,re,json,hashlib,datetime,collections,concurrent.futures,itertools,threading
import persoane_copy_20261031 as m
D=m.D; A=m.A/'Repartizare pe persoane';A.mkdir(exist_ok=True)
people={p.name.split(' - ')[0]:p for p in D.iterdir() if p.is_dir() and not p.name[0].isdigit()}
def listing(item):
 n,p=item
 return n,[x for x in p.rglob('*') if x.is_file() and x.suffix.lower() not in {'.md','.txt','.html','.lnk'}]
with concurrent.futures.ThreadPoolExecutor(12) as pool: physical=dict(pool.map(listing,people.items()))
sparse={n for n,v in physical.items() if len(v)<=1}
known=collections.defaultdict(dict)
for n,files in physical.items():
 for f in files:
  match=re.search(r' - ([a-f0-9]{10})(?: - copie \d+)?$',f.stem)
  if match:known[n].setdefault(match[1],[]).append(f)
def aliases(n):
 ts=m.s.norm(n).split()
 if len(ts)>5:return [tuple(ts)]
 return itertools.permutations(ts)
patterns={}
for n in people:
 for words in aliases(n):patterns.setdefault(' '.join(words),set()).add(n)
rx=re.compile(r'\b(?:'+'|'.join(re.escape(k) for k in sorted(patterns,key=len,reverse=True))+r')\b')
def explicit(s):
 vals=set()
 for x in rx.finditer(m.s.norm(s)):vals.update(patterns[x.group()])
 return vals
jobs={};evidence=[]
def add(n,p,sha,kind,why):
 if n in people:jobs.setdefault((n,str(p).lower()),(n,Path(p),sha,kind,why))
old=json.loads((D/'00. Arhiva/00. Administrativ/Organizare 2026-10-01/final_docs.json').read_text('utf-8'))
for r in old:
 for n in r.get('related',[]):add(n,D/r['target'],r['sha'],'Documente comune asociate','Registrul anterior confirma asocierea')
rows=m.records(m.L/'copies.jsonl')
for r in rows:
 if not r.get('target') or not r.get('source') or not r.get('sha256'):continue
 t=Path(r['target']);loc=t.relative_to(D).parts[0]
 for n in r.get('persons',[]):
  if n not in people or loc==people[n].name:continue
  source=Path(r['source'])
  if n not in explicit(source.stem) and not any(n in explicit(x) for x in source.parts[1:-1]):continue
  shared=(len(r['persons'])>1 or len(r.get('cnps',[]))>1 or loc=='00. Documente comune')
  add(n,source,r['sha256'],'Documente comune asociate' if shared else ('Variante din arhiva' if loc=='00. Arhiva' else ''),'Nume complet in calea sursei si asociere in jurnal')
def run(items):
 locks={n:threading.Lock() for n in people}
 def work(job):
  n,p,sha,kind,why=job
  try:
   with locks[n]:
    h=sha or m.digest(p)
    for q in known[n].get(h[:10],[]):
     if m.digest(q)==h:return (n,p,q,'existent',why,h)
    folder=people[n]/kind if kind else people[n]
    folder.mkdir(parents=True,exist_ok=True)
    date=datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y.%m.%d')
    stem=p.stem if p.is_relative_to(D) else (people[n].name.split(' - ',1)[-1] if ' - ' in people[n].name else 'CNP de completat')+' - '+n+' - '+p.stem
    tail=' - modificat '+date+' - '+h[:10]+p.suffix
    q=folder/(m.safe(stem)[:max(30,241-len(str(folder))-len(tail))].rstrip()+tail)
    if q.exists():
     if m.digest(q)==h:return(n,p,q,'existent',why,h)
     raise ValueError('Coliziune de nume')
    with p.open('rb') as src,q.open('xb') as dst:
     for b in iter(lambda:src.read(1024*1024),b''):dst.write(b)
    if m.digest(q)!=h:raise ValueError('SHA diferit')
    os.utime(q,(p.stat().st_mtime,p.stat().st_mtime));known[n].setdefault(h[:10],[]).append(q)
    return(n,p,q,'copiat',why,h)
  except Exception as e:return(n,p,'','eroare: '+str(e),why,sha)
 with (A/'Jurnal repartizare.jsonl').open('a',encoding='utf-8') as out,concurrent.futures.ThreadPoolExecutor(10) as pool:
  for n,p,q,state,why,h in pool.map(work,items):
   rec=dict(persoana=n,sursa=str(p),destinatie=str(q),stare=state,motiv=why,sha256=h);evidence.append(rec);out.write(json.dumps(rec,ensure_ascii=False)+'\n');out.flush()
print('ASOCIERI CONFIRMATE',len(jobs),flush=True)
run(list(jobs.values()))
jobs.clear()
# Prioritate dosarelor cu zero/unu acte: nume complet explicit in denumire sau dosar nominativ exact.
spat={k:v&sparse for k,v in patterns.items() if v&sparse}
sr=re.compile(r'\b(?:'+'|'.join(re.escape(k) for k in sorted(spat,key=len,reverse=True))+r')\b') if spat else None
if sr:
 with m.s.INV.open(encoding='utf-8-sig') as f:
  for line in f:
   rel=line.rstrip('\r\n');ext=os.path.splitext(rel)[1].strip().lower()
   if ext not in {'.pdf','.doc','.docx','.jpg','.jpeg','.png','.tif','.tiff','.xls','.xlsx','.rtf'}:continue
   parts=rel.split('\\');stem=os.path.splitext(parts[-1])[0]
   if parts[-1].startswith(('~$','._')):continue
   context=m.s.norm(stem);ns=set()
   for hit in sr.finditer(context):ns.update(spat[hit.group()])
   if not ns and len(parts)>1 and m.s.KEY.search(context):
    for comp in parts[1:-1]:
     tag=m.s.norm(comp)
     if tag in spat:ns.update(spat[tag])
   for n in ns:add(n,m.s.ROOT/rel,None,'Documente comune asociate' if len(ns)>1 else '','Nume complet in denumire sau dosar nominativ cu tip de act explicit')
print('SURSE PENTRU DOSARE PRIORITARE',len(jobs),flush=True);run(list(jobs.values()))
with concurrent.futures.ThreadPoolExecutor(12) as pool: after=dict(pool.map(listing,people.items()))
counts=collections.Counter(r['stare'] for r in evidence)
report='Repartizare in dosarele individuale\n'+str(datetime.datetime.now())+'\nCopii verificate SHA-256: '+str(counts['copiat'])+'\nDosare care au primit copii: '+str(len({r['persoana'] for r in evidence if r['stare']=='copiat'}))+'\nAlte rezultate: '+str(dict(counts))+'\n\nPersoana | acte inainte | acte dupa (inclusiv subdosare)\n'+'\n'.join(f'{n} | {len(physical[n])} | {len(after[n])}' for n in sorted(people))
(A/'Situatie dosare.txt').write_text(report,'utf-8-sig');print(report.split('\n\n')[0],flush=True)
