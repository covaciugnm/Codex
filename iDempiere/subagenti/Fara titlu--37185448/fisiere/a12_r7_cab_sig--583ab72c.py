from a12_r7_pg_cui import *
from pathlib import Path
import base64
w=(T7/'current_fixture_path.txt').read_text().strip();assert re.fullmatch('/tmp/eva-contab-codex-p01a12r7t06[.][a-zA-Z0-9]+',w)
s=(Path(__file__).parent/'a12_r7_cabinet_test.py').read_text(encoding='utf8')
with db('p01_garden')as seed:val=seed.execute("select oi.taxid from adempiere.ad_orginfo oi join adempiere.ad_org o using(ad_org_id) where o.ad_client_id=11 order by oi.ad_org_id limit 1").fetchone()[0]
orig='NULL'if val is None else "convert_from(decode('"+base64.b64encode(val.encode()).decode()+"','base64'),'UTF8')";s=s.replace("original=sql('select coalesce(taxid,'+chr(39)+'NULL'+chr(39)+') from adempiere.ad_orginfo where ad_org_id='+org)","original="+repr(orig)).replace("assert original=='NULL'or len(original)<32","assert original=='NULL'or original.startswith('convert_from(decode(')").replace("if original=='NULL':sql('update adempiere.ad_orginfo set taxid=null where ad_org_id='+org)\n else:\n  assert original.replace(' ','').isalnum();sql('update adempiere.ad_orginfo set taxid='+chr(39)+original+chr(39)+' where ad_org_id='+org)","sql('update adempiere.ad_orginfo set taxid='+original+' where ad_org_id='+org)")
s=s.replace("[('foreign',b),('same',a),('foreign_retry',b)]","[('different_again_fingerprint',b)]")
fp="select md5(string_agg(to_jsonb(z)::text,'|' order by z.eva_comparatiebanca_id)) from adempiere.eva_comparatiebanca z where ad_client_id=11"
s=s.replace('before=count()','before=count();d0=sql('+repr(fp)+')')
s=s.replace("'ids_fingerprint_after':rowsig,","'ids_fingerprint_after':rowsig,'content_fingerprint_before':d0,'content_fingerprint_after':sql("+repr(fp)+"),")
s=s.replace("'tests':outs,","'tests':outs,'multiplicity':rows(\"select t.c_bankaccount_id,count(*),count(distinct c_acctschema_id),array_agg(distinct c_acctschema_id order by c_acctschema_id) from adempiere.c_bankaccount_acct t where t.ad_client_id=11 and t.c_bankaccount_id in(select distinct c_bankaccount_id from adempiere.eva_comparatiebanca where ad_client_id=11) group by 1\"),")
z=sp.run(['ssh','-o','BatchMode=yes',server,'cd '+w+' && python3 -'],input=s.encode(),stdout=sp.PIPE,stderr=sp.PIPE,timeout=100);assert z.returncode==0,z.stderr.decode()[-550:];v=json.loads(z.stdout);assert len(v['tests'])==1;f=v['tests'][0];assert f['before']==f['after']==168 and f['content_fingerprint_before']==f['content_fingerprint_after']
wr(RP/'T06_cabinet_amprenta_integrala.json',v);print(v['multiplicity'],f['content_fingerprint_after'],f['native'])
cmd=sp.run(['ssh','-o','BatchMode=yes',server,'cd '+w+' && : >finish'],stdout=sp.PIPE,stderr=sp.PIPE,timeout=10);assert cmd.returncode==0

