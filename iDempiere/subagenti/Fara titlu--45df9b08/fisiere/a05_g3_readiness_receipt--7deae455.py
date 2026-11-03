from pathlib import Path
import json,hashlib,re,zipfile,datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A05_G3_nativ_lot04'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((R/'executie/R12_fisiere/A05_N05_lot03/Runtime_instalat_N05_v1.json').read_text(encoding='utf8'))
checks=[]
for e in manifest['entries']:
 p=Path(e['path']);got=sha(p);assert got==e['sha256'],str(p);checks.append(dict(path=str(p),sha256=got,verified=True))
log=(O/'readiness_g3_v1.stdout.txt').read_text(encoding='utf8');assert 'READINESS_G3|PASS' in log and 'BOUNDARY_DENIALS|7' in log and 'HARNESS_CONTROLLED_EXIT|0' in log
assert log.count('CANARY_DENIED|')==7 and log.count('HOOK_NULL|')==3
for n in ['com.eva.ro.contab','org.adempiere.ui.zk','org.adempiere.server']:assert f'DORMANCY_BEFORE_PROBE|{n}|state=4|startlevel=50' in log
bindings=[]
eva=Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar');core=Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar')
for m in re.finditer(r'^CLASS_BINDING\|([^|]+)\|bundle=([^|]+)\|sha256=([^|]+)\|codeSource=(.*)$',log,re.M):
 name,bundle,digest,source=m.groups();j=eva if name.startswith('com.eva.') else core
 with zipfile.ZipFile(j)as z:actual=hashlib.sha256(z.read(name.replace('.','/')+'.class')).hexdigest()
 assert actual==digest;bindings.append(dict(name=name,bundle=bundle,sha256=digest,source=source,original_match=True))
schema=json.loads((O/'Schema_G3_inainte_v1.json').read_text(encoding='utf8'));assert not schema['failed']
x=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ready_for_scoped_fixture=True,product_cases_executed=0,cache_entries_rehashed=len(checks),runtime=checks,bindings=bindings,schema_sha256=sha(O/'Schema_G3_inainte_v1.json'),readiness_sha256=sha(O/'readiness_g3_v1.json'),canaries=7,hooks_null=3,limit='Business JVM must repeat binding/readiness; auxiliary zero terms are asserted on each new native fixture. No DocAction/order/UI. LastBuildInfo placeholder unchanged.')
f=O/'Receptie_readiness_G3_v1.json';assert not f.exists();f.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(dict(file=f.name,sha256=sha(f),cache_entries=len(checks),bindings=len(bindings))))
