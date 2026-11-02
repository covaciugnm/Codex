from collections import Counter
def measure():
 z=sql("SELECT json_build_object('count',count(*),'groups',count(distinct(c_bankaccount_id,eva_luna)),'differences',count(*)filter(where eva_verdict<>'IDENTIC'),'instances',array_agg(distinct ad_pinstance_id),'amounts',md5(coalesce(string_agg(eva_luna||':'||c_bankaccount_id::text||':'||coalesce(eva_idnote,'')||':'||coalesce(eva_idtranzactie,'')||':'||eva_verdict||':'||coalesce(eva_delta,0)::text,'|' order by eva_luna,c_bankaccount_id,eva_alias_position),''))) FROM (select c.*,eva_pozitie eva_alias_position from eva_comparatiebanca c where ad_client_id=11 and eva_luna between '2026-01' and '2026-06')dd")[0];p=sql("SELECT row_to_json(q) from (select i.ad_pinstance_id, i.result, i.isprocessing from ad_pinstance i join ad_process p on p.ad_process_id=i.ad_process_id where lower(p.value)='eva_comparabancasaga' and i.ad_client_id=11 order by i.ad_pinstance_id desc limit 3)q")
 return {'physical':z,'processes':p}
def modal(page):
 return page.locator('.z-window-modal:visible,.z-window-highlighted:visible').last
record['pre_execution_scope']=sql("select json_build_object('client',11,'active_count',count(*),'active_synthetic',count(*)filter(where c_bankaccount_id between 987600000 and 987600009),'foreign',count(*)filter(where c_bankaccount_id not between 987600000 and 987600009)) from c_bankaccount where ad_client_id=11 and isactive='Y'")[0];assert record['pre_execution_scope']['active_count']==record['pre_execution_scope']['active_synthetic']==10
end=panel.locator('input.z-datebox-input').nth(1);end.fill('30.06.2026');end.press('Tab');page.wait_for_timeout(470);panel.get_by_role('button',name='Încarcă',exact=True).click();page.wait_for_timeout(500)
bt=panel.get_by_role('button',name='Compar cu SAGA',exact=True);journal=panel.get_by_role('button',name='Jurnal…',exact=True)
record['pre_buttons']={'compare_enabled':bt.is_enabled(),'session_log_enabled':journal.is_enabled(),'select':panel.locator('select:visible').evaluate_all("xs=>xs.map(x=>({name:x.title,v:x.selectedOptions[0]?.textContent}))"),'dates':panel.locator('input.z-datebox-input:visible').evaluate_all('xs=>xs.map(x=>x.value)')};assert record['pre_buttons']['dates']==['01.01.2026','30.06.2026']and record['pre_buttons']['select'][0]['v']=='(toate conturile)'
record['clicks']=[];snap(page,'00-inainte-buton');saved()
for k in [1,2]:
 before=measure();nowmark=before['processes'][0]['ad_pinstance_id']if before['processes']else 0
 rec={'number':k,'before':before,'click_utc':now(),'states':[]};record['clicks'].append(rec);bt.click()
 for i in range(80):
  page.wait_for_timeout(410);body=panel.inner_text();stat=[l.strip()for l in body.splitlines()if any(p in l for p in ['diferențe','ultima rulare','✔','❌','în curs','Rulează','se rulează','Calculez'])and len(l)<300]
  st={'compare_enabled':bt.is_enabled(),'log_enabled':journal.is_enabled(),'messages':stat}; 
  if not rec['states']or rec['states'][-1]!=st:rec['states'].append(st)
  if st['compare_enabled']and st['log_enabled']and any('✔'in x or '❌'in x for x in stat):break
 aft=measure();rec['after']=aft;rec['complete_utc']=now();rec['new_instance_id']=aft['processes'][0]['ad_pinstance_id'];assert rec['new_instance_id']>nowmark,(nowmark,aft);iid=rec['new_instance_id'];rec['dblog']=sql("select json_build_object('row_count',count(*),'start',count(*)filter(where lower(coalesce(p_msg,''))like '%porn%'or lower(coalesce(p_msg,''))like '%încep%'),'sample',left(min(p_msg),155),'result',max(i.result)) from ad_pinstance_log l join ad_pinstance i using(ad_pinstance_id)where ad_pinstance_id="+str(iid))[0];snap(page,'0'+str(k)+'-rezultat-buton');saved();event(('click',k,rec['states'],iid,aft['physical'],rec['dblog']))
 journal.click();page.wait_for_timeout(520);mod=modal(page);mod.wait_for(timeout=6000);v=mod.inner_text();rec['journal']={'length':len(v),'first':v[:860],'last':v[-250:],'buttons':mod.locator('button:visible').all_text_contents(),'title':mod.locator('.z-window-header:visible').all_text_contents()};snap(page,'0'+str(k)+'-jurnal-proces');saved()
 cb=mod.locator('.z-window-icon.z-window-close:visible,.z-window-close:visible,[aria-label="Close"]:visible'); 
 if cb.count():cb.first.click()
 else:
  buttons=mod.get_by_role('button',name=re.compile(r'Închid|Inchid|Close|OK',re.I))
  if buttons.count():buttons.first.click()
  else:page.keyboard.press('Escape')
 page.wait_for_timeout(300)

