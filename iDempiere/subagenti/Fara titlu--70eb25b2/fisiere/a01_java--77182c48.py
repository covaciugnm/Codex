import pathlib,subprocess,hashlib,json,datetime,tarfile,io,zipfile
out=pathlib.Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\A01');dst=pathlib.Path(r'D:\CodexWork\eva-a01-java');dst.mkdir(exist_ok=True);lib=dst/'lib';lib.mkdir(exist_ok=True); src=pathlib.Path(r'D:\CodexWork\eva-audit-p01-readonly-20261102\idempiere\plugins\com.eva.ro.contab'); sec=pathlib.Path(r'D:\CodexWork\eva-audit-secondary-20261102');jhome=pathlib.Path(r'C:\Program Files\Java\jdk-21\bin');
jars=['com.github.librepdf.openpdf_1.3.39.bcfips.jar','com.google.gson_2.9.0.jar','org.eclipse.osgi_3.18.500.v20230801-1826.jar','org.eclipse.equinox.common_3.18.100.v20230730-1117.jar','org.osgi.service.component_1.5.1.202212101352.jar','org.osgi.service.event_1.4.1.202109301733.jar','org.apache.commons.logging_1.2.0.jar'];extra=dst/'extra.txt'
if extra.exists():jars+=extra.read_text().splitlines()
hashes={};
for n in jars:
 assert n.endswith('.jar') and all(ch.isalnum() or ch in '._-' for ch in n);f=lib/n
 if not f.exists():
  r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',f'docker exec eva-idempiere-cesiro cat /opt/idempiere/plugins/{n}'],capture_output=True,timeout=40);assert r.returncode==0,r.stderr;assert r.stdout[:2]==b'PK';f.write_bytes(r.stdout)
 hashes[n]=hashlib.sha256(f.read_bytes()).hexdigest()
ui=lib/'installed-uizk-class-only.jar'
if not ui.exists():
 r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151','docker exec eva-idempiere-cesiro tar -C /opt/idempiere/plugins/org.adempiere.ui.zk_13.0.0.202603090043 -czf - org'],capture_output=True,timeout=32);assert r.returncode==0
 with tarfile.open(fileobj=io.BytesIO(r.stdout),mode='r:gz') as t,zipfile.ZipFile(ui,'w',compression=zipfile.ZIP_DEFLATED) as za:
  for e in t:
   if e.isfile() and e.name.endswith('.class') and e.name.startswith('org/'):za.writestr(e.name,t.extractfile(e).read())
hashes['runtime_ui_class_archive_local']=hashlib.sha256(ui.read_bytes()).hexdigest()
cp=';'.join(str(x) for x in [dst,sec/'com.eva.ro.contab_13.0.0.jar',sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',lib/'*']);names=['TestAutentificareMobil','TestT333Acces','TestApiMobil'];summary=[]
for name in names:
 c=subprocess.run([str(jhome/'javac.exe'),'-encoding','UTF-8','-proc:none','-cp',cp,'-d',str(dst),'test/'+name+'.java'],cwd=src,capture_output=True,text=True,encoding='utf-8',errors='replace');
 if c.returncode:r=c
 else:r=subprocess.run([str(jhome/'java.exe'),'-Dfile.encoding=UTF-8','-cp',cp,'com.eva.ro.contab.acces.'+name],cwd=src,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=30)
 txt=r.stdout+r.stderr;(out/(name+'.log')).write_text(txt,encoding='utf-8');summary.append({'class':name,'compiled':c.returncode==0,'returncode':r.returncode,'last':txt.strip().splitlines()[-4:],'errors':[x for x in txt.splitlines() if 'NoClassDefFoundError' in x or 'ClassNotFoundException' in x][:2],'log':name+'.log','scope':'Existing exact-SHA tests with synthetic doubles on CESIRO installed EVA classes, local JDK 21, no DB or server invocation.'})
res={'utc':datetime.datetime.now(datetime.UTC).isoformat(),'secondary_dependency_hashes':hashes,'tests':summary};(out/'java_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=True))
