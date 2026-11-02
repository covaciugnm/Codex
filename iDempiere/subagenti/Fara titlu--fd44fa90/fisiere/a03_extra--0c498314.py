from a03_exec_runner import *
import io, shutil
def pay():
  harness='''import java.util.*;import java.math.*;import java.time.*;import java.lang.reflect.*;import com.eva.ro.contab.fiscal.*;
  class A03Payroll { public static void main(String[] a)throws Exception{
  var reg=new ArrayList<>();var ctor=ParametriFiscali.Rand.class.getDeclaredConstructor(String.class,BigDecimal.class,LocalDate.class,LocalDate.class,String.class,String.class);ctor.setAccessible(true);
  String[][] params={{"SALARIU_MINIM","500"},{"CAS","0.10"},{"CASS","0.05"},{"CAM","0.02"},{"IMPOZIT_VENIT","0.10"}};
  for(var p:params)reg.add(ctor.newInstance(p[0],new BigDecimal(p[1]),LocalDate.of(2020,1,1),null,"SYNTHETIC control","nonlegal rates"));
  var cache=ParametriFiscali.class.getDeclaredField("cache");cache.setAccessible(true);cache.set(null,reg);
  var s=new MotorSalariiRO.Intrare();s.luna=LocalDate.of(2026,9,1);s.brut=new BigDecimal("1000");s.salBaza=s.brut;s.deducereInterzisa=true;var r=MotorSalariiRO.calculeaza(s);
  BigDecimal[] actual={r.cas,r.cass,r.cam,r.bazaImpozit,r.impozit,r.net};String[] exp={"100","50","20","850","85","765"};boolean ok=true;for(int i=0;i<exp.length;i++){boolean pass=actual[i].compareTo(new BigDecimal(exp[i]))==0;ok&=pass;System.out.println("component"+i+" expected="+exp[i]+" observed="+actual[i]+" "+pass);}if(!ok)System.exit(2);
  }}'''
  source=tmp/'A03Payroll.java';source.write_text(harness,encoding='utf8');(o/source.name).write_text(harness,encoding='utf8');results=[]
  for target,jar in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
    dst=tmp/target;cp=';'.join(str(x) for x in [dst,sec/jar,sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',lib/'*',plug/'src']);c=cmd([java/'javac.exe','-proc:none','-encoding','UTF-8','-cp',cp,'-sourcepath','','-d',dst,source],cwd=tmp,timeout=25)
    r=c if c.returncode else cmd([java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+(tmp/'no-net-2.policy').as_uri(),'-Dfile.encoding=UTF-8','-cp',cp,'A03Payroll'],cwd=tmp,timeout=22);out=r.stdout+r.stderr;log=o/(target+'_payroll.txt');log.write_text(out,encoding='utf8');results.append({'target':target,'jdk':str(java),'jar_sha256':dig(sec/jar),'timestamp':now(),'rc':r.returncode,'log':log.name,'content':out,'expectation':'Suma sintetică: brut1000, CAS100, CASS50, CAM20, bază impozit850, impozit85, net765. Rate de fixture arbitrare, nu cote legale.'})
  dump('payroll.json',results)
def duks():
  idx=urlopen('https://static.anaf.ro/static/10/Anaf/Informatii_R/saf_t.htm',timeout=14).read();from lxml import html as H;doc=H.fromstring(idx);zurl=U.urljoin('https://static.anaf.ro/static/10/Anaf/Informatii_R/saf_t.htm',next(a.get('href') for a in doc.xpath('//a[@href]') if a.text_content().strip().lower()=='validator'));res={'source':zurl,'utc':now(),'index':'https://static.anaf.ro/static/10/Anaf/Informatii_R/saf_t.htm','index_sha256':hashlib.sha256(idx).hexdigest()}
  try:
    raw=urlopen(Request(zurl,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();z=zipfile.ZipFile(io.BytesIO(raw));res.update(download_bytes=len(raw),zip_sha256=hashlib.sha256(raw).hexdigest(),files=z.namelist()[:35]);rdir=tmp/'duk';rdir.mkdir(exist_ok=True)
    for member in z.infolist():
      dest=(rdir/member.filename).resolve()
      if not dest.is_relative_to(rdir.resolve()):raise Exception('archive path unsafe')
      if member.is_dir():continue
      dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(member))
    jar=next((j for j in rdir.rglob('*.jar') if 'DUKIntegrator' in j.name and 'AnLunaUI' in j.name),next((j for j in rdir.rglob('*.jar') if 'DUKIntegrator' in j.name),None))
    if jar:
      src=plug/'test/fixtures/t16/D406_sintetic.xml';dst=rdir/'fixture_d406.xml';shutil.copyfile(src,dst)
      param=[java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+(tmp/'no-net-2.policy').as_uri(),'-Djava.awt.headless=true','-jar',jar.name,'-v','D406',dst,'$','$','an=2025','luna=8'];w=cmd(param,cwd=jar.parent,timeout=30);txt=w.stdout+w.stderr;(o/'D406_DUK.txt').write_text(txt,encoding='utf8');res.update(duk_sha256=dig(jar),rc=w.returncode,argv=[str(v) for v in param],output=txt[:2000],artifacts=[str(q.relative_to(rdir)) for q in rdir.rglob('fixture*')],limit='Răspuns CLI se interpretează împreună cu fișierul de erori. Nicio depunere.')
    else:res['limitation']='Arhiva Soft J are librăriile specifice formularului. DUKIntegrator nu a fost distribuit în această arhivă.'
  except Exception as e:res['diagnostic']=str(e)
  dump('d406_duk_fullkit.json',res)
if __name__=='__main__':
  import sys
  {'pay':pay,'duk':duks}[sys.argv[1]]()
