"""Reproduce F05 via the shipped FastAPI dry-run handler; isolate identity, ERP target readiness and capabilities."""
import io,json,zipfile,tempfile,warnings,struct,sys,os,hashlib,socket
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace
root=Path(__file__).parent
work=Path(tempfile.mkdtemp(prefix="a04r2-zip-"))
base=Path("D:/CodexWork/eva-audit-p01-readonly-20261102")
sys.dont_write_bytecode=True
sys.path[:0]=[str(base/"backend"),"D:/CodexWork/eva-a01-fixture-deps"]
os.environ["EVA_DATABASE_URL"]="sqlite:///"+str(work/"audit.db").replace("\\","/")
os.environ["EVA_OFFICE_STORAGE"]=str(work/"office")
os.environ["IDEMPIERE_MOCK"]="1"
os.environ["EVA_JWT_SECRET"]="fixture-only-never-used-for-access-1234567890"
def firewall(event,args):
 if event in ("socket.connect","socket.bind") and len(args)>1 and isinstance(args[1],tuple) and args[1][0] not in ("127.0.0.1","::1","localhost"):raise RuntimeError("outbound blocked")
sys.addaudithook(firewall)
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from app.db import Base,engine,SessionLocal
from app import models
from app.errors import EvaError
from app.routers import saga_import as mod
from app.idempiere import readdb
os.environ["EVA_REGISTRU_SEED"]=str(base/"idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/fiscal/ParametriModel.java")
from tests import registru_t159
readdb.registru_de_test(registru_t159.incarca_seed())
Base.metadata.create_all(engine)
mod._STATE_DIR=str(work/"state")
mod._require_ctx=lambda request,db:{"ad_client_id":11,"ad_org_id":11,"idempiere_role_id":102,"warehouse_id":103,"tenant_cui":"AUDIT-SYNTH","actor":"fixture"}
mod._target_preflight=lambda ctx:{"ok":True,"origin":"synthetic target"}
class Client:
 def upsert_bpartner(self,*a,**k):raise AssertionError("preview wrote")
 update_bpartner=create_account=create_product=create_invoice=complete_invoice=create_bp_location=post_gl_journal=upsert_bpartner
mod._build_client=lambda ctx:Client()
reports=[]
real_migration=mod._run_migration
def capture_report(**kwargs):
 out=real_migration(**kwargs);reports.append(out);return out
mod._run_migration=capture_report
linux_comparator="--linux-glob" in sys.argv
if linux_comparator:
 import glob,fnmatch
 normal_glob=glob.glob
 def case_sensitive_glob(pattern,*args,**kwargs):
  if pattern.endswith(("*.dbf","*.DBF","*.xml","*.XML")):
   parent,mask=os.path.split(pattern);return [os.path.join(parent,name) for name in os.listdir(parent) if fnmatch.fnmatchcase(name,mask)] if os.path.isdir(parent) else []
  return normal_glob(pattern,*args,**kwargs)
 glob.glob=case_sensitive_glob
app=FastAPI()
@app.exception_handler(EvaError)
async def handle(request,e):
 return JSONResponse(status_code=e.status_code,content={"code":e.code,"message":str(e),"details":e.details})
app.include_router(mod.router)
def dbf(code,name):
 fields=[("COD",12,code),("DENUMIRE",32,name),("CIF",12,"")];hlen=32+32*len(fields)+1; rlen=1+sum(x[1] for x in fields)
 h=bytearray(32);h[0:4]=bytes((3,126,11,2));struct.pack_into("<IHH",h,4,1,hlen,rlen)
 for key,size,_ in fields:
  b=bytearray(32);b[:len(key)]=key.encode();b[11]=ord("C");b[16]=size;h+=b
 return bytes(h)+b"\r "+b"".join(val.encode("ascii").ljust(size) for _,size,val in fields)+b"\x1a"
def pack(entries):
 b=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter("ignore")
  with zipfile.ZipFile(b,"w") as z:
   for n,v in entries:z.writestr(n,v)
 return b.getvalue()
a=dbf("R2-A","Synthetic A");b=dbf("R2-B","Synthetic B")
routes=[r.path for r in app.routes if hasattr(r,"path") and r.path.endswith("/dry-run")]
client=TestClient(app,raise_server_exceptions=False)
cases=[]
for k,entries in [("control-two-distinct", [("CLIENTI_A.DBF",a),("CLIENTI_B.DBF",b)]),("duplicate", [("CLIENTI.DBF",a),("CLIENTI.DBF",b)]),("traversal",[("../CLIENTI.DBF",a)])]:
 payload=pack(entries);resp=client.post("/saga/import/dry-run",files={"file":("test.zip",payload,"application/zip")});data=resp.json() if "json" in resp.headers.get("content-type","") else {"text":resp.text[:1300]}
 with SessionLocal() as db:
  alljobs=db.query(models.EvaSagaImportJob).order_by(models.EvaSagaImportJob.job_id).all()
  selected=next((j for j in alljobs if j.job_id==(data.get("job_id") or (data.get("details") or {}).get("job_id"))),None)
 cases.append({"case":k,"input_rows":len(entries),"archive_sha256":hashlib.sha256(payload).hexdigest(),"http":resp.status_code,"job":data.get("job_id"),"code":data.get("code"),"details":data.get("details"),"text":data.get("text"),"status":selected.status if selected else None,"summary":selected.entity_summary if selected else {},"manifest":(data.get("upload") or {}).get("files_manifest"),"report_entities":(data.get("report") or (reports[-1] if selected and reports else {})).get("entities")})
out={"linux_comparator":linux_comparator,"glob_note":"On Windows, emulate Linux case-sensitive pattern matches if true. Host result preserved independently.","id":"A04-R2-ZIP-HTTP","utc":datetime.now(timezone.utc).isoformat(),"sha":"6df998aee0e514d30856c461962afe99ebd0d113","route":"POST /saga/import/dry-run (FastAPI ASGI TestClient with real router, multipart ZIP, real reader, validator, migration and SQLite job storage)","adapters":"Synthetic authenticated context, target availability and capability methods, fiscal registry from pinned ParametriModel test seed; no ERP document, external account or network accessed.","cases":cases}
(root/"zip-http.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf8")
print([(t["case"],t["http"],t["status"],t["code"],t["text"],(t["summary"].get("partner") or {}).get("total")) for t in cases])






