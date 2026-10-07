from pathlib import Path
import fitz, hashlib, json, re, unicodedata, zipfile
from docx import Document
from PIL import Image, ImageDraw
import genereaza_documente as g
W=Path(__file__).resolve().parent
OUT=W.parent
pdf=next(OUT.glob('01*.pdf'));docx=next(OUT.glob('01*.docx'))
d=fitz.open(pdf); o=fitz.open(g.OFFER)
a3=next(i for i,p in enumerate(d) if 'Anlage 3 – Bestellungs- und Nachweisblatt' in p.get_text())
offer_start=a3-3
assert all(d[offer_start+i].get_pixmap().samples==o[i].get_pixmap().samples for i in range(3)), 'Offer render differs'
assert hashlib.sha256(g.OFFER.read_bytes()).digest()==hashlib.sha256(next(OUT.glob('03*.pdf')).read_bytes()).digest()
def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
    return re.sub(r'\s+','',s)
pdft=norm(' '.join(p.get_text(clip=fitz.Rect(40,40,p.rect.width-40,p.rect.height-40)) for i,p in enumerate(d) if not offer_start<=i<a3))
wd=Document(docx);wordt=norm(re.sub(r'\(https?://[^)]+\)','', ' '.join(p.text for p in wd.paragraphs)))
missp=[];missw=[]
for typ,v in g.parse(g.SOURCE.read_text(encoding='utf-8')):
    if isinstance(v,str) and typ!='pagebreak':
        n=norm(g.plain(v))
        if n not in pdft:missp.append(v[:100])
        if n not in wordt:missw.append(v[:100])
assert not missp,missp
assert not missw,missw
pages=[];out=W/'layout'
for i,p in enumerate(d):
    pix=p.get_pixmap(matrix=fitz.Matrix(.62,.62),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    canv=Image.new('RGB',(im.width,im.height+24),'#eeeeee');canv.paste(im,(0,24));ImageDraw.Draw(canv).text((8,5),f'PDF page {i+1}',fill='black');pages.append(canv)
for first in range(0,len(pages),6):
    group=pages[first:first+6];cw=max(x.width for x in group);ch=max(x.height for x in group)
    sheet=Image.new('RGB',(cw*3,ch*2),'#bbbbbb')
    for j,im in enumerate(group):sheet.paste(im,((j%3)*cw,(j//3)*ch))
    sheet.save(out/f'contact_{first+1:02d}.png')
bounds=[]
for i,p in enumerate(d):
    if offer_start<=i<a3:continue
    for b in p.get_text('blocks'):
        if b[0]<40 or b[2]>p.rect.width-40 or b[1]<15 or b[3]>p.rect.height-15:bounds.append({'page':i+1,'bbox':b[:4],'text':b[4][:80]})
assert not bounds,bounds
with zipfile.ZipFile(docx) as z:
    media=[x for x in z.namelist() if x.startswith('word/media/')]
report={'source_sha256':hashlib.sha256(g.SOURCE.read_bytes()).hexdigest(),'pdf_pages':len(d),'offer_pages':[offer_start+1,offer_start+2,offer_start+3],'source_paragraphs_all_in_pdf':not missp,'source_paragraphs_all_in_docx':not missw,'original_offer_pixel_identical':True,'original_offer_copy_sha_identical':True,'docx_facsimile_images':len(media),'docx_sections':len(wd.sections),'text_out_of_bounds':bounds,'docx_render_note':'Native Word text and package inspected; Word pagination not rendered on this host. PDF visually checked separately.'}
(W/'QA_ARTEFACTE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
