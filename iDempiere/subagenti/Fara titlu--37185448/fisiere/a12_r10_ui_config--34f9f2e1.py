from pathlib import Path
exec((Path(__file__).parent/'bank-worker.py').read_text(encoding='utf8').split('account=rf(')[0])
import sys
org=11;taxorg=int(rf("select x.ad_org_id from ad_orginfo x join ad_org o using(ad_org_id) where o.ad_client_id=11 order by x.ad_org_id limit 1")[0][0]);cfg=W/'A12-ui-restore.private';app=init['app'];target='/opt/idempiere/saga-archives/REZUMAT_11.json'
if sys.argv[1]=='prepare':
 assert not cfg.exists()
 orig=stmt("select coalesce(encode(convert_to(taxid,'UTF8'),'hex'),'~') from ad_orginfo where ad_org_id="+str(taxorg));excluded=[k[0]for k in rf("select c_bankaccount_id from c_bankaccount where c_bankaccount_id not between 987600000 and 987600009 and ad_client_id=11 and isactive='Y'")]
 present=sp.run(['docker','exec',app,'test','-e',target],capture_output=True).returncode==0
 if present:sp.check_call(['docker','cp',app+':'+target,str(W/'prior-ui-rezumat.private')])
 cfg.write_text(json.dumps({'org':taxorg,'tax':orig,'others':excluded,'present':present}));cfg.chmod(0o600);path=W/'REZUMAT_R10_FIXTURE.json';path.write_text(json.dumps({'arhiva':'A12R10_BANK_168.sqlite'}));path.chmod(0o644);sp.check_call(['docker','cp',str(path),app+':'+target])
 stmt("begin;update ad_orginfo set taxid='RO9800000414' where ad_org_id="+str(taxorg)+";update c_bankaccount set isactive='N' where c_bankaccount_id in("+','.join(excluded)+") and ad_client_id=11;commit;")
 print('active synthetic bank accounts=',stmt("select count(*) from c_bankaccount where ad_client_id=11 and isactive='Y'"),'pre-existing summary backed up?',present)
elif sys.argv[1]=='restore':
 if not cfg.exists():print('No UI fixture');sys.exit()
 z=json.loads(cfg.read_text());orig=z['tax'];stmt('begin;update c_bankaccount set isactive=\'Y\' where c_bankaccount_id in('+','.join(z['others'])+') and ad_client_id=11;update ad_orginfo set taxid='+('NULL'if orig=='~'else"convert_from(decode("+q(orig)+",'hex'),'UTF8')")+' where ad_org_id='+str(z['org'])+';commit;')
 if z['present']:sp.check_call(['docker','cp',str(W/'prior-ui-rezumat.private'),app+':'+target]);(W/'prior-ui-rezumat.private').unlink()
 else:sp.check_call(['docker','exec',app,'rm','-f','--',target])
 cfg.unlink();print('Restored source org demo metadata, states other accounts, file residue:',sp.run(['docker','exec',app,'test','-e',target]).returncode)
else:raise Exception('mode')

