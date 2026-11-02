from pathlib import Path
import json,base64,hashlib,datetime,sqlite3,shutil
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
root=Path.cwd(); fm=root/'folder map'
p=json.loads((fm/'2026.10.30 17-01 Capra payload.json').read_text(encoding='utf-8')); e=p['email']
out=root/'08. Corespondenta/2026.10.29 Capra Baupolizei'; changed=[]
stem='2026.10.30 16-56-53 PRIMIT Capra c61d9755'
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_bytes(data if isinstance(data,bytes) else data.encode('utf-8'));changed.append(path)
write(out/(stem+'.json'),json.dumps({'link_id':'link_6ae19b6ebad08191ba9bbfe616469187','mirror_id':'cb1a4280-bf8f-419e-8fe3-b5d577a6772d','data_lizibila':'2026.10.30 16:56:53 Europe/Bucharest','statut':'PRIMIT','email':e},ensure_ascii=False,indent=2))
write(out/(stem+'.txt'),'PRIMIT | 2026.10.30 16:56:53 Europe/Bucharest\nID Eva-Mail: '+e['id']+'\nDe la: '+e['from_address']+'\nCatre: '+', '.join(e['to'])+'\nCC: '+', '.join(e['cc'])+'\nSubiect: '+e['subject']+'\n\n'+e['text'])
msg=EmailMessage();msg['From']=e['from_address'];msg['To']=', '.join(e['to']);msg['Subject']=e['subject'];msg['Date']='Fri, 30 Oct 2026 14:56:53 +0000';msg['X-Eva-Mail-ID']=e['id'];msg['X-Export-Note']='Reconstructed from EVA; not original MIME';msg.set_content(e['text'])
manifest=[]
for i,d in enumerate(p['downloads']):
 a=d['attachment']; data=b''.join(base64.b64decode(c['content_base64']) for c in d['chunks']);assert len(data)==a['size']
 for c in d['chunks']:
  if c.get('chunk_sha256'):assert hashlib.sha256(base64.b64decode(c['content_base64'])).hexdigest()==c['chunk_sha256']
 path=out/'Atasamente'/(f'2026.10.30 Capra c61d9755 {i+1:02d} - '+a['name']);write(path,data)
 manifest.append({'id_eva':a['id'],'original_name':a['name'],'cale':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'verificare':'descarcare integrala base64; dimensiune si hash pe bloc'})
 msg.add_attachment(data,maintype='application',subtype='octet-stream',filename=a['name'])
 if a['content_type']=='message/rfc822':
  nested=BytesParser(policy=policy.default).parsebytes(data); body=nested.get_body(preferencelist=('plain',))
  write(out/'2026.10.30 Capra corespondenta atasata - extras.txt',str(nested.items())+'\n\n'+(body.get_content() if body else 'Fara corp plain separat'))
write(out/(stem+'.eml'),msg.as_bytes(policy=policy.SMTP))
proof={'data_lizibila':'2026.10.30 17:01 Europe/Bucharest','searches':p['searches'],'mailboxes':p['mailboxes'],'attachments':manifest,'canonical_id':e['id'],'mirror_id':'cb1a4280-bf8f-419e-8fe3-b5d577a6772d'}
write(out/'2026.10.30 17-01 Dovezi verificare.json',json.dumps(proof,ensure_ascii=False,indent=2))
report='''2026.10.30 17:01 Europe/Bucharest | Capra / Baupolizei / vanzator
Status scurt: RASPUNS NOU CAPRA primit 2026.10.30 16:56:53. Confirma primirea cererii si anunta ca il va contacta pe dl. Kornhofer. Nu confirma ca solicitarea a fost deja trimisa vanzatorului.
Destinatari efectivi: Bogdan.Capra@cerhahempel.com -> office@ac-wohnart.at; CC gol. Este raspuns avocat-client, nu email catre vanzator sau autoritate.
Ultimul raspuns: Capra spune ca pastreaza documentatia transmisa la 2026.03.17 (Bestandsunterlagen, Energieausweis DG, Bauphysik) si o poate retransmite impreuna cu un index. Aceasta oferta nu confirma predarea planurilor vizate. Poate contacta arhitectul Klaus Pristounig; aminteste factura contestata. Recomanda mai intai abordare amiabila la autoritate si dl. Asreahan, cu analiza juridica detaliata ulterior daca nu exista intelegere. Acestea sunt pozitiile avocatului, nu concluzii juridice ale verificarii.
Anexe: corespondenta istorica EML, proces-verbal de predare din 2026.03.17 PDF si sase imagini de semnatura. Toate cele opt intrari au fost descarcate integral; nu sunt planuri vizate noi. Originalele sunt pastrate; EML-ul principal este reconstruit din EVA, nu MIME original.
MA37 / vanzator: nu s-a identificat raspuns nou al autoritatii ori al vanzatorului in cautarile disponibile. Nu s-a identificat solicitarea Capra catre vanzator cu utilizatorul in CC. Absenta din casuta utilizatorului nu dovedeste absenta unei comunicari separate a avocatului.
Urmatorul pas: urmarirea solicitarii efectiv trimise catre vanzator, a destinatarilor/CC, raspunsului acestuia si MA37; obtinerea inventarului si exemplarelor vizate A/B/C, traseului si reprezentarii la depunere/primire. Nu se considera efectuata predarea planurilor ori o consultare noua.
Acoperire: 16 cautari, fiecare cu rezultate sub limita de 50, fara pagini restante, in ambele conexiuni EVA, din 2026.10.29. Un mesaj nou canonic, oglindit in a doua conexiune. Sincronizare office Primary 2026.10.30 17:00:10, office secundar 16:57:01, Gmail 14:27:26 Romania; mesajele neindexate pot lipsi. Nu se pretinde acces la casutele interne ale avocatului/vanzatorului.
Program curent conform instructiunii: luni-vineri 10:00, 13:00, 17:00 Europe/Bucharest, pana la oprire expresa, inclusiv dupa primul raspuns. Nu s-au trimis emailuri.
Sursa: 08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.30 16-56-53 PRIMIT Capra c61d9755.json; ID Eva-Mail c61d9755-daf2-4e6d-aa49-3e8db7bd919f, alias cb1a4280-bf8f-419e-8fe3-b5d577a6772d; 2026.10.30 17-01 Dovezi verificare.json.
'''
write(out/'2026.10.30 17-01 Jurnal verificare.txt',report)
hist=fm/'2026.10.30 17-01 Istoric Capra';hist.mkdir(exist_ok=True)
logs=['2026.10.30 Log progres proiect.txt','2026.10.30 Status proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.30 Log discutii - CERHA HEMPEL.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.30 Log discutii - MA37 Baupolizei.txt']
for rel in logs:
 path=root/rel;old=path.read_text(encoding='utf-8-sig') if path.exists() else ''
 if path.exists():
  bk=hist/rel;bk.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,bk)
 write(path,report+'\nISTORIC PASTRAT\n\n'+old)
rows=json.loads((fm/'inventar.json').read_text(encoding='utf-8-sig'));by={r['cale']:r for r in rows};shutil.copy2(fm/'inventar.json',hist/'inventar.json')
db=sqlite3.connect(fm/'cautare.sqlite',timeout=30)
for path in changed:
 rel=path.relative_to(root).as_posix();data=path.read_bytes();sha=hashlib.sha256(data).hexdigest();st=path.stat();txt=''
 if path.suffix.lower() in ['.txt','.json','.eml']:txt=data.decode('utf-8',errors='replace')
 elif path.suffix.lower()=='.pdf':
  import fitz
  with fitz.open(path) as doc:txt='\n'.join(pg.get_text() for pg in doc)
 cache=fm/'texte'/(sha+'.txt');cache.write_text(txt,encoding='utf-8')
 r=by.get(rel,{});r.update(cale=rel,folder=path.parent.relative_to(root).as_posix(),extensie=path.suffix.lower(),octeti=len(data),modificat=datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),modificat_ns=st.st_mtime_ns,sha256=sha,duplicat_al='',ce_reprezinta='Capra: raspuns primit, documente si monitorizare',baza_descrierii='EVA si jurnal verificat',extras_continut=txt[:1500],stare_citire='text extras' if txt else 'original binar pastrat',text_cache=cache.relative_to(root).as_posix(),detalii='',rezumat_verificat='',ocr_cache='');by[rel]=r
 db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente(cale,descriere,text,sha256) VALUES(?,?,?,?)',(rel,r['ce_reprezinta'],txt,sha))
db.commit();db.close();(fm/'inventar.json').write_text(json.dumps(list(by.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files_saved_indexed':len(changed),'attachments':len(manifest),'report':str(out/'2026.10.30 17-01 Jurnal verificare.txt')}))
