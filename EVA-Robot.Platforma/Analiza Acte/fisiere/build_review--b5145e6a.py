from pathlib import Path
import shutil, json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

base=Path(r'Z:\00.Roboti\AGV-Jining.Aowei')
out=base/'2.Verificare achizitie 2026-10-22'
out.mkdir(exist_ok=True)
src=base/'100. Inbox'

def new(title,intro):
 d=Document(); s=d.sections[0]; s.page_height=Cm(29.7); s.page_width=Cm(21)
 for border in list(d.styles.element.iter(qn('w:pBdr'))): border.getparent().remove(border)
 s.top_margin=s.bottom_margin=Cm(1.8); s.left_margin=s.right_margin=Cm(2)
 for n in ['Normal','Title','Heading 1','Heading 2']:
  st=d.styles[n]; st.font.name='Calibri'; st.font.color.rgb=RGBColor(0,0,0)
 d.styles['Normal'].font.size=Pt(10.5); d.styles['Normal'].paragraph_format.space_after=Pt(6)
 d.styles['Normal'].paragraph_format.line_spacing=1.08
 d.styles['Title'].font.size=Pt(23); d.styles['Heading 1'].font.size=Pt(15); d.styles['Heading 2'].font.size=Pt(12)
 d.add_paragraph(title,'Title'); d.add_paragraph(intro)
 return d
def h(d,t): d.add_paragraph(t,'Heading 1')
def p(d,t): d.add_paragraph(t)
def item(d,title,text):
 q=d.add_paragraph(); q.add_run(title+' ').bold=True; q.add_run(text)
def page(d,title): d.add_page_break(); h(d,title)
def table(d,heads,rows,widths):
 t=d.add_table(rows=1, cols=len(heads)); t.autofit=False
 for c,w in zip(t.columns,widths): c.width=Cm(w)
 for c,v in zip(t.rows[0].cells,heads):
  c.text=v
  sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'E7EDF3'); c._tc.get_or_add_tcPr().append(sh)
  for r in c.paragraphs[0].runs:r.bold=True
 rep=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(rep)
 for vals in rows:
  for c,v in zip(t.add_row().cells,vals):c.text=v
 for row in t.rows:
  for c,w in zip(row.cells,widths):
   c.width=Cm(w); pr=c._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    x=OxmlElement('w:'+edge);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'D9D9D9');borders.append(x)
   pr.append(borders)
   for q in c.paragraphs:q.paragraph_format.space_after=Pt(5);q.paragraph_format.space_before=Pt(5)
 return t

d=new('Verificarea achiziției platformei Aowei','22 octombrie 2026 | Concluzie: dosarul identificat este incomplet și conține contradicții care trebuie clarificate înainte de plata integrală. Verificarea documentară nu confirmă autenticitatea certificatelor sau conformitatea fizică a utilajului.')
h(d,'Documente existente')
p(d,'Folderul original conține 16 fișiere: 1 PDF de două pagini, 11 imagini și 4 videoclipuri. Subfolderul 1.Achizitie AGV este gol. PDF-ul și imaginile au fost citite; videoclipurile au fost inventariate, fără validare tehnică a testelor filmate.')
table(d,['Sursă în 100. Inbox','Conținut și statut'],[
('PI261001RO (1).pdf','Factura nr. 261001102RO din 1 octombrie 2026 și fișa tehnică la pagina 2. Titlul este INVOICE; funcția de proformă sau factură finală trebuie confirmată.'),
('4440845121.png / 5030967443.png','Fișă tehnică, aceeași configurație generală de 200 kg.'),
('5033561657.png / 5040969889.png','Reproduceri ale facturii și anexei; nu reprezintă documente comerciale suplimentare.'),
('5066555651.png','Certificat ISO 9001 în chineză, cu termen înscris 5 martie 2025. Nu dovedește conformitatea CE a produsului.'),
('5066591032.png','Atestare SZUTEST MD-20-05-50 pentru alte coduri de model decât AWC-08.'),
('5071728143.png','Declarație CE pentru AWC-08, datată 2 iulie 2025, cu serie și VIN; legătura cu unitatea comandată nu este demonstrată.'),
('30786693131.jpg / 30786697085.jpg','Ambalaj KIJO 6-GFM-85, 85 Ah la 20 h și 72 Ah la 3 h, simbol Pb. Marca diferă de fișa tehnică.'),
('30788002505.jpg / 30788006047.jpg','Platformă și telecomandă. Nu dovedesc navigație autonomă sau existența SDK-ului.')],[6,11])
h(d,'Valoare și stadiu')
p(d,'2.500 EUR echipamentul + 1.370 EUR transportul - 70 EUR reducerea = 3.800 EUR. Calculul este corect. Oferta cere 100% înainte de expediere și indică 10 zile lucrătoare după primirea plății. Nu s-a identificat o dovadă de plată în dosarul original; aceasta nu dovedește că plata nu a fost efectuată.')

page(d,'Inadvertențe comerciale și tehnice')
issues=[
('01 Cumpărător incomplet','Factura este adresată doar Mr. Cosmin Covaciu, fără societate, cod fiscal și adrese. Se cere reemitere pe cumpărătorul real; societatea din alte oferte nu se preia automat.'),
('02 Model neidentificat','Factura descrie generic un șasiu pe șenile de 48 V. Se cere codul exact, revizia, anul fabricației și seria la expediere, identice cu eticheta și documentele de conformitate.'),
('03 Sarcină utilă contradictorie','Factura: 100 kg. Anexa: 200 kg. Se cere o singură valoare garantată, cu condițiile de teren, viteză și distribuție a sarcinii. Nu se presupune că 200 kg este valoarea corectă.'),
('04 Alimentarea încărcătorului','Anexa menționează 110 V la intrare. Se cere 230 V AC, 50 Hz sau intrare universală compatibilă, confirmată prin fișa și eticheta încărcătorului.'),
('05 Baterii necorelate','Fișa indică Chaowei și baterii de 12 V, fotografiile arată KIJO 6-GFM-85/Pb, factura indică sistem de 48 V. Patru baterii de 12 V în serie ar explica tensiunea, dar numărul și conexiunea nu sunt confirmate.'),
('06 Putere ambiguă','Fișa spune 0,75 kW și două motoare BLDC. Se cere puterea nominală a fiecărui motor, puterea totală și datele controlerelor.'),
('07 SDK absent','Textul Github location for Comunication SDK nu conține URL. Se cer link funcțional, protocol, conectori/pinout, exemple și confirmarea compatibilității cu controlerul livrat.'),
('08 Autonomie nedovedită','Documentele descriu Remote Control RC. Nu există dovadă că prețul include SLAM, LiDAR, evitare obstacole sau navigație autonomă. Dacă acestea sunt necesare, se cer expres în configurație.'),
('09 Livrare ambiguă','Se separă data pregătirii/expedierii de durata tranzitului maritim și data estimată a sosirii. Cele 10 zile nu sunt tratate automat ca termen door-to-door.'),
('10 DDP insuficient precizat','Se cer adresa exactă, versiunea Incoterms, importatorul înregistrat, reprezentantul vamal și documentele privind taxele/TVA. Formula all including nu stabilește singură circuitul documentelor fiscale.'),
('11 Date bancare amestecate','Factura indică Banking Circle S.A., Luxembourg, dar la final apare Bank of Jining. Furnizorul trebuie să reemită o singură instrucțiune bancară coerentă și verificabilă. Nu se deduce fraudă doar din această eroare.'),
('12 Garanție și acceptanță lipsă','Nu sunt precizate durata, excluderile, costul transportului pieselor, suportul, testele de recepție sau remediile pentru neconformitate. Se cer clauze scrise înainte de plată.')]
for a,b in issues:item(d,a,b)

page(d,'Conformitate și documente care trebuie reemise')
item(d,'13 Modele diferite în documentele CE','Declarația indică AWC-08; atestarea SZUTEST enumeră EAW06, WL108, 910, 916, 918, 920, 930. Factura nu permite legarea acestor documente de unitatea comandată. Se cere explicația trasabilității și documentația pentru modelul efectiv.')
item(d,'14 Declarație incompletă','Rubrica persoanei autorizate să compileze dosarul tehnic în UE este goală. Câmpul NAME din blocul de semnătură repetă firma; numele și funcția persoanei semnatare trebuie precizate lizibil. Seria RC20J4C12021 și VIN C21023932002R trebuie confirmate față de eticheta unității.')
item(d,'15 Domeniu tehnic de verificat','Documentele invocă standarde pentru utilaje de terasament/excavatoare. Aplicabilitatea la platforma livrată trebuie justificată de producător. Nu se adaugă sau elimină directive și standarde fără evaluarea configurației, inclusiv telecomanda radio și încărcătorul.')
item(d,'16 ISO expirat în copia primită','Termenul înscris în imagine este 5 martie 2025, anterior analizei. Se solicită versiunea actuală dacă furnizorul invocă certificarea. ISO 9001 nu este, prin el însuși, documentul de conformitate al utilajului.')
h(d,'Ce trebuie să emită producătorul')
p(d,'Pentru o mașină completă: declarația CE corespunzătoare, identificarea exactă, persoana stabilită în UE autorizată să compileze dosarul tehnic, numele/funcția semnatarului, locul și data, legislația și standardele efectiv aplicabile. Se solicită manualul și informațiile de siguranță în română, precum și fotografii lizibile ale etichetei produsului.')
p(d,'Dacă livrarea este o cvasimașină pentru integrare, producătorul trebuie să confirme această clasificare și să furnizeze documentele aferente, inclusiv declarația de încorporare și instrucțiunile de asamblare. Nu se înlocuiește această încadrare cu o declarație CE generică. Dosarul tehnic integral nu trebuie presupus obligatoriu de predat cumpărătorului, dar trebuie să existe și să fie disponibil autorităților potrivit regimului aplicabil.')
h(d,'Baterii și transport')
p(d,'Fotografiile indică plumb prin simbolul Pb; AGM/VRLA, GEL și caracterul non-spillable nu sunt confirmate. Se cer fișa modelului, chimia, numărul bateriilor, tensiunea/capacitatea ansamblului, informații de siguranță/SDS dacă sunt furnizate ori solicitate și documentele UE ale bateriei. Confirmarea transportatorului trebuie să privească exact expedierea propusă, cu baterii montate sau separate.')
p(d,'Bateriile cu plumb și cele cu litiu pot fi importate și transportate dacă îndeplinesc cerințele aplicabile. Pentru plumb etanș, eventualele exceptări de transport trebuie susținute prin dovezi. UN 38.3 nu se cere automat unei baterii cu plumb; pentru o alternativă Li-ion/LiFePO4 se cer dovezile relevante UN 38.3. Acceptarea la transport nu înlocuiește conformitatea pentru piața UE.')
p(d,'Temeiuri consultate: Directiva 2006/42/CE, anexele I și II; Regulamentul (UE) 2023/1542, art. 41. Pentru introducerea pe piață de la 20 ianuarie 2027 se verifică noul Regulament privind mașinile. Cerințele se stabilesc pentru produsul și data efectivă, nu exclusiv după data proformei.')

page(d,'Checklist de închidere și documente similare')
table(d,['Moment','Documente și acțiuni'],[
('Înainte de plată','Proformă reemisă pe cumpărătorul real; model și configurație confirmate; instrucțiuni bancare coerente; garanție și remedii; DDP și termen clar; SDK verificabil; plan/documente de conformitate și baterii.'),
('Înainte de expediere','Factură comercială finală; packing list cu greutăți și dimensiuni; serie și fotografii ale etichetelor; declarații aplicabile; manual; raport de test funcțional; acceptarea transportatorului pentru baterii; date privind ambalajul din lemn și tratamentul aplicabil.'),
('La transport și import','Conosament/sea waybill și documentul segmentului rutier, după caz; declarație vamală/MRN și circuit fiscal documentat potrivit importatorului real; EORI dacă societatea cumpărătoare este importator; cod tarifar stabilit după produs. Dovada originii și alte documente se cer când sunt aplicabile.'),
('La recepție','Dovada livrării; verificarea seriei și accesoriilor; testele convenite; documentul de recepție și înregistrările contabile aplicabile; dovada plății când există.')],[3.3,13.7])
h(d,'Referințe locale utile')
p(d,'În Z:\\00.Roboti există Import Requirements for the Unitree G1 Humanoid Robot.docx și Acquisition guide Unitree G1-EDU-U2.docx. Sunt liste de verificare pentru alt produs, nu dovezi de conformitate Aowei. Cerințele de litiu, codul tarifar propus și standardele nu trebuie copiate automat.')
p(d,'AGV+Cobot FoxTech\\Questions 2025.07.09.docx oferă o listă utilă de întrebări despre SDK, interfețe, siguranță și suport. AGV+2Cobot  Hoa Mai conține o ofertă și descrieri API. AGV RobInt conține fișe R100/R200.')
p(d,'AGV Reeman Robot conține manuale, SDK și protocoale. Oferta Greatway din 30 iulie 2024 precizează model, garanție de un an și condiții de plată/livrare. Oferta Avatar AVT-W9D din 3 aprilie 2026, în Humanoid AGV, include manual, suport și garanție; acestea sunt exemple de clauze, nu oferte actualizate sau dovada unei achiziții finalizate.')
h(d,'Limitele căutării')
p(d,'Z: corespunde \\\\192.168.100.169\\Comun, singura partajare listată de server. A fost verificat și Z:\\192.168.100.169\\Comun. Căutarea recursivă generală după denumiri a fost inițiată; stadiul și rezultatele finale sunt consemnate în 00_Citeste_ma.txt. Nu se afirmă că fiecare document, arhivă, e-mail sau imagine de pe server a fost căutat în conținut. Absența din dosarul verificat nu demonstrează inexistența în întreaga organizație.')
d.save(out/'01_Lista_inadvertente_si_checklist.docx')

d=new('Revised proforma invoice for supplier confirmation','DRAFT FOR REISSUE BY JINING AOWEI MACHINE CO LIMITED. Not a supplier-issued invoice and not a payment instruction. Based on invoice 261001102RO dated 1 October 2026. All bracketed fields require confirmation.')
h(d,'Seller and buyer')
p(d,'Seller: Jining Aowei Machine Co., Limited. Address shown in source: No. 129 Jianshe Road, Jining City, Shandong Province, China. Contact: angela@aoweimachine.com. Seller registration number and legal address: [CONFIRM].')
p(d,'Buyer legal name: [COMPLETE]. VAT/tax ID: [COMPLETE]. Registered address: [COMPLETE]. Delivery address and postcode: [COMPLETE]. Contact: Cosmin Covaciu [CONFIRM]. Importer of record and EORI where applicable: [CONFIRM].')
p(d,'Revised proforma number: [ISSUED BY SELLER]. Issue date: [ACTUAL DATE]. Valid until: [CONFIRM]. Reference: 261001102RO. Currency: EUR.')
h(d,'Goods and price')
table(d,['Description','Qty','EUR'],[
('Remote-controlled rubber track chassis platform. Exact model/revision: [CONFIRM]. Nominal system voltage: 48 V [CONFIRM]. Dimensions quoted: 1100 × 720 mm; height 500 mm [CONFIRM]. Guaranteed payload: [RESOLVE 100 kg vs 200 kg]. Full configuration as approved technical annex.','1','2,500.00'),
('Sea freight and delivery to named destination under agreed DDP terms [seller to reconfirm scope].','1','1,370.00'),
('Discount','1','-70.00'),
('Total quoted amount subject to written reconfirmation','','3,800.00')],[12,1.5,3.5])
p(d,'Included items: chassis, motors and controllers, battery assembly, charger, remote control, communication interface, software/SDK and manuals: [SELLER TO LIST EXACT ITEMS AND EXCLUSIONS]. No autonomous navigation capability is implied unless explicitly included in the signed configuration.')
h(d,'Payment and release conditions')
p(d,'Original quotation: 100% payment before shipment. Revised payment arrangement: [AGREE IN WRITING]. Buyer verification of the corrected invoice, configuration, compliance documentation and banking details must be completed before payment approval. This wording is a proposed purchase condition, not an already accepted agreement.')
page(d,'Delivery warranty and banking confirmation')
h(d,'Delivery and import responsibilities')
p(d,'Proposed term for confirmation: DDP [FULL DELIVERY ADDRESS], Incoterms 2020. Seller to specify importer of record, customs representative, country of import clearance, treatment of duties and import VAT, and the supporting documents provided to buyer. Any exclusions, unloading responsibilities or additional charges must be stated explicitly.')
p(d,'Original lead time: 10 working days after payment. Seller to distinguish: ready for dispatch date [ ]; estimated sailing/transit duration [ ]; estimated arrival at buyer address [ ]. Packaging: one wooden box; net/gross weight [ ]; dimensions [ ]; wood type and applicable treatment/marking [ ].')
h(d,'Warranty and acceptance')
p(d,'Warranty duration and start date [ ]; battery warranty [ ]; covered parts and exclusions [ ]; labour, return freight and replacement freight [ ]; response time and remote support [ ]; spare parts availability [ ].')
p(d,'Factory acceptance evidence: serial-number-linked video/report showing agreed payload, forward/reverse/turning, stopping and loss-of-signal behaviour, charger compatibility, battery assembly and communication interface. Acceptance criteria and remedies for failure: [AGREE].')
h(d,'Banking details to be reissued by seller')
p(d,'Beneficiary legal name [ ]; bank name [ ]; bank address [ ]; IBAN/account [ ]; SWIFT/BIC [ ]; currency EUR [CONFIRM]. The original document combines Banking Circle S.A. with an additional Bank of Jining reference. Seller must provide one consistent instruction and confirmation of beneficiary ownership. No bank account is approved by this draft.')
h(d,'Documents supplied with the order')
p(d,'Final commercial invoice; packing list; transport document; applicable machinery declaration and manual; battery conformity and transport information; charger and radio documentation as applicable; serial-number/nameplate photos; test report; warranty terms; working SDK/protocol access if purchased. Customs and fiscal records shall follow the agreed import arrangement.')
p(d,'Issued and approved by seller: name [ ], role [ ], date [ ], signature [ ]. Buyer approval of commercial and technical annexes: [ ]. Supplier must reissue this document on its own letterhead; no original signature or stamp has been reproduced.')
d.save(out/'02_Proforma_revizuita_PROIECT_EN.docx')

d=new('Technical and compliance confirmation for the Aowei chassis','SUPPLIER COMPLETION REQUIRED. This annex resolves the contradictions in invoice 261001102RO and the accompanying images. It is not a declaration of conformity, test certificate or evidence that the requested features are already included.')
h(d,'Configuration to be fixed before payment')
table(d,['Field','Evidence currently available','Supplier confirmation'],[
('Model and identity','Invoice generic; DoC AWC-08; SZUTEST lists other models.','Exact model/revision [ ]; matching evidence [ ].'),
('Payload','100 kg invoice; 200 kg technical sheet.','Guaranteed payload [ ]; operating conditions [ ].'),
('Dimensions and speed','1100 × 720 mm invoice; 720 × 1100 × 500 mm and 3 km/h sheet.','Dimensions [ ]; speed at rated load [ ]; self-weight [ ].'),
('Motors','0.75 kW mentioned; two BLDC motors.','Power per motor [ ]; rated voltage [ ]; controller model [ ].'),
('Battery assembly','48 V system; 12 V batteries mentioned; KIJO 6-GFM-85/Pb photos; Chaowei in sheet.','Manufacturer/model [ ]; chemistry [ ]; count [ ]; wiring [ ]; Ah/Wh [ ].'),
('Charger','110 V AC input in sheet.','Input 230 V/50 Hz or compatible universal range [ ]; output [ ]; plug [ ].'),
('Software and interface','GitHub/SDK placeholder only.','URL/access [ ]; protocol [ ]; pinout [ ]; examples [ ]; supported commands [ ].'),
('Control and safety','Remote-control platform shown.','E-stop [ ]; braking [ ]; loss-of-signal stop [ ]; speed limitation [ ]; intended use [ ].'),
('Autonomous functions','No documented SLAM/navigation package.','Included functions [ ]; exclusions [ ]; added hardware/software [ ].')],[3.2,6.5,7.3])
p(d,'Do not replace an unresolved value with the higher or more favourable value. Battery count, charger voltage and payload must be confirmed against the actual unit, not only a generic brochure.')
page(d,'Compliance evidence and battery transport')
h(d,'Machinery and related equipment')
p(d,'Confirm whether the product is complete machinery or partly completed machinery. Supply the applicable declaration and instructions for the actual configuration. For complete machinery under Directive 2006/42/EC, include product identification, relevant legislation, standards actually applied, EU-established person authorised to compile the technical file, place/date and identified authorised signatory. For partly completed machinery, provide the appropriate declaration of incorporation and assembly instructions.')
p(d,'Explain the relationship between model AWC-08 and the models on certificate MD-20-05-50. Confirm whether serial RC20J4C12021 and VIN C21023932002R belong to the ordered unit. Provide readable nameplate photos. Explain the applicability of cited earth-moving/excavator standards. Provide documentation for the radio control and charger as applicable. A generic certificate is not a substitute for the required manufacturer declaration.')
p(d,'Provide Romanian operating and safety instructions for use in Romania, maintenance instructions, wiring/connection information needed for safe integration and warranty conditions. If ISO 9001 certification is claimed, provide a current copy: the supplied image shows expiry on 5 March 2025.')
h(d,'Battery evidence required for this shipment')
p(d,'Identify the exact battery manufacturer, model, chemistry and construction. Photographs show KIJO 6-GFM-85 and Pb; non-spillable AGM/VRLA or GEL status remains unconfirmed. Provide battery datasheet, safety information, applicable EU declaration of conformity/CE marking and identification/traceability evidence under Regulation (EU) 2023/1542, considering applicable category and implementation dates.')
p(d,'Obtain the freight forwarder’s written classification and acceptance for the complete shipment, stating whether batteries are installed in the vehicle/equipment or shipped separately. Identify applicable UN entry, packing, labelling and documents, or the exact exemption and evidence supporting it. Prevent short circuits, movement, leakage and unintended activation as applicable.')
p(d,'For lead-acid batteries, do not use a lithium UN 38.3 report as substitute evidence. If non-spillable relief is claimed, provide the supporting declaration/test evidence required for that route. If lithium-ion or LiFePO4 batteries are substituted, provide the applicable UN 38.3 test summary and updated transport and EU documentation. Any change requires buyer approval of compatibility, price and configuration.')
p(d,'Supplier representative: [NAME / ROLE / DATE / SIGNATURE]. Buyer technical acceptance: [NAME / DATE]. All answers should reference the final model and serial number where available.')
d.save(out/'03_Anexa_tehnica_si_conformitate_PROIECT_EN.docx')

refs=out/'Referinte originale';refs.mkdir(exist_ok=True)
names=['PI261001RO (1).pdf','4440845121.png','5066555651.png','5066591032.png','5071728143.png','30786697085.jpg']
for name in names: shutil.copy2(src/name,refs/name)
examples=out/'Modele din alte dosare';examples.mkdir(exist_ok=True)
for name,path in [
 ('Checklist import Unitree REFERINTA.docx',r'Z:\00.Roboti\Import Requirements for the Unitree G1 Humanoid Robot.docx'),
 ('Intrebari tehnice FoxTech REFERINTA.docx',r'Z:\00.Roboti\AGV+Cobot FoxTech\Questions 2025.07.09.docx'),
 ('Oferta Greatway 2024 REFERINTA.pdf',r'Z:\00.Roboti\AGV Reeman Robot\Greatway Quotation for Mobile Cobot Unit-20240730.pdf'),
 ('Oferta Avatar 2026 REFERINTA.pdf',r'Z:\00.Roboti\Humanoid AGV\Quotation of AVT-W9D wheeled robot chassis----Avatar (with battery).pdf')]:shutil.copy2(path,examples/name)

(out/'04_Solicitare_furnizor_EN.txt').write_text('''To: angela@aoweimachine.com
Subject: Corrections and missing documents for invoice 261001102RO

Dear Angela,

Please review the attached revised proforma draft and technical confirmation annex before we complete our purchase documentation.

Please resolve the following points in writing:
1. Reissue the invoice with our confirmed legal buyer details, the exact chassis model and the full delivery address.
2. Confirm whether the guaranteed payload is 100 kg or 200 kg, the power per motor and the complete supplied configuration.
3. Confirm the battery brand, model, chemistry, number of batteries and 48 V wiring. Your sheet states Chaowei while the photos show KIJO 6-GFM-85 with the Pb symbol. Confirm whether the batteries qualify as non-spillable and provide supporting evidence.
4. Confirm a charger compatible with 230 V AC / 50 Hz. The current sheet states 110 V input.
5. Provide the working SDK/GitHub link, communication protocol, connector pinout and examples for the supplied controller. Specify whether the product is remote-controlled only or includes autonomous navigation.
6. Provide the applicable conformity documents for the actual model. Explain why the declaration names AWC-08 while the SZUTEST attestation lists other models. Complete the EU technical-file contact and the authorised signatory identification. Confirm the serial number and VIN against nameplate photographs.
7. Provide the operating and safety manual for use in Romania, warranty conditions, test/acceptance evidence and a current ISO certificate if this certification is claimed.
8. Provide the battery EU conformity documentation and obtain the forwarder's classification and acceptance for the planned sea shipment. Lead-acid and lithium battery requirements must not be mixed.
9. Clarify the DDP delivery address, importer of record, customs/VAT documentation and dispatch versus arrival dates.
10. Reissue consistent banking instructions: the current invoice references both Banking Circle S.A. and Bank of Jining.

Please return your corrected supplier-issued documents and completed annex. The attached drafts are proposals for your confirmation; they are not issued or signed on your behalf.

Best regards,
Cosmin Covaciu
''',encoding='utf-8')

(out/'05_Surse_oficiale_si_baterii.txt').write_text('''BATERII - IMPORT IN UE SI TRANSPORT
Actualizat pentru analiza din 22.10.2026.

Bateriile cu plumb, inclusiv AGM/VRLA/GEL, si bateriile Li-ion, inclusiv LiFePO4, nu sunt interzise generic la import in UE. Conditiile depind de categoria bateriei, conformitate, data introducerii pe piata si configuratia transportului.

Pentru Aowei: fotografiile arata KIJO 6-GFM-85, 85 Ah (20 h), 72 Ah (3 h), marcaj Pb. Aceasta indica plumb, dar nu confirma AGM/VRLA/GEL sau exceptarea non-spillable. Confirmarea producatorului si a transportatorului este necesara. Nu se presupune ca bateriile vor fi expediate separat de utilaj.

1. Import UE: verificarea declaratiei UE de conformitate a bateriei, marcajului CE, identificarii/trasabilitatii, instructiunilor si informatiilor de siguranta; se verifica articolele si termenele aplicabile categoriei. SDS/MSDS si acceptarea transportatorului nu substituie conformitatea UE. Rolul de producator/importator si obligatiile de inregistrare/raspundere extinsa se stabilesc pentru circuitul real de introducere pe piata.
https://eur-lex.europa.eu/eli/reg/2023/1542/2025-07-31/eng/pdf

2. Plumb non-spillable: transport posibil; exceptarile necesita indeplinirea conditiilor si dovezilor relevante. UN2800 este o intrare pentru baterii non-spillable separate; nu este stabilit aici drept cod pentru intregul vehicul. Clasificarea finala apartine expeditorului/transportatorului pentru configuratia concreta.
https://imo-epublications.org/content/books/9789280102376.UNNo2800
https://assets.publishing.service.gov.uk/media/68e4f2b5ef1c2f72bc1e4e80/TS_59.2025_Safety_Life_Sea_IMDG_Code_Volume_III.pdf

3. Li-ion/LiFePO4: se cer dovezile aplicabile UN 38.3. LiFePO4 nu este exceptata automat de regulile pentru litiu. Pentru aer exista restrictii suplimentare privind incarcarea si acceptarea; nu se transpun automat la mare.
https://www.phmsa.dot.gov/training/hazmat/new-un-requirement-test-summaries
https://www.iata.org/contentassets/05e6d8742b0047259bf3a700bc9d42b9/lithium-battery-guidance-document.pdf

4. Masini: Directiva 2006/42/CE, anexele I si II. Declaratie, instructiuni si identificare corespunzatoare. Regimul pentru cvasimasini este distinct. Regulamentul nou se aplica in general de la 20.01.2027; verificati data efectiva a introducerii pe piata.
https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006L0042:EN:PDF
https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/machinery_en

5. Import: documente comerciale, transport si declaratie vamala potrivit circuitului real. DDP nu elimina necesitatea trasabilitatii fiscale si documentare.
https://trade.ec.europa.eu/access-to-markets/it/stories/documenti-e-procedure-di-sdoganamento

Nu a fost validata autenticitatea certificatelor Aowei la emitenti. Nu a fost atribuit un cod tarifar sau un cod de transport definitiv. Documentele pentru baterii deteriorate/deseuri necesita analiza separata si nu fac obiectul achizitiei unui echipament nou.
''',encoding='utf-8')
(out/'00_Citeste_ma.txt').write_text('''DOSAR DE VERIFICARE A ACHIZITIEI AOWEI - 22.10.2026

01 - Lista inadvertentelor, inventar si checklist pe etapele achizitiei.
02 - Proiect de proforma revizuita in engleza, de completat si reemis de furnizor.
03 - Anexa tehnica si de conformitate in engleza, de completat de furnizor.
04 - Solicitare pregatita pentru Angela; nu a fost trimisa.
05 - Explicatii despre baterii si linkuri oficiale.
Referinte originale - copii nemodificate ale documentelor Aowei relevante.
Modele din alte dosare - exemple pentru alte produse; nu sunt documente valide pentru Aowei.

Documentele 02 si 03 contin campuri [CONFIRM] / [COMPLETE]. Nu sunt documente finale emise de furnizor si nu trebuie utilizate la plata sau vamuire. Nu s-au reprodus semnaturi sau stampile. Niciun certificat CE/ISO ori document vamal nu a fost fabricat sau declarat valid prin aceasta analiza.

Z: este mapat la \\192.168.100.169\Comun. Dosarul sursa a fost analizat integral pentru PDF si imagini; videoclipurile au fost inventariate. Dosarele similare identificate sunt descrise in raport. Cautarea generala de nume pe Z: este in curs; nu exista inca o confirmare de acoperire integrala a serverului. Nu s-au deschis toate arhivele si nu s-a efectuat OCR pe toate imaginile din retea.
''',encoding='utf-8')
print(str(out))
print('\n'.join(x.name for x in out.iterdir()))
