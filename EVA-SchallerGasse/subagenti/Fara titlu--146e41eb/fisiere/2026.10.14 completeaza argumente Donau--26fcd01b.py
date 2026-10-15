from pathlib import Path
import re
d=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
p1=d/'2026.10.14 01 Incetarea politei Donau.txt';p2=d/'2026.10.14 02 Neplata si acoperirea Donau.txt'
t=p1.read_text(encoding='utf8')
a=t.index('Retragerea inițială conform');b=t.index('\n\nO contestare pentru eroare',a)
t=t[:a]+'''Retragerea inițială conform § 5c este distinctă de denunțarea ordinară și poate privi și un profesionist, cu excepțiile legale pentru riscurile mari; nu orice GmbH reprezintă un asemenea risc. Regula este un termen de 14 zile, care presupune încheierea contractului și primirea informării/documentelor cerute: poliță, condiții, reguli de primă și informarea privind retragerea. Totuși, alin.5 stabilește și stingerea cel târziu la o lună după primirea poliței împreună cu informarea corectă. Lipsa condițiilor generale singură nu depășește acest plafon dacă polița și informarea valabilă au fost primite. O informare grav defectuoasă, echivalată legal cu lipsa informării, poate lăsa dreptul deschis. [L1 § 5c alin.1–6]

Polița istorică include informarea la p.9. Pentru un eventual contract nou din prima parte a anului 2026 se aplică regimul de atunci, identic în aceste puncte cu alin.1–6 actuale. § 191c alin.25 limitează aplicarea noului § 5c alin.7 la contracte încheiate după 2026.09.30; această modificare privind contractele de consum la distanță nu creează o nouă ieșire în octombrie pentru A&C. Transferul conform § 69 nu redeschide termenul. [P2 p.9; L1 §§ 5c,191c]

Calea concretă rămasă este probatorie: dacă operațiunea Ersatzvertrag a constituit într-adevăr un contract nou, se verifică la titularul originar primirea poliței și informarea corectă. Pe baza prezenței informării în PDF nu se dovedește singură primirea, dar nici nu se poate afirma că dreptul este încă deschis. Sunt necesare cererea, acceptarea și dovada comunicării; o simplă schimbare de titular în iunie nu ajunge.''' + t[b:]
p1.write_text(t,encoding='utf8')
t=p2.read_text(encoding='utf8')
needle='Hotărârea este veche, astfel că o folosim'
t=t.replace(needle,'''Extras din motivarea OGH: „Ist auf Grund einer zugekommenen qualifizierten Mahnung gemäß §39 Abs.2 VersVG. Leistungsfreiheit eingetreten, ändert sich hiedurch am Bestand des Versicherungsverhältnisses selbst, also an der Vertragsdauer und der Prämienzahlungspflicht, nichts.” Traducere: exonerarea intervenită în baza unei somații calificate primite nu schimbă existența raportului, durata sau obligația de plată a primei. Condiția unei somații valabile este chiar în premisa principiului. [J1 p.2]

''' + needle)
needle='Situațiile care pot reduce ori exclude o parte din pretenție sunt distincte:'
t=t.replace(needle,'''Poate asigurătorul să ceară o sumă care nu i se cuvine? O poate pretinde, dar pentru a o obține în justiție trebuie să dovedească temeiul și cuantumul. Emailul și decontul nu țin locul unui titlu judiciar. Încasarea unei sume nedatorate poate genera obligația de restituire, dacă sunt îndeplinite condițiile legale. Nu calificăm întreaga cerere drept nedatorată numai pentru că asigurătorul a invocat lipsa protecției.

Excepția de neexecutare. § 1052 ABGB permite în anumite condiții refuzul propriei prestații până la contraprestația datorată. În asigurare trebuie aplicat și regimul special § 39 VersVG: dacă legea permite exonerarea ca urmare a neplății culpabile după somație valabilă, aceasta nu este pur și simplu o neexecutare ilicită a DONAU care ar șterge prima. Dacă DONAU refuză fără temei acoperirea datorată, pot exista remedii pentru neexecutare, despăgubire și, în caz grav, încetare extraordinară; întinderea și caracterul exigibil trebuie analizate concret. O afirmație generală de neacoperire nu justifică automat reținerea tuturor ratelor. [L1; L4; J1]

Restituirea și îmbogățirea fără cauză. Contractul activ și § 1 alin.2 constituie în principiu cauza primei, chiar în cazul exonerării valide. Dacă suma a fost plătită fără datorie, de exemplu după o încetare valabilă ori în dublu, § 1431 ABGB și regulile restituirii pot deveni relevante. Plata sub rezervă poate conserva contestarea și eventuala cerere de restituire; nu face singură suma nedatorată și nu garantează rambursarea. Se verifică și § 1432, cunoașterea situației și conținutul rezervei. [L4]

''' + needle)
needle='În Kostenaufstellung,'
table='''Situația pe perioade pentru decizia de plată. Datele sunt intervale ale primei; starea juridică a acoperirii se stabilește separat pe ramuri. Prima de trimestru este pentru întregul pachet. [P1, P3, P4]

| Perioada | Pretenția cunoscută | Ce poate fi datorat și ce se verifică |
| 2026.01.01–2026.04.01 | Nu este adăugată ca restanță în cererea de 5.326,15 EUR | Se cere contul pentru prima inițială și plățile fostului titular. Nu se presupune neplata numai din lipsa extrasului nostru. |
| 2026.04.01–2026.07.01 | 1.591,81 EUR, inclusă în cele două rate restante | Prima poate fi datorată prin contract și transfer. Se verifică plata, repartizarea vânzător/cumpărător și somația. Lipsa unei somații valabile afectează exonerarea, nu șterge automat rata. |
| 2026.07.01–2026.10.01 | 1.591,81 EUR | Se verifică documentele portalului, orice încetare și cererea de reducere. Nu este dovedită o reducere acceptată de la începutul trimestrului. |
| 2026.10.01–2027.01.01 | 1.591,81 EUR, deja inclusă | Contractul este tratat ca activ. Se verifică data unei eventuale încetări/reduceri și creditul proporțional; nu se dublează rata. |
| După o încetare valabilă | Nicio încetare confirmată în prezent | Primele obișnuite viitoare se opresc/recalculează potrivit § 40 ori normei speciale. Data propusă unilateral nu este suficientă. |
| Accesorii până la decontul cunoscut | 550,72 EUR | Se verifică 30 EUR creditor, 501,58 EUR recuperare și 19,14 EUR dobândă. Nu reprezintă integral primă și nu condiționează singure acoperirea. |

'''
t=t.replace(needle,table+needle)
t=t.replace('L3. UGB', 'L4. ABGB §§ 1052,1431,1432, texte consolidate: https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001622\nL3. UGB')
p2.write_text(t,encoding='utf8')
for path in [p1,p2]:
    t=path.read_text(encoding='utf8')
    # Repair numeric punctuation without changing URLs, quotations, identifiers.
    t=re.sub(r'(\d), (\d{2})(?=\s*(?:EUR|%|\b))',r'\1,\2',t)
    repl={'și91':'și 91','și3.':'și 3.','cadrului2900010498':'cadrului 2900010498','privește1.591':'privește 1.591','și20':'și 20','39și40':'39 și 40','38și':'38 și','vara2026':'vara 2026','trimestriale3.183':'trimestriale 3.183','următoare1.591':'următoare 1.591','prime4.775':'prime 4.775','adaugă30':'adaugă 30','”3.213':'” 3.213','include3.183':'include 3.183','și30':'și 30','sunt417':'sunt 417','justificareaTVA':'justificarea TVA','de4%':'de 4%','de8%':'de 8%','retroactive.4.775':'retroactive. 4.775','în2036devin':'în 2036 devin','durată1000K':'durată 1000K','suma5.326':'suma 5.326','1416ABGB':'1416 ABGB','36VersVG':'36 VersVG','L1§':'L1 §','net+':'net + ','TVA=':'TVA = ','=501':'= 501','clauza1000K':'clauza 1000K','p.2,4,10,12':'p.2, 4, 10, 12','EmailGruber':'Email Gruber','1pagină':'1 pagină','89pagini':'89 pagini','și condițiile89':'și condițiile 89','9pagini':'9 pagini','și condițiile complete':'și condițiile complete','AHVBart.':'AHVB art.','103/97s, plata':'103/97s, plata','în2026':'în 2026','contractului2026':'contractului 2026','11.2.4prevede':'11.2.4 prevede'}
    for a,b in repl.items():t=t.replace(a,b)
    # Fix authored numeric references and ordinary conjunctions.
    t=re.sub(r'(?<=\d)și(?=\d)', ' și ', t)
    t=re.sub(r'(?<=\d)EUR', ' EUR',t)
    t=t.replace('EUR TVA =501','EUR TVA = 501').replace('net +83','net + 83')
    path.write_text(t,encoding='utf8')
    print(path.name,len(t.split()))
