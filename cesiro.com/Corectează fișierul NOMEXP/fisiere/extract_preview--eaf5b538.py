import zipfile, xml.etree.ElementTree as E, pathlib, json, re
P=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp")
NS="http://schemas.openxmlformats.org/spreadsheetml/2006/main";Q=lambda s:"{"+NS+"}"+s
with zipfile.ZipFile(P.parent/"NOMEXP_v9_ultimate.(2).xlsx") as src:
    root=E.fromstring(src.read("xl/worksheets/sheet4.xml"))
    for child in list(root):
        if child.tag in {Q(k) for k in ("drawing","legacyDrawing","pivotTableParts","extLst","autoFilter","conditionalFormatting")}:
            root.remove(child)
    sd=root.find(Q("sheetData"))
    for r in list(sd):
        if int(r.get("r"))>12:sd.remove(r)
        else:
            for c in list(r):
                if re.match(r"[A-Z]+",c.get("r"))[0] not in list("ABCDEFGHIJ"):r.remove(c)
                else:
                    f=c.find(Q("f"))
                    if f is not None:c.remove(f)
    root.find(Q("dimension")).set("ref","A1:J12")
    views=root.find(Q("sheetViews"))
    if views is not None:
        for sv in views:
            for ch in list(sv):sv.remove(ch)
    with zipfile.ZipFile(P/"preview_source.xlsx","w",zipfile.ZIP_DEFLATED) as out:
        out.writestr("[Content_Types].xml",'''<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>''')
        out.writestr("_rels/.rels",'''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>''')
        out.writestr("xl/workbook.xml",f'''<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="NOMEXP02" sheetId="1" r:id="rId1"/></sheets></workbook>''')
        out.writestr("xl/_rels/workbook.xml.rels",'''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>''')
        out.writestr("xl/worksheets/sheet1.xml",E.tostring(root))
        for name in ["xl/styles.xml","xl/sharedStrings.xml"]:out.writestr(name,src.read(name))
