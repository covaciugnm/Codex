from pathlib import Path
import subprocess,json,hashlib,time,os,re
w=Path('D:/CodexWork/a06-oracles');r=Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab');s=Path('D:/CodexWork/eva-audit-secondary-20261102');jdk=Path('C:/Program Files/Java/jdk-21/bin')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
res=[]
for k,j in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
 cls=w/('classes-'+k);cls.mkdir(exist_ok=True)
 cp=';'.join(str(x) for x in [cls,s/j,s/'org.adempiere.base_13.0.0.202603090043.jar',s/'org.adempiere.base.process_13.0.0.202603090043.jar','D:/CodexWork/a05-support-jars/*','D:/CodexWork/eva-a01-java/lib/*'])
 for suite,f in [('OracleProbe',w/'OracleProbe.java'),('TestT22Pagina',r/'test/TestT22Pagina.java')]:
  c=subprocess.run([jdk/'javac.exe','-encoding','UTF-8','-cp',cp,'-d',cls,f,*([r/'test/TestT22Flux.java'] if suite=='TestT22Pagina' else [])],cwd=r,capture_output=True,timeout=12);result={'jar':k,'jar_sha256':h(s/j),'suite':suite,'source_sha256':h(f),'compile_return':c.returncode}
  if c.returncode==0:
   y=subprocess.run([jdk/'java.exe','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Duser.timezone=UTC','-Djava.net.useSystemProxies=false','-cp',cp,('com.eva.ro.contab.corelare.' if suite=='OracleProbe' else '')+suite],cwd=r,capture_output=True,timeout=18);txt=y.stdout.decode('utf8','replace');result.update(run_return=y.returncode,stderr=y.stderr.decode('utf8','replace')[:400],stdout_sha256=hashlib.sha256(y.stdout).hexdigest(),ok_lines=sum(bool(re.match(r'^\s*OK\s',z)) for z in txt.splitlines()),fail_lines=[z for z in txt.splitlines() if re.match(r'^\s*FAIL\s',z)],observations=([z.split('\t') for z in txt.splitlines()] if suite=='OracleProbe' else [z.strip() for z in txt.splitlines() if re.search(r'target|<a>|Record_UU|cronologia c11|href=|fereast',z,re.I)]))
  else:result['compiler_message']=c.stderr.decode('utf8','replace')[:650]
  res.append(result)
  print(k,suite,result.get('run_return'),result.get('ok_lines'),result.get('fail_lines'),result.get('compiler_message'),result.get('stderr','')[:70])
(w/'actual.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8')

