import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.lang.reflect.Field;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.dexbacked.DexBackedMethod;
import com.android.tools.smali.dexlib2.dexbacked.DexBackedClassDef;

/** Raw DEX metadata only. Does not invoke JADX, decompile source or load application JVM classes. */
public final class RawDexIdentityIndex {
  static String q(String s){StringBuilder b=new StringBuilder("\"");for(char c:s.toCharArray())switch(c){case '"':b.append("\\\"");break;case '\\':b.append("\\\\");break;case '\n':b.append("\\n");break;case '\r':b.append("\\r");break;case '\t':b.append("\\t");break;default:if(c<32||Character.isSurrogate(c))b.append(String.format("\\u%04x",(int)c));else b.append(c);}return b.append('"').toString();}
  static String sha(byte[] b)throws Exception{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(b));}
  static int u2(byte[] b,int p){if(p<0||p+2>b.length)throw new IllegalArgumentException("Bounds");return (b[p]&255)|((b[p+1]&255)<<8);}
  static int i4(byte[] b,int p){return u2(b,p)|(u2(b,p+2)<<16);}
  public static void main(String[] a)throws Exception {
    if(a.length!=2)throw new IllegalArgumentException("Expected plain DEX input and new NDJSON output");Path input=Path.of(a[0]),output=Path.of(a[1]);byte[] bytes=Files.readAllBytes(input);String dexSha=sha(bytes);
    if(bytes.length<112||bytes[0]!='d'||bytes[1]!='e'||bytes[2]!='x'||bytes[3]!='\n'||i4(bytes,32)!=bytes.length||i4(bytes,40)!=0x12345678)throw new IllegalArgumentException("Unsupported DEX header");
    DexFile dex=DexFileFactory.loadDexFile(input.toFile(),Opcodes.getDefault());Field offset=DexBackedMethod.class.getDeclaredField("codeOffset");if(!offset.trySetAccessible())throw new IllegalStateException("Pinned dexlib2 metadata API unavailable");Field classOffset=DexBackedClassDef.class.getDeclaredField("classDefOffset");if(!classOffset.trySetAccessible())throw new IllegalStateException("ClassDef offset API unavailable");
    List<ClassDef> classes=new ArrayList<>(dex.getClasses());classes.sort(Comparator.comparing(ClassDef::getType));if(classes.size()!=i4(bytes,96))throw new IllegalStateException("ClassDef coverage mismatch");Set<String> owners=new HashSet<>();int methodCount=0;
    Files.createDirectories(output.toAbsolutePath().getParent());try(BufferedWriter w=Files.newBufferedWriter(output,StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
      for(ClassDef c:classes){if(!(c instanceof DexBackedClassDef))throw new IllegalStateException("Unexpected ClassDef implementation");int classPos=(int)classOffset.get(c),classBase=i4(bytes,100),delta=classPos-classBase,classIndex=delta/32;if(delta<0||delta%32!=0||classIndex>=classes.size()||classPos+32>bytes.length||i4(bytes,classPos+4)!=c.getAccessFlags())throw new IllegalStateException("ClassDef table offset mismatch");if(!owners.add(c.getType()))throw new IllegalStateException("Duplicate owner descriptor");List<String> methods=new ArrayList<>();Set<String> ids=new HashSet<>();
        for(Method m:c.getMethods()){
          if(!(m instanceof DexBackedMethod)||!m.getDefiningClass().equals(c.getType()))throw new IllegalStateException("Unexpected raw method ownership");StringBuilder sig=new StringBuilder(m.getName()).append('(');for(CharSequence t:m.getParameterTypes())sig.append(t);sig.append(')').append(m.getReturnType());String id=c.getType()+"->"+sig;if(!ids.add(id))throw new IllegalStateException("Duplicate method identity");
          DexBackedMethod dm=(DexBackedMethod)m;if(dm.getMethodIndex()<0||dm.getMethodIndex()>=i4(bytes,88)||u2(bytes,i4(bytes,92)+dm.getMethodIndex()*8)!=i4(bytes,classPos))throw new IllegalStateException("Raw method/class table mismatch");int codeOffset=(int)offset.get(dm);String code="null";
          if(codeOffset!=0){if(codeOffset<0||codeOffset+16>bytes.length||m.getImplementation()==null)throw new IllegalStateException("Invalid code offset");int units=i4(bytes,codeOffset+12);long end=(long)codeOffset+16+2L*units;if(units<0||end>bytes.length||m.getImplementation().getRegisterCount()!=u2(bytes,codeOffset)||dm.getImplementation().getInstructionsSize()!=units)throw new IllegalStateException("Instruction range mismatch");byte[] ins=Arrays.copyOfRange(bytes,codeOffset+16,(int)end);code="{\"offset\":"+codeOffset+",\"registers\":"+u2(bytes,codeOffset)+",\"tries\":"+u2(bytes,codeOffset+6)+",\"instructionUnits\":"+units+",\"instructionBytesSha256\":"+q(sha(ins))+"}";}
          else if(m.getImplementation()!=null)throw new IllegalStateException("Missing code offset");
          methods.add("{\"signature\":"+q(sig.toString())+",\"rawDescriptor\":"+q(id)+",\"methodIndex\":"+dm.getMethodIndex()+",\"accessFlags\":"+m.getAccessFlags()+",\"hasImplementation\":"+(m.getImplementation()!=null)+",\"code\":"+code+"}");methodCount++;
        }
        Collections.sort(methods);List<String> interfaces=new ArrayList<>();for(String s:c.getInterfaces())interfaces.add(q(s));w.write("{\"type\":\"class\",\"descriptor\":"+q(c.getType())+",\"classDefIndex\":"+classIndex+",\"classDefOffset\":"+classPos+",\"dexSha256\":"+q(dexSha)+",\"accessFlags\":"+c.getAccessFlags()+",\"superclass\":"+(c.getSuperclass()==null?"null":q(c.getSuperclass()))+",\"interfaces\":["+String.join(",",interfaces)+"],\"methods\":["+String.join(",",methods)+"]}\n");
      }
      w.write("{\"type\":\"summary\",\"complete\":true,\"inputSha256\":"+q(dexSha)+",\"bytes\":"+bytes.length+",\"classes\":"+classes.size()+",\"methods\":"+methodCount+",\"instructionHashScope\":\"Byte identity only; different DEX references are not equivalent\"}\n");
    }
  }
}
