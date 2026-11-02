from a12_r10_base import *
from a12_r6_exec import java,base,sec,plug,repo,execute,policy
import importlib.util,shutil,os
from concurrent.futures import ThreadPoolExecutor
repo=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');framework=repo/'tools/teste/t227/mutanti.py';spec=importlib.util.spec_from_file_location('original_t227_mut',framework);framework_mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(framework_mod);sub=Path('D:/CodexWork/a12-r10-local/mut');sub.mkdir(exist_ok=True);out=P10/'T227_mutanti';out.mkdir(exist_ok=True);old=Path('D:/CodexWork/a12-r10-local/jvm/git_TestT227VerificareImport')
def batch(z):
 id,label,sfile,a,b,oracle=z;dest=sub/id;dest.mkdir(exist_ok=True);plugcopy=dest/'plugin';jardst=dest/'classes';jardst.mkdir(exist_ok=True);jar=sec/'cod-master-contab.jar';actual=repo/sfile;rel=actual.relative_to(plug)
 if not plugcopy.exists():
  shutil.copytree(plug/'src',plugcopy/'src',copy_function=os.link)
 for ref,copy in [(plug/'test/fixtures/help/ecrane.tsv',plugcopy/'test/fixtures/help/ecrane.tsv'),(plug.parent/'com.eva.ro.saga.theme/src/com/eva/ro/saga/theme/EvaSagaMenuDef.java',dest/'com.eva.ro.saga.theme/src/com/eva/ro/saga/theme/EvaSagaMenuDef.java')]:
  copy.parent.mkdir(parents=True,exist_ok=True)
  if not copy.is_file():os.link(ref,copy)
 v=plugcopy/rel;s=actual.read_text(encoding='utf8');count=s.count(a)
 meta={'id':id,'change':label,'original_exact_count':count,'canonical_source':sfile,'canonical_source_sha':sha(actual),'expected_suite_observer':oracle,'artifact':sha(jar),'mutation':{'before':a,'after':b},'product_mutated':False}
 if count!=1:return meta|{'applied':False}
 # Publication tree source is never modified. Local hardlink is unlinked first, then private staging bytes written.
 assert v.resolve().is_relative_to(sub.resolve());v.unlink();v.write_text(s.replace(a,b,1),encoding='utf8');tmp=Path('D:/CodexWork/a12-r6-preprobes')
 cp=';'.join(map(str,[jardst,old,jar,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',str(tmp/'deps/*'),plug/'src']));c=execute([java/'javac.exe','-encoding','UTF-8','-proc:none','-cp',cp,'-sourcepath','','-d',jardst,v],plugcopy)
 p=out/(id+'.log');res=execute([java/'java.exe','-Xmx300m','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(tmp),'-cp',cp,'TracerA12','com.eva.ro.contab.form.TestT227VerificareImport'],plugcopy)if c.returncode==0 else None;p.write_text(c.stdout+'\n'+(res.stdout if res else''),encoding='utf8');ls=p.read_text(encoding='utf8').splitlines()
 return meta|{'applied':True,'compiled':c.returncode,'exit':res.returncode if res else None,'source_copy_sha':sha(v),'observed_failures':[{'line':i,'text':l.strip()}for i,l in enumerate(ls,1)if re.match(r'^\s*FAIL\s+',l)][:18],'tail_notes':[s[:240]for s in ls if re.search('exception in thread|Caused by|error:|not found',s,re.I)][:5],'run_log':source(p)}
if __name__=='__main__':
 sel=[v for v in framework_mod.M if v[0]in ['M-7','M-21','M-27a','M-27b','M-28a','M-28b']]
 proto=sel[0];sel.insert(0,('ORIGINAL','Control în aceeași topologie de surse şi clase',proto[2],proto[3],proto[3],'0 FAIL'))
 with ThreadPoolExecutor(max_workers=2)as px:vv=list(px.map(batch,sel))
 f=P10/'T227_mutanti_nominali.json';wr(f,{'at':now(),'controls':vv,'official_harness':{'file':framework.relative_to(repo).as_posix(),'sha256':sha(framework)},'baseline':source(P10/'JVM/git_TestT227VerificareImport.log'),'qualification':'Rulare JVM din arbore mutat folosind copia fișierului țintă şi bytecode-ul dinaintea JAR-ului Git; nu încercarea pe JAR instalat unde tipul nu există. Contraproba trebuie să aibă FAIL nominal, nu doar ieșire nenulă.'});print(sha(f),[(x['id'],x.get('compiled'),x.get('exit'),len(x.get('observed_failures',[])),x.get('tail_notes',[])[:1])for x in vv])

