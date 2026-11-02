from a03_r4_slot import *
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
pr=sh(f'cd {wd} && [ ! -d pilot_started ] && cat pilot.py');assert pr.returncode==0, 'pilot already began'
fixture="""# Handcrafted initial asset in the exclusively owned synthetic clone; no journals are seeded.
assert sql("SELECT count(*) FROM adempiere.ad_client WHERE ad_client_id NOT IN (0,11)")=='0'
assert sql("SELECT count(*) FROM adempiere.a_asset WHERE ad_client_id=11")=='0'
sql(\"\"\"BEGIN; INSERT INTO adempiere.a_asset(a_asset_id,ad_client_id,ad_org_id,createdby,updatedby,value,name,a_asset_group_id,m_product_id,isactive,isdepreciated,isdisposed,assetservicedate,uselifemonths,description,a_asset_status) VALUES (8188130,11,11,100,100,'SYN-A03R4-DEP','A03 synthetic depreciable asset',50003,(SELECT min(m_product_id) FROM adempiere.m_product WHERE ad_client_id=11 AND isactive='Y'),'Y','Y','N','2026-04-01',12,'SYN fixture · conturi 60110/21101/60110 · metodă Liniara','AC');
INSERT INTO adempiere.a_depreciation_workfile(a_depreciation_workfile_id,ad_client_id,ad_org_id,a_asset_id,isactive,createdby,a_qty_current,updatedby,a_asset_cost,a_accumulated_depr,uselifemonths,a_life_period,a_current_period,postingtype) VALUES (8188130,11,11,8188130,'Y',100,1,100,1200,0,12,12,0,'A');COMMIT;\"\"\")
out['fixture_initial']={'asset_id':8188130,'cost':1200,'months':12,'service_date':'2026-04-01','scenario':'Inițializare strict în cabinet exclusiv: activ și fișă de amortizare sintetice, fără inserare de note/facte. Singura operație testată este apoi procesul ERP.'}
"""
code=pr.stdout.replace("for mm in ['2026-08','2026-09']:",fixture+"\nfor mm in ['2026-08','2026-09']:")
code=code.replace("(W/'finish').touch()","pass # release after optional native UI probe")
tmp=work/'pilot_with_asset.py';tmp.write_text(code,encoding='utf8',newline='\n');p=sp.run(['scp','-q','-o','BatchMode=yes',tmp,'saga-server@192.168.100.151:'+wd+'/pilot.py'],capture_output=True,text=True);assert p.returncode==0
print('prepared')
