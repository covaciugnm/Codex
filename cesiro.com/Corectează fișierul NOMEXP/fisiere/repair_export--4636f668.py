"""Normalize the exporter XML namespace and preserve duplicate source headers as ranges."""
import zipfile,pathlib,re,xml.etree.ElementTree as E,json
P=pathlib.Path(r"Z:\00.Roboti\cesiro.com\outputs\nomexp_5900_20261020\NOMEXP_SKU_5900_corectat.xlsx")
W=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp")
src=P.read_bytes()
(W/"artifact_export_before_compatibility.xlsx").write_bytes(src)
N="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
parts={}
with zipfile.ZipFile(P) as z:
    for name in z.namelist():
        content=z.read(name)
        if name.endswith(".xml"):
            text=content.decode("utf-8-sig")
            if f'xmlns:x="{N}"' in text:
                text=text.replace(f'xmlns:x="{N}"',f'xmlns="{N}"')
                text=re.sub(r"(<\/?)x:",r"\1",text)
            # Excel table columns must be unique ignoring case. The source schema
            # intentionally repeats this header, so retain these as filtered ranges.
            if name in ["xl/worksheets/sheet2.xml","xl/worksheets/sheet5.xml"]:
                text=re.sub(r"<tableParts\b.*?</tableParts>","",text,flags=re.S)
                ref="A1:AF367" if "sheet2" in name else "A6:AG373"
                text=text.replace("</sheetData>",f'</sheetData><autoFilter ref="{ref}" />')
            if name=="[Content_Types].xml":
                text=re.sub(r'<Override\b[^>]*PartName="/xl/tables/table(?:2|6)\.xml"[^>]*/>',"",text)
            content=text.encode("utf8")
        if name in ["xl/worksheets/_rels/sheet2.xml.rels","xl/worksheets/_rels/sheet5.xml.rels"]:
            # These two relationships files contain only their one table relation.
            root=E.fromstring(content)
            for e in list(root):
                if e.get("Type","").endswith("/table"):root.remove(e)
            content=E.tostring(root,encoding="utf8",xml_declaration=True)
        if name not in ["xl/tables/table2.xml","xl/tables/table6.xml"]:
            parts[name]=content
tmp=P.with_suffix(".tmp")
with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
    for name,content in parts.items():z.writestr(name,content)
tmp.replace(P)
print(json.dumps({"namespace":"default SpreadsheetML namespace","duplicate_header_tables":"converted to worksheet filters","parts":len(parts)}))
