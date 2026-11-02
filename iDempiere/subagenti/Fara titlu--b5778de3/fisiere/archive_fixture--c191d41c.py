from pathlib import Path
import sys, os, tempfile, zipfile, json, warnings, hashlib, socket
from contextlib import redirect_stdout
sys.dont_write_bytecode=True
def deny(*args,**kw):raise RuntimeError("external networking prohibited in A04 fixture")
socket.socket.connect=deny
socket.create_connection=deny
tmp=tempfile.TemporaryDirectory(prefix="eva-a04-archive-")
folder=Path(tmp.name)
os.environ["DATABASE_URL"]="sqlite:///"+str(folder/"synthetic.db").replace("\\","/")
os.environ["SAGA_IMPORT_STATE_DIR"]=str(folder/"state")
base=Path("D:/CodexWork/eva-audit-p01-readonly-20261102")
sys.path[:0]=[str(base/"backend"),"D:/CodexWork/eva-a01-fixture-deps"]
from app.routers import saga_import as mod
def run(n,members):
 p=folder/(n+".zip");dest=folder/(n+"-output");dest.mkdir()
 with warnings.catch_warnings():
  warnings.simplefilter("ignore")
  with zipfile.ZipFile(p,"w") as archive:
   for path,data in members:archive.writestr(path,data)
 try:
  class Upload:
   filename=p.name
   content_type="application/zip"
   async def read(self):return p.read_bytes()
  coro=mod._materialize_source(Upload(),str(dest))
  try:coro.send(None)
  except StopIteration as done:meta=done.value
  else:raise AssertionError("unexpected external await")
  m=meta["manifest"]; integrity=mod._assert_archive_integrity(meta); extract=dest/"extracted"; result={"outcome":"ACCEPTED","integrity_ok":integrity["ok"],"duplicate_basenames":integrity["duplicate_basenames"],"manifest_names":[r["name"] for r in m],"files":[{"name":x.name,"bytes":x.stat().st_size,"sha256":hashlib.sha256(x.read_bytes()).hexdigest()} for x in extract.rglob("*") if x.is_file()]}
 except Exception as ex:result={"outcome":"REJECTED","exception":type(ex).__name__,"code":getattr(ex,"code",None)}
 return {"id":n, "input_count":len(members),"result":result}
r=[run("normal",[("CLIENTI.DBF",b"abc")]),run("traversal",[("../OUT.DBF",b"xyz")]),run("duplicate-name",[("CLIENTI.DBF",b"first"),("CLIENTI.DBF",b"second")]),run("duplicate-alias",[("a/b/CLIENTI.DBF",b"first"),("a/b/./CLIENTI.DBF",b"second")])]
print(json.dumps(r,ensure_ascii=True,indent=2))
