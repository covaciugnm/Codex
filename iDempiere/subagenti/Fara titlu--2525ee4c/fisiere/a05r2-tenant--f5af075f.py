from lab import *
x=json.loads((W/'android-fixture-valid.json').read_text());k=x['K1'];kneg='15afe7bc-45e0-487b-ac36-050000000018'
cl=int(sql("SELECT ad_client_id FROM adempiere.ad_client WHERE value='AUDITR2B';"))
assert cl>11
org=int(sql(f"SELECT min(ad_org_id) FROM adempiere.ad_org WHERE ad_client_id={cl} AND isactive='Y';"))
uid,rid=map(int,rows(f"SELECT u.ad_user_id,r.ad_role_id FROM adempiere.ad_user u JOIN adempiere.ad_user_roles ur ON ur.ad_user_id=u.ad_user_id JOIN adempiere.ad_role r ON r.ad_role_id=ur.ad_role_id WHERE u.ad_client_id={cl} AND u.name='AudR2BAdmin' AND r.name LIKE '%Admin' ORDER BY 2 LIMIT 1;")[0])
out=[];dd='a09e2a05-2026-4000-8000-0000000000b4';a=auth('GardenAdmin',11,102,11)
# Privately generated synthetic fixture identity from native Initial Tenant Setup. The password value is never recorded.
os.environ['A05_SYNTHETIC_USER_PASSWORD']='AudR2BAdmin'
try:
 b=auth('AudR2BAdmin',cl,rid,org)
 whb=sql(f"SELECT min(m_warehouse_id) FROM adempiere.m_warehouse WHERE ad_client_id={cl} AND isactive='Y';")
 assert whb, 'no stock location in synthetic tenant B'
 whb=int(whb);sql(f"UPDATE adempiere.ad_role SET eva_aplicatiemobila='Y' WHERE ad_client_id={cl} AND ad_role_id={rid};")
 c,j=api(b,'POST','models/EVA_AccesGestiune',{'AD_Org_ID':org,'AD_User_ID':uid,'M_Warehouse_ID':whb,'IsCitire':True,'IsScriere':True,'IsValidare':False})
 if c not in(200,201):
  sql(f"INSERT INTO adempiere.eva_accesgestiune(eva_accesgestiune_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,ad_user_id,m_warehouse_id,iscitire,isscriere,isvalidare,eva_accesgestiune_uu) VALUES((SELECT coalesce(max(eva_accesgestiune_id),1700000)+1 FROM adempiere.eva_accesgestiune),{cl},{org},now(),{uid},now(),{uid},'Y',{uid},{whb},'Y','Y','N',gen_random_uuid());")
 def request(t,m,path,body,d,key=None):
  hd={'X-Eva-Dispozitiv':d,'X-Eva-Versiune-Aplicatie':'7'}
  if key:hd['Idempotency-Key']=key
  return http(m,'/eva-mobil/v1'+path,body,t,hd)
 def state():
  return {'client_B':cl,'org_B':org,'wh_B':whb,'countA_docB_doc':rows(f"SELECT ad_client_id,count(*),sum(qtycount) FROM adempiere.m_inventoryline WHERE ad_client_id IN(11,{cl}) GROUP BY ad_client_id ORDER BY 1"),'lineA':rows(f"SELECT m_inventoryline_id,qtycount,qtybook FROM adempiere.m_inventoryline WHERE m_inventoryline_id={x['line']};"),'trxAB':rows(f"SELECT ad_client_id,count(*),sum(movementqty) FROM adempiere.m_transaction WHERE ad_client_id IN (11,{cl}) GROUP BY 1 ORDER BY 1;"),'factsAB':rows(f"SELECT ad_client_id,count(*),sum(amtacctdr),sum(amtacctcr) FROM adempiere.fact_acct WHERE ad_client_id IN(11,{cl}) GROUP BY 1 ORDER BY 1;")}
 for label,t,m,path,body,d,key in [('B register its device',b,'POST','/dispozitive',{'identificator':dd,'model':'B fixture','versiuneAplicatie':7},dd,str(uuid.uuid4())),('B authorized on own warehouse',b,'GET',f'/gestiuni/{whb}/locatori',None,dd,None),('B presents A K1, A record ids',b,'POST','/inventar/pozitii',x['body_K1'],dd,k),('A asks B locators',a,'GET',f'/gestiuni/{whb}/locatori',None,x['device1'],None),('A sends B warehouse id',a,'POST','/inventar/pozitii',dict(x['body_K1'],gestiune=whb),x['device1'],kneg)]:
  before=state();c,j=request(t,m,path,body,d,key);after=state();out.append({'case':label,'http':c,'response':j,'payload_sha256':digest(wire(body)) if body else None,'before':before,'after':after,'same_business_effect':before==after,'utc':now()});print(label,c,j.get('cod',''));save('android-tenant-boundary.json',out)
except Exception as e:out.append({'error':str(e)[:500]});save('android-tenant-boundary.json',out);print(out[-1])

