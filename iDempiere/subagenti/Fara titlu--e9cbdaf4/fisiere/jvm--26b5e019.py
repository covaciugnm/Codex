from pathlib import Path
import subprocess,tempfile,hashlib,json
O=Path(__file__).parent
dep=Path('D:/CodexWork/eva-audit-secondary-20261102')
j=Path('C:/Program Files/Java/jdk-21/bin')
tmp=Path(tempfile.mkdtemp(prefix='a11-r6-'))
out=[]
for label,jar in [('git',dep/'cod-master-contab.jar'),('instalat',dep/'com.eva.ro.contab_13.0.0.jar')]:
 cp=';'.join(map(str,[jar,*dep.glob('org.*.jar'),Path('D:/CodexWork/a05-support-jars/*')]))
 sub=subprocess.run([str(j/'javac.exe'),'-encoding','UTF-8','-cp',cp,'-d',str(tmp),str(O/'A11Job.java')],capture_output=True,text=True);assert sub.returncode==0,sub.stderr
 cmd=[str(j/'java.exe'),'-cp',str(tmp)+';'+cp,'com.eva.ro.contab.form.A11Job']
 ps=[]; lines=[]; rows=[]
 try:
  for i in range(2):
   p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True);ps.append(p);line=p.stdout.readline().strip();assert line=='ACQUIRE=true SAME_OWNER_REENTRY=false',line;lines.append(line)
  for p in ps:
   stdout,_=p.communicate('\n',timeout=20);assert p.returncode==0 and 'AFTER_RELEASE=true' in stdout;rows.append(stdout.strip())
 finally:
  for p in ps:
   if p.poll() is None:p.kill();p.wait()
 columns=subprocess.run(cmd+['column'],capture_output=True,text=True);assert columns.returncode==0,(columns.stdout,columns.stderr);assert len(columns.stdout.splitlines())==8
 out.append(dict(build=label,jar=str(jar),sha256=hashlib.sha256(jar.read_bytes()).hexdigest(),simultaneous_processes_with_same_key=lines,read_after_release=rows,independent_C4_cases=columns.stdout.splitlines(),scope='Aceeași cheie ținută simultan în două JVM de laborator, distinct de două fire locale. Nu este reprodusă contabilizarea dublă sau existența a două noduri în cabinet.'))
(O/'independent_jvm.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(out)

