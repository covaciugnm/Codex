from lab import *
from decimal import Decimal
assert str(PG).startswith('eva-test-p01-t220-')
assert rows("select ad_client_id,name from adempiere.ad_client order by 1;")==[['0','System'],['11','GardenWorld']]
assert sql("select count(*) from adempiere.ad_scheduler where isactive='Y';")=='0'
r={'id':'A04-R2-PARTIAL-RETURN','utc':now(),'guard':'Only assigned isolated GardenWorld, schedulers disabled. GardenAdmin/102, client=org=11. SQL observations are SELECT; all documents created through the native REST model and DocAction.','records':[],'snapshots':{},'ids':{}}
a=r['ids'];t=auth('GardenAdmin',11,102,11);dt='2026-11-02';tag='A04-R2-RETURN';ids={}
def flush():save('a04-partial-return.json',r)
def event(method,url,data):
 c,j=api(t,method,url,data);state=j.get('DocStatus');status=state.get('id') if isinstance(state,dict) else state;r['records'].append({'method':method,'url':url,'input':data,'http':c,'id':j.get('id'),'status':status,'error':str(j.get('detail',j.get('summary','')))[:550]});flush();print(method,url,c,status,j.get('id'),str(j.get('detail',''))[:150],flush=True);return c,j
def mk(table,name,data):
 c,j=event('POST','models/'+table,{'AD_Org_ID':11,**data});assert c in (200,201),(table,name,c,str(j)[:450]);a[name]=j['id'];flush();return a[name]
def complete(table,pk):
 c,j=event('PUT','models/'+table+'/'+str(pk),{'doc-action':'CO'});d=j.get('DocStatus',{});assert c==200 and (d.get('id') if isinstance(d,dict) else d)=='CO',(table,c,str(j)[:220])
base={'C_BPartner_ID':114,'C_BPartner_Location_ID':109,'M_Warehouse_ID':103,'IsSOTrx':False,'Description':tag}
inv={'IsSOTrx':False,'AD_Org_ID':11,'C_BPartner_ID':114,'C_BPartner_Location_ID':109,'M_PriceList_ID':101,'C_Currency_ID':100,'C_PaymentTerm_ID':106,'SalesRep_ID':100,'DateInvoiced':dt,'DateAcct':dt,'Description':tag}
price={'M_Product_ID':128,'C_UOM_ID':100,'PriceList':25,'PriceActual':23.75,'PriceEntered':23.75,'C_Tax_ID':104}
def snap(key):
 c={};r['snapshots'][key]=c
 c['stock_locator']=sql("select coalesce(sum(qtyonhand),0) from adempiere.m_storageonhand where ad_client_id=11 and m_product_id=128 and m_locator_id=101;")
 if a.get('ol'):
  c['po']=rows("select o.docstatus,l.qtyordered,l.qtydelivered,l.qtyinvoiced from adempiere.c_order o join adempiere.c_orderline l using(c_order_id) where l.c_orderline_id=%d"%a['ol'])
  c['matches']=rows("select m_matchpo_id,m_inoutline_id,c_invoiceline_id,qty,processed from adempiere.m_matchpo where c_orderline_id=%d order by 1"%a['ol'])
 lines=[a[k] for k in ('rl1','rl2','retline') if k in a]
 if lines:
  j=','.join(map(str,lines));c['movements']=rows(f"select m_inoutline_id,movementtype,movementqty,m_locator_id from adempiere.m_transaction where m_inoutline_id in ({j}) order by 1;")
  c['matchinvs']=rows(f"select m_matchinv_id,m_inoutline_id,c_invoiceline_id,qty,posted from adempiere.m_matchinv where m_inoutline_id in ({j}) order by 1;")
 if a.get('rma'):
  c['rma']=rows("select h.m_rma_id,h.docstatus,l.m_rmaline_id,l.qty,l.qtydelivered,l.amt from adempiere.m_rma h left join adempiere.m_rmaline l using(m_rma_id) where h.m_rma_id=%d"%a['rma'])
 if a.get('invoice'):
  c['invoices']=rows("select h.c_invoice_id,h.c_doctype_id,h.docstatus,h.posted,h.grandtotal,h.issotrx,h.ref_invoice_id,h.m_rma_id from adempiere.c_invoice h where h.c_invoice_id in (%d,%d) order by 1"%(a['invoice'],a.get('credit',-1)))
 docs=" OR ".join("(t.tablename='%s' and f.record_id=%d)"%(tab,a[k]) for tab,k in [('M_InOut','rc1'),('M_InOut','rc2'),('M_InOut','ret'),('C_Invoice','invoice'),('C_Invoice','credit')] if k in a)
 if docs:c['postings']=rows("select t.tablename,f.record_id,f.c_acctschema_id,count(*),sum(f.amtacctdr),sum(f.amtacctcr) from adempiere.fact_acct f join adempiere.ad_table t using(ad_table_id) where "+docs+" group by 1,2,3 order by 1,2,3")
 flush()
try:
 snap('before')
 po=mk('C_Order','po',{**base,'C_DocTypeTarget_ID':126,'M_PriceList_ID':101,'C_Currency_ID':100,'C_PaymentTerm_ID':106,'SalesRep_ID':100,'DateOrdered':dt,'DateAcct':dt,'DatePromised':dt,'DeliveryRule':'A','DeliveryViaRule':'P','FreightCostRule':'I','InvoiceRule':'D'})
 ol=mk('C_OrderLine','ol',{**price,'C_Order_ID':po,'QtyOrdered':12,'QtyEntered':12,'Line':10});complete('C_Order',po);snap('po12')
 for i,n in enumerate([7,5],1):
  rec=mk('M_InOut','rc'+str(i),{**base,'C_DocType_ID':122,'MovementType':'V+','C_Order_ID':po,'MovementDate':dt,'DateAcct':dt})
  l=mk('M_InOutLine','rl'+str(i),{'M_InOut_ID':rec,'C_OrderLine_ID':ol,'M_Product_ID':128,'M_Locator_ID':101,'C_UOM_ID':100,'MovementQty':n,'QtyEntered':n,'Line':10});complete('M_InOut',rec);snap('receipt'+str(i))
 invoice=mk('C_Invoice','invoice',{**inv,'C_DocTypeTarget_ID':123,'C_Order_ID':po})
 for i,n in enumerate([7,5],1):
  mk('C_InvoiceLine','il'+str(i),{**price,'C_Invoice_ID':invoice,'M_InOutLine_ID':a['rl'+str(i)],'C_OrderLine_ID':ol,'QtyInvoiced':n,'QtyEntered':n,'Line':i*10})
 complete('C_Invoice',invoice);snap('full_purchase')
 rt=int(sql("select min(m_rmatype_id) from adempiere.m_rmatype where ad_client_id=11 and isactive='Y'"))
 hdr={'IsSOTrx':False,'C_DocType_ID':150,'M_RMAType_ID':rt,'InOut_ID':a['rc1'],'C_BPartner_ID':114}
 over=mk('M_RMA','over',{**hdr,'Name':'A04 over source 8'})
 c,j=event('POST','models/M_RMALine',{'AD_Org_ID':11,'M_RMA_ID':over,'M_InOutLine_ID':a['rl1'],'M_Product_ID':128,'Line':10,'Qty':8,'Amt':23.75})
 r['eight_vs_seven']={'http':c,'accepted_line':j.get('id'),'reason':str(j.get('detail',''))[:500]};flush()
 rid=mk('M_RMA','rma',{**hdr,'Name':'A04 return 2'})
 rl=mk('M_RMALine','rmaline',{'M_RMA_ID':rid,'M_InOutLine_ID':a['rl1'],'M_Product_ID':128,'Line':10,'Qty':2,'Amt':23.75});complete('M_RMA',rid)
 ret=mk('M_InOut','ret',{**base,'C_DocType_ID':151,'M_RMA_ID':rid,'Ref_InOut_ID':a['rc1'],'MovementType':'V-','MovementDate':dt,'DateAcct':dt})
 rlout=mk('M_InOutLine','retline',{'M_InOut_ID':ret,'M_RMALine_ID':rl,'Ref_InOutLine_ID':a['rl1'],'M_Product_ID':128,'M_Locator_ID':101,'C_UOM_ID':100,'QtyEntered':2,'MovementQty':2,'Line':10});complete('M_InOut',ret);snap('partial_return')
 cm=mk('C_Invoice','credit',{**inv,'C_DocTypeTarget_ID':124,'M_RMA_ID':rid,'Ref_Invoice_ID':invoice})
 mk('C_InvoiceLine','cl',{**price,'C_Invoice_ID':cm,'Ref_InvoiceLine_ID':a['il1'],'M_RMALine_ID':rl,'M_InOutLine_ID':rlout,'QtyInvoiced':2,'QtyEntered':2,'Line':10})
 complete('C_Invoice',cm);time.sleep(2);snap('credit')
 r['complete']=True
except Exception as ex:r['stopped']=str(ex)[:800]
finally:flush();print('RESULT',r.get('complete'),r.get('stopped'),flush=True)
