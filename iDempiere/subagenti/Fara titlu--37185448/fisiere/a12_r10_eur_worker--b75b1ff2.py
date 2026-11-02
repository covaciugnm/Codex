from pathlib import Path
defs=(Path(__file__).parent/'bank-worker.py').read_text(encoding='utf8').split('account=rf(')[0];exec(defs)
from shutil import copy2
c11=11;sch=101;b0=987600000;bid=987600011;bankdata=rf("select b.ad_org_id, b.c_bankaccount_id, b.c_currency_id,ev.value from c_bankaccount b join c_bankaccount_acct ba on ba.c_bankaccount_id=b.c_bankaccount_id join c_validcombination vc on vc.c_validcombination_id=ba.b_asset_acct join c_elementvalue ev on ev.c_elementvalue_id=vc.account_id where b.c_bankaccount_id=987600000 and ba.c_acctschema_id=101");assert len(bankdata)==1;org=int(bankdata[0][0]);code=bankdata[0][3];ctx=auth('GardenAdmin',11,102,org);taxorg=int(rf("select x.ad_org_id from ad_orginfo x join ad_org o using(ad_org_id) where o.ad_client_id=11 order by x.ad_org_id limit 1")[0][0]);orig=stmt("select coalesce(encode(convert_to(taxid,'UTF8'),'hex'),'~') from ad_orginfo where ad_org_id="+str(taxorg));prev=int(stmt("select c_currency_id from c_acctschema where c_acctschema_id=101 and ad_client_id=11"));assert prev==100
rr='A12R10_FX_rates.sqlite';db=W/rr;copy2(W/'A12R10_BANK_168.sqlite',db);app=init['app'];target='/opt/idempiere/saga-archives/'+rr
with sqlite3.connect(db)as cc:
 cc.execute('delete from REGISTRU')
 for k,(dt,lei)in enumerate([('2026-07-08','3.75'),('2026-08-09','139.59'),('2026-09-10','7.00')]):
  cc.execute('insert into REGISTRU values(?,?,?,?,?,?,?,?,?,?,?,?)',(str(k+1),'FX'+str(k+1),dt,code,'CONTRAREPLACED',lei,'','','','FX synthetic','F',''))
 cc.commit()
print('currency',prev,'org',org)
ex={'start':now(),'initial_company_currency':{'iso':'USD','id':prev},'test_company_currency':{'iso':'RON','id':346},'bank_iso':'EUR','archive_sha':hashlib.sha256(db.read_bytes()).hexdigest(),'fallback_source':'SumaVal, COD_VALUTA, CURS empty; two native daily rates inserted in dedicated clone, third missing by design.'}
try:
 assert stmt('select count(*) from c_bankaccount where c_bankaccount_id='+str(bid))=='0'
 cp=stmt("select ev.value from c_bankstatementline bl join c_charge_acct ca on ca.c_charge_id=bl.c_charge_id and ca.c_acctschema_id=101 join c_validcombination vc on vc.c_validcombination_id=ca.ch_expense_acct join c_elementvalue ev on ev.c_elementvalue_id=vc.account_id where bl.c_bankstatementline_id=987610001")
 with sqlite3.connect(db)as cc:cc.execute("update REGISTRU set CONT_C=?",(cp,));cc.commit()
 ex['archive_sha']=hashlib.sha256(db.read_bytes()).hexdigest()
 s=['begin;', "update ad_orginfo set taxid='RO9800000414' where ad_org_id="+str(taxorg)+";",'update c_acctschema set c_currency_id=346 where ad_client_id=11 and c_acctschema_id=101;',clone('c_bankaccount','c_bankaccount_id='+str(b0),{'c_bankaccount_id':bid,'accountno':'A12R10-EUR','c_currency_id':102,'c_bankaccount_uu':str(uuid.uuid4())}),'delete from c_bankaccount_acct where c_bankaccount_id='+str(bid)+';',clone('c_bankaccount_acct','c_bankaccount_id='+str(b0)+' and c_acctschema_id=101',{'c_bankaccount_id':bid,'c_bankaccount_acct_uu':str(uuid.uuid4())})]
 for k,(dt,amt,rate)in enumerate([('2026-07-08','0.74','5.0962'),('2026-08-09','27.40','5.0949'),('2026-09-10','1.00',None)]):
  bs=987625000+k;bl=987615000+k
  s+= [clone('c_bankstatement','c_bankstatement_id=987620000',{'c_bankstatement_id':bs,'c_bankstatement_uu':str(uuid.uuid4()),'c_bankaccount_id':bid,'statementdate':dt,'name':'A12 FX '+str(k),'documentno':'A12-FX-'+str(k)}),clone('c_bankstatementline','c_bankstatementline_id=987610001',{'c_bankstatementline_id':bl,'c_bankstatementline_uu':str(uuid.uuid4()),'c_bankstatement_id':bs,'stmtamt':amt,'trxamt':amt,'c_currency_id':102,'statementlinedate':dt,'valutadate':dt,'dateacct':dt,'description':'SAGA-PK=FX'+str(k+1),'efttrxid':'FX'+str(k+1)})]
  if rate:
   from decimal import Decimal
   s +=[clone('c_conversion_rate','c_conversion_rate_id=135',{'c_conversion_rate_id':987630000+k,'c_conversion_rate_uu':str(uuid.uuid4()),'ad_client_id':11,'ad_org_id':org,'c_currency_id':102,'c_currency_id_to':346,'validfrom':dt,'validto':dt,'multiplyrate':rate,'dividerate':str(round(Decimal('1')/Decimal(rate),12)),'c_conversiontype_id':114,'isactive':'Y'})]
 s.append('commit;');sqlex('\n'.join(s));sp.check_call(['docker','cp',str(db),app+':'+target],stdout=sp.DEVNULL);z=process(ctx,'eva_comparabancasaga',{'C_BankAccount_ID':bid,'LunaDeLa':'2026-07','LunaPanaLa':'2026-09','DoarVerifica':'N','FilePath':target});ex['native']=z
 assert z['instance'];iid=int(z['instance']);ex['rows']=rf('select eva_datasaga::date,eva_sumasagalei,eva_curssaga,eva_sumasaga,eva_sumaeva,eva_delta,eva_verdict,eva_cauza from eva_comparatiebanca where ad_client_id=11 and c_bankaccount_id='+str(bid)+' and ad_pinstance_id='+str(iid)+' order by eva_datasaga');ex['logs']=[l[0]for l in rf('select p_msg from ad_pinstance_log where ad_pinstance_id='+str(iid)+' order by log_id')];print(z,ex['rows'])
finally:
 stmt('begin;update c_acctschema set c_currency_id='+str(prev)+' where ad_client_id=11 and c_acctschema_id=101;update ad_orginfo set taxid='+('NULL'if orig=='~'else"convert_from(decode("+q(orig)+",'hex'),'UTF8')")+' where ad_org_id='+str(taxorg)+';commit;')
 ex['restored_base_currency']=stmt('select c_currency_id from c_acctschema where c_acctschema_id=101 and ad_client_id=11');(W/'eur-result.json').write_text(json.dumps(ex,ensure_ascii=False));
