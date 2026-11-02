from read_model import load_model,formula,P
import collections,json,re
m=load_model()
rows=[];s=m["NOMEXP02"]
cols=[chr(i) for i in range(65,91)]+["AA","AB","AC","AD","AE","AF","AG"]
for a,c in s["cells"].items():
    if re.fullmatch(r"A\d+",a) and str(c["v"]).startswith("5900_"):
        r=int(a[1:])
        row={"source_row":r,"values":{col:s["cells"].get(col+str(r),{}).get("v") for col in cols},
            "formulas":{col:formula(s,col+str(r)) for col in cols if formula(s,col+str(r))}}
        rows.append(row)
data={"source_sheet":"NOMEXP02","rows":rows,"headers":{col:s["cells"].get(col+"1",{}).get("v") for col in cols}}
(P/"data_5900.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf8")
print("COUNT",len(rows),"ROWS",min(r["source_row"] for r in rows),max(r["source_row"] for r in rows))
print("FORMULAS",[(r["source_row"],r["formulas"]) for r in rows if r["formulas"]][:20])
print("MISSING",[(col,sum(r["values"][col] in (None,"") for r in rows)) for col in cols])
print("EXAMPLES",json.dumps(rows[:5]+rows[-3:],ensure_ascii=False))
for col in ["H","I","F","G","O","P","AB","AD","AE"]:
    print("DISTINCT",col,json.dumps(collections.Counter(str(r["values"][col]) for r in rows),ensure_ascii=False))
dup=collections.defaultdict(list)
for r in rows:dup[re.sub(r"\s+","",r["values"]["A"])].append(r["source_row"])
print("DUPLICATES",json.dumps({k:v for k,v in dup.items() if len(v)>1}))
