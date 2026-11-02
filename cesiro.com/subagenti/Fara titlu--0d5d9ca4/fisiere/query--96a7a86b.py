import json,re,collections,pathlib
p=pathlib.Path(__file__).parent
d=json.loads((p/"selected_sheets.json").read_text(encoding="utf-8"))
def v(s,r,c):return d[s].get(str(r),{}).get(c+str(r),{}).get("v")
def row(s,r):return {a:{"v":c["v"],"f":c["f"]} for a,c in d[s].get(str(r),{}).items() if c["v"] is not None or c["f"]}
for s in ["NOMEXP02","SORTAT","ARS","GLAZ","BISC","CRUD"]:
    errs={}
    for r,rs in d[s].items():
        for a,c in rs.items():
            if c["type"]=="e":
                form=re.sub(r"\d+","@",c["f"] or "(constant)")
                errs.setdefault(form,[]).append(a)
    print(s,json.dumps({f:{"count":len(cs),"cells":cs[:12]} for f,cs in errs.items()},ensure_ascii=False))
    representatives={str(re.search(r"\d+",cs[0]).group()) for cs in errs.values()}
    for r in sorted(representatives,key=int): print(r,json.dumps(row(s,r),ensure_ascii=False))
