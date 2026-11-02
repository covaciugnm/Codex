from a03_r8_base import *
import xml.etree.ElementTree as ET
root=P('D:/CodexWork/eva-audit-p01-readonly-20261102');plug=root/'idempiere/plugins/com.eva.ro.contab';saga=root/'idempiere/plugins/com.eva.ro.saga.native'; sec=P('D:/CodexWork/eva-audit-secondary-20261102');jdk=P('C:/Program Files/Java/jdk-21/bin');policy=P('D:/CodexWork/p01-r5-jvm/limited-logging3.policy')
def jvm():
 names=['TestT156MutareCont','TestT254EroriInchidere','TestT186Utilitar','TestT186Propagare','TestT186PropagareLB','TestT186CatchGoale','TestPornireContab','TestT29ImportSetari','TestT03Lot5','TestT159LotD','TestA83Butoane']
 sg=work/'git-saga.jar'; sgf=ssh('cd '+repo+' && git ls-tree -r --name-only '+sha+' | grep -E "com.eva.ro.saga.native[^/]*[.]jar$" | head -1').stdout.decode().strip();print(sgf,flush=True);sg.write_bytes(get(sgf))
 for lab,n in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
  cls=work/lab;cls.mkdir(exist_ok=True);cp=os.pathsep.join(str(p) for p in [cls,P('D:/CodexWork/a03-r4-runtime')/lab,sec/n,sg,sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',P('D:/CodexWork/a05-support-jars/*'),P('D:/CodexWork/eva-a01-java/lib/*'),plug/'src',saga/'src']);res=[]
  for name in names:
   pp=(saga if name=='TestT29ImportSetari' else plug);f=pp/'test'/(name+'.java')
   if not f.exists():continue
   aa=[jdk/'javac.exe','-proc:none','-encoding','UTF-8','-sourcepath','','-cp',cp,'-d',cls,f];z=sp.run(aa,capture_output=True,cwd=pp)
   b=z.stdout+z.stderr;rc=z.returncode
   if rc==0:
    try:q=sp.run([jdk/'java.exe','-Xmx512m','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dfile.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-cp',cp,name],cwd=pp,capture_output=True,timeout=65);b=q.stdout+q.stderr;rc=q.returncode
    except sp.TimeoutExpired:rc=124;b=b'time limit'
   full=out/'log'/(lab+'-'+name+'.txt');full.parent.mkdir(exist_ok=True);full.write_bytes(b);text=b.decode('utf8',errors='replace').splitlines()
   res.append({'test':name,'test_sha256':H(f.read_bytes()),'compile_rc':z.returncode,'rc':rc,'raw':str(full.relative_to(out)),'raw_sha256':H(b),'summary':[x for x in text if 'T254-' in x or 'REZULTAT' in x or 'RESULT' in x or 'FAIL' in x][-13:]});print(lab,name,rc,str(res[-1]['summary'][-1:])[:180],flush=True)
   J(out/('JVM_'+lab+'.json'),{'utc':UTC(),'sha':sha,'contab_jar':n,'contab_sha256':H((sec/n).read_bytes()),'saga_jar_repo':sgf,'saga_jar_sha256':H(sg.read_bytes()),'policy_sha256':H(policy.read_bytes()),'results':res})
def pytest():
 b=root/'backend';tests=['test_t58_close_month.py','test_t32_l6j_rute.py','test_t32_l6h_citiri.py','test_error_catalog.py'];tmp=work/'pytest';tmp.mkdir(exist_ok=True);env=dict(os.environ,PYTHONPATH=str(P('D:/CodexWork/eva-a01-fixture-deps'))+os.pathsep+str(b),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',IDEMPIERE_MOCK='1',EVA_REGISTRU_SEED=str(plug/'src/com/eva/ro/contab/fiscal/ParametriModel.java'),PYTHONIOENCODING='utf8',EVA_ACTE_DIR=str(tmp/'acts'),TMP=str(tmp),TEMP=str(tmp))
 if os.environ.get('A03_ONLY_T58')=='1':tests=tests[:1]
 code='import sys,socket; orig=socket.socket.connect\ndef forbid(self,address):\n if self.family in (socket.AF_INET,socket.AF_INET6): raise RuntimeError("Network prohibited in R8 local fixture")\n return orig(self,address)\nsocket.socket.connect=forbid\nimport pytest; sys.exit(pytest.main(sys.argv[1:]))';x=tmp/'result.xml'
 r=sp.run([sys.executable,'-B','-c',code,'-q','-p','no:cacheprovider','--junitxml',x]+['tests/'+t for t in tests],cwd=b,env=env,capture_output=True,timeout=160); bb=r.stdout+r.stderr;log=out/'log/pytest-T58.txt';log.parent.mkdir(exist_ok=True);log.write_bytes(bb);rs=[]
 if x.exists():
  for item in ET.parse(x).iter('testcase'):rs.append({'name':item.attrib.get('name'),'class':item.attrib.get('classname'),'status':'ok' if not len(item) else [c.tag for c in item]})
 print('pytest',r.returncode,bb[-900:].decode('utf8',errors='replace'),flush=True);J(out/'T58_pytest.json',{'utc':UTC(),'sha':sha,'raw_sha256':H(bb),'raw':str(log.relative_to(out)),'rc':r.returncode,'files':{f:H((b/'tests'/f).read_bytes()) for f in tests},'results':rs,'limit':'SQLite temporaire, tenant_context du conftest simulé et ERP simulé. Interdiction technique d’accès IP. Pas de session du cabinet.'})
if __name__=='__main__':globals()[sys.argv[1]]()

