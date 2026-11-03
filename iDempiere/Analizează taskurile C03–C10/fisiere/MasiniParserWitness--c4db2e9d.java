import java.lang.reflect.Method;
import java.nio.file.*;
import java.security.Permission;
import java.time.LocalDate;
import java.time.format.*;
import java.util.*;

public class MasiniParserWitness {
  static class Guard extends SecurityManager {
    final Path root;
    Guard(Path p){root=p.toAbsolutePath().normalize();}
    public void checkPermission(Permission p){}
    public void checkPermission(Permission p,Object c){}
    public void checkConnect(String h,int p){throw new SecurityException("AUDIT_NETWORK_DENIED");}
    public void checkListen(int p){throw new SecurityException("AUDIT_LISTEN_DENIED");}
    public void checkAccept(String h,int p){throw new SecurityException("AUDIT_ACCEPT_DENIED");}
    public void checkExec(String c){throw new SecurityException("AUDIT_EXEC_DENIED");}
    public void checkWrite(String p){if(!Path.of(p).toAbsolutePath().normalize().startsWith(root))throw new SecurityException("AUDIT_WRITE_DENIED");}
    public void checkDelete(String p){checkWrite(p);}
  }
  interface Action {void run() throws Exception;}
  static void denied(String name,Action a)throws Exception{
    try{a.run();throw new AssertionError("guard failed:"+name);}catch(SecurityException expected){System.out.println("GUARD\t"+name+"\tBLOCKED");}
  }
  public static void main(String[]args)throws Exception{
    Path root=Path.of(args[0]).toAbsolutePath().normalize();
    System.setSecurityManager(new Guard(root));
    denied("network",()->{new java.net.Socket("192.0.2.1",443).close();});
    denied("listen",()->{new java.net.ServerSocket(0).close();});
    denied("exec",()->{new ProcessBuilder("cmd","/c","echo","synthetic").start();});
    denied("outside_write",()->Files.writeString(root.getParent().resolve("p01-r12-masini-canary-denied.txt"),"synthetic"));
    Class<?> c=Class.forName("com.eva.ro.contab.form.WSagaMasiniForm");
    System.out.println("CLASS\t"+c.getProtectionDomain().getCodeSource().getLocation());
    Method method=c.getDeclaredMethod("parseData",String.class);method.setAccessible(true);
    String[] inputs={"15.03.2027","29.02.2024","31.12.2026","01.01.2000","29.02.2000","29.02.1900","31.04.2027","29.02.2025","2027-03-15",""," ",null};
    LocalDate[] expected={LocalDate.of(2027,3,15),LocalDate.of(2024,2,29),LocalDate.of(2026,12,31),LocalDate.of(2000,1,1),LocalDate.of(2000,2,29),null,null,null,null,null,null,null};
    DateTimeFormatter comparator=DateTimeFormatter.ofPattern("dd.MM.uuuu").withResolverStyle(ResolverStyle.STRICT);
    for(int i=0;i<inputs.length;i++){
      Object actual=method.invoke(null,(Object)inputs[i]);LocalDate candidate=null;
      if(inputs[i]!=null&&!inputs[i].isEmpty())try{candidate=LocalDate.parse(inputs[i],comparator);}catch(DateTimeParseException e){}
      System.out.println("CASE\t"+i+"\t"+String.valueOf(inputs[i])+"\t"+String.valueOf(expected[i])+"\t"+String.valueOf(actual)+"\t"+String.valueOf(candidate)+"\t"+Objects.equals(expected[i],actual));
    }
    System.out.println("LIMIT\tOriginal private parser; no ZK session, PO save, database, role or persistence exercised. uuuu is a separate JDK comparator, not a product edit.");
  }
}
