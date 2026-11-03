from pathlib import Path
import subprocess,json,hashlib,datetime,sys
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03');W=Path('D:/CodexWork/a05-n05-harness')
C=Path('D:/CodexWork/a05-r12-native-cache');F=C/'org.eclipse.osgi_3.18.500.v20230801-1826.jar';L=Path('D:/CodexWork/a05-r12-native-lab-n05-20261103')
label=sys.argv[1];mode=sys.argv[2];assert not(O/(label+'.json')).exists()
args=['C:/Program Files/Java/jdk-21/bin/java.exe','-Djava.security.manager=allow','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-cp',str(W)+';'+str(F),'A05N05Launcher',str(L),str(C)+';D:/CodexWork/a05-n05-extra-cache','56455',mode,str(W/'a05-n05-probe.jar')]
for p in W.glob('*.java'):(O/(label+'.'+p.name)).write_bytes(p.read_bytes())
with(O/(label+'.stdout.txt')).open('wb')as a,(O/(label+'.stderr.txt')).open('wb')as b:
 try:r=subprocess.run(args,stdout=a,stderr=b,timeout=240);rc=r.returncode
 except subprocess.TimeoutExpired:rc='TIMEOUT240'
(O/(label+'.json')).write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'args':args,'exit':rc,'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in W.glob('*.java')},'probe_jar_sha256':hashlib.sha256((W/'a05-n05-probe.jar').read_bytes()).hexdigest()if(W/'a05-n05-probe.jar').exists()else None},indent=2),encoding='utf8')
print('exit',rc);print((O/(label+'.stdout.txt')).read_text(errors='replace')[-6500:]);print((O/(label+'.stderr.txt')).read_text(errors='replace')[-1800:])
