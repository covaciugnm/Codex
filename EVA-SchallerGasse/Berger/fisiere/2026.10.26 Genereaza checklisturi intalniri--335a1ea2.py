from pathlib import Path
import json,hashlib
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Flowable,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

root=Path.cwd();out=root/'00.Proiect/09. Vertraege/2026.10.26 Checklisturi intalniri'
out.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('AR','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ARB','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('AR',normal='AR',bold='ARB',italic='AR',boldItalic='ARB')
navy=colors.HexColor('#15394D');teal=colors.HexColor('#087E83');gray=colors.HexColor('#536773');line=colors.HexColor('#D5DFE3');pale=colors.HexColor('#EEF5F6')
styles={
 'title':ParagraphStyle('title',fontName='ARB',fontSize=22,leading=25,textColor=navy,spaceAfter=7),
 'sub':ParagraphStyle('sub',fontName='AR',fontSize=10,leading=14,textColor=gray,spaceAfter=8),
 'h':ParagraphStyle('h',fontName='ARB',fontSize=12,leading=15,textColor=teal,spaceBefore=10,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='AR',fontSize=9.2,leading=12.5,textColor=navy),
 'small':ParagraphStyle('small',fontName='AR',fontSize=8,leading=10.5,textColor=gray),
 'cell':ParagraphStyle('cell',fontName='AR',fontSize=8.8,leading=11,textColor=navy),
 'white':ParagraphStyle('white',fontName='ARB',fontSize=8.6,leading=11,textColor=colors.white),
}
def P(t,style='body'):return Paragraph(t,styles[style])
def esc(t):return escape(t)
class Box(Flowable):
 def __init__(self):super().__init__();self.width=11;self.height=11
 def draw(self):self.canv.setStrokeColor(teal);self.canv.setLineWidth(.75);self.canv.rect(0,1,8,8)
def checks(rows):
 t=Table([[Box(),P('<b>'+esc(title)+'</b> '+esc(body))] for title,body in rows],colWidths=[18,497],hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(1,0),(-1,-1),.35,line)]));return t
def fees(rows):
 data=[[P('Poziție / serviciu','white'),P('EUR net','white')]]+[[P(esc(a),'cell'),P(esc(b),'cell')] for a,b in rows]
 t=Table(data,colWidths=[418,97],hAlign='LEFT')
 st=[('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,-1),.3,line)]
 for i in range(1,len(data)):
  if i%2==0:st.append(('BACKGROUND',(0,i),(-1,i),pale))
 t.setStyle(TableStyle(st));return t
def notice(text):
 t=Table([[P(text,'small')]],colWidths=[515]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),pale),('BOX',(0,0),(-1,-1),.5,line),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));return t
def decisions():
 data=[[P('Concluzie / modificare agreată','white'),P('Responsabil / termen','white')]]
 data += [['',''] for _ in range(3)]
 t=Table(data,colWidths=[365,150],rowHeights=[24,24,24,24]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('GRID',(0,0),(-1,-1),.4,line),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7)]));return t
sources={
 'BERGER_R09':'00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09/2026.10.13 Werkvertrag BERGER R09.pdf',
 'BERGER_OFFER':'00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09/2026.10.13 Anlage 5 Originalangebot BERGER 2026.08.17.pdf',
 'PECH_R09':'00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09/2026.10.13 Werkvertrag PECH R09.pdf',
 'PECH_AN01':'00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09/2026.10.13 Anlage 5 Originalangebot PECH 2026.09.17.pdf',
 'PECH_AN02':'00.Proiect/09. Vertraege/zt-pech.at/2026.10.21 Oferta suplimentara AN02/2026.10.21 Oferta suplimentara PECH 2026-470 AN02.pdf',
 'PECH_EMAIL':'08. Corespondenta/2026.10.21 Verificare Berger Pech/2026.10.21 15-30-15 PRIMIT Pech 9e27d51f.txt',
}
data={
'BERGER':{
 'meeting':'2026.10.27 | 11:30 ora Vienei | Schönbrunner Straße 123/2, 1050 Wien',
 'price':[('Calcule / Ausführungsstatik','13.000,00'),('Planuri de construcție și execuție','20.000,00'),('Asistență statică - maximum 8 vizite','2.000,00'),('Prüfingenieur','10.000,00'),('TOTAL ofertă inițială / R09','45.000,00')],
 'money':'<b>Total: 45.000 EUR net / 54.000 EUR cu TVA 20%.</b> R09 cere un pachet extins; acceptarea tuturor cerințelor la acest preț trebuie obținută în scris. Oferta originală avea valabilitate 8 săptămâni, până la 2026.10.12; cereți reconfirmarea prețului și disponibilității.',
 'scope':[
 ('1. Obiectul tehnic complet.','Confirmați fundații și subzidiri, lift, consolidări/deschideri în existent, mansardă, balcoane și scări. Închideți lista exactă de elemente și goluri din Anlage 2. [B1 §§2-4]'),
 ('2. Ipotezele ofertei.','Oferta de 13.000 EUR pentru calcule presupune lipsa unei schimbări statice relevante față de predimensionare. Stabiliți ce schimbări există și dacă prețul rămâne aplicabil. [B2 p.2]'),
 ('3. Excavația - exclusă.','Nu adăugați proiectarea Baugrubensicherung/Verbau în sarcina BERGER. Numiți prestatorul separat și datele de sarcină/interfețele pe care BERGER le furnizează; subzidirile clădirii rămân distincte. [B1 §3(4)]'),
 ('4. PI și finalizarea.','Cine preia PI, controalele fizice, rapoartele și certificarea finală ZT? R09 cere acoperire până la final și persoana corespunzătoare; oferta descrie PI până la Rohbaubeschau și o anexă la finalizare. Confirmați întinderea și persoanele, fără costuri presupuse. [B1 §5; B2 p.3]'),
 ('5. Bauwerksbuch complet.','R09 solicită existent + intervenții noi, inspecția inițială și înregistrarea în pachet. Acest serviciu nu este explicit în oferta inițială. Obțineți acordul asupra întinderii, responsabilului, termenelor și acoperirii în cei 45.000 EUR. [B1 §6, Anlage 4]'),
 ('6. Detalii și documente.','Confirmați noduri, ancore, conexiuni, liste, verificarea planurilor de atelier și corecțiile incluse. R09 cere PDF semnat, DWG/DXF/IFC și fișiere native; nu presupuneți că simpla predare electronică din ofertă le acoperă pe toate. [B1 §§4,10; B2 p.3]'),
 ],
 'terms':[
 ('7. Vizitele incluse.','Maximum 8 vizite de asistență statică; o vizită T0 cu asistență efectivă intră în cele 8. Inspecțiile PI sunt separate în R09, fără plafon numeric; nu consumați automat din bugetul de asistență pentru o deplasare exclusiv PI. [B1 §§5,7; Anlage 4]'),
 ('8. Vizitele suplimentare.','Propunerea noastră: pachet comandat expres de 4 vizite = 1.000 EUR net / 1.200 EUR cu TVA. Bugete condiționate: 12 vizite totale = 46.000 net; 16 = 47.000 net. Nu este un tarif suplimentar deja acceptat de BERGER. [B1 p.25-26]'),
 ('9. Durata și pornirea.','Confirmați 18 luni de șantier de la B0 real, față de circa 12 luni în oferta inițială. T0 = începerea proiectării, B0 = începerea execuției; consemnați separat datele și închiderea documentației. [B1 §9; B2 p.1]'),
 ('10. Livrările.','R09 propune D1-D5 la 3/6/8/10/12 săptămâni de la T0. Conveniți date reale, condițiile de pornire, timpul de control și corecțiile înainte de execuție. Numiți persoana și resursele care susțin calendarul. [B1 §9; Anlage 3]'),
 ('11. Calendarul cu valori.','Cereți anexa de livrare/facturare cu sume pe rezultate verificabile. R09 păstrează plata după Leistungsbild, fără tranșe procentuale fixe: definiți când poate fi facturată fiecare parte și evitați dubla facturare. [B1 §§11-12; Anlage 4]'),
 ('12. Condițiile comerciale.','R09: plată 14 zile, fără Haftrücklass și fără penalitate contractuală. Confirmarea urmărită: preț fără indexare pentru întinderea convenită, 18 luni și garanția contractuală de 3 ani. Nu reintroduceți condițiile comerciale mai dure din versiunile vechi. [B1 §§11-13]'),
 ('13. Costuri externe și schimbări.','Identificați investigațiile, deschiderile, geotehnica și topografia necesare, cine le comandă și cât costă. Pentru suplimente reale cereți obiect, tarif/plafon și efectul asupra termenelor, distinct de corectarea erorilor proprii. [B1 §§8,11; B2 p.3]'),
 ('14. Pachetul de închis.','Completați Anlagen 2-3 și 6, numele PI/ZT, drepturile de utilizare și predarea la încetare. Confirmați documentele care vor forma pachetul semnat, inclusiv oferta originală separată, și cereți observațiile rămase în scris. [B1 §§10,15-16; Anlagen]'),
 ],
 'refs':'B1: Propunerea BERGER R09, 2026.10.13, 29 pagini; repere: §§3-7, 9-13 și Anlagen 2-6. B2: Oferta originală BERGER, 2026.08.17, 4 pagini. Datele întâlnirii: răspuns primit 2026.10.24. Ciorna confirmării este NETRIMISĂ la ultimul control.',
},
'PECH':{
 'meeting':'2026.10.27 | 14:00 ora Vienei | Johann-Strauß-Gasse 32/6, 1040 Wien',
 'price':[('AN01 / 01 Ausführungsstatik','42.000,00'),('AN01 / 02 Durchbruchsplanung Bestand','6.000,00'),('AN01 / 03 Baugrubensicherung','5.000,00'),('AN01 / 04 Untergrundbeschau','800,00'),('AN01 / 05 Baubegleitung - 12 controale','14.000,00'),('AN01 / 06 Schlussunterlagen','1.500,00'),('TOTAL AN01 / baza R09','69.300,00'),('AN02 / Prüfingenieur','3.500,00'),('AN02 / Fertigstellungsanzeige','1.800,00'),('AN02 / Bauwerksbuch','3.000,00'),('TOTAL supliment AN02','8.300,00')],
 'money':'<b>AN01: 69.300 net / 83.160 cu TVA. AN02: 8.300 net / 9.960 cu TVA.</b> Cumul aritmetic: 77.600 net / 93.120 cu TVA, înainte de opțiuni sau indexare. Nu este un total acceptat. R09 nu include încă în preț cele trei funcții complete; întinderea și suprapunerile trebuie reconciliate cu AN02.',
 'scope':[
 ('1. Funcția PI completă.','Confirmați persoana, programul de controale, rapoartele, durata și ce acoperă cei 3.500 EUR din AN02. Delimitați PI de cele 12 controale proprii din AN01, fără dublă deplasare/facturare pentru aceeași prezență. [P1 §§5,7; P2; P3 p.2]'),
 ('2. Certificarea finală ZT.','AN02 de 1.800 EUR descrie colectarea documentelor și formularelor, iar depunerea revine beneficiarului/reprezentantului. Cereți explicit cine semnează certificarea ZT integrală, ce verifică și dacă există cost separat; nu echivalați compilarea cu certificarea. [P1 §5; P3 p.2]'),
 ('3. Bauwerksbuch.','Confirmați existent + lucrări noi, inspecția inițială, inventarul, remediile/intervalele și înregistrarea, responsabilul și termenele. AN02 spune creare cu controale și intervale, fără toate aceste detalii explicite. [P1 §6; P3 p.2]'),
 ('4. Golurile și planurile.','Pentru cei 6.000 EUR confirmați lista completă de goluri/buiandrugi din Anlage 2. Stabiliți detaliile, ancorele, nodurile, listele și contribuțiile tehnice din cele șase poziții, inclusiv corecțiile incluse. [P1 §§2-4; P2 p.2]'),
 ('5. Verbau și subteran.','Confirmați ce intră în cei 5.000 EUR: soluție, calcule, planuri, faze și interfețe. Delimitați observația subsolului de 800 EUR de investigații/laborator și de asistența în șantier. [P1 §§3,8; P2]'),
 ],
 'terms':[
 ('6. Vizite și opțiuni.','AN01: 12 controale, extra 450 EUR net/vizită. R09 solicită și T0 separat inclus, până la 6 opțiuni individuale și 18 luni de la B0. Confirmați aceste completări; 6 opțiuni = 2.700 net / 3.240 cu TVA. [P1 §§7,9; Anlage 4; P2]'),
 ('7. Calendar executabil.','PECH a cerut 4 săptămâni de avans pentru cofraj/armare și a refuzat termene concrete dependente de constructor. Conveniți date și condiții pentru D1-D5 (R09: 3/6/8/10/12 săptămâni), cu avansul necesar și calendarul constructorului. [P1 §9; P4]'),
 ('8. Facturarea pe etape.','Confirmați/corectați împreună E1-E7 din Anlage 4, cu rezultate, date și valori; este doar o repartizare de lucru. Repartizați separat suplimentele acceptate, fără modificarea nejustificată a celor șase sume inițiale și fără suprapuneri. [P1 §12; Anlage 4]'),
 ('9. Plata și reținerea.','R09 cere 30 zile și 5% Haftrücklass sau garanție echivalentă. PECH cere 14 zile și nicio reținere. Notați soluția agreată și actualizați toate clauzele/anexele afectate înainte de semnare. [P1 §12; P2; P4]'),
 ('10. Indexarea și regia.','R09 cere preț fix; PECH cere indexare conform AGB. Conveniți aplicarea/baza/limitele și costul total. Regie ofertată: 195/145/125/95 EUR net/oră după rol; identificați aprobarea și plafonul suplimentelor, cheilor și staționărilor. [P1 §11; P3 p.2,4; P4]'),
 ('11. Penalități și documentare.','PECH cere eliminarea penalităților și reducerea rapoartelor săptămânale/registrelor. R09 are 0,1% pe zi lucrătoare imputabilă din etapa afectată, plafon 5% din pachet. Conveniți soluția, plus un minim practic de rapoarte, planuri și decizii urmărite. [P1 §13; P4]'),
 ('12. Predare și utilizare.','Confirmați PDF semnat, DWG/DXF/IFC, fișiere native, As-built și folosirea/continuarea de către alți specialiști. Clarificați diferența dintre drepturile cerute în R09 și drepturile rezervate în AGB. [P1 §10; P3 p.4]'),
 ('13. Documentele finale.','Stabiliți dacă se semnează R09 revizuit sau o comandă cu anexele convenite și ce document prevalează. PECH preferă ofertele semnate, care includ acceptarea AGB. Completați roluri, calendar, valori, date de facturare și adresa firmei: antetul ofertei are 32/11, emailul de întâlnire 32/6. [P1; P3 p.1,3; P4]'),
 ],
 'refs':'P1: Propunerea PECH R09, 2026.10.13, 35 pagini; mai ales §§5-7, 9-13, Anlagen 3-4. P2: AN01, 2026.09.17. P3: AN02, 2026.10.21. P4: Email PECH primit 2026.10.21, ID 9e27d51f. Întâlnire: răspuns 2026.10.22; ciorna confirmării era NETRIMISĂ la ultimul control.',
}}
def footer(c,doc):
 c.setStrokeColor(line);c.line(40,34,555,34);c.setFont('AR',7.3);c.setFillColor(gray)
 c.drawString(40,22,'A&C Wohnart | Schallergasse 35 | Fișă internă | 2026.10.26')
 c.drawRightString(555,22,str(doc.page))
for name,d in data.items():
 story=[P('CHECKLIST | '+name,'title'),P(esc(d['meeting']),'sub'),notice('Fișă internă pentru întâlnire. <b>R09 este propunerea noastră, nu un contract acceptat.</b> Bifați doar după clarificare; consemnați răspunsurile și documentele care vor fi confirmate în scris.'),P('01 / Prețuri și întinderea serviciilor','h'),fees(d['price']),Spacer(1,7),notice(d['money']),Spacer(1,3),checks(d['scope']),PageBreak(),P(name+' | DECIZII DE ÎNCHIS','title'),P('02 / Calendar, costuri suplimentare și condiții','sub'),checks(d['terms']),P('Consemnarea rezultatului','h'),decisions(),Spacer(1,8),P('<b>Surse și repere:</b> '+esc(d['refs']),'small'),Spacer(1,5),P('Excluderi urmărite în ambele pachete: BauKG și REALiG Baumanagement / Planung. Nu adăugați aceste servicii prin formulări generale.','small')]
 path=out/('2026.10.26 Checklist intalnire '+name+'.pdf')
 SimpleDocTemplate(str(path),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=35,bottomMargin=45,title='Checklist întâlnire '+name+' - 2026.10.27',author='A&C Wohnart').build(story,onFirstPage=footer,onLaterPages=footer)
manifest={'data':'2026.10.26','meeting':'2026.10.27','checklists':data,'sources':{k:{'cale':v,'sha256':hashlib.sha256((root/v).read_bytes()).hexdigest()} for k,v in sources.items()},'nota':'Doar checklisturi interne; contractele și ofertele nu au fost modificate. Valorile ofertate și cele propuse sunt diferențiate.'}
(out/'2026.10.26 Surse si continut checklisturi.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'folder':str(out),'outputs':[str(p) for p in out.glob('*.pdf')]},ensure_ascii=False))
