from a12_r11x_base import *
j=read(O/'Suite_originale_API_portal_v7/Rezultate_suite_originale.json')
for i,r in enumerate(j['rows']): print(i,r['file'],r['exit'],len(r['cases']),collections.Counter((c['stage'],c['outcome'])for c in r['cases']),str(r['summary'])[:210])

