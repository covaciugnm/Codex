from lab import *
import concurrent.futures
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-a05r8'
assert sql("SELECT count(*) FROM adempiere.ad_scheduler WHERE isactive='Y'")=='0'
t=auth('GardenAdmin',11,102,11);out={'utc':now(),'scope':'Actor GardenAdmin; native APIs product, MLots/ASIs explicitly fixture, native receipt, missing lot, movement, inventory. GardenWorld native receiving, not the EVA Intrări/medical sale report. No direct DB inserts of business output.','photos':[],'ids':{},'events':[]}
def flush():save('lots_native.json',out)
def evt(k,v):out['events'].append({'action':k,'observed':v});flush()
def snap(k):
 p=out['ids']['product'];scope=f"AND t.m_product_id={p} AND t.ad_client_id=11"
 out['photos'].append({'stage':k,'mlot':rows(f"SELECT l.m_lot_id,l.name,asi.m_attributesetinstance_id,asi.guaranteedate::date FROM adempiere.m_lot l LEFT JOIN adempiere.m_attributesetinstance asi USING(m_lot_id) WHERE l.m_product_id={p} AND l.ad_client_id=11 ORDER BY 1,3"),
 'storage':rows(f"SELECT m_locator_id,m_attributesetinstance_id,qtyonhand FROM adempiere.m_storageonhand WHERE m_product_id={p} AND ad_client_id=11 ORDER BY 1,2"),
 'trx':rows(f"SELECT t.m_transaction_id,t.movementtype,t.m_attributesetinstance_id,t.movementqty,t.m_locator_id,t.m_inoutline_id,t.m_movementline_id,t.m_inventoryline_id FROM adempiere.m_transaction t WHERE 1=1 {scope} ORDER BY 1"),
 'cost':rows(f"SELECT d.m_costdetail_id,d.m_attributesetinstance_id,d.c_acctschema_id,d.qty,d.amt FROM adempiere.m_costdetail d WHERE d.m_product_id={p} AND d.ad_client_id=11 ORDER BY 1"),
 'strata':rows(f"SELECT m_attributesetinstance_id FROM adempiere.eva_stratstoc WHERE ad_client_id=11 AND m_product_id={p} ORDER BY 1"),'utc':now()});flush()
try:
 s=int(sql("SELECT min(m_attributeset_id) FROM adempiere.m_attributeset WHERE ad_client_id=11 AND description='EVA-P01.T329-LOT' AND islot='Y' AND isguaranteedate='Y'"));base=get(t,'M_Product',123);tag='R8L'+uuid.uuid4().hex[:7]
 p=new(t,'M_Product',{'AD_Org_ID':11,'Value':tag,'Name':tag,'IsStocked':True,'ProductType':'I','C_UOM_ID':100,'C_TaxCategory_ID':ref(base['C_TaxCategory_ID']),'M_Product_Category_ID':ref(base['M_Product_Category_ID']),'M_AttributeSet_ID':s});out['ids'].update(product=p,attribute_set=s)
 l=[]
 for k,day in [('L1',35),('L2',15)]:
  lot=new(t,'M_Lot',{'AD_Org_ID':11,'M_Product_ID':p,'Name':tag+k});a=new(t,'M_AttributeSetInstance',{'AD_Org_ID':11,'M_AttributeSet_ID':s,'M_Lot_ID':lot,'Lot':tag+k,'GuaranteeDate':str(datetime.date(2026,11,2)+datetime.timedelta(days=day))});l.append(a);out['ids'][k]={'lot':lot,'asi':a}
 bp,loc=120,101
 bpl=int(sql(f"SELECT c_bpartner_location_id FROM adempiere.c_bpartner_location WHERE c_bpartner_id={bp} AND ad_client_id=11 AND isactive='Y' ORDER BY 1 LIMIT 1"))
 def sh(k,lotlist):
  did=new(t,'M_InOut',{'AD_Org_ID':11,'M_Warehouse_ID':103,'C_BPartner_ID':bp,'C_BPartner_Location_ID':bpl,'MovementType':'V+','IsSOTrx':False,'C_DocType_ID':122,'MovementDate':'2026-11-02','DateAcct':'2026-11-02','Description':tag+k})
  for i,asi in enumerate(lotlist):
   new(t,'M_InOutLine',{'AD_Org_ID':11,'M_InOut_ID':did,'M_Product_ID':p,'M_Locator_ID':loc,'M_AttributeSetInstance_ID':asi,'MovementQty':10,'QtyEntered':10,'C_UOM_ID':100,'Line':10*(i+1)})
  out['ids'][k]=did;evt(k,doc(t,'M_InOut',did,'CO'))
 snap('two fixtures and no stock');sh('NIR_two_native_lots',l);snap('NIR two lines after CO attempt')
 try:sh('NIR_without_ASI',[0])
 except Exception as e:evt('NIR_without_ASI model refused',str(e)[:300])
 snap('after attempt with no ASI')
 wid,dst=wh(t,tag+'g');out['ids']['dest']=[wid,dst]
 dt=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMM' AND isactive='Y'"))
 mov=new(t,'M_Movement',{'AD_Org_ID':11,'C_DocType_ID':dt,'MovementDate':'2026-11-02','Description':tag});out['ids']['transfer']=mov
 ml=new(t,'M_MovementLine',{'AD_Org_ID':11,'M_Movement_ID':mov,'M_Product_ID':p,'M_Locator_ID':loc,'M_LocatorTo_ID':dst,'M_AttributeSetInstance_ID':l[0],'M_AttributeSetInstanceTo_ID':l[0],'MovementQty':4,'Line':10})
 evt('transfer four units of L1',doc(t,'M_Movement',mov,'CO'));snap('after move')
 pi,il=inv(t,wid,dst,p,4,5,tag+'inventory same L1',l[0]);out['ids']['PI']=pi;evt('PI count',doc(t,'M_Inventory',pi,'CO'));snap('after PI')
except Exception as e:out['limited']=str(e)[:550];flush()
