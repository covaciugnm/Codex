import zipfile, xml.etree.ElementTree as ET, json, pathlib, re, pickle
from openpyxl.formula.translate import Translator
P=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp")
NS="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
Q=lambda s:"{"+NS+"}"+s
def load_model():
    cache=P/"model.pkl"
    if cache.exists():return pickle.loads(cache.read_bytes())
    inv=json.loads((P/"inventory.json").read_text(encoding="utf8"))
    model={}
    with zipfile.ZipFile(P.parent/"NOMEXP_v9_ultimate.(2).xlsx") as z:
        ss=[]
        for _,e in ET.iterparse(z.open("xl/sharedStrings.xml"),events=("end",)):
            if e.tag==Q("si"):ss.append("".join(t.text or "" for t in e.iter(Q("t"))));e.clear()
        for sh in inv["sheets"]:
            cells={};shared={}
            for _,e in ET.iterparse(z.open(sh["path"]),events=("end",)):
                if e.tag!=Q("c"):continue
                a=e.get("r");t=e.get("t","n");f=e.find(Q("f"));v=e.find(Q("v"))
                val=v.text if v is not None else None
                if t=="s" and val is not None:val=ss[int(val)]
                elif t=="inlineStr":val="".join(c.text or "" for c in e.iter(Q("t")))
                elif t=="n" and val is not None:
                    n=float(val);val=int(n) if n.is_integer() else n
                elif t=="b":val=val=="1"
                formula=None;si=None
                if f is not None:
                    formula=f.text;si=f.get("si")
                    if si is not None and formula:shared[si]=(a,formula)
                if val is not None or f is not None:cells[a]={"v":val,"t":t,"f":formula,"si":si}
                e.clear()
            model[sh["name"]]={"cells":cells,"shared":shared,"path":sh["path"],"dim":sh["dim"]}
            print("Loaded",sh["name"],len(cells),flush=True)
    cache.write_bytes(pickle.dumps(model))
    return model
def formula(sheet,a):
    c=sheet["cells"].get(a,{})
    if c.get("f"):return "="+c["f"]
    if c.get("si") is not None:
        origin, f=sheet["shared"][c["si"]]
        return Translator("="+f,origin=origin).translate_formula(a)
    return None
if __name__=="__main__":
    m=load_model()
    for sn,rows in {
        "NOMEXP02":[2723,2724,2801,2863,3135,3500,3615],
        "NOMEXP02 - PRET":[2343,2344,15428,15429,15438],
        "NOMEXP02 - DEC":[2343,2344,2345,2346,15430,15431],
        "ARS":[2198,2209,2500,2814,3619],
        "GLAZ":[1986,2300,2800],
        "BISC":[239,248,370],
    }.items():
        print("\n",sn)
        for row in rows:
            print(row,json.dumps({a:[c["v"],formula(m[sn],a)] for a,c in m[sn]["cells"].items() if int(re.search(r"\d+",a)[0])==row},ensure_ascii=False))
