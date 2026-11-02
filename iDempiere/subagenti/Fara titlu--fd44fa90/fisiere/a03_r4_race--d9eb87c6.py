from a03_r4_slot import *
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
remote='''from lab import *
from concurrent.futures import ThreadPoolExecutor
import threading,time
a=auth('GardenAdmin',11,102,11);b=auth('GardenAdmin',11,102,11);out={'utc':now(),'actor':'2 distinct synthetic GardenAdmin authentication sessions of the exclusive A03 GardenWorld only','attempts':[]}
def state():
 return rows("SELECT gl_journal_id,documentno,docstatus,posted,c_acctschema_id,trim(description) FROM adempiere.gl_journal WHERE ad_client_id=11 AND (description LIKE 'INCHIDERE-AMORT 2026-08%' OR description LIKE 'INCHIDERE-VC 2026-08%') ORDER BY gl_journal_id")
def post(token,op,reverse=False):
 body={'DateFrom':'2026-08-01','DateTo':'2026-08-31','Operatie':op,'EvaVerificOrdinea':True}
 if reverse:body['Devalideaza']='Y'
 t=now();code,obj=api(token,'POST','processes/eva_inchiderevenituri',body);return {'op':op,'rev':reverse,'http':code,'error':obj.get('isError'),'message':str(obj.get('summary',obj.get('detail','')))[:350],'start':t,'finish':now()}
def active(doc,keyword):return any(x[2]=='CO' and x[5].startswith('INCHIDERE-'+keyword+' ') for x in doc)
def save0(): (W/'race.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
pc=rows("SELECT c_periodcontrol_id,periodstatus FROM adempiere.c_periodcontrol WHERE c_period_id=200175 and docbasetype='GLJ'");assert len(pc)==1
out['control_before']=pc;out['schemes']=rows("select c_acctschema_id,autoperiodcontrol from adempiere.c_acctschema where ad_client_id=11 order by 1");out['journals_before']=state()
c,j=api(a,'PUT','models/C_PeriodControl/'+pc[0][0],{'PeriodAction':'O'});out['open_action']={'http':c,'detail':j.get('detail','')}
for payload in [{'record-id':int(pc[0][0])},{'*RecordIDs*':pc[0][0]}]:
 if sql("SELECT periodstatus FROM adempiere.c_periodcontrol WHERE c_periodcontrol_id="+pc[0][0])=='O':break
 rr=process(a,'c_periodcontrol_process',payload);out.setdefault('open_attempts',[]).append({'payload':payload,'result':str(rr)[:550]})
out['control_after']=rows("SELECT c_periodcontrol_id,periodstatus FROM adempiere.c_periodcontrol WHERE c_periodcontrol_id="+pc[0][0]);save0()
if out['control_after'][0][1]!='O':raise SystemExit(1)
for n in range(10):
 st=state();prep=[]
 if active(st,'VC'):prep.append(post(a,'VC',True))
 if not active(state(),'AMORT'):prep.append(post(a,'AMORT'))
 st=state()
 if active(st,'VC') or not active(st,'AMORT'):out['setup_blocked']={'before':st,'prep':prep};save0();break
 bar=threading.Barrier(2)
 def branch(rev):
  bar.wait(timeout=10);delayFirst=(n%2==0)
  if rev!=delayFirst:time.sleep(0.003)
  return post(b if rev else a,'AMORT' if rev else 'VC',rev)
 with ThreadPoolExecutor(max_workers=2) as tp:
  f1=tp.submit(branch,True);f2=tp.submit(branch,False);z=[f1.result(),f2.result()]
 end=state();okay=not (active(end,'VC') and not active(end,'AMORT'));out['attempts'].append({'round':n+1,'first_launch':'AMORT devalidate' if n%2==0 else 'VC validate','prep':prep,'before':st,'calls':z,'after':end,'VC_without_AMORT':not okay,'limitation':'3ms stagger is launch preference, not a deterministic database commit order. UTC times are recorded separately for each request.'});save0()
'''
p=work/'race.py';p.write_text(remote,encoding='utf8',newline='\n');z=sp.run(['scp','-q','-o','BatchMode=yes',p,'saga-server@192.168.100.151:'+wd+'/race.py'],capture_output=True);assert z.returncode==0
print(sh(f'cd {wd} && if mkdir race_start; then (nohup python3 race.py > race.log 2>&1 < /dev/null & echo $! >race.pid); fi').returncode)
