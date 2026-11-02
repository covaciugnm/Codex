from a12_r10_publish import *
import sys
folder=E/'R10_pregatire/A05';fi=folder/'T329_raport_individual_A05.json';fd=folder/'T325_regresii_native.json';assert H(fi)=='80a52a0972d5ef17ede41b4110148dee91d110cd0a60bdce93ceef49bc6ff775' and H(fd)=='14807747fc7fab64975294dd1054c51d8efd65ca9d0fb7dd5a9c12a2fc82c363';a=rd(fi);b=rd(fd);receipts=collections.defaultdict(list);checked=set()
for log in a['evidence']+[b['source']]:
 p=folder/log['name'];assert p.stat().st_size==log['size']and H(p)==log['sha256'];checked.add(log['name'])
def src(f,p):return {'file':f.relative_to(B).as_posix(),'sha256':H(f),'pointer':p}
def add(c,k,description,neg,limit,refs,extent='subcase'):
 receipts[c].append({'criterion':c,'kind':k,'expected':r9[c]['text'],'observed':description,'negative_or_control':neg,'limits':limit,'references':refs,'extent':extent})
c=a['criterion'];assert c=='T329-R2-012';add(c,a['disposition'],a['nominal'],{'A05 Causal control':a['causal_control'],'single_schema_control':a['positive_control']},' '.join(a['method_and_limits']),[src(fi,'/nominal'),src(fi,'/positive_control'),src(fi,'/causal_control'),src(fi,'/evidence')])
for i,z in enumerate(b['rows']):
 c=z['id'];add(c,z['state'],{'document':b['document'],'threshold':b['threshold']},'NIR de mai devreme păstrează exact aceleași rânduri; magazia rămâne aceeași pentru mișcarea între locatori.',b['scope']+' '+z['remaining'],[src(fd,'/rows/'+str(i)),src(fd,'/document'),src(fd,'/threshold'),src(folder/b['source']['name'],'')])
p=P10/'A05_handoff_prime_doua_sigilate.json';wr(p,{'utc':now(),'signed_report':{'cost':S(fi),'native_transfers':S(fd)},'count_checked':len(checked),'source_artifacts_checked':sorted(checked),'receipts':receipts,'T330_individual_outstanding':True});print(sha(p),len(checked),list(receipts))

