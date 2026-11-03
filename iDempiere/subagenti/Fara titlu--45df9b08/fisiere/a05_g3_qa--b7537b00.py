from pathlib import Path
import json,hashlib,datetime,re
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'MANIFEST_A05_G3_nativ_lot04_v1.json').read_text(encoding='utf8'))
for x in m['files']:assert sha(O/x['path'])==x['sha256'],x['path']
rows=json.loads((O/'Fise_G3_final_v1.json').read_text(encoding='utf8'))
required=['path','oid','owner','peer','role','actor','normal_path','requirement','task','positive','counterexample','persistent_effect','result','limit','event_id','coverage_class']
assert len(rows)==13 and all(all(k in x and x[k] for k in required)for x in rows)
log='\n'.join((O/f'business_g3_v{i}.stdout.txt').read_text(encoding='utf8')for i in [2,3])
case_lines=[l for l in log.splitlines() if l.startswith('CASE_G3|')];assert len(case_lines)==16
report=json.loads((O/'Raport_A05_G3_nativ_lot04_v1.json').read_text(encoding='utf8'));assert len(report['cases'])==10
allread=list(O.glob('business_g3_v*.readback_*.json'));assert len(allread)==42
v23=[p for p in allread if '.readback_'in p.name and (p.name.startswith('business_g3_v2')or p.name.startswith('business_g3_v3'))];assert len(v23)==41
cleanup=json.loads((O/'Cleanup_final_v1.json').read_text(encoding='utf-8-sig'));assert cleanup['pgStopped'] and cleanup['listenersAfter']==0 and not cleanup['targetExistsAfter'] and cleanup['ownJvmProcesses']==0
x={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest':{'path':'MANIFEST_A05_G3_nativ_lot04_v1.json','sha256':sha(O/'MANIFEST_A05_G3_nativ_lot04_v1.json')},'files_rehashed':len(m['files']),'bad_hashes':0,'fiches_checked':13,'required_fields':required,'method_source_paths':6,'handler_fixture_binding_paths':3,'constant_paths':2,'static_paths':2,'protocol_scenarios':10,'completed_CASE_G3_lines':16,'CASE_G3_lines':case_lines,'readback_total':42,'readback_v2_v3':41,'readback_setup_v1':1,'counting_rule':'Scenarii, subcazuri, capturi și surse sunt numărători diferite; nu se adună și nu implică recepție globală.','cleanup_verified_from_evidence':True,'product_conformity':False,'known_open_limit':'M_StorageReservationLog: delta nepregătită/necitată; niciun credit pentru absența efectelor persistente acolo. Nu reluăm alte probe în acest checkpoint.','independent_final_receipt':'A11 separat; această verificare este autocontrol, nu recepție independentă.'}
f=O/'QA_autoverificare_G3_v1.json';assert not f.exists();f.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
y={'utc':x['utc'],'main_manifest':x['manifest'],'qa':{'path':f.name,'sha256':sha(f)},'sealed_files_unchanged':True}
s=O/'SIGILIU_supliment_QA_G3_v1.json';assert not s.exists();s.write_text(json.dumps(y,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'qa_sha256':sha(f),'supplement_seal_sha256':sha(s),'files_verified':len(m['files'])}))

