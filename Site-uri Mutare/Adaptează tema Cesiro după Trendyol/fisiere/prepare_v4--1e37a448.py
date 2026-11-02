from pathlib import Path
import re

O=Path(__file__).parent
s=(O/'build_v3.py').read_text(encoding='utf-8')
s=s.replace("'Proiect V3'","'Proiect V4'").replace('Versiunea 3 specificație','Versiunea 4 specificație').replace('Proiect_CESIRO_Design_React_Python_V3.docx','Proiect_CESIRO_Design_React_Python_V4.docx').replace('Proiect V3 salvat','Proiect V4 salvat')
s=s.replace('Proiect CESIRO pentru o temă React pe platforma Python existentă','Proiect CESIRO pentru tema React și extensiile platformei Python')

def section(start,end,body):
    global s
    a=s.index(start); b=s.index(end,a)
    s=s[:a]+body.strip()+'\n\n\n'+s[b:]

def para(prefix,new):
    global s
    pattern=r"p\('"+re.escape(prefix)+r"[^\n]*\)"
    found=re.findall(pattern,s)
    assert len(found)==1,(prefix,len(found))
    s=s.replace(found[0],'p('+repr(new)+')')

section("head('0 Direcția propusă')","page('1 Date disponibile",r'''
head('0 Direcția și domeniul programului')
p('CESIRO va ajuta clientul să își compună masa, să completeze decorul preferat și să aleagă un cadou personal. De la Trendyol preluăm accesul clar la produse, căutarea și filtrarea; experiența proprie pornește de la ceramică, utilizări, culori și ocazii. Zona Pro are acces distinct, pe același catalog.')
p('Varianta C cuprinde tema nouă și extensiile E0–E7 în aplicația Flask și baza PostgreSQL existente. Nu creează un sistem API paralel, un backend comercial nou sau un catalog separat. JavaScript și React asigură interactivitatea, iar Flask randează paginile publice. Documentul descrie lucrări viitoare și nu reprezintă implementare sau lansare pe site.')
table(['Diferențiator','Rezultat măsurabil'],[
('Origine și încredere','100% dovezi pentru produsele promovate ca fabricate de CESIRO; păstrarea înlocuirii gratuite a produselor sosite sparte.'),
('Masa potrivită','20 serii validate și 12 scene cumpărabile; selecție pentru 2/4/6/8 persoane, cu cantități și total verificate.'),
('Cadou personal','Ambalaj cadou și mesaj din funcția existentă, din prima lansare; E6 adaugă personalizarea a 10 produse după aprobarea fabricii.')],[4.2,13.3])
h('Două livrări coordonate')
p('Tema se lansează la săptămâna 16, cu 160–200 zile-persoană. Programul complet durează 24–26 săptămâni și include încă 80–120 zile-persoană pentru E0–E7: total 240–320. E0 și E2 sunt prima etapă urgentă, planificată pe tema actuală în săptămânile 1–3. Inovarea are propriile praguri de activare și nu amână tema.')
table(['Pachet','Domeniu inclus'],[
('Temă','21 tipuri de pagini de bază, 10 variante sezoniere/de eveniment, configurator 2D, conținut, localizare, SEO și reutilizarea fluxurilor comerciale.'),
('E0–E3 esențiale','Retragere fără cont și retur; filtre serie/persoane; acces securizat la comandă fără cont; completare firmă după CUI.'),
('E4–E7 inovare','Asistent public doar citire; căutare vizuală și semantică; personalizare pilot; registru de puncte Club.'),
('Ulterior','Liste de eveniment, card cadou cu sold, precomenzi pe loturi, preț pe client Pro, abonament și AR. Nu sunt incluse în totalul variantei C.')],[4.2,13.3])
p('Tema folosește API-urile actuale, iar extensiile adaugă numai rutele și tabelele necesare în același motor. Fiecare extensie are comutator pe tenant, teste și recepție separată. Cu inovarea oprită rămân catalogul, căutarea text, coșul și cumpărarea standard. E0, fiind flux de exercitare a drepturilor, are reguli de continuitate distincte și nu se oprește printr-un experiment comercial.')
p('Comunicare de testat: „Ceramică din Sighișoara, aleasă pentru masa ta”, numai pentru produsele cu proveniență documentată. Celelalte produse păstrează producătorul real. Țintele de venit sunt ipoteze de verificat pe D02; recepția tehnică nu este o promisiune de rezultat comercial.')
''')
para('Inventarul folosește', 'Inventarul combină observațiile publice din 21 octombrie 2026, exportul istoric de produse și citirea statică a codului din U:/cesiro.com. Baze operaționale, comenzi nominale și conturi de clienți nu au fost accesate. Starea codului este documentată în §11; D01 confirmă datele actuale și versiunea instalată. [I1–I8]')
para('În U:/cesiro.com există', 'La verificarea din 21 octombrie 2026, U:/cesiro.com există, iar vechea cale U:/cesiro1-site nu mai există. Data exactă a redenumirii nu este dovedită; referințele istorice rămân în V2/V3, iar V4 folosește calea actuală. Exportul are același hash SHA-256 documentat. Pentru 14 fișiere cheie s-a salvat un manifest de hashuri în evidence-v4/source-hashes.json. Repository-ul GitHub indicat răspunde în continuare cu 404 prin conexiunea disponibilă; nu se inventează un commit și nu se echivalează hashurile de fișiere cu versiunea din producție. [I6]')
para('Câmpurile de mai sus', 'Dicționarul mapează mai întâi câmpurile și conținutul existente. E1 poate adăuga relațiile de serie/persoane; E0/E2/E6/E7 adaugă strict datele funcțiilor lor; E5 stochează vectori derivați. Migrările Alembic sunt additive, în PostgreSQL-ul actual, cu tenant și păstrarea ID-urilor canonice. Nicio extensie nu copiază întreg catalogul ca sursă comercială concurentă.')
s=s.replace('preț pe client Pro.','preț pe client Pro doar în extensie ulterioară.')
section("page('4 Obiective și rezultate cuantificabile')","page('5 Navigare",r'''
page('4 Obiective și rezultate cuantificabile')
p('Venitul net direct este valoarea produselor facturate fără TVA, minus reduceri, anulări și retururi, fără transport. Sursa financiară prevalează asupra atribuirii analytics. Creșterile sunt relative dacă nu scrie puncte procentuale. D02 fixează până la S2 baza pe 12 luni, traficul eligibil pe minimum 8 săptămâni, marja și segmentele.')
h('Indicatorii temei de bază')
table(['Indicator','Țintă inițială la 90 zile','Mecanism și populație'],[
('Venit direct','+15%; marjă/comandă fără scădere','Navigare pe ocazii, 20 serii, 12 scene și checkout; venit financiar comparabil, control pentru sezon/media/stoc.'),
('Conversie mobilă','+15%','Comenzi plătite valide / sesiuni mobile eligibile; ierarhie clară, performanță și formulare.'),
('AOV net','+10%','Venit net produse / comenzi valide; completarea seriei și configuratorul, fără a atribui efectul automat unui singur modul.'),
('Abandon checkout','−15%','1 − comenzi valide / sesiuni begin_checkout; atribuire 7 zile, plățile în așteptare reconciliate.'),
('Încredere','Recenzii la ≥5% din livrările eligibile','Recenzii autentice; rata de spargere nu crește peste 0,3 pp față de D02.'),
('Pro și QR','50 conturi firme; 20 primi cumpărători; QR ≥5% scanări și ≥2% prime comenzi','Pro la 90 zile de la temă/E3; QR pe 1.000 inserții eligibile. Scanarea nu dovedește migrarea din marketplace.')],[3.1,4.6,9.8])
p('Fereastra temei începe după activarea la 100% în S16. D02 recalibrează țintele înainte de ofertarea fermă, pe funcțiile livrate și traficul disponibil. Se păstrează și ținta Pro de venit +15% și recumpărare ≥25% în cohorte cu 90 zile complete; o bază zero cere țintă absolută, nu procent artificial.')
h('Indicatorii extensiilor')
table(['Extensie','Țintă și început de măsurare'],[
('E4 și E5 descoperire','≥10% dintre sesiunile expuse folosesc asistentul sau căutarea vizuală; separat pe extensie, în primele 90 zile de la activare. Configuratorul are raport distinct.'),
('E4 valoare incrementală','+10% conversie prin A/B pe disponibilitatea asistentului; nu comparație cauzală între cei care îl aleg și ceilalți.'),
('E6 personalizare','≥5% din comenzile cu produse eligibile au personalizare; marjă pozitivă după costul fabricii; 90 zile de la activarea pilotului.'),
('E7 Club','+3 pp recumpărare la 90 zile față de cohorta comparabilă; costul punctelor în plafonul aprobat de financiar.'),
('E0–E3 servicii','Criterii funcționale R12: retragere, acces, filtre și firmă; nu se presupune venit incremental fără experiment.')],[4.1,13.4])
p('E4/E5/E6/E7 au fiecare dată de activare, cohortă, versiune și raport la 90 zile; programul S26 nu înseamnă că toate ferestrele comerciale s-au încheiat. R10 separă rezultate, utilizare și incertitudine. Recepția tehnică se bazează pe criterii controlabile; venitul și conversia rămân ipoteze comerciale.')
''')
s=s.replace("('Nuntă și aniversare','Liste de eveniment, cantități comune și mesaje cadou.')","('Nuntă și aniversare','Selecții de cadouri și mesaje; lista partajată de eveniment rămâne extensie ulterioară.')")
para('Editorul trebuie să creeze', 'Filtrele existente în cod sunt q, category_id, brand, color, material, capacity, finish, in_stock, on_sale, min_price/max_price, sort și lang. E1 adaugă serie/decor și număr de persoane, cu compatibilitate pentru cererile vechi. Editorul creează o colecție din date pregătite în maximum 5 minute; nu se multiplică produsele pentru fiecare ocazie.')
para('Segmente precum', 'Segmente precum G242, D144, 604M și 010L sunt candidați, nu dovadă de decor. Fabrica validează 100 SKU-uri și excepțiile; E1 păstrează dicționarul și legăturile aprobate pe produsul canonic. „Completează decorul tău” se automatizează numai pentru cele 20 serii validate. Produsele terțe și codurile ambigue nu se unesc automat; zero asocieri greșite în lotul publicat.')
section("page('6 Experiența vizuală și paginile')","page('7 Sistem",r'''
page('6 Paginile de bază și starea de livrare')
p('Inventarul are 25 tipuri de design: 21 implementate în tema de bază, 2 activate prin E6/E7 și 2 păstrate numai ca idei ulterioare. „Planificat” descrie proiectul, nu o funcție deja instalată. Pentru cele 25 tipuri se livrează minimum 75 ecrane la 390, 768 și 1440 px, plus stări de eroare, gol, încărcare și indisponibilitate.')
page_types=[
('01','Homepage','Temă','Căutare, utilizări, serii și scene'),('02','Categorie și listare','Temă + E1','Filtre actuale; serie/persoane prin E1'),('03','Rezultate căutare','Temă + E5','Text la S16; vizual/semantic prin E5'),('04','Produs','Temă + E6','Fișă actuală; personalizare la activarea E6'),('05','Decor și serie','Temă + E1','20 serii aprobate; pagină HTML și filtre'),('06','Colecție și ocazie','Temă','12 familii editoriale pe catalogul actual'),('07','Scenă cumpărabilă','Temă','12 scene, piese și operații actuale de coș'),('08','Configurator 2D','Temă + E1','Selecție locală; total comercial din motor'),('09','Selector cadou','Temă','Selecție, ambalaj și mesaj existente'),('10','Personalizare produs','E6','Pilot 10 produse; disponibil după proof'),('11','Coș','Temă','Aceleași reguli și rute'),('12','Checkout','Temă','Formular local; plata Stripe conform fluxului actual'),('13','Confirmare și urmărire','Temă + E2','Acces propriu securizat pentru vizitator')]
table(['ID','Tip de pagină','Livrare','Limită funcțională'],page_types,[0.8,4.2,3.3,9.2],small=9.5)
p('Tipurile cu „Temă + E#” sunt pagini de bază cu o funcție suplimentară identificată; ele nu sunt numărate încă o dată. E0/E2 se livrează pe tema actuală în S1–3, E1/E3 până la S10, înainte de recepția temei.')
page('6.1 Paginile relației cu clientul')
page_types2=[('14','Cont și favorite','Temă','Adrese, firme, favorite și istoric existente; vizualizări recente pot rămâne locale'),('15','Listă de eveniment','Concept ulterior','Fără registru partajat sau contribuții în varianta C'),('16','Club CESIRO','E7','Sold, reguli și istoric după recepția registrului'),('17','Card cadou cu sold','Concept ulterior','Nu se vinde un sold fără registru și reconciliere'),('18','Outlet','Temă','Produse existente, defecte descrise, siguranță păstrată'),('19','Poveste fabrică showroom','Temă','Pagini editoriale și proveniență verificată'),('20','Jurnal și articol','Temă','30 ghiduri în CMS, dintre care 10 până la T2'),('21','Recenzii și UGC','Temă','Afișare conținut aprobat prin mecanisme actuale; fără platformă socială nouă'),('22','Ajutor și politici','Temă + E0','Politici, contact și acces vizibil la retragere'),('23','Pro și comandă repetată','Temă + E3','Firmă pe cont, selecție SKU/coș actual; fără preț contractual pe client'),('24','Ofertă mostre logo','Temă + E6','Cerere prin canalul actual; producția cu logo prin E6'),('25','Comenzile mele și servicii','Temă + E0/E2','Spargere, factură, retragere și solicitări; decizie operațională umană')]
table(['ID','Tip de pagină','Livrare','Limită funcțională'],page_types2,[0.8,4.2,3.3,9.2],small=9.5)
p('Contractul page_contracts declară paginile efectiv disponibile: cele 21 tipuri de bază, apoi cele două tipuri E6/E7 la activare. Nu declară funcțional un concept. Tipul de design poate grupa mai multe rute și stări; D03 păstrează maparea completă tip → rută → limbă → extensie → test.')
h('Alegerea vizuală și experiența pe mobil')
p('Cele trei planșe §21 folosesc fotografii existente din arhiva CESIRO, perechi de fonturi și fragmente de produs distincte. Două runde cu câte 8 participanți verifică găsirea unui set, completarea seriei și alegerea unui cadou. Ordinea conceptelor se alternează; se măsoară succesul, timpul și înțelegerea informației, separat de preferința estetică. În runda finală: ≥90% succes pe sarcini și SUS ≥80.')
p('Produsul păstrează ierarhia imagine și scară → nume și serie → preț/stoc → variante → livrare → cumpărare → componente și utilizări → siguranță și îngrijire → completare și recenzii. Galeria, barele de acțiuni și configuratorul au focus vizibil, control prin tastatură și respectă mișcarea redusă.')
''')
para('Inventarul de 25 tipuri', 'Inventarul are 25 tipuri proiectate și 21 tipuri implementate în tema de bază; E6/E7 adaugă două, iar două rămân concepte. Arhiva Z:/images conține la inventariere 38.872 fișiere, dintre care 38.865 cu extensie de imagine, nu tot atâtea produse sau fotografii unice. Reutilizarea precede refotografierea: asociere SKU, deduplicare, drepturi și verificare vizuală. Bugetul media păstrează ipoteza de 150 produse reutilizate, fără economie pretinsă înainte de selecție.')
section("page('8.1 Funcții comerciale", "page('8.2 Funcții",r'''
page('8.1 Masa completă și descoperirea asistată')
h('Masa completă și completarea decorului')
p('Clientul alege 2/4/6/8 persoane, buget și stil, apoi modifică piesele într-o compoziție React 2D. Fiecare poziție are rol, SKU și cantitate; totalul final este calculat de motor. E1 furnizează seriile și persoanele aprobate. „Ce ai deja?” scade selecțiile locale și propune piese din aceeași serie; alternativele sunt etichetate explicit. Țintă: 20 serii, 12 scene, 10 scenarii de buget, zero totaluri comerciale invalide.')
h('E4 Asistent public numai pentru citire')
p('E4 este planificat și estimat. Reutilizează clientul LLM și componentele sigure din ai_assistant, nu ruta admin, identitatea OWNER sau setul de unelte administrative. Primește numai catalog public, politici aprobate și, după E2, datele strict necesare ale comenzii autorizate. Nu scrie în coș, nu plasează/plătește/anulează comenzi, nu inițiază retururi și nu modifică puncte. Poate prezenta un link sau o selecție pe care clientul o confirmă într-un flux determinist separat.')
p('Răspunsurile identifică produsele și sursa politicii, verifică prețul/stocul și spun clar când informația lipsește. Interfața anunță că asistentul este AI; oferă căutare clasică și suport uman. Conținutul de produs și fișierele clientului sunt date nefiabile, nu instrucțiuni. Accesul la comenzi se filtrează înainte de model; nu se trimite întreg istoricul în prompt.')
table(['Probă','Prag de activare'],[
('Cumpărare','200 cereri etalon, inclusiv 40 adversariale; ≥90% corecte și utile evaluate uman; zero acțiuni neautorizate.'),
('După cumpărare','100 cereri suplimentare, inclusiv 30 de izolare/atac; ≥90% corecte și utile; zero divulgări între clienți/tenanturi.'),
('Timp','Primul răspuns p95 ≤4 s și răspuns complet p95 ≤10 s la sarcina agreată; timeout și alternativă clară.'),
('Cost','E4 și E5 împart plafonul propus de 600 EUR/lună. E4 urmărește ≤0,06 EUR/sesiune; volumul disponibil scade cu costul E5 și nu este garantat.')],[4.1,13.4])
h('E5 Căutare vizuală și semantică')
p('E5 este planificat în PostgreSQL-ul existent cu pgvector, fără un motor de căutare separat. Vectorii de imagine și text au model, versiune, tenant, produs canonic și sursă. Filtrarea de eligibilitate, stoc și piață precede afișarea. O imagine asemănătoare nu dovedește același decor; SKU exact are prioritate și rezultatul incert este numit alternativă.')
p('Set etalon: 100 imagini cu produs prezent și 50 fără corespondent. Recall@5 ≥85% pe cele 100; maximum o identificare exactă falsă din cele 50 fără corespondent. Căutare semantică: 60 interogări/limbă ×6, nDCG@10 ≥0,80 pe fiecare limbă. Fotografii încărcate: MIME real, limite de volum/dimensiuni, fără EXIF, acces izolat și ștergere în ≤24 h; nicio folosire pentru antrenare fără temei separat.')
p('PoC E4/E5 în S1–3 măsoară calitate, concurență și cost pe date izolate. Capacitatea LLM locală poate fi împărțită cu traduceri: se rezervă resurse sau prioritate pentru public. Alertă la 80% din plafon; la 100% se opresc procesările AI bugetate, cu căutarea text și suportul disponibile. Hardware nou nu este presupus finanțat.')
''')
section("page('8.2 Funcții", "page('8.3 Retenție",r'''
page('8.2 Cadou personal și producție')
h('Cadou disponibil din prima lansare')
p('app/gift.py și migrația 0079 susțin ambalaj cadou și mesaj pe comandă. Tema folosește opțiunile active din /api/checkout/packaging-options și validarea actuală; limita de mesaj observată este 300 caractere. Versiunea citită nu adaugă preț pentru ambalaj. Nu se introduce o taxă în interfață fără suport comercial și aprobare explicită.')
h('E6 Personalizare pilot pentru 10 produse')
p('E6 adaugă text, monogramă, dată și logo în zone aprobate de fabrică. Pentru fiecare produs se fixează fonturi, caractere, culori, rezoluție, cost, cantitate minimă și termen. E6 păstrează configurarea și fișierul asociate versiunii plătite; opțiunea, prețul și termenul se revalidează pe server înainte de comandă. Nu există recalcul comercial autoritativ în React.')
p('Flux: configurare → previzualizare → ofertă valabilă → confirmare client → plată prin motor → verificare umană → fișier aprobat → producție și control → expediere. Fișierul aprobat nu se regenerează cu alt text după plată. Datele comerciale, configurarea, previzualizarea și producția au același identificator și hash.')
table(['Element','Condiție de recepție'],[
('Fișier de producție','SVG/PDF la scară 1:1, milimetri, fonturi licențiate convertite în contururi, profil de culoare și toleranțe stabilite de fabrică.'),
('Încărcări','Logo scanat și sanitizat; fără scripturi sau resurse externe. Format raster numai dacă tehnologia fabricii și rezoluția permit.'),
('Probe','20 comenzi simulate reconciliate, cu diacritice, text la limită, logo invalid și respingere la preflight; proof fizic aprobat pentru fiecare din cele 10 produse.'),
('Capacitate','Registru al fabricii cu responsabil, termen și dată; suspendare personalizare dacă sursa e veche sau capacitatea este consumată. Nu se construiește ERP.'),
('Drepturi','Bifă separată de informare, nebifată inițial, pentru bunuri realizate efectiv după specificații; rămân drepturile de neconformitate. Un set standard configurat nu este automat exceptat.')],[4.1,13.4])
p('Text propus: „Am înțeles excepția de la dreptul de retragere pentru acest produs personalizat; drepturile legale pentru neconformitate rămân aplicabile.” Bifa documentează informarea, nu creează o renunțare generală la drepturi. Pentru dispută, E0 permite înregistrarea declarației și analiza umană. [L10b]')
h('Accesibilitate și funcții ulterioare')
p('Configuratorul 2D oferă aceeași selecție prin listă, butoane și cantități editabile; focus stabil și anunțuri ARIA pentru totaluri și erori. Drag and drop, culoarea sau gesturile nu sunt singurele mijloace de operare. AR rămâne separat, cu 10 modele GLB/USDZ ca posibil pilot ulterior.')
p('Listele de eveniment, contribuțiile de grup și precomenzile pe loturi nu intră în E0–E7. Rămân concepte cu estimare preliminară în §17.5; nu se afișează funcții cumpărabile înainte de propriile registre, reguli și recepții. Pentru un eveniment se pot cumpăra produse standard sau trimite cerere prin canalul actual.')
''')
section("page('8.3 Retenție", "page('8.4 Autoservire",r'''
page('8.3 Club CESIRO și relația cu firmele')
h('E7 Registrul de puncte')
p('Club CESIRO este planificat prin E7, în baza actuală. Registrul are intrări imuabile pentru acordare, utilizare, ajustare și expirare; soldul este derivat și reconciliabil. Cheia de idempotență include tenantul, comanda, tipul și versiunea regulii. Repetarea webhookului nu acordă puncte de două ori; folosirea simultană a soldului se serializează.')
p('Regulile precizează eligibilitatea, momentul acordării, plafonul, expirarea și tratamentul returului aprobat de om. O ajustare nu modifică automat comanda sau rambursarea. Soldul nu se transferă între clienți ori tenanturi, iar recenziile pozitive nu sunt condiție pentru puncte. Financiarul aprobă costul lunar, tratamentul soldului negativ și expirarea înainte de lansare.')
p('Recepție: dublare și reordonare de evenimente, două utilizări concurente, retur parțial/total aprobat uman, expirare, reconciliere sold și izolare tenant. Testele automate pot verifica funcții pure pe evenimente sintetice; rutele de anulare/retur/rambursare nu sunt executate de AI, nici în simulări. Integrarea acestor operații se probează de operator uman conform REGULI.md.')
h('Pro de bază și E3 completare firmă')
p('Pro de bază include pagina dedicată, firmele din cont prin /api/account/companies, cerere de ofertă și cumpărare/repetare prin fluxurile actuale. Prețul contractual pe client este extensie ulterioară. Prețul public și TVA sunt explicite; nu se pretinde că un tarif Pro există pentru fiecare firmă.')
p('E3 reutilizează logica de interogare ANAF identificată în U:/acc-florin/app/main.py, adaptată în aceeași aplicație Flask. Nu reutilizează sesiunea sau baza aplicației de facturare și nu introduce OAuth e-Factura. CUI-ul este validat, rezultatul are dată/sursă și este confirmat de client; indisponibilitatea permite completare manuală. 20 CUI-uri de test acoperă firme active, inactive, invalide, negăsite și timeout; fără a transforma interogarea în aprobare fiscală.')
h('Comunicări și QR')
table(['Flux','Regulă inițială'],[
('Coș abandonat','La 2 h și opțional 24 h, prin mecanismul actual; oprire la cumpărare, dezabonare sau indisponibilitate.'),
('După livrare','La 7 zile, îngrijire, recenzie și UGC; informațiile de serviciu sunt separate de marketing.'),
('Reaprovizionare Pro','Propunere editabilă după consum și preferință; fără comandă automată implicită.'),
('Preferințe și Club','Maximum două mesaje promoționale/săptămână ca regulă inițială; consimțământ și furnizori activi verificați.'),
('QR','20 serii, 1.000 inserții: link persistent pe serie/campanie, fără identificarea persoanei în cod. Condițiile marketplace se verifică înainte de inserare.')],[4.1,13.4])
p('Abonamentele Mystery Box, finanțarea Pro și afilierea nouă nu intră în E0–E7. Fotografiile, promisiunile și costul punctelor sunt aprobate înainte de promovare. Scanarea QR nu este import de contacte marketplace și nu dovedește migrarea unui client.')
''')
para('Autoservirea folosește', 'Autoservirea reutilizează stările comerciale actuale. E2 adaugă accesul securizat fără cont, iar E0 înregistrează retragerea și reface interfața de retur în condițiile aprobate. E0 nu depinde de primirea unui link E2: formularul public rămâne accesibil fără cont. Asistentul E4 doar explică și trimite clientul spre flux; nu îl execută. R09 se leagă direct de recepția E0, înainte de lansarea temei.')
section("page('9 Arhitectura", "page('9.1 Baza",r'''
page('9 Arhitectura temei și extensiilor')
p('Tema de bază are numele de lucru cesiro_atelier, grup base, parent=null, template atelier. Se înregistrează în motorul existent cu manifest.json, files.json, page_contracts.json și README. marketplace_pro rămâne disponibilă ca rezervă și pentru celelalte magazine. JavaScript și React sunt compilate cu Vite; Flask/Jinja servește HTML complet și asseturi statice, fără runtime Node nou în producție.')
table(['Strat','Regula de proiect'],[
('Temă','Șabloane în templates/themes/atelier, CSS și pachete React în static/themes/cesiro_atelier; sursa componentelor într-un director de build dedicat.'),
('Logică comună','Coș, checkout, cont, preț, stoc, tenant și i18n rămân în motor. Tema nu modifică templates/shared; fragmentele diferite sunt proprii temei.'),
('Extensii E0–E7','Module/blueprinturi în aceeași aplicație Flask, aceeași sesiune, tenant, CSRF și formă a erorilor. Rute și câmpuri strict necesare, documentate în OpenAPI.'),
('Date','Migrări Alembic în PostgreSQL-ul existent; tabele tenant-scoped, constrângeri și teste de izolare; aceiași identificatori comerciali.'),
('AI și vectori','LLM local deja configurat, cu capacitate probată; pgvector în PostgreSQL actual. Fără motor vectorial sau backend AI comercial paralel.'),
('Activare','Comutator pe tenant și extensie, în configurația administrată a platformei; oprirea inovării nu necesită deploy și păstrează cumpărarea standard.')],[4.1,13.4])
h('Variante sezoniere și de eveniment')
p('Se livrează 10 variante proprii: primăvară, vară, toamnă, iarnă, Anul Nou, Crăciun, Paște, Halloween, începutul școlii și Black Friday. Fiecare are parent=cesiro_atelier și modifică tokenuri, imagini și mesaje, nu logica sau structura șabloanelor. Cele 10 variante existente ale marketplace_pro rămân intacte.')
p('theme_schedule rămâne mecanismul unic: default_theme=cesiro_atelier și intrări către variantele noi. Testele verifică limitele de dată, prioritatea eveniment/sezon, fusul configurat al magazinului și Paștele ortodox/catolic. Alegerea manuală și revenirea sunt disponibile în admin. Variantele noi sunt permise inițial numai tenantului CESIRO.')
h('Decizii de arhitectură până la S2')
p('ADR01 fixează tema și contractele paginilor; ADR02 fixează modelul local, pgvector și etaloanele; ADR03 descrie cacheul și actualizarea extensiilor; ADR04 verifică infrastructura, RPO/RTO și capacitatea. R00 permite extensii E0–E7 în motor, fără sistem API paralel. Contractele vechi rămân compatibile; nu se redenumesc toate rutele în /api/v1 doar pentru noua temă.')
''')
section("page('9.1 Baza", "page('9.2 Cache",r'''
page('9.1 Docker producție și revenire')
p('Fapt verificat la 21 octombrie 2026: U: este partajarea \\\\192.168.100.151\\site-uri, cu cesiro.com și alte proiecte, inclusiv dracula-book și eva-org.com. docker-compose.yml al CESIRO declară proiectul cesiro1, PostgreSQL 16, backend, admin, tunnel Cloudflare și migrate. Partajarea și coexistența proiectelor sunt confirmate; această citire nu dovedește containerele active, resursele folosite sau disponibilitatea măsurată.')
p('D01 fixează legătura domeniu → tenant → Compose → imagine/digest → commit. GitHub rămâne inaccesibil prin conexiunea disponibilă, iar folderul citit nu are .git. Manifestul de hashuri identifică proba locală; responsabilul platformei asigură acces de citire și referința Git înainte de ofertarea fermă și dezvoltare.')
table(['Control','Cerință și probă'],[
('Izolare','Preview și staging cu date anonimizate, secrete externe eliminate și gardă de rețea; fără scrieri spre marketplace sau servicii reale.'),
('Preview','Se folosește mecanismul autorizat theme_preview. ?theme= și cookie eva_theme depind de theme_compare_public; nu se promite acces public necondiționat.'),
('Cohorte','5% →20% →50% →100%, selecție persistentă pe vizitator și tenant. Dacă regula de cohortă lipsește, se implementează ca selecție de temă în motor, în N10, fără catalog/API paralel.'),
('Revenire','Comutare la marketplace_pro din admin în <1 minut pentru tema validată. Obiectiv de recuperare operațională completă ≤15 minute; coșul și comenzile se păstrează.'),
('Continuitate','Ținte de platformă: 99,9% lunar, RPO ≤15 min, RTO ≤60 min, probate în ADR04. Alternativa 99,5% cere decizie contractuală distinctă și nu este declarată echivalentă.'),
('pgvector','Imaginea PostgreSQL existentă trebuie să conțină extensia; postgres:16 standard nu este probă că o include. E5 prevede imagine compatibilă, backup și test de migrare pe același major și același serviciu, fără bază paralelă.')],[4.1,13.4])
p('Rollbackul temei nu inversează migrările și nu restaurează baza peste comenzi noi. Extensiile au comutatoare separate și migrări additive compatibile cu marketplace_pro. E0 trebuie să rămână accesibil și după revenire. Dezactivarea unei extensii păstrează declarațiile, configurațiile plătite și registrul de puncte pentru procesare umană.')
p('Modernizarea HA/PITR, hardware AI și permanența 24/7 sunt costuri distincte. Deficitul de infrastructură nu se ascunde în CSS/React; înainte de lansare există fie dovada țintelor, fie acceptarea explicită a unui nivel inferior. Nu s-au pornit, oprit sau recreat containere în această analiză.')
''')
para('Directiva de audit Flask', 'Nu există un cache al unei aplicații frontend separate. E0–E7 folosesc mecanismul comun; actualizarea vectorilor E5 are jurnal și reindexare versionată, iar produsele retrase sunt filtrate la citire. Deficitul de consistență blochează funcția afectată. Cacheul AI nu include comenzi, tokenuri, date personale sau prețuri private.')
s=s.replace('Nu se declară un webhook nou ca prerechizită implicită.','Nu se introduce un al doilea strat comercial de cache.')
s=s.replace('Remedierea poate folosi mecanismul comun de evenimente/outbox dacă există; orice schimbare la acesta este proiect separat, cu aprobare și estimare.','E0–E7 pot extinde mecanismul comun în limitele pachetului estimat; alte schimbări sunt cotate distinct.')
s=s.replace('Încărcare separată prin Suspense sau cerere dedicată.','Insule React încărcate la interacțiune, în limita E4/E5.')
para('ADR03 verifică invalidarea', 'ADR03 verifică invalidarea și consistența cacheului existent și a datelor derivate E5. Înainte de plată se folosește validarea actuală a backendului; schimbarea totalului cere reconfirmare. Datele inițiale sunt serializate sigur în pagină, cu aceeași limbă și monedă pentru Jinja și React. Fiecare insulă deține propria zonă DOM; storefront.js/shop.js nu atașează aceiași handleri în acea zonă. Testele verifică lipsa evenimentelor duble și a diferențelor de hidratare.')
para('Playwright verifică șase trasee', 'Regresia temei verifică șase trasee: căutare text–produs–coș; categorie–filtru existent/E1; serie–completare; cadou–ambalaj–mesaj; checkout vizitator–Stripe; Pro–firmă–cerere de ofertă. E4, E5, E6 și E7 au trasee proprii după activare. /api/orders/validate acoperă preț schimbat și stoc zero, după inspectarea lanțului și în mediu izolat. Operațiile de retragere/retur/anulare cu efect sunt probate de om, nu executate automat de AI.')
s=s.replace('JS inițial comprimat','JS inițial comprimat').replace('≤170 KB transferat.','≤170 KB transferat. Componentele React ale produsului au separat ≤120 KB.')
section("page('11 Analiza diferențelor", "page('12 Checkout",r'''
page('11 Capabilități verificate în cod')
p('Citirea statică din 21 octombrie 2026 stabilește ce există în copia U:/cesiro.com. „Există în cod” nu certifică activarea în producție. D01 rămâne pentru date, configurație, probe funcționale și legătura cu imaginea instalată. Dovezile au hashuri în I6.')
table(['Capabilitate','Stare documentată','Dovadă și tratament'],[
('Catalog și filtre','Există în cod','factory.py: /api/catalog/products; parametrii actuali sunt în §5. E1 adaugă serie și persoane.'),
('Validare checkout','Există în cod','POST /api/orders/validate, descris fără comandă/cont/e-mail. Proba rămâne izolată.'),
('Coș cont firme favorite','Există în cod','storefront.py: /api/cart, /api/account/*, /companies, /favorites. Tema le reutilizează.'),
('Cadou pe comandă','Există în cod','gift.py, migrația 0079; ambalaj și mesaj, maximum 300 caractere; fără taxă de ambalaj în versiunea citită.'),
('Stripe','Există în cod','/api/payments/stripe/session și webhook; payload cu success_url/cancel_url și redirect către URL-ul sesiunii, indicând checkout găzduit.'),
('Livrare și lockere','Există în cod','/api/shipping/lockers și /api/checkout/shipping-options; activarea curierilor se probează în D01.'),
('Status comandă','Există în cod','GET /api/orders/<nr>/status. Nu ține locul autorizării pentru factură, adresă sau cereri E2.'),
('Retur din cont','Rută existentă, UI oprit implicit','account.html: returns_enabled default false; create_return cere cont și motiv de minimum 5 caractere. E0 remediază distinct.'),
('Retragere fără cont','Neidentificată în codul citit','Audit A3 confirmă lipsa; E0 este planificat urgent, pe tema actuală.'),
('Teme și calendar','Există în cod','theme_registry, manifest.parent, theme_schedule, theme_preview și validator tenant; se reutilizează.')],[4.1,4.3,9.1],small=9.5)
p('Returul existent nu se redenumește „retragere” păstrând obligația unui cont sau motiv. E0 are flux propriu pentru declarația de retragere, cu păstrarea operațiilor logistice și financiare umane. Existența unei rute nu este permisiune de a o apela în această analiză.')
page('11.1 Extensii și limite de reutilizare')
table(['Capabilitate','Fapt din surse','Decizia V4'],[
('Asistent public','Asistent OWNER numai în admin, POST /assistant/chat; acces la unelte administrative','E4 reutilizează clientul de inferență și cod sigur, cu serviciu public de citire separat în aceeași aplicație.'),
('Vectori și căutare foto','Nu s-a identificat pgvector/embeddings în codul aplicației citite','E5 adaugă vectorii derivați și interogarea în baza actuală.'),
('Personalizare','Lipsește din inventarul static al auditului','E6 adaugă configurare, preț validat, fișier și pilot.'),
('Club și puncte','Lipsește din inventarul static al auditului','E7 adaugă registru idempotent și interfață.'),
('CUI → firmă','Lipsește din CESIRO; logică ANAF găsită în U:/acc-florin/app/main.py:1206','E3 reutilizează logica; nu copiază sesiuni, baze sau credențiale.'),
('Liste de eveniment și loturi','Lipsesc din inventarul static al auditului','Ulterior; nu intră în E0–E7.'),
('Preț contractual Pro','Nu este demonstrat în contractul public inspectat','Ulterior; preț public, firme pe cont și cerere de ofertă în baza actuală.'),
('EVA documente și fiscal','Importul documentelor de curier nu demonstrează e-Factura','Conectorul fiscal al CESIRO se confirmă separat; E3 CUI nu rezolvă transmiterea fiscală.')],[4.1,6.1,7.3],small=9.5)
h('Contractele extensiilor')
p('Registrul R00 documentează pentru fiecare E# ruta propusă, metoda, tenantul, câmpurile, autorizarea, CSRF, rate limit, erorile, efectele și versiunea contractului. OpenAPI descrie numai operațiile reale din motor; nu se construiește un gateway, BFF sau sistem de autentificare paralel. Ruta admin a asistentului nu este expusă prin proxy public.')
p('Numele de rută ale extensiilor se fixează în S1–4 după convențiile aplicației. E1 extinde /api/catalog/products; E0 are operații de inițiere și confirmare a declarației; E2 de emitere/redeemare a grantului de comandă; E3 de citire a datelor firmei; E4/E5 de interogare; E6 de configurare și validare; E7 de citire a soldului și operații comerciale autorizate. Contractele descriu inclusiv comportamentul cu extensia oprită.')
p('Migrările sunt additive și reversibile operațional prin dezactivare, nu prin ștergerea datelor. Oprirea E6 păstrează configurațiile deja plătite; oprirea E7 păstrează soldurile; E0 păstrează declarațiile și canalul legal. Testele de regresie rulează și pe marketplace_pro pentru toate modificările în motor.')
''')
para('Checkoutul are o singură pagină', 'Checkoutul local grupează contactul, livrarea și sumarul într-o pagină cu progres clar; clientul poate plăti fără cont. Codul Stripe citit creează o sesiune și folosește URL-ul ei, indicând plată pe pagina găzduită de Stripe. Tema nu promite că plata rămâne în aceeași pagină. D01 confirmă modul activ și walleturile eligibile; Apple Pay/Google Pay apar numai dacă integrarea și contul Stripe le permit. Schimbarea către un element încorporat este decizie și cost distinct.')
section("page('12.1 Retragere", "page('13 Performanță",r'''
page('12.1 E0 retragere și E2 acces fără cont')
p('E0 și E2 sunt planificate în S1–3 pe tema actuală, apoi preluate de tema nouă. Codul citit nu oferă funcția publică de retragere, iar returul din cont este oprit implicit. Este o remediere urgentă a platformei actuale. Data europeană de aplicare a măsurilor din Directiva 2023/2673 este 19 iunie 2026; juridicul confirmă transpunerea națională și condițiile piețelor. Nu se declară conformă producția pe baza unei lecturi de cod. [L10, L10b]')
h('E0 Declarația de retragere')
p('Funcția este permanent ușor de găsit în perioada relevantă, fără cont obligatoriu, fără motiv și fără fotografie. Permite nume, identificarea contractului și adresa electronică pentru confirmare, cu date minime proporționale. Clientul confirmă explicit declarația; înregistrarea nu așteaptă aprobarea operatorului. Dovada cu conținut și dată/oră se transmite fără întârziere pe suport durabil și este disponibilă imediat în interfață.')
p('Înregistrarea declarației este separată de anulare, autorizarea logistică a returului și rambursare. O dispută privind excepția pentru personalizare este preluată de om; nu se refuză primirea declarației printr-un filtru AI. E0 reface și vizibilitatea returului din cont, după verificarea juridică și operațională a fluxului actual, fără a impune motiv retragerii legale.')
p('Cele 12 scenarii de recepție acoperă client fără cont, client cu cont, limbă diferită, retragere parțială, comandă mixtă, dublu click, reîncercare, e-mail indisponibil, link expirat, date minime incorecte, produs personalizat contestat și dovada cu dată/oră. Operatorul uman conduce cazurile cu efect comercial; AI nu apelează rute de anulare/retur/rambursare, nici în teste. Dublarea cererii nu dublează efectele, iar eroarea de e-mail nu pierde declarația.')
h('E2 Grant securizat pentru o comandă')
p('E2 oferă acces limitat la o singură comandă și un tenant, fără crearea unui cont. Grantul este opac, generat criptografic, cu expirare și revocare, păstrat ca hash; nu este derivat din numărul comenzii. Propunere de pornire: ≥256 biți de entropie, link valabil 30 minute, utilizare unică la confirmarea explicită; o nouă emitere nu dezvăluie existența unei comenzi unui solicitant neautorizat.')
p('GET-ul linkului nu consumă grantul și nu schimbă stări, pentru a tolera scanerele de e-mail; confirmarea folosește POST cu protecția existentă și stabilește un acces limitat. Tokenul nu intră în analytics, referer, jurnale sau cache. Reemiterea verifică proporțional posesia canalului de contact. Se testează expirare, replay, enumerare, schimbare tenant/comandă și revocare. Formularul E0 rămâne utilizabil independent de livrarea linkului E2.')
h('Fiscalitate și lansare')
p('E3 verifică date de firmă, nu transmite e-Factura. Platforma existentă trebuie să demonstreze separat emiterea și transmiterea fiscală aplicabilă, statusul, reîncercările și deduplicarea. Deficitul fiscal are responsabil și termen, fără presupunerea că este finanțat în E3. R09 cere remedierea E0 înainte de tema nouă; dreptul de retragere nu este un simplu segment comercial care poate fi ascuns. Decizia privind operarea curentă revine conducerii și juridicului.')
''')
(O/'build_v4.py').write_text(s,encoding='utf-8')
print('V4 prima parte pregătită')
