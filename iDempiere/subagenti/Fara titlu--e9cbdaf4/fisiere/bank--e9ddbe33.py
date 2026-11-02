from pathlib import Path
import tempfile,subprocess,json,hashlib
O=Path(__file__).parent;E=O.parent;G=Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab');D=Path('D:/CodexWork/eva-audit-secondary-20261102');J=Path('C:/Program Files/Java/jdk-21/bin');T=Path(tempfile.mkdtemp(prefix='a11-r3-bank-'));runner=E/'R3_zone/A07/probe/A07R7Bank.java';out=[]
for tag,n in [('git','cod-master-contab.jar'),('instalat','com.eva.ro.contab_13.0.0.jar')]:
 cp=';'.join(map(str,[D/n,*D.glob('org.*.jar'),Path('D:/CodexWork/a05-support-jars/*'),G/'src']));z=subprocess.run([str(J/'javac.exe'),'-encoding','UTF-8','-proc:none','-sourcepath','','-cp',cp,'-d',str(T),str(G/'test/TestComparatieSaga.java'),str(runner)],capture_output=True,text=True);assert z.returncode==0,z.stderr
 z=subprocess.run([str(J/'java.exe'),'-Dstdout.encoding=UTF-8','-cp',str(T)+';'+cp,'com.eva.ro.contab.banca.A07R7Bank',str(G/'test/fixtures/banca')],capture_output=True,encoding='utf8',errors='replace',cwd=G);assert z.returncode==0,(z.stderr,z.stdout[-400:])
 rows=z.stdout.splitlines();marks=[x for x in rows if 'block 'in x and 'fail='in x];assert len(marks)==2 and all('fail=0'in x for x in marks)
 out.append(dict(build=tag,jar=hashlib.sha256((D/n).read_bytes()).hexdigest(),receipt=marks,matches=len([x for x in rows if 'OK' in x]),markers=rows))
(O/'bank_primary.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print([z['receipt'] for z in out])

