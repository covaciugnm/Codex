from pathlib import Path
import sys,types,runpy,json,contextlib,io
sys.modules["psycopg"]=types.ModuleType("psycopg") # stub solely for import; no DB calls
src=Path("D:/CodexWork/eva-audit-p01-readonly-20261102/backend/saga-migration/recon/recon.py")
core=runpy.run_path(str(src))["Recon"]
class Fixture(core):
 def __init__(self,source,target):
  self.schema="fixture";self.cid=101;self.rows=[];self.notes=[];self.source=source;self.target=target
 def _tbl(self,n):return n in self.source
 def sq(self,sql):return self.source[sql.split('"."')[1].split('"')[0]]
 def iq(self,sql,p=None):return self.target
def run(name,source,target):
 f=Fixture(source,target);cap=io.StringIO()
 with contextlib.redirect_stdout(cap): f.invoices()
 return dict(case=name,source_rows=sum(map(len,source.values())),erp_invoice_rows=len(target),reported=f.rows,raw_output=cap.getvalue())
cases=[
 run("control",{"INTRARI":[("N1",1,100,100,0)]},[("N1",100)]),
 run("sales_and_purchase_same_no_only_purchase_exists",{"IESIRI":[("N1",1,20,20,0)],"INTRARI":[("N1",2,100,100,0)]},[("N1",100)]),
 run("credit_sign_reversed",{"INTRARI":[("N1",2,-100,-100,0)]},[("N1",100)]),
 run("leeway_0.99",{"INTRARI":[("N1",1,100,100,0)]},[("N1",100.99)]),
 run("different_amount",{"INTRARI":[("N1",1,100,100,0)]},[("N1",110)])]
print(json.dumps(cases,ensure_ascii=False,indent=2))
