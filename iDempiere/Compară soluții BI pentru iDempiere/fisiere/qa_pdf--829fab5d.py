from pathlib import Path
import pypdfium2 as pdfium
from pypdf import PdfReader
from PIL import Image,ImageDraw
import json
R=Path(r'\\192.168.100.169\Comun\00.Roboti\iDempiere\Documentatie\BI_iDempiere');L=Path(__file__).parent
p=R/'00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.pdf';r=PdfReader(p);out=L/'pdf_previews';out.mkdir(exist_ok=True)
d=pdfium.PdfDocument(str(p));summ=[]
for i,page in enumerate(d):
 im=page.render(scale=1.4).to_pil();im.save(out/f'page-{i+1:02}.png');txt=r.pages[i].extract_text();summ.append(dict(page=i+1,characters=len(txt),start=txt[:140]));im.close()
for base in range(0,len(d),6):
 canvas=Image.new('RGB',(1440,1320),'#dce3e8');draw=ImageDraw.Draw(canvas)
 for k in range(6):
  ix=base+k
  if ix>=len(d):break
  im=Image.open(out/f'page-{ix+1:02}.png');im.thumbnail((460,610));x=(k%3)*480+(480-im.width)//2;y=(k//3)*660+30;canvas.paste(im,(x,y));draw.text(((k%3)*480+10,(k//3)*660+10),str(ix+1),fill='black')
 canvas.save(out/f'contact-{base//6+1}.png')
(R/'08_Administrare/verificare_pag pagini.json'.replace('pag pagini','pagini')).write_text(json.dumps(summ,ensure_ascii=False,indent=2),encoding='utf-8')
print('PDF pages',len(d),'minimum chars',min(s['characters'] for s in summ));print([(s['page'],s['characters']) for s in summ if s['characters']<300])
