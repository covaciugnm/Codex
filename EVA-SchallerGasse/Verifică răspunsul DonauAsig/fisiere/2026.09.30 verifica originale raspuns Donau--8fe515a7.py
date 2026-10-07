from pathlib import Path
import json,hashlib,base64
from decimal import Decimal as D
R=Path(__file__).resolve().parent.parent
count=0
for p in (R/'folder map').glob('2026.09.30 Donau bytes *.json'):
 d=json.loads(p.read_text(encoding='utf-8'));chunks=[];offset=0
 for x in d['pages']:
  b=base64.b64decode(x['content_base64'])
  assert x['offset']==offset and len(b)==x['bytes_returned'] and hashlib.sha256(b).hexdigest()==x['sha256']
  chunks.append(b);offset+=len(b);count+=1
 actual=R/'08. Corespondenta/2026.09.30 Raspuns Commerz - analiza Donau 2616052'/('2026.09.30 '+d['name'])
 assert offset==d['size'] and actual.read_bytes()==b''.join(chunks)
assert D('1591.81')*3+D('550.72')==D('5326.15')
print('5 originale verificate integral;',count,'segmente SHA-256; totalul 5.326,15 EUR reconciliat.')
