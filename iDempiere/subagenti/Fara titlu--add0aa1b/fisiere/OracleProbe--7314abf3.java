package com.eva.ro.contab.corelare;
import java.math.*;import java.util.*;
public class OracleProbe {
 static void show(String k,String n,Object want,Object got){System.out.println(k+"\t"+n+"\t"+want+"\t"+got+"\t"+Objects.equals(want,got));}
 static void precedence(String n,String star,String ch,String expected){var v=TabelaFisaCanal.valoareEfectiva("121.00",star,ch);show("K08",n,expected,v.origine()+"|"+v.valoare());}
 static String gate(boolean active,boolean write,int actual,int actor){return PlatformeVanzari.scrierePermisa(new PlatformeVanzari.RandPoarta(true,actual,active,write,"CESIRO1"),actor,AdaptorPlatforma.Capabilitate.FISA);}
 public static void main(String[] args){
  show("K07","C05 start","rosu",CazFlux.bulinaInceput("C05","verde"));show("K07","C18 start","rosu",CazFlux.bulinaInceput("C18","verde"));
  show("K07","C26 start","verde",CazFlux.bulinaInceput("C26","rosu"));
  var closed=Set.of("C01");var threshold=new BigDecimal("0.01");
  show("K07","closed, linked, DIF=.01","verde",CazFlux.bulinaFinal("C01",new BigDecimal("0.01"),true,closed,threshold));
  show("K07","closed, linked, DIF=.02","rosu",CazFlux.bulinaFinal("C01",new BigDecimal("0.02"),true,closed,threshold));
  show("K07","closed, not linked, DIF=0","rosu",CazFlux.bulinaFinal("C01",BigDecimal.ZERO,false,closed,threshold));
  String uu="12345678-1234-4123-8123-123456789012";
  show("K09","known invoice uuid","index.zul?Action=Zoom&TableName=C_Invoice&Record_UU="+uu,RaportFluxComenzi.adresaZoom(RaportFluxComenzi.zoom("C_Invoice",uu)));show("K09","missing UU",null,RaportFluxComenzi.zoom("C_Invoice",null));show("K09","malformed identifier",null,RaportFluxComenzi.zoom("C_Invoice","CI-42"));
  show("K08","native rule -10pct","108.90",FisaCanalCalcul.valoareModificata("121.00","PROCENT","-10"));
  precedence("native only",null,null,"IDEMPIERE|121.00");precedence("platform only","108.90",null,"PLATFORMA|108.90");precedence("channel on top","108.90","100.00","CANAL|100.00");precedence("channel blank falls back","108.90"," ","PLATFORMA|108.90");
  show("K35","same firm Y FISA",null,gate(true,true,11,11));show("K35","other firm","platforma.poarta.alta_firma",gate(true,true,11,22));show("K35","inactive","platforma.poarta.inactiva",gate(false,true,11,11));show("K35","writing disabled","platforma.poarta.scriere_nepermisa",gate(true,false,11,11));
 }
}
