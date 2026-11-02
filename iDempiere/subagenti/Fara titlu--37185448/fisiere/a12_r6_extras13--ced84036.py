from a12_r6_exec import *
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
q={'T18.01-R4-001':("select to_regclass('adempiere.eva_starepornire')::text, (select count(*) from adempiere.ad_table where lower(tablename)='eva_starepornire')","Tabel fizic și AD_Table EVA_StarePornire; sunt necesare suplimentar cinci poziții pe firmă după executarea procesului."),
'T18.02-R4-001':("select to_regclass('adempiere.c_periodcontrol')::text, (select count(*) from adempiere.ad_table where lower(tablename)='c_periodcontrol')","C_PeriodControl există; indicația de reutilizare nu dovedește logica EVA de selectare a lunilor sau absența unui SQL nou."),
'T27.36-R4-001':("select t.tablename,(select count(*) from adempiere.ad_column c where c.ad_table_id=t.ad_table_id) from adempiere.ad_table t where lower(t.tablename) like '%harta%' and lower(t.tablename) like '%declara%'","Dicționarul de date al hărții declarațiilor; trebuie și lansarea ecranului."),
'T40.14-R4-001':("select count(*) from adempiere.ad_column where lower(columnname)='costingmethod'","Suportul nativ al metodei de cost; verificarea mapării TIP_DESC și a rezultatelor FIFO/LIFO/CMP rămâne distinctă.")}
with psycopg.connect(host='127.0.0.1',port=56481,user='audit_owner',dbname='p01_garden')as db:
 db.execute('set transaction read only');out=[]
 for cid,(stmt,limit) in q.items():out.append({'criterion':cid,'database':'p01_garden, reproducere restaurată din GardenWorld','sql':stmt,'expected_subcontrol':limit,'actual':db.execute(stmt).fetchall(),'runtime_functional_certification':False})
wr(E6/'Metadate_13_selectii.json',{'rows':out})

