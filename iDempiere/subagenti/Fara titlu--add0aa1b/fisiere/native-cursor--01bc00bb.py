from lab import *
import sys
stage=sys.argv[1];cfgfile='cursor-settings.json';key=(W/'cursorkey').read_text();t=auth('GardenAdmin',11,102,11)
assert PG.startswith('eva-test-p01-t220-') and sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
def snap():
 return {'rows':rows("select eva_sursa,eva_nrcomanda,eva_idextern,eva_comandasite_id,eva_actualizatsursa,eva_totalcomanda from adempiere.eva_comandasite where eva_sursa in ('CURSA','CURSB') order by eva_sursa,eva_nrcomanda"),'cursor':rows("select eva_sursa,eva_ultimaactualizare from adempiere.eva_sursasite where eva_sursa in ('CURSA','CURSB') order by eva_sursa")}
r={'stage':stage,'at':now(),'before':snap(),'process':None}
if stage=='setup':
 url=json.loads((W/cfgfile).read_text())['url']
 for alias,slug in [('CURSA','canal-a'),('CURSB','canal-b')]:
  body={'AD_Org_ID':11,'EVA_Sursa':alias,'EVA_Tenant':slug,'EVA_UrlApi':url,'EVA_Cheie':key,'EVA_Conturi':alias+'-OWN','EVA_Platforma':'CESIRO1','EVA_SursaProprie':True,'EVA_VanzariOnline':True,'EVA_ScrierePermisa':False,'EVA_Oprire':False,'EVA_StocSpreSite':False,'EVA_FisaSpreSite':False}
  c,d=api(t,'POST','models/EVA_SursaSite',body);assert c in(201,200),str(d.get('detail',''))[:120]
else:
 target='CURSB' if stage=='B-identity' else 'CURSA';si=int(sql("select eva_sursasite_id from adempiere.eva_sursasite where eva_sursa='%s' and ad_client_id=11" % target))
 if stage=='commit-before-cursor':
  sql("""CREATE FUNCTION adempiere.ex04_block_cursor() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF NEW.eva_sursa='CURSA' and NEW.eva_ultimaactualizare IS DISTINCT FROM OLD.eva_ultimaactualizare THEN RAISE EXCEPTION 'EX04 controlled failure after window commit'; END IF; RETURN NEW; END $$;
  CREATE TRIGGER ex04_block_cursor BEFORE UPDATE OF eva_ultimaactualizare ON adempiere.eva_sursasite FOR EACH ROW EXECUTE FUNCTION adempiere.ex04_block_cursor();""")
 try:
  c,j=api(t,'POST','processes/eva_preiadinsite',{'DateFrom':'2026-11-02','DateTo':'2026-11-02','Ce':'COMENZI','DoarVerifica':False,'EVA_SursaSite_ID':si});r['process']={'http':c,'error':j.get('isError'),'summary':str(j.get('summary',j.get('detail','')))[:1000],'instance':j.get('adPInstanceId')}
 finally:
  if stage=='commit-before-cursor':
   sql("DROP TRIGGER ex04_block_cursor ON adempiere.eva_sursasite; DROP FUNCTION adempiere.ex04_block_cursor();")
r['after']=snap();save('ex04-'+stage+'.json',r);print(json.dumps(r,default=str))

