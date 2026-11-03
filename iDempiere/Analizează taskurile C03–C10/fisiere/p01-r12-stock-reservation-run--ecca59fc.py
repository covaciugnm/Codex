from pathlib import Path
import sys,json,hashlib,sqlite3,re,datetime,html
sys.stdout.reconfigure(encoding='utf-8')
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A06_Rezervari_nativ_lot04'
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def save(n,x):
 p=O/n;assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8');return ref(p)
protocol=json.loads((O/'Protocol_lot04_v1.json').read_text(encoding='utf-8'))
assert sha((O/'Protocol_lot04_v1.json').read_bytes())=='0615a353af53d9a15c73be37ef4fc969a570695db171e95f93603c1a48440410'
gate=Path(sys.argv[1]);assert gate.is_file()
assert sys.argv[2]==sha(gate.read_bytes())
g=json.loads(gate.read_text(encoding='utf-8-sig'))
# Independent reviewer supplied exact gate path/hash; approval interpretation is reviewed by root before invocation.
sources=json.loads((O/'Sources.json').read_text(encoding='utf-8'))
for s in sources:
 assert sha((R/s['source_copy']).read_bytes())==s['sha256']
literal=r'"(?:[^"\\]|\\.)*"'
def extract(file,marker,end):
 t=(O/'sources'/file).read_text(encoding='utf-8-sig')
 a=t.index(marker);b=t.index(end,a)
 expr=t[a:b]
 vals=re.findall(literal,expr)
 sql=''.join(json.loads(v) for v in vals)
 assert sql.startswith('SELECT coalesce(sum(r.qty),0) FROM m_storagereservation r WHERE r.ad_client_id=?')
 assert sql.count('?')==3 and sql.endswith("r.isactive='Y'")
 return {'source_file':file,'first_line':t.count('\n',0,a)+1,'last_line':t.count('\n',0,b)+1,'exact_sql':sql,'sql_sha256':sha(sql.encode()),'expression':expr}
q1=extract('RezervareStoc.java','static final String SQL_REZ_NATIVA =',';')
q2=extract('FisaCanalProces.java','rez = rez.add(DB.getSQLValueBDEx(trx, "SELECT coalesce(sum(r.qty),0)',', client, produs, w)')
assert q1['exact_sql']==q2['exact_sql']
qr=save('Queries.json',[q1,q2])
canaries=[]
# SQLite opens only an ephemeral :memory: database. The authorizer refuses attach, extension and schema writes after fixture setup.
db=sqlite3.connect(':memory:')
db.enable_load_extension(False)
db.execute('CREATE TABLE m_storagereservation (ad_client_id INTEGER,m_product_id INTEGER,m_warehouse_id INTEGER,issotrx TEXT,isactive TEXT,qty INTEGER)')
denied={sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH}
def auth(action,a,b,c,d):
 if action in denied:return sqlite3.SQLITE_DENY
 if action==sqlite3.SQLITE_FUNCTION and str(b or a).lower()=='load_extension':return sqlite3.SQLITE_DENY
 return sqlite3.SQLITE_OK
db.set_authorizer(auth)
try:
 db.execute("ATTACH DATABASE ':memory:' AS foreign_db")
 raise AssertionError('ATTACH was not denied')
except sqlite3.DatabaseError as e:canaries.append({'kind':'attach','blocked':True,'error':str(e)})
try:
 db.execute("SELECT load_extension('unreachable')")
 raise AssertionError('extension was not denied')
except sqlite3.DatabaseError as e:canaries.append({'kind':'extension','blocked':True,'error':str(e)})
results=[]
for cid,desc,rows,pre in protocol['cases']:
 db.execute('DELETE FROM m_storagereservation')
 db.executemany('INSERT INTO m_storagereservation VALUES (?,?,?,?,?,?)',rows)
 expected=sum((r[5] or 0) for r in rows if tuple(r[:3])==(1,2,3) and r[3]=='Y' and r[4]=='Y')
 assert expected==pre,(cid,expected,pre)
 values=[db.execute(q['exact_sql'],(1,2,3)).fetchone()[0] for q in (q1,q2)]
 result={'id':cid,'description':desc,'rows':rows,'expected_sales_reservations':expected,'two_sql_results':values,'matches_oracle':[v==expected for v in values],'derived_available_not_application_output':[max(0,10-v) for v in values],'expected_illustrative_available':max(0,10-expected),'persistent_effect':'none, SQLite memory only','type':'SQL_COMPARATOR','limit':'No native Java, PO, PostgreSQL, transaction, UI, process, order-created reservation or actual channel-publish execution.'}
 results.append(result)
db.close()
assert [r['id'] for r in results if not all(r['matches_oracle'])]==['R02','R03','R04']
rr=save('Results.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':results,'case_identities':12,'sql_site_evaluations':24,'mismatch_cases':3,'controls_matches':9,'distinct_sql_texts':1,'canaries':canaries,'database_closed':True})
driver=O/'run.py';assert not driver.exists();driver.write_bytes(Path(__file__).read_bytes())
f={'id':'R12-STOC-SO-PO-01','severity_proposed':'P2','state':'REPRODUCED_SQL_COMPARATOR_PENDING_A11','title':'Disponibilul pentru vânzare scade și cantitățile comandate furnizorilor','requirement':protocol['requirement'],'actor':protocol['actor'],'normal_path':protocol['normal_path'],'head':protocol['head'],'owner':'A06','peer':'A05','independent':'A11','task':'SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING','positive':'R01: fizic10, rezervat SO2, fără PO: ambele SQL=2; disponibil ilustrativ8.','counterexample':'R02: se adaugă doar PO5; ambele SQL=7, deși rezervarea SO rămâne2; disponibil ilustrativ3 în loc8. R03: PO15 determină sumă17/disponibil plafonat0 în loc8.','native_evidence':ref(O/'Native_binding.json'),'source_sites':[{'path':x['source_file'],'line':x['first_line'],'sql_sha256':x['sql_sha256']} for x in (q1,q2)],'effect':'Subestimarea disponibilului ar putea ascunde stoc vandabil sau respinge validarea unei comenzi. Efectul pe UI/comandă/canal este inferență din apelanți, NU executat.','native_first':protocol['native_first_proposal_if_confirmed'],'not_proved':['No production impact measured','No frontend rendering or persistent ERP effect','No native order/supplier document created','No blanket correctness of other reservation terms','No task completion or full-file execution'],'next_proof':'Native synthetic SO/PO documents or MStorageReservation PO, fixed stock, then original EVA read path and UI. Preserve tenant/org access and inactive-policy explicitly.'}
fr=save('Finding.json',f)
coverage=[]
for s in sources:
 treated=Path(s['path']).name in ['RezervareStoc.java','FisaCanalProces.java']
 coverage.append({'path':s['path'],'oid':s['oid'],'sha256':s['sha256'],'owner':s['catalog_row'].get('primary'),'peer':s['catalog_row'].get('peer'),'role':'SQL site and call chain' if treated else 'supporting formula context','reading':'bounded sections, not full-file','original_component_execution':False,'sql_comparator':treated,'original_java_executed':False,'ui':False,'persistent_effect':False,'requirement':protocol['requirement'],'normal_path':protocol['normal_path'],'positive':'R01' if treated else 'not executed','negative':'R02/R03/R04' if treated else 'not executed','result':'semantic mismatch' if treated else 'supporting context only','limit':'No full-file/task/native-contract closure','a11_receipt':'pending'})
cv=save('Coverage.json',coverage)
report={'schema':'eva.audit.r12.sql-report/1','head':protocol['head'],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protocol':ref(O/'Protocol_lot04_v1.json'),'gate':ref(gate),'queries':qr,'results':rr,'finding':fr,'coverage':cv,'counts':{'sql_comparator_sites':2,'distinct_sql_queries':1,'case_identities':12,'evaluations':24,'different_results':3,'java_or_native_methods_executed':0,'whole_files_accepted':0,'task_closures':0,'persistent_effect_tests':0},'limits':protocol['sqlite_postgresql_differences'],'resources':{'database':'in-memory SQLite closed','services_created':0,'operational_writes':0,'scratch_directories_created':0,'evidence_directory':'retained intentionally'}}
rp=save('Raport_rezervari_SQL.json',report)
esc=html.escape
body='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rezervări native SO / PO — R12</title><style>body{font:16px/1.55 system-ui;max-width:1050px;margin:25px auto;padding:0 16px;color:#162a39}h1{line-height:1.15}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:8px;border:1px solid #ccd9df;text-align:left;overflow-wrap:anywhere}code{overflow-wrap:anywhere}.warn{padding:14px;background:#fff1d4;border-left:4px solid #a16b00}a{overflow-wrap:anywhere}</style><h1>Rezervările de vânzare și comenzile către furnizori</h1>'''
body+='<p class="warn">Constatare pe SQL identic din două surse EVA, executat într-un comparator SQLite sintetic. Recepția A11 este încă în așteptare. Nu este o probă de proces iDempiere, interfață sau persistență ERP.</p>'
body+='<p>'+esc(f['counterexample'])+'</p><p>Metoda nativă <code>MStorageReservation.getQtyAvailable</code> cere explicit rezervările de vânzare prin <code>getQty(..., true, ...)</code>. Inspecția binarului iDempiere 13 confirmă filtrul <code>IsSOTrx</code>; cele două SQL EVA nu îl conțin.</p>'
body+='<p>'+esc(f['native_first'])+'</p><table><tr><th>Caz</th><th>Martor</th><th>Așteptat SO</th><th>SQL EVA</th><th>Rezultat comparator</th></tr>'
for r in results:body+='<tr>'+''.join('<td>'+esc(str(x))+'</td>' for x in [r['id'],r['description'],r['expected_sales_reservations'],r['two_sql_results'][0],'corespunde' if all(r['matches_oracle']) else 'diferență'])+'</tr>'
body+='</table><p>12 identități de caz, evaluate în două locuri SQL: 24 evaluări, nu 24 cazuri independente. 3 contraexemple, 9 controale; doi canari ai comparatorului. Fișierele de formule au fost citite parțial ca documentare; nu primesc credit de execuție.</p><ul>'
for name in ['Protocol_lot04_v1.json','Sources.json','Native_binding.json','Native_getQty_and_available.txt','Queries.json','Results.json','Finding.json','Coverage.json','Raport_rezervari_SQL.json','run.py']:body+='<li><a href="'+name+'">'+name+'</a></li>'
body+='</ul><p>Revizie: <code>'+protocol['head']+'</code>. Nicio modificare în sistemele operaționale. SQLite în memorie a fost închis; niciun serviciu sau director temporar de laborator nou.</p></html>'
(O/'Raport_rezervari_SQL.html').write_text(body,encoding='utf-8')
manifest=save('MANIFEST_A06_rezervari_lot04.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':protocol['head'],'artifacts':[ref(p) for p in sorted(O.rglob('*')) if p.is_file()],'receipt':'pending independent A11'})
print(json.dumps({'manifest':manifest,'report':rp,'counts':report['counts']},ensure_ascii=False))
