from pathlib import Path
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json,re
B=Path(__file__).parent;js=json.loads((B/'jobs.json').read_text(encoding='utf-8'))
for j in js:
 p=Path(j['docx']);d=Document(p)
 for st in d.styles:
  for border in list(st.element.iter(qn('w:pBdr'))):border.getparent().remove(border)
 for pp in d.paragraphs:
  if pp.style.name=='Title':
   pp.paragraph_format.space_after=Pt(8)
   ppr=pp._p.get_or_add_pPr();bd=OxmlElement('w:pBdr');bt=OxmlElement('w:bottom');bt.set(qn('w:val'),'nil');bd.append(bt);ppr.append(bd)
   for r in pp.runs:r.font.name='Arial';r.font.size=Pt(15);r.font.color.rgb=RGBColor(0,0,0);r.font.underline=False
  pp.paragraph_format.widow_control=True
 if p.name.startswith('CV_'):
  for s in d.sections:s.top_margin=Cm(1.7);s.bottom_margin=Cm(1.7)
  for pp in d.paragraphs:
   pp.paragraph_format.space_after=Pt(3);pp.paragraph_format.line_spacing=1.0
   if len(pp.runs)==1 and pp.runs[0].bold:pp.paragraph_format.keep_with_next=True
   pp.paragraph_format.keep_together=True
  if len(d.paragraphs)>2:d.paragraphs[-2].paragraph_format.keep_with_next=True
 # Keep review warnings visible, without an otherwise empty extra page in the official letter.
 if p.name.startswith('01_Anexa_1'):
  notes=[pp for pp in d.paragraphs if pp.text.startswith('ÎNAINTE DE SEMNARE:')]
  for pp in notes:
   text=pp.text;pp._p.getparent().remove(pp._p)
   h=d.sections[0].header.add_paragraph(text)
   h.paragraph_format.space_after=Pt(0)
   for r in h.runs:r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string('9C3B10')
  while d.paragraphs and not d.paragraphs[-1].text.strip():
   pp=d.paragraphs[-1]
   if pp._p.find('.//'+qn('w:sectPr')) is not None:break
   pp._p.getparent().remove(pp._p)
 # Record the factual date discrepancy rather than silently changing it.
 if p.name.startswith('19_Verificare'):
  d.add_paragraph('Trasabilitate Szoke: CV-ul arhivat indică început voluntariat04.02.2013, iar contractul32/15.01.2013 și certificatul2/10.10.2022 indică15.01.2013. CV-ul nou folosește data din înscrisurile justificative. Funcția actuală de președinte este confirmată de utilizator; data14.11.2022 provine din CV-ul arhivat.')
 for el in d.element.iter(qn('w:t')):
  if el.text:el.text=re.sub(r'\b(la|din|anul|anii|contract|certificatul|voluntariat|indică|data|nr\.|seria)(?=\d)',r'\1 ',el.text,flags=re.I)
 d.save(p)
rs=json.loads((B/'records.json').read_text(encoding='utf-8'))
for r in rs:
 if r['title'].startswith('CV_Szoke'):r['obs']+=' | Data voluntariat: CV sursă04.02.2013; certificat/contract15.01.2013. Folosită data justificată în certificat.'
(B/'records.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Polished',len(js))
