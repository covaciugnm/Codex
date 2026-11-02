from lab import *
import traceback
assert 'a05-r8.' in str(W)
assert rows('SELECT ad_client_id,name FROM adempiere.ad_client ORDER BY 1')==[['0','System'],['11','GardenWorld']]
assert sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
out={'run':'A05-R8-E1','utc':now(),'scope':'private GardenWorld, authenticated API to genuine processes (ZK user actions recorded separately), seed-native accounts/cost and double schema; no external partners','queries':{},'events':[],'phases':{}}
def flush():save('native_inventory.json',out)
def q(k,s):v=rows(s);out['queries'][k]={'sql':s,'values':v,'utc':now()};flush();return v
def evt(label,v):out['events'].append({'utc':now(),'label':label,'result':v});flush()
q('T163-C28-AMERP',"SELECT ad_process_id,value,classname FROM adempiere.ad_process WHERE isactive='Y' AND (classname ILIKE '%amerp%react%' OR lower(value) LIKE '%react%produc%') ORDER BY 1")
q('metadata',"SELECT f.ad_form_id,m.ad_menu_id,m.name,f.classname FROM adempiere.ad_form f LEFT JOIN adempiere.ad_menu m USING(ad_form_id) WHERE f.classname LIKE '%WArticoleDiverseForm' OR f.classname LIKE '%WInventarForm' ORDER BY 1")
q('roles',"SELECT f.ad_form_id,a.ad_role_id,a.isreadwrite,a.isactive FROM adempiere.ad_form f LEFT JOIN adempiere.ad_form_access a USING(ad_form_id) WHERE f.classname LIKE '%WArticoleDiverseForm' ORDER BY 1,2")
q('period',"SELECT pc.c_periodcontrol_id,pc.periodstatus FROM adempiere.c_periodcontrol pc JOIN adempiere.c_period p USING(c_period_id) WHERE p.ad_client_id=11 AND p.startdate::date<=DATE '2026-11-02' AND p.enddate::date>=DATE '2026-11-02' AND pc.docbasetype='MMI' ORDER BY pc.c_periodcontrol_id")
q('setup_accounts',"SELECT c_elementvalue_id,value,c_element_id,accounttype,isactive FROM adempiere.c_elementvalue WHERE ad_client_id=11 AND value IN ('607','7588','6588') ORDER BY value")
q('prior_costs',"SELECT m_product_id,c_acctschema_id,currentcostprice FROM adempiere.m_cost WHERE ad_client_id=11 AND m_product_id IN (123,124) AND currentcostprice>0 ORDER BY 1,2")
q('costsetup',"SELECT c_elementvalue_id,c_element_id,value,accounttype FROM adempiere.c_elementvalue WHERE ad_client_id=11 AND issummary='N' AND isactive='Y' AND accounttype IN ('E','R') ORDER BY accounttype,c_elementvalue_id LIMIT 4")
q('process',"SELECT ad_process_id,value,classname FROM adempiere.ad_process WHERE value='EVA_ArticoleDiverse' AND isactive='Y'")
def work():
 t=auth('GardenAdmin',11,102,11);t2=auth('GardenAdmin',11,102,11)
 tag='R8I'+uuid.uuid4().hex[:7];wid,loc=wh(t,tag);out['ids']={'tag':tag,'wh':wid,'loc':loc,'x':123,'y':124}
 for label,typ in [('607','E'),('7588','R'),('6588','E')]:
  if not rows(f"SELECT c_elementvalue_id FROM adempiere.c_elementvalue WHERE ad_client_id=11 AND value='{label}' AND isactive='Y'"):
   element=int(sql("SELECT c_element_id FROM adempiere.c_elementvalue WHERE ad_client_id=11 AND isactive='Y' AND issummary='N' ORDER BY c_elementvalue_id LIMIT 1"))
   try:
    aid=new(t,'C_ElementValue',{'AD_Org_ID':0,'C_Element_ID':element,'Value':label,'Name':'A05 R8 '+label,'AccountType':typ,'AccountSign':'N','IsSummary':False});evt('fixture native C_ElementValue '+label,aid)
   except Exception as e:evt('could not prepare native account '+label,str(e)[:340])
 per=out['queries']['period']['values']
 if per and per[0][1]!='O':
  c,j=api(t,'PUT','models/C_PeriodControl/'+per[0][0],{'PeriodStatus':'O'});evt('synthetic MMI open via native REST PO',[c,j.get('detail','')])
 for pr in (123,124):
  did,li=inv(t,wid,loc,pr,0,10,'R8 T163 opening '+str(pr));evt('native opening inventory '+str(pr),doc(t,'M_Inventory',did,'CO'))
 xx=new(t,'M_Product',{'AD_Org_ID':11,'M_Product_Category_ID':ref(get(t,'M_Product',123)['M_Product_Category_ID']),'C_TaxCategory_ID':ref(get(t,'M_Product',123)['C_TaxCategory_ID']),'C_UOM_ID':100,'Value':tag+'N','Name':tag+' no cost','ProductType':'I','IsStocked':True,'IsActive':True});out['ids']['no_cost']=xx
 def do(tok,pos,day='2026-11-02'):
  return process(tok,'eva_articolediverse',{'Operatie':'PREGATESC','M_Warehouse_ID':wid,'Procedura':'P3','Pozitii':pos,'MovementDate':day})
 before=q('baseline',"SELECT coalesce(max(m_inventory_id),0),count(*) FROM adempiere.m_inventory WHERE ad_client_id=11")[0]
 evt('C14 no-cost',do(t,f'{loc}/{xx}/0=2'))
 q('C14-after',f"SELECT m_inventory_id,docstatus FROM adempiere.m_inventory WHERE ad_client_id=11 AND m_inventory_id>{int(before[0])}")
 evt('C25 closed/out-of-range period',do(t,f'{loc}/123/0=12','2101-01-02'))
 q('C25-after',f"SELECT m_inventory_id,docstatus FROM adempiere.m_inventory WHERE ad_client_id=11 AND m_inventory_id>{int(before[0])}")
 def snapshots(k):
  out['phases'][k]={'inventory':rows(f"SELECT d.m_inventory_id,d.docstatus,d.processed,d.posted,d.createdby,d.reversal_id,l.m_inventoryline_id,l.m_product_id,l.qtybook,l.qtycount,l.c_charge_id FROM adempiere.m_inventory d LEFT JOIN adempiere.m_inventoryline l USING(m_inventory_id) WHERE d.ad_client_id=11 AND d.m_warehouse_id={wid} AND d.m_inventory_id>{int(before[0])} ORDER BY 1,7"),
  'trx':rows(f"SELECT t.m_transaction_id,t.m_inventoryline_id,t.m_product_id,t.movementqty,t.m_attributesetinstance_id FROM adempiere.m_transaction t JOIN adempiere.m_inventoryline l USING(m_inventoryline_id) JOIN adempiere.m_inventory d USING(m_inventory_id) WHERE d.m_warehouse_id={wid} AND d.m_inventory_id>{int(before[0])} ORDER BY 1"),
  'gl':rows(f"SELECT f.fact_acct_id,f.record_id,f.line_id,f.c_acctschema_id,f.account_id,f.amtacctdr,f.amtacctcr FROM adempiere.fact_acct f JOIN adempiere.m_inventory d ON f.ad_table_id=321 AND f.record_id=d.m_inventory_id WHERE d.m_warehouse_id={wid} AND d.m_inventory_id>{int(before[0])} ORDER BY 1"),'stocks':rows(f"SELECT m_product_id,sum(qtyonhand) FROM adempiere.m_storageonhand WHERE m_locator_id={loc} AND m_product_id IN(123,124) GROUP BY 1 ORDER BY 1")};flush()
 snapshots('before preparations')
 gate=threading.Barrier(2)
 def attempt(tok):
  gate.wait(timeout=5);return do(tok,f'{loc}/123/0=12;{loc}/124/0=9')
 with concurrent.futures.ThreadPoolExecutor(2) as pool:both=list(pool.map(attempt,(t,t2)))
 evt('C13/C15 concurrent real process, two distinct sessions',both);snapshots('after race')
 res=out['phases']['after race']['inventory'];ids=sorted(set(int(x[0]) for x in res))
 if len(ids)==1:
  tested=ids[0];out['ids']['DR']=tested;evt('native document CO (separate from WInventar Validez)',doc(t,'M_Inventory',tested,'CO'));snapshots('after CO')
  evt('native document RC',doc(t,'M_Inventory',tested,'RC'));snapshots('after RC');evt('native doc RC retry',doc(t,'M_Inventory',tested,'RC'));snapshots('after RC retry')
 q('T329-EVA-set-scope',"SELECT ad_client_id,m_attributeset_id,islot,isguaranteedate,isserno,isinstanceattribute,mandatorytype,description FROM adempiere.m_attributeset WHERE ad_client_id=11 AND (islot='Y' OR description LIKE '%EVA-P01.T329-LOT%') ORDER BY 2")
try:work()
except Exception as e:out['limitation']=str(e)[:450];flush()
flush();print(json.dumps({'ids':out.get('ids'),'done':list(out['phases']),'error':out.get('limitation')},ensure_ascii=False))
