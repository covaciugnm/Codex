from pathlib import Path
import json,hashlib,shutil,sqlite3,datetime,csv
from pypdf import PdfReader
R=Path.cwd();B=R/'folder map';O=R/'00.Proiect/2026.10.27 Audit autorizare si servieta';Q=B/'2026.10.27 QA autorizare'
backup=B/('2026.10.27 Istoric audit autorizare '+datetime.datetime.now().strftime('%H-%M-%S'));backup.mkdir()
def preserve(p):
 if p.exists():
  dest=backup/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
body='''2026.10.27 | AUDIT ACTE MA37 SI SERVIETA
Status scurt: raport PDF final, 16 pagini cu anexe si inventare incorporabile; dosarul actual complet/semnat nu este demonstrat. Exista Bescheid 2023.04.21; planul vizat MA37 si data Rechtskraft raman de confirmat. Energieausweis prezent, valabilitate inscrisa 2031.12.20, rubrica semnaturii goala. Modificarile actuale necesita incadrare si documentatie coordonata.
Servieta: P1-P17 accesibile, 184 fisiere/183 continuturi unice; 118 fisiere identice SHA-256 cu local, 66 versiuni fara corespondent identic. P10 si P13-P17 goale. P18-P20 blocate pentru contul PECH; neinspectate. Nucleu 00.Proiect fara contracte/.md: 110 fisiere/109 unice, 90 continuturi fara copie identica online. Nu echivaleaza cu 90 acte obligatorii lipsa.
Ultimul raspuns: cerere utilizator in conversatie; nu raspuns nou MA37 sau PECH. Autentificarea permite numai verificarea contului; nu s-au schimbat documente pe site.
Urmatorul pas: obtinerea planurilor vizate si confirmarii Rechtskraft; PECH/proiectant sa stabileasca procedura si lista anexelor actualizate/semnate; reconcilierea versiunilor online si a denumirii eronate Einreichplan/Bestandsplan.
Sursa: 00.Proiect/2026.10.27 Audit autorizare si servieta/2026.10.27 Schallergasse 35 - Audit acte MA37 si servieta.pdf; folder map/2026.10.27 QA autorizare (ZIP-uri, comparatii SHA-256, imagini originale).
Fara depunere, email trimis, contract acceptat sau validare criptografica. Acoperirea Eva-Mail anterioara ramane neschimbata.
'''
(O/'2026.10.27 Jurnal audit.txt').write_text(body,encoding='utf-8')
(O/'2026.10.27 Cerere utilizator.txt').write_text('2026.10.27 | Sursa: conversatie; statut: cerere primita de la utilizator, nu email. Expeditor: utilizator; destinatar: asistent; CC si ID Eva-Mail: nu se aplica.\nSolicitare: verificarea actelor Schallergasse necesare autorizarii la Viena, inclusiv stampile/semnaturi, inventarul existent si comparatia tuturor documentelor accesibile in servieta ac-wohnart.at; rezultat intr-un document. Datele de autentificare nu sunt incluse.\n',encoding='utf-8')
targets=[R/'2026.10.27 Status proiect.txt',R/'2026.10.27 Log progres proiect.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.27 Log discutii - Pech.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.27 Log audit - MA37.txt',B/'README.md']
for p in targets:
 preserve(p);old=p.read_text(encoding='utf-8-sig') if p.exists() else '';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body+'\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
inv=B/'inventar.json';preserve(inv);rows=json.loads(inv.read_text(encoding='utf-8'));by={x['cale']:x for x in rows};db=sqlite3.connect(B/'cautare.sqlite')
files=[p for p in O.rglob('*') if p.is_file()]+[p for p in targets if B not in p.parents]
for p in files:
 rel=p.relative_to(R).as_posix();sha=hashlib.sha256(p.read_bytes()).hexdigest();cache=B/'texte'/f'{sha}.txt'
 txt='\n'.join(pg.extract_text() or '' for pg in PdfReader(p).pages) if p.suffix=='.pdf' else p.read_text(encoding='utf-8-sig');cache.write_text(txt,encoding='utf-8');st=p.stat()
 row=by.get(rel,{});row.update({'cale':rel,'folder':p.parent.relative_to(R).as_posix(),'extensie':p.suffix,'octeti':st.st_size,'modificat':datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Audit MA37 si comparatie servieta online','baza_descrierii':'verificare documentara 2026.10.27','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(R).as_posix(),'detalii':{},'rezumat_verificat':'Concluzii cu limite; nu depunere sau confirmare de autoritate.','ocr_cache':''});by[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(by.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');cp=B/'inventar.csv';preserve(cp)
with cp.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
(Q/'2026.10.27 Verificare finala.json').write_text(json.dumps({'data':'2026.10.27','pagini':16,'QA':'Contact sheet toate paginile; fara taieri; anexe integrate; rubrici si semnaturi verificate numai in paginile explicit mentionate','index':'actualizat punctual JSON CSV SQLite, folder map exclus','site':'read-only; P18-P20 neinspectate'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Raport, jurnale si index salvate.')
