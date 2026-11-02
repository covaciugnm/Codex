import os,sys,pathlib,json,datetime,hashlib,re,uuid
from decimal import Decimal
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
from psycopg import sql
O=pathlib.Path(__file__).parent
os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
db='a11_r3_'+uuid.uuid4().hex[:12];assert re.fullmatch('a11_r3_[0-9a-f]{12}',db)
def connect(database,auto=False):
 return psycopg.connect(host='127.0.0.1',port=56481,user='audit_owner',dbname=database,autocommit=auto,options='-c statement_timeout=20000')
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'template':'p01_garden','private_clone':db,'source_git_sha':'6df998aee0e514d30856c461962afe99ebd0d113','product_writes':0,'observations':{}}
src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab')
methods={k:(src/sub).read_text(encoding='utf8') for k,sub in [('guard','fiscal/GardaRepostareImport.java'),('fisa','corelare/FisaCanalProces.java'),('sets','corelare/SetLista.java'),('oper','corelare/RezervareStoc.java')]}
def lit(text):return ''.join(re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"',text)).replace('?','%s')
queries={k:lit(re.search(r'static final String '+k+' = (.*?);',methods['oper'],re.S)[1]) for k in ['SQL_STOC','SQL_REZ_NATIVA','SQL_REZ_T22']}
queries['channel_stock']=lit(methods['fisa'].split('pe.add(DB.getSQLValueBDEx(trx,')[1].split(', client')[0]);queries['channel_native']=lit(methods['fisa'].split('rez = rez.add(DB.getSQLValueBDEx(trx,')[1].split(', client')[0]);part=methods['sets'].split('static String produsLinieSite(String produs)')[1].split(';\n')[0].split('return ')[1]; link=''.join(('%s' if v=='produs' else v[1:-1]) for v in re.findall(r'"[^"]*"|\bprodus\b',part));queries['channel_orders']=lit(methods['fisa'].split('BigDecimal cmd = DB.getSQLValueBDEx(trx,')[1].split('+ SetLista')[0])+link
r['code_sha256']={k:hashlib.sha256(v.encode()).hexdigest() for k,v in methods.items()}
r['source_queries']=queries
with connect('postgres',True) as admin:
 assert admin.execute('select inet_server_addr()::text,current_database(),current_user').fetchone()==('127.0.0.1/32','postgres','audit_owner')
 admin.execute(sql.SQL('CREATE DATABASE {} TEMPLATE p01_garden').format(sql.Identifier(db)))
 try:
  with connect(db) as c:
   assert c.execute('SELECT current_database()').fetchone()[0]==db
   c.execute('set local search_path=adempiere,public')
   guard=c.execute("select array_agg(ad_client_id order by ad_client_id),(select count(*) from ad_scheduler where isactive='Y') from ad_client").fetchone();r['clone_safety']=guard;assert guard==([0,11],0)
   cases=c.execute("select record_id from fact_acct where ad_client_id=11 and ad_table_id=318 group by record_id having count(*)>1 order by record_id limit 1").fetchone()
   if cases:
    doc=cases[0];row=c.execute('select fact_acct_id from fact_acct where ad_client_id=11 and ad_table_id=318 and record_id=%s order by fact_acct_id limit 1',(doc,)).fetchone()[0]
    c.execute("update fact_acct set description='SAGA-FIDEL A11 synthetic' where fact_acct_id=%s",(row,)); marker=c.execute("select count(*),sum(amtacctdr) from fact_acct where ad_client_id=11 and ad_table_id=318 and record_id=%s and description like 'SAGA-FIDEL%%'",(doc,)).fetchone()
    negative=c.execute("select count(*) from fact_acct where ad_client_id=0 and ad_table_id=318 and record_id=%s and description like 'SAGA-FIDEL%%'",(doc,)).fetchone()[0]; assert marker[0]>=1 and negative==0
    r['observations']['T257_marker']={'synthetic_native_record':doc,'fact_id':row,'marker_count_dr':marker,'other_client_marker_count':negative,'limit':'Native Fact_Acct on isolated cloned database; no ERP repost or guarded event was triggered.'}
   cols=c.execute("select column_name from information_schema.columns where table_schema='adempiere' and table_name='c_projecttype' and column_name in ('value','name','description') order by 1").fetchall()
   cnt=c.execute("select count(*) from (select name,coalesce(description,'') from c_projecttype where ad_client_id in (0,11) and isactive='Y' order by name)t").fetchone()[0]
   try:
    with c.transaction():c.execute('select value from c_projecttype limit 1')
   except psycopg.Error as x:bad=x.sqlstate
   assert cols==[('description',),('name',)] and bad=='42703';r['observations']['T259']={'fields':cols,'name_positive_results':cnt,'broken_value_sqlstate':bad,'limit':'Native SQL, not ZK UI rendering.'}
   c.execute("SET LOCAL search_path=pg_temp,adempiere,public")
   # Temporaries intentionally model only columns consumed by the exact Java statements. Physical schema/view semantics are verified by the separately pinned native fixture.
   c.execute('CREATE TEMP TABLE m_locator(m_locator_id int,m_warehouse_id int); CREATE TEMP TABLE m_storageonhand(ad_client_id int,m_product_id int,m_locator_id int,qtyonhand numeric); CREATE TEMP TABLE m_storagereservation(ad_client_id int,m_product_id int,m_warehouse_id int,qty numeric,isactive text,issotrx text); CREATE TEMP TABLE eva_comandasite(eva_comandasite_id int,ad_client_id int,eva_sursa text,eva_starevalidare text); CREATE TEMP TABLE eva_comandasitelinie(eva_comandasite_id int,ad_client_id int,m_product_id int,eva_cantitate numeric,eva_cantitaterezervata numeric,eva_starelinie text,m_inout_id int,eva_sku text,eva_ean text); CREATE TEMP TABLE eva_mapareprodussite(ad_client_id int,m_product_id int,eva_sursa text,isactive text,eva_sku text,eva_ean text);')
   c.execute("INSERT INTO m_locator VALUES (71,701),(72,702); INSERT INTO m_storageonhand VALUES(11,17,71,17),(11,17,72,9); INSERT INTO eva_comandasite VALUES(41,11,'CH-A','OK');INSERT INTO eva_comandasitelinie VALUES(41,11,17,6,6,'REZERVAT',null,'foo','bar');")
   def measure(stage):
    wh=[701,702];stock=sum(c.execute(queries['channel_stock'],(11,17,w)).fetchone()[0] for w in wh)
    nat=sum(c.execute(queries['channel_native'],(11,17,w)).fetchone()[0] for w in wh)
    site=c.execute(queries['channel_orders'],(11,'CH-A','EXCLUS',17,17)).fetchone()[0]
    ops=[c.execute(queries['SQL_STOC'],(11,17,w)).fetchone()[1]-c.execute(queries['SQL_REZ_NATIVA'],(11,17,w)).fetchone()[0]-c.execute(queries['SQL_REZ_T22'],(11,17,'REZERVAT',999)).fetchone()[0] for w in wh]
    so=c.execute("select coalesce(sum(qty),0) from m_storagereservation where isactive='Y' and issotrx='Y' and ad_client_id=11 and m_product_id=17").fetchone()[0]
    return {'stage':stage,'per_local_operation':ops,'arithmetic_sum':sum(ops),'published':stock-nat-site,'sales_only_published_oracle':stock-so-site}
   obs=[measure('one channel order at 6')]
   c.execute("insert into m_storagereservation values(11,17,701,3,'Y','N'),(11,17,702,2,'Y','Y')");obs.append(measure('purchase 3 and sales 2'))
   assert [[t['published'],t['sales_only_published_oracle'],t['arithmetic_sum']] for t in obs]==[[20,20,14],[15,18,9]],obs
   r['observations']['G3']=obs;r['scope']='New PG numeric fixture, actual queries extracted from pinned Java against temporary narrowly modeled tables; native schemas and separately captured E2E traces have different scope. No OSGi/server invocation.'
   c.rollback()
 finally:
  assert re.fullmatch('a11_r3_[0-9a-f]{12}',db); admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(db)))
  r['cleanup']=admin.execute('select count(*) from pg_database where datname=%s',(db,)).fetchone()[0]==0
(O/'A11_PG_independent.json').write_text(json.dumps(r,ensure_ascii=False,indent=2,default=str),encoding='utf8');print(db,r['cleanup'],r['observations'])

