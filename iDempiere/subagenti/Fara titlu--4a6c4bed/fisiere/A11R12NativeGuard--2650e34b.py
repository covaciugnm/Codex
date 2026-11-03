from pathlib import Path
import json,hashlib,subprocess,tempfile,shutil,datetime,zipfile
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';O=B/'A11/Val02_loturi';N=B/'A05_Nativ_lot02'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=N/'harness/A05OsgiProbe.java';framework=Path('D:/CodexWork/a05-r12-native-cache/org.eclipse.osgi_3.18.500.v20230801-1826.jar')
assert h(src)=='2c1f961068091039c565e87f432180e3ca5711e16fb3bb9d3933014d6c8761f6' and h(framework)=='80b275d58379723b291ea650249cc3809c8f10b34f78aaf988132cd6d434ab4e'
lab=Path(tempfile.mkdtemp(prefix='a05-r12-native-lab-a11-guard-',dir='D:/CodexWork')).resolve()
try:
 shutil.copyfile(src,lab/'A05OsgiProbe.java')
 ccmd=['C:/Program Files/Java/jdk-21/bin/javac.exe','-cp',str(framework),'-d',str(lab),str(lab/'A05OsgiProbe.java')]
 c=subprocess.run(ccmd,cwd=lab,capture_output=True,text=True,encoding='utf8',timeout=30);assert c.returncode==0,c.stderr
 cmd=['C:/Program Files/Java/jdk-21/bin/java.exe','-Djava.security.manager=allow','-cp',str(lab)+';'+str(framework),'A05OsgiProbe',str(lab),'D:/CodexWork/a05-r12-native-cache','56455','canary']
 r=subprocess.run(cmd,cwd=lab,capture_output=True,text=True,encoding='utf8',timeout=30);assert r.returncode==0,r.stderr
 denied=[x.split('|')[1] for x in r.stdout.splitlines() if x.startswith('CANARY_DENIED|')];assert set(denied)=={'external_tcp','wrong_loopback_port','listen','udp','exec','outside_write','guard_remove'}
 assert 'CANARIES_ONLY|DONE' in r.stdout and 'CANARY_ALLOWED|scratch_write' in r.stdout and 'NATIVE_DB|' not in r.stdout
 assert not Path('D:/CodexWork/a05-canary-outside-denied.txt').exists()
 (lab/'stdout.txt').write_text(r.stdout,encoding='utf8');(lab/'stderr.txt').write_text(r.stderr,encoding='utf8')
 archive=O/'Control_garda_nativa_A11_v1.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
  for p in lab.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(lab).as_posix())
finally:
 assert lab.parent==Path('D:/CodexWork').resolve() and lab.name.startswith('a05-r12-native-lab-a11-guard-');shutil.rmtree(lab)
o={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Recompilare byte-exact a harnessului A05, execuție doar canari, fără framework.start/PO/PG și fără repetarea tranzacțiilor executorului.','compile':ccmd,'command':cmd,'source_sha256':h(src),'framework_sha256':h(framework),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'denied':denied,'allowed':'scriere în scratch','limit':'Gardă cooperativă Java21, nu sandbox OS; nu probă împotriva codului ostil. Reproducerea canarilor nu certifică WMS, login, autorizare sau buildul întreg.','archive':{'path':archive.relative_to(R).as_posix(),'sha256':h(archive)},'cleanup':{'own_scratch_absent':not lab.exists(),'own_processes':0,'A05_scratch_already_absent':not Path('D:/CodexWork/a05-r12-native-lab-20261103').exists(),'A05_PG_or_lab_changed_by_A11':False,'retained_masini_scratch_untouched':True},'runner_sha256':h(Path(__file__))}
p=O/'Control_garda_nativa_A11_v1.json';assert not p.exists();p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'path':str(p),'sha256':h(p),'denied':len(denied)}))
