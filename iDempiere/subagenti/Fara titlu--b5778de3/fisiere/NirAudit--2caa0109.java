import java.math.BigDecimal;
import java.util.*;
import com.eva.ro.contab.documente.NirReceptie;
public class NirAudit {
 static Map<String,Object> line(String code,int q,int price) {
  Map<String,Object> m=new HashMap<>();m.put("cod",code);m.put("cant",BigDecimal.valueOf(q));m.put("pret",BigDecimal.valueOf(price));return m;
 }
 public static void main(String[] args) {
  for(String rec:new String[]{"7\n3","\n3","eroare\n3","7\n3\n99","0\n3","-2\n3"}) {
   var a=line("X",7,10);var b=line("Y",5,100);var model=new HashMap<String,Object>();model.put("bunuri",List.of(a,b));var form=new HashMap<String,Object>();form.put("receptionat",rec);NirReceptie.calculeaza(model,form);
   System.out.printf("%s|%s,%s|%s|%s%n",rec.replace("\n","/"),a.get("receptionat"),b.get("receptionat"),model.get("total_receptionat"),String.valueOf(form.get("diferente")).replace("\n"," / "));
  }
 }
}
