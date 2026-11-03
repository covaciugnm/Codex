from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((O/'Protocol_G3_nativ_v1.json').read_text(encoding='utf8'))
p['schema']='A05.G3.native.protocol.v2';p['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p['supersedes_without_overwrite']={'path':'Protocol_G3_nativ_v1.json','sha256':sha(O/'Protocol_G3_nativ_v1.json')}
p['G03_normal_path_binding']['argument_logging']='Fiecare apel consemnează separat productId și warehouseId, apoi argumentele în ordine: getQty(productId,warehouseId,ASI,isSOTrx,trx), getQtyAvailable(warehouseId,productId,ASI,trx), RezervareStoc.disponibil(clientId,productId,warehouseId,excludedOrderId,trx). Se evită coincidența ID-urilor produs/warehouse în fixture sau se adaugă explicit o pereche cu ID-uri diferite pentru a detecta inversarea.'
p['G05_persistence']['nuisance_terms']='La fiecare caz, originale surse.brut și SetLista.cerereComponenta arată comenzi=0 și cerereSet=0; SQL separat confirmă zero linii pentru produs/familie, rezervă=0 și reguli={} din original. Hook-urile rămân null înainte și după. Orice termen suplimentar nezero invalidează identificarea efectului PO.'
r=next(x for x in p['G06_cases'] if x['id']=='G3-R01')
r['zero_row_oracle']='Înainte de R01 se cere 0 rânduri PO pentru cheia nouă. În T1 add/getCreate are un ID/UUID și Qty5. Conexiunea separată vede 0 rânduri înainte de commit. După rollback, aceeași cheie are 0 rânduri, nu doar SUM(Qty)=0. SO2 și stoc10 persistă. Retry creează exact un rând PO cu Qty5; secvența ID consumată de tentativa rollback se documentează fără a cere reutilizarea ID.'
p['G01_identity_schema']['source_binary_difference']+=' Încercarea inițială de inventariere a oprit la clasa StorageValidatorProvider absentă; nicio clasă produs încărcată și niciun PG pornit. Inventarul continuat consemnează class_present=false, fără a masca eroarea.'
f=O/'Protocol_G3_nativ_v2.json';assert not f.exists();f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
m={'utc':p['utc'],'previous_manifest':{'path':'MANIFEST_protocol_G3_v1.json','sha256':sha(O/'MANIFEST_protocol_G3_v1.json')},'protocol':{'path':f.name,'sha256':sha(f)},'runtime_started':False}
f2=O/'SIGILIU_protocol_G3_v2.json';assert not f2.exists();f2.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'protocol_sha256':sha(f),'seal_sha256':sha(f2)}))
