from lab import W,sql,rows,auth,process,now
from pathlib import Path
import subprocess as sp,sqlite3,hashlib,json,os,time
import uuid,re,sys
init={'app':(W/'auditor-app').read_text().strip(),'pg':(W/'auditor-pg').read_text().strip()}
for c in init.values():assert sp.check_output(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',c],text=True).strip()=='eva-contab-codex-p01a12r10t06'
assert sql("select count(*) from adempiere.ad_client where ad_client_id not in(0,11)")=='0';assert sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
from contextlib import redirect_stdout
def status(m):print(m,file=sys.stderr,flush=True)
sqlex=lambda t:sql('SET search_path=adempiere,pg_catalog;\n'+t)
row=lambda t:rows('SET search_path=adempiere,pg_catalog;\n'+t)
def stmt(t):
 return '\n'.join(x for x in sqlex(t).splitlines()if x not in ['SET','BEGIN','COMMIT'])
def rf(t):
 ls=row(t);return [r for r in ls if r and r[0] not in ['SET','BEGIN','COMMIT']]
def fields(tab):return [r[0]for r in rf("select column_name from information_schema.columns where table_schema='adempiere' and table_name='"+tab+"' order by ordinal_position")]
def q(v):return 'NULL'if v is None else "'"+str(v).replace("'","''")+"'"
def clone(type_,base,values):
 js=json.dumps(values).replace("'","''")
 return 'INSERT INTO '+type_+' SELECT (jsonb_populate_record(NULL::'+type_+', (SELECT to_jsonb(z) FROM '+type_+' z WHERE '+base+') || '+q(json.dumps(values))+'::jsonb)).*;'
def insert(tab,values):return 'INSERT INTO '+tab+' ('+','.join(values)+') VALUES ('+','.join(q(x)for x in values.values())+');'
account=rf("select c_bankaccount_id,ad_org_id,c_currency_id from c_bankaccount where ad_client_id=11 and isactive='Y' order by c_bankaccount_id limit 1")
assert account;aid,org,cur=(int(v)for v in account[0]);org=org if org>0 else 11
orig=stmt('select coalesce(encode(convert_to(taxid,\'UTF8\'),\'hex\'),\'~\') from ad_orginfo where ad_org_id='+str(org))
assert orig=='~'or re.fullmatch('[0-9a-f]*',orig),repr(orig)
active=[int(r[0])for r in rf("select c_bankaccount_id from c_bankaccount where ad_client_id=11 and isactive='Y' order by c_bankaccount_id")];assert active
org_list=rf("select o.ad_org_id from ad_orginfo oi join ad_org o on o.ad_org_id=oi.ad_org_id where o.ad_client_id=11 order by o.ad_org_id limit 1");taxorg=int(org_list[0][0]);orig=stmt('select coalesce(encode(convert_to(taxid,\'UTF8\'),\'hex\'),\'~\') from ad_orginfo where ad_org_id='+str(taxorg))
sch=int(rf("select c_acctschema_id from c_acctschema where ad_client_id=11 and isactive='Y' order by c_acctschema_id limit 1")[0][0]);cp=rf("select ca.c_charge_id,ev.value from c_charge_acct ca join c_validcombination vc on vc.c_validcombination_id=ca.ch_expense_acct join c_elementvalue ev on ev.c_elementvalue_id=vc.account_id where ca.ad_client_id=11 and ca.c_acctschema_id="+str(sch)+" and ev.value is not null order by ca.c_charge_id limit 1");assert cp, 'Missing charge with accounting'
charge=int(cp[0][0]);contra=cp[0][1];cand=rf("select distinct on(ev.value) vc.c_validcombination_id,ev.value from c_validcombination vc join c_elementvalue ev on ev.c_elementvalue_id=vc.account_id where vc.ad_client_id=11 and vc.c_acctschema_id="+str(sch)+" and ev.value ~ '^[0-9]+$' and ev.value<>"+q(contra)+" order by ev.value,vc.c_validcombination_id limit 10");assert len(cand)==10,cand
baseacct=int(rf("select c_bankaccount_id from c_bankaccount_acct where ad_client_id=11 and c_acctschema_id="+str(sch)+" order by c_bankaccount_id limit 1")[0][0]);basebs=rf("select c_bankstatement_id from c_bankstatement where ad_client_id=11 order by c_bankstatement_id limit 1");baseline=rf("select c_bankstatementline_id from c_bankstatementline where ad_client_id=11 order by c_bankstatementline_id limit 1")
codes=[(int(v0),code)for v0,code in cand];bankids=list(range(987600000,987600010));linebase=987610000;stmtbase=987620000;synth='RO9800000414'
RES={'at':now(),'org_id':org,'run_type':'Exclusive GardenWorld accounts, not the archival q31 raw data. Synthetic import in SQLite and native SAGA comparator.','accounting_schema':sch,'computed_expected':{'physical_accounts':10,'months':6,'nonempty_groups':13,'note_count':168,'source_lines':152,'expected_distribution':[146,5,1,16],'expected_diff':22,'journal_categories':[1,1,10,60]},'test_fixtures':[],'attempts':[]}
native=auth('GardenAdmin',11,102,org)
seq=[(0,i,n)for i,n in enumerate([15,29,27,33,17,16],1)]+[(1,i,n)for i,n in zip([2,3,4,5],[2,7,5,1])]+[(2,4,1),(3,4,14),(3,5,1)];assert sum(z[2]for z in seq)==168
archive=W/'A12R10_BANK_168.sqlite';archive.unlink(missing_ok=True);target='/opt/idempiere/saga-archives/'+archive.name
def snap():
 ac=stmt("select count(*)||'|'||count(distinct ad_pinstance_id)||'|'||coalesce(string_agg(distinct ad_pinstance_id::text,','),'')||'|'||md5(coalesce(string_agg(to_jsonb(t)::text,'|' order by eva_comparatiebanca_id),'')) from eva_comparatiebanca t where ad_client_id=11")
 summary=rf("select eva_verdict,eva_cauza,count(*) from eva_comparatiebanca where ad_client_id=11 group by 1,2 order by 1,2")
 return {'rows_instances_id_rowhash':ac,'groups':summary}
def act(label,only=False,file=None):
 before=snap();r=process(native,'eva_comparabancasaga',{'LunaDeLa':'2026-01','LunaPanaLa':'2026-06','C_BankAccount_ID':0,'DoarVerifica':'Y'if only else'N','FilePath':file or target});after=snap();iid=r.get('instance');msgcol=next(k for k in ['p_msg','log_msg','msgtext']if k in fields('ad_pinstance_log')); j=rf('select '+msgcol+' from ad_pinstance_log where ad_pinstance_id='+str(int(iid))+' order by log_id')if iid and str(iid).isdigit()else[];RES['attempts'].append({'label':label,'role':102,'before':before,'native':r,'after':after,'adpinstance_logs':[l[0]for l in j],'adpinstance_result':rf('select result from ad_pinstance where ad_pinstance_id='+str(int(iid)))if iid and str(iid).isdigit()else[]});status(label+' '+str(r))
try:
 assert stmt('select count(*) from c_bankaccount where c_bankaccount_id between 987600000 and 987600009')=='0'
 sqlparts=['BEGIN;','UPDATE c_bankaccount SET isactive=\'N\' WHERE ad_client_id=11 AND c_bankaccount_id IN ('+','.join(map(str,active))+');','UPDATE ad_orginfo SET taxid='+q(synth)+' WHERE ad_org_id='+str(taxorg)+';']
 for k,(comb,code)in enumerate(codes):
  bid=bankids[k];vals={'c_bankaccount_id':bid,'accountno':'A12R10-'+str(k+1),'c_bankaccount_uu':str(uuid.uuid4()),'ad_org_id':org,'isactive':'Y','createdby':100,'updatedby':100,'isdefault':'N'};sqlparts.append(clone('c_bankaccount','c_bankaccount_id='+str(aid),vals))
  sqlparts+=["DELETE FROM c_bankaccount_acct WHERE c_bankaccount_id="+str(bid)+";"];av={'c_bankaccount_id':bid,'c_acctschema_id':sch,'b_asset_acct':comb,'c_bankaccount_acct_uu':str(uuid.uuid4()),'isactive':'Y'}
  sqlparts.append(clone('c_bankaccount_acct','c_bankaccount_id='+str(baseacct)+' and c_acctschema_id='+str(sch),av))
 templates={'REGISTRU':['ID_NOTA','PK','DATA','CONT_D','CONT_C','SUMA','COD_VALUTA','CURS','SUMA_VAL','EXPLICATIE','FEL_D','TIP'],'NOTE_FACTURI':['ID_NOTA','ID_FACTURA'],'NOTE_FACTURI_VAL':['ID_NOTA','ID_FACTURA'],'IESIRI':['ID_IESIRE'],'INTRARI':['ID_INTRARE'],'CLIENTI':['ANALITIC','DENUMIRE'],'FURNIZORI':['ANALITIC','DENUMIRE']}
 bscols=fields('c_bankstatement');lcols=fields('c_bankstatementline')
 with sqlite3.connect(archive)as cc:
  for t,opts in templates.items():cc.execute('create table '+t+' ('+','.join(z+' text'for z in opts)+')')
  cc.execute('create table SOCIET (CODF_S text)');cc.execute('insert into SOCIET values (?)',(synth[2:],));n=0
  for group,(bk,month,qty)in enumerate(seq):
   dd='2026-'+str(month).zfill(2)+'-12';bsid=stmtbase+group
   vv={'c_bankstatement_id':bsid,'c_bankstatement_uu':str(uuid.uuid4()),'ad_client_id':11,'ad_org_id':org,'createdby':100,'updatedby':100,'c_bankaccount_id':bankids[bk],'statementdate':dd,'name':'A12-BS-'+str(group),'description':'SAGA-BANCA test controlat','docstatus':'DR','processed':'N','docaction':'CO','posted':'N','isapproved':'N','documentno':'A12-BS-'+str(group),'isactive':'Y','statementdifference':0,'beginningbalance':0,'endingbalance':0};vv={k:v for k,v in vv.items()if k in bscols}
   sqlparts.append(clone('c_bankstatement','c_bankstatement_id='+basebs[0][0],vv)if basebs else insert('c_bankstatement',vv))
   for off in range(qty):
    n+=1;fid='R10-'+str(n);amt=str(100+n)+'.00';counter='R10-DIFF'if n==152 else contra
    cc.execute('insert into REGISTRU values(?,?,?,?,?,?,?,?,?,?,?,?)',(str(n),fid,dd,codes[bk][1],counter,amt,'','1',amt,'audit synthetic '+str(n),'F',''))
    if n<=152:
     v={'c_bankstatementline_id':linebase+n,'c_bankstatementline_uu':str(uuid.uuid4()),'ad_client_id':11,'ad_org_id':org,'createdby':100,'updatedby':100,'c_bankstatement_id':bsid,'line':off+1,'statementlinedate':dd,'dateacct':dd,'valutadate':dd,'stmtamt':str(100+n+(1 if 147<=n<=151 else 0)),'trxamt':str(100+n+(1 if 147<=n<=151 else 0)),'chargeamt':0,'interestamt':0,'c_currency_id':cur,'c_charge_id':charge,'c_payment_id':None,'c_bpartner_id':None,'efttrxid':'A12-R10-'+str(n),'description':'SAGA-PK='+fid,'isactive':'Y','processed':'N'};v={k:v for k,v in v.items()if k in lcols};sqlparts.append(clone('c_bankstatementline','c_bankstatementline_id='+baseline[0][0],v)if baseline else insert('c_bankstatementline',v))
  cc.commit()
 sqlparts.append('COMMIT;');sqlex('\n'.join(sqlparts))
 RES['test_fixtures']={'account_ids':bankids,'ledger_codes':[x[1]for x in codes],'physical':stmt("select count(*) from c_bankaccount where ad_client_id=11 and isactive='Y'"),'native_mapping_rows':stmt("select count(*) from c_bankaccount_acct a join c_bankaccount b using(c_bankaccount_id) where b.ad_client_id=11 and b.isactive='Y'"),'source_lines_fixture':stmt('select count(*) from c_bankstatementline where c_bankstatementline_id between '+str(linebase+1)+' and '+str(linebase+168)),'archive_sha':hashlib.sha256(archive.read_bytes()).hexdigest(),'template_bs_line':bool(baseline),'real_tenant_data':False}
 sp.check_call(['docker','cp',str(archive),init['app']+':'+target],stdout=sp.DEVNULL)
 act('check-only-before',True);act('normal-first');act('normal-retry');act('check-only-after',True);act('invalid archive',True,target+'.absent')
 RES['per_account_month']=rf("select c_bankaccount_id,eva_luna,count(*) from eva_comparatiebanca where ad_client_id=11 group by 1,2 order by 1,2")
 RES['final']=snap();(W/'bank-result.json').write_text(json.dumps(RES,ensure_ascii=False,default=str));print(json.dumps({'complete':True,'final':RES['final'],'instances':[x['native']for x in RES['attempts']]}))
finally:
 # Restore only the synthetic demo settings we borrowed; the disposable DB retains the audit fixture until teardown.
 if active:stmt("update c_bankaccount set isactive='Y' where ad_client_id=11 and c_bankaccount_id in ("+','.join(map(str,active))+")")
 stmt('update ad_orginfo set taxid='+('NULL'if orig=='~'else"convert_from(decode("+q(orig)+",'hex'),'UTF8')")+' where ad_org_id='+str(taxorg))

