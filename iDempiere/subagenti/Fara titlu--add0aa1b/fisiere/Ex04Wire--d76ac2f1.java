package com.eva.ro.contab.corelare;
import java.sql.Timestamp;import java.util.*;
public class Ex04Wire {
 public static void main(String[] args) throws Exception {
  if(!args[0].matches("http://127\\.0\\.0\\.1:[0-9]+/api/ext/v1"))throw new IllegalArgumentException("fixture only");
  String key=System.getenv("EX04_FIXTURE_KEY");
  var cfg=new SursaSiteConfig.Config(args[0],key,args[1],List.of(),List.of(),null);
  var s=SursaCesiro1.deschide(cfg);
  try{
   var result=s.comenzi(Timestamp.valueOf(args[2]),Timestamp.valueOf(args[3]),args[4].equals("null")?null:Timestamp.valueOf(args[4]));
   for(var v:result)System.out.println("ROW\t"+v.id()+"\t"+v.nr()+"\t"+v.total()+"\t"+v.moneda()+"\t"+v.actualizat()+"\t"+v.cont()+"\t"+v.canal());
   if(args.length>5){var det=s.detaliu(args[5]);System.out.println("DETAIL\t"+det.facturi().size()+"\t"+det.expedieri().size());}
   System.out.println("RESULT\tOK\t"+result.size());
  }catch(Exception e){System.out.println("RESULT\tERROR\t"+e.getClass().getSimpleName()+"\t"+String.valueOf(e.getMessage()).replace("\n"," ").substring(0,Math.min(String.valueOf(e.getMessage()).length(),320)));}
  for(var t:s.cereri())System.out.println("HTTP\t"+t);
 }
}
