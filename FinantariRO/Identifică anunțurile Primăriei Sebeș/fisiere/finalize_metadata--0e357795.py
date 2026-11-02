from pathlib import Path
from docx import Document
import json,re
B=Path(__file__).parent;rs=json.loads((B/'records.json').read_text(encoding='utf-8'));js=json.loads((B/'jobs.json').read_text(encoding='utf-8'))
names={'62cc5bcf78':'Acord de parteneriat ROSE și Liceul Tehnologic Sebeș','0a406c5893':'Acord de parteneriat ROSE și Școala Gimnazială Avram Iancu','cf38dd61d4':'Dosar contract și oferte proiect 650H A3 și acord parteneriat','dee50e4dc4':'Raport narativ proiect 650H din arhiva ROSE','bca3842f28d5':'Raport narativ proiect 667H semnat','796597aeb1':'Centralizator campanii A1 A6 proiect 650H semnat'}
changes={}
for r in rs:
 for k,title in names.items():
  if k in r.get('dest','') and r['folder']==14:changes[r['title']]=title;r['title']=title
 for field in ['title','obs','action','source']:
  r[field]=re.sub(r'\b(la|din|anul|anii|contract|certificatul|voluntariat|indică|data|nr\.|seria)(?=\d)',r'\1 ',r.get(field,''),flags=re.I)
for j in js:
 if not Path(j['docx']).name.startswith('17_Opis'):continue
 d=Document(j['docx'])
 for t in d.tables:
  for row in t.rows:
   for c in row.cells:
    for a,z in changes.items():
     if a in c.text:c.text=c.text.replace(a,z)
 d.save(j['docx'])
(B/'records.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Metadata updated')
