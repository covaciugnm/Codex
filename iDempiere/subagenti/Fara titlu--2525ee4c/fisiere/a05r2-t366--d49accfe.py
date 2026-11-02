from lab import *
import itertools
tA=auth('GardenAdmin',11,102,11);tB=auth('GardenUser',11,103,11);store=[];seq=itertools.count(1967400)
def control(tag,body):
 id=next(seq);val='A05R2T366_'+str(id);rule='groovy:'+val
 script="""import org.osgi.framework.FrameworkUtil
import org.compiere.model.MTable
import org.compiere.util.Env
import org.compiere.util.Trx
def bund=FrameworkUtil.getBundle(MTable).getBundleContext().getBundles().find{it.getSymbolicName()=='com.eva.ro.contab'}
def v=bund.loadClass('com.eva.ro.contab.form.ValidareProdusInventar')
"""+body
 assert len(script)<4000;quoted="'"+script.replace("'","''")+"'"
 sql(f"""BEGIN;
INSERT INTO adempiere.ad_rule(ad_rule_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,value,name,ruletype,eventtype,accesslevel,entitytype,script,ad_rule_uu) VALUES({id},0,0,now(),100,now(),100,'Y','{rule}','{val}','S','P','3','U',{quoted},gen_random_uuid());
INSERT INTO adempiere.ad_process(ad_process_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,value,name,accesslevel,entitytype,classname,isreport,isdirectprint,isbetafunctionality,isserverprocess,showhelp,copyfromprocess,ad_process_uu) VALUES({id},0,0,now(),100,now(),100,'Y','{val}','{val}','3','U','@script:{rule}','N','N','N','Y','N','N',gen_random_uuid());
INSERT INTO adempiere.ad_process_access(ad_process_id,ad_role_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,isreadwrite,ad_process_access_uu) SELECT {id},x,11,0,now(),100,now(),100,'Y','Y',gen_random_uuid() FROM unnest(ARRAY[102,103]) x;
COMMIT;""")
 c,j=api(tA,'GET',f'processes?$filter=AD_Process_ID%20eq%20{id}')
 return (j.get('processes') or [{}])[0].get('slug') or val.lower()
def valrows(line):return rows(f"SELECT eva_validareprodusinv_id,eva_tipvalprodus,eva_starevalprodus,coalesce(eva_inventarprodus_id,0),eva_propusvalde,eva_numaratde,isactive FROM adempiere.eva_validareprodusinv WHERE ad_client_id=11 AND m_inventoryline_id={line} ORDER BY eva_validareprodusinv_id;")
def run_action(tag,t,slug):
 r=process(t,slug,{});store.append({'type':tag,'time':now(),'result':r});save('t366-results.json',store);return r
def snap(stage,whid,p,did,line):
 ls=valrows(line);docs=[];seen=set()
 for d in {int(l[3]) for l in ls if int(l[3])>0}:
  rs=rows(f"SELECT m_inventory_id,reversal_id,docstatus,processed,posted,xmin::text FROM adempiere.m_inventory WHERE m_inventory_id={d} OR reversal_id={d} OR m_inventory_id=(SELECT reversal_id FROM adempiere.m_inventory WHERE m_inventory_id={d}) ORDER BY 1;")
  for row in rs:
   di=int(row[0]); 
   if di not in seen:docs.append({'state':row,'txn':dbtx(di),'facts':dbfacts(di),'mirror':mirror(di)});seen.add(di)
 store.append({'type':stage,'at':now(),'list_id':did,'line_id':line,'validations':ls,'generated_documents':docs,'source_and_stocks':query_snapshot(whid,p,did)});save('t366-results.json',store)
def scenario(tag,sign):
 whid,loc=wh(tA,'V'+tag);p=123;base,bl=inv(tA,whid,loc,p,0,20,'R2 T366 baseline '+tag);op=doc(tA,'M_Inventory',base,'CO');assert op['http']==200,op
 pair=process(tA,'eva_activarewms',{'M_Warehouse_ID':whid});store.append({'type':'pair for '+tag,'result':pair})
 did,line=inv(tA,whid,loc,p,20,20+sign,'R2 T366 '+tag)
 scr=control(tag+' propose',f"""def tr=Trx.get(Trx.createTrxName('A05R2marker'),true)
try {{v.inregistreazaNumarator(11,11,{did},{line},Env.getAD_User_ID(Env.getCtx()),tr.getTrxName());tr.commit(true)}} finally {{tr.close()}}
return 'proposal='+v.propune({line})""")
 run_action(tag+' propose',tA,scr);snap(tag+' after proposal',whid,p,did,line)
 pending=[l for l in valrows(line) if l[1]=='R' and l[2]=='P']
 if not pending:store.append({'type':tag+' without actionable proposed row','observed':valrows(line)});return
 rid=int(pending[0][0]);cf=control(tag+' confirm',f"return 'confirmed='+v.confirma({rid},'41000','56300')")
 run_action(tag+' same counter attempt',tA,cf);snap(tag+' after same user refusal',whid,p,did,line)
 bar=threading.Barrier(2)
 def concur(i):
  t=auth('GardenUser',11,103,11);bar.wait();return process(t,cf,{})
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:sim=list(ex.map(concur,[0,1]))
 store.append({'type':tag+' concurrent production confirmations','result':sim});snap(tag+' after concurrency',whid,p,did,line)
 run_action(tag+' retry after commit',tB,cf);snap(tag+' after replay',whid,p,did,line)
 an=control(tag+' request reversal',f"v.propuneAnulare({rid},'A05 R2 recount correction');return 'void proposed'")
 rv=control(tag+' confirm reversal',f"return 'reverse result='+v.confirmaAnulare({rid})")
 run_action(tag+' request reversal',tA,an);run_action(tag+' confirm reversal',tB,rv);snap(tag+' after reversal',whid,p,did,line)
 run_action(tag+' replay reversal',tB,rv);snap(tag+' after reversal replay',whid,p,did,line)
for tt,qn in [('PLUS',2),('ZERO',0),('MINUS',-2)]:
 try:scenario(tt,qn)
 except Exception as e:store.append({'type':'scenario error '+tt,'detail':str(e)[:650]})
 save('t366-results.json',store);print('T366',tt,store[-1].get('type'),flush=True)

