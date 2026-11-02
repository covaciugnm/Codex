from lab import *
import glob
from playwright.sync_api import sync_playwright
out=W/'zk';out.mkdir(exist_ok=True)
with sync_playwright() as pw:
 paths=sorted(glob.glob(str(pathlib.Path.home()/'.cache/ms-playwright/chromium-*/chrome-linux*/chrome')))
 br=pw.chromium.launch(headless=True,executable_path=paths[-1] if paths else None,args=['--no-sandbox','--disable-dev-shm-usage','--proxy-server=direct://'])
 pg=br.new_context(ignore_https_errors=True,viewport={'width':1450,'height':970}).new_page();pg.goto(ROOT+'/webui/',wait_until='domcontentloaded',timeout=70000)
 pg.locator('input[type=password]:visible').first.wait_for(timeout=60000);pg.locator('input.z-textbox:visible').first.fill('System');pg.locator('input[type=password]:visible').first.fill('System');pg.locator("button:has-text('OK'):visible").first.click()
 for i in range(6):
  try:pg.locator('input.z-bandbox-input:visible').first.wait_for(timeout=4000);break
  except Exception:
   btn=pg.locator("button:has-text('OK'):visible")
   if btn.count() and not pg.locator('input[type=password]:visible').count():btn.first.click()
 box=pg.locator('input.z-bandbox-input:visible').first;box.click();box.fill('');box.press_sequentially('Initial Client Setup',delay=70);pg.wait_for_timeout(1200)
 pop=pg.locator('.z-bandpopup:visible').first
 targets=pop.get_by_text('Initial Client Setup',exact=True)
 print('initial client option',targets.count(),pop.inner_text()[:300])
 if targets.count():targets.first.click();pg.wait_for_timeout(700)
 print('visible panels',pg.locator('.z-tab:visible,.z-window-header:visible').all_text_contents()[:8])
 print('field metadata',pg.locator('input:visible,textarea:visible').evaluate_all("(els)=>els.filter(e=>e.type!=='password').map(e=>[e.tagName,e.type,e.className,(e.title||'').slice(0,75),e.value,(e.parentElement.parentElement.previousElementSibling?.innerText||'').slice(0,75),(e.closest('tr')?.innerText||'').slice(0,70)]).slice(0,45)"))
 pg.screenshot(path=str(out/'initial-client-before.png'))
 br.close()

