from a12_r10_base import *
areas=Counter()
for c in r9reg:
 if not c['cohorts']['external_38']:continue
 areas[(c['R9']=='NEEXECUTAT', '164'if c in f164 else'873'if c in nw873 else'167'if c in his167 else'prior_partially_observed')]+=1
print(areas,sum(v['cohorts']['separate_partial_218']for v in r9reg))
