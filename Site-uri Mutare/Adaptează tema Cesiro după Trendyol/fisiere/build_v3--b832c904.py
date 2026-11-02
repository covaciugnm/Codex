from pathlib import Path
import json, re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

OUT=Path(__file__).parent
stats=json.loads((OUT/'evidence-v2/catalog-summary.json').read_text(encoding='utf-8'))
def init(title,short):
    global doc
    doc=Document(); s=doc.sections[0]
    s.page_width=Cm(21);s.page_height=Cm(29.7)
    s.top_margin=Cm(1.6);s.bottom_margin=Cm(1.6);s.left_margin=Cm(1.75);s.right_margin=Cm(1.75)
    n=doc.styles['Normal'];n.font.name='Calibri';n.font.size=Pt(10.5)
    n.paragraph_format.space_after=Pt(5);n.paragraph_format.line_spacing=1.0
    for st in doc.styles:
        for x in list(st.element.xpath('.//w:pBdr')):x.getparent().remove(x)
    for nm,sz in [('Title',27),('Subtitle',14),('Heading 1',19),('Heading 2',12)]:
        st=doc.styles[nm];st.font.name='Calibri';st.font.size=Pt(sz);st.font.color.rgb=RGBColor(0,0,0)
        st.paragraph_format.space_before=Pt(8);st.paragraph_format.space_after=Pt(7)
        st.paragraph_format.keep_with_next=True
    doc.core_properties.title=title;doc.core_properties.author='';doc.core_properties.subject='Specificație de proiect pentru design și dezvoltare'
    f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=f.add_run('CESIRO  •  '+short+'  •  21 octombrie 2026  •  ');r.font.size=Pt(8)
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
def p(t,style=None):return doc.add_paragraph(t,style)
def b(t):p(t,'List Bullet')
def h(t):doc.add_heading(t,2)
def head(t):doc.add_heading(t,1)
def page(t):
    pa=doc.add_heading(t,1);pa.paragraph_format.page_break_before=True
def table(headers,rows,widths=None,small=10):
    if widths is None:widths=[17.5/len(headers)]*len(headers)
    t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
    pr=t._tbl.tblPr;bd=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');bd.append(el)
    pr.append(bd)
    for c,w in zip(t.columns,widths):c.width=Cm(w)
    for c,x in zip(t.rows[0].cells,headers):c.text=x
    for row in rows:
        for c,x in zip(t.add_row().cells,row):c.text=str(x)
    for ri,row in enumerate(t.rows):
        rp=row._tr.get_or_add_trPr();rp.append(OxmlElement('w:cantSplit'))
        if ri==0:rp.append(OxmlElement('w:tblHeader'))
        for ci,c in enumerate(row.cells):
            c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp=c._tc.get_or_add_tcPr();m=OxmlElement('w:tcMar')
            for edge in ['top','bottom','left','right']:
                e=OxmlElement('w:'+edge);e.set(qn('w:w'),'75');e.set(qn('w:type'),'dxa');m.append(e)
            cp.append(m);sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'243B53' if ri==0 else ('F4F6F8' if ri%2 else 'FFFFFF'));cp.append(sh)
            for pa in c.paragraphs:
                pa.paragraph_format.space_after=Pt(2);pa.paragraph_format.space_before=Pt(2);pa.paragraph_format.line_spacing=1.02
                if ri==0:pa.paragraph_format.keep_with_next=True
                for r in pa.runs:r.font.size=Pt(small);r.bold=(ri==0);r.font.color.rgb=RGBColor.from_string('FFFFFF' if ri==0 else '000000')
    p('').paragraph_format.space_after=Pt(0)
    return t
def link(label,url):
    pa=p('');rel=pa.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
    hl=OxmlElement('w:hyperlink');hl.set(qn('r:id'),rel);r=OxmlElement('w:r');rp=OxmlElement('w:rPr');col=OxmlElement('w:color');col.set(qn('w:val'),'225577');rp.append(col);r.append(rp);t=OxmlElement('w:t');t.text=label;r.append(t);hl.append(r);pa._p.append(hl)
def save(name):doc.save(OUT/name)

init('Proiect CESIRO pentru o temă React pe platforma Python existentă','Proiect V3')
p('Proiect CESIRO pentru o temă React pe platforma Python existentă','Title')
p('Versiunea 3 specificație de proiect și criterii de recepție','Subtitle')
p('Destinat conducerii CESIRO, echipei de produs, furnizorilor de dezvoltare și auditorilor. Bază pentru decizie, estimare și recepție.')
head('0 Direcția propusă')
p('cesiro.com va deveni locul în care clientul își compune masa, completează decorul preferat și comandă un cadou personal, cu informații verificabile despre produs și livrare. Ceramica CESIRO conduce experiența de brand. Zona Pro deservește distinct HoReCa și consumabilele, folosind același catalog și același motor comercial.')
p('De la Trendyol preluăm claritatea accesului la produse, căutarea și filtrarea. Identitatea vizuală, conținutul și serviciile sunt proiectate pentru un brand de ceramică: culoare, glazură, decor, utilizare și legătura cu fabrica. Referințele comparative sunt prezentate în capitolul 20.')
h('Domeniu și rezultat')
p('Proiectul livrează o temă nouă pentru cesiro.com, cu JavaScript și React, cuplată la platforma Python și la API-urile existente din U:/cesiro.com. Nu construiește un sistem API nou, un backend comercial paralel sau o bază de produse separată. Catalogul, administrarea, comenzile, plățile și integrările rămân cele ale platformei actuale. Documentația descrie lucrări viitoare; nu execută modificări pe site.')
p('Direcție de comunicare de testat: „Ceramică din Sighișoara, aleasă pentru masa ta”. Mesajul de origine se folosește numai pentru produsele CESIRO cu proveniență documentată; colecțiile mixte identifică producătorul fiecărei piese.')


h('Trei motive concrete pentru cumpărarea directă')
table(['Diferențiator','Rezultat verificabil propus'],[
('Origine și încredere','100% din produsele promovate ca fabricate de CESIRO au proveniență documentată; promisiunea publică de înlocuire gratuită a produselor sosite sparte este păstrată și operaționalizată în §8.4, fără restrângerea drepturilor existente.'),
('Masa potrivită și completarea seriei','12 scene cumpărabile și minimum 20 de serii eligibile la finalul etapei T3; setul se poate ajusta după persoane și buget.'),
('Cadou personal','Concept pentru 10 produse personalizabile; activare numai dacă platforma și fabrica susțin deja fluxul verificat. În caz contrar, cerere de ofertă prin fluxul existent, fără modul API nou.')],[4.2,13.3])
p('Domeniu de bază: tema, organizarea și prezentarea datelor, integrarea cu funcțiile existente și configurator 2D care folosește aceleași operații de coș. Plan: 16 săptămâni, 160–200 zile-persoană, apoi 90 zile de măsurare. Ideile care cer capabilități backend indisponibile sunt separate ca extensii necontractate; nu obligă proiectul temei să creeze un API nou.')

h('Regula de integrare și limitele temei')
p('Datele sunt preluate prin contractul paginilor și API-urile actuale. Se documentează câmpurile și comportamentul existente; nu se reproiectează API-ul pentru a se potrivi machetei. Un câmp absent este ascuns, marcat neconfirmat sau acoperit prin conținut editorial aprobat, fără inventare. O funcție nesusținută primește alternativă existentă ori rămâne în foaia de parcurs. Specificațiile din §8 pentru extensii descriu potențialul de marketing, nu un angajament de construire a unui nou sistem.')


page('1 Date disponibile și dimensiunea reală')
p('Inventarul folosește constatările publice CESIRO din 21 octombrie 2026, citirea statică a unor fișiere din U:/cesiro1-site și verificarea ulterioară a bazei indicate U:/cesiro.com și exportul de produse datat în nume 16 septembrie 2026. Nu au fost accesate baze de date operaționale, conturi de clienți sau rapoarte de vânzări. [I1–I5, S1–S4]')
table(['Sursă','Constatare','Limită'],[
('Export intern de produse','5.222 rânduri și ID-uri distincte; 5.221 SKU-uri nenule distincte; 1 SKU lipsă.','Instantaneu istoric, nu inventar curent.'),
('Stare în export','5.211 publicate, 11 cu valoarea −1; 5.217 simple, 2 grouped, 2 external, 1 variable.','Tipul exportului trebuie mapat la modelul actual; active nu înseamnă în stoc.'),
('Sitemap public','32.868 URL-uri; 31.674 de produs = 5.279 × 6 limbi.','Nu reprezintă 31.674 SKU-uri. Diferența față de export nu dovedește produse noi.'),
('Câmpuri lipsă în export','EAN/GTIN 1.145; descriere 670; imagini 50; greutate 2.014; stoc 23; preț obișnuit 5.','Lipsa din export nu dovedește lipsa în producție; GTIN nu se inventează.'),
('Structură software locală','Flask, SQLAlchemy, Alembic, PostgreSQL; admin React, TypeScript, Vite, TanStack.','Prezența codului nu certifică versiunea instalată sau funcționarea integrărilor.')],[3.5,7.8,6.2])
p('În U:/cesiro.com există mecanismul de teme: registry, manifest.json, files.json și page_contracts.json, cu logică comercială comună. Fișierele README, requirements, package.json, factory.py, cms.py și docker-compose.yml comparate sunt identice cu cele din U:/cesiro1-site. Aceasta nu dovedește identitatea tuturor datelor sau a imaginii Docker active. Repository-ul cesiroproduction/site-uri este indicat de beneficiar; accesul disponibil returnează 404, deci commitul și corespondența cu producția rămân de verificat. [I6]')


h('Inventarul contractual și analiza ABC')
p('În primele 3–5 zile lucrătoare, responsabilul platformei livrează D01 din sursa operațională existentă, folosind exportul actual sau interogări SQL de citire versionate pe un instantaneu consistent. Nu se creează un API de export nou. Exportul acoperă fiecare tenant: produse, variante, relații, stoc pe depozit/canal, istoric de preț și vânzări agregate pe 12 luni. Se stabilesc separat N produse, N SKU-uri vandabile, N active în ultimele 90 de zile și N traduceri. Numărătorile, hashurile și data de referință se semnează în registrul D01.')
p('ABC se calculează după venitul net cumulat: A până la 80%, B următoarele 15%, C restul; marja și rotația sunt dimensiuni suplimentare. Lista de maximum 300 produse prioritare combină grupa A, disponibilitatea, marja și reprezentativitatea brandului. Nu presupunem că 300 de produse generează deja 80% din venit.')
h('Portofoliul')
p('Vitrina principală prezintă Ceramică și Masă. /pro grupează HoReCa și consumabilele; produsele din alte familii rămân în inventar și primesc o decizie de canal, fără ștergere automată. Vizibilitatea publică și URL-urile existente se tratează individual, cu analiză de trafic și redirecționare relevantă. Subdomeniul Pro nu este necesar la început.')

h('Reconciliere și origine')
p('Diferența numerică de 57 dintre sitemap și CSV nu dovedește 57 produse noi. D01 compară mulțimi după ID canonic, SKU și slug: numai în bază, numai în CSV, numai în sitemap, redenumiri, retrageri și duplicate. Fiecare diferență primește cauză; 100% sunt explicate înaintea migrării. Nu se accesează clienți nominali pentru această analiză.')
p('Producător real este câmp obligatoriu distinct de brand și vânzător. Insigna și filtrul „Fabricat de CESIRO” cer document de proveniență și validare umană. Produsele terțe rămân eligibile în vitrină cu producătorul corect; materialul, originea și fabrica nu se deduc din textul comercial sau din prefixul SKU.')


page('2 Modelul datelor și folosirea integrală')
p('Maparea documentară a temei atribuie fiecărei înregistrări și fiecărui câmp sursă o destinație: utilizare, normalizare, revizuire sau arhivare justificată. Se păstrează valoarea originală, sursa, data, regula, autorul aprobării și versiunea. Arhiva brută poate fi completă înainte ca îmbogățirea editorială să fie terminată; lansarea se face pe loturi eligibile.')
table(['Grup de date','Date existente reutilizate','Destinație și necesar de verificat'],[
('Identitate','ID, SKU, EAN/GTIN, slug, brand, părinte, tip, vizibilitate','ID canonic stabil; mapare între surse și canale; identificarea producătorului real.'),
('Conținut și limbi','Nume, texte, categorii, atribute, tags, traduceri','Serie/decor, rol în set, stil, ocazie, relație destinatar, nivel de validare pe limbă.'),
('Comerț','Prețuri, monedă, taxe, disponibilitate, stoc, precomandă','Istoric efectiv al prețului, marjă doar intern, rezervări, cantități minime, preț pe client Pro.'),
('Caracteristici','Material, culoare, capacitate, dimensiuni, greutate, bucăți','Unități normalizate; culoare vizuală validată; măsurători reale; componente și persoane justificate.'),
('Conformitate','Date existente ale furnizorului și pagini de politici','Producător și contacte, operator UE când se aplică, avertismente, lot, declarații și documente alimentare.'),
('Media și SEO','Imagini, ordine, metadate, canonical, hreflang, JSON-LD','Drepturi, alt, dimensiuni, video, modele 3D, marcaj compoziție, URL-uri și redirecturi istorice.'),
('Relații comerciale','Upsell, cross-sell, produse grupate, recenzii','Relații serie–piesă–componentă–scenă; proveniența recomandării, UGC moderat, favorite.'),
('Operațional','Ambalare, livrare, retur, integrare și depozit','Greutate colet, fragilitate, termen de producție, capacitate confirmată, reguli de spargere.')],[3.1,6.2,8.2])
p('Câmpurile de mai sus reprezintă dicționarul țintă de prezentare. D01 le mapează la datele deja disponibile și la câmpurile editoriale existente. Crearea de tabele, servicii sau endpointuri nu este parte a temei; lipsurile de platformă se listează separat, cu fallback și impact de lansare.')


h('Dicționare pe familii')
p('Veselă și căni: material, decor, diametru/capacitate, rol și utilizări verificate. Seturi: listă exactă de componente și cantități, persoane fără deducere din numărul total de piese. Gătit: temperatură și surse de încălzire documentate. Decor: dimensiuni, utilizare și stabilitate; nu se presupune contact alimentar. Curățenie: cantitate, dozaj, avertismente și documentația specifică substanței, după caz.')
p('Capacitatea de 200 ml a unei căni dintr-un set aparține componentei. Valoarea necunoscută nu devine zero. Compatibilitatea, proveniența, rezistența și certificările nu se deduc din fotografie. HEX și stilul produse de AI sunt propuneri editoriale. Câmpurile comerciale publice nu expun costul sau marja.')

h('Dicționar pentru chimice și biocide')
p('Date obligatorii când sunt aplicabile: clasificare și versiune CLP, pictograme, cuvânt de avertizare, fraze H/P și EUH, cantitate netă, furnizor, UFI când este cerut, fișă cu date de securitate cu limbă și revizie, autorizație/aviz biocid și țări de valabilitate, utilizări permise, mesaj de publicitate art. 72 și link către ingredientele detergentului. Pentru fiecare câmp există stare aplicabil/neaplicabil și justificare aprobată; nu se cer automat aceleași acte tuturor produselor de curățenie.')
p('Preț unitar: prețul final al ambalajului / cantitate netă normalizată × unitate de referință. Se afișează lei/l, lei/kg sau lei/bucată unde este relevant, pe card, fișă și coș; la un pachet mixt nu se inventează o unitate înșelătoare. Exemple de test, nu oferte: 50 lei pentru 5 l = 10 lei/l; 25 lei pentru 50 bucăți = 0,50 lei/bucată. Regula legală și excepțiile se stabilesc pe piață; afișarea utilă suplimentară este cerință de produs. [L12]')


page('3 Calitate și îmbogățire asistată')
h('Scor de calitate și condiții obligatorii')
p('Scorul editorial este 0–100: atribute utile 30, media 25, descriere și consistență 20, localizare 15, relații de serie 10. Fiecare familie are o grilă cu câmpuri aplicabile; lipsurile și contradicțiile produc punctajul, cu versiune de calcul. Produse prioritare ≥90; catalog secundar ≥60. Pragurile nu înlocuiesc condițiile legale și comerciale.')
p('Publicarea cumpărabilă cere separat identitate, preț valid, disponibilitate calculabilă, media corectă și toate informațiile/documentele obligatorii pentru familia și piața respectivă, inclusiv CLP, biocide, ingrediente și preț unitar, după aplicabilitate. Un produs cu scor 100 și o condiție obligatorie neîndeplinită nu poate fi activat pentru vânzare.')
h('Fluxul de lucru')
table(['Etapă','Activitate și livrabil','Acceptare'],[
('Preluare','Arhivă nemodificată, hash, mapare de câmpuri și raport de reconciliere D01.','100% rânduri contabilizate; 0 identificatori pierduți.'),
('Reguli','Normalizare unități, duplicate, tipuri, categorii și contradicții.','Toate erorile primesc proprietar și destinație.'),
('AI în proiect izolat','Propuneri de descriere, traducere, stil și asocieri; încredere și sursă pentru fiecare sugestie.','Nicio specificație critică sau informație legală inventată; aprobare umană.'),
('Evaluare și loturi','Set etalon 200 produse, câte 40 din 5 familii majore; eșantion manual de verificare.','Precizie ≥95% pentru atributele descriptive evaluate; 100% corectitudine pentru numerele publicate.'),
('Monitorizare','Raport zilnic de regresie, traduceri restante și surse expirate.','Alertă la scăderea scorului sau lipsa unui câmp obligatoriu; blocare publicare nouă.')],[3.1,8.7,5.7])
p('PGX/Qwen rămâne candidat: modelul, licența, capacitatea și costul per 1.000 produse se măsoară în PoC. Modulul ai_assistant nu dovedește disponibilitatea inferenței necesare. Conținutul de produs și încărcările utilizatorilor sunt date nefiabile, niciodată instrucțiuni pentru agent.')

h('Capacitatea editorială și măsurarea preciziei')
p('În săptămânile 1–2 se cronometrează 100 fișe din familii diferite. Ipoteza de planificare este 60 fișe simple/zi/editor, maximum 7 minute/fișă plus control și administrare; cazurile juridice sau tehnice dificile se separă. La 5.222 fișe sunt 87 zile-editor; doi editori alocați 50 zile furnizează 100 zile și o rezervă de 13 zile. Dacă D01 indică 6.000 fișe, rezerva dispare. Sub 52 fișe/zi/editor, se adaugă capacitate sau se reduce lotul publicabil.')
p('Această capacitate CESIRO verifică datele structurale și documentele o singură dată per produs, nu rescrie 31.332 texte. Cele 300 fișe prioritare sunt revizuite în șase limbi prin devizul extern; restul folosesc traducere asistată, validări numerice și eșantion de 5% pe limbă/familie. O eroare critică sau precizie sub prag trimite lotul complet la revizie. Lipsa dovezilor obligatorii blochează vânzarea, indiferent de capacitatea editorială.')
p('Etalonul de 200 produse raportează separat culoare, stil și rol, precum și fiecare limbă: precizie ≥95% pe fiecare celulă evaluabilă, minimum 30 exemple relevante/celulă, cu completarea etalonului când lipsesc exemple. Se raportează acoperirea, abținerile și intervalul de încredere; media globală nu poate compensa un atribut slab. Numerele și datele critice publicate sunt verificate integral.')


page('4 Obiective și rezultate cuantificabile')
p('Indicatorul principal este venitul net lunar din canalul direct: valoarea produselor facturate fără TVA, minus reduceri, anulări și retururi, fără transport. Sursa financiară prevalează asupra atribuirii din analytics. Toate creșterile procentuale de mai jos sunt relative, dacă nu este indicat „puncte procentuale”.')
table(['Obiectiv','Țintă propusă','Măsurare și termen'],[
('Venit direct','+15% față de baza comparabilă; marja de contribuție/comandă nu scade.','90 zile după lansarea temei; control pentru buget media, sezon și disponibilitate.'),
('Conversie mobilă','+15% față de baza segmentată.','Comenzi plătite valide / sesiuni mobile eligibile; fără boți și trafic intern.'),
('Valoarea coșului','+10% AOV net.','Venit net produse / comenzi valide, aceeași perioadă și definiție.'),
('Recumpărare','+3 puncte procentuale la 90 zile.','Clienți cu a doua comandă în 90 zile / cohortă cu 90 zile complete.'),
('Abandon checkout','−15% relativ.','1 − comenzi valide / sesiuni cu begin_checkout; fereastră de atribuire 7 zile.'),
('Descoperire asistată','≥10% dintre sesiunile expuse folosesc AI, căutare vizuală sau configurator.','90 zile după activarea funcției existente; utilizarea și conversia se raportează separat.'),
('Personalizare','≥5% din comenzile cu produse eligibile includ personalizare.','90 zile după activarea pilotului; marja după costul producției este pozitivă.'),
('Încredere','Recenzii noi la ≥5% din comenzile livrate eligibile; spargeri fără creștere peste 0,3 pp.','Recenzii autentice; retururi și costul despăgubirii urmărite pe cohortă.')],[4.1,6.3,7.1])
h('Baza de comparație')
p('D02 se completează până în săptămâna 2: 12 luni de vânzări agregate, minimum 8 săptămâni de trafic eligibil, segmente, marjă și retururi. Baseline-ul nu este disponibil în fișierele inspectate; validarea sa precede angajamentul comercial și bugetul final.')
p('Recepția verifică livrabilele controlabile. Țintele comerciale sunt ipoteze de testat; sezonalitatea și schimbările de preț/media se controlează separat.')

h('Valoarea funcțiilor noi și a canalului Pro')
table(['Indicator','Țintă și populație'],[
('Asistent și configurator','La 90 zile: +10% conversie asistent și +10% AOV configurator, A/B pe disponibilitatea funcției. Comparația celor care aleg singuri asistentul cu ceilalți este descriptivă, afectată de selecție.'),
('Pro','50 conturi verificate și 20 clienți cu prima comandă plătită în 90 zile; recumpărare ≥25% la 90 zile de la prima comandă; venit Pro net +15% față de perioada comparabilă D02. Dacă baza este zero, financiarul fixează ținta absolută înainte de pilot, fără procent artificial.'),
('QR și canal direct','Pilot 1.000 inserții eligibile: ≥5% scanări unice și ≥2% prime comenzi directe în 90 zile. Se raportează separat comenzi atribuite codului și migrare confirmată; un scan nu dovedește că persoana era client marketplace.')],[4.1,13.4])


page('5 Navigare după produs și după intenție')
p('Meniul principal: Veselă, Căni și cești, Servire, Gătit, Decor, Colecții și decoruri, Idei de cadou, Oferte. Intrarea Pro/HoReCa este separată în antet. Desktopul folosește un meniu vizual; mobilul, un panou accesibil cu două niveluri și căutare permanent disponibilă.')
table(['Colecție de pornire','Regulă și utilizare'],[
('Veselă de zi cu zi','Piese potrivite rutinei, utilizări documentate și stoc disponibil.'),
('Cafeaua în doi','Două piese compatibile sau set verificat; buget și ambalaj opțional.'),
('Prima casă','Compoziții pentru 2/4/6 persoane, roluri explicite și listă editabilă.'),
('Duminică în familie','Veselă plus servire, organizată după număr de persoane.'),
('Gazda care ne adună','Cadouri pentru gazdă; servire, decor și mesaje aprobate.'),
('Pentru el și Pentru ea','Colecții opționale păstrate conform cererii; stilul și bugetul decid recomandarea, fără stereotipuri.'),
('Cadou pentru părinți sau colegi','Relație, ocazie, buget, termen și posibilitate de personalizare.'),
('Nuntă și aniversare','Liste de eveniment, cantități comune și mesaje cadou.'),
('Sărbători la masă','Campanii cu perioadă, disponibilitate și conținut pe limbă.'),
('Completează decorul tău','Serie exactă, identificare piesă, alternative etichetate distinct.'),
('Culoarea casei tale','Mostre de culoare și denumiri validate; filtrare fără a depinde doar de culoare.'),
('A doua șansă','Outlet cu defectul real descris și fotografiat; fără diminuarea siguranței.')],[5.2,12.3])
p('Cele 12 rânduri definesc 12 familii editoriale; „Pentru el” și „Pentru ea” pot genera două pagini distincte. Colecțiile sunt interogări salvate pe atribute, eligibilitate, stoc și marjă internă, cu includeri/excluderi editoriale, prioritate și interval de activare. Minimum 8 produse eligibile pentru o pagină promovată; altfel, recomandări alternative sau ascunderea intrării din campanie.')
p('Editorul trebuie să creeze, previzualizeze și programeze o colecție din date pregătite în maximum 5 minute. Nu se multiplică produsele pentru fiecare ocazie. Filtrele includ serie, rol, material, culoare, dimensiuni, persoane, preț și compatibilități validate; curățenia și decorul primesc filtre proprii.')

h('Serii din SKU și colecții active')
p('Segmente precum G242, D144, 604M și 010L sunt candidați pentru decor. Fabrica validează dicționarul și excepțiile pe 100 SKU-uri înaintea oricărei regulii automate. Importul produce propuneri de relații serie–piesă–culoare, cu sursă și versiune; nu unește automat produse terțe sau coduri ambigue. Recepție: 20 serii aprobate, zero asocieri de decor greșite în lotul publicat.')
p('Ținta pentru colecțiile promovate este reevaluarea la eveniment de stoc și cel mult la 5 minute, folosind automatizările existente. Sub 8 produse eligibile, intrarea de campanie se retrage sau oferă alternative marcate. Dacă mecanismul lipsește, colecția rămâne administrată manual și nu intră în promovarea automată. Pagina și URL-ul se păstrează; tema nu construiește un serviciu nou de reconciliere.')


page('6 Experiența vizuală și paginile')
p('Se compară trei direcții creative prin moodboard și prototip de homepage/produs la 390 px: „Atelier și glazură” cu texturi autentice și gesturi de producție; „Masa de acasă” cu scene cotidiene și culori calde; „Colecția contemporană” cu compoziții grafice și accent pe decor. Recomandarea inițială combină a doua direcție cu dovezi de fabricație din prima. Planșele conceptuale și wireframe-urile mobile sunt incluse în §21. Alegerea rezultă din două runde cu câte 8 participanți și criterii documentate; schițele nu reprezintă fotografii ale catalogului sau interfețe implementate.')
table(['Grup','Tipuri de pagini și stări'],[
('Descoperire 1–6','1 Homepage; 2 categorie/listare; 3 rezultate căutare; 4 produs; 5 decor/serie; 6 colecție/ocazie.'),
('Compoziție 7–10','7 scenă cumpărabilă; 8 configurator de masă; 9 selector cadou; 10 personalizare produs.'),
('Tranzacție 11–14','11 coș; 12 checkout; 13 confirmare/urmărire; 14 cont cu favorite, istoric și vizualizări recente.'),
('Relație 15–18','15 listă eveniment publică și administrare; 16 Club CESIRO; 17 card cadou; 18 Outlet.'),
('Brand 19–22','19 poveste/fabrică/showroom; 20 Jurnal și articol; 21 UGC/recenzii; 22 ajutor și politici.'),
('Profesional 23–24','23 portal Pro și comandă rapidă; 24 ofertă/mostre/logo. Compararea a până la 4 produse este un modul transversal.'),('După cumpărare 25','25 Comenzile mele cu status, factură, re-comandă, solicitări de modificare, spargere și retragere; acces și pentru clientul fără cont.')],[4,13.5])
p('Livrabil: 25 tipuri, fiecare cu referințe la 390, 768 și 1440 px, minimum 75 ecrane de bază, plus stări de eroare, gol, încărcare și lipsă stoc pentru fluxurile aplicabile. Numărul de ecrane nu substituie acoperirea funcțională. Prototipul prioritar este mobil; checkoutul permite comandă fără cont și salvarea progresului.')
h('Ordinea pe pagina principală și pe produs')
p('Homepage: căutare și meniu → promisiune verificată → produse/ocazii → compune masa → colecții după decor și culoare → origine → recenzii autentice → Pro. Produs: imagini și scară → nume/serie → preț și disponibilitate → variante → livrare → acțiune de cumpărare → componente/utilizări → siguranță/îngrijire → completare set → recenzii.')
p('Microinteracțiunile explică adăugarea în coș, schimbarea variantei și erorile; se respectă preferința de mișcare redusă. Bara inferioară de acțiuni nu acoperă conținutul sau tastatura. Galeria are gesturi și controale accesibile. PWA și notificările sunt extensii cu acord explicit, fără cache pentru coș, plăți sau date personale.')

page('7 Sistem de design și producție de conținut')
p('Figma definește componentele și tokenurile; Style Dictionary exportă valorile aprobate; Storybook documentează implementarea React, stările și accesibilitatea. Catalogul estimat conține 60–80 componente și variante utile. Recepția cere acoperirea componentelor folosite în cele 25 de tipuri, nu atingerea artificială a unui număr.')
table(['Livrabil','Volum și regulă de acceptare'],[
('Sistem vizual','Tipografie, spațiere, culori, contrast, focus, iconografie, formulare, grile și stări; zero divergențe majore între Figma și Storybook.'),
('Media pentru produse prioritare','300 produse cu galerie validată; minimum 3 imagini utile/produs din surse existente sau producție nouă. Bugetul presupune reutilizare, nu 900 fotografii noi.'),
('Conținut vizual nou','30 clipuri scurte, 12 scene cumpărabile și 100 decupaje pentru configurator 2D; 3D/AR este extensie separată, după validarea calității și costului.'),
('Blocuri pentru marketing','Minimum 12 blocuri reutilizabile: hero, categorii, grilă, culori, serie, scenă, video, ghid, UGC, beneficii, ofertă, Pro; preview și programare.'),
('Traducere completă','RO, EN, DE, HU, BG, EL; toate înregistrările intră în flux. Revizie umană pentru 300 prioritare și toate textele legale/critice; restul trec verificări și eșantionare.'),
('Voce și UGC','Ghid de redactare, drepturi pentru foto/video, moderare, trasabilitatea consimțământului și interdicția recenziilor fabricate.')],[4.2,13.3])
p('Scenele compuse și randările sunt permise dacă produsul, culoarea, decorul și proporțiile rămân fidele. Imaginile de inspirație sunt marcate când reprezintă o simulare relevantă pentru decizia clientului. Declarații precum „rezistă la spălare” cer dovezi. Video pornește la cerere, cu poster, subtitrări și alternative text; nu blochează viteza paginii.')
h('Adresarea pe limbă')
table(['Limbă','Decizie inițială pentru B2C și Pro'],[('RO','B2C tu; Pro dumneavoastră.'),('EN','You, cu formulare directă; registru profesional în Pro.'),('DE','Sie în ambele zone; „Wählen Sie die passenden Stücke für Ihren Tisch.”'),('HU','Ön în ambele zone, validare de către vorbitor nativ.'),('BG','Вие, registru politicos; consecvență între interfață și suport.'),('EL','Plural politicos εσείς; verificare nativă a formulărilor.')],[2,15.5])
p('Ghidul de ton se validează în interviurile A1 și prin editorii nativi. O schimbare de adresare se aplică întregii limbi, inclusiv e-mailurilor. Devizul pe foto, video, scene, traducere și varianta de studio intern este în §17.2.')


p('Inventarul de 25 tipuri și 75 ecrane este domeniul de design. Implementarea include numai paginile și funcțiile susținute de contractele actuale. Schițele pentru personalizare, Club, liste și AI nu creează implicit obligația de a le dezvolta în backend; D03 le marchează explicit ca disponibile, condiționate sau viitoare.')


page('8.1 Funcții comerciale care diferențiază CESIRO')
h('Masa completă și completarea unei serii')
p('Clientul alege 2/4/6/8 persoane, buget și stil, apoi modifică piesele într-o compoziție vizuală React. Fiecare poziție are rol, SKU și cantitate; totalul este calculat de backend. Seturile comerciale rămân distincte de pachetele configurate. „Ce ai deja?” scade piesele selectate și oferă completări din aceeași serie; alternativele asemănătoare sunt numite explicit alternative.')
p('Tema livrează scene 2D și un configurator de selecție; acesta folosește produsele și operațiile de coș existente. Recomandările statistice sunt condiționate de un serviciu deja disponibil, fără creare de motor nou. Țintă de acceptare: 20 serii verificate, 12 scene, 100% calcule corecte de cantitate/preț, zero componente indisponibile confirmate tacit. 10 scenarii cu bugete diferite sunt evaluate de merchandising.')
p('Domeniu condiționat: asistentul, căutarea vizuală și semantică se conectează numai la servicii existente demonstrate în D01. În lipsa lor, tema livrează căutarea text și filtrele actuale; pragurile de mai jos devin specificații pentru o etapă separată, fără API nou în contractul temei.')


h('Asistent de cumpărare și căutare vizuală')
p('Asistentul răspunde la cereri precum „6 invitați, masă rustică, 400 lei” din catalog și politici aprobate. Afișează că este AI, citează produsele, verifică disponibilitatea și cere acțiunea explicită a clientului pentru adăugare în coș. Nu finalizează plăți și nu anulează comenzi. Vocea este opțională; utilizatorul vede transcrierea înainte de trimitere.')
table(['Funcție','Probă pentru extensia activată'],[
('Asistent contextual','200 cereri etalon, dintre care 40 adversariale; ≥90% răspunsuri utile și corecte evaluate uman; 0 acțiuni neautorizate; 100% prețuri/stocuri luate din API.'),
('Căutare după fotografie','100 imagini de test cu exemplare existente și 50 fără corespondent; Recall@5 ≥85% pe subsetul existent, identificări exacte false ≤2% pe setul evaluat.'),
('Căutare semantică','60 interogări/limbă; nDCG@10 ≥0,80 după judecată editorială; SKU exact pe prima poziție în 100% cazuri eligibile.'),
('Siguranță și continuitate','Fotografii cu EXIF eliminat, dimensiuni limitate, ștergere implicită după maximum 24 h; blocarea injecțiilor de instrucțiuni; căutare text și suport uman ca alternativă.')],[4.2,13.3])
p('Pentru funcția existentă activată, timpul AI se măsoară separat: primul răspuns p95 ≤4 s, propunerea completă p95 ≤10 s în sarcina agreată. Eșecul modelului nu blochează coșul. Seriile folosesc relațiile și câmpurile actuale; un model nou de graf sau embeddings aparține unei extensii separate.')

p('Pentru o extensie AI aprobată separat, costul operațional are plafon propus de 600 EUR/lună, exclus din bugetul temei din §17: țintă ≤0,06 EUR/sesiune asistată și cel mult 10.000 sesiuni bugetate. Costul include inferență, embeddings și procesarea foto; costul muncii de moderare se raportează separat. Alertă la 80%, oprire a cererilor AI plătite la 100%, fără oprirea căutării clasice sau a suportului. PoC verifică atingerea costului și a calității; plafonul nu promite volum garantat.')
p('Extensia după cumpărare adaugă 100 cereri etalon, 30 de izolare/atac, peste cele 200 de cumpărare: ≥90% răspunsuri corecte și utile, zero divulgări între clienți, zero schimbări comerciale executate de AI. Statusul se citește numai după autentificare sau identificare sigură; reclamația se transferă într-un formular confirmat de client și apoi la operator.')


page('8.2 Funcții vizuale și cadouri personalizate')
h('Vizualizare pe masă și în cameră')
p('Scenariul recomandat livrează un configurator 2D cu fotografii reale aprobate, decupaje coerente și 12 fundaluri de masă. Glazura nu este recreată dintr-un model generic. AR rămâne opțiune separată: 10 modele GLB/USDZ, dimensiuni verificate, evaluare vizuală pe 5 dispozitive și test comercial înaintea extinderii. Creșterea AOV este ipoteză de testat, nu efect deja demonstrat pentru CESIRO.')
p('Modul accesibil oferă aceeași selecție ca lista de piese, butoane adaugă/elimină, cantități editabile, ordine de focus stabilă și anunțuri ARIA pentru totaluri și erori. Nicio operație nu depinde exclusiv de drag and drop, vedere sau culoare.')


p('Personalizarea, listele, punctele Club și precomenzile sunt capabilități condiționate. Se proiectează vizual, dar se activează în tema de bază numai dacă există deja suport complet și verificat în platformă. Dacă nu există, se oferă cerere de ofertă/contact, favorite sau notificare prin funcțiile actuale. Nu se creează registre, motoare sau API-uri noi pentru a bifa aceste idei.')


h('Personalizare și producție')
p('Pilotul cu 10 produse oferă text, monogramă, dată și logo în zone aprobate de fabrică. Pentru fiecare opțiune se definesc fonturi, limită de caractere, culori, rezoluție, cost, cantitate minimă și termen. Clientul aprobă previzualizarea; backendul păstrează versiunea și generează fișa de producție. Logo-ul încărcat este verificat pentru format, malware și drepturi declarate.')
p('Fluxul: opțiuni → previzualizare → calcul și termen → confirmare client → comandă plătită → verificare operator → fișă producție → control calitate → expediere. Un fișier aprobat nu se regenerează cu alt text după plată. 20 comenzi simulate trebuie să reconcilieze opțiunea, prețul, fișierul și termenul; capacitatea reală și regulile de retur se aprobă înainte de vânzare.')
p('Contractul de producție este vectorial: serviciul Python existent trebuie să poată genera SVG sau PDF; dacă nu poate, generarea aparține unei extensii separate, în afara temei. Fișierul de producție se definește în milimetri, la scară 1:1, cu fonturi licențiate convertite în contururi, profil de culoare, zonă imprimabilă și toleranțe stabilite de fabrică. SVG-urile încărcate sunt sanitizate fără scripturi sau resurse externe; imaginile raster sunt acceptate numai dacă tehnologia fabricii le permite la rezoluția cerută. Fișierul final, previzualizarea și comanda au același identificator și hash; operatorul aprobă un proof fizic pe fiecare dintre cele 10 produse. Cele 20 simulări includ diacritice, logo invalid, limite de text și respingere de preflight.')
p('Pentru bunurile realizate efectiv după specificațiile clientului, checkoutul cere o bifă separată, nebifată implicit: „Am înțeles excepția de la dreptul de retragere pentru acest produs personalizat; drepturile legale pentru neconformitate rămân aplicabile.” Configurarea unui set din produse standard nu activează automat excepția. Bifa atestă informarea, nu creează o renunțare la drepturi. [L10b]')


h('Liste de nuntă și eveniment')
p('Clientul poate crea o listă privată sau partajabilă, cu data evenimentului și cantități dorite. Adresa destinatarului rămâne ascunsă invitaților. Rezervarea unei piese are expirare; două cumpărări simultane nu depășesc cantitatea disponibilă. Modificările, expedierea și retururile actualizează evidența prin operațiuni autorizate.')
p('Contribuțiile de grup sunt un pilot condiționat de PSP și validarea juridică a modului de colectare, rambursare și expirare. Versiunea de bază permite cumpărarea de produse întregi pentru listă. Livrarea la o dată aleasă se promite numai pentru produse și rute cu capacitate confirmată; altfel se afișează interval estimat.')
h('Precomenzi pe loturi')
p('Modulul folosește loturi de producție confirmate: disponibil promis = capacitate alocată − rezervări − tampon. Data, avansul, plata diferenței și efectul întârzierii sunt explicite. Lansarea pilotului cere 3 loturi validate de fabrică, reconciliere fără supravânzare și procedură de informare a clientului. Dacă sursa de producție nu este disponibilă, se oferă notificare de revenire în stoc, nu o dată inventată.')

p('Sursa inițială de capacitate este un registru de loturi administrat și semnat de planificatorul fabricii, importat zilnic, cu lot, SKU, capacitate alocată, termen, tampon și versiune. Dacă există ERP verificat în D01, adaptorul înlocuiește registrul fără schimbarea contractului. Date mai vechi de 24 ore suspendă precomenzile noi. Foaia de parcurs include un pilot manual controlat cu 3 loturi; integrarea ERP completă este extensie distinctă.')


page('8.3 Retenție și zona Pro')
p('În tema de bază se redesenează exclusiv funcțiile de retenție și Pro deja disponibile. Conectarea la servicii externe noi, registrul de puncte, prețurile contractuale noi sau API ANAF nou nu sunt incluse. Se păstrează cererea de ofertă și prețul public când platforma nu poate susține încă un flux specializat.')


h('Club CESIRO și comunicări')
p('Dacă platforma are deja un program de puncte, interfața îi prezintă nivelurile, expirarea și condițiile. Se verifică idempotența și ajustarea punctelor pentru retururile aprobate uman. Bonusurile nu condiționează o recenzie pozitivă. Salvarea decorului și notificările folosesc funcțiile și acordurile existente. Fără acestea, tema prezintă colecții și comunicări prin canalele disponibile.')
table(['Automatizare','Declanșare și control'],[
('Coș abandonat','Mesaj la 2 h și, opțional, la 24 h; oprire la cumpărare, dezabonare sau indisponibilitate; bază legală și preferințe verificate.'),
('După livrare','La 7 zile: îngrijire, recenzie și solicitare UGC; informările de serviciu sunt separate de promovare.'),
('Reaprovizionare Pro','Interval derivat din consum sau ales de client; propunere editabilă, fără comandă automată implicită.'),
('Aniversare și decor','Campanii pe preferințe explicite; limită comună de frecvență, maximum 2 mesaje promoționale/săptămână ca regulă inițială.'),
('Canale și afiliere','E-mail prioritar; SMS/WhatsApp numai cu consimțământ și furnizor activ. Atribuire și plăți de afiliere din comenzi validate, cu control de fraudă.')],[4.2,13.3])
p('Mystery Box primește descriere clară a conținutului posibil, valorii și condițiilor. Dezvăluirea animată este opțională și accesibilă. Abonamentul lunar intră în extensia ambițioasă numai după verificarea marjei, cererii, plăților recurente și a unei anulări ușoare realizate de client sau operator uman; nu se introduce un mecanism de noroc cu premii sau raritate fictivă.')
h('Prezentarea Pro peste capabilitățile existente')
p('Cont de firmă verificat, preț pe client și praguri de cantitate, cerere de ofertă, încărcare listă SKU/cantitate, comandă repetată și cerere de mostre. Logo-ul pentru corporate folosește același flux de personalizare. Prețurile negociate nu apar în cache public, feeduri sau alte conturi. Creditul comercial automat și finanțarea proprie nu fac parte din pilot.')
p('Recepție Pro: 10 scenarii cu roluri și clienți diferiți, import de 100 poziții cu erori explicate, zero scurgeri de preț contractual. O ofertă tipică de 20 poziții trebuie pregătită în maximum 10 minute din catalog validat. Serviciile de mostre au cost, transport și termen explicite.')

h('QR pe ambalaj și facturare Pro')
p('Pilot pe 20 serii: QR persistent către pagina seriei, cu limbă selectabilă, îngrijire și completare set. Codul identifică seria și campania, nu persoana; înscrierea în Club este opțională. Inserțiile în colete marketplace se folosesc numai după verificarea condițiilor canalului. Nu se importă contacte marketplace în CRM fără temei; indicatorii sunt cei din §4.')
p('Pro completează denumirea și adresa firmei după CUI prin serviciul ANAF sau un furnizor aprobat, cu confirmare de către client și completare manuală la indisponibilitate. Prețul cu/fără TVA este etichetat explicit; publicul B2C vede totalul cu TVA. Se păstrează cantitatea și prețul unitar. Datele de facturare se reconfirmă înainte de emitere pentru a reduce corecțiile, fără promisiunea imposibilă de zero stornări.')

p('D01 stabilește ce este disponibil în Pro: o capacitate prezentă poate fi expusă în interfață; o capacitate lipsă rămâne în registrul de extensii. Colectarea datelor firmei prin formularul actual este fallbackul pentru completarea automată după CUI.')


page('8.4 Autoservire după cumpărare')
p('Pagina Comenzile mele este accesibilă din cont sau prin link securizat, cu expirare și verificare suplimentară pentru operațiuni sensibile. Clientul fără cont are același acces la drepturi. Se afișează comanda, data estimată, statusul curierului cu ora ultimei actualizări, factura și istoricul cererilor; indisponibilitatea curierului nu este ascunsă sub un status inventat.')
table(['Flux','Activitate și criteriu'],[
('Produs sosit spart','Selectare piesă și cantitate, fotografie opțională sau canal alternativ, confirmare. Mediană ≤60 s pentru completarea cererii, nu pentru aprobarea înlocuirii. Notificare imediată, țintă de răspuns uman ≤1 zi lucrătoare; înlocuire gratuită potrivit promisiunii publice. Lipsa fotografiei nu stinge drepturile.'),
('Retragere','Intrare publică permanent vizibilă în perioada relevantă, plus link în cont și e-mail. Identificare minimă, selecție contract/produse, confirmare explicită și dovadă pe suport durabil cu dată/oră; nu cere cont sau motiv. Detalii în §12.1.'),
('Adresă și factură','Clientul trimite cererea; operatorul verifică etapa expedierii și confirmă schimbarea. Descărcarea facturii verifică proprietarul; linkul nu expune alte documente. Corecțiile fiscale rămân la financiar.'),
('Re-comandă','Piesele din istoric se propun în coș nou; prețul și stocul sunt actuale și confirmate. Produsele lipsă au alternative etichetate, fără substituire automată.'),
('Asistent','Citește numai comanda autorizată și politicile aprobate, explică pașii și pregătește recomandări. Nu anulează, nu aprobă retururi, nu rambursează și nu modifică marketplace-uri.')],[3.4,14.1])
p('Politica de înlocuire a produselor sosite sparte este deja publicată în FAQ și este păstrată în proiect. Responsabilul logistic definește stocul de înlocuire, costul și escaladarea; orice schimbare ulterioară a condițiilor cere analiză juridică și nu reduce retroactiv drepturile. Solicitările înregistrate nu sunt supuse aprobării AI. [S5]')


p('Autoservirea folosește rutele și stările actuale. Regula de lansare pentru lipsuri legale: responsabilul platformei remediază separat capabilitatea lipsă sau domeniul afectat nu se lansează. Tema nu maschează lipsa retragerii funcționale printr-un buton fără efect și nu creează un API paralel.')


page('9 Arhitectura temei pe platforma existentă')
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
('Alternativă contractuală','Păstrarea unei infrastructuri cu obiectiv inferior, de exemplu 99,5%, cere acceptarea documentată a riscului de către beneficiar înaintea lansării; nu este declarată echivalentă cu 99,9%.')],[4.1,13.4])
p('Un plan de îmbunătățire a găzduirii, dacă devine necesar, se cotează separat cu două oferte și acoperire de permanență. Auditorul a semnalat un server local partajat; această afirmație rămâne de verificat în operarea reală. Tema nu introduce un server Node sau un al doilea backend ca răspuns implicit.')

page('9.2 Cache și consistență fără API nou')
p('Tema folosește citirea și invalidarea existente. Catalogul public poate fi cache-uit conform contractului platformei; coșul, contul, checkoutul și prețurile private nu intră în cache public. Prețul/stocul afișat și cel verificat la comandă provin din aceeași autoritate. Clientul reconfirmă orice modificare de total, iar rezerva de stoc este cea existentă.')
table(['Demonstrație','Criteriu'],[
('Actualizare produs și stoc','Se urmărește traseul real al unei schimbări în mediu izolat până în pagina temei și coș; obiectiv p95≤5s, p99≤30s dacă platforma îl susține. Nu se declară un webhook nou ca prerechizită implicită.'),
('Date expirate','Pentru oferte dinamice: maximum 60 s de informație expirată, apoi revalidare sau afișare indisponibilă. Checkoutul validează întotdeauna la sursă, cu mecanismul existent.'),
('Teste de regresie','Ultima unitate, preț schimbat, stoc zero, sesiune expirată și acces Pro: zero comenzi confirmate pe date invalide, fără duplicarea logicii în React.'),
('Capabilitate lipsă','Se deschide deficit de platformă, nu un sistem nou în temă. Remedierea poate folosi mecanismul comun de evenimente/outbox dacă există; orice schimbare la acesta este proiect separat, cu aprobare și estimare.')],[4.2,13.3])
p('Directiva de audit Flask → Next.js este tratată prin eliminarea stratului Next.js separat din soluția aleasă. Nu există un cache Next.js nou de invalidat. Dacă în viitor se aprobă o arhitectură decuplată, devin relevante outboxul tranzacțional, versiunile, retryul, semnarea și purjarea separată CDN din analiza tehnică; acestea nu sunt lucrări comandate prin proiectul temei.')


page('10 Frontend și contractul de randare')
table(['Pagină','Randare și cache','Actualizare și siguranță'],[
('Homepage și Jurnal','HTML randat de Flask/cache la CDN; module dinamice distincte.','Invalidare la publicare; cache segmentat pe tenant, limbă și piață.'),
('Produs, categorie, serie','HTML indexabil, cache cu revalidare la eveniment; țintă de propagare ≤60 s.','Disponibilitatea afișată are dată; prețul/stocul se reverifică autoritativ la coș și comandă.'),
('Căutare și configurator','Rezultate dinamice și stare în URL; încărcare progresivă.','Index actualizat p95 ≤60 s; indisponibilitatea indexului are fallback text.'),
('Coș, checkout, cont, Pro','Dinamic; Cache-Control private/no-store.','Izolare de sesiune și tenant; fără prefetch al operațiunilor cu efect comercial.'),
('Recomandări și AI','Încărcare separată prin Suspense sau cerere dedicată.','Timeout și fallback; niciun blocaj al conținutului principal.')],[4,6.4,7.1])
p('ADR03 verifică invalidarea și consistența cacheului existent; eventualele lipsuri sunt deficite ale platformei. Înainte de plată se folosește validarea actuală a backendului; modificarea totalului este prezentată clientului. Versiunea și expirarea se folosesc dacă există în contract, fără un API nou. Cacheul vechi nu poate autoriza un preț sau o cantitate. Regulile de randare Flask și cache se documentează după comportamentul existent; nu se adaugă un server Next.js.')
h('Biblioteci și compatibilitate')
p('Bază propusă: Radix pentru primitive accesibile, Tailwind pentru stiluri, TanStack Query pentru stare server unde este necesară, React Hook Form și Zod pentru formulare. Validarea critică se repetă în Python. Componentele și tokenurile adminului se reutilizează numai unde nu leagă interfața publică de permisiuni administrative.')
p('Suport: ultimele două versiuni stabile de Chrome, Edge, Firefox, Safari și Samsung Internet, plus iOS și Android reprezentative. View Transitions și Speculation Rules sunt îmbunătățiri progresive, cu fallback și respectarea economisirii datelor. Prefetch numai pentru pagini publice sigure, fără rezervări, plăți, logout sau date personale.')
h('Verificare frontend')
p('Playwright verifică șase trasee: căutare–produs–coș; categorie–filtru–variantă; serie–completare; cadou–personalizare; checkout vizitator; Pro–ofertă. Se adaugă regresie vizuală, Lighthouse CI și testare manuală cu tastatură/cititor de ecran. Stările nefericite sunt obligatorii: timeout, preț schimbat, stoc epuizat, traducere lipsă și plată în așteptare.')

h('Buget de performanță pe rută')
table(['Rută','JS inițial comprimat','Alte limite pe mobil'],[('Homepage și produs','≤170 KB transferat','Imagine LCP ≤120 KB; ≤35 cereri inițiale.'),('Listare și căutare','≤200 KB','LCP ≤120 KB; ≤40 cereri inițiale.'),('Checkout','≤220 KB cod propriu','≤35 cereri proprii; SDK PSP separat măsurat și încărcat la pasul necesar.'),('Configurator','≤170 KB înainte de activare','Pachet 2D suplimentar ≤250 KB; activele se încarcă la cerere, fără blocarea produsului.')],[4.1,4.1,9.3])
p('CI măsoară un build de producție cu cache gol, la 390 px și rețea mobilă simulată. Fonturile, CMP și analytics autorizat intră în bugetul propriu. Depășirea blochează buildul; o excepție are ADR, proprietar și termen și nu suspendă pragurile CWV. Pachetele AI, 2D și AR nu sunt în încărcarea inițială a paginii de produs.')


page('11 Analiza diferențelor față de EVA')
p('„Observat” înseamnă identificat în fișiere, nu probat în producție. D01 cere demonstrația platformei actuale. Tema reutilizează funcțiile existente; un deficit de backend se consemnează separat.')
table(['Modul','Tratament în temă','Dovadă și limită'],[
('Catalog și conținut','Reutilizare','Resources products/categories/media/translations; se mapează câmpurile disponibile.'),
('Prețuri și promoții','Verificare și afișare','price_reference.py, promotions.py; prețul de catalog nu dovedește istoricul legal al reducerii.'),
('Comenzi și plăți','Reutilizare','orders, warehouse, payments/stripe_gateway.py; demonstrarea rezervărilor și reconcilierii.'),
('Conectoare și SEO','Reutilizare după probă','marketplace/curier, feeds.py, seo_engine.py; contracte și drepturi de verificat.'),
('Asistent admin','Rămâne în platformă','ai_assistant/guard.py și history.py; nu se construiește un asistent nou în temă.'),
('EVA documente','Nu dovedește e-Factura','Importul de documente de curier nu certifică SPV. Deficitul fiscal este separat.'),
('Serii și scene','Date actuale, selecție React','Fără catalog duplicat. Embeddings sau modele noi nu sunt incluse.'),
('Personalizare, liste, Club, loturi','Numai cu suport existent','D01 confirmă funcția; în lipsă, ofertă/contact prin flux actual sau concept viitor.')],[4.1,4,9.4])
h('Maparea la contractele existente')
p('D01 mapează ecranele la ruta, metoda, câmpurile, autentificarea, CSRF, erorile și efectele existente. Se reutilizează documentația disponibilă; nu se proiectează un API sau o versiune nouă.')
table(['Funcție','Dovadă statică și limită'],[
('Catalog și filtre','factory.py: GET /api/catalog/products; tenant, limbă, categorie, q, paginare și filtre. D01 confirmă răspunsul.'),
('Validare','POST /api/orders/validate este descris ca validare fără comandă. Înainte de test se verifică tot lanțul și REGULI.md.'),
('Comandă și cont','/api/orders și /api/account: UI și fluxuri actuale. Nu au fost apelate rute tranzacționale în această analiză.'),
('Teme','cms.theme_registry, active_theme, manifest/files/page_contracts; logica comercială rămâne comună.'),
('Plăți','Se demonstrează Stripe și walleturile actuale. Tema nu introduce un PSP sau conector fiscal nou.')],[4.1,13.4])
p('Nu se planifică migrații de schemă sau sincronizări paralele. Registrul deficitelor indică alternativa disponibilă, responsabilul platformei și efectul asupra recepției; remedierea backendului nu intră implicit în bugetul temei.')


page('12 Checkout plăți și operațiuni')
p('Checkoutul are o singură pagină cu progres clar: contact, livrare, plată și total final. Comanda fără cont este implicit disponibilă. Apple Pay/Google Pay sunt oferite dacă PSP-ul, dispozitivul, țara și contractul permit; plata standard rămâne disponibilă. Revolut Pay și BNPL sunt opțiuni evaluate după eligibilitate și marjă, fără promisiunea că un anumit furnizor operează pe toate piețele.')
table(['Flux','Cerință și probă de recepție'],[
('Total și preț','Recalcul server înainte de confirmare; TVA, transport, discount, card cadou și monedă explicite; sume reconciliate până la unitatea monetară minimă.'),
('Plată','Tokenizare prin PSP, autentificare când este cerută, webhook semnat, idempotentă și reconciliere. Retrimiterea evenimentului nu dublează comanda, factura sau punctele.'),
('Ultima unitate','Rezervare atomică și expirare; simultaneitatea coșurilor și evenimentele întârziate nu produc supravânzare. Plata tardivă intră în soluționare umană dacă stocul nu mai poate fi onorat.'),
('Stoc pe canale','Autoritate comună și reconciliere cu marketplace-urile; latență măsurată, tampon pe canal și oprirea promisiunii când sincronizarea este degradată.'),
('Livrare','Autocompletare localitate, hartă de lockere plus listă accesibilă, adresă manuală alternativă; termen estimat din stoc, capacitate și calendar curier.'),
('Transport gratuit','Prag configurabil pe piață și campanie; bara folosește aceeași bază eligibilă ca checkoutul. 500 lei este informație publică observată, nu regulă fixată definitiv.'),
('Facturare','Emiterea facturii conform politicii fiscale declanșează transmiterea e-Factura când este aplicabilă. Status SPV, retry, deduplicare, alarmă înaintea termenului legal și stornare operată autorizat.')],[3.2,14.3])
p('Backendul păstrează separat starea comenzii, a plății, a livrării și a documentului fiscal. Se documentează și se reutilizează stările existente corespunzătoare plății inițiate, în așteptare, autorizată, confirmată, eșuată și rambursată, cu tranziții permise și jurnal. Nu se consideră plătită o comandă doar din revenirea browserului de la PSP. [L5]')
p('Regulile locale din REGULI.md sunt constrângeri de proiect: AI nu anulează comenzi și nu execută retururi/rambursări, nici în teste. Testele automate folosesc simulări izolate, fără scrieri spre sisteme reale. Validarea fluxurilor sensibile revine unui operator uman. Scrierile spre marketplace-uri cer autorizarea expresă a proprietarului; automatizarea AWB respectă politica pe canal. [I5]')

page('12.1 Retragere online și integrare fiscală')
p('Funcția de retragere prevăzută de art. 11a introdus prin Directiva 2023/2673 este cerință de lansare, cu data europeană de aplicare 19 iunie 2026. Registrul juridic va atașa transpunerea națională și excepțiile pe piață. Linkul din e-mail completează funcția vizibilă din interfață; nu o înlocuiește. Fluxul acceptă declarația clientului fără aprobare prealabilă, transmite fără întârziere confirmarea pe suport durabil, cu conținut și dată/oră, și păstrează dovada. [L10]')
p('Notificarea de retragere este distinctă de anularea operațională, aprobarea returului și rambursare. Clientul declanșează declarația prin aplicația deterministă; AI nu efectuează aceste operațiuni. Se permit identificarea fără cont, produse din comenzi mixte și recuperarea după eroare. În caz de dispută privind excepția pentru personalizare, cererea poate fi înregistrată pentru analiză umană. Nu se cere fotografie sau motiv pentru retragere.')
p('Recepție: 12 scenarii, inclusiv client fără cont, limbă diferită, retragere parțială, dublu click, expirare link, indisponibilitate e-mail și bun personalizat. Dovada se oferă imediat în interfață; e-mailul se reîncearcă și se alertează. Testele cu efecte sensibile sunt conduse de operator uman în mediul autorizat; AI nu execută anulări sau rambursări nici în simulări.')
h('Integrarea fiscală existentă și deficitul separat')
p('Tema folosește rezultatul facturării și documentele generate de platforma existentă. Nu implementează un API ANAF, OAuth2 sau un adaptor fiscal nou. Dacă D01 nu demonstrează transmiterea fiscală aplicabilă, responsabilul platformei primește un deficit separat, blocant pentru domeniul afectat. Cerințele tehnice de mai jos descriu acea eventuală remediere, în afara bugetului temei. [T7]')
p('Contabilul fixează termenul legal și regulile de emitere în registrul versionat. Alarmă la 50% din termen, la 24 ore înainte și imediat la respingere; retry pentru erori tranzitorii, intervenție pentru erori de date. Nu se transmit duplicate după timeout fără verificarea stării. Recepție pe 12 cazuri: B2C/B2B, monedă, TVA, duplicate, expirare token, respingere, indisponibilitate și corecție fiscală realizată uman. Documentele alimentare sunt gestionate separat în §13.2.')


p('Aceeași regulă se aplică retragerii: tema expune funcția existentă numai dacă aceasta îndeplinește fluxul legal. Dacă ruta actuală nu îl susține, lipsa este escaladată ca remediere a platformei; nu se lansează un buton nefuncțional și nu se construiește un API paralel sub denumirea de temă.')


page('13 Performanță accesibilitate și securitate')
table(['Domeniu','Criteriu de acceptare','Metodă'],[
('Experiență reală','LCP ≤2,5 s, INP ≤200 ms, CLS ≤0,1 la percentila 75, separat mobil/desktop.','RUM pe 28 zile; înainte de trafic suficient, teste de laborator și monitorizare după pilot. [T2]'),
('API și căutare','API citire p95 ≤300 ms; căutare text p95 ≤500 ms; erori tehnice <0,5%.','Măsurate fără rețeaua utilizatorului; warm/cold și dependențe raportate separat.'),
('Încărcare','Catalog curent ×6 limbi și creștere 2×; cereri/s și comenzi/min la 10× vârful observat.','Rampă, vârf 15 min, anduranță 2 h; profil tranzacțional real. Fără baseline se testează profil convenit, nu o capacitate pretinsă.'),
('Accesibilitate','WCAG 2.2 AA drept condiție contractuală; zero defecte A/AA deschise în fluxurile livrate.','Automat + audit manual tastatură, zoom 200–400%, NVDA/VoiceOver, contrast și documente. [T3, L4]'),
('Securitate','Zero vulnerabilități critice/înalte exploatabile; izolare tenant și client.','Test autorizare, CSRF/XSS, rate limit, upload, sesiune, jurnal și scanare dependențe.'),
('Operare','Disponibilitate țintă 99,9% lunar; RPO ≤15 min, RTO ≤60 min, obiective ale platformei care trebuie probate în ADR04, separat de livrarea temei din §9.1.','Backup și restaurare demonstrată, runbook și două persoane instruite; dependențe PSP raportate separat.')],[3.4,7.3,6.8])
p('WAF și protecția anti-boți limitează încercările automate, card testing și abuzul formularelor. Turnstile este candidat, cu alternativă accesibilă și evaluarea confidențialității; nu promitem absența oricărei verificări. Coada virtuală se activează doar dacă testul de sarcină arată necesitatea.')
p('Autentificarea rămâne cea existentă. Passkeys, link magic și social login se afișează numai dacă sunt deja susținute și verificate; tema nu construiește un sistem nou de identitate. Comanda nu creează automat cont fără informarea și alegerea clientului. Datele de card nu sunt stocate de CESIRO. Prețurile Pro, sesiunile și datele personale nu intră în cache comun sau în telemetrie.')
p('Se livrează informații publice despre accesibilitatea serviciului și un canal de sesizare. Legea 232/2022 include comerțul electronic de la 28 iunie 2025 și excepții, inclusiv pentru anumite microîntreprinderi; aplicabilitatea se verifică pentru entitatea vânzătoare. WCAG 2.2 AA este standardul ales al proiectului, fără a-l confunda automat cu textul integral al obligației legale. [L4]')

page('13.1 Conformitate și protecția datelor')
table(['Cerință','Aplicare în proiect','Probă și responsabil'],[
('GPSR','Oferta online afișează identificarea produsului, producătorul și contactele, operatorul UE unde este cazul, avertismentele relevante; conform art. 19 și domeniului aplicabil.','Fișă pe familie și piață; verificare 100% a câmpurilor obligatorii pentru lotul publicat; juridic + date. [L1]'),
('Contact alimentar','Reg. 1935/2004 și normele specifice ceramicii; documentație și trasabilitate, declarație de conformitate când este cerută.','Documente reale asociate produselor/loturilor; nicio confirmare generată de AI; calitate fabrică. [L2]'),
('Reduceri de preț','Istoric al prețului efectiv și preț anterior potrivit regulii de 30 zile, cu tratamentul excepțiilor aplicabile.','Teste pe promoții succesive, produs nou, istoric incomplet și monedă; juridic + comercial. [L3]'),
('GDPR și cookie','Minimizare, scop, retenție, contracte cu furnizorii, drepturi și consimțământ acolo unde este cerut.','CMP cu retragere simplă; fără marketing înainte de acord în fluxurile care îl cer; DPO/juridic. [L8]'),
('AI și transparență','Informare că asistentul este AI, gestionarea conținutului sintetic și a obligațiilor aplicabile rolului CESIRO.','Etichete și jurnal; revizuire art. 50 și a normelor în vigoare înainte de activare; juridic. [L6]'),
('e-Factura și consumator','Transmiterea facturilor emise când este obligatorie; retur, garanții, reclamații, personalizare și precomenzi explicate înainte de plată.','Validare contabilă/fiscală, flux de erori și dovada transmiterii; termene parametrizate. [L5]'),
('Pașaport de produs','Fișă voluntară de proveniență, materiale, îngrijire și dovezi; compatibilă cu evoluția cadrului DPP.','Fără afirmația că DPP este deja obligatoriu pentru toate produsele ceramice; verificare acte delegate. [L7]')],[3.3,8.1,6.1],small=9.8)
p('Consent Mode v2 și taggingul server-side transmit și respectă opțiunile utilizatorului; nu înlocuiesc consimțământul sau conformitatea GDPR. Mod implicit conservator: tagurile neesențiale nu pornesc înainte de acord. Replay de sesiune este dezactivat inițial; orice activare cere mascarea integrală a câmpurilor și o evaluare separată. [T4]')
p('Vânzătorul public identificat la 21 octombrie 2026 este CESIRO MARKET S.R.L., cod fiscal RO45050769, Alba Iulia. Producătorul ceramicii proprii este atribuit CESIRO S.A. din Sighișoara numai cu documentație per produs; produsele terțe au producătorul real. Contractele, factura și rolurile GDPR se reconciliază cu documentele societăților în A0. Identitatea vânzătorului nu dovedește originea tuturor articolelor. [S6]')

page('13.2 Conformitatea familiilor și documentelor')
table(['Domeniu și responsabil','Cerință de lansare și probă'],[
('Chimice CLP\nJuridic și date','Pericolele relevante sunt vizibile înainte de cumpărare, în limba pieței, cu date din fișa furnizorului. Dicționarul §2 și blocarea §3 sunt testate pe toate produsele chimice publicate. Calendarul revizuirii CLP este separat: unele cerințe de publicitate/vânzare la distanță sunt amânate la 1 ianuarie 2028 prin Reg. 2025/2439; proiectul pregătește datele de acum, fără a numi toate cerințele noi deja obligatorii. [L11]'),
('Biocide\nJuridic și achiziții','Clasificare și drept de comercializare pe țară, autorizare, utilizări, avertismente și mesaj art. 72 în publicitate; respingerea afirmațiilor înșelătoare de siguranță. Fără autorizație necesară sau informații aprobate, produsul nu este cumpărabil. [L13]'),
('Detergenți\nAchiziții și calitate','Link către lista publică de ingrediente și documentele aplicabile, revizie și limbă. Excepțiile pentru produse exclusiv profesionale se documentează. Reg. 648/2004 rămâne reperul tranzitoriu; noul Reg. 2026/405 are aplicare generală din 23 septembrie 2029. [L14]'),
('Preț pe unitate\nComercial și juridic','Cantitate netă, unitate de referință și reguli de afișare; exemple și excepții conform HG 947/2000 și normelor pieței. B2C cu TVA; Pro poate vedea separat baza fără TVA. Recepție pe 20 cazuri, inclusiv pachete mixte și reduceri. [L12]'),
('Retragere și SAL\nJuridic și suport','Funcție §12.1, date vânzător și SAL ANPC în subsol și mesaje relevante. Linkurile sunt verificate; nu se reactivează vechea platformă europeană SOL/ODR închisă. Nu se declară orice icon sau e-mail o obligație universală fără temei. [L10, L15]'),
('Contact alimentar\nCalitate fabrică','Asociere produs–material–lot–document, declarații și rapoarte reale. Document public aprobat accesibil din fișă; acte interne complete cu acces pe rol și jurnal. Original cu hash și revizie, scanare malware, previzualizare accesibilă. Publicarea unui PDF integral de lot pentru orice produs nu este presupusă obligație universală. [L2]')],[4.1,13.4],small=9.8)
p('R09 verifică 100% din lotul care urmează să fie cumpărabil, cu matrice aplicabil/neaplicabil justificată, emitent, valabilitate, limbă și responsabil. Documentele expirate sau revocate suspendă oferta afectată și declanșează revizuirea incidentului. Registrele de conformitate au termen de revalidare înaintea fiecărui val; informația generată de AI nu este document de conformitate.')


page('14 SEO localizare și conținut cumpărabil')
p('RO, EN, DE, HU, BG și EL sunt tratate ca șase versiuni editoriale. Piața și țara de livrare determină prețul, taxele și oferta: RON pentru RO, HUF pentru HU, EUR pentru DE/EL/BG; EN urmează țara selectată. Nu se deduce țara numai din limbă sau IP. Bulgaria a adoptat euro la 1 ianuarie 2026; istoricul BGN se păstrează ca istoric, fără a deveni moneda checkoutului nou. [L9]')
h('Continuitate și indexare')
p('Inventar pentru 100% din URL-urile cunoscute, cu destinație și motiv. URL-urile stabile se păstrează când este posibil; schimbările folosesc redirect 301 direct și relevant, fără lanțuri sau redirecționări în masă la homepage. Canonical, hreflang reciproc, x-default unde este potrivit și sitemapuri separate pe limbă/tip se validează automat. Arhivele fără echivalent au tratament 404/410 justificat; lipsa temporară de stoc nu șterge pagina.')
p('Numai combinațiile de filtre aprobate editorial sunt indexabile. Checkoutul, conturile, listele private și rezultatele cu parametri infiniți nu devin pagini SEO. Migrarea graduală servește aceeași experiență utilizatorilor și roboților din aceeași cohortă; nu folosește cloaking. Monitorizare zilnică a paginilor prioritare, erorilor și indexării în primele 30 zile.')
h('Conținut și descoperire prin AI')
p('Jurnal CESIRO: 30 ghiduri până la finalul T4, dintre care 10 în T2: alegerea setului, numărul de piese, întreținerea glazurii, completarea seriei, cadouri și mese sezoniere. Fiecare are autor/responsabil, data reviziei, răspunsuri utile și produse eligibile. Video scurt cumpărabil, subtitrat, completează ghidurile; nu substituie textul indexabil.')
p('JSON-LD Product/Offer, disponibilitate, livrare și politici de retur reflectă exact pagina și piața; recenziile se includ numai dacă sunt reale și eligibile. FAQ este util cititorului; nu promitem rich results pentru magazine. Google precizează că funcțiile sale AI nu cer optimizări speciale suplimentare. llms.txt poate fi un experiment documentar, fără garanție de indexare, citare sau recomandare. [T5]')
h('Feeduri și canale')
p('Google Merchant și Meta primesc ID-uri stabile, GTIN unde există legitim, preț, stoc, imagini, țară, limbă, transport și retur din aceeași sursă. TikTok și afilierea se activează pentru piețe și conturi eligibile; nu presupunem disponibilitatea TikTok Shop în toate cele șase piețe. Erorile, respingerile și diferențele de preț se monitorizează; țintă ≥98% articole eligibile acceptate în feed, fără a promite aprobarea externă.')

h('Conținut distinct și schema de limbă')
p('Site-ul direct publică ghiduri de utilizare, serii și scene originale; marketplace-urile primesc descrieri concise, păstrând aceleași informații esențiale de siguranță, cantitate și material. Conținutul diferit este o alegere editorială, nu garanție de clasare sau singura măsură SEO.')
p('Schema inițială hreflang: ro, de, hu, bg, el și en generic; x-default către selectorul neutru de piață. Fiecare pagină are canonical propriu și legături reciproce numai către echivalente existente. Dacă apar oferte EN distincte pe URL-uri de țară, se adaugă en-GB/en-IE sau alte coduri reale, fără a duplica artificial variante en-XX. Țara selectată nu schimbă arbitrar canonicalul.')


page('15 Măsurare și experimente')
p('Tema instrumentează evenimentele în soluția de analytics și CMP existentă, verificată în D02; datele operaționale vin din rapoarte agregate disponibile. GA4 este reperul de schemă de evenimente. Server-side tagging, PostHog sau GrowthBook se folosesc numai dacă există deja; adoptarea unui serviciu nou se estimează separat. Experimentele folosesc mecanismul actual sau rămân în plan până la asigurarea lui.')
table(['Evenimente și indicatori','Definiție sau control'],[
('Traseu de cumpărare','view_item_list, select_item, view_item, search, add_to_cart, begin_checkout, add_shipping_info, add_payment_info, purchase; transaction_id pentru deduplicare.'),
('Funcții noi','collection_view, scene_add_to_cart, table_config_complete, visual_search, ai_recommendation_click, personalization_submit, registry_purchase, pro_quote_submit.'),
('Retenție','Cohorte lunare, recumpărare la 90 zile, venit net/client la 180 zile și marjă cumulată. LTV predictiv se etichetează estimare, nu venit realizat.'),
('Calitatea livrării','Spargeri = comenzi cu incident / comenzi livrate; cost incident, retur și contact suport. CSAT la livrare și NPS la 30 zile, cu rata de răspuns.'),
('Marketing','Conversie e-mail = comenzi atribuite / destinatari eligibili; click și dezabonări. Deschiderile sunt informative, afectate de protecția confidențialității.'),
('Achiziție','Cota canalului direct din venit reconciliat și trafic organic non-brand din Search Console; nu se confundă traficul măsurat cu toți vizitatorii.')],[4.6,12.9])
h('Disciplina experimentelor')
p('Minimum 15 ipoteze ordonate prin impact, încredere și efort; țintă de două experimente pe lună dacă traficul permite. Un singur obiectiv principal, populație eligibilă, unitate de randomizare utilizator, expunere stabilă, excluderi și durată stabilite înainte de start. Se folosesc α=5%, putere 80% și efect minim detectabil calculat din baza reală; fără oprire la primul rezultat favorabil.')
p('Portofoliu inițial: căutare în antet, intrare după decor, swatchuri, scene 2D, recomandare pe persoane, pagină de cadou, ambalaj, bară transport, wallet, guest checkout, dovadă origine, UGC, completare serie, previzualizare personalizare, ghid cumpărabil. Calendarul urmărește dependențele și evită experimente care se influențează.')
p('Guardrails: marjă de contribuție/comandă, erori de plată, retururi, spargeri și suport. O scădere a marjei >2 pp sau creștere a spargerilor >0,3 pp declanșează analiză și oprirea variantei dacă este confirmată. Pentru trafic insuficient se raportează intervale și rezultat neconcludent; interviurile UX nu sunt prezentate ca dovadă A/B.')

p('D02 calculează durata realistă pentru MDE 10% relativ la conversia actuală, α=5%, putere 80%, alocare 50/50 și trafic eligibil după consimțământ. Exemplu de dimensionare, nu baseline CESIRO: de la 2,0% la 2,2% necesită aproximativ 80.600 utilizatori/grup pentru un test bilateral simplu; la 10.000 eligibili/săptămână în total ar dura circa 16 săptămâni. Durata se recalculează pentru unitatea reală de randomizare și sezonalitate; 2 teste/lună nu este un angajament fără trafic suficient.')


page('16 Activități calendar și lansări graduale')
p('Planul de 16 săptămâni acoperă o temă integrată cu backendul și API-ul existente. Calendarul de 26 săptămâni pentru întregul program de funcții noi nu este aplicat acestui domeniu. Capacitățile indisponibile sunt scoase din implementarea de bază, cu păstrarea conceptelor de design și a condițiilor de activare.')
table(['Etapă','Activități și livrabile','Ieșire'],[
('T0 S1–2','D01 actual, contracte de pagini/rute, D02, inventar media, ADR01–04 și registrul funcțiilor disponibile.','Sursă și Docker identificate; nicio presupunere de API nou.'),
('T1 S1–4','Trei concepte, teste UX, navigare după utilizări, design system și prototipuri.','Direcție aprobată ; 25 tipuri de design marcate după suportul platformei.'),
('T2 S3–10','Temă înregistrată, asseturi React, home/listare/produs, filtre, traduceri, 300 prioritare și 10 ghiduri.','Integrare pe contracte existente, R01/R02/R06 pe lot.'),
('T3 S7–12','UI pentru coș/checkout/cont, scene și configurator 2D, Pro în limitele actuale, testare de regresie.','20 serii, 12 scene; zero logică de preț/stoc duplicată; funcțiile condiționate au fallback.'),
('T4 S11–14','Accesibilitate, performanță, securitate UI, conținut final, 30 ghiduri și 20 SKU-uri de test pe familii.','R03–R09; deficitele legale și operaționale rezolvate de proprietarii platformei sau domeniu blocat.'),
('T5 S15–16','Preview, pilot și comutare graduală a temei, instruire și predare.','Rollback ≤15 minute; monitorizare și criterii comerciale.'),
('T6 după lansare','90 zile de măsurare și optimizare, distinct de construcția temei.','R10 cu baseline și limite statistice.')],[2.6,9.3,5.6],small=9.8)
p('Drumul critic este D01 → design validat → integrare pe contracte actuale → regresie checkout → lansare. Media și documentele sunt fluxuri paralele; sub debitul editorial minim se reduce lotul eligibil sau se prelungește calendarul. Nu se rezolvă prin inventarea datelor. Sprinturi de două săptămâni și decizie PO în trei zile lucrătoare.')
p('Trafic 5% → 20% → 50% → 100%, minimum 48 h și volum suficient. Eroarea de total, plată, stoc sau acces oprește creșterea. Limita inferioară a intervalului pentru conversie trebuie să depășească −5% relativ; dacă traficul nu ajunge, se poate aproba doar extindere limitată și documentată. Se schimbă tema, fără pierderea comenzilor și fără restaurare destructivă a bazei.')

page('17 Efortul temei și capacitatea echipei')
p('Deviz de jos în sus, 8 ore/zi-persoană, pentru reutilizarea platformei. Coloana Integrare Python înseamnă citirea contractelor, configurarea/înregistrarea temei și ambalarea asseturilor; nu dezvoltare de sistem API, ERP, căutare ori contabilitate. Interval 160–200 zile include maximum 25% incertitudine după baza detaliată.')
wbs=[('N01 Inventar și contracte existente',3,2,3,2),('N02 UX și concepte',12,0,0,4),('N03 Componente React',6,14,0,4),('N04 Home listare produs',4,18,2,6),('N05 CMS navigare și colecții',2,6,2,2),('N06 UI coș și checkout actual',2,8,2,6),('N07 Cont și suport existent',1,5,1,3),('N08 Configurator 2D și scene',2,8,0,4),('N09 Limbi SEO și măsurare',1,3,2,4),('N10 Integrare Docker și verificări',0,2,4,6),('N11 Coordonare și predare',2,0,0,2)]
assert sum(sum(x[1:]) for x in wbs)==160
totals=[sum(x[i] for x in wbs) for i in range(1,5)]
table(['Activitate','UX','React','Integrare Python','QA','Total'],[(*x,sum(x[1:])) for x in wbs]+[('TOTAL',*totals,160)],[8,1.2,1.5,2.7,1.2,2.9],small=9.5)
p('La 80 zile lucrătoare nominale, media este 2–2,5 echivalenți normă întreagă, vârf 3–4. PO CESIRO minimum 2 zile/săptămână și doi editori ×50 zile sunt contribuții interne distincte; timpul lor se evaluează la costul intern real. Fotografii și traducătorii nu sunt presupuşi incluși în acești editori.')
p('Conceptele avansate rămân în §8 cu probe de acceptare, însă sunt activate numai dacă D01 confirmă suportul actual. AI nou, căutare vectorială nouă, registru Club, liste de eveniment fără suport, motor de personalizare, conector fiscal și migrarea găzduirii nu sunt ascunse în cele 160–200 zile.')

page('17.1 Bugetul temei și costurile separate')
p('Sume de planificare fără TVA, nu cotații. Se cer două oferte pe același domeniu. Tarife ipotetice: echipă locală cu EVA 250–400 EUR/zi; furnizor complet 400–550 EUR/zi. Reutilizarea este premisa contractuală, nu un API nou inclus în preț.')
table(['Variantă','Componente de cost','Total cu rezervă 15%'],[
('Temă cu echipă locală/EVA','160–200 zile ×250–400 =40.000–80.000; media 19.460–35.100; cost tehnic incremental 6 luni 900–2.400; mentenanță temă 6 luni 4.500–9.000.','74.589–145.475 EUR'),
('Același domeniu cu furnizor complet','160–200 zile ×400–550 =64.000–110.000; aceleași media, operare incrementală și mentenanță.','102.189–179.975 EUR'),
('Extensii separate','Se estimează separat numai după D01 și o decizie distinctă. Prețul presupune reutilizarea API-urilor; nu promite servicii backend inexistente.','Neincluse în bugetul temei')],[4.1,9.1,4.3])
p('Total = (efort×tarif + media + cost tehnic incremental + mentenanță)×1,15. Costul incremental 150–400 EUR/lună acoperă alocația de staging/CDN/monitorizare pentru temă, dacă este necesară. Găzduirea actuală rămâne cost existent; eventuala modernizare HA/PITR se cotează separat, fără economii sau disponibilitate pretinse.')
p('Mentenanță temă 750–1.500 EUR/lună pentru 6 luni; încă 6 luni adaugă 5.400–11.400 EUR împreună cu operarea incrementală, înainte de rezervă. Nu include permanență de infrastructură 24/7, consum AI nou, comisioane, publicitate, transport, spargeri sau costul intern CESIRO. Bugetul AI de 600 EUR din §8 este doar plafon pentru o extensie aprobată ulterior.')
p('Scenariul media din §17.2 poate fi redus prin studio în fabrică, înlocuind liniile externe. Catalogul complet este contabilizat; cele 300 produse sunt prioritare editorial. Oferta finală precizează ce active există și ce trebuie produse, fără dublarea timpului furnizorului și a editorilor beneficiarului.')


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
p('Clauză contractuală propusă: 90 zile garanție pentru defectele temei față de specificația acceptată, inclusă în dezvoltare. Extinderea la 180 zile se cere în ofertă. Mentenanța temei de 750–1.500 EUR/lună este distinctă de operarea backendului, de permanența infrastructurii și de dezvoltarea unor capabilități noi.')
table(['Severitate','Răspuns și restabilire propuse','Canal și responsabil'],[
('P1 magazin/plăți/acces compromis','În programul contractat: răspuns ≤1 h, restabilire sau izolare sigură ≤8 h; pentru recuperarea datelor se aplică obiectivul mai strict RTO ≤60 min din ADR04.','Alertă externă + telefon; DevOps și lider tehnic, doi înlocuitori nominalizați.'),
('P2 funcție majoră degradată','Răspuns ≤4 h lucrătoare, soluție temporară ≤1 zi lucrătoare, termen de remediere comunicat.','Ticket și jurnal incident; proprietar de modul.'),
('P3 defect minor','Răspuns ≤2 zile lucrătoare; plan în următorul sprint.','Backlog acceptat de PO.')],[3.6,8.9,5])
p('Programul mentenanței temei este 09–18, luni–vineri, Europe/Bucharest, exceptând sărbătorile. Pentru P1 în afara programului se aplică exclusiv contractul separat de operare, dacă există. Permanența 24/7 pentru platformă este serviciu separat; fără contract activ nu se declară inclusă în mentenanța temei. Restabilirea poate fi rollback sau dezactivare sigură; cauza și remedierea definitivă se documentează în maximum 5 zile lucrătoare pentru P1. SLO 99,9% rămâne separat de ținta de răspuns.')
p('Patchuri critice exploatabile: izolare imediată, plan în 24 ore și aplicare validată conform urgenței; dependențe revizuite lunar. Backupurile și restaurarea se verifică lunar; drepturile trimestrial. Predarea include accesuri deținute de beneficiar, exporturi, configurări, manual de operare și inventar licențe, fără dependență de un singur furnizor.')


page('17.4 Guvernanță dependențe și riscuri')
table(['Responsabil','Răspundere și decizie'],[
('Sponsor CESIRO','Buget, portofoliu, entitate vânzătoare și promisiuni comerciale.'),
('Product Owner CESIRO','Priorități și acceptare; persoana se nominalizează în A0, cu înlocuitor și termen de decizie.'),
('Lider tehnic și DevOps','ADR, reutilizare, integrări, securitate, restaurare și lansare; minimum două persoane cu acces și instruire.'),
('Responsabil date și merchandising','Inventar, ABC, scor, serii și eligibilitate; aprobă ieșirea loturilor din remediere.'),
('UX content și CRM','Cercetare, media, traduceri, accesibilitate UX, comunicări și experimente.'),
('Fabrică logistică financiar juridic','Producție personalizată, capacitate loturi, spargeri, facturare și conformitate; drept de oprire pe domeniul propriu.')],[5,12.5])
table(['Risc','Măsură și prag','Responsabil'],[
('Infrastructură partajată','ADR04 și probă de failover înainte de lansare; resurse izolate și alertare externă.','DevOps'),
('Copii divergente EVA','Versiuni comune, configurare per tenant, compatibilitate API și migrații pe două configurații.','Lider tehnic'),
('Cod diferit de producție','Demonstrație a versiunii instalate și contracte API înainte de estimarea fixă.','Lider tehnic'),
('Date slabe sau acte lipsă','Loturi, scor și condiții obligatorii; zero publicări comerciale neeligibile.','Date + juridic'),
('Dependență de o persoană','Documentație, pairing și exercițiu de restaurare condus de a doua persoană.','DevOps'),
('AI greșit sau costisitor','Etalon, plafon lunar, oprire automată la epuizare și fallback; măsurare cost/cerere.','AI + PO'),
('Stoc și plăți divergente','Reconciliere, outbox/idempotentă, tampon și alarme; intervenție umană pentru excepții.','Backend + logistică'),
('Canibalizare marketplace','Marjă și cotă directă pe canal; servicii exclusive măsurabile, fără război automat de preț.','Comercial'),
('Capacitate fabrică sau personalizare','Pilot de 10 produse, fișă aprobată, cantitate și termen confirmate; flag dezactivat până la validare.','Fabrică'),
('Legal sau piață nepregătită','Matrice pe țară și familie; revalidare înainte de val, stop pentru domeniul afectat.','Juridic'),
('Conținut peste buget','Inventar media și rată de editare în A1; variația >10% din efort cere recalcul transparent.','PO + content')],[4.2,10.6,2.7],small=9.6)
p('Nu sunt incluse în costurile de mai sus: buget media plătită, comisioane PSP/marketplace, transport și spargeri, materiale și capacitate de fabricație, personal CESIRO sau achiziție hardware AI. Bugetul media/lingvistic extern nu dublează zilele de orchestrat/editat date; cele două categorii se reconciliază în deviz. Contribuțiile financiare de grup, abonamentul Mystery Box, creditul Pro, AR și integrarea ERP avansată sunt extensii separate.')

page('18 Recepție și probe cerute')
table(['Cod','Livrabil și criteriu','Probă de închidere'],[
('R01','100% rânduri și câmpuri sursă contabilizate; praguri de calitate și condiții obligatorii îndeplinite pentru fiecare lot publicat.','D01 semnat, raport diferențe, scoruri și jurnal de aprobare.'),
('R02','Design pentru 25 tipuri și 75 ecrane; implementare numai pentru cele susținute de platformă. Stări/tokenuri și SUS ≥80 în runda finală.','Fișiere editabile, prototip și raport cu sarcini, participanți și rezultate.'),
('R03','≥90% succes pe sarcini critice; mediană până la primul add-to-cart ≤60 s; checkout nou ≤90 s și wallet ≤30 s.','2×8 participanți; timpi măsurați cu datele pregătite, separat de așteptarea PSP/SCA; erori și percentile raportate.'),
('R04','Zero defecte critice deschise în totaluri, stoc, plăți, tenant și facturare.','Teste de contract, integrare izolată și demonstrații umane autorizate; fără anulări automate de AI.'),
('R05','20 serii și 12 scene pentru tema de bază. Pragurile AI/personalizare/Club din §8 se recepționează numai dacă există suport actual și funcția este inclusă explicit; altfel rămân extensii.','Etaloane, rapoarte de relevanță, fișe de producție și fallbackuri demonstrate.'),
('R06','Toate URL-urile inventariate au decizie; 0 erori critice pe URL-uri prioritare; 6 limbi cu conținut critic validat.','Crawl comparativ, mapare redirect, hreflang și teste monetare/țară.'),
('R07','Criteriile din §9.1, §9.2, §10 și §13, accesibilitate AA și lipsa vulnerabilităților critice/înalte.','Rapoarte laborator/RUM, încărcare, accesibilitate manuală și securitate.'),
('R08','Rollback temă ≤15 min; probe RPO/RTO ale platformei existente, două persoane instruite și monitorizare. Deficitele infrastructurii sunt separate.','Exercițiu documentat, runbook, alerte și responsabil de permanență.'),
('R09','Matrice legală pe entitate/piață/familie: retragere online, CLP, biocide, ingrediente, preț unitar, SAL, documente alimentare și aprobarea domeniilor aplicabile.','Politici, documente, CMP, dovada facturării și avize operaționale.'),
('R10','Dashboard și raport la 90 zile, cu baseline, guardrails, atribuiri și incertitudine.','D02, evenimente reconciliate, experimente și rezultate explicate.')],[1.4,8.1,8],small=9.8)
p('Setul critic include: ultima unitate simultană, webhook duplicat și reordonat, plată întârziată, preț schimbat, pierdere sesiune, cont Pro izolat, serie greșită, traducere numerică incorectă, fișier personalizare invalid și lipsa sursei AI. Pentru retur/rambursare și anulare, numai operatorul uman execută probele autorizate în mediul permis.')
p('Nicio acceptare nu este dedusă din simpla existență a unui fișier sau din trecerea testelor automate. Se livrează raportul, data, versiunea și responsabilul. Neconformitățile critice blochează funcția afectată; restul au termen și proprietar. Recepția poate fi parțială pe val, fără a declara întregul proiect finalizat.')

p('R00 suplimentar: zero sisteme API, backenduri comerciale, baze de catalog sau mecanisme de autentificare paralele introduse de temă. D01 mapează fiecare ecran implementat la ruta/contractul existent. O extensie nesusținută nu este declarată livrată și nu este pornită doar pentru a satisface inventarul de design.')


page('19 Eșantionul intern și exemplele țintă')
p('Am analizat un eșantion reproductibil de 50 înregistrări din exportul intern: câte 5 din 10 grupe operaționale. Încadrarea preliminară folosește termeni din denumire, în ordine, cu o singură grupă per înregistrare; selecția folosește hashul ID-ului, cu includerea prioritară a produsului de tip variable. Este o examinare de câmpuri, nu certificare tehnică, test de stoc curent sau verificare fizică. Lista de ID-uri/SKU-uri este în documentul de trasabilitate.')
p(f'În eșantion, {stats["sample_missing"].get("GTIN, UPC, EAN sau ISBN",0)} înregistrări nu au GTIN/EAN, {stats["sample_missing"].get("Descriere",0)} nu au descriere, iar {stats["sample_missing"].get("Greutate (kg)",0)} nu au greutate. Aceste lipsuri justifică prioritizarea și verificarea sursei actuale. Nu s-a identificat un produs denumit sau categorizat ca personalizabil în export; capabilitatea de personalizare este un pilot propus, nu o ofertă existentă confirmată.')
table(['Caz','Conținut existent și transformare țintă'],[
('Ceașcă 220 ml\nSKU 5900_2763_2070_G242','Exemplul public are culoare/decor și preț. Fișa țintă adaugă seria validată, fotografie la scară, capacitate pe piesă, îngrijire confirmată, livrare și completare. Dimensiunile/greutatea estimate nu devin certe.'),
('Set 9 piese\nSKU 5900_3216_9718_D144','Titlul de set și descrierea de cană trebuie reconciliate. Fișa țintă arată componente și cantități, 200 ml doar la cană, material pe componentă, persoane confirmate și fotografii ale conținutului complet.'),
('Detergent sau consumabil Pro','Fișa țintă afișează volum/unitate, dozaj și documente aplicabile, ambalare, praguri de cantitate, preț contractual și cerere repetată; nu intră în scenele de ceramică.'),
('Decor și gătit','Vaza nu primește implicit utilizare alimentară. Vasul de gătit afișează temperatura și compatibilitatea numai din fișa tehnică. Culoarea vizuală nu înlocuiește materialul.'),
('Variante și produse speciale','Exportul conține un singur tip variable, două grouped și două external. Relațiile, prețul și destinația de cumpărare se validează separat; culoarea dintr-un atribut nu dovedește o variantă vandabilă.')],[5.2,12.3])
h('Specificația machetei de produs')
p('Pentru fiecare dintre cele 10 grupe se livrează o machetă țintă cu date reale aprobate, sursa fiecărui atribut nou și stările necunoscut/indisponibil. Zonele sunt cele din capitolul 6; variantele specifice familiei sunt explicite. Aceste 10 machete fac parte din D03, nu sunt pretinse ca realizate în această revizie documentară.')
p('Datele publice despre preț și stoc din V1 rămân dovezi istorice datate. Recomandările pentru „Cafeaua în doi” sau cadouri rezultă din reguli de cantitate, material, preț și disponibilitate, nu din etichetarea manuală a fiecărui SKU.')

h('Șase concluzii acționabile din eșantion')
table(['Semnal','Acțiune și rezultat'],[('Coduri finale SKU','Validare fabrică pe 100 SKU-uri înainte de generarea seriilor.'),('Materiale și mărci terțe','Verificare producător real; originea CESIRO nu se propagă după categorie.'),('Sticlă cu text Cesiro','Investigare proveniență din acte; numele comercial nu dovedește fabricantul.'),('Chimice și biocide','Clasificare legală și documente pe piață înainte de promovare Pro.'),('20 greutăți lipsă în eșantion','Măsurare produs/ambalaj; nu se promite cost de transport din valori estimate.'),('Seturi și capacități','Descompunere în componente; dimensiunea cănii nu este atribuită întregului set.')],[5.1,12.4])


page('20 Benchmark și cercetarea cu clienți')
p('Comparație documentară a opt repere oficiale, consultate la 21 octombrie 2026. Tabelul consemnează funcții/conținut observabile și o decizie de proiect; nu pretinde un audit complet de UX, checkout sau performanță al concurenților. Trendyol rămâne reperul suplimentar pentru accesul rapid la catalog. [B1–B9]')
table(['Reper','Element observat','Adaptare CESIRO'],[
('Zara Home','Categorii de casă, editoriale și card cadou.','Scene și conținut de brand legate de produse reale.'),
('H&M Home','Căutare, favorite, coș și navigare de categorie.','Acces simplu pe mobil și favorite fără încărcarea meniului.'),
('Westwing','Selectare de țări și magazine locale.','Piață distinctă de limbă, ofertă și condiții locale explicite.'),
('IKEA','Categorii funcționale pentru casă și acces la programul Family.','Utilizare și recumpărare; nu presupunem că un configurator de mobilier se transferă direct la ceramică.'),
('Le Creuset','Categorii de veselă, colecții sezoniere, culori și cadouri.','Culoare și serie ca intrări comerciale, cu disponibilitate verificată.'),
('Villeroy & Boch','Navigare pe piese/seturi, colecții și MyClub.','Completare set și fidelizare în jurul colecției.'),
('Emma Bridgewater','Ceramică personalizată cu nume/mesaj și colecții de cadouri.','Pilot de personalizare cu termen și limite de producție proprii.'),
('HAY','Arhitectură de categorii pentru mobilier și obiecte de casă.','Coerență vizuală și prezentare pe colecții; catalogul CESIRO rămâne autoritatea.')],[3.7,6.2,7.6])
h('Repere directe și vocea cumpărătorilor')
p('A1 extinde comparația la Bonna, Kütahya Porselen, Pașabahçe și Lubiana: serii, rezistență documentată, comandă HoReCa, completare și personalizare. Bonna și Lubiana au intrări oficiale de colecții/HoReCa identificate; celelalte sunt repere de investigat, fără concluzii de performanță atribuite. Se documentează 4 fișe comparative și 10 oportunități aplicabile. [B10, B11]')
p('Pentru eMAG și Trendyol se identifică listările CESIRO și vânzătorul real, apoi se includ recenzii și întrebări publice în limita de până la 500 surse din A1. Se înregistrează URL, dată, produs și temă, fără a copia date personale. Prețurile de pe canale sunt instantanee datate; nu se presupune aceeași ofertă sau o permisiune de contactare a clienților.')


h('Cercetarea care închide ipotezele')
p('A1 include 8–10 interviuri: cumpărători recenți, persoane care au abandonat, clienți de cadouri și Pro. Se analizează până la 500 recenzii/tichete anonimizate; dacă există mai puține, se raportează totalul real. Se caută dovezi despre spargeri, completarea seriei, diferențe de culoare, ambalare și termen. Sondajul după comandă se activează numai în implementarea autorizată, cu regulile de confidențialitate.')
p('Raportul diferențiază ce au spus clienții de interpretarea echipei. Ponderea mobilului, conversia și rata de retur CESIRO se extrag din datele proprii; nu sunt înlocuite de medii de piață neverificate. Această revizie nu inventează interviuri, rezultate de sondaj sau benchmarkuri numerice de conversie.')


page('20.1 Surse interne și tehnice')
p('I1 — Audit.Claude.V1.0.docx: 92 observații și 87 propuneri numerotate; Audit.Gemini.v1.0.pdf: 3 pagini, recomandări fără coduri proprii. Identificatorii G01–G20 din matrice au fost adăugați pentru trasabilitate.')
p('I2 — U:/cesiro1-site/backend/requirements.txt și frontend/package.json: tehnologii declarate. I3 — backend/app/price_reference.py, ai_assistant/guard.py și history.py, api/admin/resources, integrations, payments, feeds.py și database/migrations: citire statică, fără execuție.')
p('I4 — U:/cesiro1-site/wc-product-export-16-9-2026-1789549595309.csv. SHA-256: '+stats['sha256']+'. Rezultatele agregate și selecția sunt păstrate în evidence-v2/catalog-summary.json. I5 — U:/cesiro1-site/REGULI.md: restricții operaționale citite și păstrate în proiect.')
p('I6 — U:/cesiro.com/README.md, backend/themes/README.md, backend/app/cms.py, backend/app/factory.py, frontend/package.json și docker-compose.yml: citire statică din 21 octombrie 2026. Registry și contracte de teme confirmate în cod; 6 fișiere cheie identice cu copia cesiro1-site. GitHub indicat de beneficiar: https://github.com/cesiroproduction/site-uri ; accesul disponibil a returnat 404. Versiunea activă Docker și commitul nu sunt certificate prin această citire.')


links1=[
('S1 CESIRO pagina principală','https://cesiro.com/'),('S2 CESIRO sitemap','https://cesiro.com/sitemap.xml'),
('S3 Ceașcă 220 ml','https://cesiro.com/p/ceasca-cu-farfurioara-220-ml-maro-decorat-cu-flori-si-spic-de-grau'),
('S4 Set 9 piese','https://cesiro.com/p/set-masa-4-pers-9-piese-cana-roz-200-ml-bol-tava-termorezistenta-portelan-cu-trandafiri-roz'),
('S5 CESIRO informații și întrebări frecvente','https://cesiro.com/legal/intrebari-frecvente'),
('T1 Next.js randare și revalidare','https://nextjs.org/docs/app/getting-started/revalidating'),
('T2 Core Web Vitals','https://web.dev/articles/vitals'),('T3 WCAG 2.2','https://www.w3.org/TR/WCAG22/'),
('T4 Google Consent Mode','https://developers.google.com/tag-platform/security/guides/consent'),
('T5 Google Search și funcțiile AI','https://developers.google.com/search/docs/appearance/ai-features')]
for x in links1:link(*x)
p('Sursele online sunt referințe de proiect, nu certificate de conformitate. Versiunile bibliotecilor, contractele furnizorilor și forma consolidată a normelor se revalidează la începutul implementării și înainte de lansare.')

page('20.2 Surse legale și repere comerciale')
links2=[
('L1 GPSR Regulamentul UE 2023/988 articolul 19','https://eur-lex.europa.eu/eli/reg/2023/988/2026-05-29'),
('L2 Ceramica în contact cu alimentele și cadrul 1935/2004','https://eur-lex.europa.eu/EN/legal-content/summary/ceramic-objects-in-contact-with-foodstuffs.html'),
('L3 Comisia Europeană interpretarea articolului 6a privind reducerile','https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021XC1229(06)'),
('L4 Legea 232/2022 accesibilitatea produselor și serviciilor','https://legislatie.just.ro/Public/FormaPrintabila/00000G0KNQ8P76GT0TQ0JXEJG1KWCZGC'),
('L5 ANAF e-Factura B2C și modificările din 2026','https://static.anaf.ro/static/10/Brasov/Brasov/facturare_electronica_89.pdf'),
('L6 Comisia Europeană transparența conținutului AI','https://digital-strategy.ec.europa.eu/en/faqs/signing-code-practice-transparency-ai-generated-content'),
('L7 Cadrul ESPR și pașaportul digital al produsului','https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng'),
('L8 Regulamentul general privind protecția datelor','https://eur-lex.europa.eu/eli/reg/2016/679/'),
('L9 Comisia Europeană adoptarea euro în Bulgaria','https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_25_3123/IP_25_3123_EN.pdf')]
for x in links2:link(*x)
for x in [('B1 Zara Home','https://www.zarahome.com/ro/'),('B2 H&M Home','https://www2.hm.com/ro_ro/home.html'),('B3 Westwing','https://www.westwing.com/'),('B4 IKEA','https://www.ikea.com/ro/ro/'),('B5 Le Creuset','https://www.lecreuset.co.uk/en_GB/'),('B6 Villeroy & Boch','https://www.villeroy-boch.com/'),('B7 Emma Bridgewater personalizare','https://www.emmabridgewater.co.uk/collections/personalised-mugs'),('B8 HAY','https://www.hay.com/'),('B9 Trendyol România','https://www.trendyol.com/ro')]:link(*x)
page('20.3 Surse suplimentare pentru cerințele V3')
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
p('V1 a stabilit direcția inițială; V2 a integrat inventarul local și reutilizarea EVA. V3 tratează auditul Claude V2 și auditul tehnic, cu precizarea finală a beneficiarului: temă nouă peste backendul și API-urile existente, fără sistem API nou. Direcția de bază este Flask cu componente React în mecanismul actual de teme; funcțiile avansate nesusținute rămân extensii separate.')
p('Versiunile anterioare și auditurile rămân nemodificate. Nu s-au modificat site-ul, Dockerul, repository-ul, backendul, catalogul sau integrările. Doar documentele și planșele de proiect au fost create. D01 curent, D02 comercial și probele funcționale rămân activități ale implementării ulterioare.')
table(['Registru','Responsabil și termen','Rezultat necesar'],[('D01 inventar actual','Date și platformă până la S2','SQL de citire versionat, snapshot, numărători, reconciliere și demonstrații.'),('D02 baseline comercial','Financiar și analytics până la S2','Venituri agregate, conversie, Pro, marjă, durată de experiment.'),('D03 design și conținut','UX și editorial S1–4','Direcție validată, 25 tipuri, 75 ecrane și 10 machete pe familii.'),('ADR01–04','Tehnic și DevOps S2','Frontend, căutare, cache și producție, cu cost și probe.'),('Registru legal și producție','Juridic și fabrică înainte de val','Entități, promisiuni, documente, capacitate și excepții pe piață.')],[4.1,5.5,7.9])


save('Proiect_CESIRO_Design_React_Python_V3.docx')
print('Proiect V3 salvat')
