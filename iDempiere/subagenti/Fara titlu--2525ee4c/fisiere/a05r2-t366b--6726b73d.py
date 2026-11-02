from lab import *
import itertools
ta=auth('GardenAdmin',11,102,11);tb=auth('GardenUser',11,103,11)
store=[]
def emit(kind,**kw):store.append({'utc':now(),'type':kind,**kw});save('t366-round2.json',store)
sql("CREATE SCHEMA IF NOT EXISTS a05_r2; CREATE TABLE IF NOT EXISTS a05_r2.t366_input(actor int PRIMARY KEY,act varchar(10),rid int,line int,doc int);")
groovy="""import org.osgi.framework.FrameworkUtil
import org.compiere.model.MTable
import org.compiere.util.Env
import org.compiere.util.DB
import org.compiere.util.Trx
def bund=FrameworkUtil.getBundle(MTable).getBundleContext().getBundles().find{it.getSymbolicName()=='com.eva.ro.contab'}
def v=bund.loadClass('com.eva.ro.contab.form.ValidareProdusInventar')
int u=Env.getAD_User_ID(Env.getCtx())
def x=DB.getSQLArrayObjectsEx(null,'SELECT act,rid,line,doc FROM a05_r2.t366_input WHERE actor=?',u)[0]
int rid=x[1] as int; int lin=x[2] as int; int doc=x[3] as int
switch(x[0]){
case 'PROPOSE':
 def tr=Trx.get(Trx.createTrxName('A05R2marker'),true)
 try { v.inregistreazaNumarator(11,11,doc,lin,u,tr.getTrxName());tr.commit(true) } finally { tr.close() }
 return 'proposed='+v.propune(lin)
case 'CONFIRM': return 'confirmed='+v.confirma(rid,'41000','56300')
case 'REVREQ': v.propuneAnulare(rid,'A05 recount correction');return 'reversal proposed'
case 'REVERSE':return 'reverse='+v.confirmaAnulare(rid)
default:throw new IllegalArgumentException('unsupported fixture action')
}"""
def bootstrap():
 quoted="'"+groovy.replace("'","''")+"'"; assert len(groovy)<4000
 for key in [1967491,1967492]:
  rule='groovy:TESTWMS'+str(key);val='TESTWMS'+str(key)
  sql(f"""BEGIN;
INSERT INTO adempiere.ad_rule(ad_rule_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,value,name,ruletype,eventtype,accesslevel,entitytype,script,ad_rule_uu) VALUES({key},0,0,now(),100,now(),100,'Y','{rule}','{val}','S','P','3','U',{quoted},gen_random_uuid());
INSERT INTO adempiere.ad_process(ad_process_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,value,name,accesslevel,entitytype,classname,isreport,isdirectprint,isbetafunctionality,isserverprocess,showhelp,copyfromprocess,ad_process_uu) VALUES({key},0,0,now(),100,now(),100,'Y','{val}','{val}','3','U','@script:{rule}','N','N','N','Y','N','N',gen_random_uuid());
INSERT INTO adempiere.ad_process_access(ad_process_id,ad_role_id,ad_client_id,ad_org_id,created,createdby,updated,updatedby,isactive,isreadwrite,ad_process_access_uu) SELECT {key},x,11,0,now(),100,now(),100,'Y','Y',gen_random_uuid() FROM unnest(ARRAY[102,103]) x;
COMMIT;""")
 emit('one-time fixture metadata cache reset',result=process(ta,'cache-reset',{}))
def setaction(act,uid,rid,line,did):
 assert act in ['PROPOSE','CONFIRM','REVREQ','REVERSE']
 sql(f"INSERT INTO a05_r2.t366_input VALUES({uid},'{act}',{rid},{line},{did}) ON CONFLICT(actor) DO UPDATE SET act=EXCLUDED.act,rid=EXCLUDED.rid,line=EXCLUDED.line,doc=EXCLUDED.doc;")
def invoke(tag,token,which=1):
 key=1967490+which;v=process(token,'testwms'+str(key),{});emit(tag,result=v);return v
def snap(tag,whid,p,did,line):
 ls=rows(f"SELECT eva_validareprodusinv_id,eva_tipvalprodus,eva_starevalprodus,coalesce(eva_inventarprodus_id,0),eva_propusvalde,eva_numaratde,isactive FROM adempiere.eva_validareprodusinv WHERE ad_client_id=11 AND m_inventoryline_id={line} ORDER BY eva_validareprodusinv_id;");docs=[];seen=set()
 for d in {int(l[3]) for l in ls if int(l[3])>0}:
  for row in rows(f"SELECT m_inventory_id,reversal_id,docstatus,processed,posted,xmin::text FROM adempiere.m_inventory WHERE m_inventory_id={d} OR reversal_id={d} OR m_inventory_id=(SELECT reversal_id FROM adempiere.m_inventory WHERE m_inventory_id={d}) ORDER BY 1;"):
   di=int(row[0]);
   if di not in seen:docs.append({'state':row,'txn':dbtx(di),'facts':dbfacts(di),'mirror':mirror(di)});seen.add(di)
 emit(tag,validations=ls,generated_docs=docs,source=query_snapshot(whid,p,did),list=did,line=line,wh=whid);return ls
def sc(tag,sgn):
 whid,loc=wh(ta,'Q'+tag);p=123;bid,bl=inv(ta,whid,loc,p,0,20,'Q opening '+tag);r=doc(ta,'M_Inventory',bid,'CO');assert r['http']==200,r
 r=process(ta,'eva_activarewms',{'M_Warehouse_ID':whid});emit(tag+' pair',result=r)
 did,line=inv(ta,whid,loc,p,20,20+sgn,'Q audit '+tag)
 setaction('PROPOSE',101,0,line,did);invoke(tag+' propose',ta);ls=snap(tag+' before confirmation',whid,p,did,line);pend=[l for l in ls if l[1]=='R' and l[2]=='P']
 if not pend:return
 rid=int(pend[0][0]);setaction('CONFIRM',101,rid,line,did);invoke(tag+' same user negative',ta);snap(tag+' after forbidden self-approval',whid,p,did,line)
 setaction('CONFIRM',102,rid,line,did);bar=threading.Barrier(2)
 def cn(i):
  tk=auth('GardenUser',11,103,11);bar.wait(timeout=7);return process(tk,'testwms'+str(1967491+i),{})
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(cn,[0,1]))
 emit(tag+' concurrent validation',responses=results);snap(tag+' result',whid,p,did,line)
 invoke(tag+' duplicate confirmation after commit',tb);snap(tag+' retry',whid,p,did,line)
 setaction('REVREQ',101,rid,line,did);invoke(tag+' request cancellation',ta);setaction('REVERSE',102,rid,line,did);invoke(tag+' reverse',tb);snap(tag+' reversed',whid,p,did,line)
 invoke(tag+' duplicate reverse',tb);snap(tag+' reversed twice result',whid,p,did,line)
if not rows('SELECT ad_process_id FROM adempiere.ad_process WHERE ad_process_id=1967491'):bootstrap()
for tag,sgn in [('POS',2),('NEG',-2),('ZERO',0)]:
 try:sc(tag,sgn)
 except Exception as ex:emit(tag+' error',detail=str(ex)[:800])
print('T366 events',len(store))

