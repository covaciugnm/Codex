from lab import *
t=auth('GardenAdmin',11,102,11);wid,loc=wh(t,'AND-AVD21');pid=125;uid=101;role=102;device='a09e2a05-2026-4000-8000-0000000000c1';key='15afe7bc-45e0-487b-ac36-050000000021'
c,j=api(t,'POST','models/EVA_AccesGestiune',{'AD_Org_ID':11,'AD_User_ID':uid,'M_Warehouse_ID':wid,'IsCitire':True,'IsScriere':True,'IsValidare':False})
if c not in(200,201):sql(f"INSERT INTO adempiere.eva_accesgestiune(eva_accesgestiune_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,ad_user_id,m_warehouse_id,iscitire,isscriere,isvalidare,eva_accesgestiune_uu) VALUES((SELECT coalesce(max(eva_accesgestiune_id),1700000)+1 FROM adempiere.eva_accesgestiune),11,11,now(),101,now(),101,'Y',{uid},{wid},'Y','Y','N',gen_random_uuid());")
base,bline=inv(t,wid,loc,pid,0,20,'A09 AVD21 opening');st=doc(t,'M_Inventory',base,'CO');assert st['http']==200,st
did,line=inv(t,wid,loc,pid,20,20,'A09 AVD21 separate draft');ver=sql(f"SELECT floor(extract(epoch FROM updated)*1000)::bigint::text||':20' FROM adempiere.m_inventoryline WHERE m_inventoryline_id={line};")
hdr={'X-Eva-Dispozitiv':device,'X-Eva-Versiune-Aplicatie':'7','Idempotency-Key':str(uuid.uuid4())}
c,j=http('POST','/eva-mobil/v1/dispozitive',{'identificator':device,'model':'R2-AVD-dedicated','versiuneAplicatie':7},t,hdr);assert c in(200,201),(c,j)
data={'key':key,'device':device,'role_id':102,'tenant':11,'org':11,'warehouse':wid,'locator':loc,'product':pid,'asi':0,'draft':did,'line':line,'version':ver,'payload':{'gestiune':wid,'locator':loc,'produs':pid,'lot':None,'termen':None,'cantitate':'18','versiune':ver},'before':query_snapshot(wid,pid,did)}
data['payload_hash']=digest(wire(data['payload']));save('avd21-fixture.json',data);print(json.dumps({k:v for k,v in data.items() if k not in ['before','payload']}))
# Token is synthetic and ephemeral, accessible to the private audit user only.
f=W/'avd21.token';f.write_text(t);f.chmod(0o600)

