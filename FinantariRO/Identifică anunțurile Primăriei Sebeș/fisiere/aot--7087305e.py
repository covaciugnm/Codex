import sqlite3,re,json,hashlib,zipfile,io
from pathlib import Path
from elftools.elf.elffile import ELFFile
O=Path(r'D:\Codex\iFLYTEK-audit\results');R=Path(r'D:\Codex\iFLYTEK-audit\prior\aot');C=sqlite3.connect(O/'aot-staging.sqlite')
C.execute('drop table if exists aot_functions')
C.executescript('create table if not exists aot_functions(artifact text,source text,class_name text,declaration text,address integer,size integer,code_hash text,verified integer,primary key(artifact,source,class_name,declaration,address)); create table if not exists aot_field_offsets(artifact text,address integer,offset_name text,kind text,primary key(artifact,address,offset_name,kind));')
original=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository\apk-analysis-2026-11-01\.work\inputs\73170cdc5c3331cd-iflytranslate-official.apk')
b=zipfile.ZipFile(original).read('lib/arm64-v8a/libapp.so');h=hashlib.sha256(b).hexdigest();assert h==json.loads((R/'CONTENTS-SHA256.json').read_text())['provenance']['originalLibrarySha256']
elf=ELFFile(io.BytesIO(b));segments=[s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_flags']&1]
def raw(addr,size):
 for s in segments:
  if s['p_vaddr']<=addr and addr+size<=s['p_vaddr']+s['p_filesz']:
   off=s['p_offset']+addr-s['p_vaddr'];return b[off:off+size]
 return None
stats={'files':0,'functions':0,'verified':0,'provenance':json.loads((R/'CONTENTS-SHA256.json').read_text())['provenance']}
for p in (R/'analysis-original/asm').rglob('*.dart'):
 stats['files']+=1;cls='';decl='';source=str(p.relative_to(R))
 for line in p.read_text(encoding='utf-8',errors='replace').splitlines():
  m=re.match(r'class (.*?)\s*\{',line)
  if m:cls=m[1]
  m=re.match(r'  (\S.*?)\s*\{\s*$',line)
  if m:decl=m[1]
  m=re.search(r'// \*\* addr: (0x[0-9a-f]+), size: (0x[0-9a-f]+)',line)
  if m:
   addr=int(m[1],16);size=int(m[2],16);code=raw(addr,size);ok=code is not None and addr%4==0 and size%4==0
   C.execute('insert or replace into aot_functions values(?,?,?,?,?,?,?,?)',(h,source,cls,decl,addr,size,hashlib.sha256(code).hexdigest() if code else None,int(ok)));stats['functions']+=1;stats['verified']+=int(ok)
  m=re.search(r'(LoadField|StoreField): .*?->(field_[0-9a-f]+)',line)
  if m:C.execute('insert or ignore into aot_field_offsets values(?,?,?,?)',(h,addr,m[2],m[1]))
C.commit();C.close();(O/'aot-validation.json').write_text(json.dumps(stats,indent=2),encoding='utf-8');print(stats)
