"""Repair unsupported renderer caches while preserving native Excel HYPERLINK formulas.

The bundled artifact engine exports HYPERLINK as t=e with a prose error cache.
That is not a valid OOXML error value and prevents Excel from opening the file.
Only those caches are replaced with the formula's literal friendly label.
All authored values, formulas, styles, tables and relationships remain intact.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import xml.etree.ElementTree as E
import re,json,sys
NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
E.register_namespace('x',NS)
def repair(p):
 p=Path(p);count=0
 with ZipFile(p) as z:members=[(i,z.read(i.filename)) for i in z.infolist()]
 out=[]
 for info,data in members:
  if re.match(r'xl/worksheets/sheet\d+\.xml$',info.filename):
   root=E.fromstring(data);changed=False
   for c in root.iter('{'+NS+'}c'):
    f=c.find('{'+NS+'}f');v=c.find('{'+NS+'}v')
    if f is not None and (f.text or '').startswith('HYPERLINK('):
     m=re.search(r',"((?:[^"]|"")*)"\)$',f.text)
     if not m:raise ValueError('Unrecognized hyperlink formula')
     c.set('t','str')
     if v is None:v=E.SubElement(c,'{'+NS+'}v')
     v.text=m[1].replace('""','"');count+=1;changed=True
   if changed:data=E.tostring(root,encoding='utf-8',xml_declaration=True)
  out.append((info,data))
 tmp=p.with_suffix('.cachefix.xlsx')
 with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
  for info,data in out:z.writestr(info,data)
 tmp.replace(p)
 return count
if __name__=='__main__':
 if len(sys.argv)>1:print(repair(sys.argv[1]))
 else:
  B=Path(__file__).parent
  for pr in json.loads((B/'projects.json').read_text(encoding='utf-8')):
   p=Path(pr['out'])/'00 Registru documente si termene ROSE.xlsx';print(pr['id'],repair(p))
