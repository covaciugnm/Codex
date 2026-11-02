import json,re,collections,zipfile
from pathlib import Path
p=Path(__file__).parent
d=json.loads((p/"cells.json").read_text(encoding="utf-8"))
inv=json.loads((p/"inventory.json").read_text(encoding="utf-8"))
def cv(s,a):return d[s]["cells"].get(a,[None,None])[0]
def fm(s,a):return d[s]["formulas"].get(a)
def row(s,r,cols):
 return {c:[cv(s,f"{c}{r}"),fm(s,f"{c}{r}")] for c in cols}
forms={}
for sh in ["Codificare forme","Adaugare forme","ADAUGARE FORME 1"]:
 m=collections.defaultdict(set)
 for a,(v,t) in d[sh]["cells"].items():
  if a.startswith("A") and a[1:].isdigit() and v:
   val=cv(sh,"C"+a[1:])
   if val:m[v].add(val)
 forms[sh]=m
print("FORMS",[(sh,len(m),{k:list(v) for k,v in m.items() if len(v)>1}) for sh,m in forms.items()])
out={"external1":[],"external2":[],"beneficiaries":[],"names_issues":[]}
for sh,addr,f in inv["formula_issues"]:
 if "[1]" in f:
  r=re.search(r"\d+",addr).group();key=cv(sh,"D"+r)
  out["external1"].append({"sheet":sh,"cell":addr,"key":key,"cached":cv(sh,addr),"local":list(forms["ADAUGARE FORME 1"].get(key,()))})
 elif "[2]" in f:
  r=re.search(r"\d+",addr).group()
  out["external2"].append({"sheet":sh,"cell":addr,"key":cv(sh,"A"+r),"cached":cv(sh,addr),"formula":f})
ben=collections.defaultdict(set)
for sh in ["NOMEXP02","DubluriLinii","NOMEXP02 - DEC","NOMEXP02 - GLAZ","NOMEXP02 - PRET","Greutati"]:
 for a,(v,t) in d[sh]["cells"].items():
  if a.startswith("P") and a[1:].isdigit() and v:
   b=cv(sh,"O"+a[1:])
   if b:ben[v].add(b)
lis=collections.Counter(cv("LISGL1",f"D{r}") for r in range(2,784))
for name,count in lis.items():out["beneficiaries"].append({"name":name,"rows":count,"codes":list(ben.get(name,()))})
for attrs,txt in inv["defined_names"]:
 if "#REF!" in txt:out["names_issues"].append([attrs,txt])
print("external1",out["external1"])
print("external2 firstlast",out["external2"][:3],out["external2"][-3:])
print("beneficiaries",out["beneficiaries"])
print("NOMEXP02 2747",row("NOMEXP02",2747,["A","D","I","V"]))
print("GLAZ 1986",row("GLAZ",1986,["A","B","C","D","E","F","G","K","L","M","N"]))
print("GLAZ 2015",row("GLAZ",2015,["A","B","C","D","E","F","G","K","L","M","N"]))
print("NOMEXP02 3243",row("NOMEXP02",3243,["A","B","C","D","F","G","I","J","S","V"]))
print("ARS 3251",row("ARS",3251,["A","B","C","D","E","F"]))
for name in ["FARFURIE INTINSA 26","VAZA","CEASCA 220ML"]:
 print("FORM",name,{s:list(m.get(name,())) for s,m in forms.items()})
(p/"lookup_report.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
