from pathlib import Path
import json,hashlib,shutil
from email.message import EmailMessage
from email.policy import SMTP
root=Path(__file__).resolve().parent.parent
case=root/'05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau'
stem='2026.10.14 Email polita anterioara si plata primelor NETRIMIS'
p=case/(stem+'.json')
d=json.loads(p.read_text(encoding='utf-8-sig'))
d['body']=(case/(stem+'.txt')).read_text(encoding='utf-8-sig').split('\n\n',1)[1]
d['verification_status']='Auditat integral; paragraful cumpărării corectat conform recomandării auditorului. NETRIMIS.'
bundle=json.loads((case/'Surse/2026.10.14 Reverificare corespondenta pentru email polita si plata.json').read_text(encoding='utf8'))
d['source_email_ids']=[x['id'] for x in bundle['emails']]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
em=EmailMessage(policy=SMTP)
em['From']=d['from'];em['To']=', '.join(d['to']);em['Cc']=', '.join(d['cc']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-Archive-Status']='LOCAL DRAFT - NOT SENT'
em.set_content(d['body'])
(case/(stem+'.eml')).write_bytes(em.as_bytes())
assert 3*159181==477543
assert 'allgemeine Hinweise auf bestehende Versicherungen' in d['body']
marker='2026.10.14 — DONAU: plată declarată de utilizator; email documente NETRIMIS'
status=('Utilizatorul declară achitarea celor trei rate până la 2027.01.01, totalul aferent primelor fiind 4.775,43 EUR. '
        'Nu există în această actualizare un ordin de plată verificat sau confirmare de încasare/alocare; nu se marchează debitul stins ori acoperirea restabilită. '
        'Draftul anunță transferul declarat, cere confirmarea încasării/alocării/acoperirii și documentele privind X712 și expirarea2036. '
        'Contractul de cumpărare menționează asigurarea existentă și termenul de reziliere; draftul nu neagă aceste clauze. '
        'Capra a transmis polița la2026.03.19; DONAU a invocat§69 la2026.07.10, iar corespondența Commerz invocă§39. Lipsește justificarea completă specifică duratei2036.')
next_step='Revizuirea și eventuala trimitere a draftului, apoi confirmarea bancară/DONAU a plății și obținerea documentelor contractuale. Nu s-a trimis niciun email nou.'
source=(case/(stem+'.txt')).relative_to(root).as_posix()
note=marker+'\n\nStatus scurt: '+status+'\n\nUltimul răspuns verificat: DONAU2026.10.06, ID2c273256-a0bf-408b-bb22-09718372e888. Ultima informație: declarația utilizatorului despre plată,2026.10.14.\n\nUrmătorul pas: '+next_step+'\n\nSursă: '+source+'; Surse/2026.10.14 Reverificare corespondenta pentru email polita si plata.json; contractul semnat, art.4.5,7.1(i),10.5.\nID Eva-Mail draft: nu există; draft local TXT/JSON/EML, fără atașamente.\n\n'
archive=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
def preserve(path):
    dest=case/'Istoric'/'2026.10.14 Inainte de declaratia de plata'/path.relative_to(root)
    dest.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and not dest.exists():shutil.copy2(path,dest)
def prepend(path,prefix=''):
    old=path.read_text(encoding='utf-8-sig') if path.exists() else ''
    if marker in old:return
    preserve(path);path.write_text(prefix+note+'ISTORIC PĂSTRAT\n\n'+old,encoding='utf-8-sig')
for n in ['2026.10.14 Status proiect.txt','2026.10.14 Log progres proiect.txt']:prepend(root/n)
for n in ['Donau Versicherung','Maritczak - Commerz Inkasso','CERHA HEMPEL']:prepend(archive/'Parteneri'/f'2026.10.14 Log discutii - {n}.txt')
prepend(root/'folder map/README.md','# ')
prepend(case/'2026.10.14 Jurnal actualizare.txt')
prepend(root/'05. Asigurari/Asigurare cladire/2026.10.14 Situatie Donau/2026.10.14 Situatie actuala Donau.txt')
rp=archive/'2026.10.14 Registru comunicatii.json';preserve(rp);reg=json.loads(rp.read_text(encoding='utf-8-sig'))
items=reg.setdefault('actualizari_punctuale',[])
entry={'data':'2026.10.14','subiect':marker,'status':status,'urmatorul_pas':next_step,'surse':[source],'plata_declarata_utilizator':4775.43,'incasare_confirmata':False,'email_trimis':False,'eva_mail_draft_id':None}
if not any(x.get('subiect')==marker for x in items):items.append(entry)
for e in reg.get('statusuri',[]):
    if e.get('partener')=='Donau Versicherung':e['plata_declarata_si_draft_2026_10_14']=entry
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'draft':'NETRIMIS','plata':'declarata, incasare neconfirmata','wordcount':len(d['body'].split()),'sha256_txt':hashlib.sha256((case/(stem+'.txt')).read_bytes()).hexdigest()},ensure_ascii=False))
