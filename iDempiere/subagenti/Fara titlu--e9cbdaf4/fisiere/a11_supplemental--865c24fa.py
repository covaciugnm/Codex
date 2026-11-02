import sqlite3,pathlib,json,datetime,hashlib
b=pathlib.Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\A11_reproduceri_lot1');db=sqlite3.connect(':memory:');rep=[]
db.executescript("""create table fact_acct(ad_client_id int,ad_org_id int,c_acctschema_id int,postingtype text,dateacct text,account_id int,amtacctdr numeric,amtacctcr numeric);create table c_elementvalue(c_elementvalue_id int,value text);
insert into fact_acct values (7,11,1,'A','2026-11-01',42,0,97),(7,11,2,'A','2026-11-01',42,0,31),(8,11,1,'A','2026-11-01',42,0,500);insert into c_elementvalue values(42,'707.A11');""")
sql="""SELECT ev.value,SUM(f.amtacctdr-f.amtacctcr) FROM fact_acct f JOIN c_elementvalue ev ON ev.c_elementvalue_id=f.account_id WHERE f.ad_client_id=? AND f.postingtype=? AND (ev.value LIKE ?) AND f.dateacct BETWEEN ? AND ? GROUP BY ev.value HAVING ABS(SUM(f.amtacctdr-f.amtacctcr))>=0.005 ORDER BY ev.value"""
rep.append({'id':'A03-F02','dynamic_java_clause':'NotaInchidere.net, tipare=[7%], deLa != null, captured SHA. Query reconstructed from exact dynamic fragments. Schema selection for creating document static only; no GL Journal posted.', 'query':sql,'observed':db.execute(sql,[7,'A','7%','2026-11-01','2026-11-30']).fetchall(),'oracle':db.execute("select c_acctschema_id,sum(amtacctdr-amtacctcr) from fact_acct where ad_client_id=7 group by c_acctschema_id order by c_acctschema_id").fetchall()})
db.executescript("create table m_product(id integer primary key,cid integer,value text,active text);create unique index m_product_value on m_product(cid,value);insert into m_product values(111,6,'A11-CPP','Y');update m_product set active='N' where id=111;")
try:db.execute("insert into m_product values (222,6,'A11-CPP','Y')");deactivation_guard=False
except sqlite3.IntegrityError:deactivation_guard=True
db.execute("update m_product set value='RETIRED-A11-CPP' where id=111");db.execute("insert into m_product values (222,6,'A11-CPP','Y')")
rep.append({'id':'A05-F08','oracle':'old business code never assigned to another identity','deactivated_original_still_blocks_code':deactivation_guard,'after_rename':db.execute('select id,cid,value,active from m_product order by id').fetchall(),'scope':'Independent projected unique key in SQLite; corroborates behavior of A05 actual authenticated REST seed, not an independent ERP/REST rerun.'})
db.close();(b/'A03_A05_supplemental.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.UTC).isoformat(),'sha':'6df998aee0e514d30856c461962afe99ebd0d113','cases':rep},indent=2),encoding='utf8');print(rep)

