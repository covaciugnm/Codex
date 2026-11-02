import json,re,collections
from pathlib import Path
p=Path(__file__).parent
cells=json.loads((p/"cells.json").read_text(encoding="utf-8"))
inv=json.loads((p/"inventory.json").read_text(encoding="utf-8"))
def cv(s,a):return cells[s]["cells"].get(a,[None,None])[0]
def fm(s,a):return cells[s]["formulas"].get(a)
def row(s,r,cols="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
 return {f"{c}{r}":[cv(s,f"{c}{r}"),fm(s,f"{c}{r}")] for c in cols if cv(s,f"{c}{r}") is not None or fm(s,f"{c}{r}")}
def show(s,rows,cols="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
 print("\nSHEET",s)
 for r in rows:print(row(s,r,cols))
for s in ["DubluriLinii","NOMEXP02 - PRET","NOMEXP02 - GLAZ","NOMEXP02 - DEC"]:
 er=[a for sh,a,v in inv["cache_errors"] if sh==s]
 rs=sorted(set(int(re.search(r"\d+",a).group()) for a in er))
 rawcols=["O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE"]
 withdata=[r for r in rs if any(cv(s,f"{c}{r}") not in (None,"") for c in rawcols)]
 print(s,"error rows",len(rs),"minmax",min(rs),max(rs),"with inputs",len(withdata),withdata[:20])
 show(s,[min(rs)-1,min(rs),max(rs)],["A","D","F","G","I","M","N","O","Q","S","V","AF"])
for s in ["NOMEXP02","BISC","LISGL1","GLAZ","ARS","CRUD","SORTAT"]:
 er=[(a,v) for sh,a,v in inv["cache_errors"] if sh==s]
 group=collections.defaultdict(list)
 for a,v in er:group[re.sub(r"\d","",a)+":"+v].append(a)
 print(s,"errors",{k:[len(x),x[:5],x[-5:]] for k,x in group.items()})
 show(s,[1,2])
show("NOMEXP02",sorted(set(int(re.search(r"\d+",a).group()) for sh,a,v in inv["cache_errors"] if sh=="NOMEXP02" and v=="#REF!")),["A","D","F","G","I","M","N","O","Q","S","V","AF"])
show("BISC",sorted(set(int(re.search(r"\d+",a).group()) for sh,a,v in inv["cache_errors"] if sh=="BISC" and v=="#VALUE!")),["A","B","D","J","K","O","P"])
show("LISGL1",range(1,7),["A","B","C","D","H","O","P","Q","R","S","T","U","V"])
show("NOMU",range(1,7),["A","B","C","D","E","F","G","H","I","J","O","P","Q","R","S","T","U"])
