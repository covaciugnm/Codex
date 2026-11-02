from lab import *
t=auth('GardenAdmin',11,102,11); src=get(t,'M_Product',123)
base={'AD_Org_ID':11,'M_Product_Category_ID':ref(src['M_Product_Category_ID']),'C_TaxCategory_ID':ref(src['C_TaxCategory_ID']),'C_UOM_ID':ref(src['C_UOM_ID']),'ProductType':'I','IsStocked':True}
a=[];code='R2-A05-CPP-CODE';newcode='R2-A05-CPP-OLD'
def attempt(tag,m,route,body):
 c,j=api(t,m,route,body);a.append({'tag':tag,'http':c,'id':j.get('id'),'detail':str(j.get('detail',''))[:280],'at':now()});save('identity-real.json',a);return c,j
c,j=attempt('CPP permanent identifier assigned','POST','models/M_Product',dict(base,Value=code,Name='R2 A05 CPP'));assert c in(200,201);orig=j['id']
c,j=attempt('distinct CPA','POST','models/M_Product',dict(base,Value='R2-A05-CPA-CODE',Name='R2 A05 CPA'));assert c in(200,201)
attempt('archive CPP','PUT','models/M_Product/'+str(orig),{'IsActive':False})
attempt('same original code blocked on archive','POST','models/M_Product',dict(base,Value=code,Name='R2 Duplicate'))
attempt('rename archived original','PUT','models/M_Product/'+str(orig),{'Value':newcode})
attempt('real new product takes old code','POST','models/M_Product',dict(base,Value=code,Name='R2 Replacement'))
attempt('reactivate original using renamed value','PUT','models/M_Product/'+str(orig),{'IsActive':True})
attempt('try restore first identifier to original','PUT','models/M_Product/'+str(orig),{'Value':code})
a.append({'native_ImportProduct_process':rows("SELECT value,classname,ad_process_id FROM adempiere.ad_process WHERE lower(classname) LIKE '%importproduct' OR value IN ('Import_Product','ImportProduct');")})
st,newi=attempt('create standard import staging row','POST','models/I_Product',{'AD_Org_ID':11,'Value':code,'Name':'R2 import arrival for old code','ProductType':'I','C_UOM_ID':100,'M_Product_Category_ID':ref(src['M_Product_Category_ID']),'C_TaxCategory_ID':ref(src['C_TaxCategory_ID'])})
if st in (200,201):
 iv=newi['id']; a.append({'before':rows(f"SELECT i_product_id,value,m_product_id,i_isimported FROM adempiere.i_product WHERE i_product_id={iv};")})
 proc=sql("SELECT lower(value) FROM adempiere.ad_process WHERE lower(classname)='org.compiere.process.importproduct' ORDER BY ad_process_id LIMIT 1;"); 
 if proc:a.append({'execution':process(t,proc,{'AD_Client_ID':11,'DeleteOldImported':False,'ImportDate':str(datetime.date.today())})})
 a.append({'after':rows(f"SELECT i_product_id,value,m_product_id,i_isimported,left(coalesce(i_errormsg,''),140) FROM adempiere.i_product WHERE i_product_id={iv};")})
a.append({'final':rows(f"SELECT m_product_id,value,name,isactive FROM adempiere.m_product WHERE ad_client_id=11 AND value IN('{code}','{newcode}','R2-A05-CPA-CODE') ORDER BY m_product_id;")})
save('identity-real.json',a);print('identity scenarios',len(a))

