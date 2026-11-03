from pathlib import Path
import os, sys, json, hashlib, socket, subprocess, tempfile, shutil, ast, inspect, collections, datetime

BASE=Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\R11_fisiere')
OUT=BASE/'Control_harness_root'
ROOT=BASE/'Suite_originale_API_portal_v7'
CHILD=Path('D:/CodexWork/p01-r11-test-isolated-child-v7.py')
RUNNER=Path('D:/CodexWork/p01-r11-original-suites-v7.py')
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
OUT.mkdir(exist_ok=True)
assert not (OUT/'Peer_A01_harness_v7.json').exists()
receipt=json.loads((ROOT/'Rezultate_suite_originale.json').read_text('utf8'))
assert H(ROOT/'Rezultate_suite_originale.json')=='737446e418f77f0e7acc1173782585fa3e91d88e25f1806c2ef5303192e56617'
assert H(CHILD)==H(ROOT/CHILD.name)==receipt['runner_sha256']
assert H(RUNNER)==H(ROOT/'Runner_coordonare.py')
assert H(ROOT/'Surse_izolate_Git.json')==receipt['manifest_sha256']
stdlib_source=inspect.getsource(socket.socketpair)
assert stdlib_source.count('csock.connect((addr, port))')==1
adapted=stdlib_source.replace('csock.connect((addr, port))','_r11_original_connect(csock,(addr,port))')
assert 'ssock.getsockname() != csock.getpeername()' in adapted
assert 'csock.getsockname() != ssock.getpeername()' in adapted

WITNESS=r'''
from pathlib import Path
import os,sys,json,socket,inspect,types,asyncio,subprocess,sqlite3
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

rows=[]
def check(name,action,expect=None):
    try:
        value=action()
    except BaseException as ex:
        if expect is None or not isinstance(ex,expect):raise
        rows.append({'id':name,'ok':True,'exception':type(ex).__name__,'detail':str(ex)[:180]})
    else:
        if expect:raise AssertionError(name+' did not refuse')
        rows.append({'id':name,'ok':True,'value':value})

native=socket.socket.connect
def connect(addr,ex=False):
    with socket.socket() as s:
        s.settimeout(.5)
        return s.connect_ex(addr) if ex else native(s,addr)
def bind(addr):
    with socket.socket() as s:s.bind(addr)
def sendto():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:s.sendto(b'SYNTHETIC',('127.0.0.1',int(os.environ['A01_PARENT_PORT'])))
check('connect_parent_process_listener',lambda:connect(('127.0.0.1',int(os.environ['A01_PARENT_PORT']))),PermissionError)
check('connect_documentation_nonlocal',lambda:connect(('192.0.2.1',9)),PermissionError)
check('connect_ex_documentation_nonlocal',lambda:connect(('192.0.2.1',9),True),PermissionError)
check('dns_nonlocal',lambda:socket.getaddrinfo('a01.example.invalid',443),PermissionError)
check('bind_nonloopback',lambda:bind(('0.0.0.0',0)),PermissionError)
check('bind_fixed_port',lambda:bind(('127.0.0.1',int(os.environ['A01_PARENT_PORT']))),PermissionError)
check('udp_sendto',sendto,PermissionError)
check('subprocess',lambda:subprocess.Popen([sys.executable,'-c','raise AssertionError("must never execute")']),PermissionError)
outside=Path(os.environ['A01_OUTSIDE_CANARY'])
check('write_outside_fixture',lambda:outside.write_text('ALTERED'),PermissionError)
check('remove_outside_fixture',lambda:outside.unlink(),PermissionError)
check('rename_outside_fixture',lambda:outside.rename(outside.with_suffix('.moved')),PermissionError)
inside=Path(os.environ['EVA_FIXTURE_DIR'])/'inside_canary.txt'
check('write_inside_fixture',lambda:inside.write_text('SYNTHETIC',encoding='utf8'))

def self_listener():
    with socket.socket() as server:
        server.bind(('127.0.0.1',0));server.listen(1)
        with socket.socket() as client:
            native(client,server.getsockname())
            accepted,peer=server.accept()
            with accepted:
                client.sendall(b'SELF');value=accepted.recv(4)
                assert value==b'SELF'
                assert client.getsockname()==accepted.getpeername()
    return 'same-process ephemeral loopback explicitly allowed'
check('same_process_ephemeral',self_listener)

original_source=Path(os.environ['A01_STDLIB_SOURCE']).read_text('utf8')
ns=dict(socket.__dict__);exec(compile(original_source,'<original-stdlib>','exec'),ns)
original_pair=ns['_fallback_socketpair']
guard_calls=[]
def garda(self,addr):
    guard_calls.append(addr)
    raise ConnectionRefusedError('T32 witness: network forbidden')
socket.socket.connect=garda
try:
    check('unadapted_original_breaks_under_test_monkeypatch',lambda:original_pair(),ConnectionRefusedError)
    before=len(guard_calls)
    def echo_pair():
        left,right=socket.socketpair()
        try:
            left.sendall(b'PAIR');assert right.recv(4)==b'PAIR'
            right.sendall(b'BACK');assert left.recv(4)==b'BACK'
            assert left.getsockname()==right.getpeername()
            assert left.getpeername()==right.getsockname()
        finally:left.close();right.close()
        assert left.fileno()==right.fileno()==-1
        assert len(guard_calls)==before
        return 'bidirectional echo and peer identities; monkeypatch not invoked'
    check('adapted_pair_under_test_monkeypatch',echo_pair)
    with socket.socket() as application_socket:
        check('ordinary_app_connect_still_monkeypatched',lambda:application_socket.connect(('127.0.0.1',1)),ConnectionRefusedError)
    def asgi_under_guard():
        app=FastAPI()
        @app.get('/synthetic')
        async def synthetic():return {'proof':'synthetic_asgi_only'}
        with TestClient(app) as client:
            r=client.get('/synthetic');assert r.status_code==200
            assert r.json()=={'proof':'synthetic_asgi_only'}
        return {'status':r.status_code,'body':r.json()}
    check('fastapi_testclient_real_asyncio_with_guard',asgi_under_guard)
finally:socket.socket.connect=native

# Run the actual adapter code object against contradictory socket doubles.
objects=[]
class FakeSocket:
    def __init__(self,*args):self.number=len(objects);self.closed=False;objects.append(self)
    def bind(self,addr):pass
    def listen(self):pass
    def setblocking(self,arg):pass
    def getsockname(self):return ('127.0.0.1',10000+self.number)
    def getpeername(self):return ('127.0.0.1',20000+self.number)
    def accept(self):return FakeSocket(),('127.0.0.1',20001)
    def close(self):self.closed=True
ns=dict(socket.socketpair.__globals__);ns['socket']=FakeSocket;ns['_r11_original_connect']=lambda obj,addr:None
contradictory=types.FunctionType(socket.socketpair.__code__,ns,argdefs=socket.socketpair.__defaults__)
check('contradictory_peer_identity_rejected',lambda:contradictory(),ConnectionError)
assert len(objects)==3 and all(o.closed for o in objects)
rows.append({'id':'contradictory_peer_handles_closed','ok':True,'value':len(objects)})

def sqlite_pragmas():
    engine=create_engine('sqlite:///'+(Path(os.environ['EVA_FIXTURE_DIR'])/'fixture.sqlite').as_posix())
    try:
        with engine.connect() as conn:
            got=[conn.exec_driver_sql('PRAGMA journal_mode').scalar(),conn.exec_driver_sql('PRAGMA synchronous').scalar()]
            assert got==['memory',0]
    finally:engine.dispose()
    return got
check('sqlite_pragmas_fixture',sqlite_pragmas)
Path(os.environ['A01_PEER_RESULT']).write_text(json.dumps({'checks':rows,'guard_calls':len(guard_calls)}),encoding='utf8')
'''

with tempfile.TemporaryDirectory(prefix='a01-r11-harness-peer-',dir='D:/CodexWork') as td:
    w=Path(td);fixture=w/'fixture';fixture.mkdir();(fixture/'scratch').mkdir()
    outside=w/'synthetic_outside_canary.txt';outside.write_text('UNCHANGED_SYNTHETIC')
    original_hash=H(outside)
    (fixture/'peer_witness.py').write_text(WITNESS,encoding='utf8')
    (fixture/'stdlib_socketpair.py').write_text(stdlib_source,encoding='utf8')
    with socket.socket() as parent:
        parent.bind(('127.0.0.1',0));parent.listen(2);parent.settimeout(.1)
        env={k:os.environ[k] for k in ('SYSTEMROOT','WINDIR','COMSPEC','PATHEXT','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE') if k in os.environ}
        env.update(PATH=str(Path(sys.executable).parent)+';'+env.get('SYSTEMROOT','C:/Windows')+'/System32',TEMP=str(fixture/'scratch'),TMP=str(fixture/'scratch'),TMPDIR=str(fixture/'scratch'),HOME=str(fixture),USERPROFILE=str(fixture),EVA_FIXTURE_DIR=str(fixture),EVA_FIXTURE_RESULT=str(fixture/'child_receipt.json'),PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf8',PYTHONSAFEPATH='1',IDEMPIERE_MOCK='1',EVA_DATABASE_URL='sqlite:///'+(fixture/'fixture.sqlite').as_posix(),A01_PARENT_PORT=str(parent.getsockname()[1]),A01_OUTSIDE_CANARY=str(outside),A01_PEER_RESULT=str(fixture/'peer_checks.json'),A01_STDLIB_SOURCE=str(fixture/'stdlib_socketpair.py'))
        p=subprocess.run([sys.executable,'-I',str(CHILD),'main','peer_witness.py'],cwd=fixture,env=env,capture_output=True,timeout=60)
        (OUT/'peer_witness_execution.log').write_bytes(p.stdout+b'\n'+p.stderr)
        assert p.returncode==0,(p.returncode,p.stderr.decode('utf8','replace'))
        accepted=0
        try:
            c,_=parent.accept();c.close();accepted+=1
        except TimeoutError:pass
        assert accepted==0 and H(outside)==original_hash
    shutil.copyfile(fixture/'peer_witness.py',OUT/'peer_witness.py')
    shutil.copyfile(fixture/'stdlib_socketpair.py',OUT/'stdlib_socketpair.py')
    for name in ('peer_checks.json','child_receipt.json'):shutil.copyfile(fixture/name,OUT/name)
    checks=json.loads((fixture/'peer_checks.json').read_text('utf8'))
    child_receipt=json.loads((fixture/'child_receipt.json').read_text('utf8'))
    assert all(row['ok'] for row in checks['checks'])
assert not w.exists()

per_suite=[];totals=collections.Counter()
for row in receipt['rows']:
    stages=collections.Counter((c['stage'],c['outcome']) for c in row.get('cases',[]))
    totals.update(stages)
    per_suite.append({'file':row['file'],'exit':row['exit'],'pytest_call_passed':stages[('call','passed')],'pytest_call_failed':stages[('call','failed')],'pytest_setup_teardown_nonpass':sum(v for (stage,status),v in stages.items() if stage!='call'),'source_sha256':row['source_sha256'],'git_blob':row['git_blob'],'original_receipt_only':True})
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A01','scope':'Independent limited peer review of root V7 isolation adapter and receipt, not a new execution of 55 original suites. Historical A01 report and root seals not modified.','head':receipt['head'],'gate_sha256':receipt['gate'],'root_receipt_sha256':H(ROOT/'Rezultate_suite_originale.json'),'root_child_sha256':H(CHILD),'root_runner_sha256':H(RUNNER),'root_sources_manifest_sha256':receipt['manifest_sha256'],'independent_result':'ACCEPTED_WITH_EXPLICIT_LIMITS','independent_checks':len(checks['checks']),'all_independent_checks_passed':True,'outside_canary_unchanged':True,'parent_process_listener_connections':0,'temporary_fixture_removed':True,'adapter_static':{'replacement_occurrences':1,'source_sha256':hashlib.sha256(stdlib_source.encode()).hexdigest(),'peer_comparisons_preserved':True,'code_object_peer_counterexample_passed':True},'receipt_summary':{'original_source_files':len(per_suite),'exit_zero':sum(x['exit']==0 for x in per_suite),'exit_nonzero':sum(x['exit']!=0 for x in per_suite),'pytest_stage_counts':[{'stage':a,'outcome':b,'count':n} for (a,b),n in sorted(totals.items())],'per_file':per_suite},'acceptance':[
'The exact child adapter preserves the original tests socket.socket.connect monkeypatch for ordinary application calls; real FastAPI TestClient on Windows operates with the patched self-pair.',
'The single standard-library self-pair connection uses captured original connect; CPython audit hook remains active. Contradictory peer sockets are rejected and closed.',
'Nonlocal connects/connect_ex, another process loopback listener, nonlocal DNS, arbitrary bind, UDP sendto, subprocess and writes/removal/rename outside fixture were refused by independent negative controls.',
'Same-process ephemeral loopback is explicitly permitted by the audit policy. It is not an external ERP connection.',
'Root receipt and exact child/runner/source-manifest hashes were independently verified; 55 source receipts are received with 42 exits zero and 13 nonzero, not 55 passed suites.'
], 'limits':[
'This is cooperative CPython audit-hook containment for these trusted inspected tests, not an OS security sandbox or a proof against hostile Python/native ctypes code. Reads outside fixture are not forbidden. Third-party native libraries and all possible filesystem/network primitives were not exhaustively audited.',
'The child hook permits any connect to a still-bound loopback socket that the same process opened on port zero, not solely socketpair. This explicit allowance is independently verified; ordinary socket.connect monkeypatch remains effective.',
'Captured fallback resolves socket factory from a copied namespace, so later monkeypatches of socket.socket itself would not affect self-pair creation. Reviewed T32 tests patch the connect method; no assertion of equivalence for other monkeypatch patterns.',
'backend/tests/conftest.py globally stubs authoritative tenant_context using X-Tenant-Cui with a fixed verified manager/org and mocks ERP. These suite successes cannot prove real JWT, user/tenant binding, native RBAC or live database isolation.',
'T32 read suite explicitly accepts 500 after successful authorization entry. Its pass is guard/route coverage, not successful end-to-end ERP reads.',
'SQLite journal_mode MEMORY and synchronous OFF change durability/concurrency semantics; accepted only for disposable synthetic fixture. PostgreSQL, crashes, fsync, native transactions and deployment behavior remain unproven.',
'55 sources are a selected suite list, not all backend/frontend files or all test suites. Storefront main programs are not individual pytest assertions.',
'Nonzero results include missing adjacent frontend fixture/data files, refused PostgreSQL access and genuine assertion mismatches requiring classification by domain owners. No blanket product defect or all-pass conclusion is justified.',
'This review independently reruns 21 focused adapter/IO controls, not the 55 suites; original suite outcome records are authenticated root evidence.'
]}
record['limits'][-1]=record['limits'][-1].replace('21',str(len(checks['checks'])))
(OUT/'Peer_A01_harness_v7.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copyfile(Path(__file__),OUT/'reproduce_peer.py')
files=[{'file':f.name,'sha256':H(f),'bytes':f.stat().st_size} for f in sorted(OUT.iterdir()) if f.is_file() and f.name!='Manifest_peer_A01.json']
(OUT/'Manifest_peer_A01.json').write_text(json.dumps({'reviewer':'A01','root_receipt_sha256':record['root_receipt_sha256'],'files':files},indent=2),encoding='utf8')
print(json.dumps({'report_sha256':H(OUT/'Peer_A01_harness_v7.json'),'manifest_sha256':H(OUT/'Manifest_peer_A01.json'),'independent_checks':len(checks['checks']),'result':record['independent_result'],'counts':record['receipt_summary']['pytest_stage_counts']},ensure_ascii=True))
