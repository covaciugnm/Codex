from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import subprocess
import sys
from urllib.parse import urlparse

sys.dont_write_bytecode = True
sys.path.insert(0, 'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright

root = Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
repo = Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
out = root/'executie/R11_fisiere/Triaj_fixture_UI_Val03'
out.mkdir(exist_ok=True)
target = out/'Proba_help_browser.json'
assert not target.exists()
manifest = json.loads((root/'executie/R11_fisiere/Suite_originale_config_sintetice_v12/Surse_izolate_Git.json').read_text(encoding='utf8'))
by_file = {row['file']: row for row in manifest['rows']}
sources = []
exact = out/'Surse_Git'
for name in ['frontend/tests/test_help_coverage.py','frontend/app.py','frontend/static/eva-help.js','frontend/static/eva-help-kb.json','frontend/static/eva-help.css']:
    data = (repo/name).read_bytes()
    expected = by_file[name]
    if hashlib.sha256(data).hexdigest() != expected['sha256']:
        data = subprocess.check_output(['git','-C','D:/CodexWork/eva-audit-p01-src-20261101','cat-file','blob',expected['git_blob']])
    assert hashlib.sha256(data).hexdigest() == expected['sha256']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == expected['git_blob']
    sources.append(expected)
    copy = exact/name
    copy.parent.mkdir(parents=True,exist_ok=True)
    copy.write_bytes(data)

spec = importlib.util.spec_from_file_location('help_original', exact/'frontend/tests/test_help_coverage.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
kb = module._load_kb()
routes = module._rendered_page_keys()
missing = {route:key for route,key in routes.items() if key not in kb}
assert missing
script = (exact/'frontend/static/eva-help.js').read_text(encoding='utf8')
css = (exact/'frontend/static/eva-help.css').read_text(encoding='utf8')
normal = next((route,key) for route,key in routes.items() if key in kb and kb[key].get('title') != kb['page:/app/default'].get('title'))
results = []
requests = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', args=['--disable-background-networking','--disable-extensions'])
    try:
        for route,key in [normal,*missing.items()]:
            context = browser.new_context(viewport={'width':1280,'height':800}, service_workers='block')
            page = context.new_page()
            errors = []
            page.on('pageerror',lambda error:errors.append(str(error)))
            def intercept(request_route):
                request = request_route.request
                url = urlparse(request.url)
                requests.append({'host':url.hostname,'path':url.path,'method':request.method})
                if url.hostname != 'audit.example.invalid':
                    request_route.abort()
                elif url.path == '/static/eva-help.js':
                    request_route.fulfill(content_type='application/javascript',body=script)
                elif url.path == '/static/eva-help-kb.json':
                    request_route.fulfill(content_type='application/json',body=json.dumps(kb,ensure_ascii=False))
                elif url.path == '/app/api/eva/preferences/help':
                    request_route.fulfill(content_type='application/json',body='{"enabled":true}')
                elif url.path == route:
                    request_route.fulfill(content_type='text/html',body='<!doctype html><html lang="ro"><head><meta charset="utf-8"><style>'+css+'</style><script src="/static/eva-help.js" defer></script></head><body><h1>Fixture pentru ajutor contextual</h1><button data-eva-page-help>Ajutor pagină</button><button>Control sintetic</button></body></html>')
                else:
                    request_route.abort()
            context.route('**/*',intercept)
            page.goto('https://audit.example.invalid'+route)
            page.locator('[data-eva-page-help]').click()
            page.locator('#eva-help-panel').wait_for(state='visible')
            title = page.locator('#eva-help-panel-title').inner_text()
            body = page.locator('#eva-help-panel-body').inner_text()
            expected_entry = kb.get(key) or kb['page:/app/default']
            assert title == expected_entry['title'], (route,title,expected_entry['title'])
            assert not errors
            results.append({'route':route,'requested_key':key,'dedicated_entry':key in kb,'title_visible':title,'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'fallback_used':key not in kb,'browser_errors':errors})
            if route == next(iter(missing)):
                page.screenshot(path=str(out/'Help_fallback_browser.png'))
            context.close()
    finally:
        browser.close()

result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':manifest['head'],'sources':sources,'missing_dedicated_help':missing,'controls':results,'requests':requests,'expected':'O pagină documentată primește articolul propriu; o pagină absentă primește fallbackul general existent.','result':'Lipsă de documentație contextuală specifică, fără dispariția totală a ajutorului.','limits':['DOM-ul gazdă este o fixture; s-a executat JS-ul original și KB-ul original, nu întregul frontend/backend de producție.','Toate cererile browserului au fost interceptate; nicio API operațională accesată.','Nu verifică accesul nativ iDempiere sau persistența DB.'],'cleanup':{'browser_closed':True,'ephemeral_contexts_closed':True,'listening_service_created':False}}
target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'routes':len(routes),'missing':missing,'controls':len(results),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},ensure_ascii=False))
