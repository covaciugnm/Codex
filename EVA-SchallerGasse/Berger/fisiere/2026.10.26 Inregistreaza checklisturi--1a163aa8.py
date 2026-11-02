from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, shutil
import pdfplumber

root=Path.cwd()
now=datetime.now(ZoneInfo('Europe/Bucharest'))
stamp=now.isoformat()
out=Path('00.Proiect/09. Vertraege/2026.10.26 Checklisturi intalniri')
manifest=json.loads((root/out/'2026.10.26 Surse si continut checklisturi.json').read_text(encoding='utf-8'))
expected={'BERGER_R09':'71b4a9eac341b3ead3c7717f269d7ddb5525769d9f72205320c32ccad8b237dd','PECH_R09':'a670ba0e33481299364ecf62e3e6434c50416dc2dc3d0ec76e7153678b75318d'}
for k,h in expected.items():
    p=root/manifest['sources'][k]['cale']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(k,'contract modificat')
qa={}
for firm in ('BERGER','PECH'):
    p=root/out/f'2026.10.26 Checklist intalnire {firm}.pdf'
    with pdfplumber.open(p) as d:
        assert len(d.pages)==2
        text='\n'.join(pg.extract_text() for pg in d.pages)
        assert 'R09' in text and '2026.10.27' in text
        qa[firm]={'pagini':len(d.pages),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'verificare_vizuala':'Toate paginile randate PNG si inspectate: fara suprapuneri, continut taiat sau pagini orfane.','cale':str(out/p.name).replace('\\','/')}
backup=root/'folder map'/('2026.10.26 Istoric checklisturi '+now.strftime('%H-%M-%S'))
backup.mkdir(exist_ok=False)
register=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.26 Registru comunicatii.json')
reg=json.loads((root/register).read_text(encoding='utf-8-sig'))
before={'comunicatii':len(reg['comunicatii']),'drafturi':len(reg['drafturi']),'acoperire':reg['acoperire'],'draft_hash':hashlib.sha256(json.dumps(reg['drafturi'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
def preserve(rel):
    p=root/rel
    b=backup/rel
    b.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,b)
def prepend(rel,body):
    preserve(rel)
    p=root/rel
    old=p.read_text(encoding='utf-8-sig')
    p.write_text(body+'\n\n'+old,encoding='utf-8')

heading='2026.10.26 | CHECKLISTURI INTERNE PENTRU INTALNIRILE BERGER / PECH DIN 2026.10.27'
body=heading+'\nStatus scurt: doua checklisturi PDF distincte, cate 2 pagini, pregatite si verificate vizual; contractele R09 sunt neschimbate, propuneri neacceptate. Nu s-au trimis emailuri si nu s-au modificat documente comerciale.\nUltimul raspuns: BERGER primit 2026.10.24 propune 11:30 la Schonbrunner Strasse 123/2; PECH primit 2026.10.22 conditioneaza 14:00 de prezentarea la Johann-Strauss-Gasse 32/6. Orele sunt ale Vienei. Ciornele confirmarilor erau NETRIMISE la ultimul control EVA din 2026.10.26 09:57; aceasta lucrare nu reprezinta o verificare noua a emailurilor.\nUrmatorul pas: clarificarea serviciilor, preturilor, calendarului cu valori si documentelor de semnat, apoi confirmare scrisa a rezultatului. PECH: AN01 69.300 EUR net, AN02 8.300 EUR net; cumul aritmetic 77.600 EUR net, neacceptat si inainte de optiuni/indexare. BERGER: oferta 45.000 EUR net, maximum 8 vizite statice; suplimentul 1.000 EUR net/4 vizite este propunerea noastra.\nSursa: '+str(out).replace('\\','/')+'; sursele si hashurile originalelor in 2026.10.26 Surse si continut checklisturi.json.'
for rel in (Path('2026.10.26 Status proiect.txt'),Path('2026.10.26 Log progres proiect.txt')):
    prepend(rel,body)
for firm,partner,last,nextstep in [
    ('BERGER','Markus Berger','2026.10.24: propunere de intalnire 2026.10.27, 11:30 ora Vienei, Schonbrunner Strasse 123/2, 1050 Wien.','Reconfirmarea pretului de 45.000 EUR net si a serviciilor adaugate in R09, PI/finalizare, Bauwerksbuch, 8 vizite si pachete suplimentare, calendar si valori de facturare.'),
    ('PECH','Pech','2026.10.22: intalnire posibila 2026.10.27, 14:00 ora Vienei, Johann-Strauss-Gasse 32/6, 1040 Wien. Observatiile comerciale si AN02 sunt din 2026.10.21.','Reconcilierea AN01/AN02 cu R09: PI, certificarea ZT, Bauwerksbuch, vizite, calendar si valori, plata/retinere, indexare, penalitati si documentare.')]:
    rel=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri')/f'2026.10.26 Log discutii - {partner}.txt'
    source=str(out/f'2026.10.26 Checklist intalnire {firm}.pdf').replace('\\','/')
    block=f'2026.10.26 | CHECKLIST INTALNIRE {firm}\nStatus scurt: material intern pregatit, 2 pagini; contractul R09 neschimbat, fara acceptare sau semnare.\nUltimul raspuns: {last} Ciorna confirmarii era NETRIMISA la ultimul control EVA; fara verificare noua in aceasta lucrare.\nUrmatorul pas: {nextstep}\nSursa: {source}; manifestul surselor din acelasi dosar.'
    prepend(rel,block)
    for row in reg['statusuri']:
        if row.get('partener')==partner:
            row['material_intalnire_checklist']={'data':'2026.10.26','intalnire':'2026.10.27','status':'material intern pregatit; contract R09 nemodificat; nu reprezinta acceptare','sursa':source,'urmatorul_pas':nextstep}
preserve(register)
reg['actualizari_punctuale'].append({'data':'2026.10.26','checked_at_iso':stamp,'tip':'Doua checklisturi interne pentru intalniri, fara modificarea contractelor','surse':[x['cale'] for x in qa.values()],'emailuri_noi':0,'mesaje_trimise':0,'nu_reprezinta_verificare_email':True})
assert len(reg['comunicatii'])==before['comunicatii'] and len(reg['drafturi'])==before['drafturi']
assert reg['acoperire']==before['acoperire']
assert hashlib.sha256(json.dumps(reg['drafturi'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==before['draft_hash']
(root/register).write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
readme=Path('folder map/README.md')
prepend(readme,'## 2026.10.26 - Checklisturi separate pentru intalnirile BERGER si PECH\n\n'+body+'\nContracte curente: '+manifest['sources']['BERGER_R09']['cale']+'; '+manifest['sources']['PECH_R09']['cale']+'.')
proof={'data':'2026.10.26','created_at_iso':stamp,'checklisturi':qa,'contracte_neschimbate':expected,'registre_inainte':before,'observatie':'Acoperirea EVA, mesajele reale si drafturile au fost pastrate. Nicio comunicare transmisa. Inspectie vizuala finala a tuturor celor 4 pagini.'}
(root/'folder map/2026.10.26 QA checklisturi/2026.10.26 Control final checklisturi.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdfs':qa,'comunicatii':before['comunicatii'],'drafturi':before['drafturi'],'backup':str(backup)},ensure_ascii=False))
