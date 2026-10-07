from pathlib import Path
from xml.sax.saxutils import escape
from docx import Document
from docx.text.paragraph import Paragraph as WParagraph
from docx.table import Table as WTable
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import fitz

out=Path(r'C:\Users\User\Documents\Codex\2026-09-30\in\outputs')
stem='Anexa 1 la factura nr. 1 din 29.09.2026'
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='ArialBold')
normal=ParagraphStyle('Normal',fontName='Arial',fontSize=9.3,leading=11.6,spaceAfter=5)
small=ParagraphStyle('Small',parent=normal,fontSize=8.4,leading=10.4)
cell=ParagraphStyle('Cell',parent=normal,fontSize=8.5,leading=10.4,spaceAfter=0)
heading=ParagraphStyle('Heading',parent=normal,fontName='ArialBold',fontSize=11,leading=13,spaceBefore=9,spaceAfter=5,textColor=colors.HexColor('#254B43'),keepWithNext=True)
title=ParagraphStyle('Title',parent=heading,fontSize=21,leading=25,spaceBefore=0)
source=ParagraphStyle('Source',parent=normal,fontSize=6.5,leading=8)
story=[]
doc=Document(out/(stem+'.docx'))
for child in doc.element.body:
    if child.tag.endswith('}p'):
        wp=WParagraph(child,doc)
        if 'w:type="page"' in child.xml:
            story.append(PageBreak()); continue
        if not wp.text: continue
        style=normal
        if wp.text=='ANEXA 1': style=title
        elif wp.style.name.startswith('Heading'): style=heading
        elif wp.text.startswith('Referință'): style=source
        elif wp.runs and wp.runs[0].font.size and wp.runs[0].font.size.pt<=9: style=small
        txt=escape(wp.text)
        if wp.runs and wp.runs[0].bold: txt='<b>'+txt+'</b>'
        story.append(Paragraph(txt,style))
    elif child.tag.endswith('}tbl'):
        wt=WTable(child,doc)
        rows=[]
        for ri,row in enumerate(wt.rows):
            line=[]
            for c in row.cells:
                txt=escape(c.text).replace('\n','<br/>')
                if ri==0: txt='<b>'+txt+'</b>'
                line.append(Paragraph(txt,cell))
            rows.append(line)
        widths=[float(c.width)/914400*72 for c in wt.rows[0].cells]
        scale=493.2/sum(widths); widths=[w*scale for w in widths]
        t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8EFEC')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#BBC9C2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.extend([t,Spacer(1,5)])

def page(canvas,doc):
    canvas.setFont('Arial',7)
    canvas.setFillColor(colors.HexColor('#66746E'))
    canvas.drawString(51,816,'ÎNTREȚINERE BAZĂ SPORTIVĂ  |  ANEXĂ LA FACTURĂ')
    canvas.drawRightString(544,24,f'Factura nr. 1 / 29.09.2026  •  Pagina {doc.page}')

pdf=out/(stem+'.pdf')
SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=51,leftMargin=51,topMargin=43,bottomMargin=40,title=stem,author='').build(story,onFirstPage=page,onLaterPages=page)
d=fitz.open(pdf)
print('Pages:',len(d))
for i,p in enumerate(d):
    print(i+1, len(p.get_text()), p.get_text()[:100].replace('\n',' | '))
    p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(str(out.parent/'work'/f'annex-{i+1}.png'))
