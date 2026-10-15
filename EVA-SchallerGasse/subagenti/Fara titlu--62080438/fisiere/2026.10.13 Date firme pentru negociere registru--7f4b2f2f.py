from pathlib import Path
import json,hashlib
root=Path.cwd()
work=root/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
local=json.loads((work/'2026.10.13 Date firme pentru negociere surse locale.json').read_text(encoding='utf-8'))
sources=[]
ids={'BERGER':'L01','PECH':'L02','AC FBA':'L03','AC UID':'L04','BERGER R05':'L05','PECH R05':'L06'}
for s in local:
 s=dict(s);s['id']=ids[s['id']];s['consulted']='2026.10.13';sources.append(s)
sources[0]['document_date']='2026.08.17'
sources[1]['document_date']='2026.09.17'
sources[2].update(document_date='2026.04.01',limit='FBA furnizat de ADVOKAT, sursă declarată BMJ; documentul însuși precizează Kein amtliches Dokument. Nu este extras oficial obținut live în 2026.10.13.')
sources[3]['document_date']='2026.03.19'
mail='08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/Avunduk/2026.08.10 09-18 TRIMIS Angebotsanfrage Prüfingenieur-Leistungen 8306b254.txt'
sources.append(dict(id='L07',path=mail,sha256=hashlib.sha256((root/mail).read_bytes()).hexdigest(),document_date='2026.08.10',consulted='2026.10.13',eva_id='8306b254-00a9-4d9f-9eb0-5325a22d57c9',status='TRIMIS',limit='Export text Eva, nu MIME integral; semnătură pentru contact, nu extras de reprezentare.'))
web=[
 ('W01','https://www.zt-pech.at/impressum/','Site-ul PECH, Impressum','Pagina deschisă; denumire, UID, adresă, contacte și patru Geschäftsführer publicați. Nu înlocuiește extrasul oficial actual.'),
 ('W02','https://www.zt-pech.at/kontakt/','Site-ul PECH, Kontakt','Pagina deschisă; denumire comercială scurtă și adresa biroului /11.'),
 ('W03','https://firmen.wko.at/bmstr-dipl-ing-fh-markus-berger-gmbh/wien/?firmaid=663f17c9-858c-462b-b4ef-c5db865dbbd2','WKO Firmen A-Z, BERGER','Textul indexat de motor a fost disponibil; deschiderea directă a dat 429, ulterior cache miss. GISA/GLN/FN/instanță sunt date publicate WKO, nu extras GISA live descărcat.'),
 ('W04','https://www.firmenabc.at/bmstr-dipl-ing-fh-markus-berger-gmbh_EAmz','FirmenABC, date Creditreform BERGER','Pagina deschisă; sursă secundară pentru UID și reprezentarea independentă. Nu este Finanzamt, VIES sau Firmenbuch live.'),
 ('W05','https://www.firmenbuchgrundbuch.at/de/abfrageservices/firmenbuch/fn/316003?affiliate=-1&source=fi','HF Data, pagina de comandă BERGER','Pagină publică pentru FN și identitate. Extrasul propriu-zis este contra cost și nu a fost cumpărat/deschis; pagina afișează Stichtag 2026.07.17, nu dovedește extragere live la data cercetării.'),
 ('W06','https://www.firmenbuchgrundbuch.at/de/abfrageservices/firmenbuch/fn/426034','HF Data, pagina de comandă PECH','Pagina publică confirmă identificarea FN; extrasul propriu-zis nu a fost obținut. Data afișată este 2026.09.15.'),
 ('W07','https://www.wirtschaft.at/u/668224h','wirtschaft.at, A&C','Rezultatul de căutare indica Schallergasse 35, însă pagina efectiv deschisă indica Parkring 2 și cache mai vechi. Se consemnează neconcordanța; nu se alege online ca dovadă actuală a adresei.'),
 ('W08','https://www.wirtschaft.at/u/426034x','wirtschaft.at, PECH','Pagina deschisă publică patru Geschäftsführer, fiecare cu reprezentare independentă. Sursă comercială secundară; nu extras oficial actual.'),
 ('W09','https://firmenakte.at/business/426034x-dr-pech-ziviltechnikergesellschaft-mbh','Firmenakte, PECH','Sursă secundară, declară Stand der Registerdaten 2026.10.02; confirmă patru Geschäftsführer, FN și instanță, fără a fi certificat registrul oficial de către cercetare.'),
 ('W10','https://www.bmberger.at/','Site-ul declarat BERGER','Încercările https și http nu au furnizat conținut accesibil prin instrumentul web. Impressum nu a fost verificat.'),
 ('W11','https://ac-wohnart.at/','Domeniul A&C','Încercarea de acces nu a furnizat conținut. Nu am verificat un Impressum A&C.'),
 ('W12','https://www.gisa.gv.at/abfrage','GISA oficial, formular public','Formularul oficial a fost accesibil, fără rezultat individual interogat sau extras obținut. Numărul BERGER este din WKO, nu din acest formular.'),
]
sources.extend(dict(id=i,url=u,title=t,consulted='2026.10.13',limit=l,sha256=None,hash_note='Nu a fost descărcată o copie HTML integrală; nu se inventează hash al paginii web.') for i,u,t,l in web)
def f(field,value,src,location,status='documentat istoric / de reconfirmat înainte de semnare',note=''):
 return dict(field=field,value=value,sources=src,location=location,status=status,note=note)
ac=[
 f('legal_name','A&C Wohnart Immobilien GmbH',['L03','L04','L01','L02','W07'],'L03 p. 1; L04 p. 1; antet destinatar L01/L02 p. 1',note='AC-Wohnart este o grafie a domeniului/contactului, nu denumirea juridică a societății din FBA.'),
 f('legal_form','Gesellschaft mit beschränkter Haftung (GmbH)',['L03','W07'],'L03 p. 1'),
 f('registered_seat','Wien',['L03','W07'],'L03 p. 1, SITZ'),
 f('business_address','Schallergasse 35, 1120 Wien',['L03','L01','L02'],'L03 p. 1; ofertele ulterioare p. 1',note='Preferată pe baza FBA 2026.04.01. Parkring 2 apare în UID 2026.03.19, FBA 2026.01.08, emailul L07 și pagina W07 deschisă; acestea sunt istorice sau neconcordante, nu o nouă schimbare confirmată.'),
 f('firmenbuchnummer','FN 668224h',['L03','W07'],'L03 p. 1, antet'),
 f('firmenbuchgericht','Handelsgericht Wien',['L03'],'L03 p. 1–2'),
 f('uid','ATU83086125',['L04'],'L04 p. 1, decizie Finanzamt 2026.03.19',note='Atribuirea UID este documentată; valabilitatea fiscală live nu a fost interogată în VIES/FinanzOnline.'),
 f('commercial_representatives',[{'name':'Cosmin-Adrian Covaciu','role':'Geschäftsführer','authority':'vertrittt selbständig, potrivit FBA la 2026.04.01'},{'name':'Anastasia-Elena-Ekaterina Covaciu','role':'Geschäftsführerin','authority':'vertritt selbständig, potrivit FBA la 2026.04.01'}],['L03'],'L03 p. 1',note='Fiecare reprezintă independent din 2026.01.08 în acel extras; actualitatea înainte de semnare trebuie reconfirmată. Nu este necesară presupunerea unei reprezentări comune.'),
 f('contact_email','office@ac-wohnart.at',['L07','L05','L06'],'L07 expeditor și semnătură; R05 § 1 alin. (1)'),
 f('contact_phone','+43 665 67055045',['L07','L05','L06'],'L07 semnătură; R05 § 1 alin. (1)'),
 f('gisa',None,[],'Nu identificat','neidentificat',note='Nu se inventează un număr și nu se deduce absența oricărei obligații de autorizare din lipsa rezultatului.'),
 f('euid','ATBRA.668224-000',['L03'],'L03 p. 2'),
]
berger=[
 f('legal_name','Bmstr. Dipl.-Ing. (FH) Markus BERGER GmbH',['L01','W03','W05'],'L01 p. 1, WKO Firmenname',note='Oferta folosește Bmstr. Dipl.Ing.(FH) fără cratime/spații tipografice, aceeași identitate; identificatorul FN este mai precis decât variația grafică.'),
 f('legal_form','Gesellschaft mit beschränkter Haftung (GmbH)',['W05','L01'],'W05 Rechtsform; L01 antet'),
 f('registered_seat','Wien',['W03','W05'],'Adresa publicată și instanța Wien','publicat / sediul statutar de reconfirmat',note='WKO publică adresa de activitate; nu a fost citit un câmp SITZ dintr-un extras oficial actual. Wien este compatibil, nu certificat live.'),
 f('business_address','Schönbrunner Straße 123/2, 1050 Wien',['L01','W03','W04','W05'],'L01 p. 1; WKO Tür 2'),
 f('firmenbuchnummer','FN 316003k',['W03','W05','W04'],'WKO Firmendaten; HF Data identificare FN',note='Nu este înscris în cele patru pagini ale ofertei și a rămas câmp de completat în R05.'),
 f('firmenbuchgericht','Handelsgericht Wien',['W03','W04'],'WKO Firmengericht; FirmenABC istoric',note='R05 § 1 alin. (2) îl lasă de completat; poate fi precompletat pentru negociere cu sursa publicată și confirmare înainte de semnare.'),
 f('uid','ATU64446068',['W04'],'FirmenABC / Creditreform, UID-Nummer','publicat de sursă secundară / de confirmat',note='Nicio dovadă Finanzamt sau verificare VIES live; nu transforma în UID fiscal certificat.'),
 f('commercial_representative','Dipl.-Ing. (FH) Markus Berger',['L01','W04'],'L01 p. 4, geschäftsführender Gesellschafter; W04 Geschäftsführer alleinvertretungsberechtigt','declarat în ofertă și publicat secundar / de reconfirmat',note='Semnătura din ofertă este vizibilă. Nu a fost obținut un extras oficial actual privind puterea de semnătură.'),
 f('gewerberechtlicher_geschaeftsfuehrer','Dipl.-Ing. (FH) Markus Roman Berger',['W03'],'WKO Berechtigungen','publicat WKO / nu extras GISA live',note='Rolul din dreptul profesiei nu este prin el însuși dovada reprezentării comerciale în Firmenbuch. Diferența Roman față de oferta Markus se păstrează.'),
 f('gisa','25240122',['W03'],'WKO GISA-Zahl pentru Baumeister','publicat WKO / nu extras GISA live'),
 f('gln','9110017308233',['W03'],'WKO GLN der öffentlichen Verwaltung','publicat WKO'),
 f('trade','Baumeister; data publicată seit 2008.10.06',['W03'],'WKO Berechtigungen','publicat WKO',note='Nu certifică o licență ZT activă; oferta p. 1 menționează separat Ingenieurkonsulent für Bauingenieurwesen rB.'),
 f('contact_email','office@bmberger.at',['L01','W04'],'L01 p. 1'),
 f('contact_phone','+43 1 7864614',['L01','W04'],'L01 p. 1, Tel./Fax'),
 f('contact_mobile','+43 664 2830933',['L01'],'L01 p. 1'),
 f('website','http://www.bmberger.at',['W04'],'FirmenABC website','domeniu publicat; site inaccesibil la cercetare'),
]
pech=[
 f('legal_name','Dr. PECH Ziviltechnikergesellschaft mbH',['L02','W01','W06'],'L02 p. 1, footer și încheiere; W01 Medieninhaber',note='Dr. PECH Ziviltechniker GmbH din logo/contact este forma comercială scurtă; contractantul se identifică prin denumirea integrală și FN.'),
 f('legal_form','Gesellschaft mit beschränkter Haftung (GmbH)',['W08','W09','L02'],'W08 Rechtsform; denumire mbH din ofertă'),
 f('registered_seat','Wien',['L02','W08'],'L02 p. 1, Geschäftssitz Wien'),
 f('business_address','Johann Strauß-Gasse 32, 1040 Wien',['W01','W08','W09'],'W01 Impressum; pagini registru comercial','publicat / de reconfirmat',note='Adresa completă a biroului și pentru corespondență este Johann Strauß-Gasse 32/11, 1040 Wien în ofertă și Kontakt. Variația Johann-Strauß-Gasse cu cratimă pe site nu indică altă societate.'),
 f('correspondence_address','Johann Strauß-Gasse 32/11, 1040 Wien',['L02','W02'],'L02 p. 1, antet; W02 Kontakt'),
 f('firmenbuchnummer','FN 426034x',['L02','W06','W08'],'L02 p. 1 footer'),
 f('firmenbuchgericht','Handelsgericht Wien',['L02','W09'],'L02 p. 1 footer'),
 f('uid','ATU69226367',['L02','W01'],'L02 p. 1 footer; W01 Ust-IdNr.',note='Concordanță între original și Impressum; valabilitate fiscală live neinterogată.'),
 f('published_commercial_representatives',['Dipl.-Ing. Dr. techn. Anton Pech','Dipl.-Ing. (FH) Peter Herzina','Dipl.-Ing. Bernhard Ployer','Dipl.-Ing. Dr. techn. Michael Höflinger'],['W01','W08','W09'],'W01 Geschäftsführer; W08/W09 persoane','publicat / nu extras oficial actual'),
 f('published_representation_mode','Jeder Geschäftsführer vertritt selbständig',['W08'],'W08 Vertretungsbefugnis','publicat secundar / de confirmat oficial',note='Nu rezultă din simpla listă Impressum; nu a fost obținut extras oficial live. Semnatarul efectiv trebuie ales și confirmat înainte de semnare.'),
 f('project_contact','DI Bernhard Ployer; ployer@zt-pech.at; +43 1 5053680-33',['L02'],'L02 p. 1 Projektleitung',note='Oferta dovedește rolul de contact. Sursele publice îl listează și ca Geschäftsführer; dovada actuală de reprezentare rămâne separată.'),
 f('offer_prepared_by','Spirkoska Gabriela',['L02'],'L02 p. 1 Angebotserstellung','contact de pregătire ofertă, nu reprezentant legal dovedit'),
 f('contact_email','office@zt-pech.at',['L02','W01','W02'],'L02 p. 1; Impressum/Kontakt'),
 f('contact_phone','+43 1 5053680',['L02','W01','W02'],'L02 p. 1; Impressum/Kontakt'),
 f('secretariat_email','sekretariat@zt-pech.at',['W02'],'W02 Kontakt','publicat pe site'),
 f('gisa',None,[],'Nu identificat','neidentificat',note='Nu se atribuie număr GISA pornind de la FN; rolurile ZT se confirmă în evidențele competente și prin persoane efectiv desemnate.'),
 f('professional_statement','Befugnis für das Fachgebiet Bauingenieurwesen; Kammermitgliedschaft declarată',['L02','W01'],'L02 p. 1 footer; W01 membru/abilitare','declarat în ofertă și pe site / nu extras profesional actual',note='Nu certifică singur abilitatea actuală a fiecărei persoane pentru PI, § 128 și BWB.'),
]
data=dict(date='2026.10.13',purpose='Date de identificare pentru negociere; nu contract acceptat și nu certificat de registru live',sources=sources,companies={'AC_WOHNART':ac,'BERGER':berger,'PECH':pech},r05_comparison=[
 dict(company='AC_WOHNART',result='§ 1 alin. (1) concordă cu FBA 2026.04.01 și UID 2026.03.19; contactele sunt confirmate prin email istoric. Reconfirmarea actualității rămâne necesară.'),
 dict(company='BERGER',result='§ 1 alin. (2) lasă FN, instanța, UID și reprezentantul în Anlage 6. Acum sunt identificate date de precompletare; numai UID/reprezentarea independentă au exclusiv suport public secundar pentru actualitate.'),
 dict(company='PECH',result='§ 1 alin. (2) concordă cu oferta originală privind denumire/FN/HG/UID/adresă birou/contact. Reprezentantul efectiv este încă de confirmat; Ployer contact nu se echivalează automat cu semnatar confirmat.'),
],discrepancies=[
 'A&C: Parkring 2 din documente vechi și pagina economică deschisă nu se reintroduce ca adresă actuală în contradicție cu FBA local 2026.04.01. Rezultatul de căutare și pagina deschisă au conținut diferit.',
 'BERGER: Markus Roman Berger este nume publicat de WKO pentru rolul gewerberechtlich; Markus Berger este numele din oferta semnată și sursa comercială privind reprezentarea. Nu inventa numele integral în rubrica semnatarului fără confirmare.',
 'PECH: /11 identifică biroul în ofertă și Kontakt, în timp ce Impressum/directoarele publică nr. 32. Identitatea FN/UID concordă; precizează adresă de corespondență vs adresă publicată de registru.',
 'Nicio identificare prin domeniu nu autorizează confuzia cu altă societate sau cu persoana fizică. Oferta BERGER semnată de prestator nu este acceptare de către AG; oferta PECH și proiectele R05 nu dovedesc semnarea contractului.',
],before_[CREDENTIAL_REDACTED]
 'Extras Firmenbuch actual pentru fiecare parte: denumire, FN, sediu/adresă, instanță, persoana semnatară și modul de reprezentare; alternativ împuternicire explicită verificată.',
 'Confirmarea UID, în special BERGER ATU64446068, prin document fiscal/verificare oficială actuală dacă necesară facturării.',
 'Confirmare BERGER GISA 25240122 și persoane/abilitări pentru serviciile efective; nu deduce ZT activ din Baumeister ori rB.',
 'Confirmarea persoanelor PECH pentru rolurile PI, § 128 și BWB și a reprezentantului firmei; acreditarea profesională și dreptul de semnătură comercială sunt probe distincte.',
 'Nu s-a cumpărat extras, nu s-a creat cont, nu s-a trimis mesaj și nu s-au modificat contractele, jurnalele sau indexul.',
])
# Corecție editorială locală a notei de reprezentare, fără modificarea originalelor.
ac[7]['value'][0]['authority']='vertritt selbständig, potrivit FBA la 2026.04.01'
target=work/'2026.10.13 Date firme pentru negociere.json'
target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['2026.10.13 — Date firme pentru negociere','',data['purpose'],'','Metodă: README și inventar consultate; hashurile celor patru originale locale coincid cu indexul. Oferta BERGER p. 1/4, oferta PECH p. 1, FBA A&C p. 1/2 și UID A&C p. 1 au fost deschise vizual la rezoluție originală. Textele cache au fost reutilizate pentru fișierele neschimbate. R05 sunt numai proiecte și nu constituie dovada identității ori reprezentării.','']
for name,fields in data['companies'].items():
 lines += [name,'']
 for row in fields:
  value=json.dumps(row['value'],ensure_ascii=False) if isinstance(row['value'],(list,dict)) else (str(row['value']) if row['value'] is not None else 'NEIDENTIFICAT')
  lines.append(f"{row['field']}: {value}. Surse: {', '.join(row['sources']) or '—'}; {row['location']}. Statut: {row['status']}. {row['note']}")
 lines.append('')
lines+=['Concordanță cu R05','']+[f"{x['company']}: {x['result']}" for x in data['r05_comparison']]
lines+=['','Neconcordanțe și limite','']+data['discrepancies']+['','Confirmări înainte de semnare','']+data['before_signature']+['','Registru surse','']
for s in sources:
 lines.append(f"[{s['id']}] {s.get('path',s.get('url'))}; consultat 2026.10.13; data documentului {s.get('document_date','data publicării necertificată')}; SHA-256 {s.get('sha256') or 'neatribuit paginii web'}; {s.get('limit','Original local; paginile relevante verificate vizual.')}")
(work/'2026.10.13 Date firme pentru negociere.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'json':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'companies':len(data['companies']),'fields':sum(map(len,data['companies'].values())),'sources':len(sources)},ensure_ascii=False))
