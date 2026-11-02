import java.math.BigDecimal;
import com.eva.ro.contab.date.BalantaService;
public class A11Precision {
 public static void main(String[] args) {
  for (String delta : new String[] {"0.000","0.002","-0.003","0.005","0.008","0.020"}) {
   var v = new BalantaService.Total();
   v.ruD = new BigDecimal("14.000").add(new BigDecimal(delta));
   v.ruC = new BigDecimal("14.000");
   System.out.println(delta + " " + v.egalitateRulaje());
  }
 }
}
