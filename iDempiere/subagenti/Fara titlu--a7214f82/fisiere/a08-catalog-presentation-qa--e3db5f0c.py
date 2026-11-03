from pathlib import Path
import sys,json,hashlib,datetime
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A08_Storefront_catalog_lot04')
f=O/'Raport_A08_catalog_lot04_v1.html';Q=O/'QA_presentation_v1';Q.mkdir(exist_ok=False)
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  for k in ['href','src']:
   if d.get(k):self.urls.append(d[k])
p=Links();p.feed(f.read_text(encoding='utf-8'));bad=[u for u in p.urls if not urlsplit(u).scheme and not (f.parent/unquote(urlsplit(u).path)).is_file()]
views=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',args=['--disable-background-networking','--disable-extensions'])
 try:
  for width in [1366,390]:
   page=b.new_page(viewport={'width':width,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('http://**',lambda r:r.abort());page.route('https://**',lambda r:r.abort())
   page.goto(f.as_uri(),wait_until='load')
   data=page.evaluate('({viewport:innerWidth,scroll:document.documentElement.scrollWidth,title:document.querySelector("h1").textContent,brokenImages:Array.from(document.images).filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src)})')
   page.screenshot(path=str(Q/f'top_{width}.png'));page.locator('h2').filter(has_text='Cazuri și rezultate').scroll_into_view_if_needed();page.screenshot(path=str(Q/f'cases_{width}.png'))
   views.append({'width':width,'data':data,'errors':errors});page.close()
 finally:b.close()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Document presentation only; no product retest, no remote requests.','html_sha256':sha(f),'links':len(p.urls),'bad_links':bad,'views':views,'passed':not bad and all(v['data']['viewport']==v['data']['scroll'] and not v['data']['brokenImages'] and not v['errors'] for v in views),'browser_closed':not b.is_connected()}
(Q/'QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['a08-catalog-presentation-qa.py','a08-storefront-catalog-package-l04.py']:(Q/name).write_bytes((Path('D:/CodexWork')/name).read_bytes())
(Q/'MANIFEST_QA.json').write_text(json.dumps({'files':[{'path':p.relative_to(O).as_posix(),'sha256':sha(p)} for p in sorted(Q.iterdir()) if p.is_file()]},indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
