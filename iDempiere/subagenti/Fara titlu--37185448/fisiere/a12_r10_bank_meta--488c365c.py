from a12_r10_lease import *
w=current()
s='''cd SCR && test -f auditor-pg && c=$(cat auditor-pg) && test "$(docker inspect -f '{{index .Config.Labels "eva.sesiune"}}' "$c")" = eva-contab-codex-p01a12r10t06 && docker exec -i "$c" sh -c 'exec psql -XqAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d idempiere' <<'SQL'
BEGIN READ ONLY;
select table_name,string_agg(column_name,',' order by ordinal_position) from information_schema.columns where table_schema='adempiere' and table_name in ('ad_pinstance_log','eva_comparatiebanca','c_bankstatement','c_bankstatementline') group by table_name order by table_name;
ROLLBACK;
SQL'''.replace('SCR',w)
p=ssh(s);print(p.returncode,p.stdout.decode('utf8','replace')[:3200],p.stderr.decode('utf8','replace')[:200])
