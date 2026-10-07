from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parent.parent
inv=json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))
q=sys.argv[1] if len(sys.argv)>1 else '1925/2025|242/2026|1263320|1261556|480960255591|375,00'
seen=set()
for x in inv:
 if x['sha256'] in seen:continue
 if any(k in x['cale'] for k in ['.xlsx','.md','.docx','Audit','Raport','Registru','Log','Situati','situati','Reconciliere','jurnal','Jurnal','verificare','Traducere','traducere','Kontoauszug.pdf','10. Banci']):continue
 texts=[]
 for k in ['text_cache','ocr_cache']:
  if x.get(k) and (R/x[k]).exists():texts.append((R/x[k]).read_text(encoding='utf-8'))
 t='\n'.join(texts)
 if re.search(q,t,re.I):
  seen.add(x['sha256']);print('\nSOURCE',x['cale'],'CACHE',x.get('text_cache'),x.get('ocr_cache'))
  if len(sys.argv)>2:print(t[:int(sys.argv[2])])
  else:
   for m in list(re.finditer(q,t,re.I))[:4]:print(t[max(0,m.start()-180):m.end()+400])
