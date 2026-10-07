import sys, pathlib, zipfile, json
base=pathlib.Path(__file__).resolve().parent
lib=base/'EVA_PRINT_WEBSITE_BRIEF_2026-10-02/12_VALIDATION/python_libs'
lib.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(base/'pypdf.whl') as z:z.extractall(lib)
sys.path.insert(0,str(lib))
from pypdf import PdfReader
root=base/'EVA_PRINT_WEBSITE_BRIEF_2026-10-02'
out=root/'09_SOURCES/datasheet_text'
out.mkdir(parents=True,exist_ok=True)
report=[]
for f in (root/'06_DATASHEETS').rglob('*.pdf'):
    if any(x in f.name.lower() for x in ['sds','msds','safety']):continue
    try:
        r=PdfReader(f);s='\n'.join(p.extract_text() or '' for p in r.pages)
        dest=out/(str(f.relative_to(root)).replace('\\','__').replace('/','__')+'.txt')
        dest.write_text(s,encoding='utf-8')
        report.append({'path':f.relative_to(root).as_posix(),'pages':len(r.pages),'characters':len(s),'status':'ok' if len(s)>80 else 'no_text'})
    except Exception as e:report.append({'path':f.relative_to(root).as_posix(),'status':'failed','error':str(e)})
(root/'12_VALIDATION/pdf-readability.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'pdfs':len(report),'readable':sum(x['status']=='ok' for x in report),'failures':[x for x in report if x['status']!='ok'][:5]}))
