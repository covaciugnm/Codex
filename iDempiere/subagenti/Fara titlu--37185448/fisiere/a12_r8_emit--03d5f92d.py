from a12_r8_list import *
from pathlib import Path
import json
q=P/'JVM'
if __name__=='__main__':
 for x in rd(q/'Executii.json'):
  if x['target']!='git':continue
  f=B/x['log']['file'];ls=f.read_text(encoding='utf8').splitlines(); arr=[l.strip()for l in ls if re.match(r'^\s*(?:FAIL|OK)\s+',l)]
  print(x['suite'],x['exit'],len(arr),'||',' // '.join(arr[:6])[:740])

