import pathlib,re,sys,subprocess as sp,socket,time,datetime,json,ipaddress,hashlib,os,traceback,csv,io,codecs
from contextlib import closing
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
base=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R10_pregatire/A12/T06_UI');base.mkdir(exist_ok=True)
scratch=pathlib.Path('D:/CodexWork/a12-r10-local/scratch.txt').read_text().strip()
assert re.fullmatch('/tmp/eva-contab-codex-p01a12r10t06[.][a-zA-Z0-9]{8}',scratch)
host='saga-server@192.168.100.151';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(cmd,stdin=None):
 s=sp.run(cmd,input=stdin,capture_output=True,timeout=22)
 if s.returncode:raise RuntimeError(s.stderr.decode('utf8','replace')[-300:])
 return s.stdout.decode().strip()
ssh=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',host]
script='''set -eu
cd SCR
test -e ready
pg=$(cat auditor-pg);app=$(cat auditor-app)
for c in "$pg" "$app"; do test "$(docker inspect --format '{{index .Config.Labels "eva.sesiune"}}' "$c")" = eva-contab-codex-p01a12r10t06;done
cat ip
'''.replace('SCR',scratch)
ip=run(ssh+['bash','-s'],script.encode()).strip();assert ipaddress.ip_address(ip).is_private and ip.startswith('10.')
def sql(stmt):
 cmd=script.replace('cat ip','''docker exec -i "$pg" sh -c 'exec psql -XqAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d idempiere' <<'FG'
BEGIN READ ONLY;SET LOCAL search_path TO adempiere,pg_catalog;SET LOCAL statement_timeout='8s';
'''+stmt+''';
ROLLBACK;
FG''')
 return [json.loads(s) for s in run(ssh+['bash','-s'],cmd.encode()).splitlines() if s and s[0] in '{[']
menu=sql("select row_to_json(q) from (select m.ad_menu_id, m.name, f.ad_form_id, f.classname from ad_menu m join ad_form f on f.ad_form_id=m.ad_form_id where m.isactive='Y' and f.isactive='Y' and f.classname like '%.WEvaComparatieBancaForm')q");assert len(menu)==1,menu
record={'utc_start':now(),'source':'Native ZK user session via verified private SSH forward; role-specific, GardenWorld synthetic','menu':menu,'screens':{},'actions':[]}
def event(txt):print(txt,flush=True)
def snap(page,n):
 q=base/(n+'.png');page.screenshot(path=str(q));record['screens'][n]={'file':q.name,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
def tabs(page):return page.locator('.z-tab:visible').all_text_contents()
def diagnostic(page,panel):
 return panel.evaluate(r"""el=>({text:el.innerText.slice(0,7500),controls:[...el.querySelectorAll('input,select,textarea,button,[role=button]')].filter(x=>x.getClientRects().length).map(x=>({tag:x.tagName,cls:x.className,type:x.type,value:x.value,text:x.innerText||'',title:x.title,disabled:x.disabled,alt:x.getAttribute('aria-label'),fmt:(window.zk&&zk.Widget.$(x)?.getFormat?.())||null})),grids:[...el.querySelectorAll('table')].filter(x=>x.getClientRects().length).map(x=>({cls:x.className,rows:x.rows?.length||0,example:x.querySelector('tr')?.innerText?.slice(0,100)})).slice(-15)})""")
def saved():
 t=base/'capture_ui.json';t.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
 if 'journal_window' in record and record.get('export',{}).get('recognized_YYYY_MM')==168:(base/'DOM_sesiune_verificata.json').write_bytes(t.read_bytes())
def zone_web(page,ctx):
 user='GardenAdmin';page.goto(url+'/webui/',wait_until='domcontentloaded',timeout=55000);page.locator('input[type=password]:visible').first.wait_for(timeout=45000)
 page.locator('input.z-textbox:visible').first.fill(user);page.locator('input[type=password]:visible').first.fill(user);page.locator("button:has-text('OK'):visible").first.click()
 for j in range(8):
  if page.locator('input.z-bandbox-input:visible').count():break
  try:page.locator('input.z-bandbox-input:visible').first.wait_for(timeout=2100);break
  except Exception:pass
  button=page.locator("button:has-text('OK'):visible"); 
  if button.count():button.first.click()
 box=page.locator('input.z-bandbox-input:visible').first;box.wait_for(timeout=16000)
 record['role']=sql("select row_to_json(q) from (select s.ad_session_id,s.ad_role_id,s.ad_org_id,s.ad_client_id,s.created from ad_session s join ad_user u on u.ad_user_id=s.createdby where s.ad_client_id=11 and u.name='GardenAdmin' and s.remote_addr='192.0.2.204' order by s.ad_session_id desc limit 1)q")
 assert record['role'] and record['role'][0]['ad_role_id']==102,record['role']
 search=menu[0]['name'];box.fill(search);box.dispatch_event('input');box.press('End');pop=page.locator('.z-bandpopup:visible').first;pop.wait_for(timeout=12500)
 match=pop.get_by_text(re.compile(r'^\s*'+re.escape(search)+r'\s*$',re.I));match.first.wait_for(timeout=6500);record['exact_menu_search_matches']=match.count();match.first.click();page.wait_for_timeout(1100)
 tab=page.locator('.z-tab-selected[title*="Comparație"]:visible')
 try:tab.first.wait_for(timeout=3600)
 except Exception:
  record['retry_diagnostic']={'tabs':tabs(page),'pop':page.locator('.z-bandpopup:visible').all_text_contents(),'modals':page.locator('.z-window-modal:visible,.z-window-highlighted:visible').all_text_contents()}
  box.fill('');box.fill(search);box.dispatch_event('input');box.press('End');match.first.wait_for(timeout=5000);box.press('Enter')
  tab.first.wait_for(timeout=10000)
 tab=tab.first;pn=tab.evaluate("t=>zk.Widget.$(t).getLinkedPanel().$n().id");panel=page.locator('#'+pn);panel.wait_for();record['tab']={'tooltip':tab.get_attribute('title'),'text':tab.inner_text(),'panel':pn}
 record['initial']=diagnostic(page,panel);record['initial_rows']=sql("select json_build_object('rows',count(*),'groups',count(distinct(c_bankaccount_id,eva_luna)),'instances',count(distinct ad_pinstance_id),'min_month',min(eva_luna),'max_month',max(eva_luna),'outside_fixture',count(*) filter(where c_bankaccount_id not between 987600000 and 987600009)) from eva_comparatiebanca where ad_client_id=11")
 snap(page,'01-formular');saved();event(('Native form initial',record['tab'],record['initial']['controls']))
 return page,panel
sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close();url='https://127.0.0.1:'+str(port)
forward=sp.Popen(['ssh','-N','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ExitOnForwardFailure=yes','-L','127.0.0.1:'+str(port)+':'+ip+':8443',host],stdin=sp.DEVNULL,stdout=sp.DEVNULL,stderr=sp.DEVNULL,creationflags=getattr(sp,'CREATE_NO_WINDOW',0))
try:
 for _ in range(30):
  try:
   with closing(socket.create_connection(('127.0.0.1',port),timeout=.5)):break
  except OSError:time.sleep(.2)
 with sync_playwright()as p:
  b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--disable-background-networking','--disable-sync','--disable-extensions']);ctx=b.new_context(ignore_https_errors=True,viewport={'width':1450,'height':960},locale='en-US',extra_http_headers={'X-Forwarded-For':'192.0.2.204'})
  ctx.route('**/*',lambda x:x.continue_() if x.request.url.startswith(url+'/')else x.abort());page=ctx.new_page()
  try:
   page,panel=zone_web(page,ctx)
   extra=pathlib.Path('D:/CodexWork/a12-r10-local/bank_ui_actions.py')
   if extra.exists():exec(extra.read_text(encoding='utf8'),globals(),locals())
  except Exception as err:record['error']=str(err)[:950];event((type(err).__name__,str(err)[:350])); snap(page,'diagnostic')
  finally:record['utc_end']=now();saved();ctx.close();b.close()
finally:
 if forward.poll() is None:forward.terminate();forward.wait(timeout=10)

