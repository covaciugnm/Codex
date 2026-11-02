from pathlib import Path
exec((Path(__file__).parent/'bank-worker.py').read_text(encoding='utf8').split('account=rf(')[0])
import threading,concurrent.futures as ft
from datetime import datetime,timezone
roles=[('GardenAdmin',102),('GardenUser',103)]
org=11;taxorg=int(rf("select x.ad_org_id from ad_orginfo x join ad_org o using(ad_org_id) where o.ad_client_id=11 order by x.ad_org_id limit 1")[0][0]);orig=stmt("select coalesce(encode(convert_to(taxid,'UTF8'),'hex'),'~') from ad_orginfo where ad_org_id="+str(taxorg));exclude=[r[0]for r in rf("select c_bankaccount_id from c_bankaccount where ad_client_id=11 and isactive='Y' and c_bankaccount_id not between 987600000 and 987600009")];tokens=[auth(user,11,role,org)for user,role in roles]
def snaprace():
 return {'count':stmt("select count(*) from eva_comparatiebanca where ad_client_id=11 and eva_luna between '2026-01' and '2026-06' and c_bankaccount_id between 987600000 and 987600009"),'groups_mixed_pinstance':rf("select c_bankaccount_id,eva_luna,count(distinct ad_pinstance_id) from eva_comparatiebanca where ad_client_id=11 and eva_luna between '2026-01' and '2026-06' and c_bankaccount_id between 987600000 and 987600009 group by 1,2 having count(distinct ad_pinstance_id)>1"),'instances':rf("select ad_pinstance_id,count(*) from eva_comparatiebanca where ad_client_id=11 and eva_luna between '2026-01' and '2026-06' and c_bankaccount_id between 987600000 and 987600009 group by 1 order by 1")}
b=threading.Barrier(2);trg='/opt/idempiere/saga-archives/A12R10_BANK_168.sqlite'
def go(i):
 b.wait();st=time.time_ns();r=process(tokens[i],'eva_comparabancasaga',{'C_BankAccount_ID':0,'LunaDeLa':'2026-01','LunaPanaLa':'2026-06','DoarVerifica':'N','FilePath':trg});en=time.time_ns()
 return {'role':roles[i][1],'request_start_epoch_ns':st,'request_end_epoch_ns':en,'native':r}
ex={'utc':now(),'route':'Deux sessions et rôles GardenWorld indépendants; REST process, pas clic ZK. Le verrou témoin est pris sur 1 compte pour rendre visible la compétition.'}
try:
 stmt("begin;update ad_orginfo set taxid='RO9800000414' where ad_org_id="+str(taxorg)+";update c_bankaccount set isactive='N' where c_bankaccount_id in("+','.join(exclude)+") and ad_client_id=11;commit;")
 ex['before']=snaprace()
 with ft.ThreadPoolExecutor(max_workers=4)as tp:
  hold=tp.submit(stmt,"begin; set local application_name='R10MASTER_A12BANK_LOCK';select c_bankaccount_id from c_bankaccount where ad_client_id=11 and c_bankaccount_id=987600000 for update;select pg_sleep(3);commit;")
  for i in range(20):
   if stmt("select count(*) from pg_stat_activity where application_name='R10MASTER_A12BANK_LOCK' and wait_event='PgSleep'")=='1':break
   time.sleep(.12)
  both=[tp.submit(go,i)for i in range(2)];ex['contended']=[]
  for _ in range(11):
   if all(t.done()for t in both):break
   cur=rf("select wait_event_type,wait_event,count(*) from pg_stat_activity where lower(query) like '%from c_bankaccount where c_bankaccount_id%' and cardinality(pg_blocking_pids(pid))>0 group by 1,2");ex['contended'].append({'at':now(),'locks':cur});time.sleep(.27)
  ex['hold_completed']=hold.result();ex['results']=[t.result()for t in both]
 ex['after']=snaprace();ss=ex['results'];ex['start_difference_ms']=abs(ss[0]['request_start_epoch_ns']-ss[1]['request_start_epoch_ns'])/10**6;ex['overlap_ms']=(min(x['request_end_epoch_ns']for x in ss)-max(x['request_start_epoch_ns']for x in ss))/10**6
finally:
 stmt("begin;update c_bankaccount set isactive='Y' where c_bankaccount_id in("+','.join(exclude)+") and ad_client_id=11;update ad_orginfo set taxid="+('NULL'if orig=='~'else"convert_from(decode("+q(orig)+",'hex'),'UTF8')")+" where ad_org_id="+str(taxorg)+";commit;")
 (W/'race-result.json').write_text(json.dumps(ex,ensure_ascii=False));print(ex.get('after'),ex.get('results'),ex.get('overlap_ms'))
