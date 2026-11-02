from a12_r3_survey import *
import collections,subprocess as sp
r4=E/'R4';rows=rd(r4/'Registru_1868.json')['records'];look=collections.defaultdict(set);syms=set()
for w in rows:
 tx=w['scope_from_task']+' '+w['expected_verbatim'];tokens=set(re.findall(r'\b(?:EVA|AD|M|C|GL|I|PP)_[A-Za-z][A-Za-z0-9_]{2,68}\b',tx,re.I))
 for t in tokens:
  tt=t.lower()
  if tt.startswith(('eVa_'.lower(),'m_','c_','gl_','ad_','pp_','i_')):look[w['criterion']].add(tt);syms.add(tt)
if not syms:raise ValueError('no IDs')
parts=','.join("'"+s+"'"for s in sorted(syms))
q=f"""BEGIN READ ONLY; SET LOCAL search_path=adempiere,pg_catalog;SET LOCAL statement_timeout='18s';
WITH n(val) AS (SELECT unnest(ARRAY[{parts}])) SELECT json_build_object('symbol',n.val,'tables',(select count(*) from ad_table t where lower(t.tablename)=n.val and t.isactive='Y'),'physical',(select count(*) from information_schema.tables a where a.table_schema='adempiere' and lower(a.table_name)=n.val),'columns',(SELECT coalesce(json_agg(q.tablename),'[]'::json) FROM (select distinct t.tablename from ad_column c join ad_table t using(ad_table_id) where c.isactive='Y' and lower(c.columnname)=n.val order by t.tablename limit 15)q),'processes',(select coalesce(json_agg(p.ad_process_id),'[]'::json) from ad_process p where lower(p.value)=n.val and p.isactive='Y'),'sysconfig_count',(select count(*) from ad_sysconfig a where lower(a.name)=n.val and a.isactive='Y')) FROM n order by n.val;ROLLBACK;"""
p=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','docker exec -i eva-postgres-cesiro psql -X -qAt -v ON_ERROR_STOP=1 -U adempiere -d idempiere'],input=q.encode(),stdout=sp.PIPE,stderr=sp.PIPE,timeout=29);assert p.returncode==0,p.stderr.decode(errors='replace')[:200];values={s['symbol']:s for s in [json.loads(x)for x in p.stdout.decode().splitlines() if x.startswith('{')]};assert set(values)==syms
o=r4/'probe/AD_nominal_criterii.json';wr(o,{'db':'CESIRO idempiere/adempiere','mode':'BEGIN READ ONLY; nici o înregistrare comercială sau valoare configurată citită. Se verifică tabela activă AD, tabela fizică, coloanele numite (limita de 15 tabele), procesul AD și numai numărul de setări. Tabele/coloane și procese nu sunt dovezi de executare a funcției.','sql_sha256':hashlib.sha256(q.encode()).hexdigest(),'symbols':values,'criterion_exact_names':{c:sorted(v)for c,v in look.items()},'count':len(values),'associated_individual_criteria':len(look)})
print('AD',len(values),'criteria',len(look))

