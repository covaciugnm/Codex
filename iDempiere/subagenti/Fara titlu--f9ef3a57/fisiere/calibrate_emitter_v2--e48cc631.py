import pathlib,json,hashlib,datetime,shutil,difflib
LAB=pathlib.Path(__file__).parent;R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');OUT=R/'executie/R12_fisiere/A08_Catalog_paginare_lot05'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def dump(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(LAB/'harness_v2').mkdir();orig=(LAB/'harness/CatalogProductProbe.java').read_text(encoding='utf8')
replacement=r'''    static String quoted(String value){
        StringBuilder out=new StringBuilder("\"");
        for(int i=0;i<value.length();i++){
            char c=value.charAt(i);
            if(c=='"')out.append("\\\"");
            else if(c=='\\')out.append("\\\\");
            else if(c<32)out.append(String.format("\\u%04x",(int)c));
            else out.append(c);
        }
        return out.append('"').toString();
    }
    static String json(Object value){
        if(value==null)return "null";
        if(value instanceof String)return quoted((String)value);
        if(value instanceof Number || value instanceof Boolean)return String.valueOf(value);
        if(value instanceof Map<?,?> map){
            StringJoiner out=new StringJoiner(",","{","}");
            for(Map.Entry<?,?> e:map.entrySet())out.add(quoted(String.valueOf(e.getKey()))+":"+json(e.getValue()));
            return out.toString();
        }
        if(value instanceof Iterable<?> values){
            StringJoiner out=new StringJoiner(",","[","]");for(Object v:values)out.add(json(v));return out.toString();
        }
        throw new IllegalArgumentException("Unsupported emitter type: "+value.getClass().getName());
    }
    static void emit(String kind,Object value){System.out.println(kind+"|"+json(value));}
    static void serializerWitness(){
        Map<String,Object> witness=new LinkedHashMap<>();
        witness.put("unicode","Română țară Ω");witness.put("escaped","quote\" slash\\ newline\n tab\t");witness.put("null",null);
        witness.put("list",Arrays.asList(1,2.5,true,false,null,"x"));emit("SERIALIZER_WITNESS",witness);
        try{json(new Object());throw new AssertionError("Unsupported type accepted");}catch(IllegalArgumentException expected){System.out.println("SERIALIZER_NEGATIVE|true");}
    }'''
old='    static void emit(String kind,Object value){System.out.println(kind+"|"+GSON.toJson(value));}'
assert orig.count(old)==1;new=orig.replace(old,replacement).replace('        Path lab=Path.of(laboratory);','        serializerWitness();\n        Path lab=Path.of(laboratory);')
newpath=LAB/'harness_v2/CatalogProductProbe.java';newpath.write_text(new,encoding='utf8');shutil.copyfile(LAB/'harness/AuditCatalogPagination.java',LAB/'harness_v2/AuditCatalogPagination.java')
diff=LAB/'harness_v2/emitter.diff';diff.write_text(''.join(difflib.unified_diff(orig.splitlines(True),new.splitlines(True),fromfile='harness/CatalogProductProbe.java',tofile='harness_v2/CatalogProductProbe.java')),encoding='utf8')
prep=json.loads((LAB/'Preparation_v2.json').read_text(encoding='utf8'));args=[a.replace(str(LAB/'classes_v2'),str(LAB/'classes_v3')).replace(str(LAB/'harness'),str(LAB/'harness_v2')) for a in prep['compile_command']]
prep['utc_v3']=datetime.datetime.now(datetime.timezone.utc).isoformat();prep['previous_v2']=ref(LAB/'Preparation_v2.json');prep['compile_command']=args;prep['runtime_classpath']=[str(LAB/'classes_v3'),str(LAB/'lib/gson.jar')];prep['harness_v2']=[ref(newpath),ref(LAB/'harness_v2/AuditCatalogPagination.java')];prep['emitter_diff']=ref(diff);prep['JVM_encoding_options']=['-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8']
runner=(LAB/'run_probe_v2.py').read_text(encoding='utf8').replace("LAB/'Preparation_v2.json'","LAB/'Preparation_v3.json'").replace("LAB/'classes_v2'","LAB/'classes_v3'").replace("'-Dfile.encoding=UTF-8',","'-Dfile.encoding=UTF-8','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8',")
rp=LAB/'run_probe_v3.py';rp.write_text(runner,encoding='utf8');prep['runner_v3']=ref(rp);dump(LAB/'Preparation_v3.json',prep)
note={'utc':prep['utc_v3'],'classification':'CALIBRARE_EMITTER_HARNESS_NU_DEFECT_PRODUS','previous_attempt':ref(LAB/'logs/business_v1.json'),'previous_stdout':ref(LAB/'logs/business_v1.stdout.txt'),'previous_stderr':ref(LAB/'logs/business_v1.stderr.txt'),'observed_readiness':{'canaries':9,'original_CatalogIndex_build_calls':2,'counts':[3,0],'CASE_records':0},'reason':'Gson.toJson a cerut accessDeclaredMembers pentru Map.of al emitterului. Se elimină serializarea reflectivă a harnessului; politica rămâne byte-identică.','new_harness':prep['harness_v2'],'diff':ref(diff),'prepared':ref(LAB/'Preparation_v3.json'),'policy_unchanged':ref(LAB/'probe.policy'),'serializer_tests':'Map/List/String/number/boolean/null; Unicode, quote, slash, newline, tab, null și tip necunoscut refuzat. Python va decoda separat rezultatul.','runtime_classpath':prep['runtime_classpath'],'core_runtime_present':False,'new_execution_yet':False}
n=OUT/'Calibrare_emitter_v2.json';dump(n,note);s=OUT/'SIGILIU_calibrare_emitter_v2.json';dump(s,{'utc':note['utc'],'files':[ref(n),ref(newpath),ref(diff),ref(LAB/'Preparation_v3.json'),ref(rp)],'immutable':True});print(json.dumps({'note':ref(n),'seal':ref(s)},ensure_ascii=False))
