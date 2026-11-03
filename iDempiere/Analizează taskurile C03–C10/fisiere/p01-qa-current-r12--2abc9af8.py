from pathlib import Path
import sys,json,hashlib,datetime,collections
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
P=R/'executie/R12_plan_delta'
plan=sorted(P.glob('Plan_delta_R12_v*.html'))[-1]
annex=sorted(P.glob('Plan_instrumente_noi_A10_v*.html'))[-1]
files=[R/'Raport_audit.html',R/'Audit_C03.html',R/'Audit_C10.html',plan,annex]
O=R/'executie/Publicare_Val04_R12'/datetime.datetime.now(datetime.timezone.utc).strftime('QA_%Y-%m-%dT%H-%M-%SZ')
O.mkdir(parents=True,exist_ok=False)
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and d.get('href'):self.links.append(d['href'])
  if 'id' in d:self.ids.append(d['id'])
links=[]
for f in files:
 p=Parser();p.feed(f.read_text(encoding='utf-8-sig'));bad=[]
 for l in p.links:
  v=urlsplit(l)
  if v.scheme:continue
  if v.path and not (f.parent/unquote(v.path)).is_file():bad.append(l)
  if not v.path and v.fragment and v.fragment not in p.ids:bad.append(l)
 links.append({'file':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'count':len(p.links),'bad':bad,'duplicate_ids':[i for i,n in collections.Counter(p.ids).items() if n>1]})
views=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',args=['--disable-background-networking','--disable-extensions'])
 for f in files:
  for width,height in [(1366,900),(390,844)]:
   page=b.new_page(viewport={'width':width,'height':height});errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('http://**',lambda route:route.abort());page.route('https://**',lambda route:route.abort())
   page.goto(f.as_uri(),wait_until='domcontentloaded',timeout=40000)
   layout=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,h1:document.querySelector("h1")?.textContent})')
   if f.name in ['Audit_C03.html','Audit_C10.html']:
    page.locator('#q').fill('T354' if f.name=='Audit_C03.html' else 'T352');assert page.locator('details.task:visible').count()==1
    page.locator('details.task:visible>summary').click();assert page.locator('details.task:visible .crit').count()>0
   if f.name=='Raport_audit.html':page.locator('#r12-lot01' if page.locator('#r12-lot01').count() else '#r11-val04').scroll_into_view_if_needed()
   if f.name in ['Raport_audit.html',plan.name,annex.name]:
    page.screenshot(path=str(O/(f.stem+'_'+str(width)+'.png')))
   views.append({'file':f.relative_to(R).as_posix(),'viewport':[width,height],'layout':layout,'errors':errors})
   page.close()
 b.close()
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'QA a documentelor autorate, fără execuție de cod produs R12; rețea HTTP(S) refuzată în pagini.','links':links,'views':views,'passed':all(not x['bad'] and not x['duplicate_ids'] for x in links) and all(not x['errors'] and x['layout']['width']==x['layout']['scroll'] for x in views),'screenshots':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in O.glob('*.png')]}
(O/'QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'path':str(O),'passed':report['passed'],'links':[(x['file'],len(x['bad'])) for x in links],'views':[(x['file'],x['viewport'][0],x['layout']['scroll']) for x in views]},ensure_ascii=False))
