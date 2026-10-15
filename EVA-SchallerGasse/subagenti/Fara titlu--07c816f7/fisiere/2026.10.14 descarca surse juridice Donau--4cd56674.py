from pathlib import Path
import urllib.request,json,hashlib,concurrent.futures,fitz
from bs4 import BeautifulSoup
base=Path.cwd(); out=base/'05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau/Surse';out.mkdir(parents=True,exist_ok=True)
old=json.loads((base/'08. Corespondenta/2026.10.07 Analiza juridica Donau auditata/2026.10.07 Registru surse redactor.json').read_text(encoding='utf-8'))['sources']
sources=[x for x in old if x['id'].startswith('J')]
sources += [{'id':'J11','descriere':'OGH7Ob9525h acces somatie','url':'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_20250925_OGH0002_0070OB00095_25H0000_000/JJT_20250925_OGH0002_0070OB00095_25H0000_000.pdf'}, {'id':'J12','descriere':'OGH7Ob5807s rate nu automat amanare','url':'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_20070418_OGH0002_0070OB00058_07S0000_000/JJT_20070418_OGH0002_0070OB00058_07S0000_000.pdf'}, {'id':'J13','descriere':'OGH7Ob6901z distinctie1lunaFeuer','url':'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_20010427_OGH0002_0070OB00069_01Z0000_000/JJT_20010427_OGH0002_0070OB00069_01Z0000_000.pdf'}, {'id':'L02','descriere':'WEG28','url':'https://www.ris.bka.gv.at/eli/bgbl/i/2002/70/P28/NOR40240616'}]
sources += [{'id':'L01','descriere':'VersVG consolidat actual14oct2026','url':'https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001979'}, {'id':'C01','descriere':'DONAU1000A ABS2018 public','url':'https://www.donauversicherung.at/fileadmin/03_service/rechtliches-compliance/klauseln-bedingungen/sach-unfall/1000A_-_ALLGEMEINE_BEDINGUNGEN_FUER_DIE_SACHVERSICHERUNG__ABS___FASSUNG_2018_.pdf'}, {'id':'J10','descriere':'OGH3Ob72254','url':'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_19541117_OGH0002_0030OB00722_5400000_000/JJT_19541117_OGH0002_0030OB00722_5400000_000.pdf'}]
sources += [
 {'id':'J14','descriere':'OGH 3 Ob 16/25m 2025.05.28 plata cu rezerva si restituire','url':'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_20250528_OGH0002_0030OB00016_25M0000_000/JJT_20250528_OGH0002_0030OB00016_25M0000_000.pdf'},
 {'id':'L03','descriere':'VersVG 5c forma 2022 aplicabila contractelor din februarie2026','url':'https://ris.bka.gv.at/eli/bgbl/1959/2/P5c/NOR40244230'},
 {'id':'J15','descriere':'OGH 1Ob669/50 incapacitate proprie asigurator distincta de39','url':'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_19501206_OGH0002_0010OB00669_5000000_000/JJT_19501206_OGH0002_0010OB00669_5000000_000.html'}
]
def fetch(x):
 try:
  prev=out/'2026.10.14 Registru surse web cercetare.json'
  if prev.exists():
   found=next((a for a in json.loads(prev.read_text(encoding='utf-8')) if a['id']==x['id'] and a['status']=='salvat'),None)
   if found:return found
  req=urllib.request.Request(x['url'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=40) as r: raw=r.read(); ctype=r.headers.get('Content-Type',''); url=r.url
  ext='.pdf' if raw.startswith(b'%PDF') else '.html'
  p=out/f"2026.10.14 {x['id']} sursa oficiala{ext}";p.write_bytes(raw)
  if ext=='.pdf':
   d=fitz.open(p);txt='\n\n'.join(f'--- PDF PAGINA {i+1} ---\n'+page.get_text() for i,page in enumerate(d))
  else:
   soup=BeautifulSoup(raw,'html.parser')
   for tag in soup(['script','style']):tag.decompose()
   txt=soup.get_text('\n',strip=True)
  p.with_suffix('.txt').write_text(txt,encoding='utf-8')
  return {**x,'consultat':'2026.10.14','status':'salvat','path':str(p),'url_final':url,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 except Exception as e:return {**x,'consultat':'2026.10.14','status':'eroare','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: results=list(ex.map(fetch,sources))
(out/'2026.10.14 Registru surse web cercetare.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'id':x['id'],'status':x['status'],'bytes':x.get('bytes'),'error':x.get('error')} for x in results],ensure_ascii=False))
