from pathlib import Path
import json, shutil, hashlib
root=Path.cwd()
dest=root/'04. Firme + Executie/2026.10.12 Comparatie servicii structura'
book='04. Firme + Executie/2026.10.12 Comparatie servicii structura/2026.10.12 Comparatie servicii si preturi structura.xlsx'
partners=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
archive=dest/'2026.10.12 Istoric inainte de comparatie'
archive.mkdir(exist_ok=True)
summary=f'''2026.10.12 | Comparație servicii și prețuri structură

Status scurt: două tabele Excel finalizate: 47 rânduri de servicii/discuții și 24 rânduri de prețuri/condiții, pe baza propunerii TOMS v4.1 TRIMISE la 2026.10.02, a ofertelor și chestionarelor originale, și a ofertelor BERGER/PECH deja arhivate. Comparație locală, fără comunicare externă nouă.
Ultimele răspunsuri reale: TOMS 2026.10.08 refuz de preluare în prezent din lipsă de resurse, întindere față de v4.1 de clarificat; BERGER 2026.08.17 ofertă; PECH 2026.09.17 ofertă. Acceptarea, semnarea și începerea nu sunt confirmate.
Prețuri: TOMS 37.900 EUR net /45.480 EUR cu TVA; BERGER 45.000 EUR net /54.000 EUR cu TVA; PECH 69.300 EUR net /83.160 EUR cu TVA. Totaluri pe domenii diferite, nu comparație omogenă de servicii. Subtotale calculate structură/asistență: TOMS 26.500, BERGER 35.000 EUR net; atribuirea parțială BERGER necesită acord. Nu se tratează ratele AG drept prețuri AN.
TOMS: confirmările punctuale Q1/Q2 sunt separate de contractul integral neacceptat. 300 EUR/vizită confirmat Q1 F5; pragul peste 3 vizite este completare AG. ANG 839: ipoteză 15 vizite, 155 EUR/oră PI; disponibilitate 24 h în Q1 F7. BauKG istoric 11.040 EUR net este în afara v4.1.
BERGER: maximum 8 vizite pentru asistență, fără plafon explicit al tuturor vizitelor PI. Calcule13.000 +planuri20.000 +asistență2.000 +PI10.000 EUR net. Valabilitate calculată până la 2026.10.12, prelungire neconfirmată.
PECH: structură42.000 +goluri6.000 +excavare5.000 +teren800 +Baubegleitung14.000 +final1.500 EUR net. Cele 12 recepții nu dovedesc numirea PI. LB exactă, planurile, formatele, drepturile, indexarea și calendarul necesită clarificare. Bauwerksbuch nu este explicit ofertat de BERGER/PECH. REALIG24.000 EUR net este sumă presupusă într-un pachet general, nu ofertă fermă separată.
Următorul pas: alinierea în scris a obiectului ofertelor, identificarea prestatorului pentru noduri/ancore/atelier și confirmarea disponibilității. Pentru TOMS clarificarea refuzului față de v4.1; pentru BERGER prelungirea; pentru PECH numirea PI, LB exactă și licența de utilizare.
Surse: {book}; 2026.10.12 Date TOMS.json; 2026.10.12 Date alternative.json; 2026.10.12 Surse comparatie.json. Fiecare rând Excel are trimiteri la surse. Originalele existente sunt reutilizate, fără modificarea lor.
Nicio trimitere, semnare sau plată efectuată. Numerele de mesaje și originale salvate nu sunt majorate. Istoricul jurnalelelor este păstrat.
'''
summary=summary.replace('Calcule13.000 +planuri20.000 +asistență2.000 +PI10.000','Calcule 13.000 + planuri 20.000 + asistență 2.000 + PI 10.000').replace('structură42.000 +goluri6.000 +excavare5.000 +teren800 +Baubegleitung14.000 +final1.500','structură 42.000 + goluri 6.000 + excavare 5.000 + teren 800 + Baubegleitung 14.000 + final 1.500').replace('REALIG24.000','REALIG 24.000').replace('jurnalelelor','jurnalelor')
(dest/'2026.10.12 Jurnal actualizare comparatie.txt').write_text(summary,encoding='utf-8')
def preserve_and_prepend(p,text):
    backup=archive/p.name
    if not backup.exists(): shutil.copy2(p,backup)
    old=p.read_text(encoding='utf-8-sig')
    if text.splitlines()[0] not in old[:400]: p.write_text(text+'\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
for name in ['2026.10.12 Status proiect.txt','2026.10.12 Log progres proiect.txt']:
    preserve_and_prepend(root/name,summary)
toms=f'''2026.10.12 | Comparație servicii și prețuri finalizată
Status scurt: 16 capitole v4.1 și discuțiile TOMS comparate cu BERGER/PECH. Pachetul TOMS37.900 EUR net se compune din25.000 structură/planuri +1.500 asistență +8.000 PI +3.400 Bauwerksbuch. Confirmări punctuale Q1/Q2, fără acceptarea integrală v4.1.
Ultimul răspuns: 2026.10.08, Dagmar Zottl: refuz de preluare în prezent din lipsă de resurse, răspuns pe firul v3.
Următorul pas: clarificarea întinderii refuzului față de v4.1 și disponibilității; completarea prestatorului pentru noduri, ancore și atelier. D1 nu se consideră început.
Sursa: {book}; ID cdd301b0-457e-4452-a394-6eea21256e61; ID trimitere v4.1 64c91100-89c3-4206-8e7e-988e575385b8; Q1/Q2 și ofertele originale în sursele Excel.
Nu este comunicare nouă primită și nu a fost trimis email.
'''.replace('TOMS37.900','TOMS 37.900').replace('din25.000','din 25.000').replace('+1.500','+ 1.500').replace('+8.000','+ 8.000').replace('+3.400','+ 3.400')
berger=f'''2026.10.12 | Comparație ofertă structurală finalizată
Status scurt: oferta BERGER45.000 EUR net, cu4 poziții:13.000 calcul /20.000 planuri /2.000 asistență (max8vizite) /10.000 PI. Maximum8vizite privește asistența, nu totalul vizitelor PI. Bauwerksbuch nespecificat; excavarea și atelierul excluse.
Ultimul răspuns: 2026.08.17, Markus Berger, ofertă detaliată. Acceptarea A&C neconfirmată.
Următorul pas: prelungirea valabilității calculate până la2026.10.12, disponibilitate/calendar, lemn/ancore, formate, Planwechsel și Bauwerksbuch. Subtotal35.000 este calcul, atribuirea parțială cere acord.
Sursa: {book}; ID ce6905cb-0c93-4e6b-8cde-7e300dfc874c; oferta originală2026.08.17,4pagini.
Fără răspuns nou sau email trimis.
'''
pech=f'''2026.10.12 | Comparație ofertă structurală finalizată
Status scurt: PECH69.300 EUR net,6poziții:42.000 statică /6.000 goluri /5.000 excavare /800 inspecție teren /14.000 Baubegleitung /1.500 documente finale.12Abnahmen nu confirmă numirea Prüfingenieur.450 EUR net/recepție suplimentară. Bauwerksbuch nespecificat.
Ultimul răspuns: 2026.09.17, oferta2026-470/AN01, ID63cd2bcb. Acceptarea A&C neconfirmată.
Următorul pas: LB exactă anexată, livrabile planuri/formate, PI/§128, Bauwerksbuch, calendar/disponibilitate, drepturi de utilizare/modificare/terți și ZT-Index. Valabilitate calculată până la2026.12.16.
Sursa: {book}; ID63cd2bcb-2160-4027-b6c8-25bb42d9ae50; oferta originală2026.09.17,4pagini.
Fără răspuns nou sau email trimis.
'''
import re
for name,entry in [('TOMS',toms),('Markus Berger',berger),('Pech',pech)]:
    entry=re.sub(r'(?<=[A-Za-zĂÂÎȘȚăâîșț])(?=\d)', ' ',entry)
    entry=re.sub(r'(?<=\d)(?=[A-Za-zĂÂÎȘȚăâîșț])',' ',entry)
    # Do not alter technical UUIDs or the fixed offer number.
    entry=entry.replace('ID 63 cd 2 bcb','ID 63cd2bcb').replace('63 cd 2 bcb-2160-4027-b 6 c 8-25 bb 42 d 9 ae 50','63cd2bcb-2160-4027-b6c8-25bb42d9ae50').replace('2026-470/AN 01','2026-470/AN01')
    if name=='TOMS': entry=toms
    if name=='Markus Berger': entry=berger.replace('BERGER45.000','BERGER 45.000').replace('cu4','cu 4').replace('poziții:13','poziții: 13').replace('max8vizite','max. 8 vizite').replace('Maximum8vizite','Maximum 8 vizite').replace('la2026','la 2026').replace('Subtotal35','Subtotal 35').replace('originală2026','originală 2026').replace(',4pagini',', 4 pagini')
    if name=='Pech': entry=pech.replace('PECH69','PECH 69').replace('net,6poziții:42','net, 6 poziții: 42').replace('.12Abnahmen','. 12 Abnahmen').replace('.450','. 450').replace('oferta2026','oferta 2026').replace('ID63','ID 63').replace('la2026','la 2026').replace('originală2026','originală 2026').replace(',4pagini',', 4 pagini')
    preserve_and_prepend(partners/f'2026.10.12 Log discutii - {name}.txt',entry)
readme=root/'folder map/README.md'
preserve_and_prepend(readme,f'''# 2026.10.12 — Comparație servicii și prețuri structură

Rezultat: ../{book}. Două foi: 1 Servicii (47 rânduri, capitolele v4.1 și discuțiile TOMS) și 2 Preturi (24 rânduri, poziții, totaluri și condiții). Datele TOMS, BERGER și PECH sunt documentate separat în același dosar. Totaluri net37.900 /45.000 /69.300 EUR, cu domenii diferite. TOMS v4.1 TRIMIS, acceptare neconfirmată și refuz actual2026.10.08; BERGER/PECH acceptare neconfirmată. Nu sunt comunicări noi sau plăți. Jurnalul actualizării: ../04. Firme + Executie/2026.10.12 Comparatie servicii structura/2026.10.12 Jurnal actualizare comparatie.txt. Verificarea zilnică2026.10.12 este păstrată mai jos.
'''.replace('net37','net 37').replace('actual2026','actual 2026').replace('zilnică2026','zilnică 2026'))
register=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.12 Registru comunicatii.json'
if not (archive/register.name).exists(): shutil.copy2(register,archive/register.name)
r=json.loads(register.read_text(encoding='utf-8'))
entry={'data':'2026.10.12','tip':'comparatie_locala_servicii_preturi','sursa':book,'mesaje_noi':0,'originale_noi':0,'trimiteri':0,'status':'TOMS v4.1 trimis, acceptare neconfirmată; BERGER/PECH acceptare neconfirmată','net_EUR':{'TOMS':37900,'BERGER':45000,'PECH':69300},'limita':'Totaluri cu domenii diferite. Analiză a documentelor existente, fără acceptare ori disponibilitate dedusă.'}
updates=r.setdefault('actualizari_punctuale',[])
if isinstance(updates,list):
    if not any(x.get('tip')==entry['tip'] for x in updates if isinstance(x,dict)):updates.append(entry)
else:updates['comparatie_servicii_preturi_2026.10.12']=entry
register.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Updated project, TOMS, BERGER, PECH journals and reference registry; preserved earlier versions; no email counts changed.')
