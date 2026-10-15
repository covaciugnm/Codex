from pathlib import Path
import json,hashlib,shutil,re
from email.message import EmailMessage
from email.policy import SMTP
root=Path(__file__).resolve().parent.parent
case=root/'05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau'
raw=case/'2026.10.14 Draft Eva-Mail Donau verificat bcbaad0d.json'
d=json.loads(raw.read_text(encoding='utf8'))
payload=json.loads((case/'2026.10.14 Cerere creare draft Eva-Mail Donau.json').read_text(encoding='utf8'))
normalize=lambda s:' '.join(s.split())
assert d['status']=='pending' and d['account_email']=='office@ac-wohnart.at'
assert d['to']==payload['to'] and d['cc']==payload['cc'] and not d.get('attachments')
assert normalize(d['body']).startswith(normalize(payload['body']))
assert normalize(d['body'])[len(normalize(payload['body'])):].strip()=='Cosmin Adrian Covaciu'
assert len(d['to'])==4 and len(d['cc'])==3
def preserve(p):
    target=case/'Istoric'/'2026.10.14 Inainte de reaudit si draft Eva-Mail'/p.relative_to(root)
    target.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and not target.exists():shutil.copy2(p,target)
stem='2026.10.14 Email polita anterioara si plata primelor NETRIMIS'
for ext in ['.txt','.json','.eml']:preserve(case/(stem+ext))
local={'data_lizibila':'2026.10.14','status':'draft Eva-Mail pending NETRIMIS','eva_mail_id':d['id'],'from':d['account_email'],'to':d['to'],'cc':d['cc'],'subject':d['subject'],'body':d['body'],'attachments':d.get('attachments',[]),'plata':'Declarată de utilizator:4.775,43EUR; încasare/alocare/acoperire neconfirmate','verification_status':'Reauditat și recitit din Eva-Mail; textul coincide cu cel auditat, cu semnătura configurată adăugată de Eva.'}
(case/(stem+'.json')).write_text(json.dumps(local,ensure_ascii=False,indent=2),encoding='utf8')
header='2026.10.14 | DRAFT EVA-MAIL NETRIMIS | ID '+d['id']+'\nDe la: '+d['account_email']+'\nCătre: '+'; '.join(d['to'])+'\nCC: '+'; '.join(d['cc'])+'\nSubiect: '+d['subject']+'\nAtașamente: niciunul\nPlată: declarată de utilizator; încasarea/alocarea nu sunt confirmate.\n\n'
(case/(stem+'.txt')).write_text(header+d['body'],encoding='utf-8-sig')
em=EmailMessage(policy=SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Cc']=', '.join(d['cc']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-Eva-Draft-ID']=d['id'];em.set_content(d['body'])
(case/(stem+'.eml')).write_bytes(em.as_bytes())
marker='2026.10.14 — DONAU: reaudit și draft creat în Eva-Mail, NETRIMIS'
status=('Email reauditat separat și creat în Eva-Mail pentru office@ac-wohnart.at; ID '+d['id']+'. Statut recitit: pending / NETRIMIS. '
        'Către cele patru adrese DONAU verificate: '+', '.join(d['to'])+'. CC: '+', '.join(d['cc'])+'. '
        'Corecții: alocarea plății celor trei prime se cere spre confirmare/agrement, fără presupunere de realocare retroactivă unilaterală; se cer temeiurile inițiale ori ulterioare ale expirării2036, inclusiv dacă exista deja în X712. '
        'Transferul păstrează durata rămasă; prelungirea anuală nu scurtează un termen fix valabil convenit. Plata4.775,43EUR rămâne declarația utilizatorului, fără încasare sau acoperire confirmată. Rezilierea2026.10.01 este menținută.')
next_step='Revizuirea și trimiterea din EVA → Drafts de către utilizator; apoi confirmarea încasării, alocării, acoperirii și primirea documentelor contractuale. Nu s-a trimis emailul prin această operațiune.'
source=(case/(stem+'.txt')).relative_to(root).as_posix()
note=marker+'\n\nStatus scurt: '+status+'\n\nUltimul răspuns DONAU verificat:2026.10.06. Observație nouă de status: cererea către Capra cu subiect datat2026.10.07 apare în Eva cu status sent și updated_at2026-10-13T17:15:27.357911Z; nu confundăm acel mesaj cu noul draft către DONAU. Sursa statusului este salvată în Surse.\n\nUrmătorul pas: '+next_step+'\n\nSursă: '+source+'; 2026.10.14 Reaudit final email Eva-Mail Donau.txt; răspunsul eva_get_draft arhivat în JSON.\n\n'
def prepend(p,prefix=''):
    old=p.read_text(encoding='utf-8-sig') if p.exists() else ''
    if marker in old:return
    preserve(p);p.write_text(prefix+note+'ISTORIC PĂSTRAT\n\n'+old,encoding='utf-8-sig')
for name in ['2026.10.14 Status proiect.txt','2026.10.14 Log progres proiect.txt']:prepend(root/name)
arc=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
for partner in ['Donau Versicherung','Maritczak - Commerz Inkasso','CERHA HEMPEL']:prepend(arc/'Parteneri'/f'2026.10.14 Log discutii - {partner}.txt')
prepend(root/'folder map/README.md','# ')
prepend(case/'2026.10.14 Jurnal actualizare.txt')
prepend(root/'05. Asigurari/Asigurare cladire/2026.10.14 Situatie Donau/2026.10.14 Situatie actuala Donau.txt')
rp=arc/'2026.10.14 Registru comunicatii.json';preserve(rp);reg=json.loads(rp.read_text(encoding='utf-8-sig'))
record={'data':'2026.10.14','subiect':marker,'status':status,'urmatorul_pas':next_step,'surse':[source,raw.relative_to(root).as_posix()],'eva_mail_draft_id':d['id'],'draft_status':'pending','email_trimis':False,'plata_declarata_utilizator':4775.43,'incasare_confirmata':False}
if not any(x.get('subiect')==marker for x in reg.setdefault('actualizari_punctuale',[])):reg['actualizari_punctuale'].append(record)
for entry in reg.get('statusuri',[]):
    if entry.get('partener')=='Donau Versicherung':entry['draft_eva_mail_reauditat_2026_10_14']=record
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf8')
files=[case/(stem+ext) for ext in ['.txt','.json','.eml']]+[raw,case/'2026.10.14 Text reauditat pentru draft Eva-Mail Donau.txt',case/'2026.10.14 Reaudit final email Eva-Mail Donau.txt']
manifest={'data':'2026.10.14','eva_mail_id':d['id'],'status':'pending / NETRIMIS','verified_body':'Identic după normalizarea spațiilor, plus semnătura configurată Cosmin Adrian Covaciu','files':[{'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(case/'2026.10.14 Manifest draft Eva-Mail Donau.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'draft':d['id'],'status':d['status'],'to':d['to'],'cc':d['cc'],'body_check':'passed','archive':'updated'},ensure_ascii=False))
