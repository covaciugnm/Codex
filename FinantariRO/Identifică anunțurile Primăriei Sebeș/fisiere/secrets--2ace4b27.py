import io,zipfile,sqlite3,hashlib,re,struct,json,math,collections
from pathlib import Path
R=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository');O=Path(r'D:\Codex\iFLYTEK-audit\results')
C=sqlite3.connect(O/'secrets-staging.sqlite');C.execute('create table if not exists key_candidates(artifact text,location text,sha256 text,length integer,shape text,status text,primary key(artifact,location))')
C.execute('create table if not exists elf_validation(artifact text primary key,has_debug_info integer,has_symtab integer,machine text,bytes integer)')
C.execute('create table if not exists protocol_constants(artifact text,location text,kind text,value text,primary key(artifact,location,kind,value))')
seen=set()
def scan(b,path):
 h=hashlib.sha256(b).hexdigest()
 if h in seen:return
 seen.add(h);items=[]
 if path.endswith('.dex'):
  n,off=struct.unpack_from('<II',b,56)
  for i in range(n):
   p=struct.unpack_from('<I',b,off+4*i)[0]
   while b[p]&128:p+=1
   p+=1;q=b.index(b'\0',p);items.append(('string_id:'+str(i),b[p:q]))
 else:
  from elftools.elf.elffile import ELFFile
  ef=ELFFile(io.BytesIO(b));C.execute('insert or ignore into elf_validation values(?,?,?,?,?)',(h,int(ef.has_dwarf_info(strict=True)),int(ef.get_section_by_name('.symtab') is not None),ef['e_machine'],len(b)))
  items=[('byte_offset:'+str(m.start()),m.group()) for m in re.finditer(rb'[\x20-\x7e]{16,2000}',b)]
 count=0
 for loc,s in items:
  text=s.decode('ascii','ignore')
  for uuid in re.findall(r'(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',text):C.execute('insert or ignore into protocol_constants values(?,?,?,?)',(h,loc,'UUID candidate (service/characteristic/id not inferred)',uuid))
  if re.fullmatch(r'/[A-Za-z0-9_./{}-]{3,200}',text):C.execute('insert or ignore into protocol_constants values(?,?,?,?)',(h,loc,'path candidate (API/file/resource not inferred)',text))
  shape=None
  if b'PRIVATE KEY-----' in s:shape='PEM marker (check source; may be public test fixture)'
  elif re.fullmatch(rb'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',s):shape='JWT-like'
  elif re.fullmatch(rb'AIza[A-Za-z0-9_-]{30,50}',s):shape='Google API-key-like'
  elif re.fullmatch(rb'[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}',s):shape='hex (hash/identifier/key ambiguous)'
  elif 24<=len(s)<=128 and re.fullmatch(rb'[A-Za-z0-9+/_=-]+',s) and re.search(rb'[0-9]',s) and re.search(rb'[A-Za-z]',s):
   freq=collections.Counter(s);entropy=-sum((n/len(s))*math.log2(n/len(s)) for n in freq.values())
   if entropy>=4.3:shape='high-entropy token (unvalidated)'
  if shape:C.execute('insert or ignore into key_candidates values(?,?,?,?,?,?)',(h,loc,hashlib.sha256(s).hexdigest(),len(s),shape,'candidate only; not tested; no raw value retained'));count+=1
 C.commit();print(h[:12],path,count,flush=True)
def comp(z):
 for e in z.infolist():
  if e.filename.endswith(('.dex','.so')):scan(z.read(e),e.filename)
inputs=list((R/'collection-2026-11-01/applications').glob('*.apk'))+list((R/'collection-2026-11-01/applications').glob('*.xapk'))+[p for p in (R/'apk-analysis-2026-11-01/.work/inputs').glob('*.apk') if not p.name.startswith('iflytek-')]+list(Path(r'D:\Codex\iFLYTEK-audit\stable-inputs').glob('*.apk'))
for p in inputs:
 with zipfile.ZipFile(p) as z:
  if p.suffix=='.xapk':
   for e in z.infolist():
    if e.filename.endswith('.apk'):comp(zipfile.ZipFile(io.BytesIO(z.read(e))))
  else:comp(z)
C.close()
