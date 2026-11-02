import json, zipfile, xml.etree.ElementTree as E, collections, pathlib, re
src=pathlib.Path(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx")
out=src.parent/"work_nomexp"/"audit_flux"
out.mkdir(exist_ok=True)
ns={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
sel=["SORTAT","ARS","GLAZ","BISC","CRUD","LISGL1","NOMEXP02","FINAL_NOMEXP","Greutati","Codificare forme","Codificare 1 Glazuri","Adaugare forme","NOMU","5358","CRUD PT VLOOK","ADAUGARE FORME 1","SEMIF.ARS","SEMIF.GLAZ","SEMIF.BISC","SEMIF.CRUD","Defalcat","GLAZURI SETURI","COD CULOARE COD","cod glazura cu dec"]
with zipfile.ZipFile(src) as z:
    shared=["".join(t.itertext()) for t in E.fromstring(z.read("xl/sharedStrings.xml"))]
    rels={r.attrib["Id"]:r.attrib["Target"] for r in E.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    sheets={}
    for sheet in E.fromstring(z.read("xl/workbook.xml")).find("m:sheets",ns):
        if sheet.attrib["name"] not in sel: continue
        rid=sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        path=rels[rid]
        if not path.startswith("xl/"): path="xl/"+path.lstrip("/")
        root=E.fromstring(z.read(path))
        rows={}
        for row in root.findall("m:sheetData/m:row",ns):
            cells={}
            for c in row:
                if c.tag.rsplit("}",1)[-1]!="c":continue
                v=c.find("m:v",ns)
                v=v.text if v is not None else None
                if c.attrib.get("t")=="s":v=shared[int(v)] if v else None
                if c.attrib.get("t")=="inlineStr":v="".join(c.find("m:is",ns).itertext())
                f=c.find("m:f",ns)
                cells[c.attrib["r"]]={"v":v,"f":None if f is None else f.text,"type":c.attrib.get("t"),"style":c.attrib.get("s"),"fa":None if f is None else f.attrib}
            rows[row.attrib["r"]]=cells
        from openpyxl.formula.translate import Translator
        masters={}
        for row in rows.values():
            for addr,c in row.items():
                if c["fa"] and c["fa"].get("t")=="shared":
                    si=c["fa"]["si"]
                    if c["f"] is not None:masters[si]=(addr,c["f"])
                    else:
                        a,f=masters[si]
                        c["f"]=Translator("="+f, origin=a).translate_formula(addr)[1:]
        sheets[sheet.attrib["name"]]=rows
(out/"selected_sheets.json").write_text(json.dumps(sheets,ensure_ascii=False,indent=2),encoding="utf-8")
for s,rows in sheets.items():
    stats=collections.Counter(c["v"] for row in rows.values() for c in row.values() if c["type"]=="e")
    print(s,len(rows),"rows",sum(len(r) for r in rows.values()),"cells",stats)
    print("headers:",json.dumps({a:c["v"] for a,c in next(iter(rows.values())).items()},ensure_ascii=False))
