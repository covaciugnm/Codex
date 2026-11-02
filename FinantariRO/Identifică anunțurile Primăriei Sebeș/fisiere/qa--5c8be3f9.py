from pathlib import Path
import json,re,hashlib,sys
import pymupdf as fitz
from docx import Document
from PIL import Image,ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).parent;out=B/'qa';out.mkdir(exist_ok=True)
jobs=json.loads((B/'jobs.json').read_text(encoding='utf-8'));result=[];images=[]
for idx,j in enumerate(jobs,1):
 d=fitz.open(j['pdf']);imgs=[];texts=[]
 for pno,p in enumerate(d,1):
  target=out/f'doc_{idx:02}_p{pno}.png'
  if not target.exists() or target.stat().st_mtime < Path(j['pdf']).stat().st_mtime:p.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(target)
  imgs.append(str(target));images.append((target,f'{idx:02} P{j["project"]} {Path(j["docx"]).stem[:35]} p{pno}'))
  texts.append(p.get_text())
 words='\n'.join(re.sub(r'(?m)^ROSE \| Audit intern dosar Sebeș[^\n]*\n?','',t) for t in texts)
 doc=Document(j['docx']);xmltext=' '.join(x.text or '' for x in doc.element.iter() if x.tag.endswith('}t'))
 norm=lambda s:re.sub(r'\W+','',s).lower()
 # A comparison of ordered text is unsuitable for tables; check every substantive paragraph or table cell.
 missing=[]
 for t in [x.text for x in doc.paragraphs]+[c.text for tb in doc.tables for row in tb.rows for c in row.cells]:
  if len(norm(t))>15 and norm(t) not in norm(words):missing.append(t[:120])
 cv='CV_' in Path(j['docx']).name
 result.append(dict(index=idx,project=j['project'],docx=j['docx'],pdf=j['pdf'],pages=len(d),images=imgs,unmatched_text=missing,signature_each_cv_page=all('Semnătura' in t and '02.11.2026' in t for t in texts) if cv else None,has_placeholder=('[DE ' in words),sha256=hashlib.sha256(Path(j['pdf']).read_bytes()).hexdigest()))
for start in range(0,len(images),9):
 batch=images[start:start+9];canvas=Image.new('RGB',(1200,1740),'#dddddd');dr=ImageDraw.Draw(canvas)
 for n,(p,label) in enumerate(batch):
  im=Image.open(p);im.thumbnail((390,530));x=(n%3)*400;y=(n//3)*580;canvas.paste(im,(x,y+30));dr.text((x+3,y+3),label,fill='black')
 canvas.save(out/f'contact_{start//9+1:02}.jpg')
(B/'qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('PDF',len(result),'pages',len(images),'text anomalies',sum(bool(r['unmatched_text']) for r in result),'CV signatures',all(r['signature_each_cv_page'] for r in result if r['signature_each_cv_page'] is not None))
for r in result:
 if r['unmatched_text']:print(r['index'],r['unmatched_text'])
