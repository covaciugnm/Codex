import pathlib,json,hashlib,subprocess,os,datetime,shutil,zipfile
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';L=B/'A08_Catalog_paginare_lot05';O=B/'A11/Val05_loturi';LAB=pathlib.Path('D:/CodexWork/a11-catalog-oracle-l05-20261103');J=pathlib.Path('C:/Program Files/Java/jdk-21/bin');CORE=pathlib.Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar');GSON=pathlib.Path('D:/CodexWork/a05-r12-native-cache/com.google.gson_2.9.0.jar')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def dump(p,x):
 assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def inventory(root):return [{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
assert not LAB.exists();LAB.mkdir();O.mkdir(parents=True,exist_ok=True)
for x in ['source','classes','harness','empty','lib','logs','fixture/tenants/valid','fixture/tenants/empty','fixture/shared','fixture/media']:(LAB/x).mkdir(parents=True,exist_ok=True)
protocol=j(L/'Protocol_paginare_JSON_v1.json');sources=[];source_refs=[]
for s in protocol['source_identities']:
 if s['role']=='STATIC_ROUTE_CONTEXT_ONLY':continue
 src=L/'Sources'/s['path'];assert sha(src)==s['sha256'];dest=LAB/'source'/s['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);sources.append(dest);source_refs.append(ref(src))
for n in ['Addendum_dependenta_RegistruLegal_v1.json','Addendum_dependenta_SeoEngine_v1.json']:
 s=j(L/n)['source'];src=R/s['path'];assert sha(src)==s['sha256'];dest=LAB/'source'/s['repository_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);sources.append(dest);source_refs.append(ref(src))
assert len(sources)==12 and sha(CORE)=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3' and sha(GSON)=='c96d60551331a196dac54b745aa642cd078ef89b6f267146b705f2c2cbef052d';shutil.copyfile(GSON,LAB/'lib/gson.jar')
products=[{'id':'A11P'+str(i),'name':{'ro':'A11 Produs '+str(i)},'slug':{'ro':'a11-produs-'+str(i)},'price_ron':i*10,'sku':'A11SKU'+str(i),'category_ids':[],'is_in_stock':True,'images':[],'reviews':[]} for i in range(1,4)]
for tenant,items in [('valid',products),('empty',[])]:dump(LAB/f'fixture/tenants/{tenant}/catalog.json',{'categories':[],'collections':[],'products':items})
(LAB/'fixture/marker').write_text('A11_ONLY',encoding='utf8')
java=r'''import java.nio.file.*;import java.net.*;import java.util.*;
public final class IndependentPageProbe {
 interface Op{void run()throws Exception;}
 static int denies=0;static void denied(String n,Op op)throws Exception{try{op.run();throw new AssertionError("CANARY_ALLOWED "+n);}catch(SecurityException e){denies++;System.out.println("DENY|"+n);}}
 public static void main(String[]args)throws Exception{
  Path root=Path.of(args[0]);if(System.getSecurityManager()==null)throw new AssertionError("No policy");
  if(!Files.readString(root.resolve("fixture/marker")).equals("A11_ONLY"))throw new AssertionError("Marker");
  denied("write",()->Files.writeString(root.resolve("fixture/forbidden"),"NO"));
  denied("readOutside",()->Files.readString(Path.of("D:/CodexWork/a11-outside-forbidden")));
  denied("tcpLocal",()->{try(Socket s=new Socket()){s.connect(new InetSocketAddress("127.0.0.1",9),100);}});
  denied("tcpRemote",()->{try(Socket s=new Socket()){s.connect(new InetSocketAddress("203.0.113.1",9),100);}});
  denied("listen",()->{try(ServerSocket s=new ServerSocket(0)){} });
  denied("udp",()->{try(DatagramSocket s=new DatagramSocket(0)){} });
  denied("exec",()->new ProcessBuilder("cmd.exe","/c","exit","0").start());
  denied("guard",()->System.setSecurityManager(null));if(denies!=8)throw new AssertionError("Canaries");
  ProductCalls.run(root);
 }
 static final class ProductCalls{
  static com.eva.ro.webshop.store.StoreConfig store(String t){return new com.eva.ro.webshop.store.StoreConfig(800011,800011,t,"a11.invalid","a11-stage.invalid","a11",List.of("ro"),"ro","RON",com.eva.ro.webshop.store.StoreConfig.DataSource.JSON);}
  static void one(String name,String tenant,int page,boolean list){
   try{
    var src=new com.eva.ro.webshop.data.JsonCatalogSource();List<?> items;long total;
    if(list){var r=src.listProducts(store(tenant),new com.eva.ro.webshop.data.CatalogSource.ProductQuery("ro",Map.of(),"",page,48));items=r.products();total=r.total();}
    else{var r=src.queryProducts(store(tenant),"ro",null,null,page,48,"",Map.of());items=(List<?>)r.get("items");total=((Number)r.get("total")).longValue();}
    List<String> ids=new ArrayList<>();for(Object x:items)ids.add(String.valueOf(((Map<?,?>)x).get("id")));
    System.out.println("OBS|"+name+"|RETURN|"+total+"|"+String.join(",",ids));
   }catch(IndexOutOfBoundsException e){System.out.println("OBS|"+name+"|THROW|"+e.getClass().getName()+"|"+e.getMessage());}
  }
  static void run(Path root)throws Exception{
   var a=com.eva.ro.webshop.data.CatalogIndex.build(root.resolve("fixture/tenants/valid/catalog.json"));
   var b=com.eva.ro.webshop.data.CatalogIndex.build(root.resolve("fixture/tenants/empty/catalog.json"));
   if(a.totalProducts()!=3||b.totalProducts()!=0)throw new AssertionError("Index invalid");System.out.println("INDEX|3|0");
   one("A11-Q-POS","valid",1,false);one("A11-Q-BEFORE","valid",44739243,false);one("A11-Q-OVER","valid",44739244,false);one("A11-Q-WRAP","valid",268435457,false);one("A11-L-WRAP","valid",268435457,true);one("A11-EMPTY-OVER","empty",44739244,false);
  }
 }
}'''
(LAB/'harness/IndependentPageProbe.java').write_text(java,encoding='utf8')
policy='grant {\npermission java.io.FilePermission "'+LAB.as_posix()+'/-", "read";\npermission java.io.FilePermission "'+LAB.as_posix()+'", "read";\npermission java.util.PropertyPermission "*", "read";\n'+''.join('permission java.lang.RuntimePermission "getenv.'+k+'";\n' for k in ['EVA_WEBSHOP_DATA','EVA_WEBSHOP_SHARED','EVA_WEBSHOP_MEDIA'])+'};\n';(LAB/'policy').write_text(policy,encoding='utf8')
before=inventory(LAB/'fixture');compile_cmd=[str(J/'javac.exe'),'-encoding','UTF-8','-proc:none','-implicit:none','-sourcepath',str(LAB/'empty'),'-cp',str(LAB/'lib/gson.jar')+';'+str(CORE),'-d',str(LAB/'classes'),*[str(p) for p in sources],str(LAB/'harness/IndependentPageProbe.java')]
dump(LAB/'Admission_A11.json',{'utc':now(),'method':'Șase apeluri originale pe fixture proprie A11 și oracol propriu. Compile originalele separat; nu reusez harnessul sau clasele executorului.','protocol':ref(L/'Protocol_paginare_JSON_v1.json'),'gate':ref(B/'A11/Val05_preflight/Verdict_A11_protocol_paginare_JSON_v1.json'),'sources':source_refs,'cases':['A11-Q-POS','A11-Q-BEFORE','A11-Q-OVER','A11-Q-WRAP','A11-L-WRAP','A11-EMPTY-OVER'],'compiler':compile_cmd,'core_compile_only':ref(CORE),'policy':ref(LAB/'policy'),'harness':ref(LAB/'harness/IndependentPageProbe.java'),'fixture_before':before,'original_sources_modified':False})
c=subprocess.run(compile_cmd,cwd=LAB,capture_output=True,timeout=60);(LAB/'logs/javac.stdout').write_bytes(c.stdout);(LAB/'logs/javac.stderr').write_bytes(c.stderr);assert c.returncode==0,c.stderr.decode('utf8','replace')
env={k:v for k,v in os.environ.items() if k in ['SystemRoot','SYSTEMROOT','WINDIR','COMSPEC']};env.update({'EVA_WEBSHOP_DATA':str(LAB/'fixture/tenants'),'EVA_WEBSHOP_SHARED':str(LAB/'fixture/shared'),'EVA_WEBSHOP_MEDIA':str(LAB/'fixture/media'),'TEMP':str(LAB/'logs'),'TMP':str(LAB/'logs')})
args=[str(J/'java.exe'),'-Xmx128m','-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+(LAB/'policy').as_uri(),'-Xlog:class+load=info:file=logs/classload.log','-cp',str(LAB/'classes')+';'+str(LAB/'lib/gson.jar'),'IndependentPageProbe',str(LAB)];r=subprocess.run(args,cwd=LAB,env=env,capture_output=True,timeout=60);(LAB/'logs/java.stdout').write_bytes(r.stdout);(LAB/'logs/java.stderr').write_bytes(r.stderr);dump(LAB/'Execution_A11.json',{'utc':now(),'command':args,'returncode':r.returncode,'stdout':ref(LAB/'logs/java.stdout'),'stderr':ref(LAB/'logs/java.stderr'),'fixture_after':inventory(LAB/'fixture')});assert r.returncode==0,r.stderr.decode('utf8','replace')
text=r.stdout.decode('utf8');obs={x.split('|')[1]:x.split('|')[2:] for x in text.splitlines() if x.startswith('OBS|')};assert len(obs)==6 and sum(x.startswith('DENY|') for x in text.splitlines())==8 and 'INDEX|3|0' in text;assert before==inventory(LAB/'fixture')
expected={'A11-Q-POS':['RETURN','3','A11P1,A11P2,A11P3'],'A11-Q-BEFORE':['RETURN','3',''],'A11-Q-OVER':['RETURN','3',''],'A11-Q-WRAP':['RETURN','3',''],'A11-L-WRAP':['RETURN','3',''],'A11-EMPTY-OVER':['RETURN','0','']}
results=[{'id':k,'oracle':v,'observed':obs[k],'contract_satisfied':obs[k]==v} for k,v in expected.items()]
assert [x['contract_satisfied'] for x in results]==[True,True,False,False,False,False]
assert obs['A11-Q-OVER'][0:2]==obs['A11-EMPTY-OVER'][0:2]==['THROW','java.lang.IndexOutOfBoundsException'];assert obs['A11-Q-WRAP']==obs['A11-L-WRAP']==['RETURN','3','A11P1,A11P2,A11P3']
for src,dst in zip(source_refs,sources):assert sha(dst)==src['sha256']
archive=O/'Dovezi_contraoracol_A11_paginare_v1.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(LAB.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(LAB).as_posix())
out={'schema':'A11.R12.Val05.pagination.counteroracle.v1','utc':now(),'reviewer':'A11 independent','method':'Fixture proprie cu trei ID-uri A11 și catalog gol, cele 12 surse originale recompilate separat, harness propriu fără Gson ca emitter, șase apeluri selectate la metodele originale; oracolul așteaptă gol pentru orice pagină peste catalog folosind întregi Python fără overflow.','results':results,'canaries':{'positive_read':1,'denied':8},'index_witness':{'valid':3,'empty':0},'fixtures_unchanged':True,'sources_unchanged':True,'core_runtime_present':False,'archive':ref(archive),'counts':{'independent_calls':6,'conformant':2,'counterexamples':4},'limits':['Acești șase martori nu se adaugă celor 16 cazuri A08 ca și cum ar fi scenarii de produs noi.','Același overflow este reprodus la queryProducts și listProducts. Nici HTTP, UI, DB, OSGi, cache concurent sau catalog real nu au fost executate.','Compilarea și folosirea tranzitivă a dependențelor nu validează fișierele integral.'],'product_score':None,'operational_writes':0,'cleanup_pending':'Procesul JVM s-a închis. Scratchul propriu va fi eliminat numai prin comandă explicită după verificarea țintei; verdict de cleanup separat.'}
op=O/'Contraoracol_A11_paginare_v1.json';dump(op,out);rp=O/'Runner_contraoracol_A11_paginare_v1.py';assert not rp.exists();shutil.copyfile(pathlib.Path(__file__),rp);seal=O/'SIGILIU_contraoracol_A11_paginare_v1.json';dump(seal,{'utc':now(),'files':[ref(op),ref(archive),ref(rp)],'immutable':True});print(json.dumps({'report':ref(op),'seal':ref(seal),'cases':results},ensure_ascii=False))
