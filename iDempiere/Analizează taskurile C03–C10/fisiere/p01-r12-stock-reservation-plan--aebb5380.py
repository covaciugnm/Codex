from pathlib import Path
import json,gzip,hashlib,subprocess,zipfile,re,datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A06_Rezervari_nativ_lot04'
assert not O.exists(), 'new additive lot only'
O.mkdir()
E=Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
names=['RezervareStoc.java','FisaCanalProces.java','FisaCanalCalcul.java','RegulaStocCanal.java']
prefix='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/corelare/'
paths={prefix+n for n in names}
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8');return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':sha(p.read_bytes())}
cat={}
with gzip.open(R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf-8-sig') as f:
 for l in f:
  r=json.loads(l)
  if r.get('path') in paths:cat[r['path']]=r
assert len(cat)==4,cat
sources=[]
for p in sorted(paths):
 b=(E/p).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 row=cat[p]
 assert oid == row.get('git_object'),row
 (O/'sources').mkdir(exist_ok=True);(O/'sources'/Path(p).name).write_bytes(b)
 sources.append({'path':p,'oid':oid,'sha256':sha(b),'bytes':len(b),'catalog_row':row,'source_copy':str((O/'sources'/Path(p).name).relative_to(R)).replace('\\','/')})
j=Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar')
c='org/compiere/model/MStorageReservation.class'
with zipfile.ZipFile(j) as z:
 b=z.read(c);(O/'native_class.class').write_bytes(b)
 native={'jar_path':str(j),'jar_sha256':sha(j.read_bytes()),'class_entry':c,'class_sha256':sha(b),'native_version':'13.0.0.202603090043','binding':'offline binary inspection only; no runtime/operational equivalence claim'}
r=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-classpath',str(j),'-c','-p','org.compiere.model.MStorageReservation'],capture_output=True,timeout=30)
assert r.returncode==0
(O/'MStorageReservation.javap.txt').write_bytes(r.stdout)
t=r.stdout.decode('utf-8',errors='replace')
a=t.index('  public static java.math.BigDecimal getQty(');b=t.index('  public static boolean add(',a)
(O/'Native_getQty_and_available.txt').write_text(t[a:b],encoding='utf-8')
native['javap_sha256']=sha(r.stdout)
meta=save('Sources.json',sources)
nm=save('Native_binding.json',native)
cases=[
 ('R00','no reservations',[],0),
 ('R01','SO sales only',[(1,2,3,'Y','Y',2)],2),
 ('R02','same SO plus incoming purchase',[(1,2,3,'Y','Y',2),(1,2,3,'N','Y',5)],2),
 ('R03','same SO plus larger incoming purchase',[(1,2,3,'Y','Y',2),(1,2,3,'N','Y',15)],2),
 ('R04','incoming purchase only',[(1,2,3,'N','Y',5)],0),
 ('R05','other client excluded',[(1,2,3,'Y','Y',2),(9,2,3,'Y','Y',5)],2),
 ('R06','other product excluded',[(1,2,3,'Y','Y',2),(1,9,3,'Y','Y',5)],2),
 ('R07','other warehouse excluded',[(1,2,3,'Y','Y',2),(1,2,9,'Y','Y',5)],2),
 ('R08','inactive excluded by EVA contract',[(1,2,3,'Y','Y',2),(1,2,3,'Y','N',5)],2),
 ('R09','two active SO rows summed',[(1,2,3,'Y','Y',2),(1,2,3,'Y','Y',3)],5),
 ('R10','NULL quantity diagnostic',[(1,2,3,'Y','Y',None)],0),
 ('R11','zero quantity',[(1,2,3,'Y','Y',0),(1,2,3,'N','Y',0)],0)]
protocol={'schema':'eva.audit.r12.sql-protocol/1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','owner':'A06','peer':'A05','independent':'A11','task':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','controls':['A05-C13','A06-C12'],'actor':'Gestionar/responsabil canal citește disponibilul articolului','requirement':'Stoc disponibil vânzării = fizic minus rezervări de vânzare; cantitățile comandate furnizorilor sunt o categorie nativă separată. Reutilizare MStorageReservation.getQty(..., true), păstrând filtrarea client/firma.','normal_path':['FisaCanalProces.stoc -> stocCuSet -> stocArticol -> surse.brut -> FisaCanalCalcul.stocCalculat','RezervareStoc.disponibil -> SQL_REZ_NATIVA (apelant citit static)'],'sources':meta,'native_binding':nm,'hypothesis_not_yet_tested':'Ambele SQL EVA scad și Qty pentru IsSOTrx=N, în timp ce disponibilul nativ scade doar IsSOTrx=Y.','method':'Extract Java string literals from exactly the two bounded source expressions, compare byte-for-byte after whitespace normalization, execute unmodified SQL in Python SQLite :memory: on minimal synthetic integer fixtures. Independent arithmetic/filter oracle in Python. This is a SQL comparator, NOT original Java/native execution or PostgreSQL conformance.','native_reference':'getQtyAvailable bytecode calls getQty with iconst_1; getQty contains IsSOTrx filter. Official upstream source corroborates semantics but does not identify deployed version.','upstream_reference':'https://github.com/idempiere/idempiere/blob/master/org.adempiere.base/src/org/compiere/model/MStorageReservation.java','fixture_columns':['ad_client_id','m_product_id','m_warehouse_id','issotrx','isactive','qty'],'cases':cases,'stock_on_hand':10,'effects':'Only ephemeral SQLite in-memory rows; NO ERP persistence, PostgreSQL, DocAction, UI, workflow, reservation creation or order import proof.','guards':['driver authored locally; no external code execution','SQLite memory only; no network/process in execution harness; read-only pinned source inputs','no current A05 PostgreSQL or N05 access','no product/system writes; results only in this unique evidence directory'],'native_first_proposal_if_confirmed':'Reuse native reservation semantics/method after validating tenant/product/warehouse ownership; retain policy differences such as IsActive explicitly; do not create new stock table.','acceptance':'No new tests until A11 concrete protocol receipt. Report each SQL value, independent expected value, derived illustrative stock and limitation; failure is finding, never change tests to green. Complete native/UI contract remains open.','coverage':'Two SQL sites read and compared; associated formula files only supporting source context, no entire-file or task execution credit.','cleanup':'Close in-memory DB; no service or temporary filesystem clone created. Evidence intentionally retained.'}
protocol['sqlite_postgresql_differences']=['No native schema constraints, AD metadata, RLS, JDBC, numeric scale or locking; no claim these synthetic rows are all insertable natively.', 'Identical subset SELECT SUM/COALESCE/WHERE bound integer parameters and ASCII Y/N comparisons; no CASE, arrays, dialect functions or casts in target SQL.', 'Integer quantities deliberately avoid SQLite floating affinity versus PostgreSQL arbitrary precision numeric differences; NULL diagnostic is explicit, not claimed valid under native Qty NOT NULL.', 'EVA IsActive filter is retained; native getQty is contextual semantics, not claimed to have the same active/client filtering. Other-client fixture tests EVA SQL only.', 'No native/JVM function executed; derived available stock uses independently written arithmetic and is illustrative, not application output.']
ref=save('Protocol_lot04_v1.json',protocol)
print(json.dumps({'protocol':ref,'sources':meta,'native':nm},ensure_ascii=False))
