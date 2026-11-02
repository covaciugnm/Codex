import sqlite3,json,sys
p=r'D:\Codex\iFLYTEK-audit\prior\extracted\catalog-apk.sqlite' if len(sys.argv)==1 else r'D:\Codex\iFLYTEK-audit\results\catalog.sqlite'
c=sqlite3.connect(p)
if len(sys.argv)<3:print(json.dumps(c.execute("select name,sql from sqlite_master where type='table'").fetchall(),indent=2))
else:
 cur=c.execute(sys.argv[2]);print(json.dumps([dict(zip([x[0] for x in cur.description],r)) for r in cur.fetchall()],indent=2,ensure_ascii=True))
