from a12_r10_jvm import *
from a12_r8_jvm import java,sec,base,repo,plug,policy,T,execute,tr
import subprocess,re,os,hashlib
from concurrent.futures import ThreadPoolExecutor
srcp=next(repo.glob('**/PdfDocument.java'));src=srcp.read_text(encoding='utf8');names=list(dict.fromkeys(re.findall(r'"(DejaVu[A-Za-z-]+\.ttf)"',src)));fontdir=Path('D:/CodexWork/a12-r10-local/fonts');fontdir.mkdir(exist_ok=True);fonts={}
for n in names:
 f=fontdir/n
 if not f.exists():
  p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','cat /usr/share/fonts/truetype/dejavu/'+n],capture_output=True);p.check_returncode();f.write_bytes(p.stdout)
 assert f.stat().st_size>10000;fonts[n]=sha(f)
des=P10/'Zone_A09';scratch=Path('D:/CodexWork/a12-r10-local');sv="""public class FontHarnessR10 { public static void main(String[] a) throws Exception { java.lang.reflect.Field f=Class.forName("com.eva.ro.contab.documente.PdfDocument").getDeclaredField("dirFonturi"); f.setAccessible(true); f.set(null,a[0]); TracerA12.main(new String[]{a[1]}); } }"""
def go(tag):
 d=scratch/('print-observe-'+tag);jar=sec/('cod-master-contab.jar'if tag=='git'else'com.eva.ro.contab_13.0.0.jar');cp=';'.join(map(str,[d,jar,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/a12-r6-preprobes/deps/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',plug/'src']));ff=d/'FontHarnessR10.java';ff.write_text(sv,encoding='utf8');cc=execute([java/'javac.exe','-proc:none','-cp',cp,'-d',d,ff],plug);assert cc.returncode==0,cc.stdout[-350:];p=plug/'test/TestT204Documente.java';pk=re.search(r'^package ([\w.]+);',p.read_text(encoding='utf8'),re.M);cn=(pk[1]+'.'if pk else'')+'TestT204Documente';rr=execute([java/'java.exe','-Xmx300m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(T),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,'FontHarnessR10',fontdir,cn],plug);fo=des/(tag+'_TestT204Documente_avec_fonts.log');fo.write_text(rr.stdout,encoding='utf8');a=rr.stdout.splitlines();return {'target':tag,'jar_sha':sha(jar),'test':cn,'exit':rr.returncode,'log':source(fo),'summary':[z[:300]for z in a if z.startswith(('REZULTAT','FAIL'))][-7:],'early_problem':[z for z in a if 'exception' in z.lower()][:2]}
with ThreadPoolExecutor(max_workers=2)as ex:vr=list(ex.map(go,['git','instalat']))
f=des/'Calibrare_fonts_T204.json';wr(f,{'utc':now(),'source_font_paths':'Saga host /usr/share/fonts/truetype/dejavu/'+str(names),'files_hash':fonts,'test_only_hook':'Reflection sets existing package-private test hook PdfDocument.dirFonturi to the temporary font directory. No product file was changed. Predicate and PDF-oracle extraction are the original application/test.','wrapper':sv,'java':vr});print(sha(f),[(z['target'],z['exit'],z['summary'],z['early_problem'])for z in vr])

