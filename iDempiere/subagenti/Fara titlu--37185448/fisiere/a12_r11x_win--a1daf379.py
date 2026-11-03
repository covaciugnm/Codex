from a12_r11x_java import *
import difflib
outp=A/'fd_windows';outp.mkdir(exist_ok=True);name='TestComparatieSaga';source=C/'test'/(name+'.java');orig=source.read_text(encoding='utf8')
known=scratch/('cal_'+name+'_candidate_restored_paths')/(name+'.java');v=known.read_text(encoding='utf8');a=v.index('    static boolean tinut(Path f)');b=v.index('    /** CO-3:',a)
win="""    static boolean tinut(Path f) throws Exception {
        try (var c = java.nio.channels.FileChannel.open(f,java.nio.file.StandardOpenOption.READ,
                  com.sun.nio.file.ExtendedOpenOption.NOSHARE_READ, com.sun.nio.file.ExtendedOpenOption.NOSHARE_WRITE,
                  com.sun.nio.file.ExtendedOpenOption.NOSHARE_DELETE)) {
            return false;
        } catch (java.nio.file.FileSystemException e) {
            String reason = String.valueOf(e.getReason()).toLowerCase(java.util.Locale.ROOT);
            if (!reason.contains("another process") && !reason.contains("alt proces")) throw e;
            return true;
        }
    }

""";v=v[:a]+win+v[b:]
for tag,j in [('candidate',jar),('mounted_copy',scratch/'cesiro-contab.jar')]:
 dst=scratch/('windowsfd_'+tag);dst.mkdir(exist_ok=True);src=dst/(name+'.java');src.write_text(v,encoding='utf8');classpath=cp(dst,j);cc=cmd([java/'javac.exe','-proc:none','-encoding','UTF-8','-sourcepath',dst,'-cp',classpath,'-d',dst,src],C);assert cc.returncode==0,cc.stdout
 tester="""package com.eva.ro.contab.banca;
public class FDWinCheck {
 public static void main(String[] p) throws Exception {
  var f=java.nio.file.Files.createTempFile("a12-winfd",".sqlite");
  try {
   boolean first=TestComparatieSaga.tinut(f);
   boolean held;
   try(var stream=java.nio.file.Files.newInputStream(f)) { held=TestComparatieSaga.tinut(f); }
   boolean after=TestComparatieSaga.tinut(f);
   System.out.println("held before/open/after = "+first+"/"+held+"/"+after);
   if(first||!held||after)throw new AssertionError();
  } finally{java.nio.file.Files.delete(f);}
 }
}
"""
 fixture=dst/'FDWinCheck.java';fixture.write_text(tester,encoding='utf8');assert cmd([java/'javac.exe','-proc:none','-encoding','UTF-8','-sourcepath',dst,'-cp',classpath,'-d',dst,fixture],C).returncode==0
 for typ,clazz,fx in [('control_fd','FDWinCheck',None),('clean','TestComparatieSaga',None),('one_amount_mutation','TestComparatieSaga',scratch/'bank_mutate'),('clean_replayed','TestComparatieSaga',None)]:
  cmdline=[java/'java.exe','-Xmx215m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(scratch),'-Dline.separator=\n','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',classpath,'com.eva.ro.contab.banca.'+clazz]+([str(fx)]if fx else[]);res=cmd(cmdline,C);log=outp/(tag+'_'+typ+'.log');log.write_text(res.stdout,encoding='utf8')
  if tag=='candidate' and typ=='control_fd':rows=[]
  mk=[(i,s.strip())for i,s in enumerate(res.stdout.splitlines(),1)if re.search(r'^\s*(OK|FAIL)\s',s)]
  rows.append({'target':tag,'test':typ,'jar_sha':sha(j),'rc':res.returncode,'ok':sum(s.startswith('OK')for i,s in mk),'fail':[(i,s)for i,s in mk if s.startswith('FAIL')],'control_values':[s for s in res.stdout.splitlines()if 'held before/open/after'in s],'observed_size':len(mk),'log':ref(log)})
df=outp/'observare_descriptori.patch';df.write_text(''.join(difflib.unified_diff(orig.splitlines(True),v.splitlines(True),'Git TestComparatieSaga.java','Windows harness')),encoding='utf8');fr=outp/'FDWinCheck.java';fr.write_text(tester,encoding='utf8'); f=A/'Banca_109_martor_descriptor_Windows.json';save(f,{'utc':now(),'candidate':head,'prior':ref(A/'Calibrari_banca_si_registre_02.json'),'class_method':'Exclusive Windows FileChannel.open with NOSHARE flags. Only recognize an OS diagnostic for sharing violation; all other exceptions propagate. Independent positive/negative control, opened handle, release, plus original SQLite positive/negative test paths. Unmodified original Linux-specific /proc test remains separately unavailable in this Windows harness.','test_source':sha(source),'harness_sha':sha(src),'test_diff':ref(df),'control_source':ref(fr),'fixture_note':'Same 109 bank assertions on both audited bundles, immutable two TSV files; negative perturbs a single amount in disposable test state. Application JAR unmodified; no production documents, PostgreSQL, network or ERP UI invoked.','rows':rows});print(ref(f),[(r['target'],r['test'],r['rc'],r['ok'],len(r['fail']),r['control_values'])for r in rows],flush=True)

