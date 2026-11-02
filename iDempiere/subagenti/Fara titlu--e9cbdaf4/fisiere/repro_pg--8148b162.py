from pathlib import Path
import subprocess,json,tempfile,socket,threading
O=Path(__file__).parent;B=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');D=Path(tempfile.mkdtemp(prefix='a11-pg-r7-'));S=subprocess.CREATE_NO_WINDOW
def run(*args):
 if Path(args[0]).name=='pg_ctl.exe':
  with tempfile.TemporaryFile() as os, tempfile.TemporaryFile() as es:
   proc=subprocess.run([str(x)for x in args],stdout=os,stderr=es,creationflags=S,timeout=45);os.seek(0);es.seek(0);proc.stdout=os.read().decode('utf8',errors='replace');proc.stderr=es.read().decode('utf8',errors='replace');return proc
 return subprocess.run([str(x)for x in args],capture_output=True,encoding='utf8',errors='replace',creationflags=S,timeout=30)
def ok(p):assert not p.returncode,(p.stdout[-800:],p.stderr[-800:])
with socket.socket()as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
ok(run(B/'initdb.exe','-D',D/'data','-A','trust','--encoding=UTF8','--no-locale','-U','a11_fixture','--no-sync'))
ok(run(B/'pg_ctl.exe','-D',D/'data','-o',f'-p {port} -h 127.0.0.1','-l',D/'server.log','-w','start'))
cmd=[str(B/'psql.exe'),'-XAt','-h','127.0.0.1','-p',str(port),'-U','a11_fixture','-d','postgres','-v','ON_ERROR_STOP=1']
def sql(s):p=run(*cmd,'-c',s);ok(p);return p.stdout.strip()
try:
 sql('create table witness(id integer not null)');rows=[]
 for k,(a,b,release,skip) in enumerate([(11202610,11202610,'commit',False),(11202610,11202611,'commit',False),(11202610,12202610,'commit',False),(11202610,11202610,'rollback',False),(11202610,11202610,'commit',True)]):
  sql('truncate witness');holder=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1,creationflags=S)
  def send(st):holder.stdin.write(st+'\n');holder.stdin.flush()
  send(f'BEGIN; SELECT 1 FROM (SELECT pg_advisory_xact_lock({a})) x; INSERT INTO witness VALUES(1); SELECT \'A11_READY\';')
  seen=[]
  while True:
   line=holder.stdout.readline().strip()
   if line=='A11_READY':break
   seen.append(line)
   if holder.poll() is not None:raise RuntimeError('unexpected holder exit')
  got=sql(f"BEGIN; SELECT pg_try_advisory_xact_lock({b}); ROLLBACK;").splitlines()[1]=='t'
  if skip:done=sql('BEGIN; INSERT INTO witness VALUES(2);COMMIT;');pre=int(sql('select count(*) from witness'))
  else:pre=int(sql('select count(*) from witness'))
  send(release+';');send(r'\q');holder.stdin.close();holder.wait(timeout=10);assert holder.returncode==0
  if not skip:sql(f'BEGIN; SELECT 1 FROM (SELECT pg_advisory_xact_lock({b})) x; INSERT INTO witness VALUES(2); COMMIT;')
  cnt=int(sql('select count(*) from witness'));assert got==(a!=b) and cnt==(1 if release=='rollback'else 2)
  rows.append(dict(holder_key=a,second_key=b,release=release,bypass=skip,can_take_before_release=got,committed_rows_visible_before_release=pre,rows_after=cnt))
 out={'server_version':sql('show server_version'),'SQL':'SELECT 1 FROM (SELECT pg_advisory_xact_lock(key)) x','new_ephemeral_pg_dir':str(D),'network':'loopback unique temporary port','tests':rows,'scope':'Reproducere independentă a literalului nativ în PostgreSQL cu două sesiuni; fără efect contabil și fără a atinge cabinetul ori serviciul local P01.'}
finally:ok(run(B/'pg_ctl.exe','-D',D/'data','-m','fast','-w','stop'))
out['cluster_stopped']=True;(O/'PG_advisory_independent.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(rows)

