from pathlib import Path
import re
O=Path(__file__).parent
p=O/'build_v3.py';s=p.read_text(encoding='utf-8')
def replace(a,b):
    global s
    assert a in s,a[:80]
    s=s.replace(a,b)
def block(a,b,new):
    global s
    x=s.index(a);y=s.index(b,x);s=s[:x]+new+'\n\n'+s[y:]
def insert(a,new):replace(a,new+'\n\n'+a)
def para(prefix,text):
    global s
    s,n=re.subn(r"p\('"+re.escape(prefix)+r"[^\n]*\n",lambda m:'p('+repr(text)+')\n',s)
    assert n==1,(prefix,n)

replace('Proiect CESIRO pentru design și dezvoltare React și Python','Proiect CESIRO pentru o temă React pe platforma Python existentă')
para('Proiectul livrează o experiență','Proiectul livrează o temă nouă pentru cesiro.com, cu JavaScript și React, cuplată la platforma Python și la API-urile existente din U:/cesiro.com. Nu construiește un sistem API nou, un backend comercial paralel sau o bază de produse separată. Catalogul, administrarea, comenzile, plățile și integrările rămân cele ale platformei actuale. Documentația descrie lucrări viitoare; nu execută modificări pe site.')
para('Calendar recomandat:','Domeniu de bază: tema, organizarea și prezentarea datelor, integrarea cu funcțiile existente și configurator 2D care folosește aceleași operații de coș. Plan: 16 săptămâni, 160–200 zile-persoană, apoi 90 zile de măsurare. Ideile care cer capabilități backend indisponibile sunt separate ca extensii necontractate; nu obligă proiectul temei să creeze un API nou.')
replace('minimum 20 de serii eligibile la finalul valului 3','minimum 20 de serii eligibile la finalul etapei T3')
replace('Pilot de 10 produse personalizabile, previzualizare și fișă de producție; țintă de 5% din comenzile eligibile la 90 de zile după activare.','Concept pentru 10 produse personalizabile; activare numai dacă platforma și fabrica susțin deja fluxul verificat. În caz contrar, cerere de ofertă prin fluxul existent, fără modul API nou.')
insert("page('1 Date disponibile",r"""h('Regula de integrare și limitele temei')
p('Datele sunt preluate prin contractul paginilor și API-urile actuale. Se documentează câmpurile și comportamentul existente; nu se reproiectează API-ul pentru a se potrivi machetei. Un câmp absent este ascuns, marcat neconfirmat sau acoperit prin conținut editorial aprobat, fără inventare. O funcție nesusținută primește alternativă existentă ori rămâne în foaia de parcurs. Specificațiile din §8 pentru extensii descriu potențialul de marketing, nu un angajament de construire a unui nou sistem.')
""")
replace('citirea statică a unor fișiere din U:/cesiro1-site','citirea statică a unor fișiere din U:/cesiro1-site și verificarea ulterioară a bazei indicate U:/cesiro.com')
insert("h('Inventarul contractual",r"""p('În U:/cesiro.com există mecanismul de teme: registry, manifest.json, files.json și page_contracts.json, cu logică comercială comună. Fișierele README, requirements, package.json, factory.py, cms.py și docker-compose.yml comparate sunt identice cu cele din U:/cesiro1-site. Aceasta nu dovedește identitatea tuturor datelor sau a imaginii Docker active. Repository-ul cesiroproduction/site-uri este indicat de beneficiar; accesul disponibil returnează 404, deci commitul și corespondența cu producția rămân de verificat. [I6]')
""")
replace('responsabilul de date livrează D01 direct din PostgreSQL EVA prin interogări SQL versionate, exclusiv de citire, pe o replică sau un instantaneu consistent, cu cont dedicat și limită de timp.','responsabilul platformei livrează D01 din sursa operațională existentă, folosind exportul actual sau interogări SQL de citire versionate pe un instantaneu consistent. Nu se creează un API de export nou.')
replace('Fiecare înregistrare și fiecare câmp sursă primește o destinație:','Maparea documentară a temei atribuie fiecărei înregistrări și fiecărui câmp sursă o destinație:')
insert("p('Fiecare",'') if "p('Fiecare" in s else None
replace('Extindere cerută','Destinație și necesar de verificat')
insert("h('Dicționare pe familii')",r"""p('Câmpurile de mai sus reprezintă dicționarul țintă de prezentare. D01 le mapează la datele deja disponibile și la câmpurile editoriale existente. Crearea de tabele, servicii sau endpointuri nu este parte a temei; lipsurile de platformă se listează separat, cu fallback și impact de lansare.')
""")
replace('90 zile după valul 4','90 zile după lansarea temei')
replace('90 zile după valul 3b','90 zile după activarea funcției existente')
replace('Se compară trei direcții creative','Se compară trei direcții creative')
insert("page('8.1",r"""p('Inventarul de 25 tipuri și 75 ecrane este domeniul de design. Implementarea include numai paginile și funcțiile susținute de contractele actuale. Schițele pentru personalizare, Club, liste și AI nu creează implicit obligația de a le dezvolta în backend; D03 le marchează explicit ca disponibile, condiționate sau viitoare.')
""")
replace('Valul 1 livrează recomandări prin reguli și primele scene 2D; valul 3a adaugă configuratorul și recomandări bazate pe coșuri agregate.','Tema livrează scene 2D și un configurator de selecție; acesta folosește produsele și operațiile de coș existente. Recomandările statistice sunt condiționate de un serviciu deja disponibil, fără creare de motor nou.')
replace('Probă de acceptare la valul 3b','Probă pentru extensia activată')
insert("h('Asistent de cumpărare",r"""p('Domeniu condiționat: asistentul, căutarea vizuală și semantică se conectează numai la servicii existente demonstrate în D01. În lipsa lor, tema livrează căutarea text și filtrele actuale; pragurile de mai jos devin specificații pentru o etapă separată, fără API nou în contractul temei.')
""")
replace('Costul operațional AI are plafon de 600 EUR/lună, inclus în §17','Pentru o extensie AI aprobată separat, costul operațional are plafon propus de 600 EUR/lună, exclus din bugetul temei din §17')
insert("h('Personalizare și producție')",r"""p('Personalizarea, listele, punctele Club și precomenzile sunt capabilități condiționate. Se proiectează vizual, dar se activează în tema de bază numai dacă există deja suport complet și verificat în platformă. Dacă nu există, se oferă cerere de ofertă/contact, favorite sau notificare prin funcțiile actuale. Nu se creează registre, motoare sau API-uri noi pentru a bifa aceste idei.')
""")
replace('backendul Python generează SVG sau PDF','serviciul Python existent trebuie să poată genera SVG sau PDF; dacă nu poate, generarea aparține unei extensii separate, în afara temei. Fișierul de producție este')
replace('Valul 4 include un pilot manual controlat cu 3 loturi','Foaia de parcurs include un pilot manual controlat cu 3 loturi')
replace('Portal Pro minimal în scenariul recomandat','Prezentarea Pro peste capabilitățile existente')
insert("h('Club CESIRO și comunicări')",r"""p('În tema de bază se redesenează exclusiv funcțiile de retenție și Pro deja disponibile. Conectarea la servicii externe noi, registrul de puncte, prețurile contractuale noi sau API ANAF nou nu sunt incluse. Se păstrează cererea de ofertă și prețul public când platforma nu poate susține încă un flux specializat.')
""")
insert("page('8.4",r"""p('D01 stabilește ce este disponibil în Pro: o capacitate prezentă poate fi expusă în interfață; o capacitate lipsă rămâne în registrul de extensii. Colectarea datelor firmei prin formularul actual este fallbackul pentru completarea automată după CUI.')
""")
insert("page('9 Arhitectura",r"""p('Autoservirea folosește rutele și stările actuale. Regula de lansare pentru lipsuri legale: responsabilul platformei remediază separat capabilitatea lipsă sau domeniul afectat nu se lansează. Tema nu maschează lipsa retragerii funcționale printr-un buton fără efect și nu creează un API paralel.')
""")
block("page('9 Arhitectura", "page('10 Frontend",r"""page('9 Arhitectura temei pe platforma existentă')
p('Decizie de proiect: tema se înregistrează în mecanismul EVA Storefront din U:/cesiro.com. Flask randează paginile publice folosind contractele și datele actuale, iar componentele React în JavaScript îmbunătățesc căutarea, filtrele, selecția de produse și compoziția 2D. Vite poate produce fișierele statice în procesul de build. Node nu este necesar ca serviciu de producție pentru această soluție.')
table(['Element','Tratament în proiect'],[
('Backend Python și PostgreSQL','Se păstrează autoritatea și regulile existente pentru catalog, preț, stoc, comandă și cont. Niciun backend comercial sau model concurent de date.'),
('API existent','Se consumă rutele actuale pe același origin, cu aceeași autentificare, CSRF și semantica erorilor. Nu se creează un sistem API, BFF, gateway sau proxy comercial nou.'),
('Registrul de teme','Manifest, fișiere, contracte de pagini, chei de traducere și preview în structura existentă. Logica de coș, checkout, preț și stoc rămâne comună, în afara temei.'),
('Frontend React','Componente interactive și prezentare. HTML public indexabil vine din Flask; datele inițiale sunt serializate sigur conform contractului existent. Valorile comerciale nu sunt autoritative în browser.'),
('Admin și integrări','Panoul React/Vite actual, marketplace-urile, curierii și plățile sunt reutilizate. Redesignul public nu înlocuiește administrarea.'),
('Docker existent','Buildul temei produce asseturi incluse în imaginea actuală a aplicației. În viitoarea implementare se actualizează doar artefactele necesare; volumele, baza, secretele și serviciile comerciale sunt păstrate.')],[4,13.5])
p('Next.js separat a fost comparat cu Flask și componente React: ar adăuga runtime și invalidare între straturi. Pentru cerința de temă integrată se alege varianta Flask + React. Next.js, API nou și motor nou de căutare nu sunt condiții de livrare. TypeScript rămâne opțional ca verificare statică peste JavaScript.')
h('ADR și demonstrații în primele două săptămâni')
p('ADR01 fixează tema înregistrată și contractele actuale. ADR02 inventariază căutarea existentă și filtrele; motoare noi sunt doar opțiuni ulterioare. ADR03 documentează cacheul actual și consistența datelor. ADR04 verifică topologia Docker, backupurile și monitorizarea, fără migrare de găzduire implicită. Orice extindere a platformei se delimitează separat de contractul temei.')

page('9.1 Baza locală Docker și continuitatea')
p('Baza de integrare indicată de beneficiar este U:/cesiro.com. Citirea docker-compose.yml arată proiectul cesiro1 și serviciile db cu postgres:16, backend, admin, tunnel și migrate. Citirea fișierelor nu dovedește ce containere sau imagini sunt active pe server. Nu au fost pornite, oprite sau recreate containere și nu au fost citite secrete. [I6]')
p('Înainte de implementare, D01 trebuie să lege explicit domeniul cesiro.com de proiectul Compose, tenant, imagine/digest și versiunea sursei. Repository de referință indicat: github.com/cesiroproduction/site-uri. Conexiunea GitHub a returnat 404; nu se presupune că repository-ul este public, inexistent sau sincronizat cu U:. Commitul de referință se confirmă de echipa platformei.')
table(['Control','Cerință pentru lansarea temei'],[
('Izolare','Preview și staging cu date anonimizate, fără scrieri spre marketplace sau servicii reale. Se utilizează mecanismul existent de preview; acesta nu trebuie să schimbe prețul efectiv al coșului.'),
('Revenire','Comutare la tema anterioară în ≤15 minute, fără restaurarea bazei peste comenzile noi. Se verifică păstrarea sesiunilor, coșului și URL-urilor.'),
('Continuitate','Obiectiv de platformă: 99,9% lunar, RPO≤15 minute și RTO≤60 minute. ADR04 cere probe ale infrastructurii existente; tema nu poate garanta aceste valori prin CSS/React.'),
('Deficit de infrastructură','Dacă testul arată o limită, se oferă separat opțiuni: resurse izolate, PostgreSQL standby/PITR, copie de backup în cont separat și monitorizare externă. Nu se presupune că tema cumpără ori migrează găzduirea.'),
('Alternativă contractuală','Păstrarea unei infrastructuri cu obiectiv inferior, de exemplu99,5%, cere acceptarea documentată a riscului de către beneficiar înaintea lansării; nu este declarată echivalentă cu99,9%.')],[4.1,13.4])
p('Un plan de îmbunătățire a găzduirii, dacă devine necesar, se cotează separat cu două oferte și acoperire de permanență. Auditorul a semnalat un server local partajat; această afirmație rămâne de verificat în operarea reală. Tema nu introduce un server Node sau un al doilea backend ca răspuns implicit.')

page('9.2 Cache și consistență fără API nou')
p('Tema folosește citirea și invalidarea existente. Catalogul public poate fi cache-uit conform contractului platformei; coșul, contul, checkoutul și prețurile private nu intră în cache public. Prețul/stocul afișat și cel verificat la comandă provin din aceeași autoritate. Clientul reconfirmă orice modificare de total, iar rezerva de stoc este cea existentă.')
table(['Demonstrație','Criteriu'],[
('Actualizare produs și stoc','Se urmărește traseul real al unei schimbări în mediu izolat până în pagina temei și coș; obiectiv p95≤5s, p99≤30s dacă platforma îl susține. Nu se declară un webhook nou ca prerechizită implicită.'),
('Date expirate','Pentru oferte dinamice: maximum60s de informație expirată, apoi revalidare sau afișare indisponibilă. Checkoutul validează întotdeauna la sursă, cu mecanismul existent.'),
('Teste de regresie','Ultima unitate, preț schimbat, stoc zero, sesiune expirată și acces Pro: zero comenzi confirmate pe date invalide, fără duplicarea logicii în React.'),
('Capabilitate lipsă','Se deschide deficit de platformă, nu un sistem nou în temă. Remedierea poate folosi mecanismul comun de evenimente/outbox dacă există; orice schimbare la acesta este proiect separat, cu aprobare și estimare.')],[4.2,13.3])
p('Directiva de audit Flask → Next.js este tratată prin eliminarea stratului Next.js separat din soluția aleasă. Nu există un cache Next.js nou de invalidat. Dacă în viitor se aprobă o arhitectură decuplată, devin relevante outboxul tranzacțional, versiunile, retryul, semnarea și purjarea separată CDN din analiza tehnică; acestea nu sunt lucrări comandate prin proiectul temei.')
""")
s=s.replace('SSR/ISR','randare Flask')
s=s.replace('Next.js App Router și React','Flask și componente React')
replace('Conținut prerandat/cache la CDN','HTML randat de Flask/cache la CDN')
block("h('Contractul API')", "page('12 Checkout",r"""h('Maparea la contractele existente')
p('Livrabilul este o matrice de integrare a temei cu API-ul actual, nu specificarea unui API nou. Se consemnează ruta, metoda, scopul, câmpurile, autentificarea, CSRF, erorile și efectele. Documentația OpenAPI existentă se reutilizează dacă există; o documentare suplimentară descrie comportamentul actual, fără redenumiri și fără versiune nouă cerută de temă.')
table(['Funcție','Dovadă statică și limită'],[
('Catalog și filtre','factory.py declară GET /api/catalog/products, cu tenant, limbă, categorie, q, pagină, sortare și filtre de preț/material/culoare/capacitate. Se confirmă contractul răspunsului în D01.'),
('Validarea comenzii','POST /api/orders/validate este descris în cod ca validare fără comandă, cont sau e-mail. În implementare, înainte de test se inspectează tot lanțul și se respectă REGULI.md.'),
('Comandă și cont','Rutele actuale /api/orders și /api/account sunt reutilizate prin UI și fluxurile existente. În această analiză nu au fost apelate rute tranzacționale.'),
('Teme','cms.theme_registry și active_theme, plus manifest/files/page_contracts. Tema nu preia funcțiile comerciale comune în propriul director.'),
('Plăți','Se demonstrează Stripe existent și walleturile eligibile înainte de alt PSP. Lipsa walletului nu autorizează o integrare fiscală sau de plăți nouă în temă.')],[4.1,13.4])
p('Întrucât lucrările sunt de prezentare și integrare, nu se planifică migrații de schemă sau sincronizări paralele de catalog. Dacă o funcție presupune asemenea schimbări, ea este separată ca extensie și nu se ascunde în costul temei. Registrul deficitelor indică fallbackul, responsabilul platformei și efectul asupra recepției.')
""")
replace('Se definesc stările de plată inițiată','Se documentează și se reutilizează stările existente corespunzătoare plății inițiate')
replace('Conector fiscal dedicat în valul 2','Integrarea fiscală existentă și deficitul separat')
para('Adaptorul Python se conectează','Tema folosește rezultatul facturării și documentele generate de platforma existentă. Nu implementează un API ANAF, OAuth2 sau un adaptor fiscal nou. Dacă D01 nu demonstrează transmiterea fiscală aplicabilă, responsabilul platformei primește un deficit separat, blocant pentru domeniul afectat. Cerințele tehnice de mai jos descriu acea eventuală remediere, în afara bugetului temei. [T7]')
s=s.replace('pentru integrarea directă','pentru o eventuală integrare directă')
insert("page('13 Performanță",r"""p('Aceeași regulă se aplică retragerii: tema expune funcția existentă numai dacă aceasta îndeplinește fluxul legal. Dacă ruta actuală nu îl susține, lipsa este escaladată ca remediere a platformei; nu se lansează un buton nefuncțional și nu se construiește un API paralel sub denumirea de temă.')
""")
replace('condiționate de topologia și probele ADR04 din §9.1.','obiective ale platformei care trebuie probate în ADR04, separat de livrarea temei din §9.1.')
block("page('16 Activități", "page('17.2 Devizul",r"""page('16 Activități calendar și lansări graduale')
p('Planul de16 săptămâni acoperă o temă integrată cu backendul și API-ul existente. Calendarul de26 săptămâni pentru întregul program de funcții noi nu este aplicat acestui domeniu. Capacitățile indisponibile sunt scoase din implementarea de bază, cu păstrarea conceptelor de design și a condițiilor de activare.')
table(['Etapă','Activități și livrabile','Ieșire'],[
('T0 S1–2','D01 actual, contracte de pagini/rute, D02, inventar media, ADR01–04 și registrul funcțiilor disponibile.','Sursă și Docker identificate; nicio presupunere de API nou.'),
('T1 S1–4','Trei concepte, teste UX, navigare după utilizări, design system și prototipuri.','Direcție aprobată;25 tipuri de design marcate după suportul platformei.'),
('T2 S3–10','Temă înregistrată, asseturi React, home/listare/produs, filtre, traduceri,300 prioritare și10 ghiduri.','Integrare pe contracte existente, R01/R02/R06 pe lot.'),
('T3 S7–12','UI pentru coș/checkout/cont, scene și configurator2D, Pro în limitele actuale, testare de regresie.','20 serii,12 scene; zero logică de preț/stoc duplicată; funcțiile condiționate au fallback.'),
('T4 S11–14','Accesibilitate, performanță, securitate UI, conținut final,30 ghiduri și20 SKU-uri de test pe familii.','R03–R09; deficitele legale și operaționale rezolvate de proprietarii platformei sau domeniu blocat.'),
('T5 S15–16','Preview, pilot și comutare graduală a temei, instruire și predare.','Rollback≤15minute; monitorizare și criterii comerciale.'),
('T6 după lansare','90 zile de măsurare și optimizare, distinct de construcția temei.','R10 cu baseline și limite statistice.')],[2.6,9.3,5.6],small=9.8)
p('Drumul critic este D01 → design validat → integrare pe contracte actuale → regresie checkout → lansare. Media și documentele sunt fluxuri paralele; sub debitul editorial minim se reduce lotul eligibil sau se prelungește calendarul. Nu se rezolvă prin inventarea datelor. Sprinturi de două săptămâni și decizie PO în trei zile lucrătoare.')
p('Trafic5% →20% →50% →100%, minimum48h și volum suficient. Eroarea de total, plată, stoc sau acces oprește creșterea. Limita inferioară a intervalului pentru conversie trebuie să depășească−5% relativ; dacă traficul nu ajunge, se poate aproba doar extindere limitată și documentată. Se schimbă tema, fără pierderea comenzilor și fără restaurare destructivă a bazei.')

page('17 Efortul temei și capacitatea echipei')
p('Deviz de jos în sus,8 ore/zi-persoană, pentru reutilizarea platformei. Coloana Integrare Python înseamnă citirea contractelor, configurarea/înregistrarea temei și ambalarea asseturilor; nu dezvoltare de sistem API, ERP, căutare ori contabilitate. Interval160–200 zile include maximum25% incertitudine după baza detaliată.')
wbs=[('N01 Inventar și contracte existente',3,2,3,2),('N02 UX și concepte',12,0,0,4),('N03 Componente React',6,14,0,4),('N04 Home listare produs',4,18,2,6),('N05 CMS navigare și colecții',2,6,2,2),('N06 UI coș și checkout actual',2,8,2,6),('N07 Cont și suport existent',1,5,1,3),('N08 Configurator2D și scene',2,8,0,4),('N09 Limbi SEO și măsurare',1,3,2,4),('N10 Integrare Docker și verificări',0,2,4,6),('N11 Coordonare și predare',2,0,0,2)]
assert sum(sum(x[1:]) for x in wbs)==160
totals=[sum(x[i] for x in wbs) for i in range(1,5)]
table(['Activitate','UX','React','Integrare Python','QA','Total'],[(*x,sum(x[1:])) for x in wbs]+[('TOTAL',*totals,160)],[8,1.2,1.5,2.7,1.2,2.9],small=9.5)
p('La80 zile lucrătoare nominale, media este2–2,5 echivalenți normă întreagă, vârf3–4. PO CESIRO minimum2 zile/săptămână și doi editori×50 zile sunt contribuții interne distincte; timpul lor se evaluează la costul intern real. Fotografii și traducătorii nu sunt presupuşi incluși în acești editori.')
p('Conceptele avansate rămân în §8 cu probe de acceptare, însă sunt activate numai dacă D01 confirmă suportul actual. AI nou, căutare vectorială nouă, registru Club, liste de eveniment fără suport, motor de personalizare, conector fiscal și migrarea găzduirii nu sunt ascunse în cele160–200 zile.')

page('17.1 Bugetul temei și costurile separate')
p('Sume de planificare fără TVA, nu cotații. Se cer două oferte pe același domeniu. Tarife ipotetice: echipă locală cu EVA250–400 EUR/zi; furnizor complet400–550 EUR/zi. Reutilizarea este premisa contractuală, nu un API nou inclus în preț.')
table(['Variantă','Componente de cost','Total cu rezervă15%'],[
('Temă cu echipă locală/EVA','160–200 zile×250–400 =40.000–80.000; media19.460–35.100; cost tehnic incremental6 luni900–2.400; mentenanță temă6 luni4.500–9.000.','74.589–145.475 EUR'),
('Același domeniu cu furnizor complet','160–200 zile×400–550 =64.000–110.000; aceleași media, operare incrementală și mentenanță.','102.189–179.975 EUR'),
('Funcții/backend/infrastructură suplimentare','Se estimează separat numai după D01 și o decizie distinctă. Prețul presupune reutilizarea API-urilor; nu promite servicii backend inexistente.','Neincluse în bugetul temei')],[4.1,9.1,4.3])
p('Total = (efort×tarif + media + cost tehnic incremental + mentenanță)×1,15. Costul incremental150–400 EUR/lună acoperă alocația de staging/CDN/monitorizare pentru temă, dacă este necesară. Găzduirea actuală rămâne cost existent; eventuala modernizare HA/PITR se cotează separat, fără economii sau disponibilitate pretinse.')
p('Mentenanță temă750–1.500 EUR/lună pentru6 luni; încă6 luni adaugă5.400–11.400 EUR împreună cu operarea incrementală, înainte de rezervă. Nu include permanență de infrastructură24/7, consum AI nou, comisioane, publicitate, transport, spargeri sau costul intern CESIRO. Bugetul AI de600 EUR din §8 este doar plafon pentru o extensie aprobată ulterior.')
p('Scenariul media din §17.2 poate fi redus prin studio în fabrică, înlocuind liniile externe. Catalogul complet este contabilizat; cele300 produse sunt prioritare editorial. Oferta finală precizează ce active există și ce trebuie produse, fără dublarea timpului furnizorului și a editorilor beneficiarului.')
""")
para('Clauză contractuală propusă:','Clauză contractuală propusă:90 zile garanție pentru defectele temei față de specificația acceptată, inclusă în dezvoltare. Extinderea la180 zile se cere în ofertă. Mentenanța temei750–1.500 EUR/lună este distinctă de operarea backendului, de permanența infrastructurii și de dezvoltarea unor capabilități noi.')
replace('24/7: răspuns ≤1 h','În programul contractat: răspuns ≤1 h')
replace('Furnizorul confirmă în ofertă permanența 24/7; fără acoperire nominală și cost nu se declară SLA contractat.','Permanența24/7 pentru platformă este serviciu separat; fără contract activ nu se declară inclusă în mentenanța temei.')
replace('Pragurile din §8.1–8.4, 20 serii, 12 scene, 10 produse personalizabile și fișiere vectoriale verificate; AR este în afara recepției recomandate.','20 serii și12 scene pentru tema de bază. Pragurile AI/personalizare/Club din §8 se recepționează numai dacă există suport actual și funcția este inclusă explicit; altfel rămân extensii.')
replace('25 tipuri, 75 ecrane de bază, stări, tokenuri și bibliotecă; SUS ≥80 în runda finală.','Design pentru25 tipuri și75 ecrane; implementare numai pentru cele susținute de platformă. Stări/tokenuri și SUS≥80 în runda finală.')
replace('Rollback ≤15 min; restaurare RPO/RTO; două persoane instruite și monitorizare.','Rollback temă≤15 min; probe RPO/RTO ale platformei existente, două persoane instruite și monitorizare. Deficitele infrastructurii sunt separate.')
insert("page('19 Eșantionul",r"""p('R00 suplimentar: zero sisteme API, backenduri comerciale, baze de catalog sau mecanisme de autentificare paralele introduse de temă. D01 mapează fiecare ecran implementat la ruta/contractul existent. O extensie nesusținută nu este declarată livrată și nu este pornită doar pentru a satisface inventarul de design.')
""")
insert("links1=[",r"""p('I6 — U:/cesiro.com/README.md, backend/themes/README.md, backend/app/cms.py, backend/app/factory.py, frontend/package.json și docker-compose.yml: citire statică din21 octombrie2026. Registry și contracte de teme confirmate în cod;6 fișiere cheie identice cu copia cesiro1-site. GitHub indicat de beneficiar: https://github.com/cesiroproduction/site-uri ; accesul disponibil a returnat404. Versiunea activă Docker și commitul nu sunt certificate prin această citire.')
""")
replace('D03 design și conținut\',\'UX și editorial S1–6','D03 design și conținut\',\'UX și editorial S1–4')
replace('ADR01–04\',\'Tehnic și DevOps S2/S4','ADR01–04\',\'Tehnic și DevOps S2')
para('V1 a stabilit direcția','V1 a stabilit direcția inițială; V2 a integrat inventarul local și reutilizarea EVA. V3 tratează auditul Claude V2 și auditul tehnic, cu precizarea finală a beneficiarului: temă nouă peste backendul și API-urile existente, fără sistem API nou. Direcția de bază este Flask cu componente React în mecanismul actual de teme; funcțiile avansate nesusținute rămân extensii separate.')
para('Versiunile anterioare și auditurile','Versiunile anterioare și auditurile rămân nemodificate. Nu s-au modificat site-ul, Dockerul, repository-ul, backendul, catalogul sau integrările. Doar documentele și planșele de proiect au fost create. D01 curent, D02 comercial și probele funcționale rămân activități ale implementării ulterioare.')
# Spacing of newly introduced prose, without touching API names or URLs.
for a,b in {'de16':'de 16','de26':'de 26','după D01':'după D01',';25':' ; 25','traduceri,300':'traduceri, 300','și10 ghiduri':'și 10 ghiduri','configurator2D':'configurator 2D','20 serii,12':'20 serii, 12','final,30':'final, 30','și20 SKU':'și 20 SKU','Rollback≤15minute':'Rollback ≤15 minute','Trafic5%':'Trafic 5%','→20%':'→ 20%','→50%':'→ 50%','→100%':'→ 100%','minimum48h':'minimum 48 h','depășească−5%':'depășească −5%','sus,8 ore':'sus, 8 ore','Interval160':'Interval 160','maximum25%':'maximum 25%','La80':'La 80','este2–2,5':'este 2–2,5','vârf3–4':'vârf 3–4','minimum2':'minimum 2','editori×50':'editori ×50','cele160':'cele 160','EVA250':'EVA 250','complet400':'complet 400','rezervă15%':'rezervă 15%','zile×':'zile ×','media19.460':'media 19.460','incremental6':'incremental 6','luni900':'luni 900','temă6':'temă 6','luni4.500':'luni 4.500','incremental150':'incremental 150','temă750':'temă 750','pentru6':'pentru 6','încă6':'încă 6','adaugă5.400':'adaugă 5.400','infrastructură24/7':'infrastructură 24/7','de600':'de 600','cele300':'cele 300','propusă:90':'propusă: 90','la180':'la 180','Permanența24/7':'Permanența 24/7','și12 scene':'și 12 scene','pentru25':'pentru 25','și75':'și 75','SUS≥80':'SUS ≥80','temă≤15':'temă ≤15','din21':'din 21','octombrie2026':'octombrie 2026','cod;6':'cod; 6','returnat404':'returnat 404','exemplu99,5%':'exemplu 99,5%','cu99,9%':'cu 99,9%','maximum60s':'maximum 60 s'}.items():s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
print('Domeniul temei aliniat la backend și API existente')
