from pathlib import Path
import json, tomllib, hashlib, shutil, datetime, csv, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd(); b=r/'folder map'; a=Path('C:/Users/User/.codex/automations/check-email-pech/automation.toml')
d=tomllib.loads(a.read_text(encoding='utf-8'))
assert d['status']=='ACTIVE' and d['rrule']=='FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=10,13,17;BYMINUTE=0;BYSECOND=0'
o=r/'08. Corespondenta/2026.10.29 Programare check-email PECH'; o.mkdir(exist_ok=True)
backup=b/('2026.10.29 Istoric programare PECH '+datetime.datetime.now().strftime('%H-%M-%S-%f')); backup.mkdir()
changed=[]
def save(p,s):
    if p.exists():
        q=backup/p.relative_to(r);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    p.write_text(s,encoding='utf-8'); changed.append(p)
evidence={'data':'2026.10.29','status':'ACTIVE','name':d['name'],'id':d['id'],'schedule_readable':'Luni-vineri, 10:00, 13:00 si 17:00, fusul aplicatiei UTC+02:00','target_thread_id':d['target_thread_id'],'created_at':d['created_at'],'updated_at':d['updated_at'],'prompt':d['prompt'],'source':'Cererea utilizatorului: seteaza reminderul check-email pentru Pech la 10.00, 13.00 si 17.00; completare: in zilele lucratoare. Configurare prin automation_update, recitita din automation.toml.','limite':'Nu reprezinta o noua verificare a emailurilor sau un email trimis. Monitorizarea generala a proiectului ramane separata.'}
save(o/'2026.10.29 Configurare verificata PECH.json',json.dumps(evidence,ensure_ascii=False,indent=2))
note='''2026.10.29 | CHECK-EMAIL PECH - PROGRAMARE ACTIVA
Status scurt: automatizare dedicata PECH activa luni-vineri la 10:00, 13:00 si 17:00, fusul aplicatiei UTC+02:00. ID check-email-pech; rezultatele revin in conversatia 01a17d72-f016-7252-8121-a17345dfc047. Configuratia a fost recitita si validata dupa salvare.
Ultimul raspuns: instructiunea utilizatorului pentru programare, completata cu zilele lucratoare; nu este raspuns nou PECH si nu s-au verificat emailuri in aceasta operatiune.
Urmatorul pas: verificarile programate cauta noutati PECH in Eva-Mail, compara cu registrul pentru a evita repetarea, salveaza mesajele/atasamentele relevante si actualizeaza jurnalele si indexul. Continua pana la oprire explicita. Monitorizarea generala de proiect este separata; automatizarea BERGER isi pastreaza configuratia curenta.
Sursa: 08. Corespondenta/2026.10.29 Programare check-email PECH/2026.10.29 Configurare verificata PECH.json; automation_update si configuratia locala recitita. Niciun email trimis, document comercial modificat sau contract acceptat. Acoperirea istorica a emailurilor nu este extinsa prin aceasta programare.
'''
save(o/'2026.10.29 Programare check-email PECH.txt',note)
for p in [r/'2026.10.29 Status proiect.txt',r/'2026.10.29 Log progres proiect.txt',r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - Pech.txt',b/'README.md']:
    old=p.read_text(encoding='utf-8-sig') if p.exists() else ''
    save(p,note+'\nISTORIC PASTRAT\n\n'+old)
inv=b/'inventar.json'; cp=b/'inventar.csv'; dp=b/'cautare.sqlite'
for p in [inv,cp,dp]:shutil.copy2(p,backup/p.name)
rows=json.loads(inv.read_text(encoding='utf-8')); by={x['cale']:x for x in rows}; db=sqlite3.connect(dp)
for p in changed:
    if b in p.parents:continue
    rel=p.relative_to(r).as_posix(); sha=hashlib.sha256(p.read_bytes()).hexdigest();txt=p.read_text(encoding='utf-8-sig');c=b/'texte'/f'{sha}.txt';c.write_text(txt,encoding='utf-8'); st=p.stat();row=by.get(rel,{})
    row.update({'cale':rel,'folder':p.parent.relative_to(r).as_posix(),'extensie':p.suffix,'octeti':st.st_size,'modificat':datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Programare check-email PECH activa, luni-vineri 10:00 13:00 17:00','baza_descrierii':'Configuratie recitita 2026.10.29','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':c.relative_to(r).as_posix(),'detalii':{},'rezumat_verificat':'Programare activa; nu verificare noua de emailuri.','ocr_cache':''})
    by[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(by.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with cp.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print('PECH: ACTIVE; luni-vineri 10:00, 13:00, 17:00. Jurnale si index actualizate.')
