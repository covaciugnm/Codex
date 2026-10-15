from pathlib import Path
import shutil,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'08. Corespondenta'/'2026.10.07 Analiza juridica Donau auditata'
HIST=OUT/'2026.10.07 Istoric jurnale inaintea opiniei auditate'
HIST.mkdir(exist_ok=True)
block='''2026.10.07 | ANALIZĂ JURIDICĂ DETALIATĂ REDACTATĂ ȘI AUDITATĂ

Status scurt: opinia documentată privind DONAU 2044001194 este finalizată în Word și PDF, cu sinteză pentru decizie, legislație austriacă, nouă hotărâri OGH și audit separat. Durata comercială de zece ani este posibilă; încetarea în 2027 nu este demonstrată doar prin trei luni de preaviz. Priorități: acordul-cadru 2900010498, dovada acordului de durată, controlul clauzei 1000K, somația și acoperirea, ajustarea riscului și regresul față de vânzătoare. Analiză de doi agenți AI, fără semnătură sau atribuire unui avocat.
Ultimul răspuns DONAU: 2026.10.06, Loschy, primit, ID 2c273256-a0bf-408b-bb22-09718372e888. Nu s-a primit ori trimis o nouă comunicare în această redactare.
Următorul pas: examinarea sintezei și alegerea strategiei; clarificarea acoperirii și obținerea probelor lipsă înaintea unei poziții definitive. Termenul Commerz 2026.10.12 rămâne distinct; analiza nu îl suspendă și nu recunoaște soldul.
Sursa: 08. Corespondenta/2026.10.07 Analiza juridica Donau auditata/2026.10.07 Opinie juridica Donau Schallergasse 35.docx și .pdf; 2026.10.07 Analiza redactor.txt; 2026.10.07 Audit juridic.txt.
Draftul DONAU aa653a96-7eee-4133-a41d-5892ea79788d rămâne NETRIMIS. Solicitarea Capra 3b3a2213-bc82-47ea-a023-4692db3da65c rămâne DRAFT NETRIMIS, neutilizată după schimbarea sarcinii la analiză și audit; export în dosarul opiniei. Nicio semnare, plată sau acord de încetare/acoperire confirmat.

ISTORIC

'''
paths=[ROOT/'2026.10.07 Status proiect.txt',ROOT/'2026.10.07 Log progres proiect.txt']
partners=ROOT/'08. Corespondenta'/'2026.09.30 Arhiva Eva-Mail'/'Parteneri'
paths += [partners/'2026.10.07 Log discutii - Donau Versicherung.txt',partners/'2026.10.07 Log discutii - Maritczak - Commerz Inkasso.txt']
for path in paths:
    if path.exists():
        dest=HIST/path.name
        if not dest.exists():shutil.copy2(path,dest)
        old=path.read_text(encoding='utf-8-sig')
        if not old.startswith('2026.10.07 | ANALIZĂ JURIDICĂ DETALIATĂ'):
            path.write_text(block+old,encoding='utf-8')
capra=partners/'2026.10.07 Log discutii - CERHA HEMPEL.txt'
if capra.exists():
    dest=HIST/capra.name
    if not dest.exists():shutil.copy2(capra,dest)
    note='2026.10.07 | Analiză DONAU și audit realizate local de doi agenți AI, fără comunicare nouă către CERHA HEMPEL. Draftul solicitării de opinie 3b3a2213-bc82-47ea-a023-4692db3da65c este NETRIMIS și neutilizat în sarcina curentă. Următorul pas este alegerea strategiei pe analiza finală; nu se prezumă opinie sau acceptare din partea avocatului. Sursa: 08. Corespondenta/2026.10.07 Analiza juridica Donau auditata/. Ultimul răspuns extern rămâne cel consemnat în istoric.\n\nISTORIC\n\n'
    old=capra.read_text(encoding='utf-8-sig')
    if not old.startswith('2026.10.07 | Analiză DONAU și audit'):capra.write_text(note+old,encoding='utf-8')
readme=ROOT/'folder map'/'README.md'
old=readme.read_text(encoding='utf-8-sig')
if not (HIST/'2026.10.07 README anterior.txt').exists():shutil.copy2(readme,HIST/'2026.10.07 README anterior.txt')
intro='''# 2026.10.07 — Opinie juridică DONAU redactată și auditată

Punctul curent juridic: ../08. Corespondenta/2026.10.07 Analiza juridica Donau auditata/. Începe cu 2026.10.07 Opinie juridica Donau Schallergasse 35.docx sau PDF și 2026.10.07 Audit juridic.txt. Document detaliat cu sinteză, surse RIS și nouă hotărâri OGH; două roluri AI separate, fără atribuire unui avocat. Opinia înlocuiește analiza preliminară ca reper juridic actual. Durata comercială de zece ani este posibilă; căile de ieșire sunt condiționate de acord, cadrul complet, exercitarea în termen sau cauze speciale. Controlul 1000K, proba somației și regresul contractual sunt distincte. Drafturile DONAU și Capra sunt NETRIMISE; Capra neutilizat la cererea utilizatorului. Termenul Commerz 2026.10.12 nu este suspendat. Jurnalele TXT actualizate, istoricul păstrat.

'''
if not old.startswith('# 2026.10.07 — Opinie juridică DONAU'):readme.write_text(intro+old,encoding='utf-8')
(OUT/'2026.10.07 Jurnal actualizare opinie.txt').write_text(block.replace('\nISTORIC\n\n','\n'),encoding='utf-8')
files=[]
for path in OUT.iterdir():
    if path.is_file():files.append({'nume':path.name,'dimensiune':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(OUT/'2026.10.07 Registru documente opinie.json').write_text(json.dumps({'data_lizibila':'2026.10.07','tip':'Analiză locală și audit; nicio comunicare trimisă','documente':files},ensure_ascii=False,indent=2),encoding='utf-8')
print('Jurnale, README și registru documente actualizate; istoricul păstrat.')
