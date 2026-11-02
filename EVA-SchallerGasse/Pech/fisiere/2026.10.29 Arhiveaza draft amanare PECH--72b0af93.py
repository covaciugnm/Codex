from pathlib import Path
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from email.policy import SMTP
import json, hashlib, shutil, sqlite3, csv, sys
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd(); b=r/'folder map'; p=json.loads((b/'2026.10.29 PECH amanare date verificate.json').read_text(encoding='utf-8'));d=p['draft']
assert d['status']=='pending' and d['account_email']=='office@ac-wohnart.at' and d['to']==['ployer@zt-pech.at'] and d['cc']==['sekretariat@zt-pech.at'] and not d['attachments']
o=r/'08. Corespondenta/2026.10.29 PECH amanare intalnire';o.mkdir(exist_ok=True)
now=datetime.now(timezone(timedelta(hours=2)));stamp=now.isoformat(timespec='seconds');hist=b/('2026.10.29 Istoric draft amanare PECH '+now.strftime('%H-%M-%S'));hist.mkdir()
changed=[]
def preserve(f):
    if f.exists():
        q=hist/f.relative_to(r);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,q)
def save(f,text):
    preserve(f);f.write_text(text,encoding='utf-8');changed.append(f)
def jsave(f,obj):save(f,json.dumps(obj,ensure_ascii=False,indent=2))
df=o/'2026.10.29 DRAFT PECH amanare - EVA.json'; jsave(df,p)
head='2026.10.29 | DRAFT NETRIMIS\nExpeditor: '+d['account_email']+'\nDestinatari: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nID draft Eva-Mail: '+d['id']+'\nSubiect: '+d['subject']+'\nAtasamente: niciunul\n\n'
tf=o/'2026.10.29 DRAFT PECH amanare.txt'; save(tf,head+d['body'])
em=EmailMessage();em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Cc']=', '.join(d['cc']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-Eva-Draft-ID']=d['id'];em.set_content(d['body'])
ef=o/'2026.10.29 DRAFT NETRIMIS PECH amanare.eml';preserve(ef);ef.write_bytes(em.as_bytes(policy=SMTP));changed.append(ef)
note=f'''2026.10.29 | DRAFT PECH - MULTUMIRI, RECUPERARE ACTE SI AMANARE
Status scurt: draft german salvat si recitit in EVA, NETRIMIS; expeditor office@ac-wohnart.at; catre DI Bernhard Ployer, ployer@zt-pech.at, CC sekretariat@zt-pech.at; ID {d['id']}; fara atasamente. Ployer este interlocutorul din emailul PECH dupa intalnirea efectuata.
Continut: multumiri pentru discutia utila si instructiva; speranta rezolvarii rapide a problemei identificate; demersuri paralele prin avocat, fost proprietar, arhitectul initial si primarie; indicii privind originalele la Baupolizei, cu verificare in curs. Se propune amanarea urmatoarei discutii pana marti, 2026.11.03, pentru primele raspunsuri; ora de propus de destinatar. Text generic, fara detalii juridice sau date din dosar.
Ultimul raspuns relevant consultat: Capra 2026.10.29, ID 478abcb0-1094-4b10-b3e4-ecbc02840715, cere MA37 confirmarea existentei actelor si acces la Bauakt/Uberwachungsakt. Emailul MA37 din 2025.11.19 arata ca proiectul nu era in Hauseinlage, cu trimitere la Uberwachungsakt. Nu exista confirmare noua de recuperare/localizare completa a originalelor. Demersurile la fostul proprietar/arhitect sunt declarate de utilizator.
Urmatorul pas: utilizatorul poate trimite draftul din EVA; asteptarea raspunsului PECH privind 2026.11.03 si ora, precum si a primelor raspunsuri privind actele. Amanarea este numai PROPUSA; nu este acceptata si calendarul nu a fost modificat. Nicio acceptare de oferta/contract.
Sursa: {df.relative_to(r).as_posix()}; sursele Capra/MA37 si PECH sunt indicate in JSON, cu mesajul Capra recitit integral si surse locale neschimbate fata de index. Cautare punctuala Capra astazi, nu sincronizare generala.
'''
save(o/'2026.10.29 Jurnal draft amanare PECH.txt',note)
rp=r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.29 Registru comunicatii.json';reg=json.loads(rp.read_text(encoding='utf-8'));before=hashlib.sha256(json.dumps(reg['comunicatii'],sort_keys=True).encode()).hexdigest()
entry={'id':d['id'],'partener':'Pech','status':'pending','statut':'DRAFT NETRIMIS','account_email':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'bcc':d['bcc'],'subiect':d['subject'],'created_at':d['created_at'],'data_verificarii':stamp,'atasamente':[],'sursa':df.relative_to(r).as_posix(),'cale':tf.relative_to(r).as_posix(),'eml':ef.relative_to(r).as_posix(),'intalnire_propusa':p['meeting']}
assert not any(x.get('id')==d['id'] for x in reg['drafturi']);reg['drafturi'].append(entry)
status=next(x for x in reg['statusuri'] if x.get('partener')=='Pech');status['draft_amanare_2026_11_03']=entry
assert before==hashlib.sha256(json.dumps(reg['comunicatii'],sort_keys=True).encode()).hexdigest();jsave(rp,reg)
for f in [r/'2026.10.29 Status proiect.txt',r/'2026.10.29 Log progres proiect.txt',r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - Pech.txt',b/'README.md']:
    save(f,note+'\nISTORIC PASTRAT\n\n'+f.read_text(encoding='utf-8-sig'))
inv=b/'inventar.json';cp=b/'inventar.csv';dp=b/'cautare.sqlite'
for f in [inv,cp,dp]:preserve(f)
rows=json.loads(inv.read_text(encoding='utf-8'));indexed={x['cale']:x for x in rows};db=sqlite3.connect(dp)
for f in changed:
    if b in f.parents:continue
    rel=f.relative_to(r).as_posix();sha=hashlib.sha256(f.read_bytes()).hexdigest();txt=head+d['body'] if f.suffix=='.eml' else f.read_text(encoding='utf-8-sig');cache=b/'texte'/f'{sha}.txt';cache.write_text(txt,encoding='utf-8');st=f.stat();row=indexed.get(rel,{})
    row.update({'cale':rel,'folder':f.parent.relative_to(r).as_posix(),'extensie':f.suffix,'octeti':st.st_size,'modificat':datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Draft PECH multumiri si propunere amanare 2026.11.03','baza_descrierii':'draft EVA recitit 2026.10.29','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(r).as_posix(),'detalii':{},'rezumat_verificat':'NETRIMIS; marti 2026.11.03 propus, ora nefixata; fara confirmare de recuperare a actelor.','ocr_cache':''})
    indexed[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(indexed.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with cp.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps({'draft_id':d['id'],'status':d['status'],'local_text':tf.relative_to(r).as_posix(),'meeting_proposed':p['meeting'],'archive_and_index_updated':True},ensure_ascii=False))
