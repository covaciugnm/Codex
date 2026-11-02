from pathlib import Path
from datetime import datetime, timezone, timedelta
import json,hashlib,shutil,csv,sqlite3,sys
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd();b=r/'folder map';now=datetime.now(timezone(timedelta(hours=2)));day=now.strftime('%Y.%m.%d');tag=now.strftime('%H-%M-%S');stamp=now.isoformat(timespec='seconds')
p=json.loads((b/'2026.10.30 Dovezi check-email PECH 10.json').read_text(encoding='utf-8'))
assert day=='2026.10.30' and not p['errors'] and not p['scoped_email_ids'] and p['draft_readback']['status']=='pending'
assert all(s['args']['offset']+len(s['result']['items'])>=s['result']['total'] for s in p['searches'])
ids={x['id'] for s in p['searches'] for x in s['result']['items']};assert ids==set(p['excluded_email_ids'])
rp=r/p['baseline']['register_path'];reg=json.loads(rp.read_text(encoding='utf-8'));status=next(x for x in reg['statusuri'] if x.get('partener')=='Pech')
inv=b/'inventar.json';cp=b/'inventar.csv';dp=b/'cautare.sqlite';rows=json.loads(inv.read_text(encoding='utf-8'));indexed={x['cale']:x for x in rows}
checked=[]
for rel in status['sursa_status']+[status['draft_amanare_2026_11_03']['sursa']]:
    sha=hashlib.sha256((r/rel).read_bytes()).hexdigest();assert sha==indexed[rel]['sha256'];checked.append({'cale':rel,'sha256':sha,'unchanged':True})
prior=json.loads((r/status['draft_amanare_2026_11_03']['sursa']).read_text(encoding='utf-8'))['draft']
assert all(prior[k]==p['draft_readback'][k] for k in ['id','status','body','subject','to','cc','attachments'])
out=r/'08. Corespondenta'/(day+' Check-email PECH');out.mkdir(exist_ok=True);hist=b/(day+' Istoric check-email PECH '+tag);hist.mkdir();changed=[]
def preserve(f):
    if f.exists():
        q=hist/f.relative_to(r);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,q)
def save(f,t):preserve(f);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(t,encoding='utf-8');changed.append(f)
def jsave(f,d):save(f,json.dumps(d,ensure_ascii=False,indent=2))
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def local(v):return datetime.fromisoformat(v.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=2))).strftime('%Y.%m.%d %H:%M:%S') if v else 'indisponibil'
proof=out/(day+' '+tag+' Dovezi check-email PECH.json');report=out/(day+' '+tag+' Raport check-email PECH.txt')
primary={x['email']:x.get('last_sync') for x in p['mailboxes_primary']['mailboxes']};secondary={x['email']:x.get('last_sync') for x in p['mailboxes_secondary']['mailboxes']}
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Pech'],'mesaje_noi':0,'atasamente_noi':0,'query_count':len(p['searches']),'page_count':len(p['searches']),'metadate_unice':len(ids),'perioada':p['period'],'paginare_completa':True,'control_integral_casute':True,'sincronizare_office':primary['office@ac-wohnart.at'],'sincronizare_gmail':primary['covaciu.gnm@gmail.com'],'sincronizare_office_secundar':secondary['office@ac-wohnart.at'],'draft_amanare_status':'pending','decizie_notificare':'DONT_NOTIFY','sursa':proof.relative_to(r).as_posix()}
note=f'''{day} {now.strftime('%H:%M:%S')} | CHECK-EMAIL PECH
Status scurt: Nicio noutate PECH fata de verificarea generala de astazi la 08:15:47. Nu s-au identificat raspunsuri, observatii contractuale, contrapropuneri, modificari de pret/servicii, termene, programari, atasamente sau nelivrari PECH noi.
Ultimul raspuns extern: 2026.10.27, DI Bernhard Ployer recomanda arhitectul Roland Gasperl si confirma discutia efectuata; nu reprezinta mandat sau acceptare contractuala.
Ultima trimitere cunoscuta: 2026.10.28 13:02:01 UTC+02:00, acces servieta, ID 8fe2ffcc-a7e5-45a5-aab2-cb27e85e5860; fara confirmare noua a primirii/functionarii.
Draftul de multumiri si amanare: ebe46e54-bdee-407a-971f-1025f67f6482, recitit si in continuare pending/NETRIMIS. Corpul, subiectul, destinatarii si lipsa atasamentelor sunt identice versiunii arhivate. Marti 2026.11.03 si ora ramasa de stabilit sunt doar propunere; nicio acceptare a amanarii. Stare cunoscuta, fara notificare repetata.
Urmatorul pas: trimiterea draftului de catre utilizator si ulterior confirmarea zilei/orei de catre PECH; urmarirea raspunsului comercial, documentelor necesare si demersurilor pentru recuperarea actelor. Punctele tehnice/comerciale anterior consemnate raman deschise.
Acoperire: {len(p['searches'])} cautari/{len(p['searches'])} pagini complete; perioada 2026.10.29-2026.10.30, cu suprapunere de o zi. {len(ids)} ID-uri de metadate, zero relevante PECH: 26 Gmail din alte subiecte si 16 ID-uri office (8 mesaje de proiect deja inregistrate si 8 aliasuri din cealalta conexiune). Control integral primit/trimis office in ambele conexiuni si Gmail Primary, cautari globale PECH/adrese/Ployer/Schallergasse/AN01/AN02/P2026-470/nelivrari. Originalele relevante neschimbate SHA-256 fata de index au fost reutilizate.
Indicatori sincronizare UTC+02:00: Primary office {local(primary['office@ac-wohnart.at'])}; Gmail {local(primary['covaciu.gnm@gmail.com'])}; a doua conexiune office {local(secondary['office@ac-wohnart.at'])}. Sunt indicatori afisati, nu dovada exhaustivitatii; unele rezultate pot avea data mai recenta. Mesajele neindexate pot lipsi; casutele shared/team necautabile sunt excluse.
Sursa: {proof.relative_to(r).as_posix()}. Registrul comunicatiilor si istoricul ciornelor sunt pastrate. Nu exista mesaje/atasamente PECH noi de exportat. Nu s-au trimis emailuri/RSVP, modificat calendarul, documente comerciale sau automatizarea, semnat ori platit. DONT_NOTIFY: situatie neschimbata, fara actiune noua.
'''
before={k:digest(reg[k]) for k in ['comunicatii','drafturi']};general=reg['acoperire']['verificare_incrementala'].copy()
status['verificare_punctuala_PECH']={'checked_at_iso':stamp,'mesaje_noi':0,'draft_amanare_status':'pending','sursa':entry['sursa']};reg['acoperire']['verificare_punctuala_PECH']=entry;reg.setdefault('verificari_parteneri',[]).append(entry)
assert all(digest(reg[k])==v for k,v in before.items()) and reg['acoperire']['verificare_incrementala']==general
jsave(rp,reg);save(report,note);jsave(proof,{'verificare':entry,'dovezi':p,'surse_reutilizate':checked,'draft_unchanged':True,'register_count':len(reg['comunicatii']),'general_baseline_preserved':general})
for f in [r/(day+' Status proiect.txt'),r/(day+' Log progres proiect.txt'),r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'/(day+' Log discutii - Pech.txt'),b/'README.md']:
    old=f.read_text(encoding='utf-8-sig') if f.exists() else '';save(f,note+'\nISTORIC PASTRAT\n\n'+old)
for f in [inv,cp,dp]:preserve(f)
db=sqlite3.connect(dp)
for f in changed:
    if b in f.parents:continue
    rel=f.relative_to(r).as_posix();sha=hashlib.sha256(f.read_bytes()).hexdigest();txt=f.read_text(encoding='utf-8-sig');cache=b/'texte'/f'{sha}.txt';cache.write_text(txt,encoding='utf-8');st=f.stat();row=indexed.get(rel,{})
    row.update({'cale':rel,'folder':f.parent.relative_to(r).as_posix(),'extensie':f.suffix,'octeti':st.st_size,'modificat':datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Verificare PECH fara noutati; draft amanare pending','baza_descrierii':'verificare '+day,'extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(r).as_posix(),'detalii':{},'rezumat_verificat':'25 cautari, 42 metadate; zero mesaje PECH noi. Draft amanare NETRIMIS, situatie cunoscuta.','ocr_cache':''})
    indexed[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(indexed.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with cp.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps({'report':report.relative_to(r).as_posix(),'decision':'DONT_NOTIFY','new_messages':0,'draft':'pending','register_count':len(reg['comunicatii'])},ensure_ascii=False))
