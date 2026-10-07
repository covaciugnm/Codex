from pathlib import Path
import json, datetime, hashlib, sqlite3, shutil
from email.message import EmailMessage
from email.policy import SMTP

root=Path(__file__).resolve().parent.parent
folder=root/'08. Corespondenta/2026.10.05 Draft negociere Schmitt + Sohn'
source=folder/'2026.10.05 Draft Eva-Mail Schmitt + Sohn.json'
d=json.loads(source.read_text(encoding='utf-8'))['eva']
assert d['status']=='pending' and d['account_email']=='office@ac-wohnart.at'
assert d['to']==['t.jeitler@schmitt-aufzuege.at']
meta=f"Data: 2026.10.05\nCreat UTC: {d['created_at']}\nStatut: DRAFT NETRIMIS\nID Eva-Mail: {d['id']}\nExpeditor: {d['account_email']}\nDestinatar: {', '.join(d['to'])}\nCC: niciunul\nBCC: niciunul\nSubiect: {d['subject']}\nAtasamente: niciunul\nExport API; nu este dovada trimiterii.\n\n"
txt=folder/'2026.10.05 DRAFT NETRIMIS Schmitt + Sohn.txt'
txt.write_text(meta+d['body']+'\n',encoding='utf-8')
msg=EmailMessage(policy=SMTP)
msg['From']=d['account_email'];msg['To']=', '.join(d['to']);msg['Subject']=d['subject']
msg['Date']=datetime.datetime.fromisoformat(d['created_at'].replace('Z','+00:00'))
msg['X-Unsent']='1';msg['X-Eva-Draft-ID']=d['id'];msg['X-Archive-Status']='DRAFT NOT SENT'
msg.set_content(d['body'])
eml=folder/'2026.10.05 DRAFT NETRIMIS Schmitt + Sohn.eml'
eml.write_bytes(msg.as_bytes())
entry=f"2026.10.05 | Schmitt + Sohn — negociere oferta ANG0232318\nStatus scurt: DRAFT NETRIMIS salvat in Eva-Mail, office@ac-wohnart.at, catre t.jeitler@schmitt-aufzuege.at, fara CC si atasamente. Propunere garantie 72 luni cu intretinere 6 ani; detaliere lucrari/costuri suplimentare, piese si disponibilitate 20 ani; modele contracte; plata 25/25/40/10; verificare independenta si formalitati WAZG. Nu este comanda sau acceptare comerciala.\nUltimul raspuns primit: 2026.10.02, oferta ANG0232318, ID fea3c0c1-7a62-411a-b1d9-adfc1774f9b9. Nu s-a facut o noua verificare generala a corespondentei.\nUrmatorul pas: Revizuirea si trimiterea draftului de catre utilizator din Eva-Mail; dupa trimitere, verificarea dovezii si urmarirea raspunsului. Compatibilitatea 630/675 kg ramane de clarificat.\nSursa: Eva-Mail draft {d['id']}; {source.relative_to(root).as_posix()}\n"
project=root/'2026.10.05 Jurnal proiect - completare negociere Schmitt + Sohn.txt'
project.write_text(entry,encoding='utf-8')
partner=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.05 Log discutii - Schmitt + Sohn.txt'
status=root/'2026.10.05 Status proiect.txt'
history=folder/'2026.10.05 Istoric inainte de draft';history.mkdir(exist_ok=True)
for p in [partner,status]:
 old=p.read_text(encoding='utf-8')
 if d['id'] not in old:
  shutil.copy2(p,history/p.name)
  p.write_text(entry+'\nISTORIC — situatia anterioara salvarii draftului\n\n'+old,encoding='utf-8')
readme=root/'folder map/README.md'
old=readme.read_text(encoding='utf-8')
if d['id'] not in old:
 readme.write_text('# 2026.10.05 — Draft negociere Schmitt + Sohn\n\nDraft NETRIMIS in Eva-Mail, office@ac-wohnart.at, ID '+d['id']+'. Sursa: ../08. Corespondenta/2026.10.05 Draft negociere Schmitt + Sohn/. Jurnal proiect: ../2026.10.05 Jurnal proiect - completare negociere Schmitt + Sohn.txt; status si jurnal partener TXT actualizate. Registrul Excel si copia DOCX a jurnalului partenerului reflecta verificarea anterioara; aceasta completare TXT consemneaza draftul. Oferta nu este acceptata.\n\n'+old,encoding='utf-8')
# Actualizare incrementala a indexului JSON si a cautarii FTS; fara recitirea arhivei.
index=root/'folder map/inventar.json';rows=json.loads(index.read_text(encoding='utf-8'));by={x['cale']:x for x in rows}
paths=[source,txt,eml,project,partner,status]+list(history.iterdir())
db=sqlite3.connect(root/'folder map/cautare.sqlite')
for p in paths:
 rel=p.relative_to(root).as_posix();raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest();st=p.stat()
 text=meta+d['body'] if p.suffix=='.eml' else p.read_text(encoding='utf-8')
 cache=root/'folder map/texte'/f'{h}.txt';cache.write_text(text,encoding='utf-8')
 row=by.get(rel,{});row.update(cale=rel,folder=p.parent.relative_to(root).as_posix(),octeti=st.st_size,modificat_ns=st.st_mtime_ns,modificat=datetime.datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(),sha256=h,text_cache=cache.relative_to(root).as_posix(),ocr_cache='',ce_reprezinta='Arhiva draft si jurnal Schmitt + Sohn',extras_continut=text[:1500],stare_citire='text citit; draft netrimis',duplicat_al='',rezumat_verificat='2026.10.05: DRAFT NETRIMIS; nu este acceptare comerciala.' if p not in history.iterdir() else 'Versiune istorica pastrata inainte de draft.')
 by[rel]=row
 db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente(cale,descriere,text,sha256) VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],text,h))
index.write_text(json.dumps(list(by.values()),ensure_ascii=False,indent=2),encoding='utf-8');db.commit();db.close()
assert d['id'] in partner.read_text(encoding='utf-8')
print(json.dumps({'draft_id':d['id'],'status':'DRAFT NETRIMIS','archived_files':len(paths),'project_journal':str(project)},ensure_ascii=False))
