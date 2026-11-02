from a12_r11_core import *
r10=rd(R10/'Registru_reexecutare_R10.json')['rows'];f={z['criterion']:z for z in r10 if z['R10_entry_cohorts']['164']and z['R10']=='NEEXECUTAT'};a=rd(P10/'Plan_R10_164_et_dix_zones.json')['each_zone']
for zz in a:
 remain=[k for k in zz['assigned']if k['id']in f];print(zz['owner'],len(remain),sorted(set(v['task']for v in remain)))

