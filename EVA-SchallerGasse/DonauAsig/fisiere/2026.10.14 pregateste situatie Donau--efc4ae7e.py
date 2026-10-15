from pathlib import Path
import json,hashlib,shutil,re,html
from datetime import datetime
from zoneinfo import ZoneInfo
from email.message import EmailMessage
from email.policy import SMTP
from email.utils import format_datetime
from pypdf import PdfReader
R=Path(__file__).resolve().parent.parent
P=R/'05. Asigurari/Asigurare cladire/2026.10.14 Situatie Donau'
S=P/'Surse';A=P/'Anexe';A.mkdir(exist_ok=True)
B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
data=json.loads((S/'2026.10.14 Verificare Eva-Mail.json').read_text(encoding='utf-8'))
extra=json.loads((S/'2026.10.14 Completare istoric Eva-Mail.json').read_text(encoding='utf-8'))
emails=data['emails']+extra['emails']
idx={x['cale']:x for x in json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))}
ats={x['id']:x for x in json.loads((B/'2026.10.14 Registru atasamente.json').read_text(encoding='utf-8-sig'))}
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def txt(p,x):p.write_text(x,encoding='utf-8-sig')
summaries={
'd9216be2':'Cerem clarificarea restanței de 1.591,81 EUR + 10 EUR, contul de plată, situația acoperirii și actualizarea titularului. Mesaj adresat DONAU, Capra și Hofhans.',
'99a141bd':'Confirmare automată de primire a solicitării. Nu confirmă acoperirea sau soluționarea.',
'e683de9b':'DONAU solicită o împuternicire actuală a titularului poliței, semnată de reprezentantul autorizat al societății.',
'1e194934':'Indicăm office@ac-wohnart.at pentru corespondență și transmitem extrasul de carte funciară și hotărârea asociaților, prezentată în mesaj ca împuternicire.',
'1b869379':'Confirmare automată de primire a mesajului privind societatea și documentele.',
'4782ca5f':'Serviciul clienți confirmă trimiterea solicitării către departamentul competent.',
'78fa484e':'Notificăm schimbarea proprietarului. Cerem situația poliței, delimitarea datoriilor înainte/după 2026.04.01 și o soluție fără întreruperea acoperirii.',
'0f8353c0':'Confirmare automată de primire a cererii privind schimbarea proprietarului.',
'ba56aa79':'Serviciul clienți confirmă redirecționarea cererii către departamentul competent.',
'16a82de2':'Confirmă trecerea poliței pe A&C; cere plata pentru 2026.04.01–2026.10.01 până la 2026.06.18 și avertizează asupra pierderii acoperirii.',
'2dd29262':'Cerem acoperire minimă și reducerea primei din 2026.07.01; anunțăm plata după recalculare. Cerem alternativ examinarea încetării prin acord.',
'4b3dab07':'Notificare automată: o somație nouă este disponibilă în portalul Meine DONAU. Emailul nu conține documentul somației.',
'6706f86a':'Invocă transferul legal al contractului și expirarea dreptului de reziliere la schimbarea proprietarului. Declară lipsa acoperirii din cauza restanțelor.',
'd10bdd3f':'Pfeiffer ar putea elimina riscul de apă și pierderea chiriilor; cere autorizația, descrierea lucrărilor și confirmarea instalatorului. Reducerea nu este aprobată definitiv.',
'1bc16469':'Retransmite poziția din 2026.07.10 și confirmă că răspunsese cererii de reducere. Face referire și la o solicitare prin portal.',
'6b7b1131':'Capra transmite somația Commerz pentru 3.734,34 EUR, dosar 2616052, termen 2026.09.21.',
'b487e95f':'Cerem Maritczak documentele justificative, detalierea primelor și costurilor, clarificarea acoperirii și prelungirea termenului. Corectăm adresa de corespondență.',
'b8bab41b':'Capra precizează că polița fusese comunicată la 2026.03.19 și retransmite documentele. Nu este răspunsul creditorului la justificarea creanței.',
'41c4c52a':'Revenim la Maritczak, cu Capra în CC: documente până la 2026.10.07, termen de 14 zile după completare și suspendarea demersurilor/costurilor solicitate.',
'1fa19552':'Commerz spune că răspunsurile din 2026.09.17 nu s-au livrat și au fost trimise poștal. Cere 5.326,15 EUR, inclusiv Q4, cu termen 2026.10.12.',
'23eaa675':'Cerem încetare imediată prin acord și notificăm subsidiar încetarea la primul termen admis; cerem decont și status acoperire. CC efectiv: Maritczak/Gruber, fără Capra.',
'2c273256':'Refuză încetarea; indică 2036.01.01 cu preaviz de 3 luni. Declară că nu există acoperire pentru prime restante și că documentele pentru reducere încă lipsesc.'}
duplicates={'f9f87af8-c7ae-4790-b898-d7b75a63a61e':'78fa484e-d365-434a-946c-817ebf24a2b0','30da3512-03a0-4d68-b25b-a7c58ac482d8':'2dd29262-8d57-41c2-81e5-80e3b909d32e'}
manifest=[];saved={};rows=[];exports=[]
for e in sorted(emails,key=lambda x:x['received_at']):
 date=e['received_at'][:10].replace('-','.')
 typ='Email trimis' if e['is_sent'] else 'Email primit'
 docs=[];docbytes=[]
 for a in e.get('attachments',[]):
  if (a.get('content_type') or '').startswith('image/'):continue
  docs.append(a['name'])
  z=ats.get(a['id']);assert z and z.get('cale'),a
  original=R/z['cale'];raw=original.read_bytes();sha=hashlib.sha256(raw).hexdigest()
  assert sha==z['sha256'] and sha==idx[z['cale']]['sha256'] and len(raw)==a['size'],original
  if sha not in saved:
   clean=re.sub(r'[<>:"/\\|?*\r\n]','_',a['name'])
   target=A/(date+' '+a['id'][:8]+' '+clean)
   shutil.copy2(original,target);saved[sha]=target
  target=saved[sha]
  manifest.append({'email_id':e['id'],'attachment_id':a['id'],'nume_original':a['name'],'sha256':sha,'octeti':len(raw),'sursa':z['cale'],'cale':target.relative_to(R).as_posix()})
  if not any(x[0]==sha for x in docbytes):docbytes.append((sha,a,raw))
 stem=date+' '+('TRIMIS' if e['is_sent'] else 'PRIMIT')+' '+e['id'][:8]
 meta={'data_lizibila':date,'statut':typ,'sursa':'Eva-Mail, verificare 2026.10.14','limita':'Export API; EML reconstruit cu anexe documentare originale, fără imaginile inline; nu este MIME original integral.','email':e}
 js(S/(stem+'.json'),meta)
 header=f"{date} | {typ}\nID Eva-Mail: {e['id']}\nData tehnica: {e['received_at']}\nDe la: {e['from_address']}\nCatre: {', '.join(e.get('to',[]))}\nCC: {', '.join(e.get('cc',[]))}\nSubiect: {e['subject']}\nCorp trunchiat de API: {e.get('truncated',False)}\nAnexe: {', '.join(docs) or 'Fara anexe documentare'}\n\n"
 txt(S/(stem+'.txt'),header+e['text'])
 m=EmailMessage(policy=SMTP)
 for k,v in [('From',e['from_address']),('To',', '.join(e.get('to',[]))),('Cc',', '.join(e.get('cc',[]))),('Subject',e['subject']),('X-Eva-ID',e['id']),('X-Archive-Source','EVA API reconstruction')]:
  if v:m[k]=' '.join(v.splitlines())
 m['Date']=format_datetime(datetime.fromisoformat(e['received_at'].replace('Z','+00:00')))
 m.set_content(e['text'])
 for sha,a,raw in docbytes:
  content=a.get('content_type') or 'application/octet-stream';main,sub=content.split('/',1)
  m.add_attachment(raw,maintype=main,subtype=sub,filename=a['name'])
 (S/(stem+'.eml')).write_bytes(m.as_bytes())
 exports.append({'id':e['id'],'cale':(S/(stem+'.txt')).relative_to(R).as_posix(),'tip':typ})
 if e['id'] in duplicates:continue
 name='A&C / Cosmin Covaciu' if e['is_sent'] else (e.get('from_name') or e['from_address'])
 anex='\n'.join(dict.fromkeys(docs)) or ('Imagini de antet/semnătură; fără documente' if e.get('attachments') else 'Fără anexe')
 if e['id'].startswith('78fa484e'):anex='Nicio anexă în EVA; corpul menționează extrasul funciar și datele firmei.'
 if e['id'].startswith('1bc16469'):anex='PDF al cererii de reducere. Mesajul menționează și un al doilea atașament, absent din lista EVA.'
 rows.append({'data':date,'tip':typ,'de_la':name,'cuprins':summaries[e['id'][:8]],'anexe':anex,'id':e['id'],'sursa':(S/(stem+'.txt')).relative_to(R).as_posix()})
d=data['draft'];js(S/'2026.10.14 DRAFT verificat Eva-Mail.json',d)
txt(S/'2026.10.14 DRAFT NETRIMIS din 2026.10.07.txt',f"Verificat 2026.10.14 | DRAFT NETRIMIS\nID: {d['id']}\nCreat: {d['created_at']}\nActualizat in EVA: {d['updated_at']}\nDe la: {d['account_email']}\nCatre: {', '.join(d['to'])}\nCC: {', '.join(d['cc'])}\nSubiect: {d['subject']}\n\n"+d['body'])
conclusion='DONAU declară lipsa acoperirii pentru prime restante; contractul nu este confirmat încetat. Nu există o suspendare agreată a poliței sau a primelor.'
draftnote='Ciorna din 2026.10.07 este pending / NETRIMISĂ. Ultimul email trimis în dosarul verificat: 2026.10.01. Ultimul răspuns DONAU: 2026.10.06.'
summary='2026.10.14 — Situația DONAU, polița 2044001194, dosar Commerz 2616052\n\n'+conclusion+'\n\n'+draftnote+'\n\nDONAU scrie la 2026.10.06: „Bitte beachten Sie, dass aufgrund des aktuellen Prämienverzugs derzeit kein Versicherungsschutz besteht.” Nu am identificat ulterior o confirmare de restabilire a acoperirii, acceptare a rezilierii ori reducere aprobată. Aceasta este poziția comunicată de asigurător; verificarea nu stabilește judiciar validitatea refuzului de acoperire.\n\nDONAU refuză încetarea prin acord și cea ordinară la momentul solicitării și indică 2036.01.01, cu preaviz de 3 luni. Afirmația sa nu înlocuiește verificarea condițiilor complete și a drepturilor speciale.\n\nPentru reducere, Memoformat.pdf retransmite mesajul Pfeiffer din 2026.07.14: autorizația de construire, descrierea lucrărilor și confirmarea instalatorului privind închiderea/securizarea instalațiilor de apă. Nu este o aprobare a reducerii.\n\nUltima sumă solicitată de Commerz: 5.326,15 EUR, inclusiv prima Q4 de 1.591,81 EUR. Termenul 2026.10.12 a trecut. Nu s-a identificat o amânare sau suspendare a recuperării. Nu se afirmă că suma reprezintă soldul actual: nu s-a făcut reconciliere bancară și nu există un decont nou în mesajele verificate.\n\nCiorna din 2026.10.07 propune încetarea la 2027.01.01, alternativ 2027.01.08; cere deconturi și condițiile restabilirii acoperirii. Nu este răspuns trimis. Termenul solicitat în ciornă, 2026.10.09, este depășit; textul trebuie actualizat înainte de o eventuală trimitere.\n\nCC efectiv în mesajul trimis la 2026.10.01 și în răspunsul din 2026.10.06: office@maritczak.at și s.gruber@commerz-inkasso.at. Capra nu este în CC în aceste mesaje.\n\nDistincția juridică: §39 VersVG separă lipsa obligației de despăgubire pentru neplata primei de încetarea contractului. Aplicarea cere verificarea somației, termenului și comunicării. Sursa verificată 2026.10.14: https://www.ris.bka.gv.at/eli/bgbl/1959/2/P39/NOR12037674 . Analiza juridică detaliată existentă din 2026.10.07 rămâne reperul pentru aceste condiții.\n\nAcoperire: căutări după poliță, dosar, X712, DONAU, Commerz, Maritczak, Capra și Beendigung; fără pagini restante în rezultatele respective. Office sincronizat 2026.10.14 12:32:19 România; cosmin@ig.ro numai 2026.10.10 02:30:10. Celelalte căsuțe au sincronizări proprii; shared/team nesearchable nu sunt acoperite. Nu există dovadă de lipsă absolută a altor mesaje nesincronizate.\n\nTabelul acoperă comunicările relevante recuperate 2026.05.27–2026.10.06, inclusiv confirmările administrative și notificarea de portal. Codurile de autentificare și înregistrarea portalului sunt omise. Două copii ale trimiterilor din 2026.06.08 și 2026.07.01 sunt grupate o singură dată. Referirea la comunicarea din 2026.03.19 este afirmația Capra din 2026.09.17, nu un email din martie reconstituit.\n\nUrmătorul pas: clarificare scrisă urgentă cu DONAU a sumei, alocării și momentului restabilirii acoperirii și a datei de încetare. Actualizarea ciornei și decizia de trimitere sunt separate. Niciun mesaj nou nu a fost trimis în această verificare.\n'
txt(P/'2026.10.14 Situatie actuala Donau.txt',summary)
js(P/'2026.10.14 Cronologie Donau.json',{'data_verificare':'2026.10.14','concluzie':conclusion,'draft':draftnote,'randuri':rows})
js(S/'2026.10.14 Registru anexe verificate.json',manifest)
js(S/'2026.10.14 Registru mesaje exportate.json',exports)
js(S/'2026.10.14 Audit verificare.json',{'emailuri_ID':len(emails),'randuri_unice':len(rows),'copii_grupate':duplicates,'anexe_documentare_ID':len(manifest),'fisiere_unice':len(saved),'corpuri_trunchiate':[e['id'] for e in emails if e.get('truncated')],'draft_status':d['status'],'nicio_trimitere_efectuata':True,'anexe_verificate_hash_index':True})
# Open decisive originals, using existing extracts for unchanged supporting pages.
for item in manifest:
 if item['attachment_id'] in ['951d3284-2a63-4de1-9158-d2be11f06308','589967a1-945d-4cee-8e58-53d111190749','ad453388-c79d-4b5a-830b-6a9ab0509c4e']:
  pdf=PdfReader(R/item['cale'])
  text=pdf.pages[0].extract_text();assert text.strip()
  txt(S/('2026.10.14 Original verificat '+item['attachment_id'][:8]+'.txt'),text)
print(json.dumps({'mesaje':len(emails),'randuri':len(rows),'anexe_unice':len(saved),'dosar':str(P)},ensure_ascii=False))
