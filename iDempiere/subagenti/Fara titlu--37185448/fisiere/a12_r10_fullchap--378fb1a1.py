from a12_r10_publish import *
r=rd(R10/'A12_raport.json');sel={}
for x in r['records']:
 w=rd(R10/x['file']);ch=w['chapter'];y=sel.setdefault(str(ch),[0,0,0]);y[0]+=1;y[1]+=len(criteria(w));y[2]+=sum(q['R10']['effective_status']=='NEEXECUTAT'for q in criteria(w))
print([(k,z)for k,z in sel.items()if '03'in k or'10'in k][:8])
