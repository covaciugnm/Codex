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
public class A05OsgiProbe {
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
   try(var paths=Files.list(Path.of(args[1]))){
    for(Path p:paths.filter(x->x.toString().endsWith(".jar")).sorted().toList()){
     if(p.getFileName().toString().startsWith("org.eclipse.osgi_"))continue;
     String fn=p.getFileName().toString();
     if(fn.startsWith("org.idempiere.")||fn.startsWith("com.trekglobal.")||fn.startsWith("com.eva."))continue;
     if(fn.startsWith("org.adempiere.")&&!fn.startsWith("org.adempiere.base_")&&!fn.startsWith("org.adempiere.base.process_"))continue;
     Bundle b=ctx.installBundle(p.toUri().toString());bundles.put(b.getSymbolicName(),b);
    }
   }
   System.out.println("BUNDLES_INSTALLED_DORMANT|"+bundles.size());
   List<String> active=List.of("org.apache.felix.scr","org.eclipse.equinox.event","org.adempiere.base","org.postgresql.jdbc","com.zaxxer.HikariCP","org.compiere.db.postgresql.provider");
   boolean resolved=framework.adapt(FrameworkWiring.class).resolveBundles(active.stream().map(bundles::get).toList());
   System.out.println("RESOLVE_NATIVE|"+resolved);
   for(String name:active){
    Bundle b=bundles.get(name);
    System.out.println("BUNDLE|"+name+"|state="+b.getState()+"|version="+b.getVersion());
    if(b.getState()==Bundle.INSTALLED){try{b.start();}catch(BundleException e){System.out.println("RESOLVE_ERROR|"+name+"|"+e.getMessage());}}
   }
   if(!resolved)throw new IllegalStateException("native-dependency-closure-incomplete");
   for(String name:active){Bundle b=bundles.get(name);b.start();System.out.println("STARTED|"+name+"|state="+b.getState());}
   for(int i=0;i<30;i++){ServiceReference<?>[] refs=ctx.getAllServiceReferences("org.compiere.db.AdempiereDatabase","(id=PostgreSQL)");if(refs!=null&&refs.length>0){Object service=ctx.getService(refs[0]);System.out.println("NATIVE_PG_PROVIDER|"+service.getClass().getName()+"|bundle="+refs[0].getBundle().getSymbolicName());break;}Thread.sleep(100);}
   Bundle base=bundles.get("org.adempiere.base");Class<?> db=base.loadClass("org.compiere.db.Database");
   Object provider=db.getMethod("getDatabase",String.class).invoke(null,"PostgreSQL");
   if(provider==null)throw new IllegalStateException("nativeServiceLocatorReturnedNull");
   System.out.println("NATIVE_SERVICE_LOCATOR|"+provider.getClass().getName());
   if(args[3].equals("po")){
    Bundle probe=ctx.installBundle(Path.of(args[4]).toUri().toString());probe.start();
   }
   for(Bundle b:ctx.getBundles())if(b.getState()==Bundle.ACTIVE)System.out.println("ACTIVE_END|"+b.getSymbolicName()+"|"+b.getVersion());
  }catch(Throwable t){outcome=1;System.out.println("PROBE_ERROR|"+t);t.printStackTrace(System.out);}finally{try{framework.stop();System.out.println("FRAMEWORK_STOP|"+framework.waitForStop(12000).getType());}finally{System.out.println("BOUNDARY_DENIALS|"+guard.refused);}}
  System.out.println("HARNESS_CONTROLLED_EXIT|"+outcome+"|native_static_executors_not_reused");guard.controlledExit=true;System.exit(outcome);
 }
}
