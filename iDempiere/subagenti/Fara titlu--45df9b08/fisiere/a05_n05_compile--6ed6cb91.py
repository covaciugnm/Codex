from pathlib import Path
import subprocess,zipfile,hashlib
W=Path('D:/CodexWork/a05-n05-harness');C=Path('D:/CodexWork/a05-r12-native-cache');E=Path('D:/CodexWork/a05-n05-extra-cache');classes=W/'classes';classes.mkdir(exist_ok=True)
r=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javac.exe','-cp',str(C/'*')+';'+str(E/'*'),'-d',str(classes),str(W/'A05N05Probe.java')],capture_output=True,timeout=60)
print(r.stderr.decode(errors='replace'));assert r.returncode==0
m='Manifest-Version: 1.0\r\nBundle-ManifestVersion: 2\r\nBundle-SymbolicName: a05.n05.native.probe\r\nBundle-Version: 1.0.0\r\nBundle-Activator: A05N05Probe\r\nRequire-Bundle: org.adempiere.base,com.eva.ro.contab\r\nImport-Package: org.osgi.framework,org.osgi.service.event\r\n\r\n'
with zipfile.ZipFile(W/'a05-n05-probe.jar','w',zipfile.ZIP_DEFLATED)as z:
 z.writestr('META-INF/MANIFEST.MF',m)
 for p in classes.rglob('*.class'):z.write(p,p.relative_to(classes).as_posix())
print('compiled',hashlib.sha256((W/'a05-n05-probe.jar').read_bytes()).hexdigest())
