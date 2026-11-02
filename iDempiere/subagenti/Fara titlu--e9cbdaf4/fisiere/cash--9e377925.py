from pathlib import Path
import json,subprocess,hashlib,tempfile
O=Path(__file__).parent;E=O.parent;D=Path('D:/CodexWork/eva-audit-secondary-20261102');J=Path('C:/Program Files/Java/jdk-21/bin');tmp=Path(tempfile.mkdtemp(prefix='a11-a07cash-'));primary=E/'R3_zone/A07/probe/A07R3COD.java';out=[]
for mode,jar in [('git',D/'cod-master-contab.jar'),('instalat',D/'com.eva.ro.contab_13.0.0.jar')]:
 cp=';'.join(map(str,[jar,*D.glob('org.*.jar'),Path('D:/CodexWork/a05-support-jars/*')]));z=subprocess.run([str(J/'javac.exe'),'-encoding','UTF-8','-cp',cp,'-d',str(tmp),str(primary),str(O/'CashMatrix.java')],capture_output=True,text=True);assert z.returncode==0,z.stderr
 rows={}
 for n in ['A07R3COD','CashMatrix']:
  r=subprocess.run([str(J/'java.exe'),'-cp',str(tmp)+';'+cp,'com.eva.ro.contab.corelare.'+n],capture_output=True,text=True);assert r.returncode==0,r.stderr;rows[n]=r.stdout.splitlines()
 assert sum('MISMATCH' in l for l in rows['A07R3COD'])==1 and any('actual=ALLOW' in s for s in rows['A07R3COD'])
 assert len(rows['CashMatrix'])==6
 out.append(dict(build=mode,jar_hash=hashlib.sha256(jar.read_bytes()).hexdigest(),scenarios=rows,qualification='Comportamentul porții de decontare, cu valori deja potrivite ca total. Fără proces bancar/expediție/postare/furnizor real.'))
(O/'cash_primary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(out[0]['scenarios']['CashMatrix'])

