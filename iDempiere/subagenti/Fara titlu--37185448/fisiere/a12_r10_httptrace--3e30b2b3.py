from a12_r10_auth import *
import ast
trace=r'''import httpx,json
trace=[]
default_send=httpx.Client.send
def traced(self,request,*args,**kw):
 resp=default_send(self,request,*args,**kw)
 if "/baselinker/" in request.url.path:
  b=resp.json();er=b.get("error")if isinstance(b,dict)else None
  trace.append({"method":request.method,"path":request.url.path,"accepts_auth_header":"authorization" in request.headers,"status":resp.status_code,"error_code":er.get("code")if isinstance(er,dict)else None})
 return resp
httpx.Client.send=traced
'''
def probe():
 ss=runner.replace('import pytest',trace+'\nimport pytest').replace('print("FINAL_RESULT="+str(session.testscollected)+"/"+str(session.testsfailed)+" RC="+str(exitstatus))','print("FINAL_RESULT="+str(session.testscollected)+"/"+str(session.testsfailed)+" RC="+str(exitstatus));print("NETWORK_TRACE="+json.dumps(trace))')
 script=dest/'trace_uniquement_ASGI.py';script.write_text(ss,encoding='utf8');rs=[]
 with tempfile.TemporaryDirectory(prefix='r10http-',dir=work)as tp:
  for mode in ('original','mutant'):
   env=dict(os.environ,TEMP=tp,TMP=tp,IDEMPIERE_MOCK='1',BASELINKER_WRITE_ENABLED='0',EVA_REGISTRU_SEED=str(repo/'idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/fiscal/ParametriModel.java'),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
   p=subprocess.run([sys.executable,'-B','-X','utf8',str(script),str(backend),mode],cwd=backend,env=env,capture_output=True,timeout=120);fp=dest/(mode+'_trace.log');fp.write_bytes(p.stdout+p.stderr);ls=(p.stdout+p.stderr).decode('utf8','replace').splitlines();lines=[(i,v)for i,v in enumerate(ls,1)if 'NETWORK_TRACE='in v];assert lines,(mode,ls[-4:]);off,ln=lines[-1];arr=json.loads(ln.split('NETWORK_TRACE=')[1]);rs.append({'mode':mode,'exit':p.returncode,'trace':arr,'primary_log':source(fp),'line':off})
 py=repo/'backend/app/routers/idempiere_ui.py';tr=ast.parse(py.read_text(encoding='utf8'));urls=[]
 for n in ast.walk(tr):
  if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
  for de in n.decorator_list:
   if isinstance(de,ast.Call)and isinstance(de.func,ast.Attribute)and de.args and isinstance(de.args[0],ast.Constant)and 'baselinker/'in str(de.args[0].value):urls.append({'func':n.name,'method':de.func.attr.upper(),'path':de.args[0].value,'line':de.lineno})
 out=P10/'T210_auth_trace_routes.json';wr(out,{'utc':now(),'source':str(py.relative_to(repo).as_posix()),'source_sha':sha(py),'routes_in_target_router':urls,'replays':rs,'observed_scope':'Transportul este HTTP in-process TestClient fără conexiune la partener; nu înlocuiește verificarea unei mutări la plugin sau a contului extern real.'});print(sha(out),[(r['mode'],r['exit'],len(r['trace']))for r in rs])
if __name__=='__main__':probe()

