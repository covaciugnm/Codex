from pathlib import Path
import subprocess,zipfile,json,hashlib,sys
CACHE=Path('D:/CodexWork/a05-r12-native-cache');JDK=Path('C:/Program Files/Java/jdk-21/bin');OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
source=Path('D:/CodexWork/A05NativePoProbe.java');classes=CACHE/'probe_classes';classes.mkdir(exist_ok=True)
label=sys.argv[1]if len(sys.argv)>1 else'po_compile'
r=subprocess.run([str(JDK/'javac.exe'),'-cp',str(CACHE/'*'),'-d',str(classes),str(source)],capture_output=True,timeout=45)
assert not(OUT/(label+'.stdout.txt')).exists()
(OUT/(label+'.stdout.txt')).write_bytes(r.stdout);(OUT/(label+'.stderr.txt')).write_bytes(r.stderr)
assert r.returncode==0,r.stderr.decode()
manifest='Manifest-Version: 1.0\nBundle-ManifestVersion: 2\nBundle-SymbolicName: audit.a05.nativeprobe\nBundle-Version: 1.0.0\nBundle-Activator: A05NativePoProbe\nRequire-Bundle: org.adempiere.base\nImport-Package: org.osgi.framework\n\n'
target=CACHE/'a05-native-po-probe.jar'
with zipfile.ZipFile(target,'w')as z:
 z.writestr('META-INF/MANIFEST.MF',manifest)
 z.write(classes/'A05NativePoProbe.class','A05NativePoProbe.class')
(OUT/(label+'.A05NativePoProbe.java')).write_bytes(source.read_bytes())
(OUT/(label+'.jar')).write_bytes(target.read_bytes())
print({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'jar_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
