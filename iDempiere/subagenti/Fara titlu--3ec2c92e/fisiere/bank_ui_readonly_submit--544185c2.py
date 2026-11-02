active=page.locator('.desktop-tabpanel:visible').filter(has_text='Doar verificare (nu scrie nimic)').last
mandatory=[page.locator('#'+c['id']) for c in record['dispatcher']['controls'] if c['tag']=='INPUT' and 'idempiere-mandatory' in c['cls']];assert len(mandatory)==2
for i,val in enumerate(['2026-01','2026-06']):
 mandatory[i].fill(val);mandatory[i].press('Tab');page.wait_for_timeout(250)
ctl=record['dispatcher']['controls'];verify=next(t['id']for t in ctl if t['type']=='checkbox'and 'Doar verificare'in t['scope']);check=page.locator('#'+verify);check.check();page.wait_for_timeout(320)
assert check.is_checked() and [mandatory[i].input_value()for i in [0,1]]==['2026-01','2026-06'] and not page.locator('#'+next(c['id']for c in ctl if c['scope']=='Run as Job')).is_checked()
record['entered']={'LunaDeLa':mandatory[0].input_value(),'LunaPanaLa':mandatory[1].input_value(),'DoarVerifica':check.is_checked(),'account_empty':active.locator('input.z-decimalbox:visible').input_value()==''};assert record['entered']['account_empty']
def dbsnapshot():return sql("select json_build_object('rows',count(*),'unique_run_ids',array_agg(distinct ad_pinstance_id),'identical_rowhash',md5(coalesce(string_agg(to_jsonb(c)::text,'|' order by eva_comparatiebanca_id),''))) from eva_comparatiebanca c where ad_client_id=11 and eva_luna between '2026-01' and '2026-06'")[0]
def lastproc():return sql("select row_to_json(q) from (select i.ad_pinstance_id,i.result,i.isprocessing,i.errormsg from ad_pinstance i where i.ad_client_id=11 and i.ad_process_id=1000218 order by i.ad_pinstance_id desc limit 1)q")[0]
record['before_check_only']={'physical':dbsnapshot(),'process':lastproc()};snap(page,'02-uniquement-verification');saved()
active.get_by_role('button',name=re.compile(r'^\s*OK\s*$',re.I)).click()
for i in range(35):
 page.wait_for_timeout(450);pr=lastproc()
 if pr['ad_pinstance_id']>record['before_check_only']['process']['ad_pinstance_id']and pr['result']is not None and pr['isprocessing']=='N':break
pr=lastproc();record['after_check_only']={'physical':dbsnapshot(),'process':pr,'display':page.locator('.desktop-tabpanel:visible').all_text_contents()[-1][-4200:]};assert pr['ad_pinstance_id']>record['before_check_only']['process']['ad_pinstance_id'];pid=pr['ad_pinstance_id']
record['submitted_parameters']=sql("select row_to_json(q) from (select parametername,p_string,p_number from ad_pinstance_para where ad_pinstance_id="+str(pid)+" order by seqno) q")
record['logs_only_check']=sql("select row_to_json(q)from (select log_id,left(p_msg,260) as p_msg from ad_pinstance_log where ad_pinstance_id="+str(pid)+" and ((p_msg ilike '%verif%' or p_msg ilike '%scri%') and p_msg not ilike '%Σ%') order by log_id desc limit 8)q")
snap(page,'03-rezultat-verificare');saved();event(('readonly',record['before_check_only'],record['after_check_only']['physical'],pr,record['logs_only_check']))

