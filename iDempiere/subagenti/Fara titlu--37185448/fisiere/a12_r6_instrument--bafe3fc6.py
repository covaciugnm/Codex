from a12_r6_exec import *
from a12_r6_mutations_cal import original
import re,ast,uuid
CLI={'TestT204Ecrane':'com.eva.ro.contab.form.TestT204Ecrane','TestT314Meniu':'TestT314Meniu','TestT29Tiparire':'TestT29Tiparire'}
def test(z):
 tag,n,mut=z
 j=sec/('cod-master-contab.jar'if tag=='git'else 'com.eva.ro.contab_13.0.0.jar');dest=T/f'cal_{tag}_{n}';dest.mkdir(exist_ok=True);tmp=dest/'tmp';tmp.mkdir(exist_ok=True);src=plug/'test'/(n+'.java');s=src.read_text(encoding='utf8');cp=';'.join(map(str,[dest,j,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',str(deps/'*'),plug/'src']));p=dest/src.name;cl=CLI[n];extra=[];additional=[]
 if n=='TestT204Ecrane':
  s=s.replace('if (c)\n            ok++;\n        else {','if (c) {ok++; System.out.println("OK " + m);}\n        else {');assert 'System.out.println("OK " + m)' in s
 if n=='TestT314Meniu':s=s.replace('c.getProtectionDomain().getCodeSource().getLocation().getPath()', 'Path.of(c.getProtectionDomain().getCodeSource().getLocation().toURI()).toString()')
 if n=='TestT29Tiparire':
  extra_src=dest/'FonturiA12.java';extra_src.write_text('public class FonturiA12 { public static void main(String[] args) throws Exception {var field=Class.forName("com.eva.ro.contab.documente.PdfDocument").getDeclaredField("dirFonturi");field.setAccessible(true);field.set(null,"C:/Windows/Fonts");TestT29Tiparire.main(args);}}',encoding='utf8');additional=[extra_src];cl='FonturiA12'
 p.write_text(s,encoding='utf8');cc=execute([java/'javac.exe','-encoding','UTF-8','-proc:none','-cp',cp,'-d',dest,*additional,p],plug)
 work=plug
 if mut and n=='TestT204Ecrane':
  work=T/('mut_'+mut+'_r6'); (work/'test').mkdir(exist_ok=True);shutil.copytree(plug/'test/fixtures',work/'test/fixtures',dirs_exist_ok=True)
 if mut and n=='TestT314Meniu':
  theme=plug.parent/'com.eva.ro.saga.theme';mtheme=T/'mut_theme_314';ssrc=mtheme/'src/com/eva/ro/saga/theme';ssrc.mkdir(exist_ok=True,parents=True)
  for fn in ['EvaSagaMenuDef.java','EvaSagaHeaderPanel.java']:shutil.copyfile(theme/'src/com/eva/ro/saga/theme'/fn,ssrc/fn)
  f=ssrc/'EvaSagaMenuDef.java';st=f.read_text(encoding='utf8');pattern=r'new Item\("([^"]+)", null, null\)';m=re.search(pattern,st)
  if not m:raise RuntimeError('no exact mutable leaf')
  f.write_text(st[:m.start()]+m.group().replace(', null, null)',', "FISA_TEST_NOMINAL", null)')+st[m.end():],encoding='utf8');extra=[mtheme,repo/'tools/teste/t314/arbore_vanzari.tsv']
 cmd=[java/'java.exe','-Xmx350m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Dline.separator=\n','-Djava.io.tmpdir='+str(tmp),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,cl,*extra];rr=execute(cmd,work)if cc.returncode==0 else None
 txt=cc.stdout+'\n'+(rr.stdout if rr else '');log=E6/('rec_'+tag+'_'+n+'_'+(mut or 'martor')+'.log');log.write_text(txt,encoding='utf8')
 return {'suite':n,'target':tag,'mutant':mut,'source_sha256':sha(src),'test_adapter_sha256':sha(p),'test_adapter':str(p),'adapter_intent':{'TestT314Meniu':'Normalizare URL→Path numai în javap Windows.','TestT204Ecrane':'Tipărire mesaje și pentru aserțiuni reușite; aceleași condiții și contoare.','TestT29Tiparire':'Adaptor FonturiA12 desemnează directorul real al fonturilor pe acest host; sursa testului neschimbată.'}[n],'jar_sha':sha(j),'compile':cc.returncode,'run':rr.returncode if rr else None,'raw':log.name,'raw_sha':sha(log),'witness':[(i,l[:475])for i,l in enumerate(txt.splitlines(),1)if re.search(r'^(?:\s*FAIL|Exception in thread|REZULTAT)|19/19 situri|18/19 situri|T314-inlucru|LR-2: cazurile.*19|rolul|refuzul pe rol',l)][-18:]}
if __name__=='__main__':
 trg=[(z,n,mut)for z in ['git','instalat']for n,mut in [('TestT314Meniu',None),('TestT204Ecrane',None),('TestT29Tiparire',None)]]
 # Avoid parallel compile of the same target directory while the same class is running.
 with ThreadPoolExecutor(max_workers=3)as ex:r=list(ex.map(test,trg))
 for m in ['M01','M02','M03']:
  with ThreadPoolExecutor(max_workers=2)as ex:r.extend(ex.map(test,[(z,'TestT204Ecrane',m)for z in ['git','instalat']]))
 wr(E6/'JVM_calibrat_r6.json',r);print([(a['suite'],a['target'],a['mutant'],a['compile'],a['run'],a['witness'][-1:]if a['run']!=0else '')for a in r])

