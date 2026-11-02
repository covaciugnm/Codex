from pathlib import Path
import json,hashlib,shutil,sqlite3,datetime,csv
from docx import Document
root=Path.cwd(); base=root/'folder map'; out=root/'00.Proiect/09. Vertraege/zt-pech.at/2026.10.27 Kurzvertrag Checkliste'
stamp=datetime.datetime.now().astimezone(); backup=base/('2026.10.27 Istoric contract scurt PECH '+stamp.strftime('%H-%M-%S'));backup.mkdir()
def preserve(p):
 b=backup/p.relative_to(root);b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
req=out/'2026.10.27 Cerere utilizator.txt'
req.write_text('2026.10.27 | Cerere utilizator in conversatie\nStatut: informare primita de la utilizator; nu email PECH verificat.\nExpeditor: utilizator; destinatar: asistent; CC: nu se aplica; ID Eva-Mail: nu se aplica.\nText original:\nPech solicită o versiune mai simplă de contract model checklist pornind de la ce a ofertat și ce am pus în checklistul inițial când am cerut prima dată oferta. Mai scurt clar și concis fără multă vorbă -\n',encoding='utf-8')
manifest=json.loads((out/'2026.10.27 Surse si diferente.json').read_text(encoding='utf-8'))
sd=out/'Surse';sd.mkdir(exist_ok=True)
for key in ['PECH_AN01','PECH_AN02','PECH_EMAIL','CERERE_INITIALA']:
 p=root/manifest['surse'][key]['cale'];shutil.copy2(p,sd/p.name)
email=next((root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/Pech').glob('2026.07.20*.txt'));shutil.copy2(email,sd/email.name)
body='2026.10.27 | PROPUNERE CONTRACT SCURT PECH\nStatus scurt: creat Word in germana, 3 pagini, tip checklist, DRAFT NETRIMIS / NESEMNAT. Baza: cererea initiala trimisa 2026.07.20, AN01 2026.09.17, AN02 si observatiile PECH 2026.10.21. AN01 69.300 EUR net + AN02 8.300 EUR net = 77.600 EUR net, neacceptat.\nUltimul raspuns: utilizatorul relateaza astazi solicitarea PECH de simplificare; nu este un email PECH nou verificat si nu confirma alte rezultate ale intalnirii.\nUrmatorul pas: discutarea checklistului cu PECH, completarea optiunilor, termenelor, rolurilor si eventualelor costuri; apoi versiune finala pentru semnare.\nSursa: '+out.relative_to(root).as_posix()+'; 2026.10.27 Cerere utilizator.txt si 2026.10.27 Surse si diferente.json.\nVerificare: 3 pagini exportate prin Word si inspectate vizual. Fara trimitere email, semnare ori modificarea R09. Acoperirea EVA ramane neschimbata.'
targets=[root/'2026.10.27 Status proiect.txt',root/'2026.10.27 Log progres proiect.txt',root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.27 Log discutii - Pech.txt',base/'README.md']
for p in targets:
 preserve(p);old=p.read_text(encoding='utf-8-sig');p.write_text(body+'\n\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
(out/'2026.10.27 Jurnal pregatire.txt').write_text(body,encoding='utf-8')
# Targeted incremental refresh: no reread of the archive, folder map excluded.
inv=base/'inventar.json';preserve(inv);rows=json.loads(inv.read_text(encoding='utf-8'));by={x['cale']:x for x in rows}
db=sqlite3.connect(base/'cautare.sqlite')
files=list(out.rglob('*'))+[p for p in targets if base not in p.parents]
for p in files:
 if not p.is_file():continue
 rel=p.relative_to(root).as_posix();sha=hashlib.sha256(p.read_bytes()).hexdigest();cache=base/'texte'/f'{sha}.txt'
 if p.suffix=='.docx':
  d=Document(p);txt='\n'.join(x.text for x in d.paragraphs)+'\n'+'\n'.join(' | '.join(c.text for c in row.cells) for t in d.tables for row in t.rows)
 elif p.suffix=='.pdf':
  from pypdf import PdfReader
  txt='\n'.join(pg.extract_text() or '' for pg in PdfReader(p).pages)
 else:txt=p.read_text(encoding='utf-8-sig')
 cache.write_text(txt,encoding='utf-8');st=p.stat()
 row=by.get(rel,{});row.update({'cale':rel,'folder':p.parent.relative_to(root).as_posix(),'extensie':p.suffix,'octeti':st.st_size,'modificat':datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':'','ce_reprezinta':'Propunere scurta PECH si surse / actualizare jurnal','baza_descrierii':'actualizare punctuala 2026.10.27','extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras','text_cache':cache.relative_to(root).as_posix(),'detalii':{},'rezumat_verificat':'Draft netrimis; nu acceptare contractuala.' if 'Kurzvertrag PECH Checkliste' in p.name else '', 'ocr_cache':''})
 by[rel]=row;db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(by.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
cp=base/'inventar.csv';preserve(cp)
with cp.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
(base/'2026.10.27 QA contract scurt PECH/2026.10.27 Verificare finala.json').write_text(json.dumps({'data':'2026.10.27','pagini':3,'verificare_vizuala':'Toate cele 3 pagini verificate; titlu fara linie, tabele si semnaturi integrale.','renderer':'render_docx.py indisponibil: LibreOffice lipseste; fallback Word ExportAsFixedFormat si pypdfium2','index':'inventar.json, inventar.csv si cautare.sqlite actualizate punctual; folder map exclus','surse_neschimbate':all(s['neschimbat_fata_de_index'] for s in manifest['surse'].values()),'statut':'DRAFT NETRIMIS NESEMNAT'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Jurnale si index actualizate; '+str(len(files))+' intrari candidate.')
