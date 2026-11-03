from pathlib import Path
import json,sys,datetime,hashlib,re,subprocess
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Comanda_rezervare_lot05');label=sys.argv[1]
p=json.loads((O/'Protocol_Comanda_rezervare_v1.json').read_text(encoding='utf8'))
tables=p['G01_izolare_identitate_schema']['schema_minima']+['EVA_MapareProdusSite','M_Transaction','M_CostDetail','C_Invoice','C_InvoiceLine','EVA_AlarmaLunaViitoare','C_Calendar','C_Year','EVA_CanalVanzare','EVA_CanalGrupa','C_BP_Group','C_Campaign','AD_SysConfig','EVA_SetareFirmaPerioada','EVA_SetareFirmaJurnal']
rows={};native=['C_Order','C_OrderLine','C_DocType','M_StorageReservation','M_StorageReservationLog','M_InOut','M_InOutLine','M_InOutConfirm','M_InOutLineConfirm','M_Transaction','M_CostDetail']
for t in native:
 f=O/'native_bytecode'/('I_'+t+'.txt')
 if not f.exists():
  r=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-constants','-classpath','D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar','org.compiere.model.I_'+t],capture_output=True);assert r.returncode==0;r.stdout.decode();f.write_bytes(r.stdout)
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True) as conn:
 with conn.cursor(row_factory=psycopg.rows.dict_row) as c:
  c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
  def q(k,s,p=None):c.execute(s,p);rows[k]=c.fetchall()
  names=sorted(set(t.lower() for t in tables))
  q('session',"SELECT pg_backend_pid(),current_setting('transaction_read_only') AS readonly, current_setting('transaction_isolation') AS isolation")
  q('system','SELECT version,releaseno,lastbuildinfo,isfailonbuilddiffer,dbaddress FROM ad_system')
  q('validators','SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1')
  q('tables','SELECT ad_table_id,tablename,accesslevel,isactive,entitytype FROM ad_table WHERE lower(tablename)=ANY(%s) ORDER BY lower(tablename)',(names,))
  q('columns','SELECT t.tablename,c.ad_column_id,c.columnname,c.ad_reference_id,c.ad_reference_value_id,c.fieldlength,c.ismandatory,c.iskey,c.isupdateable,c.defaultvalue,c.columnsql,c.entitytype FROM ad_column c JOIN ad_table t USING(ad_table_id) WHERE lower(t.tablename)=ANY(%s) ORDER BY lower(t.tablename),lower(c.columnname)',(names,))
  q('physical',"SELECT table_name,column_name,data_type,udt_name,is_nullable,column_default,character_maximum_length,numeric_precision,numeric_scale FROM information_schema.columns WHERE table_schema='adempiere' AND table_name=ANY(%s) ORDER BY table_name,ordinal_position",(names,))
  q('constraints',"SELECT c.relname,t.conname,t.contype,pg_get_constraintdef(t.oid) AS definition FROM pg_constraint t JOIN pg_class c ON c.oid=t.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relname=ANY(%s) ORDER BY c.relname,t.conname",(names,))
  q('indexes',"SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='adempiere' AND tablename=ANY(%s) ORDER BY tablename,indexname",(names,))
  q('doc_types','SELECT c_doctype_id,ad_client_id,name,docbasetype,docsubtypeso,issotrx,isactive,isautogenerateinout,isautogenerateinvoice,ispickqaconfirm,isshipconfirm,issplitwhendifference,docnosequence_id,c_doctypeshipment_id,c_doctypeinvoice_id FROM c_doctype WHERE ad_client_id IN(0,11) ORDER BY 1')
  q('price_lists','SELECT * FROM m_pricelist WHERE ad_client_id=11 ORDER BY 1')
  q('price_versions','SELECT m_pricelist_version_id,m_pricelist_id,name,validfrom,isactive FROM m_pricelist_version WHERE ad_client_id=11 ORDER BY 1')
  q('tax','SELECT c_tax_id,ad_client_id,name,rate,sopotype,validfrom,isactive,issummary,isdefault,to_country_id,c_taxcategory_id FROM c_tax WHERE ad_client_id=11 ORDER BY 1')
  q('periods','SELECT p.c_period_id,p.name,p.startdate,p.enddate,p.ad_client_id,c.docbasetype,c.periodstatus FROM c_period p JOIN c_periodcontrol c USING(c_period_id) WHERE p.ad_client_id=11 AND c.docbasetype IN(\'SOO\',\'MMS\') ORDER BY p.startdate DESC LIMIT 20')
  q('paymentterms','SELECT c_paymentterm_id,name,isactive FROM c_paymentterm WHERE ad_client_id=11')
  q('bp_groups','SELECT c_bp_group_id,value,name,isactive FROM c_bp_group WHERE ad_client_id=11')
  if any(x['table_name']=='eva_canalgrupa' for x in rows['physical']): q('bp_group_links','SELECT * FROM eva_canalgrupa WHERE ad_client_id=11')
  else: rows['bp_group_links']=[{'missing_table':'eva_canalgrupa','result':'STOP_SCHEMA_DEPENDENCY'}]
  q('categories','SELECT m_product_category_id,name,isactive FROM m_product_category WHERE ad_client_id=11')
  q('counts',"SELECT (SELECT count(*) FROM ad_client WHERE ad_client_id NOT IN(0,11)) AS foreign_clients,(SELECT count(*) FROM ad_scheduler WHERE isactive='Y') AS active_schedulers,(SELECT count(*) FROM rest_authtoken WHERE isactive='Y') AS active_tokens,(SELECT count(*) FROM fact_acct) AS fact_count")
ad={(x['tablename'].lower(),x['columnname'].lower()):x for x in rows['columns']};phys={(x['table_name'],x['column_name']):x for x in rows['physical']};checks=[]
for t in native:
 for n in re.findall(r'COLUMNNAME_\w+ = "([^"]+)"',(O/'native_bytecode'/('I_'+t+'.txt')).read_text()):
  k=(t.lower(),n.lower());a=ad.get(k);b=phys.get(k);checks.append(dict(table=t,column=n,ad=bool(a),physical=bool(b),virtual=bool(a and a['columnsql']),passed=bool(a) and (bool(b) or bool(a['columnsql']))))
required={'EVA_ComandaSite':'EVA_ComandaSite_ID AD_Client_ID EVA_Sursa EVA_StareValidare C_Order_ID M_InOut_ID C_Invoice_ID','EVA_ComandaSiteLinie':'EVA_ComandaSiteLinie_ID EVA_ComandaSite_ID AD_Client_ID M_Product_ID EVA_Cantitate EVA_CantitateRezervata EVA_StareLinie C_Order_ID M_InOut_ID C_Invoice_ID','EVA_SursaSite':'EVA_SursaSite_ID AD_Client_ID M_Warehouse_ID EVA_GestiuniStoc EVA_StocRezerva EVA_UrlApi','C_BPartner':'AD_OrgBP_ID EVA_LimitaSold','EVA_CanalGrupa':'AD_Client_ID C_BP_Group_ID EVA_CanalVanzare_ID','EVA_AlarmaLunaViitoare':'AD_Table_ID Record_ID'}
for t,ns in required.items():
 for n in ns.split():
  k=(t.lower(),n.lower());checks.append(dict(table=t,column=n,ad=k in ad,physical=k in phys,passed=k in ad and k in phys))
doc=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),read_only=True,rows=rows,checks=checks,failed=[x for x in checks if not x['passed']],limit='Existență nominală plus schema/AD exacte în rânduri; nu probă globală de compatibilitate sau editabilitate. LastBuildInfo nu este schimbat.')
f=O/(label+'.json');assert not f.exists();f.write_text(json.dumps(doc,default=str,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),checks=len(checks),failed=doc['failed'],counts=rows['counts'])))
