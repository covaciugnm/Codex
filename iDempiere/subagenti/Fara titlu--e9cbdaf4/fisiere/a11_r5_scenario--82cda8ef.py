exec(open('C:/Users/User/AppData/Local/Temp/a11_r5_108.py',encoding='utf8').read().split('print(len(ls))')[0])
from collections import Counter
import re
s=[(c,i)for c,_ in ls for i in c['R5_measured_scenarios']]
print(len(s),len(set(q['evidence']for c,q in s)),Counter((q['layer'],bool(q.get('explicit_expected')))for _,q in s))
for c,i in s:
 if re.search(r'\bFAIL\b|\bEȘEC\b|\berror\b|mismatch',str(i['result']),re.I):
  print(c['id'],i['result'][:135])

