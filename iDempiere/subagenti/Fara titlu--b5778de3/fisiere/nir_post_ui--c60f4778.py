from lab import W,PG,AP,IP,sql,cmd,rows,now
from pathlib import Path
import re,json,glob,hashlib,time
from playwright.sync_api import sync_playwright
d=W/'a04-nir-post/run3';d.mkdir(exist_ok=True)
rec={'time':now(),'mode':'ZK native, postconfiguration witness','cases':[],'navigation':[]}
def save(): (d/'obs.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2))
def gotofile(x):return hashlib.sha256(x.read_bytes()).hexdigest()
assert 'eva-test-' in PG and W.name=='eva-contab-codex-p01uizk-r5.vUjauFBh' and cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-p01uizkr5'
assert rows("select ad_client_id,name from adempiere.ad_client order by 1;")==[['0','System'],['11','GardenWorld']]
assert rows("select value from adempiere.ad_sysconfig where ad_client_id=11 and name='EVA_SETARI_FIRMA_MIGRAT'")==[['Y']]
seed=json.loads((W/'nir-document-source.json').read_text());docno=seed['snapshot'][0][0]
with sync_playwright() as pw:
 ce=sorted(glob.glob(str(Path.home()/'.cache/ms-playwright/chromium-*/chrome-linux*/chrome')))
 b=pw.chromium.launch(headless=True,executable_path=ce[-1] if ce else None,args=['--no-sandbox','--disable-dev-shm-usage','--proxy-server=direct://'])
 ctx=b.new_context(ignore_https_errors=True,viewport={'width':1440,'height':1050},locale='ro-RO')
 ctx.route('**/*',lambda rt:rt.continue_() if rt.request.url.startswith('https://'+IP+':8443/') else rt.abort())
 pg=ctx.new_page();pg.set_default_timeout(6500);pg.on('dialog',lambda dialog:dialog.dismiss())
 def tabs():return pg.locator('.z-tab:visible').all_text_contents()
 def snap(k):
  rec[k]={'tabs':tabs(),'footer':pg.locator('body').inner_text()[-1700:],'dialogs':pg.locator('.z-window-header:visible').all_text_contents()};save()
 def open_menu(name,ready):
  for tries in range(3):
   if ready.count() and ready.first.is_visible():return
   box=pg.locator('input.z-bandbox-input:visible').first;box.press('Escape');box.fill('');box.dispatch_event('input');pg.wait_for_timeout(380)
   box.fill(name);box.dispatch_event('input');box.press('End');pop=pg.locator('.z-bandpopup:visible').first;hit=pop.locator('span.z-label:visible').filter(has_text=re.compile('^'+re.escape(name)+'$',re.I));hit.first.wait_for(timeout=8000)
   rec['navigation'].append({'menu':name,'try':tries,'candidates':hit.evaluate_all("els=>els.map(e=>[e.outerHTML.slice(0,350),e.parentNode.outerHTML.slice(0,450)])")});save()
   hit.first.click();pg.wait_for_timeout(900)
   if ready.count() and ready.first.is_visible():return
   try:ready.first.wait_for(timeout=3100);return
   except Exception:pass
   if pop.count() and pop.is_visible():box.press('Escape')
  raise AssertionError('menu not opened: '+name)
 try:
  pg.goto('https://'+IP+':8443/webui/',wait_until='domcontentloaded',timeout=60000);pwd=pg.locator('input[type=password]:visible').first;pwd.wait_for(timeout=60000);pg.locator('input.z-textbox:visible').first.fill('GardenAdmin');pwd.fill('GardenAdmin');pg.locator("button:has-text('OK'):visible").first.click()
  for k in range(12):
   try:pg.locator('input.z-bandbox-input:visible').first.wait_for(timeout=2700);break
   except Exception:
    ok=pg.locator("button:has-text('OK'):visible")
    if ok.count() and not pg.locator('input[type=password]:visible').count():ok.first.click()
  pg.wait_for_timeout(1700)
  m=pg.get_by_role('button',name=re.compile(r'Migrez setările din SysConfig|Migrate the settings from SysConfig',re.I))
  open_menu('Setări firmă pe perioade',m)
  m.first.click();pg.wait_for_timeout(2500)
  hdr=pg.locator('.z-window-header:visible').filter(has_text=re.compile('Migrarea setărilor firmei|migration',re.I));hdr.wait_for(timeout=20000)
  snap('after_native_callback_rejected_migration');pg.screenshot(path=str(d/'callback.png'))
  # The JobFundal completion callback, including for a refused migration, resets the cache.
  win=pg.locator('.z-window:visible').filter(has=hdr).last
  btn=win.get_by_role('button',name=re.compile(r'Închid|Close',re.I)).last
  if btn.count():btn.click()
  else:pg.get_by_role('button',name=re.compile('Închid',re.I)).last.click()
  pg.wait_for_timeout(850)
  row=pg.get_by_text(docno,exact=True);open_menu('Intrări - lei',row)
  row.first.click();pg.wait_for_timeout(400);pg.get_by_role('button',name=re.compile(r'^Document(?:s|e)?[.…]',re.I)).first.click();item=pg.locator('.z-listitem:visible').filter(has_text=re.compile('14-3-1A|NOT[ĂA] DE RECEP',re.I)).first;item.click();pg.wait_for_timeout(900)
  rec['emission_fields']=pg.locator('textarea:visible').evaluate_all("els=>els.map(e=>({value:e.value,outer:e.outerHTML.slice(0,210),context:e.parentNode.innerText.slice(0,180)}))");snap('form');pg.screenshot(path=str(d/'form.png'))
  quant=pg.locator('textarea:visible');ind=quant.evaluate_all("els=>els.findIndex(e=>/7/.test(e.value)&&/5/.test(e.value))")
  if ind<0:
   ind=quant.evaluate_all("els=>els.findIndex(e=>/cantitățile recepționate/i.test(e.previousElementSibling?.innerText||''))")
  assert ind>=0,'no quantity field';field=quant.nth(ind)
  for label,value in [('control','7\n3'),('blank','\n3'),('invalid','invalida\n3')]:
   field.fill(value);field.press('Tab');pg.wait_for_timeout(330);case={'id':label,'expected':('370.00' if label!='invalid' else 'validare sau corecție fără deplasarea valorii la alt articol'),'input':value,'field_readback':field.input_value()};rec['cases'].append(case);save()
   try:
    with ctx.expect_page(timeout=9000) as pp:
     pg.get_by_role('button',name=re.compile('Previzualiz|Preview',re.I)).first.click()
    out=pp.value;out.locator('tr.total').first.wait_for(timeout=6500);case['table_rows']=out.locator('table tr').all_text_contents();case['totals']=out.locator('tr.total').all_text_contents()
    html=d/(label+'.html');html.write_text(out.content());case['html_sha256']=gotofile(html);out.screenshot(path=str(d/(label+'.png')),full_page=True)
    pdf=d/(label+'.pdf');out.pdf(path=str(pdf),format='A4',print_background=True);case['pdf_sha256']=gotofile(pdf);out.close()
   except Exception as e:case['issue']=str(e)[:350];case['dialog']=pg.locator('body').inner_text()[-1000:];pg.screenshot(path=str(d/(label+'-error.png')))
   save()
 except Exception as e:
  rec['stopped']=str(e)[:720];snap('end');pg.screenshot(path=str(d/'stopped.png'))
 finally:save();ctx.close();b.close()
print(rec.get('stopped'),[(c['id'],c.get('totals'),c.get('issue')) for c in rec['cases']],flush=True)
