from a12_r11x_discover import B,E,P,O
import json,gzip,collections
rows=[json.loads(r) for r in gzip.open(P/'Dispatch_tehnic_integral.jsonl.gz','rt',encoding='utf8')]
print('rows',len(rows),collections.Counter(r['owner'] for r in rows),collections.Counter(r['profile'] for r in rows))
for r in rows:
 p=r['path']
 if ('Bancar' in p or 'T06' in p or 'T201' in p or 'T257' in p) and ('Test' in p or 'Proces' in p or p.endswith('.jar')): print(r['id'],r['owner'],p)
print('java',[(r['path'],r['owner']) for r in rows if r['path'].endswith('.jar')][:80])
print('delta',[(r['delta'],r['path']) for r in rows if r['path'].endswith('.java') and r['delta']!='UNCHANGED_VS_R10'][:50])
