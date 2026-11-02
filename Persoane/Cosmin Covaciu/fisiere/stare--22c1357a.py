import sqlite3,json,time
from pathlib import Path
base=Path(__file__).resolve().parent
c=sqlite3.connect(base/'inventar.sqlite',timeout=60)
print(json.dumps({'files':dict(c.execute('select status,count(*) from files group by status')),'documents':dict(c.execute('select status,count(*) from documents group by status')),'bytes_hashed':c.execute('select sum(size) from files').fetchone()[0],'unique_hashes':c.execute('select count(distinct sha256) from files').fetchone()[0]},ensure_ascii=False,indent=2))
for row in c.execute("select min(f.path),d.status,d.error from documents d join files f using(sha256) where d.status in ('error','partial') group by d.sha256 limit 12"):
    print(json.dumps(row,ensure_ascii=False))
print('Error log:')
if (base/'erori.log').exists():print((base/'erori.log').read_text(encoding='utf-8',errors='replace')[-3000:])
