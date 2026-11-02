from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pypdf import PdfReader,PdfWriter
import json,shutil
root=Path(r'Z:\00.Roboti\AGV-Jining.Aowei');out=root/'3.Documente furnizor si import';out.mkdir(exist_ok=True)
work=Path(r'C:\Users\User\.codex\visualizations\2026\10\22\01a16433-6d2f-7bf2-93f1-ca88c3efba44')
def new(title):
 d=Document()
 for b in list(d.styles.element.iter(qn('w:pBdr'))):b.getparent().remove(b)
 s=d.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7);s.top_margin=s.bottom_margin=Cm(1.7);s.left_margin=s.right_margin=Cm(1.9)
 for n in ['Normal','Title','Heading 1','Heading 2']:
  d.styles[n].font.name='Calibri';d.styles[n].font.color.rgb=RGBColor(0,0,0)
 d.styles['Normal'].font.size=Pt(10.5);d.styles['Normal'].paragraph_format.space_after=Pt(6)
 d.styles['Title'].font.size=Pt(22);d.styles['Heading 1'].font.size=Pt(14)
 d.add_paragraph(title,'Title');return d
def p(d,t):d.add_paragraph(t)
def h(d,t):d.add_paragraph(t,'Heading 1')
def entry(d,t,v):
 q=d.add_paragraph();q.add_run(t+' ').bold=True;q.add_run(v)
def page(d,t):d.add_page_break();d.add_paragraph(t,'Title')
def table(d,heads,rows,widths):
 t=d.add_table(rows=1,cols=len(heads));t.autofit=False
 for c,w in zip(t.columns,widths):c.width=Cm(w)
 for c,v in zip(t.rows[0].cells,heads):
  c.text=v
  sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E8EDF2');c._tc.get_or_add_tcPr().append(sh)
  for run in c.paragraphs[0].runs:run.bold=True
 rep=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(rep)
 for vals in rows:
  for c,v in zip(t.add_row().cells,vals):c.text=v
 for row in t.rows:
  for c,w in zip(row.cells,widths):
   c.width=Cm(w);b=OxmlElement('w:tcBorders')
   for e in ['top','bottom','left','right']:
    x=OxmlElement('w:'+e);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'D9D9D9');b.append(x)
   c._tc.get_or_add_tcPr().append(b)
   for q in c.paragraphs:q.paragraph_format.space_after=Pt(4);q.paragraph_format.space_before=Pt(4)
 return t
def sign(d):p(d,'Authorised name: ____________________   Position: ____________________\nPlace and date: _____________________   Signature: ___________________')

d=new('Commercial invoice')
p(d,'Invoice number: ____________________    Issue date: ____________________\nOrder reference: 261001102RO    Currency: EUR')
p(d,'Seller: Jining Aowei Machine Co., Limited\nRegistered address: __________________________________________________\nRegistration number: __________________   Email: angela@aoweimachine.com')
p(d,'Buyer legal name: ___________________________________________________\nVAT/tax number: __________________   Registered address: __________________\n____________________________________________________________________\nDelivery address: ____________________________________________________\nContact: _________________________   Telephone: ________________________')
p(d,'Importer of record: ______________________________   EORI: ______________\nCountry of origin: ____________   Country of dispatch: ____________')
table(d,['Description','Qty','Unit EUR','Total EUR'],[
('Remote-controlled electric tracked chassis platform\nModel: __________   Serial: __________\nSupplied configuration: technical annex __________','1','2,500.00','2,500.00'),
('Freight and agreed delivery charges','','','1,370.00'),('Discount','','','-70.00'),('Invoice total','','','3,800.00')],[10.3,1.2,2.7,3])
p(d,'HS/CN code: __________________   EU TARIC code: __________________\nDelivery term: DDP _________________________________ Incoterms 2020\nPayment terms: __________________   Payment status/reference: ______________\nNumber of packages: ______   Net weight: ______ kg   Gross weight: ______ kg')
p(d,'Bank beneficiary: _____________________   Bank: _________________________\nIBAN/account: ________________________   SWIFT/BIC: ____________________')
p(d,'Seller confirms that the description, quantities, values and origin stated above correspond to the goods supplied.')
sign(d)

page(d,'Packing list')
p(d,'Packing list number: __________________    Date: __________________\nCommercial invoice number: __________________   Order: 261001102RO')
p(d,'Seller: Jining Aowei Machine Co., Limited\nConsignee: __________________________________________________________\nDelivery address: ____________________________________________________\nShipping marks: _____________________________________________________')
table(d,['Package','Contents and identification','Qty','Net kg'],[
('1','Tracked chassis model __________ serial __________','1','______'),
('1','Battery manufacturer/model __________________\nInstalled in chassis / separately packed: __________','____','______'),
('1','Charger manufacturer/model __________________\nInput 220–240 V AC, 50 Hz','1','______'),
('1','Remote controller and receiver __________________','____','______'),
('1','Cables, connectors and accessories ______________','____','______'),
('1','Manuals and documents ________________________','____','______')],[1.5,10,2,3.7])
p(d,'Total packages: ______   Total net weight: ______ kg   Total gross weight: ______ kg\nPackage dimensions L × W × H: __________ × __________ × __________ cm\nPackaging material: __________________________________________________\nSolid wood treatment/ISPM 15 mark reference, where applicable: _______________\n____________________________________________________________________')
p(d,'Battery arrangement and securing: ______________________________________\nTransport booking/reference: __________________________________________\nPhotograph references for packed goods and marks: _________________________')
p(d,'We confirm that the contents and weights stated above correspond to the packed shipment.')
sign(d)

page(d,'Technical specification')
p(d,'Manufacturer: Jining Aowei Machine Co., Limited\nOrder: 261001102RO   Specification reference: ____________________________\nModel: __________________   Revision: ______   Serial: _____________________\nYear of manufacture: ______   Intended function: ___________________________')
table(d,['Parameter','Confirmed specification'],[
('Rated payload and operating conditions','________ kg; terrain/slope/load distribution __________________'),
('Dimensions and unladen mass','L ______ mm × W ______ mm × H ______ mm; mass ______ kg'),
('Speed and slope','Rated-load speed ______ km/h; maximum permitted slope ______'),
('Motors and controllers','Number ______; rated power per motor ______ W; voltage ______ V\nMotor model ______; controller model ______'),
('Control mode','Remote control __________________; other included functions __________________'),
('Stopping and protection','Emergency stop ______; braking ______; loss-of-signal response ______\nMaximum speed setting ______; protective devices ______'),
('Environment','Indoor/outdoor ______; IP rating ______; temperature limits ______'),
('Communication','Physical interface ______; protocol ______; connector/pinout document ______'),
('SDK and documentation','Repository/access URL __________________; version ______\nExamples ______; licence ______; supported commands ______'),
('Warranty and support','Period/start date ______; battery coverage ______; service contact ______\nReplacement/return freight responsibility __________________')],[4.8,12.4])
p(d,'Included equipment and accessories: ____________________________________\n____________________________________________________________________\nOperation and maintenance manual reference: ______________________________\nSafety instructions in Romanian reference: _________________________________')
sign(d)

page(d,'Battery and charger specification')
p(d,'Chassis model/serial: __________________   Specification reference: __________')
table(d,['Battery parameter','Confirmed value'],[
('Manufacturer and model','Manufacturer __________________; model __________________'),
('Chemistry and construction','Chemistry __________________; construction __________________'),
('Battery assembly','Quantity ______; individual voltage ______ V; series/parallel arrangement ______'),
('Pack capacity','Nominal voltage ______ V; capacity ______ Ah at ______ hour rate; energy ______ Wh'),
('Charging limits','Maximum permitted current ______ A; charging voltage/profile ______\nTemperature compensation ______; charging temperature range ______'),
('Safety and conformity documents','Datasheet ______; EU declaration ______; safety information ______'),
('Transport configuration','Installed/separate ______; classification/reference ______\nExemption evidence, if applicable __________________')],[4.8,12.4])
table(d,['Charger parameter','Supplied configuration and performance'],[
('Manufacturer and model','____________________________________________'),
('AC input','220–240 V AC, 50 Hz; Romanian socket-compatible mains lead'),
('DC output','Nominal battery system ______ V; charging voltage range ______ V\nContinuous output current ______ A; continuous output power ______ W'),
('Charging profile','Automatic profile approved for the supplied battery model: __________________'),
('Compatibility and protection','Connector/polarity ______; overcharge/overcurrent/short-circuit/thermal protection ______'),
('Recharge performance','Maximum 8 hours from 20% to 100% state of charge\nAmbient 20–25°C; chassis switched off; completion criterion __________________'),
('Verification','Test date ______; result ______; battery manufacturer approval/reference ______'),
('Documents','EU declaration ______; charger manual ______; rating-label photograph ______')],[4.8,12.4])
p(d,'We confirm that the supplied charger is compatible with the actual battery assembly and its permitted charging limits and provides the charging performance stated above.')
sign(d)

page(d,'EC declaration of conformity')
p(d,'Declaration number: ____________________')
p(d,'Manufacturer: Jining Aowei Machine Co., Limited\nFull registered address: ______________________________________________\n____________________________________________________________________')
p(d,'Person established in the European Union authorised to compile the technical file\nName: ______________________________________________________________\nFull address: ________________________________________________________')
p(d,'Description and identification of machinery\nProduct: Remote-controlled electric tracked chassis platform\nFunction: ___________________________________________________________\nModel/type: __________________   Commercial name: _______________________\nSerial number: __________________   Year of manufacture: _________________')
p(d,'We declare that the machinery identified above fulfils all relevant provisions of Directive 2006/42/EC.')
p(d,'Other applicable Union legislation: _______________________________________\n____________________________________________________________________\n____________________________________________________________________')
p(d,'Harmonised standards applied, including dated references: ____________________\n____________________________________________________________________\n____________________________________________________________________\nOther technical standards/specifications applied: ____________________________\n____________________________________________________________________')
p(d,'Notified body and certificate details, where applicable: _______________________\n____________________________________________________________________')
p(d,'Signed for and on behalf of: Jining Aowei Machine Co., Limited')
sign(d)

page(d,'Shipment documentation record')
p(d,'Seller: Jining Aowei Machine Co., Limited\nInvoice: __________________   Shipment reference: __________________\nModel: __________________   Serial: __________________')
table(d,['Document','Number or version','Issuer','Supplied'],[
('Commercial invoice','____________','Seller','______'),('Packing list','____________','Seller','______'),
('Machinery declaration applicable to supplied product','____________','Manufacturer','______'),
('Operating and safety instructions in Romanian','____________','Manufacturer / translator','______'),
('Battery EU declaration and safety information','____________','Battery manufacturer','______'),
('Charger EU declaration and instructions','____________','Charger manufacturer','______'),
('Radio equipment EU declaration and instructions','____________','Radio manufacturer','______'),
('Battery transport classification and supporting evidence','____________','Responsible issuer','______'),
('Transport document / booking details','____________','Carrier / forwarder','______'),
('Other applicable shipment documents','____________','____________','______')],[7.1,3.2,4.3,2.6])
p(d,'Importer of record and customs representative: ______________________________\n____________________________________________________________________\nShipping marks and nameplate photograph references: _________________________\n____________________________________________________________________')
p(d,'The completed references above identify the documents supplied with or transmitted for this shipment.')
sign(d)
d.save(out/'01_Formulare_furnizor_DE_COMPLETAT_EN.docx')

r=new('Controlul documentelor de import din China')
p(r,'22 octombrie 2026 | Document intern pentru cumpărător și comisionarul vamal. Nu se semnează de furnizor ca declarație de produs și nu se atașează automat coletului.')
p(r,'Concluzie: există documente suficiente pentru a pregăti formularele și solicitările, dar nu pentru a valida un dosar final de import. Lipsesc cumpărătorul juridic, importatorul, modelul/configurația confirmate, greutățile, datele exacte ale bateriei/încărcătorului și încadrarea TARIC verificată pentru expediere.')
h(r,'Documentele de bază și responsabilitatea emiterii')
table(r,['Document sau verificare','Emitent și moment','Stadiu'],[
('Factură comercială cu cumpărător, vânzător, descriere exactă, model, cantitate, valoare, monedă, origine, condiții de livrare','Vânzător; înainte de vămuire','Formular pregătit; date de completat'),
('Packing list cu număr colete, conținut, serie, greutăți nete/brute, dimensiuni și ambalaj','Vânzător; înainte de expediere','Formular pregătit; măsurători lipsă'),
('Conosament / sea waybill și documente de transport pentru segmentele relevante','Transportator/expeditor','De emis la transport'),
('EORI, mandat reprezentare, cod TARIC, valoare în vamă, origine și măsuri aplicabile','Importator/comisionar','Identitatea importatorului și încadrarea de confirmat'),
('ENS/ICS2 și datele de securitate înainte de intrarea în UE','Transportator și actorii responsabili de depunere','Se confirmă cu expeditorul; nu este formular de semnat în locul transportatorului'),
('Declarație vamală, MRN, liber de vamă și documente privind taxele/TVA','Declarant/vamă; la import','Nu pot fi emise anticipat de cumpărător'),
('Documente de conformitate și instrucțiuni pentru utilaj, baterie, încărcător și radio','Producătorul responsabil','Se obțin pentru modelele efective'),
('Dovada plății și documentele de recepție/înregistrare','Bancă/cumpărător','Se arhivează când sunt disponibile')],[7.2,5,5])
p(r,'DDP nu stabilește singur cine figurează ca importator în documentele vamale. Se confirmă în scris entitatea, EORI, reprezentarea, țara de vămuire și documentele fiscale pe care le primește cumpărătorul.')

page(r,'Condiții specifice și documente care nu se cer automat')
entry(r,'Utilajul','Dacă este mașină completă, sunt necesare declarația aplicabilă, marcajele și instrucțiunile corespunzătoare. Formularul CE pregătit este pentru regimul Directivei 2006/42/CE și numai pentru o mașină completă. Dacă este cvasimașină sau intrarea pe piață are loc sub alt regim, se înlocuiește cu documentul corect înainte de semnare. Nu se semnează ambele variante ca și cum ar fi echivalente.')
entry(r,'Încărcătorul și telecomanda','Se cer declarațiile UE și instrucțiunile producătorilor lor, identificând modelele livrate; producătorul stabilește legislația efectiv aplicabilă. Un certificat generic al șasiului nu acoperă automat încărcătorul sau radio-ul. Pentru 220–240 V, compatibilitatea și siguranța încărcătorului trebuie documentate.')
entry(r,'Bateria','Se cer documentația de conformitate UE și trasabilitatea, fișa exactă, siguranța și încadrarea transportului. Bateria industrială și bateria portabilă nu au automat aceleași obligații/termene. Dacă ansamblul depășește 2 kWh, se verifică și cerințele specifice categoriei și datei aplicabile, inclusiv informațiile de performanță/durabilitate. Nu se presupune că fotografia unei cutii constituie documentație UE.')
entry(r,'Transportul bateriilor','Furnizorul și expeditorul confirmă chimia, starea, instalarea/separarea, încadrarea exactă, ambalarea și eventuala exceptare. Se obțin declarația de mărfuri periculoase și documentele suport când sunt cerute. Nu se atribuie UN2800 întregului vehicul fără analiză. UN 38.3 este relevant pentru litiu, nu automat pentru plumb. SDS nu înlocuiește testele sau declarația UE.')
entry(r,'Ambalajul din lemn','Pentru lemn masiv se verifică tratamentul și marcajul ISPM 15/IPPC, inclusiv paleții și materialele de fixare. Lemnul complet prelucrat, precum placajul, poate fi exceptat. Nu se cere automat un certificat de fumigare dacă cerința este satisfăcută prin tratament/marcaj corespunzător sau ambalaj exceptat.')
entry(r,'Originea','Originea se declară corect. Certificatul de origine nepreferențial se obține dacă îl cere măsura aplicabilă, vama sau contractul. China nu beneficiază de un aranjament preferențial general al UE; nu se presupune reducere de taxă doar pentru că există un certificat de origine.')
entry(r,'Alte obligații','Comisionarul verifică măsurile TARIC, eventuale restricții sau controale, în funcție de cod și produs. În România se verifică separat rolul și obligațiile de mediu pentru baterii, echipamente electrice și ambalaje. Un certificat ISO 9001, o declarație generică de produs nou sau un certificat CE comercial nu substituie documentele obligatorii și nu se cer automat ca documente vamale universale.')
entry(r,'Manual și dosar tehnic','Manualul și informațiile de siguranță trebuie asigurate pentru utilizarea în România. Dosarul tehnic trebuie să existe și să fie disponibil autorităților în condițiile legale; nu se pretinde automat predarea integrală a tuturor desenelor proprietare cumpărătorului.')

page(r,'Încadrare vamală și reducerea legală a costurilor')
p(r,'Cotele de mai jos sunt cote convenționale din Nomenclatura combinată UE 2026, Regulamentul de punere în aplicare (UE) 2025/1926. Nu reprezintă o confirmare TARIC completă la data importului; accesul direct la interogarea TARIC a fost refuzat de serviciul web. Nu au fost validate suspendări, contingente sau măsuri suplimentare pentru expedierea concretă.')
table(r,['Poziție de analizat','Cotă de bază','Când poate fi aplicabilă'],[
('8709 11 90','4%','Vehicul electric de transport intern, fără dispozitiv de ridicare/manipulare, de tipul folosit pe distanțe scurte în fabrici/depozite etc. Candidat de verificat pentru platforma completă.'),
('8479 50 00','1,7%','Robot industrial nespecificat în altă parte. Denumirea RC Robot și folosirea într-un laborator nu demonstrează această încadrare.'),
('8504 40 60','0%','Încărcător de acumulatori, dacă tratamentul vamal al prezentării sale justifică încadrarea separată. Nu se separă artificial un ansamblu doar pentru taxă.')],[3.2,2,12])
p(r,'Încadrarea depinde de caracteristicile obiective la import, funcția reală, configurația completă/incompletă și regulile generale de interpretare. Un viitor braț robotic montat după import nu transformă automat șasiul importat într-un robot industrial. Pentru un șasiu sau o parte se analizează separat poziția corectă; nu s-a stabilit aici un cod de parte prin presupunere.')
p(r,'Economia legală se verifică prin: aplicarea codului corect și a oricărei suspendări/scutiri efectiv eligibile; documentarea costurilor DDP și a sumelor care pot fi excluse legal din valoarea în vamă; evitarea dublării transportului sau a taxelor deja incluse; evidențierea autentică a articolelor distincte, dacă regulile de clasificare o permit. Nu se modifică descrierea, valoarea sau originea ca să se obțină o cotă mai mică.')
p(r,'Exemplu de comparație, nu calcul de plată: la o valoare în vamă ipotetică de 3.000 EUR, 4% înseamnă 120 EUR, iar 1,7% înseamnă 51 EUR. Diferența de 69 EUR nu justifică un cod necorespunzător. TVA și alte costuri nu sunt incluse. Totalul DDP de 3.800 EUR nu este automat valoarea în vamă.')
p(r,'Comisionarul primește: fișa finală, poze, funcția principală, sarcina utilă, masa, viteza, propulsia, dispozitivele montate, utilizarea, schema configurației și factura. Se cere confirmarea codului de 10 cifre, cotei și măsurilor pentru China la data declarării. Dacă persistă incertitudinea, se poate solicita ITO/BTI; opinia furnizorului nu echivalează cu decizia vamală.')

page(r,'Dimensionarea încărcătorului și sursele verificării')
p(r,'Cerința de intrare este 220–240 V AC, 50 Hz, cu cablu și fișă compatibile cu prizele din România. Un încărcător exclusiv de 110 V nu îndeplinește cerința. Trebuie confirmate puterea DC continuă, curentul, tensiunea/profilul, protecțiile, conectorul/polaritatea și timpul garantat pentru bateria livrată.')
p(r,'Puterea necesară nu poate fi fixată corect doar din inscripția 48 V. Dacă se confirmă 4 baterii de 12 V/85 Ah în serie, ansamblul are 48 V/85 Ah, aproximativ 4,08 kWh nominal la rata de capacitate declarată; nu 340 Ah. Tensiunea efectivă de încărcare și curentul maxim trebuie să vină din fișa KIJO pentru modelul real.')
p(r,'Calcul orientativ pentru verificare, nu specificație aprobată: un curent de 15 A la 57,6 V ar însemna circa 864 W DC. Alimentarea de la rețea trebuie să acopere și pierderile. Valorile 15 A și 57,6 V nu au fost înscrise drept caracteristici garantate; pot fi nepotrivite fără confirmarea producătorului bateriei. Pentru 85 Ah, refacerea a 80% din capacitate în faza de curent constant ar necesita ideal 4,5 ore la 15 A sau 6,8 ore la 10 A, la care se adaugă fazele finale și pierderile.')
p(r,'Ca țintă comercială propusă pentru o încărcare peste noapte, formularul cere maximum 8 ore de la 20% la 100% SOC, la 20–25°C, cu șasiul oprit și criteriul de terminare precizat. Aceasta este o cerință de achiziție de confirmat prin test de furnizor, nu o performanță deja constatată. Nu se aprobă un curent mai mare decât permite bateria pentru reducerea duratei. Instrucțiunea generală KIJO nu este fișa modelului 6-GFM-85 și nu a fost folosită pentru a fixa limitele acestuia.')
h(r,'Surse oficiale și primare')
sources=[
('Nomenclatura 2026, paginile 611, 623 și 664','https://www.stat.si/StatWeb/File/DocSysFile/14592/Commission%20implementing%20Regulation%201926_2025.pdf'),
('Încadrare și ITO în România','https://www.customs.ro/e-customs/ITOE3---Informatii-tarifare-obligatorii/instructiuni-de-completare-cereri'),
('Aranjamente tarifare pentru țările terțe','https://taxation-customs.ec.europa.eu/list-non-eu-countries_en'),
('ISPM 15 și ambalaje exceptate','https://food.ec.europa.eu/plants/plant-health-and-biosecurity/trade-plants-plant-products-non-eu-countries/requirements-wood-packaging-dunnage_en'),
('ICS2','https://taxation-customs.ec.europa.eu/customs/customs-security/import-control-system-2_en'),
('Regulamentul privind bateriile','https://eur-lex.europa.eu/eli/reg/2023/1542/2025-07-31/eng/pdf'),
('Directiva privind mașinile','https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006L0042:EN:PDF'),
('Instrucțiuni generale KIJO','https://www.kijo-battery.com/precautions-for-using-kijo-storage-battery.html')]
for label,url in sources:
 q=r.add_paragraph(label+' — '+url);q.paragraph_format.space_after=Pt(4)
 for run in q.runs:run.font.size=Pt(8)
r.save(out/'02_Control_import_incadrare_vamala_si_incarcator_RO.docx')

readme='''DOCUMENTE PENTRU FURNIZOR SI IMPORT - 22.10.2026

01_Formulare_furnizor_DE_COMPLETAT_EN.docx: formulare curate in engleza pentru factura comerciala, packing list, specificatie tehnica, baterie/incarcator, declaratie CE pentru masina completa si registrul documentelor expedierii. Fara comentarii de analiza in paginile de semnat.

NU ESTE INCA UN DOSAR FINAL DE COLET. Furnizorul completeaza datele reale si semneaza numai documentele pe care este autorizat sa le emita. Nu se semneaza campuri goale. Preturile precompletate provin din oferta originala si se reconfirma la emiterea facturii. Codul vamal nu este precompletat.

Declaratia CE pregatita se utilizeaza numai daca produsul este masina completa sub Directiva 2006/42/CE. Daca este cvasimasina sau se aplica alt regim la introducerea pe piata, producatorul emite declaratia corecta. Declaratiile UE pentru baterie, incarcator si radio trebuie obtinute de la producatorii responsabili; nu au fost fabricate in locul lor.

02_Control_import_incadrare_vamala_si_incarcator_RO: analiza interna, nu se anexeaza automat coletului.
03_Explicatia_modificarilor_RO: explicatie separata, nu document vamal.
04_Dosar_revizuire_furnizor_cu_originale.pdf: formulare plus documentele originale, pentru schimbul cu furnizorul. Certificatele originale cu probleme sunt referinte, NU sunt validate pentru colet.

In colet se anexeaza versiunile FINALE aplicabile, completate si semnate, manualul si documentele specifice produsului. Nu se includ raportul intern, proiectele depasite sau certificatele necorelate cu unitatea.

Incarcator: intrare 220-240 V AC, 50 Hz. Curentul, puterea continua, tensiunea/profilul si timpul de incarcare trebuie confirmate pentru bateria reala. Nu s-a inventat o putere garantata.

Lipsesc de confirmat: societatea cumparatoare/CUI/adrese, importator/EORI, utilizarea principala, model/serie, sarcina utila, configuratia bateriei, charger, greutati, dimensiuni colet, documentele producatorilor si TARIC la data importului.
'''
(out/'00_INSTRUCTIUNI_PENTRU_FINALIZARE.txt').write_text(readme,encoding='utf-8')
# Preserve an excerpt of the actual 2026 tariff for internal review.
w=PdfWriter();cn=PdfReader(str(work/'CN2026.pdf'))
for i in [610,622,663]:w.add_page(cn.pages[i])
with (out/'Referinta_CN2026_p611_p623_p664.pdf').open('wb') as f:w.write(f)
# Record the completed bounded network scan precisely.
rs=[json.loads(x) for x in (work/'scan_shallow.jsonl').read_text(encoding='utf-8').splitlines()]
review=root/'2.Verificare achizitie 2026-10-22'
with (review/'00_Citeste_ma.txt').open('a',encoding='utf-8') as f:
 f.write('\nACTUALIZARE CAUTARE: scanare pe 84 de directoare de la radacina Z:, 670879 intrari enumerate, pana la 5 niveluri sub fiecare director. 16577 directoare mai adanci nu au fost parcurse de aceasta scanare; 0 erori raportate. Scanarile recursive fara limita au fost oprite deoarece nu s-au incheiat. Cautarea nu este exhaustiva in continut/arhive. Documentele Aowei gasite se afla in dosarul cunoscut si in copiile create in aceasta sesiune. Au fost gasite si materiale AGV-AMR in Nvidia\\Documente.\n')
 f.write('\nVERSIUNEA PENTRU FORMULARE CURATE este in folderul vecin 3.Documente furnizor si import. PDF-ul 06 din acest folder ramane dosar de analiza/referinta, nu dosar final de colet.\n')
(review/'09_Jurnal_cautare_limitata.jsonl').write_text((work/'scan_shallow.jsonl').read_text(encoding='utf-8'),encoding='utf-8')
print(str(out),flush=True)
