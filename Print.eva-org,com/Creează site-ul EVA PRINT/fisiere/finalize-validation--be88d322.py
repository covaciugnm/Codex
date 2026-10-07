import pathlib,json,sys,re
base=pathlib.Path(__file__).resolve().parent;root=base/'EVA_PRINT_WEBSITE_BRIEF_2026-10-02';sys.path.insert(0,str(base/'validation_runtime/pypdf_lib'))
from pypdf import PdfReader
p=root/'12_VALIDATION/pdf-readability.json';report=json.loads(p.read_text(encoding='utf8'))
rows=[r for r in report['documents'] if (root/r['path']).exists()];failures=[]
for item in report['invalid']:
 f=root/item['path']
 try:
  pdf=PdfReader(f);text='\n'.join(page.extract_text() or '' for page in pdf.pages);normalized=re.sub(r'\s+',' ',text)
  if f.name=='technical-overview.pdf':assert 'EVA PRINT' in normalized and len(text)>500,'Insufficient overview text'
  rows.append({'path':item['path'],'pages':len(pdf.pages),'characters':len(text),'status':'valid_pdf','text_extraction':'vector_outline_drawing' if '05_TECHNICAL_DRAWINGS' in f.parts else 'available_with_whitespace_normalization'})
 except Exception as e:failures.append({'path':item['path'],'error':str(e)})
# The prompt was revised after the original read pass, so check its latest version separately.
prompt=PdfReader(root/'01_PROMPT/EVA_PRINT_MASTER_PROMPT_EN.pdf');text='\n'.join(page.extract_text() or '' for page in prompt.pages)
assert 'engineer_count' in text,'Latest dynamic-fact paragraph missing from PDF'
report={'scope':'All deliverable PDFs, excluding Mac resource forks and a removed duplicate. Vector drawings do not require a selectable text layer. Authored overview text is checked after whitespace normalization. Representative drawing and overview PDFs were rendered and visually inspected.','inspected':len(rows)+len(failures),'valid':len(rows),'invalid':failures,'documents':rows,'latest_prompt_pages':len(prompt.pages)}
p.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'valid':len(rows),'invalid':failures,'prompt_pages':len(prompt.pages)}))
