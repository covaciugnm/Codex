nm='Bancă: compară cu SAGA (proces)';box=page.locator('input.z-bandbox-input:visible').first;box.fill(nm);box.dispatch_event('input');box.press('End');pop=page.locator('.z-bandpopup:visible').first;target=pop.get_by_text(re.compile(r'^\s*'+re.escape(nm)+r'\s*$'));target.first.wait_for(timeout=6500);record['hit_menu_process']=target.count();assert target.count()==1;target.first.click();page.wait_for_timeout(1200)
def inspect_ui():
 return page.evaluate(r"""()=>({tabs:[...document.querySelectorAll('.z-tab')].map(e=>({label:e.innerText,title:e.title})),active_panels:[...document.querySelectorAll('.z-window,.desktop-tabpanel')].filter(e=>e.getClientRects().length).map(e=>({id:e.id,cls:e.className,summary:e.innerText.slice(-1600)})).slice(-5),controls:[...document.querySelectorAll('input,select,button,a[title],textarea')].filter(e=>e.getClientRects().length).map(e=>({id:e.id,tag:e.tagName,cls:e.className,txt:e.innerText||'',title:e.title,type:e.type,v:(e.type==='password'?null:e.value),lbl:e.getAttribute('aria-label'),disabled:!!e.disabled,checked:e.checked,scope:e.closest('tr,tr.z-row,div.z-row-content,.z-grid')?.innerText?.slice(0,120)||''})).slice(-45)})""")
record['dispatcher']=inspect_ui()
if nm not in str(record['dispatcher']['active_panels'])or not any('Luna' in x['summary']or 'Month' in x['summary'] for x in record['dispatcher']['active_panels']):
 box.fill('');box.fill(nm);box.dispatch_event('input');box.press('End');target.first.wait_for(timeout=5800);box.press('Enter');page.wait_for_timeout(1300);record['dispatcher']=inspect_ui()
snap(page,'01-parametri');saved();event(('process',record['dispatcher']['active_panels'][-1]['summary'],record['dispatcher']['controls'][-13:]))
extra=pathlib.Path('D:/CodexWork/a12-r10-local/bank_ui_readonly_submit.py')
if extra.exists():exec(extra.read_text(encoding='utf8'),globals(),locals())

