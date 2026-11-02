from a12_r9_orig import *
import socket,tempfile,secrets,os,sys
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
pgb=Path('D:/CodexWork/p01-local-pg16/pgsql/bin')
def t():
 with tempfile.TemporaryDirectory(prefix='a12r9det-',dir=R9L) as tmpname:
  temp=Path(tmpname);data=temp/'data';pf=temp/'secret';secret=secrets.token_hex(32);pf.write_text(secret+'\n')
  def proc(ar,timeout=48):return subprocess.run([str(z)for z in ar],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL,timeout=timeout)
  with socket.socket()as ss:ss.bind(('127.0.0.1',0));port=ss.getsockname()[1]
  r=proc([pgb/'initdb.exe','-D',data,'-U','a12_r9','--encoding=UTF8','--locale=C','--auth=scram-sha-256','--pwfile='+str(pf)]);assert r.returncode==0;pf.unlink();r=proc([pgb/'pg_ctl.exe','-D',data,'-l',temp/'log','-o','-h 127.0.0.1 -p '+str(port),'start','-w']);assert r.returncode==0
  ck=None
  try:
   ck=psycopg.connect(host='127.0.0.1',port=port,user='a12_r9',dbname='postgres',password=secret,autocommit=True)
   def sq(s,params=None):return ck.execute(s,params)
   sq('create table eva_comandasite(eva_comandasite_id integer primary key, ad_client_id integer, c_order_id integer,c_invoice_id integer,eva_starelegare text,eva_blocatlinie char(1))');sq('create table eva_comandasitelinie(eva_comandasite_id integer,ad_client_id integer,c_invoice_id integer)')
   sq("insert into eva_comandasite select i,11,i+1000,null,'NELEGAT','N' from generate_series(1,16) i");sq('insert into eva_comandasitelinie select i,11,i+10000 from generate_series(1,16)i')
   sq("insert into eva_comandasite values(20,11,100,0,'LEGAT_MANUAL','N'),(21,11,101,0,'STINS','N'),(22,11,102,0,'NELEGAT','Y'),(23,11,0,0,'NELEGAT','N'),(24,11,104,null,'NELEGAT','N'),(25,11,105,228,'NELEGAT','N'),(26,11,106,0,'NELEGAT','N'),(27,12,107,0,'NELEGAT','N')")
   sq('insert into eva_comandasitelinie values(20,11,200),(21,11,201),(22,11,202),(23,11,203),(24,11,null),(25,11,228),(26,12,206),(27,12,207)')
   fn='tools/teste/t220/detectie_k12.sh';oid,buf=getp(fn);s=buf.decode();literal=s.split("<<'SQL'\n")[1].split('\nSQL')[0];qml=literal.split('BEGIN READ ONLY;')[1].split('ROLLBACK;')[0].strip()
   def read():
    sq('BEGIN READ ONLY')
    try:return [x[0]for x in sq(qml).fetchall()]
    finally:sq('ROLLBACK')
   a=read();sq('update eva_comandasite set c_invoice_id=eva_comandasite_id+10000 where ad_client_id=11 and eva_comandasite_id between 1 and 16');b=read();sq('update eva_comandasite set c_invoice_id=0 where eva_comandasite_id=1');m=read();assert a==['k12|11|16','k12|12|1','k12|total|17'];assert b==['k12|11|0','k12|12|1','k12|total|1'];assert m==['k12|11|1','k12|12|1','k12|total|2']
   result={'utc':now(),'criterion':'T220-R2-015','source':{'commit':BASE,'file':fn,'oid':oid,'query_sha':hashlib.sha256(qml.encode()).hexdigest(),'query_literal':qml},'engine':sq('select version()').fetchone()[0],'seeded_conditions':'16 antete în firma A cu linii facturate și antet nelegat; 1 în B. Controale A: legată manual/stinsă/blocată/c_order_id=0/linie fără factură/factură deja corectă/linie doar în B.','expected_before_A':16,'observed_before':a,'expected_after_A':0,'observed_after':b,'single_header_mutated_again':m,'rule':'Exclude manual, stins, blocat, fără comandă sau fără linii eligibile din aceeași firmă; martorul B trebuie să rămână la 1.','qualification':'S-a executat detectorul exact al proiectului. Repararea celor 16 antete este un UPDATE explicit în fixture, nu executarea Corelez pe produs și nu o citire a cabinetelor reale.'}
  finally:
   if ck is not None:ck.close()
   r=proc([pgb/'pg_ctl.exe','-D',data,'-m','fast','stop','-w']);assert r.returncode==0
  f=P9/'T220_detector_PG.json';wr(f,result);print(sha(f),a,b,m)
if __name__=='__main__':t()

