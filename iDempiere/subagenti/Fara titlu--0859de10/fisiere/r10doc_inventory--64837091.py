from pathlib import Path
import re,gzip,json
T=Path('D:/CodexWork/A12_evidence_20261102'); tree={}
for s in (T/'fulltree.raw').read_bytes().split(b'\0'):
 if b'\t' in s:
  head,name=s.split(b'\t',1);parts=head.split()
  if len(parts)>=3: tree[name.decode('utf8',errors='replace')]=parts[2].decode()
for path,id in tree.items():
 if('/dovezi-11-L1a/'in path and '/T35-'in path)or(re.search(r'/test/Test.{0,55}(Partener|Conector|Corelare|ComparatieS|Decont|Extras).{0,35}\.java$',path)and '/com.eva.ro.contab/'in path):print(id,path, 'cached' if (T/'blobs'/(id+'.gz')).exists()else '')
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');L=B/'executie/R9_pregatire/A12/Relectura_882_addendum_aliasuri.json';print(L.exists());print([str(p) for p in (B/'executie').rglob('*addendum_aliasuri*')])
