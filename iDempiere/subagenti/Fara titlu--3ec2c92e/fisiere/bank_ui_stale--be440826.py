import collections
end=panel.locator('input.z-datebox-input').nth(1);end.fill('30.06.2026');end.press('Tab');page.wait_for_timeout(450);panel.get_by_role('button',name='Încarcă',exact=True).click();page.wait_for_timeout(800)
panel.locator('select[title="Nivel"]').select_option(label='Linii');page.wait_for_timeout(450);acc=panel.locator('select').first;record['samples']=[]
def check(name,seconds,evidence_label):
 start=time.monotonic()
 for i in range(16):
  page.wait_for_timeout(250)
  texts=panel.inner_text()
  if time.monotonic()-start>=seconds and (('137 rânduri' in texts)if name=='A12R10-1'else('Nu s-a' in texts or 'necalculat'in texts.lower()or time.monotonic()-start>seconds+.5)):break
 rows=panel.locator('tr').evaluate_all(r"""xs=>xs.map(x=>[...x.cells].map(c=>c.innerText.trim())).filter(c=>c.length>3&&/^[0-9]+$/.test(c[0])&&/^2026-0[1-6]$/.test(c[1])).length""");txt=panel.inner_text();snap(page,evidence_label);record['samples'].append({'control':evidence_label,'elapsed_s':round(time.monotonic()-start,2),'selected':acc.locator('option:checked').inner_text(),'datefilter':panel.locator('input.z-datebox-input').evaluate_all("xs=>xs.map(x=>x.value)"),'dom_data_rows':rows,'footer_and_explanation':[v.strip()for v in txt.splitlines()if 'rânduri'in v or 'necunosc'in v.lower()or 'ercalcul'in v or 'calculat'in v or 'comparat'in v or 'diferențe'in v][:9]});saved()
acc.select_option(label='A12R10-1');check('A12R10-1',1.1,'prima-grila-137')
acc.select_option(label='A12R10-10');check('A12R10-10',3.0,'a-doua-grila-0')
panel.get_by_role('button',name='Încarcă',exact=True).click();check('A12R10-10',3.0,'reincarca-cont-gol')
acc.select_option(index=0);check('all',1.0,'revenire-toate')
record['qualified_empty_control']=sql("SELECT json_build_object('name',b.accountno,'rows',count(c.eva_comparatiebanca_id),'groups',count(distinct c.eva_luna)) from c_bankaccount b left join eva_comparatiebanca c on c.c_bankaccount_id=b.c_bankaccount_id and c.ad_client_id=11 and c.eva_luna between '2026-01' and '2026-06' where b.ad_client_id=11 and b.accountno in('A12R10-1','A12R10-10') group by b.accountno order by b.accountno")

