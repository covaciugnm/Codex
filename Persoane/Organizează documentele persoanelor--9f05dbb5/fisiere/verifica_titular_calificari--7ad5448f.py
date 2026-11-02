import sys,time,json,collections,os,re
from pathlib import Path
import calificari as c
import persoane_ocr_20261031 as o
from persoane_supervisor_20261031 import alive
import fitz
import numpy as np
J=c.A/'Verificare continut si OCR.jsonl'
def inspect(row):
 p=Path(row['sursa']);h=row['sha256'];pages=[]
 if c.m.digest(p)!=h:raise ValueError('Sursa modificata')
 ext=p.suffix.lower().strip()
 if ext=='.pdf':
  with fitz.open(stream=p.read_bytes(),filetype='pdf') as doc:
   for i,pg in enumerate(doc):
    t=pg.get_text()
    if len(t.strip())<45 and pg.get_images():
     pix=pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5),colorspace=fitz.csRGB,alpha=False)
     t=o.ocr_image(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3))
    pages.append((i+1,t))
 elif ext in c.s.IMGEXT:pages=[(1,o.ocr_image(p.read_bytes()))]
 elif ext in c.s.DOCEXT:pages=[(None,c.s.extract(str(p),ext)[0])]
 out=[]
 for nr,t in pages:
  norm=c.s.norm(t);hit=c.key.search(norm)
  if not hit or c.neg.search(norm[:180]):continue
  # For holder assignment require the complete name or known personal number near the credential on the same page.
  small=norm[max(0,hit.start()-200):hit.end()+450];names=c.m.closematch(small,list(c.people.values()))
  if len(names)==1:
   r=c.store(p,names[0],'Nume complet sau CNP langa denumirea calificarii pe aceeasi pagina; asociere de verificat',nr,h);out.append(r)
 return out
def main(pid):
 done={r.get('sha256') for r in c.readrows(J)};counts=collections.Counter()
 while True:
  active=alive(pid)
  rows={r['sha256']:r for r in c.readrows(c.log) if r.get('sha256') and r.get('persoana')=='Titular de verificat' and r.get('sha256') not in done}
  with J.open('a',encoding='utf-8') as f:
   for h,row in rows.items():
    try:found=inspect(row);state='asociere identificata' if found else 'titular neconfirmat'
    except Exception as e:found=[];state='eroare: '+str(e)
    f.write(json.dumps(dict(sha256=h,sursa=row['sursa'],stare=state,pagini_si_destinatii=found),ensure_ascii=False)+'\n');f.flush();done.add(h);counts[state]+=1
  if not active:break
  time.sleep(20)
 print(dict(counts),flush=True)
if __name__=='__main__':main(int(sys.argv[1]))
