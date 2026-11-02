from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path

OUT=Path(__file__).parent
doc=Document()
sec=doc.sections[0]
sec.page_width=Cm(21); sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.65);sec.bottom_margin=Cm(1.65);sec.left_margin=Cm(1.8);sec.right_margin=Cm(1.8)
normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(10.5)
normal.paragraph_format.space_after=Pt(6);normal.paragraph_format.line_spacing=1.06
for style in doc.styles:
    for border in list(style.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)
doc.styles['Subtitle'].font.color.rgb=RGBColor.from_string('555555')
doc.styles['Subtitle'].font.italic=False
for name,size in [('Title',28),('Heading 1',20),('Heading 2',12)]:
    st=doc.styles[name];st.font.name='Calibri';st.font.size=Pt(size)
    st.font.color.rgb=RGBColor.from_string('000000' if name=='Title' else '713C2D')
    st.paragraph_format.space_before=Pt(9);st.paragraph_format.space_after=Pt(8)
    st.paragraph_format.keep_with_next=True
doc.core_properties.title='Proiect pentru redesignul și dezvoltarea platformei CESIRO'
doc.core_properties.subject='Specificație de proiect pentru design și arhitectură React și Python'
doc.core_properties.author=''
doc.core_properties.keywords='CESIRO, proiect, design, React, JavaScript, Python, catalog, ecommerce'
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=footer.add_run('CESIRO  ·  Proiect 1.0  ·  ');r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string('666666')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)

def p(text,style=None):
    return doc.add_paragraph(text,style)
def h(text):doc.add_heading(text,2)
def b(text):p(text,'List Bullet')
def page(title):doc.add_page_break();doc.add_heading(title,1)
def table(headers,rows,widths=None):
    t=doc.add_table(rows=1,cols=len(headers));t.style='Table Grid';t.autofit=False
    if widths:
        for c,w in zip(t.columns,widths):c.width=Cm(w)
    for c,x in zip(t.rows[0].cells,headers):c.text=x
    for row in rows:
        for c,x in zip(t.add_row().cells,row):c.text=str(x)
    for ri,row in enumerate(t.rows):
        props=row._tr.get_or_add_trPr();props.append(OxmlElement('w:cantSplit'))
        if ri==0:props.append(OxmlElement('w:tblHeader'))
        for ci,c in enumerate(row.cells):
            if widths:c.width=Cm(widths[ci])
            if ri==0:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'F0E7DF');c._tc.get_or_add_tcPr().append(shade)
            for para in c.paragraphs:
                para.paragraph_format.space_after=Pt(4);para.paragraph_format.space_before=Pt(3)
                para.paragraph_format.line_spacing=1.02
                for run in para.runs:run.font.size=Pt(9.4);run.bold=(ri==0)
    p('')
def link(label,url):
    para=doc.add_paragraph();rel=para.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
    hl=OxmlElement('w:hyperlink');hl.set(qn('r:id'),rel);run=OxmlElement('w:r');props=OxmlElement('w:rPr');col=OxmlElement('w:color');col.set(qn('w:val'),'713C2D');props.append(col);run.append(props);txt=OxmlElement('w:t');txt.text=label;run.append(txt);hl.append(run);para._p.append(hl)

p('Proiect pentru redesignul și dezvoltarea platformei CESIRO','Title')
p('Experiență de cumpărare după produse, utilizări și ocazii','Subtitle')
p('Frontend JavaScript și React  |  Backend Python')
p('Versiunea 1.0  •  21 octombrie 2026')
h('Scopul proiectului')
p('Proiectul propune o nouă experiență comercială pentru cesiro.com, inspirată de accesul rapid la catalog oferit de Trendyol și adaptată identității CESIRO. Produsele vor putea fi descoperite atât după tip, cât și după momentul de utilizare, persoana care primește cadoul, stil, culoare și buget. Întregul catalog existent rămâne în domeniul proiectului.')
p('Rezultatul urmărit este o platformă cu prezentare coerentă, date verificabile și parcurs de cumpărare măsurabil. Ceramica și masa vor conduce comunicarea de brand, iar celelalte familii de produse vor avea trasee proprii, accesibile din catalog și căutare.')
h('Natura documentului')
p('Documentul este o descriere de proiect și o bază pentru estimare, contractare și recepție. Definește obiective, activități viitoare, livrabile, arhitectură și criterii de acceptare. Redactarea sa nu include implementarea, publicarea sau modificarea site-ului CESIRO. Observațiile sunt datate; indicatorii propuși reprezintă ținte, nu rezultate deja obținute.')
h('Rezultatele principale propuse')
b('Inventar reconciliat al datelor și trasabilitate pentru 100% dintre înregistrările furnizate proiectului.')
b('16 tipuri de pagini publice proiectate pentru mobil, tabletă și desktop, plus 5 ecrane administrative.')
b('12 colecții comerciale, un selector de cadouri și minimum 6 compoziții de masă asociate produselor reale.')
b('Frontend React, servicii comerciale Python și integrarea documentată a catalogului, plăților, livrării și comenzilor.')
b('Recepție prin teste funcționale, verificarea datelor, accesibilitate, performanță, migrare SEO și măsurarea rezultatelor comerciale.')
h('Orizont de planificare')
p('Estimare de referință: 14–18 săptămâni de execuție după clarificarea integrărilor și accesului la date, urmate de 90 de zile de măsurare comercială. Efortul de remediere editorială a întregului catalog se dimensionează separat după auditul complet.')

page('1 Date publice disponibile și dimensiunea catalogului')
p('Constatările provin din citirea paginii principale, a două pagini de produs, a patru pagini informative, a robots.txt și a sitemap.xml. Nu reprezintă o verificare individuală a tuturor produselor și nu confirmă infrastructura internă. [S1–S8]')
table(['Indicator public observat','Valoare și interpretare'],[
('Adrese în sitemap','32.868 URL-uri distincte; sunt adrese publicate în sitemap, nu pagini testate individual.'),
('Adrese de produs','31.674 URL-uri de produs; 5.279 pentru fiecare dintre cele 6 limbi. Numărul de SKU-uri unice trebuie reconciliat cu sursa de catalog.'),
('Limbi','RO, EN, DE, HU, BG, EL. Prezența unei adrese nu certifică traducerea integrală.'),
('Structură publică','60 adrese informative și 1.134 alte adrese, inclusiv pagina principală și adrese cu parametri de categorie.'),
('Date pentru automatizare','JSON-LD și un bloc JSON public de produs; sitemap; URL-uri de imagini; canonical și alternate/hreflang în eșantion.'),
],[4.7,12.7])
p('Numărătorile sitemapului au fost calculate din răspunsul public primit la 21 octombrie 2026. URL-urile pe limbi și numărătorile de categorie nu se însumează pentru a obține un total de produse unice. [S2]')
h('Familii de catalog afișate în meniul principal')
table(['Categorie','Număr afișat','Categorie','Număr afișat'],[
('Veselă și seturi de masă','2.035','Produse de curățenie','1.308'),
('Căni, cești și pahare','677','Boluri și salatiere','539'),
('Decorațiuni și vaze','234','Accesorii de servire','120'),
('Vase de gătit și copt','115','Tacâmuri și ustensile','101'),
('Promoții și pachete','67','Grădină și ghivece','60'),
('Recipiente și depozitare','43','Electrocasnice și sezoniere','44'),
('Fără categorie','47','Total unic de produse','De confirmat'),
],[6.1,2.0,7.1,2.2])
p('Acestea sunt valori afișate de site, fără confirmarea stocului fizic sau a regulilor de numărare. Proiectul tratează fiecare familie și păstrează identificatorii vechi pentru reconciliere. [S1]')

page('2 Inventarul câmpurilor și utilizarea lor')
p('În cele două produse verificate, datele sunt disponibile în pagina vizibilă și în JSON public. Contractul de date trebuie să păstreze separat valoarea originală, valoarea normalizată și starea validării. Existența unui câmp în eșantion nu confirmă completarea lui în tot catalogul. [S3, S4]')
table(['Date observate','Utilizare în noua platformă','Tratament'],[
('ID produs, SKU, EAN, slug','Identitate, căutare exactă, relații, redirecționări','ID intern stabil; SKU/EAN ca șiruri; verificare duplicate și cifră de control EAN.'),
('Nume, descriere scurtă și lungă','Carduri, pagini de produs, căutare','Se păstrează sursa; se corectează contradicțiile înaintea publicării.'),
('Categorii, ID-uri de categorii, tags','Navigare, filtre, colecții','Mapare între taxonomia veche și nouă; tags sunt goale în eșantion.'),
('Atribute, brand, culoare, material, capacitate, bucăți','Filtre și recomandări explicabile','Unități normalizate; materialele multiple și seturile se modelează explicit.'),
('Preț curent, preț regulat, reducere, monedă','Listare, coș, promoții','Sume exacte; istoricul prețurilor se preia separat, nu se deduce din prețul curent.'),
('Stoc, disponibilitate, manage_stock','Filtrare și verificare comandă','Stocul public este un instantaneu; confirmare în sursa operațională.'),
('Imagini, ordine, MIME, metadate media','Galerie, imagini responsive, accesibilitate','Păstrarea originalelor; completarea dimensiunilor și textelor alternative lipsă.'),
('Titlu SEO, descriere SEO, canonical, hreflang, JSON-LD','Continuitate SEO și indexare','Separarea metadatelor sursă de cele publicate; o singură versiune validată.'),
('Recenzii și număr de recenzii','Dovadă socială','În cele două exemple sunt 0 recenzii; nu se generează ratinguri artificiale.'),
('Limbi, cursuri valutare și data cursului','Localizare și afișare monetară','Separarea monedei afișate de moneda de plată; reguli confirmate comercial.'),
],[4.1,5.0,8.3])
h('Date informative reutilizabile')
p('Paginile Despre CESIRO, contact, întrebări frecvente, retur, politici și Mystery Box sunt surse de conținut. Se inventariază toate cele 10 tipuri de pagini informative din sitemap și se verifică versiunea aprobată pentru fiecare limbă. [S2, S5–S8]')
p('Datele despre comenzi, clienți, costuri, marje, abandon, trafic, contracte și stoc fizic sunt dependențe interne. Nu sunt considerate disponibile din consultarea publică.')

page('3 Calitatea datelor și reguli de reutilizare integrală')
h('Neconcordanțe confirmate în eșantion')
table(['Observație','Consecință pentru proiect'],[
('Setul de 9 piese este descris în unele câmpuri ca o singură cană. [S4]','Se verifică lista componentelor, cantitățile și numărul real de persoane; nu se construiesc pachete din acest text fără validare.'),
('La ceașcă, JSON-LD marchează anumite dimensiuni, greutatea și materialul drept estimate. [S3]','Estimările rămân etichetate; nu devin specificații certe, criterii de transport sau promisiuni de compatibilitate.'),
('În metadatele media ale setului există câmpuri alt, width și height necompletate. [S4]','Se verifică fișierul real și se completează metadatele necesare; lipsa lor în JSON nu dovedește lipsa textului alternativ din HTML.'),
('Recomandările și povestea ceramicii includ și alte materiale. [S1]','Colecțiile vor folosi reguli de eligibilitate pe material, tip și utilizare, plus verificare editorială.'),
('Meniul include Fără categorie și încadrări neadecvate. [S1]','Produsele sunt remapate într-o categorie validă; cele neclarificate rămân în inventarul de remediere.'),
],[8.3,9.1])
h('Ce înseamnă folosirea completă a datelor')
p('Fiecare înregistrare primită este păstrată și primește o destinație documentată: publicare, îmbogățire, arhivare justificată sau validare necesară. Niciun câmp necunoscut nu este eliminat tacit. Datele istorice și cele nevalidate se păstrează în arhiva de import, fără a fi prezentate drept informații comerciale certe.')
b('Registrele de import consemnează sursa, data, identificatorul, valoarea originală, regula de transformare și erorile.')
b('O valoare goală rămâne necunoscută. Nu devine automat zero, fals, fără stoc sau compatibil.')
b('Capacitatea unei căni din set se păstrează la componentă; nu se interpretează ca volum al întregului set.')
b('Compatibilitatea cu mașina de spălat, microunde sau cuptorul, proveniența și certificările se publică numai dacă există confirmare pentru produsul respectiv.')
b('Asocierile de marketing pot porni de la text, dar sunt distincte de specificațiile tehnice și pot fi aprobate sau respinse de editor.')
h('Criterii de recepție pentru date')
p('100% dintre înregistrările sursă sunt contabilizate; 100% dintre câmpuri sunt mapate sau arhivate; 0 duplicate de identitate nerezolvate în catalogul publicat; 100% dintre produsele cumpărabile au identitate, preț, monedă, disponibilitate și categorie valide. Lipsurile necritice au responsabil și termen de remediere.')

page('4 Obiectivele proiectului și rezultatele măsurabile')
p('Criteriile de livrare se verifică înaintea lansării. Obiectivele comerciale se evaluează după lansare și depind de trafic, stoc, prețuri și campanii. Valorile comerciale de mai jos sunt ipoteze de lucru ce se calibrează după stabilirea referinței inițiale.')
table(['ID și obiectiv','Activități principale','Rezultat și verificare'],[
('O1 Date complete și coerente','Inventariere, mapare, deduplicare, validare','100% din sursa agreată reconciliată; raport per câmp și per produs.'),
('O2 Găsirea mai ușoară a produselor','Taxonomie, căutare, filtre, teste cu utilizatori','Minimum 90% sarcini de găsire finalizate fără ajutor; timp median ≤60 secunde în testul final.'),
('O3 Design consistent și accesibil','Sistem vizual, prototipuri, verificare mobil și tastatură','48 ecrane publice de bază, 5 administrative, minimum 30 componente; audit WCAG 2.2 AA în domeniul agreat.'),
('O4 Cumpărare după context','12 colecții, selector de cadouri, 6 scene de masă','100% produse eligibile verificate; fără colecții goale promovate; rezultate explicabile.'),
('O5 Comerț corect și integrări stabile','Coș, checkout, plăți, stoc, livrare, reconciliere','100% scenarii critice trecute; 0 comenzi sau încasări duplicate în testele de repetare.'),
('O6 Viteză și continuitate','Optimizare React, cache, observabilitate, backup','Țintele de performanță din secțiunea 13; restaurare și revenire la versiunea anterioară demonstrate.'),
('O7 Continuitate SEO și localizare','Mapare URL-uri, metadate, sitemap, 6 limbi','100% URL-uri inventariate au destinație sau decizie explicită; 0 redirecționări circulare.'),
('O8 Îmbunătățire comercială','Măsurare funnel, experimente și optimizare','Ținte la 90 de zile: +15% conversie relativă, +10% valoare medie, −15% abandon checkout relativ.'),
],[3.8,5.1,8.5])
p('Testele de utilizare vor avea două runde a câte minimum 8 participanți și 5 sarcini per participant. Pragul de 90% în runda finală înseamnă cel puțin 36 de reușite din 40 de sarcini; este un criteriu practic de recepție, nu o estimare reprezentativă a întregii populații.')

page('5 Organizarea catalogului și direcția comercială')
h('Arhitectura informației')
p('Meniul principal propus: Toate produsele, Zi de zi, Mese cu cei dragi, Cadouri, Colecții și culori, Oferte. Zona Toate produsele conține toate familiile existente, reorganizate coerent. Pentru casă și HoReCa au pagini de acces dedicate și sunt prezente în căutare; nu sunt ascunse prin repoziționarea ceramicii.')
p('Categoriile descriu ce este produsul. Colecțiile descriu de ce și în ce context poate fi cumpărat. Relația dintre produs și colecție este multiplă; un produs păstrează aceeași identitate, același stoc și aceeași pagină, chiar dacă apare în mai multe selecții.')
table(['Colecție propusă','Regulă editorială și de selecție'],[
('Veselă de zi cu zi','Piese pentru mese uzuale; verificarea informațiilor de utilizare și întreținere.'),
('Cafea în doi','Cești sau căni compatibile, cu cantități și capacități clare.'),
('Micul dejun împreună','Boluri, căni și farfurii de desert; asociere pe stil și colecție.'),
('Vin musafirii','Platouri, boluri de servire și seturi potrivite grupului selectat.'),
('Prima noastră casă','Pachete pentru 2, 4 sau 6 persoane, calculate din componente confirmate.'),
('Cadouri pentru el și Cadouri pentru ea','Două intrări; selecția continuă după pasiuni, stil și buget, fără atribuirea automată a culorilor după gen.'),
('Cadou pentru gazdă','Selecție de dimensiuni și prețuri potrivite unui cadou de vizită.'),
('Masa de Crăciun, Paște, Toamnă, Grădină','Patru colecții sezoniere, cu perioadă de publicare și selecție validată.'),
],[6.3,11.1])
p('Rezultat inițial: 8 colecții permanente și 4 sezoniere. Pentru o colecție promovată se propun 8–24 produse eligibile, cu minimum 6 cumpărabile. Dacă pragul nu este îndeplinit, colecția nu primește promovare; produsele rămân accesibile individual.')
h('Filtre potrivite produsului')
p('Filtre comune: preț, disponibilitate, brand și culoare. Filtre specifice: material, capacitate, diametru, număr de piese, număr de persoane, colecție și utilizare. Pentru curățenie, depozitare sau grădină se folosesc alte atribute relevante; nu se impun câmpuri de veselă întregului catalog.')

page('6 Designul experienței și paginile necesare')
p('Direcția vizuală folosește spațiu generos, tonuri calde, accent teracotă, fotografie fidelă culorii și contrast bun. Identitatea CESIRO rămâne distinctă. Din referința Trendyol se preiau accesul rapid la căutare, explorarea pe categorii și scurtăturile comerciale. [S9]')
table(['Tipuri de pagini','Cerințe de design'],[
('1 Pagina principală','Mesaj principal; momente de utilizare; selecții relevante; scene de masă; beneficii și poveste validate.'),
('2 Catalog și categorie / 3 Colecție tematică','Filtre relevante, sortare, număr de rezultate, filtre active, revenire la poziția din listă.'),
('4 Rezultate de căutare','Căutare după cuvinte, SKU/EAN și intenții; sugestii; lipsă rezultate cu alternative.'),
('5 Produs','Galerie, preț, variante, disponibilitate, compoziție, specificații, livrare, întreținere și recomandări.'),
('6 Selector de cadouri / 7 Rezultate cadouri','Persoană, ocazie, buget, preferințe; motivul recomandării și opțiunea de modificare.'),
('8 Masă completă','Produse din scenă, cantități editabile, total actualizat, variante și lipsuri de stoc.'),
('9 Favorite / 10 Coș','Persistență; preț și stoc actualizate; editare cantități; explicarea oricărei modificări.'),
('11 Checkout / 12 Confirmare comandă','Date, livrare, plată, sumar; validări locale; confirmare numai după răspunsul backendului.'),
('13 Autentificare / 14 Cont și comenzi','Cont opțional la cumpărare, recuperare acces, adrese, istoric și detaliu comandă.'),
('15 Pagini informative / 16 Pentru casă și HoReCa','Șabloane pentru conținut și politici; acces adaptat produselor secundare și profesionale.'),
],[6.5,10.9])
h('Livrabile și verificare UX')
p('16 tipuri × 3 dimensiuni de referință = 48 ecrane publice: 390, 768 și 1440 px. Alte 5 ecrane acoperă administrarea. Prototipul include 6 trasee: cumpărare directă, cadou, masă completă, completare set, căutare fără rezultate și comandă cu indisponibilitate apărută în coș.')
p('Se documentează stările normală, încărcare, eroare, lipsă rezultate, stoc insuficient și succes, acolo unde se aplică. Comportamentul responsive se verifică între 320 și 1920 px; ecranele de referință nu înlocuiesc această verificare.')

page('7 Sistemul de design și producția de conținut')
h('Sistemul de design')
p('Se livrează o bibliotecă de minimum 30 de componente reutilizabile, cu reguli pentru culori, tipografie, spațiere, iconografie, fotografie, formulare și feedback. Exemple: antet, meniu, căutare, card produs, preț, selector cantitate, selector variantă, galerie, filtre, dialog, notificare, sumar coș și pași de checkout.')
p('Fiecare componentă primește stări, comportament la tastatură, reguli responsive și conținut exemplificativ. Biblioteca vizuală și cea React vor avea aceeași nomenclatură, pentru a reduce diferențele dintre prototip și produsul final.')
h('Fotografie și prezentare')
b('Toate imaginile existente se inventariază după produs, rol, rezoluție, format și drept de utilizare. Originalele se păstrează; derivatele se regenerează controlat.')
b('Minimum 6 scene de masă pentru lansare, fiecare asociată explicit cu SKU-urile vizibile. Fotografia nouă se planifică numai unde materialele existente nu sunt suficiente.')
b('Minimum 12 imagini de colecție și 3 concepte de campanie. Imaginile de produs trebuie să reprezinte varianta cumpărabilă; recuzita care nu se vinde se identifică clar.')
b('Nu se schimbă digital culoarea, decorul sau forma astfel încât imaginea să promită alt produs. Nu se folosesc fotografii generice pentru a sugera caracteristici tehnice neverificate.')
h('Conținut și localizare')
p('Se definește un ghid editorial pentru titluri, beneficii, specificații, unități, compoziția seturilor și mesaje de eroare. Fiecare descriere comercială este legată de produs și de datele confirmate. Povestea fabricii și afirmațiile despre origine sunt aprobate de responsabilul CESIRO.')
p('Pentru toate cele 6 limbi se livrează dicționarul interfeței, reguli de formatare, texte operaționale și stări de traducere. Textele de catalog existente se păstrează integral; publicarea lor se face potrivit nivelului de validare. Traducerea și revizia umană completă a zecilor de mii de pagini se estimează după inventarul real, distinct de dezvoltarea temei.')
h('Criterii de acceptare')
p('100% componente documentate; 0 texte tăiate sau elemente suprapuse în scenariile verificate; 100% imagini informative au text alternativ relevant; toate acțiunile principale sunt accesibile cu tastatura. Revizia include contrast, focus vizibil, etichete, mesaje de eroare și zoom. Auditul urmărește criteriile aplicabile WCAG 2.2 AA. [S12]')

page('8 Funcționalități comerciale și idei de marketing')
table(['Funcționalitate','Comportament prevăzut','Rezultat verificabil'],[
('Cumpără masa din fotografie','Fiecare scenă indică produsele și cantitățile. Clientul poate elimina o piesă sau schimba varianta.','Minimum 6 scene; total calculat în Python; toate SKU-urile se verifică înainte de adăugarea în coș.'),
('Găsește un cadou','Maximum 4 pași: persoană, ocazie, buget, preferințe. Rezultatele explică potrivirea.','3–12 rezultate eligibile când există suficiente produse; explicație și ajustare filtre când nu există.'),
('Completează setul','Recomandă piese din aceeași colecție și decor, pe baza relațiilor validate.','Minimum 20 grupuri de compatibilitate validate sau toate grupurile existente, dacă sunt mai puține.'),
('Prima noastră casă','Seturi și combinații pentru 2, 4 sau 6 persoane.','Minimum 3 configurații complete, dacă datele și stocul permit; fără deducție simplă piese ÷ persoane.'),
('Masa în culorile tale','Combinații editoriale care țin cont de formă, dimensiune, finisaj și culoare.','Minimum 6 combinații verificate, cu motivul recomandării.'),
('Campanii sezoniere','Publicare programată, produse eligibile și mesaje locale.','4 colecții sezoniere și 3 campanii pregătite; nicio reducere sau raritate inventată.'),
],[3.9,6.6,6.9])
h('Regulile motorului de recomandare')
p('Prima versiune folosește reguli explicabile: tip, utilizare, colecție, material confirmat, culoare, buget și disponibilitate. Produsele indisponibile nu sunt recomandate ca achiziție imediată. Scorul comercial poate folosi vânzări și marjă numai după obținerea și validarea acelor date. Un model de inteligență artificială nu este necesar pentru lansare.')
p('Colecțiile pentru el sau pentru ea sunt puncte de acces în selecție. Preferințele declarate de client au prioritate față de asocieri generale. În prima etapă nu se deduc profiluri sensibile și nu se cere autentificare pentru a primi recomandări.')
h('Funcționalități condiționate de operațiuni')
p('Ambalarea de cadou, mesajele tipărite, livrarea la o dată aleasă, notificările de revenire în stoc, fidelizarea și extinderea Mystery Box se activează numai dacă există proces operațional, costuri și date suficiente. Ele se proiectează ca extensii; nu se prezintă drept servicii deja oferite sau garantate.')

page('9 Arhitectura tehnică și responsabilitățile sistemelor')
h('Structura propusă')
p('Interfață React în JavaScript → servicii HTTP ale backendului Python → PostgreSQL și adaptoare pentru sistemele comerciale. Imaginile sunt livrate prin stocare de obiecte și CDN. Redis susține cache-ul și sarcinile de fundal; un worker Python procesează importurile, notificările și reconcilierile.')
table(['Strat','Alegere propusă','Responsabilitate'],[
('Frontend','JavaScript, React și Next.js','Componente, rutare, pagini randate pe server, metadate și interacțiuni.'),
('Backend','Python, Django și Django REST Framework','Catalog, reguli comerciale, coș, comenzi, permisiuni, administrare și contract API.'),
('Persistență','PostgreSQL','Produse, relații, colecții, conținut, comenzi și audit; tranzacții pentru operațiuni comerciale.'),
('Cache și fundal','Redis și worker Python, de exemplu Celery','Cache invalidabil, importuri și sarcini reluabile; baza de date rămâne autoritatea durabilă.'),
('Căutare','PostgreSQL cu indexare și normalizare','Căutare exactă și textuală, sinonime și filtre; motor separat numai dacă testele justifică.'),
('Media și operare','Stocare obiecte, CDN, jurnale și monitorizare','Imagini responsive, versiuni, erori, latențe, disponibilitate și alerte.'),
],[3.0,6.1,8.3])
p('Next.js este propus pentru randarea React pe server și funcțiile de prezentare. Acest strat poate necesita un proces Node.js de randare; logica de business, autorizarea și operațiunile comerciale rămân în Python. Django oferă un punct de pornire pentru administrare și autentificare. Versiunile se aleg dintre cele suportate la începerea execuției. [S10, S11]')
h('Delimitarea față de sistemul actual')
p('Tehnologia și API-urile interne actuale nu sunt confirmate prin auditul public. Referințele de import observate în date nu demonstrează că magazinul rulează pe o anumită platformă. Prima etapă va decide dacă backendul Python existent se extinde sau se introduce un serviciu Python nou, cu adaptor către sursa actuală.')
p('Pentru fiecare domeniu se desemnează o singură sursă de adevăr: catalog, preț, stoc, comenzi, clienți și politici. În tranziție, serviciul Python poate orchestra sistemul existent. Migrarea proprietății datelor și eventualele scrieri în sistemul vechi sunt activități viitoare, documentate separat.')
h('Medii și livrare controlată')
p('Se prevăd medii separate de dezvoltare, test și producție, cu configurații și secrete distincte. Publicarea trece prin verificări automate, teste de contract și validare în mediul de test, protejat de autentificare și exclus din indexare. Migrarea bazei de date este versionată și verificată pentru compatibilitate. Funcțiile comerciale noi pot fi activate gradual; revenirea nu trebuie să piardă comenzile primite între versiuni.')

page('10 Specificația frontendului React')
h('Randare și navigare')
p('Paginile publice importante livrează conținut HTML util înaintea executării JavaScript. Interacțiunile de filtrare, galerie, favorite, cadouri și coș sunt componente React. Starea filtrelor, sortarea, pagina și limba se reflectă în URL pentru distribuire și revenire. Rezultatele paginate au legături navigabile; încărcarea suplimentară nu blochează accesul motoarelor de căutare.')
h('Componente și stare')
b('Biblioteca de componente reutilizează regulile de design, fără dublarea formulelor comerciale în interfață.')
b('Datele de server sunt separate de starea locală a interfeței. Cache-ul ține cont de limbă, monedă, client și context de preț.')
b('Coșul afișează răspunsul autoritativ al backendului. Modificările optimiste sunt limitate și sunt corectate vizibil dacă operațiunea eșuează.')
b('Favoritele pot fi locale pentru vizitatori și sincronizate la autentificare, cu reguli de unire fără duplicate.')
b('Formularele validează pentru claritate în browser și obligatoriu în Python. Mesajele păstrează datele neconfidențiale deja introduse.')
h('Imagini și resurse')
p('Se folosesc dimensiuni explicite, variante responsive, formate moderne și încărcare amânată pentru imaginile aflate sub prima zonă vizibilă. Imaginea principală este prioritizată. Codul se împarte pe trasee; filtrele și recomandările complexe nu blochează afișarea conținutului de bază.')
h('Contractul dintre frontend și backend')
p('API-ul este versionat și documentat prin OpenAPI. Include identificatori stabili, paginare, metadate de filtrare, erori standard, cod de corelare și reguli pentru monedă și precizie. Operațiile de comandă folosesc chei de idempotentă pentru a preveni repetarea efectului la retransmitere. Frontendul nu primește chei de integrare sau secrete comerciale.')
h('Recepție frontend')
p('Cele 16 tipuri de pagini sunt verificate pe Chrome, Edge, Firefox și Safari, în ultimele două versiuni stabile disponibile la testare, plus iOS Safari și Android Chrome reprezentative. Toate cele 6 trasee principale funcționează la tastatură. Erorile de rețea, sesiunea expirată, coșul gol și stocul schimbat au comportament definit și testat.')

page('11 Specificația backendului Python și modelul de date')
table(['Modul','Entități și reguli principale'],[
('Catalog','Product, Variant/SKU, Category, AttributeDefinition, AttributeValue, Brand; unități și atribute pe categorie.'),
('Date și proveniență','SourceRecord, ImportRun, FieldMapping, ValidationIssue; original, valoare normalizată, sursă, dată și statut.'),
('Conținut și media','ProductTranslation, MediaAsset, Page, ContentBlock; versiuni, revizie, limbă și publicare.'),
('Merchandising','Collection, CollectionRule, ProductCollection, Scene, SceneItem, CompatibilityGroup, Campaign; excluderi explicite și programare.'),
('Comerț','Price, PriceHistory, Inventory, Reservation, Cart, CartItem, Promotion, Order, OrderLine; calcul exact și instantaneu al comenzii.'),
('Operațiuni și clienți','Customer, Address, PaymentAttempt, Shipment, ReturnRequest, ConsentRecord, AuditEvent; acces limitat și retenție definită.'),
],[4.3,13.1])
h('Modelarea seturilor')
p('Un set comercial cu SKU propriu se distinge de un pachet compus la comandă. Setul are compoziție declarată și stoc propriu sau o regulă explicită de derivare. Pachetul din scenă are componente, cantități și disponibilitate calculată din fiecare SKU. Rezervarea și eliberarea stocului sunt atomice și au termene de expirare.')
h('Grupuri de servicii API')
p('Se specifică servicii pentru catalog și variante; categorii și filtre; căutare și sugestii; colecții și scene; recomandări de cadouri; favorite; coș și recalculare; checkout și cotație transport; comenzi și plăți; cont și adrese; conținut și traduceri; administrare, import și audit. Fiecare grup are schemă, permisiuni, erori, limite și teste de contract.')
h('Reguli de corectitudine')
p('Sumele se calculează cu precizie zecimală și reguli de rotunjire explicite. O comandă păstrează prețul, taxele, reducerile, moneda și descrierea produselor la momentul confirmării. Disponibilitatea este verificată din nou la finalizare. Confirmarea plății vine dintr-un mesaj autentificat al procesatorului și se reconciliază cu tranzacția, nu din simpla revenire a browserului.')
h('Administrare')
p('Cele 5 ecrane de bază: catalog și importuri; colecții și reguli; scene și pachete; conținut și traduceri; comenzi și integrări. Se prevăd roluri pentru editor, catalog, operațiuni și administrator, istoric al modificărilor și separarea editării de publicare.')

page('12 Integrări și fluxul comercial complet')
table(['Integrare','Date și comportament','Verificare de acceptare'],[
('Catalog și gestiune','Export/API sau conector; import inițial și actualizări incrementale; versiuni și ștergeri controlate.','100% înregistrări reconciliate; reluare fără duplicate; jurnal al diferențelor.'),
('Preț și stoc','O sursă autoritativă per câmp; evenimente sau sincronizare periodică.','95% actualizări propagate în ≤5 minute, dacă sursa permite; revalidare la checkout.'),
('Plăți','Furnizorul contractat de CESIRO; inițiere, confirmare, eșec, expirare, rambursare.','Câte un scenariu complet pentru fiecare stare; retry și webhook duplicat fără efect dublu.'),
('Livrare','Curier la adresă și locker unde sunt contractate; țară, adresă, eligibilitate, tarif, AWB și urmărire.','Tariful final coincide cu sumarul acceptat; adresă sau locker invalid blocat explicabil.'),
('Facturare și ERP','Transmitere comandă și date fiscale, statut, documente și corecții.','Totalurile se reconciliază; retry controlat; identificator extern salvat.'),
('Mesaje și analiză','Email tranzacțional, consimțământ, evenimente și feeduri comerciale.','Fără dublare la retry; evenimente fără date personale nejustificate; respectarea alegerilor clientului.'),
],[3.2,7.5,6.7])
h('Fluxul comenzii')
p('Selecție produse → coș recalculat → identificare opțională → adresă și livrare → total final → rezervare și comandă în așteptare → plată sau metoda alternativă acceptată → confirmare → facturare și expediere → livrare → eventual retur și rambursare. Fiecare tranziție are stare, condiții de intrare și reguli de anulare.')
p('Pentru lipsa de stoc, preț schimbat, plată întârziată sau indisponibilitatea curierului, utilizatorul primește explicație și o acțiune posibilă. Comanda nu este marcată plătită de frontend. Dacă apare plata după expirarea rezervării, backendul aplică un flux explicit de verificare și rezolvare.')
h('Configurarea politicilor')
p('Tarifele, pragurile de transport, metodele de plată, cotele fiscale și returul vor fi configurabile și confirmate de CESIRO. Informațiile publice despre livrare și FAQ sunt puncte de inventariere, nu contracte tehnice ale furnizorilor. Datele estimate de greutate sau dimensiune nu sunt folosite la calculul transportului. [S3, S7]')

page('13 Performanță accesibilitate și securitate')
table(['Domeniu','Țintă propusă','Metodă și condiții'],[
('Experiență reală','LCP ≤2,5 s; INP ≤200 ms; CLS ≤0,1 la percentila 75.','RUM pe mobil și desktop, separat, în fereastră de 28 de zile; dacă volumul este insuficient, se raportează limitarea. [S13]'),
('Laborator înainte de lansare','Lighthouse mobil ≥90 pentru performanță pe home, listare, produs și colecție.','Mediana a 3 rulări per pagină, profil mobil fix și aceleași condiții; nu înlocuiește măsurarea reală.'),
('API și căutare','Citire API p95 ≤400 ms; căutare p95 ≤500 ms; erori 5xx <0,5%.','10.000 SKU-uri, 6 limbi, 100 utilizatori virtuali, 30 minute; cache rece și cald raportate separat; timpii furnizorilor externi separați.'),
('Operațiuni comerciale','Recalculare coș p95 ≤700 ms; 0 stocuri negative în testele de concurență.','Scenarii cu minimum 20 tentative simultane asupra ultimelor unități disponibile.'),
('Continuitate','Disponibilitate lunară ≥99,9%; RPO ≤1 oră; RTO ≤4 ore.','Ținte operaționale; monitorizare, copii de siguranță și exercițiu documentat de restaurare.'),
('Accesibilitate','WCAG 2.2 AA pentru paginile și fluxurile livrate.','Audit automat și manual: tastatură, cititor de ecran, zoom, contrast, focus și formulare. [S12]'),
],[3.2,6.2,8.0])
h('Securitate și protecția datelor')
p('Se prevăd HTTPS, sesiuni în cookie-uri protejate, control acces pe server, MFA pentru administratori, protecție CSRF, validare și curățare conținut, limitarea cererilor și jurnalizarea acțiunilor importante. Drepturile sunt verificate pentru fiecare resursă, inclusiv comenzi, adrese și exporturi. Secretele rămân în infrastructură, separat de cod.')
p('Plățile folosesc fluxul furnizorului; platforma nu stochează numere complete de card. Datele personale sunt minimizate și au politici de retenție, export și ștergere aprobate de responsabilul desemnat. Copiile de test sunt anonimizate. Taxele și regulile juridice sunt configurate și validate de specialiștii CESIRO, fără preluare automată din texte istorice.')
p('Criteriu de lansare: zero vulnerabilități critice sau ridicate nerezolvate în domeniul testat și 100% scenarii de autorizare, plată și acces la date trecute.')

page('14 Migrarea datelor SEO și localizarea')
h('Preluarea datelor')
p('Sursa preferată pentru execuție este un export complet sau un API autorizat, cu identificatori și relații. Datele publice citite pentru acest proiect ajută la definirea contractului; nu înlocuiesc baza operațională. Importul are zonă de pregătire, raport de validare și publicare separată. Fiecare rulare este reluabilă și idempotentă.')
p('Succesiune: inventar și export de referință → păstrare date brute → mapare câmpuri → normalizare → validare → reconciliere → încărcare în mediul de test → verificare comercială → plan de actualizare diferențială și trecere în producție.')
h('Conservarea adreselor și vizibilității')
b('Se inventariază toate URL-urile din sitemap și sursele interne disponibile; fiecare primește decizie: păstrare, redirecționare permanentă, arhivare sau răspuns corespunzător pentru eliminare.')
b('Redirecționările duc direct la echivalentul relevant, fără lanțuri sau trimitere generală la pagina principală. Produsele temporar fără stoc își păstrează pagina utilă.')
b('Paginile publice au titlu, descriere, canonical, legături interne și date structurate concordante cu informația vizibilă. Ratingurile apar doar dacă există recenzii reale.')
b('Sitemapurile se împart pe tip și limbă, pentru operare și verificare mai ușoare, în limitele publicate de Google. Nu se afirmă că dimensiunea actuală depășește automat aceste limite. [S14]')
b('Filtrele indexabile sunt selectate editorial; combinațiile fără valoare distinctă au reguli explicite de indexare. Nu se produc mii de pagini aproape identice.')
h('Șase limbi și monede')
p('RO, EN, DE, HU, BG și EL păstrează corespondența între aceleași produse. URL-urile existente pe limbi sunt mapate explicit, inclusiv variantele de slug. Se validează hreflang reciproc și canonical pentru fiecare variantă publicată. Limba nu determină automat țara de livrare sau moneda de plată.')
p('RON este moneda observată pentru exemplele de produs. Afișările EUR și HUF sunt tratate separat, cu dată a cursului și reguli de rotunjire; plata într-o monedă se activează numai dacă procesatorul și politica magazinului o susțin. [S3, S4]')
h('Recepție')
p('100% SKU-uri și relații sursă contabilizate; 100% URL-uri inventariate cu decizie; 0 pagini importante blocate accidental; 0 asocieri hreflang nereciproce sau cu destinație nevalidă în setul publicat; 0 diferențe de preț între datele structurate și oferta vizibilă la aceeași versiune.')

page('15 Indicatori comerciali și măsurarea rezultatelor')
p('Referința inițială se stabilește din ultimele 28 de zile comparabile înainte de lansare, cu excluderea traficului intern, testelor și roboților identificați. Se înregistrează separat mobil/desktop, canal, țară și clienți noi/recurenți. Dacă analiza existentă nu este fiabilă, perioada de referință începe după validarea instrumentării.')
table(['Indicator și formulă','Țintă la 90 de zile','Interpretare'],[
('Conversie = comenzi confirmate eligibile / sesiuni eligibile','+15% relativ față de referință','Exemplu: 2,00% → 2,30%; nu +15 puncte procentuale.'),
('Valoare medie = venit produse după reduceri / comenzi eligibile','+10% relativ','Se exclud transportul și comenzile de test; anulările și retururile se urmăresc separat.'),
('Abandon checkout = 1 − comenzi finalizate / checkouturi unice începute','−15% relativ','Aceeași fereastră de atribuire și aceeași definiție înainte/după.'),
('Căutări fără rezultate / total căutări valide','−20% relativ','Separare interogări valide de trafic automat; analiză săptămânală a primelor 50 interogări problematice.'),
('Venit din comenzi cu minimum un pachet sau combinație comercială','≥10% din venitul eligibil','Definiția pachetului se fixează înaintea măsurării; nu se dublează atribuirea între colecții.'),
('Publicare colecție standard','≤30 minute de lucru editorial','Măsurat pe 3 colecții, cu date și imagini deja pregătite; fără dezvoltare software.'),
],[7.2,3.7,6.5])
h('Evenimente necesare')
p('Vizualizare listă și produs, selecție produs, căutare, aplicare filtre, acces colecție, început/finalizare selector cadouri, vizualizare scenă, adăugare în coș, început checkout, alegere livrare/plată, cumpărare și rambursare. Evenimentele au identificatori consistenți, limbă, monedă și context de listă; cumpărarea este deduplicată după comandă.')
h('Experimente și protejarea marjei')
p('Se propun 3 experimente: intrări după moment versus prezentarea curentă; selecție de cadouri ghidată; scenă completă versus recomandări individuale. Eșantionul se calculează după trafic și rata de bază, cu prag de semnificație și putere stabilite înaintea pornirii. Dacă volumul nu permite, rezultatul se raportează ca observație, fără concluzie cauzală.')
p('Creșterea veniturilor se urmărește împreună cu marja, rata retururilor și costul reducerilor. Guardrail propus: rata retururilor să nu crească cu peste 1 punct procentual și marja procentuală să nu scadă cu peste 1 punct fără justificare aprobată. Aceste evaluări necesită date interne.')

page('16 Activități etape și livrabile')
table(['Pachet și interval','Activități','Livrabile și prag de închidere'],[
('A1 Audit și contract de date\nSăptămânile 1–2','Inventar complet, surse, interviuri, indicatori de referință, integrare.','Dicționar, mapări, raport calitate, proprietari de date; toate sursele și necunoscutele înregistrate. O1, O8.'),
('A2 Taxonomie și concept\nSăptămânile 2–4','Meniu, categorii, colecții, reguli și parcursuri.','Arhitectură informațională; 12 fișe de colecții; 6 fluxuri; prima rundă de test. O2, O4.'),
('A3 Design și conținut\nSăptămânile 3–6','Sistem vizual, prototip, administrare, fotografie și localizare.','48 ecrane publice + 5 administrative; ≥30 componente; a doua rundă de test. O2, O3.'),
('A4 Date și backend\nSăptămânile 4–10','Model, API, import, catalog, reguli, administrare și integrări.','API documentat; import reconciliat; servicii comerciale testate; rapoarte de erori. O1, O5.'),
('A5 Frontend\nSăptămânile 6–11','Pagini React, căutare, coș, checkout, cadouri și scene.','16 tipuri de pagini funcționale în mediul de test; integrare cu Python. O3, O4, O5.'),
('A6 Validare și pregătire lansare\nSăptămânile 11–14','Regresie, accesibilitate, securitate, performanță, SEO și migrare de probă.','Toate scenariile critice trecute; zero defecte blocante; raport de recepție. O5, O6, O7.'),
('A7 Lansare și stabilizare\nSăptămânile 15–16','Trecere controlată, verificări, instruire și corectarea incidentelor.','Plan de revenire validat; 2 sesiuni de instruire; 14 zile de stabilizare.'),
('Rezervă\nPână la săptămâna 18','Remedieri de date, integrări și aprobări întârziate.','Replanificare explicită, fără eliminarea criteriilor de recepție.'),
],[4.0,6.0,7.4])
p('Etapele se suprapun unde dependențele permit. Calendarul presupune acces la date și medii de test la început, furnizori disponibili și răspunsuri la deciziile de proiect în maximum 3 zile lucrătoare. Lansarea este o activitate viitoare; acest document nu o execută și nu o autorizează implicit.')
p('După lansare: evaluări la 30, 60 și 90 de zile, cu raport asupra indicatorilor, stocului, traficului și experimentelor. Obiectivele comerciale nu blochează recepția tehnică dacă sunt îndeplinite criteriile de livrare, dar rămân urmărite în etapa de optimizare.')

page('17 Resurse dependențe și riscuri')
h('Echipă și estimare de efort')
table(['Rol','Efort orientativ în zile persoană'],[
('Coordonare și analiză','20–30'),('Design UX și UI','25–35'),('Frontend React','55–70'),('Backend Python și integrări','60–80'),('Date și conținut inițial','20–30'),('Testare și accesibilitate','25–35'),('Infrastructură și SEO tehnic','15–25')
],[11.4,6.0])
p('Total estimativ: 220–305 zile persoană. Rolurile pot fi cumulate, dar disponibilitatea lor trebuie păstrată. Estimarea nu este ofertă de preț. Bugetul se calculează din efort × tarif, plus infrastructură, servicii externe, fotografie și revizie editorială extinsă. Migrarea unui istoric complex de clienți/comenzi sau refacerea integrărilor majore poate extinde estimarea.')
h('Date și decizii necesare înaintea execuției')
p('CESIRO desemnează responsabilul comercial și furnizează exportul complet cu variante și relații, sursa prețului și stocului, istoricul reducerilor, configurația plăților și curierilor, documentația facturării, politicile aprobate, drepturile asupra media și accesul la analitice. Se decide păstrarea ori migrarea conturilor și comenzilor, fără expunerea parolelor sau a datelor personale în medii neprotejate.')
table(['Risc','Măsură și responsabil'],[
('Date inconsistente sau seturi incomplete','Responsabil catalog: reguli și verificare; lipsurile critice blochează produsul afectat, nu sunt completate prin presupunere.'),
('API-uri ori furnizori incompatibili','Responsabil tehnic: probă de integrare în primele două săptămâni; contract și plan alternativ înainte de dezvoltare extinsă.'),
('Pierdere trafic organic','Responsabil SEO: inventar complet, păstrare URL-uri, redirecționări și verificare după lansare.'),
('Preț ori stoc expirat','Operațiuni și backend: sursă unică, timp de sincronizare, revalidare și reconciliere.'),
('Volum mare de traduceri și corecții','Responsabil conținut: inventar, prioritizare și buget separat; păstrarea tuturor originalelor și a stării de revizie.'),
],[6.0,11.4])

page('18 Recepția proiectului și limitele domeniului')
h('Pachetul final de livrare prevăzut')
b('Registrul datelor, dicționarul de câmpuri, maparea taxonomiilor și raportul de reconciliere, cu toate excepțiile.')
b('Prototipurile și sistemul de design, biblioteca React, șabloanele de conținut și regulile celor 12 colecții.')
b('Codul și documentația frontendului JavaScript + React și a backendului Python, livrate în depozitul beneficiarului.')
b('Contractul API, schema datelor, documentația integrărilor și ghidul administrării, inclusiv import și publicare.')
b('Rapoarte funcționale, de accesibilitate, securitate, performanță, SEO și migrare, cu dovezi și condiții de test.')
b('Plan de instalare, operare, monitorizare, backup, restaurare și revenire; instrucțiuni pentru incidente.')
b('Planul de măsurare, definițiile indicatorilor, tabloul de raportare și rezultatele instruirii.')
h('Condiții obligatorii de recepție')
p('Beneficiarul validează cele 6 parcursuri principale și scenariile comerciale negative. Sunt trecute 100% testele critice, inclusiv ultima unitate de stoc, actualizarea prețului, plată eșuată, plată întârziată, webhook duplicat, livrare indisponibilă și rambursare. Nu există defecte blocante ori pierderi de date nerezolvate. Excepțiile necritice sunt consemnate cu termen și responsabil.')
p('Sunt demonstrate importul repetabil, reconcilierea totalurilor, izolarea accesului la conturi, restaurarea unei copii și revenirea controlată. Datele și prețurile afișate coincid cu sursa agreată la aceeași versiune. Rapoartele de recepție disting testele din mediu de test de verificările ulterioare pe producție.')
h('Domeniu suplimentar care se estimează separat')
p('Marketplace cu vânzători independenți; aplicații mobile native; înlocuirea ERP-ului; program complex de fidelizare; prețuri B2B negociate și conturi de credit; personalizare predictivă; producție foto pentru întregul catalog; revizie umană integrală a tuturor traducerilor; migrarea istoricului vechi dacă schema și calitatea acestuia necesită un proiect separat.')
h('Ce rămâne neschimbat prin acest document')
p('Nu s-au executat modificări pe cesiro.com, comenzi, plăți, autentificări administrative, importuri sau operații de publicare. Toate activitățile de dezvoltare și lansare descrise sunt viitoare. Auditul public confirmă existența unor surse și câmpuri; validarea completă a stocului, produselor și operațiunilor aparține primei etape de execuție.')

page('19 Exemple de date și destinația câmpurilor publice')
p('Valorile de mai jos sunt instantanee publice din 21 octombrie 2026. Stocul afișat nu confirmă cantitatea fizică, iar prețurile se pot schimba. Exemplele arată cum se păstrează informația și cum este folosită în noua temă. [S3, S4]')
table(['Câmp','Exemplul de ceașcă','Exemplul de set'],[
('Identificator public','wp-112938','wp-105304'),
('SKU','5900_2763_2070_G242','5900_3216_9718_D144'),
('EAN','5949414069102','5949414090298'),
('Preț afișat / regulat','15,29 / 16,99 RON','89,99 / 99,99 RON'),
('Stoc public','17','100'),
('Atribute utilizabile','Maro; capacitate 220 ml','Roz; 9 bucăți; 200 ml pentru cana din set'),
('Decizie de marketing propusă','Cafea în doi sau cadou, după validarea selecției','Casă nouă, după confirmarea componentelor și numărului de persoane'),
],[4.3,6.55,6.55])
table(['Grup în JSON public','Destinație în proiect'],[
('product_identity','Registru de identitate și corelare cu SKU/variante; câmpurile sursă nule rămân nule.'),
('commerce','Preț, disponibilitate și reguli de stoc; sincronizare cu sursa autoritativă.'),
('content','Texte, categorii, atribute și etichete; original plus versiune validată.'),
('media','Galerie și arhiva de media; deduplicarea referințelor și păstrarea ordinii.'),
('reviews','Recenzii reale, moderare și agregate calculate; zero nu devine rating public pozitiv.'),
('seo','Metadate importate și versiunea publicată, cu controlul diferențelor.'),
('language, schema, visibility','Limbă și metadate de proveniență/import; nu devin mesaje comerciale.'),
('JSON-LD, canonical, hreflang și cursuri','Verificare SEO și localizare; concordanță cu informația vizibilă și regulile comerciale.'),
],[5.4,12.0])
p('Pentru fiecare grup, livrabilul A1 detaliază câmpurile efectiv existente în exportul complet, tipurile, unitățile, exemplele, obligativitatea, proprietarul, regula de transformare și destinația. Câmpurile suplimentare descoperite sunt adăugate în registru înainte de import, fără eliminare tacită.')

page('20 Surse și metoda de verificare')
p('Consultare la 21 octombrie 2026. Pentru CESIRO s-au folosit exclusiv cereri de citire a paginilor și fișierelor publice. Nu s-au apelat rute administrative, de scriere sau de API restricționate în robots.txt. Datele publice pot varia după data consultării.')
sources=[
('S1 CESIRO pagina principală și navigarea','https://cesiro.com/'),
('S2 CESIRO sitemap public','https://cesiro.com/sitemap.xml'),
('S3 Ceașcă de 220 ml pagina și datele structurate','https://cesiro.com/p/ceasca-cu-farfurioara-220-ml-maro-decorat-cu-flori-si-spic-de-grau'),
('S4 Set de masă de 9 piese pagina și datele structurate','https://cesiro.com/p/set-masa-4-pers-9-piese-cana-roz-200-ml-bol-tava-termorezistenta-portelan-cu-trandafiri-roz'),
('S5 Despre CESIRO','https://cesiro.com/legal/despre-cesiro'),
('S6 Politica de retur și garanție','https://cesiro.com/legal/politica-de-retur-si-garantie'),
('S7 Întrebări frecvente','https://cesiro.com/legal/intrebari-frecvente'),
('S8 Mystery Box','https://cesiro.com/legal/mistery-box'),
('S9 Trendyol România referință de navigare','https://www.trendyol.com/ro'),
('S10 Next.js Server and Client Components','https://nextjs.org/docs/app/getting-started/server-and-client-components'),
('S11 Django prezentare oficială','https://www.djangoproject.com/start/overview/'),
('S12 W3C WCAG 2.2','https://www.w3.org/TR/WCAG22/'),
('S13 Google Web Vitals','https://web.dev/articles/vitals'),
('S14 Google Search Central sitemapuri','https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap'),
('S15 CESIRO robots.txt','https://cesiro.com/robots.txt')]
for label,url in sources:link(label,url)
h('Cum se interpretează dovezile')
p('Numărătorile sunt măsurători ale sitemapului și valorilor afișate în meniul public, nu audit de gestiune. Exemplele de câmpuri și probleme provin din două produse. Datele din JSON sunt publicate de site și pot necesita reconciliere cu pagina vizibilă și sursa internă. Nu s-au verificat conversia, performanța reală, furnizorii integrați sau acuratețea fiecărei traduceri.')
p('Toate pragurile de recepție, volumele de livrabile, eforturile și țintele comerciale sunt propuneri ale proiectului. Ele se fixează contractual după etapa A1, păstrând explicit unitățile, condițiile de test și responsabilitățile.')

path=OUT/'Proiect_CESIRO_Design_React_Python.docx'
doc.save(path)
print(path)
print('Paragraphs',len(doc.paragraphs),'Tables',len(doc.tables))
