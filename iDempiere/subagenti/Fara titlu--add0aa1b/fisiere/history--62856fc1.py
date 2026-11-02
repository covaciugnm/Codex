import datetime,hashlib,json,sqlite3
from pathlib import Path
here=Path(__file__).resolve().parent
q=(here/'installed-query.sql').read_text(encoding='utf-8-sig').strip()
db=sqlite3.connect(':memory:');db.create_function('starts_with',2,lambda a,b:a.startswith(b))
db.executescript("""
CREATE TABLE eva_comandasitelinie(eva_comandasite_id int,ad_client_id int,m_product_id int,eva_cantitate numeric,eva_sku text,eva_ean text,m_inout_id int,eva_starelinie text,c_order_id int);
CREATE TABLE eva_comandasite(eva_comandasite_id int,ad_client_id int,eva_sursa text,eva_starevalidare text);
CREATE TABLE m_product(ad_client_id int,m_product_id int,isbom text,isstocked text,producttype text);
CREATE TABLE eva_mapareprodussite(ad_client_id int,eva_sursa text,isactive text,m_product_id int,eva_sku text,eva_ean text);
CREATE TABLE pp_product_bom(pp_product_bom_id int,m_product_id int,ad_client_id int,isactive text,bomtype text,bomuse text,value text);
CREATE TABLE pp_product_bomline(pp_product_bom_id int,ad_client_id int,isactive text,m_product_id int,qtybom numeric);
INSERT INTO eva_comandasite VALUES(700,11,'synthetic','ELIGIBIL');
INSERT INTO eva_comandasitelinie VALUES(700,11,100,1,'SKU-TEST','EAN-TEST',null,'REZERVAT',null);
INSERT INTO m_product VALUES(11,100,'Y','N','I');
INSERT INTO pp_product_bom VALUES(1,100,11,'Y','A','A','FIXTURE-v1');
INSERT INTO pp_product_bomline VALUES(1,11,'Y',101,6);""")
def observed():return db.execute(q,('NONBIZ-PREFIX',11,101,-1,1,'REZERVAT',0,'EXCLUS')).fetchone()[0]
v1=observed()
db.execute('update pp_product_bomline set qtybom=3 where pp_product_bom_id=1')
v2=observed()
db.execute("update pp_product_bom set isactive='N' where pp_product_bom_id=1");v0=observed()
data={'id':'A06-BOM-TEMPORAL','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'Constant SQL_CERERE_COMPONENTA from installed CESIRO JAR, emitted by ExportQuery.java. SQLite in-memory runs the literal SELECT binding 8 values. PostgreSQL starts_with equivalence supplied in fixture; no PostgreSQL locks, ERP validators or documents simulated.','query_sha256':hashlib.sha256(q.encode()).hexdigest(),'unchanged_line':700,'baseline_consumption':v1,'after_edit_same_row':v2,'after_deactivation':v0,'expected_for_unchanged_committed_version':[6,6,6],'actual':[v1,v2,v0],'interpretation':'The read depends on current active BOM rows. The fixture does not establish that a particular user can edit a reserved recipe through deployed ZK or that a validator prevents such edit.'}
(here/'bom-history.json').write_text(json.dumps(data,indent=2),encoding='utf8');print(json.dumps(data))

