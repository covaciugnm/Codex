from pathlib import Path
import json, shutil, hashlib, datetime, sqlite3
from email.message import EmailMessage
from email.policy import SMTP
root=Path.cwd(); base=root/'folder map'; out=root/'08. Corespondenta/2026.10.28 Capra dosar autorizare'
d=json.loads((out/'2026.10.28 Draft EVA Capra.json').read_text(encoding='utf-8'))
m=EmailMessage(policy=SMTP);m['From']=d['account_email'];m['To']=', '.join(d['to']);m['Subject']=d['subject'];m['X-Unsent']='1';m['X-Eva-Draft-ID']=d['id'];m.set_content(d['body'])
(out/'2026.10.28 DRAFT NETRIMIS Capra.eml').write_bytes(m.as_bytes())
entry='''\n2026.10.28 | CAPRA - DOSAR AUTORIZARE
Status scurt: DRAFT NETRIMIS salvat si recitit in EVA, office@ac-wohnart.at catre Bogdan.Capra@cerhahempel.com, fara CC/atasamente. ID ff0832eb-8177-48d9-9ec9-5688b7e16adb.
Ultimul raspuns: cerere utilizator pentru solicitarea dosarului vizat de la vanzatoare; nu raspuns nou Capra. Emailul istoric 2026.03.17 confirma documente electronice, nu inventar complet.
Urmatorul pas: trimiterea din EVA de catre utilizator; Capra sa verifice pachetul primit si sa solicite completarea la vanzatoare, subsidiar recuperare MA37.
Sursa: 08. Corespondenta/2026.10.28 Capra dosar autorizare; Baubescheid p.1-3/8, §§63-64 forma 2023 si §§124/127 BO Wien. Lista separa documentele conditionate si actele noi de executie. Fara pretentie ca fiecare anexa trebuie stampilata; planurile vizate sunt expres parte esentiala a deciziei. Acoperirea email nu s-a extins.
'''
changed=list(out.iterdir())
for rel in ['2026.10.28 Log progres proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - CERHA HEMPEL.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - CP Immobilien - Kornhofer.txt']:
    p=root/rel
    with p.open('a',encoding='utf-8') as f:f.write(entry)
    changed.append(p)
with (base/'README.md').open('a',encoding='utf-8') as f:f.write(entry)
idx=base/'inventar.json';shutil.copy2(idx,base/'2026.10.28 QA contract cumparare/2026.10.28 inventar inainte draft Capra.json')
rows={r['cale']:r for r in json.loads(idx.read_text(encoding='utf-8'))};db=sqlite3.connect(base/'cautare.sqlite')
for p in changed:
    rel=p.relative_to(root).as_posix();h=hashlib.sha256(p.read_bytes()).hexdigest();s=p.stat();tx=p.read_text(encoding='utf-8-sig');cp=base/'texte'/f'{h}.txt';cp.write_text(tx,encoding='utf-8')
    r=dict(cale=rel,folder=p.parent.relative_to(root).as_posix(),extensie=p.suffix,octeti=s.st_size,modificat=datetime.datetime.fromtimestamp(s.st_mtime).isoformat(),modificat_ns=s.st_mtime_ns,sha256=h,duplicat_al='',ce_reprezinta='Draft Capra dosar autorizare / jurnal',baza_descrierii='actualizare punctuala 2026.10.28',extras_continut=tx[:1000],stare_citire='text citit',text_cache=cp.relative_to(root).as_posix(),detalii={},rezumat_verificat='DRAFT NETRIMIS; lista conditionata, surse juridice in corp.',ocr_cache='')
    rows[rel]=r;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,r['ce_reprezinta'],tx,h))
db.commit();db.close();idx.write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print('Draft TXT/JSON/EML arhivat; jurnale actualizate; index JSON/SQLite actualizat punctual.')
