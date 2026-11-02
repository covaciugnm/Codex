from a12_r11x_java import *
import time,tempfile,socket,shutil
home0=Path('D:/CodexWork'); pg=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');bk=Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump'); temp=Path(tempfile.mkdtemp(prefix='a12-r11-db-',dir=home0)); pgdata=temp/'data';db='r11_a12_garden';dest=A/'pg';dest.mkdir(exist_ok=True); steps=[]
with socket.socket()as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
ep=['-h','127.0.0.1','-p',str(port),'-U','adempiere'];en={**os.environ,'PGCLIENTENCODING':'UTF8'}
def run(tag,args,timeout=130):
 oo=temp/(tag+'.out');ee=temp/(tag+'.err')
 with oo.open('wb')as out1,ee.open('wb')as err1: ret=sp.run([str(x)for x in args],stdout=out1,stderr=err1,env=en,timeout=timeout,creationflags=getattr(sp,'CREATE_NO_WINDOW',0)).returncode
 stdout=oo.read_text(encoding='utf8',errors='replace');stderr=ee.read_text(encoding='utf8',errors='replace');log=dest/(tag+'.log');log.write_text(stdout+stderr,encoding='utf8');x={'tag':tag,'exit':ret,'log':ref(log),'assertions':[{'line':i,'text':r.strip()}for i,r in enumerate((stdout+stderr).splitlines(),1)if re.search(r'^\s*(OK|FAIL|REZULTAT)',r)]};steps.append(x);print(tag,ret,stdout[-100:].strip(),flush=True);return ret,stdout
def sql(tag,q):
 return run(tag,[pg/'psql.exe',*ep,'-AtXq','-v','ON_ERROR_STOP=1','-d',db,'-c','SET search_path=adempiere,pg_catalog; '+q])
term_sql="""SELECT 'AD_clients='||string_agg(ad_client_id::text,',' ORDER BY ad_client_id) FROM ad_client;SELECT 'tables='||count(*) FROM pg_tables WHERE schemaname='adempiere'; SELECT 'protection_triggers='||count(*) FROM pg_trigger WHERE tgname='eva_registrufirma_protectie' AND NOT tgisinternal; SELECT 'register_rows='||(SELECT count(*) from eva_registrucorespondenta)||','||(SELECT count(*) from eva_registrucontrol)||','||(SELECT count(*) from eva_seriiplaje);"""
try:
 assert run('00_init',[pg/'initdb.exe','--no-sync','--encoding=UTF8','--locale=C','-U','adempiere','-A','trust','-D',pgdata])[0]==0
 assert run('01_start',[pg/'pg_ctl.exe','-D',pgdata,'-l',temp/'pg.log','-o','-h 127.0.0.1 -p '+str(port)+' -c fsync=off -c shared_buffers=56MB -c synchronous_commit=off','-w','start'])[0]==0 
 assert run('02_create',[pg/'createdb.exe',*ep,db])[0]==0 
 restore=run('03_restore',[pg/'pg_restore.exe',*ep,'--no-owner','--no-acl','-j','3','-d',db,bk],400)
 assert restore[0]==0
 rc,before=sql('04_baseline',term_sql);assert rc==0 and 'AD_clients=0,11' in before and 'protection_triggers=2'in before
 name='TestT201Registre';fq='com.eva.ro.contab.documente.'+name
 for target,j in [('candidate',jar),('mounted_copy',scratch/'cesiro-contab.jar')]:
  clsdir=scratch/(target+'_'+name)
  for i in range(110):
   if j.is_file()and (clsdir/(fq.replace('.','/')+'.class')).is_file():break
   time.sleep(1)
  assert j.is_file()and (clsdir/(fq.replace('.','/')+'.class')).is_file()
  for mode in [None,'--fara-blocare','--alta-trx','--fara-trigger']:
   label=target+'_'+(mode[2:]if mode else'normal'); prog=[java/'java.exe','-Xmx210m','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp(clsdir,j),fq,'--clona','jdbc:postgresql://127.0.0.1:'+str(port)+'/'+db,'11'];
   if mode:prog.append(mode)
   run(label,prog,60);sql('after_'+label,term_sql)
 rc,after=sql('05_final',term_sql);assert rc==0
finally:
 if (pgdata/'postmaster.pid').exists():run('06_stop',[pg/'pg_ctl.exe','-D',pgdata,'-m','fast','-w','stop'])
 stopped=not(pgdata/'postmaster.pid').exists();rm=False
 if stopped and temp.resolve().parent==home0.resolve()and temp.name.startswith('a12-r11-db-'):
  shutil.rmtree(temp);rm=True
 f=A/'T201_DB_registre_doua_sesiuni.json'; save(f,{'utc':now(),'head':head,'gate':ref(gate),'origin':'Freshly restored synthetic GardenWorld backup, dedicated PostgreSQL16 loopback, only System/GardenWorld; candidate Java test, candidate and current mounted-copy bundles. No operational DB modified.','source_git':d['idempiere/plugins/com.eva.ro.contab/test/TestT201Registre.java'],'input_backup_sha256':sha(bk),'fixture':'two simultaneous SQL writers x 20, rollback/retry, same transaction, guards for delete and mutations by exact names','preflight':before if 'before'in locals() else None,'post':after if 'after'in locals()else None,'steps':steps,'cleanup':{'cluster_stopped':stopped,'temp_removed':rm},'limitations':'True PostgreSQL and compiled application allocator. Synthetic client11, DBA fixture, no desktop entry or ERP actor permissions. Mutant invocations are counterfactual controls, not bugs of unaltered runtime.'});print(ref(f),flush=True)

