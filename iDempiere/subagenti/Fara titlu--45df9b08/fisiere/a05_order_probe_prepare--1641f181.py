from pathlib import Path
W=Path('D:/CodexWork/a05-order-harness');P=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04/harness/A05G3Probe.java')
s=P.read_text(encoding='utf8').split(' record F(')[0]
s=s.replace('A05G3Probe','A05OrderProbe').replace('A05_G3_MODE','A05_ORDER_MODE')
s=s.replace('"component.EvaAuditPostareEvents"))identity(c(n));','"component.EvaAuditPostareEvents","component.EvaCanalB2BEvents","component.EvaSetLinieEvents","component.EvaLunaViitoareEvents","component.EvaLotExpiratEvents","component.EvaWmsOglindaEvents","corelare.GeneratorDocumente","corelare.Culegere","corelare.CanalB2B"))identity(c(n));')
s=s.replace('PO.class,IReservationTracer.class','PO.class,IReservationTracer.class,MOrder.class,MOrderLine.class,MInOut.class,MStorageReservationLog.class,org.adempiere.util.DefaultReservationTracerFactory.class,org.adempiere.util.ReservationLogTracer.class')
s=s.replace('List.of("EvaWmsGardaEvents","EvaStocEvents","EvaAuditPostareEvents")','List.of("EvaWmsGardaEvents","EvaStocEvents","EvaAuditPostareEvents","EvaCanalB2BEvents","EvaSetLinieEvents","EvaLunaViitoareEvents","EvaLotExpiratEvents","EvaWmsOglindaEvents")')
s=s.replace('System.out.println("READINESS_G3|PASS|NO_BUSINESS_YET|tracer=NULL|no_DocAction");','System.out.println("BINDING_ORDER|PASS|NO_BUSINESS_YET|schema_gate_separate");')
s=s.replace('if(System.getProperty("A05_ORDER_MODE").startsWith("business"))business();','if(System.getProperty("A05_ORDER_MODE").equals("migrate"))migrate();')
s+='''
 void migrate()throws Exception {
  Properties installation=new Properties();Env.setContext(installation,"#AD_Client_ID",0);Env.setContext(installation,"#AD_Org_ID",0);Env.setContext(installation,"#AD_User_ID",100);Env.setContext(installation,"#AD_Role_ID",0);Env.setContext(installation,"#AD_Language","en_US");ServerContext.setCurrentInstance(installation);
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM ad_role WHERE ad_role_id=0 AND ad_client_id=0 AND isactive='Y'")==1,"System role");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM eva_canalvanzare")==0,"No business channel completion");
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM eva_sursasite")==0,"No source endpoints");
  identity(c("setup.EvaMetadata"));identity(c("setup.EvaMetadata$Rezultat"));identity(c("corelare.CorelareTabele"));identity(c("corelare.OperatiiCanale"));identity(c("corelare.VanzariPeCanal"));
  Class<?> result=c("setup.EvaMetadata$Rezultat");
  for(int pass=1;pass<=2;pass++){
   Object r=result.getConstructor().newInstance();
   int n214=(Integer)call("setup.EvaMetadata","ensureT214",new Class<?>[]{Properties.class,String.class,result},installation,null,r);
   int n211=(Integer)call("setup.EvaMetadata","ensureT211Canale",new Class<?>[]{Properties.class,String.class,result},installation,null,r);
   String detail=String.valueOf(result.getField("log").get(r));System.out.println("MIGRATION_ORIGINAL|pass="+pass+"|T214="+n214+"|T211="+n211+"|log="+detail.replace('\\n',' '));
   check(detail.isBlank(),"Migration reports no suppressed error");if(pass==2)check(n214==0&&n211==0,"Original migration idempotent");
  }
  Field sql=c("corelare.CanalB2B").getField("SQL_STRUCTURA");check(DB.getSQLValueEx(null,(String)sql.get(null))==6,"B2B complete6");
  System.out.println("MIGRATION_FINISHED|NO_ORDER_TESTS|schema_readback_required");ServerContext.setCurrentInstance(actor);
 }
 public void stop(BundleContext ignored)throws Exception {for(AbstractEventHandler h:handlers)try{h.unbindEventManager(EventManager.getInstance());}catch(Throwable t){System.out.println("UNBIND_ERROR|"+t);}handlers.clear();ServerContext.dispose();}
}
'''
f=W/'A05OrderProbe.java';assert not f.exists();f.write_text(s,encoding='utf8');print('Prepared binding and gated migration modes only; not executed.')
