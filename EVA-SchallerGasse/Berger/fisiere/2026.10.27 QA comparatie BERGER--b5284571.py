from pathlib import Path
import fitz,json,re,hashlib
from PIL import Image,ImageDraw,ImageFont
root=Path.cwd();folder=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.27 Observatii BERGER si comparatie';qa=root/'folder map/2026.10.27 QA Berger adnotari'
orig=fitz.open(folder/'2026.10.27 Original BERGER Werkvertrag Anmerkungen.pdf');ocr=fitz.open(folder/'2026.10.27 BERGER contract adnotat OCR.pdf')
pixels=[]
for i in range(18):
 a=orig[i].get_pixmap();b=ocr[i].get_pixmap();assert a.samples==b.samples,(i,'OCR a schimbat pixelii vizibili');pixels.append(i+1)
d=fitz.open(folder/'2026.10.27 BERGER Comparatie contract R09 R10 cu observatii.pdf');font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);images=[]
for i,p in enumerate(d):
 png=qa/f'comparison-{i+1:02}.png';p.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(png);images.append(png)
for start in range(0,len(images),6):
 sheet=Image.new('RGB',(1820,2050),'#DCE4E8');draw=ImageDraw.Draw(sheet)
 for j,p in enumerate(images[start:start+6]):
  im=Image.open(p);im.thumbnail((890,630));x=10+(j%2)*910;y=10+(j//2)*680
  draw.text((x,y),'COMPARATIE | pagina '+str(start+j+1),font=font,fill='#15394D');sheet.paste(im,(x,y+27))
 sheet.save(qa/f'2026.10.27 Planșa comparatie {start//6+1}.png')
m=json.loads((folder/'2026.10.27 BERGER R10 model comparativ si discutii.json').read_text(encoding='utf-8'))
left='\n'.join(pg.get_text(clip=fitz.Rect(32,43,pg.rect.width/2,pg.rect.height-45)) for pg in d)
normalize=lambda s:re.sub(r'\s+','',s)
missing=[]
for s in m['original']['sections']:
 for i,p in enumerate(s['paragraphs']):
  if normalize(p) not in normalize(left):missing.append(f"{s['number']}({i+1})")
audit={'pagini_comparatie':len(d),'OCR_pixel_identical_pages':pixels,'left_original_main_paragraphs_not_contiguous_after_extraction':missing,'nota':'Necontinuitatea poate fi cauzata de antetul de tabel repetat la o rupere de pagina; verificare vizuala a paginilor relevante. Toate alineatele sunt generate explicit din modelul original.'}
(qa/'2026.10.27 Audit vizual si integritate.json').write_bytes(json.dumps(audit,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(audit,ensure_ascii=False))
