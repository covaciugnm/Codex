import contextlib,datetime,hashlib,io,json,os,pathlib,re,sys,tempfile,uuid
from unittest.mock import patch
OUT=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R2_zone/A02');OUT.mkdir(parents=True,exist_ok=True)
SRC=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102');sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(SRC/'backend')];sys.dont_write_bytecode=True
os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
import psycopg
from psycopg import sql
from sqlalchemy import create_engine,text
from app.idempiere.client_map_migration import migrate_client_map_per_cabinet
uid='a02_r2_'+uuid.uuid4().hex[:14];kw={'host':'127.0.0.1','port':56481,'user':'audit_owner','connect_timeout':8};assert re.fullmatch(r'a02_r2_[a-f0-9]{14}',uid)
ev={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':'EV-A02-R2-PG16','sha':'6df998aee0e514d30856c461962afe99ebd0d113','host':'127.0.0.1:56481','clone':uid,'source_template':'p01_garden','steps':[],'cleanup':False}; evfile=OUT/'probe_pg_migration_portal.json'
if evfile.exists():raise RuntimeError('immutable evidence already exists')
with psycopg.connect(dbname='postgres',autocommit=True,**kw) as admin:
 assert admin.execute('select count(*) from pg_database where datname=%s',(uid,)).fetchone()==(0,)
 admin.execute(sql.SQL('CREATE DATABASE {} TEMPLATE p01_garden').format(sql.Identifier(uid)))
try:
 with psycopg.connect(dbname=uid,autocommit=True,**kw) as con:
  ev['server_version']=con.execute('SELECT version()').fetchone()[0];con.execute('CREATE SCHEMA fixture_a02');con.execute('SET search_path=fixture_a02,public');
  engine=create_engine('postgresql+psycopg://audit_owner@127.0.0.1:56481/'+uid,connect_args={'options':'-c search_path=fixture_a02,public'});
  for case,rows in [('newer_logically_inserted_first',[('2026-10-20',210),('2026-01-10',110)]),('newer_logically_inserted_last',[('2026-01-10',110),('2026-10-20',210)]),('unique_input',[('2026-10-20',210)])]:
   con.execute('DROP TABLE IF EXISTS fixture_a02.eva_idempiere_client_map');con.execute('CREATE TABLE fixture_a02.eva_idempiere_client_map(tenant_cui text, managing_uuid text, idempiere_client_id int, mapping_effective_date date)');
   for date,client in rows:
    with psycopg.connect(dbname=uid,**kw) as tx:tx.execute('INSERT INTO fixture_a02.eva_idempiere_client_map VALUES (%s,%s,%s,%s)',('SYNTH','cabA',client,date))
   def values():return [dict(ctid=r[0],client=r[1],business_date=str(r[2])) for r in con.execute('select ctid::text,idempiere_client_id,mapping_effective_date from fixture_a02.eva_idempiere_client_map order by ctid')]
   before=values();outbuf=io.StringIO()
   with contextlib.redirect_stdout(outbuf):migrate_client_map_per_cabinet(engine)
   after=values()
   with contextlib.redirect_stdout(outbuf):migrate_client_map_per_cabinet(engine)
   after2=values();ev['steps'].append(dict(id='F08-'+case,actual_callable='app.idempiere.client_map_migration.migrate_client_map_per_cabinet',before=before,after=after,rerun=after2,expected_latest_business_mapping=210,observed_client=after[0]['client'],passed_business_oracle=(after[0]['client']==210),qualification='Date of mapping is synthetic oracle. Existing legacy inputs with one row per CUI do not trigger deduplication. Earlier and later inserts committed in independent transactions.'))
  engine.dispose();ddl=(SRC/'backend/migrations/eva_product_ext.sql').read_text(encoding='utf8');con.execute(ddl);con.execute("INSERT INTO eva_product_ext(tenant_cui,m_product_id,ad_client_id,sku_cache) VALUES('SAME',123,11,'SRC-A')")
  try:con.execute("INSERT INTO eva_product_ext(tenant_cui,m_product_id,ad_client_id,sku_cache) VALUES('SAME',123,22,'SRC-B')");state='NO_ERROR'
  except psycopg.errors.UniqueViolation as e:state=e.sqlstate
  con.execute("INSERT INTO eva_product_ext(tenant_cui,m_product_id,ad_client_id,sku_cache) VALUES('OTHER',123,22,'SRC-B')")
  ev['steps'].append(dict(id='F05-local-keys',sql_sha256=hashlib.sha256(ddl.encode()).hexdigest(),same_cui_same_product_second_sqlstate=state,rows=con.execute('SELECT tenant_cui,m_product_id,ad_client_id,sku_cache FROM eva_product_ext ORDER BY tenant_cui').fetchall(),scope='Real portal DDL, same numeric product ID in two cabinets sharing tenant_cui in one portal schema. Different CUI succeeds. No authenticated data read was performed; this is a storage collision.'))
finally:
 with psycopg.connect(dbname='postgres',autocommit=True,**kw) as admin:
  admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(uid)));ev['cleanup']=admin.execute('select count(*) from pg_database where datname=%s',(uid,)).fetchone()==(0,)
with evfile.open('x',encoding='utf8') as f:json.dump(ev,f,ensure_ascii=False,indent=2,default=str)
print(json.dumps({'cases':[x['id'] for x in ev['steps']],'cleanup':ev['cleanup']}))
