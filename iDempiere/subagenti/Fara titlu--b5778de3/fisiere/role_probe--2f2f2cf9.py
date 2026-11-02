from lab import *
import json
assert W.name=='eva-contab-codex-p01uizk-r5.vUjauFBh' and cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-p01uizkr5'
assert rows("select ad_client_id,name from adempiere.ad_client order by 1;")==[['0','System'],['11','GardenWorld']]
dbroles=rows("select u.name,r.name,r.ad_role_id,ur.isactive from adempiere.ad_user u join adempiere.ad_user_roles ur using(ad_user_id) join adempiere.ad_role r using(ad_role_id) where u.name in ('GardenAdmin','GardenUser') and r.ad_role_id in (102,103) order by 1,3")
iv=1000002
related=rows("select i.c_bpartner_id,l.m_product_id,l.c_invoiceline_id from adempiere.c_invoice i join adempiere.c_invoiceline l using(c_invoice_id) where i.c_invoice_id=1000002 order by l.line")
assert len(related)==2
queries=[('Invoice','C_Invoice',iv),('Partner','C_BPartner',int(related[0][0])),('Product','M_Product',int(related[0][1])),('Line 1','C_InvoiceLine',int(related[0][2])),('Line 2','C_InvoiceLine',int(related[1][2]))]
out={'tag':'A04-R3-ROLES-API','utc':now(),'scope':'Read-only regular REST entry points on articles and synthetic invoice only. These are two authorized Garden roles; both belong to the same organization, so a 200 on both does not prove cross-tenant denial.','visible_grants':dbroles,'invoice':iv,'queries':[]}
for actor,rid in [('GardenAdmin',102),('GardenUser',103)]:
 token=auth(actor,11,rid,11)
 for tag,tab,i in queries:
  c,v=api(token,'GET',f'models/{tab}/{i}')
  cur=v.get('C_Currency_ID')
  out['queries'].append({'actor':actor,'role':rid,'client':11,'org':11,'method':'GET','route':f'models/{tab}/{i}','http':c,'id':v.get('id'),'message':str(v.get('detail',''))[:230],'currency':cur.get('id') if isinstance(cur,dict) else cur,'total':v.get('TotalLines'),'qty':v.get('QtyInvoiced')})
print(json.dumps(out,ensure_ascii=False,indent=2))
