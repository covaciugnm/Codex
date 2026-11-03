import java.util.Properties;
import java.math.BigDecimal;
import java.sql.Timestamp;
import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;
import org.compiere.db.CConnection;
import org.compiere.model.*;
import org.compiere.util.*;
import org.compiere.Adempiere;

/** Uses original native classes, real OSGi factories, native DB adapter and transactions. */
public class A05NativePoProbe implements BundleActivator {
 static void check(boolean value,String message){if(!value)throw new AssertionError(message);}
 static MProduct make(Properties ctx,String value,String trx){
  MProduct p=new MProduct(ctx,0,trx);p.setAD_Org_ID(11);p.setValue(value);p.setName("A05 synthetic native "+value);
  p.setC_UOM_ID(100);p.setM_Product_Category_ID(DB.getSQLValueEx(null,"SELECT min(m_product_category_id) FROM m_product_category WHERE ad_client_id=11 AND isactive='Y'"));
  p.setC_TaxCategory_ID(DB.getSQLValueEx(null,"SELECT min(c_taxcategory_id) FROM c_taxcategory WHERE ad_client_id=11 AND isactive='Y'"));
  p.setProductType(MProduct.PRODUCTTYPE_Item);p.setIsStocked(true);p.setIsPurchased(true);p.setIsSold(true);return p;
 }
 public void start(BundleContext bundle)throws Exception{
  Ini.setClient(true);Ini.setAdempiereHome(System.getProperty("AdempiereHome"));
  CConnection cc=CConnection.get("PostgreSQL","127.0.0.1",56455,"idempiere","adempiere","A05SyntheticOnlyR12");DB.setDBTarget(cc);
  check(DB.isConnected(),"native DB connection");
  Properties ctx=Env.getCtx();
  Env.setContext(ctx,"#AD_Client_ID",11);Env.setContext(ctx,"#AD_Org_ID",11);Env.setContext(ctx,"#AD_User_ID",101);Env.setContext(ctx,"#AD_Role_ID",102);Env.setContext(ctx,"#AD_Language","en_US");Env.setContext(ctx,"#Date",new Timestamp(System.currentTimeMillis()));
  System.out.println("NATIVE_DB|"+DB.getDatabase().getClass().getName()+"|"+DB.getSQLValueStringEx(null,"SELECT current_database()||'|'||inet_server_addr()||'|'||inet_server_port()"));
  String build=DB.getSQLValueStringEx(null,"SELECT lastbuildinfo FROM ad_system");System.out.println("BUILD|DB="+build+"|JAR="+Adempiere.getVersion()+"|native_check="+DB.isBuildOK(ctx));
  System.out.println("ROLE|"+MRole.getDefault(ctx,false).getName()+"|client="+Env.getAD_Client_ID(ctx)+"|org="+Env.getAD_Org_ID(ctx)+"|user="+Env.getAD_User_ID(ctx));
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_user_roles WHERE ad_user_id=101 AND ad_role_id=102 AND isactive='Y'")==1,"actor role binding");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_client WHERE ad_client_id NOT IN(0,11)")==0,"only synthetic clients");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_scheduler WHERE isactive='Y'")==0,"schedulers off");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_client WHERE smtphost<>'127.0.0.1' OR smtpport<>1")==0,"email neutralized");
  ModelValidationEngine.get();
  String prefix="A05R12_"+System.currentTimeMillis();System.setProperty("A05_NATIVE_PRODUCT_PREFIX",prefix);
  String txName=Trx.createTrxName("A05_NATIVE_COMMIT");Trx tx=Trx.get(txName,true);int cpp,cpa;boolean committed=false;
  try{
   MProduct p=make(ctx,prefix+"_CPP",txName);p.saveEx();cpp=p.get_ID();
   MProduct a=make(ctx,prefix+"_CPA",txName);a.saveEx();cpa=a.get_ID();check(cpp!=cpa,"distinct native permanent row IDs");tx.commit(true);committed=true;
  }finally{if(!committed)tx.rollback();tx.close();}
  MProduct cppRead=new MProduct(ctx,cpp,null),cpaRead=new MProduct(ctx,cpa,null);
  check(cppRead.getValue().equals(prefix+"_CPP")&&cpaRead.getValue().equals(prefix+"_CPA"),"native PO readback");
  System.out.println("PO_COMMIT_READBACK|prefix="+prefix+"|CPP="+cpp+"|CPA="+cpa+"|distinct="+(cpp!=cpa));
  String rollbackName=Trx.createTrxName("A05_NATIVE_ROLLBACK");Trx rollback=Trx.get(rollbackName,true);int removed;
  try{MProduct p=make(ctx,prefix+"_ROLLBACK",rollbackName);p.saveEx();removed=p.get_ID();rollback.rollback();}finally{rollback.close();}
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM m_product WHERE m_product_id=?",removed)==0,"rollback persisted nothing");
  System.out.println("PO_ROLLBACK_READBACK|id="+removed+"|rows=0");
  String duplicateName=Trx.createTrxName("A05_NATIVE_DUPLICATE");Trx duplicate=Trx.get(duplicateName,true);boolean rejected=false;
  try{MProduct p=make(ctx,prefix+"_CPP",duplicateName);p.saveEx();}catch(RuntimeException expected){rejected=true;System.out.println("PO_DUPLICATE_REJECTED|"+expected.getClass().getName()+"|"+expected.getMessage());}finally{duplicate.rollback();duplicate.close();}
  check(rejected,"native duplicate must reject");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM m_product WHERE value=?",prefix+"_CPP")==1,"duplicate no persistent effect");
  String retryName=Trx.createTrxName("A05_NATIVE_RETRY");Trx retry=Trx.get(retryName,true);
  boolean retried=false;try{MProduct p=new MProduct(ctx,cpp,retryName);p.setDescription("A05 retry after rollback succeeded");p.saveEx();retry.commit(true);retried=true;}finally{if(!retried)retry.rollback();retry.close();}
  check("A05 retry after rollback succeeded".equals(new MProduct(ctx,cpp,null).getDescription()),"retry readback");
  System.out.println("PO_RETRY_READBACK|id="+cpp+"|PASS");
  System.out.println("NATIVE_PO_SMOKE|PASS|WMS_EVENTS_NOT_ENABLED|NO_DOCACTION_OR_FACT_ACCT_CREDIT");
 }
 public void stop(BundleContext context){DB.closeTarget();System.out.println("NATIVE_DB_TARGET_CLOSED");}
}
