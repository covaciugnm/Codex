from pathlib import Path
import re, json
from docx import Document

O=Path(__file__).parent
s=(O/'build_v2.py').read_text(encoding='utf-8')
def rep(a,b):
    global s
    assert a in s, a[:100]
    s=s.replace(a,b)
def before(anchor,content):rep(anchor,content+'\n\n'+anchor)
def block(start,end,new):
    global s
    a=s.index(start); b=s.index(end,a); s=s[:a]+new+'\n\n'+s[b:]

rep("'Proiect V2'","'Proiect V3'")
rep('Versiunea 2 revizuită după auditurile Claude și Gemini','Versiunea 3 specificație de proiect și criterii de recepție')
rep('Revizie documentară pe baza auditurilor Claude și Gemini','Specificație de proiect pentru design și dezvoltare')
rep("h('0 Direcția propusă')","head('0 Direcția propusă')")
block("h('Ce se schimbă față de versiunea 1')","h('Trei motive concrete", r"""h('Domeniu și rezultat')
p('Proiectul livrează o experiență React în JavaScript, integrată cu motorul comercial Python EVA Storefront. Include proiectarea vizuală, organizarea întregului catalog disponibil, fluxurile comerciale, zona Pro, producția de conținut și recepția pe dovezi. Această documentație descrie lucrările viitoare; nu autorizează și nu execută modificări pe site.')
p('Direcție de comunicare de testat: „Ceramică din Sighișoara, aleasă pentru masa ta”. Mesajul de origine se folosește numai pentru produsele CESIRO cu proveniență documentată; colecțiile mixte identifică producătorul fiecărei piese.')
""")
rep('promisiunea privind spargerea este legată de o politică și un proces aprobate.','promisiunea publică de înlocuire gratuită a produselor sosite sparte este păstrată și operaționalizată în §8.4, fără restrângerea drepturilor existente.')
rep('Calendar recomandat: 18 săptămâni de la îndeplinirea condițiilor de pornire, apoi 90 de zile de măsurare. Nota finală aparține auditorilor; acest document definește probele necesare, nu declară anticipat obținerea notei 10.','Calendar recomandat: 26 săptămâni de la pornire, cu puncte de decizie în săptămânile 2 și 4, apoi 90 zile de măsurare. Efort de bază 360 zile-persoană, interval de planificare 360–450. Configuratorul 2D este inclus; AR se finanțează separat după validare. Bugetul complet și capacitatea echipei sunt în §17.')
rep('Revizia folosește cele două audituri primite, constatările publice CESIRO','Inventarul folosește constatările publice CESIRO')
rep('responsabilul de date livrează un export curent pe tenant:','responsabilul de date livrează D01 direct din PostgreSQL EVA prin interogări SQL versionate, exclusiv de citire, pe o replică sau un instantaneu consistent, cu cont dedicat și limită de timp. Exportul acoperă fiecare tenant:')
before("page('2 Modelul", r"""h('Reconciliere și origine')
p('Diferența numerică de 57 dintre sitemap și CSV nu dovedește 57 produse noi. D01 compară mulțimi după ID canonic, SKU și slug: numai în bază, numai în CSV, numai în sitemap, redenumiri, retrageri și duplicate. Fiecare diferență primește cauză; 100% sunt explicate înaintea migrării. Nu se accesează clienți nominali pentru această analiză.')
p('Producător real este câmp obligatoriu distinct de brand și vânzător. Insigna și filtrul „Fabricat de CESIRO” cer document de proveniență și validare umană. Produsele terțe rămân eligibile în vitrină cu producătorul corect; materialul, originea și fabrica nu se deduc din textul comercial sau din prefixul SKU.')
""")
before("page('3 Calitate", r"""h('Dicționar pentru chimice și biocide')
p('Date obligatorii când sunt aplicabile: clasificare și versiune CLP, pictograme, cuvânt de avertizare, fraze H/P și EUH, cantitate netă, furnizor, UFI când este cerut, fișă cu date de securitate cu limbă și revizie, autorizație/aviz biocid și țări de valabilitate, utilizări permise, mesaj de publicitate art. 72 și link către ingredientele detergentului. Pentru fiecare câmp există stare aplicabil/neaplicabil și justificare aprobată; nu se cer automat aceleași acte tuturor produselor de curățenie.')
p('Preț unitar: prețul final al ambalajului / cantitate netă normalizată × unitate de referință. Se afișează lei/l, lei/kg sau lei/bucată unde este relevant, pe card, fișă și coș; la un pachet mixt nu se inventează o unitate înșelătoare. Exemple de test, nu oferte: 50 lei pentru 5 l = 10 lei/l; 25 lei pentru 50 bucăți = 0,50 lei/bucată. Regula legală și excepțiile se stabilesc pe piață; afișarea utilă suplimentară este cerință de produs. [L12]')
""")
rep('toate informațiile/documentele obligatorii pentru familia și piața respectivă.','toate informațiile/documentele obligatorii pentru familia și piața respectivă, inclusiv CLP, biocide, ingrediente și preț unitar, după aplicabilitate.')
before("page('4 Obiective", r"""h('Capacitatea editorială și măsurarea preciziei')
p('În săptămânile 1–2 se cronometrează 100 fișe din familii diferite. Ipoteza de planificare este 60 fișe simple/zi/editor, maximum 7 minute/fișă plus control și administrare; cazurile juridice sau tehnice dificile se separă. La 5.222 fișe sunt 87 zile-editor; doi editori alocați 50 zile furnizează 100 zile și o rezervă de 13 zile. Dacă D01 indică 6.000 fișe, rezerva dispare. Sub 52 fișe/zi/editor, se adaugă capacitate sau se reduce lotul publicabil.')
p('Această capacitate CESIRO verifică datele structurale și documentele o singură dată per produs, nu rescrie 31.332 texte. Cele 300 fișe prioritare sunt revizuite în șase limbi prin devizul extern; restul folosesc traducere asistată, validări numerice și eșantion de 5% pe limbă/familie. O eroare critică sau precizie sub prag trimite lotul complet la revizie. Lipsa dovezilor obligatorii blochează vânzarea, indiferent de capacitatea editorială.')
p('Etalonul de 200 produse raportează separat culoare, stil și rol, precum și fiecare limbă: precizie ≥95% pe fiecare celulă evaluabilă, minimum 30 exemple relevante/celulă, cu completarea etalonului când lipsesc exemple. Se raportează acoperirea, abținerile și intervalul de încredere; media globală nu poate compensa un atribut slab. Numerele și datele critice publicate sunt verificate integral.')
""")
before("page('5 Navigare", r"""h('Valoarea funcțiilor noi și a canalului Pro')
table(['Indicator','Țintă și populație'],[
('Asistent și configurator','Ținte la 90 zile: +10% conversie pentru disponibilitatea asistentului și +10% AOV pentru disponibilitatea configuratorului, măsurate A/B pe utilizatori eligibili. Comparația utilizatorilor care aleg singuri asistentul cu ceilalți este doar descriptivă, afectată de selecție.'),
('Pro','50 conturi verificate și 20 clienți cu prima comandă plătită în 90 zile; recumpărare ≥25% la 90 zile de la prima comandă; venit Pro net +15% față de perioada comparabilă D02. Dacă baza este zero, financiarul fixează ținta absolută înainte de pilot, fără procent artificial.'),
('QR și canal direct','Pilot 1.000 inserții eligibile: ≥5% scanări unice și ≥2% prime comenzi directe în 90 zile. Se raportează separat comenzi atribuite codului și migrare confirmată; un scan nu dovedește că persoana era client marketplace.')],[4.1,13.4])
""")
before("page('6 Experiența", r"""h('Serii din SKU și colecții active')
p('Segmente precum G242, D144, 604M și 010L sunt candidați pentru decor. Fabrica validează dicționarul și excepțiile pe 100 SKU-uri înaintea oricărei regulii automate. Importul produce propuneri de relații serie–piesă–culoare, cu sursă și versiune; nu unește automat produse terțe sau coduri ambigue. Recepție: 20 serii aprobate, zero asocieri de decor greșite în lotul publicat.')
p('La fiecare eveniment de stoc și prin reconciliere la 5 minute, colecțiile promovate sunt reevaluate. Sub 8 produse eligibile, editorul primește alertă; sistemul afișează alternative marcate sau retrage intrarea din campanie în maximum 5 minute. Pagina și URL-ul rămân accesibile cu mesaj sincer, fără schimbarea tacită a produselor cumpărate.')
""")
rep('24 tipuri','25 tipuri');rep('72 ecrane','75 ecrane');rep('cele 24 de tipuri','cele 25 de tipuri')
rep("('Profesional 23–24','23 portal Pro și comandă rapidă; 24 ofertă/mostre/logo. Compararea a până la 4 produse este un modul transversal.')", "('Profesional 23–24','23 portal Pro și comandă rapidă; 24 ofertă/mostre/logo. Compararea a până la 4 produse este un modul transversal.'),('După cumpărare 25','25 Comenzile mele cu status, factură, re-comandă, solicitări de modificare, spargere și retragere; acces și pentru clientul fără cont.')")
rep('Alegerea rezultă din două runde cu câte 8 participanți și criterii documentate.','Planșele conceptuale și wireframe-urile mobile sunt incluse în §21. Alegerea rezultă din două runde cu câte 8 participanți și criterii documentate; schițele nu reprezintă fotografii ale catalogului sau interfețe implementate.')
rep('30 clipuri scurte, 12 scene cumpărabile și pilot de 10 modele 3D corecte la scară. Extindere după validarea costului și efectului.','30 clipuri scurte, 12 scene cumpărabile și 100 decupaje pentru configurator 2D; 3D/AR este extensie separată, după validarea calității și costului.')
block("h('Exemple de ton", "page('8 Funcții comerciale", r"""h('Adresarea pe limbă')
table(['Limbă','Decizie inițială pentru B2C și Pro'],[('RO','B2C tu; Pro dumneavoastră.'),('EN','You, cu formulare directă; registru profesional în Pro.'),('DE','Sie în ambele zone; „Wählen Sie die passenden Stücke für Ihren Tisch.”'),('HU','Ön în ambele zone, validare de către vorbitor nativ.'),('BG','Вие, registru politicos; consecvență între interfață și suport.'),('EL','Plural politicos εσείς; verificare nativă a formulărilor.')],[2,15.5])
p('Ghidul de ton se validează în interviurile A1 și prin editorii nativi. O schimbare de adresare se aplică întregii limbi, inclusiv e-mailurilor. Devizul pe foto, video, scene, traducere și varianta de studio intern este în §17.2.')
""")
rep("page('8 Funcții comerciale", "page('8.1 Funcții comerciale")
rep("page('8 Funcții vizuale", "page('8.2 Funcții vizuale")
rep("page('8 Retenție", "page('8.3 Retenție")
rep('Valul 1 livrează recomandări prin reguli și scene 2D; valul 3 adaugă configuratorul','Valul 1 livrează recomandări prin reguli și primele scene 2D; valul 3a adaugă configuratorul')
rep('Probă de acceptare la valul 3','Probă de acceptare la valul 3b')
before("page('8.2", r"""p('Costul operațional AI are plafon de 600 EUR/lună, inclus în §17: țintă ≤0,06 EUR/sesiune asistată și cel mult 10.000 sesiuni bugetate. Costul include inferență, embeddings și procesarea foto; costul muncii de moderare se raportează separat. Alertă la 80%, oprire a cererilor AI plătite la 100%, fără oprirea căutării clasice sau a suportului. PoC verifică atingerea costului și a calității; plafonul nu promite volum garantat.')
p('Extensia după cumpărare adaugă 100 cereri etalon, 30 de izolare/atac, peste cele 200 de cumpărare: ≥90% răspunsuri corecte și utile, zero divulgări între clienți, zero schimbări comerciale executate de AI. Statusul se citește numai după autentificare sau identificare sigură; reclamația se transferă într-un formular confirmat de client și apoi la operator.')
""")
block("p('Pilotul WebAR", "h('Personalizare și producție')", r"""p('Scenariul recomandat livrează un configurator 2D cu fotografii reale aprobate, decupaje coerente și 12 fundaluri de masă. Glazura nu este recreată dintr-un model generic. AR rămâne opțiune separată: 10 modele GLB/USDZ, dimensiuni verificate, evaluare vizuală pe 5 dispozitive și test comercial înaintea extinderii. Creșterea AOV este ipoteză de testat, nu efect deja demonstrat pentru CESIRO.')
p('Modul accesibil oferă aceeași selecție ca lista de piese, butoane adaugă/elimină, cantități editabile, ordine de focus stabilă și anunțuri ARIA pentru totaluri și erori. Nicio operație nu depinde exclusiv de drag and drop, vedere sau culoare.')
""")
before("h('Liste de nuntă", r"""p('Contractul de producție este vectorial: backendul Python generează SVG sau PDF, în milimetri, la scară 1:1, cu fonturi licențiate convertite în contururi, profil de culoare, zonă imprimabilă și toleranțe stabilite de fabrică. SVG-urile încărcate sunt sanitizate fără scripturi sau resurse externe; imaginile raster sunt acceptate numai dacă tehnologia fabricii le permite la rezoluția cerută. Fișierul final, previzualizarea și comanda au același identificator și hash; operatorul aprobă un proof fizic pe fiecare dintre cele 10 produse. Cele 20 simulări includ diacritice, logo invalid, limite de text și respingere de preflight.')
p('Pentru bunurile realizate efectiv după specificațiile clientului, checkoutul cere o bifă separată, nebifată implicit: „Am înțeles excepția de la dreptul de retragere pentru acest produs personalizat; drepturile legale pentru neconformitate rămân aplicabile.” Configurarea unui set din produse standard nu activează automat excepția. Bifa atestă informarea, nu creează o renunțare la drepturi. [L10]')
""")
before("page('8.3", r"""p('Sursa inițială de capacitate este un registru de loturi administrat și semnat de planificatorul fabricii, importat zilnic, cu lot, SKU, capacitate alocată, termen, tampon și versiune. Dacă există ERP verificat în D01, adaptorul înlocuiește registrul fără schimbarea contractului. Date mai vechi de 24 ore suspendă precomenzile noi. Valul 4 include un pilot manual controlat cu 3 loturi; integrarea ERP completă este extensie distinctă.')
""")
before("page('9 Arhitectura", r"""h('QR pe ambalaj și facturare Pro')
p('Pilot pe 20 serii: QR persistent către pagina seriei, cu limbă selectabilă, îngrijire și completare set. Codul identifică seria și campania, nu persoana; înscrierea în Club este opțională. Inserțiile în colete marketplace se folosesc numai după verificarea condițiilor canalului. Nu se importă contacte marketplace în CRM fără temei; indicatorii sunt cei din §4.')
p('Pro completează denumirea și adresa firmei după CUI prin serviciul ANAF sau un furnizor aprobat, cu confirmare de către client și completare manuală la indisponibilitate. Prețul cu/fără TVA este etichetat explicit; publicul B2C vede totalul cu TVA. Se păstrează cantitatea și prețul unitar. Datele de facturare se reconfirmă înainte de emitere pentru a reduce corecțiile, fără promisiunea imposibilă de zero stornări.')

page('8.4 Autoservire după cumpărare')
p('Pagina Comenzile mele este accesibilă din cont sau prin link securizat, cu expirare și verificare suplimentară pentru operațiuni sensibile. Clientul fără cont are același acces la drepturi. Se afișează comanda, data estimată, statusul curierului cu ora ultimei actualizări, factura și istoricul cererilor; indisponibilitatea curierului nu este ascunsă sub un status inventat.')
table(['Flux','Activitate și criteriu'],[
('Produs sosit spart','Selectare piesă și cantitate, fotografie opțională sau canal alternativ, confirmare. Mediană ≤60 s pentru completarea cererii, nu pentru aprobarea înlocuirii. Notificare imediată, țintă de răspuns uman ≤1 zi lucrătoare; înlocuire gratuită potrivit promisiunii publice. Lipsa fotografiei nu stinge drepturile.'),
('Retragere','Intrare publică permanent vizibilă în perioada relevantă, plus link în cont și e-mail. Identificare minimă, selecție contract/produse, confirmare explicită și dovadă pe suport durabil cu dată/oră; nu cere cont sau motiv. Detalii în §12.1.'),
('Adresă și factură','Clientul trimite cererea; operatorul verifică etapa expedierii și confirmă schimbarea. Descărcarea facturii verifică proprietarul; linkul nu expune alte documente. Corecțiile fiscale rămân la financiar.'),
('Re-comandă','Piesele din istoric se propun în coș nou; prețul și stocul sunt actuale și confirmate. Produsele lipsă au alternative etichetate, fără substituire automată.'),
('Asistent','Citește numai comanda autorizată și politicile aprobate, explică pașii și pregătește recomandări. Nu anulează, nu aprobă retururi, nu rambursează și nu modifică marketplace-uri.')],[3.4,14.1])
p('Politica de înlocuire a produselor sosite sparte este deja publicată în FAQ și este păstrată în proiect. Responsabilul logistic definește stocul de înlocuire, costul și escaladarea; orice schimbare ulterioară a condițiilor cere analiză juridică și nu reduce retroactiv drepturile. Solicitările înregistrate nu sunt supuse aprobării AI. [S5]')
""")
rep('Meilisearch candidat principal; pgvector pentru similitudine','Un singur motor derivat ales prin ADR02')
rep('Index derivat, fațete, diacritice și sinonime; alegere finală prin PoC, PostgreSQL rămâne sursa.','Meilisearch hibrid sau PostgreSQL FTS/trigram + pgvector; text, fațete și imagini testate în PoC. Fără două motoare secundare implicit.')
block("h('Decizii care se închid", "page('10 Frontend", r"""h('Decizii de arhitectură')
table(['ADR și termen','Opțiuni și criteriul de alegere'],[
('ADR01 săptămâna 2','A: Next.js separat, randare React unitară, runtime Node și cache suplimentar. B: teme Flask cu insule React, operare mai simplă și reutilizare mai mare, cu risc de duplicare UI/stare între pagini. Ambele satisfac JavaScript/React și Python. Se probează produs, listare și coș cu același buget de performanță; devizul presupune A. Dacă B trece SEO, accesibilitate și testele, iar TCO pe 24 luni este ≥15% mai mic, PO poate alege B prin deviz revizuit. Nu se presupune economia înaintea probei.'),
('ADR02 săptămâna 4','Un singur motor de căutare pentru text, fațete și similitudine: Meilisearch hibrid versus FTS/trigram/pgvector în PostgreSQL. Relevanță §8.1, șase limbi, SKU exact, indexare și cost lunar măsurate pe același set. Dacă o opțiune nu acoperă imaginile, funcția vizuală rămâne dezactivată; al doilea motor cere justificare și buget separat.'),
('ADR03 săptămâna 2','Contract de cache și tranzacții din §9.2 și §10, inclusiv model de versiune, invalidare CDN și protecția datelor Pro.'),
('ADR04 săptămâna 2','Topologia producției, furnizor, regiune UE, capacitate, cost și plan de restaurare din §9.1. PoC de sarcină și failover înainte de lansare.')],[3.1,14.4],small=9.8)
p('Motorul EVA are o ramură principală și versiuni etichetate; particularitățile CESIRO sunt configurare sau extensii per tenant, fără copii divergente de schemă. API compatibil N și N−1 pentru cel puțin un ciclu de lansare, migrații expand/contract și verificări pe două configurații de tenant în CI. Distribuirea în alte magazine rămâne operațiune separată autorizată, nu efect automat al proiectului CESIRO.')

page('9.1 Găzduirea și continuitatea producției')
p('Topologie propusă pentru ținta 99,9%: regiune UE, resurse de producție izolate, două instanțe aplicație în domenii de defect distincte după balansator; PostgreSQL administrat cu standby și PITR; worker separat, coadă durabilă și stocare obiecte replicată. CDN/WAF este în față; baza nu este publică. Stagingul are date anonimizate și secrete diferite. Administratorii folosesc MFA și acces privat.')
p('Afirmația despre serverul local partajat și tunel provine din audit, nu dintr-o inspecție a infrastructurii active. D01 inventariază topologia reală. Un singur server sau tunel local nu poate fi acceptat drept dovadă pentru acest SLO. Alternativa locală rămâne doar variantă reestimată, cu țintă 99,5%, infrastructură și riscuri acceptate distinct înainte de contract.')
table(['Control','Specificație și recepție'],[
('Disponibilitate','SLO 99,9% lunar pentru navigare și API de checkout CESIRO, incluzând mentenanța planificată; 43,2 minute buget într-o lună de 30 zile. Monitorizare externă la 1 minut din două regiuni; PSP și curier raportate separat, inclusiv efectul asupra parcursului clientului.'),
('Backup','Arhivare WAL cu alertă la întârziere >5 minute, RPO ≤15 minute; backup zilnic, 35 zile PITR și copie zilnică în cont separat cu retenție 90 zile. Restaurare lunară pe mediu izolat, criptare și control acces.'),
('Revenire','Failover la pierderea unei instanțe și restaurare la pierderea bazei demonstrate; RTO ≤60 minute la volumul real. Runbook, cronometrare, integritatea comenzilor și exercițiu condus de al doilea operator.'),
('Cost și operare','Plafon estimativ infrastructură/licențe 700–1.300 EUR/lună, plus AI până la 600 EUR/lună. Acestea sunt alocații de planificare, nu cotații. ADR04 cere două oferte cu topologia, backupurile, traficul și suportul incluse.')],[3.2,14.3])
p('Rollbackul de interfață în ≤15 minute este diferit de restaurarea bazei. La incident se păstrează comenzile noi; nu se restaurează orbește o copie veche peste tranzacțiile încasate. Reconcilierea cu PSP, controlul facturilor și reluarea outboxului fac parte din runbook.')

page('9.2 Evenimente cache și consistența catalogului')
p('În aceeași tranzacție PostgreSQL cu modificarea produsului, stocului, prețului sau eligibilității se scrie un eveniment outbox: ID unic, tenant, entitate, versiune monotonă, tip, dată și piețe afectate. Nu se face apel de rețea din tranzacția SQL. Toate căile de scriere, inclusiv importurile și operațiile bulk, trebuie să emită evenimentul; reconcilierea periodică detectează omisiunile.')
p('După commit, workerul livrează cel puțin o dată către index și invalidator, cu confirmare separată per consumator. Se folosesc autentificare mTLS sau HMAC, timestamp, protecție replay și allowlist de tenant/tag; endpointul nu acceptă URL-uri arbitrare. Retrimiterile și evenimentele reordonate sunt idempotente; versiunea veche nu suprascrie versiunea nouă. Retry cu backoff, coadă de erori și reluare controlată.')
p('Dacă ADR01 alege Next.js, handlerul invalidează tagurile tenant/produs/limbă/piață și paginile afectate, apoi purjează separat CDN-ul. Pentru preț și stoc nu se presupune că revalidateTag cu profil max elimină imediat conținutul vechi: se folosește expirare imediată compatibilă cu versiunea fixată, de exemplu expire 0, și se verifică următoarea citire. Revalidarea Node nu purjează automat orice CDN extern. În varianta Flask, același contract invalidează cacheul HTML și CDN. [T6]')
table(['Probă','Prag contractual'],[
('Latență normală','Commit → index și afișare proaspătă: p95 ≤5 secunde, p99 ≤30 secunde; alertă când cel mai vechi eveniment nelivrat depășește 30 secunde.'),
('Degradare','La întârziere >60 secunde se suspendă ofertele dinamice afectate sau se citesc direct din API; TTL maxim 60 secunde pentru fragmente de preț/stoc, fără stale nelimitat. Dacă sursa nu răspunde, cumpărarea afectată este oprită explicit.'),
('Siguranță tranzacțională','Backendul reverifică prețul, eligibilitatea și stocul la adăugare și confirmare; rezervare atomică. O pagină cache nu poate autoriza vânzarea ultimei unități.'),
('Fault injection','Worker oprit, evenimente duplicate/reordonate, preț modificat și ultimul stoc: zero comenzi confirmate cu preț/stoc invalid; după revenire, toate versiunile converg și coada este reconciliată.')],[3.7,13.8])
""")
before("page('11 Analiza", r"""h('Buget de performanță pe rută')
table(['Rută','JS inițial comprimat','Alte limite pe mobil'],[('Homepage și produs','≤170 KB transferat','Imagine LCP ≤120 KB; ≤35 cereri inițiale.'),('Listare și căutare','≤200 KB','LCP ≤120 KB; ≤40 cereri inițiale.'),('Checkout','≤220 KB cod propriu','≤35 cereri proprii; SDK PSP separat măsurat și încărcat la pasul necesar.'),('Configurator','≤170 KB înainte de activare','Pachet 2D suplimentar ≤250 KB; activele se încarcă la cerere, fără blocarea produsului.')],[4.1,4.1,9.3])
p('CI măsoară un build de producție cu cache gol, la 390 px și rețea mobilă simulată. Fonturile, CMP și analytics autorizat intră în bugetul propriu. Depășirea blochează buildul; o excepție are ADR, proprietar și termen și nu suspendă pragurile CWV. Pachetele AI, 2D și AR nu sunt în încărcarea inițială a paginii de produs.')
""")
rep('Contracte versionate, reguli, autorizare, tranzacții și integrări existente.','Contracte versionate, reguli, autorizare, tranzacții și integrări existente.')
before("page('12 Checkout", r"""p('În D01 se demonstrează integrarea Stripe existentă înaintea contractării altui PSP: eligibilitate Apple Pay/Google Pay pe domeniu, țară, monedă și dispozitiv, 3DS, webhookuri și comisioane. Se păstrează PSP-ul actual dacă îndeplinește cerințele; prezența stripe_gateway.py nu este probă de activare a walleturilor.')
""")
before("page('13 Performanță", r"""page('12.1 Retragere online și integrare fiscală')
p('Funcția de retragere prevăzută de art. 11a introdus prin Directiva 2023/2673 este cerință de lansare, cu data europeană de aplicare 19 iunie 2026. Registrul juridic va atașa transpunerea națională și excepțiile pe piață. Linkul din e-mail completează funcția vizibilă din interfață; nu o înlocuiește. Fluxul acceptă declarația clientului fără aprobare prealabilă, transmite fără întârziere confirmarea pe suport durabil, cu conținut și dată/oră, și păstrează dovada. [L10]')
p('Notificarea de retragere este distinctă de anularea operațională, aprobarea returului și rambursare. Clientul declanșează declarația prin aplicația deterministă; AI nu efectuează aceste operațiuni. Se permit identificarea fără cont, produse din comenzi mixte și recuperarea după eroare. În caz de dispută privind excepția pentru personalizare, cererea poate fi înregistrată pentru analiză umană. Nu se cere fotografie sau motiv pentru retragere.')
p('Recepție: 12 scenarii, inclusiv client fără cont, limbă diferită, retragere parțială, dublu click, expirare link, indisponibilitate e-mail și bun personalizat. Dovada se oferă imediat în interfață; e-mailul se reîncearcă și se alertează. Testele cu efecte sensibile sunt conduse de operator uman în mediul autorizat; AI nu execută anulări sau rambursări nici în simulări.')
h('Conector fiscal dedicat în valul 2')
p('Adaptorul Python se conectează la serviciul fiscal deja autorizat dacă există sau direct la API ANAF, după demonstrație. Pentru integrarea directă: aplicație înregistrată, OAuth2 asociat certificatului autorizat, tokenuri criptate și rotație; XML UBL/RO_CIUS validat față de schemele actuale, trimitere, ID încărcare, interogare status și arhivarea răspunsului. Un HTTP 200 nu înseamnă validare fiscală. [T7]')
p('Contabilul fixează termenul legal și regulile de emitere în registrul versionat. Alarmă la 50% din termen, la 24 ore înainte și imediat la respingere; retry pentru erori tranzitorii, intervenție pentru erori de date. Nu se transmit duplicate după timeout fără verificarea stării. Recepție pe 12 cazuri: B2C/B2B, monedă, TVA, duplicate, expirare token, respingere, indisponibilitate și corecție fiscală realizată uman. Documentele alimentare sunt gestionate separat în §13.2.')
""")
rep("page('13 Conformitate", "page('13.1 Conformitate")
rep('Disponibilitate țintă 99,9% lunar; RPO ≤15 min, RTO ≤60 min.','Disponibilitate țintă 99,9% lunar; RPO ≤15 min, RTO ≤60 min, condiționate de topologia și probele ADR04 din §9.1.')
block("p('Entitatea contractuală trebuie confirmată", "page('14 SEO", r"""p('Vânzătorul public identificat la 21 octombrie 2026 este CESIRO MARKET S.R.L., cod fiscal RO45050769, Alba Iulia. Producătorul ceramicii proprii este atribuit CESIRO S.A. din Sighișoara numai cu documentație per produs; produsele terțe au producătorul real. Contractele, factura și rolurile GDPR se reconciliază cu documentele societăților în A0. Identitatea vânzătorului nu dovedește originea tuturor articolelor. [S6]')

page('13.2 Conformitatea familiilor și documentelor')
table(['Domeniu și responsabil','Cerință de lansare și probă'],[
('Chimice CLP\nJuridic și date','Pericolele relevante sunt vizibile înainte de cumpărare, în limba pieței, cu date din fișa furnizorului. Dicționarul §2 și blocarea §3 sunt testate pe toate produsele chimice publicate. Calendarul revizuirii CLP este separat: unele cerințe de publicitate/vânzare la distanță sunt amânate la 1 ianuarie 2028 prin Reg. 2025/2439; proiectul pregătește datele de acum, fără a numi toate cerințele noi deja obligatorii. [L11]'),
('Biocide\nJuridic și achiziții','Clasificare și drept de comercializare pe țară, autorizare, utilizări, avertismente și mesaj art. 72 în publicitate; respingerea afirmațiilor înșelătoare de siguranță. Fără autorizație necesară sau informații aprobate, produsul nu este cumpărabil. [L13]'),
('Detergenți\nAchiziții și calitate','Link către lista publică de ingrediente și documentele aplicabile, revizie și limbă. Excepțiile pentru produse exclusiv profesionale se documentează. Reg. 648/2004 rămâne reperul tranzitoriu; noul Reg. 2026/405 are aplicare generală din 23 septembrie 2029. [L14]'),
('Preț pe unitate\nComercial și juridic','Cantitate netă, unitate de referință și reguli de afișare; exemple și excepții conform HG 947/2000 și normelor pieței. B2C cu TVA; Pro poate vedea separat baza fără TVA. Recepție pe 20 cazuri, inclusiv pachete mixte și reduceri. [L12]'),
('Retragere și SAL\nJuridic și suport','Funcție §12.1, date vânzător și SAL ANPC în subsol și mesaje relevante. Linkurile sunt verificate; nu se reactivează vechea platformă europeană SOL/ODR închisă. Nu se declară orice icon sau e-mail o obligație universală fără temei. [L10, L15]'),
('Contact alimentar\nCalitate fabrică','Asociere produs–material–lot–document, declarații și rapoarte reale. Document public aprobat accesibil din fișă; acte interne complete cu acces pe rol și jurnal. Original cu hash și revizie, scanare malware, previzualizare accesibilă. Publicarea unui PDF integral de lot pentru orice produs nu este presupusă obligație universală. [L2]')],[4.1,13.4],small=9.8)
p('R09 verifică 100% din lotul care urmează să fie cumpărabil, cu matrice aplicabil/neaplicabil justificată, emitent, valabilitate, limbă și responsabil. Documentele expirate sau revocate suspendă oferta afectată și declanșează revizuirea incidentului. Registrele de conformitate au termen de revalidare înaintea fiecărui val; informația generată de AI nu este document de conformitate.')
""")
before("page('15 Măsurare", r"""h('Conținut distinct și schema de limbă')
p('Site-ul direct publică ghiduri de utilizare, serii și scene originale; marketplace-urile primesc descrieri concise, păstrând aceleași informații esențiale de siguranță, cantitate și material. Conținutul diferit este o alegere editorială, nu garanție de clasare sau singura măsură SEO.')
p('Schema inițială hreflang: ro, de, hu, bg, el și en generic; x-default către selectorul neutru de piață. Fiecare pagină are canonical propriu și legături reciproce numai către echivalente existente. Dacă apar oferte EN distincte pe URL-uri de țară, se adaugă en-GB/en-IE sau alte coduri reale, fără a duplica artificial variante en-XX. Țara selectată nu schimbă arbitrar canonicalul.')
""")
before("page('16 Activități", r"""p('D02 calculează durata realistă pentru MDE 10% relativ la conversia actuală, α=5%, putere 80%, alocare 50/50 și trafic eligibil după consimțământ. Exemplu de dimensionare, nu baseline CESIRO: de la 2,0% la 2,2% necesită aproximativ 80.600 utilizatori/grup pentru un test bilateral simplu; la 10.000 eligibili/săptămână în total ar dura circa 16 săptămâni. Durata se recalculează pentru unitatea reală de randomizare și sezonalitate; 2 teste/lună nu este un angajament fără trafic suficient.')
""")
block("page('16 Activități", "page('17 Guvernanță", r"""page('16 Activități calendar și lansări graduale')
p('Calendarul recomandat are 26 săptămâni nominale; sărbătorile, disponibilitatea fabricii și timpii de avizare se transformă în date calendaristice la pornire. Valurile se suprapun numai în limita capacității nominalizate. Fiecare val are domeniu recepționabil și activare separată; interfața existentă rămâne disponibilă până la trecerea verificărilor.')
table(['Etapă','Activități și livrabile','Dependențe și ieșire'],[
('A0/A1\nS1–4','D01/D02, cercetare, trei direcții, inventar media, ADR01/03/04 până la S2; PoC căutare și AI, ADR02 până la S4.','Conturi de citire, proprietari și materiale; deviz și topologie validate la S4.'),
('Val 1\nS3–10','Design S1–6, dezvoltare S3–10; home, listare, produs, căutare text, 300 prioritare, primele scene și 10 ghiduri.','Design și model date aprobate pe loturi; R01/R02/R03/R06; nicio publicare neeligibilă.'),
('Val 2\nS9–14','Checkout, Stripe/wallet eligibil, livrare, fiscal, autoservire și retragere, CMP, măsurare.','Contractele PSP/fiscal și politicile validate; R04/R07/R08/R09.'),
('Val 3a\nS13–18','Căutare semantică, 20 serii, configurator 2D, 12 scene, QR, Pro minimal și 20 ghiduri cumulat.','ADR02, imagini, dicționar SKU și documentele Pro; etaloane și izolare preț.'),
('Val 3b\nS17–22','Asistent înainte/după cumpărare, căutare vizuală, UGC și monitorizare cost.','Etaloane, politici și identitate sigură; R05 și fallback independent de AI.'),
('Val 4\nS21–26','Personalizare 10 produse, liste de bază, Club, card cadou, 3 loturi manuale dacă fabrica validează, 30 ghiduri și restul catalogului eligibil.','Proofuri de fabrică, financiar și juridic; fiecare funcție are flag distinct.'),
('A5\n90 zile după','Măsurare la 90 zile de la activarea fiecărei funcții/cohorte, optimizare și predare.','R10; întreținere și garanție conform §17.3.')],[2.8,8.5,6.2],small=9.8)
p('Drum critic: D01 și topologie → model de produs → design validat → checkout/fiscal → test integral și activare. În paralel, drepturile și documentele, media, traducerile și capacitatea fabricii pot deveni blocante. Lipsa lor reduce lotul eligibil sau mută data funcției; nu se acoperă cu valori inventate. Demo la două săptămâni, decizie PO în trei zile lucrătoare.')
p('Trepte 5% → 20% → 50% → 100%, minimum 48 ore și volum suficient per treaptă. Eroarea critică de total, plată, stoc sau acces oprește creșterea. Limita inferioară a intervalului pentru variația conversiei trebuie să depășească −5% relativ; fără putere statistică se poate aproba doar o extindere limitată și documentată, nu declara non-inferioritate. Piața pilot este aleasă din D02. Rollback de interfață demonstrat în ≤15 minute, fără pierderea comenzilor.')

page('17 Efortul pe funcții și capacitatea echipei')
p('Estimare de jos în sus pentru scenariul recomandat, 8 ore/zi-persoană. Coloana BE include explicit ingineria datelor și DevOps; QA pe funcție este distinct de probele transversale. Zilele de mai jos sunt un deviz de planificare, nu durate calendaristice și nu oferte ferme. Intervalul total 360–450 reprezintă baza plus maximum 25% incertitudine de volum/integrare, fără dublarea acelorași lucrări.')
wbs=[
('F01 Discovery și contracte',4,0,8,2),('F02 Sistem design și componente',14,6,0,4),('F03 Home listare produs cont',8,22,8,6),('F04 PIM și flux catalog complet',2,4,12,4),('F05 Căutare unificată',2,4,8,4),('F06 Checkout livrare fiscal',3,10,14,7),('F07 Autoservire și retragere',2,6,6,4),('F08 Configurator serii QR',4,10,8,4),('F09 Asistent și căutare vizuală',2,6,14,8),('F10 Pro și firme',2,6,8,4),('F11 Personalizare și loturi pilot',2,6,10,4),('F12 Liste Club card cadou',2,10,10,6),('F13 CRM măsurare SEO',2,4,10,4),('F14 Infrastructură și probe globale',0,0,16,6),('F15 Coordonare documentare predare',6,0,8,4)]
assert sum(sum(x[1:]) for x in wbs)==360
table(['Funcție','UX','FE','BE date ops','QA','Total'],[(*x,sum(x[1:])) for x in wbs]+[('TOTAL',55,94,140,71,360)],[8.3,1.3,1.3,2.3,1.3,3],small=9.5)
p('La 130 zile lucrătoare nominale, media este 2,77–3,46 echivalenți normă întreagă; vârful S3–22 este 4–5. Plan minim de disponibilitate: frontend 1, backend 1, UX 0,5–1, QA 0,5–1 și date/DevOps/AI 1, cu reducerea alocărilor în afara vârfului. Un tabel nominal săptămânal la S2 trebuie să acopere zilele fiecărui pachet, fără aceeași persoană alocată simultan peste 100%.')
p('F08/F09/F11/F12 însumează 106 zile, adică 29,4% din bază, pentru diferențiere. Producția externă de media și revizia lingvistică sunt separate. PO CESIRO minimum 2 zile/săptămână și doi editori ×50 zile pentru catalog sunt contribuții interne declarate, suplimentare celor 360–450 zile ale furnizorului; trebuie evaluate financiar la costul intern real.')

page('17.1 Scenarii și buget total')
p('Tarife ipotetice pentru cererea de ofertă: echipă locală cu platforma EVA 250–400 EUR/zi; alternativă furnizor complet 400–550 EUR/zi. Nu sunt prețuri de piață verificate. Se cer minimum două oferte comparabile pe WBS și topologia ADR04. Sumele sunt fără TVA, fără conversie fictivă în lei.')
table(['Scenariu','Calcul','Total cu rezervă'],[
('Minim\nValurile 1–2','F01–04, F06–07, F13–15 = 216–270 zile ×250–400; media 8.000–14.000; operare tehnică 6 luni 7.800–11.400; mentenanță 6 luni 9.000–18.000.','90.620–174.110 EUR; rezervă 15%. Domeniu redus, fără promisiunea tuturor funcțiilor recomandate.'),
('Recomandat local\nValurile 1–4','360–450 zile ×250–400; media 19.460–35.100; operare tehnică 7.800–11.400; mentenanță 9.000–18.000.','145.199–281.175 EUR; rezervă 15%.'),
('Recomandat furnizor complet','Același domeniu 360–450 zile ×400–550; aceleași media, operare și mentenanță.','207.299–358.800 EUR; rezervă 15%.'),
('Extensii ambițioase','AR, contribuții financiare de grup, abonament Mystery Box, credit Pro și integrare ERP avansată: +60–90 zile ×250–400; media 3D +2.500–5.000; operare +1.000–2.000.','+22.200–51.600 EUR; rezervă 20%; activare și calendar separate de cele 26 săptămâni.')],[3.8,9.4,4.3],small=9.7)
p('Formula totalului: (zile × tarif + media externă + operare tehnică + mentenanță) × (1 + rezervă). Capătul superior folosește 450 zile și costurile maxime; rezerva de 15% acoperă riscuri comerciale reziduale și variația tarifelor, nu încă o tranșă de zile pentru aceleași pachete. Extensiile nu sunt incluse în totalul recomandat.')
p('Operare tehnică: 6 × (700–1.300 EUR infrastructură/licențe + plafon AI 600 EUR) = 7.800–11.400 EUR. Mentenanța și permanența sunt separat 1.500–3.000 EUR/lună. Pentru 12 luni de operare după lansare, se adaugă încă 16.800–29.400 EUR, înainte de rezervă. Perioada de 6 luni începe la prima producție nouă; activarea serviciilor înainte de aceasta se cotează în ADR04.')
p('Nu sunt incluse: publicitate plătită, comisioane tranzacționale, transport, spargeri, materiale/echipamente de fabrică, hardware AI, costul intern al PO/editorilor și certificate/documente ce trebuie procurate de furnizori. Facturile și timpul CESIRO sunt bugetate de beneficiar înainte de angajament; suma de mai sus nu este prezentată ca întregul cost economic al firmei.')

page('17.2 Devizul media și localizare')
table(['Linie și volum','Ipoteză unitară EUR','Interval EUR'],[
('150 produse refotografiate ×3 cadre; 150 reutilizate','450 cadre ×12–20','5.400–9.000'),
('30 clipuri scurte din filmări grupate','80–160 / clip','2.400–4.800'),
('12 scene cu styling și drepturi','180–350 / scenă','2.160–4.200'),
('100 decupaje pentru configurator','8–15 / imagine','800–1.500'),
('Revizie RO pentru 300 prioritare','4–7 / fișă','1.200–2.100'),
('Revizie 5 limbi ×300 prioritare','4–7 / fișă și limbă','6.000–10.500'),
('Texte UI și politici în 6 limbi','250–500 / pachet lingvistic','1.500–3.000'),
('TOTAL scenariu recomandat','','19.460–35.100')],[9.2,4.7,3.6])
p('Ipotezele sunt alocații pentru ofertare, cu reutilizarea activelor și filmări în lot, nu prețuri de piață certificate. Devizul final precizează numărul de cuvinte, complexitatea tehnică, stylingul, drepturile, reviziile și deplasările. Estimarea nu finanțează rescrierea completă a tuturor textelor secundare. Necesarul juridic specializat se cotează separat dacă depășește revizia textelor din pachet.')
h('Varianta cu studio în fabrică')
p('Producție internă foto/video/scene/decupaje: echipamente 2.000–4.000 EUR și 30–40 zile de fotograf/editor CESIRO la costul intern real c EUR/zi. Revizia RO și a limbilor rămâne 8.700–15.600 EUR. Total alternativ = 10.700–19.600 EUR + (30–40) × c. Înlocuiește liniile vizuale externe, nu se adaugă peste ele. Se aprobă numai după 10 produse pilot care trec controlul de culoare, scară și decupaj.')
p('Doi editori de date ai CESIRO nu sunt considerați automat fotografi sau traducători. Orice persoană comună se alocă o singură dată în planul săptămânal. Dacă reutilizarea pentru 150 produse eșuează, se suplimentează devizul și calendarul media înainte de publicare.')

page('17.3 Garanție mentenanță și incidente')
p('Clauză contractuală propusă: garanție de 90 zile de la recepția fiecărui val pentru defecte față de specificație, inclusă în prețul dezvoltării. O corecție recurentă pentru același defect nu se facturează ca funcție nouă. Serviciile de monitorizare, actualizări de securitate și permanență sunt în abonamentul separat, inclus în calculele pe 6 luni. Extinderea garanției la 180 zile se solicită în ofertă, cu preț explicit.')
table(['Severitate','Răspuns și restabilire propuse','Canal și responsabil'],[
('P1 magazin/plăți/acces compromis','24/7: răspuns ≤1 h, restabilire sau izolare sigură ≤8 h; pentru recuperarea datelor se aplică obiectivul mai strict RTO ≤60 min din ADR04.','Alertă externă + telefon; DevOps și lider tehnic, doi înlocuitori nominalizați.'),
('P2 funcție majoră degradată','Răspuns ≤4 h lucrătoare, soluție temporară ≤1 zi lucrătoare, termen de remediere comunicat.','Ticket și jurnal incident; proprietar de modul.'),
('P3 defect minor','Răspuns ≤2 zile lucrătoare; plan în următorul sprint.','Backlog acceptat de PO.')],[3.6,8.9,5])
p('Programul lucrător este 09–18, luni–vineri, Europe/Bucharest, exceptând sărbătorile, în afara P1. Furnizorul confirmă în ofertă permanența 24/7; fără acoperire nominală și cost nu se declară SLA contractat. Restabilirea poate fi rollback sau dezactivare sigură; cauza și remedierea definitivă se documentează în maximum 5 zile lucrătoare pentru P1. SLO 99,9% rămâne separat de ținta de răspuns.')
p('Patchuri critice exploatabile: izolare imediată, plan în 24 ore și aplicare validată conform urgenței; dependențe revizuite lunar. Backupurile și restaurarea se verifică lunar; drepturile trimestrial. Predarea include accesuri deținute de beneficiar, exporturi, configurări, manual de operare și inventar licențe, fără dependență de un singur furnizor.')
""")
rep("page('17 Guvernanță", "page('17.4 Guvernanță")
rep("('Cod diferit de producție'", "('Infrastructură partajată','ADR04 și probă de failover înainte de lansare; resurse izolate și alertare externă.','DevOps'),\n('Copii divergente EVA','Versiuni comune, configurare per tenant, compatibilitate API și migrații pe două configurații.','Lider tehnic'),\n('Cod diferit de producție'")
rep('Contribuțiile financiare de grup, abonamentul Mystery Box, creditul Pro și AR extins apar în scenariul ambițios, după pilot.','Contribuțiile financiare de grup, abonamentul Mystery Box, creditul Pro, AR și integrarea ERP avansată sunt extensii separate.')
rep('și 10 modele AR pilot.','și fișiere vectoriale verificate; AR este în afara recepției recomandate.')
rep('Matrice legală pe entitate/piață/familie și aprobarea domeniilor aplicabile.','Matrice legală pe entitate/piață/familie: retragere online, CLP, biocide, ingrediente, preț unitar, SAL, documente alimentare și aprobarea domeniilor aplicabile.')
rep('Criteriile din capitolul 13, accesibilitate AA','Criteriile din §9.1, §9.2, §10 și §13, accesibilitate AA')
before("page('20 Benchmark", r"""h('Șase concluzii acționabile din eșantion')
table(['Semnal','Acțiune și rezultat'],[('Coduri finale SKU','Validare fabrică pe 100 SKU-uri înainte de generarea seriilor.'),('Materiale și mărci terțe','Verificare producător real; originea CESIRO nu se propagă după categorie.'),('Sticlă cu text Cesiro','Investigare proveniență din acte; numele comercial nu dovedește fabricantul.'),('Chimice și biocide','Clasificare legală și documente pe piață înainte de promovare Pro.'),('20 greutăți lipsă în eșantion','Măsurare produs/ambalaj; nu se promite cost de transport din valori estimate.'),('Seturi și capacități','Descompunere în componente; dimensiunea cănii nu este atribuită întregului set.')],[5.1,12.4])
""")
before("h('Cercetarea care închide", r"""h('Repere directe și vocea cumpărătorilor')
p('A1 extinde comparația la Bonna, Kütahya Porselen, Pașabahçe și Lubiana: serii, rezistență documentată, comandă HoReCa, completare și personalizare. Bonna și Lubiana au intrări oficiale de colecții/HoReCa identificate; celelalte sunt repere de investigat, fără concluzii de performanță atribuite. Se documentează 4 fișe comparative și 10 oportunități aplicabile. [B10, B11]')
p('Pentru eMAG și Trendyol se identifică listările CESIRO și vânzătorul real, apoi se includ recenzii și întrebări publice în limita de până la 500 surse din A1. Se înregistrează URL, dată, produs și temă, fără a copia date personale. Prețurile de pe canale sunt instantanee datate; nu se presupune aceeași ofertă sau o permisiune de contactare a clienților.')
""")
block("h('Domeniul acestei revizii')", "page('20 Surse interne", '')
rep("page('20 Surse interne", "page('20.1 Surse interne")
rep("page('20 Surse legale", "page('20.2 Surse legale")
rep("save('Proiect_CESIRO_Design_React_Python_V2.docx')", "save('Proiect_CESIRO_Design_React_Python_V3.docx')")
rep("print('Proiect V2 salvat')", "print('Proiect V3 salvat')")
before("save('Proiect_CESIRO_Design_React_Python_V3.docx')", r"""page('20.3 Surse suplimentare pentru cerințele V3')
for x in [
('S6 CESIRO identitatea vânzătorului','https://cesiro.com/legal/termeni-si-conditii'),
('T6 Next.js revalidateTag și expirare','https://nextjs.org/docs/app/api-reference/functions/revalidateTag'),
('T7 ANAF înregistrarea aplicațiilor OAuth','https://static.anaf.ro/static/10/Anaf/Informatii_R/API/Oauth_procedura_inregistrare_aplicatii_portal_ANAF.pdf'),
('L10 Directiva 2023/2673 și funcția de retragere','https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32023L2673'),
('L10b OUG 34/2014 dreptul de retragere și excepții','https://legislatie.just.ro/Public/FormaPrintabila/00000G1YMI9WLN4N9523GGWAROSL0LJK'),
('L11 ECHA calendarul revizuirii CLP','https://echa.europa.eu/regulations/clp/understanding-clp'),
('L12 HG 947/2000 prețul pe unitate și excepții','https://legislatie.just.ro/Public/DetaliiDocumentAfis/24730'),
('L13 Biocide articolul 72','https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:02012R0528-20220415'),
('L14 Regulamentul 2026/405 și tranziția detergenților','https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32026R0405'),
('L15 Comisia Europeană portalul de soluționare a litigiilor','https://consumer-redress.ec.europa.eu/'),
('B10 Bonna colecții','https://www.bonna.global/all-collections'),
('B11 Lubiana clienți profesionali','https://lubiana.com.pl/biznesowy/')]:link(*x)
p('Consultare la 21 octombrie 2026. Registrul juridic al implementării trebuie să verifice textele consolidate, transpunerile și condițiile pieței efective. Sumele și debitele de lucru sunt ipoteze explicite de estimare; nu sunt cotații obținute de la furnizori.')

for i,ttl in enumerate(['Atelier și glazură','Masa de acasă','Colecția contemporană','Homepage pe mobil','Produs pe mobil','Masa completă pe mobil'],1):
    page(f'21.{i} '+ttl)
    p('Planșă conceptuală de proiectare. Formele sunt ilustrații schematice, nu fotografii sau produse certificate din catalog.' if i<=3 else 'Wireframe de structură și conținut. Valorile sunt exemple de interfață, nu oferte comerciale sau ecrane implementate.')
    doc.add_picture(str(OUT/'visuals-v3'/f'plan-{i}.png'),width=Cm(17.1))
    p(['Texturi minerale, tonuri de lut, gesturi de fabricare reale în etapa foto. Originea este afișată numai unde poate fi demonstrată.', 'Direcție recomandată pentru test: mese reale, utilizări și ocazii; intrarea după decor susține completarea setului.', 'Compoziție grafică, contrast și culoare. Testul verifică dacă identitatea modernă păstrează percepția de ceramică.', 'Prioritate: căutare, utilizări, serie și configurator. Pro are intrare distinctă; fără carusel obligatoriu sau urgență fictivă.', 'Prețul și stocul vin din aceeași sursă comercială; detaliile tehnice, producătorul și siguranța sunt verificabile înainte de cumpărare.', 'Alternativa de listă este complet funcțională cu tastatura. Schimbarea persoanelor recalculează cantitățile și afișează piesele indisponibile.'][i-1])

page('22 Istoricul documentului și registrele de decizie')
p('V1 a stabilit direcția inițială; V2 a integrat inventarul local și reutilizarea EVA. V3 răspunde celor 118 coduri A2 din Audit.Claude.V2.0 și directivelor din auditul tehnic V2 din 21 octombrie 2026. Matricea separată păstrează decizia, referința exactă și proba viitoare, fără a confunda o specificație cu o funcție realizată.')
p('Versiunile anterioare și auditurile rămân nemodificate. Nu s-au modificat site-ul, codul platformei, catalogul operațional sau integrarea cu marketplace-uri. Planșele sunt propuneri documentare; D01 curent, D02 comercial, testele funcționale și recepția se execută în proiectul ulterior.')
table(['Registru','Responsabil și termen','Rezultat necesar'],[('D01 inventar actual','Date și platformă până la S2','SQL de citire versionat, snapshot, numărători, reconciliere și demonstrații.'),('D02 baseline comercial','Financiar și analytics până la S2','Venituri agregate, conversie, Pro, marjă, durată de experiment.'),('D03 design și conținut','UX și editorial S1–6','Direcție validată, 25 tipuri, 75 ecrane și 10 machete pe familii.'),('ADR01–04','Tehnic și DevOps S2/S4','Frontend, căutare, cache și producție, cu cost și probe.'),('Registru legal și producție','Juridic și fabrică înainte de val','Entități, promisiuni, documente, capacitate și excepții pe piață.')],[4.1,5.5,7.9])
""")
(O/'build_v3.py').write_text(s,encoding='utf-8')

audit=Document(O/'Audituri/Audit.Claude.V2.0.docx')
rows=[]
for t in audit.tables:
    for r in t.rows[1:]:
        c=[x.text.strip() for x in r.cells]
        if c and c[0].startswith('A2-'):rows.append(dict(id=c[0],text=c[1],priority=c[2]))
assert len(rows)==118 and len(set(x['id'] for x in rows))==118
(O/'evidence-v3').mkdir(exist_ok=True)
(O/'evidence-v3/audit-claude-v2.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('V3 prepared; audit IDs',len(rows))
