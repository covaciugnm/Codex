from pathlib import Path
import sys,json,hashlib,datetime
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
conn=psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=False)
rows=[]
with conn:
 with conn.cursor()as c:
  c.execute('SET search_path=adempiere,pg_catalog')
  c.execute("SELECT table_name FROM information_schema.columns WHERE table_schema='adempiere' AND column_name='isactive' AND (table_name LIKE '%processor%' OR table_name LIKE '%scheduler%' OR table_name IN ('ad_modelvalidator','ad_printpaper','rest_authtoken')) ORDER BY table_name")
  for (table,)in c.fetchall():
   if table=='ad_printpaper':continue
   c.execute(psycopg.sql.SQL("UPDATE {} SET isactive='N' WHERE isactive='Y'").format(psycopg.sql.Identifier('adempiere',table)));rows.append({'table':table,'deactivated':c.rowcount})
  c.execute("UPDATE ad_client SET smtphost='127.0.0.1',smtpport=1,requestemail='synthetic@example.invalid',issmtpauthorization='N',isserveremail='N',modelvalidationclasses=NULL")
  c.execute("UPDATE ad_user SET email=NULL,notificationtype='X'")
  c.execute("UPDATE rest_authtoken SET isactive='N'")
  c.execute("SELECT ad_client_id,value FROM ad_client ORDER BY ad_client_id");clients=c.fetchall();assert [r[0]for r in clients]==[0,11]
  c.execute("SELECT ad_role_id,ad_client_id,name,userlevel FROM ad_role WHERE ad_client_id=11 ORDER BY ad_role_id");roles=c.fetchall()
  c.execute("SELECT ad_user_id,ad_client_id,name FROM ad_user WHERE ad_client_id=11 ORDER BY ad_user_id");users=c.fetchall()
  c.execute("SELECT ad_org_id,ad_client_id,value FROM ad_org ORDER BY ad_org_id");orgs=c.fetchall()
  c.execute("SELECT version FROM ad_system");version=c.fetchone()[0]
  c.execute("SELECT ad_client_id,smtphost,smtpport,isserveremail FROM ad_client ORDER BY ad_client_id");mail=c.fetchall()
  c.execute("SELECT name,current_setting(name) FROM pg_settings WHERE name IN ('listen_addresses','port','statement_timeout','idle_in_transaction_session_timeout') ORDER BY name");settings=c.fetchall()
  c.execute("SELECT count(*) FROM ad_scheduler WHERE isactive='Y'");sched=c.fetchone()[0];assert sched==0
  c.execute("SELECT count(*) FROM ad_modelvalidator WHERE isactive='Y'");vals=c.fetchone()[0];assert vals==0
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target':'LOCAL synthetic cluster127.0.0.1:56455 only','seed_type':'GardenWorld original image seed enriched solely by earlier A07 synthetic tests; no additional real clients','clients':clients,'roles':roles,'users':users,'organizations':orgs,'version':version,'bundle_version':'13.0.0.202603090043','mail_neutralized':mail,'deactivated':rows,'settings':settings,'active_schedulers':sched,'active_modelvalidators':vals,'limit':'Native generic PO smoke baseline temporarily disables configured validators. WMS credit requires separately enabling exact EVA event bundle and normal role/process; this baseline cannot receive WMS acceptance.'}
target=OUT/'Izolare_si_readiness_seed.json';assert not target.exists();target.write_text(json.dumps(report,default=str,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,default=str,ensure_ascii=False))
