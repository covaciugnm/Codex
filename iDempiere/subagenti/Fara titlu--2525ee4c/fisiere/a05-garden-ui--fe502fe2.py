import os,pathlib,sys,glob
from playwright.sync_api import sync_playwright
w=pathlib.Path('/tmp/codex-a05.ObWQES'); ip=(w/'ip').read_text().strip()
assert ip.startswith('10.250.')
out=w/'ui';out.mkdir(exist_ok=True)
with sync_playwright() as pw:
    paths=sorted(glob.glob(str(pathlib.Path.home()/'.cache/ms-playwright/chromium-*/chrome-linux*/chrome')))
    browser=pw.chromium.launch(headless=True,executable_path=paths[-1] if paths else None,args=['--no-sandbox','--disable-dev-shm-usage','--proxy-server=direct://'])
    ctx=browser.new_context(ignore_https_errors=True,viewport={'width':1440,'height':960})
    page=ctx.new_page(); page.goto('https://'+ip+':8443/webui/',wait_until='domcontentloaded',timeout=60000)
    page.locator('input[type=password]:visible').first.wait_for(timeout=80000)
    page.locator('input.z-textbox:visible').first.fill('GardenAdmin'); page.locator('input[type=password]:visible').first.fill('GardenAdmin')
    page.locator("button:has-text('OK'):visible").first.click()
    for i in range(7):
        try:
            page.locator('input.z-bandbox-input:visible').first.wait_for(timeout=4000)
            break
        except Exception:
            ok=page.locator("button:has-text('OK'):visible")
            if ok.count() and not page.locator('input[type=password]:visible').count(): ok.first.click()
    box=page.locator('input.z-bandbox-input:visible').first
    if not box.count():
        print('No native search. Visible interface: '+page.locator('body').inner_text()[:480]);page.screenshot(path=str(out/'garden-desktop.png'));sys.exit(2)
    print('GardenWorld browser session, native desktop visible'); page.screenshot(path=str(out/'garden-desktop.png'))
    box.fill('Physical Inventory');box.dispatch_event('input');box.press('End')
    try:
        pop=page.locator('.z-bandpopup:visible').first
        pop.wait_for(timeout=10000)
        targets=pop.get_by_text('Physical Inventory',exact=True)
        if not targets.count():
            print('Search result',pop.inner_text()[:360]);sys.exit(3)
        targets.first.click()
        page.wait_for_timeout(1300);print('Opened tabs',page.locator('.z-tab:visible').all_text_contents()[:8])
        page.screenshot(path=str(out/'physical-inventory.png'))
    finally:
        browser.close()

