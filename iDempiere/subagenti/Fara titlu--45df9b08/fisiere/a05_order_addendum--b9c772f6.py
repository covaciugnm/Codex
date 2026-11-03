from pathlib import Path
import json, subprocess, os, hashlib, datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); O=R/'executie/R12_fisiere/A05_Comanda_rezervare_lot05'
H='df85d33c1648ce2b2df130a60a05ef696e2e5480'; G='D:/CodexWork/eva-audit-p01-src-20261101'; E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
sha=lambda b:hashlib.sha256(b).hexdigest()
ss=[]
for n in ['corelare/CanalB2B.java','fiscal/AlarmaLunaViitoare.java','fiscal/PoartaPerioada.java','component/EvaNoteInchidereEvents.java','component/EvaRepostareImportEvents.java']:
 p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+n; oid=subprocess.check_output(['git','-C',G,'rev-parse',H+':'+p],env=E).decode().strip(); b=subprocess.check_output(['git','-C',G,'cat-file','blob',oid],env=E)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
 d=O/'surse_df85'/n; assert not d.exists(); d.parent.mkdir(parents=True,exist_ok=True); d.write_bytes(b)
 ss.append(dict(path=p,oid=oid,sha256=sha(b),owner='A05',peer_planned=['A06','A11'],review_performed='Lectură A05 pentru protocol; A11 verifică independent; A06 nu a efectuat review',role='DEPENDENȚĂ/HANDLER: LECTURĂ DE APLICABILITATE, NEEXECUTAT',requirement='V04-N02 / readiness DocAction',actor='Actor viitor GardenAdmin client11/org11',normal_path='CanalB2B comandaB2B/linieB2B; EvaLunaViitoareEvents → PoartaPerioada/AlarmaLunaViitoare; ceilalți doi handleri sunt excluși motivat',native_method='PO/DocAction și Trx originale; încă neexecutate',positive='NEEXECUTAT',counterexample='NEEXECUTAT',persistent_effect='NEEXECUTAT',limit='Nicio probă business și niciun credit integral al sursei din această lectură.'))
data=dict(schema='A05.DocAction.site.protocol.addendum.v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=H,
 base=dict(path='Protocol_Comanda_rezervare_v1.json',sha256=sha((O/'Protocol_Comanda_rezervare_v1.json').read_bytes())),runtime_started=False,
 corrections=[
 'Coloana M_StorageReservationLog se numește DocumentNo; DocNo din protocol este numai abreviere narativă, nu identificator SQL. PK/UUID și toate coloanele sunt rezolvate din schema efectivă și confruntate cu modelul nativ înainte de oracol.',
 'Adaugă explicit în schema consumată de oracol M_Transaction și M_CostDetail, plus C_Invoice/C_InvoiceLine pentru absența efectelor; nu este suficient să apară numai în lista de readback.',
 'Auxiliare nominale suplimentare: EVA_AlarmaLunaViitoare, C_Calendar/C_Year/C_Period/C_PeriodControl pentru handlerul de dată; EVA_CanalVanzare/EVA_CanalGrupa/C_BP_Group/C_Campaign și C_BPartner.EVA_LimitaSold pentru handlerul B2B, inclusiv structura SQL_STRUCTURA originală. Inventarul de dependențe continuă înainte de readiness, fără ignorarea lipsurilor.',
 'CanalB2B.canalComenzii alege campania dacă există, altfel canalul grupei partenerului. Nu este suficient Campaign_ID=0. Fixturea BP trebuie să aibă grupă validă fără legătură B2B în EVA_CanalGrupa; se recitește rezultatul original canalPartener și relațiile SQL. Dacă nu există candidat seed, se creează MBPGroup sintetic prin PO, fără legături de canal, și se comite înainte de BP. Nu se dezactivează handlerul.',
 'AlarmaLunaViitoare.aziFirmei/idNou/utilizatorul/executia/tranzactia rămân implementările originale; nicio atribuire în test. Pentru fixturedate se consemnează valoarea reală; alarmele create legitim se măsoară pe documente și tranzacții, nu se impune zero dacă regula le cere.',
 'EvaNoteInchidereEvents privește GL_Journal și tabele de închidere, neatinse. EvaRepostareImportEvents privește DOC_BEFORE_POST, reactivări, procese contabile și setări/procesor; aceste operații nu sunt executate de A/B după neutralizarea seedului. Excluderi nominale, fără credit pentru aceste clase.',
 'C_OrderLineMA din lista orientativă v1 se verifică pentru existență/aplicabilitate; nu devine condiție artificială dacă modelul core13 nu o folosește. Coloanele/tabelele realmente consumate de MOrder/MOrderLine se fixează prin bytecode și schema exactă.',
 'A06 este peer planificat, nu reviewer efectiv. Nu se atribuie independență A06 pentru faptul că apare în lista peer a fișelor de plan.'
 ],sources=ss)
f=O/'Addendum_protocol_comanda_v1.json'; assert not f.exists(); f.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
files=[dict(path=f.relative_to(O).as_posix(),sha256=sha(f.read_bytes()))]+[dict(path='surse_df85/'+s['path'].split('/src/com/eva/ro/contab/')[1],sha256=s['sha256']) for s in ss]
m=O/'Sigiliu_addendum_protocol_v1.json'; assert not m.exists(); m.write_text(json.dumps(dict(base_manifest_sha256=sha((O/'MANIFEST_PLAN_Comanda_v1.json').read_bytes()),files=files),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(addendum_sha256=sha(f.read_bytes()),seal_sha256=sha(m.read_bytes()),sources_added=len(ss)),ensure_ascii=False))
