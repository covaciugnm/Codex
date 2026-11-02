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

init('Proiect CESIRO pentru tema React și extensiile platformei Python','Proiect V4')
p('Proiect CESIRO pentru tema React și extensiile platformei Python','Title')
p('Versiunea 4 specificație de proiect și criterii de recepție','Subtitle')
p('Destinat conducerii CESIRO, echipei de produs, furnizorilor de dezvoltare și auditorilor. Bază pentru decizie, estimare și recepție.')
head('0 Direcția și domeniul programului')
p('CESIRO va ajuta clientul să își compună masa, să completeze decorul preferat și să aleagă un cadou personal. De la Trendyol preluăm accesul clar la produse, căutarea și filtrarea; experiența proprie pornește de la ceramică, utilizări, culori și ocazii. Zona Pro are acces distinct, pe același catalog.')
p('Varianta C cuprinde tema nouă și extensiile E0–E7 în aplicația Flask și baza PostgreSQL existente. Nu creează un sistem API paralel, un backend comercial nou sau un catalog separat. JavaScript și React asigură interactivitatea, iar Flask randează paginile publice. Documentul descrie lucrări viitoare și nu reprezintă implementare sau lansare pe site.')
table(['Diferențiator','Rezultat măsurabil'],[
('Origine și încredere','100% dovezi pentru produsele promovate ca fabricate de CESIRO; păstrarea înlocuirii gratuite a produselor sosite sparte.'),
('Masa potrivită','20 serii validate și 12 scene cumpărabile; selecție pentru 2/4/6/8 persoane, cu cantități și total verificate.'),
('Cadou gata de dăruit','Ambalaj cadou și mesaj din funcția existentă, din prima lansare; E6 adaugă personalizarea a 10 produse după aprobarea fabricii.')],[4.2,13.3])
h('Două livrări coordonate')
p('Tema se lansează la săptămâna 16, cu 160–200 zile-persoană. Programul complet durează 24–26 săptămâni și include încă 80–120 zile-persoană pentru E0–E7: total 240–320. E0 și E2 sunt prima etapă urgentă, planificată pe tema actuală în săptămânile 1–3. Inovarea are propriile praguri de activare și nu amână tema.')
table(['Pachet','Domeniu inclus'],[
('Temă','21 tipuri de pagini de bază, 10 variante sezoniere/de eveniment, configurator 2D, conținut, localizare, SEO și reutilizarea fluxurilor comerciale.'),
('E0–E3 esențiale','Retragere fără cont și retur; filtre serie/persoane; acces securizat la comandă fără cont; completare firmă după CUI.'),
('E4–E7 inovare','Asistent public doar citire; căutare vizuală și semantică; personalizare pilot; registru de puncte Club.'),
('Ulterior','Liste de eveniment, card cadou cu sold, precomenzi pe loturi, preț pe client Pro, abonament și AR. Nu sunt incluse în totalul variantei C.')],[4.2,13.3])
p('Tema folosește API-urile actuale, iar extensiile adaugă numai rutele și tabelele necesare în același motor. Fiecare extensie are comutator pe tenant, teste și recepție separată. Cu inovarea oprită rămân catalogul, căutarea text, coșul și cumpărarea standard. E0, fiind flux de exercitare a drepturilor, are reguli de continuitate distincte și nu se oprește printr-un experiment comercial.')



page('1 Date disponibile și dimensiunea reală')
p('Inventarul combină observațiile publice din 21 octombrie 2026, exportul istoric de produse și citirea statică a codului din U:/cesiro.com. Baze operaționale, comenzi nominale și conturi de clienți nu au fost accesate. Starea codului este documentată în §11; D01 confirmă datele actuale și versiunea instalată. [I1–I8]')
table(['Sursă','Constatare','Limită'],[
('Export intern de produse','5.222 rânduri și ID-uri distincte; 5.221 SKU-uri nenule distincte; 1 SKU lipsă.','Instantaneu istoric, nu inventar curent.'),
('Stare în export','5.211 publicate, 11 cu valoarea −1; 5.217 simple, 2 grouped, 2 external, 1 variable.','Tipul exportului trebuie mapat la modelul actual; active nu înseamnă în stoc.'),
('Sitemap public','32.868 URL-uri; 31.674 de produs = 5.279 × 6 limbi.','Nu reprezintă 31.674 SKU-uri. Diferența față de export nu dovedește produse noi.'),
('Câmpuri lipsă în export','EAN/GTIN 1.145; descriere 670; imagini 50; greutate 2.014; stoc 23; preț obișnuit 5.','Lipsa din export nu dovedește lipsa în producție; GTIN nu se inventează.'),
('Structură software locală','Flask, SQLAlchemy, Alembic, PostgreSQL; admin React, TypeScript, Vite, TanStack.','Prezența codului nu certifică versiunea instalată sau funcționarea integrărilor.')],[3.5,7.8,6.2])
p('La verificarea din 21 octombrie 2026, U:/cesiro.com există, iar vechea cale U:/cesiro1-site nu mai există. Data exactă a redenumirii nu este dovedită; referințele istorice rămân în V2/V3, iar V4 folosește calea actuală. Exportul are același hash SHA-256 documentat. Pentru 14 fișiere cheie s-a salvat un manifest de hashuri în evidence-v4/source-hashes.json. Repository-ul GitHub indicat răspunde în continuare cu 404 prin conexiunea disponibilă; nu se inventează un commit și nu se echivalează hashurile de fișiere cu versiunea din producție. [I6]')


h('Inventarul contractual și analiza ABC')
p('În primele 3–5 zile lucrătoare, responsabilul platformei livrează D01 din sursa operațională existentă, folosind exportul actual sau interogări SQL de citire versionate pe un instantaneu consistent. Nu se creează un API de export nou. Exportul acoperă fiecare tenant: produse, variante, relații, stoc pe depozit/canal, istoric de preț și vânzări agregate pe 12 luni. Se stabilesc separat N produse, N SKU-uri vandabile, N active în ultimele 90 de zile și N traduceri. Numărătorile, hashurile și data de referință se semnează în registrul D01.')
p('ABC se calculează după venitul net cumulat: A până la 80%, B următoarele 15%, C restul; marja și rotația sunt dimensiuni suplimentare. Lista de maximum 300 produse prioritare combină grupa A, disponibilitatea, marja și reprezentativitatea brandului. Nu presupunem că 300 de produse generează deja 80% din venit.')
h('Portofoliul')
p('Vitrina principală prezintă Ceramică și Masă. /pro grupează HoReCa și consumabilele; produsele din alte familii rămân în inventar și primesc o decizie de canal, fără ștergere automată. Vizibilitatea publică și URL-urile existente se tratează individual, cu analiză de trafic și redirecționare relevantă. Subdomeniul Pro nu este necesar la început.')

h('Reconciliere și origine')
p('Diferența numerică de 57 dintre sitemap și CSV nu dovedește 57 produse noi. D01 compară mulțimi după ID canonic, SKU și slug: numai în bază, numai în CSV, numai în sitemap, redenumiri, retrageri și duplicate. Fiecare diferență primește cauză; 100% sunt explicate înaintea migrării. Nu se accesează clienți nominali pentru această analiză.')
p('Producător real este câmp obligatoriu distinct de brand și vânzător. Insigna și filtrul „Fabricat de CESIRO” cer document de proveniență și validare umană. Produsele terțe rămân eligibile în vitrină cu producătorul corect; materialul, originea și fabrica nu se deduc din textul comercial sau din prefixul SKU.')


page('2 Modelul datelor și folosirea integrală')
p('Fiecare rând și câmp sursă are destinație: utilizare, normalizare, revizuire sau arhivare justificată. Se păstrează originalul, sursa, data, regula, aprobarea și versiunea. Arhiva brută poate preceda îmbogățirea; se publică numai loturi eligibile.')
table(['Grup de date','Date existente reutilizate','Destinație și necesar de verificat'],[
('Identitate','ID, SKU, EAN/GTIN, slug, brand, părinte, tip, vizibilitate','ID canonic stabil; mapare între surse și canale; identificarea producătorului real.'),
('Conținut și limbi','Nume, texte, categorii, atribute, tags, traduceri','Serie/decor, rol în set, stil, ocazie, relație destinatar, nivel de validare pe limbă.'),
('Comerț','Prețuri, monedă, taxe, disponibilitate, stoc, precomandă','Istoric efectiv al prețului, marjă doar intern, rezervări, cantități minime, preț pe client Pro doar în extensie ulterioară.'),
('Caracteristici','Material, culoare, capacitate, dimensiuni, greutate, bucăți','Unități normalizate; culoare vizuală validată; măsurători reale; componente și persoane justificate.'),
('Conformitate','Date existente ale furnizorului și pagini de politici','Producător și contacte, operator UE când se aplică, avertismente, lot, declarații și documente alimentare.'),
('Media și SEO','Imagini, ordine, metadate, canonical, hreflang, JSON-LD','Drepturi, alt, dimensiuni, video, modele 3D, marcaj compoziție, URL-uri și redirecturi istorice.'),
('Relații comerciale','Upsell, cross-sell, produse grupate, recenzii','Relații serie–piesă–componentă–scenă; proveniența recomandării, UGC moderat, favorite.'),
('Operațional','Ambalare, livrare, retur, integrare și depozit','Greutate colet, fragilitate, termen de producție, capacitate confirmată, reguli de spargere.')],[3.1,6.2,8.2])
p('Dicționarul mapează mai întâi câmpurile și conținutul existente. E1 poate adăuga relațiile de serie/persoane; E0/E2/E6/E7 adaugă strict datele funcțiilor lor; E5 stochează vectori derivați. Migrările Alembic sunt additive, în PostgreSQL-ul actual, cu tenant și păstrarea ID-urilor canonice. Nicio extensie nu copiază întreg catalogul ca sursă comercială concurentă.')


h('Dicționare pe familii')
p('Veselă și căni: material, decor, diametru/capacitate, rol și utilizări verificate. Seturi: listă exactă de componente și cantități, persoane fără deducere din numărul total de piese. Gătit: temperatură și surse de încălzire documentate. Decor: dimensiuni, utilizare și stabilitate; nu se presupune contact alimentar. Curățenie: cantitate, dozaj, avertismente și documentația specifică substanței, după caz.')
p('Capacitatea de 200 ml a unei căni dintr-un set aparține componentei. Valoarea necunoscută nu devine zero. Compatibilitatea, proveniența, rezistența și certificările nu se deduc din fotografie. HEX și stilul produse de AI sunt propuneri editoriale. Câmpurile comerciale publice nu expun costul sau marja.')

h('Dicționar pentru chimice și biocide')
p('Date obligatorii când sunt aplicabile: clasificare și versiune CLP, pictograme, cuvânt de avertizare, fraze H/P și EUH, cantitate netă, furnizor, UFI când este cerut, fișă cu date de securitate cu limbă și revizie, autorizație/aviz biocid și țări de valabilitate, utilizări permise, mesaj de publicitate art. 72 și link către ingredientele detergentului. Pentru fiecare câmp există stare aplicabil/neaplicabil și justificare aprobată; nu se cer automat aceleași acte tuturor produselor de curățenie.')
p('Preț unitar = preț final / cantitate netă normalizată × unitate de referință. Se afișează pe card, fișă și coș în lei/l, lei/kg ori lei/bucată unde este relevant; la pachete mixte nu se inventează unități înșelătoare. Exemple de test: 50 lei/5 l =10 lei/l; 25 lei/50 buc. =0,50 lei/buc. Aplicabilitatea legală se confirmă pe piață. [L12]')


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
('Nuntă și aniversare','Selecții de cadouri și mesaje; lista partajată de eveniment rămâne extensie ulterioară.'),
('Sărbători la masă','Campanii cu perioadă, disponibilitate și conținut pe limbă.'),
('Completează decorul tău','Serie exactă, identificare piesă, alternative etichetate distinct.'),
('Culoarea casei tale','Mostre de culoare și denumiri validate; filtrare fără a depinde doar de culoare.'),
('A doua șansă','Outlet cu defectul real descris și fotografiat; fără diminuarea siguranței.')],[5.2,12.3])
p('Cele 12 rânduri definesc 12 familii editoriale; „Pentru el” și „Pentru ea” pot genera două pagini distincte. Colecțiile sunt interogări salvate pe atribute, eligibilitate, stoc și marjă internă, cu includeri/excluderi editoriale, prioritate și interval de activare. Minimum 8 produse eligibile pentru o pagină promovată; altfel, recomandări alternative sau ascunderea intrării din campanie.')
p('Filtrele existente în cod sunt q, category_id, brand, color, material, capacity, finish, in_stock, on_sale, min_price/max_price, sort și lang. E1 adaugă serie/decor și număr de persoane, cu compatibilitate pentru cererile vechi. Editorul creează o colecție din date pregătite în maximum 5 minute; nu se multiplică produsele pentru fiecare ocazie.')

h('Serii din SKU și colecții active')
p('Segmente precum G242, D144, 604M și 010L sunt candidați, nu dovadă de decor. Fabrica validează 100 SKU-uri și excepțiile; E1 păstrează dicționarul și legăturile aprobate pe produsul canonic. „Completează decorul tău” se automatizează numai pentru cele 20 serii validate. Produsele terțe și codurile ambigue nu se unesc automat; zero asocieri greșite în lotul publicat.')
p('Ținta pentru colecțiile promovate este reevaluarea la eveniment de stoc și cel mult la 5 minute, folosind automatizările existente. Sub 8 produse eligibile, intrarea de campanie se retrage sau oferă alternative marcate. Dacă mecanismul lipsește, colecția rămâne administrată manual și nu intră în promovarea automată. Pagina și URL-ul se păstrează; tema nu construiește un serviciu nou de reconciliere.')


page('6 Paginile de bază și starea de livrare')
p('Inventarul are 25 tipuri de design: 21 de implementat în tema de bază, 2 activate prin E6/E7 și 2 păstrate numai ca idei ulterioare. „Planificat” descrie proiectul, nu o funcție deja instalată. Pentru cele 25 tipuri se livrează minimum 75 ecrane la 390, 768 și 1440 px, plus stări de eroare, gol, încărcare și indisponibilitate.')
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


p('Inventarul are 25 tipuri proiectate și 21 tipuri de implementat în tema de bază; E6/E7 adaugă două, iar două rămân concepte. Arhiva Z:/images conține la inventariere 38.872 fișiere, dintre care 38.865 cu extensie de imagine, nu tot atâtea produse sau fotografii unice. Reutilizarea precede refotografierea: asociere SKU, deduplicare, drepturi și verificare vizuală. Bugetul media păstrează ipoteza de 150 produse reutilizate, fără economie pretinsă înainte de selecție.')


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


page('8.4 Autoservire după cumpărare')
p('Pagina Comenzile mele este accesibilă din cont sau prin link securizat, cu expirare și verificare suplimentară pentru operațiuni sensibile. Clientul fără cont are același acces la drepturi. Se afișează comanda, data estimată, statusul curierului cu ora ultimei actualizări, factura și istoricul cererilor; indisponibilitatea curierului nu este ascunsă sub un status inventat.')
table(['Flux','Activitate și criteriu'],[
('Produs sosit spart','Selectare piesă și cantitate, fotografie opțională sau canal alternativ, confirmare. Mediană ≤60 s pentru completarea cererii, nu pentru aprobarea înlocuirii. Notificare imediată, țintă de răspuns uman ≤1 zi lucrătoare; înlocuire gratuită potrivit promisiunii publice. Lipsa fotografiei nu stinge drepturile.'),
('Retragere','Intrare publică permanent vizibilă în perioada relevantă, plus link în cont și e-mail. Identificare minimă, selecție contract/produse, confirmare explicită și dovadă pe suport durabil cu dată/oră; nu cere cont sau motiv. Detalii în §12.1.'),
('Adresă și factură','Clientul trimite cererea; operatorul verifică etapa expedierii și confirmă schimbarea. Descărcarea facturii verifică proprietarul; linkul nu expune alte documente. Corecțiile fiscale rămân la financiar.'),
('Re-comandă','Piesele din istoric se propun în coș nou; prețul și stocul sunt actuale și confirmate. Produsele lipsă au alternative etichetate, fără substituire automată.'),
('Asistent','Citește numai comanda autorizată și politicile aprobate, explică pașii și pregătește recomandări. Nu anulează, nu aprobă retururi, nu rambursează și nu modifică marketplace-uri.')],[3.4,14.1])
p('Politica de înlocuire a produselor sosite sparte este deja publicată în FAQ și este păstrată în proiect. Responsabilul logistic definește stocul de înlocuire, costul și escaladarea; orice schimbare ulterioară a condițiilor cere analiză juridică și nu reduce retroactiv drepturile. Solicitările înregistrate nu sunt supuse aprobării AI. [S5]')


p('Autoservirea reutilizează stările comerciale actuale. E2 adaugă accesul securizat fără cont, iar E0 înregistrează retragerea și reface interfața de retur în condițiile aprobate. E0 nu depinde de primirea unui link E2: formularul public rămâne accesibil fără cont. Asistentul E4 doar explică și trimite clientul spre flux; nu îl execută. R09 se leagă direct de recepția E0, înainte de lansarea temei.')


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


page('9.2 Cache și consistență în motorul existent')
p('Tema folosește citirea și invalidarea existente. Catalogul public poate fi cache-uit conform contractului platformei; coșul, contul, checkoutul și prețurile private nu intră în cache public. Prețul/stocul afișat și cel verificat la comandă provin din aceeași autoritate. Clientul reconfirmă orice modificare de total, iar rezerva de stoc este cea existentă.')
table(['Demonstrație','Criteriu'],[
('Actualizare produs și stoc','Se urmărește traseul real al unei schimbări în mediu izolat până în pagina temei și coș; obiectiv p95≤5s, p99≤30s dacă platforma îl susține. Nu se introduce un al doilea strat comercial de cache.'),
('Date expirate','Pentru oferte dinamice: maximum 60 s de informație expirată, apoi revalidare sau afișare indisponibilă. Checkoutul validează întotdeauna la sursă, cu mecanismul existent.'),
('Teste de regresie','Ultima unitate, preț schimbat, stoc zero, sesiune expirată și acces Pro: zero comenzi confirmate pe date invalide, fără duplicarea logicii în React.'),
('Capabilitate lipsă','Se deschide deficit de platformă, nu un sistem nou în temă. E0–E7 pot extinde mecanismul comun în limitele pachetului estimat; alte schimbări sunt cotate distinct.')],[4.2,13.3])
p('Nu există un cache al unei aplicații frontend separate. E0–E7 folosesc mecanismul comun; actualizarea vectorilor E5 are jurnal și reindexare versionată, iar produsele retrase sunt filtrate la citire. Deficitul de consistență blochează funcția afectată. Cacheul AI nu include comenzi, tokenuri, date personale sau prețuri private.')


page('10 Frontend și contractul de randare')
table(['Pagină','Randare și cache','Actualizare și siguranță'],[
('Homepage și Jurnal','HTML randat de Flask/cache la CDN; module dinamice distincte.','Invalidare la publicare; cache segmentat pe tenant, limbă și piață.'),
('Produs, categorie, serie','HTML indexabil, cache cu revalidare la eveniment; țintă de propagare ≤60 s.','Disponibilitatea afișată are dată; prețul/stocul se reverifică autoritativ la coș și comandă.'),
('Căutare și configurator','Rezultate dinamice și stare în URL; încărcare progresivă.','Index actualizat p95 ≤60 s; indisponibilitatea indexului are fallback text.'),
('Coș, checkout, cont, Pro','Dinamic; Cache-Control private/no-store.','Izolare de sesiune și tenant; fără prefetch al operațiunilor cu efect comercial.'),
('Recomandări și AI','Insule React încărcate la interacțiune, în limita E4/E5.','Timeout și fallback; niciun blocaj al conținutului principal.')],[4,6.4,7.1])
p('ADR03 verifică invalidarea cacheului și actualizarea E5. Totalul se validează în motor și orice schimbare cere reconfirmare. Datele inițiale sunt serializate sigur, în aceeași limbă/monedă pentru Jinja și React. Fiecare insulă deține propria zonă DOM; storefront.js/shop.js nu dublează handlerii. Testele verifică evenimentele duble și hidratarea.')
h('Biblioteci și compatibilitate')
p('Bază propusă: Radix, Tailwind, TanStack Query unde este necesar, React Hook Form și Zod. Python repetă validarea critică. Tokenurile și componentele adminului sunt reutilizabile numai fără dependență de permisiuni administrative.')
p('Suport: ultimele două versiuni stabile Chrome, Edge, Firefox, Safari și Samsung Internet; iOS/Android reprezentative. Îmbunătățiri progresive cu fallback și economisire de date. Prefetch doar pentru pagini publice sigure, fără efecte comerciale ori date personale.')
h('Verificare frontend')
p('Regresia temei verifică șase trasee: căutare text–produs–coș; categorie–filtru existent/E1; serie–completare; cadou–ambalaj–mesaj; checkout vizitator–Stripe; Pro–firmă–cerere de ofertă. E4, E5, E6 și E7 au trasee proprii după activare. /api/orders/validate acoperă preț schimbat și stoc zero, după inspectarea lanțului și în mediu izolat. Operațiile de retragere/retur/anulare cu efect sunt probate de om, nu executate automat de AI.')

h('Buget de performanță pe rută')
table(['Rută','JS inițial comprimat','Alte limite pe mobil'],[('Homepage și produs','≤170 KB total; React pe produs ≤120 KB','Imagine LCP ≤120 KB; ≤35 cereri inițiale.'),('Listare și căutare','≤200 KB','LCP ≤120 KB; ≤40 cereri inițiale.'),('Checkout','≤220 KB cod propriu','≤35 cereri proprii; SDK PSP separat măsurat și încărcat la pasul necesar.'),('Configurator','≤170 KB înainte de activare','Pachet 2D suplimentar ≤250 KB; activele se încarcă la cerere, fără blocarea produsului.')],[4.1,4.1,9.3])
p('CI măsoară un build de producție cu cache gol, la 390 px și rețea mobilă simulată. Fonturile, CMP și analytics autorizat intră în bugetul propriu. Depășirea blochează buildul; o excepție are ADR, proprietar și termen și nu suspendă pragurile CWV. Pachetele AI, 2D și AR nu sunt în încărcarea inițială a paginii de produs.')


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


page('12 Checkout plăți și operațiuni')
p('Checkoutul local grupează contactul, livrarea și sumarul într-o pagină cu progres clar; clientul poate plăti fără cont. Codul Stripe citit creează o sesiune și folosește URL-ul ei, indicând plată pe pagina găzduită de Stripe. Tema nu promite că plata rămâne în aceeași pagină. D01 confirmă modul activ și walleturile eligibile; Apple Pay/Google Pay apar numai dacă integrarea și contul Stripe le permit. Schimbarea către un element încorporat este decizie și cost distinct.')
table(['Flux','Cerință și probă de recepție'],[
('Total și preț','Recalcul server înainte de confirmare; TVA, transport, discount și monedă explicite; sume reconciliate până la unitatea monetară minimă.'),
('Plată','Tokenizare prin PSP, autentificare când este cerută, webhook semnat, idempotentă și reconciliere. Retrimiterea evenimentului nu dublează comanda, factura sau punctele.'),
('Ultima unitate','Rezervare atomică și expirare; simultaneitatea coșurilor și evenimentele întârziate nu produc supravânzare. Plata tardivă intră în soluționare umană dacă stocul nu mai poate fi onorat.'),
('Stoc pe canale','Autoritate comună și reconciliere cu marketplace-urile; latență măsurată, tampon pe canal și oprirea promisiunii când sincronizarea este degradată.'),
('Livrare','Autocompletare localitate, hartă de lockere plus listă accesibilă, adresă manuală alternativă; termen estimat din stoc, capacitate și calendar curier.'),
('Transport gratuit','Prag configurabil pe piață și campanie; bara folosește aceeași bază eligibilă ca checkoutul. 500 lei este informație publică observată, nu regulă fixată definitiv.'),
('Facturare','Emiterea facturii conform politicii fiscale declanșează transmiterea e-Factura când este aplicabilă. Status SPV, retry, deduplicare, alarmă înaintea termenului legal și stornare operată autorizat.')],[3.2,14.3])
p('Backendul păstrează separat starea comenzii, a plății, a livrării și a documentului fiscal. Se documentează și se reutilizează stările existente corespunzătoare plății inițiate, în așteptare, autorizată, confirmată, eșuată și rambursată, cu tranziții permise și jurnal. Nu se consideră plătită o comandă doar din revenirea browserului de la PSP. [L5]')
p('Regulile locale din REGULI.md sunt constrângeri de proiect: AI nu anulează comenzi și nu execută retururi/rambursări, nici în teste. Testele automate folosesc simulări izolate, fără scrieri spre sisteme reale. Validarea fluxurilor sensibile revine unui operator uman. Scrierile spre marketplace-uri cer autorizarea expresă a proprietarului; automatizarea AWB respectă politica pe canal. [I5]')

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
p('Numai combinațiile de filtre aprobate editorial sunt indexabile. Checkoutul, conturile, listele private și rezultatele cu parametri infiniți nu devin pagini SEO. Schimbarea temei păstrează URL-urile; crawlul compară cele două randări pe aceleași adrese. Monitorizare zilnică a paginilor prioritare, erorilor și indexării în primele 30 zile.')
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
('Funcții noi','collection_view, scene_add_to_cart, table_config_complete, visual_search, ai_recommendation_click, personalization_submit, pro_quote_submit; evenimentele E4–E7 se activează odată cu extensia. registry_purchase rămâne rezervat conceptului ulterior.'),
('Retenție','Cohorte lunare, recumpărare la 90 zile, venit net/client la 180 zile și marjă cumulată. LTV predictiv se etichetează estimare, nu venit realizat.'),
('Calitatea livrării','Spargeri = comenzi cu incident / comenzi livrate; cost incident, retur și contact suport. CSAT la livrare și NPS la 30 zile, cu rata de răspuns.'),
('Marketing','Conversie e-mail = comenzi atribuite / destinatari eligibili; click și dezabonări. Deschiderile sunt informative, afectate de protecția confidențialității.'),
('Achiziție','Cota canalului direct din venit reconciliat și trafic organic non-brand din Search Console; nu se confundă traficul măsurat cu toți vizitatorii.')],[4.6,12.9])
h('Disciplina experimentelor')
p('Minimum 15 ipoteze ordonate prin impact, încredere și efort; se selectează 3–4 experimente principale în șase luni, după puterea statistică. Un singur obiectiv principal, populație eligibilă, unitate de randomizare utilizator, expunere stabilă, excluderi și durată stabilite înainte de start. Se folosesc α=5%, putere 80% și efect minim detectabil calculat din baza reală; fără oprire la primul rezultat favorabil.')
p('În primele șase luni se prioritizează 3–4 teste cu efect potențial mare: checkout, configurator, intrare după decor și asistent după activarea E4. Restul ipotezelor rămân în backlog. Se testează disponibilitatea funcției, cu un singur obiectiv primar și fără suprapuneri care împiedică atribuirea.')
p('Guardrails: marjă de contribuție/comandă, erori de plată, retururi, spargeri și suport. O scădere a marjei >2 pp sau creștere a spargerilor >0,3 pp declanșează analiză și oprirea variantei dacă este confirmată. Pentru trafic insuficient se raportează intervale și rezultat neconcludent; interviurile UX nu sunt prezentate ca dovadă A/B.')

p('D02 calculează durata realistă pentru MDE 10% relativ la conversia actuală, α=5%, putere 80%, alocare 50/50 și trafic eligibil după consimțământ. Exemplu de dimensionare, nu baseline CESIRO: de la 2,0% la 2,2% necesită aproximativ 80.600 utilizatori/grup pentru un test bilateral simplu; la 10.000 eligibili/săptămână în total ar dura circa 16 săptămâni. Durata se recalculează pentru unitatea reală de randomizare și sezonalitate; 2 teste/lună nu este un angajament fără trafic suficient.')


page('16 Calendarul integrat al variantei C')
p('Program complet 24–26 săptămâni; tema se lansează în S16. S1 înseamnă începutul implementării autorizate, nu data redactării. Fluxul urgent E0/E2 începe pe tema actuală și nu așteaptă designul. Pentru fiecare extensie există responsabil, dependențe, comutator și probă R12.')
table(['Interval','Temă și conținut','Extensii','Ieșire'],[
('S1–3','T0: D01/D02, inventar media, ADR01–04','E0 + E2; PoC E4/E5; validare fabrică E6','Flux de retragere și acces fără cont pe tema actuală după teste umane; PoC măsurat.'),
('S1–4','T1: trei concepte, teste UX și design system','Contracte finale E1, E3–E7','Direcție aprobată; 25 tipuri cu stări și contracte.'),
('S3–10','T2: temă înregistrată, home/listare/produs, 10 ghiduri și 300 prioritare','E1 filtre și E3 CUI','Serii și persoane în catalog; completare firmă cu alternativă manuală.'),
('S7–12','T3: coș/checkout/cont, Pro, 2D și 12 scene','E4 dezvoltare','Regresie comercială pe ambele teme; asistent testat izolat.'),
('S11–14','T4: QA accesibilitate/securitate, 30 ghiduri','E5 dezvoltare','R03–R09 și R11 pentru temă; etalon E5 și capacitate PGX.'),
('S15–16','T5: pilot și comutare 5–20–50–100%','E6 dezvoltare; E4/E5 pregătire activare','Temă la 100% în S16; E0/E2 rămân disponibile.'),
('S17–20','Măsurare și optimizare temă','E4 pe cohorte; E5 activ; E7 dezvoltare','R12 E4/E5, cost și praguri de calitate.'),
('S21–26','Continuitatea temei și conținut','E6 pilot 10 produse; E7 activ','Proof fizic și registru de puncte recepționate; program complet.')],[1.7,5.1,4.3,6.4],small=9.5)
p('E1 necesită dicționarul de decoruri aprobat; E4 necesită izolarea datelor și PoC; E5 depinde de pgvector compatibil și surse media; E6 depinde de capacitate și proof; E7 depinde de regulile financiarului. S24 este ținta optimistă, S26 capătul intervalului planificat. O dependență neîndeplinită produce reestimare vizibilă, nu lansare fără probă.')
p('Tema are drum critic D01 → design → contracte → regresie checkout → R11 → lansare. E0/E2 au prioritate separată pentru drepturile clientului. Lipsa inovării nu împiedică lansarea temei conforme; lipsa E0 nu se amână până la E6/E7.')
p('Minimum 48 h și volum suficient pentru fiecare treaptă de trafic. Erorile de total, plată, stoc ori acces opresc creșterea; revenirea înseamnă comutarea temei. Limita inferioară a intervalului de conversie urmărește pragul −5% relativ; trafic insuficient înseamnă incertitudine și expunere limitată documentată.')
p('Cele 90 zile de măsurare pornesc separat: temă din activarea integrală S16, fiecare extensie din data sa de activare. Ultimul raport poate ajunge aproximativ în S39. Garanția și mentenanța se raportează la recepția fiecărei livrări, fără consumarea perioadei unei extensii înainte de lansarea ei.')


page('17 Efortul temei și extensiilor')
p('Deviz de planificare, 8 ore/zi-persoană. Tema păstrează baza de 160 zile și intervalul 160–200; E0–E7 adaugă baza de 80 zile și intervalul 80–120. Total 240–320 zile. Baza detaliată include QA, integrare și documentare; limitele superioare acoperă incertitudinea tehnică, fără a pretinde cotație fermă înainte de D01 și PoC.')
wbs=[('N01 Inventar și contracte',3,2,3,2),('N02 UX și concepte',12,0,0,4),('N03 Componente și 10 variante',6,14,0,4),('N04 Home listare produs',4,18,2,6),('N05 CMS navigare colecții',2,6,2,2),('N06 Coș și checkout actual',2,8,2,6),('N07 Cont și suport actual',1,5,1,3),('N08 Configurator 2D și scene',2,8,0,4),('N09 Limbi SEO măsurare',1,3,2,4),('N10 Docker cohorte R11',0,2,4,6),('N11 Coordonare și predare',2,0,0,2)]
assert sum(sum(r[1:]) for r in wbs)==160
table(['Temă','UX','React','Python','QA','Zile'],[list(r)+[sum(r[1:])] for r in wbs]+[['Total',35,66,16,43,160]],[6.9,1.5,1.6,1.8,1.5,1.7],small=9.5)
exts=[('E0 Retragere și retur',1,1,2,2,10),('E1 Serie și persoane',0,1,2,1,6),('E2 Acces fără cont',0,1,1,1,5),('E3 Date firmă CUI',0,0,1,1,4),('E4 Asistent public',1,4,6,4,25),('E5 Căutare vizuală',1,3,7,4,20),('E6 Personalizare pilot',3,6,7,4,30),('E7 Club puncte',1,2,9,3,20)]
assert sum(sum(r[1:5]) for r in exts)==80 and sum(r[5] for r in exts)==120
table(['Extensie','UX','React','Python','QA','Interval'],[[r[0],*r[1:5],f'{sum(r[1:5])}–{r[5]}'] for r in exts]+[['Total',7,18,35,20,'80–120']],[6.9,1.5,1.6,1.8,1.5,1.7],small=9.5)
p('Vârful de 4–5 echivalenți normă întreagă în S7–16 este capacitate rezervată în planul nominal, nu medie pe toate cele 26 săptămâni. Nu se facturează automat 5 persoane × întregul calendar. Rolurile se combină controlat; costul urmează zilele efective ale WBS. PO CESIRO, editorii, fabrică și juridic sunt contribuții distincte.')
page('17.1 Bugetul variantei C')
p('Sume fără TVA, pentru planificare, nu cotații de piață. Se cer două oferte pe același domeniu temă + E0–E7. Formula păstrată este (efort × tarif + media + cost tehnic incremental + mentenanță temă) ×1,15. Rezerva financiară 15% este separată de intervalul de efort și se consumă numai documentat.')
table(['Scenariu','Calcul','Total cu rezervă'],[
('Local sau EVA','240–320 zile ×250–400 EUR = 60.000–128.000; media 19.460–35.100; tehnic 900–2.400; mentenanță temă 4.500–9.000.','97.589–200.675 EUR'),
('Furnizor complet','240–320 zile ×400–550 EUR = 96.000–176.000; aceleași linii de media, tehnic și mentenanță.','138.989–255.875 EUR'),
('Extensii singure','80–120 zile: local 20.000–48.000; furnizor 32.000–66.000.','Înainte de rezerva 15%')],[3.7,9.2,4.6])
p('Costul tehnic de 150–400 EUR/lună și mentenanța temei de 750–1.500 EUR/lună acoperă câte șase luni conform ipotezei de bază. Găzduirea existentă rămâne cost separat. Calendarul de 24–26 săptămâni nu se confundă cu durata mentenanței după recepție. Ofertele precizează datele de început pentru fiecare linie și orice suprapunere.')
h('Costuri suplimentare vizibile')
table(['Element','Ipoteză explicită'],[
('AI E4 + E5','Plafon comun 600 EUR/lună; pentru șase luni de utilizare: maximum 3.600 EUR. Inferența locală include alocarea de electricitate, capacitate și operare; nu este declarată gratuită.'),
('Mentenanță extensii','Alocație de ofertare suplimentară 300–600 EUR/lună pentru șase luni: 1.800–3.600 EUR. Nu este inclusă în mentenanța temei și se confirmă prin ofertă.'),
('Timp intern CESIRO','100 zile-editor + 48–52 zile PO (2/săptămână ×24–26) =148–152 zile. La un tarif intern ipotetic de 150 EUR/zi: 22.200–22.800 EUR.'),
('Fabrică și Club','Proof-uri și materiale E6, costul punctelor E7 și munca fabricii/juridicului se bugetează de responsabili înainte de pilot. Nu sunt ascunse în costul software.'),
('Infrastructură','Hardware AI nou, HA/PITR și permanență 24/7 nu sunt incluse; se cotează numai dacă ADR04/PoC identifică deficit.')],[4.1,13.4])
p('Anvelopă de planificare cu timpul intern de mai sus, șase luni AI la plafon și mentenanță extensii: local 125.999–231.755 EUR; furnizor 167.399–286.955 EUR. Calcul: totalul de bază + timpul intern + (3.600 + 1.800–3.600) ×1,15. Rămân variabile distincte fabrica, punctele Club și infrastructura. Nu se prezintă această anvelopă ca preț fix complet.')


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
p('Clauză contractuală propusă: 90 zile garanție pentru defectele temei față de specificația acceptată, inclusă în dezvoltare. Extinderea la 180 zile se cere în ofertă. Mentenanța temei de 750–1.500 EUR/lună și suplimentul estimat pentru extensii din §17.1 sunt distincte de operarea infrastructurii. Cele 90 zile de garanție se aplică separat fiecărui pachet recepționat.')
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
('Copii divergente EVA','Hashuri locale, commit și digest de producție; migrări E0–E7 și regresie pe ambele teme.','Lider tehnic'),
('Cod diferit de producție','Demonstrație a versiunii instalate și contracte API înainte de estimarea fixă.','Lider tehnic'),
('Date slabe sau acte lipsă','Loturi, scor și condiții obligatorii; zero publicări comerciale neeligibile.','Date + juridic'),
('Dependență de o persoană','Documentație, pairing și exercițiu de restaurare condus de a doua persoană.','DevOps'),
('AI greșit sau costisitor','Etalon, plafon lunar, oprire automată la epuizare și fallback; măsurare cost/cerere.','AI + PO'),
('Stoc și plăți divergente','Reconcilierea existentă, idempotentă, tampon și alarme; fără outbox comercial nou în temă.','Backend + logistică'),
('Canibalizare marketplace','Marjă și cotă directă pe canal; servicii exclusive măsurabile, fără război automat de preț.','Comercial'),
('Capacitate fabrică sau personalizare','Pilot de 10 produse, fișă aprobată, cantitate și termen confirmate; flag dezactivat până la validare.','Fabrică'),
('Legal sau piață nepregătită','Matrice pe țară și familie; revalidare înainte de val, stop pentru domeniul afectat.','Juridic'),
('Conținut peste buget','Inventar media și rată de editare în A1; variația >10% din efort cere recalcul transparent.','PO + content')],[4.2,10.6,2.7],small=9.6)
p('Nu sunt incluse în bugetul software de bază: publicitate plătită, comisioane PSP/marketplace, transport și spargeri, materiale și capacitate de fabricație sau hardware AI. Timpul editorilor și al PO CESIRO este cuantificat separat și inclus numai în anvelopa extinsă din §17.1. Bugetul media/lingvistic extern nu dublează zilele de orchestrat/editat date; cele două categorii se reconciliază în deviz. Contribuțiile financiare de grup, abonamentul Mystery Box, creditul Pro, AR și integrarea ERP avansată sunt extensii separate.')

page('17.5 Extensii ulterioare și limitele programului')
p('Următoarele idei sunt în registrul de oportunități, fără a intra în cele 240–320 zile sau în bugetul variantei C. Intervalele sunt ordine de mărime preliminare pentru comparație, cu incertitudine ridicată, nu oferte sau activități pornite.')
table(['Idee','Efort preliminar','Condiție de pornire'],[
('Liste de eveniment','20–35 zile','Rezervare concurentă, confidențialitate destinatar și reguli logistice; contribuțiile financiare de grup cer analiză separată.'),
('Precomenzi pe loturi','15–25 zile','Capacitate de fabrică semnată, avans și informarea întârzierii; fără ERP complet.'),
('Preț pe client Pro','10–18 zile','Reguli comerciale și TVA, autorizare și teste de izolare a prețului.'),
('Card cadou cu sold','12–20 zile','Registru, răscumpărare, expirare și tratament fiscal; nu se substituie E7.'),
('AR pilot 10 produse','15–25 zile plus active','Modele fidele GLB/USDZ, scara reală, cinci dispozitive și dovada valorii comerciale.')],[4.2,3.7,9.6])
h('Riscurile suplimentare ale variantei C')
table(['Risc','Măsură și proprietar'],[
('PGX ocupat cu alte sarcini','DevOps + AI: rezervare de capacitate, prioritate pentru public, limită cereri/minut și test de concurență cu traducerile în PoC.'),
('Răspunsuri AI greșite','AI + PO: catalog/politici aprobate, citare și abținere; oprire imediată la divulgare/acțiune interzisă; calitate sub prag suspendă cohorta până la revalidare.'),
('Capacitate E6','Fabrică: comutator închis până la 10 proof-uri; termen din registru semnat, fără promisiuni deduse din fotografie.'),
('Coordonare la vârf','Lider tehnic: un PO, sprinturi comune și integrare pe extensii cu teste pe ambele teme; niciun schimb de tenant implicit.'),
('Cost Club și AI','Financiar: plafon lunar aprobat pentru puncte, reconciliere și control de marjă; E4/E5 împart plafonul, fără dublarea bugetului de 600 EUR.')],[4.2,13.3])
p('Documentele A3 și addendumul stabilesc planul, nu probează implementarea. Cererea de oferte, contactarea furnizorilor, activarea E0 și orice modificare pe site sunt activități ulterioare. În această revizie s-au realizat citire, verificare documentară și redactare.')
page('18 Recepția programului')
table(['Cod','Livrabil și prag','Probă de închidere'],[
('R00','Un singur motor; E0–E7 sunt extensii aprobate în registru. Zero catalog, backend comercial sau autentificare paralele.','Mapă rută → E# → modul Flask → tenant → contract OpenAPI → test.'),
('R01','100% rânduri/câmpuri sursă contabilizate; loturi publicate eligibile.','D01, hashuri, reconciliere și aprobare editorială.'),
('R02','25 tipuri proiectate, 75 ecrane; 21 tipuri de bază +2 E6/E7, două concepte.','D03 și fișiere editabile; testele disting designul de implementare.'),
('R03','≥90% succes pe sarcini; add-to-cart median ≤60 s; checkout local ≤90 s.','2×8 participanți; timpii PSP/SCA raportați separat; SUS ≥80.'),
('R04','Zero defecte critice de total, stoc, plăți, tenant și facturare.','Regresie izolată pe ambele teme; operațiile sensibile sunt conduse de om.'),
('R05','20 serii și 12 scene în temă; E4–E7 conform R12.','Dicționar aprobat, 10 scenarii configurator și alternative accesibile.'),
('R06','URL-uri existente păstrate; 6 limbi și SEO fără erori critice.','Crawl comparativ veche/nouă, canonical/hreflang/JSON-LD.'),
('R07','Bugete de performanță, WCAG 2.2 AA și zero vulnerabilități exploatabile critice/înalte.','CI, audit manual și RUM după pilot.'),
('R08','Comutare temă <1 min; recuperare completă ≤15 min; RPO/RTO conform ADR04.','Exercițiu pe staging/cohortă, fără restaurarea bazei peste comenzi noi.'),
('R09','Matrice legală aplicabilă pe piețe/familii; E0 recepționat înaintea temei.','Dovadă retragere, documente reale, fiscalitate și semnături juridic/financiar.'),
('R10','Raport temă și rapoarte extensii la 90 zile de la activarea fiecăruia.','D02, cohorte, costuri, intervale statistice și limitări.'),
('R11 și R12','Recepții distincte ale temei și ale extensiilor.','Criteriile și probele din §18.1–18.2.')],[1.1,8.4,8],small=9.5)
p('Niciun statut „planificat” nu se transformă în „livrat” fără versiune, raport, dată și semnatar. Defectele critice blochează activarea; datele sau documentele fabricii lipsă nu sunt înlocuite de o notă de audit. E0 și exercitarea drepturilor nu sunt un comutator de marketing.')
page('18.1 R11 Recepția temei')
table(['Criteriu','Probă'],[
('Înregistrare și validare','Manifest, files și page_contracts; raport al validatorului /admin/api/tenants/<tenant>/validate fără erori pentru identificatorul CESIRO confirmat în D01.'),
('Pagini și limbi','21 tipuri de bază ×6 limbi, rutele/stările mapate în D03; două tipuri suplimentare la E6/E7. Zero chei lipsă și zero texte de interfață fixe în șabloane.'),
('Citire fără JavaScript','Conținutul esențial al celor 21 tipuri rămâne lizibil fără JavaScript; paginile publice sunt navigabile. Funcțiile interactive au alternativă sau mesaj clar, fără pagini goale.'),
('Izolarea temei','Zero modificări de temă în templates/shared. Extensiile motorului au diff separat și regresie pe marketplace_pro; logica comercială nu se copiază în temă.'),
('Comutare și revenire','Activare/revenire din admin în <1 minut, fără deploy, cu sesiuni/coș/comenzi păstrate. Preview autorizat și selecție persistentă pe cohortă.'),
('URL-uri și SEO','Crawl comparativ pe aceleași URL-uri; title, canonical, hreflang, JSON-LD, limbă și conținut esențial corecte.'),
('Zece variante','parent=cesiro_atelier; tokenuri și mesaje distincte; theme_schedule verificat pentru anotimpuri, evenimente și ambele calendare pascale.'),
('Performanță','Limitele §10 pe tip de pagină; pe produs, componente React inițiale ≤120 KB și total JS inițial ≤170 KB comprimat.'),
('Compatibilitate','Zero handleri dubli, diferențe de hidratare sau scurgeri între tenanturi; test coș/checkout pe noua temă și pe rezervă.')],[5.1,12.4])
p('R11 privește tema și comportamentul ei real. Faptul că o pagină are machetă nu permite marcarea ei ca suportată în manifest. Rolul de cititor, editor, administrator și client este verificat separat; tokenul admin folosit de validator nu ajunge în frontend.')
h('Predare și operare')
p('Se predau sursele, buildurile reproductibile, licențele, inventarul media, contractele, rapoartele și manualul de comutare. Două persoane pot activa, reveni și identifica extensiile fără dependență de autorul codului. Tema de rezervă este păstrată și testată cu toate migrările additive.')
page('18.2 R12 Recepția extensiilor')
table(['Cod','Prag obligatoriu','Probă'],[
('E0','12 scenarii §12.1; fără cont/motiv; confirmare durabilă fără întârziere; reactivare retur în condițiile aprobate.','Operator uman, jurnal și dovadă; fără execuție AI de anulări/retururi.'),
('E1','Serie și persoane în 6 limbi; 20 serii și 100 SKU-uri validate, zero decoruri greșite.','Teste de contract vechi/noi și aprobarea fabricii.'),
('E2','Grant unic și expirabil, o comandă/un tenant; revocare, replay și enumerare controlate.','Test de securitate și izolare; GET fără consumare; lipsă token în log/analytics.'),
('E3','20 CUI-uri de test; active/inactive/invalide și timeout; completare manuală disponibilă.','Raport contract ANAF simulat și validare client; fără confuzie cu e-Factura.'),
('E4','200 +100 cereri; ≥90% corecte/utile; zero divulgări/acțiuni interzise; p95 ≤4 s primul răspuns.','Etalon versionat, atacuri, informare AI, cost și capacitate PGX.'),
('E5','150 imagini; Recall@5 ≥85% pe 100 prezente; ≤1 fals exact/50 absente; nDCG@10 ≥0,80 în fiecare limbă.','60 interogări/limbă; ștergere foto ≤24 h; test actualizare/filtrare produse retrase.'),
('E6','20 comenzi simulate reconciliate; 10 proof-uri fizice aprobate; fișier SVG/PDF 1:1 cu hash.','Fabrică, preflight, bifa de informare și termen din registru.'),
('E7','Puncte idempotente, fără dublă cheltuire, ajustare după retur uman și expirare; cost plafonat.','Funcții pure pe evenimente sintetice; probele operaționale sensibile de către om.')],[1.3,9,7.2],small=9.5)
p('Cerințe comune: feature flag pe tenant, autorizare și CSRF conforme motorului, rate limit, schema erorilor, OpenAPI, migrare documentată, regresie pe ambele teme și oprire fără pierdere de date. Funcția oprită are alternativă clară și nu lasă butoane fără efect.')
p('E4/E5 se activează numai după PoC și pragurile de calitate/cost; E6 numai după proof și capacitate; E7 numai după regulile financiarului. Dacă pragurile nu se ating, extensia rămâne nelivrată și are plan de remediere sau schimbare de domeniu explicită. Nu se declară închisă pentru că există cod sau pentru că tema a fost lansată.')


page('19 Eșantionul intern și exemplele țintă')
p('Am analizat un eșantion reproductibil de 50 înregistrări din exportul intern: câte 5 din 10 grupe operaționale. Încadrarea preliminară folosește termeni din denumire, în ordine, cu o singură grupă per înregistrare; selecția folosește hashul ID-ului, cu includerea prioritară a produsului de tip variable. Este o examinare de câmpuri, nu certificare tehnică, test de stoc curent sau verificare fizică. Lista de ID-uri/SKU-uri este păstrată în Matrice_Raspuns_Audituri_CESIRO_V2.docx, anexa eșantionului.')
p(f'În eșantion, {stats["sample_missing"].get("GTIN, UPC, EAN sau ISBN",0)} înregistrări nu au GTIN/EAN, {stats["sample_missing"].get("Descriere",0)} nu au descriere, iar {stats["sample_missing"].get("Greutate (kg)",0)} nu au greutate. Aceste lipsuri justifică prioritizarea și verificarea sursei actuale. Nu s-a identificat un produs denumit sau categorizat ca personalizabil în export; capabilitatea de personalizare este un pilot propus, nu o ofertă existentă confirmată.')
table(['Caz','Conținut existent și transformare țintă'],[
('Ceașcă 220 ml\nSKU 5900_2763_2070_G242','Exemplul public are culoare/decor și preț. Fișa țintă adaugă seria validată, fotografie la scară, capacitate pe piesă, îngrijire confirmată, livrare și completare. Dimensiunile/greutatea estimate nu devin certe.'),
('Set 9 piese\nSKU 5900_3216_9718_D144','Titlul de set și descrierea de cană trebuie reconciliate. Fișa țintă arată componente și cantități, 200 ml doar la cană, material pe componentă, persoane confirmate și fotografii ale conținutului complet.'),
('Detergent sau consumabil Pro','Fișa țintă afișează volum/unitate, dozaj și documente aplicabile, ambalare, praguri existente de cantitate, preț public și cerere repetată; prețul contractual pe client rămâne ulterior; nu intră în scenele de ceramică.'),
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


page('20.1 Surse interne și probe de referință')
p('I1 — Audit.Claude.V1.0.docx și Audit.Gemini.v1.0.pdf; I7 — Audit.Claude.V2.0.docx, Audit Tehnic si Directii Arhitecturale CESIRO v2.0.pdf, Audit.Claude.V2.0.Addendum1.docx, Audit.Claude.V3.0.docx și Audit.Claude.V3.0.Addendum1.docx. Toate sunt păstrate în folderul Audituri. A3 are 80 coduri unice: 44 observații și 36 propuneri.')
p('I2 — U:/cesiro.com/backend/requirements.txt și frontend/package.json. I3 — backend/app/factory.py, api/storefront.py, cms.py, gift.py, theme_schedule.py, theme_preview.py, payments/stripe_gateway.py, api/admin/resources/assistant.py și templates/themes/generic/account.html. Citire statică, fără apeluri tranzacționale.')
p('I4 — U:/cesiro.com/wc-product-export-16-9-2026-1789549595309.csv. SHA-256: bbbf54a45baa5dc098b40a7765f7c122ff1179162a0b480e055716407843dbe8. Agregatele și eșantionul de 50 produse din evidence-v2 rămân istorice și reproductibile; nu sunt inventar curent.')
p('I5 — U:/cesiro.com/REGULI.md, citit: nicio anulare/retur/rambursare executată de AI, inclusiv în teste; nicio modificare a comenzilor marketplace. I6 — README, themes/README, manifests, page_contracts, Docker Compose și hashurile din evidence-v4/source-hashes.json. U: mapat la \\\\192.168.100.151\\site-uri; GitHub cesiroproduction/site-uri a returnat 404 prin conexiunea disponibilă la 21 octombrie 2026.')
p('I8 — Z:/images și _RAPORT/index.html: 38.872 fișiere, 38.865 cu extensie de imagine la inventariere. Numărul include posibile duplicate și active neeligibile. Fotografiile planșelor au sursă și hash în evidence-v4/visual-sources.json; clasificarea arhivei nu certifică originea, drepturile sau compatibilitatea produsului.')
p('I9 — U:/acc-florin/app/main.py:1206, anaf_lookup; logică de validare CUI și citire ANAF identificată. Nu au fost citite baze de facturi, setări secrete sau date personale și nu s-a apelat serviciul ANAF.')
for x in [('S1 CESIRO pagina principală','https://cesiro.com/'),('S2 CESIRO sitemap','https://cesiro.com/sitemap.xml'),('S3 Ceașcă 220 ml','https://cesiro.com/p/ceasca-cu-farfurioara-220-ml-maro-decorat-cu-flori-si-spic-de-grau'),('S4 Set 9 piese','https://cesiro.com/p/set-masa-4-pers-9-piese-cana-roz-200-ml-bol-tava-termorezistenta-portelan-cu-trandafiri-roz'),('S5 CESIRO întrebări frecvente','https://cesiro.com/legal/intrebari-frecvente'),('S6 CESIRO termeni și identitatea vânzătorului','https://cesiro.com/legal/termeni-si-conditii'),('T2 Core Web Vitals','https://web.dev/articles/vitals'),('T3 WCAG 2.2','https://www.w3.org/TR/WCAG22/'),('T4 Google Consent Mode','https://developers.google.com/tag-platform/security/guides/consent'),('T5 Google Search și funcțiile AI','https://developers.google.com/search/docs/appearance/ai-features')]:link(*x)
p('Starea sursei, starea configurației și starea producției sunt distincte. Manifestul local permite repetarea lecturii; commitul și digestul instalat sunt livrabile D01. Lipsa accesului GitHub nu este dovadă că repository-ul nu există.')


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
page('20.3 Surse actualizate pentru V4')
for x in [
('S6 CESIRO identitatea vânzătorului','https://cesiro.com/legal/termeni-si-conditii'),
('T7 ANAF înregistrarea aplicațiilor OAuth','https://static.anaf.ro/static/10/Anaf/Informatii_R/API/Oauth_procedura_inregistrare_aplicatii_portal_ANAF.pdf'),
('L10 Directiva 2023/2673 funcția de retragere și aplicarea','https://eur-lex.europa.eu/eli/dir/2023/2673/oj/eng'),
('L10b OUG 34/2014 dreptul de retragere și excepții','https://legislatie.just.ro/Public/FormaPrintabila/00000G1YMI9WLN4N9523GGWAROSL0LJK'),
('L11 Regulamentul 2025/2439 calendarul CLP','https://eur-lex.europa.eu/eli/reg/2025/2439/oj/eng'),
('L12 HG 947/2000 prețul pe unitate și excepții','https://legislatie.just.ro/Public/DetaliiDocumentAfis/24730'),
('L13 Biocide articolul 72','https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:02012R0528-20220415'),
('L14 Regulamentul 2026/405 articolul 37','https://eur-lex.europa.eu/eli/reg/2026/405/oj/eng'),
('L15 Comisia Europeană portalul de soluționare a litigiilor','https://consumer-redress.ec.europa.eu/'),
('B10 Bonna colecții','https://www.bonna.global/all-collections'),
('B11 Lubiana clienți profesionali','https://lubiana.com.pl/biznesowy/')]:link(*x)
p('Consultare la 21 octombrie 2026. Registrul juridic al implementării trebuie să verifice textele consolidate, transpunerile și condițiile pieței efective. Sumele și debitele de lucru sunt ipoteze explicite de estimare; nu sunt cotații obținute de la furnizori.')

def board_image(path,width):
    pa=p('');pa.alignment=WD_ALIGN_PARAGRAPH.CENTER
    sh=pa.add_run().add_picture(str(path),width=Cm(width))
    sh._inline.docPr.set('descr','Fotografie din arhiva CESIRO pentru direcția vizuală; '+Path(path).name)
    return pa

def concept(idx,title,subtitle,hero,product,name,fonts,colors,idea,cta):
    page(f'21.{idx} '+title)
    p(subtitle)
    board_image(hero,10.6 if idx==3 else 8.5)
    pa=p('');r=pa.add_run(title);r.font.name=fonts[0];r.font.size=Pt(24);r.font.color.rgb=RGBColor.from_string(colors[1])
    pa=p('');r=pa.add_run('Titluri '+fonts[0]+'   |   Text '+fonts[1]);r.font.name=fonts[1];r.font.size=Pt(11)
    t=table(['Fundal','Text','Accent'],[[f'#{colors[0]}',f'#{colors[1]}',f'#{colors[2]}']],[5.83,5.83,5.84])
    for c,col in zip(t.rows[1].cells,colors):
        sh=OxmlElement('w:shd');sh.set(qn('w:fill'),col);c._tc.get_or_add_tcPr().append(sh)
        for pa in c.paragraphs:
            for rr in pa.runs:rr.font.color.rgb=RGBColor.from_string('FFFFFF' if col==colors[1] else '000000')
    p(idea)
    h('Fragment de pagină de produs')
    t=doc.add_table(rows=1,cols=2);t.autofit=False;t.columns[0].width=Cm(5.8);t.columns[1].width=Cm(11.7)
    pr=t._tbl.tblPr;bd=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideV']:
        el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');bd.append(el)
    pr.append(bd)
    for cell in t.rows[0].cells:
        m=OxmlElement('w:tcMar')
        for edge in ['top','bottom','left','right']:
            el=OxmlElement('w:'+edge);el.set(qn('w:w'),'100');el.set(qn('w:type'),'dxa');m.append(el)
        cell._tc.get_or_add_tcPr().append(m)
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
    c=t.cell(0,0);c.paragraphs[0].add_run().add_picture(str(product),width=Cm(5.4));c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    c=t.cell(0,1);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    pr=c._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),colors[0]);pr.append(sh)
    pa=c.paragraphs[0];rr=pa.add_run(name);rr.font.name=fonts[0];rr.font.size=Pt(18)
    for tx in ['Preț și disponibilitate din catalog','Alege piesele sau cantitatea • Ambalaj și mesaj cadou',cta,'Materiale • Dimensiuni • Producător • Îngrijire']:
        pa=c.add_paragraph();rr=pa.add_run(tx);rr.font.name=fonts[1];rr.font.size=Pt(11);rr.bold=(tx==cta)
        if tx==cta:rr.font.color.rgb=RGBColor.from_string(colors[1])
    p('Fotografii din arhiva locală, fără modificarea produsului; sursele exacte sunt în I8 și manifestul vizual. Prețul, certificările și stocul nu sunt inventate. Fragmentul este design, nu pagină implementată.').runs[0].font.size=Pt(8.5)

imgroot=Path('Z:/images/Bucatarie & Masa')
mug=imgroot/'Cani & Cesti/cana-striatii-bej-model-cesiro-casa-masa-familie-locuin-01.jpg'
white=imgroot/'Seturi de masa (Vesela)/010l-set-16-01.jpg'
green=imgroot/'Seturi de masa (Vesela)/set-mic-dejun-verde-aranjat-01.jpg'
dark=imgroot/'Seturi de masa (Vesela)/set-vesela-ceramica-24-piese-negru-cu-tacamuri-aurii-01.jpg'
concept(1,'Atelier și glazură','Produsul în prim plan, textură și ritm calm; potrivit poveștii de fabricație.',mug,mug,'Cană cu striații bej',('Georgia','Arial'),('F3E9DD','4B3026','C58C69'),'Compoziție aerisită, fotografie de obiect mare și informații de proveniență lângă produs. Detaliile tactile conduc alegerea; promisiunile de fabricație cer dovezi.','Adaugă în coș')
concept(2,'Masa de acasă','Oameni, gesturi și ocazii cotidiene; direcția recomandată pentru test.',green,white,'Set pentru masa de fiecare zi',('Cambria','Calibri'),('F4F1E6','2F583D','AFCA84'),'Intrarea principală este după momentul zilei și numărul de persoane. Fotografia în utilizare și butonul de compunere a mesei precedă lista de categorii.','Compune masa ta')
concept(3,'Colecția contemporană','Contrast puternic, decor recognoscibil și cadouri pentru ocazii.',dark,dark,'O masă în negru',('Arial Black','Arial'),('F0F1F4','182133','DAB86E'),'Structură geometrică, titluri ferme și accent rezervat selecției. Decorul și combinațiile au prioritate; fotografia de scenă nu promite includerea tacâmurilor.','Vezi piesele colecției')

for i,ttl in [(4,'Homepage pe mobil'),(5,'Produs pe mobil'),(6,'Masa completă pe mobil')]:
    page(f'21.{i} '+ttl)
    p('Wireframe de structură și conținut. Ilustrațiile și textele sunt schițe de interfață; datele comerciale vor proveni din catalog.')
    sh=doc.add_picture(str(OUT/'visuals-v3'/f'plan-{i}.png'),width=Cm(17.1));sh._inline.docPr.set('descr',ttl+' cu explicația zonelor și a accesibilității')
    p({4:'Căutare, utilizări și completarea decorului; E4/E5 au intrări distincte numai după activare.',5:'Produsul identifică producătorul și datele verificate; personalizarea apare numai pe cele 10 produse eligibile E6.',6:'Lista oferă același rezultat ca scena 2D, cu tastatură, cantități editabile și total reverificat.'}[i])


page('22 Versiunea de referință și registrele')
p('V4 consolidează proiectul V3, Audit Claude V3.0 și cele două addendumuri. Varianta C planifică tema și E0–E7 în motorul existent. Addendumul V3 stabilește domeniul și estimarea curente; cerințele de temă din addendumul V2 sunt preluate cu inventarul actual de 25 tipuri și R11. Variantele istorice de arhitectură, termene și bugete nu sunt contractul V4.')
p('Matricea V4 urmărește toate cele 80 coduri A3, cerințele celor două addendumuri și schimbarea statusurilor A2 relevante. V2/V3 și auditurile sunt păstrate. Nota 8,3/10 din audit și estimarea condiționată 8,8/10 din addendum aparțin auditorului; documentația V4 nu își acordă singură o notă și nu pretinde că sistemul a fost recepționat.')
table(['Registru','Responsabil și termen','Ieșire'],[
('D01','Platformă și date S1–2','Commit/digest, tenant, sursă curentă, snapshot și reconciliere; manifest local de hashuri deja disponibil.'),
('D02','Financiar și analytics S1–2','Baze comerciale, trafic, marjă, cost intern și recalibrarea țintelor.'),
('D03','UX și editorial S1–4','25 tipuri cu status, 75 ecrane, mapă de rute, două runde de test și concept ales.'),
('ADR01–04','Lider tehnic și DevOps S1–2','Temă, pgvector/LLM, cache, infrastructură și nivel de continuitate.'),
('E0/E2 urgent','Platformă juridic și suport S1–3','Fluxuri testate de om pe tema actuală; dovadă de exercitare a drepturilor.'),
('R00 și OpenAPI','Tehnic S1–4 și la fiecare extensie','Rute și migrări aprobate, comutatoare și contracte fără sistem paralel.'),
('Fabrică și Club','Fabrică/financiar înainte de activare','100 SKU-uri și 20 serii, 10 proof-uri, capacitate E6 și cost puncte E7.'),
('R11 și R12','Proprietarii recepției','Versiune, raport, data activării și semnătură per temă/extensie.'),
('R10','PO și analytics la 90 zile','Raport separat per livrare, cu cohortă, cost și incertitudine.')],[4.1,5.4,8])
p('Starea acestei livrări: proiect și matrice redactate, surse citite și planșe pregătite. Nu au fost schimbate site-ul, Dockerul, backendul, bazele, integrările sau repository-ul; nu s-au trimis mesaje către furnizori. Implementarea, probele operaționale și activările rămân lucrări viitoare din calendar.')


save('Proiect_CESIRO_Design_React_Python_V4.docx')
print('Proiect V4 salvat')
