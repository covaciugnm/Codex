from a12_r10_base import *
from a12_r8_jvm import java,sec,plug,base,execute
import os,tempfile,socket,subprocess as sp,shutil,time
from pathlib import Path
pg=Path('D:/CodexWork/p01-local-pg16/pgsql/bin');bk=Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump');tmp=Path(tempfile.mkdtemp(prefix='a12-r10-pg-',dir='D:/CodexWork'));home=tmp/'data';db='a12_native_r10';nativebin=Path('D:/CodexWork/a12-r10-local/jvm');dest=P10/'PG201';dest.mkdir(exist_ok=True)
def call(cmd,t=120,env=None):return sp.run(list(map(str,cmd)),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=t,env=env,creationflags=getattr(sp,'CREATE_NO_WINDOW',0))
s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close();basecmd=['-h','127.0.0.1','-p',str(port),'-U','adempiere'];en={**os.environ,'PGCLIENTENCODING':'UTF8'};meta={'at':now(),'cutoff':BASE,'sink':'Dedicated loopback PostgreSQL 16; empty temporary cluster, GardenWorld-A07 source, no production.','archive_sha256':sha(bk),'attempts':[]}
def execpg(cmd,tag,t=100):
 v=call(cmd,t,en);out=v.stdout+v.stderr;path=dest/(tag+'.log');path.write_text(out[-8000:],encoding='utf8');meta['attempts'].append({'stage':tag,'exit':v.returncode,'stdout_tail_source':source(path)});return v
try:
 q=execpg([pg/'initdb.exe','--no-sync','--encoding=UTF8','--locale=C','-U','adempiere','-A','trust','-D',home],'init');assert q.returncode==0,q.stderr[-600:]
 q=execpg([pg/'pg_ctl.exe','-D',home,'-l',tmp/'pg.log','-o','-h 127.0.0.1 -p '+str(port)+' -c fsync=off -c shared_buffers=64MB -c synchronous_commit=off','-w','start'],'start');assert q.returncode==0,q.stderr[-640:]
 q=execpg([pg/'createdb.exe',*basecmd,db],'createdb');assert q.returncode==0
 q=execpg([pg/'pg_restore.exe',*basecmd,'--no-owner','--no-acl','-j','3','-d',db,bk],'restore',400)
 print('restored',q.returncode,q.stderr[-900:],flush=True)
 gate=execpg([pg/'psql.exe',*basecmd,'-AtXq','-d',db,'-c',"set search_path=adempiere,pg_catalog;select string_agg(t::text,',') from unnest(array[to_regclass('eva_seriiplaje'),to_regclass('eva_registrucorespondenta'),to_regclass('eva_registrucontrol')]) as s(t);select count(*) from pg_trigger where tgname='eva_registrufirma_protectie'and not tgisinternal;select count(*) from ad_client where ad_client_id not in (0,11);"],'catalog')
 assert gate.returncode==0 and 'eva_registrucorespondenta'in gate.stdout and '\n2\n'in gate.stdout,repr(gate.stdout)
 cls='com.eva.ro.contab.documente.TestT201Registre';src=plug/'test/TestT201Registre.java';import re;pkg=re.search(r'^package ([\w.]+);',src.read_text(encoding='utf8'),re.M);cls=(pkg[1]+'.'if pkg else'')+'TestT201Registre'
 for tag in ['git','instalat']:
  jar=sec/('cod-master-contab.jar'if tag=='git'else'com.eva.ro.contab_13.0.0.jar');dd=nativebin/(tag+'_TestT201Registre');cp=';'.join(map(str,[dd,jar,base,next(sec.glob('org.adempiere.base.process_*.jar')),'D:/CodexWork/a12-r6-preprobes/deps/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',plug/'src']))
  for mode in ['', '--fara-blocare','--alta-trx','--fara-trigger']:
   arc=execpg([java/'java.exe','-Xmx220m','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,cls,'--clona','jdbc:postgresql://127.0.0.1:'+str(port)+'/'+db,'11',*([mode]if mode else[])],tag+'_'+(mode.removeprefix('--')or'normal'),40)
   print(tag,mode or'base',arc.returncode,arc.stdout[-190:],arc.stderr[-160:],flush=True)
   meta.setdefault('scenarios',[]).append({'jar':tag,'jar_sha256':sha(jar),'test_sha256':sha(src),'driver':cls,'mode':mode or'original','exit':arc.returncode,'markers':[t.strip()for t in arc.stdout.splitlines()if re.search(r'^\s*(OK|FAIL)',t)],'log':source(dest/(tag+'_'+(mode.removeprefix('--')or'normal')+'.log'))})
finally:
 if (home/'postmaster.pid').exists():v=execpg([pg/'pg_ctl.exe','-D',home,'-m','fast','-w','stop'],'stop')
 meta['cleanup']={'process_released':not(home/'postmaster.pid').exists(),'kept_db':False if not(home/'postmaster.pid').exists()else True}
 if not(home/'postmaster.pid').exists()and tmp.resolve().parent==Path('D:/CodexWork').resolve()and tmp.name.startswith('a12-r10-pg-'):shutil.rmtree(tmp)
 f=P10/'T201_PG16_two_writers.json';wr(f,meta);print('artifact',sha(f),flush=True)

