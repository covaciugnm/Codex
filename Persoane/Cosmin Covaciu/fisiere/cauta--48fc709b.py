import sys,sqlite3,json
from pathlib import Path
base=Path(__file__).resolve().parent
query=' '.join(sys.argv[1:]).strip()
if not query:raise SystemExit('Utilizare: cauta.py text cautat')
c=sqlite3.connect(base/'inventar.sqlite',timeout=60)
rows=c.execute('''select s.sha256,s.text,d.text_path from search s join documents d using(sha256) where lower(s.text) like lower(?)''',('%'+query+'%',))
for sha,text,path in rows:
    pos=text.lower().find(query.lower())
    print(json.dumps({'sha256':sha,'sources':[r[0] for r in c.execute('select path from files where sha256=?',(sha,))],'text':str(base/path),'context':text[max(0,pos-180):pos+650]},ensure_ascii=False))
