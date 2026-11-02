from pathlib import Path
import json,base64,hashlib,re
from decimal import Decimal
import pdfplumber
V=Path(__file__).parent;O=V/'2026.10.14 Originale EVA';O.mkdir(exist_ok=True)
results=[]
for f in sorted(V.glob('2026.10.14 download chunks *.json')):
 d=json.loads(f.read_text(encoding='utf-8'));parts=[];offset=0
 for c in d['chunks']:
  b=base64.b64decode(c['content_base64']);assert c['offset']==offset;offset+=len(b);assert len(b)==c['bytes_returned'];assert hashlib.sha256(b).hexdigest()==c['chunk_sha256'];parts.append(b)
 raw=b''.join(parts);assert len(raw)==d['document']['size'] and d['chunks'][-1]['eof']
 name=re.sub(r'[<>:"/\\|?*\r\n]',' ',d['document']['name']);name=re.sub(r'\s+',' ',name)
 p=O/('2026.10.13 ORIGINAL '+d['document']['id'][:8]+' '+name);p.write_bytes(raw)
 with pdfplumber.open(p) as q:text='\n\n'.join(x.extract_text() or '' for x in q.pages);pages=len(q.pages)
 (O/(p.stem+'.txt')).write_text(text,encoding='utf-8')
 entry={**d['document'],'sha256':hashlib.sha256(raw).hexdigest(),'local_staging_path':str(p),'pages':pages,'original_bytes_verified':True,'text':text}
 if d['document']['name'].startswith('M_'):
  amount=re.search(r'offener Betrag\s+([\d.]+,\d\d)',text,re.I);assert amount,d['document']['name']
  installation=re.search(r'M_(\d+)',d['document']['name']).group(1)
  entry['claimed_balance_eur']=amount.group(1);entry['installation']=installation
  entry['payment_reference']=re.search(r'Zahlungsreferenz\s+(\d+)',text).group(1)
 results.append(entry)
(V/'2026.10.14 Originale verificate si texte.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sturm=[x for x in results if 'claimed_balance_eur' in x]
total=sum(Decimal(x['claimed_balance_eur'].replace('.','').replace(',','.')) for x in sturm)
print(json.dumps({'original_PDFs':len(results),'sturm_positions':[{k:x[k] for k in ['name','installation','claimed_balance_eur','payment_reference']} for x in sturm],'sturm_claimed_total_eur':str(total)},ensure_ascii=False,indent=2))
