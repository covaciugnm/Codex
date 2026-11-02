package com.eva.ro.contab.corelare;
import java.util.*;import java.math.*;import java.nio.file.*;import java.sql.Timestamp;
public class OwnerMatrix {
 public static void main(String[] args)throws Exception{
  var frozen=DetaliuComanda.din(Files.readString(Path.of(args[0])));
  if(frozen.linii().size()!=2)throw new AssertionError("witness lines");
  var ctx=new ValidareComanda.Context("123456",Set.of(),Map.of(),Set.of(),Set.of(),Map.of(),true,true,21,Set.of(11,21),true,new BigDecimal(".01"),true,true,true,true,null,null,Set.of(),BigDecimal.ZERO,false,false);
  for(boolean own:List.of(false,true))for(String seller:new String[]{frozen.cuiVanzator(),"RO123456","RO999999"}){
   var header=new ValidareComanda.Comanda(own,seller,"placed",null,null,false,null,"RON",List.of(),null,null,null,new BigDecimal("87.88"),"PF",true,true,null,List.of());
   var decision=ValidareComanda.valideaza(header,ctx,true);boolean v1=decision.motive().contains("V01"),v2=decision.motive().stream().anyMatch(x->x.startsWith("V02"));
   if(v1==own||v2=="RO123456".equals(seller))throw new AssertionError("unexpected gates");
   System.out.println("owner="+own+" seller="+seller+" V01="+v1+" V02="+v2+" result="+decision.stare());
  }
  for(String time:List.of("2026-11-02T09:00:00Z","2026-11-02T10:00:00Z","2026-11-02T11:00:00Z")){
   var rec=SursaCesiro1.comanda(Map.of("id","ID","order_number","ID","updated_at",time));
   Timestamp wall=Timestamp.from(java.time.Instant.parse("2026-11-02T10:00:00Z"));
   boolean result=PreiaDinSite.deActualizat(rec,wall);boolean expected=!time.equals("2026-11-02T10:00:00Z");
   if(result!=expected)throw new AssertionError(time+" "+result);System.out.println("compare "+time+" against 10:00Z => "+result);
  }
 }
}
