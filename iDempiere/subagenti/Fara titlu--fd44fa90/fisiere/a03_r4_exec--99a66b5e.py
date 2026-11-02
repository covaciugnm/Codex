from a03_r4_pick import *
import os,sys,subprocess as sp,datetime,tempfile
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
import psycopg
from psycopg.rows import dict_row
root=P('D:/CodexWork/eva-audit-p01-readonly-20261102');plug=root/'idempiere/plugins/com.eva.ro.contab';sec=P('D:/CodexWork/eva-audit-secondary-20261102');work=P('D:/CodexWork/a03-r4-runtime');work.mkdir(exist_ok=True);jdk=P('C:/Program Files/Java/jdk-21/bin');cases=j(probe/'A03_R6_criterii.json');idx={c['id']:c for c in cases}; sha='6df998aee0e514d30856c461962afe99ebd0d113'
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def dump1(name,obj):dump(probe/name,obj)
def java(tag,jar):
 dst=work/tag;dst.mkdir(exist_ok=True);srcf=['TestT16Declaratii','TestT159LotA','TestT159LotB','TestT159LotC','TestT03Lot5','TestT03Front','TestT256D394','TestT58Inchidere','TestT194Salarii','TestT199Parametri','TestT153Interimar','TestT154BilantCredite']
 cp=';'.join(str(x) for x in [dst,sec/jar,sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',P('D:/CodexWork/a05-support-jars/*'),P('D:/CodexWork/eva-a01-java/lib/*'),plug/'src']); env={**os.environ,'JAVA_HOME':str(jdk.parent),'PATH':str(jdk)+';'+os.environ.get('PATH','')};args0=[jdk/'javac.exe','-proc:none','-encoding','UTF-8','-classpath',cp,'-sourcepath','','-d',dst]
 def cmd(args,timeout=45):return sp.run(args,cwd=plug,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=timeout)
 classes=[]
 for n in srcf:
  p=plug/'test'/(n+'.java');z=cmd(args0+[p]); classes.append({'class':n,'fixture_sha256':h(p),'rc':z.returncode,'diagnostic':z.stderr[:1000]})
 # Run independent subsections directly, avoiding unrelated javap on Windows. Same-package reflection only to choose the fixture methods.
 har=work/'R4SalCases.java'; har.write_text('''public class R4SalCases {public static void main(String[] x)throws Exception{var z=Class.forName("TestT194Salarii"); for(String name:x){var m=z.getDeclaredMethod(name);m.setAccessible(true);m.invoke(null);System.out.println("END "+name);}var f=z.getDeclaredField("fail");f.setAccessible(true);var ok=z.getDeclaredField("ok");ok.setAccessible(true);System.out.println("RESULT "+ok.get(null)+" OK / "+f.get(null)+" FAIL");if(f.getInt(null)>0)System.exit(2);}}''',encoding='utf8')
 hc=cmd(args0+[har]);classes.append({'class':'R4SalCases','rc':hc.returncode,'diagnostic':hc.stderr[:300]})
 policy=P('D:/CodexWork/p01-r5-jvm/limited-logging3.policy');probes=[]
 for n,extra in [(x,[]) for x in ['TestT159LotA','TestT159LotB','TestT159LotC','TestT03Lot5','TestT03Front','TestT256D394','TestT58Inchidere','TestT199Parametri','TestT153Interimar','TestT154BilantCredite']]+[('R4SalCases',['coA']),('R4SalCases',['coB']),('R4SalCases',['simB']),('R4SalCases',['simC']),('R4SalCases',['simH'])]:
  if not (dst/(n+'.class')).exists():continue
  argv=[jdk/'java.exe','-Xmx512m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dfile.encoding=UTF-8','-cp',cp,n]+extra
  try: rr=cmd(argv);text=rr.stdout+rr.stderr;rc=rr.returncode
  except sp.TimeoutExpired:rc=124;text='Timeout at 45 seconds'
  nm=tag+'_'+n+(''.join(extra))+'_R4.log';path=probe/nm;path.write_text(text,encoding='utf8');probes.append({'test':n,'subcases':extra,'rc':rc,'output':nm,'output_sha256':h(path),'tail':[l for l in text.splitlines() if 'REZULTAT' in l or 'RESULT ' in l][-2:],'explicit_failure':[l[:220] for l in text.splitlines() if re.match(r'\s*FAIL\b',l) or 'Exception in thread' in l][:8]});dump1(tag+'_runs.json',{'utc':now(),'jar':jar,'jar_sha256':h(sec/jar),'classes':classes,'cases':probes,'policy':{'file':str(policy),'hash':h(policy)},'sha':sha,'limits':'Teste de unitate, cu citire parametri din sursa înghețată, accesorii mock ale testului și fără conectare la parteneri sau la cabinetul real. Simularea nu execută un document native PO.'})
def pg():
 os.environ['PGPASSFILE']='D:/CodexWork/p01-local-pg16/pgpass.conf';cx=psycopg.connect(host='127.0.0.1',port=56481,dbname='p01_garden',user='audit_owner',row_factory=dict_row,options='-c default_transaction_read_only=on -c search_path=adempiere,public -c statement_timeout=12000'); queries={};res={}
 def q(id,sql,params=()):queries[id]={'sql':sql,'parameters':params};res[id]=cx.execute(sql,params).fetchall()
 q('identity',"select current_database() db,current_setting('transaction_read_only') ro, current_setting('server_version') version")
 q('registry_tables',"SELECT table_name FROM information_schema.tables WHERE table_schema='adempiere' AND (table_name LIKE 'eva_%%parametr%%fiscal%%' OR table_name LIKE 'eva_%%parametr%%leg%%' OR table_name LIKE 'eva_%%registr%%fiscal%%') ORDER BY 1")
 q('cols',"select table_name,column_name from information_schema.columns where table_schema='adempiere' and (column_name in ('origine','motiv','eva_origine','eva_motiv')) order by 1,2")
 q('chart',"SELECT c_acctschema_id,c.iso_code,c.stdprecision FROM c_acctschema s JOIN c_currency c USING(c_currency_id) WHERE s.ad_client_id=11 ORDER BY c_acctschema_id")
 loc=j(e/'Reverificare_balanta_si_receptie_nativa.json');q('eva',loc['sql']['eva_balance'],('2000-01-01','2000-01-01','2000-01-01','2030-12-31','2000-01-01','2030-12-31',11,'2030-12-31'));q('correct',loc['sql']['reference_native_schema'],('2000-01-01','2030-12-31'))
 q('native_currency_columns',"select table_name,column_name from information_schema.columns where table_schema='adempiere' and table_name in ('c_conversion_rate','c_acctschema','fact_acct','c_invoice') and column_name in ('c_currency_id','c_currency_id_to','validfrom','validto','multiplyrate','dateacct','amtacctdr','c_acctschema_id') order by 1,2")
 q('native_currency_rate_selection',"SELECT f.c_currency_id,f.c_currency_id_to,rate.multiplyrate,rate.validfrom,rate.validto FROM (VALUES (100::numeric,102::numeric),(102::numeric,100::numeric)) f(c_currency_id,c_currency_id_to) LEFT JOIN LATERAL (SELECT r.multiplyrate,r.validfrom,r.validto FROM c_conversion_rate r WHERE r.c_currency_id=f.c_currency_id AND r.c_currency_id_to=f.c_currency_id_to AND r.validfrom<=date '2002-12-31' AND r.validto>=date '2002-12-31' AND r.isactive='Y' ORDER BY r.validfrom DESC LIMIT 1) rate ON true")
 # An actual maintained native conversion function, on synthetic dates/tenants only. Record overloads before invoking.
 q('fx_function',"select p.proname,pg_get_function_identity_arguments(p.oid) args from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='adempiere' and p.proname in ('currencyconvert','currencyrate') order by 1,2")
 q('signed_posted_invoice106',"select distinct i.c_invoice_id,i.c_currency_id source_currency, i.dateacct, i.docstatus,i.posted,f.c_acctschema_id,s.c_currency_id functional_currency,f.line_id,sum(f.amtsourcedr) sourcedr,sum(f.amtsourcecr) sourcecr,sum(f.amtacctdr) acctdr,sum(f.amtacctcr) acctcr from c_invoice i join fact_acct f on f.record_id=i.c_invoice_id and f.ad_table_id=(select ad_table_id from ad_table where tablename='C_Invoice') join c_acctschema s using(c_acctschema_id) where i.ad_client_id=11 and i.c_invoice_id=106 group by i.c_invoice_id,i.c_currency_id,i.dateacct,i.docstatus,i.posted,f.c_acctschema_id,s.c_currency_id,f.line_id order by 5,7")
 cx.rollback();cx.close();dump1('pg_native_readback.json',{'utc':now(),'sha':sha,'sql':queries,'results':res,'safety':'Tranzacție read-only, doar clona GardenWorld sintetică. Cursurile comerciale actuale nu sunt evaluate.'})
if __name__=='__main__':
 import sys
 if sys.argv[1]=='git':java('git','cod-master-contab.jar')
 if sys.argv[1]=='installed':java('installed','com.eva.ro.contab_13.0.0.jar')
 if sys.argv[1]=='pg':pg()
