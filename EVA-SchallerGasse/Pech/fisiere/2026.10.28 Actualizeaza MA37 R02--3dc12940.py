from pathlib import Path
import json, hashlib, shutil, datetime, csv, sqlite3, sys
from email.message import EmailMessage
from email.policy import SMTP
from email.parser import BytesParser
sys.stdout.reconfigure(encoding='utf-8')
R=Path.cwd(); B=R/'folder map'; O=R/'08. Corespondenta/2026.10.28 MA37 cerere planuri vizate'
payload=json.loads((B/'2026.10.28 MA37 R02 date verificate.json').read_text(encoding='utf-8'))
d=payload['draft']; assert d['status']=='pending' and len(d['attachments'])==6
assert d['attachments']==payload['before_draft']['attachments']
stamp=datetime.datetime.now().strftime('%H-%M-%S-%f')
backup=B/('2026.10.28 Istoric MA37 inainte R02 '+stamp); backup.mkdir()
def preserve(p):
    if p.exists():
        target=backup/p.relative_to(R); target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,target)
changed=[]
def save(p,content):
    preserve(p); p.write_text(content,encoding='utf-8'); changed.append(p)
old_path=O/'2026.10.28 Draft EVA si surse.json'
meta=json.loads(old_path.read_text(encoding='utf-8'))
meta.update({k:payload[k] for k in ['data','revizie','statut','draft','body_authored','verification']})
meta['source_update']={'data':'2026.10.28','tip':'mesaj utilizator in conversatie','text_original':payload['user_message'],'limita':'Vizita confirmata de utilizator; data vizitei nespecificata. Arhivarea in curs ramane ipoteza de verificat la MA37.'}
save(old_path,json.dumps(meta,ensure_ascii=False,indent=2))
head='2026.10.28 | R02 | DRAFT NETRIMIS\nExpeditor: '+d['account_email']+'\nDestinatari: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nID draft Eva-Mail: '+d['id']+'\nSubiect: '+d['subject']+'\n\n'
save(O/'2026.10.28 DRAFT MA37 cerere planuri vizate.txt',head+d['body'])
source='2026.10.28 | R02 | SURSA ACTUALIZARII\nSursa: mesaj utilizator in aceasta conversatie; nu email MA37.\nText original:\n'+payload['user_message']+'\n\nInterpretare pentru jurnal: vizita la arhiva confirmata de utilizator, data vizitei neprecizata. Arhiva detine numai plansele deja disponibile; lipsa documentelor la proiectant si ratacirea exemplarelor fostului proprietar sunt declarate de utilizator. Localizarea in circuitul intern / arhivarea in curs se solicita spre verificare, nu se prezinta ca fapt confirmat de autoritate.\nStatut email: DRAFT NETRIMIS; ID EVA '+d['id']+'; 6 atasamente originale pastrate.\n'
save(O/'2026.10.28 R02 Sursa vizita arhiva si cerere explicita.txt',source)
manifest=json.loads((O/'2026.10.28 Manifest atasamente.json').read_text(encoding='utf-8'))
by_id={m['eva_id']:m for m in manifest}
em=EmailMessage(); em['From']=d['account_email']; em['To']=', '.join(d['to']); em['Cc']=', '.join(d['cc']); em['Subject']=d['subject']; em['X-Unsent']='1'; em['X-Eva-Draft-ID']=d['id']; em['X-Project-Revision']='R02'; em.set_content(d['body'])
for a in d['attachments']:
    m=by_id[a['id']]; content=(R/m['local_path']).read_bytes()
    assert len(content)==a['size'] and hashlib.sha256(content).hexdigest()==m['sha256']
    em.add_attachment(content,maintype='application',subtype='pdf',filename=a['filename'])
ep=O/'2026.10.28 DRAFT NETRIMIS MA37 cerere planuri vizate.eml'; preserve(ep); ep.write_bytes(em.as_bytes(policy=SMTP)); changed.append(ep)
parsed=BytesParser(policy=SMTP).parsebytes(ep.read_bytes()); assert parsed['X-Unsent']=='1' and len(list(parsed.iter_attachments()))==6
for part,a in zip(parsed.iter_attachments(),d['attachments']):
    assert hashlib.sha256(part.get_payload(decode=True)).hexdigest()==by_id[a['id']]['sha256']
note='''2026.10.28 | MA37 R02 - CAUTARE INTERNA EXPLICITA A PLANURILOR VIZATE
Status scurt: draft german actualizat si recitit in EVA -> Drafts; NETRIMIS. Expeditor office@ac-wohnart.at; destinatar west@ma37.wien.gv.at; CC post@ma37.wien.gv.at; ID 2b13f782-3bdd-4720-8d16-c774ae404311. Cele 6 atasamente originale sunt pastrate.
Ultimul raspuns: utilizatorul confirma vizita efectuata la arhiva MA37, unde erau numai plansele deja detinute; proiectantul nu mai are documentele, iar fostul proprietar le-a ratacit. Data vizitei nu este precizata. Nu este un raspuns nou MA37 si nu se considera confirmata localizarea dosarului in curs de arhivare.
Cerere actualizata: cercetare interna la responsabilul de dosar / Gebietsgruppe West / registratura / alte servicii; verificare traseu si predare catre arhiva, ultimul loc documentat, stadiu, copii electronice, persoana responsabila si termen/loc consultare. Daca nu se gaseste, raspuns scris cu locurile verificate, actele ramase si procedura de stabilire a proiectului aprobat. Este explicata vizita deja efectuata, pentru a evita o simpla retrimitere generica la arhiva, proiectant sau fostul proprietar.
Urmatorul pas: utilizatorul trimite draftul din EVA, apoi obtinerea raspunsului concret si consultarea/copierea documentelor oficiale. Nu s-a trimis email si nu s-a rezervat un termen nou.
Sursa: 08. Corespondenta/2026.10.28 MA37 cerere planuri vizate/2026.10.28 R02 Sursa vizita arhiva si cerere explicita.txt; draft EVA recitit, JSON, text si EML cu 6 PDF originale. Versiunea anterioara pastrata in folder map. Acoperirea preluarii emailurilor ramane neschimbata.
'''
targets=[O/'2026.10.28 Jurnal pregatire MA37.txt',R/'2026.10.28 Status proiect.txt',R/'2026.10.28 Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log audit - MA37.txt',B/'README.md']
for p in targets:
    old=p.read_text(encoding='utf-8-sig') if p.exists() else ''
    save(p,note+'\nISTORIC PASTRAT\n\n'+old)
inv=B/'inventar.json'; csv_path=B/'inventar.csv'; db_path=B/'cautare.sqlite'
for p in [inv,csv_path,db_path]: preserve(p)
rows=json.loads(inv.read_text(encoding='utf-8')); indexed={x['cale']:x for x in rows}; db=sqlite3.connect(db_path)
for p in changed:
    if B in p.parents: continue
    rel=p.relative_to(R).as_posix(); raw=p.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
    txt=head+d['body']+'\nAtasamente: '+', '.join(a['filename'] for a in d['attachments']) if p.suffix=='.eml' else p.read_text(encoding='utf-8-sig')
    cache=B/'texte'/f'{sha}.txt'; cache.write_text(txt,encoding='utf-8'); st=p.stat(); row=indexed.get(rel,{})
    row.update({'cale':rel,'folder':p.parent.relative_to(R).as_posix(),'extensie':p.suffix,'octeti':st.st_size,'modificat':datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'MA37 R02 - cerere cautare interna planset aprobat; draft netrimis','baza_descrierii':'verificare 2026.10.28; mesaj utilizator si draft EVA recitit','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(R).as_posix(),'detalii':{},'rezumat_verificat':'Vizita arhiva confirmata de utilizator; circuitul intern si arhivarea in curs cerute spre verificare. DRAFT NETRIMIS.','ocr_cache':''})
    indexed[rel]=row; db.execute('DELETE FROM documente WHERE cale=?',(rel,)); db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit(); db.close(); rows=sorted(indexed.values(),key=lambda x:x['cale']); inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with csv_path.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)
print(json.dumps({'status':'DRAFT NETRIMIS','revision':'R02','draft_id':d['id'],'attachment_count':6,'attachment_hashes_verified':True,'files_updated':len(changed),'backup':backup.relative_to(R).as_posix(),'local_text':(O/'2026.10.28 DRAFT MA37 cerere planuri vizate.txt').relative_to(R).as_posix()},ensure_ascii=False,indent=2))
