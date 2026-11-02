from a12_r4_suites import cmd,java,tmp,base,sec,plug,repo,policy
from a12_r3_survey import *
import concurrent.futures as cf,shutil
R=E/'R5';out=R/'calibrare';out.mkdir(exist_ok=True);temp=Path('D:/CodexWork/a12-r5-classes');temp.mkdir(exist_ok=True);policytext=policy.read_text(encoding='utf8')
# Runtime may inspect test dependencies/JAR through javap; neither business credentials nor sockets are granted.
pol=temp/'read-network-denied.policy';pol.write_text(policytext+'grant {permission java.io.FilePermission "C:/Program Files/Java/jdk-21/bin/javap","execute";permission java.io.FilePermission "C:/Program Files/Java/jdk-21/bin/javap.exe","execute";};',encoding='utf8')
names=['TestListaPicking','TestListaPickingEcran','TestFefo','TestPutaway','TestListaAmplasare','TestLoturi','TestLoturiEcrane','TestApiMobilInventar','TestReges','TestRegesPoarta','TestComparatieSaga','TestInchidereTVA','TestT58Inchidere','TestT58Alarma','TestT159LotA','TestT159LotB','TestT159LotC','TestT159LotD','TestT03Lot5','TestT03Front','TestT40L2Motor','TestT29Catalog','TestT29Acoperire','TestT27eHarta','TestT354Set','TestT354Disponibil']
def runner(z):
 tag,j,f=z;name=f.stem;dest=temp/(tag+'_'+name);dest.mkdir(exist_ok=True);body=f.read_text(encoding='utf8');pkg=re.search(r'^package ([\w.]+);',body,re.M);cl=(pkg[1]+'.'if pkg else '')+name;cp=';'.join([str(dest),str(j),str(base),str(next(sec.glob('org.adempiere.base.process_*.jar'))),'D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',str(plug/'src')]);helpers=[p for p in (plug/'test').glob('*.java')if p!=f and re.search(r'\b'+re.escape(p.stem)+r'\b',body) and p.stat().st_size<65000 and (not p.stem.startswith('Test')or p.stem=='TestT16Declaratii')];cc=cmd([java/'javac.exe','-J-Xmx240m','-proc:none','-encoding','UTF-8','-cp',cp,'-sourcepath','','-d',dest,*helpers,f]);args=[]
 if cc.returncode==0:
  rr=cmd([java/'java.exe','-Xmx310m','-Dline.separator=\n','-Djava.security.manager','-Djava.security.policy=='+pol.as_uri(),'-Djava.io.tmpdir='+str(tmp),'-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,cl,*args])
 else:rr=None
 txt=cc.stdout+'\n'+(rr.stdout if rr else '');p=out/(tag+'_'+name+'.log');p.write_text(txt,encoding='utf8');lines=txt.splitlines();return {'suite':name,'target':tag,'test_file':str(f.relative_to(repo)).replace('\\','/'),'test_sha':sha(f),'jar_sha':sha(j),'compile':cc.returncode,'run':rr.returncode if rr else None,'verified_log':p.name,'log_sha':sha(p),'summary':[[i,l[:350]]for i,l in enumerate(lines,1)if re.search(r'REZULTAT|FAIL |Caused by:|Exception in thread|error:',l)][-9:]}
if __name__=='__main__':
 jobs=[(tag,j,plug/'test'/(n+'.java'))for n in names if (plug/'test'/(n+'.java')).exists() for tag,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]]
 with cf.ThreadPoolExecutor(max_workers=4) as px:res=list(px.map(runner,jobs))
 wr(out/'executii.json',res);print('runs',len(res),'compiled',sum(v['compile']==0 for v in res),'exit0',sum(v['run']==0 for v in res))

