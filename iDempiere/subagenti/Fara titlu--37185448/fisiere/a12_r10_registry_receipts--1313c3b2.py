from a12_r10_base import *
a=Path(__file__).parent/'a12_r10_receipt.py';exec(a.read_text(encoding='utf8').split("j=P10/")[0])
jj=P10/'JVM_registre'
for n,suite,pattern,etalon,neg,lim in [
 ('007','TestT201Ecrane','K-3: 9/9','9 rubrici legale RUC în antetul grilei.','Testul găsește 20 celule distincte în coloanele formate.','Fără schema BD sau textul PDF obținut din buton în această măsurare.'),
 ('008','TestT201Ecrane','K-4: 13/13','13 rubrici RC în antetul grilei.','Marcajul compară grila cu lista de rubrici.','Nu acoperă 13/13 × 3 pentru BD, grilă și PDF.'),
 ('009','TestT201Ecrane','K-5: nota','Nota «evidență internă» prezentă în titlu, bara ecranului și dialog.','Testul static urmărește titlu și funcția de notă.','Nu s-a măsurat captură de UI nativ și pdftotext RO/EN dintr-un document.'),
 ('010','TestT201Registre','K-6.*(10 rubrici|cele 10 câmpuri|10/10 rubrici|controlul pozitiv|Validare cere)','Context CONTROL și context LIBER disting cele zece rubrici D3713.','LIBER 10/10 goale; testul pozitiv conține explicit doar 3 valori completate, celelalte goale.','Emiterea de două ori din interfață, măsurarea tuturor celor 10 câmpuri completate și query K6 rămân separate.'),
 ('012','TestT201Ecrane','K-8:|TIPURI = cele 2','Cele două tipuri de registre sunt în lista de serii.','Tipurile trebuie să fie distincte.','Selecția și crearea celor trei înregistrări prin UI nu s-au executat aici.'),
 ('015','TestT201Registre','R-N3 plina|R-N2 fără plajă','99 și 100 admise; 101 refuzat pe plaja până la 100; fără plajă rezultă refuz.','Listă goală și număr peste plafon testate.','Butonul de plajă ocupată și zero rânduri persistate cer un control nativ separat.'),
 ('016','TestT201Registre','R-N11 / K-12|R-N11: plajele','01.01.2027 00:30 ora României duce la RC-2027-1.','Ceasul e citit o singură dată după blocarea plajelor.','Fără verificarea nativă a celor două plaje create din formular sau a fiecărui moment din ambele părți ale pragului.'),
 ('018','TestT201Registre','ținta conexării negăsită|ținta găsită \\(ACTIV|a doua|deja.*răspuns','Conexare acceptată pentru țintă activă existentă și refuz pentru țintă negăsită.','ID diferit ori țintă invalidă: refuzul nominal este observat.','Fără click pe «Răspund» de două ori sau dovadă fizică privind ultimul număr în acest test.'),
 ('021','TestT201Registre','retroactiv, K-17|consemnarea = ziua\\+1|data act = început|consemnarea lipsă','Validarea datelor include un control început acum 30 zile și consemnat atunci.','Viitorul, data act înainte de control și lipsa consemnării au controale specifice.','Aserțiunile de validator nu ating toate celelalte reguli, butoanele și efectele fizice.'),
 ('022','TestT201Registre','R-G1: firma 0|parametrii = \\{1: id 42|negăsit în firmă \\(0\\)|găsit exact o dată','Firma 0 refuzată, criteriile SQL includ firma și ID-ul din cererea normată.','ID5 din altă firmă sau absent nu se leagă într-un acces simulat.','Fără rularea mutantului care scoate filtrul și fără probă prin click pe firmele 11 și 1000000.'),
 ('023','TestT201Ecrane','X142: dreptul de scriere','Acces AD_Form_Access pentru clasele enumerate; scrierea cere permisiune.','False trebuie să refuze scrierea în validatorul clasei.','Inspecție/exercițiu de clasă; trei sesiuni rol nativ cu drepturile distincte nu au fost executate aici.'),
 ('025','TestT201Ecrane','K-21: SENSIBILE','Cele două ecrane sunt văzute în SENSIBILE.','Testul cere ca ambele clase să fie prezente.','Nu demonstrează și al doilea registru SENSIBILE_SPEC cerut.')]:
 hits=[]
 for tag in ['git','instalat']:hits+=lines(jj/(tag+'_'+suite+'.log'),r'^\s*OK.*('+pattern+')')[:8]
 assert hits,(n,pattern)
 add('T201-R2-'+n,'A12 – aserțiune originală · două JAR',etalon,[{'file':z['file'],'line':z['line'],'result':z['text']}for z in hits],neg,lim,hits)
# Real exact target of T216-R2-004 is old 26. Separate new 37 incl current source.
tfile=Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab/test/TestT22Factura.java');ls=tfile.read_text(encoding='utf8').splitlines();n=len([l for l in ls if 'chk('in l]);outcomes=[]
for tag in ['git','instalat']:outcomes+=lines(jj/(tag+'_TestT22Factura.log'),r'^REZULTAT:')
add('T216-R2-004','Testul actual al facturării, dublu JAR','Ținta istorică T0=26 testată în versiunea inițială; măsoară distinct versiunea de azi.',{'current_source_physical_lines_containing_chk':n,'current_source_sha256':sha(tfile),'runtime':[z['text']for z in outcomes]},'Ambele implementări sunt executate cu aceleași teste și se urmăresc cele 37 verificări, fără a reduce numitorul la vechile 26.','Două suite de componentă; încă nu reprezintă numărul de comenzi validate fără factură din cabinetul q31 și nu demonstrează încasarea unei facturi.',outcomes)
dest=P10/'Registru_componenta_A12_supliment.json';wr(dest,{'utc':now(),'fixed':BASE,'input_jars':jr(P10/'JVM_registre_corelare.json','/runs'),'receipts':out,'count':len(out)});print('more',len(out),sha(dest))
