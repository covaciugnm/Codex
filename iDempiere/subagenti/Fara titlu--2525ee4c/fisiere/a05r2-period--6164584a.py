from lab import *
ta=auth('GardenAdmin',11,102,11);tb=auth('GardenUser',11,103,11)
obs=[]
r=rows("SELECT pc.c_periodcontrol_id,pc.periodstatus,p.name FROM adempiere.c_period p JOIN adempiere.c_periodcontrol pc ON pc.c_period_id=p.c_period_id WHERE p.ad_client_id=11 AND DATE '2026-11-02' BETWEEN p.startdate AND p.enddate AND pc.docbasetype='MMI' ORDER BY 1 LIMIT 1;")
assert len(r)==1;r0=int(r[0][0]);obs.append({'before':r})
c,j=api(ta,'PUT','models/C_PeriodControl/'+str(r0),{'PeriodAction':'O'});obs.append({'request_open_action':c,'detail':j.get('detail','')})
for body in [{'record-id':r0},{'*RecordIDs*':str(r0)}]:
 if sql(f"SELECT periodstatus FROM adempiere.c_periodcontrol WHERE c_periodcontrol_id={r0};")=='O':break
 proc=process(ta,'c_periodcontrol_process',body);obs.append({'native_open':proc,'parameter':body})
if sql(f"SELECT periodstatus FROM adempiere.c_periodcontrol WHERE c_periodcontrol_id={r0};")!='O':
 c,j=api(ta,'PUT','models/C_PeriodControl/'+str(r0),{'PeriodStatus':'O','PeriodAction':'N'});obs.append({'native_model_fixture_setup_if_process_unavailable':c,'detail':j.get('detail','')})
obs.append({'prepared':sql(f'SELECT periodstatus,periodaction FROM adempiere.c_periodcontrol WHERE c_periodcontrol_id={r0};')});save('t366-open-period.json',obs);print(obs[-1])
assert obs[-1]['prepared'].startswith('O|')
for q in rows("SELECT v.eva_validareprodusinv_id,v.m_inventoryline_id,v.m_inventory_id,v.eva_inventarprodus_id,d.m_warehouse_id,i.description FROM adempiere.eva_validareprodusinv v JOIN adempiere.m_inventory d ON d.m_inventory_id=v.eva_inventarprodus_id JOIN adempiere.m_inventory i ON i.m_inventory_id=v.m_inventory_id WHERE v.eva_starevalprodus='Q' AND i.description IN ('Q audit POS','Q audit NEG') ORDER BY 1;"):
 rid,line,src,native,whid=map(int,q[:5]);tag=q[5];sql(f"UPDATE a05_r2.t366_input SET act='REVERSE',rid={rid},line={line},doc={src} WHERE actor=102;")
 for k in ('first authorized reversal','repeat reversal'):
  v=process(tb,'testwms1967491',{});d=rows(f"SELECT m_inventory_id,reversal_id,docstatus,processed,posted FROM adempiere.m_inventory WHERE m_inventory_id={native} OR reversal_id={native} OR m_inventory_id=(SELECT reversal_id FROM adempiere.m_inventory WHERE m_inventory_id={native});")
  outcome={'tag':tag,'step':k,'response':v,'docs':[{'state':di,'transactions':dbtx(int(di[0])),'facts':dbfacts(int(di[0])),'mirror':mirror(int(di[0]))} for di in d],'validation_state':rows(f"SELECT eva_starevalprodus,isactive FROM adempiere.eva_validareprodusinv WHERE eva_validareprodusinv_id={rid};"),'source':query_snapshot(whid,123,src)}
  obs.append(outcome);save('t366-open-period.json',obs); print(tag,k,v['http'],v['error'],str(v['summary'])[:100],len(d))

