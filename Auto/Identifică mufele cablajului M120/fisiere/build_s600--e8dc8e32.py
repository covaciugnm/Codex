from pathlib import Path
import json, math
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import ezdxf

OUT=Path(r'D:\Auto\Cablaj S600\Documentatie reconstructie'); OUT.mkdir(parents=True,exist_ok=True)
TMP=OUT/'Verificare'; TMP.mkdir(exist_ok=True)
FONT=Path(r'C:\Windows\Fonts')
pdfmetrics.registerFont(TTFont('Arial',str(FONT/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialB',str(FONT/'arialbd.ttf')))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialB',italic='Arial',boldItalic='ArialB')
styles=getSampleStyleSheet()
for k in ['Normal','BodyText','Heading1','Heading2','Title']:
 styles[k].fontName='ArialB' if k in ['Heading1','Heading2','Title'] else 'Arial'
styles['BodyText'].fontSize=9; styles['BodyText'].leading=13
styles.add(ParagraphStyle(name='Cell',fontName='Arial',fontSize=7.3,leading=10))
styles.add(ParagraphStyle(name='Smallx',fontName='Arial',fontSize=8,leading=11))
navy=colors.HexColor('#17324D'); teal=colors.HexColor('#087E8B')
S={
'S01':('Mercedes România - piese originale','https://www.mercedes-benz.ro/passengercars/services/genuine-parts.html'),
'S02':('Mercedes B2B Connect - comandă piese','https://b2bconnect.mercedes-benz.com/ro/help/faq/mercedes-benz-genuine-parts-and-products'),
'S03':('TE 282189-1 - fișă producător','https://www.te.com/en/product-282189-1.html'),
'S04':('TME România - carcasă 282189-1','https://www.tme.eu/ro/details/282189-1/conectori-automotive/te-connectivity/'),
'S05':('Mouser - alternativă 282189-1','https://www.mouser.co.uk/en/ProductDetail/TE-Connectivity-AMP/282189-1?qs=ZDXmSm13591Xq1pSitNwJg%3D%3D'),
'S06':('TE 929939-3 - terminal','https://www.te.com/en/product-929939-3.html'),
'S07':('TME România - terminal 929939-3','https://www.tme.eu/ro/details/929939-3/conectori-automotive/te-connectivity/'),
'S08':('TME - garnitură albastră 828904-1','https://www.tme.eu/ro/details/828904-1/conectori-automotive/te-connectivity/'),
'S09':('TME - garnitură albă 828905-1','https://www.tme.eu/en/details/828905-1/automotive-connectors/te-connectivity/'),
'S10':('LAPP 0046001 - 2X0,75','https://www.lapp.com/de/de/oelflex-heat-180-sihf/p/0046001'),
'S11':('HELU - catalog producător, SiHF','https://www.helukabel.de/HELUKABEL/Publikationen/Kataloge/HELUKABEL_CW_Short-Form-Catalogue_EN_0520.pdf'),
'S12':('Geca Electric - SiHF VOP 2x0,75','https://www.gecaelectric.ro/cabluri/sihf-2-x-0-75-6-1848.html'),
'S13':('Cablezone - SiHF-OB 2x0,75','https://www.cablezone.ro/catalog/alte-cabluri/cabluri-si-conductori-cu-izolatie-din-silicon/sihf-ob-2x0-75'),
'S14':('Elektrobode - HELU 23001 2x0,75','https://www.elektrobode.nl/products/helukabel-sihf-2x0-75mm2-23001'),
'S15':('HELU-sklep - 23104 3x0,75','https://www.helukabel-sklep.pl/sihf-3x0-75-czerwono-brazowyizol-silikon-elast-300-500vczerwono-brazowy-odp-temp-180-3-85546'),
'S16':('Bürklin - HELU 23105 4x0,75','https://www.buerklin.com/en/p/helu/control-cables/23105/93F2570/'),
'S17':('FCP Euro - Mercedes A0115457128','https://www.fcpeuro.com/products/mercedes-coolant-level-sensor-housing-connector-2-pin-0015457128'),
'S18':('TE DR-25-3/8-0-SP - producător','https://www.te.com/en/product-5039264026.html'),
'S19':('Cablecraft - fișă DR-25, vânzare la metru','https://www.cablecraft.co.uk/mwdownloads/download/link/id/651'),
'S20':('tesa 51036 PV2 - producător','https://www.tesa.com/en-us/industry/tesa-triple-a-51036-2.html'),
'S21':('IPD - tesa 51036','https://www.ipdusa.com/products/21999/Tesa-51036-High-Heat-Harness-Tape-Aftermarket'),
'S22':('Kurth - cablaj nou A1405404705','https://kurth-classics-autoparts.de/gb/wiring-harness/14-mercedes-engine-harness-a1405404705.html'),
'S23':('Stolk - contact rotund A0035452626','https://www.stolkcarparts.com/en/product/soldeerkabelschoen-stekkerhuls-mercedes/'),
}
def P(s,style='BodyText'):return Paragraph(s,styles[style])
def txt(s):return escape(str(s)).replace('\n','<br/>')
def tab(headers,rows,widths):
 data=[[P(txt(c),'Cell') for c in headers]]+[[P(txt(c),'Cell') for c in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('TEXTCOLOR',(0,0),(-1,0),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F5F8'),colors.white]),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#CDD8DF')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 # Paragraphs need explicit header text colour.
 for p in data[0]: p.style=ParagraphStyle('th',parent=styles['Cell'],textColor=colors.white,fontName='ArialB')
 return t
story=[]
def h(s):story.append(P(s,'Heading1'))
def p(s):story.append(P(s));story.append(Spacer(1,7))
def page():story.append(PageBreak())
def table(hd,rs,ws):story.append(tab(hd,rs,ws));story.append(Spacer(1,10))

h('S600 / W140 / M120');p('<b>Dosar de achiziție și reconstrucție cablaj A1405404705</b><br/>Revizia P01 • 30 octombrie 2026 • Document preliminar pentru ofertare și măsurători')
p('Două variante: A - cablaj/piese originale Mercedes; B - realizare din componente separate și cabluri multiconductoare. Cantitățile de rezervă sunt distincte de piesele montate. Nu sunt incluse cablajele clapetelor, debitmetrelor sau alte ansambluri care nu au fost identificate în fotografii.')
p('<b>Stare tehnică:</b> codul cablajului și unele carcase sunt identificabile. Pinajul electric, derivațiile interne, secțiunile originale și lungimile de debitare nu sunt confirmate. PDF-ul și CAD-ul anexat sunt documentație de pregătire; <b>nu sunt o schemă electrică validată pentru montaj sau alimentare.</b>')
table(['Constatare','Bază / consecință'],[
('A1405404705','Cod vizibil pe tub: fotografia 15.15.06 (5).'),
('AMP 963274-1 / A0005454881','Marcajul carcasei conectorului principal; nu identifică automat terminalele interioare.'),
('Numerotare până la 38','Foto 15.15.06 (4). Nu se tratează drept conector ECU de 60 pini. Numărul contactelor populate se inventariază.'),
('12 poziții pentru injectoare','BOM dimensionat pentru cele 12 ramuri; echivalența TE necesită verificarea cheilor și a blocării.'),
('Auxiliare diferite','Mufe cu contacte rotunde: 4, 2 și 1 poziții observate; două terminații fără carcasă și încă o ramură cu burduf necesită inventariere.'),
('A1405461480','Cod observat pe protecția rigidă, nu cod de mufă.')],[140,375])
p('Fotografii: folderul Poze, în D:\\Auto\\Cablaj S600. Denumirile scurte din dosar păstrează ora și sufixul fișierului WhatsApp din 30.10.2026. Etichetele X0, J01...J12 și A1...A5 sunt etichete de lucru create aici; nu sunt indicativi Mercedes și nu exprimă ordinea cilindrilor.')
p('<b>Citirea stocurilor:</b> valorile sunt cele returnate de paginile web consultate la 30.10.2026; unele sunt copii indexate. Nu există rezervare sau verificare în coș. „Neconfirmat” nu înseamnă zero. Transportul, TVA la destinație, debitarea și MOQ se reconfirmă înaintea plății.')

page();h('A. Comandă prin Mercedes')
table(['Reper','Necesar','Ce se cere la ofertare'],[
('A1405404705','1 ansamblu','Disponibilitate nouă, cod înlocuitor oficial, aplicabilitate după VIN și data fabricației; preț cu TVA și termen scris.'),
('A0005454881 / AMP 963274-1','1 ansamblu carcasă','Confirmare carcasă completă cu levier, insert, capac și etanșare; codurile contactelor se cer separat.'),
('A1405461480','1 piesă, dacă deteriorată','Verificare că este exact canalul/capacul observat; nu presupune că include toate elementele riglei.'),
('A0115457128','1 mostră, condiționat','Carcasă auxiliară de verificat pe piesa veche; nu comanda 12 ca mufe de injector.'),
('Restul carcaselor rotunde, burdufuri și contacte','După inventar fizic','Identificare la ghișeu după mostră și VIN; nu există aici coduri confirmate pentru toate.')],[143,75,297])
p('Pentru persoană fizică: solicită oferta departamentului de piese al unui partener autorizat, prin S01. Pentru atelier: B2B Connect permite comandă după înregistrare și asociere aprobată cu retailerul (S02). VIN-ul este util pentru verificarea în catalog, dar cablajul existent poate fi cartografiat fizic fără VIN.')
p('<b>Text pregătit pentru cererea de ofertă:</b>')
rfq='Solicit ofertă pentru un cablaj NOU A1405404705, Mercedes-Benz S600 W140, 1993, motor M120 cu distribuitoare. Atașez fotografiile marcajului și conectorilor. Vă rog confirmați codul înlocuitor, aplicabilitatea după VIN (îl voi comunica la validare), disponibilitatea reală, termenul, prețul cu TVA și condițiile de retur. Separat, vă rog ofertă pentru carcasa A0005454881 / AMP 963274-1, protecția A1405461480 și identificarea contactelor, garniturilor și mufelor auxiliare după mostre. A0115457128 este doar candidat pentru o mufă auxiliară, nu echivalență confirmată de injector. Dacă nu se mai livrează, vă rog răspuns explicit pentru fiecare cod.'
p(txt(rfq));(OUT/'Cerere_oferta_Mercedes.txt').write_text(rfq,encoding='utf-8')
p('<b>Disponibilitate cablaj complet:</b> nu am confirmare de stoc Mercedes. Nu declar piesa retrasă din producție fără răspuns de catalog/dealer. Kurth listează un cablaj nou cu acest cod (S22), însă accesul direct a fost blocat HTTP 403; prețul și stocul rămân neconfirmate. Este o alternativă de ansamblu realizat de un specialist, nu ofertă Mercedes.')

page();h('B. BOM - mufe și contacte')
connectors=[
('B01','Carcasă injector TE 282189-1','12 + 2 rezervă = 14 buc','2 poziții, JPT, cheie/clips de verificat; -30...125°C. Mai întâi 1 mostră.','S03/S04/S05'),
('B02','Terminal TE 929939-3','24 + 6 rezervă = 30 buc','0,5...1 mm²; conductor 0,75 candidat; izolație declarată 1,4...2,7 mm; max.130°C. Validează desenul și sertizarea cu garnitura.','S06/S07'),
('B03','Garnitură TE 828904-1 SAU 828905-1','24 + 6 rezervă = 30 buc în total','Albastră: OD izolație 1,2...2,1 mm; albă: 2,2...3 mm. Se alege după diametrul fiecărei vene, nu mantaua cablului. Nu cumpăra 30 din fiecare.','S08/S09'),
('B04','Conector principal A0005454881 / AMP 963274-1','1 ansamblu','Carcasă nouă separată: sursă neconfirmată. Păstrează originalul dacă trece inspecția mecanică. Nu înlocui cu o mufă generică de 38 pini.','S01/S22'),
('B05','Terminale conector principal','N populate + max(4; 20% rezervă)','Cod și dimensiune necunoscute. Nu presupune JPT 929939-3. Nu se lansează comanda înainte de extragerea unei mostre.','RFQ'),
('B06','Carcasă auxiliară A0115457128','1 mostră; necesar final de confirmat','Candidat OEM cu 2 poziții; compară contactele rotunde, cheia și închiderea cu foto 15.15.04 (6).','S17'),
('B07','Mufă rotundă 4 contacte + burduf','1 observată; a doua ramură de verificat','Identificarea componentei și codurile nu sunt stabilite. Nu desemna alimentare/masă doar după formă.','RFQ'),
('B08','Mufă auxiliară 1 contact + protecție','1 observată','Foto 15.15.04 (3). Cod/contact/diametru de confirmat.','RFQ'),
('B09','Terminații rotunde fără carcase','2 observate; nu adăuga automat două mufe','Foto 15.15.04 (2); pot aparține unor carcase inventariate deja. Candidatul A0035452626 nu are echivalență demonstrată.','S23/RFQ'),
('B10','Garnituri față, clipsuri, capace, burdufuri','12 seturi injector; auxiliare după inventar','Verifică ce include 282189-1. Garniturile individuale de fir B03 sunt separate. Nu dubla clipsurile dacă sunt incluse.','S03/RFQ')]
table(['ID','Piesă / model','Necesar și rezervă','Condiții de acceptare','Surse'],connectors,[28,112,100,223,52])
p('B01-B03 formează un set candidat coerent pentru probă, nu un echivalent confirmat pentru toate mufele din poze. La mostră verifică împerecherea completă, retenția terminalului, etanșarea și ieșirea cablului fără tensiune. Pentru terminalele rotunde, alege sertizare sau lipire numai după construcția piesei originale și fișa contactului.')

page();h('B. Cabluri multiconductoare și metraj')
cables=[
('C01','2X0,75 mm² SiHF; LAPP 0046001 sau HELU 23001','12 ramuri injector: 15 m ipoteză; +20%=18 m; buget comandă 20 m','180°C, OD aprox.6,4 mm. Nu tăia înainte de măsurare. S10/S11/S14.'),
('C02','2X0,75 mm², aceeași construcție','Rezervă AUX: 5 m; condiționată','Exemplu buget: 2 ramuri x1,5 m + marjă. Nu dovedește existența a două circuite de acest tip.'),
('C03','3X0,75 mm² HELU 23104, fără PE','0 m comandă inițială; opțiune 3 m','180°C, OD aprox.6,8 mm. Numai dacă se identifică circuit cu 3 conductoare. S11/S15; MOQ furnizor 10 m.'),
('C04','4X0,75 mm² HELU 23105, fără PE','0 m inițial; buget 5 m dacă se confirmă 2 ramuri','180°C, OD aprox.7,6 mm. Patru poziții nu probează patru vene populate; păstrează perechile dacă există. S11/S16.'),
('C05','2X1,5 mm² LAPP SiHF 0046013','0 m inițial; opțiune 3 m','Pentru circuite confirmate care cer 1,5 mm²; nu este alegere automată pentru orice alimentare/masă. Fișa exactă înaintea comenzii.'),
('C06','Cablu ecranat/torsadat de temperatură','Cantitate și cod de stabilit','Se păstrează construcția originală și terminația ecranului. SiHF simplu nu este înlocuitor automat pentru senzori ecranați.')]
table(['ID','Construcție','Lungime estimată / comandă','Limitări'],cables,[28,150,159,178])
p('<b>C01, calcul transparent:</b> 12 x 1,25 m = 15 m; 20% rezervă = 18 m; rotunjire de aprovizionare = 20 m. Intervalul de sensibilitate pentru 1,0...1,5 m/ramură este 14,4...21,6 m cu rezervă. Dacă media măsurată depășește 1,39 m, cei 20 m nu mai acoperă rezerva de 20%. Lungimile sunt ipoteze pentru trasee complete, nu măsurători din fotografie.')
p('Varianta cu perechi individuale în manta poate necesita o zonă de distribuție protejată. Păstrează exact legăturile comune existente; nu forța două vene într-un contact proiectat pentru una. Un cablu multiconductor trebuie dezizolat la capete: venele sale intră separat în locașurile mufei, cu ieșirea din manta protejată.')
p('Nu comandăm cablu generic „3x...” peste tot. Pentru injector cu două contacte, perechea 2X este mai compactă. Evită variantele 3G/4G și produsele numite 3x care includ în descriere conductor verde-galben. SiF este de regulă monofilar; SiHF este multiconductor. FLRY-B nu este silicon de 180°C. SPEC55 este ETFE și trebuie selectat după construcția exactă, nu după numele familiei.')

page();h('B. Protecții, montaj și scule')
table(['ID','Reper','Cantitate de buget','Selecție / achiziție'],[
('P01','DR-25-3/8-0-SP; TE 5039264026','3 m, pentru segmente locale','9,53 mm înainte /4,8 mm după contracție; -75...150°C. Potrivit dimensional pentru cablu OD6,4 mm, verificat la probă. S18/S19.'),
('P02','Tub fibră de sticlă siliconată','5 m ramuri; 2 m trunchi, estimativ','Diametre după pachet, fișă min.200°C dacă zona o cere. Cod, preț și stoc neconfirmate; RFQ, nu comandă generică de tub corugat.'),
('P03','tesa 51036 PV2','1 rolă 19 mm x25 m, buget','150°C/3000 h în fișa producătorului. Nu folosi banda ca protecție la 180°C; S20/S21. Confirmă varianta și dimensiunea rolei.'),
('P04','Coliere / bride / cleme de fixare','20 buc, estimativ','Preferă refacerea fixărilor originale. Variante termice după zona reală, fără strângerea excesivă a siliconului; cod după diametru.'),
('P05','Identificatori permanenți','60 buc, estimativ','Câte două etichete de ramură plus identificarea venelor; material potrivit temperaturii locale. Nu folosi etichete de hârtie.'),
('P06','Protecție ieșire principală și ramificații','1 set principal + ramuri după probă','Burdufurile trebuie să accepte noul diametru și să descarce tracțiunea; soluție dimensionată după machetă.'),
('P07','Derivații electrice / îmbinări','Necunoscut până la cartografiere','Contacte de îmbinare conforme cu suma secțiunilor; izolare și descărcare mecanică. Nu inventăm numărul nodurilor comune.'),
('T01','Cleşte și matriță pentru terminalul ales','1 set / folosește scule existente','Sertizarea conductorului și suportul izolației/garniturii trebuie validate conform documentației TE; un clește generic nu este automat echivalent.'),
('T02','Extractor, șubler, micrometru, dezizolator','1 set','Extractor compatibil exact cu terminalul, fără deformarea aripioarelor. Măsoară OD venă și mantaua.'),
('T03','Multimetru și sonde; panou de montaj','1 set','Continuitate pe cablaj complet deconectat; scule de verificare a sertizării; șablon 1:1 din cablajul existent.')],[28,146,110,231])
p('Metrajele P01/P02 sunt rezerve de atelier, nu consum măsurat și nu se adună automat ca acoperire integrală a tuturor cablurilor. Nu este stabilit un buget total: lipsesc prețuri/coduri pentru conectorul principal, auxiliare, burdufuri și manoperă.')

page();h('Registru prețuri și disponibilitate')
stock=[
('282189-1 / TME','0 buc afișate','4,06 lei net /4,92 brut la 1 buc','14 buc:68,88 lei brut, numai reper de preț; lipsă stoc. S04'),
('282189-1 / Mouser','15.668 în rezultat indexat; pagina 403','Preț neconfirmat','Nu este stoc live validat. Cere ofertă pentru 14 buc. S05'),
('929939-3 / TME','20.128 buc afișate','0,89 lei net /1,07 brut la 25+','30 buc:32,10 lei brut; MOQ1. S07'),
('828904-1 / TME','Rezultate cache divergente','Preț RO actual neconfirmat','Nu folosim ca stoc actual cifra veche 122.290. S08'),
('828905-1 / TME','51.976 EN /49.064 PL, cache vechi','Preț RO actual neconfirmat','Confirmare în coș; cantitate necesară30 doar dacă OD permite. S09'),
('SiHF2x0,75 / Geca VOP','„În stoc”; număr metri absent','5,67 lei/m afișat','25 m:141,75 lei afișat; confirmă TVA, fișa VOP și disponibilitatea lungimii. Nu echivala automat cu LAPP. S12'),
('SiHF-OB2x0,75 / Cablezone','Stoc epuizat','6,58 lei/m la10...49 m','Doar alternativă de ofertare; TVA de confirmat. S13'),
('HELU23001 / Elektrobode','Număr metri neconfirmat','1,02 EUR net /1,24 incl.TVA local /m','25 m:31 EUR cu TVA afișat; livrare RO, debitare și fiscalitate neconfirmate. S14'),
('HELU23104 / HELU-sklep','„Disponibil”, segment500m; indexat','6,78 PLN brut/m; minim10m','10m=67,80 PLN +61,50 PLN debitare sub100m; transport separat. Nu comanda dacă nu există circuit3 vene. S15'),
('HELU23105 / Bürklin','600m în5 zile în pagina indexată','2,6656 EUR/m, prag100m','Nu este stoc imediat; oferta pentru5m neconfirmată. La100m:266,56 EUR. S16'),
('A0115457128 / FCP','„In Stock”, număr absent','3,29 USD/buc','1 mostră numai după comparație; import/transport separat. S17'),
('tesa51036 / IPD','„In Stock” în rezultat indexat','7,59 USD/rolă','Varianta PV2 și dimensiunea de confirmat; nu este ofertă locală RO. S21'),
('A1405404705 / Mercedes','Neconfirmat','La ofertă','Nu există aici preț sau termen garantat. S01'),
('A1405404705 / Kurth','Neconfirmat; acces403','La ofertă','Cablaj complet nou listat; solicitare separată. S22')]
table(['Produs / furnizor','Stoc public citit','Preț unitar','Cost / condiții'],stock,[115,112,112,176])
p('Nu am efectuat comenzi și nu am trimis mesaje furnizorilor. Prețurile din monede diferite nu sunt însumate. Costul cablajului complet nu poate fi dedus din subtotalul mufelor de injector și al cablului.')

page();h('Validarea cablului înainte de comandă')
p('<b>Temperatura nu este singurul criteriu.</b> SiHF industrial este candidat de prototip, nu certificare automată pentru compartimentul motor. Cere producătorului acceptul pentru ulei, vapori/stropire combustibil, vibrații, cicluri termice și raza minimă de curbură în montajul propus. Nu sunt asumate rezistența la imersie în benzină sau flexarea continuă.')
table(['Interfață','Criteriu de acceptare'],[
('Cablu - contact','Secțiunea intră în domeniul contactului; construcția lițată este admisă; sertizarea este verificată. Nu micșora secțiunea originală și nu dimensiona alimentări după presupuneri.'),
('Venă - garnitură','Măsoară diametrul peste izolație. Pentru 929939-3 și garnitura albă, zona comună nominală este 2,2...2,7 mm; pentru albastră,1,4...2,1 mm. Desenul terminalului/fișa aplicației prevalează; pagina TE are unități imperial/metrice inconsecvente.'),
('Manta - burduf','6,4 mm este diametrul cablului2X0,75, nu al unei vene. Nu trece mantaua prin garnitura unei singure vene. Protejează separat desprinderea celor două vene.'),
('Pachet - canal','12 cabluri OD6,4 mm au circa386 mm² arie geometrică însumată. La umplere ipotetică60%, diametrul circular echivalent este28,6 mm, fără auxiliare/protecții. Este calcul de gabarit, nu regulă de omologare.'),
('Temperatură ansamblu','Mufa125°C și terminalul130°C limitează local ansamblul; DR-25150°C, tesa150°C/3000h; cablul180°C nu ridică limitele celorlalte piese.'),
('Topologie electrică','Identifică toate nodurile comune și ecranele. Nu introduce nod comun între bănci sau masă de senzor și masă de putere fără dovada circuitului original.')],[120,395])
p('<b>Ordinea practică:</b> inventariere și măsurare → 1 set probă mufă/contact/garnitură + 1 m cablu → verificare în canal și pe motor → probă de sertizare/etanșare → listă finală de debitare → lot complet. Cantitățile de mostră se scad din comanda finală dacă piesele rămân utilizabile.')
p('Pentru metraj final: măsoară fiecare traseu pe cablajul așezat fără întindere, adaugă necesarul real pentru intrările în mufe și service, apoi însumează separat pe tip de cablu. Rezerva de achiziție se adaugă după calcul; nu se transformă în bucle inutile lângă piese fierbinți sau mobile.')

page();h('Pinaj: ce este necesar pentru schema finală')
p('Schema electrică finală trebuie reconstruită prin continuitate pe cablajul vechi. O fotografie arată forma și uneori numărul locașului; nu arată la ce injector/senzor ajunge fiecare fir. În anexele PDF/CAD nu sunt trasate legături presupuse între X0 și ramuri.')
table(['Pas','Rezultat de înscris'],[
('1. Orientare','Fotografie perpendiculară a fiecărei fețe de împerechere, cu cheia/levierul sus și numerele turnate lizibile. Vederea din spate este în oglindă; nu se copiază numerotarea prin presupunere.'),
('2. Inventar','Pentru fiecare locaș: populat/gol, tip contact, culoare și secțiune. Contactele aparent comune se verifică pe toate ramurile.'),
('3. Continuitate','Cu cablajul separat de mașină, ECU și componente: pin sursă → toate destinațiile. Compensează rezistența sondelor; consemnează valoarea, nu doar semnalul sonor.'),
('4. Derivații','Deschide învelișul controlat, păstrează câte un traseu identificabil. Izolația degradată poate crea scurtcircuite false; confirmă fiecare nod prin inspecție și măsurare repetată.'),
('5. Dimensionare','Măsoară conductorul și lungimea utilă; validează curentul, căderea de tensiune și temperatura pentru circuitele de putere. Copiază ecranarea/torsadarea când există.'),
('6. Verificare nou','Verificare100% pin-la-pin, absența legăturilor suplimentare, retenție și mecanică. Orice test cu tensiune de izolație se face doar pe cablaj izolat, conform unei proceduri adecvate; nu aplica megohmmetru pe ECU/senzori.')],[105,410])
p('<b>Condiție de emitere revizie de execuție:</b> toate cele38 locașuri inventariate, toate capetele identificate, toate nodurile/ecranele documentate și comparate, lista de debitare măsurată și probele de componente acceptate. Fără acestea, un pinaj detaliat „completat” ar fi o invenție.')
p('Fișierele Plan_cablare_P01.pdf și Plan_cablare_P01.dxf conțin registrul logic al ramurilor, locașurile X0 și fișa conexiunilor necompletate. Desenul nu reprezintă poziția geometrică a pinilor în carcasă și nu atribuie ramurile cilindrilor. Conversia DWG este livrată numai dacă se generează și se validează efectiv.')

page();h('Surse tehnice și linkuri de comandă')
for key,(label,url) in S.items():
 story.append(P(f'<b>{key} - {txt(label)}</b><br/><link href="{escape(url)}" color="#087E8B">Deschide pagina produsului / furnizorului</link>','Smallx'))
 story.append(Spacer(1,8))
def footer(c,d):
 c.setFont('Arial',7);c.setFillColor(navy);c.drawString(40,24,'S600 • A1405404705 • P01 • PRELIMINAR - pinaj nevalidat');c.drawRightString(A4[0]-40,24,str(d.page))
doc=SimpleDocTemplate(str(OUT/'BOM_S600_doua_variante_P01.pdf'),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=34,bottomMargin=40,title='S600 - BOM doua variante - preliminar',author='Dosar de reconstructie')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

# Standalone clickable purchasing register, not a spreadsheet.
html=['<!doctype html><meta charset="utf-8"><title>Surse BOM S600</title><style>body{font:16px Arial;max-width:1100px;margin:40px auto;line-height:1.5}td,th{border:1px solid #bbb;padding:10px;vertical-align:top}table{border-collapse:collapse}th{background:#17324d;color:white}a{color:#087e8b}</style><h1>S600 - surse de cumpărare, P01</h1><p>30.10.2026. Stocuri publice/indexate, fără rezervare. Compatibilitatea candidaților se verifică înainte de comandă. Consultați BOM-ul PDF.</p><table><tr><th>Produs</th><th>Stoc citit</th><th>Preț</th><th>Condiții</th></tr>']
for row in stock:html.append('<tr>'+''.join('<td>'+escape(x)+'</td>' for x in row)+'</tr>')
html.append('</table><h2>Linkuri directe</h2>')
for k,(label,url) in S.items():html.append(f'<p>{k}: <a href="{escape(url)}">{escape(label)}</a></p>')
(OUT/'Linkuri_cumparare_si_stocuri.html').write_text('\n'.join(html),encoding='utf-8')

# CAD and companion PDF share geometric primitives. Units mm on A3; NOT physical pin geometry.
dw=ezdxf.new('R2000'); dw.units=4; ms=dw.modelspace()
for name,col in [('CADRU',7),('INVENTAR',4),('DE_MASURAT',1),('NOTE',7)]:dw.layers.new(name,dxfattribs={'color':col})
cadpdf=canvas.Canvas(str(OUT/'Plan_cablare_P01.pdf'),pagesize=(420*72/25.4,297*72/25.4))
U=72/25.4; offset=0
def line(x1,y1,x2,y2,layer='NOTE'):
 ms.add_line((x1+offset,y1),(x2+offset,y2),dxfattribs={'layer':layer})
 cadpdf.setStrokeColor(colors.HexColor('#B44B31') if layer=='DE_MASURAT' else navy);cadpdf.setLineWidth(.5);cadpdf.line(x1*U,y1*U,x2*U,y2*U)
def label(x,y,s,size=2.7,layer='NOTE'):
 # ASCII CAD for portability, Unicode in PDF.
 import unicodedata
 asc=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
 ms.add_text(asc,dxfattribs={'height':size,'insert':(x+offset,y),'layer':layer})
 cadpdf.setFont('Arial',size*U);cadpdf.setFillColor(navy);cadpdf.drawString(x*U,y*U,s)
def box(x,y,w,h,title,layer='INVENTAR'):
 for a,b,c,d in [(x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)]:line(a,b,c,d,layer)
 if title:label(x+2,y+h-5,title,2.6,layer)
def frame(title,n):
 box(8,8,404,281,'','CADRU');label(15,279,title,4);label(15,271,'A1405404705 | P01 | 30.10.2026 | PRELIMINAR - NU SE CABLAZA DUPA ACEST DESEN',2.7)
 label(15,15,'Inventar logic; fara scara fizica, fara ordine cilindri. TBD = de masurat. Nicio legatura electrica presupusa.',2.3)
 label(375,15,f'Foaia {n}/3',2.5)
frame('01 / Inventar de interfete si ramuri',1)
box(15,155,95,100,'X0 - conector principal')
for y,s in [(240,'AMP 963274-1'),(232,'Mercedes A0005454881'),(222,'Numerotare observata pana la 38'),(212,'Locasuri populate: TBD'),(202,'Contacte si sectiuni: TBD'),(190,'Nu este declarata interfata ECU.'),(180,'Destinatiile se masoara separat.'),(167,'Nu conectati liniile din presupuneri.')]:label(18,y,s,2.5)
for i in range(12):
 col=i//6; row=i%6; x=130+col*139;y=226-row*30
 box(x,y,128,25,f'J{i+1:02d} - injector (eticheta atelier)')
 label(x+3,y+10,'2 contacte; pinii turnati se transcriu',2.35)
 label(x+3,y+4,'Cablu candidat 2X0,75; L=TBD',2.35)
box(15,40,95,100,'Auxiliare observate - ID provizorii')
for y,s in [(124,'A1: mufa rotunda, 4 contacte'),(113,'A2: a doua ramura cu burduf'),(102,'A3: mufa cu 2 contacte rotunde'),(91,'A4: mufa cu 1 contact rotund'),(80,'A5: 2 terminatii fara carcase'),(65,'A5 poate apartine altor carcase.'),(54,'Functii/pini/cantitati: de verificat')]:label(18,y,s,2.3)
label(130,35,'Etichetele J01...J12 NU inseamna cilindrii 1...12.',3)
cadpdf.showPage();offset=440
frame('02 / Registru locasuri X0 - nu este vedere geometrica',2)
for col in range(2):
 x=15+col*200
 for dx in [0,18,43,98,155,190]:line(x+dx,57,x+dx,257)
 for r in range(21):line(x,257-r*10,x+190,257-r*10)
 for dx,s in [(2,'Pin'),(20,'Populat'),(45,'Destinatie / pin'),(100,'Culoare / mm2'),(157,'R masurat')]:label(x+dx,250,s,2.3)
 for j in range(19):
  n=col*19+j+1;y=240-j*10
  label(x+3,y,str(n));label(x+22,y,'TBD');label(x+46,y,'TBD');label(x+101,y,'TBD');label(x+158,y,'TBD')
label(15,36,'Toate conexiunile sunt NECUNOSCUTE. Notati GOL numai dupa verificarea fizica a locasului.',2.7)
label(15,27,'Se masoara toate destinatiile fiecarui pin, inclusiv noduri comune si ecrane. Nu se presupune legatura 1-la-1.',2.7)
cadpdf.showPage();offset=880
frame('03 / Fisa ramurilor - legaturi si lungimi de completat',3)
widths=[0,25,78,130,182,235,290,390];x=15;top=257
for dx in widths:line(x+dx,77,x+dx,top)
for r in range(19):line(x,top-r*10,x+390,top-r*10)
for dx,s in zip(widths,['ID','Pin mufa A','X0 / nod A','Pin mufa B','X0 / nod B','L traseu m','Observatii']):label(x+dx+2,250,s,2.4)
ids=[f'J{i:02d}' for i in range(1,13)]+['A1','A2','A3','A4','A5']
for i,id in enumerate(ids):
 y=240-i*10;label(x+2,y,id)
 for dx in widths[1:-1]:label(x+dx+2,y,'TBD',2.5)
label(15,63,'Pentru mufe cu mai mult de 2 contacte: adaugati cate un rand pe fiecare pin, pastrand numerotarea turnata.',2.7)
label(15,51,'Dezizolare, sectiune, culoare, ecran, derivatii si intrari in burduf: masurate pe original, nu deduse din poze.',2.7)
label(15,39,'Estimare C01: 12 x 1,25 m x 1,20 = 18 m; buget 20 m. Nu este lista de debitare.',2.7)
label(15,27,'Emitere pentru executie numai dupa completarea si verificarea intregului registru de conexiuni.',2.7)
cadpdf.showPage();cadpdf.save()
dw.set_modelspace_vport(310,center=(650,148));dw.saveas(OUT/'Plan_cablare_P01.dxf')
(OUT/'README.txt').write_text('S600 - Documentatie reconstructie, revizia P01, 30.10.2026\n\nBOM_S600_doua_variante_P01.pdf: achizitie Mercedes si componente separate.\nPlan_cablare_P01.pdf / .dxf: inventar si fise de masurare, NU schema electrica validata.\nLinkuri_cumparare_si_stocuri.html: linkuri directe si disponibilitate publica.\nCerere_oferta_Mercedes.txt: text de trimis de utilizator; nu a fost expediat.\n\nPinajul, lungimile si auxiliarele necesita masurare fizica. Nu alimentati un cablaj construit pe conexiuni presupuse. Stocurile publice pot fi cache; se reconfirma inaintea comenzii.\n',encoding='utf-8')
print(str(OUT));print('PDF, DXF, HTML, TXT generate')



