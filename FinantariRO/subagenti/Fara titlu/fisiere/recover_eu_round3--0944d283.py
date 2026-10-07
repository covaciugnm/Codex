from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests, json, hashlib, io
from bs4 import BeautifulSoup
from pypdf import PdfReader

out=Path('2.1 Legislatie si eligibilitate/Recuperari Runda3'); out.mkdir(parents=True,exist_ok=True)
items=[('Regulament2021_1057','32021R1057'),('Regulament2024_2509','32024R2509'),('Regulament2023_1676','32023R1676'),('Recomandare2022_C476_01','32022H1215(01)'),('Carta_drepturi_2016','12016P/TXT'),('Agenda_competente_COM2020_274','52020DC0274'),('Plan_educatie_digitala_COM2020_624','52020DC0624'),('Pact_verde_COM2019_640','52019DC0640')]
def run(item):
 name,celex=item; rec={'nume':name,'celex':celex,'incercari':[],'data':'2026-10-07','status':'NERECUPERAT'}
 urls=[f'https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:{celex}',f'https://eur-lex.europa.eu/legal-content/RO/TXT/PDF/?uri=CELEX:{celex}']
 if celex.startswith('520'):
  year=celex[1:5]; number=celex[-4:]; urls.append(f'https://www.europarl.europa.eu/RegData/docs_autres_institutions/commission_europeenne/com/{year}/{number}/COM_COM({year}){number}_RO.pdf')
 for url in urls:
  attempt={'url':url}
  try:
   r=requests.get(url,timeout=16,headers={'User-Agent':'Mozilla/5.0'}); raw=r.content;attempt.update(http=r.status_code,octeti=len(raw),tip=r.headers.get('Content-Type'))
   if r.status_code!=200 or len(raw)<1000: raise ValueError('Raspuns insuficient: cod HTTP sau corp gol/scurt')
   if raw.startswith(b'%PDF'):
    reader=PdfReader(io.BytesIO(raw)); text='\n\n'.join(f'=== PAGINA {i+1} ===\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages)); ext='.pdf';attempt['pagini']=len(reader.pages)
   else:
    r.encoding='utf-8';soup=BeautifulSoup(r.text,'html.parser'); text=soup.get_text('\n',strip=True);ext='.html'
   if len(text)<2500 or 'captcha' in text[:1000].lower() or 'challenge' in text[:1000].lower():raise ValueError('Text insuficient sau pagina anti-bot')
   path=out/(name+ext);path.write_bytes(raw); path.with_suffix(ext+'.txt').write_text(text,encoding='utf-8');rec.update(status='DESCARCAT_DE_VALIDAT',fisier=path.name,sha256=hashlib.sha256(raw).hexdigest(),octeti=len(raw),caractere_text=len(text),url_sursa=url,pagini=attempt.get('pagini'));rec['incercari'].append(attempt);break
  except Exception as e:attempt['eroare']=str(e)[:240]
  rec['incercari'].append(attempt)
 return rec
with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(run,items))
(out/'Registru_recuperare_Runda3.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for r in results:print(r['nume'],r['status'],r.get('octeti'),r.get('fisier'))
