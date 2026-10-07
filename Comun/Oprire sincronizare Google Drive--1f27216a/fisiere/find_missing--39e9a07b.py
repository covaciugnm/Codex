import os, json
from collections import Counter

os.chdir(os.path.dirname(os.path.abspath(__file__)))
missing = json.load(open('missing.json', encoding='utf-8'))
want = {}
for p, s, cid in missing:
    want.setdefault((os.path.basename(p).lower(), s), []).append(p)

base = r'\\192.168.100.169\Comun'
skip = {'00. proiecte', '#recycle', '.claude'}
found = {}
for top in os.listdir(base):
    if top.lower() in skip:
        continue
    tp = os.path.join(base, top)
    if not os.path.isdir(tp):
        continue
    for d, _, fs in os.walk(tp):
        for f in fs:
            fp = os.path.join(d, f)
            try:
                k = (f.lower(), os.path.getsize(fp))
            except OSError:
                continue
            if k in want and k not in found:
                found[k] = fp

rest = [m for m in missing if (os.path.basename(m[0]).lower(), m[1]) not in found]
print('gasite in alta parte pe NAS:', len(missing) - len(rest))
print('ramase doar pe Drive:', len(rest), round(sum(m[1] for m in rest) / 1e9, 2), 'GB')
for k, v in Counter('/'.join(p.split('/')[:2]) for p, _, _ in rest).most_common(20):
    print(v, k)
json.dump({'found': [[want[k], v] for k, v in found.items()], 'rest': rest},
          open('find_result.json', 'w', encoding='utf-8'), ensure_ascii=False)
