from pathlib import Path
import fitz, json, hashlib
from PIL import Image,ImageOps,ImageDraw
root=Path.cwd();qa=root/'folder map/2026.10.29 QA BERGER R11';out=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.29 Werkvertrag R11'
stats={}
for key,name in [('contract','2026.10.29 Werkvertrag BERGER R11.pdf'),('comparison','2026.10.29 BERGER Comparatie contract R09 R11 cu decizii.pdf')]:
 d=fitz.open(out/name); thumbs=[]
 for i,page in enumerate(d):
  pix=page.get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.save(qa/f'{key}-{i+1:02}.png')
  im.thumbnail((620,800));c=Image.new('RGB',(640,830),'#dce5e8');c.paste(im,((640-im.width)//2,25));ImageDraw.Draw(c).text((12,7),f'{key} {i+1}',fill='black');thumbs.append(c)
 for j in range(0,len(thumbs),6):
  sheet=Image.new('RGB',(1920,1660),'white')
  for k,im in enumerate(thumbs[j:j+6]):sheet.paste(im,((k%3)*640,(k//3)*830))
  sheet.save(qa/f'{key}-sheet-{j//6+1:02}.png')
 stats[key]={'pages':len(d),'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest()}
offer=fitz.open(root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09/2026.10.13 Anlage 5 Originalangebot BERGER 2026.08.17.pdf');clean=fitz.open(out/'2026.10.29 Werkvertrag BERGER R11.pdf')
stats['offer_pixel_identical']=[offer[i].get_pixmap().samples==clean[len(clean)-4+i].get_pixmap().samples for i in range(4)]
assert all(stats['offer_pixel_identical'])
(qa/'2026.10.29 Verificare randare finala.json').write_text(json.dumps(stats,indent=2),encoding='utf-8');print(json.dumps(stats))
