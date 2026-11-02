from a12_r10_base import *
from collections import defaultdict,Counter
exp=E/'R10_pregatire/A05/T330_numitor_declarat.json';nm=rd(exp)['classes'];index={(k,n):[]for k,d in nm.items()for n in d['classes']};assert len(index)==300
rdir=E/'R5_pregatire/JVM';orig=rdir/'Executii_JVM_R5.json';s5=rd(orig);repo=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');same={};notincluded=[];count=0
def add(mod,n,tar,jrc,report,ref,log,hh,source0,ss):
 if (mod,n)not in index:return
 assert log.exists(),log
 assert sha(log)==hh,log
 sp=repo/source0;assert sp.exists(),sp
 if sha(sp)!=ss:raise AssertionError(('source',n))
 it={'target':tar,'result_code':jrc,'source_file':source0,'source_sha256':ss,'bound_to_fixed_input_and_existing_jar':True,'report':source(report),'pointer':ref,'log':source(log),'official_fresh_suite':False}
 index[mod,n].append(it)
for i,v in enumerate(s5['runs']):
 n=v['suite'];m='saga'if'com.eva.ro.saga.native'in v['source']else'contab';same[n,v['target']]=v;fo=rdir/v['log'];add(m,n,v['target'],v.get('run_rc'),orig,'/runs/'+str(i),fo,v['log_sha256'],v['source'],v['source_sha256'])
for fn in ['Calibrare_JVM_R5_2.json','Calibrare_JVM_R5_3.json']:
 df=rdir/fn;rr=rd(df)['results']
 for i,v in enumerate(rr):
  prev=same[v['suite'],v['target']];mod='saga'if'com.eva.ro.saga.native'in prev['source']else'contab'
  add(mod,v['suite'],v['target'],v['rc'],df,'/results/'+str(i),rdir/v['log'],v['sha256'],prev['source'],prev['source_sha256'])
for f in [P10/'JVM_original.json',P10/'JVM_registre_corelare.json',P10/'Zone_A08/Suita_T316.json',P10/'Zone_A08/T351_gates_si_suita.json',P10/'Zone_A09/Suita_tiparituri.json']:
 data=rd(f);key='runs'if 'runs'in data else'suite'
 for i,v in enumerate(data[key]):
  rr=v['log'];mod='saga'if'com.eva.ro.saga.native'in v['file']else'contab'
  add(mod,v['suite'],v['target'],v['exit'],f,'/'+key+'/'+str(i),B/rr['file'],rr['sha256'],v['file'],v['source_sha'])
rows=[];cnt=Counter()
for (mod,n),arts in index.items():
 vs={v['target']for v in arts if v['result_code']==0};state='0_COMPONENT_METADATA' if not arts else'COMPONENT_EXIT0_BOTH'if len(vs)==2 else'COMPONENT_EXIT0_ONE'if vs else'COMPONENT_ATTEMPTS_WITHOUT_EXIT0'
 cnt[state]+=1;rows.append({'module':mod,'suite':n,'alternate_evidence_state':state,'archive_instances':arts,'full_runner_state_for_this_record':'NEEXECUTAT_DE_ACEST_RAPORT','no_grade':True})
rows.append({'module':'Garda','suite':'GardaSeparata','alternate_evidence_state':'NERECONCILIATA_COMPLET','archive_instances':[],'full_runner_state_for_this_record':'NEEXECUTAT_DE_ACEST_RAPORT','no_grade':True})
f=P10/'T330_reconciliere_de_componente_301.json';wr(f,{'utc':now(),'source_population':source(exp),'method':'Source filename/module + SHA of the test source + SHA read from every original log. One row per member of the official list, repeated executions kept separately. No assertion extracted from exit0 in this appendix; no acceptance/FAIL of the official suite R10. For calibrated R5 traces, R5 root data provide common source and JAR identity. The initial listed inputs are bounded to the chosen R5/R10 datasets, not all historical packets.','count':len(rows),'component_counts_only':cnt,'historical_and_current_component_log_records':sum(len(q['archive_instances'])for q in rows),'records':rows,'qualification':'La contraproba completă T330 contează exportul comun, toate cele 301 probe și numărătoarea tranzacțiilor, nu acest inventar individual al testelor. Suite cu același nume/prioritate și multiple JAR nu se însumează ca suite distincte.'})
print(sha(f),cnt,sum(len(q['archive_instances'])for q in rows))

