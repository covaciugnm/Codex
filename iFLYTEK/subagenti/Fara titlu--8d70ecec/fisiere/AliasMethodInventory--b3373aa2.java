import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.zip.ZipFile;
import jadx.api.*;
import jadx.core.dex.nodes.*;
import jadx.core.dex.info.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.dexbacked.DexBackedMethod;

/** Static metadata only: never calls getCode(), decompile(), save(), or loads application JVM classes. */
public final class AliasMethodInventory {
  static Map<String,Object> map(Object... pairs){Map<String,Object> r=new LinkedHashMap<>();for(int i=0;i<pairs.length;i+=2)r.put((String)pairs[i],pairs[i+1]);return r;}
  static String quote(String s){StringBuilder b=new StringBuilder("\"");for(char c:s.toCharArray())switch(c){case '"':b.append("\\\"");break;case '\\':b.append("\\\\");break;case '\n':b.append("\\n");break;case '\r':b.append("\\r");break;case '\t':b.append("\\t");break;default:if(c<32||Character.isSurrogate(c))b.append(String.format("\\u%04x",(int)c));else b.append(c);}return b.append('"').toString();}
  static String json(Object o){if(o==null)return"null";if(o instanceof String)return quote((String)o);if(o instanceof Number||o instanceof Boolean)return o.toString();if(o instanceof Map){List<String> a=new ArrayList<>();for(Object entry:((Map<?,?>)o).entrySet()){Map.Entry<?,?> e=(Map.Entry<?,?>)entry;a.add(quote((String)e.getKey())+":"+json(e.getValue()));}return"{"+String.join(",",a)+"}";}if(o instanceof Iterable){List<String>a=new ArrayList<>();for(Object x:(Iterable<?>)o)a.add(json(x));return"["+String.join(",",a)+"]";}throw new IllegalArgumentException("Unsupported JSON type");}
  static String sha(byte[] b)throws Exception{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(b));}
  static Set<String> ownerNames(String raw,String alias){Set<String> r=new TreeSet<>();for(String s:List.of(raw,alias)){r.add(s);r.add(s.replace('$','.'));}return r;}
  static Set<String> typeNames(String descriptor,Map<String,Set<String>> aliases){int dims=0;while(descriptor.charAt(dims)=='[')dims++;String base=descriptor.substring(dims),suffix="[]".repeat(dims);Set<String> names=new TreeSet<>();if(base.startsWith("L")){String raw=base.substring(1,base.length()-1).replace('/','.');names.addAll(aliases.getOrDefault(base,ownerNames(raw,raw)));}else{String p=switch(base){case"V"->"void";case"Z"->"boolean";case"B"->"byte";case"S"->"short";case"C"->"char";case"I"->"int";case"J"->"long";case"F"->"float";case"D"->"double";default->throw new IllegalArgumentException("Invalid DEX type "+descriptor);};names.add(p);}Set<String> out=new TreeSet<>();for(String n:names)out.add(n+suffix);return out;}
  static String descriptor(ClassNode c){return"L"+c.getRawName().replace('.','/')+";";}
  public static void main(String[] args)throws Exception {
    if(args.length!=3)throw new IllegalArgumentException("Expected original APK, output NDJSON, exact raw/alias owner selector file");Path input=Path.of(args[0]),output=Path.of(args[1]),selectors=Path.of(args[2]);Set<String>wanted=new TreeSet<>();for(String s:Files.readAllLines(selectors,StandardCharsets.UTF_8))if(!s.isBlank())wanted.add(s.trim());if(wanted.isEmpty())throw new IllegalArgumentException("Empty selectors");
    Map<String,Map<String,Object>> rawMethods=new HashMap<>();List<Map<String,Object>> dexEvidence=new ArrayList<>();MultiDexContainer<?> container=DexFileFactory.loadDexContainer(input.toFile(),Opcodes.getDefault());
    try(ZipFile zip=new ZipFile(input.toFile())){for(String dexName:container.getDexEntryNames()){
      byte[] dex=zip.getInputStream(Objects.requireNonNull(zip.getEntry(dexName))).readAllBytes();String dexSha=sha(dex);MultiDexContainer.DexEntry<?> entry=Objects.requireNonNull(container.getEntry(dexName));int classes=0,methods=0;
      for(ClassDef c:entry.getDexFile().getClasses()){classes++;for(Method m:c.getMethods()){StringBuilder signature=new StringBuilder(m.getName()).append('(');List<String> params=new ArrayList<>();for(CharSequence p:m.getParameterTypes()){params.add(p.toString());signature.append(p);}signature.append(')').append(m.getReturnType());String id=c.getType()+"->"+signature;int index=m instanceof DexBackedMethod?((DexBackedMethod)m).getMethodIndex():-1;if(index<0)throw new IllegalStateException("No independent DEX method index");Map<String,Object> record=map("rawDescriptor",id,"ownerDescriptor",c.getType(),"name",m.getName(),"shortId",signature.toString(),"parameters",params,"returnType",m.getReturnType(),"dexEntry",dexName,"dexSha256",dexSha,"methodIndex",index,"accessFlags",m.getAccessFlags(),"hasImplementation",m.getImplementation()!=null);if(rawMethods.put(id,record)!=null)throw new IllegalStateException("Duplicate raw method descriptor");methods++;}}
      dexEvidence.add(map("entry",dexName,"sha256",dexSha,"bytes",dex.length,"classDefinitions",classes,"definedMethods",methods));
    }}
    JadxArgs options=new JadxArgs();options.setInputFile(input.toFile());options.setOutDir(output.toAbsolutePath().getParent().resolve("unused-code-output").toFile());options.setThreadsCount(1);options.setSkipResources(true);options.setSkipFilesSave(true);options.setFsCaseSensitive(false);options.setGeneratedRenamesMappingFile(output.toAbsolutePath().getParent().resolve("absent-renames.jobf").toFile());
    Files.createDirectories(output.toAbsolutePath().getParent());
    try(JadxDecompiler decoder=new JadxDecompiler(options);BufferedWriter w=Files.newBufferedWriter(output,StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW)){
      decoder.load();List<ClassNode> all=new ArrayList<>(decoder.getRoot().getClasses());all.sort(Comparator.comparing(ClassNode::getRawName));Map<String,Set<String>> aliases=new HashMap<>();for(ClassNode c:all)aliases.put(descriptor(c),ownerNames(c.getRawName(),c.getClassInfo().getAliasFullName()));
      int selectedClasses=0,selectedMethods=0,unmatchedMethods=0;Set<String> matchedSelectors=new TreeSet<>();
      for(ClassNode c:all){Set<String> names=aliases.get(descriptor(c)),hits=new TreeSet<>(names);hits.retainAll(wanted);if(hits.isEmpty())continue;matchedSelectors.addAll(hits);selectedClasses++;List<Map<String,Object>> methods=new ArrayList<>();
        for(MethodNode m:c.getMethods()){MethodInfo info=m.getMethodInfo();String rawId=descriptor(c)+"->"+info.getShortId();Map<String,Object> raw=rawMethods.get(rawId);if(raw==null){unmatchedMethods++;methods.add(map("jadxRawId",info.getRawFullId(),"rawDescriptorCandidate",rawId,"independentDexMatch",false,"reason","API-generated/synthetic or unsupported metadata; cannot map to original DEX"));continue;}
          if(!Objects.equals(raw.get("name"),info.getName())||((List<?>)raw.get("parameters")).size()!=info.getArgsCount())throw new IllegalStateException("Independent DEX/API proto mismatch");List<Set<String>> paramNames=new ArrayList<>();for(Object p:(List<?>)raw.get("parameters"))paramNames.add(typeNames((String)p,aliases));Set<String> methodNames=new TreeSet<>();methodNames.add(info.getName());methodNames.add(info.getAlias());Map<String,Object> result=new LinkedHashMap<>(raw);result.putAll(map("independentDexMatch",true,"jadxRawFullId",info.getRawFullId(),"jadxFullId",info.getFullId(),"jadxAliasFullName",info.getAliasFullName(),"ownerJavaNames",names,"methodJavaNames",methodNames,"parameterJavaNames",paramNames,"returnJavaNames",typeNames((String)raw.get("returnType"),aliases),"methodCodeOffset",m.getMethodCodeOffset(),"inputFile",m.getInputFileName()));methods.add(result);selectedMethods++;
        }
        methods.sort(Comparator.comparing(x->String.valueOf(x.getOrDefault("rawDescriptor",x.get("rawDescriptorCandidate")))));w.write(json(map("type","class","rawDescriptor",descriptor(c),"rawName",c.getRawName(),"aliasFullName",c.getClassInfo().getAliasFullName(),"ownerJavaNames",names,"matchedSelectors",hits,"inputFile",c.getInputFileName(),"topParentRawName",c.getTopParentClass().getRawName(),"methods",methods))+"\n");
      }
      Set<String> missing=new TreeSet<>(wanted);missing.removeAll(matchedSelectors);w.write(json(map("type","summary","complete",true,"inputSha256",sha(Files.readAllBytes(input)),"dexEntries",dexEvidence,"rawDefinedMethods",rawMethods.size(),"apiClassNodes",all.size(),"selectedClasses",selectedClasses,"selectedMethods",selectedMethods,"apiMethodsWithoutIndependentDexIdentity",unmatchedMethods,"unmatchedSelectors",missing,"sourceDecompilationCalled",false,"semanticRepairsApproved",0))+"\n");
      System.out.println("Exported metadata for "+selectedClasses+" classes / "+selectedMethods+" independently matched DEX methods; source decompilation=false");
    }
  }
}
