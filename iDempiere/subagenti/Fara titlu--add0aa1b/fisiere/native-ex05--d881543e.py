from lab import *
assert PG.startswith('eva-test-p01-t220-') and rows("select ad_client_id,name from adempiere.ad_client order by 1")==[['0','System'],['11','GardenWorld']] and sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
r={'at':now(),'events':[],'levels':{},'setup_errors':[],'case':'EX05','fixture_ips':json.loads((W/'relay-settings.json').read_text())}
def flush():save('native-ex05.json',r)
key=(W/'sourcekey').read_text();spec=json.loads((W/'fixture-q.json').read_text());ids=spec['ids'];slugs=spec['slugs'];t=auth('GardenAdmin',11,102,11)
def record(title,m,route,fields=None):
 code,j=api(t,m,route,fields);r['events'].append({'title':title,'route':route,'method':m,'http':code,'id':j.get('id'),'error':j.get('isError'),'summary':str(j.get('detail',j.get('summary','')))[:900].replace(key,'***'),'instance':j.get('adPInstanceId',j.get('AD_PInstance_ID'))});flush();return code,j
cols=rows("select table_name,string_agg(column_name,',' order by ordinal_position) from information_schema.columns where table_schema='adempiere' and table_name in ('eva_comandasite','eva_comandasitelinie','eva_sursasite') group by table_name order by 1")
r['columns_selected']={a:[x for x in c.split(',') if x in ('c_order_id','c_orderline_id','eva_idextern','eva_canal','eva_starevalidare','eva_sursa','eva_proprie','eva_idcomanda','eva_stat','m_product_id','m_inout_id','c_invoice_id','eva_comandasite_id','eva_nrcomanda','eva_moneda','eva_totalcomanda','eva_actualizatsursa','eva_sursasite_id','eva_ultimaactualizare','eva_ultimapreluare')] for a,c in cols}
def snapshot(stage):
 subs=','.join("'"+i+"'" for i in ids)
 cs=r['columns_selected']['eva_comandasite'];ls=r['columns_selected']['eva_comandasitelinie'];ss=r['columns_selected']['eva_sursasite']
 r['levels'][stage]={
 'stage_orders':rows('select '+','.join(cs)+' from adempiere.eva_comandasite where eva_idextern in ('+subs+') order by eva_sursa,eva_idextern'),
 'stage_lines':rows('select '+','.join('l.'+s for s in ls)+' from adempiere.eva_comandasitelinie l join adempiere.eva_comandasite s on s.eva_comandasite_id=l.eva_comandasite_id where s.eva_idextern in ('+subs+') order by l.eva_comandasite_id'),
 'physical_order_rows_in_sandbox':sql('select count(*) from adempiere.c_order where ad_client_id=11'),
 'physical_facts_rows_in_sandbox':sql('select count(*) from adempiere.fact_acct where ad_client_id=11'),
 'storage_reservation':rows('select issotrx,count(*),coalesce(sum(qty),0) from adempiere.m_storagereservation where ad_client_id=11 group by issotrx order by issotrx'),
 'source_metadata':rows('select '+','.join(ss)+' from adempiere.eva_sursasite where ad_client_id=11 order by eva_sursasite_id'),
 'scoped_role':'GardenAdmin, client 11 org 11','side_effects_scope':'Zero global change relative to initial count within disposable exclusive GardenWorld environment is a secondary indicator, not sole join evidence.'};flush()
try:
 snapshot('before_source')
 url=r['fixture_ips']['url'];sources={}
 for alias,slug in [('EX05A',slugs['A']),('EX05B',slugs['B'])]:
  old=rows("select eva_sursasite_id from adempiere.eva_sursasite where ad_client_id=11 and eva_sursa='%s'" % alias)
  if old:
   sources[alias]=int(old[0][0]); record('configure own fixture account '+alias,'PUT','models/EVA_SursaSite/'+str(sources[alias]),{'EVA_Conturi':alias+'-OWN'});continue
  c,j=record('source setup '+alias,'POST','models/EVA_SursaSite',{'AD_Org_ID':11,'EVA_Sursa':alias,'EVA_Tenant':slug,'EVA_UrlApi':url,'EVA_Cheie':key,'EVA_Platforma':'CESIRO1','EVA_SursaProprie':True,'EVA_VanzariOnline':True,'EVA_ScrierePermisa':False,'EVA_Oprire':False,'EVA_StocSpreSite':False,'EVA_FisaSpreSite':False})
  if c not in (200,201):raise RuntimeError('Source refuz '+str(r['events'][-1]))
  sources[alias]=j['id']
 r['source_ids']=sources
 for k in ['EX05A','EX05A','EX05B']:
  body={'DateFrom':'2026-11-02','DateTo':'2026-11-02','Ce':'COMENZI','DoarVerifica':False,'EVA_SursaSite_ID':sources[k]}
  code,j=record('preia comenzi '+k,'POST','processes/eva_preiadinsite',body);snapshot(k+'-'+str(len(r['events'])))
 s=rows("select eva_comandasite_id from adempiere.eva_comandasite where ad_client_id=11 and eva_idextern='%s' order by eva_comandasite_id limit 1" % ids[0])
 if s:
  code,j=record('validation on exact external order','POST','processes/eva_valideazacomenzi',{'Operatie':'VALIDEZ','Inregistrari':str(s[0][0])});snapshot('after_validation')
 r['completed']=True
except Exception as e:r['exception']=str(e)[:1000].replace(key,'***')
flush();print(json.dumps({'exception':r.get('exception'),'events':r['events'],'rows':{k:[len(v['stage_orders']),len(v['stage_lines']),v['physical_order_rows_in_sandbox']] for k,v in r['levels'].items()}},ensure_ascii=False))

