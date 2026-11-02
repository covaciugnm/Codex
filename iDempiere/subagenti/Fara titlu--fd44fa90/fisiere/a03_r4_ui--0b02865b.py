from a03_r4_slot import *
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
ui=r'''from lab import *
from playwright.sync_api import sync_playwright
import re,glob,traceback
r={'utc':now(),'actor':'GardenAdmin, GardenWorld. Browser authenticates from a fresh session; role and form visibility are collected from actual DOM.','steps':[],'refusal_seen':False,'new_journals':None}
before=sql("SELECT count(*) FROM adempiere.gl_journal WHERE ad_client_id=11 AND description LIKE 'INCHIDERE-VC 2026-08%'")
def state(p):
 b=p.locator('body').inner_text(timeout=6000)
 return b[:3200]
def save(): (W/'ui.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
with sync_playwright() as pw:
 chrome=sorted(glob.glob(str(pathlib.Path.home()/'.cache/ms-playwright/chromium-*/chrome-linux*/chrome')));browser=pw.chromium.launch(headless=True,executable_path=chrome[-1] if chrome else None,args=['--no-sandbox','--disable-dev-shm-usage','--disable-background-networking']);ctx=browser.new_context(ignore_https_errors=True,viewport={'width':1366,'height':768},locale='ro-RO');page=ctx.new_page();page.set_default_timeout(5500)
 try:
  page.goto(ROOT+'/webui/',wait_until='domcontentloaded',timeout=35000)
  page.locator("input[type=text]:visible").first.fill("GardenAdmin");page.locator("input[type=password]:visible").first.fill("GardenAdmin");page.locator("button:has-text('OK'):visible").first.click()
  for i in range(8):
   try:page.locator('input.z-bandbox-input:visible').first.wait_for(timeout=2500);break
   except Exception:
    if page.locator("button:has-text('OK'):visible").count():page.locator("button:has-text('OK'):visible").first.click(timeout=2500)
  box=page.locator('input.z-bandbox-input:visible').first;box.wait_for(timeout=8000);r['steps'].append({'step':'native desktop','text':state(page)[:450]})
  metadata=rows("SELECT m.name,m.ad_menu_id,f.ad_form_id FROM adempiere.ad_form f JOIN adempiere.ad_menu m USING(ad_form_id) WHERE f.classname='com.eva.ro.contab.form.WSagaInchidereLunaForm' AND f.isactive='Y' AND m.isactive='Y' LIMIT 3");r['menu_metadata']=metadata;assert metadata
  opened=False
  for label in [metadata[0][0],'Închidere lună','Month closing','Month close']:
   box.fill(label);box.dispatch_event('input');box.press('End');page.wait_for_timeout(550)
   popup=page.locator('.z-bandpopup:visible').first
   try:popup.wait_for(timeout=3500)
   except Exception:continue
   tar=popup.get_by_text(label,exact=True)
   if tar.count():tar.first.click();page.wait_for_timeout(1500);r['steps'].append({'step':'opened','label':label});opened=True;break
  r['menu_opened']=opened
  if not opened:raise ValueError('Exact menu result was not shown')
  page.screenshot(path=str(W/'T58-native-form.png'));r['form_state_initial']=state(page)
  all_sel=page.locator('select:visible'); opts=[all_sel.nth(i).locator('option').all_text_contents() for i in range(all_sel.count())];r['selects']=opts
  for i,labels in enumerate(opts):
   target=next((x for x in labels if x.strip()=='2026'),None)
   if target:all_sel.nth(i).select_option(label=target);page.wait_for_timeout(450)
  all_sel=page.locator('select:visible')
  for i in range(all_sel.count()):
   labels=all_sel.nth(i).locator('option').all_text_contents();target=next((x for x in labels if re.search(r'^\s*(08|8|august)\b',x,re.I)),None)
   if target:all_sel.nth(i).select_option(label=target);page.wait_for_timeout(1300);r['selected_month']=target;break
  state_now=state(page);r['period_state']=state_now; tr=page.locator('tr:visible').filter(has_text=re.compile('Închidere conturi de venituri și cheltuieli|Closing revenue and expense accounts|Close revenue and expense accounts|Closing income and expense accounts|Close revenue and expense|income and expense',re.I));candidates=[]
  for i in range(tr.count()):
   row=tr.nth(i);bs=row.locator('button:visible');txt=row.inner_text()
   if not bs.count() or bs.count()>8:continue
   candidates.append({'text':txt[:350],'buttons':[{'name':bs.nth(k).inner_text(),'disabled':bs.nth(k).is_disabled(),'title':bs.nth(k).get_attribute('title')} for k in range(bs.count())]})
   matches=bs.filter(has_text=re.compile('^\s*(Validez|Validate|Post)\s*$',re.I))
   if matches.count()==1 and r.get('selected_month'):
    btn=matches.first; r['button']={'disabled':btn.is_disabled(),'tooltip':btn.get_attribute('title'),'text':btn.inner_text()}
    btn.hover(timeout=3000);page.wait_for_timeout(650)
    if btn.is_disabled():
     r['conclusion']='Validarea VC este dezactivată înainte de scriere. Se reține motivul afișat. Nu se forțează click-ul prin script.';r['refusal_seen']=bool(re.search(r'pasul 5|step 5|5\.\s',r['button']['tooltip'] or '',re.I))
    else:
     btn.click();page.wait_for_timeout(800);r['after_click']=state(page);r['refusal_seen']=bool(re.search(r'pasul 5|step 5',r['after_click'],re.I));r['conclusion']='Click operator pe Validez; vezi mesajul și readback.'
    break
  r['candidate_rows']=candidates;page.screenshot(path=str(W/'T58-native-august.png'));r['final_state']=state(page)
 except Exception as er:r['diagnostic']=type(er).__name__+': '+str(er)[:550];r['browser_state']=state(page)[:800];page.screenshot(path=str(W/'T58-native-diagnostic.png'))
 finally:
  after=sql("SELECT count(*) FROM adempiere.gl_journal WHERE ad_client_id=11 AND description LIKE 'INCHIDERE-VC 2026-08%'");r['new_journals']=int(after)-int(before);r['before_count']=before;r['after_count']=after;save();browser.close()
'''
p=work/'ui.py';p.write_text(ui,encoding='utf8',newline='\n');r=sp.run(['scp','-q','-o','BatchMode=yes',p,'saga-server@192.168.100.151:'+wd+'/ui.py'],capture_output=True);assert r.returncode==0
print(sh(f'cd {wd} && if mkdir ui_started 2>/dev/null; then (nohup python3 ui.py > ui.log 2>&1 < /dev/null &); fi').returncode)
