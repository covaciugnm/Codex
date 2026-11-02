from a12_r8_review import *
from a12_r6_exec import java,plug,base,sec,repo,T,policy,execute,ThreadPoolExecutor
import subprocess,shutil,hashlib,base64,os
T8=Path('D:/CodexWork/a12-r8-runs');T8.mkdir(exist_ok=True);J=P/'JVM';J.mkdir(exist_ok=True)
tr=Path('D:/CodexWork/a12-r7/TracerA12.java')
ss=['TestComparatieSaga','TestComparatieSagaEcran','TestT201Registre','TestT201Ecrane','TestT173Numar','TestDocumente','TestT29Acoperire','TestT29Catalog','TestT204Documente','TestT204Ecrane','TestT227VerificareImport','TestT220Corelez','TestT22Stripe','TestT22Trimitere','TestT22Preluare','TestT314Meniu','TestT314Rol','TestT28Meniu','TestT22FisaCanal','TestT22Api','TestT22Ramburs','TestT22Livrare','TestT22Validare','TestT195Pilon2','TestT199Parametri']
def go(z):
 tag,suite=z;dest=T8/(tag+'_'+suite);dest.mkdir(exist_ok=True);jar=sec/('cod-master-contab.jar' if tag=='git'else'com.eva.ro.contab_13.0.0.jar');src=plug/'test'/(suite+'.java');content=src.read_text(encoding='utf8');pkg=re.search(r'^package ([\w.]+);',content,re.M);cn=(pkg[1]+'.'if pkg else'')+suite
 cp=';'.join(map(str,[dest,jar,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/a12-r6-preprobes/deps/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',plug/'src']))
 cc=execute([java/'javac.exe','-J-Xmx220m','-g:lines,source','-encoding','UTF-8','-proc:none','-cp',cp,'-sourcepath',plug/'test','-d',dest,tr,src],plug);rr=execute([java/'java.exe','-Xmx270m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Dline.separator=\n','-Djava.io.tmpdir='+str(T),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,'TracerA12',cn],plug) if cc.returncode==0 else None
 p=J/(tag+'_'+suite+'.log');v=cc.stdout+'\n'+(rr.stdout if rr else'');p.write_text(v,encoding='utf8')
 return {'target':tag,'suite':suite,'file':src.relative_to(repo).as_posix(),'source_sha':sha(src),'jar_sha':sha(jar),'compile':cc.returncode,'exit':rr.returncode if rr else None,'log':source(p),'traced':v.count('ANCHOR:')}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4)as px:m=list(px.map(go,[(t,n)for n in ss for t in ['git','instalat']]))
 wr(J/'Executii.json',m);print(len(m),sum(x['traced']for x in m),sum(x['exit']==0 for x in m))

