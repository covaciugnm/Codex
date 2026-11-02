import zipfile, xml.etree.ElementTree as E, json, collections, pathlib
P=pathlib.Path(r"Z:\00.Roboti\cesiro.com")
F=P/"NOMEXP_v9_ultimate.(2).xlsx"
N={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
q=lambda s:"{"+N["m"]+"}"+s
with zipfile.ZipFile(F) as z:
    shared=[]
    if "xl/sharedStrings.xml" in z.namelist():
        with z.open("xl/sharedStrings.xml") as f:
            for _,e in E.iterparse(f,events=("end",)):
                if e.tag==q("si"):
                    shared.append("".join(t.text or "" for t in e.iter(q("t"))));e.clear()
    rels={x.get("Id"):x.get("Target") for x in E.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    wb=E.fromstring(z.read("xl/workbook.xml"))
    out={"size":F.stat().st_size,"parts":len(z.namelist()),"sheets":[],"names":[dict(x.attrib,text=x.text) for x in wb.findall("m:definedNames/m:definedName",N)],"calc":None}
    calc=wb.find("m:calcPr",N)
    if calc is not None:out["calc"]=calc.attrib
    for sh in wb.findall("m:sheets/m:sheet",N):
        target=rels[sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")]
        path=target.lstrip("/") if target.startswith("/") else "xl/"+target
        root=E.fromstring(z.read(path))
        vals=[]; fc=collections.Counter();errs=[];cells=0;filled=0;maxrow=0;types=collections.Counter()
        for c in root.iter(q("c")):
            cells+=1;f=c.find(q("f"));v=c.find(q("v"));t=c.get("t","n")
            text=v.text if v is not None else None
            if t=="s" and text is not None:text=shared[int(text)]
            if t=="inlineStr":text="".join(x.text or "" for x in c.iter(q("t")))
            if f is not None:
                fc["total"]+=1;fc[f.get("t","normal")]+=1
                if not text:fc["no_cache"]+=1
            if text is not None or f is not None:
                filled+=1;row=int("".join(filter(str.isdigit,c.get("r"))));maxrow=max(maxrow,row);types[t]+=1
                if row<=8 or (len(vals)<16):vals.append([c.get("r"),text, f.text if f is not None else None])
            if t=="e":errs.append([c.get("r"),text])
        desc=dict(sh.attrib)
        desc.update(path=path,dim=root.find(q("dimension")).get("ref") if root.find(q("dimension")) is not None else None,
                    cells=cells,filled=filled,maxrow=maxrow,formulas=dict(fc),types=dict(types),
                    errors_count=len(errs),errors=errs[:12],sample=vals[:150],
                    merges=[x.get("ref") for x in root.findall("m:mergeCells/m:mergeCell",N)][:20],
                    validations=len(root.findall("m:dataValidations/m:dataValidation",N)),
                    cf=len(root.findall("m:conditionalFormatting",N)),tables=len(root.findall("m:tableParts/m:tablePart",N)))
        out["sheets"].append(desc)
    out["special_parts"]=[x for x in z.namelist() if any(a in x for a in ["externalLink","pivot","vba","drawing","table","connection"])]
    (P/"work_nomexp"/"inventory.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps({**out,"sheets":[{k:v for k,v in s.items() if k not in ["sample"]} for s in out["sheets"]]},ensure_ascii=False))
    for s in out["sheets"]:
        print("\nSAMPLE",s["name"],json.dumps(s["sample"][:70],ensure_ascii=False))
