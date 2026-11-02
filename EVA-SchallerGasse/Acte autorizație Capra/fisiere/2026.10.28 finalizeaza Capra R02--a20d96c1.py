from pathlib import Path
import json,hashlib,datetime,sqlite3,shutil
from email.message import EmailMessage
from email.policy import SMTP
from pypdf import PdfReader
root=Path.cwd();base=root/'folder map';out=root/'08. Corespondenta/2026.10.28 Capra dosar autorizare'
d=json.loads((out/'2026.10.28 R02 Draft EVA Capra.json').read_text(encoding='utf-8'))
prefix='2026.10.28 R02 DRAFT NETRIMIS Capra'
header=f"2026.10.28 | R02 | DRAFT NETRIMIS\nDe la: {d['account_email']}\nCatre: {', '.join(d['to'])}\nCC: fara\nID Eva-Mail: {d['id']}\nSubiect: {d['subject']}\n\n"
(out/(prefix+'.txt')).write_text(header+d['body'],encoding='utf-8')
m=EmailMessage(policy=SMTP);m['From']=d['account_email'];m['To']=', '.join(d['to']);m['Subject']=d['subject'];m['X-Unsent']='1';m['X-Eva-Draft-ID']=d['id'];m.set_content(d['body'])
manifest=[]
for a in d['attachments']:
 p=out/'2026.10.28 R02 Anexe legale'/a['filename'];b=p.read_bytes()
 pdf=PdfReader(p)
 tx='\n'.join(pg.extract_text() or '' for pg in pdf.pages)
 assert 'Bauordnung' in tx and ('§ 63' in tx or '§ 64' in tx)
 pages=len(pdf.pages)
 m.add_attachment(b,maintype='application',subtype='pdf',filename=p.name)
 manifest.append(dict(a,sha256=hashlib.sha256(b).hexdigest(),pagini=pages))
(out/(prefix+'.eml')).write_bytes(m.as_bytes())
(out/'2026.10.28 R02 Manifest anexe.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
entry='''\n2026.10.28 | CAPRA R02 - PREDARE CONTRACTUALA
Status scurt: acelasi draft EVA ff0832eb-8177-48d9-9ec9-5688b7e16adb revizuit si recitit, NETRIMIS; office@ac-wohnart.at catre Bogdan.Capra@cerhahempel.com, fara CC. Trei PDF oficiale RIS atasate integral: §§63/64 forma 2023 si §63 forma 2026. R01 pastrata local.
Ultimul raspuns: utilizatorul cere baza contractuala si actele oficiale nepredate, necesare acum pentru incepere. Nu raspuns nou Capra; fara sincronizare email noua.
Urmatorul pas: utilizatorul trimite din EVA; Capra solicita completarea predarii la vanzatoare si verifica pachetul 2026.03.17.
Sursa: 08. Corespondenta/2026.10.28 Capra dosar autorizare/2026.10.28 R02 DRAFT NETRIMIS Capra.txt; contract 1.2/2.1/7.1(d)/7.3; Bescheid p.1/8; RIS §§63/64/65/124/127. Cerintele 2026 nu sunt impuse retroactiv dosarului 2023; recomandari distincte de obligatii conditionate. EML local contine cele trei atasamente reale.
'''
changed=[p for p in out.rglob('*') if p.is_file() and 'R02' in str(p.relative_to(out))]
for rel in ['2026.10.28 Log progres proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - CERHA HEMPEL.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - CP Immobilien - Kornhofer.txt']:
 p=root/rel
 with p.open('a',encoding='utf-8') as f:f.write(entry)
 changed.append(p)
with (base/'README.md').open('a',encoding='utf-8') as f:f.write(entry)
idx=base/'inventar.json';shutil.copy2(idx,base/'2026.10.28 QA contract cumparare/2026.10.28 inventar inainte Capra R02.json')
rows={r['cale']:r for r in json.loads(idx.read_text(encoding='utf-8'))};db=sqlite3.connect(base/'cautare.sqlite')
for p in changed:
 rel=p.relative_to(root).as_posix();h=hashlib.sha256(p.read_bytes()).hexdigest();s=p.stat()
 if p.suffix=='.pdf':
  tx='\n'.join(pg.extract_text() or '' for pg in PdfReader(p).pages)
 elif p.suffix=='.eml':tx=header+d['body']+'\nAnexe reale: '+', '.join(a['filename'] for a in manifest)
 else:tx=p.read_text(encoding='utf-8-sig')
 cp=base/'texte'/f'{h}.txt';cp.write_text(tx,encoding='utf-8')
 rows[rel]=dict(cale=rel,folder=p.parent.relative_to(root).as_posix(),extensie=p.suffix,octeti=s.st_size,modificat=datetime.datetime.fromtimestamp(s.st_mtime).isoformat(),modificat_ns=s.st_mtime_ns,sha256=h,duplicat_al='',ce_reprezinta='Capra R02 predare contractuala / surse legale',baza_descrierii='actualizare punctuala',extras_continut=tx[:1000],stare_citire='text citit',text_cache=cp.relative_to(root).as_posix(),detalii={},rezumat_verificat='DRAFT NETRIMIS; anexe RIS originale.',ocr_cache='')
 db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,rows[rel]['ce_reprezinta'],tx,h))
db.commit();db.close();idx.write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print('R02 arhivata, 3 PDF originale verificate si incluse in EML; jurnale si index JSON/SQLite actualizate.')
