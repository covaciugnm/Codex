from a03_r8_base import *
import secrets
pg=P('D:/CodexWork/p01-local-pg16');env=dict(os.environ,PGPASSFILE=str(pg/'pgpass.conf'),PGCLIENTENCODING='UTF8')
def run(sql,db='postgres'):
 return sp.run([str(pg/'pgsql/bin/psql.exe'),'-X','-v','ON_ERROR_STOP=1','-A','-F','|','-h','127.0.0.1','-p','56481','-U','audit_owner','-d',db],env=env,input=sql,capture_output=True,cwd=work)
def execute():
 db='p01_a03r8_'+secrets.token_hex(5)
 assert re.fullmatch('p01_a03r8_[0-9a-f]{10}',db)
 cr=run(('CREATE DATABASE '+db+' TEMPLATE template0 ENCODING \'UTF8\';').encode());assert cr.returncode==0,cr.stderr
 try:
  src=path('T256','dovezi-02-plan/mutanti_sql_fixturi.sql');s=get(src); rr=run(s,db)
  assert rr.returncode==0,rr.stderr
  lines=rr.stdout.decode('utf8').splitlines()
  product=[x for x in lines if x.startswith('PROD ')];mutants=[x for x in lines if '|ROSU|' in x or '|SUPRAVIETUITOR|' in x]
  check=run(b"set search_path=f; select current_database(),current_setting('server_version'),count(*),count(distinct ad_client_id) from f.c_invoice; select * from f.nr('PROD',false,'PR_V%-','SAGA ',2,'2026-10-01','2026-10-31 23:59:59');",db);assert check.returncode==0,check.stderr
  a={'utc':UTC(),'fixed_sha':sha,'source':src,'source_sha256':H(s),'engine':check.stdout.decode(),'reproduction':'psql -X -v ON_ERROR_STOP=1 in a new isolated UTF8 audit database created from template0. Fixture internally drops/creates f only there; full source unmodified.','rc':rr.returncode,'stdout':lines,'stderr':rr.stderr.decode('utf8',errors='replace'),'product_rows':product,'mutations':mutants}
 finally:
  cl=run(('DROP DATABASE '+db+';').encode());assert cl.returncode==0
 a['released']=cl.stdout.decode().strip();a['database']=db
 J(out/'T256_SQL.json',a);print(a['engine'],product,len(mutants),a['released'])
if __name__=='__main__':execute()

