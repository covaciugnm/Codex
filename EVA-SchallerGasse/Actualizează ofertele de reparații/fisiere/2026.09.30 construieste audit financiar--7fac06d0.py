from pathlib import Path
import json,re,shutil,hashlib,datetime,collections,zipfile,xml.etree.ElementTree as ET
from decimal import Decimal as D
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
from docx import Document
from docx.shared import Pt
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
R=Path(__file__).resolve().parent.parent;DATE='2026.09.30'
B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail';F=R/'10. Banci + Extrase de cont';A=F/(DATE+' Audit facturi si plati');A.mkdir(exist_ok=True)
es={e['id']:e for p in (B/'Surse').glob('*.json') for e in json.loads(p.read_text(encoding='utf-8'))}
comm_path=B/(DATE+' Registru comunicatii.json')
comm={e['id']:e['cale'] for e in json.loads(comm_path.read_text(encoding='utf-8'))['comunicatii']} if comm_path.exists() else {}
ar={a['id']:a for a in json.loads((B/(DATE+' Registru atasamente.json')).read_text(encoding='utf-8'))}
allpdf=[p for p in R.rglob('*') if p.suffix.lower()=='.pdf' and 'folder map' not in p.parts and A not in p.parents]
def source(query):
 if query in ar and ar[query].get('cale'):return ar[query]['cale']
 matches=[p for p in allpdf if query.lower() in p.name.lower()]
 if matches:
  matches.sort(key=lambda p:('Arhiva Eva-Mail' in str(p),'Facturi neachitate' in str(p),len(str(p))))
  return matches[0].relative_to(R).as_posix()
 return ''
def safe(s):return re.sub(r'[<>:"/\\|?*]','-',s)
tx=json.loads((A/(DATE+' Tranzactii extrase.json')).read_text(encoding='utf-8'))
snow=source('03 - 2026-09-28 ATTENSAM')
tx.append(dict(id_intern='AT22-036',cont='A&C AT22',data_platii='2026.09.28',data_valutei='2026.09.28',suma_eur='-640.06',text_banca='ATTENSAM Rechnung 34642 / 1088117; Zahlungsreferenz 346421088117',sursa=snow,pagina=1,numar_plata_banca='1471264511',referinta_banca='346421088117',document_asociat='',data_document='',tip='de clasificat'))
bytx={t['id_intern']:t for t in tx};invoices=[];alloc=[];sources=[]
def add(key,provider,no,date,amount,status,query='',ref='',due='',period='',note='',pay=None,extra=0,discount=0,emails=None,external=0,account='',currency='EUR'):
 if key=='F007':
  date='2026.06.03'
  note=note.replace('Extras FinanzOnline la 2026.06.03: obligatie 186.','Extras FinanzOnline din 2026.06.03: obligatie 186, inregistrata fiscal 2026.05.22.')
 amount=D(str(amount));extra=D(str(extra));discount=D(str(discount));paid=D('0');dates=[];numbers=[];ids=[];accounts=[]
 for tid,amt in pay or []:
  t=bytx[tid];v=D(str(amt));paid+=v;dates.append(t['data_platii']);ids.append(tid);accounts.append(t['cont']);numbers.append(t.get('numar_plata_banca',''))
  t.update(document_asociat=no,data_document=date,referinta_banca=ref,tip='Factura/taxa asociata',factura_id=key)
  alloc.append({'ID plata intern':tid,'ID document':key,'Nr factura/document':no,'Data document':date,'Data plata':t['data_platii'],'Alocat EUR':float(v),'Cont':t['cont'],'Referinta banca':ref,'Nr bancar disponibil':t.get('numar_plata_banca',''),'Sursa plata':t['sursa'],'Pagina extras':t['pagina']})
 p=source(query) if query else ''
 if p:
  original=R/p;target=A/'Documente justificative'/(date+' '+safe(provider[:22]+' '+no[:35])+original.suffix);target.parent.mkdir(exist_ok=True)
  shutil.copy2(original,target);p=target.relative_to(R).as_posix()
  sources.append({'Document':key,'Sursa original':original.relative_to(R).as_posix(),'Copie audit':p,'SHA256':hashlib.sha256(original.read_bytes()).hexdigest()})
 balance=amount+extra-paid-discount-D(str(external))
 row={'ID':key,'Furnizor':provider,'Nr factura/document':no,'Data document':date,'Perioada':period,'Valoare document EUR':float(amount),'Accesorii EUR':float(extra),'Achitat bancar EUR':float(paid),'Achitat alt cont EUR':external,'Skonto EUR':float(discount),'Sold document EUR':float(balance),'Statut':status,'Scadenta':due,'Data plata':'; '.join(dates),'Nr plata bancar':'; '.join(n for n in numbers if n),'ID plata intern':'; '.join(ids),'Cont platitor':'; '.join(dict.fromkeys(accounts)),'Referinta plata':ref,'Cont client':account,'Observatii':note,'Document local':p,'Email ID sursa':'; '.join(emails or []),'Original verificabil':bool(p)}
 invoices.append(row);return row

# Plati dovedite: o factura este inregistrata o singura data, indiferent de numarul copiilor si somatiilor.
add('F001','Benn-Ibler notar','1925/2025','2025.12.04',1362,'ACHITAT','1925 25_20251204152623',ref='Re.Nr.1925/2025 UID ATU57639112 667/2025',due='2025.12.18',period='Constituire GmbH, decembrie 2025',pay=[('AT22-009',1362)],emails=['0178644b-ac12-46e3-bc36-29090219bae0'])
add('F002','CERHA HEMPEL','25/31404','2026.01.27',6147.70,'ACHITAT','HN 25_31404 A&C Wohnart',ref='Honorarnote 25/31404',period='2025.11.01–2026.01.12',pay=[('AT22-010',6147.70)],note='3.000 constituire + 875 due diligence + 700 servicii suplimentare net; cheltuieli si TVA. Taxa registru 493 este deja inclusa; nu se inregistreaza o a doua plata.',emails=['7ecc37bb-e3f2-4467-af48-d58bbb1220e2'])
add('F003','Benn-Ibler notar','242/2026','2026.02.24',933,'ACHITAT PERSONAL','242 2026.pdf',ref='Kaufvertrag ob EZ2235KG Meidling',due='2026.03.10',period='Legalizare contract, februarie 2026',pay=[('AT13-012',933)],note='Factura emisa A&C, plata Cosmin. Nu s-a identificat rambursare catre Cosmin in extrasele analizate.',emails=['849ddbf6-3bf4-468f-875a-b6e34b26a1bb'])
add('F004','ARESCO','20260301','2026.03.02',59400,'ACHITAT','20260301 Schallergasse 35',ref='Rechnung 20260301',period='2025.11–2026.02',pay=[('AT22-014',59400)],note='Numarul facturii nu este data emiterii: documentul este emis 2026.03.02. Comision 49.500 + TVA 9.900.',emails=['81df9242-74cc-4111-b4a2-0b12fc406246'])
add('F005','CERHA HEMPEL','26/30186','2026.03.17',24116,'ACHITAT','HN_26_30186_A&C_Wohnart',ref='Honorarnote 26/301186 (text bancar)',due='2026.03.31',period='2025.11.18–2026.03.15',pay=[('AT22-021',24116)],note='Extrasul are un 1 suplimentar: 26/301186. Asociere confirmata prin suma, beneficiar si factura. Subiectul somatiei mentioneaza eronat vechiul 25/31404, dar atasamentul si corpul se refera la 26/30186.',emails=['5f2f077b-8297-4843-9111-3a5584c04426'])
add('F006','ARTUS','1261556','2026.03.31',360,'ACHITAT','AR1261556',ref='1261556',period='Inregistrare fiscala',pay=[('AT22-027',378.08)],extra=18.08,note='Plata 378,08 = factura 360 + Mahngebühr 15 + dobanzi 3,08 conform somatiei 2026.05.26. Textul emailului mentioneaza 1261850/2026.04.16, diferit de subiect si de ambele PDF-uri; nu creeaza singur o factura suplimentara.',emails=['d3515f4d-790d-442d-882b-2a8c4c3cf511'])
bytx['AT22-028']['numar_plata_banca']='1050243883'
add('F007','Finanzamt','K 04-06/2026; StNr 094466620','2026.05.22',186,'ACHITAT','FA Kontoauszug A&C.pdf',ref='2604/06+18600K 094466620',due='2026.05.15',period='Inregistrare fiscala 04-06/2026',pay=[('AT22-028',186)],note='Extras FinanzOnline la 2026.06.03: obligatie 186. Ordin 2026.06.10; debit 2026.06.11, valuta 2026.06.10. Dovada bancara indica beneficiar AT62 0100 0000 0550 4099.',emails=['4aba8366-e06d-4082-a2ba-cfec65295770'])
add('F008','MA6 - impozit si gunoi','480960255591 / 889970805056','2026.04.10',93.23,'ACHITAT PERSONAL','20260426162134457.pdf',ref='889970805056',due='2026.05.15',period='2026.04–06',pay=[('AT13-021',93.23)],note='Avizul si somatia 05/2026 sunt aceeasi obligatie. Hofhans a cerut returnarea debitului sau din 2026.05.15; plata proprie din 2026.07.27 se inregistreaza o singura data. Confirmare de alocare MA6 utila.',emails=['6380c08d-1bf6-44b7-99c2-053b4cfdd295','9062dd6c-1685-41dc-bd9e-437fd223e300'],account='058899708')
add('F009','ARTUS','1263320','2026.06.30',240,'ACHITAT PERSONAL','Honorarnote 1263320',ref='1263320',period='Contabilitate 2026.01–03',pay=[('AT13-022',240)],emails=['f15607c1-5e31-4100-af08-f947c74d9d43'])
add('F010','Sturm Energie','29700/10/2026','2026.05.18',115.36,'ACHITAT PERSONAL','R_D_4000108031_29700',ref='400011831511',due='2026.06.02',period='2025.06.11–2026.04.08; Top 15',pay=[('AT13-023',115.36)],note='Perioada originala se termina la 2026.04.08, nu 2026.03.08. Factura foloseste UID ATU76175979 si p.a. A&C; apartenenta economica fost/nou proprietar ramane de clarificat.',account='42017328')
add('F011','Attensam','34648/1088117','2026.09.03',156.53,'ACHITAT; ALOCARE DE CONFIRMAT','3464803092026.pdf',ref='Rechnung 34648/1088117 0926KST606/4410',due='2026.09.17',period='Deratizare 2026.07–2027.06',pay=[('AT13-024',156.53)],note='Debit personal 2026.09.09. Furnizorul cere dovada la 2026.09.16. Nu repeta plata. Extrasul general nu arata IBAN-ul destinatarului, deci ipoteza vechiului IBAN nu este probata.',emails=['68e6121b-8670-4bc2-b2ce-5920a4e49b23'],account='1088117')
add('F012','Conrad','9789934508','2026.09.16',44.99,'ACHITAT','9789934508.pdf',ref='2019635130.528114263.Vorauskasse',period='2 telecomenzi RS2W F1 + transport',pay=[('AT22-034',44.99)],note='Plata anticipata 2026.09.14, factura ulterioara 2026.09.16 mentioneaza deja achitat. Nu este o plata lipsa.',account='528114263')
add('F013','MA37','1303993-2026-3 / 000235125033','2026.09.25',39,'ACHITAT','ZA_Lokal_20260925',ref='000235125033',due='2026.10.30',period='Consultare planuri',pay=[('AT22-035',39)],emails=['ad4b69d0-b596-42c5-aead-5e5d7cfddcbc'])
add('F014','Attensam','34642/1088117','2026.09.03',653.12,'ACHITAT CU SKONTO','3464203092026.pdf',ref='346421088117',due='2026.09.30 cu Skonto; 2026.10.15 integral',period='Deszapezire 2026.11.01–2027.04.15',pay=[('AT22-036',640.06)],discount=13.06,note='Dovada separata, ulterioara extrasului general din aceeasi zi; confirmat de utilizator. 653,12 - 640,06 - 13,06 = 0. Nu se adauga din nou la totalul extrasului.',account='1088117')
add('F015','MA29','SHOP2026000439','2026.07.09',21.60,'ACHITAT CONFORM FACTURII','RechnungSHOP2026000439',ref='BestellNr 712819',period='Profiluri geotehnice',external=21.60,note='Factura confirma plata electronica 2026.07.09. Contul si numarul bancar nu sunt identificate in cele doua extrase; nu presupunem card RO/Wise.')

# Obligatii cu document, fara debit identificat in conturile analizate.
add('F016','CERHA HEMPEL','26/30363','2026.04.21',2640.22,'FARA PLATA IDENTIFICATA','HN 26_30363 A&C Wohnart',ref='HN 26/30363 / COVACIU/42222000',due='2026.05.05',period='2026.03.16–2026.03.31',note='Emailul Capra acorda expres 14 zile; vechiul Excel spunea la primire. Nicio plata egala/asociabila in AT22 sau AT13.',emails=['ae6603d1-5fed-4efc-b5d2-6e44e91d2d2a'])
add('F017','ARTUS','1264971','2026.09.15',144,'FARA PLATA IDENTIFICATA','Honorarnote 1264971',ref='1264971',due='La primire',period='Contabilitate 2026.04–06',emails=['c1c120a7-8474-4949-8d60-c3616187621e'])
add('F018','MA6 - impozit si gunoi','480960377428 / 889970805086','2026.07.10',93.23,'FARA PLATA IDENTIFICATA','20260720185303213',ref='889970805086',due='2026.08.15 (document)',period='2026.07–09',note='Document recuperat: total tiparit 186,46 = trimestru curent 93,23 + restant trimestru precedent 93,23. Plata AT13-021 din 2026.07.27 stinge componenta precedenta; ramane 93,23, sub rezerva alocarii MA6.',emails=['470a26f6-cb6f-4f97-b97e-567a0a82cd4c'],account='058899708')
add('F019','MA31 - Wiener Wasser','310910909051','2026.09.07',15.18,'ORDIN ANUNTAT; DEBIT DE CONFIRMAT','6_20260929_0033_009_Post',ref='010010047297',due='2026.10.15',period='2026.03.27–2026.06.01 + avans nou',note='7,59 taxa contor + 7,59 avans. Abgabenkonto NOU 123482077, contract WA120031905/06. Capturile 2026.09.30 arata GESENDET, fara suma/debit verificabil. Nu declaram achitat si nu reluam plata pana la verificare.',emails=['1c6fe6ec-d827-48b0-97b4-2a735c430559'],account='123482077; contor 120031905')
sturm=[('29701',109.99,'400011831611','10'),('29702',109.99,'400011831811','3'),('29703',109.99,'400011834111','13,14'),('29704',114.05,'400011850011','4'),('29705',109.99,'400011850111','12'),('29706',109.99,'400011850211','8'),('29708',109.99,'400012685811','17'),('29721',109.99,'400012438711','5')]
for idx,(no,amount,ref,top) in enumerate(sturm,20):
 add('F'+str(idx).zfill(3),'Sturm Energie',no+'/10/2026','2026.05.18',amount,'FARA PLATA; REPARTIZARE DE CLARIFICAT','_'+no+'_10_2026_1.pdf',ref=ref,due='2026.06.02',period='2025.06.11–2026.04.08; Top '+top,note='Factura finala pe HI Schallergasse, p.a. A&C; datele/UID nu coincid cu A&C. Clarificat cu furnizorul si Capra cine suporta perioada anterioara preluarii. Nu se compenseaza automat cu creditul Strom.',account='42018142' if no=='29721' else '42017328')
add('F028','Wien Energie','5147075005','2026.07.10',109.02,'FARA PLATA; REPARTIZARE DE CLARIFICAT','13 - 2026-07-10 WIEN',ref='260005332090',due='2026.07.27; somatie 2026.08.18',period='2025.06.11–2026.06.01; gaz Top 16',note='Costuri fixe, consum 0. Document pe vechea administrare; clarificat perioada si destinatarul.',account='1202807776 / 220005332090')
add('F029','Donau / Commerz-Inkasso','2616052 / polita 2044001194','2026.09.09',3183.62,'CONTESTAT / DOCUMENTE CERUTE','01 - 2026-09-09 DONAU',ref='2616052',due='2026.09.21 (cererea de amanare neconfirmata)',period='Doua prime trimestriale',extra=550.72,note='3734,34 = 3183,62 principal + 501,58 Inkasso + 30 cost creditor + 19,14 dobanda. Nu exista plata identificata. Cererea 2026.09.15 si draftul revenirii 2026.09.30 nu reprezinta acordul creditorului.',emails=['b487e95f-96c3-4cf4-b31e-c01a286a98ae'])
add('F030','E3 / KSV1870','RE26-0001 / KSV 20260504299','2026.01.12',597.60,'CONTESTAT','RE26-0001_P2041',ref='20260504299',extra=281.74,period='DWG',note='Creanta comunicata KSV 879,34, din care factura 597,60. Oprirea demersurilor extrajudiciare la 2026.07.05 nu anuleaza creanta. Se urmareste separat de Donau.')
add('F031','Sturm Energie','29707/10/2026 - CREDIT','2026.05.18',-846.92,'CREDIT; BENEFICIAR DE CLARIFICAT','_29707_10_2026_1.pdf',period='Curent 2025.06.11–2026.03.18',note='Factura arata servicii 190,08 si sold creditor 846,92 dupa avansuri; rambursare anuntata in contul vechi AT21...0800. Nu exista credit in AT22/AT13. Nu este automat o creanta certa a A&C si nu reduce gazul fara confirmare.',account='42017328')
add('F032','Finanzamt','K 07-09/2026 (din registrul anterior)','2026.04.15',93,'DE RECONFIRMAT DIN CONT FISCAL','14 - 2026-06-22 FINANZAMT',ref='StNr 094466620; K 07-09/2026',due='2026.08.17 (din registrul anterior)',period='2026.07–09',note='PDF local criptat; suma/data nu au putut fi recitite independent. Exista decizia anuala 2026 de 375 EUR si plata 186 EUR. IBAN AT36 din vechiul Excel difera de AT62 din decizia originala si plata efectuata; nu reutiliza fara verificare ARTUS/FinanzOnline.')
add('F033','MA6 - apa cont vechi','Mahnung 070000622528','2026.08.12',7.59,'CONT VECHI; SOLD DE CLARIFICAT','20260818125542.pdf',ref='070000622528',due='2 saptamani de la comunicare',period='Iulie 2026, contract /05',note='Pe fostul proprietar, Abgabenkonto 123003016. Avizul anterior de 15,18 includea 7,59 vechi + 7,59 curent; nu adunam avizul si somatia. Contul nou /06 este distinct. Cerut extras de transfer/storno intre conturi.',account='123003016; contor 120031905')
add('F034','Attensam','14983/1001371','2026.07.20',156.53,'OMISIUNE; PERIOADA/STORNO DE CLARIFICAT','20260727212104743.pdf',ref='14983/1001371',due='2026.08.03',period='Original: Juli - Juni 2026 (ambiguu)',note='Factura identificata in mesajul Capra 2026.07.28, pe Hofhans, cu BANKEINZUG. Acelasi contract ATT500347000, dar perioada diferita/ambigua fata de 25777 si 34648. Necesita fisa furnizor si eventual storno; nu se adauga automat la plata.',emails=['ecee4a0a-0c7c-4823-bbbd-bea218e703d9'],account='1001371')
add('F035','Attensam','6253/1001371','2026.07.14',653.12,'REEMISA; NU SE ADUNA','20260721182945252.pdf',period='Winterservice 2026.11–2027.04',note='Versiune veche aceeasi prestatie si contract ATT803319000; 34642 este versiunea A&C, deja achitata. Confirmat storno/alocare cu furnizorul.')
add('F036','Attensam','25777/1001371','2026.08.11',156.53,'REEMISA; NU SE ADUNA','Scan2026-08-20_175626',period='Deratizare 2026.07–2027.06',note='Versiune veche aceeasi prestatie si contract ATT500347000; 34648 este versiunea A&C, plata identificata. Nu confunda cu 14983.')
add('F037','TOMS','77260142','2026.09.10',540,'DESTINATAR GRESIT; EXCLUS','77260142',note='Proiect C751 Wurmbstraße 48, destinatar RP Projektentwicklung GmbH. Nu reprezinta datoria Schallergasse. Confirmare TOMS 2026.09.22 de arhivat.',period='Alt proiect')
add('F038','Donau','Estimare prima trimestriala Q4','2026.09.30',1591.81,'ESTIMARE; FARA AVIZ Q4','02 - 2026-06-05 DONAU',due='2026.10.01 estimat',note='Documentul etichetat Q4 in vechiul folder este somatia din 2026.06.05, nu aviz Q4! Suma trebuie verificata cu Donau dupa cererea de reducere/acoperire; exclusa din total facturi confirmate.')
add('F039','Finanzamt','Estimare K 10-12/2026','2026.09.30',96,'ESTIMARE; DE CONFIRMAT',due='2026.11.16 din registrul anterior',note='96 = 375 anual - 186 platit - 93 presupus Q3. Nu este document fiscal nou, soldul curent FinanzOnline trebuie verificat.')
add('F040','WOHR','Wartung Parklift - oferta','2026.09.15',285,'ANGAJAMENT NET; NU ESTE FACTURA',period='Interventie propusa octombrie 2026',note='285 EUR NET in oferta. Nu se amesteca in totaluri brute si nu este datorie exigibila in lipsa interventiei/facturii.')

# Provenienta email exacta: niciun ID aproximat nu este publicat ca sursa.
electric=[('41409',149.53,'6','2025.05.25–2026.04.08','400011831411',1),('41410',290.89,'15','2024.05.25–2026.04.08','400011831711',5),('41411',129.62,'10','2025.05.25–2026.04.08','400011831911',9),('41412',290.89,'2','2024.05.25–2026.04.08','400011832011',13),('41413',290.89,'3','2024.05.25–2026.04.08','400011832111',17),('41414',290.89,'12','2024.05.25–2026.04.08','400011833911',21),('40809',99.67,'16','2023.05.25–2024.05.24','400011852911',25),('41415',248.23,'16','2024.05.25–2026.04.08','400011852911',29),('41422',27.12,'5','2025.05.25–2026.04.08','400012438611',1)]
assert sum(D(str(x[1])) for x in electric)==D('1817.73')
for i,(no,amount,top,period,ref,page) in enumerate(electric,41):
 query='f68f3c74-23f0-4e9d-826f-bad75bfe0998' if no=='41422' else '7c11a093-4ace-4582-af6a-640b3ed6bfe2'
 note=f'Factura curent transmisa de Capra 2026.07.21; pagina {page} din PDF. Fara debit in cele doua conturi. Perioada include fostul proprietar; repartizarea si soldul furnizorului de clarificat.'
 if no=='41415':note+=' Totalul de plata tiparit 347,90 include 99,67 din 40809, deja in F047. Aici se retin doar serviciile noi 248,23, fara dublare.'
 if no=='41422':note+=' Servicii 149,53 minus credit furnizor 122,41 = suma solicitata 27,12. Creditul este deja aplicat in factura; nu este o plata din conturile proprii. Extrasul STURM din 2026.06.16 arata istoricul facturilor 16522/2023, 62639/2025 si 62640/2025 si platile Hofhans; sold creditor 122,41. Acestea nu se adauga ca datorii noi ale A&C.'
 add(f'F{i:03d}','Sturm Energie',no+'/10/2026','2026.07.15',amount,'FARA PLATA; REPARTIZARE DE CLARIFICAT',query,ref=ref,due='2026.08.03',period=period+'; curent Top '+top,note=note,account='42018142' if no=='41422' else '42017328',emails=['2703c8af-f944-4ae8-9799-07bc5d5032d0'])
for row in invoices:
 row['Original local disponibil']=row.pop('Original verificabil')
 row['Total tiparit document EUR']=186.46 if row['ID']=='F018' else row['Valoare document EUR']
 if row['ID']=='F048':row['Total tiparit document EUR']=347.90
 if row['ID']=='F018':row['Observatii']+=' Coloana Valoare document EUR contine numai obligatia unica Q3; totalul avizului este in coloana Total tiparit document EUR. Componenta Q2 si plata ei sunt deja in F008.'
 if row['ID']=='F035':row['Observatii']=row['Observatii'].replace('Confirmat storno/alocare cu furnizorul.','De confirmat storno/alocare cu furnizorul.')
 if row['ID']=='F037':
  row['Observatii']='Proiect C751 Wurmbstrasse 48, destinatar RP Projektentwicklung GmbH. TOMS confirma expres la 2026.09.22 ca emailul a fost trimis din greseala. Exclus din datoriile Schallergasse.'
  row['Email ID sursa']='a3bdca29-8982-4b24-8d7c-300d3c256960'
 if row['ID']=='F033':row['Observatii']+=' Capra descrie in email suma drept 8 EUR; PDF-ul somatiei arata 7,59 EUR. Nu este identificata o a doua taxa de 8 EUR.'
 valid=[i for i in row['Email ID sursa'].split('; ') if i in es]
 if row['ID']=='F011':valid=[i for i in es if i.startswith('68e6121b')]
 if row['ID']=='F029':valid=[i for i in es if i.startswith('b487e95f')]
 row['Email ID sursa']='; '.join(valid)
 row['Email local']=next((comm[i] for i in valid if i in comm),'')

# Toate miscarile bancare raman vizibile, inclusiv cele care nu reprezinta facturi.
pair={'AT22-001':'AT13-007','AT22-011':'AT13-011','AT22-020':'AT13-013','AT13-007':'AT22-001','AT13-011':'AT22-011','AT13-013':'AT22-020','AT22-015':'AT22-016','AT22-016':'AT22-015','AT22-005':'AT22-019','AT22-006':'AT22-018','AT22-007':'AT22-017','AT22-017':'AT22-007','AT22-018':'AT22-006','AT22-019':'AT22-005'}
for t in tx:
 t['suma_eur']=float(D(str(t['suma_eur'])));t['pereche']=pair.get(t['id_intern'],'');t['observatii']=''
 if t['tip']=='de clasificat':
  s=t['text_banca'];id=t['id_intern']
  if id in ['AT22-001','AT22-011','AT22-020','AT13-007','AT13-011','AT13-013']:t['tip']='Transfer asociat–firma';t['observatii']='Nu este plata catre furnizor. Perechea din celalalt cont nu se aduna ca a doua cheltuiala.'
  elif id in ['AT22-012','AT22-013']:
   t['tip']='Achizitie / fonduri Treuhand';t['document_asociat']='Kaufvertrag 2026.02.20';t['data_document']='2026.02.20';t['observatii']='75.900 avans taxe / 1.650.000 pret imobil; nu sunt facturi de servicii. Contract si ordine identificate; decont final Treuhand si dovada virarii taxelor de obtinut.'
  elif id in ['AT22-015','AT22-016']:t['tip']='Numerar intrare/iesire';t['observatii']='Pereche -10/+10; net zero, fara factura identificata.'
  elif 'Karten' in s:t['tip']='Comision card / stornare';t['observatii']='Patru debite 37,90; trei stornari 37,90. Cost net 37,90.'
  elif 'Habenzinsen' in s:t['tip']='Dobanda cont personal'
  elif id in ['AT13-010','AT13-016','AT13-017','AT13-018']:t['tip']='Transfer propriu personal';t['observatii']='Cont sursa in afara celor doua extrase; nu este venit din facturi.'
  elif 'Burgenland' in s:t['tip']='Plata personala; document lipsa';t['referinta_banca']='266000185790' if id=='AT13-025' else '266000172222';t['observatii']='Plata efectuata; lipseste Strafverfügung/decizia. Nu o atribuim firmei si nu se plateste din nou.'
  else:t['tip']='Comision bancar';t['document_asociat']='Extras bancar';t['data_document']='2026.09.28';t['observatii']='Justificare prin extras; nu confundam absenta unei facturi de furnizor cu plata nerecunoscuta.'
 t['perioada_firma']='Anterior actului de constituire 2025.12.03' if t['data_platii']<'2025.12.03' else 'Constituire pana la registru 2026.01.08' if t['data_platii']<'2026.01.08' else 'Dupa inregistrarea firmei'
 if t.get('factura_id'):t['document_local']=next(x['Document local'] for x in invoices if x['ID']==t['factura_id'])
 else:t['document_local']=t['sursa']

corrections=[
 ('Email Capra 2026.07.21','Doua PDF-uri de 32 si 4 pagini','Facturi curent STURM absente din tabelele istorice','Noua facturi, suma unica 1.817,73 EUR fara debit. Perioade din 2023–2026: repartizare fost/nou proprietar de clarificat. 41415 include 40809; 41422 aplica deja credit 122,41.','F041–F049'),
 ('De platit 2026-09-21','De platit!J4:K5; F15','Attensam 809,65 de achitat','796,59 debitat + 13,06 Skonto; sold matematic zero. Alocare 34648 de confirmat.','F011; F014'),
 ('Servicii platite 2026-09-28','Servicii cladire!K22; K26; K37','Rest 13,06 la deszapezire','Rest 0; reducerea in coloana separata, inclusa in formula.','F014'),
 ('De platit 2026-09-21','De platit!10:11','Doua pozitii MA6 x 93,23','Aceeasi obligatie Q2; achitata 2026.07.27.','F008'),
 ('Reconciliere 2026-09-28','Neachitate!17','MA6 Q3 estimat, fara document','Aviz 2026.07.10 gasit: 186,46 cumulativ minus 93,23 achitat = 93,23.','F018'),
 ('Reconciliere 2026-09-28','Achitate!E7','ARTUS1261556 factura 378,08','Factura 360; accesorii 18,08; plata 378,08.','F006'),
 ('Reconciliere 2026-09-28','Neachitate!G5; Servicii!L34','HN26/30363 scadenta la primire','Capra fixeaza 2026.05.05, termen 14 zile.','F016'),
 ('De platit 2026-09-21','De platit!F8; Note verificare!A13','Donau 3183,62+501,58+19,14=3734,34','Lipseau 30 costuri creditor. Totalul corect este 3734,34.','F029'),
 ('Reconciliere 2026-09-28','Neachitate!3; Facturi neachitate/02 PDF','Q4 Donau documentat prin PDF iunie','PDF-ul este somatia iunie. Q4 ramane estimare de reconfirmat.','F038'),
 ('Servicii platite 2026-09-28','F9:F17','STURM perioada pana 2026.03.08','Originalele gaz: pana 2026.04.08; documentele au vechiul UID.','F010; F020–F027'),
 ('Reconciliere 2026-09-28','Neachitate!13; Servicii!A41','Credit STURM disponibil compensarii','Rambursare anuntata spre contul vechi AT21...0800; dreptul A&C si incasarea de clarificat.','F031'),
 ('Reconciliere 2026-09-28','Neachitate!16; Servicii!8','Apa 15,18 restant + somatie 7,59','Nu se cumuleaza; cont vechi 123003016 si cont nou 123482077, aviz nou 310910909051.','F019; F033'),
 ('Toate registrele anterioare','Lipsa rand Attensam14983','Factura 14983 neinventariata','156,53 pe Hofhans, perioada Juli–Juni2026 ambigua; verificare storno/perioada.','F034'),
 ('Reconciliere 2026-09-28','Neachitate!H15; denumire PDF14','FA IBAN AT36 in tabel','Decizie si plata reala indica AT62; documentul cu AT36 este criptat. Nu preluam ca date certe.','F007; F032'),
 ('Reconciliere 2026-09-28','Achitate!Lipsa date document','Facturi cu date lipsa','Datele facturilor si datele bancare sunt coloane distincte. Numere bancare numai cand exista in sursa.','Registru documente; Plati banca'),
 ('De platit 2026-09-21','Note verificare!A7:A10','Recomandare re-plata Attensam','Debit confirmat. Se trimite dovada/alocare; nicio plata repetata pe baza unei ipoteze.','F011'),
 ('Servicii platite 2026-09-28','K25; totaluri','Contestat are rest 0','Soldul documentar al creantelor contestate ramane vizibil, separat de lista de plata.','F029; F030'),
 ('Reconciliere 2026-09-28','Achitate!G17','MA29 platit probabil card RO/Wise','Factura confirma plata; contul nu este identificat.','F015'),
 ('Mesaj Capra 2026.03.12','Bescheid Finanzamt','375 EUR pentru anul trecut','Decizia spune expres Vorauszahlungsbescheid2026, nu impozit2025 suplimentar.','F007; F032; F039'),
]
checks=json.loads((A/(DATE+' Control totaluri extrase.json')).read_text(encoding='utf-8'))
personal=sum(D(str(x['Alocat EUR'])) for x in alloc if x['Cont']=='Cosmin AT13')
confirmed=sum(D(str(x['Sold document EUR'])) for x in invoices if x['Statut']=='FARA PLATA IDENTIFICATA')
assert personal==D('1538.12')
assert len(tx)==62 and len({t['id_intern'] for t in tx})==62
assert all(c['egal'] for c in checks)
assert all(abs(sum(D(str(a['Alocat EUR'])) for a in alloc if a['ID plata intern']==t['id_intern']))<=abs(D(str(t['suma_eur']))) for t in tx)
assert all(x['Sold document EUR']==0 for x in invoices if x['ID'] in [f'F{i:03d}' for i in range(1,16)])
assert sum(D(str(bytx[i]['suma_eur'])) for i in ['AT22-001','AT22-011','AT22-020'])==D('1834000')

overview=[
 ('Data verificarii',DATE),('Obiect','Schallergasse35; A&C Wohnart si platile personale relevante'),
 ('Rezultat','Registrele istorice contin omisiuni si clasificari gresite. Acest registru le corecteaza fara a transforma estimarile in datorii certe.'),
 ('Acoperire bancara','Toate cele61 tranzactii din cele5 pagini de extrase 2025.01.01–2026.09.28, plus plata Attensam640,06 din dovada separata =62.'),
 ('Data firmei','Act constitutiv 2025.12.03; inregistrare Firmenbuch 2026.01.08, FN668224h. Pastrate inclusiv operatiunile de constituire si cele personale anterioare.'),
 ('Limita temporala','Extrase generale generate 2026.09.28 14:33/14:34; nu exista extras complet 2026.09.29–30. Dovada Attensam de mai tarziu este adaugata o singura data.'),
 ('Platit personal pentru obligatii asociate firmei EUR',float(personal)),('Facturi/taxe cu document fara plata identificata EUR',float(confirmed)),
 ('Ce include totalul de mai sus','CERHA2640,22 + ARTUS144 + MA6Q3 93,23. Este constatarea lipsei unui debit in sursele verificate, nu autorizare de plata.'),
 ('Apa noua','15,18; ordin anuntat 2026.09.30, debit de confirmat. Nu se repeta automat.'),
 ('Sturm si Wien Energie','Curent STURM1.817,73 + gaz STURM883,98 + WienEnergie109,02 fara debit; repartizare intre proprietari si corectarea destinatarilor de clarificat. Credit846,92 separat.'),
 ('Contestatii','Donau3734,34 si KSV879,34 sunt expuneri distincte, nu facturi declarate stinse.'),
 ('Alte puncte','Attensam14983 156,53 neclar; FA93 de reconfirmat; apa cont vechi7,59; DonauQ4 1591,81 estimare; WOHR285net angajament.'),
 ('Documente lipsa','Deciziile Burgenland250/55; decont final Treuhand si taxele efectiv virate; extras fiscal curent/decriptare PDF; alocari furnizori; contul platii MA29.'),
 ('Regula numarului platii','AT22-xxx/AT13-xxx sunt ID-uri interne de reconciliere, nu numere bancare. Referinta ordinului si Buchungsnummer sunt campuri separate; lipsurile raman goale.'),
 ('Validare','Totalurile tuturor tranzactiilor coincid la cent cu cele doua extrase. Fiecare plata este clasificata; nu s-au identificat doua debite proprii pentru aceeasi factura.'),
 ('Originale','Cele4 Exceluri istorice sunt pastrate. PDF-urile din Documente justificative sunt copii identice cu sursele, hash in foaia Surse.'),
 ('Operatiuni externe','Nu au fost trimise emailuri si nu au fost initiate plati in aceasta reconciliere.')]

def sheet(wb,name,rows,headers=None):
 sh=wb.create_sheet(name)
 if headers is None:headers=list(rows[0]) if rows else ['Nota']
 sh.append(headers)
 for r in rows:sh.append([r.get(k,'') for k in headers] if isinstance(r,dict) else list(r))
 sh.freeze_panes='A2';sh.auto_filter.ref=sh.dimensions
 for c in sh[1]:c.font=Font(name='Calibri',bold=True,color='FFFFFF',size=11);c.fill=PatternFill('solid',fgColor='203E54');c.alignment=Alignment(wrap_text=True,vertical='center')
 sh.row_dimensions[1].height=32
 for row in sh.iter_rows(min_row=2):
  sh.row_dimensions[row[0].row].height=58
  for c in row:
   c.font=Font(name='Calibri',size=10);c.alignment=Alignment(wrap_text=True,vertical='top')
   if c.row%2==0:c.fill=PatternFill('solid',fgColor='F0F5F8')
   if isinstance(c.value,(int,float)) and 'EUR' in str(sh.cell(1,c.column).value):c.number_format='#,##0.00;[Red]-#,##0.00'
   if isinstance(c.value,str) and (R/c.value).is_file():c.hyperlink=(R/c.value).as_uri();c.font=Font(color='0563C1',underline='single',size=10)
 for i,k in enumerate(headers,1):
  width=15
  if any(s in k.lower() for s in ['observ','sursa','document local','corect','initial','copie','text_banca','descriere','valoare']):width=48
  elif any(s in k.lower() for s in ['statut','furnizor','factura','perioada','referinta','email']):width=28
  sh.column_dimensions[sh.cell(1,i).column_letter].width=width
 sh.sheet_view.zoomScale=80
 if name=='Citeste intai':
  sh.column_dimensions['A'].width=46;sh.column_dimensions['B'].width=110
 for row in sh.iter_rows(min_row=2):
  lines=max((len(str(c.value or ''))//max(10,int(sh.column_dimensions[c.column_letter].width)-2)+1 for c in row),default=1)
  sh.row_dimensions[row[0].row].height=max(32,min(200,lines*14+8))
 return sh

def build(path,brief=False,services=False):
 wb=Workbook();wb.remove(wb.active)
 sheet(wb,'Citeste intai',overview,['Camp','Valoare'])
 if brief:
  sheet(wb,'Fara plata identificata',[x for x in invoices if x['Statut']=='FARA PLATA IDENTIFICATA'])
  sheet(wb,'Clarificari inainte de plata',[x for x in invoices if x['ID'] not in ['F016','F017','F018'] and not x['Statut'].startswith('ACHITAT')])
  sheet(wb,'Deja achitate',[x for x in invoices if x['Statut'].startswith('ACHITAT')])
 else:
  sh=sheet(wb,'Registru documente',invoices)
  for n,x in enumerate(invoices,2):sh.cell(n,11,f'=ROUND(F{n}+G{n}-H{n}-I{n}-J{n},2)')
  sheet(wb,'Plati banca',tx)
  sheet(wb,'Legaturi plata-factura',alloc)
  sheet(wb,'Personal pentru firma',[a for a in alloc if a['Cont']=='Cosmin AT13'])
  sheet(wb,'Fara factura sau alt document',[t for t in tx if not t.get('factura_id')])
  sheet(wb,'Control extrase',[{'Cont':c['cont'],'Tranzactii':c['tranzactii'],'Credit PDF EUR':float(c['pdf']['credit']),'Credit calculat EUR':float(c['calculat']['credit']),'Debit PDF EUR':float(c['pdf']['debit']),'Debit calculat EUR':float(c['calculat']['debit']),'Coincid':c['egal']} for c in checks]+[{'Cont':'A&C dovada separata','Tranzactii':1,'Debit calculat EUR':-640.06,'Coincid':'In afara totalului PDF; nu este duplicat'}])
 sheet(wb,'Corectii fata de vechi',corrections,['Registru istoric','Foaie/celula','Initial','Corectat','Legatura'])
 sheet(wb,'Surse',sources)
 path.parent.mkdir(exist_ok=True);wb.save(path)
 # Cache numeric pentru formula simpla a soldului, astfel incat rezultatul sa fie vizibil si in cititoare fara Excel.
 if not brief:
  ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
  with zipfile.ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
  xml=ET.fromstring(parts['xl/worksheets/sheet2.xml'])
  for n,x in enumerate(invoices,2):
   c=xml.find(f'.//m:c[@r="K{n}"]',ns);v=c.find('m:v',ns)
   if v is None:v=ET.SubElement(c,'{'+ns['m']+'}v')
   v.text=str(x['Sold document EUR'])
  parts['xl/worksheets/sheet2.xml']=ET.tostring(xml,encoding='utf-8',xml_declaration=True)
  with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
   for n,b in parts.items():z.writestr(n,b)
 return path

master=build(F/(DATE+' Reconciliere completa facturi si plati.xlsx'))
payables=build(R/'08. Corespondenta'/(DATE+' De platit - Schallergasse 35 - verificat.xlsx'),brief=True)
services=build(F/(DATE+' Servicii si facturi - situatie verificata.xlsx'),brief=True)
(A/(DATE+' Registru verificat.json')).write_text(json.dumps({'data':DATE,'documente':invoices,'plati':tx,'alocari':alloc,'corectii':corrections,'controale':checks,'surse':sources},ensure_ascii=False,indent=2),encoding='utf-8')

paras=[('2026.09.30 | Verificarea facturilor si platilor',1),('Schallergasse 35 • A&C Wohnart Immobilien GmbH • Situatie bazata pe documentele disponibile',0)]
paras += [('Concluzie',2),('Excelurile anterioare nu sunt complet corecte. Platile celor doua conturi sunt acum inregistrate individual si legate de facturi sau de documentul bancar corespunzator. Sunt 62 de miscari reconciliate:61 in extrasele generale si plata separata Attensam de640,06EUR. Totalurile coincid la cent cu extrasele.',0)]
paras += [('Facturi deja platite care nu trebuie achitate din nou',2),('Attensam34642:640,06EUR platit la2026.09.28 +13,06EUR Skonto, sold zero. Attensam34648:156,53EUR platit personal la2026.09.09, dar furnizorul trebuie sa confirme alocarea. MA6Q2:93,23EUR platit la2026.07.27; cele doua referinte din Excelul vechi descriu aceeasi obligatie. MA37:39EUR platit la2026.09.28.',0)]
paras += [('Plati personale pentru obligatii asociate firmei',2),('Total1538,12EUR: notar933; MA6 93,23; ARTUS240; STURM115,36; Attensam156,53. Nu s-a identificat rambursarea lor catre Cosmin. Pentru facturile cu datele fostului proprietar, contabilul trebuie sa confirme atribuirea; plata bancara este certa.',0)]
paras += [('Documente fara plata identificata',2),(f'CERHA HN26/30363:2640,22EUR, scadenta2026.05.05; ARTUS1264971:144EUR; MA6Q3:93,23EUR. Total{confirmed}EUR. Aceasta lista nu include sumele contestate, estimate sau ordinele in asteptare. Verificati eventualele debite de dupa2026.09.28 inainte de plata.',0)]
paras += [('Ce a scapat sau a fost clasificat gresit',2)]
for _,_,old,new,ids in corrections:paras.append((old+' → '+new+' ['+ids+']',0))
paras += [('Puncte ramase pentru confirmare documentara',2),('Attensam: alocarea34648, storno/reemitere6253/25777 si perioada/storno14983. MA6: soldQ3 si inchiderea contului vechi de apa. Apa noua: factura310910909051,15,18EUR, scadenta2026.10.15; ordin anuntat2026.09.30, debit neconfirmat. STURM:1.817,73EUR curent si883,98EUR gaz fara debit si credit846,92EUR pe contul vechi, fara compensare confirmata. WienEnergie109,02EUR: repartizare intre proprietari.',0),('ARTUS/FinanzOnline: PDF fiscal criptat, sold93EUR si IBAN de reconfirmat. Donau:3734,34EUR contestat/documente cerute; Q4 1591,81EUR este estimare, iar PDF-ul numitQ4 este somatia din iunie. E3/KSV879,34EUR: creanta contestata, demersurile extrajudiciare oprite, fara anulare dovedita. Amenzi Burgenland250/55EUR: platite, deciziile lipsesc.',0),('CERHA: pentru75900EUR taxe si1650000EUR pret de cumparare exista debitele si contractul; sunt necesare decontul final Treuhand si documentele taxelor efectiv virate. Transferurile personale spre firma de1834000EUR sunt finantare, nu cheltuieli de furnizori.',0)]
paras += [('Limite si utilizare',2),('Constituire la2025.12.03; inregistrare Firmenbuch la2026.01.08. Au fost pastrate toate operatiunile din2025, inclusiv cele anterioare firmei. Extrasele generale se opresc la2026.09.28 14:33/14:34. Nu exista extras complet pentru2026.09.29–30, extrase ale altor conturi sau confirmari actuale de sold de la toti furnizorii. Un debit dovedeste plata initiata si inregistrata la banca platitorului; alocarea la creditor poate necesita confirmare.',0),('Coloanele Nr plata bancar si Referinta plata sunt distincte. ID-urileAT22-xxx/AT13-xxx sunt create pentru legaturi in registru si nu sunt numere bancare. Originalele si Excelurile istorice sunt pastrate. Nu au fost trimise emailuri si nu au fost initiate plati.',0)]
# Spatiere lizibila pentru numerele compuse din paragrafele rezumative.
def human(t):
 t=re.sub(r'(?<=[A-Za-zĂÂÎȘȚăâîșț])(?=\d)|(?<=\d)(?=[A-Za-zĂÂÎȘȚăâîșț])',' ',t)
 t=re.sub(r'\b(MA|AT|F|Q|E) (\d)',r'\1\2',t)
 t=re.sub(r'([:;])(?=\S)',r'\1 ',t)
 t=t.replace('soldQ3','sold Q3').replace('numitQ4','numit Q4').replace('ID-urileAT','ID-urile AT').replace('WienEnergie','Wien Energie').replace('2877.45','2.877,45')
 return t
paras=[(human(t),h) for t,h in paras]
txt='\n\n'.join(t for t,h in paras);(A/(DATE+' Concluzii verificare facturi si plati.txt')).write_text(txt,encoding='utf-8-sig')
doc=Document();doc.styles['Normal'].font.name='Calibri';doc.styles['Normal'].font.size=Pt(10)
for t,h in paras:
 if h:doc.add_heading(t,h-1)
 else:doc.add_paragraph(t)
doc.save(A/(DATE+' Concluzii verificare facturi si plati.docx'))
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyRO',fontName='Arial',fontSize=9,leading=13,spaceAfter=7));styles.add(ParagraphStyle(name='HeadRO',fontName='ArialBold',fontSize=12,leading=16,spaceBefore=9,spaceAfter=7));styles.add(ParagraphStyle(name='TitleRO',fontName='ArialBold',fontSize=18,leading=23,spaceAfter=14))
story=[Paragraph(escape(t),styles['TitleRO' if h==1 else 'HeadRO' if h else 'BodyRO']) for t,h in paras]
def footer(canvas,doc):canvas.setFont('Arial',8);canvas.drawString(38,22,DATE+' • Schallergasse35 • Verificare documentara');canvas.drawRightString(557,22,str(doc.page))
SimpleDocTemplate(str(A/(DATE+' Concluzii verificare facturi si plati.pdf')),leftMargin=38,rightMargin=38,topMargin=38,bottomMargin=38).build(story,onFirstPage=footer,onLaterPages=footer)
# QA: surse si totaluri disponibile in fisier separat.
qa={'tranzactii':len(tx),'documente':len(invoices),'alocari':len(alloc),'personal_pentru_firma':str(personal),'documentate_fara_debit':str(confirmed),'documente_fara_fisier':[x['ID'] for x in invoices if not x['Document local']],'toate_totalurile_extraselor_coincid':all(c['egal'] for c in checks),'surse_lipsa':[s for s in sources if not (R/s['Copie audit']).exists()]}
check=load_workbook(master,data_only=True);qa['sold_skonto_cache']=check['Registru documente']['K15'].value;assert qa['sold_skonto_cache']==0
(A/(DATE+' Control calitate.json')).write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(qa,ensure_ascii=False))
