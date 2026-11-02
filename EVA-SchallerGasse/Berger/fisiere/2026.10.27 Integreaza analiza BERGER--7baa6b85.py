import json, hashlib, shutil
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).resolve().parent.parent
STAMP=datetime.now().astimezone().isoformat(timespec='seconds')
DAY='2026.10.27'
CENTRAL=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
MAIL=ROOT/'08. Corespondenta/2026.10.27 BERGER contract adnotat si Teams'
OUT=ROOT/'00.Proiect/09. Vertraege/bmberger.at/2026.10.27 Observatii BERGER si comparatie'
QA=ROOT/'folder map/2026.10.27 QA Berger adnotari'
BACKUP=ROOT/'folder map'/('2026.10.27 Istoric inainte integrare BERGER '+datetime.now().strftime('%H-%M-%S'))
BACKUP.mkdir(parents=True,exist_ok=True)

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def backup(p):
    if p.exists():
        dst=BACKUP/p.relative_to(ROOT);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
def prepend(p,text):
    backup(p)
    old=p.read_text(encoding='utf-8-sig') if p.exists() else ''
    if '2026.10.27 | BERGER - CONTRACT ADNOTAT, OCR SI COMPARATIE' not in old[:2000]:
        p.write_text(text+'\n\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')

manifest=read(MAIL/'2026.10.27 Registru surse BERGER.json')
original=ROOT/manifest['original_pdf']
assert sha(original)==manifest['sha256_original']
comparison=OUT/'2026.10.27 BERGER Comparatie contract R09 R10 cu observatii.pdf'
ocr=OUT/'2026.10.27 BERGER contract adnotat OCR.pdf'
assert sha(comparison)==read(QA/'2026.10.27 Audit comparatie.json')['sha256']
audit=read(QA/'2026.10.27 Audit vizual si integritate.json')
assert audit['OCR_pixel_identical_pages']==list(range(1,19))
assert not audit['left_original_main_paragraphs_not_contiguous_after_extraction']

regpath=CENTRAL/'2026.10.27 Registru comunicatii.json'
backup(regpath);reg=read(regpath)
ids={x.get('id') for x in reg['comunicatii']}
for row in manifest['mesaje']:
    m=read(ROOT/row['json'])
    if m['id'] in ids:continue
    reg['comunicatii'].append({'data':DAY,'ora_utc':m['received_at'][11:19],
      'partener':'Markus Berger','domeniu':'Structura / contract adnotat' if m['attachments'] else 'Structura / invitatie Teams',
      'sens':'PRIMIT','subiect':m['subject'],'expeditor':m['from_address'],'destinatari':m['to'],'cc':m['cc'],
      'id':m['id'],'cale':row['txt'],'json':row['json'],'atasamente':m['attachments'],
      'trunchiat':m['truncated'],'data_preluarii':DAY})
    ids.add(m['id'])

status='2026.10.27: BERGER a transmis contractul R09 adnotat, scan de 18 pagini, si invitatia Teams pentru 2026.10.29, 13:00–13:30 Viena / 14:00–14:30 Romania. OCR si comparatie interna R09/R10 realizate; 21 puncte de discutie, fara acceptarea modificarilor sau semnare.'
last='2026.10.27 13:46:46 Romania: invitatie Baubesprechung prin Teams; anterior, 13:27:16, BERGER a trimis observatiile «wie heute besprochen». Originalul ICS fixeaza 2026.10.29, nu 2026.10.27. Beneficiarul are PARTSTAT=NEEDS-ACTION.'
nextstep='Raspunsurile proprietarului la punctele deschise (PI/ZT, Bauwerksbuch, planuri, termene si formate), apoi revizuire si discutie cu BERGER. Inscrierea/corectarea calendarului asteapta confirmarea datei, orei, fusului orar si calendarului ceruta de instrumentul EVA. Nu exista acceptare RSVP transmisa.'
sources=[x['txt'] for x in manifest['mesaje']]+[rel(original),rel(comparison),rel(ocr)]
for s in reg['statusuri']:
    if s.get('partener')=='Markus Berger':
        if s.get('status')!=status:
            s.setdefault('istoric_status',[]).append({'data_preluarii':DAY,'status':s.get('status'),'ultimul_raspuns':s.get('ultimul_raspuns'),'urmatorul_pas':s.get('urmatorul_pas'),'sursa_status':s.get('sursa_status')})
        s.update(status=status,ultima_comunicare=DAY,ultimul_primit=DAY,subiect_ultimul_primit='Baubesprechung',ultimul_raspuns=last,urmatorul_pas=nextstep,sursa_status=sources,data_actualizarii=DAY)
        s['verificare_manuala_adnotari_2026_10_27']={'mesaje_noi':2,'pagini_scan':18,'pagini_comparatie':42,'puncte_discutie':21,'calendar':'confirmare utilizator in asteptare','sursa':rel(MAIL/'2026.10.27 Registru surse BERGER.json')}
        s['mesaje']=sum(x.get('partener')=='Markus Berger' for x in reg['comunicatii'])

point={'data':DAY,'checked_at_iso':STAMP,'tip':'BERGER - contract adnotat, OCR si comparatie','mesaje_noi':2,'IDuri_noi':[x['id'] for x in manifest['mesaje']],
 'atasamente_originale_noi':1,'pagini_OCR':18,'pagini_comparatie':42,'puncte_discutie':21,'calendar_creat':False,
 'calendar_stare':'Asteapta confirmarea explicita datei/orei/fusului orar/calendarului solicitata prin intrebare async; nu s-a transmis RSVP.',
 'acoperire':'Verificare punctuala a celor doua mesaje BERGER, cautari paginate dupa expeditorii office@bmberger.at si meetingtisch@bmberger.at, citire integrala; nu reprezinta o noua verificare globala a tuturor casutelor sau partenerilor.',
 'surse':sources}
reg['acoperire']['verificare_manuala_BERGER_adnotari']=point
reg['actualizari_punctuale']=[x for x in reg['actualizari_punctuale'] if x.get('tip')!=point['tip']]+[point]
reg['data_actualizarii']=DAY
write(regpath,reg)

attpath=CENTRAL/'2026.10.27 Registru atasamente.json'
backup(attpath)
atts=read(attpath if attpath.exists() else CENTRAL/'2026.10.22 Registru atasamente.json')
a=manifest['atasament']
if not any(x.get('id')==a['id'] for x in atts):
    atts.append({'id':a['id'],'email_id':'580b41a5-ab32-4827-911d-4b0443e8d0f6','data':DAY,'partener':'Markus Berger','nume_original':a['name'],'octeti':original.stat().st_size,'sha256':sha(original),'cale':rel(original),'stare':'original integral descarcat si verificat; 18 pagini scanate, original nemodificat; OCR generat separat'})
write(attpath,atts)

report=f'''2026.10.27 | BERGER - CONTRACT ADNOTAT, OCR SI COMPARATIE
Actualizat: {STAMP}

Status scurt: {status}
Ultimul raspuns: {last}
Urmatorul pas: {nextstep}

Fisiere noi: scanul original BERGER (18 pagini), PDF OCR (18 pagini, aspect identic originalului), comparatia R09/R10 (42 pagini A3 landscape), modelul comparativ si registrul celor 21 de puncte de discutie. Stanga: textul original R09; dreapta: propunerea in germana. Observatiile si intrebarile proprietarului sunt in romana. Clauzele afectate din toate cele 6 anexe sunt incluse in comparatie. Scanul primit contine numai primele 18 pagini din R09 (29 pagini); anexele nu au fost returnate adnotate, ceea ce nu constituie acceptarea lor.

Financiar: baza 45.000 EUR net / 54.000 EUR cu TVA, 4 pozitii nemodificate (13.000 + 20.000 + 2.000 + 10.000 EUR net). Maximum 8 vizite statice, T0 inclus in cele 8 daca are obiect static. Calupuri suplimentare propuse numai la comanda: 1.000 EUR net / 4 vizite. Cadrul fazei de executie: 18 luni de la B0 efectiv. Nicio suma suplimentara aprobata. Discutiile privind PI/ZT, Bauwerksbuch si alte servicii nu sunt acceptari sau excluderi comerciale definitive.

Puncte deschise: cine furnizeaza Polierplane si Baufuhrer, B0/T0 si Planwechsel; persoana PI (nume manuscris incert, nepreluat drept cert), verificarile PI si certificarea ZT; Bauwerksbuch (BERGER il declara neinclus, cerinta beneficiarului ramane deschisa); formatele editabile/IFC; termenele de raspuns propuse 5/3 zile; raportarea si calendarul de livrare/facturare cu valori. Au fost initiate intrebari catre proprietar; nicio alegere nu este presupusa acceptata.

Calendar: joi 2026.10.29, 13:00–13:30 Viena / 14:00–14:30 Romania, Teams. Cerere de confirmare a datei/orei/fusului si calendarului in asteptare, ceruta de instrumentul EVA. Nu s-a creat un eveniment si nu s-a transmis RSVP. Evenimentul EVA extras automat la 2026.10.27 este eronat fata de ICS; nu este folosit ca dovada a programarii corecte.

Acoperire: doua emailuri originale PRIMITE, citite integral, un atasament original descarcat. Verificare punctuala BERGER, fara a pretinde actualizarea generala a tuturor casutelor. Registru comunicatii: {len(reg['comunicatii'])} ID-uri unice; registru atasamente: {len(atts)} pozitii. OCR/comparatia sunt produse locale, nu atasamente primite. ICS este extras din corpul emailului.

Surse:
'''+''.join('- '+x+'\n' for x in sources)+f'''- {rel(MAIL/'2026.10.27 Invitatie originala BERGER 2026.10.29 Teams.ics')}
- {rel(regpath)}
- {rel(attpath)}

Originalele R09 si oferta BERGER au fost pastrate nemodificate. Nu s-au trimis emailuri, semnat contracte sau efectuat plati. Documentul R10 este o propunere pentru analiza, cu puncte deschise, nu un contract acceptat sau pregatit pentru semnare.
'''
reportpath=OUT/'2026.10.27 Status analiza si surse BERGER.txt'
reportpath.write_text(report,encoding='utf-8')
for p in [ROOT/'2026.10.27 Status proiect.txt',ROOT/'2026.10.27 Log progres proiect.txt',CENTRAL/'Parteneri/2026.10.27 Log discutii - Markus Berger.txt']:
    prepend(p,report)
prepend(ROOT/'folder map/README.md',report+f'\nPunct curent: ../{rel(reportpath)}\nComparatie PDF: ../{rel(comparison)}\nOCR PDF: ../{rel(ocr)}\n')

audit.update({'verificare_vizuala_efectuata':True,'pagini_comparatie_inspectate':list(range(1,43)),
 'pagini_scan_inspectate':list(range(1,19)),'observatii_manuscrise_verificate_pe_imagini':True,
 'financial_tables_identical':True,'comparatie_sha256':sha(comparison),'pdf_ocr_sha256':sha(ocr),
 'limita':'Numele PI manuscris si deciziile proprietarului raman deschise; auditul de integritate nu constituie acceptare juridica sau comerciala.'})
write(QA/'2026.10.27 Audit vizual si integritate.json',audit)
print(json.dumps({'registry':len(reg['comunicatii']),'unique_ids':len(ids),'attachments':len(atts),'comparison_sha256':sha(comparison),'backup':rel(BACKUP)},ensure_ascii=False))
