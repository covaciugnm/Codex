from lab import *
T=auth('GardenAdmin',11,102,11)
P=123
class Gate:
 def __init__(self,key,tag):
  self.key=key
  self.p=subprocess.Popen(['docker','exec','-i',PG,'psql','-X','-q','-v','ON_ERROR_STOP=1','-U','postgres','-d','idempiere','-At'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
  self.p.stdin.write(f"BEGIN; SET LOCAL application_name='A05R2-{tag}'; SELECT pg_advisory_xact_lock(50575,{key}); SELECT 'GATE_READY';\n");self.p.stdin.flush()
  while self.p.stdout.readline().strip()!='GATE_READY':
   if self.p.poll() is not None: raise ValueError('gate not acquired')
 def wait(self):
  for _ in range(220):
   v=sql(f"SELECT count(*) FROM pg_locks WHERE locktype='advisory' AND classid=50575 AND objid={self.key} AND NOT granted;")
   if v!='0':return {'at':now(),'blocked_sessions':int(v),'wal_lsn':sql('SELECT pg_current_wal_lsn();'),'snapshot':sql('SELECT txid_current_snapshot();')}
   time.sleep(.12)
  raise RuntimeError('gate hook not reached')
 def release(self):
  self.p.stdin.write("COMMIT; SELECT 'RELEASED';\n");self.p.stdin.flush();self.p.stdin.close();self.p.wait(timeout=6)
def wh_tx(label,order):
 whid,loc=wh(T,label[:10]);baseid,baseln=inv(T,whid,loc,P,0,20,label+' opening stock'); op=doc(T,'M_Inventory',baseid,'CO');assert op['http']==200,(baseid,op)
 inv_id,inv_ln=inv(T,whid,loc,P,20,18,label+' book=20 count=18')
 ids={'wh':whid,'loc':loc,'baseline_doc':baseid,'doc':inv_id,'line':inv_ln,'product':P}
 before=query_snapshot(whid,P,inv_id);assert before['g1'].split('.')[0]=='20' and before['g2'].split('.')[0]=='0',before
 key=7001 if order=='adjustment_first' else 7002
 fn='a05_gate_'+str(key); stmt=f"CREATE OR REPLACE FUNCTION adempiere.{fn}() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN "
 if order=='adjustment_first':stmt+=f"IF NEW.m_warehouse_id={whid} THEN PERFORM pg_advisory_xact_lock(50575,{key}); END IF; RETURN NEW; END $$; CREATE TRIGGER {fn} BEFORE INSERT ON adempiere.eva_perechewms FOR EACH ROW EXECUTE FUNCTION adempiere.{fn}();"
 else:stmt+=f"IF NEW.m_inventoryline_id={inv_ln} THEN PERFORM pg_advisory_xact_lock(50575,{key}); END IF; RETURN NEW; END $$; CREATE TRIGGER {fn} BEFORE INSERT ON adempiere.m_transaction FOR EACH ROW EXECUTE FUNCTION adempiere.{fn}();"
 sql(stmt);gate=Gate(key,label); execs=concurrent.futures.ThreadPoolExecutor(max_workers=2);result={'ids':ids,'order':order,'baseline':before,'fixture_gate':stmt}
 try:
  if order=='adjustment_first':
   job=execs.submit(process,T,'eva_activarewms',{'M_Warehouse_ID':whid})
   result['barrier']=gate.wait()
   t2=auth('GardenAdmin',11,102,11)
   result['first_commit']=doc(t2,'M_Inventory',inv_id,'CO')
  else:
   job=execs.submit(doc,T,'M_Inventory',inv_id,'CO')
   result['barrier']=gate.wait()
   t2=auth('GardenAdmin',11,102,11)
   result['first_commit']=process(t2,'eva_activarewms',{'M_Warehouse_ID':whid})
  result['observed_after_first_http_before_release']=query_snapshot(whid,P,inv_id)
 finally:
  gate.release()
 result['second_commit']=job.result(timeout=75);execs.shutdown()
 result['final']=query_snapshot(whid,P,inv_id);result['retry']=process(T,'eva_activarewms',{'M_Warehouse_ID':whid})
 result['after_retry']=query_snapshot(whid,P,inv_id);result['pair_count']=int(sql(f'SELECT count(*) FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id={whid};'))
 tab='eva_perechewms' if order=='adjustment_first' else 'm_transaction';sql(f'DROP TRIGGER {fn} ON adempiere.{tab}; DROP FUNCTION adempiere.{fn}();')
 return result
res=[]; 
for nm,rd in [('R2WH-A','adjustment_first'),('R2WH-B','activation_first')]:
 try:res.append(wh_tx(nm,rd))
 except Exception as err:res.append({'order':rd,'error':str(err),'at':now()})
 save('barriers.json',res);print(rd,res[-1].get('error') or res[-1].get('final'),flush=True)

