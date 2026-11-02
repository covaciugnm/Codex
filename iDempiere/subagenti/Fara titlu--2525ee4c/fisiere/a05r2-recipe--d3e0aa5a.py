from lab import *
t=auth('GardenAdmin',11,102,11);run=[]
def emit(stage,record):run.append({'utc':now(),'stage':stage,**record});save('recipe-cost-cycle.json',run)
def snap(st,whid,pg,prod,box,setid):
 emit(st,{'g1':{str(k):g1(whid,k) for k in [prod,box,setid]},'g2':{str(k):g2(whid,k) for k in [prod,box,setid]},'native_stock_trx':rows(f"SELECT m_product_id,count(*),sum(movementqty) FROM adempiere.m_transaction t JOIN adempiere.m_locator l USING(m_locator_id) WHERE t.ad_client_id=11 AND l.m_warehouse_id={whid} AND t.m_product_id IN ({prod},{box},{setid}) GROUP BY 1 ORDER BY 1;"),'wms_moves':rows(f"SELECT eva_miscarewms_id,eva_tipmiscarewms,record_id,m_locator_id,m_locatorto_id,m_product_id,qty,eva_miscarewmsinversa_id FROM adempiere.eva_miscarewms WHERE m_warehouse_id={pg} AND ad_client_id=11 ORDER BY eva_miscarewms_id;"),'native_cost':rows(f"SELECT m_product_id,count(*),sum(amt),sum(qty) FROM adempiere.m_costdetail WHERE ad_client_id=11 AND m_product_id IN({prod},{box},{setid}) GROUP BY 1 ORDER BY 1;"),'facts':rows(f"SELECT count(*),coalesce(sum(amtacctdr),0),coalesce(sum(amtacctcr),0) FROM adempiere.fact_acct WHERE ad_client_id=11 AND m_product_id IN ({prod},{box},{setid});")})
try:
 prod=123;box=124;whid,l=wh(t,'R2NOTE')
 for p in (prod,box):
  did,li=inv(t,whid,l,p,0,12,'R2 WMS packing base '+str(p)); res=doc(t,'M_Inventory',did,'CO');assert res['http']==200,res
 pr=process(t,'eva_activarewms',{'M_Warehouse_ID':whid});emit('activate G2',{'response':pr})
 pg,loc,exp=map(int,rows(f"SELECT eva_gestiunewms_id,eva_locatorneamplasat_id,eva_locatorexpediere_id FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id={whid}")[0])
 src=get(t,'M_Product',prod);mb={'AD_Org_ID':11,'M_Product_Category_ID':ref(src['M_Product_Category_ID']),'C_TaxCategory_ID':ref(src['C_TaxCategory_ID']),'C_UOM_ID':ref(src['C_UOM_ID']),'ProductType':'I','IsStocked':False,'IsBOM':True}
 setid=new(t,'M_Product',dict(mb,Value='R2-NOTE-CPA',Name='R2 packed item CPP+box'))
 bom=new(t,'PP_Product_BOM',{'AD_Org_ID':11,'M_Product_ID':setid,'Name':'R2 CPP plus A1','Value':'R2-NOTE-B1','BOMType':'A','BOMUse':'A','C_UOM_ID':100})
 for i,p in enumerate([prod,box]):new(t,'PP_Product_BOMLine',{'AD_Org_ID':11,'PP_Product_BOM_ID':bom,'M_Product_ID':p,'C_UOM_ID':100,'QtyBOM':1,'Line':(i+1)*10,'ComponentType':'CO'})
 snap('BASELINE',whid,pg,prod,box,setid)
 payload={'M_Warehouse_ID':whid,'M_Product_ID':setid,'Qty':1,'M_Locator_ID':loc,'PP_Product_BOM_ID':bom}
 def req(label,tip,key,qty=1):
  body=dict(payload,EVA_TipNota=tip,Qty=qty); c,j=http('POST','/api/v1/processes/eva_notasetwms',body,t,{'Idempotency-Key':key})
  emit(label,{'key':key,'request_hash':digest(wire(body)),'http':c,'summary':j.get('summary',j.get('detail','')),'isError':j.get('isError'),'instance':j.get('AD_PInstance_ID',j.get('id'))});snap(label+'::snapshot',whid,pg,prod,box,setid)
 req('original real packing operation',1,'A05-R2-pack-original')
 req('same operation retry after success',1,'A05-R2-pack-original')
 req('legitimate new packing event',1,'A05-R2-pack-new')
 req('physical compensation once for mistaken duplicate',2,'A05-R2-unpack-compensation')
 emit('supports PInstance economic cancel? Definition of installed params',{'parameters':rows("SELECT columnname,ismandatory FROM adempiere.ad_process_para WHERE ad_process_id=(SELECT ad_process_id FROM adempiere.ad_process WHERE value='EVA_NotaSetWms') ORDER BY seqno;"),'type_resolution':'Tip=2 implements a fresh physical disassembly. It is not a native reversal referencing original note.'})
except Exception as ex:emit('ERROR',{'description':str(ex)[:800]});print('recipe error',str(ex)[:300])

