from pathlib import Path
import shutil
from xml.sax.saxutils import escape
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
p=Path("Z:/00. Proiecte 2025/AFIR FotoVoltaic 1/Comunicatii oficiale AFIR/2026-10-15 Solicitare 961 - transa 1")
for fn in ['02_Proiect_raspuns_AFIR_961.pdf','AP_raspuns_informatii_suplimentare_COMPLETAT.pdf']:
 shutil.copy2(p/fn,p/'_verificare'/('anterior_'+fn))
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
body=ParagraphStyle('body',fontName='Arial',fontSize=10.5,leading=14.8,spaceAfter=9)
head=ParagraphStyle('head',parent=body,fontName='ArialBold',fontSize=11.5,spaceBefore=10,spaceAfter=9,textColor=colors.HexColor('#17354a'))
title=ParagraphStyle('title',parent=head,fontSize=17,leading=21,spaceAfter=12)
small=ParagraphStyle('small',parent=body,fontSize=9,leading=12)
story=[];plain=[]
def add(t,style=body):
 story.append(Paragraph(escape(t).replace('\n','<br/>'),style));plain.append(t)
add('CESIRO PRODUCTION S.R.L.',head)
add('CUI 45050734 | Nr. ONRC J01/1328/2021\nSediu: municipiul Alba Iulia, str. Theodor Pallady nr. 5, județul Alba',small)
add('Nr. de înregistrare beneficiar: __________ / 16.10.2026',small)
add('Către: Agenția pentru Finanțarea Investițiilor Rurale\nCentrul Regional pentru Finanțarea Investițiilor Rurale 7 Centru Alba Iulia')
add('RĂSPUNS LA SOLICITAREA DE INFORMAȚII SUPLIMENTARE\nNr. 961 din 15.10.2026',title)
add('Registrul-jurnal și clarificarea celor 30 de panouri fotovoltaice suplimentare',head)
add('Proiect: „IMPLEMENTAREA SISTEMULUI FOTOVOLTAIC 1 MW PENTRU AUTOCONSUM PENTRU FABRICA DE PRELUCRARE A NUCILOR, ALUNELOR, PISTACIO ȘI MIGDALELOR”')
add('Contract de finanțare: CFMSES011011372801030/30.12.2024\nCod proiect: FFMSES011011372801030\nDosarul cererii de rambursare: RFMSES011011372801030.1, tranșa 1\nData depunerii dosarului: 25.08.2026',small)
add('Stimată doamnă / Stimate domn,')
add('Subscrisa CESIRO PRODUCTION S.R.L., reprezentată legal prin administrator Cosmin-Adrian Covaciu, în calitate de beneficiar al contractului de finanțare menționat, vă transmitem răspunsul la cele două puncte din solicitarea nr. 961/15.10.2026, comunicată electronic la 15.10.2026.')
add('Proiectul este finanțat din Fondul de Modernizare, prin Schema de ajutor de stat privind sprijinirea investițiilor în noi capacități de producere a energiei electrice din surse regenerabile pentru autoconsumul întreprinderilor din cadrul sectorului agricol și industriei alimentare. Prezentele clarificări și documentele anexate sunt transmise pentru verificarea dosarului de rambursare, în contextul art. 5 alin. (2) și art. 6 alin. (1) din contract și al Anexei IV - Instrucțiuni de plată.')
add('1. Registrul-jurnal aferent operațiunilor proiectului',head)
add('Anexăm extrasul Registrului-jurnal pentru grupa „PROIECT AFIR CFMSES011011372801030”, în 5 pagini, care cuprinde înregistrări contabile aferente proiectului din lunile ianuarie, februarie, martie, aprilie și iulie 2026.')
add('Factura SST0033/03.07.2026, emisă de SUNTREE SOLAR TECH S.R.L., este evidențiată la pagina 5/5, pozițiile 10-12: înregistrarea valorii de 2.466.942,15 lei în conturile 231.1/401.00033, TVA de 518.057,85 lei în conturile 4426/401.00033 și decontarea sumei de 1.435.000,00 lei în conturile 401.00033/4091.1. Acest extras este transmis ca răspuns la punctul 1 al solicitării.')
story.append(PageBreak())
add('2. Clarificarea celor 30 de panouri fotovoltaice suplimentare',head)
add('La vizita pe teren din 08.09.2026 au fost identificate 2.252 de panouri, față de cele 2.222 aprobate pentru proiect. Numărul de 2.222 de panouri aferente proiectului este prevăzut în Actul adițional nr. 1 la contractul CFMSES011011372801030/30.12.2024, înregistrat electronic cu nr. 1.360.244, care aprobă modificările tehnice cu menținerea puterii totale instalate a sistemului de 1 MW.')
add('Proprietatea, proveniența și finanțarea',head)
add('Diferența de 30 de panouri reprezintă panouri aflate în proprietatea domnului Cosmin-Adrian Covaciu, proprietarul clădirii. Acestea au fost achiziționate de proprietar din fonduri personale, distinct de investiția CESIRO PRODUCTION S.R.L. finanțată prin AFIR.')
add('Motivul montării și destinația',head)
add('Cele 30 de panouri au fost montate pentru alimentarea consumurilor aferente iluminatului exterior și altor activități de întreținere și pază ale imobilului. Clădirea utilizată de CESIRO PRODUCTION S.R.L. face parte dintr-un complex de clădiri mai amplu, care include și alte spații decât cele utilizate de societate.')
add('Separarea electrică și raportarea la configurația aprobată',head)
add('Partea utilizată de CESIRO PRODUCTION S.R.L. este separată din punct de vedere electric de restul complexului. Cele 30 de panouri ale proprietarului sunt conectate într-o instalație complet separată electric de instalația fotovoltaică finanțată prin proiectul AFIR.')
add('Prin urmare, cele 30 de panouri nu fac parte din instalația aferentă proiectului și nu determină modificarea configurației sau a puterii aprobate a acesteia. Numărul total constatat la amplasament include atât cele 2.222 de panouri ale proiectului, cât și cele 30 de panouri ale proprietarului. Prezența acestora din urmă la același amplasament nu reprezintă o suplimentare a instalației finanțate prin contract.')
add('3. Documente care însoțesc răspunsul',head)
add('1. Registrul-jurnal pentru grupa „PROIECT AFIR CFMSES011011372801030” - extras în 5 pagini, inclusiv factura SST0033/03.07.2026 la pagina 5.\n2. Actul adițional nr. 1 la contractul de finanțare CFMSES011011372801030/30.12.2024, nr. de înregistrare electronică 1.360.244 - copie, 2 pagini.')
add('Vă rugăm să aveți în vedere prezentele clarificări și documentele anexate la continuarea verificării dosarului cererii de rambursare, tranșa 1.')
add('Cu stimă,\nCESIRO PRODUCTION S.R.L.\nCosmin-Adrian COVACIU\nAdministrator / reprezentant legal\nSemnătura electronică',body)
def footer(c,d):
 c.setStrokeColor(colors.HexColor('#bdcbd3'));c.line(45,40,550,40)
 c.setFont('Arial',8);c.drawString(45,27,'Răspuns la solicitarea AFIR nr. 961/15.10.2026 | CESIRO PRODUCTION S.R.L.');c.drawRightString(550,27,str(d.page))
out=p/'02_Proiect_raspuns_AFIR_961.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=45,rightMargin=45,topMargin=35,bottomMargin=50).build(story,onFirstPage=footer,onLaterPages=footer)
(p/'02_Proiect_raspuns_AFIR_961.txt').write_text('\n\n'.join(plain),encoding='utf-8')
shutil.copy2(Path('16.1 Act aditional 1/Act de semnat AFIR/Act Aditional Semnat/C3.3.4_.pdf'),p/'04_Act_aditional_nr_1_contract_finantare.pdf')
f=p/'AP_raspuns_informatii_suplimentare_COMPLETAT.pdf'
r=PdfReader(f);w=PdfWriter(r,incremental=True);a=w.root_object['/AcroForm']['/XFA']
i=next(i+1 for i in range(0,len(a),2) if str(a[i])=='datasets')
ds=E.fromstring(a[i].get_object().get_data());c=ds.find('{http://www.xfa.org/schema/xfa-data/1.0/}data/cerere')
docs=c.find('listaDocumente/altedocumente')
for x in list(docs): docs.remove(x)
texts=[
('Răspuns la solicitarea de informații suplimentare nr. 961/15.10.2026 - Registrul-jurnal și clarificarea celor 30 de panouri fotovoltaice suplimentare; proiect FFMSES011011372801030, contract CFMSES011011372801030/30.12.2024.',str(len(PdfReader(out).pages))),
('Registrul-jurnal pentru grupa PROIECT AFIR CFMSES011011372801030 - extras, inclusiv înregistrarea facturii SST0033/03.07.2026 la pagina 5 (Cesiro_Production_registru_jurnal_16102026_142808.pdf).','5'),
('Actul adițional nr. 1 la contractul de finanțare CFMSES011011372801030/30.12.2024, nr. de înregistrare electronică 1.360.244 - copie.','2')
]
for n,(txt,pages) in enumerate(texts,1):
 d=E.SubElement(docs,'document')
 for key,val in [('Nr',str(n)),('Descriere',txt+' '+pages+' pagini.'),('Pagini',pages)]: E.SubElement(d,key).text=val
a[i].get_object().set_data(E.tostring(ds,encoding='utf-8'))
tmp=p/'_verificare/formular_actualizat.pdf';w.write(tmp);shutil.copy2(tmp,f)
print('Raspuns pagini:',len(PdfReader(out).pages))
print('Formular actualizat; date beneficiar pastrate.')

