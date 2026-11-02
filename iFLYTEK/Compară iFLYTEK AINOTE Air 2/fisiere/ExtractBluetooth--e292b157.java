import jadx.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
public class ExtractBluetooth {
 public static void main(String[] args) throws Exception {
  Path out=Path.of(args[1]); Files.createDirectories(out);
  JadxArgs config=new JadxArgs();config.setInputFiles(List.of(new File(args[0])));config.setThreadsCount(4);
  try(JadxDecompiler dex=new JadxDecompiler(config)) {
   dex.load(); int count=0; List<String> inventory=new ArrayList<>();
   for(JavaClass c:dex.getClasses()) {
    String raw=c.getRawName();
    boolean selected=args.length>2 ? Files.readAllLines(Path.of(args[2])).contains(raw) : raw.startsWith("com.iflytek.easytrans.headset.");
    if(!selected)continue;
    String code=c.getCode(); Path p=out.resolve(c.getFullName().replace('.','/')+".java");Files.createDirectories(p.getParent());Files.writeString(p,code);
    inventory.add(raw+"\t"+c.getFullName());count++;
   }
   Files.write(out.resolve("class-mapping.tsv"),inventory);
   System.out.println("Extracted classes: "+count);
  }
 }
}
