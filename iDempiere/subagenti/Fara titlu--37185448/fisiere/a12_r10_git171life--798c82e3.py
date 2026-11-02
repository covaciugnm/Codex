from a12_r10_base import *
z=rd(E/'A12_referinte_git.json');print(list(z))
for k in z:
 if isinstance(z[k],list)and z[k]and isinstance(z[k][0],dict):
  for q in z[k]:
   if q.get('task',q.get('alias'))in ['T06','T171']:print(k,str(q)[:950])

