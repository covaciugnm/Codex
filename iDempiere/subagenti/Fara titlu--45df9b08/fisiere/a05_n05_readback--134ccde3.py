from pathlib import Path
import json,hashlib,sys,datetime
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03');label=sys.argv[1]
rows={}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True)as conn:
 with conn.cursor(row_factory=psycopg.rows.dict_row)as c:
  c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
  def q(k,s):c.execute(s);rows[k]=c.fetchall()
  q('connection',"SELECT pg_backend_pid(),current_database(),inet_server_addr(),inet_server_port(),current_setting('transaction_isolation'),current_setting('transaction_read_only')")
  q('products',"SELECT m_product_id,ad_client_id,ad_org_id,value,name,isstocked,isbom,upc,sku FROM m_product WHERE value LIKE 'N05_%' ORDER BY m_product_id")
  q('warehouses',"SELECT m_warehouse_id,ad_client_id,ad_org_id,value,eva_tipevidenta FROM m_warehouse WHERE value LIKE 'N05_%' ORDER BY m_warehouse_id")
  q('pairs',"SELECT x.* FROM eva_perechewms x JOIN m_warehouse w ON w.m_warehouse_id=x.m_warehouse_id WHERE w.value LIKE 'N05_%' ORDER BY x.eva_perechewms_id")
  q('stock',"SELECT s.* FROM eva_stocwms s JOIN m_warehouse w USING(m_warehouse_id) WHERE w.value LIKE 'N05_%' ORDER BY s.eva_stocwms_id")
  q('movements',"SELECT s.* FROM eva_miscarewms s JOIN m_warehouse w USING(m_warehouse_id) WHERE w.value LIKE 'N05_%' ORDER BY s.eva_miscarewms_id")
  q('bom',"SELECT * FROM pp_product_bom WHERE value LIKE 'N05_%' ORDER BY pp_product_bom_id")
  q('bom_lines',"SELECT l.* FROM pp_product_bomline l JOIN pp_product_bom b USING(pp_product_bom_id) WHERE b.value LIKE 'N05_%' ORDER BY pp_product_bomline_id")
  q('native_stock',"SELECT s.* FROM m_storageonhand s JOIN m_product p USING(m_product_id) WHERE p.value LIKE 'N05_%' ORDER BY s.m_product_id,s.m_locator_id")
  q('native_facts',"SELECT f.* FROM fact_acct f JOIN m_product p USING(m_product_id) WHERE p.value LIKE 'N05_%' ORDER BY fact_acct_id")
  q('instances',"SELECT * FROM ad_pinstance WHERE ad_process_id=1000228 AND ad_pinstance_id>=1002645 ORDER BY ad_pinstance_id")
  q('instance_parameters',"SELECT p.* FROM ad_pinstance_para p JOIN ad_pinstance i USING(ad_pinstance_id) WHERE i.ad_process_id=1000228 AND i.ad_pinstance_id>=1002645 ORDER BY p.ad_pinstance_id,seqno")
  q('instance_logs',"SELECT l.* FROM ad_pinstance_log l JOIN ad_pinstance i USING(ad_pinstance_id) WHERE i.ad_process_id=1000228 AND i.ad_pinstance_id>=1002645 ORDER BY l.ad_pinstance_id,log_id")
  q('runtime_isolation',"SELECT (SELECT count(*) FROM ad_client WHERE ad_client_id NOT IN(0,11)) AS foreign_clients,(SELECT count(*) FROM ad_scheduler WHERE isactive='Y') AS active_schedulers,(SELECT count(*) FROM ad_client WHERE smtphost<>'127.0.0.1' OR smtpport<>1) AS unsafe_smtp,(SELECT count(*) FROM rest_authtoken WHERE isactive='Y') AS active_tokens,(SELECT count(*) FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid()) AS other_connections")
  q('system',"SELECT ad_system_id,version,releaseno,lastbuildinfo,isautoerrorreport,isallowstatistics,noprocessors,dbaddress FROM ad_system")
  q('validators','SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1')
p=O/(label+'.json');assert not p.exists();p.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Independent psycopg connection, read-only, after native JVM exit; synthetic owned cluster only','rows':rows},ensure_ascii=False,indent=2,default=str),encoding='utf8');print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'counts':{k:len(v)for k,v in rows.items()}},ensure_ascii=False))
