from collections import Counter
def capture_state(pan,period=True):
 text=pan.inner_text();sel=pan.locator('select:visible').evaluate_all("els=>els.map(n=>({title:n.title,selection:n.selectedOptions[0]?.textContent}))")
 cc=pan.locator('tr').evaluate_all(r"""xs=>xs.map(x=>[...x.cells].map(c=>c.innerText.trim())).filter(c=>c.length>3&&/^[0-9]+$/.test(c[0])&&/^2026-0[1-6]$/.test(c[1]))""")
 return {'datefilter':pan.locator('input.z-datebox-input:visible').evaluate_all("xs=>xs.map(x=>x.value)"),'selection':sel,'rows_observed_dom':len(cc),'rows':cc,'footer':[t.strip()for t in text.splitlines()if re.search(r'\b(diferențe|luni ·|rânduri|rândurile)\b',t,re.I) and len(t)<155][:9],'journal_disabled':pan.get_by_role('button',name='Jurnal…',exact=True).is_disabled()}
end=panel.locator('input.z-datebox-input').nth(1);end.fill('30.06.2026');end.press('Tab');page.wait_for_timeout(300);panel.get_by_role('button',name='Încarcă',exact=True).click();page.wait_for_timeout(630)
record['months']=capture_state(panel);assert record['months']['datefilter']==['01.01.2026','30.06.2026'];snap(page,'02-luni-filtrate')
sel=panel.locator('select[title="Nivel"]');sel.select_option(label='Linii');page.wait_for_timeout(830);record['lines']=capture_state(panel);snap(page,'03-linii-filtrate');saved();event(('line amounts',record['lines']['rows_observed_dom'],record['lines']['footer']))
try:
 panel.get_by_role('button',name='Export CSV',exact=True).click();page.wait_for_timeout(420);mod=page.locator('.z-window-modal:visible,.z-window-highlighted:visible,.z-messagebox-window:visible').last;mod.wait_for(timeout=6000)
 formtxt=mod.inner_text();cb=mod.locator('input[type=checkbox]');record['export_dialog']={'text':formtxt[:1300],'boxes':cb.count(),'checked':mod.locator('input[type=checkbox]:checked').count(),'buttons':mod.locator('button:visible').all_text_contents()};snap(page,'04-export-optiuni');saved()
 buttons=mod.get_by_role('button',name=re.compile(r'^(accept|ok|confirm|aplic|transfer|export|continu)',re.I));assert buttons.count()==1,record['export_dialog']
 with page.expect_download(timeout=12000)as d:buttons.first.click()
 dl=d.value;f=base/'export_linii_ian_iunie.csv';dl.save_as(str(f));csvrows=list(csv.reader(io.StringIO(f.read_text(encoding='utf-8-sig')),delimiter=';'));head=csvrows[0];works=[i for i in csvrows[1:]if re.match(r'^2026-0[1-6]$',i[0])]
 counts=Counter(w[0]for w in works);veridx=next((i for i,h in enumerate(head)if 'verdict'in h.lower()),None);verdict=Counter(w[veridx]for w in works)if veridx is not None else {}
 record['export']={'download_name':dl.suggested_filename,'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'length':f.stat().st_size,'headers':head,'csv_data_after_header':len(csvrows)-1,'recognized_YYYY_MM':len(works),'extra_after_header':[c[:2]for c in csvrows[1:]if not re.match(r'^2026-0[1-6]$',c[0])][:3],'months':dict(counts),'verdicts':dict(verdict)};event(('download',record['export']))
except Exception as exc:
 record['export_error']=str(exc)[:400];saved();event(('export_error',str(exc)[:300]))
 if page.locator('.z-window-modal:visible,.z-window-highlighted:visible').count():page.keyboard.press('Escape');page.wait_for_timeout(300)
# account with six months then empty one, measured as an independent control
acc=panel.locator('select').first
for nm in ['A12R10-1','A12R10-10']:
 acc.select_option(label=nm);page.wait_for_timeout(500);v=capture_state(panel);record.setdefault('by_account',{})[nm]={'footer':v['footer'],'rendered_actual':v['rows_observed_dom'],'selected':v['selection']};saved()
acc.select_option(index=0);page.wait_for_timeout(500)
record['db_months']=sql("SELECT json_build_object('month',eva_luna,'rows',count(*),'outside_ten_accounts',count(*) filter(where c_bankaccount_id not between 987600000 and 987600009),'difference',count(*)filter(where eva_verdict<>'IDENTIC'),'physical_groups',count(distinct c_bankaccount_id),'run',array_agg(distinct ad_pinstance_id)) from eva_comparatiebanca where ad_client_id=11 and eva_luna between '2026-01' and '2026-06' group by eva_luna order by eva_luna")
record['db_verdicts']=sql("SELECT json_build_object('verdict',eva_verdict,'n',count(*)) from eva_comparatiebanca where ad_client_id=11 and eva_luna between '2026-01' and '2026-06' group by eva_verdict order by 1::text")
record['db_control_account']=sql("SELECT json_build_object('name',b.accountno,'rows',count(c.eva_comparatiebanca_id),'groups',count(distinct c.eva_luna)) from c_bankaccount b left join eva_comparatiebanca c on c.c_bankaccount_id=b.c_bankaccount_id and c.ad_client_id=11 and c.eva_luna between '2026-01' and '2026-06' where b.ad_client_id=11 and b.accountno in('A12R10-1','A12R10-10') group by b.accountno order by b.accountno")
bt=panel.get_by_role('button',name='Jurnal de bancă…',exact=True);old=tabs(page);bt.click();page.wait_for_timeout(1150);record['journal_window']={'old_tabs':old,'new_tabs':tabs(page),'selected_tooltip':page.locator('.z-tab-selected').last.get_attribute('title'),'dialogs':page.locator('.z-window-modal:visible,.z-window-highlighted:visible').all_text_contents()};snap(page,'05-jurnal-banca');saved();event(('journal',record['journal_window']))

