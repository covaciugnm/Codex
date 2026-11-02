from pathlib import Path
import json, hashlib, datetime, sqlite3, shutil
root=Path.cwd()
base=root/'folder map'
out=root/'01. Proprietate + Acte/Contract Vanzare Cumparare/2026.10.28 Analiza predare documentatie'
out.mkdir(exist_ok=True)
note='''2026.10.28 | Analiza obligatiei de predare a documentatiei de autorizare

CONCLUZIE
Exista un argument juridic serios pentru obligatia accesorie a vanzatoarei de a preda documentatia existenta, relevanta si necesara utilizarii autorizatiilor garantate. Contractul nu contine o clauza expresa care sa enumere predarea tuturor documentelor care au stat la baza autorizarii. Nu este demonstrata o obligatie nelimitata de a recrea documente inexistente ori de a furniza automat fisiere CAD editabile.

CONTRACT SEMNAT 2026.02.20
Original: 01. Proprietate + Acte/Contract Vanzare Cumparare/Kaufvertrag_Schallergasse_35_signiert.pdf
SHA256 237ff87a2576302a4e44316009eb4cea18d387029f7b0d353d8d49b12c4da365, identic indexului.
Pct. 1.2 si 2.1: accesorii juridice/materiale si transmiterea drepturilor aferente imobilului.
Pct. 4.3: predare chei si proces-verbal; nu inventar complet al dosarului de autorizare.
Pct. 7.1(d), p.9: garantie expresa pentru autorizatiile definitive de utilizare si pentru mansarda, BV12-340248/2023 si MA37/1539234-2021-1. Contractul mentioneaza Rechtskraft la 2023.06.01 conform informatiei autoritatii si termenul 2027.06.01 pentru Bauanzeige conform §74. Aceasta este o garantie contractuala; nu este verificarea independenta a dovezii administrative ori a termenului aplicabil astazi.
Pct. 7.2: indemnizare daca garantiile 7.1 erau incorecte la predare. Lipsa unei copii nu demonstreaza singura lipsa autorizatiei sau activarea indemnizarii.
Pct. 7.3: garantie conform legii. Pct. 7.4-7.5: stare de renovat si inspectia cumparatoarei; nu exclud expres documentatia autorizarii.
Pct. 10.1-10.2: integralitatea contractului si desfiintarea de comun acord a ofertei 2025.12.29 considerate executate. O promisiune dintr-un draft nu trebuie tratata automat ca obligatie finala.
Pct. 10.7, p.12: avocatul redactor nu a consultat Bauakt la autoritate. Nu confirma completitudinea dosarului.
Paginile 9-12 au fost verificate vizual in original; fara validare criptografica a semnaturilor.

PROBE DE PREDARE
Proces-verbal 2026.03.17, original CH_260317_Übergabeprotokoll_Schallergasse_35.pdf, SHA256 95a38ffe17d43718584749fa9854e4442e00b9a76f6ad11d87242fed0405342d, identic indexului. Paginile 1-2 verificate vizual: preluare fara rezerve, teme deschise barate; D: weitere Dokumente: elektronisch gespeichert. Semnaturi vizibile. Nu contine inventar individual al documentelor.
Email PRIMIT in casuta Gmail 2026.03.17 12:25 UTC, ID Eva-Mail 48df163b-ac4a-4a3e-9dd2-ab2b4c25bec4: Bogdan Capra catre M.Kornhofer@cp-ag.at; CC cosmin.covaciu@ipec.ro, covaciu.gnm@gmail.com, C.Asreahan@cp-ag.at. Confirma primirea Ordner Bestandsunterlagen sowie Energieausweis DG + Bauphysikalische Unterlagen. Lantul include cererea avocatului din 2026.03.16 pentru documentele tehnice si alte acte. Corpul arhivat este trunchiat la 20.000 caractere, dar pasajul relevant este disponibil. Exporturile TXT/JSON si atasamentul original sunt deja arhivate; copii relevante pastrate in acest dosar.
Confirmarea poate fi invocata de vanzatoare. Nu dovedeste singura ca fiecare plan vizat/anexa necesara a fost inclus. Nu se poate afirma ca nu s-a predat niciun document.

TEMEI SI LIMITE
§914 ABGB: interpretare dupa intentia partilor si uzantele loiale. §§1061/1047 ABGB: predarea bunului cu accesoriile sale.
https://www.ris.bka.gv.at/eli/jgs/1811/946/P914/NOR12018638
https://www.ris.bka.gv.at/eli/jgs/1811/946/P1047/NOR12018776
OGH 1 Ob 190/02a, 2002.11.26: intr-un litigiu privind teren contaminat, instanta considera cel putin informarea despre obligatiile autoritatii, daca nu chiar predarea tuturor documentelor existente aferente, drept obligatie accesorie a vanzatorului. Analogie utila, nu hotarare care impune automat orice dosar de autorizare in toate vanzarile.
https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_20021126_OGH0002_0010OB00190_02A0000_000/JJT_20021126_OGH0002_0010OB00190_02A0000_000.pdf
Surse RIS consultate prin cautare web la 2026.10.28; deschiderea directa a unor pagini RIS a esuat, pasajul relevant al deciziei a fost disponibil in rezultatul indexat.

URMATORUL PAS
Solicitarea catre CERHA a pachetului exact primit in 2026.03.17, cu inventar; comparatie cu Bauakt MA37. Cerere punctuala catre vanzatoare pentru planuri vizate, descrierea aprobata, calcule/expertize/anexe care fac parte din autorizare, modificari si dovada Rechtskraft ori indicarea detinatorului. Termen propus de remediere 14 zile, necomunicat. Costurile/despagubirile necesita temei si prejudiciu demonstrat; nu sunt automat datorate. Nu exista email nou trimis/draft creat sau verificare noua Eva-Mail.
'''
p=out/'2026.10.28 Analiza obligatie predare documentatie.txt';p.write_text(note,encoding='utf-8')
changed=[p]
src=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/CERHA HEMPEL'
for f in src.glob('*48df163b.*'):
    q=out/f.name;shutil.copy2(f,q);changed.append(q)
src=root/'04. Firme + Executie/00. Oferte primite/Übergabeprotokoll/CH_260317_Übergabeprotokoll_Schallergasse_35.pdf'
q=out/'2026.03.17 Proces verbal predare original.pdf';shutil.copy2(src,q);changed.append(q)
entry='''\n2026.10.28 | Analiza predare documentatie de autorizare - vanzatoare / CERHA
Status scurt: temei serios pentru obligatie accesorie privind documentatia existenta necesara; fara clauza expresa pentru toate actele. Analiza, nu pretentie admisa.
Ultimul raspuns relevant: email Capra 2026.03.17 confirma Bestandsunterlagen + Energieausweis DG + Bauphysikalische Unterlagen; proces-verbal fara rezerve, fara inventar individual. Fara verificare email nou.
Urmatorul pas: recuperarea pachetului exact de la CERHA si comparatie cu MA37, apoi cerere punctuala vanzatoare.
Sursa: 01. Proprietate + Acte/Contract Vanzare Cumparare/2026.10.28 Analiza predare documentatie/2026.10.28 Analiza obligatie predare documentatie.txt; contract 7.1(d), 7.2, 10.7; OGH 1 Ob 190/02a. Contractul afirma Rechtskraft 2023.06.01; dovada administrativa independenta ramane de obtinut. Fara trimitere/acceptare.
'''
for rel in ['2026.10.28 Log progres proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - CP Immobilien - Kornhofer.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.28 Log discutii - CERHA HEMPEL.txt']:
    q=root/rel
    with q.open('a',encoding='utf-8') as f:f.write(entry)
    changed.append(q)
with (base/'README.md').open('a',encoding='utf-8') as f:f.write(entry)
# Scoped incremental index: retain all prior entries, update only files written above.
index=base/'inventar.json'; backup=base/'2026.10.28 QA contract cumparare/2026.10.28 inventar anterior.json';shutil.copy2(index,backup)
rows=json.loads(index.read_text(encoding='utf-8'));by={r['cale']:r for r in rows}
db=sqlite3.connect(base/'cautare.sqlite')
for p in changed:
    rel=p.relative_to(root).as_posix();h=hashlib.sha256(p.read_bytes()).hexdigest();st=p.stat()
    if p.suffix=='.pdf':tx=(base/'texte/95a38ffe17d43718584749fa9854e4442e00b9a76f6ad11d87242fed0405342d.txt').read_text(encoding='utf-8')
    else:tx=p.read_text(encoding='utf-8-sig')
    cache=base/'texte'/f'{h}.txt';cache.write_text(tx,encoding='utf-8')
    r=dict(cale=rel,folder=p.parent.relative_to(root).as_posix(),extensie=p.suffix,octeti=st.st_size,modificat=datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),modificat_ns=st.st_mtime_ns,sha256=h,duplicat_al='',ce_reprezinta='Analiza predare documentatie / sursa / jurnal',baza_descrierii='actualizare punctuala 2026.10.28',extras_continut=tx[:1000],stare_citire='text citit',text_cache=cache.relative_to(root).as_posix(),detalii={},rezumat_verificat='',ocr_cache='')
    by[rel]=r
    db.execute('DELETE FROM documente WHERE cale=?',(rel,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(rel,r['ce_reprezinta'],tx,h))
db.commit();db.close();index.write_text(json.dumps(list(by.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Salvate si indexate {len(changed)} fisiere; inventar.json si cautare.sqlite actualizate punctual. CSV/XLSX derivate nu regenerate.')
