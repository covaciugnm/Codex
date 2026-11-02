from a12_r7_pg_cui import *
w=(T7/'current_fixture_path.txt').read_text().strip();assert re.fullmatch('/tmp/eva-contab-codex-p01a12r7t06[.][a-zA-Z0-9]+',w)
s=(Path(__file__).parent/'a12_r7_cabinet_test.py').read_text(encoding='utf8')
with db('p01_garden')as seed:val=seed.execute("select oi.taxid from adempiere.ad_orginfo oi join adempiere.ad_org o using(ad_org_id) where o.ad_client_id=11 order by oi.ad_org_id limit 1").fetchone()[0]
import base64
orig='NULL'if val is None else "convert_from(decode('"+base64.b64encode(val.encode()).decode()+"','base64'),'UTF8')"
s=s.replace("original=sql('select coalesce(taxid,'+chr(39)+'NULL'+chr(39)+') from adempiere.ad_orginfo where ad_org_id='+org)","original="+repr(orig)).replace("assert original=='NULL'or len(original)<32","assert original=='NULL'or original.startswith('convert_from(decode(')").replace("if original=='NULL':sql('update adempiere.ad_orginfo set taxid=null where ad_org_id='+org)\n else:\n  assert original.replace(' ','').isalnum();sql('update adempiere.ad_orginfo set taxid='+chr(39)+original+chr(39)+' where ad_org_id='+org)","sql('update adempiere.ad_orginfo set taxid='+original+' where ad_org_id='+org)")
stmt="select ba.c_bankaccount_id,ev.value from adempiere.c_bankaccount ba join adempiere.c_bankaccount_acct baa on baa.c_bankaccount_id=ba.c_bankaccount_id and baa.ad_client_id=ba.ad_client_id join adempiere.c_validcombination vc on vc.c_validcombination_id=baa.b_asset_acct join adempiere.c_elementvalue ev on ev.c_elementvalue_id=vc.account_id where ba.ad_client_id=11 and ba.isactive='Y' and ev.value is not null order by ba.c_bankaccount_id limit 1"
s=s.replace('def count():','account,ledger=rows('+repr(stmt)+')[0];assert account.isdigit()\ndef count():')
s=s.replace("con.execute('create table SOCIET (CODF_S text)')","con.executemany('insert into REGISTRU values(?,?,?,?,?,?,?,?,?,?,?,?)',[(str(i),str(i),'2026-01-08',ledger,'R7_CONTRA','1.00','','1','1.00','A12 synthetic statement '+str(i),'F','')for i in range(1,169)]);con.execute('create table SOCIET (CODF_S text)')")
s=s.replace("[('foreign',b),('same',a),('foreign_retry',b)]","[('same168',a),('foreign168',b),('foreign168retry',b)]").replace("'C_BankAccount_ID':0","'C_BankAccount_ID':int(account)")
z=sp.run(['ssh','-o','BatchMode=yes',server,'cd '+w+' && python3 -'],input=s.encode(),stdout=sp.PIPE,stderr=sp.PIPE,timeout=100);assert z.returncode==0,z.stderr.decode()[-600:]
v=json.loads(z.stdout);wr(RP/'T06_cabinet_nativ_168_note.json',v);print([(x['tag'],x['native'],x['before'],x['after'])for x in v['tests']])

