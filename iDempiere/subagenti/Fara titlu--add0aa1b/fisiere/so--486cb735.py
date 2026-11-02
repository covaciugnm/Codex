from lab import *
r={'id':'A06-SO-DRCO','utc':now(),'events':[],'snapshots':{},'fixture':'Exclusively owner-labeled GardenWorld independent cabinet; synthetic product with 6 pieces, Standard SO, no shipping/invoice auto.'}
def flush():save('a06-so-proof.json',r)
def record(t,method,route,body,hdr=None):
 c,j=http(method,'/api/v1/'+route,body,t,hdr);row={'route':route,'http':c,'id':j.get('id'),'DocStatus':j.get('DocStatus'),'reason':str(j.get('detail',j.get('summary','')))[:1200]};r['events'].append(row);flush();return c,j
def make(t,tab,fields,hdr=None):
 c,j=record(t,'POST','models/'+tab,fields,hdr);assert c in (200,201),(tab,r['events'][-1]);return j['id']
def act(t,tab,i,action):
 c,j=record(t,'PUT','models/'+tab+'/'+str(i),{'doc-action':action})
 status=j.get('DocStatus',{});return {'id':i,'http':c,'status':status.get('id') if isinstance(status,dict) else status,'summary':r['events'][-1]['reason']}
def snap(k):
 p=r['ids']['product'];o=r['ids'].get('orders',[]);ids=','.join(str(x) for x in o) or '-1'
 r['snapshots'][k]={'orders':rows('SELECT o.c_order_id,o.docstatus,o.posted,l.c_orderline_id,l.qtyordered,l.qtyreserved,l.qtydelivered,l.qtyinvoiced FROM adempiere.c_order o LEFT JOIN adempiere.c_orderline l USING(c_order_id) WHERE o.c_order_id IN ('+ids+') ORDER BY 1;'),'onhand':rows(f'SELECT s.m_locator_id,sum(s.qtyonhand) FROM adempiere.m_storageonhand s WHERE s.m_product_id={p} GROUP BY 1 ORDER BY 1;'),'reservations':rows(f'SELECT r.issotrx,r.m_warehouse_id,sum(r.qty) FROM adempiere.m_storagereservation r WHERE r.m_product_id={p} GROUP BY 1,2 ORDER BY 1,2;'),'sales_facts':rows('SELECT count(*) FROM adempiere.fact_acct f JOIN adempiere.ad_table t USING(ad_table_id) WHERE t.tablename=\'C_Order\' AND f.record_id IN ('+ids+');'),'deliveries':rows('SELECT count(*) FROM adempiere.m_inoutline l JOIN adempiere.c_orderline ol USING(c_orderline_id) WHERE ol.c_order_id IN ('+ids+');'),'invoices':rows('SELECT count(*) FROM adempiere.c_invoiceline l JOIN adempiere.c_orderline ol USING(c_orderline_id) WHERE ol.c_order_id IN ('+ids+');')};flush()
try:
 assert PG.startswith('eva-test-p01-t220-') and rows("select ad_client_id,name from adempiere.ad_client order by 1")==[['0','System'],['11','GardenWorld']]
 assert sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'; r['guards']={'pg_label':'eva-contab-codex-p01crossr2','schedulers':0,'client':'GardenWorld','image':cmd(['docker','inspect','--format','{{.Image}}',AP])}
 tag='A06-'+uuid.uuid4().hex[:8];r['tag']=tag;t=auth('GardenAdmin',11,102,11);t2=auth('GardenAdmin',11,102,11)
 p0=get(t,'M_Product',123);ids=r['ids']={};p=ids['product']=make(t,'M_Product',{'AD_Org_ID':11,'M_Product_Category_ID':ref(p0['M_Product_Category_ID']),'C_TaxCategory_ID':ref(p0['C_TaxCategory_ID']),'C_UOM_ID':100,'ProductType':'I','IsStocked':True,'IsActive':True,'Value':tag+'-CPP','Name':tag+' primary'})
 cpa=ids['cpa']=make(t,'M_Product',{'AD_Org_ID':11,'M_Product_Category_ID':ref(p0['M_Product_Category_ID']),'C_TaxCategory_ID':ref(p0['C_TaxCategory_ID']),'C_UOM_ID':100,'ProductType':'I','IsStocked':True,'IsActive':True,'Value':tag+'-CPA','Name':tag+' packed'})
 idag=sql("select c_doctype_id from adempiere.c_doctype where ad_client_id=11 and docbasetype='MMI' and isactive='Y' order by c_doctype_id limit 1;")
 inv=ids['inventory']=make(t,'M_Inventory',{'AD_Org_ID':11,'M_Warehouse_ID':103,'C_DocType_ID':int(idag),'MovementDate':'2026-11-02','Description':tag+' seed'})
 il=ids['inventory_line']=make(t,'M_InventoryLine',{'AD_Org_ID':11,'M_Inventory_ID':inv,'M_Product_ID':p,'M_Locator_ID':101,'QtyBook':0,'QtyCount':6,'Line':10})
 r['inventory_action']=act(t,'M_Inventory',inv,'CO');snap('before_order')
 assert sql(f'select coalesce(sum(qtyonhand),0) from adempiere.m_storageonhand where m_product_id={p}') and sum(float(x[1]) for x in r['snapshots']['before_order']['onhand'])==6,'Inv seed missing 6'
 order={'AD_Org_ID':11,'IsSOTrx':True,'C_DocTypeTarget_ID':132,'M_Warehouse_ID':103,'C_BPartner_ID':112,'C_BPartner_Location_ID':108,'M_PriceList_ID':101,'C_Currency_ID':100,'C_PaymentTerm_ID':106,'SalesRep_ID':100,'DateOrdered':'2026-11-02','DateAcct':'2026-11-02','DatePromised':'2026-11-02','Description':tag,'POReference':tag,'DeliveryRule':'A','DeliveryViaRule':'P','FreightCostRule':'I','InvoiceRule':'D'}
 pv=sql("select m_pricelist_version_id from adempiere.m_pricelist_version where m_pricelist_id=101 and isactive='Y' and validfrom<=date '2026-11-02' order by validfrom desc,m_pricelist_version_id desc limit 1")
 assert pv,'No active price list version'
 c,j=record(t,'POST','models/M_ProductPrice',{'AD_Org_ID':11,'M_Product_ID':p,'M_PriceList_Version_ID':int(pv),'PriceList':10,'PriceStd':10,'PriceLimit':0});assert c in (200,201),r['events'][-1]
 ids['orders']=[];ids['lines']=[]
 for token in (t,t2):
  k=make(token,'C_Order',order,{'Idempotency-Key':tag+'-request'});ids['orders'].append(k)
  if k not in ids['orders'][:-1]:ids['lines'].append(make(token,'C_OrderLine',{'AD_Org_ID':11,'C_Order_ID':k,'M_Product_ID':p,'C_UOM_ID':100,'QtyOrdered':6,'QtyEntered':6,'PriceActual':10,'PriceEntered':10,'PriceList':10,'C_Tax_ID':104,'Line':10}))
 snap('two_requests_before_CO')
 if len(set(ids['orders']))==2:
  bar=threading.Barrier(2)
  def run(a):bar.wait(timeout=8);return act(a[0],'C_Order',a[1],'CO')
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:r['compete']=list(ex.map(run,zip((t,t2),ids['orders'])))
 else:r['compete']=[act(t,'C_Order',ids['orders'][0],'CO')]
 snap('after_competing_CO')
 for failed in [x['id'] for x in r['compete'] if x['status']!='CO']:
  r.setdefault('repeat_CO_before_void',[]).append(act(t,'C_Order',failed,'CO'))
 snap('after_retry_before_void')
 role=rows("select u.ad_user_id,a.ad_role_id,a.name from adempiere.ad_user u join adempiere.ad_user_roles ur using(ad_user_id) join adempiere.ad_role a using(ad_role_id) where u.name='GardenUser' and ur.isactive='Y' and a.isactive='Y' and a.ad_client_id=11 order by a.ad_role_id limit 1")
 if role:
  r['role_probe']={'user':'GardenUser','role':role[0][2]};token=auth('GardenUser',11,int(role[0][1]),11)
  c,j=record(token,'GET',f'models/C_Order/{ids["orders"][0]}',None);r['role_probe']['get_order']=c
  c,j=record(token,'GET',f'models/C_OrderLine/{ids["lines"][0]}',None);r['role_probe']['get_line']=c
 k=next((x['id'] for x in r['compete'] if x['status']=='CO'),ids['orders'][-1]);r['void1']=act(t,'C_Order',k,'VO');snap('after_void_first');r['void2']=act(t,'C_Order',k,'VO');snap('after_void_retry')
 r['completed']=True
except Exception as e:r['incomplete']=str(e)[:1100]
flush();print(json.dumps({'id':r['id'],'finished':r.get('completed'),'error':r.get('incomplete'),'steps':len(r['events']),'ids':r.get('ids'),'snapshots':list(r['snapshots'])},ensure_ascii=False))

