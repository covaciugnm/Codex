from pathlib import Path
import subprocess,json,hashlib,sys,datetime
CACHE=Path('D:/CodexWork/a05-r12-native-cache')
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
JDK=Path('C:/Program Files/Java/jdk-21/bin')
SRC=Path('D:/CodexWork/A05OsgiProbe.java')
fw=CACHE/'org.eclipse.osgi_3.18.500.v20230801-1826.jar'
source_bytes=SRC.read_bytes();source_sha=hashlib.sha256(source_bytes).hexdigest()
r=subprocess.run([str(JDK/'javac.exe'),'-cp',str(fw),'-d',str(CACHE),str(SRC)],capture_output=True,timeout=30)
assert r.returncode==0,r.stderr.decode()
label=sys.argv[1];assert not (OUT/(label+'.json')).exists()
(OUT/(label+'.A05OsgiProbe.java')).write_bytes(source_bytes)
args=[str(JDK/'java.exe'),'-Djava.security.manager=allow','-cp',str(CACHE)+';'+str(fw),'A05OsgiProbe','D:/CodexWork/a05-r12-native-lab-20261103',str(CACHE),'56455',sys.argv[2]if len(sys.argv)>2 else'resolve',str(CACHE/'a05-native-po-probe.jar')]
with (OUT/(label+'.stdout.txt')).open('wb')as stdout,(OUT/(label+'.stderr.txt')).open('wb')as stderr:
 try:r=subprocess.run(args,stdout=stdout,stderr=stderr,timeout=150);rc=r.returncode
 except subprocess.TimeoutExpired:rc='TIMEOUT_150_SECONDS'
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'args':args,'exit':rc,'source_sha256':source_sha,'probe_jar_sha256':hashlib.sha256((CACHE/'a05-native-po-probe.jar').read_bytes()).hexdigest() if(CACHE/'a05-native-po-probe.jar').exists()else None,'scope':'Native framework and provider bootstrap; no product task receives acceptance without explicit PO witness.'}
(OUT/(label+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
print((OUT/(label+'.stdout.txt')).read_text(errors='replace')[-6000:])
print((OUT/(label+'.stderr.txt')).read_text(errors='replace')[-1600:])
