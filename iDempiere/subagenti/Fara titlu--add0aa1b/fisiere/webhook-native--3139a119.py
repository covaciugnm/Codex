from lab import *
import base64,secrets,hmac
assert PG.startswith('eva-test-p01-t220-') and sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
q='ORD-2026-000001'; t=auth('GardenAdmin',11,102,11);secret=secrets.token_urlsafe(24);cab=str(uuid.uuid4());public=cab+'.'+uuid.uuid4().hex;sid=int(sql("select eva_sursasite_id from adempiere.eva_sursasite where ad_client_id=11 and eva_sursa='EX05A'"))
ref='04255ef2-38dd-446f-89a7-d369a1a67335'
r={'scope':'Independent synthetic event referencing the same C-Q business number, not evidence C actually emits the event. Event-side actor tested on private installation.','source_id':sid,'at':now()}
def snap():
 return {'event_states':rows("select eva_codeveniment,eva_nrcomanda,eva_stareeveniment from adempiere.eva_evenimentsite where eva_sursasite_id=%s and eva_nrcomanda='%s'"%(sid,q)),'order':rows("select eva_comandasite_id,eva_proprie,eva_starevalidare,c_order_id,m_inout_id,c_invoice_id from adempiere.eva_comandasite where eva_idextern='%s'"%ref),'stage_lines':sql("select count(*) from adempiere.eva_comandasitelinie l join adempiere.eva_comandasite s using(eva_comandasite_id) where s.eva_idextern='%s'"%ref),'global_order_count':sql("select count(*) from adempiere.c_order where ad_client_id=11")}
r['before']=snap()
old=rows("select eva_cheieapi_id from adempiere.eva_cheieapi where eva_sursasite_id=%d and eva_sens='IN'"%sid)
c,j=api(t,'PUT' if old else 'POST','models/EVA_CheieApi/'+old[0][0] if old else 'models/EVA_CheieApi',{'AD_Org_ID':11,'EVA_SursaSite_ID':sid,'EVA_Sens':'IN','EVA_IdCheie':public,'EVA_CabinetUuid':cab,'EVA_SecretCheie':secret})
r['key_setup_http']=c
if c in (200,201):
 uid=str(uuid.uuid4());tm=int(time.time()); d={'id':uid,'event':'order.updated','order_number':q,'updated_at':now(),'sent_at':now()};body=wire(d);mac=hmac.new(secret.encode(),str(tm).encode()+b'.'+body,digestmod='sha256').hexdigest()
 authparams={'CorpBase64':base64.b64encode(body).decode(),'Semnatura':mac,'Marcaj':str(tm),'IdCheie':public}
 r['attempts']=[]
 for name,who in [('wrong_role','GardenAdmin'),('signed_relay','relay'),('replay_relay','relay'),('role_read','GardenUser')]:
  token=t if who=='GardenAdmin' else auth('GardenUser',11,1000000 if who=='relay' else 103,11)
  c,v=api(token,'POST','processes/eva_primesteevenimentsite',authparams);r['attempts'].append({'case':name,'http':c,'process_error':v.get('isError'),'text':str(v.get('summary',v.get('detail','')))[:290].replace(public,'[fixture key id]').replace(secret,'[fixture]'),'persisted':snap()})
r['after']=snap();save('ex05-webhook.json',r);print(json.dumps(r,default=str))

