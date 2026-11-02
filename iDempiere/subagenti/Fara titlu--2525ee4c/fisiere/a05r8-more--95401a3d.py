from pathlib import Path
import json,os,subprocess as sp,importlib.machinery,datetime,re,concurrent.futures,sys
w=Path('D:/CodexWork/a05r8');r=importlib.machinery.SourceFileLoader('r8run','D:/CodexWork/a05r8-run.py').load_module()
dest=r.out/'JVM_service';dest.mkdir(exist_ok=True)
cp=r.classpath+';D:/CodexWork/a12-r6-preprobes/deps/*'
wrap=w/'AuditR8Suite.java';wrap.write_text('''public class AuditR8Suite {
 public static void main(String[] args) throws Exception {
  var f=Class.forName("com.eva.ro.contab.documente.PdfDocument").getDeclaredField("dirFonturi");
  f.setAccessible(true); f.set(null,"D:/CodexWork/a05-test-adapt/fonts");
  Class.forName(args[0]).getMethod("main",String[].class).invoke(null,(Object)new String[0]);
 }
}''',encoding='utf8')
assert r.run([r.jd/'javac.exe','-cp',cp,'-d',w/'classes',wrap])[0]==0
res=[]
initial=json.loads((r.out/'JVM_index_progres.json').read_text(encoding='utf8'))
retry=[x['suite'] for x in initial['suites'] if x['exit']!=0]
todo=list(dict.fromkeys(retry+r.allow[len(initial['suites']):]))
def test(name):
 f=r.plug/'test'/(name+'.java');io=r.bo(f.read_bytes());assert r.gj('rev-parse',r.cut+':'+f.relative_to(r.root).as_posix())==io
 pkg=re.search(r'^package ([\w.]+);',f.read_text(encoding='utf8'),re.M);cl=(pkg.group(1)+'.' if pkg else '')+name
 b,o=r.run([r.jd/'javac.exe','-encoding','UTF-8','-cp',cp,'-sourcepath',r.plug/'test','-d',w/'classes',f])
 status=None
 if b==0:
  try:
   status,t=r.run([r.jd/'java.exe','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dline.separator=\n','-Djava.security.manager','-Djava.security.policy=='+r.pol.as_posix(),'-Djava.io.tmpdir='+(w/'tmp').as_posix(),'-cp',cp,'AuditR8Suite',cl],timeout=75);o+=t
  except sp.TimeoutExpired as e:
   status='TIMEOUT_75s';o+=(e.stdout or b'').decode('utf8','replace')+'\nTIMEOUT_75s'
 path=dest/(name+'.txt');path.write_text(o,encoding='utf8')
 return {'suite':name,'src_blob_oid':io,'build':b,'exit':status,'log':'JVM_service/'+path.name,'hash':r.sha(path),'ok_lines':len(re.findall(r'^\s*ok\s',o,re.I|re.M)),'fail_lines':len(re.findall(r'^\s*fail\s',o,re.I|re.M))}
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for x in ex.map(test,todo):res.append(x);r.dump(dest/'index.json',{'scope':'aceleași fișiere test, fonturile livrate prin câmpul documentat al producției, dependențe adăugate; test original neschimbat și rulări cu limită de timp conservate separat.', 'rows':res});print(x['suite'],x['exit'],flush=True)
