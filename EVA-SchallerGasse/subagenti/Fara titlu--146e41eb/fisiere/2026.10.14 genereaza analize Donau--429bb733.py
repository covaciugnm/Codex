from pathlib import Path
import re,json,hashlib,html,sys
import pypdfium2 as pdfium
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
root=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
styles={
 'title':ParagraphStyle('title',fontName='Arial-Bold',fontSize=21,leading=25,spaceAfter=10,textColor=colors.black),
 'sub':ParagraphStyle('sub',fontName='Arial',fontSize=11,leading=15,spaceAfter=5,textColor=colors.HexColor('#39434c')),
 'meta':ParagraphStyle('meta',fontName='Arial',fontSize=9,leading=13,spaceAfter=18,textColor=colors.HexColor('#59616a')),
 'h':ParagraphStyle('h',fontName='Arial-Bold',fontSize=13.3,leading=17,spaceBefore=15,spaceAfter=8,keepWithNext=True,textColor=colors.black),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10.3,leading=14.2,spaceAfter=8,allowWidows=0,allowOrphans=0,splitLongWords=True),
 'ref':ParagraphStyle('ref',fontName='Arial',fontSize=8.7,leading=11.8,spaceAfter=7,splitLongWords=True),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=8.5,leading=11.5,spaceAfter=0),
 'th':ParagraphStyle('th',fontName='Arial-Bold',fontSize=8.5,leading=11.5,spaceAfter=0,textColor=colors.white),
}
def clean_final(path):
 t=path.read_text(encoding='utf8')
 t=t.replace('și108 VersVG','și 108 VersVG').replace('00: 00','00:00').replace('Kostenaufstellung,„','Kostenaufstellung, „').replace('1000Kse','1000K se')
 t=re.sub(r'\bAlin\.(?=\d)','Alin. ',t)
 if '01 Incetarea' in path.name:
  t=t.replace('încălcarea culpabilă a unei obligații de către cealaltă parte;', 'încălcarea de către cealaltă parte a unei obligații legale sau contractuale legate de sinistru;')
  t=t.replace('că imobilul nu mai este grevat ori că creditorul consimte.', 'că imobilul nu era grevat la momentul la care încetarea putea fi notificată cel mai târziu ori că creditorul consimte.')
 # Preserve quotations and URLs; format only authored material.
 parts=re.split(r'(„[^”]*”|https?://\S+|[a-f0-9]{64})',t)
 for i,s in enumerate(parts):
  if s.startswith(('„','http')) or re.fullmatch('[a-f0-9]{64}',s):continue
  for a,b in {'în05':'în 05','și91':'și 91','și3':'și 3','în2036':'în 2036','Somație2026':'Somație 2026','1000K se':'1000K se','primitID':'primit ID ','trimisID':'trimis ID ','§ 39alin.3':'§ 39 alin.3','globaleDONAU':'globale DONAU','expresABS':'expres ABS','DacăDONAU':'Dacă DONAU','cadrului290':'cadrului 290','pct.4':'pct. 4'}.items():s=s.replace(a,b)
  s=re.sub(r'\balin\.(?=\d)','alin. ',s)
  parts[i]=s
 t=''.join(parts)
 path.write_text(t,encoding='utf8')
 return t
def xml(s):
 s=html.escape(s)
 # Hyperlinks keep full target and a short readable display, preserving full URLs in TXT.
 def url(m):
  u=html.unescape(m.group(0)); label='RIS - sursa oficială'
  return '<link href="'+html.escape(u,quote=True)+'" color="#164f78"><u>'+label+'</u></link>'
 return re.sub(r'https?://[^\s]+',url,s)
class Doc(BaseDocTemplate):
 def __init__(self,*a,short='',**kw):
  super().__init__(*a,**kw);self.short=short;self.hidx=0
 def afterFlowable(self,flow):
  if isinstance(flow,Paragraph) and flow.style.name=='h':
   self.hidx+=1;key=f'h{self.hidx}';self.canv.bookmarkPage(key);self.canv.addOutlineEntry(flow.getPlainText(),key,0,False)
def footer(c,d):
 c.saveState();c.setFont('Arial',8);c.setFillColor(colors.HexColor('#5b626a'))
 c.drawString(20*mm,13*mm,'DONAU 2044001194  |  2026.10.14')
 c.drawRightString(A4[0]-20*mm,13*mm,str(d.page));c.restoreState()
summary=[]
selected=[f for f in sorted(root.glob('2026.10.14 0[12]*.txt')) if len(sys.argv)<2 or sys.argv[1] in f.name]
if len(sys.argv)>1 and (root/'2026.10.14 Registru documente finale.json').exists():
 summary=[x for x in json.loads((root/'2026.10.14 Registru documente finale.json').read_text(encoding='utf8')) if sys.argv[1] not in x['pdf']]
for file in selected:
 t=clean_final(file);lines=t.splitlines();out=file.with_suffix('.pdf')
 doc=Doc(str(out),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=22*mm,title=lines[0],author='Analiză documentară pentru A&C Wohnart Immobilien GmbH')
 frame=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
 doc.addPageTemplates(PageTemplate(id='normal',frames=[frame],onPage=footer))
 story=[Paragraph(xml(lines[0]),styles['title']),Paragraph(xml(lines[1]),styles['sub']),Paragraph(xml(lines[2]),styles['meta'])]
 i=3;refs=False
 while i<len(lines):
  line=lines[i].strip();i+=1
  if not line:continue
  if re.match(r'^\d+ [A-ZĂÂÎȘȚ]',line):
   refs=('Surse' in line)
   if refs:story.append(PageBreak())
   story.append(Paragraph(xml(line),styles['h']));continue
  if line.startswith('|'):
   story.append(PageBreak())
   rows=[line]
   while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
   cells=[]
   for j,r in enumerate(rows):
    row=[]
    for k,x in enumerate(r.strip('|').split('|')):
     val=xml(x.strip())
     if k==0 and re.match(r'^2026\.\d\d\.\d\d–',x.strip()):val=val.replace('–','<br/>– ')
     row.append(Paragraph(val,styles['th' if j==0 else 'cell']))
    cells.append(row)
   tb=Table(cells,colWidths=[35*mm,37*mm,98*mm],repeatRows=1,hAlign='LEFT')
   tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#374651')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#374651')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f4f5'),colors.white]),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d6dde1'))]))
   story.extend([tb,Spacer(1,10)]);continue
  story.append(Paragraph(xml(line),styles['ref' if refs else 'body']))
 doc.build(story)
 pdf=pdfium.PdfDocument(str(out));qa=root/'2026.10.14 Control vizual'/file.stem;qa.mkdir(parents=True,exist_ok=True)
 for n,page in enumerate(pdf,1):page.render(scale=1.6).to_pil().save(qa/f'2026.10.14 pagina {n:02d}.png')
 extracted='\n'.join(p.extract_text() for p in PdfReader(str(out)).pages)
 (qa/'2026.10.14 Text PDF.txt').write_text(extracted,encoding='utf8')
 summary.append({'pdf':str(out.resolve()),'pages':len(pdf),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'txt_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'qa':str(qa.resolve())})
(root/'2026.10.14 Registru documente finale.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
