import jadx.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.*;
public class ExportSmali {
 public static void main(String[] args)throws Exception{
  File raw=new File(args[0]);Path out=Path.of(args[1]);Files.createDirectories(out);
  JadxArgs config=new JadxArgs();config.setInputFiles(Arrays.stream(raw.listFiles()).filter(f->f.getName().matches("classes[0-9]*\\.dex")).toList());
  int ok=0,failed=0;
  try(JadxDecompiler dex=new JadxDecompiler(config);ZipOutputStream zip=new ZipOutputStream(Files.newOutputStream(out.resolve("smali-complet.zip")));BufferedWriter index=Files.newBufferedWriter(out.resolve("smali-index.tsv"));BufferedWriter errors=Files.newBufferedWriter(out.resolve("smali-errors.txt"))){
   zip.setLevel(1);dex.load();index.write("class\tarchiveEntry\n");
   List<JavaClass> classes=dex.getClassesWithInners();int i=0;
   for(JavaClass c:classes){String name=c.getRawName();String entry=String.format("classes/%05d.smali",i++);
    try{String code=c.getSmali();zip.putNextEntry(new ZipEntry(entry));zip.write(code.getBytes(java.nio.charset.StandardCharsets.UTF_8));zip.closeEntry();index.write(name+"\t"+entry+"\n");ok++;}
    catch(Exception e){errors.write(name+"\t"+e+"\n");failed++;}
    if(i%5000==0)System.out.println("Smali "+i+" / "+classes.size());
   }
  }
  Files.writeString(out.resolve("smali-summary.json"),"{\"exported\":"+ok+",\"failed\":"+failed+"}");
  System.out.println("Smali exported="+ok+" failed="+failed);
 }
}
