from pathlib import Path
import json,sys,datetime,hashlib,re
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04');label=sys.argv[1]
p=json.loads((O/'Protocol_G3_nativ_v2.json').read_text(encoding='utf8'));tables=p['G01_identity_schema']['schema_tables']+['EVA_MapareProdusSite','M_ReservationTrace','Fact_Acct','C_Order','C_OrderLine']
rows={}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True)as conn:
 with conn.cursor(row_factory=psycopg.rows.dict_row)as c:
  c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
  def q(k,s,p=None):c.execute(s,p);rows[k]=c.fetchall()
  q('system','SELECT version,releaseno,lastbuildinfo,isfailonbuilddiffer,dbaddress FROM ad_system')
  q('validators','SELECT ad_modelvalidator_id,modelvalidationclass,isactive FROM ad_modelvalidator ORDER BY 1')
  q('roles','SELECT ad_role_id,name,userlevel,ismanual,ismasterrole,isaccessallorgs FROM ad_role ORDER BY 1')
  q('user_roles','SELECT ad_user_id,ad_role_id,isactive FROM ad_user_roles ORDER BY 1,2')
  q('table',"SELECT ad_table_id,tablename,accesslevel,isactive,entitytype FROM ad_table WHERE lower(tablename)=ANY(%s) ORDER BY lower(tablename)",([x.lower()for x in tables],))
  q('columns',"SELECT t.tablename,c.ad_column_id,c.columnname,c.ad_reference_id,c.ad_reference_value_id,c.fieldlength,c.ismandatory,c.iskey,c.defaultvalue,c.columnsql,c.entitytype FROM ad_column c JOIN ad_table t USING(ad_table_id) WHERE lower(t.tablename)=ANY(%s) ORDER BY lower(t.tablename),lower(c.columnname)",([x.lower()for x in tables],))
  q('physical',"SELECT table_name,column_name,data_type,udt_name,is_nullable,column_default,character_maximum_length,numeric_precision,numeric_scale FROM information_schema.columns WHERE table_schema='adempiere' AND table_name=ANY(%s) ORDER BY table_name,ordinal_position",([x.lower()for x in tables],))
  q('constraints',"SELECT c.relname,t.conname,t.contype,pg_get_constraintdef(t.oid) AS definition FROM pg_constraint t JOIN pg_class c ON c.oid=t.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND c.relname=ANY(%s) ORDER BY c.relname,t.conname",([x.lower()for x in tables],))
  q('indexes',"SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='adempiere' AND tablename=ANY(%s) ORDER BY tablename,indexname",([x.lower()for x in tables],))
  q('counts',"SELECT (SELECT count(*) FROM ad_client WHERE ad_client_id NOT IN (0,11)) AS foreign_clients,(SELECT count(*) FROM ad_scheduler WHERE isactive='Y') AS active_schedulers,(SELECT count(*) FROM rest_authtoken WHERE isactive='Y') AS active_tokens,(SELECT count(*) FROM ad_client WHERE smtphost<>'127.0.0.1' OR smtpport<>1) AS unsafe_smtp")
ad={(r['tablename'].lower(),r['columnname'].lower()):r for r in rows['columns']};physical={(r['table_name'],r['column_name']):r for r in rows['physical']}
checks=[]
for t in ['M_StorageReservation','M_AttributeSet','M_AttributeSetInstance','M_LocatorType']:
 s=(O/'native_bytecode'/('I_'+t+'.txt')).read_text()
 for n in re.findall(r'COLUMNNAME_\w+ = "([^"]+)"',s):
  key=(t.lower(),n.lower());a=ad.get(key);b=physical.get(key)
  checks.append(dict(table=t,column=n,ad_exists=a is not None,physical_exists=b is not None,virtual=bool(a and a['columnsql']),passed=a is not None and (b is not None or bool(a['columnsql']))))
required={
 'EVA_SursaSite':'AD_Client_ID AD_Org_ID EVA_SursaSite_ID EVA_Sursa IsActive EVA_VanzariOnline EVA_ScrierePermisa EVA_FisaSpreSite EVA_StocSpreSite EVA_SursaProprie EVA_GestiuniStoc EVA_StocRezerva EVA_UltimaCitire EVA_Limba M_PriceList_ID M_Warehouse_ID EVA_UrlApi',
 'EVA_ComandaSiteLinie':'AD_Client_ID EVA_ComandaSite_ID M_Product_ID EVA_Cantitate EVA_CantitateReservata M_InOut_ID EVA_StareLinie EVA_SKU EVA_EAN',
 'EVA_ComandaSite':'EVA_ComandaSite_ID AD_Client_ID EVA_Sursa EVA_StareValidare',
 'EVA_MapareProdusSite':'AD_Client_ID EVA_Sursa IsActive M_Product_ID EVA_SKU EVA_EAN',
 'M_StorageOnHand':'AD_Client_ID M_Product_ID M_Locator_ID M_AttributeSetInstance_ID QtyOnHand',
 'M_Locator':'M_Locator_ID AD_Client_ID M_Warehouse_ID M_LocatorType_ID',
 'M_Product':'M_Product_ID AD_Client_ID IsBOM IsStocked ProductType M_AttributeSet_ID',
 'PP_Product_BOM':'AD_Client_ID PP_Product_BOM_ID M_Product_ID IsActive BOMType BOMUse Value',
 'PP_Product_BOMLine':'AD_Client_ID PP_Product_BOMLine_ID PP_Product_BOM_ID M_Product_ID QtyBOM IsActive'}
required['EVA_ComandaSiteLinie']=required['EVA_ComandaSiteLinie'].replace('EVA_CantitateReservata','EVA_CantitateRezervata')
for t,cols in required.items():
 for n in cols.split():
  key=(t.lower(),n.lower());checks.append(dict(table=t,column=n,ad_exists=key in ad,physical_exists=key in physical,passed=key in ad and key in physical))
doc=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope=tables,read_only=True,rows=rows,checks=checks,failed=[x for x in checks if not x['passed']],limit='Scoped schema only; LastBuildInfo placeholder unchanged. EVA_MapareProdusSite added as actual nested read dependency, zero writes.')
f=O/(label+'.json');assert not f.exists();f.write_text(json.dumps(doc,default=str,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),checks=len(checks),failed=doc['failed'],counts=rows['counts'])))
