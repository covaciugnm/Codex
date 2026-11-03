import json, pathlib, hashlib, datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A11/Val04_preflight'
G=R/'executie/R12_fisiere/A05_G3_nativ_lot04'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
def out(name,d):
 p=O/name
 assert not p.exists()
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return p
when=datetime.datetime.now(datetime.timezone.utc).isoformat()
d={'utc':when,'author':'A11','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','scope':'Clarificare limitată de fixture F03 și disocierea controalelor F01; înaintea reluării acestor scenarii. Nu schimbă oracolul principal SO/PO ori contractul comercial.',
 'protocol':ref(G/'Protocol_G3_nativ_v2.json'),'gate':ref(O/'Verdict_A11_protocol_G3_nativ_v2.json'),
 'evidence_read':[ref(G/'business_g3_v2.A05G3Probe.java'),ref(G/'business_g3_v2.stdout.txt'),ref(G/'business_g3_v2.stderr.txt'),ref(G/'business_g3_v2.json'),ref(G/'Schema_G3_inainte_v1.json')],
 'decision':'ACCEPTAT CONDIȚIONAT, exclusiv parametrizarea fixturei native și controalele deja prevăzute; fără notă de produs.',
 'F03':{'observed':'Setterul IsActive asupra rândului persistent este refuzat de PO cu ColumnReadonly. Flagul rămâne Y; rezultatul 7 este compatibil cu această intrare. Nu este defect nou al produsului.',
 'allowed':'Familie separată: constructor original MStorageReservation, setter IsActive=false înainte de primul saveEx, apoi commit. Fără SQL de modificare, set_ValueNoCheck sau schimbarea AD.',
 'required':['Readback din conexiune separată înaintea citirii disponibilului: IsActive=N, cheia compusă și UUID, Qty, client, produs, depozit și IsSOTrx.','Dacă setterul sau saveEx refuză și la creare, se consemnează control indisponibil; nu se forțează.','Se păstrează distinct caracterizarea API native pentru rând N de accesibilitatea flagului prin operațiuni comerciale.','Refuzul setterului inițial rămâne probă de limită nativă; comparația inițială cu oracolul pentru N este exclusă.']},
 'F01':{'observed':'Fixturea other schimba simultan produsul și depozitul; sameP_otherW izolează numai depozitul.',
 'required':'Se adaugă rezervare pentru alt produs în același depozit al țintei, prin API original, cu ownership valid și readback. Disponibilul țintei trebuie să rămână neschimbat.',
 'fallback':'Dacă acest martor nu se execută, recepția nu va susține izolarea individuală a filtrului produsului.'},
 'counts':'Cazurile deja valide pot fi reutilizate. Eventualele reluări se numără separat ca observații repetate, nu cazuri unice noi.',
 'limits':['Zero DocAction, comandă, UI, RBAC comercial sau Fact_Acct validat prin această aprobare.','Controalele de existență AD/coloană din schema138 nu echivalează cu verificarea integrală a metadatelor de editabilitate.','17 contracte rămân deschise; raportul și logurile anterioare rămân imuabile.'],
 'execution_by_A11':0}
p=out('Addendum_A11_G3_F03_F01_v1.json',d)
s=out('SIGILIU_Addendum_A11_G3_F03_F01_v1.json',{'utc':when,'artifact':ref(p),'immutable':True})
print(json.dumps({'addendum':ref(p),'seal':ref(s)},ensure_ascii=False))
