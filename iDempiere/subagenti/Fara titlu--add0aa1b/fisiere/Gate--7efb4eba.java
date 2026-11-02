import java.util.*;import java.util.regex.Pattern;import java.io.IOException;import com.eva.ro.contab.corelare.*;
public class Gate {
 public static void main(String[] x){
  for(boolean btn:new boolean[]{false,true})for(boolean allowed:new boolean[]{false,true})run(btn,allowed,11,11,false);
  run(true,true,22,11,false);run(true,true,11,11,true);
  System.out.println("AUTO_SCHEDULER_WITHOUT_MANUAL_BUTTON="+TrimiteFisaCanal.refuzAuto(TrimiteFisaCanal.AUTO,102,"AUTOMAT"));
 }
 static void run(boolean clicked,boolean allowed,int owner,int cur,boolean lost){
  var op=AdaptorPlatforma.Capabilitate.FISA;
  String gate=PlatformeVanzari.scrierePermisa(new PlatformeVanzari.RandPoarta(true,owner,true,allowed,"CESIRO1"),cur,op);
  var dest=new ApiSite.Destinatie("CESIRO1",true,"http://127.0.0.1:4122/api/ext/v1","fixture-no-network");
  var request=new TransportScriere.CerereHttp(7,op,"SITE","PUT","/products/5",List.of(Pattern.compile("^/products/[0-9]{1,9}$")),"/products/{id}","N1","a06-stable-operation","{}");
  List<String> calls=new ArrayList<>();Set<String> effects=new HashSet<>();List<ApiSite.RandJurnal> journal=new ArrayList<>();
  TransportScriere.ExpeditorCanal sink=(m,u,k,id,payload)->{calls.add(id);effects.add(id);if(lost&&calls.size()==1)throw new IOException("timeout after remote persistence");return new AdaptorPlatforma.Raspuns(201,"{}");};
  List<String> outcomes=new ArrayList<>(); if(clicked){int max=lost?2:1;for(int z=0;z<max;z++){var res=TransportScriere.executa(gate,dest,request,sink,journal::add);outcomes.add(res.stare());}}
  System.out.println("click="+clicked+" allowed="+allowed+" client="+cur+" owner="+owner+" lost="+lost+" gate="+gate+" networkAttempts="+calls.size()+" keys="+new HashSet<>(calls).size()+" businessEffectsDedupStub="+effects.size()+" journal="+journal.size()+" states="+outcomes);
 }
}
