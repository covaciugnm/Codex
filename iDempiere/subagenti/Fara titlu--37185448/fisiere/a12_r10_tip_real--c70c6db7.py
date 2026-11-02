from a12_r10_jvm import *
from a12_r8_jvm import java,sec,base,repo,plug,policy,T,execute,tr
from concurrent.futures import ThreadPoolExecutor
import os,re
des=P10/'Zone_A09';des.mkdir(exist_ok=True);scratch=Path('D:/CodexWork/a12-r10-local');ss=['TestT29Catalog','TestT204Documente','TestT204Ecrane']
def ru(tag):
 d=scratch/('print-observe-'+tag);d.mkdir(exist_ok=True);jar=sec/('cod-master-contab.jar'if tag=='git'else'com.eva.ro.contab_13.0.0.jar');cp=';'.join(map(str,[d,jar,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/a12-r6-preprobes/deps/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',plug/'src']))
 sr=[];pro=[]
 for k in ss:
  p=plug/'test'/(k+'.java');st=p.read_text(encoding='utf8');orig='if (c)\n            ok++;';assert st.count(orig)==1;dest=d/(k+'.java');dest.write_text(st.replace(orig,'if (c) { ok++; System.out.println("OK   " + m); }'),encoding='utf8');sr+=[dest];pro.append({'test':k,'original':sha(p),'observer_copy':sha(dest),'repository_path':p.relative_to(repo).as_posix()})
 cc=execute([java/'javac.exe','-J-Xmx240m','-g:lines,source','-encoding','UTF-8','-proc:none','-cp',cp,'-sourcepath',plug/'test','-d',d,tr,*sr],plug);new=[]
 for k in ss:
  p=next(p for p in sr if p.stem==k);pkg=re.search(r'^package ([\w.]+);',p.read_text(encoding='utf8'),re.M);pkg=pkg[1]+'.' if pkg else '';rr=execute([java/'java.exe','-Xmx280m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(T),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,'TracerA12',pkg+k],plug)if cc.returncode==0 else None
  f=des/(tag+'_'+k+'_observable.log');f.write_text(cc.stdout+'\n'+(rr.stdout if rr else''),encoding='utf8');new.append({'test':k,'compile':cc.returncode,'exec':rr.returncode if rr else None,'target':tag,'jar':sha(jar),'log':source(f)})
 return {'driver':'Prints existing test label on success; original predicate, count, data, ordering and failures unchanged. TestT204Ecrane is compiled alongside TestT204Documente.','source_provenance':pro,'results':new}
with ThreadPoolExecutor(max_workers=2)as ex:v=list(ex.map(ru,['git','instalat']))
f=des/'Suita_individual_observable.json';wr(f,{'utc':now(),'runs':v,'relationship_to_original':source(des/'Suita_tiparituri.json')});print(sha(f),[[(q['test'],q['exec'])for q in z['results']]for z in v])
