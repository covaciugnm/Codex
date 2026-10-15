from pathlib import Path
import json,sys,hashlib,re
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
def field(p,key):
 r=p.add_run(); e=OxmlElement('w:fldChar');e.set(qn('w:fldCharType'),'begin');r._r.append(e)
 r=p.add_run(); e=OxmlElement('w:instrText');e.set(qn('xml:space'),'preserve');e.text=' '+key+' ';r._r.append(e)
 r=p.add_run(); e=OxmlElement('w:fldChar');e.set(qn('w:fldCharType'),'end');r._r.append(e)
def cellprops(c,shade):
 pr=c._tc.get_or_add_tcPr()
 b=OxmlElement('w:tcBorders')
 for x in ['top','left','bottom','right']:
  e=OxmlElement('w:'+x);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
 pr.append(b)
 m=OxmlElement('w:tcMar')
 for x,v in [('top',95),('bottom',95),('left',100),('right',100)]:
  e=OxmlElement('w:'+x);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');m.append(e)
 pr.append(m);s=OxmlElement('w:shd');s.set(qn('w:fill'),shade);pr.append(s)
def addtable(doc,spec):
 headers=spec['headers'];rows=spec['rows'];n=len(headers)
 widths=spec.get('widths_cm') or {2:[5.2,11.4],3:[2.2,10.8,3.6],4:[2.2,7.2,3.8,3.4],5:[1.6,7.6,2.4,2.4,2.6]}.get(n,[16.6/n]*n)
 assert len(widths)==n
 factor=16.6/sum(widths);widths=[x*factor for x in widths]
 tb=doc.add_table(rows=1,cols=n);tb.alignment=WD_TABLE_ALIGNMENT.CENTER;tb.autofit=False
 for i,c in enumerate(tb.columns):c.width=Cm(widths[i])
 for i,v in enumerate(headers):tb.rows[0].cells[i].text=str(v)
 for row in rows:
  assert len(row)==n,(headers,row)
  cells=tb.add_row().cells
  for i,v in enumerate(row):cells[i].text=str(v if v is not None else '')
 for ri,row in enumerate(tb.rows):
  pr=row._tr.get_or_add_trPr()
  nonsplit=OxmlElement('w:cantSplit');pr.append(nonsplit)
  if ri==0:
   e=OxmlElement('w:tblHeader');e.set(qn('w:val'),'true');pr.append(e)
  for ci,c in enumerate(row.cells):
   c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   cellprops(c,'E7EBEF' if ri==0 else ('F7F8F9' if ri%2==0 else 'FFFFFF'))
   for p in c.paragraphs:
    p.paragraph_format.line_spacing=1.04;p.paragraph_format.space_after=Pt(2);p.paragraph_format.space_before=Pt(2)
    p.paragraph_format.keep_with_next=ri==0;p.paragraph_format.widow_control=True
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER if ri==0 else (WD_ALIGN_PARAGRAPH.RIGHT if 'EUR' in headers[ci] or '%' in headers[ci] else WD_ALIGN_PARAGRAPH.LEFT)
    for run in p.runs:
     run.font.name='Arial';run.font.size=Pt(9.5);run.font.color.rgb=RGBColor(0,0,0);run.bold=ri==0
 doc.add_paragraph().paragraph_format.space_after=Pt(2)
def addparagraph(doc,s):
 p=doc.add_paragraph(s)
 p.paragraph_format.widow_control=True
 # Signature and completion fields must stay together.
 if 'Unterschrift' in s or ('____' in s and len(s)<300):p.paragraph_format.keep_together=True
 return p
def additem(doc,item,numbered=True):
 for i,p in enumerate(item.get('paragraphs',[]),1):
  if numbered:
   assert not re.match(r'^\(\d+[a-z]?\)',p),p[:100]
  addparagraph(doc,(f'({i}) ' if numbered else '')+p)
 tables=item.get('tables',[])
 if item.get('table'):tables=tables+[item['table']]
 for tb in tables:addtable(doc,tb)
def build(src,out):
 data=json.loads(src.read_text(encoding='utf-8-sig'))
 d=Document();sec=d.sections[0]
 sec.page_width=Cm(21);sec.page_height=Cm(29.7)
 sec.top_margin=Cm(2.1);sec.bottom_margin=Cm(2.1);sec.left_margin=Cm(2.2);sec.right_margin=Cm(2.2)
 sec.header_distance=Cm(0.8);sec.footer_distance=Cm(0.8)
 st=d.styles['Normal'];st.font.name='Times New Roman';st.font.size=Pt(11.5);st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.line_spacing=1.08;st.paragraph_format.space_after=Pt(5);st.paragraph_format.widow_control=True
 lang=OxmlElement('w:lang');lang.set(qn('w:val'),'de-AT');st._element.get_or_add_rPr().append(lang)
 for name,size in [('Title',17),('Subtitle',11),('Heading 1',12),('Heading 2',11)]:
  s=d.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.bold=name!='Subtitle';s.font.color.rgb=RGBColor(0,0,0)
  s.paragraph_format.keep_with_next=True;s.paragraph_format.space_after=Pt(7);s.paragraph_format.space_before=Pt(11 if name.startswith('Heading') else 0)
  if s._element.pPr is not None:
   for e in list(s._element.pPr):
    if e.tag==qn('w:pBdr'):s._element.pPr.remove(e)
 d.core_properties.author='A&C Wohnart Immobilien GmbH'
 d.core_properties.title=data.get('title','Werkvertrag')
 d.core_properties.subject='Schallergasse 35 Tragwerksplanung Prüfingenieur und Bauwerksbuch'
 d.core_properties.keywords='Entwurf 2026.10.13 nicht unterzeichnet nicht versendet'
 d.core_properties.comments=''
 update=OxmlElement('w:updateFields');update.set(qn('w:val'),'true');d.settings._element.append(update)
 d.add_paragraph(data['title'],style='Title')
 d.add_paragraph('A&C Wohnart Immobilien GmbH und '+data['provider']+'   |   Schallergasse 35 1120 Wien',style='Subtitle')
 for p in data.get('preamble',[]):addparagraph(d,p)
 numbers=[int(s['number']) for s in data['sections']]
 assert numbers==list(range(1,len(numbers)+1)),numbers
 for s in data['sections']:
  d.add_paragraph(f'§ {s["number"]} {s["title"]}',style='Heading 1');additem(d,s)
 # Signatures bind the contract and annexes, and occur before the annexes.
 sigs=data.get('signatures',[])
 if sigs:
  d.add_paragraph('Unterfertigung',style='Heading 1')
  for i,text in enumerate(sigs):
   p=addparagraph(d,text)
   p.paragraph_format.keep_together=True
   p.paragraph_format.keep_with_next=i<len(sigs)-1
 for a in data.get('annexes',[]):
  p=d.add_paragraph(f'Anlage {a["number"]} {a["title"]}',style='Heading 1')
  p.paragraph_format.page_break_before=True
  additem(d,a,numbered=False)
 footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
 footer.add_run(f'{data["provider"]}   |   Entwurf 2026.10.13   |   Seite ');field(footer,'PAGE');footer.add_run(' von ');field(footer,'NUMPAGES')
 for r in footer.runs:r.font.name='Arial';r.font.size=Pt(9);r.font.color.rgb=RGBColor(0,0,0)
 out.parent.mkdir(parents=True,exist_ok=True);d.save(out)
 # Verify that every authored paragraph and cell is retained verbatim.
 check=Document(out)
 alltext=''.join(x.text or '' for el in check.element.body for x in el.xpath('.//w:t'))
 assert data['title'] in alltext
 for container in data['sections']+data.get('annexes',[]):
  for p in container.get('paragraphs',[]):assert p in alltext, p[:100]
  tables=container.get('tables',[])+([container['table']] if container.get('table') else [])
  for tb in tables:
   for row in [tb['headers']]+tb['rows']:
    for cell in row:assert str(cell if cell is not None else '') in alltext,str(cell)[:100]
 print(json.dumps(dict(source=str(src),output=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),sections=len(data['sections']),annexes=len(data.get('annexes',[])),tables=len(check.tables)),ensure_ascii=False))
if __name__=='__main__':build(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
