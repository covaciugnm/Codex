import sqlite3, os, json
from collections import Counter

os.chdir(os.path.dirname(os.path.abspath(__file__)))
c = sqlite3.connect('metadata_sqlite_db')
kids = {}
for i, p in c.execute('select item_stable_id,parent_stable_id from stable_parents'):
    kids.setdefault(p, []).append(i)
info = {r[0]: r[1:] for r in c.execute('select stable_id,local_title,is_folder,file_size,id from items')}
out = []


def walk(sid, path):
    for k in kids.get(sid, []):
        if k not in info:
            continue
        t, f, s, cid = info[k]
        p = path + '/' + (t or '')
        if f:
            walk(k, p)
        else:
            out.append((p, s or 0, cid))


walk(121540, '')
json.dump(out, open('drive_tree.json', 'w', encoding='utf-8'))
nas = r'\\192.168.100.169\Comun\00. Proiecte'
loc = {}
for d, _, fs in os.walk(nas):
    rel = d[len(nas):].replace(os.sep, '/')
    for f in fs:
        try:
            loc[(rel + '/' + f).lower()] = os.path.getsize(os.path.join(d, f))
        except OSError:
            loc[(rel + '/' + f).lower()] = -1
print('Drive:', len(out), 'fisiere', round(sum(s for _, s, _ in out) / 1e9, 2), 'GB')
print('NAS  :', len(loc), 'fisiere', round(sum(v for v in loc.values() if v > 0) / 1e9, 2), 'GB')
missing = [(p, s, cid) for p, s, cid in out if p.lower() not in loc]
diff = [(p, s, loc[p.lower()]) for p, s, _ in out if p.lower() in loc and s and loc[p.lower()] != s]
print('pe Drive dar NU pe NAS:', len(missing), round(sum(s for _, s, _ in missing) / 1e9, 2), 'GB')
print('marime diferita:', len(diff))
for k, v in Counter('/'.join(p.split('/')[:2]) for p, _, _ in missing).most_common(25):
    print(v, k)
json.dump(missing, open('missing.json', 'w', encoding='utf-8'))
json.dump(diff, open('diff.json', 'w', encoding='utf-8'))
