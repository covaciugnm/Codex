from pathlib import Path
import json,collections,csv,io,hashlib
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
R=Path.cwd();Q=R/'folder map/2026.10.27 QA autorizare';O=R/'00.Proiect/2026.10.27 Audit autorizare si servieta';O.mkdir(exist_ok=True)
d=json.loads((Q/'2026.10.27 Comparatie servieta.json').read_text(encoding='utf-8'));m=json.loads((Q/'2026.10.27 Surse locale.json').read_text(encoding='utf-8'));missing=json.loads((Q/'2026.10.27 Lipsuri nucleu.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
styles=getSampleStyleSheet()
for n in ['Normal','BodyText','Heading1','Heading2','Title']:styles[n].fontName='Arial'
styles['Normal'].fontSize=9;styles['Normal'].leading=12
styles['Title'].fontSize=22;styles['Title'].leading=26;styles['Title'].textColor=colors.HexColor('#163953')
styles['Heading1'].fontSize=16;styles['Heading1'].leading=20;styles['Heading1'].textColor=colors.HexColor('#163953')
styles['Heading2'].fontSize=11;styles['Heading2'].leading=14;styles['Heading2'].keepWithNext=True
styles.add(ParagraphStyle(name='Small',fontName='Arial',fontSize=7,leading=9,wordWrap='CJK'))
story=[]
def p(t,style='Normal'):return Paragraph(escape(t).replace('\n','<br/>'),styles[style])
def add(t,style='Normal'):story.extend([p(t,style),Spacer(1,7)])
def table(headers,rows,widths,small=False):
 data=[[p(x,'Small' if small else 'Normal') for x in headers]]+[[p(str(x),'Small' if small else 'Normal') for x in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3edf3')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#b5c4cd')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,9)])
def page(title):story.append(PageBreak());add(title,'Heading1')
add('Schallergasse 35\nActe pentru MA37 și verificarea servietei','Title')
add('2026.10.27 • Schallergasse 35, 1120 Wien • Verificare documentară')
add('CONCLUZIE: nu este demonstrat un dosar complet și semnat pentru modificările actuale. Servieta accesibilă nu este o copie integrală a arhivei locale.','Heading2')
add('Există deja autorizația MA37/1539234-2021-1 din 2023.04.21 și aprobarea derogării §69 din 2023.03.16. Problema actuală este documentarea proiectului aprobat și încadrarea modificărilor, inclusiv compartimentările și spațiul yoga, în procedura potrivită. Nu rezultă că trebuie obținută automat o autorizație nouă pentru întreaga clădire.')
table(['Prioritate','Ce trebuie rezolvat'],[
('1 • LIPSĂ CONFIRMARE','Setul exact de planuri cu viza MA37 (amtlicher Sichtvermerk), corelat cu decizia. PDF-ul A3 este o prezentare; fișierul online „Einreichplan – Original” este un BESTANDSPLAN/releveu.'),
('2 • DE COMPLETAT','Planwechsel: planuri coordonate, descriere actuală și asumarea de către autorul cu drept de practică; acordul proprietarului, după caz; cerere și dovada depunerii.'),
('3 • DE ACTUALIZAT','Statica, bau fizica/energia, securitatea la incendiu și accesibilitatea pentru soluția actuală. Nu confundați proiectul tehnic sau traducerile cu documentația semnată pentru depunere.'),
('4 • DE CLARIFICAT','Data rămânerii definitive și termenul de începere. Nu am identificat în actele verificate confirmarea MA37 a datei Rechtskraft.'),
('5 • SERVIETĂ','184 fișiere în P1–P17; 118 identice cu fișiere locale, 66 fără corespondent identic SHA-256. P10 și P13–P17 sunt goale. P18–P20 sunt blocate pentru contul folosit.')],[85,430])
add('„Lipsă” în raport înseamnă neidentificat în materialele verificate, nu dovadă că documentul nu există la autoritate. „De actualizat” înseamnă că există o bază istorică, dar corespondența cu proiectul actual nu este confirmată. Lipsa unei ștampile grafice nu echivalează automat cu nevalabilitatea juridică.')
add('Inventarul anterior există: 00.Proiect/00_INHALTSVERZEICHNIS_und_CHECKLISTE.docx (2026.07.09). A fost folosit ca punct de plecare, nu ca dovadă că toate actele sunt încă actuale. Energia nu trebuie amânată automat până la recepție: §63 o cere la depunere în cazurile aplicabile. [L1, L2]')
page('1. Ce trebuie depus și ce avem')
add('Pentru intervențiile actuale, proiectantul trebuie să stabilească dacă este Planwechsel conform §73, Bauanzeige conform §62 sau o altă procedură. Modificările minore pot avea alt regim; nu orice schimbare cere un nou Bescheid. Tabelul este lista de control pentru o depunere de modificare/supraetajare, cu verificarea aplicabilității de către autor. [L3]')
table(['Act / cerință','Avem','Lipsă / următorul pas'],[
('Cerere și identificarea intervenției [L1]','Modele de scrisori MA37; inventarul vechi.','Nu am identificat cererea actuală completată și depusă cu anexele și număr de înregistrare.'),
('Planuri de depunere, autor autorizat; conținut §64 [L2,L4]','P2041 A3, CAD C-01/C-02; releveu; planuri A.01–A.03 și execuție 2026.','Set actual coordonat pentru depunere, semnat; diferențe față de planul oficial aprobate/identificate. Planșa AP 1:50 nu este automat Einreichplan.'),
('Descrierea lucrărilor / Baubeschreibung [L2,L4]','P2041_C_220329_Baubeschreibung.pdf, 7 pagini, proiect vechi.','Descriere actuală pentru yoga, repartizare, structură și instalații; asumare autor.'),
('Proprietar și acord [L1,L2]','Grundbuch actual A&C și documente de cumpărare.','Verificați solicitantul și semnatarul societății; acordul tuturor coproprietarilor dacă este necesar. Nu presupuneți că extrasul CF ține loc de acord.'),
('Împuternicire, dacă depune un reprezentant','Vollmacht Baupolizei.pdf, semnată, 2025.11.17.','Este pentru consultarea arhivei și vechiul proprietar; nu confirmă mandatul A&C pentru depunerea actuală.'),
('Statică preliminară/fundare și excavare [L2]','Statische Vorbemessung + Fundierungskonzept, 297 pagini, 2022.01; VorKonzept 2021.12.07.','Inginerul să confirme/adapteze la soluția actuală. Documentul spune explicit că nu este statică de execuție.'),
('Bau fizică: termic/acustic [L1,L2]','Raport 127 pagini, revizie 2022.09.06.','Actualizare/confirmare pe planul final și semnare. Nu este Ausführungsbauphysik.'),
('Energie și sistem energetic [L1,L2]','Energieausweis în raport, PDF pp.64–65: emis 2021.12.21, valabilitate înscrisă 2031.12.20.','Rubrica semnăturii goală; verificați energia/sistemele actuale, depunerea electronică și justificările cerute. Nu este „inexistent” sau expirat doar din cauza vechimii.'),
('Protecție la supraîncălzire [L2]','Raportul vechi conține capitol de vară.','Confirmare actuală a autorului și corelare cu ferestre, utilizări și sistemele noi.')],[140,175,200])
page('2. Completări tehnice și cerințe condiționale')
table(['Act / cerință','Avem','Lipsă / următorul pas'],[
('Incendiu și apă pentru stingere [L2,L4]','Cerințe în Bescheid; planuri istorice; în folderul Brandschutz există lista _CE_TREBUIE.','Nu am identificat o documentație actuală asumată pentru yoga/ansamblu și dovada disponibilității apei. Stabiliți dacă este necesar un concept separat.'),
('Accesibilitate [L1,L2]','Declarație generală în Baubeschreibung 2022, p.7.','Declarația autorului pentru soluția actuală: acces, lift, trasee, grupuri sanitare și yoga.'),
('Parcări și obligații aferente [L2]','Calcul istoric în Baubeschreibung, p.7.','Recalculare/confirmare după numărul de unități, suprafețe și destinații actuale.'),
('Tabel suprafețe/unități existente [L2]','Releveu și tabele în planurile vechi.','Tabel final pe niveluri, suprafețe brute/utile și numerotări; §63(1)(o), dacă se aplică.'),
('Bauplatz/Baulos și regim urbanistic [L2]','Autorizație și derogare §69; planuri de amplasament istorice.','Clarificați dovada necesară în procedura actuală și eventuala excepție §66; nu marchez automat un nou act obligatoriu.'),
('Canalizare / ape pluviale [L2,L4]','Date istorice și planuri sanitare actuale.','Coordonare evacuare ape; acceptarea apelor pluviale este cerință specifică pentru Neubau, dacă se aplică, nu automat pentru orice Planwechsel.'),
('Arbori stradali; demolare; zone speciale [L2]','Nu există dovadă suficientă în pachetul verificat.','Verificați impactul asupra arborilor, eventual demolare autorizabilă, Seveso și zonă de locuințe subvenționate. Documente numai dacă situația o cere.'),
('PV / suprafețe alternative energetice [L2]','Raportul vechi Energieausweis indică fără PV.','Verificați obligația actuală și dispozițiile tranzitorii; dacă se aplică, amplasare, suprafață, putere și justificări.'),
('Lift / pompă de căldură / activitate yoga','Lift și pompă prevăzute în proiectul vechi; planuri yoga 2026.','Bescheid menționează autorizare separată pentru pompă și cerințe lift. Verificați separat procedurile actuale și eventuala Betriebsanlage; autorizația de construire nu le înlocuiește. [L6]')],[140,175,200])
add('Dovada depunerii inițiale nu trebuie reconstituită numai din arhiva privată: cereți de la MA37 copia completă a dosarului aprobat și lista anexelor. Autorizația existentă dovedește că procedura din 2023 s-a finalizat, nu că orice plan din foldere este planul vizat.')
page('3. Ștampile și semnături: constatări')
add('§65 în forma actuală cere semnarea planurilor, descrierilor și calculelor de către autor; în procedura electronică, semnarea se face electronic. Acordul proprietarului se verifică separat conform §63. Nu aplic cerințe de semnare din versiuni istorice ale §65. [L5,L2]')
table(['Document / pagina PDF','Verificare vizuală','Concluzie'],[
('Baubescheid, D01, p.12','Mențiune/logo Amtssignatur vizibile.','Marcaj oficial prezent în copia scanată. Nu este o validare criptografică a originalului electronic.'),
('P2041 A3, D02, 19 pagini','Prezentare cu antet EIGENSINN; nu am identificat viza MA37 în paginile revizuite.','Eticheta „genehmigt” și numele fișierului nu dovedesc viza oficială. Solicitați setul vizat.'),
('„Einreichplan – Original” din P2, prima pagină','Cartuș BESTANDSPLAN, Office Müllner, 2021.09.15, 1:100; rubrica proprietar fără semnătură vizibilă.','Releveu, nu dovadă de plan vizat. Identic SHA-256 cu „1120 Wien, Schallergasse 35.pdf” din Bestandsplaene.'),
('Baubeschreibung D03, p.7','Nu există semnătură/ștampilă vizibilă pe pagina finală verificată.','Asumarea completă a fișierului nu este confirmată; solicitați exemplarul semnat.'),
('Bauphysik D04, pp.1,65,127','Siglă firmă; Energieausweis are rubrica Unterschrift goală; pagina finală datată fără semnătură vizibilă.','Sigla nu este semnătură. Solicitați documentul asumat și actualizat/confirmat.'),
('Statica preliminară 297 pagini, coperta','Nume/siglă Berger, fără semnătură vizibilă pe copertă.','Nu s-au verificat vizual toate anexele; semnarea întregului raport rămâne neconfirmată. Nu afirm absența tuturor semnăturilor.'),
('Vollmacht D07, o pagină','Semnătură olografă vizibilă, vechiul proprietar.','Semnată, dar mandat limitat la consultare; nepotrivită ca dovadă a mandatului actual de depunere.'),
('Online A.01 / IE01, câte o pagină','A.01: nume proiectant, fără semnătură vizibilă în cartuș; IE01: coloana Unterschrift goală.','Eșantionul verificat nu dovedește asumare pentru depunere. Restul planșelor online nu sunt certificate vizual individual.')],[140,195,180])
add('Controlul tehnic al câmpurilor /Sig din PDF-urile D01–D11 nu a găsit câmpuri de semnătură. Acest test nu validează și nu invalidează o semnătură scanată ori semnarea făcută în platforma de depunere. Au fost verificate hash-urile celor 12 surse principale: neschimbate față de index.')
page('4. Termene și documente pentru etapa următoare')
add('Pentru autorizația §70: termenul de începere este, în principiu, patru ani de la rămânerea definitivă; termenul de finalizare, patru ani de la începere. Nu calculați automat termenul de la data tipărită 2023.04.21. Planwechsel nu prelungește prin el însuși valabilitatea autorizației. [L3,L7]')
add('În arhivă există solicitarea trimisă MA37 la 2026.09.22 privind proprietarul/valabilitatea și răspunsul din 2026.09.25 cu document de taxă pentru consultare. Acestea nu reprezintă confirmarea datei Rechtskraft. Referințe Eva-Mail: 05fba18c-d593-40d6-a310-4d076253fab6 și ad4b69d0-b596-42c5-aead-5e5d7cfddcbc.')
table(['Moment','Documente / acțiuni'],[
('Înainte de depunere','Clarificarea procedurii, recuperarea setului oficial și completarea matricei de la pp.2–3. Numerotați reviziile identic în arhitectură, statică, bau fizică și instalații.'),
('Înainte de începerea lucrărilor','Conform Bescheid: Bauführer și Prüfingenieur, nominalizări și confirmări; notificarea începerii cu termenul prevăzut în decizie; verificarea conceptului de fundare/excavare și documentația de execuție. Modelele goale sau ofertele nu dovedesc nominalizarea.'),
('În șantier','Planuri aprobate și calcule de execuție, verificări și procese-verbale conform condițiilor autorizației. BauKG/SiGe și coordonarea securității trebuie tratate în etapa aplicabilă, nu confundate cu anexele universale ale cererii.'),
('La finalizare','Fertigstellungsanzeige, confirmările și planurile conforme execuției cerute în Bescheid; documente lift/instalații și, după caz, Bauwerksbuch. P17 gol astăzi nu este, singur, un motiv de respingere a unei cereri inițiale.')],[115,400])
add('Lista de cerut PECH / proiectantului (germană)','Heading2')
for t in [
'1. Bitte übermitteln Sie den vollständigen, mit dem amtlichen Sichtvermerk versehenen Plansatz zum Bescheid MA37/1539234-2021-1 sowie den Nachweis der Rechtskraft und der Baubeginnfrist.',
'2. Bitte legen Sie fest, welche Änderungen als Planwechsel bzw. Bauanzeige einzureichen sind, insbesondere die neue Raumaufteilung und die Yoga-Nutzung im Keller.',
'3. Bitte erstellen Sie eine kurze Fehlunterlagenliste mit Verantwortlichem und Liefertermin: Einreichpläne, Baubeschreibung, Statik, Bauphysik/Energie, Brandschutz, Barrierefreiheit und sonstige erforderliche Nachweise.',
'4. Bitte bestätigen Sie für jede Einreichunterlage den Planstand, die Übereinstimmung mit den übrigen Fachplanungen und die erforderliche Unterfertigung.',
'5. Bitte korrigieren Sie die Bezeichnung des Bestandsplans in P2 und klären Sie die fehlenden bzw. abweichenden Unterlagen der Dokumentenmappe.']:add(t)
page('5. Servieta online: acoperire și diferențe')
add('Verificat prin autentificare și descărcarea ZIP-urilor oferite de interfață la 2026.10.27. P1–P17 accesibile; P18–P20 blocate. Nu au fost încărcate, șterse sau redenumite documente pe site. Verificarea privește vizibilitatea contului PECH, nu inventarul administrativ al serverului.')
labels=['Societate și proprietate','Autorizație / P2041','Arhivă autorizare','Teren / structură','Arhitectură execuție','Încălzire, gaz, ventilație','Apă / canalizare','Mansardă','Electric / curenți slabi','Lift','Releveu / fotografii','Licitație GU','Statică / PI','BauKG','ÖBA','Șantier / procese-verbale','Finalizare / Bauwerksbuch']
rows=[]
for pg in d['stats']['pages']:
 n=int(pg['page'][1:]);fs=[x for x in d['files'] if x['page']==pg['page']];exact=sum(bool(x['local_matches']) for x in fs)
 rows.append((pg['page']+' • '+labels[n-1],len(fs),exact,len(fs)-exact,'GOL' if not fs else 'Inventariat'))
table(['Secțiune','Fișiere','Identice','Diferite*','Situație'],rows,[260,50,55,55,95],True)
add('* „Diferite” = fără identitate SHA-256 cu fișierele locale comparate, inclusiv verificarea a două arhive RAR de planuri/cantități. Poate fi traducere, export sau revizie; nu înseamnă automat document absent local ori conținut greșit. Cele 184 de intrări reprezintă 183 de conținuturi distincte (un duplicat).')
add('Nucleu local 00.Proiect, fără 09. Vertraege și fără .md: 110 fișiere / 109 conținuturi unice; 90 conținuturi nu apar identic în servieta accesibilă. Acest nucleu conține și variante, modele și calcule de cost, nu numai anexe obligatorii. Lista concretă este în anexa B. Cele 66 versiuni online neidentice sunt marcate în anexa A.')
add('Exemple importante nepreluate identic: inventarul 2026.07.09; procura de consultare; modelele MA37; planuri locale RO/M.v.3; fișiere DWG/DXF de execuție; documente utilități; liste de cantități și devize MIN/MAX. Aceste diferențe trebuie selectate și reconciliate; nu recomand publicarea automată a corespondenței private, actelor de proprietate sau tuturor versiunilor istorice.')
page('6. Surse și limite exacte ale controlului')
add('Metodă: indexul local și cache-urile de text existente; verificarea metadatelor pentru inventarul comparat; SHA-256 al surselor principale și fișierelor descărcate; verificări vizuale punctuale menționate în tabel. Nu s-a reverificat tehnic fiecare cotă, calcul, semnătură sau pagină din arhivă. Nu s-a accesat dosarul intern MA37.')
add('Inventarul comparativ larg are 5.317 fișiere candidate, inclusiv corespondență, istoric, materiale administrative și posibile documente auxiliare ale altor proiecte. Nu îl folosesc pentru a afirma că lipsesc mii de acte obligatorii. Compararea exactă și listele pot fi reproduse din auditul salvat în folder map/2026.10.27 QA autorizare.')
add('PDF-ul include ca atașamente: inventarul online (184 intrări), comparația locală largă și sursele principale cu hash. Într-un cititor PDF care acceptă atașamente, deschideți panoul Attachments. Anexele vizibile de mai jos permit citirea inventarului online și a diferențelor nucleului fără alte fișiere.')
sources=[('L1','MA37 – Documente necesare','https://www.wien.gv.at/wohnen/baugenehmigung-dokumente-einreichung'),('L2','BO Wien §63 – Anexe și condiții','https://ris.bka.gv.at/NormDokument.wxe?Abfrage=LrW&Anlage=&Artikel=&Gesetzesnummer=20000006&Paragraf=63&Uebergangsrecht='),('L3','BO Wien §73 – Modificări','https://ris.bka.gv.at/NormDokument.wxe?Abfrage=LrW&Anlage=&Artikel=&Gesetzesnummer=20000006&Paragraf=73&Uebergangsrecht='),('L4','BO Wien §64 – Planuri','https://ris.bka.gv.at/NormDokument.wxe?Abfrage=LrW&Anlage=&Artikel=&Gesetzesnummer=20000006&Paragraf=64&Uebergangsrecht='),('L5','BO Wien §65 – Semnarea de către autor, forma actuală','https://ris.bka.gv.at/eli/lgbl/WI/1930/11/P65/LWI40014415'),('L6','Stadt Wien – Procedura generală','https://www.wien.gv.at/amtswege/allgemeine-baubewilligung-bauten-bauliche-anlagen'),('L7','BO Wien §74 – Valabilitate','https://ris.bka.gv.at/NormDokument.wxe?Abfrage=LrW&Anlage=&Artikel=&Gesetzesnummer=20000006&Paragraf=74&Uebergangsrecht=')]
for code,label,url in sources:story.append(Paragraph(f'{code} • <link href="{escape(url)}" color="#12628a">{escape(label)}</link>',styles['Normal']));story.append(Spacer(1,6))
add('Surse oficiale consultate la 2026.10.27. Pentru §63 s-a consultat forma intrată în vigoare la 2026.07.15. Aplicarea dispozițiilor tranzitorii la proiectul deja autorizat trebuie stabilită pentru intervenția exactă, nu dedusă numai din data raportului.')
add('Repere locale','Heading2')
for k in ['D01','D02','D03','D04','D06','D07','D12']:add(k+' • '+m[k]['cale'],'Small')
add('Statica completă: 00.Proiect/09. Vertraege/neid.co.at/2026.08.11/04_Einreichstatik_2021-2022/Statische_Vorbemessung_2021_inkl_Mauerwerksgutachten.pdf','Small')
page('Anexa A • Toate fișierele online accesibile')
add('= identic SHA-256 cu cel puțin un fișier local. ≠ fără corespondent identic; versiune de reconciliat. Calea locală completă și hash-ul sunt în atașamentul inventarului. Numele terților sunt păstrate.')
for pg in d['stats']['pages']:
 fs=[x for x in d['files'] if x['page']==pg['page']]
 if not fs:continue
 add(pg['page']+' • '+labels[int(pg['page'][1:])-1],'Heading2')
 table(['Fișier online','SHA'],[(x['name'],'=' if x['local_matches'] else '≠') for x in fs],[480,35],True)
page('Anexa B • Fișiere locale fără copie identică online')
add('Domeniu precis: 00.Proiect, exclus 09. Vertraege și fișiere .md. Lista nu afirmă lipsa conținutului în traduceri/exporturi și nu este o listă de acte obligatorii. P18–P20 nu au fost accesibile. Duplicatele locale sunt păstrate pentru trasabilitate.')
table(['Cale locală relativă la 00.Proiect'],[(x['cale'][11:],) for x in missing],[515],True)
def footer(c,doc):
 c.setFont('Arial',8);c.setFillColor(colors.HexColor('#587080'));c.drawString(40,24,'2026.10.27 • Schallergasse 35 • Audit documentar');c.drawRightString(555,24,str(doc.page))
tmp=Q/'2026.10.27 Raport fara atasamente.pdf';SimpleDocTemplate(str(tmp),pagesize=(595,842),leftMargin=40,rightMargin=40,topMargin=35,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
w=PdfWriter();w.clone_document_from_reader(PdfReader(tmp))
for name,obj in [('2026.10.27 Comparatie integrala.json',d),('2026.10.27 Surse principale.json',m)]:w.add_attachment(name,json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8'))
s=io.StringIO();cw=csv.writer(s);cw.writerow(['Pagina','Fisier online','SHA256','Cai locale identice'])
for x in d['files']:cw.writerow([x['page'],x['name'],x['sha256'],' | '.join(x['local_matches'])])
w.add_attachment('2026.10.27 Inventar online.csv',s.getvalue().encode('utf-8-sig'))
final=O/'2026.10.27 Schallergasse 35 - Audit acte MA37 si servieta.pdf';w.write(final)
pdf=pdfium.PdfDocument(final);renders=Q/'2026.10.27 Raport randat';renders.mkdir(exist_ok=True)
for i in range(len(pdf)):pdf[i].render(scale=1).to_pil().save(renders/f'{i+1:02}.png')
print(str(final));print('PAGES',len(pdf));print('ATTACHMENTS',list(PdfReader(final).attachments))
