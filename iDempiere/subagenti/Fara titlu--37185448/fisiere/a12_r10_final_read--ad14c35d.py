from a12_r10_publish import *
x=R10/'MANIFEST_R10.json';d=rd(x);assert sha(x)=='92577020e8d8647c617b4a6dd098c82004eb66fe5dde3c6f4a1d3900e14380fd';assert all(sha(R10/k)==v for k,v in d['artifacts'].items());r=rd(R10/'Registru_reexecutare_R10.json')['rows']
for c in ['C03','C10']:
 sel=[z for z in r if (z['canonical']or'').startswith('P01.'+c+'.')];print(c,len(sel),sum(z['R10']=='NEEXECUTAT'for z in sel),sum(z['R9']=='NEEXECUTAT'for z in sel),len({z['task']for z in sel}))
print('readback '+sha(x))
