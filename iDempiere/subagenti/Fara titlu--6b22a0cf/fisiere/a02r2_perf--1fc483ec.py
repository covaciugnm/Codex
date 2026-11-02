import datetime,os,pathlib,sys,uuid,json,time,math,concurrent.futures
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
from psycopg import sql
base=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie');dst=base/'R2_zone/A02/probe_perf_sql.json'; assert not dst.exists()
os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'; dbname='a02_perf_'+uuid.uuid4().hex[:12]; kw={'host':'127.0.0.1','port':56481,'user':'audit_owner','connect_timeout':7};source=json.loads((base/'Reverificare_G3_rezervare_canal.json').read_text(encoding='utf8'));q=source['queries']['CHANNEL_STOCK']; assert q.count('%s')==3
result={'id':'EV-A02-R2-PERF','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sql':q,'method':'SQL exact CHANNEL_STOCK extrait de FisaCanalProces. PG local, schéma projeté synthetique deux G1/64 produits/8 locatori, valeurs avec skew. Latences SQL-only y compris tour local du driver, 2 exécutions de réchauffement puis 50 mesures par niveau avec connexions indépendantes. Pas de mesure UI/SLA ou fréquence réelle de production.','volumes':[]};
with psycopg.connect(dbname='postgres',autocommit=True,**kw) as a:
 assert a.execute('select count(*) from pg_database where datname=%s',(dbname,)).fetchone()==(0,);a.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(dbname)))
try:
 with psycopg.connect(dbname=dbname,autocommit=True,**kw) as conn:
  conn.execute('CREATE TABLE m_locator(m_locator_id integer PRIMARY KEY,m_warehouse_id integer NOT NULL); INSERT INTO m_locator SELECT i,1+(i%2) FROM generate_series(1,8)i; CREATE TABLE m_storageonhand(ad_client_id int,m_product_id int,m_locator_id int,qtyonhand numeric); CREATE INDEX perf_storage_fixture ON m_storageonhand(ad_client_id,m_product_id,m_locator_id)');
  for volume in (1000,100000,1000000):
   conn.execute('TRUNCATE m_storageonhand');conn.execute('INSERT INTO m_storageonhand SELECT 1,CASE WHEN n%%4=0 THEN 1 ELSE n%%64+1 END,n%%8+1,n%%7+1 FROM generate_series(1,%s)n',(volume,));conn.execute('ANALYZE m_storageonhand');conn.execute('ANALYZE m_locator'); params=(1,1,1);oracle=conn.execute('SELECT SUM(qtyonhand) FROM m_storageonhand WHERE m_product_id=1 AND m_locator_id IN (2,4,6,8)').fetchone()[0];
   # Producer inserts use correlated dimensions, so the selected skew product may have 0 quantity for warehouse 1.
   params=(1,1,2);oracle=conn.execute('SELECT COALESCE(SUM(qtyonhand),0) FROM m_storageonhand WHERE m_product_id=1 AND m_locator_id IN (1,3,5,7)').fetchone()[0];
   for conns in (1,10,50):
    def sample(i):
     with psycopg.connect(dbname=dbname,autocommit=True,**kw) as db:
      observed=db.execute(q,params).fetchone()[0];assert observed==oracle
      measured=[]
      for k in range(max(1,50//conns)):
       t=time.perf_counter();z=db.execute(q,params).fetchone()[0];measured.append((time.perf_counter()-t)*1000);assert z==oracle
      return measured
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(3,conns)) as ex: sets=list(ex.map(sample,range(conns)))
    vals=sorted(x for ss in sets for x in ss);pct=lambda p:round(vals[min(len(vals)-1,math.ceil(p*len(vals))-1)],3)
    result['volumes'].append(dict(volume=volume,requested_client_sessions=conns,max_simultaneous_fixture_sessions=min(3,conns),samples=len(vals),sum_expected_and_observed=str(oracle),p50_ms=pct(.5),p95_ms=pct(.95),p99_ms=pct(.99)))
finally:
 with psycopg.connect(dbname='postgres',autocommit=True,**kw) as a:a.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(dbname)));result['cleanup']=a.execute('SELECT count(*) FROM pg_database WHERE datname=%s',(dbname,)).fetchone()==(0,)
result['method']='SQL CHANNEL_STOCK extras din FisaCanalProces. PostgreSQL 16 local, model sintetic cu două G1/64 produse/8 locatori și distribuție inegală. Fiecare conexiune verifică întâi rezultatul apoi transmite măsurători pentru 50 de apeluri per nivel. Timpii includ SQL și turul local al driverului. Prima tentativă de 50 conexiuni simultane a atins limita de conexiuni a serviciului partajat și clona a fost curățată. Reluarea limitează concurența simultană la 3. Valorile 10 și 50 sunt sesiuni distribuite în loturi, nu probe de concurență efectivă 10 și 50. Nu sunt SLA și nu măsoară ERP/UX/serviciul web.'
with dst.open('x',encoding='utf8')as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(len(result['volumes']),result['cleanup'],[(s['volume'],s['requested_client_sessions'],s['p95_ms']) for s in result['volumes']]);
