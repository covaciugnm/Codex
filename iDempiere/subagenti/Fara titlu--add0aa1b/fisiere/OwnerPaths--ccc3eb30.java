package com.eva.ro.contab.corelare;
import java.util.*;import java.math.*;import java.nio.file.*;import java.sql.*;import com.eva.ro.contab.documente.JsonMic;
public class OwnerPaths {
 public static void main(String[] args)throws Exception {
  String raw=Files.readString(Path.of(args[0]));
  Object parsed=JsonMic.citeste(raw);Map<String,Object> changed=new LinkedHashMap<>((Map<String,Object>)parsed);
  var a=DetaliuComanda.din(raw); changed.put("seller",Map.of("cui","RO123456"));
  for(var scenario:List.of(a,DetaliuComanda.din(changed))){
   var d=scenario;
   var ctx=new ValidareComanda.Context("123456",Set.of(),Map.of(),Set.of(),Set.of(),Map.of(),true,true,21,Set.of(11,21),true,BigDecimal.valueOf(.01),true,true,true,true,null,null,Set.of(),BigDecimal.ZERO,false,false);
   var v=new ValidareComanda.Comanda(false,d.cuiVanzator(),"placed",null,null,false,null,"RON",List.of(),null,null,null,BigDecimal.valueOf(87.88),"PF",true,true,null,List.of());
   var decision=ValidareComanda.valideaza(v,ctx,true);
   System.out.println("owner_from_witness=false seller="+(d.cuiVanzator()==null||d.cuiVanzator().isEmpty()?"missing":"provided")+" dto_lines="+d.linii().size()+" stored_lines=0 V01="+decision.motive().contains("V01")+" V02="+decision.motive().stream().anyMatch(s->s.startsWith("V02"))+" outcome="+decision.stare());
  }
  var rec=SursaCesiro1.comanda(Map.of("id","SYNTH","order_number","SYNTH","updated_at","2026-11-02T10:00:00Z"));
  System.out.println("when incoming earlier than stored, change accepted="+PreiaDinSite.deActualizat(rec,Timestamp.valueOf("2026-11-02 12:00:00")));
 }
}
