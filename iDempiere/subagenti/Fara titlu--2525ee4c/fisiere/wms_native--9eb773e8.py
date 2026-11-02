from lab import *
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-a05r8'
t=auth('GardenAdmin',11,102,11);o={'utc':now(),'events':[],'states':[]};tag='R8NC'+uuid.uuid4().hex[:7]
def record(k,c,j):o['events'].append({'case':k,'http':c,'id':j.get('id'),'state':j.get('DocStatus'),'error':j.get('isError'),'message':str(j.get('summary',j.get('detail','')))[:560]});save('wms_native.json',o)
before=json.loads((W/'cmp_result.json').read_text())['before'];extras={k for k in ['EVA_STRATURI_DE_LA','EVA_STRATURI_GENERATIE','EVA_METODA_DESCARCARE'] if k not in {row[1] for row in before}}
for key in extras:
  rows(f"UPDATE adempiere.ad_sysconfig SET isactive='N' WHERE ad_client_id=11 AND name='{key}' AND created>=date '2026-11-02' RETURNING ad_sysconfig_id")
g,l=wh(t,tag);sg,sl=wh(t,tag+'T');pr=123;opening,_=inv(t,g,l,pr,0,4,tag+'qty');o['opening']=doc(t,'M_Inventory',opening,'CO')
cfg=process(t,'eva_activarewms',{'M_Warehouse_ID':g});o['activate']=cfg
w,wl,wx=map(int,rows(f"SELECT eva_gestiunewms_id,eva_locatorneamplasat_id,eva_locatorexpediere_id FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id={g}")[0])
o['ids']={'g':g,'gl':l,'w':w,'w_neutral':wl,'w_dispatch':wx,'cv2':sg,'cv2l':sl}
def snapshot(label):
 o['states'].append({'step':label,'native_nonaccounting_onhand_rows':sql(f'SELECT count(*) FROM adempiere.m_storageonhand h JOIN adempiere.m_locator l USING(m_locator_id) WHERE h.ad_client_id=11 AND l.m_warehouse_id={w}'),'wms_g2':rows(f'SELECT m_product_id,m_locator_id,qty FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_warehouse_id={w} ORDER BY 1,2'),'gl_operational_tables':rows("SELECT t.tablename,count(f.fact_acct_id) FROM adempiere.ad_table t LEFT JOIN adempiere.fact_acct f ON f.ad_table_id=t.ad_table_id AND f.ad_client_id=11 WHERE t.tablename IN ('EVA_StocWms','EVA_MiscareWms') GROUP BY 1 ORDER BY 1"),'w_reservation':sql(f'SELECT count(*) FROM adempiere.m_storagereservation WHERE ad_client_id=11 AND m_warehouse_id={w}')});save('wms_native.json',o)
def call(k,m,route,data):c,j=api(t,m,route,data);record(k,c,j);return c,j
def run_doc(tab,rid,k):
 for ac in ('PR','CO'):call(k+' '+ac,'PUT',f'models/{tab}/{rid}',{'doc-action':ac})
def testmovement(k,from_l,to_l):
 dt=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMM' AND isactive='Y'"))
 c,h=call('movement '+k+' header','POST','models/M_Movement',{'AD_Org_ID':11,'C_DocType_ID':dt,'MovementDate':'2026-11-02','Description':tag+k})
 if c!=201:return
 did=h['id'];c,j=call('movement '+k+' line','POST','models/M_MovementLine',{'AD_Org_ID':11,'M_Movement_ID':did,'M_Product_ID':pr,'M_Locator_ID':from_l,'M_LocatorTo_ID':to_l,'MovementQty':1,'Line':10})
 if c!=201:return
 run_doc('M_Movement',did,'movement '+k);snapshot(k)
try:
 snapshot('paired eligible source')
 for k,fl,tl in [('CV-NC',l,wl),('NC-CV',wl,l),('NC-NC',wl,wx),('CV-CV',l,sl)]:testmovement(k,fl,tl)
 physicaltype=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMI' AND docsubtypeinv='PI' AND isactive='Y'"))
 c,h=call('NC native inventory header','POST','models/M_Inventory',{'AD_Org_ID':11,'M_Warehouse_ID':w,'C_DocType_ID':physicaltype,'MovementDate':'2026-11-02','Description':tag+'nc'})
 if c==201:
  rr=h['id'];call('NC inventory line','POST','models/M_InventoryLine',{'AD_Org_ID':11,'M_Inventory_ID':rr,'M_Product_ID':pr,'M_Locator_ID':wl,'QtyBook':0,'QtyCount':1,'Line':10});run_doc('M_Inventory',rr,'NC inventory');o['inventory_state']=rows(f"SELECT docstatus,processed,posted FROM adempiere.m_inventory WHERE m_inventory_id={rr}")
 for k,view,wanted in [('SO',True,'SO'),('PO',False,''),('binding quotation',True,'OB')]:
  if k=='SO':dt=132
  elif k=='PO':dt=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='POO' AND isactive='Y'"))
  else:dt=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docsubtypeso='OB' AND isactive='Y'"))
  c,h=call('NC '+k+' header','POST','models/C_Order',{'AD_Org_ID':11,'IsSOTrx':view,'C_DocTypeTarget_ID':dt,'M_Warehouse_ID':w,'C_BPartner_ID':112,'C_BPartner_Location_ID':108,'M_PriceList_ID':101,'C_Currency_ID':100,'C_PaymentTerm_ID':106,'SalesRep_ID':100,'DateOrdered':'2026-11-02','DateAcct':'2026-11-02','DatePromised':'2026-11-02','Description':tag+k,'POReference':tag+k})
  if c!=201:continue
  did=h['id'];c,j=call('NC '+k+' line','POST','models/C_OrderLine',{'AD_Org_ID':11,'M_Warehouse_ID':w,'C_Order_ID':did,'M_Product_ID':pr,'C_UOM_ID':100,'QtyOrdered':1,'QtyEntered':1,'PriceActual':10,'PriceEntered':10,'C_Tax_ID':104,'Line':10})
  run_doc('C_Order',did,'NC '+k);snapshot('after '+k)
 c,j=call('NC attempt to change registration despite W pair','PUT',f'models/M_Warehouse/{w}',{'EVA_TipEvidenta':'CV'})
 o['reg_after']=rows(f"SELECT m_warehouse_id,eva_tipevidenta FROM adempiere.m_warehouse WHERE m_warehouse_id IN ({g},{w}) ORDER BY 1")
except Exception as e:o['boundary']=str(e)[:600]
save('wms_native.json',o)
