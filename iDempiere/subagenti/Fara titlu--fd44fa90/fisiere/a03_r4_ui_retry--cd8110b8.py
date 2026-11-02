from a03_r4_slot import *
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
raw=j(probe/'T58_native_gate.json');assert raw['probes'][0]['new_journals']==[['0']]
orig=P('D:/CodexWork/p01cross-account-close-sept.py').read_text(encoding='utf8').splitlines();ss='\n'.join(orig[3:10]).replace('2026-09','2026-08').replace('close-two-schemas','a03-native-setup').replace('828492','818894')
p=work/'extra_seed_ui.py';p.write_text('from lab import *\nt=auth("GardenAdmin",11,102,11);r={}\n'+ss+'\n(W/"august-extra-seed.json").write_text(json.dumps({"GL_target":r,"synthetic_opening_control":rows("select c_acctschema_id,account_id,amtacctdr,amtacctcr from adempiere.fact_acct where fact_acct_id between 8188940 and 8188943 order by fact_acct_id")}))\n',encoding='utf8',newline='\n')
assert 'insert into adempiere.fact_acct' in p.read_text().lower()
z=sp.run(['scp','-q','-o','BatchMode=yes',p,'saga-server@192.168.100.151:'+wd+'/extra_seed_ui.py'],capture_output=True);assert z.returncode==0
q=sh(f'cd {wd} && python3 extra_seed_ui.py >extra_seed_ui.log 2>&1');assert q.returncode==0,sh(f'cd {wd} && tail -6 extra_seed_ui.log').stdout
original=sh(f'cat {wd}/ui.json');dump1('T58_ZK_first_attempt.json',json.loads(original.stdout))
p2=work/'ui.py';current=p2.read_text(encoding='utf8').replace('\x08',r'\b');p3=work/'ui_retry.py';p3.write_text(current.replace("W/'ui.json'","W/'ui2.json'").replace("W/'T58-native","W/'T58-r2-native"),encoding='utf8',newline='\n')
z=sp.run(['scp','-q','-o','BatchMode=yes',p3,'saga-server@192.168.100.151:'+wd+'/ui_retry.py'],capture_output=True);assert z.returncode==0
print(sh(f'cd {wd} && if mkdir uir_started; then (nohup python3 ui_retry.py > uir.log 2>&1 < /dev/null &); fi').returncode)
