import json,re,zipfile,posixpath,collections,sys
from pathlib import Path
from xml.etree import ElementTree as ET
from openpyxl.formula.translate import Translator
SRC=Path(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx")
OUT=Path(__file__).parent
NS={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
r={"sheets":[],"defined_names":[],"formula_issues":[],"cache_errors":[],"external_links":[]}
fs=[]; cells={}
with zipfile.ZipFile(SRC) as z:
    root=ET.fromstring(z.read("xl/workbook.xml"))
    rels={el.attrib["Id"]:el.attrib["Target"] for el in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    ss=[]
    if "xl/sharedStrings.xml" in z.namelist():
        for _,el in ET.iterparse(z.open("xl/sharedStrings.xml"),events=("end",)):
            if el.tag==f"{{{NS['m']}}}si":
                ss.append("".join(t.text or "" for t in el.findall(".//m:t",NS)));el.clear()
    for s in root.findall("m:sheets/m:sheet",NS):
        title=s.attrib["name"]; target=rels[s.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
        path=target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/"+target)
        info={"name":title,"formula_count":0,"formula_examples":[],"text_examples":[],"functions":collections.Counter(),"path":path,"error_counts":collections.Counter()}
        shared={}; scells={}; formulas={}
        for _,c in ET.iterparse(z.open(path),events=("end",)):
            if c.tag==f"{{{NS['m']}}}dimension": info["dims"]=c.attrib.get("ref")
            if c.tag!=f"{{{NS['m']}}}c":continue
            addr=c.attrib["r"]; cv=c.find("m:v",NS); cv=cv.text if cv is not None else None
            typ=c.attrib.get("t")
            if typ=="s" and cv is not None:cv=ss[int(cv)]
            elif typ=="inlineStr":cv="".join(t.text or "" for t in c.findall(".//m:t",NS))
            f=c.find("m:f",NS)
            if f is not None:
                form=f.text
                if f.attrib.get("t")=="shared":
                    si=f.attrib["si"]
                    if form: shared[si]=(addr,form)
                    elif si in shared:
                        origin,base=shared[si];form=Translator("="+base,origin=origin).translate_formula(addr)[1:]
                    else:form="MISSING_SHARED_FORMULA"
                if form is None:form=""
                fs.append([title,addr,form,cv]);formulas[addr]=form
                info["formula_count"]+=1
                info["functions"].update(x.upper() for x in re.findall(r"(?<![A-Za-z0-9_\.])([A-Za-z_][A-Za-z0-9_\.]*)\s*\(",form))
                if len(info["formula_examples"])<12:info["formula_examples"].append([addr,form,cv])
                if "#REF!" in form or "[" in form: r["formula_issues"].append([title,addr,form])
            elif isinstance(cv,str) and len(info["text_examples"])<50:info["text_examples"].append([addr,cv])
            if typ=="e":r["cache_errors"].append([title,addr,cv]);info["error_counts"][cv]+=1
            if cv is not None or f is not None:scells[addr]=[cv,typ]
            c.clear()
        cells[title]={"cells":scells,"formulas":formulas}
        r["sheets"].append(info)
        print(title,info["dims"],info["formula_count"],dict(info["error_counts"]),flush=True)
    for d in root.findall("m:definedNames/m:definedName",NS):r["defined_names"].append([d.attrib,d.text])
    r["external_links"]=[name for name in z.namelist() if "externalLinks" in name]
    r["external_link_xml"]={name:z.read(name).decode() for name in r["external_links"] if name.endswith(".rels")}
    r["package_parts"]=[name for name in z.namelist() if any(k in name for k in ["calcChain","pivot","connections","query","vba"])]
    r["calculation"]=root.find("m:calcPr",NS).attrib
r["total_formulas"]=len(fs)
(OUT/"inventory.json").write_text(json.dumps(r,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
(OUT/"formulas.json").write_text(json.dumps(fs,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"cells.json").write_text(json.dumps(cells,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print("Total formulas",len(fs),"formula issues",len(r["formula_issues"]),"cache errors",len(r["cache_errors"]))
