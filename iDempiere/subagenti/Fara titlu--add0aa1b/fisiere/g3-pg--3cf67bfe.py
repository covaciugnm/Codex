import datetime,hashlib,json,sys,os,threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
from psycopg.conninfo import make_conninfo
out=Path('D:/CodexWork/a06r2/cases');os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
def connect():
 c=psycopg.connect(make_conninfo(host='127.0.0.1',port=56481,dbname='a06_r2_20261102',user='audit_owner',options='-c statement_timeout=15000 -c search_path=a06_r2,public'))
 assert c.execute('select current_database(),inet_server_addr()::text').fetchone()==('a06_r2_20261102','127.0.0.1/32');c.commit();return c
q=Path('D:/CodexWork/a06-run-20261102/installed-query.sql').read_text(encoding='utf-8-sig').strip().replace('?','%s')
def used(c,i):return c.execute(q,('EOS-',11,i,-1,True,'REZERVAT',False,'EXCLUS')).fetchone()[0]
setup=Path('D:/CodexWork/a06-run-20261102/history.py').read_text(encoding='utf8').split('db.executescript("""')[1].split('INSERT INTO eva_comandasite')[0]
c=connect();c.execute('CREATE SCHEMA a06_r2');c.execute(setup);c.execute("CREATE TABLE a06_physical(wh int,component int,qty int);INSERT INTO a06_physical SELECT w,p,60 FROM (VALUES(1),(2)) wh(w) CROSS JOIN (VALUES(101),(102),(103)) prod(p);");c.execute("INSERT INTO m_product VALUES(11,201,'Y','N','I'),(11,202,'Y','N','I');INSERT INTO pp_product_bom VALUES(901,201,11,'Y','A','A','S1-v1'),(902,202,11,'Y','A','A','S2-v1');INSERT INTO pp_product_bomline SELECT s.id,11,'Y',p.id,s.n FROM (VALUES(901,6),(902,3)) s(id,n) CROSS JOIN (VALUES(101),(102),(103)) p(id);");c.commit()
def snap(label):
 pool={i:int(c.execute('select sum(qty) from a06_physical where component=%s',(i,)).fetchone()[0])-int(used(c,i)) for i in [101,102,103]}
 r={'stage':label,'committed_demands':[int(used(c,i)) for i in [101,102,103]],'remaining_components':pool,'orders':c.execute('select eva_sursa, l.m_product_id,l.eva_cantitate,l.eva_starelinie from eva_comandasite c join eva_comandasitelinie l using(eva_comandasite_id) order by 1').fetchall(),'projection':{'S1':min(pool.values())//6,'S2':min(pool.values())//3},'available_physically':c.execute('select component,sum(qty) from a06_physical group by component order by 1').fetchall()};c.commit();return r
report={'id':'A06-R2-G3-PG','started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Dedicated PG16 clone of GardenWorld; native table structures in adempiere are left intact. Separate a06_r2 schema has minimal synthetic tables, using exact query SQL_CERERE_COMPONENTA from installed JAR. Direct insertion of pre-reserved order lines does not run the ERP ingestion, role validation or reserveStock. Formula of set uses limiting component as in separately tested JAR.','stages':[snap('pre-order')]}
bar=threading.Barrier(2)
def book(x):
 k,p,source=x;cx=connect();bar.wait(4);cx.execute('insert into eva_comandasite values(%s,11,%s,\'ELIGIBIL\')',(k,source));cx.execute("insert into eva_comandasitelinie values(%s,11,%s,10,'sku','ean',null,'REZERVAT',null)",(k,p));cx.commit();cx.close()
with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(book,[(701,201,'Canal-A'),(702,202,'Canal-B')]))
report['stages'].append(snap('10*S1 and 10*S2 committed in separate DB sessions'))
c.execute("update pp_product_bomline set qtybom=5 where pp_product_bom_id=901");c.commit();report['stages'].append(snap('existing S1 recipe altered from 6 to 5, same commitments'))
c.execute("update pp_product_bom set isactive='N' where pp_product_bom_id=901");c.commit();report['stages'].append(snap('existing S1 recipe inactive, same commitments'))
c.execute("update pp_product_bom set isactive='Y' where pp_product_bom_id=901");c.execute("update pp_product_bomline set qtybom=6 where pp_product_bom_id=901");c.execute("update a06_physical set qty=0 where component=103");c.commit();report['stages'].append(snap('component P3 unavailable'))
# Commercial projection clamp at zero even when pre-existing commitments exceed stock.
for r in report['stages']:r['projection']={k:max(0,v) for k,v in r['projection'].items()}
report['native_formula_test_fingerprint']=hashlib.sha256(q.encode()).hexdigest()
assert [r['committed_demands'][0] for r in report['stages']]==[0,90,80,30,90]
assert report['stages'][1]['remaining_components']=={101:30,102:30,103:30}
(out/'g3-pg.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf8')
print([(r['stage'],r['committed_demands'],r['projection']) for r in report['stages']])

