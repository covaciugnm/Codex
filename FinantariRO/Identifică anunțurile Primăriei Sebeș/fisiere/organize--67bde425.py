from pathlib import Path
import json,shutil,hashlib,re
from pypdf import PdfReader,PdfWriter
B=Path(__file__).parent
ROOT=Path(r'\\192.168.100.169\Comun\00. Proiecte 2026')
paths=[Path(x) for x in (B/'paths.txt').read_text(encoding='utf-8-sig').splitlines()]
folders=['00 Procedura si modele oficiale','01 A Scrisoare de intentie','02 Fisa partenerului','03 B Declaratie eligibilitate','04 B Resurse si cofinantare','05 B Numar proiecte in apel','06 B Spatii de lucru','07 B Acte statutare si reprezentare','08 B CV si documente experti','09 C Disponibilitate experti','10 Voluntariat si experienta individuala','11 C Bilanturi 2022-2025','12 C Balante analitice 2022-2025','13 C Certificate fiscale','14 C Experienta organizatiei si punctaj','15 C Nota justificativa','16 C Activitati si subactivitati','17 Opis si numerotare','18 Adresa de inaintare','19 Audit si corecturi']
projects=[]
for i,num,title in [(1,'78398','Acces egal la educație timpurie în municipiul Sebeș'),(2,'78418','Diversificarea serviciilor de educație timpurie în Municipiul Sebeș')]:
 src=next(ROOT.glob(f'*/ANUNT {i}/ANUNT {i}'))
 out=src.parents[1]/'3. DOSAR SELECTIE PARTENER ROSE - 02.11.2026'
 for f in folders:(out/f).mkdir(parents=True,exist_ok=True)
 projects.append(dict(id=i,num=num,title=title,source=str(src),out=str(out)))
records=[]
def record(pr,folder,title,status,source='',dest='',obs='',owner='ROSE',signer='',required='Obligatoriu',action=''):
 records.append(dict(project=pr['id'],folder=folder,title=title,status=status,source=source,dest=dest,obs=obs,owner=owner,signer=signer,required=required,action=action,due='2026-11-02T16:00:00',email_due='2026-11-03T00:00:00'))
def copy(pr,p,folder,title=None,status='Copiat de verificat',obs='',owner='ROSE',required='Suport',name=None,pages=None):
 p=Path(p);d=Path(pr['out'])/folders[folder]/'Surse';d.mkdir(exist_ok=True)
 target=d/(name or p.name)
 if pages:
  target=target.with_suffix('.pdf');w=PdfWriter();r=PdfReader(p)
  for n in pages:w.add_page(r.pages[n-1])
  with target.open('wb') as f:w.write(f)
 else:shutil.copy2(p,target)
 h=hashlib.sha256(target.read_bytes()).hexdigest()
 record(pr,folder,title or target.stem,status,str(p),str(target),obs+(' | Pagini sursă: '+','.join(map(str,pages)) if pages else '')+' | SHA256 '+h,owner,required=required,action='Verificare finală și includere în opis' if status=='Copiat de verificat' else '')
def key(k):return next(p for p in paths if k in p.name)
for pr in projects:
 for p in Path(pr['source']).iterdir():
  if p.is_file():copy(pr,p,0,status='Referinta oficiala',required='Referință')
 for k,title in [('b105697401','Certificat de înregistrare fiscală ROSE'),('54f8d3ead1','Act constitutiv ROSE'),('83797f4e63','Certificat înscriere Registrul special')]:copy(pr,key(k),7,title,'Copiat verificat',required='Obligatoriu',obs='Identitatea ROSE verificată; actualitatea actelor statutare se confirmă înainte de depunere.')
 for p in paths:
  if p.name=='2023.10.23 - Incheiere nr. 4586.pdf':copy(pr,p,7,'Încheiere modificări statutare 4586/2023')
 # Resolve actual documents, never copy a shortcut as a supporting act.
 for p in [Path(r'\\192.168.100.169\Comun\00. Firme\00. DE VERIFICAT\Colectare 2026-10-31\Firma neidentificata\DATA NECONFIRMATA - 5. Copie a actului constitutiv sau a statutului organizatiei__6cc58156f6.pdf'),Path(r'\\192.168.100.169\Comun\00. Firme\00. DE VERIFICAT\Colectare 2026-10-31\Firma neidentificata\DATA NECONFIRMATA - Hotarare ROSE 2023__9874b0ead9.pdf')]:
  if p.exists():copy(pr,p,7,obs='Exemplar din dosarul statutar 2023; confirmare lipsă modificări ulterioare necesară.')
 for year,k in [(2022,'5940a11164'),(2023,'0df390428e'),(2024,'32f3bd051d'),(2025,'4599158376')]:
  copy(pr,key(k),11,f'Bilanț ROSE {year}',status='Necesita forma lizibila' if year==2024 else 'Copiat de verificat',required='Obligatoriu',obs='PDF XFA afișează Please wait în cititoarele obișnuite; solicitați export lizibil contabilului.' if year==2024 else 'Confirmați versiunea finală depusă și recipisa aferentă.',name=f'Bilant_ROSE_{year}.pdf')
 for year,k in [(2024,'423ecdf370'),(2025,'6167008ffe')]:copy(pr,key(k),12,f'Balanță ROSE {year}',required='Obligatoriu',obs='Perioada și CIF verificate în conținut; contabilul confirmă caracterul analitic și versiunea anuală finală.',name=f'Balanta_ROSE_{year}.pdf')
 for year in [2022,2023]:record(pr,12,f'Balanță analitică anuală ROSE {year}','Lipsa',obs='Nu a fost identificată în centralizarea financiară verificată.',owner='Contabil ROSE',required='Obligatoriu',action='Obțineți balanța analitică anuală semnată de la contabil.')
 copy(pr,key('4508f71af0'),13,'Certificat ANAF arhivat 26.04.2023','Arhivat de reinnoit',required='Arhivă',obs='Nu dovedește situația fiscală la depunerea din 02.11.2026.')
 for typ in ['ANAF','taxe locale']:record(pr,13,f'Certificat de atestare fiscală actual {typ}','Lipsa',obs='Este necesar certificat actual pentru ROSE CIF 29433614, nu cazier fiscal și nu certificat AFM.',owner='ROSE / contabil',required='Obligatoriu',action='Obțineți certificatul și verificați valabilitatea și obligațiile înscrise.')
 people=[('Szoke Andrei-Alexandru','2ab2af8759',list(range(7,15)),[(16,16),(20,20),(21,25)]),('Neamțiu Toader-Florin','9282144560',list(range(5,12)),[(12,12),(13,16),(17,22),(23,28)]),('Neamțiu Ilinca-Mariana','611216dbe2',[4,5],[])]
 for person,k,pgs,extra in people:
  p=key(k);slug=person.replace('ț','t').replace('ă','a').replace('ș','s')
  copy(pr,p,8,f'Diplome și certificate {person}','Copiat verificat',owner=person,required='Obligatoriu',name=f'{slug}_diplome_si_certificate.pdf',pages=pgs,obs='Conținut verificat vizual. Nu reprezintă dovada automată a tuturor cerințelor rolului.')
  copy(pr,p,8,f'CV arhivat {person}','Sursa CV',owner=person,required='Arhivă',name=f'{slug}_CV_sursa.pdf',pages=list(range(1,7)) if 'Szoke' in person else list(range(1,5)) if 'Florin' in person else [1,2,3])
  for a,z in extra:copy(pr,p,10 if ('Szoke' in person and a>=20) else 8,f'Dovadă experiență {person} pagini {a}-{z}','Copiat verificat',owner=person,name=f'{slug}_suport_p{a}-{z}.pdf',pages=list(range(a,z+1)))
 for k,title in [('95a8744bc3','Diplomă licență inginer Cosmin Covaciu'),('ac559469cb','Certificat formator Cosmin Covaciu'),('458d543f13','Diplomă INA Cosmin Covaciu'),('87e46458c0','Certificat audit Cosmin Covaciu')]:copy(pr,key(k),8,title,owner='Cosmin-Adrian Covaciu')
 for p in paths:
  if 'COVACIU COSMIN' in str(p) and ('25a2cc09c3.doc' in p.name or '2d692c5035.doc' in p.name):copy(pr,p,8,'CV arhivat Cosmin-Adrian Covaciu','Sursa CV',owner='Cosmin-Adrian Covaciu',required='Arhivă')
 for person in ['Ilinca_Mariana_Neamtiu','Toader_Florin_Neamtiu']:
  ps=[p for p in paths if p.name==f'Reconstituire_contract_ROSE_10.01.2022_{person}.docx']
  if ps:copy(pr,ps[0],10,f'Contract voluntariat reconstituit {person}','Proiect de completat',obs='Exemplar nesemnat cu câmpuri lipsă. Începutul 10.01.2022 este declarat; nu reprezintă dovadă verificată de activitate, ore ori vechime.',owner=person,required='Suport condiționat')
  record(pr,10,f'Pontaje și rapoarte voluntariat {person}','Lipsa',owner=person,required='Suport experiență',action='Identificați evidențele efective; nu transformați 15 ore/săptămână în ore istorice realizate.')
 copy(pr,key('b71ea34951'),10,'Contract Ilinca din arhiva ROSE','Neconcordante',obs='Nr.12/14.10.2024 în antet; data01.08.2024 în încheiere; telefon diferit de CV. Semnarea și perioada efectivă nu sunt confirmate.',owner='Ilinca-Mariana Neamțiu')
 record(pr,10,'Contract voluntariat Cosmin-Adrian Covaciu','Lipsa',obs='Nu a fost identificat un contract personal de voluntariat în sursele verificate. Experiența profesională se susține separat.',owner='Cosmin-Adrian Covaciu',required='Suport dacă se invocă voluntariat',action='Furnizați contractul existent, dacă se invocă această experiență.')
 for k in ['62cc5bcf78','0a406c5893','cf38dd61d4','dee50e4dc4','bca3842f28d5','796597aeb1']:
  copy(pr,key(k),14,obs='Document candidat pentru experiență/punctaj. Verificați rolul ROSE, perioada, finalizarea și legătura cu cerința exactă; nu se atribuie automat experiența altor entități.')
 for title,obs in [('Proiect relevant ONG implementat în ultimii 3 ani','Nu este confirmată îndeplinirea integrală a criteriului din secțiunea1.1.b.ii doar prin existența proiectelor de educație ecologică.'),('Dovezi experiență minimum 6 luni pe activitățile asumate','Descrierea și documentele trebuie să corespundă activităților A1.1/A1.2/A3, nu doar management general.'),('Rapoarte cu număr participanți și indicatori realizați','Trebuie identificate valorile asumate/realizate, perioada și documentele aprobate. Nu însumați participanți din proiecte diferite fără bază.'),('Recomandări beneficiari și confirmări implementare','Contractul sau acordul nu dovedește singur executarea și finalizarea proiectului.')]:record(pr,14,title,'De demonstrat',obs=obs,required='Obligatoriu / punctaj',action='Selectați și validați dovezile relevante înainte de depunere.')
 for title in ['Atestat liberă practică Ilinca și condiții de supervizare','Dovadă experiență Ilinca cu copii 0–6 ani inclusiv CES și/sau consilierea părinților','Diplomă master Ilinca','Dovadă continuitate funcții și activități după ultima versiune CV','Acceptarea rolurilor propuse și disponibilitatea comună pentru ambele proiecte','Confirmare număr total proiecte în același apel','Confirmare spații disponibile pentru activități în Sebeș','Confirmare situații de eligibilitate și cofinanțare','Mandat vicepreședinte dacă semnează în locul președintelui']:
  record(pr,8 if 'Ilinca' in title or 'CV' in title or 'rolur' in title else 7,title,'De confirmat',required='Condiționat' if 'Mandat' in title else 'Obligatoriu',action='Confirmați în scris și anexați documentul justificativ, după caz.')
(B/'projects.json').write_text(json.dumps(projects,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'folders.json').write_text(json.dumps(folders,ensure_ascii=False),encoding='utf-8')
print('Dosare create',len(projects),'înregistrări',len(records))
