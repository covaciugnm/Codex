import re,os,json,hashlib,shutil,collections,datetime,threading,concurrent.futures
from pathlib import Path
import persoane_scan_20261031 as s
import persoane_copy_20261031 as m
A=s.AUDIT/'Diplome acreditari si licente';A.mkdir(exist_ok=True)
cat='03. Diplome si Cursuri'; log=A/'Registru.jsonl'
key=re.compile(r'\b(?:DIPLOM(?:A|E|EI|ELE|ELOR)?|ACREDITAR\w*|ACREDITAT\w*|LICENT[AE]\w*|LICIENT[AE]\w*|ATESTAT\w*|BACALAUREAT|FOAIE MATRICOLA|CERTIFICAT(?:UL|E)? (?:DE )?(?:ABSOLVIRE|CALIFICARE|COMPETENT\w*|PARTICIPARE|FORMARE|SPECIALIZARE)|CERTIFICATION|ACCREDITATION|DEGREE CERTIFICATE)\b')
neg=re.compile(r'\b(?:SOFTWARE|WINDOWS|MICROSOFT|ANTIVIRUS|AUTODESK|COPYRIGHT|GPL|OPEN SOURCE|OFFICE 365|END USER|TEZA DE LICENTA|LUCRARE DE LICENTA|CAIET DE SARCINI|FISA DE DATE|CERINTE MINIME|GHIDUL SOLICITANTULUI)\b')
def hits(t):return bool(key.search(s.norm(t)))
def readrows(p):
 if p.exists():
  with p.open(encoding='utf-8-sig') as f:
   for line in f:
    try:yield json.loads(line)
    except ValueError:pass
people={p['name']:p for p in s.people()}
locks=collections.defaultdict(threading.Lock);index={};memo={};counts=collections.Counter()
def store(src,name,why,page=None,want=None):
 p=Path(src); f=s.DEST/people[name]['folder']/cat if name in people else s.DEST/'99. De verificat'/cat
 record=dict(sursa=str(p),persoana=name,motiv=why,pagina=page)
 try:
  sha=want or m.digest(p)
  with locks[str(f)]:
   f.mkdir(parents=True,exist_ok=True)
   if f not in index:
    index[f]=collections.defaultdict(list)
    for y in f.iterdir():
     ix=re.search(r' - ([a-f0-9]{10})(?: - copie \d+)?$',y.stem)
     if ix:index[f][ix[1]].append(y)
   q=next((y for y in index[f][sha[:10]] if m.digest(y)==sha),None)
   if q:state='deja prezent'
   else:
    st=p.stat(); prefix=(people[name].get('cnp') or 'CNP de completat')+' - '+name if name in people else 'CNP de completat - TITULAR DE VERIFICAT'
    original=p.stem; stem=m.safe(prefix+' - '+original) if not p.is_relative_to(s.DEST) else m.safe(original)
    tail=' - modificat '+datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y.%m.%d')+' - '+sha[:10]+p.suffix
    q=f/(stem[:max(22,238-len(str(f))-len(tail))].rstrip()+tail)
    if q.exists():raise ValueError('coliziune')
    with p.open('rb') as srcf,q.open('xb') as dest:shutil.copyfileobj(srcf,dest,1024*1024)
    if m.digest(q)!=sha:raise ValueError('SHA diferit')
    os.utime(q,(st.st_mtime,st.st_mtime));index[f][sha[:10]].append(q);state='copiat'
   record.update(stare=state,destinatie=str(q),sha256=sha)
 except Exception as e:record.update(stare='eroare',detaliu=str(e))
 return record
def save(rows):
 with log.open('a',encoding='utf-8') as f:
  for r in rows:
   counts[r['stare']]+=1;f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush()
def report(msg):
 (A/'Stadiu.txt').write_text(msg+'\n'+str(dict(counts))+'\nRegistrul contine sursa, destinatia, baza identificarii si pagina (cand este cunoscuta).\n','utf-8-sig')
def main():
 s.init();old=s.AUDIT.parent/'Organizare 2026-10-01';jobs=[]
 for filename in ['embedded.json','final_docs.json']:
  for r in json.loads((old/filename).read_text('utf-8')):
   if hits(r.get('type','')) and r.get('name') in people and r.get('target'):
    jobs.append((s.DEST/r['target'],r['name'],'Tip si titular din registrul verificat: '+r['type'],r.get('page'),r.get('sha')))
 report('In curs: verificare acte si pagini din registrul anterior.')
 with concurrent.futures.ThreadPoolExecutor(6) as pool:save(pool.map(lambda j:store(*j),jobs))
 scans={r['sha256']:r for r in readrows(s.LOCAL/'scan.jsonl') if r.get('sha256') and not r.get('error')}
 candidates={};exts=s.DOCEXT|s.IMGEXT
 with s.INV.open(encoding='utf-8-sig') as f:
  for l in f:
   rel=l.strip(); ext=os.path.splitext(rel)[1].lower().replace(' ','')
   if ext not in exts or not hits(rel):continue
   p=s.ROOT/rel
   if p.name.startswith(('~$','._')) or neg.search(s.norm(rel)):continue
   # An explicit document name, or a scan inside a qualification folder, is evidence.
   if hits(p.stem) or (hits(p.parent.name) and ext in s.IMGEXT|{'.pdf'}):candidates[str(p)]=('denumire sau dosar de calificari',None)
 report('In curs: '+str(len(candidates))+' candidati dupa denumire; verific si continutul indexat.')
 # Require credential wording typical of an issued act for text-only candidates; a CV mention alone is insufficient.
 issued=re.compile(r'\b(DIPLOMA DE (?:LICENTA|MASTER|BACALAUREAT|DOCTOR)|CERTIFICAT DE (?:ABSOLVIRE|CALIFICARE|COMPETENTE PROFESIONALE)|ATESTAT DE (?:COMPETENT|LIBERA PRACTICA)|SE ACORDA (?:PREZENT\w* )?(?:DIPLOMA|ATESTAT)|TITULAR(?:UL)? (?:LICENTEI|ACREDITARII))\b')
 for cache in [Path(os.environ['TEMP'])/'persoane-20261031/text',s.LOCAL/'text']:
  if not cache.exists():continue
  for f in cache.glob('*.txt'):
   r=scans.get(f.stem)
   if not r or r['source'] in candidates:continue
   try:t=s.norm(f.read_text('utf-8'));match=issued.search(t)
   except (OSError,UnicodeError):continue
   if match and not neg.search(s.norm(Path(r['source']).stem)):candidates[r['source']]=('formulare de act in continut; necesita confirmare',r)
 persons=list(people.values())
 def verify(it):
  src,(why,r)=it;p=Path(src)
  names=m.closematch(p.stem,persons)
  if not names:
   for comp in reversed(p.parts[1:-1]):
    ns=m.closematch(comp,persons)
    if ns:names=ns;break
  if len(names)!=1 or 'necesita confirmare' in why:names=['Titular de verificat']
  return store(p,names[0],why,None,r.get('sha256') if r else None)
 report('In curs: '+str(len(candidates))+' surse candidate, inclusiv cele din continut. Se verifica copiile.')
 with concurrent.futures.ThreadPoolExecutor(6) as pool:save(pool.map(verify,candidates.items()))
 report('Trecerea prin inventar si textele disponibile s-a incheiat. OCR general continua; scanarile inca necitite nu sunt acoperite.')
if __name__=='__main__':main()
