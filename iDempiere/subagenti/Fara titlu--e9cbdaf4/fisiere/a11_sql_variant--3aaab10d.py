"""Reproduce query semantics on SQLite memory using exact literals of the pinned Java functions.
No ERP/database connection; this is a SQL projection, not an ERP integration test."""
import pathlib,sqlite3,re,json,datetime,hashlib
root=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab')
out=pathlib.Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\A11_reproduceri_lot1')
db=sqlite3.connect(':memory:');results=[]
def literals(txt): return ''.join(re.findall(r'"([^"]*)"',txt))
def put(id,expected,observed,scope,query=None):results.append(dict(id=id,oracle=expected,observed=observed,scope=scope,query=query))
res=(root/'corelare/RezervareStoc.java').read_text(encoding='utf8')
sqls={}
for n in ['SQL_STOC','SQL_REZ_NATIVA','SQL_REZ_T22']:
 sqls[n]=literals(re.search(r'static final String '+n+r'\s*=\s*(.*?);',res,re.S)[1])
db.executescript('create table m_locator(m_locator_id int,m_warehouse_id int);create table m_storageonhand(ad_client_id int,m_product_id int,m_locator_id int,qtyonhand numeric);create table m_storagereservation(ad_client_id int,m_product_id int,m_warehouse_id int,isactive text,issotrx text,qty numeric);create table EVA_ComandaSiteLinie(ad_client_id int,m_product_id int,eva_starelinie text,m_inout_id int,eva_comandasite_id int,eva_cantitaterezervata numeric);insert into m_locator values (10,3),(20,7);insert into m_storageonhand values(44,2,10,19),(44,2,20,13);insert into EVA_ComandaSiteLinie values (44,2,"R",null,40,5);')
def avail(w):
 stock=db.execute(sqls['SQL_STOC'],(44,2,w)).fetchone()[1];n=db.execute(sqls['SQL_REZ_NATIVA'],(44,2,w)).fetchone()[0];t=db.execute(sqls['SQL_REZ_T22'],(44,2,'R',999)).fetchone()[0];return stock-n-t
put('A02.F01',27,[avail(3),avail(7),avail(3)+avail(7)],'19+13−5=27 globally; sum of exact SQL on 2 G1 subtracts global 5 twice. Only manifests when combining separate requests; not a live order result.',sqls)
db.execute("delete from EVA_ComandaSiteLinie");put('A02.F01-control-no-reservation',32,avail(3)+avail(7),'counterexample: zero global reserve, no undercount.')
db.executemany('insert into m_storagereservation values (44,2,3,"Y",?,?)',[('N',6),('Y',2)]);put('A02.F02',17,avail(3),'19 on hand; customer reservation 2; supplier order 6 is not sales issue. Exact SQL does not filter IsSOTrx.')
bal=(root/'date/BalantaService.java').read_text(encoding='utf8')
frag=bal[bal.index('String sql =',bal.index('public static List<Rand> incarca')):];frag=frag[:frag.index(';')];frag='\n'.join(l for l in frag.splitlines() if 'orgId > 0' not in l);sql=literals(frag);db.executescript('create table c_elementvalue(c_elementvalue_id int,value text,name text);create table fact_acct(ad_client_id int,ad_org_id int,c_acctschema_id int,postingtype text,dateacct text,account_id int,amtacctdr numeric,amtacctcr numeric);insert into c_elementvalue values (78,"707.A11","Synthetic");insert into fact_acct values(44,9,100,"A","2026-10-13",78,0,125),(44,9,200,"A","2026-10-13",78,0,29),(45,9,100,"A","2026-10-13",78,0,500),(44,9,100,"B","2026-10-13",78,0,700)')
a='2026-10-01';z='2026-10-31';rows=db.execute(sql,(a,a,z,a,z,44,z)).fetchall();oracle=db.execute('select c_acctschema_id,sum(amtacctcr) from fact_acct where ad_client_id=44 and postingtype="A" group by c_acctschema_id order by 1').fetchall()
put('A03-F01',oracle,rows,'Exact BalantaService.incarca SQL orgId=0. Two schemes (one illustrative currency each); tenant 45 and budget postings excluded. Single scheme counter-control obtained by removing second scheme.',sql)
db.execute('delete from fact_acct where c_acctschema_id=200');put('A03-F01-control-one-schema',125,db.execute(sql,(a,a,z,a,z,44,z)).fetchone()[4],'single eligible scheme yields expected turnover.')
db.close()
(out/'A02_A03_SQL_independent.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.UTC).isoformat(),sha='6df998aee0e514d30856c461962afe99ebd0d113',engine=sqlite3.sqlite_version,source_hashes={str(k):hashlib.sha256(k.read_bytes()).hexdigest() for k in [root/'corelare/RezervareStoc.java',root/'date/BalantaService.java']},results=results,limit='No PostgreSQL type/locking validation; independent relational counterexample; native calls and UI not executed.'),indent=2),encoding='utf8')
print([(x['id'],x['oracle'],x['observed']) for x in results])
