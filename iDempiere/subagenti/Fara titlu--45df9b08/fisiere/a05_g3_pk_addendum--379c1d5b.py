from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((O/'Schema_G3_inainte_v1.json').read_text(encoding='utf8'))
x={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'type':'CORECTIE_ORACOL_HARNESS_FARA_SCHIMBARE_PRODUS','attempt':'business_g3_v1','attempt_sha256':sha(O/'business_g3_v1.json'),'error':'SQL readback al harnessului a presupus eronat M_StorageReservation_ID; această coloană nu există. Schema recepționată avea corect cheia compusă, fără această coloană.',
 'actual_identity': [x for x in s['rows']['constraints'] if x['relname']=='m_storagereservation' and x['contype'] in ('p','u')],
 'oracle_correction':'Rândurile sunt identificate prin (M_Product_ID,M_Warehouse_ID,IsSOTrx,M_AttributeSetInstance_ID) și UUID; getCreate/saveEx native rămân nemodificate. Readback JSON și bariera rollback folosesc UUID, nu ID numeric inventat.',
 'impact':'Încercarea v1 s-a oprit după masterdata+stoc fixture și înaintea oricărui MStorageReservation.add; zero cazuri G3 executate/creditate. Fixturea rămâne identificată separat, nu se șterge și nu intră în fixturele noi, cu surse/gestiuni/produs noi.',
 'retained':['business_g3_v1.A05G3Probe.java','business_g3_v1.stdout.txt','business_g3_v1.stderr.txt','business_g3_v1.readback_01_masterdata_committed.json'],
 'next':'Readiness/binding revalidate în noua JVM; runner ignoră tokenul checkpoint anterior. Nicio modificare schemă/aplicație/servicii, niciun drept suplimentar.',
 'protocol_clarification':'Câmpul generic ID/UUID din G05 înseamnă cheia naturală compusă și UUID pentru această tabelă; la rollback dispariția rândului se verifică prin cheia compusă și UUID anterior, nu prin sumă.'}
f=O/'Corectie_oracol_cheie_nativa_G3_v1.json';assert not f.exists();f.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8');print(sha(f))
