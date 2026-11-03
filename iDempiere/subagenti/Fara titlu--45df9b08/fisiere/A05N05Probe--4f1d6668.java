import java.util.*;
import java.math.BigDecimal;
import java.sql.*;
import java.lang.reflect.*;
import java.security.MessageDigest;
import java.util.concurrent.*;
import org.osgi.framework.*;
import org.adempiere.base.IProcessFactory;
import org.adempiere.base.event.*;
import org.adempiere.util.ServerContext;
import org.compiere.db.CConnection;
import org.compiere.model.*;
import org.compiere.process.*;
import org.compiere.util.*;
import org.eevolution.model.*;

/** Audit-only orchestration. All business methods are original core and exact Git EVA classes. */
public class A05N05Probe implements BundleActivator {
 BundleContext context;Bundle eva;Properties actor;ServiceRegistration<IProcessFactory> factoryReg;
 List<AbstractEventHandler> handlers=new ArrayList<>();
 static void check(boolean b,String s){if(!b)throw new AssertionError(s);}
 Class<?> c(String suffix)throws Exception{return eva.loadClass("com.eva.ro.contab."+suffix);}
 Object call(String suffix,String method,Class<?>[] types,Object... args)throws Exception{
  try{return c(suffix).getMethod(method,types).invoke(null,args);}catch(InvocationTargetException e){if(e.getCause() instanceof Exception x)throw x;if(e.getCause() instanceof Error x)throw x;throw e;}
 }
 static Properties actor(int user,int role){Properties p=new Properties();Env.setContext(p,"#AD_Client_ID",11);Env.setContext(p,"#AD_Org_ID",11);Env.setContext(p,"#AD_User_ID",user);Env.setContext(p,"#AD_Role_ID",role);Env.setContext(p,"#AD_Language","en_US");Env.setContext(p,"#Date",new Timestamp(System.currentTimeMillis()));return p;}
 static void set(Properties p){ServerContext.setCurrentInstance(p);}
 void identity(Class<?> k)throws Exception{
  String path="/"+k.getName().replace('.','/')+".class";byte[] b;try(var in=k.getResourceAsStream(path)){b=in.readAllBytes();}
  Bundle bound=FrameworkUtil.getBundle(k);
  System.out.println("CLASS_BINDING|"+k.getName()+"|bundle="+(bound==null?null:bound.getSymbolicName()+":"+bound.getVersion())+"|sha256="+HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(b))+"|codeSource="+k.getProtectionDomain().getCodeSource());
 }
 public void start(BundleContext bundle)throws Exception{try{startProbe(bundle);}catch(Throwable t){stop(bundle);if(t instanceof Exception x)throw x;if(t instanceof Error x)throw x;throw new RuntimeException(t);}}
 void startProbe(BundleContext bundle)throws Exception{
  context=bundle;for(Bundle b:bundle.getBundles())if(b.getSymbolicName().equals("com.eva.ro.contab"))eva=b;check(eva!=null&&eva.getState()==Bundle.RESOLVED,"EVA resolved dormant");
  Ini.setClient(false);Ini.setAdempiereHome(System.getProperty("AdempiereHome"));
  CConnection descriptor=CConnection.get("PostgreSQL","127.0.0.1",56455,"idempiere","adempiere","A05SyntheticOnlyR12");Ini.setProperty(Ini.P_CONNECTION,descriptor.toStringLong());DB.setDBTarget(descriptor);check(DB.isConnected(),"native DB connection");check(CConnection.get().getDbHost().equals("127.0.0.1")&&CConnection.get().getDbPort()==56455,"native default descriptor loopback");
  actor=actor(101,102);set(actor);
  System.out.println("NATIVE_DB|"+DB.getDatabase().getClass().getName()+"|"+DB.getSQLValueStringEx(null,"SELECT current_database()||'|'||inet_server_addr()||'|'||inet_server_port()"));
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_client WHERE ad_client_id NOT IN(0,11)")==0,"synthetic clients");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_scheduler WHERE isactive='Y'")==0,"schedulers disabled");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_client WHERE smtphost<>'127.0.0.1' OR smtpport<>1")==0,"mail neutralized");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_user_roles WHERE ad_user_id=101 AND ad_role_id=102 AND isactive='Y'")==1,"normal actor linked");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_modelvalidator WHERE ad_modelvalidator_id=50004 AND isactive='Y'")==1,"FixedAssets preserved");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_modelvalidator WHERE ad_modelvalidator_id=50000 AND isactive='N'")==1,"Libero preserved");
  System.out.println("BUILD_SCOPED_LIMIT|"+DB.getSQLValueStringEx(null,"SELECT version||'|'||releaseno||'|'||lastbuildinfo||'|FailOnDiffer='||isfailonbuilddiffer FROM ad_system")+"|native_permissive_check="+DB.isBuildOK(actor));
  ModelValidationEngine.get();StringBuffer info=new StringBuffer();ModelValidationEngine.get().getInfoDetail(info,actor);System.out.println("NATIVE_VALIDATORS|"+info);
  for(String n:List.of("corelare.NotaSetWmsProces","component.EvaProcessFactory","component.EvaNotaSetBomEvents","component.EvaWmsGardaEvents","component.EvaAuditPostareEvents","component.EvaStocEvents","form.ProceseEcran","wms.StocWms","wms.PerecheWms"))identity(c(n));
  identity(MPPProductBOMLine.class);identity(MProcess.class);identity(MPInstance.class);
  Field hook=c("corelare.NotaSetWmsProces").getDeclaredField("surseTest");hook.setAccessible(true);check(hook.get(null)==null,"SurseTest must stay null");System.out.println("SURSE_TEST|NULL");
  IProcessFactory factory=(IProcessFactory)c("component.EvaProcessFactory").getConstructor().newInstance();Dictionary<String,Object> props=new Hashtable<>();props.put("service.ranking",1);factoryReg=context.registerService(IProcessFactory.class,factory,props);
  for(String n:List.of("EvaNotaSetBomEvents","EvaWmsGardaEvents","EvaAuditPostareEvents","EvaStocEvents")){
   AbstractEventHandler h=(AbstractEventHandler)c("component."+n).getConstructor().newInstance();h.bindEventManager(EventManager.getInstance());handlers.add(h);
  }
  for(ServiceReference<?> ref:context.getAllServiceReferences("org.osgi.service.event.EventHandler",null)){
   Object h=context.getService(ref);if(handlers.contains(h))System.out.println("HANDLER_SERVICE|"+h.getClass().getName()+"|topics="+Arrays.deepToString(new Object[]{ref.getProperty("event.topics")})+"|filter="+ref.getProperty("event.filter"));context.ungetService(ref);
  }
  int process=DB.getSQLValueEx(null,"SELECT ad_process_id FROM ad_process WHERE value='EVA_NotaSetWms'");check(process>0,"process exists");
  ProcessCall actual=org.adempiere.base.Core.getProcess("com.eva.ro.contab.corelare.NotaSetWmsProces");check(actual!=null&&actual.getClass()==c("corelare.NotaSetWmsProces"),"native Core process factory binding");
  System.out.println("PROCESS_BINDING|id="+process+"|factory="+factory.getClass().getName()+"|class="+actual.getClass().getName()+"|role_access="+MRole.get(actor,102).getProcessAccess(process));
  check(Boolean.TRUE.equals(MRole.get(actor,102).getProcessAccess(process)),"normal role process access");
  check(!Boolean.TRUE.equals(MRole.get(actor(50001,50004),50004).getProcessAccess(process)),"negative role has no process access");
  System.out.println("READINESS_NATIVE|PASS|NO_BUSINESS_YET");
  if(System.getProperty("A05_N05_MODE").startsWith("business"))business(process);
 }
 record F(String tag,int g,int w,int loc,int piece,int set,int bom,int line){}
 MProduct product(String value,boolean set,String trx){
  MProduct p=new MProduct(actor,0,trx);p.setAD_Org_ID(11);p.setValue(value);p.setName(value);p.setC_UOM_ID(100);
  p.setM_Product_Category_ID(DB.getSQLValueEx(null,"SELECT min(m_product_category_id) FROM m_product_category WHERE ad_client_id=11 AND isactive='Y'"));
  p.setC_TaxCategory_ID(DB.getSQLValueEx(null,"SELECT min(c_taxcategory_id) FROM c_taxcategory WHERE ad_client_id=11 AND isactive='Y'"));
  p.setProductType("I");p.setIsStocked(!set);p.setIsBOM(set);p.setIsPurchased(!set);p.setIsSold(true);p.saveEx();return p;
 }
 F fixture(String tag)throws Exception{
  String name="N05_"+tag+"_"+System.currentTimeMillis();String t=Trx.createTrxName("N05_fixture");Trx tx=Trx.get(t,true);boolean ok=false;
  try{
   MProduct piece=product(name+"P",false,t),set=product(name+"S",true,t);
   MWarehouse g=new MWarehouse(actor,0,t);g.setAD_Org_ID(11);g.setValue(name);g.setName(name);g.setC_Location_ID(DB.getSQLValueEx(null,"SELECT min(c_location_id) FROM m_warehouse WHERE ad_client_id=11"));g.set_ValueOfColumn("EVA_TipEvidenta","CV");g.saveEx();
   MLocator l=new MLocator(g,"G1");l.setX("G1");l.setY("0");l.setZ("0");l.setIsDefault(true);l.saveEx();
   check(MStorageOnHand.add(actor,g.get_ID(),l.get_ID(),piece.get_ID(),0,BigDecimal.TEN,t),"synthetic stock add");
   MPPProductBOM bom=new MPPProductBOM(actor,0,t);bom.setAD_Org_ID(11);bom.setM_Product_ID(set.get_ID());bom.setValue(name+"B");bom.setName(name+"B");bom.setC_UOM_ID(100);bom.setBOMType("A");bom.setBOMUse("A");bom.setValidFrom(Timestamp.valueOf("2020-01-01 00:00:00"));bom.saveEx();
   MPPProductBOMLine line=new MPPProductBOMLine(bom);line.setAD_Org_ID(11);line.setLine(10);line.setM_Product_ID(piece.get_ID());line.setC_UOM_ID(100);line.setComponentType("CO");line.setQtyBOM(BigDecimal.valueOf(2));line.setIsQtyPercentage(false);line.setScrap(BigDecimal.ZERO);line.setValidFrom(Timestamp.valueOf("2020-01-01 00:00:00"));line.saveEx();
   Object result=call("wms.PerecheWms","activeaza",new Class<?>[]{Properties.class,int.class,int.class,String.class},actor,11,g.get_ID(),t);
   Object refusal=result.getClass().getMethod("refuz").invoke(result);check(refusal==null,"activate pair refusal "+refusal);
   Object pair=result.getClass().getMethod("pereche").invoke(result);int w=(Integer)pair.getClass().getMethod("gestiuneWms").invoke(pair),loc=(Integer)pair.getClass().getMethod("locatorNeamplasat").invoke(pair);
   F f=new F(tag,g.get_ID(),w,loc,piece.get_ID(),set.get_ID(),bom.get_ID(),line.get_ID());tx.commit(true);ok=true;System.out.println("FIXTURE_NATIVE|"+f);snapshot(f,"fixture",10,0,1);return f;
  }finally{if(!ok)tx.rollback();tx.close();}
 }
 ProcessInfoParameter[] params(F f,int typ,int qty){return new ProcessInfoParameter[]{new ProcessInfoParameter("M_Warehouse_ID",f.g,null,null,null),new ProcessInfoParameter("EVA_TipNota",typ,null,null,null),new ProcessInfoParameter("M_Product_ID",f.set,null,null,null),new ProcessInfoParameter("Qty",BigDecimal.valueOf(qty),null,null,null),new ProcessInfoParameter("M_Locator_ID",f.loc,null,null,null),new ProcessInfoParameter("PP_Product_BOM_ID",typ==2?f.bom:0,null,null,null)};}
 String tr(String key,Object...args)throws Exception{return (String)call("documente.Etichete","t",new Class<?>[]{String.class,Object[].class},key,args);}
 int normal(F f,int type,int qty,Properties ctx,String expected)throws Exception{
  set(ctx);int prior=DB.getSQLValueEx(null,"SELECT coalesce(max(ad_pinstance_id),0) FROM ad_pinstance");
  Object r=call("form.ProceseEcran","ruleaza",new Class<?>[]{Properties.class,String.class,String.class,ProcessInfoParameter[].class},ctx,"EVA_NotaSetWms","N05 "+f.tag,params(f,type,qty));
  boolean ok=r.getClass().getField("ok").getBoolean(r);String text=(String)r.getClass().getMethod("text").invoke(r);
  System.out.println("NORMAL_PROCESS|tag="+f.tag+"|type="+type+"|qty="+qty+"|actor="+Env.getAD_User_ID(ctx)+"|role="+Env.getAD_Role_ID(ctx)+"|ok="+ok+"|summary="+text);
  if(expected==null)check(ok,"normal process success "+text);else if(Env.getAD_Role_ID(ctx)==50004){check(Language.isBaseLanguage(Env.getAD_Language(ctx)),"negative oracle fixes native base language");check(!ok&&text.equals("EROARE la EVA_NotaSetWms: "+expected),"exact native access refusal "+expected+" actual="+text);}else check(!ok&&text.contains(expected),"exact expected refusal "+expected+" actual="+text);
  int id=DB.getSQLValueEx(null,"SELECT max(ad_pinstance_id) FROM ad_pinstance WHERE ad_pinstance_id>? AND ad_process_id=(SELECT ad_process_id FROM ad_process WHERE value='EVA_NotaSetWms')",prior);
  if(Env.getAD_Role_ID(ctx)==50004){check(id<=0,"native access denied before new instance");System.out.println("INSTANCE|NONE|native CannotAccessProcess before instance creation");set(actor);return 0;}
  check(id>prior,"new persisted process instance");System.out.println("INSTANCE|"+DB.getSQLValueStringEx(null,"SELECT ad_pinstance_id||'|process='||ad_process_id||'|client='||ad_client_id||'|user='||ad_user_id||'|result='||coalesce(result::text,'NULL')||'|params='||(SELECT count(*) FROM ad_pinstance_para p WHERE p.ad_pinstance_id=i.ad_pinstance_id) FROM ad_pinstance i WHERE ad_pinstance_id=?",id));set(actor);return id;
 }
 ProcessInfo coordinated(F f,int proc,Trx tx)throws Exception{
  ProcessInfo pi=new ProcessInfo("N05 "+f.tag,proc);pi.setAD_Client_ID(11);pi.setAD_User_ID(101);pi.setParameter(params(f,1,1));
  boolean ok=new MProcess(actor,proc,null).processIt(pi,tx,false);check(ok&&!pi.isError(),"managedFalse process "+pi.getSummary());
  System.out.println("COORDINATED_PROCESS|tag="+f.tag+"|instance="+pi.getAD_PInstance_ID()+"|trx="+tx.getTrxName()+"|managedTrx=false|"+DB.getSQLValueStringEx(tx.getTrxName(),"SELECT pg_backend_pid()||'|xid='||txid_current()||'|isolation='||current_setting('transaction_isolation')"));return pi;
 }
 void snapshot(F f,String label,int p,int s,int moves)throws Exception{
  try(Connection conn=DB.getConnection(true);Statement st=conn.createStatement()){
   check(conn.getAutoCommit(),"oracle connection autocommit");String q="SELECT pg_backend_pid(),coalesce((SELECT sum(qty) FROM eva_stocwms WHERE m_warehouse_id="+f.w+" AND m_product_id="+f.piece+"),0),coalesce((SELECT sum(qty) FROM eva_stocwms WHERE m_warehouse_id="+f.w+" AND m_product_id="+f.set+"),0),(SELECT count(*) FROM eva_miscarewms WHERE m_warehouse_id="+f.w+"),(SELECT qtybom FROM pp_product_bomline WHERE pp_product_bomline_id="+f.line+"),coalesce((SELECT sum(qtyonhand) FROM m_storageonhand WHERE m_product_id="+f.piece+"),0),(SELECT count(*) FROM fact_acct WHERE m_product_id IN("+f.piece+","+f.set+"))";
   try(ResultSet r=st.executeQuery(q)){r.next();System.out.println("PERSISTENT_SNAPSHOT|"+f.tag+"|"+label+"|pid="+r.getInt(1)+"|pieces="+r.getBigDecimal(2)+"|sets="+r.getBigDecimal(3)+"|moves="+r.getInt(4)+"|bomQty="+r.getBigDecimal(5)+"|nativeQty="+r.getBigDecimal(6)+"|facts="+r.getInt(7));check(r.getBigDecimal(2).compareTo(BigDecimal.valueOf(p))==0&&r.getBigDecimal(3).compareTo(BigDecimal.valueOf(s))==0&&r.getInt(4)==moves,"snapshot "+label);check(r.getBigDecimal(6).compareTo(BigDecimal.TEN)==0&&r.getInt(7)==0,"no native stock/accounting duplicate");}
  }
 }
 void change(F f,boolean expectedReject)throws Exception{
  String t=Trx.createTrxName("N05_BOM");Trx tx=Trx.get(t,true);boolean committed=false;
  try{MPPProductBOMLine line=new MPPProductBOMLine(actor,f.line,t);line.setQtyBOM(BigDecimal.valueOf(3));line.saveEx();check(!expectedReject,"used BOM unexpectedly editable");tx.commit(true);committed=true;System.out.println("BOM_CHANGE|"+f.tag+"|COMMITTED|pid="+DB.getSQLValueEx(null,"SELECT pg_backend_pid()"));}
  catch(org.adempiere.exceptions.AdempiereException e){String exact=tr("t355.refuz.lista_folosita");check(expectedReject&&e.getMessage()!=null&&e.getMessage().contains(exact),"wrong BOM rejection "+e);System.out.println("BOM_CHANGE|"+f.tag+"|REJECTED_EXACT|"+e.getClass().getName()+"|"+e.getMessage());}
  finally{if(!committed)tx.rollback();tx.close();}
 }
 void business(int process)throws Exception{
  int factsBefore=DB.getSQLValueEx(null,"SELECT count(*) FROM fact_acct");F serial;
  if(System.getProperty("A05_N05_MODE").equals("business_continuation")){serial=new F("serial",1000000,1000001,1000003,1000000,1000001,1000000,1000000);check(new MWarehouse(actor,serial.g,null).getValue().equals("N05_serial_1793668158122"),"bound immutable v1 fixture identity");snapshot(serial,"continued_v1_fixture",10,0,5);}
  else{serial=fixture("serial");int a=normal(serial,1,1,actor,null);snapshot(serial,"assembled",8,1,3);change(serial,true);snapshot(serial,"serial_guard",8,1,3);normal(serial,2,1,actor,null);snapshot(serial,"disassembled",10,0,5);
   normal(serial,1,0,actor,tr("t355.refuz.cantitate"));snapshot(serial,"N01_QTY",10,0,5);
   String code=new MProduct(actor,serial.piece,null).getValue();normal(serial,1,6,actor,tr("t355.refuz.piese",code,"2"));snapshot(serial,"N02_STOC",10,0,5);}
  Properties noRole=actor(50001,50004);check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_user_roles WHERE ad_user_id=50001 AND ad_role_id=50004 AND isactive='Y'")==1,"negative actor binding");String deny=Msg.getMsg(noRole,"CannotAccessProcess",new Object[]{"["+MProcess.get(noRole,process).getName()+"]",MRole.get(noRole,50004).getName()});normal(serial,1,1,noRole,deny);snapshot(serial,"N03_ROL",10,0,5);
  F rollback=fixture("rollback");Trx tx=Trx.get(Trx.createTrxName("N05_ROLLBACK"),true);try{coordinated(rollback,process,tx);snapshot(rollback,"before_rollback_invisible",10,0,1);tx.rollback();}finally{tx.close();}snapshot(rollback,"rolledback",10,0,1);
  normal(rollback,1,1,actor,null);snapshot(rollback,"retry_committed_once",8,1,3);
  F race=fixture("race");Trx t1=Trx.get(Trx.createTrxName("N05_RACE_T1"),true);ExecutorService es=Executors.newSingleThreadExecutor();Future<String> t2=null;boolean committed=false;
  try{
   ProcessInfo pi=coordinated(race,process,t1);System.out.println("T1_VISIBLE|"+DB.getSQLValueStringEx(t1.getTrxName(),"SELECT sum(qty)::text FROM eva_stocwms WHERE m_warehouse_id=? AND m_product_id=?",race.w,race.piece));snapshot(race,"barrier_T1_not_visible",10,0,1);
   t2=es.submit(()->{set(actor(101,102));String tn=Trx.createTrxName("N05_RACE_T2");Trx tt=Trx.get(tn,true);boolean done=false;try{System.out.println("T2_START|"+DB.getSQLValueStringEx(tn,"SELECT pg_backend_pid()||'|xid='||txid_current()||'|isolation='||current_setting('transaction_isolation')")+"|trx="+tn);MPPProductBOMLine line=new MPPProductBOMLine(Env.getCtx(),race.line,tn);line.setQtyBOM(BigDecimal.valueOf(3));line.saveEx();tt.commit(true);done=true;return "COMMITTED_QTY3";}catch(org.adempiere.exceptions.AdempiereException e){String exact=tr("t355.refuz.lista_folosita");if(e.getMessage()!=null&&e.getMessage().contains(exact))return "REJECTED_EXACT";throw e;}finally{if(!done)tt.rollback();tt.close();ServerContext.dispose();}});
   String second;
   try{second=t2.get(3,TimeUnit.SECONDS);}catch(TimeoutException waiting){System.out.println("T2_WAITING|pg_locks="+DB.getSQLValueStringEx(null,"SELECT coalesce(string_agg(pid||':'||locktype||':'||mode||':'||granted,','),'') FROM pg_locks WHERE pid IN(SELECT pid FROM pg_stat_activity WHERE datname=current_database())"));t1.commit(true);committed=true;second=t2.get(15,TimeUnit.SECONDS);}
   System.out.println("T2_RESULT|"+second);if(!committed){t1.commit(true);committed=true;}snapshot(race,"race_assembly_committed",8,1,3);normal(race,2,1,actor,null);
   if(second.equals("COMMITTED_QTY3")){snapshot(race,"RACE_DEFECT_11_FROM_10",11,0,5);System.out.println("FINDING_N05|CONFIRMED|native process + PO handler permit concurrent BOM edit causing 11 pieces from original 10");}else snapshot(race,"race_guard_conserved",10,0,5);
  }finally{if(!committed)t1.rollback();t1.close();if(t2!=null&&!t2.isDone())t2.cancel(true);es.shutdownNow();es.awaitTermination(10,TimeUnit.SECONDS);set(actor);}
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM fact_acct")==factsBefore,"global fact count unchanged after baseline");System.out.println("GLOBAL_FACT_COUNT|before="+factsBefore+"|after="+factsBefore);System.out.println("N05_CASES_COMPLETE|SERIAL_NEGATIVES_ROLLBACK_RETRY_RACE|NO_GLOBAL_WMS_RECEIPT");
 }
 public void stop(BundleContext context){
  for(AbstractEventHandler h:handlers)try{h.unbindEventManager(EventManager.getInstance());}catch(Exception e){System.out.println("HANDLER_CLEANUP_ERROR|"+e);}
  if(factoryReg!=null)factoryReg.unregister();DB.closeTarget();ServerContext.dispose();System.out.println("NATIVE_PROBE_CLEANUP|handlers_unbound|factory_unregistered|DB_closed");
 }
}
