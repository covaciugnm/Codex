from pathlib import Path
import json,subprocess,os,hashlib,zipfile,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Comanda_rezervare_lot05');O.mkdir(exist_ok=True)
G='D:/CodexWork/eva-audit-p01-src-20261101';H='df85d33c1648ce2b2df130a60a05ef696e2e5480';E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
sha=lambda b:hashlib.sha256(b).hexdigest()
names=['corelare/GeneratorDocumente.java','corelare/ValideazaComenzi.java','corelare/ValidareComanda.java','corelare/RezervareStoc.java','corelare/FisaCanalProces.java','corelare/FisaCanalCalcul.java','corelare/SetLista.java','corelare/Culegere.java','corelare/FluxTabele.java','corelare/DomeniiT22.java','culegere/ListaCulegere.java','form/PanouFluxComenzi.java','form/DialogConfirmComanda.java','form/JobFundal.java','form/ProceseEcran.java','component/EvaProcessFactory.java','component/EvaSetLinieEvents.java','component/EvaWmsGardaEvents.java','component/EvaAuditPostareEvents.java','component/EvaStocEvents.java','component/EvaValidareProdusEvents.java','component/EvaValidareWmsEvents.java','EvaActivator.java']
ss=[]
for n in names:
 p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+n;k=subprocess.check_output(['git','-C',G,'rev-parse',H+':'+p],env=E).decode().strip();b=subprocess.check_output(['git','-C',G,'cat-file','blob',k],env=E);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==k
 d=O/'surse_df85'/n;d.parent.mkdir(parents=True,exist_ok=True);assert not d.exists();d.write_bytes(b);ss.append(dict(path=p,oid=k,sha256=sha(b),owner='A05',peer=['A06','A11'],state='LECTURA_PENTRU_PROTOCOL',task='SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING'))
core=Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar');assert sha(core.read_bytes())=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'
with zipfile.ZipFile(core)as z:
 ns=[]
 for n in ['org.compiere.model.MOrder','org.compiere.model.MOrderLine','org.compiere.model.MStorageReservation','org.compiere.model.MStorageReservationLog','org.compiere.process.DocumentEngine','org.compiere.process.DocAction']:
  e=n.replace('.','/')+'.class';b=z.read(e);ns.append(dict(name=n,class_sha256=sha(b),core_sha256=sha(core.read_bytes())))
  rr=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-p','-c','-classpath',str(core),n],capture_output=True,timeout=20);assert rr.returncode==0
  d=O/'native_bytecode'/(n.rsplit('.',1)[-1]+'.txt');d.parent.mkdir(exist_ok=True);d.write_bytes(rr.stdout)
f=O/'Identitati_plan_comanda_v1.json';f.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=H,sources=ss,native=ns,runtime_started=False),ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(dict(sources=len(ss),native=len(ns),sha256=sha(f.read_bytes()))))
