from a03_r8_jvm import *
def main():
 b=root/'backend';tmp=work/'pytest-utf8';tmp.mkdir(exist_ok=True);env=dict(os.environ,PYTHONPATH=str(P('D:/CodexWork/eva-a01-fixture-deps'))+os.pathsep+str(b),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',IDEMPIERE_MOCK='1',EVA_REGISTRU_SEED=str(plug/'src/com/eva/ro/contab/fiscal/ParametriModel.java'),PYTHONIOENCODING='utf8',EVA_ACTE_DIR=str(tmp/'acts'),TMP=str(tmp),TEMP=str(tmp))
 code="""import sys,socket
orig=socket.socket.connect
def forbid(self,address):
 if self.family in (socket.AF_INET,socket.AF_INET6): raise RuntimeError('Network prohibited in test')
 return orig(self,address)
def internal_pair(*args,**kwargs):
 with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as l:
  l.bind(('127.0.0.1',0));l.listen(1);r=socket.socket(socket.AF_INET,socket.SOCK_STREAM);orig(r,l.getsockname());v,addr=l.accept();return v,r
socket.socketpair=internal_pair
socket.socket.connect=forbid
import pytest
sys.exit(pytest.main(sys.argv[1:]))"""
 xml=tmp/'result.xml';rr=sp.run([sys.executable,'-X','utf8','-B','-c',code,'--tb=short','-q','-p','no:cacheprovider','--junitxml',xml,'tests/test_t58_close_month.py'],env=env,cwd=b,capture_output=True,timeout=240)
 b0=rr.stdout+rr.stderr;f=out/'log/pytest-T58-utf8.txt';f.write_bytes(b0);res=[]
 for i in ET.parse(xml).iter('testcase'):
  errors=[(child.tag,child.attrib.get('message','')[:130]) for child in i if child.tag in ('failure','error','skipped')];res.append({'name':i.attrib.get('name'),'status':errors or 'ok'})
 J(out/'T58_pytest_utf8.json',{'utc':UTC(),'repo_sha':sha,'rc':rr.returncode,'source_sha256':H((b/'tests/test_t58_close_month.py').read_bytes()),'results':res,'log_sha256':H(b0),'log':str(f.relative_to(out)),'test_environment':'UTF8. Windows asyncio internal socketpair bound only to 127.0.0.1 via an ephemeral loopback listener. Application sockets blocked both by runner and by unchanged original fixture. No call to any cabinet. The portal scenarios come from the same fixture and use a fake proxy.'});print(rr.returncode,sum(r['status']=='ok' for r in res),len(res),[r['name'] for r in res if r['status']!='ok'])
if __name__=='__main__':main()

