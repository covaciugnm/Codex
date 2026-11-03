from pathlib import Path
import subprocess,shlex,tarfile,io,zipfile,json,hashlib,shutil
CACHE=Path('D:/CodexWork/a05-n05-extra-cache');CACHE.mkdir(exist_ok=True)
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03')
name='org.adempiere.ui.zk_13.0.0.202603090043';target=CACHE/(name+'.jar');assert not target.exists()
cmd=['docker','exec','eva-idempiere-cesiro','tar','-C','/opt/idempiere/plugins/'+name,'-cf','-','.']
r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',shlex.join(cmd)],capture_output=True,timeout=60);assert r.returncode==0,r.stderr.decode()
rows=[]
with tarfile.open(fileobj=io.BytesIO(r.stdout))as t,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED)as z:
 for m in t:
  if not m.isfile():continue
  rel=m.name.removeprefix('./');assert not rel.startswith('/')and'..'not in Path(rel).parts
  b=t.extractfile(m).read();z.writestr(rel,b);rows.append({'path':rel,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
report={'origin':name,'method':'Read-only tar of native directory bundle; ZIP locally with original entry bytes. Only dependency resolution planned; UI not started.','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'files':rows}
(OUT/'Native_UI_bundle_readonly.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
eva=Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar');b=eva.read_bytes();assert hashlib.sha256(b).hexdigest()=='82099cd7f436a8fb4d532d8a46b83c62ae0e0176d86d9345c08598299d01d558';shutil.copyfile(eva,CACHE/eva.name)
print({'ui_entries':len(rows),'ui_bytes':target.stat().st_size,'product_started':False})
