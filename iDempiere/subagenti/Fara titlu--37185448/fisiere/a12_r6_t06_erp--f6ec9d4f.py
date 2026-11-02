from lab import W,sql,rows,auth,process,api
import subprocess as sp,sqlite3,os,json,hashlib,uuid,tempfile,datetime
from pathlib import Path
app=(W/'auditor-app').read_text().strip();marker=sp.check_output(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',app],text=True).strip()
assert marker=='eva-contab-codex-p01uizkr5' and sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
pid=sql("select ad_process_id from adempiere.ad_process where value='EVA_ComparaBancaSaga'");assert pid.isdigit()
tabs=rows("select tablename from adempiere.ad_table where lower(tablename) like 'eva_comparatiebanca%' order by tablename"); assert tabs
def countbyclient():return {z[0]:int(sql("select count(*) from adempiere."+z[0]+" where ad_client_id=11"))for z in tabs}
org=sql("select ad_org_id from adempiere.ad_org where ad_client_id=11 and ad_org_id<>0 and isactive='Y' order by ad_org_id limit 1");token=auth('GardenAdmin',11,102,int(org))
prefix='a12r6t06_'+uuid.uuid4().hex[:12];paths=[];skipped=[];rr=[];arch='/opt/idempiere/saga-archives'
def inspect(f,blob):
 assert f.startswith(prefix) and '/'not in f;p=arch+'/'+f
 if sp.run(['docker','exec',app,'test','-e',p]).returncode==0:raise RuntimeError('fixture file collision')
 ftemp=W/f;ftemp.write_bytes(blob);sp.check_call(['docker','cp',str(ftemp),app+':'+p],stdout=sp.DEVNULL);paths.append((ftemp,p));return p
try:
 with tempfile.TemporaryDirectory(prefix='a12t06-') as tmp:
  bad=inspect(prefix+'_corrupt.json',b'{"fixture":"audit invalid sqlite"}');f=Path(tmp)/'src.db'
  with sqlite3.connect(f) as c:c.execute('create table SOCIET (CODF_S text)');c.execute('insert into SOCIET values (?)',('907060501',));c.commit()
  foreign=inspect(prefix+'_foreign.db',f.read_bytes())
  assert sql("select count(*) from adempiere.c_bankaccount where c_bankaccount_id=1988667711")=='0'
  cases=[('T27','range_invalid',{'LunaDeLa':'2026-06','LunaPanaLa':'2026-01'}),('T25','unknown_bank',{'C_BankAccount_ID':1988667711}),('T06_scope','missing_summary',{}),('C20','foreign_archive',{'FilePath':foreign}),('C21','unreadable_archive',{'FilePath':bad})]
  for label,name,d in cases:
   par={'LunaDeLa':'2026-01','LunaPanaLa':'2026-06','DoarVerifica':'N',**d};before=countbyclient()
   # Use the resource's native slug in the process registry; try alternatives only on HTTP 404 (no execution).
   aliases=['eva-comparabancasaga','eva_comparabancasaga',pid]
   for slug in aliases:
    out=process(token,slug,par)
    if out['http']!=404:break
   after=countbyclient();rr.append({'case':name,'source_tag_or_recipe':label,'request':par,'native_process_id':int(pid),'actual_path':slug,'response':out,'client11_before':before,'client11_after':after,'delta':{k:after[k]-v for k,v in before.items()}})
finally:
 cleanup=[]
 for local,remote in paths:
  assert remote.startswith(arch+'/'+prefix)and local.parent==W and local.name.startswith(prefix);deleted=sp.run(['docker','exec',app,'rm','--',remote]);local.unlink(missing_ok=True);cleanup.append({'file':local.name,'removed':deleted.returncode==0})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cabinet':'GardenWorld 11, rol 102','process':pid,'sources':'Exact clone r57. Two files created for this fixture only, with different CUI and unreadable bytes. AD_PInstance process traces deliberately retained. No business row is cleaned because attempts are intended to reject.','runs':rr,'removed':cleanup,'scope':'Variațiile, rolul și popularea diferă de clona istorică cu 168 rânduri. Zero delta în GardenWorld nu validează rândurile istorice 168.'},ensure_ascii=False))

