import json,re,collections
from pathlib import Path
p=Path(__file__).parent
d=json.loads((p/"cells.json").read_text(encoding="utf-8"))
names=set(d)
# Identify local/cross-sheet precedents; string literals are removed before matching.
rx=re.compile(r"(?<![\w.])(?:(?:'((?:[^']|'')+)'|([A-Za-z_][\w. ]*))!)?(\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?|\$?[A-Z]{1,3}:\$?[A-Z]{1,3})(?![\w(])")
def col(c):
 n=0
 for x in c:n=n*26+ord(x)-64
 return n
def xy(a):
 m=re.fullmatch(r"([A-Z]+)(\d+)",a.replace("$",""))
 return col(m[1]),int(m[2])
selfrefs=[];missing=[];edges=collections.defaultdict(set);localcycles=[]
for sh,sd in d.items():
 fs=sd["formulas"]; graph={}
 for addr,f in fs.items():
  clean=re.sub(r'"(?:[^"]|"")*"',"",f)
  deps=[]
  for m in rx.finditer(clean):
   target=(m[1] or m[2] or sh).replace("''","'")
   ref=m[3].replace("$","")
   if target.startswith("["):continue
   if target not in names:
    missing.append([sh,addr,target]);continue
   if target!=sh:edges[sh].add(target);continue
   if ":" not in ref:
    if ref==addr:selfrefs.append([sh,addr,f])
    if ref in fs:deps.append(ref)
   else:
    a,b=ref.split(":")
    ownx,owny=xy(addr)
    if a.isalpha():
     inside=col(a)<=ownx<=col(b)
    else:
     ax,ay=xy(a);bx,by=xy(b);inside=ax<=ownx<=bx and ay<=owny<=by
    if inside:selfrefs.append([sh,addr,f])
  graph[addr]=deps
 state={};stack=[]
 def visit(node):
  s=state.get(node)
  if s==1:
   localcycles.append([sh,stack[stack.index(node):]+[node]]);return
  if s==2:return
  state[node]=1;stack.append(node)
  for dep in graph.get(node,[]):visit(dep)
  stack.pop();state[node]=2
 for node in graph:visit(node)
print("selfrefs",selfrefs[:20],"count",len(selfrefs))
print("missing sheets",missing[:20],"count",len(missing))
print("local cycles",localcycles[:20],"count",len(localcycles))
print("sheet graph",{k:list(v) for k,v in edges.items()})
out={"direct_self_references":selfrefs,"missing_sheets":missing,"same_sheet_cycles_single_cell_refs":localcycles,"sheet_dependencies":{k:sorted(v) for k,v in edges.items()},"scope":"Regex static scan excludes dynamic reference functions and expands no ranges into graph nodes. Same-sheet direct single-cell cycles plus self-including ranges checked."}
(p/"cycle_report.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
