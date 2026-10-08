from pathlib import Path
import json,hashlib,shutil,zipfile,re,xml.etree.ElementTree as ET
from pypdf import PdfReader
P=Path(__file__).parent; O=P/'package';repo=P.parent/'eva-production-docs';network=Path(r'\\192.168.100.169\Comun\00.Roboti\iDempiere\Documentatie')
data=json.loads((P/'workbook_data.json').read_text(encoding='utf8'))
assert len(data['rows'])==109 and len(data['versions'])==28
assert len(set(s['id'] for s in data['sources']))==len(data['sources'])
for s in data['sources']:
 if s.get('local'):assert (O/s['local']).exists(),s['id']
pdf=PdfReader(O/'01_Raport/Raport_ERP_Productie.pdf');assert len(pdf.pages)==30
assert all(len(p.extract_text())>500 for p in pdf.pages)
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(O/'01_Raport/Comparatie_ERP_Productie.xlsx') as z:
 assert z.testzip() is None
 wb=ET.fromstring(z.read('xl/workbook.xml'));assert len(wb.find('s:sheets',ns))==4
 for n in range(1,5):
  sh=ET.fromstring(z.read(f'xl/worksheets/sheet{n}.xml'));pane=sh.find('.//s:pane',ns)
  assert pane is not None and pane.attrib.get('xSplit')=='2' and pane.attrib.get('ySplit')=='7',str(pane.attrib if pane is not None else None)
  assert not sh.findall('.//s:c[@t="e"]',ns)
  assert sh.find('s:tableParts',ns) is not None
for f in (O/'01_Raport').glob('*.inspect.ndjson'):f.unlink()
(O/'.gitattributes').write_text('* -text\n',encoding='utf8')
verification={'date':'2026-10-08','excel':{'functions':109,'products_configurations':7,'modules':21,'sheets':4,'freeze':'2 columns / 7 rows','filters':True,'formula_errors':0,'visual_review':'Toate cele patru foi; matrice în trei intervale orizontale.'},'pdf':{'pages':30,'visual_review':'Toate paginile, inclusiv reverificarea capitolului cu descărcările.'},'sources':{'references':len(data['sources']),'local':sum(bool(s.get('local')) for s in data['sources']),'unavailable':sum(bool(s.get('error')) for s in data['sources'])},'functional_ERP_tests':'Neexecutate. Analiză documentară și statică de cod.'}
(O/'VERIFICARE.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf8')
# Detect accidental inclusion of this task's authentication material without printing any secret.
for f in O.rglob('*'):
 if not f.is_file():continue
 assert f.stat().st_size<100*1024*1024,'File exceeds GitHub limit: '+str(f.relative_to(O))
 if f.suffix in ['.txt','.json','.md','.py','.mjs','.html']:
  b=f.read_bytes();assert b'BEGIN OPENSSH PRIVATE KEY' not in b and b'eva_accounting_docs_20261008' not in b,'Unexpected credential material'
files=sorted(f for f in O.rglob('*') if f.is_file() and f.name!='SHA256SUMS.txt')
hashes={f.relative_to(O).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(O/'SHA256SUMS.txt').write_text(''.join(h+'  '+n+'\n' for n,h in hashes.items()),encoding='utf8')
archive=P/'ERP_Productie_2026-10-08.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(O.rglob('*')):
  if f.is_file():z.write(f,'ERP_Productie/'+f.relative_to(O).as_posix())
assert archive.stat().st_size<100*1024*1024
for dest in [repo/'Documentatie/ERP_Productie',network/'ERP_Productie']:
 assert not dest.exists(),'Destination already exists; review before merging: '+str(dest)
 shutil.copytree(O,dest)
 for n,h in hashes.items():assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==h,n
shutil.copy2(archive,repo/'Documentatie'/archive.name);shutil.copy2(archive,network/archive.name)
print(json.dumps({'files':len(files)+1,'bytes':sum(f.stat().st_size for f in files),'zip_bytes':archive.stat().st_size,'network':str(network/'ERP_Productie'),'validation':verification},ensure_ascii=False),flush=True)
