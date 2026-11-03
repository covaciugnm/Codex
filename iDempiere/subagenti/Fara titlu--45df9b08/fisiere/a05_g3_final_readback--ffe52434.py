from pathlib import Path
import json,sys,datetime,hashlib
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04');rows={}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True)as conn:
 with conn.cursor(row_factory=psycopg.rows.dict_row)as c:
  c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
  def q(k,s,p=None):c.execute(s,p);rows[k]=c.fetchall()
  q('session',"SELECT pg_backend_pid(),current_setting('transaction_read_only') AS readonly")
  q('products',"SELECT m_product_id,ad_client_id,ad_org_id,value,name,isactive,isbom,isstocked,producttype,m_attributeset_id FROM m_product WHERE value LIKE 'G3%' ORDER BY m_product_id")
  ids=[int(x['m_product_id'])for x in rows['products']]
  q('warehouses',"SELECT m_warehouse_id,ad_client_id,ad_org_id,value,isactive,eva_tipevidenta FROM m_warehouse WHERE value LIKE 'G3%' ORDER BY m_warehouse_id")
  q('reservations','SELECT * FROM m_storagereservation WHERE m_product_id=ANY(%s) ORDER BY m_product_id,m_warehouse_id,issotrx,m_attributesetinstance_id',(ids,))
  q('stock','SELECT s.*,l.m_warehouse_id FROM m_storageonhand s JOIN m_locator l USING(m_locator_id) WHERE s.m_product_id=ANY(%s) ORDER BY s.m_product_id,l.m_warehouse_id,s.m_attributesetinstance_id',(ids,))
  q('sources',"SELECT eva_sursasite_id,ad_client_id,ad_org_id,eva_sursa,isactive,eva_gestiunistoc,eva_stocrezerva,m_warehouse_id,eva_vanzarionline,eva_scrierepermisa,eva_fisaspresite,eva_stocspresite,eva_urlapi FROM eva_sursasite WHERE eva_sursa LIKE 'G3%' ORDER BY eva_sursasite_id")
  q('attribute_set',"SELECT * FROM m_attributeset WHERE name LIKE 'G3%' ORDER BY m_attributeset_id")
  q('attribute_instance',"SELECT * FROM m_attributesetinstance WHERE lot LIKE 'G3%' ORDER BY m_attributesetinstance_id")
  q('reservation_metadata',"SELECT c.columnname,c.isupdateable,c.iskey,c.ismandatory,c.ad_reference_id FROM ad_column c JOIN ad_table t USING(ad_table_id) WHERE t.tablename='M_StorageReservation' ORDER BY c.columnname")
  q('auxiliary','SELECT (SELECT count(*) FROM c_orderline WHERE m_product_id=ANY(%s)) AS order_lines,(SELECT count(*) FROM eva_comandasitelinie WHERE m_product_id=ANY(%s)) AS site_lines,(SELECT count(*) FROM fact_acct WHERE m_product_id=ANY(%s)) AS fixture_facts,(SELECT count(*) FROM fact_acct) AS global_fact_count',(ids,ids,ids))
  q('trace_table',"SELECT table_name FROM information_schema.tables WHERE table_schema='adempiere' AND table_name LIKE '%reservation%'")
  for r in rows['trace_table']:
   if r['table_name']=='m_reservationtrace':q('trace_count','SELECT count(*) FROM m_reservationtrace')
  q('build','SELECT version,releaseno,lastbuildinfo,isfailonbuilddiffer FROM ad_system')
  q('validators','SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1')
assert rows['auxiliary'][0]==dict(order_lines=0,site_lines=0,fixture_facts=0,global_fact_count=308)
f=O/'Readback_final_G3_v1.json';assert not f.exists();f.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),read_only=True,rows=rows),default=str,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(sha256=hashlib.sha256(f.read_bytes()).hexdigest(),counts={k:len(v) for k,v in rows.items()},auxiliary=rows['auxiliary']),default=str))
