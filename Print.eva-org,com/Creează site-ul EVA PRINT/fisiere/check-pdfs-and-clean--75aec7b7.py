import pathlib,sys,zipfile,json,shutil
base=pathlib.Path(__file__).resolve().parent;root=(base/'EVA_PRINT_WEBSITE_BRIEF_2026-10-02').resolve();lib=base/'validation_runtime/pypdf_lib'
lib.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(base/'pypdf.whl') as z:z.extractall(lib)
sys.path.insert(0,str(lib))
from pypdf import PdfReader
rows=[];failed=[]
for p in root.rglob('*.pdf'):
 if '__MACOSX' in p.parts or p.name.startswith('._'):continue
 try:
  r=PdfReader(p);text='\n'.join(page.extract_text() or '' for page in r.pages)
  row={'path':p.relative_to(root).as_posix(),'pages':len(r.pages),'characters':len(text),'status':'valid_pdf','text_extraction':'available' if len(text)>80 else 'image_or_minimal_text'}
  if '02_MATERIALS' in p.parts and p.name=='technical-overview.pdf':
   assert 'EVA PRINT' in text and len(text)>500, 'Overview text not readable'
  if '05_TECHNICAL_DRAWINGS' in p.parts:assert 'EVA PRINT' in text,'Drawing text not readable'
  rows.append(row)
 except Exception as e:failed.append({'path':p.relative_to(root).as_posix(),'error':str(e)})
(root/'12_VALIDATION/pdf-readability.json').write_text(json.dumps({'scope':'All deliverable PDFs, excluding Mac resource forks','inspected':len(rows)+len(failed),'valid':len(rows),'invalid':failed,'documents':rows},indent=2),encoding='utf8')
# Remove only generated dependency copies and extracted Mac metadata inside this exact package.
targets=[root/'12_VALIDATION/python_libs',root/'12_VALIDATION/postgres-runtime',root/'06_DATASHEETS/TDS_FIBERON-ASA-CF08_V1.0_EN.pdf']+list(root.rglob('__MACOSX'))
for p in targets:
 if p.exists():
  assert p.resolve().is_relative_to(root) and p.resolve()!=root,'Unsafe cleanup target'
  if p.is_dir():shutil.rmtree(p)
  else:p.unlink()
print(json.dumps({'inspected':len(rows)+len(failed),'valid':len(rows),'invalid':failed}))
