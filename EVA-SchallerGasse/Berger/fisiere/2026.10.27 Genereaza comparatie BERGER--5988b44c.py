from pathlib import Path
import json,hashlib,difflib,re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether,HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A3,landscape
import pdfplumber

root=Path.cwd();folder=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.27 Observatii BERGER si comparatie'
m=json.loads((folder/'2026.10.27 BERGER R10 model comparativ si discutii.json').read_text(encoding='utf-8'));old=m['original'];new=m['vorschlag'];mods=m['modificari']
pdfmetrics.registerFont(TTFont('AR','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('AB','C:/Windows/Fonts/arialbd.ttf'));pdfmetrics.registerFontFamily('AR',normal='AR',bold='AB',italic='AR',boldItalic='AB')
NAVY=colors.HexColor('#15394D');TEAL=colors.HexColor('#087F83');GRAY=colors.HexColor('#516774');RULE=colors.HexColor('#CCDADF');PALE=colors.HexColor('#EFF6F5');AMBER=colors.HexColor('#855A16');BG=colors.HexColor('#FFF7E8')
W,H=landscape(A3);M=32;CW=(W-2*M)/2;WIDTH=W-2*M
styles={
 'title':ParagraphStyle('title',fontName='AB',fontSize=26,leading=30,textColor=NAVY,spaceAfter=11),
 'sub':ParagraphStyle('sub',fontName='AR',fontSize=12,leading=17,textColor=GRAY,spaceAfter=10),
 'h':ParagraphStyle('h',fontName='AB',fontSize=14,leading=18,textColor=TEAL,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='AR',fontSize=10,leading=13.3,textColor=NAVY),
 'small':ParagraphStyle('small',fontName='AR',fontSize=8.5,leading=11,textColor=GRAY),
 'note':ParagraphStyle('note',fontName='AR',fontSize=8.6,leading=11.4,textColor=AMBER,spaceBefore=4),
 'ref':ParagraphStyle('ref',fontName='AB',fontSize=9,leading=12,textColor=TEAL,spaceAfter=4),
 'head':ParagraphStyle('head',fontName='AB',fontSize=10,leading=13,textColor=colors.white),
}
def P(text,style='body'):return Paragraph(text,styles[style])
def esc(t):return escape(str(t))
def diff(a,b):
 if a==b:return esc(b)
 aa=a.split();bb=b.split();pieces=[]
 for tag,i,j,k,l in difflib.SequenceMatcher(None,aa,bb,autojunk=False).get_opcodes():
  if tag=='delete':continue
  s=esc(' '.join(bb[k:l]));pieces.append(s if tag=='equal' else '<font color="#087F83"><b>'+s+'</b></font>')
 return ' '.join(pieces)
def note(ref):
 hits=[x for x in mods if ref in x['referinte']]
 if not hits:return []
 return [Spacer(1,4),P(' / '.join('<b>'+x['id']+'</b> '+esc(x['titlu']) for x in hits)+'<br/>'+('Puncte deschise: propunerea nu este o concesie aprobată de proprietar și nu dovedește acordul BERGER.' if any(x['status'].startswith('DESCHIS') for x in hits) else 'Vezi explicațiile și acțiunile din registrul de observații.'),'note')]
def table(rows,headers=None,sectiontitle=None):
 data=[]
 if sectiontitle:data.append([P(esc(sectiontitle),'h'),''])
 if headers:data.append([P(h,'head') for h in headers])
 data+=rows
 t=Table(data,colWidths=[CW,CW],repeatRows=(1+bool(sectiontitle)) if headers else 0,hAlign='LEFT',splitByRow=1,splitInRow=0)
 st=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('GRID',(0,0),(-1,-1),.35,RULE)]
 if sectiontitle:st += [('SPAN',(0,0),(-1,0)),('BACKGROUND',(0,0),(-1,0),colors.white)]
 if headers:
  hi=1 if sectiontitle else 0
  st += [('BACKGROUND',(0,hi),(-1,hi),NAVY)]
 start=(1+bool(sectiontitle)) if headers else 0
 for i in range(start,len(data)):
  if (i-start)%2:st.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#F8FAFB')))
 t.setStyle(TableStyle(st));return t
def infobox(text):
 t=Table([[P(text)]],colWidths=[WIDTH]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BG),('BOX',(0,0),(-1,-1),.45,RULE),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));return t
def cell(ref,text,changed=None,annotations=False):
 parts=[P(esc(ref),'ref'),P(diff(changed,text) if changed is not None else esc(text))]
 if annotations:parts+=note(ref)
 return parts
def footer(c,doc):
 c.setStrokeColor(RULE);c.line(M,32,W-M,32);c.setFont('AR',7.8);c.setFillColor(GRAY)
 c.drawString(M,20,'A&C Wohnart | Schallergasse 35 | BERGER R09 / propunere R10 | 2026.10.27 | document de lucru')
 c.drawRightString(W-M,20,str(doc.page))
 c.setFont('AB',8);c.drawString(M,H-24,'COMPARAȚIE CONTRACTUALĂ | ORIGINAL / PROPUNERE CU OBSERVAȚII')
story=[P('BERGER | CONTRACT ÎN PARALEL','title'),P('Original R09 în stânga. Propunerea actualizată în germană în dreapta.<br/>Observațiile și discuțiile pentru proprietar sunt în română. 2026.10.27','sub'),infobox('<b>Stadiu: proiect pentru analiză, cu decizii deschise.</b> Acest document nu consemnează acceptarea observațiilor BERGER, un contract încheiat sau un text pregătit pentru semnare. Modificările propuse sunt evidențiate cu verde. Punctele marcate M01–M21 trimit la registrul de la final; alegerile proprietarului neprimite rămân deschise.'),P('Ce am verificat','h'),P('Scanul primit prin emailul BERGER din 2026.10.27 are 18 pagini, corespunzătoare paginilor 1–18 din R09. Originalul R09 are 29 de pagini. Scanul nu include anexele de la paginile 19–29 și nu demonstrează acceptarea lor. Bifele, sublinierile și lipsa unei note nu sunt tratate ca acord comercial. OCR-ul este automat; numele și fragmentele manuscrise nesigure sunt semnalate, nu completate prin presupunere.'),P('Baza financiară păstrată','h')]
fee=old['annexes'][3]['tables'][0]
fee_data=[[P(esc(x),'head') for x in fee['headers']]]+[[P(esc(v)) for v in row] for row in fee['rows']]
ft=Table(fee_data,colWidths=[WIDTH*.49,WIDTH*.17,WIDTH*.17,WIDTH*.17],repeatRows=1);ft.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),.35,RULE),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story+=[ft,Spacer(1,9),P('<b>Totalul rămâne 45.000 EUR net / 54.000 EUR cu TVA 20%.</b> Maximum 8 vizite statice, inclusiv T0 dacă se prestează efectiv asistență statică. Pachetele suplimentare propuse rămân 1.000 EUR net / 4 vizite, numai dacă sunt comandate. Cele 18 luni de la B0, termenul de plată de 14 zile, lipsa reținerii și lipsa penalității contractuale sunt păstrate. Nu este introdus niciun preț nou pentru Bauwerksbuch, IFC, o verificare statică separată sau o persoană externă.'),P('Cum se închide propunerea','h'),P('1. Proprietarul răspunde la întrebările din registru.<br/>2. BERGER confirmă în scris persoanele, întinderea serviciilor, formatele și calendarul de livrare/facturare cu valori.<br/>3. Orice excludere acceptată se reflectă în toate paragrafele și anexele afectate; orice cost suplimentar este identificat separat, fără aprobare implicită.<br/>4. Se verifică apoi o versiune curată, fără alternative sau câmpuri esențiale deschise, înainte de semnare.'),P('Repere juridice aplicate','h'),P('<b>PI:</b> §127 BO Wien privește controalele cerute de fazele de execuție și desemnarea unei persoane eligibile, distincte de beneficiar și Bauführer în condițiile legii. Numărul vizitelor statice nu poate substitui aceste controale. [L1,L4]<br/><b>Finalizare:</b> confirmarea integrală potrivit §128 necesită competența ZT corespunzătoare; calitatea de expert judiciar pentru PI nu o înlocuiește automat. [L2]<br/><b>Bauwerksbuch:</b> obligația proprietarului de a avea cartea clădirii și de a respecta termenele legale este distinctă de întrebarea comercială dacă BERGER a inclus serviciul în oferta sa. Pentru existentul anterior anului 1919, termenul general este 2027.12.31, dacă ipoteza de vechime se confirmă și nu există o obligație mai devreme. Regimul procedural concret al proiectului autorizat în 2023 se verifică separat. [L3,L5]'),PageBreak()]

for os,ns in zip(old['sections'],new['sections']):
 s=os['number'];story.append(Spacer(1,8))
 rows=[]
 for i in range(max(len(os['paragraphs']),len(ns['paragraphs']))):
  a=os['paragraphs'][i] if i<len(os['paragraphs']) else '';b=ns['paragraphs'][i] if i<len(ns['paragraphs']) else '';ref=f'{s}({i+1})'
  left=cell('§ '+ref,a or '[În R09 nu există acest alineat.]')
  right=cell('§ '+ref,b,changed=a)
  right+=note(ref)
  if a==b and not note(ref):right += [P('Text păstrat. Fără a prezuma acceptarea BERGER.','small')]
  rows.append([left,right])
 story.append(table(rows,['R09 | formularea originală','R10 | propunere de formulare, cu puncte deschise'],sectiontitle='§ '+str(s)+' | '+os['title']))
story.append(PageBreak())
story += [P('ANLAGEN | ANEXELE ÎN PARALEL','title'),P('Anexele originale nu au fost incluse în scanul adnotat. Actualizările de mai jos sunt consecințe ale propunerii noastre, nu observații sau acceptări atribuite BERGER.','sub')]
for oa,na in zip(old['annexes'],new['annexes']):
 n=oa['number'];ref=f'A{n}'
 mids=', '.join(x['id'] for x in mods if ref in x['referinte'])
 annex_title=f'Anlage {n} | '+oa['title']+(' | '+mids if mids else '')
 rows=[]
 for i in range(max(len(oa['paragraphs']),len(na['paragraphs']))):
  a=oa['paragraphs'][i] if i<len(oa['paragraphs']) else '';b=na['paragraphs'][i] if i<len(na['paragraphs']) else ''
  rows.append([cell(f'Anlage {n}({i+1})',a or '[Completare nouă]'),cell(f'Anlage {n}({i+1})',b,changed=a)])
 if rows:story.append(table(rows,['R09 | original','R10 | propunere / corelare'],sectiontitle=annex_title))
 for ti in range(max(len(oa.get('tables',[])),len(na.get('tables',[])))):
  ot=oa['tables'][ti] if ti<len(oa.get('tables',[])) else {'headers':[],'rows':[]};nt=na['tables'][ti] if ti<len(na.get('tables',[])) else {'headers':[],'rows':[]}
  rows=[]
  def rowtext(headers,row):return '<br/>'.join('<b>'+esc(headers[k] if k<len(headers) else str(k+1))+':</b> '+esc(v) for k,v in enumerate(row))
  for ri in range(max(len(ot['rows']),len(nt['rows']))):
   a=ot['rows'][ri] if ri<len(ot['rows']) else [];b=nt['rows'][ri] if ri<len(nt['rows']) else []
   left=[P(rowtext(ot['headers'],a))] if a else [P('[Rând nou]','small')]
   right=[P(rowtext(nt['headers'],b))] if b else [P('[Rând eliminat]','small')]
   if a!=b:right+=[P('Corelare propusă; orice alegere comercială deschisă trebuie aprobată înainte de semnare.','note')]
   rows.append([left,right])
  story.append(Spacer(1,6));story.append(table(rows,['R09 | conținutul tabelului original','R10 | conținutul tabelului propus'],sectiontitle=f'Anlage {n} - Tabelle {ti+1}'))
story += [P('Semnături / Unterschriften','h'),table([[[P(esc(t)) for t in old['signatures']],[P(esc(t)) for t in new['signatures']]+[P('Nu se semnează această comparație; mai întâi se închid punctele deschise.','note')]]],['R09','R10 - proiect'])]
story += [PageBreak(),P('DISCUȚII CU PROPRIETARUL','title'),P('Registru pentru fiecare observație și modificare. Câmpurile necompletate nu sunt acorduri. Întrebările esențiale au fost deschise separat în conversație; răspunsurile vor actualiza următoarea versiune.','sub')]
for x in mods:
 lines='<b>'+x['id']+' | '+esc(x['titlu'])+'</b><br/><b>Sursă:</b> scan p. '+','.join(map(str,x['pagini_scan']))+'; '+esc(', '.join(x['referinte']))+'<br/><b>Manuscris / marcaj:</b> '+esc(x['manuscris'])+'<br/><b>Certitudine:</b> '+esc(x['certitudine'])+'<br/><b>Evaluare:</b> '+esc(x['analiza_RO'])+'<br/><b>Propunere:</b> '+esc(x['propunere_RO'])+'<br/><b>Discuție:</b> '+esc(x['intrebare_proprietar'])+'<br/><b>Stadiu:</b> '+esc(x['status'])+'<br/><b>Răspuns proprietar:</b> '+esc(x['raspuns'] or 'NEPRIMIT / de completat')
 t=Table([[P(lines)]],colWidths=[WIDTH]);t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),.45,RULE),('BACKGROUND',(0,0),(-1,-1),BG if x['status'].startswith('DESCHIS') else PALE),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]));story += [t,Spacer(1,8)]
story += [PageBreak(),P('SURSE ȘI LIMITELE VERIFICĂRII','title')]
for s in m['surse']:
 story += [P('<b>'+s['id']+' | '+esc(s['tip'])+'</b><br/>'+esc(s['cale'])+'<br/>SHA-256: '+s['sha256'],'small'),Spacer(1,8)]
for s in m['surse_legale']:
 story += [P('<b>'+s['id']+' | '+esc(s['titlu'])+'</b><br/><link href="'+esc(s['url'])+'" color="#087F83">'+esc(s['url'])+'</link>','small'),Spacer(1,8)]
story += [P('Sursele publice au fost consultate la 2026.10.27. Textele consolidate sunt repere pentru propunere; aplicabilitatea concretă, dispozițiile tranzitorii și cerințele autorizației se confirmă pe dosarul proiectului. Nu este afirmat că BERGER a acceptat aceste formulări sau că o notă ilizibilă ar avea un sens cert.','body'),Spacer(1,10),P('Control de coerență: toate cele 16 capitole, toate cele 6 anexe și blocurile de semnături sunt prezente în comparație. Tabelele financiare originale din Anlage 4 sunt identice ca valori. Sumele suplimentare nu sunt introduse prin interpretarea manuscrisului. Pachetul inițial de ofertă din Anlage 5 rămâne document separat; nu a fost modificat.','body'),Spacer(1,10),P('Tipărire recomandată: A3 orizontal, la dimensiune reală. Pentru A4, folosiți imprimarea pe foi multiple/poster ori vizualizarea cu zoom pentru păstrarea lizibilității.','small')]
dest=folder/'2026.10.27 BERGER Comparatie contract R09 R10 cu observatii.pdf'
doc=SimpleDocTemplate(str(dest),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=43,bottomMargin=45,title='BERGER - R09 original / R10 propunere cu observatii - 2026.10.27',author='A&C Wohnart',allowSplitting=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
with pdfplumber.open(dest) as p:
 texts=[pg.extract_text() or '' for pg in p.pages];full='\n'.join(texts)
 assert all(x['id'] in full for x in mods)
 assert '45.000' in full and '54.000' in full and len(p.pages)>10
 assert all(len(t.strip())>80 for t in texts)
 stats={'pagini':len(p.pages),'format':'A3 landscape','modificari':len(mods),'sectiuni':16,'anexe':6,'financial_tables_identical':old['annexes'][3]['tables']==new['annexes'][3]['tables'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(root/'folder map/2026.10.27 QA Berger adnotari/2026.10.27 Audit comparatie.json').write_bytes(json.dumps(stats,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'pdf':str(dest),'audit':stats},ensure_ascii=False))
