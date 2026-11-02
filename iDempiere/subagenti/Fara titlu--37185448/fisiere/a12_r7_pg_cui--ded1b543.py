from a12_r6_exec import *
import sqlite3,uuid
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
T7=Path('D:/CodexWork/a12-r7');RP=E/'R7_pregatire/A12';RP.mkdir(exist_ok=True,parents=True);os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf'
def db(n,a=False):return psycopg.connect(host='127.0.0.1',port=56481,user='audit_owner',dbname=n,autocommit=a,connect_timeout=5)
def cui(in9):
 assert len(in9)==9 and in9.isdecimal()
 k=(sum(int(x)*int(y)for x,y in zip(in9,'753217532'))*10)%11
 return in9+str(k%10)
A,B=cui('980000041'),cui('980000052')
src=plug/'src/com/eva/ro/contab/banca/CititorArhivaSaga.java';cols={a:re.findall('"([A-Z_]+)"',b)for a,b in re.findall(r'COLOANE\.put\("([A-Z_]+)", List\.of\((.*?)\)\)',src.read_text(encoding='utf8'),re.S)};assert len(cols)==7
def data(filename,cui_):
 f=T7/filename;assert not f.exists()
 with sqlite3.connect(f)as c:
  for t,l in cols.items():c.execute('create table '+t+' ('+','.join(k+' text'for k in l)+')')
  c.execute('create table SOCIET (CODF_S text)');c.execute('insert into SOCIET values(?)',(cui_,));c.commit()
 return f
javas='''package com.eva.ro.contab.banca; import java.nio.file.Path;
public class CUIOracleA12 { public static void main(String[] args) throws Exception {try(CititorArhivaSaga a=new CititorArhivaSaga(Path.of(args[0]))){try{a.verificaFirma(args[1]);System.out.println("MATCH");}catch(IllegalStateException e){System.out.println("REFUZ="+e.getMessage());}}}}'''
if __name__=='__main__':
 dbn='a12_r7cui_'+uuid.uuid4().hex[:12];assert re.fullmatch(r'a12_r7cui_[a-f0-9]{12}',dbn)
 with db('postgres',True)as conn:conn.execute('create database '+dbn+' template p01_garden')
 try:
  with db(dbn)as conn:
   initial=conn.execute('select oi.ad_org_id,oi.taxid is not null from adempiere.ad_orginfo oi join adempiere.ad_org o on o.ad_org_id=oi.ad_org_id where o.ad_client_id=11 order by oi.ad_org_id').fetchall()
   assert initial;conn.execute('update adempiere.ad_orginfo set taxid=%s where ad_org_id=%s',('RO'+A,initial[0][0]));verified=conn.execute('select oi.taxid from adempiere.ad_orginfo oi join adempiere.ad_org o on o.ad_org_id=oi.ad_org_id where o.ad_client_id=11 and oi.taxid is not null order by oi.ad_org_id limit 1').fetchone()[0];assert verified=='RO'+A
  out=[];p=T7/'CUIOracleA12.java';p.write_text(javas,encoding='utf8');d=T7/'cuitest';d.mkdir(exist_ok=True);archs=[('same',data('cui_synthetic_same_'+dbn+'.db',A)),('different',data('cui_synthetic_different_'+dbn+'.db',B))]
  for tag,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]:
   cp=';'.join(map(str,[d,j,base,'D:/CodexWork/a12-r6-preprobes/deps/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*']));rr=execute([java/'javac.exe','-proc:none','-encoding','UTF-8','-sourcepath','','-cp',cp,'-d',d,p],T7);assert rr.returncode==0,rr.stdout
   for nm,arc in archs:
    cmd=[java/'java.exe','-cp',cp,'com.eva.ro.contab.banca.CUIOracleA12',arc,verified];r=execute(cmd,T7);assert r.returncode==0,r.stdout[-800:]
    res=r.stdout.strip().splitlines()[-1];out.append({'target':tag,'jar_sha256':sha(j),'case':nm,'setup_native_company_taxid':verified,'synthetic_archive_taxid':A if nm=='same'else B,'archive_sha':sha(arc),'actual':res,'expected':'MATCH'if nm=='same'else'refuz specific de CUI diferit','JVM_SAGA_reader':True})
    assert (res=='MATCH')==(nm=='same') and ('refuz' in res.lower() or 'difer' in res.lower() or nm=='same')
 finally:
  with db('postgres',True)as conn:conn.execute('drop database '+dbn)
 wr(RP/'T06_preconditii_Garden_PG_JAR.json',{'org_selection_initial_taxid_presence':[(int(z[0]),z[1])for z in initial],'company_taxid':A,'archive_other_taxid':B,'CUI_check_algorithm':'9 cifre corp ponderate 753217532; rest 10→0','rows':out,'table_scope':'JAR direct + metadate ale cabinetului restaurat pe PG. Verdict REST și delta de rânduri se măsoară separat, pe cabinetul efemer exclusiv solicitat.','seed_db_fixture_dropped':True});print(A,B,[(z['case'],z['actual'])for z in out])

