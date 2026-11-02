import zipfile,xml.etree.ElementTree as E,collections
N="http://schemas.openxmlformats.org/spreadsheetml/2006/main";Q=lambda s:"{"+N+"}"+s
p=r"C:\Users\User\.codex\tmp\nomexp_20261020"
with zipfile.ZipFile(p+r"\NOMEXP_SKU_5900_corectat.xlsx") as a,zipfile.ZipFile(p+r"\recovery_diagnostic.xlsx") as b:
 for sn in ["sheet1","sheet2","sheet4"]:
    f="xl/worksheets/"+sn+".xml"
    get=lambda z:{c.get("r"):c.findtext(Q("f")) for c in E.fromstring(z.read(f)).iter(Q("c")) if c.find(Q("f")) is not None}
    fa,fb=get(a),get(b)
    removed=set(fa)-set(fb);print(sn,len(fa),len(fb),"removed",len(removed))
    print([(x,fa[x]) for x in sorted(removed)[:5]])
    print("PRESERVED",[(x,fb[x]) for x in sorted(fb)[:3]])
 for t in ["table2","table6"]:
    path="xl/tables/"+t+".xml"
    for z in[a,b]:
      r=E.fromstring(z.read(path))
      print(t,r.attrib,"names",[c.get("name") for c in r.iter(Q("tableColumn"))])
