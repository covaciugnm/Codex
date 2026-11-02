from pathlib import Path
import json, hashlib, re, sys
from pypdf import PdfReader
from docx import Document
sys.stdout.reconfigure(encoding='utf-8')
base=Path(__file__).parent
paths=[Path(s) for s in (base/'paths.txt').read_text(encoding='utf-8-sig').splitlines()]
rows=[]
for p in paths:
 s=str(p); n=p.name.lower()
 relevant=(('00. Persoane' in s and ('cv' in n or '03. Diplome' in s or 'voluntar' in n)) or ('ASOCIATIA ROSE' in s and any(k in n for k in ['statut','constitut','cui rose','certificat de inscriere','hotararea membrilor','voluntar','contract florin','certificat anaf','certificat fiscal','nota justific','fisa partener','scrisoare'])) or ('14. Situatii financiare' in s and any(k in s for k in ['2022','2023','2024','2025'])))
 if not relevant or n.startswith('~$') or p.suffix.lower() not in ['.pdf','.docx','.doc','.tif','.jpg','.png']: continue
 try:
  b=p.read_bytes(); h=hashlib.sha256(b).hexdigest()
  if any(r.get('sha256')==h for r in rows): continue
  text=''
  if p.suffix.lower()=='.pdf':
   r=PdfReader(p); text='\n'.join(f'PAGE {i+1}\n'+(pg.extract_text() or '') for i,pg in enumerate(r.pages))
  elif p.suffix.lower()=='.docx':
   d=Document(p);text='\n'.join([x.text for x in d.paragraphs]+[c.text for t in d.tables for rw in t.rows for c in rw.cells])
  rows.append({'path':s,'sha256':h,'text':text,'bytes':len(b)})
 except Exception as e: rows.append({'path':s,'error':str(e)})
(base/'extracted.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Extracted',len(rows))
for r in rows:
 if '14. Situatii financiare' not in r['path']: print(r['path'],len(r.get('text','')))
