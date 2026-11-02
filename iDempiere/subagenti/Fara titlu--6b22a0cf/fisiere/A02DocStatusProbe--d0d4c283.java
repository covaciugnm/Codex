import java.lang.reflect.Proxy;
import org.compiere.process.DocAction;
import org.compiere.process.DocumentEngine;
public class A02DocStatusProbe {
 public static void main(String[] args){
  for(String result:new String[]{"IP","WC","WP","IN"}){
   String[] po={"IP"};
   DocAction action=(DocAction)Proxy.newProxyInstance(DocAction.class.getClassLoader(),new Class[]{DocAction.class},(object,m,a)->{
    switch(m.getName()){case "completeIt": return result;case "getDocStatus":return po[0];case "setDocStatus":po[0]=(String)a[0];return null;default: if(m.getReturnType()==boolean.class)return false; if(m.getReturnType()==int.class)return 0;return null;}
   });
   DocumentEngine engine=new DocumentEngine(action,"IP");
   boolean accepted=engine.processIt("CO");
   System.out.println(result+"|"+accepted+"|"+po[0]+"|"+engine.getDocStatus());
  }
 }
}
