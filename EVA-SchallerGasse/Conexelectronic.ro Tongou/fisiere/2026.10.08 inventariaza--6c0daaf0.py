from pathlib import Path
import json,csv,hashlib,shutil
R=Path.cwd(); A=R/'Acasa'; D='2026.10.08'
for sub in ['Poze originale','Liste','Surse','Lucru']: (A/sub).mkdir(parents=True,exist_ok=True)
ids=['ead1a92a-101d-415f-af7e-d3bd9df36313','ad3d7875-7901-41ad-8978-fa30a146d5f7','d6b0c152-a9e3-4677-92f6-50b5ec8dc393','0090594c-baa6-4d6b-a7e2-8a5c1ddc6a06','e088c6dd-40d0-4609-816e-91f93e52a8df','8e5b535c-5f14-42b0-8900-cb32a7485361','9809a332-ee96-4549-942f-a29bb358b432']
manifest=[]
for i,k in enumerate(ids,1):
 p=Path('C:/Users/User/AppData/Local/Temp')/f'codex-clipboard-{k}.png'; out=A/'Poze originale'/f'{D} Foto {i:02d}.png'; shutil.copy2(p,out)
 manifest.append(dict(foto=f'F{i}',original=str(p),salvat=str(out.relative_to(A)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),statut='Primit de la utilizator în chat; data capturii necunoscută'))
(A/'Surse'/f'{D} Manifest fotografii.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
cat=R/'04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.08 Catalog comparativ'
products=json.loads((cat/'Date structurate'/f'{D} produse-normalizate.json').read_text('utf8')); P={p['sku']:p for p in products}
rows=[]
def add(f,pos,tip,qty,poli='',rating='',marca='Schneider Electric',certainty='✓ Vizibil',note='',plan='V'):
 rows.append(dict(ID=f'F{f}-{sum(x["Foto"]==f"F{f}" for x in rows)+1:02d}',Foto=f'F{f}',Pozitie=pos,Tip=tip,Cantitate=qty,Poli=poli,Marcaj=rating,Marca=marca,Certitudine=certainty,Observatii=note,Plan=plan))
def m(f,pos,poli,rating,qty=1,note='',certainty='✓ Vizibil'):
 plan='H' if rating in ['C80','C100'] else ('M1' if poli=='1P+N' else ('M3' if poli=='3P' else 'M4' if poli=='4P' else 'V'))
 add(f,pos,'Disjunctor MCB',qty,poli,rating,certainty=certainty,note=note,plan=plan)
m(1,'Sus stânga / CASA','4P','Ilizibil',note='4 manete cuplate; nominalul nu poate fi citit.',certainty='? Marcaj incomplet')
add(1,'Sus central / aparat suspendat','Aparat modular văzut din spate',1,'3P aparent',marca='Neidentificată',certainty='? Neidentificat',note='Nu poate fi clasificat sigur drept disjunctor/contactor din această vedere.')
for s in ['R','S','T']: m(1,'Rând superior / '+s,'1P','C50',note='Aparate separate; nu presupune declanșare comună trifazată.')
m(1,'Rând superior / PISCINĂ','3P','C20')
m(1,'Rând superior / ALARMĂ - PRIZE S-EST','3P aparent','C16',certainty='? Grupare de confirmat',note='Etichetele de circuite traversează modulele; confirmă dacă sunt poli cuplați sau circuite separate.')
m(1,'Rând superior / după C16','3P aparent','C10',certainty='? Grupare de confirmat',note='Cablurile și materialul negru ascund separația aparatelor.')
add(1,'Rând superior / zona acoperită înainte de nr. 1','Aparate modulare acoperite','Necunoscut',marca='Schneider Electric',certainty='? Acoperit',note='Fără numărare suplimentară: posibilă suprapunere cu grupul C10.')
for n in range(1,40):
 rating='Ilizibil'; cert='? Marcaj incomplet'; note='Numerotarea este reper vizual, nu identificare a consumatorului.'
 if n in [7,8,13,14,15,25,26]: note+=' Poziție dedusă din succesiunea 1–39; ascunsă/parțial în afara cadrului. Nu este aparat confirmat independent.';cert='? Poziție dedusă'
 if n in [10,11,12,16]: rating='C16'; cert='✓ Vizibil'
 if n in [17,18,21,22,23,24]: rating='C10';cert='✓ Vizibil'
 if n in [27,28,29,30,31]: rating='C6';cert='✓ Vizibil'
 if n in [1,2,3,4,5,6]: rating='C20 aparent';note+=' Valoare de confirmat prin fotografie apropiată.'
 m(1,f'Circuit numerotat {n}', '1P+N probabil',rating,qty=0 if cert=='? Poziție dedusă' else 1,note=note,certainty=cert)
 rows[-1]['Plan']='M1'; rows[-1]['Poli']='1P+N probabil'
add(1,'Jos / două prize rotunde','Priză modulară DIN cu contact de protecție',2,marca='Neidentificată',note='Curent nominal ilizibil; fără echivalent în catalogul analizat.',plan='A')
add(1,'Jos central / Siemens','Contactor de putere',1,'3P aparent',marca='Siemens',certainty='? Cod ilizibil',plan='K')
add(1,'Jos / stânga contactorului Siemens','Contactor/releu auxiliar',1,marca='Neidentificată',certainty='? Identificare provizorie',plan='K')
m(1,'Jos dreapta','3P','Ilizibil',certainty='? Marcaj incomplet')
add(1,'Sus dreapta / capac fumuriu','Bloc de distribuție cu capac',1,marca='Neidentificată',plan='A')
add(2,'Sus / ALIMENTARE PANOURI SOLARE ȘI C.E.','Contactor de putere',1,'3P','3RT1054-1…6',marca='Siemens SIRIUS',certainty='? Sufix / bobină ilizibile',note='Inscripția nu dovedește comutație DC; categoria AC/DC și tensiunea bobinei trebuie citite.',plan='K')
add(2,'Lateral contactor','Bloc auxiliar atașat',1,marca='Siemens probabil',certainty='? Referință ilizibilă',plan='A')
m(2,'Jos stânga','1P+N','C16')
m(2,'Jos / POMPE','1P+N','C6 aparent',certainty='? Valoare de confirmat')
m(2,'Jos / CENTRALE ELECTRICE','3P','C80')
m(2,'Jos dreapta','4P','C40')
for pos in ['Sus stânga','Sus dreapta']:
 add(3,pos,'Contactor de putere',1,'3P','3RT10…',marca='Siemens SIRIUS',certainty='? Cod complet ilizibil',note='Nu se atribuie curent nominal după aspect; citește plăcuța și bobina.',plan='K')
add(3,'Margine stângă sus','Disjunctoare parțial vizibile',2,'Nedeterminat','Ilizibil',certainty='? Cadru incomplet',note='Pot aparține altui compartiment; nu se presupune duplicare sau aparat suplimentar sigur.')
for pos,pol in [('Jos stânga','3P'),('Jos centru-stânga','4P aparent'),('Jos centru-dreapta','3P'),('Jos dreapta','3P')]:m(3,pos,pol,'Ilizibil',certainty='? Marcaj incomplet')
add(3,'Peste contactorul drept','Ecran izolant transparent',1,marca='Neidentificată',plan='A')
add(3,'Jos / între grupuri','Conectori / blocuri de conexiune','Necunoscut',marca='Neidentificată',plan='A')
for n,r in enumerate(['C40','C40','C16','C6'],1):m(4,f'Sus / nr. {n}','3P',r)
for n in range(5,18):m(4,f'Sus / nr. {n}','1P+N','C20' if n<8 else 'C10' if n==8 else 'C6',note='Nominal și numerotare de reconfirmat la inventarul fizic.')
for n in range(1,8):add(4,f'Rând median / K{n}','Contactor compact',1,'3P + auxiliar aparent',marca='Schneider / Telemecanique',certainty='? Referință și bobină ilizibile',plan='K')
add(4,'Dreapta / cadran circular','Ceas programator analogic DIN',1,marca='Neidentificată',certainty='? Cod și contacte ilizibile',plan='T')
for pos,r in [('Sus','C100'),('Jos stânga','C100'),('Jos dreapta','C63')]:m(5,pos,'3P',r)
for n,r in enumerate(['C16','C16','C10','C40','C16','C16','C16'],1):m(6,f'Rând principal / de la stânga {n}','3P',r)
for n,r in enumerate(['C10','C6'],1):m(6,f'Dreapta / disjunctor {n}','1P+N',r)
add(6,'Sus / stânga, centru, dreapta','Transformator de curent',3,'','METSECT…',certainty='? Raport/clasă ilizibile',note='Trei corpuri vizibile, cel stâng este tăiat de cadru. Necesare raport primar/secundar, VA și clasa.',plan='CT')
add(6,'Deasupra disjunctoarelor','Bară pieptene trifazată',1,'3P','A9XPH357; 100 A / 40 °C aparent',note='Compatibilitatea mecanică nu se transferă automat la Tongou.',plan='A')
add(6,'Colț inferior dreapta','Aparat modular parțial vizibil',1,marca='Schneider Electric',certainty='? Neidentificat',note='Fără echivalare; nu se vede fața aparatului.')
for n,r in enumerate(['C32','C16','C32'],1):m(7,f'Sus / grup {n}','3P',r)
for n in range(1,4):m(7,f'Sus dreapta / disjunctor {n}','1P+N','C10')
m(7,'Jos stânga / separat','1P+N','C25')
m(7,'Jos central / primul grup','3P','C6')
for n in range(1,6):m(7,f'Jos / după C6 / disjunctor {n}','1P+N','C16')
add(7,'Jos dreapta','Contactor compact',1,'3P + auxiliar aparent',marca='Schneider Electric',certainty='? Cod / bobină ilizibile',plan='K')
for f in range(1,8):
 add(f,'Distribuite în fotografie','Borne PE / N / trecere și suporturi','Necunoscut',marca='Mărci ilizibile',note='Tipurile apar diferit în fiecare cadru; cantități și secțiuni de inventariat fizic.',plan='A')
 add(f,'Structură și conexiuni','Șine DIN, cabluri, papuci / ferule și carcasă','Necunoscut',marca='Diverse',note='Lungimi, secțiuni, tipuri de izolație și numărul terminalelor nu pot fi stabilite complet din fotografie.',plan='A')
 if f in [1,4,7]:add(f,'Trasee interioare','Canale de cablu / capace','Necunoscut',marca='Neidentificată',plan='A')
plans={
'M1':('✓ Propunere condiționată','43082','43079;43070','RCBO smart monofazat: preferință Zigbee, alternativ Wi-Fi.','Păstrează nominalul și curba circuitului; reglajul electronic 1–40 A nu dovedește echivalența unui MCB fix C6/C10/C16. Cere tip A, 30 mA unde cerut, capacitate de rupere și protecție autonomă fără cloud. 1P+N nu înseamnă doi poli protejați. Alternativa 2P cere verificarea schemei.'),
'M3':('✓ Propunere condiționată','43080','43071;43077;43068','RCBO smart 3P Zigbee, Wi-Fi alternativ; MCB smart doar dacă diferențialul este separat.','Nu înlocuiește direct C6–C40 cu C63. Confirmă curba, pragul termomagnetic real, Icn/Icu și tipul diferențial. Pentru consumatori cu N poate fi necesar 3P+N/4P; verifică schema. Pentru C63, 43089 este MCB fix C63 fără diferențial/smart, doar după verificarea capacității de rupere.'),
'M4':('✓ Propunere condiționată','43081','43078','RCBO smart 4P Zigbee; alternativ MCB smart 4P plus protecție diferențială separată.','Confirmă 3P+N versus 4 poli protejați, utilizarea neutrului și selectivitatea. 43081 este reglabil 1–63 A / 30–500 mA în catalog; aceasta nu confirmă echivalența cu un C40 fix. Wi-Fi 4P RCBO nu este disponibil în cele 29 produse analizate.'),
'H':('✗ Fără echivalent direct','','','MCB 80/100 A: aparat dimensionat separat, monitorizare smart distinctă.','Nu se înlocuiește cu Tongou 63 A. Necesare curent proiectat, curent de scurtcircuit, secțiuni, selectivitate și categoria aparatului.'),
'K':('✗ Fără echivalent direct','','','Contactor adecvat sarcinii + comandă smart separată, dacă este necesară.','Un întrerupător smart nu este echivalent de contactor. Confirmă AC-1/AC-3, curent, bobină, contacte auxiliare, interblocări și frecvența manevrelor. Nu deduce 115 A din codul Siemens incomplet.'),
'CT':('✗ Fără echivalent direct','','','Transformatoare de curent și contor compatibile, selectate separat.','Contorizarea internă a unui smart breaker nu înlocuiește automat CT-urile sau protecția/contorul existent.'),
'T':('✓ Funcție parțială; stoc epuizat','43074','','Temporizare Zigbee posibilă numai ca funcție de comandă, după verificări.','43074 este întrerupător smart, nu ceas cu contacte echivalente garantate. Stoc 0. Verifică contact uscat/ieșire alimentată, tensiune bobină și funcționare fără internet; nu comuta sarcina contactorului printr-o echivalare de aspect.'),
'A':('✗ Fără echivalent în selecție','','','Accesoriu / componentă de păstrat sau dimensionat separat.','Catalogul Tongou de 29 produse nu conține un echivalent verificat. Nu se deduc secțiuni și curenți după fotografie.'),
'V':('? Identificare necesară','','','Nicio înlocuire propusă înaintea identificării.','Citește codul integral, nominalul, numărul polilor și funcția. Pentru R/S/T verifică dacă sunt trei circuite separate sau alimentare comună înainte de a propune aparat multipolar.')}
equiv=[]
for r in rows:
 status,sku,alts,solution,limits=plans[r['Plan']]
 p=P.get(sku); tech=p['technical'] if p else {}
 equiv.append({'ID existent':r['ID'],'Foto / poziție':r['Foto']+' / '+r['Pozitie'],'Echipament existent':r['Tip']+' '+r['Poli']+' '+r['Marcaj'],'Statut':status,'SKU preferat':sku,'Model / produs':p['name'] if p else 'Fără echivalent verificat','Protocol':tech.get('Comunicație SKU','—'),'Alternative SKU':alts,'Propunere':solution,'Diferențe / condiții':limits+' '+r['Observatii'],'Stoc buc.':tech.get('Cantitate disponibilă (buc.)','—'),'Data stoc':D if p else '—','Preț RON cu TVA':tech.get('Preț cu TVA (RON)','—'),'Sursă':p['source'] if p else 'Inventar foto / catalog Tongou analizat'})
selected=['43082','43079','43080','43081','43070','43071','43077','43078','43068','43089','43074','43094','43095','43096','43097','43098']
sources=[]
for sku in selected:
 p=P[sku];t=p['technical'];sources.append({'SKU':sku,'Denumire':p['name'],'Protocol':t.get('Comunicație SKU','—'),'Poli':p['poles'],'Curent A':t.get('Curent nominal / reglaj (A)','—'),'Diferențial mA':t.get('Curent diferențial (mA)','—'),'Stoc':t['Cantitate disponibilă (buc.)'],'RON cu TVA':t['Preț cu TVA (RON)'],'Observații':' '.join(p['observations']),'Sursă':p['source']})
protection=[
 ['1. Identificare și verificări','Inventarul este vizual; nu este proiect de execuție.','Electricianul identifică sistemul de legare la pământ, N/PE/PEN, secțiuni, impedanță buclă, curenți de scurtcircuit, izolație și continuitate PE. În F3 apar conductoare verde-galben la bornele aparatelor: destinația lor trebuie verificată prioritar, fără concluzie numai din culoare.'],
 ['2. Supracurent / scurtcircuit','Nominalul circuitului se păstrează după calcul și măsurători.','Nu se majorează C6/C10/C16 etc. la C63 pentru a obține funcții smart. Pentru C80/C100 nu există echivalent direct în selecția Tongou.'],
 ['3. Protecție diferențială','RCBO pe circuit, tip adecvat sarcinii; 30 mA pentru protecția suplimentară unde aplicabil.','Tip A pentru aplicații compatibile; F/B ori soluția cerută de producător pentru convertoare, pompe, fotovoltaic sau încărcare EV. Tipul A/B al SKU-urilor Tongou propuse nu este confirmat. Nu se setează 100–500 mA ca substitut pentru 30 mA. Absența unui RCD în poze nu dovedește absența sa în instalație.'],
 ['4. Supratensiuni tranzitorii AC','SPD coordonat la intrare și subtablouri, după evaluare.','Candidați 43094/43095/43096 (2/3/4P, 275 V, 15/40 kA), fără Zigbee/Wi-Fi. Numărul polilor, tipul T1/T2/T3, Up, sistemul TT/TN și protecția de rezervă trebuie confirmate. Nu se declară protecție la trăsnet doar după 40 kA.'],
 ['5. Fotovoltaic / DC','Numai dacă circuitele sunt efectiv DC.','43097 (500 V DC) / 43098 (1000 V DC) sunt candidați SPD, nu disjunctoare și nu separatoare. Alegerea cere Voc maxim la rece și configurația stringurilor; eticheta PANOURI SOLARE nu este suficientă.'],
 ['6. Supratensiune susținută / faze','Funcție distinctă de SPD.','Verifică pragurile, timpul de reacție, pierderea/ordinea fazelor și defectul de neutru. Nu atribui toate acestea fiecărui Tongou doar pentru că este smart.'],
 ['7. Arc electric / incendiu','Evaluează necesitatea AFDD pe circuitele potrivite.','Niciun AFDD verificat în catalogul celor 29 de produse. Protecția la temperatură a aparatului nu este detecție de arc pe tot circuitul.'],
 ['8. Motoare, pompe, piscină','Protecția motorului și cerințele zonelor umede se verifică separat.','Contactoarele și RCBO nu substituie automat protecția termică de motor. Verifică legăturile echipotențiale, separarea circuitelor și condițiile specifice piscinei.'],
 ['9. Zigbee prioritar / Wi-Fi alternativ','Comanda și monitorizarea se adaugă protecției electrice validate.','Confirmă gateway-ul și compatibilitatea exactă, inclusiv funcționarea locală. Protecțiile trebuie să funcționeze fără cloud. Reînchiderea automată după defect se dezactivează implicit până la evaluarea riscului, în special la motoare și piscină.'],
 ['10. Achiziție','Listă de candidați, nu comandă sau deviz final.','Stocurile și prețurile sunt captura catalogului 2026.10.08; același SKU propus la multe rânduri nu înseamnă stoc alocat fiecărui rând. Nu se însumează prețurile în lipsa cantităților confirmate și a echivalenței certificate.']]
def csvout(name,data):
 with (A/'Liste'/f'{D} {name}.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter=';');w.writeheader();w.writerows(data)
csvout('Lista echipamente identificate',rows);csvout('Lista echivalente propuse',equiv)
bundle=dict(inventory=rows,equivalents=equiv,products=sources,protection=protection,photos=manifest)
(A/'Surse'/f'{D} Inventar si echivalente.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2),encoding='utf8')
guide=f'''ACASA — INVENTAR FOTO ȘI ECHIVALENTE PROPUSE — {D}
7 fotografii originale arhivate, fără modificări, cu SHA-256 în manifest.
{len(rows)} poziții de inventar (inclusiv accesorii și poziții ascunse). Nu reprezintă {len(rows)} aparate.
Cantitate 0 la o poziție dedusă înseamnă zero aparate confirmate vizual, NU lipsa fizică a aparatului.
Pozele sunt tratate ca șapte vederi. Numărul de tablouri distincte și eventualele dubluri nu sunt confirmate. Nu se face total de comandă.
Inventarul acoperă echipamentele vizibile; codurile ilizibile și componentele acoperite sunt marcate. Data fotografierii și amplasamentul instalației nu sunt confirmate. „Acasa” este denumirea cerută pentru dosar, nu o constatare că fotografiile provin din Schallergasse.

CITEȘTE: {D} Acasa inventar si echivalente.xlsx
Foi: Echivalente propuse; Inventar foto; Protectie; Produse candidate.
În Liste sunt cele două liste separate CSV. În Poze originale sunt F1–F7 în ordinea primită.
Legendă: ✓ albastru = funcție suplimentară/candidat condiționat, NU echivalență certificată; ✓ verde în inventar = marcaj vizibil; ? galben = necunoscut; ✗ roșu = fără echivalent în selecția analizată. Stoc 0 = epuizat.
Niciun rând de propunere nu este autorizare de înlocuire sau confirmare a protecției maxime. Prioritatea este protecția certificată și dimensionată corect, apoi Zigbee, apoi Wi-Fi.
Principalele blocaje: MCB C80/C100, contactoare, CT, accesorii și coduri ascunse. RCBO smart cu prag electronic reglabil nu dovedește echivalența cu MCB fix de curba C. Tipul diferențial și capacitatea de rupere trebuie confirmate pentru SKU exact.
Datele Tongou sunt reutilizate din catalogul arhivat {D}, cu sursa URL pe fiecare produs. Datasheet-urile originale și matricea completă cu 29 de produse rămân în:
{cat}
Nu s-au făcut comenzi, modificări fizice, trimiteri de email sau rezervări de stoc.
'''
(A/f'{D} Citeste intai.txt').write_text(guide,encoding='utf8')
(A/'Surse'/f'{D} Cerere utilizator.txt').write_text('Data primirii: '+D+'\nSubiect: Acasa — inventar din fotografii și echivalente Tongou\nExpeditor: utilizator în chat\nDestinatar: asistent\nCC: nu se aplică\nID Eva-Mail: nu se aplică\nStatut: PRIMIT în chat; nu este email\n\nextrage din imagine lista completa de toate echipamentele utilizate si echivaleaza cu produsele tongue identificate\nsalveaza pozele si lista in folder separat cu denumirea "Acasa" in baza folderului principal schaller - salveaza pozele / lista identificata / lista cu echivalente propuse\ndorim maxim de protectie de preferat Zigbee / Wifi\n',encoding='utf8')
print(json.dumps({'inventory_rows':len(rows),'photos':len(manifest),'products':len(sources)},ensure_ascii=False))
