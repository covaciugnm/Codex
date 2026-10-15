from pathlib import Path
import json, hashlib, shutil
from pypdf import PdfReader

ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
WORK=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
OUT=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH'
DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def rel(p):return p.relative_to(ROOT).as_posix()
def rec(p):return {'cale':rel(p),'sha256':sha(p),'octeti':p.stat().st_size}
def fresh(p,s):assert not p.exists(),p;p.write_text(s,encoding='utf-8')

frozen=read(WORK/f'{DATE} Surse inghetate audit R05.json')
for r in frozen['surse']:assert sha(ROOT/r['cale'])==r['sha256']
previous=read(WORK/f'{DATE} Registru audit comparativ final R05.json')
for r in previous['contracte']:assert sha(ROOT/r['cale'])==r['sha256']
matrix=read(OUT/f'{DATE} Cerinte comune negociere matrice.json')
objections=read(OUT/f'{DATE} Obiectii negociere reformulate.json')
firms=read(OUT/f'{DATE} Date firme pentru negociere.json')
export=read(OUT/f'{DATE} Export baza negociere pentru verificare.json')
reports=[]
for r in export['documente']:
    p=ROOT/r['docx'];reports.append(rec(p))
    q=p.with_suffix('.pdf');reports.append({**rec(q),'pagini':len(PdfReader(str(q)).pages)})
qa=list(OUT.glob(f'{DATE} QA*.txt'))
assert qa, 'Notele de QA lipsesc'

regpath=ROOT/f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/{DATE} Registru comunicatii.json'
partners=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
targets=[ROOT/f'{DATE} Status proiect.txt',ROOT/f'{DATE} Log progres proiect.txt',
         partners/f'{DATE} Log discutii - Markus Berger.txt',partners/f'{DATE} Log discutii - Pech.txt',
         regpath,ROOT/'folder map/README.md']
history=OUT/f'{DATE} Istoric jurnale inainte reformulare negociere'
assert not history.exists();history.mkdir()
backups=[]
for p in targets:
    dest=history/(p.name if p.name.startswith(DATE) else f'{DATE} {p.name}')
    shutil.copy2(p,dest);assert sha(p)==sha(dest)
    backups.append({'original':rel(p),'hash_inainte':sha(p),'copie':rel(dest)})

entry='''2026.10.13 | Bază comună de negociere BERGER și PECH
Status scurt: reformulare la cererea utilizatorului, pornind de la contractele R05 și audit, pentru același pachet solicitat ambilor. Matrice explicită pe criterii și faze, obiecții reformulate ca puncte de negociere și datele celor trei firme din arhivă și surse publice. Cerințele mai ample față de ofertă sunt poziții AG, nu defecte prin simpla lor existență. Documentele nu sunt contracte finalizate; R05 rămâne nemodificat.
Scop comun: proiectare structură, documentație execuție, 12 vizite fizice incluse + până la 6 opționale, PI și contribuții §128 până la final, Bauwerksbuch existent+intervenții noi; execuție 18 luni de la B0 real, planificare T0 distinctă. Fără BauKG/management general REALIG. Diferențele R05 de termene, numărare/vizite PI, penalitate și facturare sunt prezentate explicit cu aceeași cerință propusă pentru ambii.
Economie: BERGER 45.000 EUR net/54.000 EUR cu TVA; PECH 69.300 EUR net/83.160 EUR cu TVA. Opțiuni: BERGER2.000/12 net per vizită, cumul maxim1.000 EUR net pentru6; PECH450 EUR net per vizită, maxim2.700 EUR net pentru6. Totaluri cu toate6:46.000/72.000 EUR net. Valorile și tarifele rămân distincte; condițiile și conținutul solicitate se uniformizează în matrice. Nicio opțiune nu este comandată automat.
Date firme: A&C FN668224h/UIDATU83086125 din acte locale; BERGER FN316003k, UIDATU64446068 din sursă publică secundară; PECH FN426034x/UIDATU69226367 din originalul ofertei și surse publice. Adresele și reprezentarea sunt documentate în anexă cu nivelul confirmării. Neinsistăm pe majorarea asigurării; se păstrează doar completarea administrativă și obligațiile aplicabile.
Ultimul răspuns real: BERGER2026.08.17; PECH2026.09.17. Cercetarea publică nu este un răspuns comercial nou. Nu este o verificare generală zilnică EVA.
Următorul pas autorizat: transpunerea cerințelor comune în două proiecte R06 germane și formatarea PDF elegantă, cu chenare fine și numerotare clară, la cererea utilizatorului. Operațiunea R06 este distinctă și se consemnează prin registrul propriu după finalizare. Baza comparativă nu modifică R05, nu trimite mesaje și nu acceptă ofertele.
Surse curente: 00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH/2026.10.13 Matrice explicita cerinte comune BERGER PECH.docx/PDF și 2026.10.13 Obiectii reformulate si pozitii comune negociere.docx/PDF; registrul final și cele trei JSON sursă în același dosar.
Istoricul auditului și toate versiunile contractuale sunt păstrate. Numărătorile Eva802mesaje/826originale/783documentare neschimbate. Nicio trimitere, semnare sau plată.
'''
def prepend(p,s):
    b=next(x for x in backups if x['original']==rel(p));assert sha(p)==b['hash_inainte']
    old=p.read_text(encoding='utf-8-sig');p.write_text(s.rstrip()+'\n\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
for p in targets[:4]:prepend(p,entry)

reg=read(regpath);n=len(reg['comunicatii'])
reg.setdefault('actualizari_punctuale',[]).append({'data':DATE,'tip':'baza_comuna_negociere_cerinte_identice_BERGER_PECH',
 'registru':rel(OUT/f'{DATE} Registru baza negociere final.json'),'livrabile':[r['cale'] for r in reports],
 'statut':'BAZĂ DE NEGOCIERE; R05 nemodificat; nu contract finalizat',
 'criterii_comune':len(matrix['matrice']),'puncte_negociere':len(objections['puncte_negociere']),
 'mesaje_noi':0,'originale_noi':0,'trimiteri':0,'semnaturi':0,'plati':0})
assert len(reg['comunicatii'])==n
regpath.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepend(targets[5],'''# 2026.10.13 — Bază comună de negociere BERGER și PECH

Punct curent: ../00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH/. Începe cu `2026.10.13 Matrice explicita cerinte comune BERGER PECH.docx` sau PDF și `2026.10.13 Obiectii reformulate si pozitii comune negociere.docx` sau PDF. Registru: `2026.10.13 Registru baza negociere final.json`. Aceste documente definesc aceeași poziție AG pentru ambii; contractele R05 sunt documentele de pornire și rămân nemodificate. Auditul anterior păstrează constatările istorice și sursele, nu se prezintă drept acceptare ori contract finalizat.

Pachet comun: structură și planuri complete, PI/§128, Bauwerksbuch existent+nou, 18luni de laB0 real, 12vizite fizice+6opționale; fărăBauKG/managementgeneralREALIG. Matricea explică fiecare criteriu și diferențele actuale de termene, numărarePI/vizite, penalitate și facturare, cu o cerință comună pentru uniformizare. Diferențele de valoare și tarife rămân economice:45.000/69.300EURnet; cu6opțiuni46.000/72.000EURnet. Asigurarea este doar completare administrativă secundară, fără cerință AG de majorare.

Datele A&C, BERGER și PECH sunt completate în anexa administrativă din surse locale și publice, cu limite și neconcordanțe păstrate. UIDBERGER este publicat numai secundar; reprezentarea la semnare trebuie confirmată în etapa corespunzătoare. Nu este un nou scan zilnicEVA și nu există comunicare comercială nouă. Jurnalele și registrul sunt actualizate cu istoricul păstrat; nicio trimitere, semnare sau plată.
''')

manifest={'data':DATE,'statut':'BAZĂ DE NEGOCIERE, cerințe identice propuse; contracte R05 nemodificate',
 'livrabile':reports,'surse':[rec(OUT/f'{DATE} {name}.json') for name in ['Cerinte comune negociere matrice','Obiectii negociere reformulate','Date firme pentru negociere']],
 'criterii':len(matrix['matrice']),'puncte_negociere':len(objections['puncte_negociere']),
 'date_firme_campuri':sum(len(v) for v in firms['companies'].values()),'surse_identificare':len(firms['sources']),
 'qa':[rec(p) for p in qa],'contracte_frozen':previous['contracte'],
 'istoric_jurnale':backups,'jurnale_actualizate':[rec(p) for p in targets],
 'contracte_modificate':0,'mesaje_trimise':0,'semnaturi':0,'plati':0}
fresh(OUT/f'{DATE} Registru baza negociere final.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
fresh(OUT/f'{DATE} Jurnal actualizare baza negociere.txt',entry)
for r in previous['contracte']:assert sha(ROOT/r['cale'])==r['sha256']
print(json.dumps({'statut':'PASS','criterii':manifest['criterii'],'puncte':manifest['puncte_negociere'],
 'livrabile':reports,'contracte_identice':6,'comunicatii_neschimbate':n},ensure_ascii=False))
