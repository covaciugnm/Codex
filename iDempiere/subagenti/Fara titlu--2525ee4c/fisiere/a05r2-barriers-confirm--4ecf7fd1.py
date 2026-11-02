from lab import *
# Reuse Gate class only, no execution of exploratory program.
exec((W/'barriers.py').read_text().split('def wh_tx(')[0].split('class Gate:',1)[1].join(['class Gate:','']))
t=auth('GardenAdmin',11,102,11);prod=123
def visible(whid,did):
 s=query_snapshot(whid,prod,did);s['pair_rows']=rows(f"SELECT eva_perechewms_id,xmin::text FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id={whid};");return s
def prepare(label):
 wid,l=wh(t,label);d0,l0=inv(t,wid,l,prod,0,20,label+' baseline');assert doc(t,'M_Inventory',d0,'CO')['http']==200;did,ln=inv(t,wid,l,prod,20,18,label+' adjust -2');return wid,l,did,ln
def run(tag,mode):
 wid,loc,did,ln=prepare(tag);out={'mode':mode,'warehouse':wid,'locator':loc,'baseline':visible(wid,did),'events':[],'source_document':did}
 def log(name,d=None):out['events'].append({'at':now(),'event':name,'data':d})
 def adjust():return doc(auth('GardenAdmin',11,102,11),'M_Inventory',did,'CO')
 def activate():return process(auth('GardenAdmin',11,102,11),'eva_activarewms',{'M_Warehouse_ID':wid})
 if mode=='G1_commit_then_activation':
  log('native inventory commit response',adjust());log('independent observer before activation',visible(wid,did));log('native activation commit response',activate())
 elif mode=='activation_commit_then_G1':
  log('native activation commit response',activate());log('independent observer before inventory',visible(wid,did));log('native inventory commit response',adjust())
 else:
  fn='r2_hold_pair_'+str(wid);key=7921
  sql(f"CREATE FUNCTION adempiere.{fn}() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN IF NEW.m_warehouse_id={wid} THEN PERFORM pg_advisory_xact_lock(50575,{key}); END IF; RETURN NEW; END$$; CREATE TRIGGER {fn} BEFORE INSERT ON adempiere.eva_perechewms FOR EACH ROW EXECUTE FUNCTION adempiere.{fn}();")
  gate=Gate(key,'F10-overlap'); pool=concurrent.futures.ThreadPoolExecutor(max_workers=2);job=pool.submit(activate)
  try:
   log('activation reached instrument after stock read',gate.wait())
   pgwait=rows(f"SELECT pid FROM pg_locks WHERE locktype='advisory' AND classid=50575 AND objid={key} AND NOT granted")
   assert len(pgwait)==1,pgwait;activation_pid=int(pgwait[0][0]);j2=pool.submit(adjust)
   for _ in range(200):
    comm=rows(f"SELECT pid,state,wait_event_type,wait_event,pg_blocking_pids(pid)::text,left(query,120) FROM pg_stat_activity WHERE datname=current_database() AND {activation_pid}=ANY(pg_blocking_pids(pid)) AND upper(trim(query))='COMMIT';")
    if comm or j2.done():break
    time.sleep(.09)
   log('second transaction before barrier release',{'native_http_returned':j2.done(),'blocked_COMMIT':comm,'observed':visible(wid,did),'activation_pid':activation_pid})
  finally:gate.release()
  log('release own advisory lock',{'utc':now()});log('T1 HTTP',job.result(timeout=90));log('T2 HTTP',j2.result(timeout=90));pool.shutdown()
  sql(f'DROP TRIGGER {fn} ON adempiere.eva_perechewms; DROP FUNCTION adempiere.{fn}();')
 out['final']=visible(wid,did);out['repeat_activation']=activate();out['after_repeat']=visible(wid,did);return out
rr=[]
for label,mode in [('F10OV','overlap'),('F10IA','G1_commit_then_activation'),('F10AI','activation_commit_then_G1')]:
 try:rr.append(run(label,mode))
 except Exception as e:rr.append({'mode':mode,'error':str(e)[:500]})
 save('barriers-confirmed.json',rr);print(mode,rr[-1].get('error') or (rr[-1]['final']['g1'],rr[-1]['final']['g2']),flush=True)

