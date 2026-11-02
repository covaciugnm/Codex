import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import com.eva.ro.contab.corelare.Fefo;
import com.eva.ro.contab.corelare.LoturiArticole;
import com.eva.ro.contab.corelare.FisaCanalCalcul;
import com.eva.ro.contab.corelare.RegulaStocCanal;
public class A11Measured {
 static BigDecimal b(String x){return new BigDecimal(x);}
 static void expect(String id,Object x,Object y){if(!String.valueOf(x).equals(String.valueOf(y)))throw new AssertionError(id+" "+x+" expected "+y);System.out.println(id+" = "+x);}
 public static void main(String[] args){
  var date=LocalDate.of(2028,2,27);
  expect("days/3 includes leap day",Fefo.termenDinZile(date,"3"),LocalDate.of(2028,3,1));
  var lots=List.of(new LoturiArticole.Lot(71,"expired",date.minusDays(1),b("80")),new LoturiArticole.Lot(72,"early",date.plusDays(1),b("2")),new LoturiArticole.Lot(73,"later",date.plusDays(2),b("7")));
  expect("FEFO/2",Fefo.propus(lots,b("2"),date).asi(),72);
  expect("FEFO/5",Fefo.propus(lots,b("5"),date).asi(),73);
  expect("FEFO/8",Fefo.propus(lots,b("8"),date),null);
  expect("stock/raw",FisaCanalCalcul.stocCalculat(List.of(b("9"),b("17")),b("4"),b("6"),3,Map.of()),13);
  expect("stock/50%",FisaCanalCalcul.stocCalculat(List.of(b("9"),b("17")),b("4"),b("6"),3,Map.of(RegulaStocCanal.PROCENT,"50")),6);
  expect("stock/no negative",FisaCanalCalcul.stocCalculat(List.of(b("5")),b("4"),b("6"),3,Map.of()),0);
  expect("gross from net",FisaCanalCalcul.pretBrut(b("13.25"),b("0.21"),false).setScale(2),b("16.03"));
 }
}
