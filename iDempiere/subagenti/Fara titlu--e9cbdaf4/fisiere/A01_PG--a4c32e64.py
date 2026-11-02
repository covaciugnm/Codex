import pathlib,os,uuid,subprocess,sys,tempfile,json,hashlib
O=pathlib.Path(__file__).parent;E=O.parent;root=pathlib.Path('D:/CodexWork/p01-local-pg16');pg=root/'pgsql/bin/psql.exe';env={**os.environ,'PGPASSFILE':str(root/'pgpass.conf')};name='a11r2_'+uuid.uuid4().hex[:12]
def sql(db,s):
 p=subprocess.run([str(pg),'-X','-qAt','-v','ON_ERROR_STOP=1','-h','127.0.0.1','-p','56481','-U','audit_owner','-d',db,'-c',s],capture_output=True,env=env,timeout=20);assert p.returncode==0,'private PG command failed';return p.stdout.decode().strip()
assert sql('postgres',"select count(*) from pg_database where datname='"+name+"'")=='0' and name.isidentifier()
sql('postgres','CREATE DATABASE '+name)
try:
 text=(E/'A01/a01_probe.py').read_text(encoding='utf8');h=text[:text.index("request('T01'")];h=h.replace('from app.main import app',"os.environ['EVA_DATABASE_URL']='postgresql+psycopg://audit_owner@127.0.0.1:56481/"+name+"'\nfrom app.main import app");h=h.replace('Base.metadata.create_all(engine);',"from sqlalchemy import text\nwith engine.begin() as dbsetup: dbsetup.execute(text('create table eva_idempiere_client_map (tenant_cui text, managing_uuid text, idempiere_client_id integer)'))\nBase.metadata.create_all(engine);")
 owned=(E/'A11_reproduceri_lot1/a11_p0_independent.py').read_text(encoding='utf8').split('cases=[]',1)[1]
 with tempfile.TemporaryDirectory(prefix='a11-zone-pg-') as t:
  work=pathlib.Path(t);script=work/'trace.py';script.write_text("import hashlib,json\n"+h+"\nOUT=pathlib.Path("+repr(str(O))+"); h="+repr(h)+"\ncases=[]"+owned.replace("OUT/'A01_P0_independent.json'","OUT/'A01_P0_PG_native.json'"),encoding='utf8');out=subprocess.run([sys.executable,'-B',str(script)],env={**env,'A01_OUTPUT':str(work)},capture_output=True,timeout=100);assert out.returncode==0,out.stderr.decode('utf8','replace')[-900:]
  ob=json.loads((O/'A01_P0_PG_native.json').read_text(encoding='utf8'));assert len(ob['cases'])==4 and ob['cases'][0]['observed'][0]==201 and ob['cases'][1]['observed']==[403,False,201,True,1] and ob['cases'][2]['observed']['canary_read_by_A'] and ob['cases'][3]['observed']==[200,200,401,200,401]
finally: sql('postgres','DROP DATABASE '+name)
ob['scope']='A11 repeated independent synthetic ASGI variant now on actual PostgreSQL 16 loopback DB isolated from ERP, distinct from the portal client-cache experiment; no exploit on production claimed.';ob['cleanup_db']=sql('postgres',"select count(*) from pg_database where datname='"+name+"'")=='0';assert ob['cleanup_db']; (O/'A01_P0_PG_native.json').write_text(json.dumps(ob,ensure_ascii=False,indent=2),encoding='utf8');print([x['id'] for x in ob['cases']],ob['cleanup_db'])

