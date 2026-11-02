import json,sys,os,tempfile,hashlib
from pathlib import Path
from datetime import datetime,timezone
base=Path("D:/CodexWork/eva-audit-p01-readonly-20261102");work=Path(tempfile.mkdtemp(prefix="a04-r3-interface-"));sys.dont_write_bytecode=True;sys.path[:0]=[str(base/"backend"),"D:/CodexWork/eva-a01-fixture-deps"]
os.environ["EVA_DATABASE_URL"]="sqlite:///"+str(work/"syn.db").replace("\\","/");os.environ["EVA_JWT_SECRET"]="A04-fictitious-sandbox-only-123456789"
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.db import Base,engine,SessionLocal
from app import models
from app.errors import EvaError,eva_error_handler
from app.routers import saga_import as mod
Base.metadata.create_all(engine);app=FastAPI();app.include_router(mod.router);app.add_exception_handler(EvaError,eva_error_handler)
contexts={'role-a':{'tenant_cui':'SYN-A','ad_client_id':101,'ad_org_id':11,'actor':'role-a'},'role-b':{'tenant_cui':'SYN-B','ad_client_id':102,'ad_org_id':22,'actor':'role-b'}}
real=mod._require_ctx
def identity(request,db):
 key=request.headers.get("x-r3-fixture-role");return contexts[key] if key in contexts else real(request,db)
mod._require_ctx=identity
with SessionLocal() as db:
 j=models.EvaSagaImportJob(tenant_cui='SYN-A',ad_client_id=101,ad_org_id=11,mode='dry-run',status='dry_run_valid',filename='A_ONLY_FIXTURE.zip',storage_path='/test',sha256='f'*64);db.add(j);db.commit();jid=j.job_id
client=TestClient(app)
out=[]
for label,method,target,headers,expected in [('own-job','GET',f'/saga/import/jobs/{jid}',{'X-R3-Fixture-Role':'role-a'},200),('other-tenant','GET',f'/saga/import/jobs/{jid}',{'X-R3-Fixture-Role':'role-b'},404),('missing','GET',f'/saga/import/jobs/{jid+50}',{'X-R3-Fixture-Role':'role-a'},404),('no-context','GET',f'/saga/import/jobs/{jid}',{},None),('apply-no-approved-run','POST','/saga/import/run',{'X-R3-Fixture-Role':'role-a','X-Idempotency-Key':'r3-a04-at-least-16'},423)]:
 resp=client.request(method,target,headers=headers,**({'files':{'file':('placeholder.zip',b'unopened fixture','application/zip')}} if method=='POST' else {}));data=resp.json()
 if expected:assert resp.status_code==expected,(label,resp.status_code,data)
 if label=='no-context':assert resp.status_code in (400,401,403)
 assert label=='own-job' or 'A_ONLY_FIXTURE.zip' not in resp.text
 out.append({'case':label,'method':method,'url':target,'expected':expected,'observed_http':resp.status_code,'body':data})
with SessionLocal() as db: assert db.query(models.EvaSagaImportJob).count()==1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
probe={'utc':datetime.now(timezone.utc).isoformat(),'cutoff':'6df998aee0e514d30856c461962afe99ebd0d113','git_file':'backend/app/routers/saga_import.py','git_file_sha256':sha(base/'backend/app/routers/saga_import.py'),'runtime':'local ASGI/FastAPI with synthetic SQLite and explicit identity adapter for two positive contexts, actual auth path for missing header. No ERP writes, no external calls. Tests job row scoping and run gate AFTER identity resolution; does not validate authentication provider or production route.','initial_jobs':1,'final_jobs':1,'results':out}
outp=Path(__file__).parent/'roluri_job_gate.json';outp.write_text(json.dumps(probe,indent=2,ensure_ascii=False),encoding='utf8');print([(x['case'],x['observed_http']) for x in out])
