from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protocol':{'path':'Protocol_G3_nativ_v2.json','sha256':sha(O/'Protocol_G3_nativ_v2.json')},'reason':'MStorageReservation.add citește MProduct.get(ctx,id), fără trx; metadata necomisă poate deveni invizibilă acestui cache/cititor. Nu este constatare de defect, ci ordine corectă a fixturei.',
 'order':['1. Masterdata prin PO originale: produs, categorie/UM/taxă existente, warehouse/locator, sursă EVA, attribute set/ASI; commit explicit.',
          '2. Conexiune readonly separată: ownership și atribute reale, sursa originală recitită; pentru ASI IsLot=true și IsInstanceAttribute=true persistente, ambii ASI din același attribute set. ID produs și warehouse distincte în cel puțin o familie.',
          '3. Stoc inițial prin MStorageOnHand.add în tranzacție separată; commit și readback; baseline LocatorType eligibil.',
          '4. SO/PO prin MStorageReservation.add în tranzacții business ale probei; momentul commit/rollback și absența/prezența rândurilor consemnate.',
          '5. Oracol independent după commit și înainte/după rollback; evaluatorii EVA originali și native comparatori citiți pe cheile documentate.'],
 'runtime_started':False,'scope_change':False}
p=O/'Clarificare_ordine_fixture_G3_v1.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
print(sha(p))
