from pathlib import Path
import json, hashlib, subprocess, os, zipfile, datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A05_G3_nativ_lot04';O.mkdir(exist_ok=True)
G='D:/CodexWork/eva-audit-p01-src-20261101';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
sha=lambda b:hashlib.sha256(b).hexdigest()
oid=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
names=['corelare/RezervareStoc.java','corelare/FisaCanalProces.java','corelare/FisaCanalCalcul.java','corelare/RegulaStocCanal.java','corelare/SetLista.java','corelare/TabelaFisaCanal.java','corelare/DomeniiT22.java','corelare/FluxTabele.java','fiscal/TipGestiune.java','component/EvaWmsGardaEvents.java','component/EvaStocEvents.java','component/EvaAuditPostareEvents.java','EvaActivator.java']
ss=[]
jar=Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar')
jb=jar.read_bytes();assert oid(jb)=='4a5e399ebc671569098235c6ec6d151defd20be6'
with zipfile.ZipFile(jar) as z:
 for n in names:
  p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+n
  key=subprocess.check_output(['git','-C',G,'rev-parse',H+':'+p],env=E).decode().strip()
  b=subprocess.check_output(['git','-C',G,'cat-file','blob',key],env=E);assert oid(b)==key
  write(O/'surse_df85'/n,b)
  entry='com/eva/ro/contab/'+n[:-5]+'.class';cb=z.read(entry)
  ss.append(dict(path=p,oid=key,sha256=sha(b),class_entry=entry,class_sha256=sha(cb),owner='A05',peer=['A06','A11'],requirement='V03-N04 / D04; R12-STOC-SO-PO-01',task='SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING',state='LECTURA_PENTRU_PROTOCOL_FARA_EXECUTIE'))
core=Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar');nb=core.read_bytes()
assert sha(nb)=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'
nr=Path('D:/CodexWork/eva-audit-secondary-20261102/native/org.adempiere.base/src')
nn=['org/compiere/model/MStorageReservation','org/compiere/model/MStorageOnHand','org/compiere/model/MAttributeSet','org/compiere/model/MAttributeSetInstance','org/adempiere/base/StorageValidatorProvider','org/adempiere/base/IStorageValidator','org/adempiere/util/IReservationTracer']
ns=[]
with zipfile.ZipFile(core)as z:
 for n in nn:
  b=(nr/(n+'.java')).read_bytes();write(O/'native_source_cache'/(n+'.java'),b)
  cb=z.read(n+'.class') if n+'.class' in z.namelist() else None
  ns.append(dict(source_cache_path=str(nr/(n+'.java')),source_sha256=sha(b),class_entry=n+'.class',class_present=cb is not None,class_sha256=sha(cb) if cb is not None else None,provenance='Native source cache, not assumed identical to binary; actual binary javap required',owner='A05',peer=['A06','A11']))
for n in nn[:4]+nn[4:]:
 rr=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-p','-c','-classpath',str(core),n.replace('/','.')],capture_output=True,timeout=20)
 write(O/'native_bytecode'/(n.rsplit('/',1)[-1]+'.txt'),rr.stdout+rr.stderr)
for n in ['I_M_StorageReservation','I_M_AttributeSet','I_M_AttributeSetInstance','I_M_LocatorType']:
 rr=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-constants','-classpath',str(core),'org.compiere.model.'+n],capture_output=True,timeout=20);assert rr.returncode==0
 write(O/'native_bytecode'/(n+'.txt'),rr.stdout)
doc=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=H,product_executed=False,sources=ss,native=ns,eva_jar=dict(path=str(jar),oid=oid(jb),sha256=sha(jb)),native_core=dict(path=str(core),sha256=sha(nb)))
write(O/'Identitati_lectura_G3_v1.json',json.dumps(doc,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(sources=len(ss),native=len(ns),sha256=sha((O/'Identitati_lectura_G3_v1.json').read_bytes()),product_executed=False)))
