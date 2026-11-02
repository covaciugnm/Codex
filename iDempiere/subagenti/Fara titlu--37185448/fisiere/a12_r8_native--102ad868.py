from a12_r8_review import *
import subprocess
queries={
'T06_dictionary':"""select count(*) from ad_table where lower(tablename)='eva_comparatiebanca' UNION ALL select count(*) from ad_column c join ad_table t using(ad_table_id)where lower(t.tablename)='eva_comparatiebanca' UNION ALL select count(*) from ad_process where lower(value)='eva_comparabancasaga' UNION ALL select count(*) from ad_process_para a join ad_process p using(ad_process_id) where lower(p.value)='eva_comparabancasaga' UNION ALL select count(*) from ad_form where classname like '%ComparatieBancaForm' OR classname like '%ComparatieSagaForm';""",
'T06_index':"select indexname,indexdef from pg_indexes where schemaname='adempiere' and indexname='eva_comparatiebanca_cheie';",
'T227_ad_mapping':"""select coalesce(f.classname,'-'),count(m.ad_menu_id),count(n.node_id), string_agg(n.seqno::text,',' order by n.ad_tree_id) from ad_form f left join ad_menu m on m.ad_form_id=f.ad_form_id left join ad_treenodemm n on n.node_id=m.ad_menu_id where f.classname='com.eva.ro.contab.form.WSagaVerificareImportForm' group by f.classname;""",
'T212_source_denominator':"select count(*) from m_product_category where ad_client_id=1000000 and isactive='Y';",
'T314_role_access_metadata':"select count(*) from ad_role where name='Operator vânzări' and isactive='Y';",
'T201_trigger_catalog':"""select tablename from pg_tables where schemaname='adempiere' and (tablename ilike '%registr%control%' or tablename ilike '%registr%coresp%'); select c.relname,t.tgname from pg_trigger t join pg_class c on c.oid=t.tgrelid join pg_namespace n on n.oid=c.relnamespace where n.nspname='adempiere' and not t.tgisinternal and (c.relname ilike '%registr%control%' or c.relname ilike '%registr%coresp%') order by c.relname,t.tgname;""",
'T310_installed_processes':"select count(*) from ad_table where lower(tablename)='eva_d107beneficiar';"}
server='saga-server@192.168.100.151'
if __name__=='__main__':
 out=[]
 for k,q in queries.items():
  sql="BEGIN READ ONLY;SET LOCAL statement_timeout='7s';SET LOCAL search_path=adempiere,pg_catalog;"+q+"ROLLBACK;"
  p=subprocess.run(['ssh','-o','BatchMode=yes',server,"docker exec -i eva-postgres-cesiro sh -c 'exec psql -XqAt -v ON_ERROR_STOP=1 -U \"$POSTGRES_USER\" -d idempiere'"],input=sql.encode(),capture_output=True,timeout=17);out.append({'name':k,'sql':sql,'exit':p.returncode,'lines':p.stdout.decode('utf8','replace').splitlines(),'stderr':p.stderr.decode('utf8','replace')[:240]})
 wr(P/'Dictionar_CESIRO_readonly.json',{'utc':now(),'database':'idempiere, adempiere; only count/system metadata','queries':out});print(out)

