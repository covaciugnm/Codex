from a12_r3_survey import *
import subprocess as sp,socket,time,sys,datetime
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
out=E/'R4/T259_ZK';out.mkdir(parents=True,exist_ok=True);role=sys.argv[1]if len(sys.argv)>1 else 'GardenAdmin';server='saga-server@192.168.100.151'
src="""import pathlib,json,ipaddress,subprocess
w=pathlib.Path('/tmp/eva-contab-codex-p01cross-r2.VzMxY8xx');pg=(w/'auditor-pg').read_text().strip();app=(w/'auditor-app').read_text().strip();ip=(w/'ip').read_text().strip();assert ip.startswith('10.250.') and ipaddress.ip_address(ip).is_private
def dk(*a,inp=None):return subprocess.check_output(['docker',*a],input=inp)
for name in (pg,app):
 l=json.loads(dk('inspect','--format','{{json .Config.Labels}}',name));assert l['eva.sesiune']=='eva-contab-codex-p01crossr2' and l['eva.task']=='P01.T220'
sql="BEGIN READ ONLY;SET LOCAL search_path=adempiere,public;SELECT row_to_json(q) FROM (SELECT m.ad_menu_id,m.name,m.action,m.ad_form_id,f.classname,(select array_agg(ad_role_id order by ad_role_id) from ad_form_access a where a.ad_form_id=f.ad_form_id and a.isactive='Y') roles,(select count(*) from ad_treenodemm t where t.node_id=m.ad_menu_id) nodes FROM ad_menu m JOIN ad_form f ON f.ad_form_id=m.ad_form_id WHERE f.classname LIKE '%WSagaContracteForm' and m.isactive='Y')q; SELECT row_to_json(q) FROM (select name,coalesce(description,'') description from c_projecttype where ad_client_id in (0,11) and isactive='Y' order by name)q;ROLLBACK;"
res=dk('exec','-i',pg,'psql','-qXAt','-v','ON_ERROR_STOP=1','-U','postgres','-d','idempiere',inp=sql.encode()); print(json.dumps(dict(ip=ip,rows=[json.loads(l)for l in res.splitlines()if l.startswith(b'{')],jar=dk('exec',app,'sha256sum','/opt/idempiere/plugins/com.eva.ro.contab_13.0.0.jar').decode().split()[0])))
"""
meta=json.loads(sp.check_output(['ssh','-o','BatchMode=yes',server,'python3 -'],input=src.encode(),timeout=30));ip=meta.pop('ip');wr(out/'AD_si_tipuri.json',meta);s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
t=sp.Popen(['ssh','-o','BatchMode=yes','-o','ExitOnForwardFailure=yes','-N','-L',f'127.0.0.1:{port}:{ip}:8443',server],stdout=sp.DEVNULL,stderr=sp.PIPE,creationflags=sp.CREATE_NO_WINDOW);r={'time':datetime.datetime.now(datetime.UTC).isoformat(),'role':role,'fixture':'GardenWorld client11, isolated ERP r57','jar':meta['jar'],'menu':meta['rows'][0],'expected':meta['rows'][1:],'steps':[],'credentials_logged':False};pg=None
try:
 for i in range(40):
  try:a=socket.create_connection(('127.0.0.1',port),timeout=.3);a.close();break
  except OSError:time.sleep(.2)
 with sync_playwright() as w:
  b=w.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--disable-background-networking','--disable-sync','--no-first-run','--proxy-server=direct://']);c=b.new_context(ignore_https_errors=True,viewport={'width':1440,'height':1000});pg=c.new_page();pg.goto(f'https://127.0.0.1:{port}/webui/',wait_until='domcontentloaded',timeout=55000)
  try:
   pg.locator('input[type=password]:visible').first.wait_for(timeout=40000);pg.locator('input.z-textbox:visible').first.fill(role);pg.locator('input[type=password]:visible').first.fill(role);pg.locator("button:has-text('OK'):visible").first.click()
   for i in range(8):
    try:pg.locator('input.z-bandbox-input:visible').first.wait_for(timeout=2300);break
    except Exception:
     ok=pg.locator("button:has-text('OK'):visible")
     if ok.count()and not pg.locator('input[type=password]:visible').count():ok.first.click()
   pg.locator('input.z-bandbox-input:visible').first.wait_for(timeout=10000);pg.wait_for_timeout(1100);r['steps'].append('ZK desktop')
   box=pg.locator('input.z-bandbox-input:visible').first;name=meta['rows'][0]['name'];box.fill(name);box.dispatch_event('input');box.press('End');pop=pg.locator('.z-bandpopup:visible').first;pop.wait_for(timeout=9000);sel=pop.get_by_text(name,exact=True).first;sel.wait_for(timeout=9000);r['search']=sel.inner_text();sel.click();ta=pg.get_by_text('Tipuri de contracte',exact=True).first;ta.wait_for(timeout=16000);r['steps'].append('menu X → WSagaContracteForm');ta.click();pg.wait_for_timeout(900);r['visible_error']=bool(re.search('eroare la citirea tipurilor|column .value. does not exist',pg.locator('body').inner_text(),re.I));ls=pg.locator('.z-listbox:visible').evaluate_all("xs=>xs.map(x=>({headers:[...x.querySelectorAll('th.z-listheader')].map(v=>v.innerText.trim()),rows:[...x.querySelectorAll('tr.z-listitem')].map(tr=>[...tr.querySelectorAll('td.z-listcell')].map(td=>td.innerText.trim())).filter(d=>d.some(v=>v))}))");r['visible_tables']=ls;exp=[[v['name'],v['description']] for v in meta['rows'][1:]];got=next((v['rows']for v in ls if any(z[0]=='Consulting'for z in v['rows'])),[]);r['exact_pairs_equal']=got==exp;r['result']='PASS_LITERAL_DOM'if got==exp and not r['visible_error']else'FAIL_LITERAL_DOM';pg.screenshot(path=str(out/(role+'_tab.png')));r['screenshot_sha256']=sha(out/(role+'_tab.png'))
  except Exception as exc:
   r['result']='INCONCLUDENT_DRIVER';r['exception']=str(exc).splitlines()[0];r['diag']=re.sub(r'\s+',' ',pg.locator('body').inner_text())[:900];r['tabs']=pg.locator('.z-tab:visible').all_text_contents();pg.screenshot(path=str(out/(role+'_diagnostic.png')))
  c.close();b.close()
finally:
 t.terminate();t.wait(timeout=8);wr(out/(role+'.json'),r)
print(role,r.get('result'),r.get('exception'),r.get('diag','')[:170],r.get('visible_tables'))

