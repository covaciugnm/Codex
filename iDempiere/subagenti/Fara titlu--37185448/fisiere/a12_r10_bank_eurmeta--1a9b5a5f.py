from a12_r10_lease import *
q="""set search_path=adempiere,pg_catalog;
select ad_client_id,c_acctschema_id,c_currency_id from c_acctschema where ad_client_id=11 order by 2;
select c_currency_id,iso_code from c_currency where iso_code in('RON','EUR','USD');
select c_conversiontype_id,ad_client_id,isdefault from c_conversiontype where isdefault='Y' and ad_client_id in(0,11) order by 2 desc;
select c_conversion_rate_id,c_conversiontype_id,c_currency_id,c_currency_id_to from c_conversion_rate order by c_conversion_rate_id limit 2;
select count(*) from c_bankstatementline where c_bankstatementline_id=987610001;
select column_name from information_schema.columns where table_schema='adempiere'and table_name='c_conversion_rate' order by ordinal_position;"""
w=current();s='cd '+w+' && c=$(cat auditor-pg) && test "$(docker inspect -f \'{{index .Config.Labels "eva.sesiune"}}\' "$c")" = eva-contab-codex-p01a12r10t06 && docker exec -i "$c" sh -c \'exec psql -XqAt -U "$POSTGRES_USER" -d idempiere\' <<\'SQL\'\nBEGIN READ ONLY;\n'+q+'\nROLLBACK;\nSQL';r=ssh(s);print(r.stdout.decode()[-1300:],r.stderr.decode()[-150:])
