from pathlib import Path
from docx import Document
import json,re
B=Path(__file__).parent;rs=json.loads((B/'records.json').read_text(encoding='utf-8'));js=json.loads((B/'jobs.json').read_text(encoding='utf-8'))
seen=set();out=[]
for r in rs:
 key=(r['project'],r['dest'],r['title'])
 if key in seen:continue
 seen.add(key)
 if r['folder']==19:r['action']='Document intern pentru verificare; nu se semnează și nu se depune în această formă.'
 if r['title']=='Diplomă master Ilinca':r['required']='Suport dacă se invocă';r['action']='Atașați diploma pentru susținerea afirmației din CV sau eliminați afirmația dacă nu poate fi confirmată.'
 for k in ['title','obs','action']:
  r[k]=re.sub(r'(?<=[A-Za-zĂÂÎȘȚăâîșț])(?=\d)', ' ',r.get(k,''))
  r[k]=r[k].replace('A 1','A1').replace('A 6','A6').replace('P 1','P1').replace('P 2','P2').replace('0–6','0–6')
 out.append(r)
for j in js:
 if not Path(j['docx']).name.startswith('19_Verificare'):continue
 d=Document(j['docx'])
 for p in d.paragraphs:
  s=re.sub(r'(?<=[A-Za-zĂÂÎȘȚăâîșț])(?=\d)', ' ',p.text)
  s=re.sub(r'(?<=:)(?=\d)',' ',s)
  if s!=p.text:p.text=s
 d.save(j['docx'])
(B/'records.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Records after dedup',len(out))
