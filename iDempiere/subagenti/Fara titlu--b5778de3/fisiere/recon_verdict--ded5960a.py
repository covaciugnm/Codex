from pathlib import Path
import json,runpy,sys,types,contextlib,io
sys.modules["psycopg"]=types.ModuleType("psycopg")
src=Path("D:/CodexWork/eva-audit-p01-readonly-20261102/backend/saga-migration/recon/recon.py")
Core=runpy.run_path(str(src))["Recon"]
class F(Core):
 def __init__(self,n,raise_error):
  self.schema="fixture";self.cid=101;self.ccode="F";self.rows=[];self.notes=[];self.n=n;self.raise_error=raise_error
 def partners(self):
  if self.raise_error:raise RuntimeError("fixture read failed")
  self._emit("PARTENERI",self.n,0,0,{str(i) for i in range(self.n)})
 def other(self):pass
 products=accounts=invoices=payments=assets=employees=other
 def gl_money(self):self.gl_balanced=True
out=[]
for n,b in [(0,False),(1,False),(100,False),(101,False),(0,True)]:
 f=F(n,b);s=io.StringIO()
 with contextlib.redirect_stdout(s):f.run()
 txt=s.getvalue()
 out.append({"missing_rows_fixture":n,"forced_source_error":b,"printed_error":"fixture read failed" in txt,"printed_complete":"DATE COMPLETE" in txt,"observed_tail":txt.split("VERDICT")[-1]})
print(json.dumps(out,ensure_ascii=True,indent=2))
