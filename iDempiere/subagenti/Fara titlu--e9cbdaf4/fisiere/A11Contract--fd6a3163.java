package com.eva.ro.contab.corelare;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
public class A11Contract {
 public static void main(String[] args) throws Exception {
  String raw=Files.readString(Path.of(args[0]));
  var cfg=new SursaSiteConfig.Config("http://127.0.0.1:4121/api/ext/v1","A11-synthetic", "canal-a", List.of(),List.of(),null);
  var api=SursaCesiro1.pentruTeste(cfg,(url,key)->new AdaptorPlatforma.Raspuns(200,raw));
  var target=api.detaliu("orig-A11");
  var parsed=DetaliuComanda.din(raw);
  System.out.println("lines="+parsed.linii().size()+" total="+parsed.totalRon()+" seller_present="+(parsed.cuiVanzator()!=null&&!parsed.cuiVanzator().isBlank()));
  for(var l:parsed.linii())System.out.println("line="+l.sku()+" "+l.cantitate()+" "+l.cotaTva()+" "+l.totalLinie());
  for(var s:target.expedieri())System.out.println("parcel="+s.id()+" awb="+s.awb()+" cod="+s.ramburs()+" state="+s.stareColet());
 }
}
