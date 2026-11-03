from pathlib import Path
import json,sys,re,subprocess,hashlib
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03');D=json.loads((O/'Schema_inainte_v1.json').read_text())['rows'];core=Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar')
a={(r['tablename'].lower(),r['columnname'].lower()):r for r in D['columns']};b={(r['table_name'],r['column_name']):r for r in D['physical']}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True)as conn:
 with conn.cursor()as c:
  c.execute('SET default_transaction_read_only=on');c.execute("SELECT t.tablename,c.columnname,c.columnsql FROM adempiere.ad_column c JOIN adempiere.ad_table t USING(ad_table_id) WHERE c.columnsql IS NOT NULL AND lower(t.tablename)=ANY(%s)",([r['tablename'].lower()for r in D['table']],));virtual={(t.lower(),n.lower()):s for t,n,s in c.fetchall()}
interfaces=[];unexplained=[]
for t in [r['tablename']for r in D['table'] if not r['tablename'].startswith('EVA_')]:
 name=('org.eevolution.model.I_' if t.startswith('PP_')else 'org.compiere.model.I_')+t
 r=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-constants','-classpath',str(core),name],capture_output=True,timeout=15)
 assert r.returncode==0,(t,r.stderr.decode());raw=r.stdout;(O/('native_interface_'+t+'.txt')).write_bytes(raw)
 cols=re.findall(r'COLUMNNAME_\w+ = "([^"]+)"',raw.decode())
 missing=[n for n in cols if(t.lower(),n.lower())not in b and(t.lower(),n.lower())not in virtual]
 interfaces.append({'table':t,'class':name,'class_columns':len(cols),'missing':missing,'output_sha256':hashlib.sha256(raw).hexdigest()});unexplained.extend((t,n)for n in missing)
wms=[]
for table,var in [('EVA_PerecheWms','COL_PERECHE'),('EVA_StocWms','COL_STOC'),('EVA_MiscareWms','COL_MISCARE')]:
 src=(O/'surse_df85/wms/ModelWms.java').read_text(encoding='utf8');part=src.split('Object[][] '+var+' = {')[1].split('\n    };')[0]
 refs={'STRING':10,'INTEGER':11,'DATETIME':16,'YESNO':20,'NUMBER':22}
 for name,ref,ln in re.findall(r'\{"([^"]+)", REF_(\w+), (\d+),',part):
  x=a.get((table.lower(),name.lower()));y=b.get((table.lower(),name.lower()));ok=x is not None and y is not None and int(x['ad_reference_id'])==refs[ref]
  typ={'STRING':'character varying','INTEGER':'numeric','DATETIME':'timestamp without time zone','YESNO':'character','NUMBER':'numeric'}[ref]
  ok=ok and y['data_type']==typ
  if int(ln)>0:ok=ok and int(x['fieldlength'])==int(ln) and int(y['character_maximum_length'])==int(ln)
  wms.append({'table':table,'column':name,'expected_reference':refs[ref],'expected_length':int(ln),'actual_dictionary':x,'actual_physical':y,'pass':ok})
  if not ok:unexplained.append((table,name))
expected={'M_Warehouse_ID':(11,'Y'),'EVA_TipNota':(11,'Y'),'M_Product_ID':(11,'Y'),'Qty':(22,'Y'),'M_Locator_ID':(11,'N'),'PP_Product_BOM_ID':(11,'N')}
actual={r['columnname']:(int(r['ad_reference_id']),r['ismandatory'])for r in D['parameters']};assert actual==expected
indexnames={r['indexname']for r in D['indexes']};required={'eva_perechewms_g_uk','eva_perechewms_w_uk','eva_stocwms_uk','eva_miscarewms_sursa_ix'};assert required<=indexnames
assert len(D['process'])==1 and D['process'][0]['classname']=='com.eva.ro.contab.corelare.NotaSetWmsProces' and D['process'][0]['isactive']=='Y'
report={'schema':'A05.N05.schema.reconciliation.v1','source_snapshot_sha256':hashlib.sha256((O/'Schema_inainte_v1.json').read_bytes()).hexdigest(),'native_core_sha256':hashlib.sha256(core.read_bytes()).hexdigest(),'native_interfaces':interfaces,'virtual_columns':[{'table':t,'column':n,'sql':s}for(t,n),s in virtual.items()],'dictionary_without_physical':[{'table':t,'column':n,'virtual':virtual.get((t,n))}for t,n in set(a)-set(b)],'physical_without_dictionary':[{'table':t,'column':n,'disposition':'legacy physical field not referenced by tested native interfaces/path; not a complete migration acceptance'}for t,n in set(b)-set(a)],'wms_spec_columns':wms,'params_match':actual==expected,'wms_indexes_present':sorted(required),'schema_changes':'NONE: current synthetic seed already has all required WMS/process/settings objects; no native/EVA ensure method or ALTER application tables executed','unexplained_mismatches':unexplained,'result':'PASS_SCOPED' if not unexplained else 'BLOCK','build_limit':'LastBuildInfo placeholder unchanged. isBuildOK is permissive. This matches native13 class interfaces and exact EVA WMS table/parameter specification for this process only; no global migration/build acceptance.'}
out=O/'Reconciliere_schema_efectiva_v1.json';assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'result':report['result'],'interfaces':len(interfaces),'wms_columns':len(wms),'unexplained':unexplained,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
