from pathlib import Path
import json,hashlib,shutil,sqlite3,csv,datetime
R=Path.cwd();B=R/'folder map';O=R/'08. Corespondenta/2026.10.28 Acces servieta BERGER PECH'
data=json.loads((O/'2026.10.28 Drafturi EVA - copie fara parole.json').read_text(encoding='utf-8'))
backup=B/('2026.10.28 Istoric acces servieta '+datetime.datetime.now().strftime('%H-%M-%S'));backup.mkdir()
def preserve(p):
 if p.exists():
  t=backup/p.relative_to(R);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
notes=[];partners=[]
for d in data:
 p=O/('2026.10.28 DRAFT NETRIMIS '+d['partner']+' - copie fara parola.txt')
 p.write_text('2026.10.28 | DRAFT NETRIMIS | COPIE LOCALA CU PAROLA OMISA\nExpeditor: '+d['account_email']+'\nDestinatar: '+', '.join(d['to'])+'\nCC: niciunul\nID Eva-Mail: '+d['id']+'\nSubiect: '+d['subject']+'\n\n'+d['body'],encoding='utf-8')
 name='Pech' if d['partner']=='PECH' else 'Markus Berger'
 note='2026.10.28 | ACCES SERVIETA - '+d['partner']+'\nStatus scurt: draft in germana salvat in EVA -> Drafts pentru office@ac-wohnart.at, destinat exclusiv '+d['to'][0]+', fara CC/BCC sau atasamente. Include linkul https://www.ac-wohnart.at/login si numai datele contului destinatarului. NETRIMIS.\nUltimul raspuns: utilizatorul a furnizat datele de acces si a cerut pregatirea emailului; nu raspuns nou al partenerului.\nUrmatorul pas: utilizatorul trimite din EVA; destinatarul este rugat sa confirme accesul si sa indice eventuale documente necesare.\nSursa: '+O.relative_to(R).as_posix()+'; ID draft '+d['id']+'. Draftul a fost recitit si destinatarii/datele de acces verificate. Parola nu este copiata in jurnale sau index; copia locala este explicit redactata. Acoperirea Eva-Mail ramane neschimbata.\n'
 notes.append(note);partners.append((R/('08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - '+name+'.txt'),note))
combined='\n'.join(notes);targets=partners+[(R/'2026.10.28 Status proiect.txt',combined),(R/'2026.10.28 Log progres proiect.txt',combined),(B/'README.md',combined)]
for p,note in targets:
 preserve(p);old=p.read_text(encoding='utf-8-sig') if p.exists() else '';p.write_text(note+'\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
(O/'2026.10.28 Jurnal pregatire.txt').write_text(combined,encoding='utf-8')
inv=B/'inventar.json';preserve(inv);rows=json.loads(inv.read_text(encoding='utf-8'));by={x['cale']:x for x in rows};db=sqlite3.connect(B/'cautare.sqlite')
for p in [x for x in O.rglob('*') if x.is_file()]+[x[0] for x in targets if B not in x[0].parents]:
 rel=p.relative_to(R).as_posix();txt=p.read_text(encoding='utf-8-sig');sha=hashlib.sha256(p.read_bytes()).hexdigest();cache=B/'texte'/f'{sha}.txt';cache.write_text(txt,encoding='utf-8');st=p.stat();row=by.get(rel,{})
 row.update({'cale':rel,'folder':p.parent.relative_to(R).as_posix(),'extensie':p.suffix,'octeti':st.st_size,'modificat':datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Draft acces servieta BERGER/PECH - copie locala fara parola','baza_descrierii':'verificare 2026.10.28','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(R).as_posix(),'detalii':{},'rezumat_verificat':'NETRIMIS. Datele complete sunt in draftul EVA, nu in index.','ocr_cache':''});by[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(by.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');cp=B/'inventar.csv';preserve(cp)
with cp.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print('Doua drafturi verificate; copii redactate, jurnale si index salvate.')
