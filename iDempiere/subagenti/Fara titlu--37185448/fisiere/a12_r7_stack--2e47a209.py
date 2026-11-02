from a12_r7_pg_cui import *
from functools import lru_cache
classes=['TestPutaway','TestListaPicking','TestFefo','TestStudiiSalariat','TestLoturi','TestT58Alarma','TestT25Ecran','TestT159LotA','TestT156MutareCont','TestT354Set','TestT354Disponibil','TestT217Filtru','TestT220Corelez','TestT331Oglinda','TestLocatiiMultiple','TestReges']
j='''import java.io.*;import java.nio.charset.StandardCharsets;import java.lang.reflect.*;
public class TracerA12 {public static void main(String[] a)throws Exception{var old=System.out;System.setOut(new PrintStream(old,true,StandardCharsets.UTF_8) {
 public synchronized void println(String s){old.println(s);if(s!=null && s.stripLeading().matches("(?i)(ok|fail)\\\\s+.*")){var loc=new StringBuilder();for(var x:Thread.currentThread().getStackTrace()){if(x.getClassName().contains("Test") && !x.getClassName().contains("TracerA12"))loc.append(x.getFileName()).append(":").append(x.getLineNumber()).append(":").append(x.getMethodName()).append("|");}old.println("ANCHOR:"+java.util.Base64.getEncoder().encodeToString(s.getBytes(StandardCharsets.UTF_8))+"|"+loc);}}
});var target=Class.forName(a[0]);target.getMethod("main",String[].class).invoke(null,(Object)new String[0]);}}'''
tf=T7/'TracerA12.java';tf.write_text(j,encoding='utf8')
def case(z):
 tag,suite=z;dest=T7/('stack_'+tag+'_'+suite);dest.mkdir(exist_ok=True);j=sec/('cod-master-contab.jar'if tag=='git'else 'com.eva.ro.contab_13.0.0.jar');src=plug/'test'/(suite+'.java');body=src.read_text(encoding='utf8');pkg=re.search(r'^package ([\w.]+);',body,re.M);cname=(pkg[1]+'.'if pkg else '')+suite;cp=';'.join(map(str,[dest,j,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/a12-r6-preprobes/deps/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',plug/'src']));extra=[plug/'test/TestT16Declaratii.java',plug/'test/TestT29Perioade.java']if suite=='TestT159LotA'else[]
 cc=execute([java/'javac.exe','-J-Xmx240m','-g:lines,source','-encoding','UTF-8','-proc:none','-cp',cp,'-sourcepath',plug/'test','-d',dest,tf,*extra,src],plug);rr=execute([java/'java.exe','-Xmx330m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Dline.separator=\n','-Djava.io.tmpdir='+str(T),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,'TracerA12',cname],plug)if cc.returncode==0 else None
 root=RP/'stack';root.mkdir(exist_ok=True);p=root/(tag+'_'+suite+'.log');txt=cc.stdout+'\n'+(rr.stdout if rr else '');p.write_text(txt,encoding='utf8');return{'target':tag,'suite':suite,'test_source':src.relative_to(repo).as_posix(),'sha_source':sha(src),'jar_sha':sha(j),'compile':cc.returncode,'exit':rr.returncode if rr else None,'log':p.relative_to(RP).as_posix(),'sha':sha(p),'traced':txt.count('ANCHOR:')}
if __name__=='__main__':
 todo=[(tag,k)for k in classes if (plug/'test'/(k+'.java')).is_file() for tag in ['git','instalat']]
 with ThreadPoolExecutor(max_workers=4)as pool:
  vals=[]
  for v in pool.map(case,todo):vals.append(v)
 wr(RP/'stack_exec.json',vals);print('calibrated',len(vals),sum(v['traced']for v in vals),[(v['suite'],v['exit'])for v in vals if v['target']=='git'])

