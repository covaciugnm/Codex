from pathlib import Path
import json,hashlib
from pypdf import PdfReader,PdfWriter
B=Path(__file__).parent
rs=json.loads((B/'records.json').read_text(encoding='utf-8'));prs=json.loads((B/'projects.json').read_text(encoding='utf-8'))
paths=[Path(x) for x in (B/'paths.txt').read_text(encoding='utf-8-sig').splitlines()]
maps={'9282144560':[('Licență economist Florin',5,5),('Diplomă inginer Florin',6,6),('Certificat ANEVAR bunuri mobile Florin',7,7),('Certificat CECCAR evaluare întreprinderi Florin',8,8),('Certificat ANEVAR proprietăți imobiliare Florin',9,9),('Certificat Formator și supliment Florin',10,11),('Adeverință ELEN nr228 din24.02.2014 Florin',12,12),('Contract individual muncă ELEN Florin',13,16),('Fișă post expert local ELEN Florin',17,21),('Criterii evaluare post ELEN Florin',22,22),('Contract individual muncă GAL Florin',23,28)],'2ab2af8759':[('Licență terapie ocupațională Szoke',7,8),('Diplomă bacalaureat Szoke',9,10),('Certificat antreprenor economie socială Szoke',11,13),('Certificat inspector resurse umane Szoke',14,14),('Recomandare activitate copil6ani Szoke',16,16),('Certificat voluntariat ROSE Szoke',20,20),('Contract voluntariat ROSE Szoke',21,25)],'611216dbe2':[('Diplomă licență psihologie Ilinca și verso',4,5)]}
for pr in prs:
 for k,acts in maps.items():
  source=next(p for p in paths if k in p.name and p.suffix.lower()=='.pdf');r=PdfReader(source)
  for idx,(title,a,z) in enumerate(acts):
   name=''.join(c if c.isalnum() else '_' for c in title)[:80]+'.pdf'
   folder=10 if 'voluntariat' in title else 8
   parent=next(x for x in Path(pr['out']).iterdir() if x.is_dir() and x.name.startswith(f'{folder:02} '))
   target=parent/'Acte individuale'/name;target.parent.mkdir(exist_ok=True)
   w=PdfWriter()
   for pg in range(a-1,z):w.add_page(r.pages[pg])
   with target.open('wb') as f:w.write(f)
   rs.append(dict(project=pr['id'],folder=folder,title=title,status='Copiat verificat',source=str(source)+f' | pagini {a}-{z}',dest=str(target),obs='Copie extrasă din dosarul justificativ, verificată vizual; nu este autentificare. SHA256 '+hashlib.sha256(target.read_bytes()).hexdigest(),owner='Titular / ROSE',signer='',required='Suport',action='Corelați cu rolul și CV-ul actualizat.',due='2026-11-02T16:00:00',email_due='2026-11-03T00:00:00'))
 # Each CV has a traceable original source, rather than an unspecified reference.
 for row in rs:
  if row['project']!=pr['id']:continue
  title=row['title']
  if title.startswith('CV_'):
   k='2ab2af8759' if 'Szoke' in title else '9282144560' if 'Florin' in title else '611216dbe2' if 'Ilinca' in title else '25a2cc09c3'
   p=next(p for p in paths if k in p.name)
   row['source']=str(p)
   row['obs']+=' | CV redactat la02.11.2026 din sursa indicată; perioadele deschise nu sunt extinse automat.'
 for person in ['Szoke Andrei-Alexandru','Neamțiu Toader-Florin','Neamțiu Ilinca-Mariana','Covaciu Cosmin-Adrian']:
  for typ in ['CV datat și semnat pe fiecare pagină','Declarație disponibilitate completată și semnată']:
   rs.append(dict(project=pr['id'],folder=8 if typ.startswith('CV') else 9,title=typ+' – '+person,status='Lipsa semnatura',source='Anunț '+pr['num']+' secțiunea2.2',dest='',obs='Există variantă de lucru; semnătura titularului nu a fost aplicată. Rolul și orele se confirmă.',owner=person,signer=person,required='Opțional' if 'Cosmin' in person else 'Obligatoriu',action='Validați conținutul și semnați personal; apoi scanați PDF.',due='2026-11-02T16:00:00',email_due='2026-11-03T00:00:00'))
 for row in rs:
  if row['project']==pr['id'] and row['title'].startswith('Diplome și certificate '):row['required']='Dosar suport consolidat';row['obs']+=' | Actele sunt evidențiate individual în registru.'
# Stable identifiers and real file availability are generated at export time.
for i,r in enumerate(rs,1):r['id']=f"P{r['project']}-{sum(1 for x in rs[:i] if x['project']==r['project']):03}"
(B/'records.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2),encoding='utf-8')
print('records',len(rs))
