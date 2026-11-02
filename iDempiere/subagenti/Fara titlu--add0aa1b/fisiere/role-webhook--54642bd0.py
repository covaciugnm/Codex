from lab import *
assert PG.startswith('eva-test-p01-t220-') and rows("select ad_client_id,name from adempiere.ad_client order by 1")==[['0','System'],['11','GardenWorld']]
before=rows("select ad_role_id,name from adempiere.ad_role where ad_client_id=11 and name='Releu evenimente site'");r={'at':now(),'initial_roles':before,'steps':[]}
t=auth('GardenAdmin',11,102,11)
def ins(table,data):
 c,j=api(t,'POST','models/'+table,data);r['steps'].append({'table':table,'http':c,'reason':str(j.get('detail',''))[:400]});save('relay-role.json',r)
 if c not in (200,201):raise RuntimeError('Refuz '+table)
 return j
try:
 rid=int(before[0][0]) if before else ins('AD_Role',{'Name':'Releu evenimente site','AD_Org_ID':0,'UserLevel':' CO','IsManual':True,'IsAccessAllOrgs':False,'IsCanExport':False,'IsCanReport':False,'IsChangeLog':True,'IsActive':True})['id']
 r['fixture_role']=rid
 uid=int(sql("select ad_user_id from adempiere.ad_user where ad_client_id=11 and name='GardenUser'"))
 ins('AD_User_Roles',{'AD_Org_ID':0,'AD_Role_ID':rid,'AD_User_ID':uid});ins('AD_Role_OrgAccess',{'AD_Org_ID':11,'AD_Role_ID':rid,'IsReadOnly':False});ins('AD_Process_Access',{'AD_Org_ID':0,'AD_Role_ID':rid,'AD_Process_ID':1000168,'IsReadWrite':True})
 r['token_eligible']='GardenUser' if auth('GardenUser',11,rid,11) else None
except Exception as e:r['exception']=str(e)[:200]
save('relay-role.json',r);print(json.dumps(r))

