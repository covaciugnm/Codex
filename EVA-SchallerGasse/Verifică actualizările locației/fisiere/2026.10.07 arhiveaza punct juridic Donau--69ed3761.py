from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from email.message import EmailMessage
from email.policy import SMTP
from email.utils import format_datetime
import json,hashlib,shutil,fitz
R=Path(__file__).resolve().parent.parent;D='2026.10.07'
P=R/'08. Corespondenta'/f'{D} Cerere reziliere Donau 2027';B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
d=json.loads((P/f'{D} DRAFT Eva-Mail.json').read_text(encoding='utf-8'))
assert d['status']=='pending' and d['id']=='aa653a96-7eee-4133-a41d-5892ea79788d'
def rel(p):return p.relative_to(R).as_posix()
def txt(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8-sig')
def js(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def backup(p):
 if p.exists():
  dest=P/f'{D} Istoric inainte de cerere'/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():shutil.copy2(p,dest)
index={x['cale']:x for x in json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))}
audit=[]
files=['05. Asigurari/Asigurare cladire/814BC40FC7831FE197E21FDA1089ECC3_Polizzenkopie.pdf','05. Asigurari/Asigurare cladire/Schalle_1080_DON_SHU_2044001194_2939905718.pdf','10. Banci + Extrase de cont/Facturi neachitate/02 - 2026-06-05 DONAU Polizze 2044001194 Praemie Quartal 1.591,81 EUR (Q4 faellig 01.10.2026) - IBAN AT67 2011 1403 1004 1414 Ref 002044001194.pdf']
for f in files:
 p=R/f;h=hashlib.sha256(p.read_bytes()).hexdigest();x=index[f];assert h==x['sha256']
 audit.append({'cale':f,'sha256':h,'hash_identic_index':True,'metadate_identice':p.stat().st_size==x['octeti'] and p.stat().st_mtime_ns==x.get('modificat_ns')})
with fitz.open(R/files[2]) as pdf:
 assert 'zwei Wochen' in pdf[0].get_text() and '39' in pdf[0].get_text()
m=EmailMessage(policy=SMTP)
for k,v in [('From',d['account_email']),('To',', '.join(d['to'])),('Cc',', '.join(d['cc'])),('Subject',d['subject']),('X-Unsent','1'),('X-Eva-Draft-ID',d['id']),('X-Archive-Export','Draft from EVA; reconstructed EML')]:m[k]=v
m['Date']=format_datetime(datetime.fromisoformat(d['created_at'].replace('Z','+00:00')));m.set_content(d['body'])
(P/f'{D} DRAFT Cerere reziliere Donau.eml').write_bytes(m.as_bytes())
created=datetime.fromisoformat(d['created_at'].replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Bucharest'))
header=f"{D} | DRAFT NETRIMIS\nCreat: {created.strftime('%Y.%m.%d %H:%M:%S')} Romania\nData tehnica: {d['created_at']}\nExpeditor: {d['account_email']}\nDestinatari: {', '.join(d['to'])}\nCC: {', '.join(d['cc'])}\nSubiect: {d['subject']}\nID Eva-Mail: {d['id']}\nAtasamente: niciunul\nSursa: draft verificat in Eva-Mail; nu exista dovada trimiterii.\n\n"
txt(P/f'{D} DRAFT Cerere reziliere Donau.txt',header+d['body'])
status='2026.10.07: punct de vedere juridic documentar finalizat si draft german NETRIMIS in Eva-Mail. Cere incetare prin acord la 2027.01.01, alternativ 2027.01.08; subsidiar primul termen legal/contractual admis, pastrand notificarea din 2026.10.01. Cere deconturi separate, justificarea duratei 2036, renuntarea la prima suplimentara 1000K, dovada somatiei si suma/data exacta pentru restabilirea acoperirii. Raspuns cerut pana la 2026.10.09, 12:00 Viena /13:00 Romania. Nicio incetare, plata, acoperire sau suspendare Inkasso confirmata.'
nxt='Trimiterea ciornei din Eva-Mail, verificarea dovezii si a raspunsului; control cu Capra al dreptului de incetare, clauzei 1000K si conditiilor acoperirii/platii. Termenul Commerz 2026.10.12 ramane distinct. Nu se presupune ca trei luni permit singure incetarea contractului cu expirare 2036.'
last='Ultimul raspuns primit: 2026.10.06, Cornelia Loschy, ID 2c273256-a0bf-408b-bb22-09718372e888; refuza rezilierea si declara lipsa acoperirii pentru prime restante.'
source=rel(P/f'{D} DRAFT Cerere reziliere Donau.txt')
note=f"{D} | CERERE REZILIERE LA 2027.01.01 /2027.01.08 SI PUNCT JURIDIC\n\nStatus scurt: {status}\n{last}\nUrmatorul pas: {nxt}\nSursa: {source}\nPunct juridic: {rel(P/f'{D} Punct de vedere juridic Donau.txt')}\nID draft Eva-Mail: {d['id']}\nCatre: {', '.join(d['to'])}\nCC: {', '.join(d['cc'])}; Capra nu este in CC.\n\n"
for p in [R/f'{D} Status proiect.txt',R/f'{D} Log progres proiect.txt']:
 backup(p);old=p.read_text(encoding='utf-8-sig');txt(p,note+'ISTORIC\n\n'+old)
for name in ['Donau Versicherung','Maritczak - Commerz Inkasso','CERHA HEMPEL']:
 p=B/'Parteneri'/f'{D} Log discutii - {name}.txt';backup(p);old=p.read_text(encoding='utf-8-sig')
 if name=='CERHA HEMPEL':prefix='Informare documentara locala; nu s-a trimis mesaj nou catre Capra.\n\n'
 else:prefix=''
 txt(p,prefix+note+'ISTORIC\n\n'+old)
regp=B/f'{D} Registru comunicatii.json';backup(regp);reg=json.loads(regp.read_text(encoding='utf-8'))
for st in reg['statusuri']:
 if st['partener'] in ['Donau Versicherung','Maritczak - Commerz Inkasso']:
  st['status']=status+' '+last;st['urmatorul_pas']=nxt;st['sursa_status']=[d['id'],source,'2c273256-a0bf-408b-bb22-09718372e888',rel(P/f'{D} Punct de vedere juridic Donau.txt')]
reg.setdefault('drafturi',[]).append({'data':D,'id':d['id'],'statut':'DRAFT NETRIMIS','cale':source,'expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'subiect':d['subject'],'note':'Data alternativa 2027.01.08 confirmata de utilizator; acest draft nu este email trimis.'})
reg.setdefault('actualizari_punctuale',[]).append({'data':D,'subiect':'Punct juridic si cerere reziliere Donau 2027','status':status,'sursa':source,'nota':'Un draft nou; acoperirea si numarul emailurilor primite/trimise nu se modifica.'})
js(regp,reg)
txt(P/f'{D} Jurnal actualizare.txt',note+'Trimiterea se face din Eva-Mail; instrumentul a salvat o ciorna si nu are functie de trimitere.\nConfirmare utilizator: alternativa corecta este 2027.01.08.\n')
js(P/f'{D} Audit surse si status.json',{'data':D,'polite_verificate':audit,'verificare_vizuala':['polita curenta p.1/7','polita istorica p.1/12, clauza 1000K'],'id_draft':d['id'],'statut':'NETRIMIS','creat_tehnic':d['created_at'],'surse_oficiale':['https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001979','https://www.ris.bka.gv.at/NormDokument.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001979&Paragraf=39','https://www.ris.bka.gv.at/eli/bgbl/1959/2/P69/NOR12026489','https://www.ris.bka.gv.at/eli/bgbl/1959/2/P70/NOR12037688','https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_19541117_OGH0002_0030OB00722_5400000_000/JJT_19541117_OGH0002_0030OB00722_5400000_000.pdf'],'data_consultarii':'2026.10.07','limita':'Punct juridic documentar; contract-cadru complet, comunicarea somatiilor si eventuale notificari istorice de verificat; nu confirma soldul sau restabilirea acoperirii.'})
read=R/'folder map/README.md';backup(read);t=read.read_text(encoding='utf-8')
head=f"# {D} — DONAU: punct juridic si draft reziliere 2027\n\nDosar curent: ../08. Corespondenta/{D} Cerere reziliere Donau 2027/. Incepe cu {D} Punct de vedere juridic Donau.txt si {D} Jurnal actualizare.txt. Draft EVA {d['id']}, NETRIMIS, catre Loschy/DONAU, CC Maritczak/Gruber, fara Capra. Incetare propusa 2027.01.01, alternativ 2027.01.08 confirmat de utilizator; subsidiar primul termen admis. Solicita doua deconturi, suma/data pentru restabilirea acoperirii, dovezi §39 si renuntare la prima suplimentara 1000K. Preavizul de 3 luni nu garanteaza incetarea politei care indica 2036.01.01. Primele nu dispar automat din lipsa acoperirii. Jurnalele TXT/JSON actualizate, istoricul pastrat. Nu este mesaj trimis, acord acceptat sau plata efectuata. Termenul Commerz 2026.10.12 ramane distinct.\n\n"
read.write_text(head+t,encoding='utf-8')
assert reg['acoperire']['mesaje_salvate']==795 and 'X-Unsent: 1' in (P/f'{D} DRAFT Cerere reziliere Donau.eml').read_text(encoding='utf-8')
print('Punct juridic, draft TXT/JSON/EML, jurnale si surse salvate; 795 mesaje; draft NETRIMIS.')

