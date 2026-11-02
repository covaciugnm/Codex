import java.util.*;import java.nio.charset.StandardCharsets;import java.nio.file.*;import java.math.BigDecimal;import com.eva.ro.contab.documente.*;
public class A04NirRendered{
 static String template(String name){try(var stream=A04NirRendered.class.getResourceAsStream("/com/eva/ro/contab/documente/sabloane/"+name+".sablon.html")){if(stream==null)throw new IllegalArgumentException(name);return new String(stream.readAllBytes(),StandardCharsets.UTF_8);}catch(Exception e){throw new RuntimeException(e);}}
 static Map<String,Object> line(String code,int q,int p){Map<String,Object> m=new LinkedHashMap<>();m.put("cod",code);m.put("denumire",code);m.put("cant",BigDecimal.valueOf(q));m.put("pret",BigDecimal.valueOf(p));m.put("um","BUC");return m;}
 public static void main(String[]args) throws Exception{
  for(String input:new String[]{"7\n3","\n3","abc\n3"}){Map<String,Object> model=new HashMap<>(),form=new HashMap<>();var x=line("X",7,10);var y=line("Y",5,100);model.put("bunuri",List.of(x,y));model.put("emitere",form);form.put("receptionat",input);NirReceptie.calculeaza(model,form);
   String html=Sablon.randeaza(template("D0901"),model,name->template(name.startsWith("_")?name:"_"+name)).html;
   String key=input.startsWith("7")?"control":input.startsWith("abc")?"invalid":"blank";Files.writeString(Path.of(args[0],"nir-"+key+".html"),html);System.out.println(key+" "+x.get("receptionat")+" "+y.get("receptionat")+" "+model.get("total_receptionat")+" "+form.get("diferente"));}}
}
