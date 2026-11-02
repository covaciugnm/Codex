from pathlib import Path
import json,hashlib,re,datetime
from pypdf import PdfReader
import pypdfium2 as pdf
R=Path.cwd(); Q=R/'folder map/2026.10.27 QA autorizare';Q.mkdir(exist_ok=True)
I=json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8')); idx={x['cale']:x for x in I}
sel={
'D01':'00.Proiect/01. Behoerden + Eigentum/01. Baubescheid + genehmigte Plaene/Schallergasse_35_Baubescheid.pdf',
'D02':'00.Proiect/01. Behoerden + Eigentum/01. Baubescheid + genehmigte Plaene/P2041_C_220404_GENEHMIGUNG+GESCHOSSE_A3.pdf',
'D03':'00.Proiect/01. Behoerden + Eigentum/01. Baubescheid + genehmigte Plaene/P2041_C_220329_Baubeschreibung.pdf',
'D04':'00.Proiect/03. Einreichplanung - Planwechsel/04. Bauphysik + Energieausweis/12S35_EinrBPH_2022-03-22+2022-09-06_Abgabe.pdf',
'D05':'00.Proiect/03. Einreichplanung - Planwechsel/03. Statik/WC0321_000_A.pdf',
'D06':'00.Proiect/03. Einreichplanung - Planwechsel/03. Statik/STATIK VorKonzept_2021-12-07.pdf',
'D07':'00.Proiect/01. Behoerden + Eigentum/04. Vollmachten/Vollmacht Baupolizei.pdf',
'D08':'00.Proiect/03. Einreichplanung - Planwechsel/01. Architektur/A.01 Plan demisol-Yoga.pdf',
'D09':'00.Proiect/03. Einreichplanung - Planwechsel/01. Architektur/A.02 Plan parter.pdf',
'D10':'00.Proiect/03. Einreichplanung - Planwechsel/01. Architektur/A.03 Plan etaj intermediar.pdf',
'D11':'00.Proiect/01. Behoerden + Eigentum/02. Grundbuch + Kaufvertrag/Grundbuchauszug_aktuell_A&C_EZ2235.pdf',
'D12':'00.Proiect/00_INHALTSVERZEICHNIS_und_CHECKLISTE.docx'}
manifest={}
for key,path in sel.items():
 p=R/path; dig=hashlib.sha256(p.read_bytes()).hexdigest(); row=idx[path]
 info={'cale':path,'sha256':dig,'unchanged':dig==row['sha256'],'text_cache':row['text_cache']}
 if p.suffix.lower()=='.pdf':
  rd=PdfReader(p);info['pages']=len(rd.pages);info['page_sizes']=[(float(x.mediabox.width),float(x.mediabox.height)) for x in rd.pages];info['signature_fields']=[k for k,v in (rd.get_fields() or {}).items() if str(v.get('/FT'))=='/Sig']
  doc=pdf.PdfDocument(p)
  pages=range(len(rd.pages)) if key in ['D01','D02','D03','D06','D07','D08','D09','D10','D11'] else [0,1,len(rd.pages)-1]
  for n in pages:
   pg=doc[n]; scale=min(1.6,1800/max(pg.get_size()));pg.render(scale=scale).to_pil().save(Q/f'{key}-{n+1:03}.png')
  info['rendered_pages']=[n+1 for n in pages]
 manifest[key]=info
(Q/'2026.10.27 Surse locale.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
