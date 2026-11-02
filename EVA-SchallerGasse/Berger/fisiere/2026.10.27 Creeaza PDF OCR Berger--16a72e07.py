from pathlib import Path
import json,csv,io,hashlib
import fitz
root=Path.cwd();folder=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.27 Observatii BERGER si comparatie';qa=root/'folder map/2026.10.27 QA Berger adnotari'
src=folder/'2026.10.27 Original BERGER Werkvertrag Anmerkungen.pdf';d=fitz.open(src)
assert len(d)==18 and src.stat().st_size==6248347
texts=[];stats=[]
for i,pg in enumerate(d):
 r=json.loads((qa/f'ocr-{i+1}.json').read_text(encoding='utf-8'));texts.append(f'--- PAGINA SCAN {i+1} / PAGINA R09 {i+1} ---\n'+r['text'])
 count=0
 for w in csv.DictReader(io.StringIO(r['tsv']),delimiter='\t',fieldnames=['level','page_num','block_num','par_num','line_num','word_num','left','top','width','height','conf','text']):
  text=(w.get('text') or '').strip()
  if w.get('level')!='5' or not text:continue
  x,y,h=float(w['left'])/2.5,float(w['top'])/2.5,float(w['height'])/2.5
  pg.insert_text((x,y+h*.84),text,fontsize=max(3.0,h*.88),fontname='OCRArial',fontfile='C:/Windows/Fonts/arial.ttf',render_mode=3)
  count+=1
 stats.append({'pagina':i+1,'confidence':r['confidence'],'cuvinte':count})
dest=folder/'2026.10.27 BERGER contract adnotat OCR.pdf';d.set_metadata({'title':'BERGER - adnotari 2026.10.27 - OCR al scanului original','subject':'18 pagini scanate, cu strat OCR automat; manuscrisul necesita verificare vizuala','author':'A&C Wohnart'});d.save(dest,garbage=4,deflate=True);d.close()
with fitz.open(dest) as check:assert len(check)==18 and all(len(pg.get_text().strip())>500 for pg in check)
txt='2026.10.27 | OCR AUTOMAT - VERIFICAREA VIZUALA A MANUSCRISULUI RAMANE NECESARA\nTextul OCR nu certifica nume, cifre, semnaturi sau acceptari. Scanul contine numai paginile 1-18 din R09 (29 pagini).\n\n'+'\n\n'.join(texts)
(folder/'2026.10.27 Text OCR automat BERGER.txt').write_bytes(txt.encode('utf-8'))
digest=hashlib.sha256(src.read_bytes()).hexdigest();cache=root/'folder map/ocr';cache.mkdir(exist_ok=True);(cache/(digest+'.txt')).write_bytes(txt.encode('utf-8'))
(qa/'2026.10.27 Audit OCR.json').write_bytes(json.dumps({'source_sha256':digest,'pdf_ocr':str(dest.relative_to(root)).replace('\\','/'),'pages':stats,'nota':'Stratul OCR este invizibil; scanul si manuscrisul vizibil sunt pastrate. Textul tiparit a fost confruntat cu R09; notele manuscrise sunt analizate separat.'},ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'pdf':str(dest),'pagini':18,'confidence_min':min(x['confidence'] for x in stats),'text_chars':len(txt)},ensure_ascii=False))
