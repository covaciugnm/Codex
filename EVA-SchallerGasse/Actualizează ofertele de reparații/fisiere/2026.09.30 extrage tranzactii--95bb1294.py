from pathlib import Path
import re,json,decimal,fitz,collections
R=Path(__file__).resolve().parent.parent;D=R/'10. Banci + Extrase de cont'/'2026.09.30 Audit facturi si plati'
def value(s):return decimal.Decimal(s.replace('.','').replace(',','.'))
def date(s):return '.'.join(s.split('.')[::-1])
tx=[];checks=[]
for p in (R/'10. Banci + Extrase de cont').glob('Extrase*/*.pdf'):
 account='A&C AT22' if 'AT22' in p.name else 'Cosmin AT13';short='AT22' if 'AT22' in p.name else 'AT13';doc=fitz.open(p);current=None;subtotal={}
 for pg,page in enumerate(doc,1):
  lines=page.get_text(sort=True).splitlines()
  for line in lines:
   if 'Logged in as:' in line:continue
   m=re.match(r'^\s*(\d{2}\.\d{2}\.\d{4})\s+(.*?)\s+(\d{2}\.\d{2}\.\d{4})\s+(-?[\d.]+,\d{2}) EUR\s*$',line)
   if m:
    current={'id_intern':short+'-'+str(sum(x['cont']==account for x in tx)+1).zfill(3),'cont':account,'data_platii':date(m[1]),'data_valutei':date(m[3]),'suma_eur':str(value(m[4])),'text_banca':m[2].strip(),'sursa':p.relative_to(R).as_posix(),'pagina':pg,'numar_plata_banca':'','referinta_banca':'','document_asociat':'','data_document':'','tip':'de clasificat'};tx.append(current)
   elif re.match(r'^\s*\d{2}\.\d{2}\.\d{4}',line):current=None
   elif 'Sum of credit entries' in line or 'Sum of debit entries' in line:
    subtotal['credit' if 'credit' in line else 'debit']=str(value(re.search(r'(-?[\d.]+,\d{2}) EUR',line)[1]));current=None
   elif current and line.strip() and not any(s in line for s in ['Booking date','Booking text','Value date','Logged in as:','page ']):
    current['text_banca']+=' '+line.strip()
 totals={k:sum(decimal.Decimal(x['suma_eur']) for x in tx if x['cont']==account and ((decimal.Decimal(x['suma_eur'])>0)==(k=='credit'))) for k in ['credit','debit']}
 checks.append({'cont':account,'tranzactii':sum(x['cont']==account for x in tx),'pdf':subtotal,'calculat':{k:str(v) for k,v in totals.items()},'egal':all(totals[k]==decimal.Decimal(subtotal[k]) for k in subtotal)})
 # Render each page for source validation.
 for pg,page in enumerate(doc,1):page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(str(D/f'2026.09.30 Verificare {short} pagina {pg}.png'))
(D/'2026.09.30 Tranzactii extrase.json').write_text(json.dumps(tx,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'2026.09.30 Control totaluri extrase.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
for t in tx:print(t['id_intern'],t['data_platii'],t['suma_eur'],t['text_banca'])
