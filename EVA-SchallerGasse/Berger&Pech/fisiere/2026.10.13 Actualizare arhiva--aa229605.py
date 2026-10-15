import json, pathlib, shutil, hashlib, datetime
ROOT = pathlib.Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
STAGE = pathlib.Path(r'C:\Users\User\.codex\visualizations\2026\10\01\01a0f6eb-c105-7760-973e-241d6f6be8c1')
DATE = '2026.10.13'
BASE = ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
RUN = ROOT/'08. Corespondenta/2026.10.13 Verificare zilnica'
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def writej(p,r):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def writet(p,t):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as f:f.write(t)
def rel(p):return p.relative_to(ROOT).as_posix()
def unwrap(r):return r.get('structuredContent') or json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
r=readj(BASE/'2026.10.12 Registru comunicatii.json')
ar=readj(BASE/'2026.10.12 Registru atasamente.json')
ev=readj(STAGE/'2026.10.13 Dovezi verificare Eva-Mail.json')
assert len(ev['searches'])==59
for q in ev['searches']:
    d=unwrap(q['result']); assert q['args'].get('offset',0)+len(d['items'])>=d['total']
m=unwrap(ev['full_new_emails'][0])
assert m['id']=='c384374a-c419-4747-a768-326f41f4e4b2' and not m['is_sent'] and not m['truncated']
assert m['id'] not in {x['id'] for x in r['comunicatii']}
a=m['attachments'][0]
original=STAGE/'2026.10.12 ORIGINAL bd01729c image001.png'
b=original.read_bytes(); sha=hashlib.sha256(b).hexdigest()
d=readj(STAGE/'2026.10.13 Export original Eva.json')
assert len(b)==37110==a['size'] and sha==d['sha256'] and d['eof']
RUN.mkdir(parents=True,exist_ok=True)
dest=RUN/original.name
shutil.copyfile(original,dest)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
ap=dict(id=a['id'],email_id=m['id'],data='2026.10.12',data_export=DATE,partener='Frigo',nume_original=a['name'],octeti=len(b),sha256=sha,cale=rel(dest),stare='salvat original integral',tip_verificat='Imagine de semnătură/logo și contacte; fără ofertă nouă',documentar=False)
txt=RUN/'2026.10.12 14-12 PRIMIT Frigo c384374a.txt'
meta=RUN/'2026.10.12 14-12 PRIMIT Frigo c384374a.json'
header = (
'2026.10.12 14:12:36 UTC / 17:12:36 România | PRIMIT | Frigo\n'
'Data export: 2026.10.13\n'
'De la: Frigo Peter Rupert <peter.frigo@frigo.at>\n'
'Către: covaciu.gnm@gmail.com\nCC: —\nSubiect: 1120 WIEN, Schallergasse 35\n'
'ID Eva-Mail: c384374a-c419-4747-a768-326f41f4e4b2\n'
'Căsuță: covaciu.gnm@gmail.com\n'
'Statut: PRIMIT; nu este draft, mesaj trimis sau contract acceptat.\n'
'Stare sursă: corp integral furnizat de API Eva-Mail, netrunchiat; exportul nu este MIME integral.\n'
'Data tehnică originală: 2026-10-12T14:12:36Z\n'
f'Atașament: image001.png | {len(b)} octeți | salvat original integral | {rel(dest)}\n'
'Verificare vizuală: semnătură/logo Peter Rupert FRIGO, contacte; fără ofertă PDF nouă.\n'
'\n--- TEXTUL FURNIZAT DE EVA, NEMODIFICAT ---\n')
writet(txt,header+m['text'])
mr=dict(m)
mr.update(data_afisata='2026.10.12',data_export=DATE,partener='Frigo',domeniu='Administrare imobil',statut='PRIMIT',text_fisier=rel(txt),atasamente_salvate=[ap])
writej(meta,mr)
old_source='08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/Frigo/2026.09.10 08-18 PRIMIT WG 1120 WIEN, Schallergasse 35 f5bac94e.txt'
new_status=('2026.10.12: Peter Rupert Frigo revine asupra ofertei de administrare trimise la 2026.09.10, speră că transmiterea a reușit și invită întrebări. '
'Nu transmite ofertă PDF, sume, condiții sau termen nou. Unicul atașament este semnătura/logo. Acceptarea nu este confirmată.')
next_step='Dacă administrarea Frigo rămâne de interes, confirmarea primirii ofertei și clarificarea condițiilor înaintea deciziei; niciun răspuns nu a fost trimis în această verificare.'
coverage=('59 căutări complete pentru 2026.10.11–13, primite și trimise separat în office, plus căutări globale după adresă, firme, servicii și referințe; '
'1 căutare contextuală pentru oferta Frigo din 2026.09.10. Toate totalurile sunt <=1, fără pagini restante. '
'Office sincronizat până la 2026.10.13 08:00:15 România; covaciu.gnm@gmail.com până la 2026.10.13 05:04:19; cosmin@ig.ro numai până la 2026.10.10 02:30:10. '
'Alte căsuțe au sincronizări diferite; căsuțele shared/team marcate nesearchable nu sunt acoperite. Exportul API nu garantează MIME integral.')
ev.update(
 note=('Toate paginile au fost preluate: fiecare total este <=1. Filtrarea Eva pe zile include două teste din 2026.10.10 21:xx UTC / 2026.10.11 00:xx România, excluse anterior. '
'Google/Claude și reclama Industrial Robots sunt false rezultate fără legătură cu proiectul. Mesajul Frigo este integral, netrunchiat. '
'Căutarea contextuală 2026.09.10 indică un mesaj cu aceleași metadate într-o altă căsuță, ID974d8861; nu este tratat ca noutate în interval. Oferta din 2026.09.10 era deja arhivată; originalele istorice nu sunt descărcate din nou. '
'Descărcarea HTTP a imaginii a eșuat la autentificare TLS; preluarea originalului base64 într-o singură pagină a reușit, cu verificare dimensiune/hash și verificare vizuală.'),
 original_salvat=ap,
 download_base64_verification={k:v for k,v in d.items() if k not in ['content_base64','url']},
 audit_agent='Audit independent READ-ONLY: interpretarea mesajului și baza 801/825/783 confirmate; căutările și sincronizarea sunt dovezile Eva root.',
 surse_locale=[rel(txt),rel(meta),rel(dest),old_source])
ev['rezultat'].update(mesaje_arhiva=802,originale_arhiva=826,documentare_arhiva=783)
writej(RUN/'2026.10.13 Dovezi verificare Eva-Mail.json',ev)
source=rel(RUN/'2026.10.13 Dovezi verificare Eva-Mail.json')
report=(f'{DATE} | Verificare zilnică Schallergasse 35\n\nNOUTĂȚI FAȚĂ DE VERIFICAREA 2026.10.12\n\n'
f'Un mesaj relevant nou PRIMIT: {new_status}\n'
'Sume și termene noi: niciunul. Nu este o ofertă structurală nouă și nu este un contract acceptat.\n'
f'Următorul pas: {next_step}\n'
f'Sursă integrală: {rel(txt)}\n'
f'Atașament descărcat: {rel(dest)} | {len(b)} octeți | SHA-256 {sha}\n'
f'Oferta și prezentarea din 2026.09.10 sunt deja arhivate; mesajul istoric: {old_source}\n\n'
'Nu au fost identificate alte comunicări relevante noi, inclusiv de la TOMS, BERGER, PECH, DONAU/Commerz, furnizorii de lifturi și SCHAUERLEUTE, în rezultatele accesibile ale verificării.\n\n'
f'ACOPERIRE\n{coverage}\n'
'Față de indexul local 2026.10.12 19:24:35: zero documente externe noi/modificate înaintea acestei salvări; două fișiere temporare Office ~$ nu sunt documente de proiect.\n\n'
'ARHIVARE\n1 mesaj integral nou și 1 imagine originală; 0 oferte PDF și 0 anexe documentare noi. Total:802 mesaje,826 originale,783 documentare. '
'68 corpuri istorice limitate de API rămân marcate trunchiat; noul mesaj nu este trunchiat.\n'
'Jurnalul proiectului, Frigo și partenerilor verificați, registrele și punctul de intrare sunt actualizate. Istoricul este păstrat. '
'Niciun email trimis, contract semnat sau plată efectuată.\n'
f'Dovezi: {source}\n')
writet(RUN/'2026.10.13 Raport verificare.txt',report)
r['data_actualizarii']=DATE
r['comunicatii'].append(dict(data='2026.10.12',ora_utc='14:12:36',partener='Frigo',domeniu='Administrare imobil',sens='PRIMIT',subiect=m['subject'],expeditor=m['from_address'],destinatari='; '.join(m['to']),cc='; '.join(m['cc']),id=m['id'],cale=rel(txt),atasamente=1,trunchiat=False))
ar.append(ap)
r['acoperire']['mesaje_salvate']=len(r['comunicatii'])
r['acoperire']['atasamente_salvate']=len(ar)
r['acoperire']['atasamente_identificate']+=1
r['acoperire']['mesaje_suplimentare_fata_de_lista']+=1
r['acoperire']['verificare_incrementala']=dict(data=DATE,mesaje_noi=1,originale_noi=1,pdf_salvate=0,imagini_salvate=1,anexe_documentare_noi=0,office_sincronizat='2026.10.13 08:00:15 România',gmail_sincronizat='2026.10.13 05:04:19 România',cosmin_sincronizat='2026.10.10 02:30:10 România',perioada='2026.10.11–13',cautari_complete=59,cautari_context=1,limita=coverage)
for s in r['statusuri']:
    if s.get('partener')=='Frigo':
        s.update(status=new_status,ultima_comunicare='2026.10.12',ultimul_primit='2026.10.12',subiect_ultimul_primit=m['subject'],urmatorul_pas=next_step,sursa_status=[m['id'],rel(txt),source],mesaje=s.get('mesaje',8)+1,ultima_verificare=DATE,nivel='Sinteză verificată; original nou netrunchiat')
r['actualizari_punctuale'].append(dict(data=DATE,subiect='Verificare zilnică: revenire Frigo asupra ofertei de administrare',mesaje=1,originale=1,anexe_documentare_noi=0,sursa=source,id_email=m['id']))
writej(BASE/'2026.10.13 Registru comunicatii.json',r)
writej(BASE/'2026.10.13 Registru atasamente.json',ar)
intro=(f'{DATE} | Verificare zilnică Schallergasse 35\n'
f'Status scurt: {new_status}\n'
'Ultimul răspuns nou: 2026.10.12 17:12:36 România, Frigo către covaciu.gnm@gmail.com, CC gol, IDc384374a-c419-4747-a768-326f41f4e4b2, PRIMIT.\n'
f'Următorul pas: {next_step}\n'
f'Acoperire: {coverage}\n'
'1 mesaj și 1 imagine semnătură salvate; 0 oferte PDF noi. Total802 mesaje/826 originale/783 documentare. '
'Propunerile locale BERGER/PECH din 2026.10.12 rămân NETRIMISE/NESEMNATE; nu sunt prezentate drept răspunsuri noi.\n'
f'Surse: {rel(txt)}; {source}\n'
'Repere existente: termenul Commerz 2026.10.12 și valabilitatea calculată BERGER 2026.10.12 au trecut, fără nouă confirmare de amânare/prelungire. '
'Promisiunea Füglister pentru 2026.10.12–18 este încă în curs. Acestea nu sunt comunicări noi.\n'
'Niciun email trimis, semnătură sau plată.\n\nISTORIC PĂSTRAT\n\n')
for suffix in ['Status proiect.txt','Log progres proiect.txt']:
    old=ROOT/('2026.10.12 '+suffix)
    writet(ROOT/(DATE+' '+suffix),intro+old.read_text(encoding='utf-8-sig'))
partners=BASE/'Parteneri'
frigo_old=partners/'2026.09.30 Log discutii - Frigo.txt'
pintro=(f'{DATE} | Frigo — verificare și mesaj nou\n'
f'Status scurt: {new_status}\n'
f'Ultimul răspuns: 2026.10.12 | {m["subject"]} | PRIMIT | peter.frigo@frigo.at către covaciu.gnm@gmail.com; CC gol.\n'
f'Următorul pas: {next_step}\n'
f'Sursă: {rel(txt)}; ID{m["id"]}; {source}\n'
'Un atașament original salvat, imagine semnătură/logo; nicio anexă contractuală nouă. Oferta din 2026.09.10 rămâne sursă istorică, fără acceptare identificată. '
'Eticheta vechiului folder „INCHIS” reprezintă situația din 2026.09.08 și nu înlocuiește mesajele ulterioare.\n\nISTORIC PĂSTRAT\n\n')
writet(partners/'2026.10.13 Log discutii - Frigo.txt',pintro+frigo_old.read_text(encoding='utf-8-sig'))
updated_partners=['Frigo']
for pname in ['TOMS','Markus Berger','Pech','Donau Versicherung','Maritczak - Commerz Inkasso','Füglister','SCHAUERLEUTE','Schmitt+Sohn','KONE','Weigl']:
    files=sorted(partners.glob('* Log discutii - '+pname+'.txt'))
    old=next((x for x in reversed(files) if not x.name.startswith(DATE)),None)
    if not old:continue
    match=next((x for x in r['statusuri'] if x.get('partener')==pname),None)
    last=(match or {}).get('ultimul_primit') or (match or {}).get('ultima_comunicare') or 'vezi istoricul de mai jos'
    nxt=(match or {}).get('urmatorul_pas') or 'Menținerea următorului pas documentat în istoricul de mai jos.'
    src=(match or {}).get('sursa_status') or [rel(old)]
    block=(f'{DATE} | Verificare zilnică — {pname}\n'
    'Status scurt: niciun mesaj relevant nou identificat pentru acest partener în căutările Eva pentru 2026.10.11–13. Condițiile, acceptarea și calendarul anterior nu sunt modificate prin această verificare.\n'
    f'Ultimul răspuns real: {last}; sursa și conținutul sunt păstrate mai jos.\n'
    f'Următorul pas: {nxt}\n'
    f'Surse: {source}; {json.dumps(src,ensure_ascii=False)}\n'
    'Limită: sincronizări diferite pe căsuțe; cosmin@ig.ro numai până la 2026.10.10 02:30:10 România.\n\nISTORIC PĂSTRAT\n\n')
    writet(partners/(DATE+' Log discutii - '+pname+'.txt'),block+old.read_text(encoding='utf-8-sig'))
    updated_partners.append(pname)
README=ROOT/'folder map/README.md'
hist=RUN/'2026.10.13 Istoric inainte verificare'
hist.mkdir(exist_ok=True)
shutil.copyfile(README,hist/'2026.10.13 README anterior.md')
readme_intro=(
'# 2026.10.13 — Revenire Frigo privind oferta de administrare\n\n'
'Puncte curente: ../2026.10.13 Status proiect.txt; ../2026.10.13 Log progres proiect.txt; registrele 2026.10.13 din arhiva Eva-Mail; '
'../08. Corespondenta/2026.10.13 Verificare zilnica/2026.10.13 Raport verificare.txt. '
'Un mesaj nou Frigo PRIMIT 2026.10.12, privind oferta transmisă 2026.09.10; fără sume, condiții sau termen nou. Unicul atașament original descărcat este semnătura/logo. '
'59 căutări complete pentru 2026.10.11–13 +1 contextuală; fără alte comunicări relevante noi. Office sincronizat 2026.10.13 08:00:15 România; Gmail 05:04:19; cosmin@ig.ro numai 2026.10.10 02:30:10. '
'Jurnalele proiectului și partenerilor sunt actualizate, istoricul păstrat. Total802 mesaje/826 originale/783 documentare. Nicio trimitere, semnare sau plată. '
'Propunerile locale BERGER/PECH de mai jos rămân NETRIMISE/NESEMNATE.\n\nISTORIC PĂSTRAT\n\n')
writet(README,readme_intro+(hist/'2026.10.13 README anterior.md').read_text(encoding='utf-8-sig'))
manifest=dict(data=DATE,status='Salvare finalizată; indexul se actualizează separat',mesaje_arhiva=len(r['comunicatii']),originale_arhiva=len(ar),documentare_arhiva=r['acoperire']['atasamente_documentare_salvate'],jurnale_parteneri=updated_partners,sursa=source,mesaj=rel(txt),meta=rel(meta),original=ap)
writej(RUN/'2026.10.13 Jurnal actualizare.json',manifest)
assert len(r['comunicatii'])==802 and len(ar)==826
assert r['acoperire']['atasamente_documentare_salvate']==783
assert m['text']==readj(meta)['text']
assert txt.read_text(encoding='utf-8',newline='') if False else True
with txt.open('r',encoding='utf-8',newline='') as f: assert f.read().endswith(m['text'])
assert readj(BASE/'2026.10.12 Registru comunicatii.json')['acoperire']['mesaje_salvate']==801
print(json.dumps(manifest,ensure_ascii=False,indent=2))

