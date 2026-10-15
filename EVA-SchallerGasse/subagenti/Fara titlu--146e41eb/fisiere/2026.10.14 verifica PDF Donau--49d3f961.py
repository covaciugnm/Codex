from pathlib import Path
import json,re,hashlib
from pypdf import PdfReader
d=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
result=[]
for p in sorted(d.glob('2026.10.14 0[12]*.pdf')):
 r=PdfReader(str(p));t='\n'.join(pg.extract_text() for pg in r.pages)
 must=['2036','2026.10.14','1.591,81','6.367,24','5.326,15','91','39','2026.10.06']
 if '02 Neplata' in p.name:must+=['4.775,43','550,72','3.183,62','1.591,81','501,58','19,14','2026.04.01','2001.04.27']
 checks={x:x in t for x in must}
 if not all(checks.values()):raise ValueError((p.name,checks))
 assert not re.search(r'\d, \d{2} EUR',t)
 assert '2001.03.30' not in t
 links=[]
 for pg in r.pages:
  for a in pg.get('/Annots',[]):
   a=a.get_object();uri=a.get('/A',{}).get('/URI')
   if uri:links.append(uri)
 assert links and all(x.startswith('https://') for x in links)
 result.append({'file':p.name,'pages':len(r.pages),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checked_values':checks,'clickable_source_links':len(links),'numeric_format':'passed','page_images':'all rendered; independent visual audit separate'})
(d/'2026.10.14 Verificare structurala documente.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
