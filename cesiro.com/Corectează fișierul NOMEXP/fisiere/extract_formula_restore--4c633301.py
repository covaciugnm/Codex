import zipfile,xml.etree.ElementTree as E,pathlib,json,re,collections
P=pathlib.Path(r"Z:\00.Roboti\cesiro.com")
N="http://schemas.openxmlformats.org/spreadsheetml/2006/main";Q=lambda s:"{"+N+"}"+s
blocks=[]
with zipfile.ZipFile(P/"outputs/nomexp_5900_20261020/NOMEXP_SKU_5900_corectat.xlsx") as z:
 for sn,name in [(1,"SKU_5900"),(2,"NOMEXP02_5900"),(4,"Corectii")]:
    root=E.fromstring(z.read(f"xl/worksheets/sheet{sn}.xml"));cols=collections.defaultdict(list)
    for c in root.iter(Q("c")):
        f=c.find(Q("f"))
        if f is not None:cols[re.match("[A-Z]+",c.get("r"))[0]].append((int(re.search(r"\d+",c.get("r"))[0]),"="+f.text))
    for col,values in cols.items():
        values.sort();ranges=[];current=[]
        for row,f in values:
            if current and row!=current[-1][0]+1:ranges.append(current);current=[]
            current.append((row,f))
        if current:ranges.append(current)
        for rs in ranges:blocks.append({"sheet":name,"range":f"{col}{rs[0][0]}:{col}{rs[-1][0]}","formulas":[[f] for _,f in rs]})
(P/"work_nomexp/formula_restore.json").write_text(json.dumps(blocks,ensure_ascii=False),encoding="utf8")
print("Formula blocks:",len(blocks),"Formula cells:",sum(len(b["formulas"]) for b in blocks))
