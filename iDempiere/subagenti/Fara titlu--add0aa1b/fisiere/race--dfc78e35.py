from lab import *
assert PG.startswith('eva-test-p01-t220-') and sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
t=auth('GardenAdmin',11,102,11);t2=auth('GardenAdmin',11,102,11);key=(W/'cursorkey').read_text();url=json.loads((W/'cursor-settings.json').read_text())['url']
s_id=new(t,'EVA_SursaSite',{'AD_Org_ID':11,'EVA_Sursa':'CURRACE','EVA_Tenant':'canal-a','EVA_UrlApi':url,'EVA_Cheie':key,'EVA_Conturi':'CURRACE-OWN','EVA_Platforma':'CESIRO1','EVA_SursaProprie':True,'EVA_VanzariOnline':True,'EVA_ScrierePermisa':False,'EVA_Oprire':False,'EVA_StocSpreSite':False,'EVA_FisaSpreSite':False})
def snap():return {'rows':rows("select s.eva_idextern,s.eva_nrcomanda,s.eva_starecomanda,s.eva_comandasite_id,s.c_order_id,(select count(*) from adempiere.eva_comandasitelinie l where l.eva_comandasite_id=s.eva_comandasite_id) from adempiere.eva_comandasite s where s.eva_sursa='CURRACE' order by s.eva_idextern"),'cursor':rows("select eva_ultimaactualizare from adempiere.eva_sursasite where eva_sursa='CURRACE'"),'erp_order_count':sql("select count(*) from adempiere.c_order where ad_client_id=11")}
report={'at':now(),'source':s_id,'before':snap(),'induced_fault':'none; simultaneous real processes with independent ERP sessions reading the same own source'};bar=threading.Barrier(2)
def run(token,sync):
 if sync:bar.wait(timeout=3)
 c,j=api(token,'POST','processes/eva_preiadinsite',{'DateFrom':'2026-11-02','DateTo':'2026-11-02','Ce':'COMENZI','DoarVerifica':False,'EVA_SursaSite_ID':s_id});return {'http':c,'error':j.get('isError'),'summary':str(j.get('summary',j.get('detail','')))[:420]}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:report['concurrent']=list(ex.map(lambda token:run(token,True),(t,t2)))
report['immediately_after']=snap();report['replay']=run(t,False);report['after_replay']=snap();save('native-race.json',report);print(json.dumps(report['concurrent']),json.dumps(report['replay']),len(report['immediately_after']['rows']))

