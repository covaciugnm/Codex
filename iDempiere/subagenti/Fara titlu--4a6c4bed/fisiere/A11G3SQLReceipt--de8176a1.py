from pathlib import Path
import ast,json,hashlib,re,sqlite3,datetime,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');D=R/'executie/R12_fisiere/A06_Rezervari_nativ_lot04';O=R/'executie/R12_fisiere/A11/Val03_loturi'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,d):
 p=O/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':h(p)}
checks=[]
def ck(label,ok,detail=None):checks.append({'check':label,'ok':bool(ok),'detail':detail})
mf=D/'MANIFEST_A06_rezervari_lot04.json';ck('manifest',h(mf)=='bf5dee20c4e539bc10610ec17ba23433d907a71e483f53fb31c0dd36293e4232')
for x in read(mf)['artifacts']:ck(x['path'],h(R/x['path'])==x['sha256'] and (R/x['path']).stat().st_size==x['bytes'])
queries=read(D/'Queries.json');derived=[]
for q in queries:
 lines=(D/'sources'/q['source_file']).read_text(encoding='utf-8').splitlines();expression='\n'.join(lines[q['first_line']-1:q['last_line']]);sql=''.join(ast.literal_eval(l) for l in re.findall(r'"(?:[^"\\]|\\.)*"',expression));ck('SQL extracted from source '+q['source_file'],sql==q['exact_sql'] and hashlib.sha256(sql.encode()).hexdigest()==q['sql_sha256']);derived.append(sql)
ck('one SQL for two sites',len(queries)==2 and len(set(derived))==1)
results=read(D/'Results.json');r=results['cases'];ck('12 unique fixtures',len(r)==len({x['id'] for x in r})==12)
for x in r:
 sales=sum((v[5] or 0) for v in x['rows'] if v[:3]==[1,2,3] and v[3]=='Y' and v[4]=='Y')
 total=sum((v[5] or 0) for v in x['rows'] if v[:3]==[1,2,3] and v[4]=='Y')
 ck('counter arithmetic '+x['id'],sales==x['expected_sales_reservations'] and x['two_sql_results']==[total,total])
ck('three mismatching fixtures',[x['id'] for x in r if not all(x['matches_oracle'])]==['R02','R03','R04'])
own=[];base=[41,52,63,'Y','Y',4]
fixtures=[('SO_only',[base]),('PO_only_change',[base,[41,52,63,'N','Y',9]]),('inactive_PO_control',[base,[41,52,63,'N','N',9]]),('foreign_PO_control',[base,[99,52,63,'N','Y',9]])]
for name,rows in fixtures:
 c=sqlite3.connect(':memory:');c.execute('CREATE TABLE m_storagereservation(ad_client_id INTEGER,m_product_id INTEGER,m_warehouse_id INTEGER,issotrx TEXT,isactive TEXT,qty INTEGER)');c.executemany('INSERT INTO m_storagereservation VALUES(?,?,?,?,?,?)',rows)
 def authorizer(code,a,b,*rest):
  if code==sqlite3.SQLITE_SELECT:return sqlite3.SQLITE_OK
  if code==sqlite3.SQLITE_READ and a=='m_storagereservation':return sqlite3.SQLITE_OK
  if code==sqlite3.SQLITE_FUNCTION and b in ('sum','coalesce'):return sqlite3.SQLITE_OK
  return sqlite3.SQLITE_DENY
 c.set_authorizer(authorizer);actual=c.execute(derived[0],(41,52,63)).fetchone()[0]
 expected=sum(x[5] for x in rows if x[:3]==[41,52,63] and x[3:5]==['Y','Y'])
 blocked=False
 try:c.execute("ATTACH DATABASE ':memory:' AS forbidden")
 except sqlite3.DatabaseError:blocked=True
 c.close();closed=False
 try:c.execute('SELECT 1')
 except sqlite3.ProgrammingError:closed=True
 own.append({'id':name,'rows':rows,'sql_actual':actual,'independent_sales_oracle':expected,'illustrative_stock50_actual':50-actual,'illustrative_stock50_expected':50-expected,'attach_denied':blocked,'connection_closed':closed})
ck('A11 4 changed-data fixtures',[x['sql_actual'] for x in own]==[4,13,4,4] and all(x['independent_sales_oracle']==4 and x['attach_denied'] and x['connection_closed'] for x in own))
assert all(x['ok'] for x in checks),[x for x in checks if not x['ok']]
proof=save('Proba_A11_G3_SQL_lot04_v1.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Comparator SQLite memory, exact extracted query (one text/two sites); independent values41/52/63 and SO4/PO9; no original Java/native methods','source_sql':derived[0],'cases':own,'unique_cases':4,'evaluations':4,'canary_evaluations':4,'no_persistent_effect':True,'no_scratch_or_services':True})
qa=save('QA_A11_G3_SQL_lot04_v1.json',{'checks':checks,'issues':[],'metadata_and_independent_counter_oracle':True})
verdict=save('Verdict_A11_G3_SQL_lot04_v1.json',{'schema':'A11.R12.G3.sql.receipt.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'df85d33c1648ce2b2df130a60a05ef696e2e5480','decision':'ACCEPTAT_DEFECT_IN_LOGICA_SQL_CU_REPRODUCERE_LIMITATA_COMPARATOR; EFECT_ERP_UI_NEEXECUTAT','target':{'path':str(mf.relative_to(R)).replace('\\','/'),'sha256':h(mf)},'finding':'R12-STOC-SO-PO-01','priority_proposed':'P2','evidence':{'root':'12 fixtures ×2 situri; aceeași interogare,3 fixtures diferă de oracol și9controle conforme; zeroJava/native/ERP','A11':proof,'QA':qa,'binding':'Binarul nativ identificat la poartă folosește IsSOTrx=true în getQtyAvailable; identitatea lui nu se confundă cu versiunea serverHEAD.'},'conclusion':'SQL-ul celor două surse include Qty cu IsSOTrx=N în aceeași sumă care este scăzută din disponibil. Martorul A11 menține SO4 și fizic50; numai PO9 schimbat duce SQL4→13 și disponibilul ilustrativ46→37. Citirea apelanților susține impactul potențial asupra afișării/validării, dar acestea nu au fost rulate.','per_file':[{'file':'RezervareStoc.java','lines':'203-204; consumator214-220','state':'SQL_COMPARATOR_PARTIAL','whole_file':False},{'file':'FisaCanalProces.java','lines':'370-371; consumator342-345','state':'SQL_COMPARATOR_PARTIAL','whole_file':False},{'file':'FisaCanalCalcul.java','state':'SUPORT_STATIC_FORMULA; NEEXECUTAT','whole_file':False},{'file':'RegulaStocCanal.java','state':'SUPORT_STATIC_CONTEXT; NEEXECUTAT','whole_file':False}],'native_first':'Adaptează citirea existentă la semantica nativă de rezervări de vânzare; folosește metoda nativă potrivită numai după verificarea ownership/client/warehouse/produs/ASI și păstrarea politicii IsActive. Nu este nevoie de o tabelă nouă de stoc.','limits':['SQLite nu dovedește PostgreSQL/PO/JDBC/locking/RLS/scale numeric.','NULL este diagnostic, nu rând nativ valid presupus.','Stocul derivat este aritmetică ilustrativă, nu valoare capturată din G3/UI. Pentru RezervareStoc.disponibil formula nu plafonează la0, iar FisaCanalCalcul o plafonează; valorile pozitive demonstrate sunt comune, exemplul PO15→0 se referă numai formulei ilustrative plafonate.','12fixtures nu sunt24cerințe/24testeJava;4A11 nu se dublează pentru două situri identice.','Nu s-a demonstrat impactul asupra unui client operațional ori o comandă reală.'],'next_tests':['Clonă nativă separată: stoc fix plus rezervăriSO/PO create prin PO/documente native, apelant EVA original și recitire; apoi UI cu rol/canal.','Păstrează separat rezervări propriiT22/seturi și evită dublarea lor; această constatare nu validează alți termeni.','Corelare nominală de task înainte de atribuirea unei stări sau unui criteriu; momentan SHARED_NO_TASK_ASSIGNED_PENDING_NOMINAL_MAPPING.'],'remaining_contracts_open':17,'task_closures':0,'full_file_acceptances':0,'product_score':None,'resources':'4conexiuniSQLite memory închise; nicioDBpersistată, scratch sau serviciu. Artefacte păstrate intenționat.'})
runner=O/'Runner_A11_G3_SQL_lot04_v1.py';assert not runner.exists();shutil.copyfile('D:/CodexWork/A11G3SQLReceipt.py',runner)
seal=save('Sigiliu_A11_G3_SQL_lot04_v1.json',{'files':[proof,qa,verdict,{'path':str(runner.relative_to(R)).replace('\\','/'),'sha256':h(runner)}]})
print(json.dumps({'verdict':verdict,'seal':seal,'checks':len(checks)},ensure_ascii=False))
