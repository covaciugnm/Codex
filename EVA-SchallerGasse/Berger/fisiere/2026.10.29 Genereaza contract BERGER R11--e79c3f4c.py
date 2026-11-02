from pathlib import Path
import json,hashlib
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter

root=Path.cwd();folder=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.29 Werkvertrag R11';qa=root/'folder map/2026.10.29 QA BERGER R11';qa.mkdir(parents=True,exist_ok=True)
n=json.loads((folder/'2026.10.29 Werkvertrag BERGER R11.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('AR','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('AB','C:/Windows/Fonts/arialbd.ttf'));pdfmetrics.registerFontFamily('AR',normal='AR',bold='AB',italic='AR',boldItalic='AB')
NAVY=colors.HexColor('#183849');TEAL=colors.HexColor('#08767B');RULE=colors.HexColor('#CDDADD');GRAY=colors.HexColor('#546672');PALE=colors.HexColor('#F4F8F8');W,H=A4;M=44;WIDTH=W-2*M
styles={'title':ParagraphStyle('title',fontName='AB',fontSize=23,leading=28,textColor=NAVY,spaceAfter=8),'sub':ParagraphStyle('sub',fontName='AR',fontSize=10,leading=14,textColor=GRAY,spaceAfter=6),'h':ParagraphStyle('h',fontName='AB',fontSize=12,leading=16,textColor=TEAL,spaceAfter=5),'body':ParagraphStyle('body',fontName='AR',fontSize=9.5,leading=13.3,textColor=NAVY),'small':ParagraphStyle('small',fontName='AR',fontSize=8.5,leading=11.4,textColor=NAVY),'head':ParagraphStyle('head',fontName='AB',fontSize=8.7,leading=11.6,textColor=colors.white)}
def P(t,style='body'):return Paragraph(t,styles[style])
def E(t):return escape(str(t))
def panel(title,paragraphs):
 rows=[[P(E(title),'h')]]+[[P('<b>('+str(i)+')</b> '+E(p))] for i,p in enumerate(paragraphs,1)]
 t=Table(rows,colWidths=[WIDTH],repeatRows=1,splitByRow=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.45,RULE),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.25,RULE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('BACKGROUND',(0,0),(-1,0),PALE)]));return t
def tab(data, compact=False):
 widths=data.get('widths_cm');col=[WIDTH*x/sum(widths) for x in widths] if widths and len(widths)==len(data['headers']) else [WIDTH/len(data['headers'])]*len(data['headers'])
 rows=[[P(E(v),'head') for v in data['headers']]]+[[P(E(v),'small') for v in row] for row in data['rows']]
 t=Table(rows,colWidths=col,repeatRows=1,hAlign='LEFT',splitByRow=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),.35,RULE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),4 if compact else 7),('BOTTOMPADDING',(0,0),(-1,-1),4 if compact else 7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE])]))
 return t
def footer(c,doc):
 c.setStrokeColor(RULE);c.line(M,32,W-M,32);c.setFont('AR',7);c.setFillColor(GRAY);c.drawString(M,21,'A&C Wohnart | Schallergasse 35 | BERGER | R11 | 2026.10.29');c.drawRightString(W-M,21,'Seite '+str(doc.page));c.setFont('AB',7);c.drawString(M,H-25,'WERKVERTRAG  |  TRAGWERKSPLANUNG  |  PRÜFLEISTUNGEN  |  BAUWERKSBUCH')

story=[P('WERKVERTRAG','title'),P('Wohnhaus Schallergasse 35 1120 Wien','sub'),P('A&C Wohnart Immobilien GmbH<br/>und<br/>Bmstr. Dipl.-Ing. (FH) Markus BERGER GmbH','sub'),Spacer(1,7),tab({'headers':['Gesamthonorar netto','Umsatzsteuer 20 %','Gesamthonorar brutto'],'rows':[['EUR 47.500,00','EUR 9.500,00','EUR 57.000,00']],'widths_cm':[1,1,1]}),Spacer(1,12)]
for s in n['sections']:
 story += [panel('§ '+str(s['number'])+' '+s['title'],s['paragraphs']),Spacer(1,11)]
signature_block=[P('Unterzeichnung','h')]
for text in n['signatures']:signature_block += [P(E(text)),Spacer(1,7)]
story += [Spacer(1,5),KeepTogether(signature_block)]
for a in n['annexes']:
 story += [PageBreak(),panel('Anlage '+str(a['number'])+' '+a['title'],a['paragraphs']),Spacer(1,10)]
 for t in a['tables']:story += [tab(t, compact=(a['number'] in (3,6))),Spacer(1,8 if a['number'] in (3,6) else 11)]
body=qa/'2026.10.29 BERGER R11 Vertragsseiten.pdf'
SimpleDocTemplate(str(body),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=42,bottomMargin=45,title='Werkvertrag BERGER R11 Schallergasse 35',author='A&C Wohnart Immobilien GmbH').build(story,onFirstPage=footer,onLaterPages=footer)
offer=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09/2026.10.13 Anlage 5 Originalangebot BERGER 2026.08.17.pdf'
assert len(PdfReader(offer).pages)==4
dest=folder/'2026.10.29 Werkvertrag BERGER R11.pdf';writer=PdfWriter();writer.append(str(body),outline_item='Werkvertrag R11 und Anlagen 1 bis 6');writer.append(str(offer),outline_item='Anlage 5 Originalangebot 2026.08.17 unverändert')
writer.add_metadata({'/Title':'Werkvertrag BERGER R11 Schallergasse 35 2026.10.29','/Author':'A&C Wohnart Immobilien GmbH','/Subject':'Gesamthonorar EUR 47.500,00 netto einschließlich vollständigem Bauwerksbuch; Personen und Terminplan vor Unterzeichnung ergänzen'})
with dest.open('wb') as f:writer.write(f)
reader=PdfReader(dest);full='\n'.join(page.extract_text() or '' for page in reader.pages)
assert '47.500,00' in full and '57.000,00' in full and len(reader.pages)>15
assert 'Offene AG-Entscheidungen' not in full and 'Arbeitsvorschlag' not in full
stats={'pdf':str(dest),'pages':len(reader.pages),'contract_pages':len(PdfReader(body).pages),'offer_original_pages':4,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'offer_sha256':hashlib.sha256(offer.read_bytes()).hexdigest(),'price_net':47500,'price_gross':57000}
(qa/'2026.10.29 Audit generare contract.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,ensure_ascii=False))
