from pathlib import Path
import hashlib,json,subprocess,datetime,socket
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A05_Comanda_rezervare_lot05';P=R/'executie/R12_fisiere/A05_G3_nativ_lot04';W=Path('D:/CodexWork/a05-order-harness')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not Path('D:/CodexWork/a05-r12-native-lab-order-20261103').exists()
with socket.socket() as s:assert s.connect_ex(('127.0.0.1',56455))!=0
assert not W.exists();W.mkdir()
old=json.loads((P/'Receptie_readiness_G3_v1.json').read_text(encoding='utf8')); entries=[]
for e in old['runtime']:
 p=Path(e['path']);got=sha(p);assert got==e['sha256'];entries.append(dict(path=str(p),sha256=got))
manifest=json.loads((P/'MANIFEST_A05_G3_nativ_lot04_v1.json').read_text(encoding='utf8'))
for n in ['a05_g3_restore.py','a05_g3_compile.py','a05_g3_run.py','A05G3Launcher.java']:
 p=P/'harness'/n
 matches=[e for e in manifest['files'] if e['path']=='harness/'+n];assert len(matches)==1 and sha(p)==matches[0]['sha256']
 s=p.read_text(encoding='utf8').replace('A05_G3_nativ_lot04','A05_Comanda_rezervare_lot05').replace('a05-r12-native-lab-g3-20261103','a05-r12-native-lab-order-20261103').replace('a05-g3-harness','a05-order-harness').replace('A05G3Launcher','A05OrderLauncher').replace('A05G3Probe','A05OrderProbe').replace('A05_G3_MODE','A05_ORDER_MODE').replace('a05.g3.native.probe','a05.order.native.probe').replace('a05-g3-probe.jar','a05-order-probe.jar')
 s=s.replace('A11/Val04_preflight/Verdict_A11_protocol_G3_nativ_v2.json','A11/Val05_preflight/Verdict_A11_protocol_Comanda_rezervare_v1.json').replace('abf849cb254c6c13d43ac318f4fe1f44d90dd61f0c1fffb328a3bad03f6ab80f','50e05e9e8fce3c4565c55ed0f964454f5d740ac147d7995f07284ef004374c9c')
 dest=W/'A05OrderLauncher.java' if n.endswith('.java') else Path('D:/CodexWork')/n.replace('a05_g3_','a05_order_')
 assert not dest.exists();dest.write_text(s,encoding='utf8')
r=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javac.exe','-cp','D:/CodexWork/a05-r12-native-cache/org.eclipse.osgi_3.18.500.v20230801-1826.jar',str(W/'A05OrderLauncher.java')],capture_output=True);assert r.returncode==0,r.stderr.decode()
(O/'Preflight_resurse_cache_v1.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lab_absent=True,port_free=True,runtime=entries,product_executed=False),indent=2),encoding='utf8')
print('Cache387 verificate; launcher compilat; nicio probă de produs; restaurarea este pregătită.')
