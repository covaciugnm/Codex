import java.math.BigDecimal;
import java.util.*;
import com.eva.ro.contab.corelare.*;
public class G3Probe {
 static BigDecimal d(long n){return BigDecimal.valueOf(n);}
 static List<SetLista.Componenta> bom(int q){return List.of(new SetLista.Componenta(11,d(q),true),new SetLista.Componenta(12,d(q),true),new SetLista.Componenta(13,d(q),true));}
 static String q(Map<Integer,BigDecimal> m){return SetLista.disponibilSet(m,bom(6))+"/"+SetLista.disponibilSet(m,bom(3));}
 static void chk(String id,String exp,Object val){System.out.println(id+" | expected="+exp+" | observed="+val+" | equals="+exp.equals(String.valueOf(val)));}
 public static void main(String[] a) {
  System.out.println("class_origin="+SetLista.class.getProtectionDomain().getCodeSource().getLocation());
  var pool=Map.of(11,d(120),12,d(120),13,d(120)); chk("G01 base S1/S2","20/40",q(pool));
  chk("G02 P2 negative literal","0/0",q(Map.of(11,d(120),12,d(-120),13,d(120))));
  chk("G03 mixed order residual theoretical, not DB reservation","13/27",q(Map.of(11,d(83),12,d(90),13,d(90))));
  chk("G04 remaining after allocation 1 S1","19/38",q(Map.of(11,d(114),12,d(114),13,d(114))));
  var repeated=List.of(new SetLista.Componenta(11,d(2),true),new SetLista.Componenta(11,d(4),true));
  chk("G05 repeated component consolidated","20",SetLista.disponibilSet(pool,repeated));
  chk("G06 empty component list","0",SetLista.disponibilSet(pool,List.of()));
  Map<String,String> rules=Map.of("EVA_StocRezerva","2","EVA_StocMaxim","7","EVA_StocRotunjire","JOS");
  chk("G07 reserve and cap integer piece","7",RegulaStocCanal.cantitateOferita(10,rules));
  chk("G08 pack-3 entered as rounding value (fixture contract)","6",RegulaStocCanal.cantitateOferita(10,Map.of("EVA_StocRezerva","2","EVA_StocMaxim","7","EVA_StocRotunjire","3")));
  System.out.println("G08 reason="+RegulaStocCanal.refuzRegula(Map.of("EVA_StocRotunjire","3")));
  chk("G09 aggregate independent snapshot warehouse 1","10/20",q(Map.of(11,d(60),12,d(60),13,d(60))));
  chk("G10 impossible one-site completeness","0/0",q(Map.of(11,d(120),12,d(0),13,d(0))));
 }
}
