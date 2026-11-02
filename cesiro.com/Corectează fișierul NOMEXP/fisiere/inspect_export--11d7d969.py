import zipfile,xml.etree.ElementTree as E,json,pathlib,collections
P=pathlib.Path(r"Z:\00.Roboti\cesiro.com\outputs\nomexp_5900_20261020\NOMEXP_SKU_5900_corectat.xlsx")
N="http://schemas.openxmlformats.org/spreadsheetml/2006/main";Q=lambda s:"{"+N+"}"+s
with zipfile.ZipFile(P) as z:
    for n in ["xl/worksheets/sheet1.xml","xl/worksheets/sheet2.xml","xl/worksheets/sheet4.xml"]:
        root=E.fromstring(z.read(n)); print(n)
        fs=[(c.get("r"),dict(c.find(Q("f")).attrib),c.find(Q("f")).text) for c in root.iter(Q("c")) if c.find(Q("f")) is not None]
        print(json.dumps(fs[:14],ensure_ascii=False))
        print("FORMULA TYPES",collections.Counter(f[1].get("t","normal") for f in fs))
        print("PANE",E.tostring(root.find(Q("sheetViews")),encoding="unicode"))
    for n in [f for f in z.namelist() if f.startswith("xl/tables/table")]:
        root=E.fromstring(z.read(n))
        print(n,root.attrib)
        print("COLS",json.dumps([(c.attrib,c.findtext(Q("calculatedColumnFormula"))) for c in root.iter(Q("tableColumn"))],ensure_ascii=False)[:4000])
