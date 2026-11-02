import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import com.android.tools.smali.baksmali.BaksmaliOptions;
import com.android.tools.smali.baksmali.Adaptors.ClassDefinition;
import com.android.tools.smali.baksmali.formatter.BaksmaliWriter;
import com.android.tools.smali.dexlib2.DexFileFactory;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.iface.*;

/** Static library API exporter; never loads or executes application classes. */
public final class SmaliFingerprintExport {
  private static String quote(String s) {
    StringBuilder b=new StringBuilder("\"");
    for(char c:s.toCharArray())switch(c){case '"':b.append("\\\"");break;case '\\':b.append("\\\\");break;case '\n':b.append("\\n");break;case '\r':b.append("\\r");break;case '\t':b.append("\\t");break;default:if(c<32)b.append(String.format("\\u%04x",(int)c));else b.append(c);}
    return b.append('"').toString();
  }
  private static String sha(byte[] bytes)throws Exception{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));}
  public static void main(String[] args)throws Exception {
    if(args.length<2||args.length>3)throw new IllegalArgumentException("Expected input APK/DEX, output NDJSON, optional exact class descriptor or @descriptor-list-file");
    Path input=Path.of(args[0]),output=Path.of(args[1]);
    Set<String> requested=new TreeSet<>();
    if(args.length==3){if(args[2].startsWith("@")){for(String line:Files.readAllLines(Path.of(args[2].substring(1)),StandardCharsets.UTF_8))if(!line.isBlank())requested.add(line.trim());}else requested.add(args[2]);}
    for(String s:requested)if(!s.startsWith("L")||!s.endsWith(";")||s.contains(" "))throw new IllegalArgumentException("Invalid class descriptor");
    BaksmaliOptions o=new BaksmaliOptions();o.debugInfo=false;o.sequentialLabels=true;o.implicitReferences=false;o.parameterRegisters=false;o.localsDirective=false;o.codeOffsets=false;o.accessorComments=false;o.normalizeVirtualMethods=false;o.registerInfo=0;o.allowOdex=false;o.deodex=false;
    MultiDexContainer<?> container=DexFileFactory.loadDexContainer(input.toFile(),Opcodes.getDefault());
    Set<String> seen=new HashSet<>(),found=new HashSet<>();int count=0;
    Files.createDirectories(output.toAbsolutePath().getParent());
    try(BufferedWriter w=Files.newBufferedWriter(output,StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
      for(String dexName:container.getDexEntryNames()){
        MultiDexContainer.DexEntry<?> de=container.getEntry(dexName);if(de==null)throw new IOException("Missing DEX entry");
        List<ClassDef> classes=new ArrayList<>(de.getDexFile().getClasses());classes.sort(Comparator.comparing(ClassDef::getType));
        for(ClassDef c:classes){if(!seen.add(c.getType()))throw new IOException("Duplicate class descriptor: "+c.getType());if(!requested.isEmpty()&&!requested.contains(c.getType()))continue;
          StringWriter text=new StringWriter();BaksmaliWriter bw=new BaksmaliWriter(text);ClassDefinition cd=new ClassDefinition(o,c);cd.writeTo(bw);bw.flush();if(cd.hadValidationErrors())throw new IOException("Baksmali validation errors: "+c.getType());
          byte[] bytes=text.toString().getBytes(StandardCharsets.UTF_8);String data=Base64.getEncoder().encodeToString(bytes);
          w.write("{\"type\":\"class\",\"descriptor\":"+quote(c.getType())+",\"dexEntry\":"+quote(dexName)+",\"smaliSha256\":"+quote(sha(bytes))+",\"smaliBytes\":"+bytes.length+",\"smaliBase64\":"+quote(data)+",\"validationErrors\":false}\n");
          found.add(c.getType());count++;
        }
      }
      if(!found.containsAll(requested)){Set<String> missing=new TreeSet<>(requested);missing.removeAll(found);throw new IOException("Requested classes not found: "+missing);}
      w.write("{\"type\":\"summary\",\"complete\":true,\"classes\":"+count+",\"filtered\":"+(!requested.isEmpty())+",\"requested\":"+requested.size()+",\"inputSha256\":"+quote(sha(Files.readAllBytes(input)))+"}\n");
    }
    System.out.println("Exported "+count+" static Smali classes; complete=true");
  }
}
