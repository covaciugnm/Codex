from pathlib import Path
import subprocess,os,json,hashlib,datetime,shlex,tarfile,io,zipfile
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');OUT=R/'executie/R12_fisiere/A05_N05_lot03';OUT.mkdir(exist_ok=True)
HEAD='df85d33c1648ce2b2df130a60a05ef696e2e5480';GIT=Path('D:/CodexWork/eva-audit-p01-src-20261101')
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
sha=lambda b:hashlib.sha256(b).hexdigest();oid=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
sources=[]
names=['EvaActivator.java','component/EvaProcessFactory.java','component/EvaNotaSetBomEvents.java','component/EvaWmsGardaEvents.java','component/EvaSetLinieEvents.java','component/EvaValidareWmsEvents.java','component/EvaValidareProdusEvents.java','corelare/NotaSetWmsProces.java','corelare/SetLista.java','wms/ListaMaterialeWms.java','wms/StocWms.java','wms/NotaSetWms.java','wms/ModelWms.java','wms/PerecheWms.java','wms/MiscareWms.java','wms/TipMiscareWms.java','wms/AlegerePozitii.java','form/DialogNotaSetWms.java','setup/EvaMetadata.java','fiscal/SetariFirma.java','fiscal/SetariFirmaPerioadaCatalog.java']
for name in names:
 path='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+name
 rr=subprocess.run(['git','-C',str(GIT),'rev-parse',HEAD+':'+path],capture_output=True,env=env,timeout=20);assert rr.returncode==0;key=rr.stdout.decode().strip()
 rr=subprocess.run(['git','-C',str(GIT),'cat-file','blob',key],capture_output=True,env=env,timeout=20);assert rr.returncode==0;data=rr.stdout;assert oid(data)==key
 dest=OUT/'surse_df85'/name;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();dest.write_bytes(data)
 sources.append({'path':path,'oid':key,'sha256':sha(data),'owner':'A05','peer':['A03','A11'],'requirement':'P01.C03.T0029 / N05 / V02-N01,N02','state':'LECTURĂ/PROTOCOL; NICIO EXECUȚIE DE PRODUS','role':'componentă a traseului BOM/WMS sau gardă relevantă','normal_path':'DialogNotaSetWms → AD_Process → MProcess.processIt → EvaProcessFactory → NotaSetWmsProces → StocWms; PO.saveEx → EventManager → EvaNotaSetBomEvents','positive':'propus în protocol; neexecutat','counterexample':'propus în protocol; neexecutat','persistent_effect':'niciunul; citire/copie de surse','limit':'Nu presupune că source și bytecode Git sunt identice fără binding.'})
native_jar=Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar');data=native_jar.read_bytes();assert oid(data)=='4a5e399ebc671569098235c6ec6d151defd20be6'
classes=[]
with zipfile.ZipFile(native_jar)as z:
 for name in names:
  c='com/eva/ro/contab/'+name[:-5]+'.class';b=z.read(c);classes.append({'entry':c,'sha256':sha(b),'bytes':len(b)})
 (OUT/'Manifest_bundle_EVA_df85.txt').write_bytes(z.read('META-INF/MANIFEST.MF'))
(OUT/'Identitati_sursee_bundle_v1.json').write_text(json.dumps({'head':HEAD,'source_files':sources,'jar':{'path':str(native_jar),'oid':oid(data),'sha256':sha(data),'bytes':len(data)},'classes':classes},ensure_ascii=False,indent=2),encoding='utf8')
seed=Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump');assert sha(seed.read_bytes())=='54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4'
pg='D:/CodexWork/p01-local-pg16/pgsql/bin/pg_restore.exe'
for label,args in [('seed_schema',['--schema-only']),('seed_build_migrations',['--data-only','-t','ad_system','-t','ad_migrationscript','-t','ad_modelvalidator'])]:
 result=subprocess.run([pg,*args,'--file=-',str(seed)],capture_output=True,timeout=30);assert result.returncode==0,result.stderr.decode();(OUT/(label+'.sql')).write_bytes(result.stdout)
ssh=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151']
cmd=['docker','exec','eva-idempiere-cesiro','tar','-C','/opt/idempiere/migration','-cf','-','iD13/postgresql','processes_post_migration/postgresql']
result=subprocess.run(ssh+[shlex.join(cmd)],capture_output=True,timeout=45);assert result.returncode==0,result.stderr.decode()
migrations=[]
with tarfile.open(fileobj=io.BytesIO(result.stdout))as t:
 for m in t:
  if not m.isfile():continue
  assert not Path(m.name).is_absolute() and '..'not in Path(m.name).parts
  b=t.extractfile(m).read();target=OUT/'native_migration_readonly'/m.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b);migrations.append({'path':m.name,'sha256':sha(b),'md5':hashlib.md5(b).hexdigest(),'bytes':len(b)})
(OUT/'Native_migration_inventory.json').write_text(json.dumps({'origin':'installed native image /opt/idempiere/migration, read-only tar stdout; never executed','image':'sha256:72eb56ecdd7953c05efebe2f7641c8a98eced0fbcf8eef0d673fb6152f432235','files':migrations},ensure_ascii=False,indent=2),encoding='utf8')
print({'sources':len(sources),'native_sql':len(migrations),'seed_schema_bytes':(OUT/'seed_schema.sql').stat().st_size,'product_started':False})
