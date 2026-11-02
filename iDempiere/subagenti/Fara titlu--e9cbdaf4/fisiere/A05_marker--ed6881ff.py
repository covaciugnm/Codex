import os,pathlib,json,hashlib,uuid,re,datetime,sys
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
from psycopg import sql
O=pathlib.Path(__file__).parent;src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/corelare/LoturiArticole.java')
txt=src.read_text(encoding='utf8');expression=re.search(r'static final String SQL_URMARIT = (.*?);',txt,re.S)[1];query=''.join(re.findall(r'"([^"]+)"',expression)).replace('?','%s')
os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf';dbname='a11wr2_'+uuid.uuid4().hex[:12]; assert re.fullmatch('a11wr2_[a-z0-9]{12}',dbname)
def conn(name,ac=False):return psycopg.connect(host='127.0.0.1',port=56481,user='audit_owner',dbname=name,autocommit=ac)
rec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_file':src.name,'sha256_original_bytes':hashlib.sha256(src.read_bytes()).hexdigest(),'query':query,'cases':[]}
with conn('postgres',True) as admin:
 assert admin.execute('select inet_server_addr()::text,current_user').fetchone()==('127.0.0.1/32','audit_owner')
 admin.execute(sql.SQL('create database {}').format(sql.Identifier(dbname)))
 try:
  with conn(dbname) as c:
   c.execute('create temporary table m_product(ad_client_id int,m_product_id int,m_attributeset_id int); create temporary table m_attributeset(ad_client_id int,m_attributeset_id int,islot text,isguaranteedate text,isserno text,isinstanceattribute text,mandatorytype text,description text);')
   c.execute("insert into m_product values (11,7701,902); insert into m_attributeset values (11,902,'Y','Y','N','Y','N','native same flags');")
   for label,desc,want in [('native semantic flags only','native same flags',0),('same product and set, exact marker','EVA-P01.T329-LOT',1),('same product and set renamed marker','EVA-P01.T329-LOT-A11',0)]:
    c.execute('update m_attributeset set description=%s',(desc,))
    value=c.execute(query,(11,7701,'EVA-P01.T329-LOT')).fetchone()[0];assert value==want
    rec['cases'].append({'case':label,'expected_for_current_impl':want,'actual':value})
   fake=c.execute(query,(12,7701,'EVA-P01.T329-LOT')).fetchone()[0];assert fake==0
   c.rollback()
 finally:
  admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(dbname)));rec['cleanup']=admin.execute('select count(*) from pg_database where datname=%s',(dbname,)).fetchone()[0]==0
rec['scope']='Exact SQL from fixed LoturiArticole class, isolated synthetic tables, same product/set except marker. Confirms implemented selection; current D-T329-8 explicitly identifies company set by marker. Generic native→EVA compatibility is a requirement decision, not a universal defect proved by the three results.'
(O/'A05_lot_marker_PG.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf8');print(rec['cases'],rec['cleanup'])

