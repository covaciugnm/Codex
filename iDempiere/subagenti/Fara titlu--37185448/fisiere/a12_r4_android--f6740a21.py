from a12_r3_survey import *
import shutil,datetime
R=E/'R4';ip=R/'inputs/android';ip.mkdir(parents=True,exist_ok=True)
for f in sorted((E/'A09/android_R2').glob('AND*.json')):shutil.copyfile(f,ip/f.name)
def safe(s,maxl=700):return str(s or '')[:maxl]
out={}
for fp in ip.glob('AND*.json'):
 a=rd(fp);ser=a['observed_server'] or {};acc=a.get('observed_accessibility')or{}
 rot=acc.get('rotation_control')or[];rot=rot if isinstance(rot,list)else[rot]
 out[a['id']]={'file':fp.name,'sha':sha(fp),'status':a['execution_status'],'observed':a['observed'],'finished':a['instrumentation_finished'],'passing_subset_in_card':a['executed_instrumented_pass'],'instrumented_failed':a['instrumented_failed'],'hardware':a['hardware_physical'],'aliases':[v['source']for v in a['task_aliases']],'server_basis':ser.get('interpretation')if isinstance(ser,dict)else None,'accessibility':{'rotation_evidence':[{k:v.get(k)for k in ('step','rotation','pixels','visible_error','user')if k in v}for v in rot if isinstance(v,dict)]} if acc else None,'limit':a.get('limitations')}
wr(R/'probe/Android_snapshot_R4.json',out);print([(k,v['status'],v['finished'])for k,v in out.items()])

