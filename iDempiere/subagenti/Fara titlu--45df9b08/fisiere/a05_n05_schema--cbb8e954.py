from pathlib import Path
import json,sys,datetime,hashlib
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03');label=sys.argv[1]
tables=['AD_System','AD_MigrationScript','AD_Process','AD_Process_Para','AD_Process_Access','AD_PInstance','AD_PInstance_Para','AD_User_Roles','M_Product','M_Warehouse','M_Locator','M_StorageOnHand','PP_Product_BOM','PP_Product_BOMLine','EVA_PerecheWms','EVA_StocWms','EVA_MiscareWms','EVA_SetareFirmaPerioada','EVA_SetareFirmaJurnal','C_DocType']
rows={}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True)as conn:
 with conn.cursor(row_factory=psycopg.rows.dict_row)as c:
  c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
  def q(k,s,p=None):c.execute(s,p);rows[k]=c.fetchall()
  q('system','SELECT * FROM ad_system')
  q('validators','SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1')
  q('roles','SELECT ad_role_id,name,userlevel,ismanual,ismasterrole,isaccessallorgs FROM ad_role ORDER BY 1')
  q('user_roles','SELECT ad_user_id,ad_role_id,isactive FROM ad_user_roles ORDER BY 1,2')
  q('process',"SELECT * FROM ad_process WHERE value='EVA_NotaSetWms'")
  q('parameters',"SELECT p.* FROM ad_process_para p JOIN ad_process a USING(ad_process_id) WHERE a.value='EVA_NotaSetWms' ORDER BY p.seqno")
  q('access',"SELECT x.* FROM ad_process_access x JOIN ad_process a USING(ad_process_id) WHERE a.value='EVA_NotaSetWms' ORDER BY ad_role_id")
  q('table',"SELECT ad_table_id,tablename,accesslevel,isactive,entitytype FROM ad_table WHERE lower(tablename)=ANY(%s) ORDER BY lower(tablename)",([x.lower()for x in tables],))
  q('columns',"SELECT t.tablename,c.ad_column_id,c.columnname,c.ad_reference_id,c.ad_reference_value_id,c.fieldlength,c.ismandatory,c.iskey,c.defaultvalue,c.entitytype FROM ad_column c JOIN ad_table t USING(ad_table_id) WHERE lower(t.tablename)=ANY(%s) ORDER BY lower(t.tablename),lower(c.columnname)",([x.lower()for x in tables],))
  q('physical',"SELECT table_name,column_name,data_type,udt_name,is_nullable,column_default,character_maximum_length,numeric_precision,numeric_scale FROM information_schema.columns WHERE table_schema='adempiere' AND table_name=ANY(%s) ORDER BY table_name,ordinal_position",([x.lower()for x in tables],))
  q('constraints',"SELECT c.relname,t.conname,t.contype,pg_get_constraintdef(t.oid) AS definition FROM pg_constraint t JOIN pg_class c ON c.oid=t.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relname=ANY(%s) ORDER BY c.relname,t.conname",([x.lower()for x in tables],))
  q('indexes',"SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='adempiere' AND tablename=ANY(%s) ORDER BY tablename,indexname",([x.lower()for x in tables],))
  q('counts',"SELECT (SELECT count(*) FROM ad_client WHERE ad_client_id NOT IN (0,11)) AS foreign_clients,(SELECT count(*) FROM ad_scheduler WHERE isactive='Y') AS active_schedulers,(SELECT count(*) FROM rest_authtoken WHERE isactive='Y') AS active_tokens,(SELECT count(*) FROM ad_client WHERE smtphost<>'127.0.0.1' OR smtpport<>1) AS unsafe_smtp")
  q('native_defaults',"SELECT 'category' AS kind,min(m_product_category_id) AS id FROM m_product_category WHERE ad_client_id=11 AND isactive='Y' UNION ALL SELECT 'tax',min(c_taxcategory_id) FROM c_taxcategory WHERE ad_client_id=11 AND isactive='Y' UNION ALL SELECT 'location',min(c_location_id) FROM c_location WHERE ad_client_id=11")
dest=O/(label+'.json');assert not dest.exists();dest.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':tables,'read_only':True,'rows':rows},default=str,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'file':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'counts':{k:len(v)for k,v in rows.items()},'process':rows['process'],'access':rows['access'],'roles':rows['roles'],'validators':rows['validators']},ensure_ascii=False,default=str))
