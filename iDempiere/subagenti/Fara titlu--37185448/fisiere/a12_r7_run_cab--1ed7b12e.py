from a12_r7_pg_cui import *
w=(T7/'current_fixture_path.txt').read_text().strip();assert re.fullmatch('/tmp/eva-contab-codex-p01a12r7t06[.][a-zA-Z0-9]+',w)
with db('p01_garden')as seed:
 val=seed.execute("select oi.taxid from adempiere.ad_orginfo oi join adempiere.ad_org o using(ad_org_id) where o.ad_client_id=11 order by oi.ad_org_id limit 1").fetchone()[0]
 import base64
 orig="NULL" if val is None else "convert_from(decode('"+base64.b64encode(val.encode()).decode()+"','base64'),'UTF8')"
s=Path(__file__).parent.joinpath('a12_r7_cabinet_test.py').read_text(encoding='utf8')
s=s.replace("original=sql('select coalesce(taxid,'+chr(39)+'NULL'+chr(39)+') from adempiere.ad_orginfo where ad_org_id='+org)","original="+repr(orig))
s=s.replace("assert original=='NULL'or len(original)<32","assert original=='NULL'or original.startswith('convert_from(decode(')")
s=s.replace("if original=='NULL':sql('update adempiere.ad_orginfo set taxid=null where ad_org_id='+org)\n else:\n  assert original.replace(' ','').isalnum();sql('update adempiere.ad_orginfo set taxid='+chr(39)+original+chr(39)+' where ad_org_id='+org)", "sql('update adempiere.ad_orginfo set taxid='+original+' where ad_org_id='+org)")
z=sp.run(['ssh','-o','BatchMode=yes',server,'cd '+w+' && python3 -'],input=s.encode(),stdout=sp.PIPE,stderr=sp.PIPE,timeout=120);assert z.returncode==0,z.stderr.decode()[-500:];v=json.loads(z.stdout);wr(RP/'T06_cabinet_nativ_egal_diferit.json',v);print([(r['tag'],r['native'],r['before'],r['after'])for r in v['tests']])

