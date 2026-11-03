from pathlib import Path
import sys,json,hashlib,datetime,traceback
from urllib.parse import urlsplit,parse_qs
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright

R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A08_Storefront_catalog_lot04'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
protocol=json.loads((O/'Protocol_A08_catalog_v1.json').read_text(encoding='utf-8'))
assert sha(O/'Protocol_A08_catalog_v1.json')=='f04a2c9de4abe00b7bbf541e0526e71a89196d2a8ca2f74bb79fb1a9dd99c688'
# The concrete A11 receipt is supplied only after approval; no browser launches without it.
assert len(sys.argv)==3,'Usage: harness <A11 concrete gate path> <gate SHA-256>'
gate=Path(sys.argv[1]);assert sha(gate)==sys.argv[2]
assert 'A11' in str(gate) and gate.is_file()
src=O/'Sources/idempiere/plugins/com.eva.ro.webshop/resources/static/themes/storefront.js'
assert sha(src)=='5c7af41dff422695aa0970e28ab00fa978c47bd974dc47071197b71b42e50e9f'
assert src.read_bytes()==(O/'Sources/frontend/storefront/static/themes/storefront.js').read_bytes()
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
RUN=O/('Run_'+stamp);RUN.mkdir(exist_ok=False)
(RUN/'Harness.py').write_bytes(Path(__file__).read_bytes())
fixture='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Laborator sintetic catalog</title>
<style>body{font:17px Arial;padding:24px;max-width:1000px;margin:auto;color:#17253c}h1{font-size:22px}.notice{background:#eef3f9;padding:14px}a,button{margin-right:18px;padding:8px}.category-tree{margin:22px 0}.is-active{background:#d6e9ff}.product-card{border:1px solid #9cacbc;padding:14px;margin:10px 0;max-width:650px}.product-actions{display:none}.featured-zone{padding:6px;color:#53657a}.category-empty{background:#fff0d5;padding:14px}input{padding:8px}button{cursor:pointer}</style>
<body data-tenant="audit-synthetic" data-lang="ro" data-theme="marketplace_pro" data-currency="RON">
<h1>Probă A08 — DOM sintetic; script original</h1><p class="notice">Date fictive. Nu este site-ul operațional și nu este o probă de design.</p>
<form data-product-search><label>Căutare <input name="q" autocomplete="off"></label><button type="submit">Caută</button></form>
<nav class="category-tree"><a href="#category-A" data-category="Categoria A" data-category-id="A">Categoria A</a><a href="#category-B" data-category="Categoria B" data-category-id="B">Categoria B</a><a href="#category-C" data-category="Categoria C" data-category-id="C">Categoria C</a></nav>
<div class="featured-zone">Selecție inițială</div><section class="products-zone"><div class="section-head"><h2>Toate produsele</h2><p data-results-summary data-results-label="Rezultate">Rezultate: 1</p></div>
<form data-catalog-filters><select name="sort" data-sort-control><option value="relevance">Relevanță</option><option value="price_asc">Preț</option></select><input name="min_price"><input name="max_price"><input name="in_stock" type="checkbox" value="1"><select name="material"><option value="">Oricare</option></select><select name="color"><option value="">Oricare</option></select><select name="finish"><option value="">Oricare</option></select><select name="capacity"><option value="">Oricare</option></select><button type="submit">Filtrează</button></form>
<p data-category-empty hidden></p><div data-product-grid><article data-product-card data-product-id="SEED" data-product-name="Produs inițial" data-product-price-ron="10">Produs inițial SEED</article></div><button type="button" data-load-more>Încarcă mai multe</button></section>
<div hidden data-commerce-panel data-search-empty="Niciun produs găsit pentru căutare" data-no-category-products="Niciun produs în această categorie" data-all-products="Toate produsele" data-stock-in-label="În stoc" data-stock-out-label="Indisponibil" data-stock-map-label="Date sintetice"></div>
</body></html>'''
(RUN/'Fixture.html').write_text(fixture,encoding='utf-8')

def product(pid):return {'id':pid,'name':'Produs '+pid,'slug':pid.lower(),'price':10,'images':[],'category_ids':[pid.split('-')[0]],'categories':[],'is_in_stock':True}
def payload(pid,more=True):return {'items':[product(pid)],'total':10,'has_more':more}
def spec(body=None,status=200,mode='json',hold=False):return {'body':body,'status':status,'mode':mode,'hold':hold}
def snapshot(page,label):
 d=page.evaluate('''() => ({title:document.querySelector('.products-zone h2').textContent, query:document.querySelector('input[name=q]').value, active:Array.from(document.querySelectorAll('.category-tree .is-active')).map(x=>x.dataset.categoryId), cardIds:Array.from(document.querySelectorAll('[data-product-card]')).map(x=>x.dataset.productId), cardNames:Array.from(document.querySelectorAll('[data-product-card]')).map(x=>x.dataset.productName), summary:document.querySelector('[data-results-summary]').textContent, emptyHidden:document.querySelector('[data-category-empty]').hidden, emptyText:document.querySelector('[data-category-empty]').textContent, loadMoreHidden:document.querySelector('[data-load-more]').hidden, localStorageKeys:Object.keys(localStorage), hash:location.hash, grid:document.querySelector('[data-product-grid]').innerHTML})''')
 d['label']=label;d['grid_sha256']=hashlib.sha256(d.pop('grid').encode()).hexdigest();return d

results=[];browser_closed=False;contexts_created=0;contexts_closed=0
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',args=['--disable-background-networking','--disable-extensions','--disable-component-update','--no-first-run'])
 try:
  browser_version=b.version
  for meta in protocol['cases']:
   cid=meta['id'];d=RUN/cid;d.mkdir()
   context=b.new_context(viewport={'width':1200,'height':900},service_workers='block');contexts_created+=1
   page=context.new_page();page.set_default_timeout(5000)
   req=[];blocked=[];pending=[];errors=[];snapshots=[];screen=[];configured=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   def deliver(route,s,record):
    record['delivered']=True
    if s['mode']=='abort':route.abort('failed');return
    body=json.dumps(s['body'],ensure_ascii=False) if s['mode']=='json' else s['body']
    route.fulfill(status=s['status'],content_type='application/json; charset=utf-8',body=body)
   def route_handler(route):
    u=urlsplit(route.request.url)
    if u.hostname=='audit.invalid' and u.path=='/' and route.request.method=='GET':route.fulfill(status=200,content_type='text/html; charset=utf-8',body=fixture);return
    if u.hostname=='audit.invalid' and u.path=='/api/catalog/products' and route.request.method=='GET':
     n=len(req);s=configured[n] if n<len(configured) else spec(payload('UNEXPECTED'))
     record={'ordinal':n+1,'method':route.request.method,'url':route.request.url,'params':parse_qs(u.query),'response_spec':s,'delivered':False};req.append(record)
     if s['hold']:pending.append((route,s,record))
     else:deliver(route,s,record)
     return
    blocked.append({'url':route.request.url,'method':route.request.method});route.abort('blockedbyclient')
   page.route('**/*',route_handler)
   def pause():page.wait_for_timeout(100)
   def take(label,screenshot=False):
    pause();snapshots.append(snapshot(page,label))
    if screenshot:
     fp=d/(label+'.png');page.screenshot(path=str(fp),full_page=True);screen.append(fp.relative_to(O).as_posix())
    return snapshots[-1]
   def clickcat(cat):page.locator('[data-category-id="'+cat+'"]').click();pause()
   def search(q):
    # Fixture preparation of control value only. Real Enter invokes the original submit listener.
    # Deliberately excludes the separate 280ms input-debounce path from this bounded protocol.
    page.locator('input[name="q"]').evaluate('(el,v)=>{el.value=v}',q);page.locator('input[name="q"]').press('Enter');pause()
   def release():
    assert len(pending)==1,('pending-route-count',len(pending))
    route,s,record=pending.pop(0);deliver(route,s,record);pause()
   try:
    page.goto('https://audit.invalid/',wait_until='domcontentloaded')
    assert not page.evaluate('Object.keys(localStorage).length')
    script=page.add_script_tag(content=src.read_text(encoding='utf-8'))
    assert hashlib.sha256(script.text_content().encode('utf-8')).hexdigest()==sha(src)
    take('initial');assert len(req)==0
    if cid=='S01':
     configured=[spec(payload('PAGE2')),spec(payload('PAGE3'))]
     page.locator('[data-load-more]').click();take('page2')
     page.locator('[data-load-more]').click();s=take('page3',True)
     ok=len(req)==2 and [r['params'].get('page') for r in req]==[['2'],['3']] and s['cardIds']==['SEED','PAGE2','PAGE3']
    elif cid=='S02':
     configured=[spec(payload('A')),spec(payload('B'))]
     clickcat('A');a=take('categoryA');clickcat('B');s=take('categoryB')
     ok=len(req)==2 and a['cardIds']==['A'] and s['cardIds']==['B'] and s['title']=='Categoria B' and all(r['params']['page']==['1'] for r in req) and [r['params'].get('category_id') for r in req]==[['A'],['B']]
    elif cid=='S03':
     configured=[spec({'items':[],'total':0,'has_more':False}),spec(payload('FOUND'))]
     search('EMPTY');empty=take('valid_empty');search('FOUND');s=take('recovered')
     ok=not empty['cardIds'] and not empty['emptyHidden'] and empty['loadMoreHidden'] and len(req)==2 and s['cardIds']==['FOUND'] and s['emptyHidden']
    elif cid=='S04':
     configured=[spec(payload('ONCE'),hold=True)]
     page.locator('[data-load-more]').click();pause();assert len(pending)==1
     page.locator('[data-load-more]').click();take('second_click_pending');release();s=take('single_response')
     ok=len(req)==1 and s['cardIds']==['SEED','ONCE']
    elif cid in ['N01','N02']:
     configured=[spec(mode='abort') if cid=='N01' else spec('{broken-json',mode='text'),spec(payload('B'))]
     page.locator('[data-load-more]').click();page.wait_for_timeout(250);fail=take('after_error')
     clickcat('B');s=take('retry_categoryB',True)
     ok=len(req)==2 and s['cardIds']==['B']
    elif cid=='N03':
     configured=[spec({'error':'synthetic'},status=500),spec(payload('B'))]
     clickcat('A');fail=take('http500_as_displayed',True);clickcat('B');s=take('retry_success')
     # Error must not be indistinguishable from an ordinary successful empty-category result.
     masquerades=not fail['cardIds'] and fail['summary']=='Rezultate: 0' and not fail['emptyHidden'] and fail['emptyText']=='Niciun produs în această categorie'
     ok=not masquerades and len(req)==2 and s['cardIds']==['B']
    elif cid in ['N04','S05']:
     configured=[spec(payload('A'),hold=True),spec(payload('C'))]
     clickcat('A');assert len(pending)==1;clickcat('B');take('B_selected_while_A_pending');release();stale=take('A_response_under_B_title',True)
     if cid=='N04':ok=not (stale['active']==['B'] and stale['title']=='Categoria B' and stale['cardIds']==['A'])
     else:
      clickcat('C');s=take('C_after_completed_response');ok=len(req)==2 and s['active']==['C'] and s['cardIds']==['C'] and req[1]['params'].get('category_id')==['C']
    elif cid=='N05':
     configured=[spec(payload('QUERY-A'),hold=True)]
     search('QUERY-A');assert len(pending)==1;search('QUERY-B');take('queryB_while_A_pending');release();s=take('A_response_under_B_query',True)
     ok=not (s['query']=='QUERY-B' and s['title']=='QUERY-B' and s['cardIds']==['QUERY-A'])
    else:raise AssertionError(cid)
    result={**meta,'execution':'ORIGINAL_JS_ON_SYNTHETIC_DOM','oracle_met':ok,'status':'CONFORM_LIMITAT' if ok else 'CONTRAEXEMPLU_REPRODUS','requests':req,'blocked_nonfixture_requests':blocked,'page_errors':errors,'snapshots':snapshots,'screenshots':screen,'infrastructure_failure':None,'normal_route_limit':'Backend și template rendering neexecutate; script original, DOM sintetic și răspunsuri locale; fără efect persistent ERP.'}
   except Exception as e:
    result={**meta,'execution':'INCOMPLETE','status':'INFRASTRUCTURE_ATTEMPT_NOT_PRODUCT_VERDICT','infrastructure_failure':traceback.format_exc(),'requests':req,'blocked_nonfixture_requests':blocked,'page_errors':errors,'snapshots':snapshots,'screenshots':screen}
   finally:
    context.close();contexts_closed+=1
   (d/'Evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');results.append(result)
 finally:
  b.close();browser_closed=not b.is_connected()
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':RUN.relative_to(R).as_posix(),'head':protocol['head'],'gate':{'path':str(gate),'sha256':sha(gate)},'protocol_sha256':sha(O/'Protocol_A08_catalog_v1.json'),'script_oid':'b901bec7b36c35589c4040d82586f2681db9d7e0','script_sha256':sha(src),'script_path_identities':2,'executed_blobs':1,'script_modified':False,'browser_version':browser_version,'cases':results,'summary':{'planned':len(protocol['cases']),'completed':sum(x['execution']!='INCOMPLETE' for x in results),'conform_limited':sum(x.get('oracle_met') is True for x in results),'counterexamples':sum(x.get('oracle_met') is False for x in results),'infrastructure_attempts':sum(x['execution']=='INCOMPLETE' for x in results)},'resources':{'contexts_created':contexts_created,'contexts_closed':contexts_closed,'browser_closed':browser_closed,'persistent_service_created':False,'product_database_accessed':False,'existing_six_retained_roots_touched':False},'search_method':'Valoarea inputului pregătită în fixture, apoi Enter real/submit original; debounce input 280ms nu este probat.','acceptance':'Așteaptă verificarea A11; fără recepție de fișier/task/control integral.'}
(RUN/'Rezultate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
files=[{'path':p.relative_to(O).as_posix(),'sha256':sha(p)} for p in sorted(RUN.rglob('*')) if p.is_file()]
(RUN/'MANIFEST_RUN.json').write_text(json.dumps({'utc':report['utc'],'files':files,'summary':report['summary'],'resources':report['resources']},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'run':str(RUN),'summary':report['summary'],'resources':report['resources']},ensure_ascii=False))
