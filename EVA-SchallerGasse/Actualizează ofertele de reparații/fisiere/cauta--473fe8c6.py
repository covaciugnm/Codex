"""Caută în textele deja extrase, fără recitirea documentelor originale."""
from pathlib import Path
import argparse,sqlite3,json
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('query',help='Expresie SQLite FTS5, de exemplu: Bauwerksbuch sau "Schallergasse 35"')
p.add_argument('--folder',default='',help='Filtru cale relativă')
p.add_argument('--limit',type=int,default=12)
a=p.parse_args()
db=sqlite3.connect(Path(__file__).resolve().parent/'cautare.sqlite')
rows=db.execute("SELECT cale,descriere,snippet(documente,2,'[',']',' … ',50),sha256 FROM documente WHERE documente MATCH ? AND cale LIKE ? ORDER BY rank LIMIT ?",(a.query,'%'+a.folder+'%',a.limit)).fetchall()
print(json.dumps([dict(cale=r[0],descriere=r[1],fragment=r[2],sha256=r[3]) for r in rows],ensure_ascii=False,indent=2))
