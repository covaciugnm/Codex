from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A08_Storefront_catalog_lot04');R=O.parents[2]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((O/'Raport_A08_catalog_lot04_v1.json').read_text(encoding='utf-8'))
run=O/'Run_2026-11-03T02-00-34Z';raw=json.loads((run/'Rezultate.json').read_text(encoding='utf-8'))
refs=[{'case_id':c['id'],'evidence':{'path':(run/c['id']/'Evidence.json').relative_to(R).as_posix(),'sha256':sha(run/c['id']/'Evidence.json')},'screenshots':[{'path':(O/p).relative_to(R).as_posix(),'sha256':sha(O/p)} for p in c['screenshots']]} for c in raw['cases']]
r['corrects_metadata_of']={'path':(O/'Raport_A08_catalog_lot04_v1.json').relative_to(R).as_posix(),'sha256':sha(O/'Raport_A08_catalog_lot04_v1.json')}
r['metadata_correction_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
r['corrections']=['peer_catalog provine din planned_peer=A06 pentru toate7 căile. Nu este dovadă că A06 a efectuat peer review.','Ancore per caz și captură cu SHA-256, suplimentar manifestului de lot.','Fereastra de linii pentru applySearchQuery precizată215–222.','HTMLv2 adaugă overflow-wrap:anywhere pe corp pentru citirea mobilă; fără modificare de produs sau concluzii.']
for f in r['file_sheets']:
 f['peer_catalog']=f['catalog_identity']['planned_peer'];assert f['peer_catalog']=='A06'
 f['test_evidence_sha256']=sha(run/'Rezultate.json') if f['role']=='original_component_to_execute' else None
 f['per_case_evidence']=refs if f['role']=='original_component_to_execute' else []
r['findings'][2]['source_lines']=[215,222,265,283,287,296]
for name,data in [('Raport_A08_catalog_lot04_v2.json',r),('Fise_7_cai_A08_v2.json',r['file_sheets'])]:
 p=O/name;assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
h=(O/'Raport_A08_catalog_lot04_v1.html').read_text(encoding='utf-8').replace('body{font:','body{overflow-wrap:anywhere;font:').replace('Raport_A08_catalog_lot04_v1.json','Raport_A08_catalog_lot04_v2.json').replace('Fise_7_cai_A08_v1.json','Fise_7_cai_A08_v2.json')
h=h.replace('<h2>Limite și resurse</h2>','<p>Fișele v2 consemnează explicit peerul planificat A06, fără să atribuie o verificare A06 efectuată. Ancorele fiecărui caz și ale capturilor au hash SHA-256. Versiunea1 rămâne păstrată.</p><h2>Limite și resurse</h2>')
p=O/'Raport_A08_catalog_lot04_v2.html';assert not p.exists();p.write_text(h,encoding='utf-8')
q=Path('D:/CodexWork/a08-catalog-presentation-qa.py').read_text(encoding='utf-8').replace('Raport_A08_catalog_lot04_v1.html','Raport_A08_catalog_lot04_v2.html').replace('QA_presentation_v1','QA_presentation_v2')
Path('D:/CodexWork/a08-catalog-presentation-qa-v2.py').write_text(q,encoding='utf-8')
manifest={'utc':r['metadata_correction_utc'],'no_new_product_executions':True,'original_manifest_sha256':sha(O/'MANIFEST_A08_catalog_lot04_v1.json'),'corrections':r['corrections'],'files':[{'path':p.name,'sha256':sha(p)} for p in [O/'Raport_A08_catalog_lot04_v2.json',O/'Fise_7_cai_A08_v2.json',O/'Raport_A08_catalog_lot04_v2.html']]}
p=O/'MANIFEST_corectii_A08_v2.json';assert not p.exists();p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'manifest_sha256':sha(p),'files':manifest['files']},ensure_ascii=False))
