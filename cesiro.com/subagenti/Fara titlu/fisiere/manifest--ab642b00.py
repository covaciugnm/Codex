import json,re,zipfile,collections
from pathlib import Path
from xml.etree import ElementTree as E
p=Path(__file__).parent
d=json.loads((p/"cells.json").read_text(encoding="utf-8"))
inv=json.loads((p/"inventory.json").read_text(encoding="utf-8"))
def cv(s,a):return d[s]["cells"].get(a,[None,None])[0]
def fm(s,a):return d[s]["formulas"].get(a)
out=[]
def add(sheet,cell,new,reason,expected=None):
 out.append(dict(sheet=sheet,cell=cell,old_formula=fm(sheet,cell),old_cache=cv(sheet,cell),new_formula="="+new,expected=expected,reason=reason))
for sh,addr,f in inv["formula_issues"]:
 if "[1]" in f:
  add(sh,addr,f.replace("'[1]ADAUGARE FORME 1'!A:C","'ADAUGARE FORME 1'!$A$2:$C$869"),"Cheie univocă identică în nomenclatorul local; rezultat verificat cu cache sursă.",cv(sh,addr))
glazes=collections.defaultdict(set)
for r in range(4,189):
 if cv("Codificare 1 Glazuri",f"A{r}") is not None:glazes[cv("Codificare 1 Glazuri",f"A{r}")].add(cv("Codificare 1 Glazuri",f"B{r}"))
for sh,addr,err in inv["cache_errors"]:
 if sh=="NOMEXP02" and err=="#REF!" and addr.startswith("G"):
  r=addr[1:];key=cv(sh,"F"+r);matches=list(glazes.get(key,()))
  assert len(matches)==1,(addr,key,matches)
  add(sh,addr,f"VLOOKUP(F{r},'Codificare 1 Glazuri'!$A$4:$B$188,2,0)","Coloana întoarsă 3 depășea intervalul de 2 coloane; intervalul glisa neancorat. Cheie verificată în nomenclator.",matches[0])
add("NOMEXP02","I2747","VLOOKUP(D2747,'Adaugare forme'!$A$2:$C$224,3,0)","Denumire exactă absentă din ADAUGARE FORME 1, dar prezentă în Adaugare forme r195 și Codificare forme r182 cu același cod 9049.","9049")
(p/"safe_formula_manifest.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
ns={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with zipfile.ZipFile(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx") as z:
 e=E.fromstring(z.read("xl/externalLinks/externalLink2.xml"))
 erows={}
 for row in e.findall(".//m:row",ns):
  dat={re.sub(r"\d+","",c.attrib["r"]):c.findtext("m:v",namespaces=ns) for c in row}
  if dat.get("G"):erows[dat["G"]]=dat
 matches=[]
 for r in range(1986,2016):
  key=cv("GLAZ",f"A{r}")
  exact=erows.get(key)
  near=[v for k,v in erows.items() if k.strip()==key.strip()]
  matches.append([r,key,exact,near])
 print("external2 cache rows",len(erows),"matched",sum(x[2] is not None for x in matches))
 print("external2 sample keys",list(erows)[:5],list(erows)[-5:])
 (p/"external2_cache_match.json").write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding="utf-8")
print("Safe manifest",len(out),"cells. Expected",[(x["cell"],x["expected"]) for x in out[38:]])
