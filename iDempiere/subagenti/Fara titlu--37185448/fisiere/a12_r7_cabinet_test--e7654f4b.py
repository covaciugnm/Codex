from lab import W,sql,rows,auth,process,api
import subprocess as sp,sqlite3,os,json,hashlib,uuid,tempfile,datetime
from pathlib import Path
app=(W/'auditor-app').read_text().strip();pg=(W/'auditor-pg').read_text().strip();marker=sp.check_output(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',app],text=True).strip()
assert marker=='eva-contab-codex-p01a12r7t06'and sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
assert sql('select count(*) from adempiere.ad_client where ad_client_id not in(0,11)')=='0'
a,b='9800000414','9800000520';org=sql("select o.ad_org_id from adempiere.ad_orginfo oi join adempiere.ad_org o using(ad_org_id) where o.ad_client_id=11 order by oi.ad_org_id limit 1");assert org.isdigit()
original=sql('select coalesce(taxid,'+chr(39)+'NULL'+chr(39)+') from adempiere.ad_orginfo where ad_org_id='+org)
assert original=='NULL'or len(original)<32
own_cui=sql('begin;update adempiere.ad_orginfo set taxid='+chr(39)+'RO'+a+chr(39)+' where ad_org_id='+org+';commit;select oi.taxid from adempiere.ad_orginfo oi join adempiere.ad_org o on o.ad_org_id=oi.ad_org_id where o.ad_client_id=11 and oi.taxid is not null order by oi.ad_org_id limit 1;').splitlines()[-1]
assert own_cui=='RO'+a
user=auth('GardenAdmin',11,102,int(org))
templ={'REGISTRU':['ID_NOTA','PK','DATA','CONT_D','CONT_C','SUMA','COD_VALUTA','CURS','SUMA_VAL','EXPLICATIE','FEL_D','TIP'],'NOTE_FACTURI':['ID_NOTA','ID_FACTURA'],'NOTE_FACTURI_VAL':['ID_NOTA','ID_FACTURA'],'IESIRI':['ID_IESIRE'],'INTRARI':['ID_INTRARE'],'CLIENTI':['ANALITIC','DENUMIRE'],'FURNIZORI':['ANALITIC','DENUMIRE']}
def count():return int(sql('select count(*) from adempiere.eva_comparatiebanca where ad_client_id=11'))
def att(path,c):
 with sqlite3.connect(path)as con:
  for t,opts in templ.items():con.execute('create table '+t+' ('+','.join(z+' text'for z in opts)+')')
  con.execute('create table SOCIET (CODF_S text)');con.execute('insert into SOCIET values (?)',(c,));con.commit()
pfx='A12R7T06_'+uuid.uuid4().hex[:10];arc='/opt/idempiere/saga-archives';outs=[];files=[]
try:
 for tag,val in [('foreign',b),('same',a),('foreign_retry',b)]:
  fp=W/(pfx+'_'+tag+'.db');att(fp,val);remote=arc+'/'+fp.name;assert sp.run(['docker','exec',app,'test','-e',remote]).returncode!=0
  sp.check_call(['docker','cp',str(fp),app+':'+remote],stdout=sp.DEVNULL);files.append((fp,remote));before=count()
  par={'LunaDeLa':'2026-01','LunaPanaLa':'2026-01','C_BankAccount_ID':0,'DoarVerifica':'N','FilePath':remote}
  r=process(user,'eva_comparabancasaga',par);after=count();rowsig=sql('select md5(coalesce(string_agg(eva_comparatiebanca_id::text,'+chr(39)+','+chr(39)+' order by eva_comparatiebanca_id),'+chr(39)+chr(39)+')) from adempiere.eva_comparatiebanca where ad_client_id=11')
  outs.append({'tag':tag,'cabinet_supplier_taxid':own_cui,'archive_taxid':val,'source_archive_sha':hashlib.sha256(fp.read_bytes()).hexdigest(),'native':r,'before':before,'after':after,'delta':after-before,'ids_fingerprint_after':rowsig,'fixture_month':'2026-01'})
finally:
 notes=[]
 for f,rp in files:
  assert f.parent==W and f.name.startswith(pfx)and rp==arc+'/'+f.name;rc=sp.run(['docker','exec',app,'rm','--',rp]).returncode;f.unlink(missing_ok=True);notes.append((Path(rp).name,rc==0))
 # Scratch cabinet exclusively A12, original demo field restored before destruction of the complete PostgreSQL instance.
 if original=='NULL':sql('update adempiere.ad_orginfo set taxid=null where ad_org_id='+org)
 else:
  assert original.replace(' ','').isalnum();sql('update adempiere.ad_orginfo set taxid='+chr(39)+original+chr(39)+' where ad_org_id='+org)
print(json.dumps({'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cabinet':'A12 exclusive synthetic GardenWorld, comparator native, REST authenticated role102','org':int(org),'scope':'Fixture validă de structură pentru șapte tabele și SOCIET.CODF_S; data de închidere istorică și cele 168 înregistrări din vechea instalație sunt separate.','tests':outs,'fixture_files_cleaned':notes,'ad_orginfo_taxid_restored':True},ensure_ascii=False))

