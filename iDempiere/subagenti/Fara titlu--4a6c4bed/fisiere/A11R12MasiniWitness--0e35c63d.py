from pathlib import Path
import json,hashlib,subprocess,tempfile,shutil,datetime,zipfile
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A11/Val02_loturi'
J=Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert h(J)=='82099cd7f436a8fb4d532d8a46b83c62ae0e0176d86d9345c08598299d01d558'
lab=Path(tempfile.mkdtemp(prefix='a11-r12-masini-independent-',dir='D:/CodexWork')).resolve()
src=r'''import java.lang.reflect.*;
import java.util.*;
import java.nio.file.*;
import java.security.*;
public class IndependentMasini {
 static class Guard extends SecurityManager {
  final Path root; Guard(Path p){root=p;}
  public void checkPermission(Permission p){if(p instanceof RuntimePermission && p.getName().equals("setSecurityManager"))throw new SecurityException("guard immutable");}
  public void checkConnect(String h,int p){throw new SecurityException("network denied");}
  public void checkListen(int p){throw new SecurityException("listen denied");}
  public void checkExec(String c){throw new SecurityException("process denied");}
  public void checkWrite(String p){if(!Path.of(p).toAbsolutePath().normalize().startsWith(root))throw new SecurityException("write denied");}
  public void checkDelete(String p){checkWrite(p);}
 }
 static boolean oracle(String v){
  if(v==null || !v.matches("[0-9]{2}\\.[0-9]{2}\\.[0-9]{4}"))return false;
  int d=Integer.parseInt(v.substring(0,2)),m=Integer.parseInt(v.substring(3,5)),y=Integer.parseInt(v.substring(6));
  GregorianCalendar c=new GregorianCalendar(TimeZone.getTimeZone("UTC"),Locale.ROOT);c.clear();c.setLenient(false);c.set(y,m-1,d);
  try{c.getTimeInMillis();return true;}catch(IllegalArgumentException e){return false;}
 }
 public static void main(String[] a)throws Exception {
  System.setSecurityManager(new Guard(Path.of(a[0]).toAbsolutePath().normalize()));
  try {new java.net.Socket("127.0.0.1",9);throw new AssertionError();}catch(SecurityException e){System.out.println("GUARD_NETWORK_DENIED");}
  Class<?> c=Class.forName("com.eva.ro.contab.form.WSagaMasiniForm");
  System.out.println("ORIGIN="+c.getProtectionDomain().getCodeSource().getLocation());
  Method m=c.getDeclaredMethod("parseData",String.class);m.setAccessible(true);
  String[] cases={"08.07.2031","29.02.2028","30.04.2030","29.02.2100","31.06.2030","2031-07-08","",null};
  for(String v:cases){Object result=m.invoke(null,v);System.out.println("CASE="+String.valueOf(v)+"|"+oracle(v)+"|"+String.valueOf(result));}
 }
}'''
try:
 (lab/'IndependentMasini.java').write_text(src,encoding='utf8');(lab/'logging.properties').write_text('.level=OFF\n')
 compile_cmd=['C:/Program Files/Java/jdk-21/bin/javac.exe','-encoding','UTF-8','-d',str(lab),str(lab/'IndependentMasini.java')]
 c=subprocess.run(compile_cmd,cwd=lab,capture_output=True,text=True,encoding='utf8',timeout=30);assert c.returncode==0,c.stderr
 cp=';'.join([str(lab),str(J),'D:/CodexWork/a12-r5-classes/all_deps/*','D:/CodexWork/a05-support-jars/*'])
 cmd=['C:/Program Files/Java/jdk-21/bin/java.exe','-Djava.security.manager=allow','-Djava.util.logging.config.file='+str(lab/'logging.properties'),'-cp',cp,'IndependentMasini',str(lab)]
 r=subprocess.run(cmd,cwd=lab,capture_output=True,text=True,encoding='utf8',timeout=30);assert r.returncode==0,r.stderr
 rows=[dict(zip(['input','gregorian_valid','actual'],line[5:].split('|'))) for line in r.stdout.splitlines() if line.startswith('CASE=')]
 assert len(rows)==8 and sum(x['gregorian_valid']=='true' for x in rows)==3 and all(x['actual']=='null' for x in rows)
 assert 'GUARD_NETWORK_DENIED' in r.stdout and str(J).replace('\\','/').lower() in r.stdout.lower()
 for n,t in [('stdout.txt',r.stdout),('stderr.txt',r.stderr),('compile.stderr.txt',c.stderr)]: (lab/n).write_text(t,encoding='utf8')
 archive=O/'Martor_independent_Masini_v1.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
  for f in lab.iterdir():
   if f.is_file():z.write(f,f.name)
finally:
 assert lab.parent==Path('D:/CodexWork').resolve() and lab.name.startswith('a11-r12-masini-independent-');shutil.rmtree(lab)
o={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','actor':'A11, instanțiere absentă; metodă statică privată din JAR original','method':'Reflection pe parseData; oracol propriu GregorianCalendar strict, fără DateTimeFormatter și fără comparatorul uuuu al executorului. Gardă JVM cooperativă, nu sandbox OS.','jar':{'path':str(J),'sha256':h(J)},'command':cmd,'compile_command':compile_cmd,'cases':rows,'stdout':r.stdout,'stderr':r.stderr,'unique_cases':8,'valid_counterexamples':3,'negative_controls':5,'persistent_effect':'Numai artefacte de probă. Niciun PO, DB, browser sau saveEx nu este invocat.','conclusion':'Confirmat independent: date calendaristice valide returnează null; cinci intrări invalide/goale returnează null conform.','archive':{'path':str(archive),'sha256':h(archive)},'cleanup':{'own_scratch_absent':not lab.exists(),'own_processes':0,'operational_writes':0,'parent_masini_retained_folder_untouched':True},'runner_sha256':h(Path(__file__))}
p=O/'Martor_independent_Masini_v1.json';assert not p.exists();p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'path':str(p),'sha256':h(p),'cases':len(rows)}))
