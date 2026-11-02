import com.eva.ro.contab.wms.*;
import com.eva.ro.contab.corelare.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;
public class WmsProbe {
  static BigDecimal b(int v) {return BigDecimal.valueOf(v);}
  static void result(String id, Object expected, Object actual) { System.out.println(id+" | expected="+expected+" | observed="+actual+" | equal="+expected.toString().equals(String.valueOf(actual))); }
  static SetLista.RandLista row(int p, String type, int qty) {return new SetLista.RandLista(p,b(qty),type,false,b(0),true,false,false);}
  static class Mem implements StocWms.Depozit {
    Map<String,StocWms.Rand> state=new LinkedHashMap<>(); int nb=0;
    String key(int loc,int p,int asi,int bom){return loc+"."+p+"."+asi+"."+bom;}
    public Set<Integer> locatori(int c,int w){return Set.of(20,21,22,23);}
    public boolean produsActiv(int c,int p){return true;}
    public void lacat(String k){}
    public StocWms.Rand citesteBlocat(int c,int loc,int p,int asi,int bom){return state.get(key(loc,p,asi,bom));}
    public void scrieStoc(int c,int w,int l,int p,int a,int v,BigDecimal q,StocWms.Rand old){state.put(key(l,p,a,v),new StocWms.Rand(1,q,old==null?1:old.revizie()+1));}
    public void scrieMiscare(int c,MiscareWms m){nb++;}
  }
  public static void main(String[] args){
    var base=List.of(row(101,"CO",6),row(102,"CO",6),row(103,"CO",6));
    result("J01 baseline simple set","null",NotaSetWms.refuzDefinitie(true,false,"I",1,base,0));
    result("J02 lot-enabled pieces permitted by target","null",NotaSetWms.refuzDefinitie(true,false,"I",1,base,1));
    result("J03 packaging line native PK permitted by target","null",NotaSetWms.refuzDefinitie(true,false,"I",1,List.of(row(101,"CO",1),row(104,"PK",1)),0));
    result("J04 labor 0.5h nonstock accepted by target","null",NotaSetWms.refuzDefinitie(true,false,"I",1,List.of(row(101,"CO",1),new SetLista.RandLista(105,new BigDecimal("0.5"),"CO",false,b(0),false,false,false)),0));
    var c=new NotaSetWms.Cerere(NotaSetWms.Tip.DEZAMBALARE,11,10,20,500,1,21,77,282,9001);
    var bon=NotaSetWms.dezambalare(c,Map.of(101,b(6),102,b(6),103,b(6)));
    result("J05 unpack quantities","[1, 6, 6, 6]",bon.stream().map(MiscareWms::qty).toList());
    result("J06 destination each output same locator","[21]",bon.stream().filter(x->x.locatorLa()>0).map(MiscareWms::locatorLa).distinct().toList());
    result("J07 BOM retained on consumed set",77,bon.get(0).bom());
    result("J08 input from foreign locator rejected","t355.refuz.pozitie",NotaSetWms.refuzCerere(c,Set.of(22,23)));
    var mem=new Mem();mem.state.put(mem.key(21,500,0,77),new StocWms.Rand(1,b(20),1));
    StocWms.aplica(mem,11,bon); result("J09 one note causes −1 real set",19,mem.state.get(mem.key(21,500,0,77)).qty());
    StocWms.aplica(mem,11,bon); result("J10 retry same source, same lines, one intended business event",19,mem.state.get(mem.key(21,500,0,77)).qty());
    result("J11 retry should leave only four movements",4,mem.nb);
    var av=Map.of(101,b(120),102,b(120),103,b(120));
    var s1=av.keySet().stream().map(x->new SetLista.Componenta(x,b(6),true)).toList();var s2=av.keySet().stream().map(x->new SetLista.Componenta(x,b(3),true)).toList();
    result("J12 G3 S1/S2 alternatives","20/40",SetLista.disponibilSet(av,s1)+"/"+SetLista.disponibilSet(av,s2));
    var d=new LinkedHashMap<String,BigDecimal>();av.forEach((p,q)->d.put(RezervareStoc.cheie(p,10),q));
    var g1=new RezervareStoc.Grup(7,av.keySet().stream().map(p->new RezervareStoc.LinieCerere(7,p,10,b(60))).toList());
    var g2=new RezervareStoc.Grup(8,av.keySet().stream().map(p->new RezervareStoc.LinieCerere(8,p,10,b(30))).toList());
    RezervareStoc.alocaGrupuri(List.of(g1,g2),d);result("J13 shared commitment residual",30,d.get("101|10"));
    var fr=new LinkedHashMap<String,BigDecimal>();fr.put("101|10",b(80));fr.put("101|11",b(40));
    result("J14 aggregate 120 requested as one SKU in auto-location allocation", "REZERVAT",RezervareStoc.aloca(List.of(new RezervareStoc.LinieCerere(11,101,0,b(120))),fr).get(11));
    var day=LocalDate.of(2026,11,2);
    var early=new LoturiArticole.Lot(1,"early",day.plusDays(2),b(4));var later=new LoturiArticole.Lot(2,"later",day.plusDays(10),b(8));
    var selected=Fefo.propus(List.of(early,later),b(6),day);result("J15 single FEFO proposal for 6 when earlier has 4",2,selected==null?-1:selected.asi());
    result("J16 global negative check tracks whole group", "[2]",RezervareStoc.liniiPesteStoc(List.of(new RezervareStoc.LinieCerere(1,101,10,b(6)),new RezervareStoc.LinieCerere(2,101,10,b(6))),Map.of("101|10",b(6))));
  }
}

