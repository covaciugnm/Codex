from pathlib import Path
import sys,json,hashlib,importlib.util,types,base64
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
L=Path('D:/CodexWork/a10-r12-l03/dom');L.mkdir(exist_ok=False)
S=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A10_Instrumente_ramase_lot03/sources/proba_buton.py')
sp=importlib.util.spec_from_file_location('audit_original',S);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
png='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
def win(title,body='<h3>Heading</h3><h4>Fields</h4><div class="man-intro">Role</div>',style='',header=True,content=True):
 return f'<div class="z-window eva-aj-fereastra" style="{style}">'+(f'<div class="z-window-header">{title}</div>' if header else '')+(f'<div class="eva-ajutor-ecran">{body}</div>' if content else body)+'</div>'
cases=[
 ('zero','<p>No windows</p>',None),
 ('one',win('One'),'titlu=One'),
 ('two',win('First')+win('Second'),'last DOM visible=Second; no proof it belongs to current button'),
 ('hidden_window',win('First')+win('Hidden',style='display:none'),'First'),
 ('no_content',win('One',content=False),{'fara_continut':True}),
 ('hidden_h3',win('One','<h3 style="display:none">Hidden heading</h3><h3>Visible heading</h3>'),'hidden heading must not count as displayed; record observed'),
 ('hidden_row',win('One','<table><tr style="display:none"><th>1</th><th>Hidden field</th><td>Value</td></tr></table>'),'visible rows=0 independently; component counts DOM structure'),
 ('header_absent',win('One',header=False),'empty title'),
 ('selectors_absent','<div class="other">Other</div>',None),
 ('image_ok',win('One',f'<img class="eva-aj-img" src="{png}" style="width:100px;height:100px">'),'naturalWidth=1, img_ok=true'),
 ('image_bad',win('One','<img class="eva-aj-img" src="data:image/png;base64,AAAA">'),'img=true, img_ok=false'),
 ('zone_outside',win('One',f'<img class="eva-aj-img" src="{png}" style="width:100px;height:100px"><div class="eva-aj-zona" style="position:absolute;left:300px;top:300px"><b class="eva-aj-nr">1</b></div>'),'afara=1'),
 ('stack_order',win('Front','<h3>Front</h3>',style='position:absolute;z-index:999')+win('Back','<h3>Back</h3>',style='position:absolute;z-index:1'),'component chooses Back by DOM order; independent topmost at point is Front'),
]
results=[];requests=[];blocked=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--disable-background-networking','--disable-component-update','--no-first-run'])
 c=b.new_context(viewport={'width':900,'height':700},service_workers='block')
 def route(r):blocked.append(r.request.url);r.abort()
 c.route('http://**/*',route);c.route('https://**/*',route)
 pg=c.new_page();pg.on('request',lambda r:requests.append(r.url))
 for name,body,oracle in cases:
  html='<!doctype html><html><meta charset="utf-8"><style>body{font:16px Arial}.z-window{padding:12px;background:#eee;margin:10px;width:500px}.eva-ajutor-ecran{position:relative;min-height:120px}</style><body>'+body+'</body></html>'
  (L/(name+'.html')).write_text(html,encoding='utf-8');pg.set_content(html,wait_until='load')
  val=pg.evaluate(m.JS_FEREASTRA,['.z-window.eva-aj-fereastra','.eva-ajutor-ecran'])
  independent=pg.evaluate("() => ({visibleHeadings:[...document.querySelectorAll('h3')].filter(e=>e.offsetParent!==null).map(e=>e.innerText),visibleFieldRows:[...document.querySelectorAll('tr')].filter(e=>e.offsetParent!==null).length,topmost:document.elementFromPoint(40,40)?.closest('.z-window')?.querySelector('.z-window-header')?.innerText||null})")
  results.append({'id':'I17_DOM_'+name,'method':'ORIGINAL_JS_SYNTHETIC_DOM','oracle':oracle,'observed':val,'independent':independent})
  if name in ('hidden_row','stack_order','image_ok'):pg.screenshot(path=str(L/(name+'.png')))
 for name,html,oracle in [
  ('one_panel','<div class="z-tab-selected">Screen</div><div class="z-tabpanel desktop-tabpanel" style="height:250px"><button>Help</button></div>','[data-t240-panou]'),
  ('home_only','<div class="z-tab-selected desktop-hometab">Home</div><div class="z-tabpanel desktop-tabpanel" style="height:250px"><button>Help</button></div>',None),
  ('two_panels','<div class="z-tab-selected">Screen</div>'+2*'<div class="z-tabpanel desktop-tabpanel" style="height:250px"><button>Help</button></div>',None),
  ('nested_selected_only','<div class="z-tabpanel desktop-tabpanel" style="height:250px"><div class="z-tab-selected">Nested</div><button>Help</button></div>',None),
  ('old_marker_removed','<div data-t240-panou="1">Old</div>',None),
 ]:
  (L/(name+'.html')).write_text(html,encoding='utf-8');pg.set_content(html);obj=m.Proba.__new__(m.Proba);obj.c=types.SimpleNamespace(pg=pg)
  val=obj.panou();results.append({'id':'I17_DOM_'+name,'method':'ORIGINAL_PANOU_SYNTHETIC_DOM','oracle':oracle,'observed':val,'pass_component':val==oracle,'markers':pg.locator('[data-t240-panou]').count()})
 c.close();b.close()
put(L/'Results.json',results);put(L/'Boundaries.json',{'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'original_js_sha256':hashlib.sha256(m.JS_FEREASTRA.encode()).hexdigest(),'constructor':False,'Clona_login_DB_ZK':False,'browser':'Chrome headless dedicated new context','http_requests_observed':[u for u in requests if u.startswith(('http:','https:'))],'blocked':blocked,'contexts_closed':True,'cases':len(results),'initializations_bypassed':['Proba.__init__','captureaza_ecrane.py','CE.Clona','CE.Captura','MC masking','SQL','login','language save','E inventory traversal']})
print(json.dumps({'cases':len(results),'http_requests':len([u for u in requests if u.startswith(('http:','https:'))])}))
