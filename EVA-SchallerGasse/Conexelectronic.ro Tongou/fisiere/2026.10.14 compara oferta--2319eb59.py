from pathlib import Path
import json,requests,time,re,concurrent.futures
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
R=Path.cwd();C=R/'04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic';O=C/'2026.10.14 Comparatie oferta si stoc';O.mkdir(exist_ok=True)
P=json.loads((C/'2026.10.08 Catalog comparativ/Date structurate/2026.10.08 produse-normalizate.json').read_text('utf8'))
def get(p):
 out={'sku':p['sku'],'url':p['source'],'data':'2026.10.14','name':p['name']}
 try:
  for delay in [2,5,10]:
   r=requests.get(p['source'],timeout=30)
   if r.status_code!=429:break
   time.sleep(delay)
  r.raise_for_status();s=BeautifulSoup(r.text,'html.parser');(O/f"2026.10.14 Produs {p['sku']}.html").write_text(r.text,encoding='utf8')
  objs=[]
  for sc in s.find_all('script',type='application/ld+json'):
   x=json.loads(sc.string);objs.extend(x if isinstance(x,list) else [x])
  product=next(x for x in objs if x.get('@type')=='Product');assert str(product['sku'])==p['sku']
  stock=s.select_one('.product-summary__info--stock .info-value')
  out.update(product=product,stock_text=stock.get_text(' ',strip=True) if stock else None,status='Verificat live')
 except Exception as e:out.update(status='Neverificat live',error=str(e))
 return out
cache=O/'2026.10.14 Date actuale.json'
result=json.loads(cache.read_text('utf8')) if cache.exists() else []
done={x['sku'] for x in result if x['status']=='Verificat live'}
result=[x for x in result if x['sku'] in done]
for p in P:
 if p['sku'] in ['43067','43068','43079','43081'] and p['sku'] not in done:
  time.sleep(12);result.append(get(p))
(O/'2026.10.14 Date actuale.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
for r in result: print(json.dumps(r,ensure_ascii=False))
