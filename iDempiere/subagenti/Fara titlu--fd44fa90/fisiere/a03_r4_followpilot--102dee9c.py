from a03_r4_slot import *
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
old=sh(f'cat {wd}/pilot.py');first=sh(f'cat {wd}/pilot.json');assert old.returncode==0 and first.returncode==0
f0=j(probe/'T58_native_gate.json');dump1('T58_native_first_period_guard.json',f0)
s=old.stdout;s=s[:s.index('# Handcrafted')]+'''# Configure accounting start through native model, not ledger writes. Preserve prior overlapping historical-year result separately.
present=rows("SELECT ad_sysconfig_id,value FROM adempiere.ad_sysconfig WHERE ad_client_id=11 AND name='EVA_PRIMA_LUNA_CONTABILA'")
if present:
 result=put(t,'AD_SysConfig',int(present[0][0]),{'Value':'2026-08'})
else: result=new(t,'AD_SysConfig',{'AD_Org_ID':0,'Name':'EVA_PRIMA_LUNA_CONTABILA','Value':'2026-08','Description':'A03 synthetic August starting period for isolated C-04 reproduction','ConfigurationLevel':'C','EntityType':'U'})
out['setup']={'native_method':'AD_SysConfig through EVA REST','before':present,'after':rows("SELECT ad_sysconfig_id,value FROM adempiere.ad_sysconfig WHERE ad_client_id=11 AND name='EVA_PRIMA_LUNA_CONTABILA'"),'asset':rows("SELECT a.a_asset_id,a.assetservicedate,w.a_asset_cost,w.uselifemonths FROM adempiere.a_asset a JOIN adempiere.a_depreciation_workfile w USING(a_asset_id) WHERE a.a_asset_id=8188130")}
'''+s[s.index("for mm in ['2026-08'"):];s=s.replace("(W/'pilot.json').write_text","(W/'pilot2.json').write_text")
p=work/'pilot2.py';p.write_text(s,encoding='utf8',newline='\n');rr=sp.run(['scp','-q','-o','BatchMode=yes',p,'saga-server@192.168.100.151:'+wd+'/pilot2.py'],capture_output=True);assert rr.returncode==0
res=sh(f'cd {wd} && python3 pilot2.py >pilot2.log 2>&1 && cat pilot2.json');assert res.returncode==0,sh(f'cd {wd} && tail -4 pilot2.log').stdout[:500];v=json.loads(res.stdout);dump1('T58_native_gate.json',v);print([(y['month'],y['isError'],y['summary'][:240],y['new_journals']) for y in v['probes']])
