from pathlib import Path
from datetime import datetime, timezone, timedelta
import json, hashlib, shutil, sqlite3, csv, sys
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd(); b=r/'folder map'; now=datetime.now(timezone(timedelta(hours=2))); day=now.strftime('%Y.%m.%d'); tag=now.strftime('%H-%M-%S'); stamp=now.isoformat(timespec='seconds')
p=json.loads((b/'2026.10.29 Dovezi check-email PECH 17.json').read_text(encoding='utf-8'))
rp=r/p['baseline_register']; reg=json.loads(rp.read_text(encoding='utf-8')); inv=b/'inventar.json'; rows=json.loads(inv.read_text(encoding='utf-8')); indexed={x['cale']:x for x in rows}
known={x['id'] for x in reg['comunicatii']}; assert not p['errors'] and set(p['scoped_email_ids'])<=known
assert all(s['args']['offset']+len(s['result']['items'])>=s['result']['total'] for s in p['searches'])
ids={x['id'] for s in p['searches'] for x in s['result']['items']}; assert ids==set(p['scoped_email_ids'])|set(p['excluded_unrelated_email_ids'])
status=next(s for s in reg['statusuri'] if s.get('partener')=='Pech')
source_messages=[m for m in reg['comunicatii'] if m['id'] in p['scoped_email_ids']]
checked=[]
for rel in [p['baseline_register']]+[m['cale'] for m in source_messages]+status['sursa_status']:
    f=r/rel; sha=hashlib.sha256(f.read_bytes()).hexdigest(); unchanged=sha==indexed.get(rel,{}).get('sha256'); assert unchanged,rel
    checked.append({'cale':rel,'sha256':sha,'unchanged':unchanged})
o=r/'08. Corespondenta'/(day+' Check-email PECH');o.mkdir(exist_ok=True)
hist=b/(day+' Istoric check-email PECH '+tag);hist.mkdir()
changed=[]
def preserve(f):
    if f.exists():
        target=hist/f.relative_to(r);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
def save(f,text):
    preserve(f);f.write_text(text,encoding='utf-8');changed.append(f)
def jsave(f,d):save(f,json.dumps(d,ensure_ascii=False,indent=2))
def digest(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
before={k:digest(reg[k]) for k in ['comunicatii','drafturi']}; general=reg['acoperire']['verificare_incrementala'].copy()
proof=o/(day+' '+tag+' Dovezi check-email PECH.json');report=o/(day+' '+tag+' Raport check-email PECH.txt')
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']}
def local(value):return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=2))).strftime('%Y.%m.%d %H:%M:%S')
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Pech'],'mesaje_noi':0,'atasamente_noi':0,'query_count':len(p['searches']),'page_count':len(p['searches']),'metadate_unice':len(ids),'mesaje_PECH_deja_arhivate':len(p['scoped_email_ids']),'perioada':p['period'],'paginare_completa':True,'control_integral_casute':True,'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'decizie_notificare':'DONT_NOTIFY','sursa':proof.relative_to(r).as_posix()}
note=f'''{day} {now.strftime('%H:%M:%S')} | CHECK-EMAIL PECH
Status scurt: Nicio comunicare, observatie contractuala, contrapropunere, pret, serviciu, termen, invitatie sau atasament PECH nou fata de verificarea 2026.10.29 16:01:36. Nicio nelivrare PECH identificata. Situatia ramane in asteptare, fara actiune noua.
Ultimul raspuns extern: 2026.10.27, Bernhard Ployer recomanda arhitectul Roland Gasperl si confirma discutia efectuata. Recomandare, nu mandat, oferta acceptata sau contract semnat.
Ultima trimitere: 2026.10.28 13:02:01 UTC+02:00, acces servieta digitala, ID 8fe2ffcc-a7e5-45a5-aab2-cb27e85e5860. Mesaj TRIMIS deja arhivat; nicio confirmare noua de primire sau functionare acces.
Urmatorul pas: {status['urmatorul_pas']}
Acoperire: {len(p['searches'])} cautari/{len(p['searches'])} pagini complete; {len(ids)} ID-uri unice de metadate; un mesaj PECH deja arhivat, zero noi. Control integral primit/trimis in office si Gmail, cautari globale domeniu, adrese, Ployer, PECH, Schallergasse, AN01/AN02/P2026-470 si nelivrari. {len(p['excluded_unrelated_email_ids'])} ID-uri din alte subiecte, excluse din controlul PECH. Sursele relevante sunt neschimbate SHA-256 fata de index; se reutilizeaza arhiva.
Indicatori ultima sincronizare EVA: office {local(sync['office@ac-wohnart.at'])}; Gmail {local(sync['covaciu.gnm@gmail.com'])}, UTC+02:00. Acestia sunt indicatorii afisati, nu dovada exhaustivitatii: unele rezultate au date mai recente. Mesajele neindexate pot lipsi; casutele shared/team necautabile sunt excluse. Registrul ramane la {len(reg['comunicatii'])} comunicatii; preluarea generala si sursele istorice nu sunt redefinite.
Monitorizare: check-email-pech ramane ACTIVE luni-vineri, 10:00,13:00,17:00 UTC+02:00. Dublura verificare-emailuri-pech, creata concomitent in alta conversatie cu programul vechi zilnic 10:00/16:00, a fost eliminata pentru a respecta noul program si a evita verificarile repetate. Configuratia veche este pastrata ca istoric.
Sursa: {proof.relative_to(r).as_posix()}; mesajele originale indicate in registru. Nu s-au trimis emailuri sau RSVP, modificat documente comerciale, semnat contracte ori efectuat plati. DONT_NOTIFY: nicio noutate PECH si nicio actiune noua.
'''
status['verificare_punctuala_PECH']={'checked_at_iso':stamp,'mesaje_noi':0,'sursa':entry['sursa']}
reg['acoperire']['verificare_punctuala_PECH']=entry;reg.setdefault('verificari_parteneri',[]).append(entry)
reg['monitorizare_PECH_actuala']={'id':'check-email-pech','status':'ACTIVE','program':'Luni-vineri 10:00,13:00,17:00 UTC+02:00','actualizat':day,'dublura_eliminata':'verificare-emailuri-pech'}
assert all(digest(reg[k])==v for k,v in before.items()) and reg['acoperire']['verificare_incrementala']==general
jsave(rp,reg); save(report,note)
for f in [r/(day+' Status proiect.txt'),r/(day+' Log progres proiect.txt'),r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'/(day+' Log discutii - Pech.txt'),b/'README.md']:
    save(f,note+'\nISTORIC PASTRAT\n\n'+f.read_text(encoding='utf-8-sig'))
jsave(proof,{'verificare':entry,'dovezi':p,'fisiere_reutilizate':checked,'surse_status':status['sursa_status'],'baseline_general_preserved':general,'nota':'Niciun mesaj sau atasament PECH nou de exportat. Metadatele cautarilor sunt salvate fara extrase; parolele nu sunt copiate.'})
save(o/(day+' ISTORIC automatizare PECH 10-16 eliminata.toml'),(b/'2026.10.29 Automatizare PECH veche 10-16.toml').read_text(encoding='utf-8'))
for f in [inv,b/'inventar.csv',b/'cautare.sqlite']:preserve(f)
db=sqlite3.connect(b/'cautare.sqlite')
for f in changed:
    if b in f.parents:continue
    rel=f.relative_to(r).as_posix();sha=hashlib.sha256(f.read_bytes()).hexdigest();txt=f.read_text(encoding='utf-8-sig');cache=b/'texte'/f'{sha}.txt';cache.write_text(txt,encoding='utf-8');st=f.stat();row=indexed.get(rel,{})
    row.update({'cale':rel,'folder':f.parent.relative_to(r).as_posix(),'extensie':f.suffix,'octeti':st.st_size,'modificat':datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Verificare email PECH - fara noutati; monitorizare consolidata','baza_descrierii':'verificare '+day,'extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(r).as_posix(),'detalii':{},'rezumat_verificat':'21 cautari, 53 metadate unice, un mesaj PECH deja arhivat, zero mesaje noi.','ocr_cache':''})
    indexed[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(indexed.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (b/'inventar.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps({'new_messages':0,'new_attachments':0,'decision':'DONT_NOTIFY','report':report.relative_to(r).as_posix(),'queries':len(p['searches']),'unique_metadata':len(ids),'registry_count':len(reg['comunicatii'])},ensure_ascii=False))
