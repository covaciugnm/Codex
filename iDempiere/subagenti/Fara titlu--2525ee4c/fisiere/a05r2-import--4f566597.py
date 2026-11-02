from lab import *
t=auth('GardenAdmin',11,102,11);obs=[]
code='R2-A05-CPP-CODE'
s,j=api(t,'POST','models/I_Product',{'AD_Org_ID':11,'Value':code,'Name':'A05 imported record referring to previous code','ProductType':'I','C_UOM_ID':100,'M_Product_Category_ID':ref(get(t,'M_Product',123)['M_Product_Category_ID'])});obs.append({'stage':'create native import row','http':s,'id':j.get('id'),'detail':j.get('detail','')})
if s in (200,201):
 i=j['id'];before=rows(f"SELECT i_product_id,value,m_product_id,i_isimported FROM adempiere.i_product WHERE i_product_id={i};")
 params=rows("SELECT columnname,ismandatory FROM adempiere.ad_process_para WHERE ad_process_id=196 ORDER BY seqno;")
 c,j=api(t,'POST','processes/import_product',{'AD_Client_ID':11,'DeleteOldImported':False})
 obs.append({'params':params,'before':before,'http':c,'result_errors':j.get('isError'),'process_summary':j.get('summary',j.get('detail','')),'pinstance':j.get('AD_PInstance_ID',j.get('id'))})
 obs.append({'stage':'after import','staging':rows(f"SELECT i_product_id,value,m_product_id,i_isimported,left(coalesce(i_errormsg,''),200) FROM adempiere.i_product WHERE i_product_id={i};"),'product':rows(f"SELECT m_product_id,value,name,isactive FROM adempiere.m_product WHERE ad_client_id=11 AND value IN ('{code}','R2-A05-CPP-OLD') ORDER BY m_product_id;")})
save('identity-import.json',obs);print(json.dumps(obs)[:680])

