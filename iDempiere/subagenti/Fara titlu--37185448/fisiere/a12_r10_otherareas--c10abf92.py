from a12_r10_base import *
bb=rd(P10/'Plan_R10_164_et_dix_zones.json')['each_zone']
for z in bb:
 if z['owner']in ['A01','A02','A04','A06','A08','A09','A10']:
  for rr in z['assigned']:print(z['owner'],rr['id'],rr['norm'][:174])

