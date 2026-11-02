from a12_r10_base import *
import subprocess,os,tempfile,uuid,sys
repo=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');backend=repo/'backend';dest=P10/'T210_auth';dest.mkdir(exist_ok=True);work=Path('D:/CodexWork/a12-r10-local');work.mkdir(exist_ok=True)
runner='''from pathlib import Path
import os,sys,socket
sys.dont_write_bytecode=True
base=Path(sys.argv[1]);mode=sys.argv[2]
sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(base)]
import inspect,ipaddress
native_connect=socket.socket.connect
native_connect_ex=socket.socket.connect_ex
def guard(fn):
 def safe(sock,addr):
  ip=addr[0] if isinstance(addr,tuple)else ""
  try:loop=ipaddress.ip_address(ip).is_loopback
  except ValueError:loop=False
  if loop and any(fr.function in ("_fallback_socketpair","socketpair","_make_self_pipe")for fr in inspect.stack()):return fn(sock,addr)
  raise AssertionError("real socket forbidden in R10")
 return safe
socket.socket.connect=guard(native_connect);socket.socket.connect_ex=guard(native_connect_ex)
import pytest
class Plugin:
 def pytest_collection_modifyitems(self,config,items):
  if mode=='mutant':
   from app import middleware
   middleware._PUBLIC_SUFFIXES=(*middleware._PUBLIC_SUFFIXES,"/baselinker/push-order","/baselinker/call")
  print("COLLECTED="+str(len(items)))
 def pytest_sessionfinish(self,session,exitstatus):print("FINAL_RESULT="+str(session.testscollected)+"/"+str(session.testsfailed)+" RC="+str(exitstatus))
sys.exit(pytest.main(["-vv","-p","no:cacheprovider","--tb=line",str(base/"tests/test_t28_baselinker_auth.py")],plugins=[Plugin()]))
'''
def run():
 script=dest/'court_sans_reseau.py';script.write_text(runner,encoding='utf8');rr=[]
 with tempfile.TemporaryDirectory(prefix='t210r10-',dir=work)as t:
  for mode in ('original','mutant'):
   env=dict(os.environ,TEMP=t,TMP=t,IDEMPIERE_MOCK='1',BASELINKER_WRITE_ENABLED='0',PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',EVA_REGISTRU_SEED=str(repo/'idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/fiscal/ParametriModel.java'))
   p=subprocess.run([sys.executable,'-B','-X','utf8',str(script),str(backend),mode],cwd=backend,env=env,capture_output=True,timeout=90);fo=dest/(mode+'.log');fo.write_bytes(p.stdout+p.stderr);ss=(p.stdout+p.stderr).decode('utf8','replace').splitlines();rr.append({'variant':mode,'exit':p.returncode,'log':source(fo),'per_test': [{'line':i,'node':v.split('::')[-1].split()[0],'result':re.search(r'\b(PASSED|FAILED|ERROR|SKIPPED)\b',v)[1]}for i,v in enumerate(ss,1)if '::test_t28_'in v and re.search(r'\b(PASSED|FAILED|ERROR|SKIPPED)\b',v)and not v.startswith(('FAILED','ERROR'))],'summary':[v for v in ss if 'FINAL_RESULT='in v or 'COLLECTED='in v or v.startswith('ERROR:')or 'ImportError' in v or 'ModuleNotFoundError:'in v][-8:]})
 f=P10/'T210_auth_original_et_mutant.json';wr(f,{'utc':now(),'criteria':['T210-R2-001','T210-R2-003','T210-R2-004','T210-R2-005'],'primary_blob':{n:sha(repo/n)for n in ['backend/tests/test_t28_baselinker_auth.py','backend/tests/conftest.py','backend/app/middleware.py','backend/app/routers/idempiere_ui.py']},'runner':source(script),'rows':rr,'oracle':'9/9 suite originale, push-order și call refuză actorul anonim 401 și 0 apeluri. Martor pozitiv autentificat cu scriere dezactivată și respingerea unui token invalid.','limit':'TestClient ASGI, SQLite sintetic și filtrele TestClient. Garda rețelei în proces înlocuiește conectarea socket reală. Nu este un transfer live BaseLinker, o mutare a rutelor în plugin sau un test Docker --network none.'});print(sha(f),[(v['variant'],v['exit'],v['summary'])for v in rr])
if __name__=='__main__':run()

