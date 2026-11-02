from a12_r3_java import cmd,java,tmp,base,sec,plug,repo,policy
from a12_r3_survey import *
import concurrent.futures as cf,collections
o=E/'R4/Java';o.mkdir(parents=True,exist_ok=True);tt=Path('D:/CodexWork/a12-r4-java');tt.mkdir(exist_ok=True)
patt=re.compile('^TestT(02|07|08|10|12|17|18|22|27|28|32|33|35|36|40|43|152|154|161|170|176|179|187|197|200|211|212|215|216|217|218|223|224|225|227|232|239|244|248|252|253|254|257|259|263|287|303|312|313|314|327|333|334|335|336|337|338|349|350|351|352|353|354|355|356|359|361|362|363|364|365|366|368|369|370|371)(?![0-9])')
files=[f for f in sorted((plug/'test').glob('Test*.java')) if (patt.match(f.stem) or f.stem=='TestAjutor') and f.stat().st_size<120000 and 'static void main(' in f.read_text(encoding='utf8',errors='replace')];old=rd(E/'R3/probe_unitare/executii.json')+rd(E/'R3/probe_unitare/executii_suplimentare.json');done={x['suite']for x in old}
files=[f for f in files if f.stem not in done];part=collections.defaultdict(list)
def rr(z):
 tag,jar,f=z;name=f.stem;dest=tt/(tag+name);dest.mkdir(exist_ok=True);bb=f.read_text(encoding='utf8');pkg=re.search(r'^package ([\w.]+);',bb,re.M);klass=(pkg[1]+'.'if pkg else '')+name;cp=';'.join([str(dest),str(jar),str(base),str(next(sec.glob('org.adempiere.base.process_*.jar'))),'D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',str(plug/'src')]);helpers=[p for p in (plug/'test').glob('*.java') if p!=f and re.search(r'\b'+re.escape(p.stem)+r'\b',bb) and (not p.stem.startswith('Test') or p.stem=='TestT16Declaratii') and p.stat().st_size<160000]
 cc=cmd([java/'javac.exe','-J-Xmx220m','-proc:none','-encoding','UTF-8','-cp',cp,'-sourcepath','','-d',dest,*helpers,f]);r=cmd([java/'java.exe','-Xmx224m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(tmp),'-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,klass])if cc.returncode==0 else None;txt=cc.stdout+'\n'+(r.stdout if r else '');log=o/(tag+'_'+name+'.log');log.write_text(txt,encoding='utf8');lines=txt.splitlines();return {'suite':name,'target':tag,'source':str(f.relative_to(repo)).replace('\\','/'),'source_sha256':sha(f),'jar_sha256':sha(jar),'helpers':[v.stem for v in helpers],'compile_exit':cc.returncode,'run_exit':r.returncode if r else None,'log':log.name,'log_sha256':sha(log),'summary':[(j,line[:370])for j,line in enumerate(lines,1)if re.search(r'REZULTAT|TOTAL |error:|Exception in thread|^\s*FAIL\b',line,re.I)][-12:]}
if __name__=='__main__':
 result=[]
 with cf.ThreadPoolExecutor(max_workers=5) as pool:
  for ix,v in enumerate(pool.map(rr,[(t,j,f)for f in files for t,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]])):
   result.append(v)
   if ix%10==0:wr(o/'progress.json',{'completed':len(result),'expected':len(files)*2})
 wr(o/'executii.json',result);print('fixtures',len(files),'runs',len(result),'ran',sum(x['run_exit']is not None for x in result),'passed',sum(x['run_exit']==0 for x in result))

