import openpyxl, collections, json, pathlib, re

src = pathlib.Path(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx")
out = pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
out.mkdir(parents=True, exist_ok=True)
w = openpyxl.load_workbook(src, read_only=True, data_only=True)
rows = {s.title: list(s.iter_rows(values_only=True)) for s in w}

def nonempty(v): return v is not None and str(v).strip() != ""
def duplicate_groups(data, cols, start=2):
    d = collections.defaultdict(list)
    for i,r in enumerate(data[start-1:], start):
        vals = tuple(r[c] if c < len(r) else None for c in cols)
        if any(nonempty(v) for v in vals): d[vals].append(i)
    return [{"key":list(k), "rows":v} for k,v in d.items() if len(v)>1]

summary={}
for n,rs in rows.items():
    present = [(i,r) for i,r in enumerate(rs,1) if any(nonempty(v) for v in r)]
    errs = [(i,openpyxl.utils.get_column_letter(j),v) for i,r in present for j,v in enumerate(r,1) if isinstance(v,str) and v in {'#REF!','#N/A','#VALUE!','#DIV/0!','#NAME?','#NUM!','#NULL!'}]
    summary[n] = {
        "rows_including_headers":len(present),
        "last_row_with_value":present[-1][0] if present else None,
        "errors":len(errs),"error_examples":errs[:10],
        "duplicate_colA_groups":len(duplicate_groups(rs,[0])),
        "exact_duplicate_groups":len(duplicate_groups(rs,list(range(len(rs[0]))))) if rs else 0,
        "top_colA_duplicates":sorted(duplicate_groups(rs,[0]),key=lambda x:-len(x['rows']))[:5],
    }

detail={}
for n in ["NOMEXP02","FINAL_NOMEXP","NOMEXP02 - PRET","NOMEXP02 - GLAZ","NOMEXP02 - DEC","Greutati","NOMU","SORTAT","ARS","GLAZ","BISC","CRUD","SEMIF.ARS","SEMIF.GLAZ","SEMIF.BISC","SEMIF.CRUD"]:
    rs=rows[n]
    headers=rs[0]
    cols={}
    for j,h in enumerate(headers):
        if not nonempty(h): continue
        vals=[(i,r[j]) for i,r in enumerate(rs[1:],2) if any(nonempty(x) for x in r)]
        vals_non=[(i,v) for i,v in vals if nonempty(v)]
        types=collections.Counter(type(v).__name__ for i,v in vals_non)
        cnt=collections.Counter(str(v) for i,v in vals_non)
        numeric=[(i,v) for i,v in vals_non if isinstance(v,(int,float))]
        cols[openpyxl.utils.get_column_letter(j+1)]={
            "header":h,"nonempty":len(vals_non),"blank":len(vals)-len(vals_non),
            "types":dict(types),"distinct":len(cnt),"top":cnt.most_common(12),
            "zero":sum(v==0 for i,v in numeric),
            "negative":[[i,v] for i,v in numeric if v<0][:20],
            "whitespace":[[i,v] for i,v in vals_non if isinstance(v,str) and v!=v.strip()][:20],
            "replacement_character":[[i,v] for i,v in vals_non if isinstance(v,str) and '\ufffd' in v][:20],
        }
    detail[n]=cols

# Duplicates and inconsistencies in lookup tables
lookups={}
for n,col,targetcols,start in [
    ("Greutati",0,[1,2,14,15],2),("NOMU",1,[2,3,9,10],2),
    ("Codificare forme",0,[2],4),("Adaugare forme",0,[2],1),
    ("ADAUGARE FORME 1",0,[2],2),("Codificare 1 Glazuri",0,[1],4),
    ("GLAZURI SETURI",0,list(range(1,10)),2),
    ("COD CULOARE COD",0,[1],2),("cod glazura cu dec",0,[1,2,3],2),
]:
    rs=rows[n]; groups=duplicate_groups(rs,[col],start)
    conflicts=[]
    for g in groups:
        variants=collections.defaultdict(list)
        for i in g['rows']:
            variants[tuple(rs[i-1][c] for c in targetcols)].append(i)
        if len(variants)>1: conflicts.append({"key":g['key'],"variants":[{"values":k,"rows":v} for k,v in variants.items()]})
    lookups[n]={"duplicate_groups":groups, "conflicts":conflicts}

# Final code consistency against fields
final=rows["FINAL_NOMEXP"]
final_issues={}
final_issues["codificare_vs_fields"]=[]
final_issues["nr1_vs_fields"]=[]
final_issues["category_vs_group"]=[]
for i,r in enumerate(final[1:],2):
    if not nonempty(r[0]): continue
    exp=f"{r[22]}_{r[9]}_{r[6]}_A"
    expnr=f"{r[16]}_{r[22]}_{r[9]}_{r[6]}"
    if r[0]!=exp: final_issues["codificare_vs_fields"].append([i,r[0],exp])
    if r[1]!=expnr: final_issues["nr1_vs_fields"].append([i,r[1],expnr])
    if isinstance(r[9],(int,float)):
        expcat="PF.SC" if r[9]<9001 else "PF.C"
        if r[8]!=expcat:final_issues["category_vs_group"].append([i,r[8],expcat])

for fn,data in [("summary.json",summary),("detail.json",detail),("lookups.json",lookups),("final_issues.json",final_issues)]:
    (out/fn).write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
print("LOOKUP CONFLICT COUNTS", {n:len(x["conflicts"]) for n,x in lookups.items()})
print("FINAL ISSUES", {k:len(v) for k,v in final_issues.items()})
