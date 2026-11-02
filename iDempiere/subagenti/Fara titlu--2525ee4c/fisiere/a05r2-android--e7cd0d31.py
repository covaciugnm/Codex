from lab import *
ROLE_A=102; USER_A=101; READ_ROLE=103; READ_USER=102
A=auth('GardenAdmin',11,ROLE_A,11);R=auth('GardenUser',11,READ_ROLE,11)
d1='a09e2a05-2026-4000-8000-0000000000a1';dr='a09e2a05-2026-4000-8000-0000000000a2';d2='a09e2a05-2026-4000-8000-0000000000a3';k1='15afe7bc-45e0-487b-ac36-050000000001';k2='15afe7bc-45e0-487b-ac36-050000000002'
events=[]
def getapi(t,m,path,body,device,key):
 h={'X-Eva-Versiune-Aplicatie':'7','X-Eva-Dispozitiv':device}
 if key:h['Idempotency-Key']=key
 return http(m,'/eva-mobil/v1'+path,body,t,h)
def fixture_rights(wid):
 sql("UPDATE adempiere.ad_role SET eva_aplicatiemobila='Y' WHERE ad_client_id=11 AND ad_role_id IN(102,103);")
 for uid,rid,write in [(101,102,'Y'),(102,103,'N')]:
  c,j=api(A,'POST','models/EVA_AccesGestiune',{'AD_Org_ID':11,'AD_User_ID':uid,'M_Warehouse_ID':wid,'IsCitire':True,'IsScriere':write=='Y','IsValidare':False})
  if c not in (200,201):
   sql(f"INSERT INTO adempiere.eva_accesgestiune(eva_accesgestiune_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,ad_user_id,m_warehouse_id,iscitire,isscriere,isvalidare,eva_accesgestiune_uu) VALUES((SELECT coalesce(max(eva_accesgestiune_id),1700000)+1 FROM adempiere.eva_accesgestiune),11,11,now(),101,now(),101,'Y',{uid},{wid},'Y','{write}','N',gen_random_uuid());")
  events.append({'prepare':'mobile test fixture rights','role':rid,'user':uid,'write':write,'native_setup_http':c,'isolated_sql_fallback':c not in (200,201)})
def snapshot(did,loc,prod,whid,asi=0):
 return {'utc':now(),'warehouse':whid,'lines':rows(f"SELECT m_inventoryline_id,m_product_id,m_attributesetinstance_id,m_locator_id,qtybook,qtycount,updated FROM adempiere.m_inventoryline WHERE m_inventory_id={did} ORDER BY m_inventoryline_id;"),'txn':dbtx(did),'facts':dbfacts(did),'journal':rows(f"SELECT eva_idempotencykey,eva_starehttp,eva_rezultat,eva_amprentacerere FROM adempiere.eva_jurnalmobil WHERE eva_idempotencykey IN ('{k1}','{k2}') ORDER BY 1;"),'G1':g1(whid,prod),'G2':g2(whid,prod)}
def sent(tag,t,m,path,b,dev,k,docid,loc,pid,wid,asi):
 before=snapshot(docid,loc,pid,wid,asi);c,j=getapi(t,m,path,b,dev,k);after=snapshot(docid,loc,pid,wid,asi)
 safe={bk:bv for bk,bv in j.items() if 'token' not in bk.lower() and 'pass' not in bk.lower()}
 record={'tag':tag,'http':c,'canonical_payload':b,'sha256':digest(wire(b)),'response':safe,'key':k,'before':before,'after':after}
 events.append(record); save('android-results.json',events);print(tag,c, str(safe)[:145],flush=True);return c,j
def dev(t,d):
 return getapi(t,'POST','/dispozitive',{'identificator':d,'model':'AND-R2-synthetic','versiuneAplicatie':7},d,str(uuid.uuid4()))
stage='init'
try:
 wid,loc=wh(A,'AND-R2-A');loc2=new(A,'M_Locator',{'AD_Org_ID':11,'M_Warehouse_ID':wid,'Value':'ANDR2-L2','X':'R2','Y':'2','Z':'1'})
 fixture_rights(wid)
 lot='AND-R2-A05-X';asi=new(A,'M_AttributeSetInstance',{'AD_Org_ID':11,'M_AttributeSet_ID':101,'Lot':lot,'Description':lot,'GuaranteeDate':'2027-06-30'});pid=136
 bi,bl=inv(A,wid,loc,pid,0,20,'AND R2 initial +20',asi);br=doc(A,'M_Inventory',bi,'CO');assert br['http']==200,br
 did,line=inv(A,wid,loc,pid,20,20,'AND R2 canonical K1',asi)
 versions=sql(f"SELECT floor(extract(epoch FROM updated)*1000)::bigint::text||':20' FROM adempiere.m_inventoryline WHERE m_inventoryline_id={line};")
 b={'gestiune':wid,'locator':loc,'produs':pid,'lot':lot,'termen':'2027-06-30','cantitate':'18','versiune':versions}
 save('android-fixture.json',{'run_id':'AND-R2-20261102','device1':d1,'read_device':dr,'revoked_device':d2,'tenantA':11,'org':11,'userA':101,'roleA':102,'userRead':102,'roleRead':103,'warehouse':wid,'locator':loc,'locator2':loc2,'product':pid,'asi':asi,'draft':did,'line':line,'version':versions,'K1':k1,'K2':k2,'body_K1':b,'payload_K1_sha256':digest(wire(b)),'origin':'WMS synthetic isolated GardenWorld','api_path':'/eva-mobil/v1/inventar/pozitii'})
 for t,d,rname in [(A,d1,'writer'),(R,dr,'reader'),(A,d2,'revokable')]:
  c,j=dev(t,d);events.append({'registration':rname,'http':c,'response':{key:v for key,v in j.items() if 'token' not in key.lower()}});print('register',rname,c,str(j)[:110],flush=True)
  if rname=='writer' and c not in(200,201):raise RuntimeError('E4 refused '+str(j)[:220])
 stage='pre-send';before=snapshot(did,loc,pid,wid,asi);events.append({'tag':'offline before send','before':before,'after':snapshot(did,loc,pid,wid,asi),'actor':'no request submitted','server_observation_only':True})
 path='/inventar/pozitii'
 # Test-only trigger on this one draft row. Produces an error inside the server write transaction before commit.
 sql(f"""CREATE OR REPLACE FUNCTION adempiere.a05r2_android_fail() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN IF NEW.m_inventoryline_id={line} AND NEW.qtycount=18 THEN RAISE EXCEPTION 'AND03 isolated controlled rollback'; END IF; RETURN NEW; END$$;CREATE TRIGGER a05r2_android_fail BEFORE UPDATE OF qtycount ON adempiere.m_inventoryline FOR EACH ROW EXECUTE FUNCTION adempiere.a05r2_android_fail();""")
 sent('K1 forced rollback before commit',A,'POST',path,b,d1,k1,did,loc,pid,wid,asi)
 sql('DROP TRIGGER a05r2_android_fail ON adempiere.m_inventoryline; DROP FUNCTION adempiere.a05r2_android_fail();')
 stage='commit+replay'
 c,j=sent('K1 first valid commit; response ignored by simulated client',A,'POST',path,b,d1,k1,did,loc,pid,wid,asi)
 sent('K1 exact replay after committed response discarded',A,'POST',path,b,d1,k1,did,loc,pid,wid,asi)
 gate=threading.Barrier(2)
 def again(i):
  gate.wait();return getapi(A,'POST',path,b,d1,k1)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:tw=list(ex.map(again,[0,1]))
 events.append({'tag':'K1 same committed event concurrently re-delivered','results':[{'status':res[0],'response':res[1]} for res in tw],'after':snapshot(did,loc,pid,wid,asi)})
 sent('K1 changed to qty 17',A,'POST',path,dict(b,cantitate='17'),d1,k1,did,loc,pid,wid,asi)
 sent('reader role, K1 replay from writer',R,'POST',path,b,dr,k1,did,loc,pid,wid,asi)
 derived='EVA-MOBIL:'+hashlib.sha256(d2.encode()).hexdigest()
 dev_id=sql(f"SELECT min(mfa_registereddevice_id) FROM adempiere.mfa_registereddevice WHERE ad_client_id=11 AND mfadeviceidentifier='{derived}';")
 if dev_id:
  c,j=api(A,'PUT','models/MFA_RegisteredDevice/'+dev_id,{'IsActive':False})
  if c not in(200,201):sql(f"UPDATE adempiere.mfa_registereddevice SET isactive='N' WHERE mfa_registereddevice_id={int(dev_id)} AND ad_client_id=11;")
  sent('revoked device D2 replay K1',A,'POST',path,b,d2,k1,did,loc,pid,wid,asi)
 stage='finalization';events.append({'tag':'K1 finalize once','response':doc(A,'M_Inventory',did,'CO'),'after':snapshot(did,loc,pid,wid,asi)})
 events.append({'tag':'K1 finalize again','response':doc(A,'M_Inventory',did,'CO'),'after':snapshot(did,loc,pid,wid,asi)})
 dt=int(sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMI' AND docsubtypeinv='PI' AND isactive='Y';"))
 d2id=new(A,'M_Inventory',{'AD_Org_ID':11,'C_DocType_ID':dt,'M_Warehouse_ID':wid,'MovementDate':'2026-11-02','Description':'AND R2 separate K2'})
 b2={'gestiune':wid,'locator':loc2,'produs':124,'lot':None,'termen':None,'cantitate':'2','versiune':'0'}
 sent('legitimate new K2, separate draft/line',A,'POST',path,b2,d1,k2,d2id,loc2,124,wid,0)
except Exception as ex:events.append({'stage':stage,'error':str(ex)[:600]});print('ERROR ',stage,str(ex)[:300],flush=True)
finally:save('android-results.json',events)

