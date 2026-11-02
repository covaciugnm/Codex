import sys,pathlib,os,uuid,datetime,json,re,hashlib,contextlib,io
sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps','D:/CodexWork/eva-audit-p01-readonly-20261102/backend'];sys.dont_write_bytecode=True
import psycopg
from psycopg import sql
from sqlalchemy import create_engine
from app.idempiere.client_map_migration import migrate_client_map_per_cabinet
from decimal import Decimal
O=pathlib.Path(__file__).parent;E=O.parent;os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
dbname='a11_br2_'+uuid.uuid4().hex[:12];kw={'host':'127.0.0.1','port':56481,'user':'audit_owner'}
res={'db':dbname,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'migration_runs':[],'scope':'Only a private cloned GardenWorld, no ERP process called. Actual migration invoked via SQLAlchemy; accounting balance read on native rows via PostgreSQL. Independent from executor input fixture.'}
with psycopg.connect(dbname='postgres',autocommit=True,**kw) as admin:
 assert admin.execute('select current_database(),inet_server_addr()::text').fetchone()==('postgres','127.0.0.1/32')
 assert re.fullmatch('a11_br2_[0-9a-f]{12}',dbname)
 admin.execute(sql.SQL('create database {} template p01_garden').format(sql.Identifier(dbname)))
 try:
  with psycopg.connect(dbname=dbname,autocommit=True,**kw) as c:
   assert c.execute('select current_database()').fetchone()[0]==dbname
   c.execute("SET search_path=adempiere,public"); assert c.execute("select count(*) from ad_scheduler where isactive='Y'").fetchone()[0]==0
   for scope,atoms in [('A11laterinsertedfirst',[('2024-05-01',17),('2020-06-20',3)]),('A11laterinsertedlast',[('2020-06-20',3),('2024-05-01',17)]),('A11unique',[('2024-05-01',17)])]:
    sc=scope.lower(); assert re.fullmatch('a11[a-z]+',sc);c.execute(sql.SQL('create schema {}').format(sql.Identifier(sc)))
    c.execute(sql.SQL('create table {}.eva_idempiere_client_map(tenant_cui text,managing_uuid text,idempiere_client_id int,mapping_effective_date date)').format(sql.Identifier(sc)))
    for date,val in atoms:c.execute(sql.SQL('insert into {}.eva_idempiere_client_map values(%s,%s,%s,%s)').format(sql.Identifier(sc)),('A11CASE','cabA',val,date))
    c.execute(sql.SQL('insert into {}.eva_idempiere_client_map values(%s,%s,%s,%s)').format(sql.Identifier(sc)),('A11OTHER','cabB',54,'2021-02-11'))
    engine=create_engine('postgresql+psycopg://audit_owner@127.0.0.1:56481/'+dbname,connect_args={'options':'-c search_path='+sc+',public'})
    keep=[]
    for t in range(2):
     with contextlib.redirect_stdout(io.StringIO()):migrate_client_map_per_cabinet(engine)
     vals=c.execute(sql.SQL('select tenant_cui,idempiere_client_id from {}.eva_idempiere_client_map order by 1').format(sql.Identifier(sc))).fetchall();keep.append(vals)
    engine.dispose(); assert keep[0]==keep[1] and keep[0][-1]==('A11OTHER',54);res['migration_runs'].append({'case':scope,'input':atoms,'one_run':keep[0],'rerun':keep[1]})
   assert [x['one_run'][0][1]for x in res['migration_runs']]==[3,17,17]
   src=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/date/BalantaService.java');code=src.read_text(encoding='utf8')
   q=rd=json.loads((E/'R2_zone/A03/dovezi/pg_replay.json').read_text(encoding='utf8'));r=rd['queries'];balance=r['balance'];oracle=r['schema_oracle']
   native=c.execute(balance['sql'],tuple(balance['args'])).fetchall();by_schema=c.execute(oracle['sql'],tuple(oracle['args'])).fetchall()
   assert native and len(by_schema)>1;res['balance']={'query_on_pinned_native':balance,'query_group_by_schema':oracle,'native':native,'group_by_schema':by_schema,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scope':'Reexecuted from physical native template; totals in 2 currencies cannot be added as one money measure.'}
 finally:
  admin.execute(sql.SQL('drop database {}').format(sql.Identifier(dbname)));res['deleted']=admin.execute('select count(*) from pg_database where datname=%s',(dbname,)).fetchone()[0]==0
assert res['deleted'];(O/'pg_independent.json').write_text(json.dumps(res,ensure_ascii=False,indent=2,default=str),encoding='utf8');print([x['one_run'] for x in res['migration_runs']],res['balance']['native'][:1],res['balance']['group_by_schema'][:2],res['deleted'])

