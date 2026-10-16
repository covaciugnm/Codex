import json, pathlib, hashlib, re
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
work=pathlib.Path(__file__).parent
root=pathlib.Path(r'Z:\00. Proiecte 2025\AFIR FotoVoltaic 1\50. Fabrica Nuci\nuttechnology.com')
emails=json.loads((work/'emails.json').read_text(encoding='utf-8'))
dl=json.loads((work/'downloads.json').read_text(encoding='utf-8'))
chats=json.loads((work/'chats.json').read_text(encoding='utf-8'))
pdfs=json.loads((work/'pdfs.json').read_text(encoding='utf-8'))
existing=json.loads((work/'existing.json').read_text(encoding='utf-8'))
# Consolidation retains source PDFs unchanged and deduplicates by SHA-256 only.
unique=[]; seen={}
for d in sorted(pdfs,key=lambda d:(0 if '02_Oferte' in d['path'] else 1 if '03_Cataloage' in d['path'] else 2 if 'Brosuri' in d['path'] else 3,d['path'])):
 if d['hash'] not in seen: seen[d['hash']]=d;unique.append(d)
# Consolidated PDF cover and index.
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold',r'C:\Windows\Fonts\arialbd.ttf'))
indexfile=work/'index.pdf'
index_pages=1+(len(unique)+11)//12
offset=index_pages
for d in unique: d['start']=offset+1;offset+=len(d['pages'])
c=canvas.Canvas(str(indexfile),pagesize=(595,842))
c.setFont('ArialBold',20);c.drawString(42,780,'Fabrica de nuci')
c.setFont('ArialBold',16);c.drawString(42,748,'Dosar tehnic consolidat')
c.setFont('Arial',11)
notes=['Nut Technology / TEHNO MSS - CESIRO PRODUCTION','Documente disponibile la 16.10.2026','',
'Include ofertele, cataloagele, broșurile și fișele electrice propuse.',
'Originalele sunt păstrate separat. Documentele identice apar o singură dată.',
'Fișele electrice CESIRO sunt propuneri de validat de furnizor.',
'Imaginile 3S și M600 rămân în folder; nu înlocuiesc o fișă tehnică.',
'Nu a fost identificată o broșură tehnică separată pentru M600.',
'',
'Oferta 179/11.10.2026: total declarat 320.400 EUR fără TVA.',
'Suma valorilor de rând declarate: 320.400 EUR.',
'Suma preț unitar × cantitate: 314.400 EUR.',
'Poziția 7: 44.900 × 2 = 89.800 EUR, dar sunt înscriși 95.800 EUR.',
'Diferența de 6.000 EUR necesită clarificarea furnizorului.',
'Panourile de comandă sunt excluse conform emailului din 11.10.2026.',
'',
'Parametrii tehnici din documente sunt declarațiile surselor.',
'Neconcordanțele și datele lipsă sunt semnalate în Excel.']
y=710
for s in notes:
 for line in simpleSplit(s,'Arial',11,510):c.drawString(42,y,line);y-=19
c.showPage()
for start in range(0,len(unique),12):
 c.setFont('ArialBold',16);c.drawString(42,790,'Cuprins - documente originale')
 y=750
 for d in unique[start:start+12]:
  name=pathlib.Path(d['path']).name
  name=re.sub(r'^[0-9a-f]{8}_','',name)
  lines=simpleSplit(name,'Arial',9,450)
  c.setFont('Arial',9)
  for line in lines[:3]:c.drawString(42,y,line);y-=12
  c.drawRightString(554,y+12,str(d['start']))
  y-=15
 c.showPage()
c.save()
writer=PdfWriter();writer.append(str(indexfile))
for d in unique:writer.append(str(root/d['path']),outline_item=pathlib.Path(d['path']).stem,import_outline=False)
out=root/'08_Dosar_tehnic'/'Dosar_tehnic_complet_2026-10-16.pdf'
writer.write(str(out))
assert len(PdfReader(out).pages)==offset
for d in pdfs:d['start']=seen[d['hash']]['start']
# Communications with localized timestamps, full originals linked separately.
summ={
'5f73380d':'Ofertă 179; recomandă două linii 200 kg/h, a treia ulterior. NERI/MOTOVARIO, inox; panouri excluse. Promite lista motoarelor marți.',
'406df854':'Solicitare configurație 500 kg/h cu trei spărgătoare, automatizare RevPi/Schneider și M600; cere validare tehnică.',
'4af3a062':'Transmitere internă a contactului Tudor: 0755 781 425.',
'917fe888':'Transmitere internă ofertă 82/16.04.2026, varianta 200 kg/h.',
'e67bc9dd':'Transmitere internă ofertă 82/16.04.2026, fișier denumit 400 kg/h.',
'3cbc4897':'Tudor retransmite oferta 82/16.04.2026, varianta 200 kg/h.',
'1999f7b9':'Tudor retransmite oferta 82/16.04.2026, fișier denumit 400 kg/h.'}
comm=[]
def localdate(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Bucharest')).replace(tzinfo=None).isoformat()
for e in emails:
 comm.append([localdate(e['received_at']),'Email','Trimis' if e['is_sent'] else 'Primit',e['from_address'],', '.join(e['to']),e['subject'],summ[e['id'][:8]],len(e['attachments']),e['local'],e['id'],e['account_email'],', '.join(e.get('cc',[]))])
for ch in chats:
 for m in ch['items']:
  comm.append([localdate(m['timestamp']),'WhatsApp','Trimis' if m['is_from_me'] else 'Primit',m['sender'],ch['chat']['name'],m['type'],m['text'],len(m['attachments']),'01_Comunicatii/WhatsApp_export.json',m['id'],m['wa_account'],''])
comm.sort(key=lambda r:r[0])
# Each attachment occurrence remains traceable even if the binary is identical.
attach=[]
for d in dl:
 attach.append([d['date'][:10],d['filename'],d['email_id'],d['id'],d['size'],d['local'],hashlib.sha256((root/d['local']).read_bytes()).hexdigest()])
attach.append(['2026-09-22','Customer request.docx','94c65b55-f8d7-405c-8c10-8aafe4d78461','6feb3d0f-f02f-436d-8437-62f6e811a1da',16745,'05_Documente_interne/Customer request.docx','Copie locală existentă, dimensiune concordantă'])
offer=next(d for d in pdfs if '82ab706d' in d['path'])
old200=next(d for d in pdfs if '6d433786' in d['path'])
old400=next(d for d in pdfs if '39b20753' in d['path'])
names=['Mașină industrială de curățat și spălat nucile 1 t/h','Uscător nuci, alune, migdale 4 tone/zi','Elevator Noria 4 tone/oră','Mașină de sortat nuci goale în coajă','Calibrator rotativ nuci 8 fracții','Mașină de îndepărtat coji verzi de alune','Linie completă 200 kg/h combinată (nuci, alune, migdale)','Separator cromatic 3S','Masă de inspecție cu bandă']
units=[34000,22400,9800,8500,21200,4800,44900,56000,7900];qty=[1,2,1,2,2,1,2,1,2];amount=[34000,44800,9800,17000,42400,4800,95800,56000,15800]
caps=['1 t/h','4 t/24 h','4 t/h în tabel; 2 t/h în descriere','300 kg/h; denumire neconcordantă la p. 5','500 kg/h','până la 300 kg/h','200 kg/h per linie','4 t/h, de confirmat pentru nuci','Bandă 4 m']
powers=[3.7,14,None,4.5,2.95,2.2,None,2,0.55]
pg=[1,4,3,5,6,7,8,15,16]
notes=['220 V declarat; specificație electrică de confirmat','14 kW declarat; bilanț termic și putere încălzire de confirmat','Capacitate și putere de confirmat','Descriere SKU 20 / separare miez 100 kg/h; dimensiuni suspecte','2 bucăți ofertate, 1 solicitată','Opțiune inclusă în oferta de bază','Total rând diferă cu 6.000 EUR; două linii 200 kg/h ofertate','Origine motor Polonia în PDF vs motoare italiene în email','2 mese simple ofertate; cerută una pe două niveluri; dimensiuni de confirmat']
latest=[[i+1,n,qty[i],units[i],amount[i],None,None,caps[i],powers[i],notes[i],offer['path'],pg[i]] for i,n in enumerate(names)]
old=[]
for label,d,ns,ps,qs in [
 ('82 / 200 kg-h',old200,['Curățare nuci verzi 500 kg/h','Uscător 2 tone/zi','Elevator Noria 2 t/h','Calibrator 4 fracții (2 buc.)','Îndepărtare coji verzi alune','Linie combinată 200 kg/h'],[8000,16000,6700,17200,4300,32900],[1,1,1,2,1,1]),
 ('82 / 400 kg-h (titlu fișier)',old400,[names[0],names[1],names[2],'Calibrator 4 fracții (2 buc.)',names[5],'Linie completă nuci 200 kg/h','Linie combinată 200 kg/h - alternativă'],[29000,19200,8600,17200,4300,28600,32900],[1,1,1,2,1,1,1])]:
 for i,n in enumerate(ns):old.append([label,'2026-04-16',n,qs[i],ps[i],ps[i]/qs[i],'Preț unitar derivat din lot' if qs[i]==2 else 'Preț din tabel; 1 buc. presupusă',d['path'],1])
catalog=[]
for r in existing['Echipamente'][4:]:
 if not isinstance(r[0],(int,float)):continue
 path=(r[18] or '').replace('\\\\','\\')
 rel=path.split('nuttechnology.com\\')[-1] if path else ''
 match=next((d for d in pdfs if d['path']==rel),None)
 catalog.append([r[0],r[1],r[2],r[4],r[10],r[11],r[12],r[13],rel,match['start'] if match else None,'Broșură în dosar' if match else 'Imagine / fișă PDF lipsă',r[19],r[15]])
index=[[d['path'],len(d['pages']),d['start'],d['hash'],'Propunere CESIRO - de validat' if '04_Fise' in d['path'] else 'Document furnizor / broșură existentă'] for d in pdfs]
actions=[
['Total ofertă','Poziția 7: 44.900 × 2 = 89.800, dar totalul de rând este 95.800 EUR.','Confirmare preț unitar sau total și emitere ofertă corectată.',offer['path']+' p. 1'],
['Configurație','Solicitare 500 kg/h cu 3 spărgătoare; ofertă două linii de 200 kg/h.','Confirmare configurație acceptată și debit garantat.',emails[0]['local']],
['Tablouri electrice','Excluse din preț potrivit emailului din 11.10.2026.','Buget separat pentru tablouri și automatizare.',emails[0]['local']],
['Lista motoarelor','Promisă marți, 13.10.2026, în emailul din 11.10.2026.','Nu am găsit răspunsul cu lista în comunicările disponibile.',emails[0]['local']],
['Noria','4 t/h în tabel; 2 t/h în descriere.','Clarificare capacitate, putere și schiță.',offer['path']+' p. 1, 3'],
['Sortare nuci goale','Titlu mașină nuci goale; descriere separator miez 100 kg/h și debit 300 kg/h.','Confirmare model, dimensiuni, debit.',offer['path']+' p. 5'],
['Sortare optică','3S ofertat, M600 cerut. Pentru M600 există numai imagine locală și fișă electrică propusă.','Broșură M600, preț și protocol de comunicație.',offer['path']+' p. 15-16'],
['Motoare','Email: toate italiene NERI/MOTOVARIO; 3S în PDF: motor Polonia.','Confirmare excepții și modele exacte.',offer['path']+' p. 16'],
['Garanție','Condiții generale 12 luni; unele poziții 24 luni.','Clarificare garanție per utilaj.',offer['path']+' p. 5, 16'],
['Livrare și montaj','Email include transport, montaj pe poziție și cabluri; descrierea Noria spune livrare exclusă.','Aliniere ofertă și condiții contractuale; termen de livrare.',emails[0]['local']],
['Uscător','14 kW menționat; lipsește bilanțul termic cerut.','Putere electrică totală, umiditate inițială, durată și consum pe șarjă.',offer['path']+' p. 4-5'],
['Echipamente locale','Buncăr, benzi și pâlnie apă uzată propuse pentru fabricație locală.','Dimensiuni, cantități și prețuri separate.',emails[0]['local']]
]
media=[[p.name,p.stat().st_size,str(p.relative_to(root)),'Fișier local; data din nume, fără mesaj WhatsApp recuperat'] for p in sorted((root/'06_Media').glob('*'))]
data={'comm':comm,'attachments':attach,'latest':latest,'old':old,'catalog':catalog,'index':index,'actions':actions,'media':media,'totalPages':offset,'uniquePdf':len(unique)}
(work/'data.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
(root/'00_CITESTE.txt').write_text('Organizare la 16.10.2026\n\n07_Centralizatoare: două Exceluri noi, cu surse și legături locale.\n08_Dosar_tehnic: PDF consolidat, cu cuprins și marcaje.\n01_Comunicatii: 7 emailuri exportate ca text/JSON și 5 mesaje WhatsApp.\n02_Oferte: oferte primite, păstrate distinct per atașament.\n03_Cataloage: cele 3 PDF-uri inițiale.\nBrosuri echipamente: structura inițială păstrată.\n04_Fise_electrice_propuse: 12 propuneri CESIRO, nevalidate de furnizor.\n05_Documente_interne: Excelul anterior, cererea, propunerea de automatizare, analizele și contactul.\n06_Media: 13 filmări copiate din TechnoMS.\n\nCăutare în toate căsuțele accesibile EVA după adresele Tudor/TehnoMS/Nut Technology și cuvinte asociate, plus WhatsApp după contact/telefon. Disponibilitatea depinde de istoricul sincronizat. Nu este o certificare că arhiva externă este completă. Apelul menționat la 11.10 nu are transcriere. Grupul Prelucrare Nuci este disponibil fără mesaje.\n\nDatele mesajelor din Excel sunt în ora României; exportul original păstrează UTC. Prețurile sunt istorice, în EUR fără TVA. Nu au fost actualizate de pe internet. Oferta 179 are diferență aritmetică de 6.000 EUR; vezi Excel. Ofertele 82 sunt istorice și necesită reconfirmare.\n\nDocumentele originale nu au fost editate. Cele 3 PDF-uri și Excelul inițial au fost mutate în subfoldere. Fișierele din TechnoMS au fost copiate, sursele au rămas acolo. Broșurile identice sunt deduplicate numai în PDF-ul consolidat; toate căile originale apar în index.\n',encoding='utf-8')
print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in data.items()}))

