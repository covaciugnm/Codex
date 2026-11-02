from pathlib import Path
import requests,json,hashlib
from bs4 import BeautifulSoup
r=Path('05. Asigurari/Asigurare cladire/2026.10.29 Renuntare componente Donau/Surse')
sources=[('VersVG actual','https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001979&FassungVom=2026-10-29'),('OGH 7 Ob 53 14s','https://www.ris.bka.gv.at/JustizEntscheidung.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20150218_OGH0002_0070OB00053_14S0000_000&IncludeSelf=True&ShowPrintPreview=True'),('OGH 7 Ob 178 24p','https://www.ris.bka.gv.at/JustizEntscheidung.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20241218_OGH0002_0070OB00178_24P0000_000&IncludeSelf=True&ShowPrintPreview=True')]
out=[]
for name,url in sources:
 q=requests.get(url,timeout=40);q.raise_for_status()
 p=r/('2026.10.29 '+name+'.html');p.write_bytes(q.content)
 text=BeautifulSoup(q.content,'html.parser').get_text('\n',strip=True)
 p.with_suffix('.txt').write_text(text,encoding='utf8')
 out.append({'name':name,'url':url,'bytes':len(q.content),'sha256':hashlib.sha256(q.content).hexdigest()})
(r/'2026.10.29 Registru surse primare.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=True))
