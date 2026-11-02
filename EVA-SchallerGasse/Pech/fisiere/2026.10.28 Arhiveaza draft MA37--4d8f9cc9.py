from pathlib import Path
import json,base64,hashlib,shutil,datetime,csv,sqlite3
from email.message import EmailMessage
from email.policy import SMTP
from pypdf import PdfReader
import pypdfium2 as pdfium
R=Path.cwd();B=R/'folder map';O=R/'08. Corespondenta/2026.10.28 MA37 cerere planuri vizate';Q=B/'2026.10.28 QA draft MA37';Q.mkdir(exist_ok=True)
data=json.loads((O/'2026.10.28 Draft EVA si surse.json').read_text(encoding='utf-8'));draft=data['draft'];A=O/'Atasamente';A.mkdir(exist_ok=True)
chunks=json.loads((B/'2026.10.28 Firma inregistrare bytes.json').read_text(encoding='utf-8'));out=b''
for ch in sorted(chunks,key=lambda x:x['offset']):
 raw=base64.b64decode(ch['content_base64']);assert len(out)==ch['offset'];assert len(raw)==ch['bytes_returned'];assert hashlib.sha256(raw).hexdigest()==ch['chunk_sha256'];out+=raw
founder=A/'2026.10.28 01 Eintragungsbeschluss Gruendung.pdf';founder.write_bytes(out)
paths=[founder]
sources=[None,'01. Proprietate + Acte/Acte Firma A&C Wohnart/CHSH-#2688665-v1-Sonstiger_Beschluss__Eintragungsbeschluss.PDF','08. Corespondenta/2026.10.16 Verificare zilnica/2026.10.15 ORIGINAL d02a044d FBA A&C Wohnart, FN 668224h.pdf','00.Proiect/01. Behoerden + Eigentum/02. Grundbuch + Kaufvertrag/Grundbuchauszug_aktuell_A&C_EZ2235.pdf','01. Proprietate + Acte/Cadastru/A&C GB Beschluss, KG 01305, EZ 2235.pdf','00.Proiect/01. Behoerden + Eigentum/01. Baubescheid + genehmigte Plaene/Schallergasse_35_Baubescheid.pdf']
names=['','02 Eintragungsbeschluss Anschrift.pdf','03 Firmenbuchauszug Stand 2026.04.01.pdf','04 Grundbuchauszug 2026.03.11.pdf','05 Grundbuchbeschluss TZ466-2026.pdf','06 Baubescheid 2023.04.21 samt Beilagen.pdf']
for src,name in zip(sources[1:],names[1:]):
 dest=A/('2026.10.28 '+name);shutil.copy2(R/src,dest);paths.append(dest)
manifest=[]
for i,p in enumerate(paths):
 a=draft['attachments'][i];assert p.stat().st_size==a['size'],p
 manifest.append({'local_path':p.relative_to(R).as_posix(),'source_local_path':sources[i],'eva_id':a['id'],'original_name':a['filename'],'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'2026.10.28 Manifest atasamente.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
head='2026.10.28 | DRAFT NETRIMIS\nExpeditor: '+draft['account_email']+'\nDestinatari: '+', '.join(draft['to'])+'\nCC: '+', '.join(draft['cc'])+'\nID draft Eva-Mail: '+draft['id']+'\nSubiect: '+draft['subject']+'\n\n'
(O/'2026.10.28 DRAFT MA37 cerere planuri vizate.txt').write_text(head+draft['body'],encoding='utf-8')
em=EmailMessage();em['From']=draft['account_email'];em['To']=', '.join(draft['to']);em['Cc']=', '.join(draft['cc']);em['Subject']=draft['subject'];em['X-Unsent']='1';em['X-Eva-Draft-ID']=draft['id'];em.set_content(draft['body'])
for p,a in zip(paths,draft['attachments']):em.add_attachment(p.read_bytes(),maintype='application',subtype='pdf',filename=a['filename'])
(O/'2026.10.28 DRAFT NETRIMIS MA37 cerere planuri vizate.eml').write_bytes(em.as_bytes(policy=SMTP))
for p in [paths[0],paths[2]]:
 pdf=pdfium.PdfDocument(p)
 for i in [0,len(pdf)-1]:pdf[i].render(scale=1.3).to_pil().save(Q/(p.stem+' pagina '+str(i+1)+'.png'))
note='''2026.10.28 | DRAFT MA37: ACCES LA PLANURILE VIZATE
Status scurt: draft in germana salvat si recitit in EVA -> Drafts, expeditor office@ac-wohnart.at, destinatar west@ma37.wien.gv.at, CC post@ma37.wien.gv.at; ID 2b13f782-3bdd-4720-8d16-c774ae404311; NETRIMIS. Sase atasamente reale: infiintare, modificare adresa, extras firma, extras CF, decizie intabulare, Baubescheid cu anexa §69.
Ultimul raspuns: utilizatorul solicita mesaj juridic pentru consultarea/copierea proiectului aprobat, deoarece fostul proprietar nu a predat complet actele; nu raspuns nou MA37.
Temei: §17 AVG si §63(1)(a) BO Wien (inclusiv forma 2023). Se cere plansetul cu vize, descrierea si anexele tehnice, eventualele modificari, dovada Rechtskraft/termen inceput. Datele istorice ale extraselor sunt declarate explicit; nu sunt prezentate drept extrase emise astazi. MA37 nu trimite arhiva de planuri prin email: draftul cere consultare/copii sau procedura disponibila de digitalizare, cu informare privind costuri si documente actuale.
Urmatorul pas: revizuirea si trimiterea de catre utilizator din EVA; apoi raspuns/programare MA37. Nu s-a rezervat termen si nu s-a asumat ca intalnirea anterioara a avut loc.
Sursa: 08. Corespondenta/2026.10.28 MA37 cerere planuri vizate; text, EML cu atasamente originale, manifest si surse juridice salvate. Acoperirea email ramane limitata la sursele consultate; nu este sincronizare generala.
'''
(O/'2026.10.28 Jurnal pregatire MA37.txt').write_text(note,encoding='utf-8')
stamp=datetime.datetime.now().strftime('%H-%M-%S');backup=B/('2026.10.28 Istoric draft MA37 '+stamp);backup.mkdir()
def preserve(p):
 if p.exists():
  d=backup/p.relative_to(R);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
targets=[R/'2026.10.28 Status proiect.txt',R/'2026.10.28 Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log audit - MA37.txt',B/'README.md']
for p in targets:
 preserve(p);old=p.read_text(encoding='utf-8-sig') if p.exists() else '';p.write_text(note+'\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
inv=B/'inventar.json';preserve(inv);rows=json.loads(inv.read_text(encoding='utf-8'));by={x['cale']:x for x in rows};db=sqlite3.connect(B/'cautare.sqlite')
for p in [x for x in O.rglob('*') if x.is_file()]+[x for x in targets if B not in x.parents]:
 rel=p.relative_to(R).as_posix();sha=hashlib.sha256(p.read_bytes()).hexdigest();cache=B/'texte'/f'{sha}.txt'
 if p.suffix.lower()=='.pdf':txt='\n'.join(pg.extract_text() or '' for pg in PdfReader(p).pages)
 elif p.suffix=='.eml':txt=head+draft['body']+'\nAtasamente: '+', '.join(x['filename'] for x in draft['attachments'])
 else:txt=p.read_text(encoding='utf-8-sig')
 cache.write_text(txt,encoding='utf-8');st=p.stat();row=by.get(rel,{})
 row.update({'cale':rel,'folder':p.parent.relative_to(R).as_posix(),'extensie':p.suffix,'octeti':st.st_size,'modificat':datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Draft MA37 Akteneinsicht si anexe reale','baza_descrierii':'verificare 2026.10.28','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(R).as_posix(),'detalii':{},'rezumat_verificat':'Draft NETRIMIS; atasamente existente copiate fara modificarea originalelor.','ocr_cache':''});by[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(by.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');cp=B/'inventar.csv';preserve(cp)
with cp.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print('Draft arhivat cu 6 PDF originale; EML NETRIMIS, jurnale si index actualizate.')
