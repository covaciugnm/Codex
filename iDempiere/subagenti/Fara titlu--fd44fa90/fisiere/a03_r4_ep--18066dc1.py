from a03_r4_slot import *
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
def export_ui():
 rr=sh(f'cd {wd} && cat ui2.json');assert rr.returncode==0,rr.stderr[:200]
 ui=json.loads(rr.stdout);f=probe/'T58_ZK.json';dump1('T58_ZK.json',ui)
 for named in ['T58-r2-native-form.png','T58-r2-native-august.png','T58-r2-native-diagnostic.png']:
  y=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','cat '+wd+'/'+named],capture_output=True,timeout=12)
  if y.returncode==0 and y.stdout.startswith(b'\x89PNG'): (probe/named).write_bytes(y.stdout)
 print(ui.get('selected_month'),ui.get('button'),ui.get('refusal_seen'),ui.get('new_journals'),ui.get('diagnostic'))
def positive():
 assert (probe/'T58_ZK.json').is_file()
 test='''from lab import *
t=auth('GardenAdmin',11,102,11);out={'utc':now(),'actor':'GardenAdmin, client11 role102 org11','params':'August 2026; accounting start Aug, active asset 1200/12 before closing, 4 synthetic opening source lines, both schemes active. No GL outputs pre-created.','operations':[]}
def docs():return rows("SELECT j.gl_journal_id,j.documentno,j.docstatus,j.posted,j.c_acctschema_id,c.iso_code,trim(j.description) FROM adempiere.gl_journal j JOIN adempiere.c_currency c USING(c_currency_id) WHERE j.ad_client_id=11 AND j.description LIKE 'INCHIDERE-%2026-08%' ORDER BY j.gl_journal_id")
def action(op,rev=False):
 b={'DateFrom':'2026-08-01','DateTo':'2026-08-31','Operatie':op,'EvaVerificOrdinea':True}
 if rev:b['Devalideaza']='Y'
 x=docs(); h,obj=api(t,'POST','processes/eva_inchiderevenituri',b);z=docs();out['operations'].append({'op':op,'reverse':rev,'http':h,'isError':obj.get('isError'),'summary':str(obj.get('summary',obj.get('detail','')))[:1200],'before':x,'after':z,'body':b});return obj
first=action('AMORT')
if not first.get('isError',True):
 for k in ('SAL','CURS','IMP'):action(k)
 v=action('VC')
 if not v.get('isError',True):action('AMORT',True);action('VC',True)
out['facts']=rows("SELECT j.gl_journal_id,j.documentno,j.docstatus,j.posted,coalesce(f.line_id,0),f.account_id,f.c_acctschema_id,sum(f.amtacctdr),sum(f.amtacctcr) FROM adempiere.gl_journal j LEFT JOIN adempiere.fact_acct f ON f.ad_table_id=(SELECT ad_table_id FROM adempiere.ad_table WHERE tablename='GL_Journal') AND f.record_id=j.gl_journal_id WHERE j.ad_client_id=11 AND j.description LIKE 'INCHIDERE-%2026-08%' GROUP BY 1,2,3,4,5,6,7 ORDER BY 1,5,6")
out['asset_facts']=rows("SELECT a_asset_id,postingtype,a_period,expense FROM adempiere.a_depreciation_exp WHERE a_asset_id=8188130 ORDER BY a_period") if sql("SELECT count(*) FROM information_schema.columns WHERE table_schema='adempiere' AND table_name='a_depreciation_exp' AND column_name='expense'")=='1' else rows("SELECT a_asset_id,postingtype,a_period FROM adempiere.a_depreciation_exp WHERE a_asset_id=8188130 ORDER BY a_period")
(W/'positive.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
'''
 p=work/'positive.py';p.write_text(test,encoding='utf8',newline='\n');r=sp.run(['scp','-q','-o','BatchMode=yes',p,'saga-server@192.168.100.151:'+wd+'/positive.py'],capture_output=True);assert r.returncode==0
 z=sh(f'cd {wd} && python3 positive.py >positive.log 2>&1 && cat positive.json')
 assert z.returncode==0,sh(f'cd {wd} && tail -6 positive.log').stdout[:580]
 v=json.loads(z.stdout);dump1('T58_positive_and_reverse.json',v);print([(x['op'],x['isError'],x['summary'][:135]) for x in v['operations']])
if __name__=='__main__':{'ui':export_ui,'positive':positive}[sys.argv[1]]()
