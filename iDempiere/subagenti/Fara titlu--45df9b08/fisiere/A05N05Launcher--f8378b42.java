import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.security.Permission;
import java.util.*;
import org.osgi.framework.*;
import org.osgi.framework.launch.*;
import org.osgi.framework.wiring.*;

/** Audit harness only. No replacement of native iDempiere logic. */
@SuppressWarnings("removal")
public class A05N05Launcher {
 static Path root;
 static int pgPort;
 static class Guard extends SecurityManager {
  int refused=0;
  boolean controlledExit=false;
  void refuse(String why){refused++;throw new SecurityException("A05_BOUNDARY:"+why);}
  public void checkPermission(Permission p){
   if(p instanceof FilePermission && (p.getActions().contains("write")||p.getActions().contains("delete"))) {
    Path target=Path.of(p.getName()).toAbsolutePath().normalize();
    if(!target.startsWith(root))refuse("write-outside-scratch");
   }
   if(p instanceof RuntimePermission && (p.getName().equals("setSecurityManager")||p.getName().equals("setIO")))refuse(p.getName());
  }
  public void checkConnect(String host,int port){if(!(host.equals("127.0.0.1")&&(port==pgPort||port==-1)))refuse("network:"+host+":"+port);}
  public void checkConnect(String host,int port,Object context){checkConnect(host,port);}
  public void checkListen(int port){refuse("listen:"+port);}
  public void checkAccept(String host,int port){refuse("accept");}
  public void checkMulticast(InetAddress addr){refuse("multicast");}
  public void checkExec(String cmd){refuse("exec");}
  public void checkExit(int code){if(!controlledExit)refuse("exit:"+code);}
 }
 interface Case {void run() throws Exception;}
 static void denied(String name,Case c)throws Exception{try{c.run();throw new AssertionError("CANARY_ESCAPED:"+name);}catch(SecurityException e){System.out.println("CANARY_DENIED|"+name+"|"+e.getMessage());}}
 public static void main(String[] args)throws Exception{
  root=Path.of(args[0]).toAbsolutePath().normalize();pgPort=Integer.parseInt(args[2]);
  if(!root.startsWith(Path.of("D:/CodexWork").toAbsolutePath().normalize())||!root.getFileName().toString().startsWith("a05-r12-native-lab-"))throw new IllegalArgumentException("scratch");
  Files.createDirectories(root);
  System.setProperty("user.home",root.toString());System.setProperty("user.dir",root.toString());
  System.setProperty("java.io.tmpdir",root.resolve("tmp").toString());Files.createDirectories(root.resolve("tmp"));
  System.setProperty("AdempiereHome",root.toString());System.setProperty("IDEMPIERE_HOME",root.toString());System.setProperty("java.awt.headless","true");
  Guard guard=new Guard();System.setSecurityManager(guard);
  denied("external_tcp",()->new Socket("192.0.2.1",443));
  denied("wrong_loopback_port",()->new Socket("127.0.0.1",pgPort+1));
  denied("listen",()->new ServerSocket(0));
  denied("udp",()->new DatagramSocket());
  denied("exec",()->new ProcessBuilder("A05_NONEXISTENT_CANARY").start());
  denied("outside_write",()->Files.writeString(root.getParent().resolve("a05-canary-outside-denied.txt"),"MUST_NOT_EXIST"));
  denied("guard_remove",()->System.setSecurityManager(null));
  Files.writeString(root.resolve("canary-allowed.txt"),"synthetic");
  System.out.println("CANARY_ALLOWED|scratch_write");
  if(args[3].equals("canary")){System.out.println("CANARIES_ONLY|DONE");return;}
  Map<String,String> config=new HashMap<>();
  config.put(Constants.FRAMEWORK_STORAGE,root.resolve("framework").toString());
  config.put(Constants.FRAMEWORK_STORAGE_CLEAN,"onFirstInit");
  config.put("osgi.instance.area",root.resolve("instance").toUri().toString());
  config.put("osgi.install.area",root.toUri().toString());
  config.put("osgi.framework.useSystemProperties","false");
  config.put("osgi.compatibility.bootdelegation","true");
  Framework framework=ServiceLoader.load(FrameworkFactory.class).iterator().next().newFramework(config);
  int outcome=0;
  try{
   framework.init();framework.start();BundleContext ctx=framework.getBundleContext();
   ctx.addFrameworkListener(e->{if(e.getThrowable()!=null)System.out.println("FRAMEWORK_EVENT|"+e.getType()+"|"+e.getThrowable());});
   Map<String,Bundle> bundles=new TreeMap<>();
   for(String cache:args[1].split(";"))try(var paths=Files.list(Path.of(cache))){
    for(Path p:paths.filter(x->x.toString().endsWith(".jar")).sorted().toList()){
     if(p.getFileName().toString().startsWith("org.eclipse.osgi_"))continue;
     String fn=p.getFileName().toString();
     if((fn.startsWith("org.idempiere.")&&!fn.startsWith("org.idempiere.zk."))||fn.startsWith("com.trekglobal.")||fn.startsWith("org.amerpsoft.")||fn.startsWith("a05-"))continue;
     if(fn.startsWith("org.adempiere.")&&!fn.startsWith("org.adempiere.base_")&&!fn.startsWith("org.adempiere.base.process_")&&!fn.startsWith("org.adempiere.ui_")&&!fn.startsWith("org.adempiere.ui.zk_")&&!fn.startsWith("org.adempiere.plugin.utils_")&&!fn.startsWith("org.adempiere.report.jasper")&&!fn.startsWith("org.adempiere.server_"))continue;
     Bundle b=ctx.installBundle(p.toUri().toString());bundles.put(b.getSymbolicName(),b);
     if(b.getSymbolicName().equals("com.eva.ro.contab")||b.getSymbolicName().startsWith("org.adempiere.ui")||b.getSymbolicName().startsWith("org.idempiere.zk.")||b.getSymbolicName().equals("org.adempiere.server"))b.adapt(org.osgi.framework.startlevel.BundleStartLevel.class).setStartLevel(50);
    }
   }
   System.out.println("BUNDLES_INSTALLED_DORMANT|"+bundles.size());
   List<String> active=List.of("org.apache.felix.scr","org.eclipse.equinox.event","org.adempiere.base","org.postgresql.jdbc","com.zaxxer.HikariCP","org.compiere.db.postgresql.provider");
   boolean resolved=framework.adapt(FrameworkWiring.class).resolveBundles(java.util.stream.Stream.concat(active.stream(),java.util.stream.Stream.of("com.eva.ro.contab")).map(bundles::get).toList());
   System.out.println("RESOLVE_NATIVE|"+resolved);
   for(String name:active){
    Bundle b=bundles.get(name);
    System.out.println("BUNDLE|"+name+"|state="+b.getState()+"|version="+b.getVersion());
    if(b.getState()==Bundle.INSTALLED){try{b.start();}catch(BundleException e){System.out.println("RESOLVE_ERROR|"+name+"|"+e.getMessage());}}
   }
   if(!resolved){for(Bundle b:ctx.getBundles())if(b.getState()==Bundle.INSTALLED){for(var req:b.adapt(BundleRevision.class).getDeclaredRequirements(null))if(!"optional".equals(req.getDirectives().get("resolution"))&&framework.adapt(FrameworkWiring.class).findProviders(req).isEmpty())System.out.println("MISSING_REQUIREMENT|"+b.getSymbolicName()+"|"+req);}throw new IllegalStateException("native-dependency-closure-incomplete");}
   for(String name:active){Bundle b=bundles.get(name);b.start();System.out.println("STARTED|"+name+"|state="+b.getState());}
   for(int i=0;i<30;i++){ServiceReference<?>[] refs=ctx.getAllServiceReferences("org.compiere.db.AdempiereDatabase","(id=PostgreSQL)");if(refs!=null&&refs.length>0){Object service=ctx.getService(refs[0]);System.out.println("NATIVE_PG_PROVIDER|"+service.getClass().getName()+"|bundle="+refs[0].getBundle().getSymbolicName());break;}Thread.sleep(100);}
   Bundle base=bundles.get("org.adempiere.base");Class<?> db=base.loadClass("org.compiere.db.Database");
   Object provider=db.getMethod("getDatabase",String.class).invoke(null,"PostgreSQL");
   if(provider==null)throw new IllegalStateException("nativeServiceLocatorReturnedNull");
   System.out.println("NATIVE_SERVICE_LOCATOR|"+provider.getClass().getName());
   for(String n:List.of("com.eva.ro.contab","org.adempiere.ui.zk","org.adempiere.server")){Bundle b=bundles.get(n);System.out.println("DORMANCY_BEFORE_PROBE|"+n+"|state="+b.getState()+"|startlevel="+b.adapt(org.osgi.framework.startlevel.BundleStartLevel.class).getStartLevel());if(b.getState()==Bundle.ACTIVE||b.getState()==Bundle.STARTING)throw new AssertionError("unexpected_activation:"+n);}
   System.setProperty("A05_N05_MODE",args[3]);
   if(!args[3].equals("resolve")){
    Bundle probe=ctx.installBundle(Path.of(args[4]).toUri().toString());probe.start();
   }
   if(bundles.get("com.eva.ro.contab").getState()==Bundle.ACTIVE||bundles.get("org.adempiere.ui.zk").getState()==Bundle.ACTIVE)throw new AssertionError("unexpected_EVA_or_UI_activation");
   for(Bundle b:ctx.getBundles())if(b.getState()==Bundle.ACTIVE)System.out.println("ACTIVE_END|"+b.getSymbolicName()+"|"+b.getVersion());
  }catch(Throwable t){outcome=1;System.out.println("PROBE_ERROR|"+t);t.printStackTrace(System.out);}finally{try{framework.stop();System.out.println("FRAMEWORK_STOP|"+framework.waitForStop(12000).getType());}finally{System.out.println("BOUNDARY_DENIALS|"+guard.refused);}}
  System.out.println("HARNESS_CONTROLLED_EXIT|"+outcome+"|native_static_executors_not_reused");guard.controlledExit=true;System.exit(outcome);
 }
}
