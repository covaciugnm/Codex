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
    n=doc.styles['Normal'];n.font.name='Calibri';n.font.size=Pt(11)
    n.paragraph_format.space_after=Pt(6);n.paragraph_format.line_spacing=1.04
    for st in doc.styles:
        for x in list(st.element.xpath('.//w:pBdr')):x.getparent().remove(x)
    for nm,sz in [('Title',27),('Subtitle',14),('Heading 1',19),('Heading 2',12)]:
        st=doc.styles[nm];st.font.name='Calibri';st.font.size=Pt(sz);st.font.color.rgb=RGBColor(0,0,0)
        st.paragraph_format.space_before=Pt(8);st.paragraph_format.space_after=Pt(7)
        st.paragraph_format.keep_with_next=True
    doc.core_properties.title=title;doc.core_properties.author='';doc.core_properties.subject='Revizie documentară pe baza auditurilor Claude și Gemini'
    f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=f.add_run('CESIRO  •  '+short+'  •  21 octombrie 2026  •  ');r.font.size=Pt(8)
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
def p(t,style=None):return doc.add_paragraph(t,style)
def b(t):p(t,'List Bullet')
def h(t):doc.add_heading(t,2)
def head(t):doc.add_heading(t,1)
def page(t):doc.add_page_break();doc.add_heading(t,1)
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

init('Proiect CESIRO pentru design și dezvoltare React și Python','Proiect V2')
p('Proiect CESIRO pentru design și dezvoltare React și Python','Title')
p('Versiunea 2 revizuită după auditurile Claude și Gemini','Subtitle')
p('Destinat conducerii CESIRO, echipei de produs, furnizorilor de dezvoltare și auditorilor. Bază pentru decizie, estimare și recepție.')
h('0 Direcția propusă')
p('cesiro.com va deveni locul în care clientul își compune masa, completează decorul preferat și comandă un cadou personal, cu informații verificabile despre produs și livrare. Ceramica CESIRO conduce experiența de brand. Zona Pro deservește distinct HoReCa și consumabilele, folosind același catalog și același motor comercial.')
p('De la Trendyol preluăm claritatea accesului la produse, căutarea și filtrarea. Identitatea vizuală, conținutul și serviciile sunt proiectate pentru un brand de ceramică: culoare, glazură, decor, utilizare și legătura cu fabrica. Referințele comparative sunt prezentate în capitolul 20.')
h('Ce se schimbă față de versiunea 1')
b('Infrastructură EVA Storefront confirmată în fișiere: Python Flask, SQLAlchemy, PostgreSQL și administrare React. Proiectul reutilizează această bază; Django nu mai este soluția propusă.')
b('Inventar intern din exportul disponibil, control al calității întregului catalog și un eșantion de 50 de produse. Datele istorice sunt separate de starea curentă.')
b('Funcții comerciale diferențiatoare în patru valuri: masă completă, căutare vizuală, asistent de cumpărare, personalizare, liste de eveniment, fidelitate și Pro.')
b('Obiective comerciale definite prin formule, buget în trei scenarii, responsabilități, criterii de lansare și răspuns trasabil la fiecare punct de audit.')
h('Trei motive concrete pentru cumpărarea directă')
table(['Diferențiator','Rezultat verificabil propus'],[
('Origine și încredere','100% din produsele promovate ca fabricate de CESIRO au proveniență documentată; promisiunea privind spargerea este legată de o politică și un proces aprobate.'),
('Masa potrivită și completarea seriei','12 scene cumpărabile și minimum 20 de serii eligibile la finalul valului 3; setul se poate ajusta după persoane și buget.'),
('Cadou personal','Pilot de 10 produse personalizabile, previzualizare și fișă de producție; țintă de 5% din comenzile eligibile la 90 de zile după activare.')],[4.2,13.3])
p('Calendar recomandat: 18 săptămâni de la îndeplinirea condițiilor de pornire, apoi 90 de zile de măsurare. Nota finală aparține auditorilor; acest document definește probele necesare, nu declară anticipat obținerea notei 10.')

page('1 Date disponibile și dimensiunea reală')
p('Revizia folosește cele două audituri primite, constatările publice CESIRO din 21 octombrie 2026, citirea statică a unor fișiere din U:/cesiro1-site și exportul de produse datat în nume 16 septembrie 2026. Nu au fost accesate baze de date operaționale, conturi de clienți sau rapoarte de vânzări. [I1–I5, S1–S4]')
table(['Sursă','Constatare','Limită'],[
('Export intern de produse','5.222 rânduri și ID-uri distincte; 5.221 SKU-uri nenule distincte; 1 SKU lipsă.','Instantaneu istoric, nu inventar curent.'),
('Stare în export','5.211 publicate, 11 cu valoarea −1; 5.217 simple, 2 grouped, 2 external, 1 variable.','Tipul exportului trebuie mapat la modelul actual; active nu înseamnă în stoc.'),
('Sitemap public','32.868 URL-uri; 31.674 de produs = 5.279 × 6 limbi.','Nu reprezintă 31.674 SKU-uri. Diferența față de export nu dovedește produse noi.'),
('Câmpuri lipsă în export','EAN/GTIN 1.145; descriere 670; imagini 50; greutate 2.014; stoc 23; preț obișnuit 5.','Lipsa din export nu dovedește lipsa în producție; GTIN nu se inventează.'),
('Structură software locală','Flask, SQLAlchemy, Alembic, PostgreSQL; admin React, TypeScript, Vite, TanStack.','Prezența codului nu certifică versiunea instalată sau funcționarea integrărilor.')],[3.5,7.8,6.2])
h('Inventarul contractual și analiza ABC')
p('În primele 3–5 zile lucrătoare, responsabilul de date livrează un export curent pe tenant: produse, variante, relații, stoc pe depozit/canal, istoric de preț și vânzări agregate pe 12 luni. Se stabilesc separat N produse, N SKU-uri vandabile, N active în ultimele 90 de zile și N traduceri. Numărătorile, hashurile și data de referință se semnează în registrul D01.')
p('ABC se calculează după venitul net cumulat: A până la 80%, B următoarele 15%, C restul; marja și rotația sunt dimensiuni suplimentare. Lista de maximum 300 produse prioritare combină grupa A, disponibilitatea, marja și reprezentativitatea brandului. Nu presupunem că 300 de produse generează deja 80% din venit.')
h('Portofoliul')
p('Vitrina principală prezintă Ceramică și Masă. /pro grupează HoReCa și consumabilele; produsele din alte familii rămân în inventar și primesc o decizie de canal, fără ștergere automată. Vizibilitatea publică și URL-urile existente se tratează individual, cu analiză de trafic și redirecționare relevantă. Subdomeniul Pro nu este necesar la început.')

page('2 Modelul datelor și folosirea integrală')
p('Fiecare înregistrare și fiecare câmp sursă primește o destinație: utilizare, normalizare, revizuire sau arhivare justificată. Se păstrează valoarea originală, sursa, data, regula, autorul aprobării și versiunea. Arhiva brută poate fi completă înainte ca îmbogățirea editorială să fie terminată; lansarea se face pe loturi eligibile.')
table(['Grup de date','Date existente reutilizate','Extindere cerută'],[
('Identitate','ID, SKU, EAN/GTIN, slug, brand, părinte, tip, vizibilitate','ID canonic stabil; mapare între surse și canale; identificarea producătorului real.'),
('Conținut și limbi','Nume, texte, categorii, atribute, tags, traduceri','Serie/decor, rol în set, stil, ocazie, relație destinatar, nivel de validare pe limbă.'),
('Comerț','Prețuri, monedă, taxe, disponibilitate, stoc, precomandă','Istoric efectiv al prețului, marjă doar intern, rezervări, cantități minime, preț pe client Pro.'),
('Caracteristici','Material, culoare, capacitate, dimensiuni, greutate, bucăți','Unități normalizate; culoare vizuală validată; măsurători reale; componente și persoane justificate.'),
('Conformitate','Date existente ale furnizorului și pagini de politici','Producător și contacte, operator UE când se aplică, avertismente, lot, declarații și documente alimentare.'),
('Media și SEO','Imagini, ordine, metadate, canonical, hreflang, JSON-LD','Drepturi, alt, dimensiuni, video, modele 3D, marcaj compoziție, URL-uri și redirecturi istorice.'),
('Relații comerciale','Upsell, cross-sell, produse grupate, recenzii','Relații serie–piesă–componentă–scenă; proveniența recomandării, UGC moderat, favorite.'),
('Operațional','Ambalare, livrare, retur, integrare și depozit','Greutate colet, fragilitate, termen de producție, capacitate confirmată, reguli de spargere.')],[3.1,6.2,8.2])
h('Dicționare pe familii')
p('Veselă și căni: material, decor, diametru/capacitate, rol și utilizări verificate. Seturi: listă exactă de componente și cantități, persoane fără deducere din numărul total de piese. Gătit: temperatură și surse de încălzire documentate. Decor: dimensiuni, utilizare și stabilitate; nu se presupune contact alimentar. Curățenie: cantitate, dozaj, avertismente și documentația specifică substanței, după caz.')
p('Capacitatea de 200 ml a unei căni dintr-un set aparține componentei. Valoarea necunoscută nu devine zero. Compatibilitatea, proveniența, rezistența și certificările nu se deduc din fotografie. HEX și stilul produse de AI sunt propuneri editoriale. Câmpurile comerciale publice nu expun costul sau marja.')

page('3 Calitate și îmbogățire asistată')
h('Scor de calitate și condiții obligatorii')
p('Scorul editorial este 0–100: atribute utile 30, media 25, descriere și consistență 20, localizare 15, relații de serie 10. Fiecare familie are o grilă cu câmpuri aplicabile; lipsurile și contradicțiile produc punctajul, cu versiune de calcul. Produse prioritare ≥90; catalog secundar ≥60. Pragurile nu înlocuiesc condițiile legale și comerciale.')
p('Publicarea cumpărabilă cere separat identitate, preț valid, disponibilitate calculabilă, media corectă și toate informațiile/documentele obligatorii pentru familia și piața respectivă. Un produs cu scor 100 și o condiție obligatorie neîndeplinită nu poate fi activat pentru vânzare.')
h('Fluxul de lucru')
table(['Etapă','Activitate și livrabil','Acceptare'],[
('Preluare','Arhivă nemodificată, hash, mapare de câmpuri și raport de reconciliere D01.','100% rânduri contabilizate; 0 identificatori pierduți.'),
('Reguli','Normalizare unități, duplicate, tipuri, categorii și contradicții.','Toate erorile primesc proprietar și destinație.'),
('AI în proiect izolat','Propuneri de descriere, traducere, stil și asocieri; încredere și sursă pentru fiecare sugestie.','Nicio specificație critică sau informație legală inventată; aprobare umană.'),
('Evaluare și loturi','Set etalon 200 produse, câte 40 din 5 familii majore; eșantion manual de verificare.','Precizie ≥95% pentru atributele descriptive evaluate; 100% corectitudine pentru numerele publicate.'),
('Monitorizare','Raport zilnic de regresie, traduceri restante și surse expirate.','Alertă la scăderea scorului sau lipsa unui câmp obligatoriu; blocare publicare nouă.')],[3.1,8.7,5.7])
p('PGX/Qwen rămâne candidat pentru execuție locală; capacitatea, modelul, licența, accesul și costul per 1.000 produse se măsoară în PoC. Existența modulului ai_assistant este confirmată în fișiere, dar nu dovedește disponibilitatea unui serviciu de inferență potrivit pentru toate funcțiile. Conținutul de produs și încărcările utilizatorilor sunt date nefiabile, niciodată instrucțiuni pentru agent.')
h('Proveniență și promisiuni')
p('Anul 1957 și afirmațiile privind capacitatea fabricii sunt informații de brand care necesită validare documentară. Superlativele, originea, sustenabilitatea și garanția „100%” se aprobă juridic și operațional înainte de campanie. Fișa de trasabilitate propusă nu este prezentată ca pașaport digital obligatoriu pentru toată ceramica. [L1, L2, L7]')

page('4 Obiective și rezultate cuantificabile')
p('Indicatorul principal este venitul net lunar din canalul direct: valoarea produselor facturate fără TVA, minus reduceri, anulări și retururi, fără transport. Sursa financiară prevalează asupra atribuirii din analytics. Toate creșterile procentuale de mai jos sunt relative, dacă nu este indicat „puncte procentuale”.')
table(['Obiectiv','Țintă propusă','Măsurare și termen'],[
('Venit direct','+15% față de baza comparabilă; marja de contribuție/comandă nu scade.','90 zile după valul 4; control pentru buget media, sezon și disponibilitate.'),
('Conversie mobilă','+15% față de baza segmentată.','Comenzi plătite valide / sesiuni mobile eligibile; fără boți și trafic intern.'),
('Valoarea coșului','+10% AOV net.','Venit net produse / comenzi valide, aceeași perioadă și definiție.'),
('Recumpărare','+3 puncte procentuale la 90 zile.','Clienți cu a doua comandă în 90 zile / cohortă cu 90 zile complete.'),
('Abandon checkout','−15% relativ.','1 − comenzi valide / sesiuni cu begin_checkout; fereastră de atribuire 7 zile.'),
('Descoperire asistată','≥10% dintre sesiunile expuse folosesc AI, căutare vizuală sau configurator.','90 zile după valul 3; utilizarea și conversia se raportează separat.'),
('Personalizare','≥5% din comenzile cu produse eligibile includ personalizare.','90 zile după activarea pilotului; marja după costul producției este pozitivă.'),
('Încredere','Recenzii noi la ≥5% din comenzile livrate eligibile; spargeri fără creștere peste 0,3 pp.','Recenzii autentice; retururi și costul despăgubirii urmărite pe cohortă.')],[4.1,6.3,7.1])
h('Baza de comparație')
p('Baza comercială nu este disponibilă în fișierele inspectate. Registrul D02 se completează în săptămâna 1 din 12 luni de vânzări agregate și minimum 8 săptămâni de trafic măsurabil; include mobil/desktop, țară, canal, consimțământ, marjă și retururi. Aprobarea D02 precede fixarea angajamentelor comerciale și a bugetului final. Exemplele numerice nu vor fi prezentate drept performanță actuală.')
p('Recepția livrabilelor se bazează pe criterii tehnice și UX controlabile. Țintele comerciale sunt ipoteze de creștere evaluate separat; traficul redus sau schimbările de preț/media nu se transformă într-o concluzie cauzală nejustificată.')

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

page('6 Experiența vizuală și paginile')
p('Se compară trei direcții creative prin moodboard și prototip de homepage/produs la 390 px: „Atelier și glazură” cu texturi autentice și gesturi de producție; „Masa de acasă” cu scene cotidiene și culori calde; „Colecția contemporană” cu compoziții grafice și accent pe decor. Recomandarea inițială combină a doua direcție cu dovezi de fabricație din prima. Alegerea rezultă din două runde cu câte 8 participanți și criterii documentate.')
table(['Grup','Tipuri de pagini și stări'],[
('Descoperire 1–6','1 Homepage; 2 categorie/listare; 3 rezultate căutare; 4 produs; 5 decor/serie; 6 colecție/ocazie.'),
('Compoziție 7–10','7 scenă cumpărabilă; 8 configurator de masă; 9 selector cadou; 10 personalizare produs.'),
('Tranzacție 11–14','11 coș; 12 checkout; 13 confirmare/urmărire; 14 cont cu favorite, istoric și vizualizări recente.'),
('Relație 15–18','15 listă eveniment publică și administrare; 16 Club CESIRO; 17 card cadou; 18 Outlet.'),
('Brand 19–22','19 poveste/fabrică/showroom; 20 Jurnal și articol; 21 UGC/recenzii; 22 ajutor și politici.'),
('Profesional 23–24','23 portal Pro și comandă rapidă; 24 ofertă/mostre/logo. Compararea a până la 4 produse este un modul transversal.')],[4,13.5])
p('Livrabil: 24 tipuri, fiecare cu referințe la 390, 768 și 1440 px, minimum 72 ecrane de bază, plus stări de eroare, gol, încărcare și lipsă stoc pentru fluxurile aplicabile. Numărul de ecrane nu substituie acoperirea funcțională. Prototipul prioritar este mobil; checkoutul permite comandă fără cont și salvarea progresului.')
h('Ordinea pe pagina principală și pe produs')
p('Homepage: căutare și meniu → promisiune verificată → produse/ocazii → compune masa → colecții după decor și culoare → origine → recenzii autentice → Pro. Produs: imagini și scară → nume/serie → preț și disponibilitate → variante → livrare → acțiune de cumpărare → componente/utilizări → siguranță/îngrijire → completare set → recenzii.')
p('Microinteracțiunile explică adăugarea în coș, schimbarea variantei și erorile; se respectă preferința de mișcare redusă. Bara inferioară de acțiuni nu acoperă conținutul sau tastatura. Galeria are gesturi și controale accesibile. PWA și notificările sunt extensii cu acord explicit, fără cache pentru coș, plăți sau date personale.')

page('7 Sistem de design și producție de conținut')
p('Figma definește componentele și tokenurile; Style Dictionary exportă valorile aprobate; Storybook documentează implementarea React, stările și accesibilitatea. Catalogul estimat conține 60–80 componente și variante utile. Recepția cere acoperirea componentelor folosite în cele 24 de tipuri, nu atingerea artificială a unui număr.')
table(['Livrabil','Volum și regulă de acceptare'],[
('Sistem vizual','Tipografie, spațiere, culori, contrast, focus, iconografie, formulare, grile și stări; zero divergențe majore între Figma și Storybook.'),
('Media pentru produse prioritare','300 produse cu galerie validată; minimum 3 imagini utile/produs din surse existente sau producție nouă. Bugetul presupune reutilizare, nu 900 fotografii noi.'),
('Conținut vizual nou','30 clipuri scurte, 12 scene cumpărabile și pilot de 10 modele 3D corecte la scară. Extindere după validarea costului și efectului.'),
('Blocuri pentru marketing','Minimum 12 blocuri reutilizabile: hero, categorii, grilă, culori, serie, scenă, video, ghid, UGC, beneficii, ofertă, Pro; preview și programare.'),
('Traducere completă','RO, EN, DE, HU, BG, EL; toate înregistrările intră în flux. Revizie umană pentru 300 prioritare și toate textele legale/critice; restul trec verificări și eșantionare.'),
('Voce și UGC','Ghid de redactare, drepturi pentru foto/video, moderare, trasabilitatea consimțământului și interdicția recenziilor fabricate.')],[4.2,13.3])
p('Scenele compuse și randările sunt permise dacă produsul, culoarea, decorul și proporțiile rămân fidele. Imaginile de inspirație sunt marcate când reprezintă o simulare relevantă pentru decizia clientului. Declarații precum „rezistă la spălare” cer dovezi. Video pornește la cerere, cu poster, subtitrări și alternative text; nu blochează viteza paginii.')
h('Exemple de ton propuse pentru revizie lingvistică')
table(['Limbă','Microtext de orientare'],[('RO','Alege piesele potrivite pentru masa ta.'),('EN','Choose the pieces that suit your table.'),('DE','Wähle die passenden Stücke für deinen Tisch.'),('HU','Válaszd ki az asztalodhoz illő darabokat.'),('BG','Избери подходящите съдове за твоята маса.'),('EL','Διάλεξε τα κομμάτια που ταιριάζουν στο τραπέζι σου.')],[2,15.5])
p('Nu se publică traduceri cu erori de cantitate, material, siguranță sau preț, indiferent de scor. Costul pentru întregul flux de catalog și cele șase limbi este inclus în scenariul recomandat, în limitele de volum din capitolul 17.')

page('8 Funcții comerciale care diferențiază CESIRO')
h('Masa completă și completarea unei serii')
p('Clientul alege 2/4/6/8 persoane, buget și stil, apoi modifică piesele într-o compoziție vizuală React. Fiecare poziție are rol, SKU și cantitate; totalul este calculat de backend. Seturile comerciale rămân distincte de pachetele configurate. „Ce ai deja?” scade piesele selectate și oferă completări din aceeași serie; alternativele asemănătoare sunt numite explicit alternative.')
p('Valul 1 livrează recomandări prin reguli și scene 2D; valul 3 adaugă configuratorul și recomandări bazate pe coșuri agregate. Țintă de acceptare: 20 serii verificate, 12 scene, 100% calcule corecte de cantitate/preț, zero componente indisponibile confirmate tacit. 10 scenarii cu bugete diferite sunt evaluate de merchandising.')
h('Asistent de cumpărare și căutare vizuală')
p('Asistentul răspunde la cereri precum „6 invitați, masă rustică, 400 lei” din catalog și politici aprobate. Afișează că este AI, citează produsele, verifică disponibilitatea și cere acțiunea explicită a clientului pentru adăugare în coș. Nu finalizează plăți și nu anulează comenzi. Vocea este opțională; utilizatorul vede transcrierea înainte de trimitere.')
table(['Funcție','Probă de acceptare la valul 3'],[
('Asistent contextual','200 cereri etalon, dintre care 40 adversariale; ≥90% răspunsuri utile și corecte evaluate uman; 0 acțiuni neautorizate; 100% prețuri/stocuri luate din API.'),
('Căutare după fotografie','100 imagini de test cu exemplare existente și 50 fără corespondent; Recall@5 ≥85% pe subsetul existent, identificări exacte false ≤2% pe setul evaluat.'),
('Căutare semantică','60 interogări/limbă; nDCG@10 ≥0,80 după judecată editorială; SKU exact pe prima poziție în 100% cazuri eligibile.'),
('Siguranță și continuitate','Fotografii cu EXIF eliminat, dimensiuni limitate, ștergere implicită după maximum 24 h; blocarea injecțiilor de instrucțiuni; căutare text și suport uman ca alternativă.')],[4.2,13.3])
p('Timpul AI se măsoară separat: primul răspuns p95 ≤4 s, propunerea completă p95 ≤10 s în sarcina agreată. Eșecul modelului nu blochează coșul. Relațiile serie–culoare–stil–piesă formează inițial un graf logic în PostgreSQL; o bază de graf separată necesită o nevoie demonstrată.')

page('8 Funcții vizuale și cadouri personalizate')
h('Vizualizare pe masă și în cameră')
p('Pilotul WebAR folosește 10 modele GLB/USDZ verificate dimensional. Configuratorul 2D funcționează pe toate dispozitivele suportate; 3D/AR se încarcă la cerere, cu fallback imagine. Testele pe iOS și Android verifică dimensiunea, poziționarea, memoria și potrivirea cu SKU-ul. O cameră sau un model incompatibil nu blochează cumpărarea. Efectul comercial se măsoară înainte de extinderea la toate formele.')
h('Personalizare și producție')
p('Pilotul cu 10 produse oferă text, monogramă, dată și logo în zone aprobate de fabrică. Pentru fiecare opțiune se definesc fonturi, limită de caractere, culori, rezoluție, cost, cantitate minimă și termen. Clientul aprobă previzualizarea; backendul păstrează versiunea și generează fișa de producție. Logo-ul încărcat este verificat pentru format, malware și drepturi declarate.')
p('Fluxul: opțiuni → previzualizare → calcul și termen → confirmare client → comandă plătită → verificare operator → fișă producție → control calitate → expediere. Un fișier aprobat nu se regenerează cu alt text după plată. 20 comenzi simulate trebuie să reconcilieze opțiunea, prețul, fișierul și termenul; capacitatea reală și regulile de retur se aprobă înainte de vânzare.')
h('Liste de nuntă și eveniment')
p('Clientul poate crea o listă privată sau partajabilă, cu data evenimentului și cantități dorite. Adresa destinatarului rămâne ascunsă invitaților. Rezervarea unei piese are expirare; două cumpărări simultane nu depășesc cantitatea disponibilă. Modificările, expedierea și retururile actualizează evidența prin operațiuni autorizate.')
p('Contribuțiile de grup sunt un pilot condiționat de PSP și validarea juridică a modului de colectare, rambursare și expirare. Versiunea de bază permite cumpărarea de produse întregi pentru listă. Livrarea la o dată aleasă se promite numai pentru produse și rute cu capacitate confirmată; altfel se afișează interval estimat.')
h('Precomenzi pe loturi')
p('Modulul folosește loturi de producție confirmate: disponibil promis = capacitate alocată − rezervări − tampon. Data, avansul, plata diferenței și efectul întârzierii sunt explicite. Lansarea pilotului cere 3 loturi validate de fabrică, reconciliere fără supravânzare și procedură de informare a clientului. Dacă sursa de producție nu este disponibilă, se oferă notificare de revenire în stoc, nu o dată inventată.')

page('8 Retenție și zona Pro')
h('Club CESIRO și comunicări')
p('Programul de bază acordă puncte pentru comenzi eligibile, cu niveluri, expirare și cost financiar plafonat. Registrul de puncte este idempotent; retururile aprobate uman ajustează punctele. Bonusurile nu condiționează o recenzie pozitivă. Clientul poate salva decorul preferat și poate primi, cu acordul necesar, notificări despre piese noi și revenire în stoc.')
table(['Automatizare','Declanșare și control'],[
('Coș abandonat','Mesaj la 2 h și, opțional, la 24 h; oprire la cumpărare, dezabonare sau indisponibilitate; bază legală și preferințe verificate.'),
('După livrare','La 7 zile: îngrijire, recenzie și solicitare UGC; informările de serviciu sunt separate de promovare.'),
('Reaprovizionare Pro','Interval derivat din consum sau ales de client; propunere editabilă, fără comandă automată implicită.'),
('Aniversare și decor','Campanii pe preferințe explicite; limită comună de frecvență, maximum 2 mesaje promoționale/săptămână ca regulă inițială.'),
('Canale și afiliere','E-mail prioritar; SMS/WhatsApp numai cu consimțământ și furnizor activ. Atribuire și plăți de afiliere din comenzi validate, cu control de fraudă.')],[4.2,13.3])
p('Mystery Box primește descriere clară a conținutului posibil, valorii și condițiilor. Dezvăluirea animată este opțională și accesibilă. Abonamentul lunar intră în extensia ambițioasă numai după verificarea marjei, cererii, plăților recurente și a unei anulări ușoare realizate de client sau operator uman; nu se introduce un mecanism de noroc cu premii sau raritate fictivă.')
h('Portal Pro minimal în scenariul recomandat')
p('Cont de firmă verificat, preț pe client și praguri de cantitate, cerere de ofertă, încărcare listă SKU/cantitate, comandă repetată și cerere de mostre. Logo-ul pentru corporate folosește același flux de personalizare. Prețurile negociate nu apar în cache public, feeduri sau alte conturi. Creditul comercial automat și finanțarea proprie nu fac parte din pilot.')
p('Recepție Pro: 10 scenarii cu roluri și clienți diferiți, import de 100 poziții cu erori explicate, zero scurgeri de preț contractual. O ofertă tipică de 20 poziții trebuie pregătită în maximum 10 minute din catalog validat. Serviciile de mostre au cost, transport și termen explicite.')

page('9 Arhitectura propusă și decizia de reutilizare')
p('Arhitectura de bază păstrează EVA Storefront drept autoritate pentru produse, prețuri, stocuri, clienți și comenzi. Noul storefront este JavaScript cu React și Next.js; TypeScript este recomandat ca verificare statică, compilată în JavaScript, fără schimbarea tehnologiei cerute. Backendul comercial rămâne Python Flask. Adminul React/Vite existent se extinde. [I2, I3, T1]')
table(['Strat','Decizie','Responsabilitate'],[
('Interfață publică','Next.js App Router și React','Randare, navigare, compoziție, accesibilitate; fără calcule comerciale autoritative în browser.'),
('API comercial','Flask, SQLAlchemy, Alembic, PostgreSQL','Contracte versionate, reguli, autorizare, tranzacții și integrări existente.'),
('Căutare','Meilisearch candidat principal; pgvector pentru similitudine','Index derivat, fațete, diacritice și sinonime; alegere finală prin PoC, PostgreSQL rămâne sursa.'),
('Procesare','Coadă de joburi și worker Python; reutilizare înainte de alegerea Redis/Celery','Traduceri, indexare, exporturi, media; retry, idempotentă și coadă pentru erori persistente.'),
('Livrare și monitorizare','CDN/WAF, Sentry și OpenTelemetry, GrowthBook','Cache sigur, protecție, trasare fără date personale, activări graduale și experimente.'),
('AI și fișiere','Serviciu local validat sau alternativă contractuală; stocare cu acces controlat','Embeddings, inferență și media; limite de cost, audit și retenție.')],[3.4,6.5,7.6])
p('Next.js poate necesita un runtime Node pentru randare; acesta nu devine un al doilea backend comercial. Nu introducem Django, Saleor sau Medusa pentru simpla schimbare a temei. Medusa ar schimba și cerința de backend Python. Saleor rămâne alternativă numai dacă analiza de diferență demonstrează blocaje structurale și un cost total mai bun. Nici 5.000, nici 30.000 de produse nu dovedesc singure o limită de performanță PostgreSQL.')
h('Decizii care se închid în săptămâna 2')
p('ADR01 documentează reutilizarea, contractele și diferența față de codul instalat. ADR02 compară motorul de căutare pe aceleași interogări, limbile reale, relevanță, p95, cost și mentenanță. ADR03 fixează cacheul, invalidarea, sesiunile și infrastructura. PGX/Qwen, Cloudflare și PSP sunt candidați, nu servicii declarate active fără probă. FastAPI rămâne o opțiune ulterioară justificată de măsurători.')

page('10 Frontend și contractul de randare')
table(['Pagină','Randare și cache','Actualizare și siguranță'],[
('Homepage și Jurnal','Conținut prerandat/cache la CDN; module dinamice distincte.','Invalidare la publicare; cache segmentat pe tenant, limbă și piață.'),
('Produs, categorie, serie','HTML indexabil, cache cu revalidare la eveniment; țintă de propagare ≤60 s.','Disponibilitatea afișată are dată; prețul/stocul se reverifică autoritativ la coș și comandă.'),
('Căutare și configurator','Rezultate dinamice și stare în URL; încărcare progresivă.','Index actualizat p95 ≤60 s; indisponibilitatea indexului are fallback text.'),
('Coș, checkout, cont, Pro','Dinamic; Cache-Control private/no-store.','Izolare de sesiune și tenant; fără prefetch al operațiunilor cu efect comercial.'),
('Recomandări și AI','Încărcare separată prin Suspense sau cerere dedicată.','Timeout și fallback; niciun blocaj al conținutului principal.')],[4,6.4,7.1])
p('Invalidarea de cache este semnată, urmărită și reconciliată între instanțe. Înainte de plată, backendul întoarce o ofertă cu versiune și expirare; modificarea totalului este prezentată clientului. Cacheul vechi nu poate autoriza un preț sau o cantitate. Regulile exacte de randare se fixează pentru versiunea Next.js aleasă în ADR03. [T1]')
h('Biblioteci și compatibilitate')
p('Bază propusă: Radix pentru primitive accesibile, Tailwind pentru stiluri, TanStack Query pentru stare server unde este necesară, React Hook Form și Zod pentru formulare. Validarea critică se repetă în Python. Componentele și tokenurile adminului se reutilizează numai unde nu leagă interfața publică de permisiuni administrative.')
p('Suport: ultimele două versiuni stabile de Chrome, Edge, Firefox, Safari și Samsung Internet, plus iOS și Android reprezentative. View Transitions și Speculation Rules sunt îmbunătățiri progresive, cu fallback și respectarea economisirii datelor. Prefetch numai pentru pagini publice sigure, fără rezervări, plăți, logout sau date personale.')
h('Verificare frontend')
p('Playwright verifică șase trasee: căutare–produs–coș; categorie–filtru–variantă; serie–completare; cadou–personalizare; checkout vizitator; Pro–ofertă. Se adaugă regresie vizuală, Lighthouse CI și testare manuală cu tastatură/cititor de ecran. Stările nefericite sunt obligatorii: timeout, preț schimbat, stoc epuizat, traducere lipsă și plată în așteptare.')

page('11 Analiza diferențelor față de EVA')
p('„Observat” în tabel înseamnă existență în fișierele locale citite, nu test în producție. Analiza statică se completează cu demonstrație de către echipa platformei în etapa D01. Nu se creează automat entități duplicate pentru funcții existente.')
table(['Modul observat sau cerut','Tratament','Dovada și extinderea necesară'],[
('Catalog, categorii, media, traduceri','Reutilizare și extindere','Resources products/categories/media/translations; atribute pe familii, scor și aprobare.'),
('Prețuri și promoții','Reutilizare cu verificare','price_reference.py și promotions.py; verificarea istoricului efectiv. Fallbackul la preț de catalog când istoricul lipsește nu este dovadă legală a prețului anterior.'),
('Comenzi, plăți, depozit','Reutilizare cu contracte','orders, warehouse, payments/stripe_gateway.py; idempotentă, rezervări și reconciliere între canale.'),
('Conectoare, lockere, SEO, feeduri','Reutilizare condiționată de test','Directoare marketplace/curier și feeds.py, seo_engine.py; capabilități, contracte și drepturi efective de verificat.'),
('Asistent admin','Extindere controlată','ai_assistant/guard.py și history.py există; generatorul de drafturi respectă restricțiile, jurnalul și aprobarea umană.'),
('EVA documente','Nu echivalează cu e-Factura','Modulul inspectat descrie importul documentelor de curier din EVA. Conectorul fiscal SPV trebuie identificat sau proiectat separat.'),
('Serie, scene, relații și embedding','Extindere sau nou după mapare','Chei spre produsul canonic; versiune model, sursă și data recalculării; fără copie concurentă a catalogului.'),
('Personalizare, liste, fidelitate, loturi','Nou sau extindere după inventar','PersonalizationConfig/Job, GiftRegistry/Item, LoyaltyLedger, ProductionLot/Allocation; nume conceptuale, nu schemă deja instalată.')],[4.1,4,9.4])
h('Contractul API')
p('Se livrează OpenAPI pentru catalog/căutare, preț și disponibilitate, coș, checkout, plăți, personalizare, liste și Pro. Contractul definește paginare, erori stabile, monedă, sume exacte, unități, versiuni și idempotency key. Validarea, autorizarea și izolarea pe tenant sunt obligatorii pe server; limitele de rată sunt configurabile.')
p('Migrațiile Alembic urmează extindere → populare → comutare → retragere ulterioară. Evenimentele de catalog/comandă se publică prin outbox tranzacțional sau mecanism echivalent demonstrat; consumatorii sunt idempotenți. Adminul primește cozi de calitate, preview colecții, aprobare AI, personalizare, liste și indicatori, integrate în navigarea existentă.')

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
p('Backendul păstrează separat starea comenzii, a plății, a livrării și a documentului fiscal. Se definesc stările de plată inițiată, în așteptare, autorizată, confirmată, eșuată și rambursată, cu tranziții permise și jurnal. Nu se consideră plătită o comandă doar din revenirea browserului de la PSP. [L5]')
p('Regulile locale din REGULI.md sunt constrângeri de proiect: AI nu anulează comenzi și nu execută retururi/rambursări, nici în teste. Testele automate folosesc simulări izolate, fără scrieri spre sisteme reale. Validarea fluxurilor sensibile revine unui operator uman. Scrierile spre marketplace-uri cer autorizarea expresă a proprietarului; automatizarea AWB respectă politica pe canal. [I5]')

page('13 Performanță accesibilitate și securitate')
table(['Domeniu','Criteriu de acceptare','Metodă'],[
('Experiență reală','LCP ≤2,5 s, INP ≤200 ms, CLS ≤0,1 la percentila 75, separat mobil/desktop.','RUM pe 28 zile; înainte de trafic suficient, teste de laborator și monitorizare după pilot. [T2]'),
('API și căutare','API citire p95 ≤300 ms; căutare text p95 ≤500 ms; erori tehnice <0,5%.','Măsurate fără rețeaua utilizatorului; warm/cold și dependențe raportate separat.'),
('Încărcare','Catalog curent ×6 limbi și creștere 2×; cereri/s și comenzi/min la 10× vârful observat.','Rampă, vârf 15 min, anduranță 2 h; profil tranzacțional real. Fără baseline se testează profil convenit, nu o capacitate pretinsă.'),
('Accesibilitate','WCAG 2.2 AA drept condiție contractuală; zero defecte A/AA deschise în fluxurile livrate.','Automat + audit manual tastatură, zoom 200–400%, NVDA/VoiceOver, contrast și documente. [T3, L4]'),
('Securitate','Zero vulnerabilități critice/înalte exploatabile; izolare tenant și client.','Test autorizare, CSRF/XSS, rate limit, upload, sesiune, jurnal și scanare dependențe.'),
('Operare','Disponibilitate țintă 99,9% lunar; RPO ≤15 min, RTO ≤60 min.','Backup și restaurare demonstrată, runbook și două persoane instruite; dependențe PSP raportate separat.')],[3.4,7.3,6.8])
p('WAF și protecția anti-boți limitează încercările automate, card testing și abuzul formularelor. Turnstile este candidat, cu alternativă accesibilă și evaluarea confidențialității; nu promitem absența oricărei verificări. Coada virtuală se activează doar dacă testul de sarcină arată necesitatea.')
p('Autentificarea poate folosi passkeys și link magic cu expirare, token unic și protecție la enumerare; social login este opțional. Comanda nu creează automat un cont activ fără informarea și alegerea clientului. Datele de card nu sunt stocate de CESIRO. Prețurile Pro, sesiunile și datele personale nu intră în cache comun sau în telemetrie.')
p('Se livrează informații publice despre accesibilitatea serviciului și un canal de sesizare. Legea 232/2022 include comerțul electronic de la 28 iunie 2025 și excepții, inclusiv pentru anumite microîntreprinderi; aplicabilitatea se verifică pentru entitatea vânzătoare. WCAG 2.2 AA este standardul ales al proiectului, fără a-l confunda automat cu textul integral al obligației legale. [L4]')

page('13 Conformitate și protecția datelor')
table(['Cerință','Aplicare în proiect','Probă și responsabil'],[
('GPSR','Oferta online afișează identificarea produsului, producătorul și contactele, operatorul UE unde este cazul, avertismentele relevante; conform art. 19 și domeniului aplicabil.','Fișă pe familie și piață; verificare 100% a câmpurilor obligatorii pentru lotul publicat; juridic + date. [L1]'),
('Contact alimentar','Reg. 1935/2004 și normele specifice ceramicii; documentație și trasabilitate, declarație de conformitate când este cerută.','Documente reale asociate produselor/loturilor; nicio confirmare generată de AI; calitate fabrică. [L2]'),
('Reduceri de preț','Istoric al prețului efectiv și preț anterior potrivit regulii de 30 zile, cu tratamentul excepțiilor aplicabile.','Teste pe promoții succesive, produs nou, istoric incomplet și monedă; juridic + comercial. [L3]'),
('GDPR și cookie','Minimizare, scop, retenție, contracte cu furnizorii, drepturi și consimțământ acolo unde este cerut.','CMP cu retragere simplă; fără marketing înainte de acord în fluxurile care îl cer; DPO/juridic. [L8]'),
('AI și transparență','Informare că asistentul este AI, gestionarea conținutului sintetic și a obligațiilor aplicabile rolului CESIRO.','Etichete și jurnal; revizuire art. 50 și a normelor în vigoare înainte de activare; juridic. [L6]'),
('e-Factura și consumator','Transmiterea facturilor emise când este obligatorie; retur, garanții, reclamații, personalizare și precomenzi explicate înainte de plată.','Validare contabilă/fiscală, flux de erori și dovada transmiterii; termene parametrizate. [L5]'),
('Pașaport de produs','Fișă voluntară de proveniență, materiale, îngrijire și dovezi; compatibilă cu evoluția cadrului DPP.','Fără afirmația că DPP este deja obligatoriu pentru toate produsele ceramice; verificare acte delegate. [L7]')],[3.3,8.1,6.1],small=9.8)
p('Consent Mode v2 și taggingul server-side transmit și respectă opțiunile utilizatorului; nu înlocuiesc consimțământul sau conformitatea GDPR. Mod implicit conservator: tagurile neesențiale nu pornesc înainte de acord. Replay de sesiune este dezactivat inițial; orice activare cere mascarea integrală a câmpurilor și o evaluare separată. [T4]')
p('Entitatea contractuală trebuie confirmată: auditul Gemini numește CESIRO S.A., iar informațiile comerciale publice trebuie reconciliate cu operatorul efectiv al magazinului. Același registru stabilește vânzătorul, producătorul, operatorul de date și emitentul facturii; aceste roluri nu se presupun identice.')

page('14 SEO localizare și conținut cumpărabil')
p('RO, EN, DE, HU, BG și EL sunt tratate ca șase versiuni editoriale. Piața și țara de livrare determină prețul, taxele și oferta: RON pentru RO, HUF pentru HU, EUR pentru DE/EL/BG; EN urmează țara selectată. Nu se deduce țara numai din limbă sau IP. Bulgaria a adoptat euro la 1 ianuarie 2026; istoricul BGN se păstrează ca istoric, fără a deveni moneda checkoutului nou. [L9]')
h('Continuitate și indexare')
p('Inventar pentru 100% din URL-urile cunoscute, cu destinație și motiv. URL-urile stabile se păstrează când este posibil; schimbările folosesc redirect 301 direct și relevant, fără lanțuri sau redirecționări în masă la homepage. Canonical, hreflang reciproc, x-default unde este potrivit și sitemapuri separate pe limbă/tip se validează automat. Arhivele fără echivalent au tratament 404/410 justificat; lipsa temporară de stoc nu șterge pagina.')
p('Numai combinațiile de filtre aprobate editorial sunt indexabile. Checkoutul, conturile, listele private și rezultatele cu parametri infiniți nu devin pagini SEO. Migrarea graduală servește aceeași experiență utilizatorilor și roboților din aceeași cohortă; nu folosește cloaking. Monitorizare zilnică a paginilor prioritare, erorilor și indexării în primele 30 zile.')
h('Conținut și descoperire prin AI')
p('Jurnal CESIRO: 30 ghiduri până la finalul valului 4, dintre care 10 la primul val: alegerea setului, numărul de piese, întreținerea glazurii, completarea seriei, cadouri și mese sezoniere. Fiecare are autor/responsabil, data reviziei, răspunsuri utile și produse eligibile. Video scurt cumpărabil, subtitrat, completează ghidurile; nu substituie textul indexabil.')
p('JSON-LD Product/Offer, disponibilitate, livrare și politici de retur reflectă exact pagina și piața; recenziile se includ numai dacă sunt reale și eligibile. FAQ este util cititorului; nu promitem rich results pentru magazine. Google precizează că funcțiile sale AI nu cer optimizări speciale suplimentare. llms.txt poate fi un experiment documentar, fără garanție de indexare, citare sau recomandare. [T5]')
h('Feeduri și canale')
p('Google Merchant și Meta primesc ID-uri stabile, GTIN unde există legitim, preț, stoc, imagini, țară, limbă, transport și retur din aceeași sursă. TikTok și afilierea se activează pentru piețe și conturi eligibile; nu presupunem disponibilitatea TikTok Shop în toate cele șase piețe. Erorile, respingerile și diferențele de preț se monitorizează; țintă ≥98% articole eligibile acceptate în feed, fără a promite aprobarea externă.')

page('15 Măsurare și experimente')
p('GA4 cu CMP și tagging server-side este configurația propusă pentru marketing; datele operaționale și cohortele vin din rapoarte agregate ale backendului. PostHog intern este alternativă pentru analiză de produs, evaluată după cost și confidențialitate; nu se instalează două sisteme suprapuse fără nevoie. GrowthBook gestionează expunerea și experimentele.')
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

page('16 Activități calendar și lansări graduale')
table(['Etapă','Activități și livrabile','Condiție de trecere'],[
('A0 și A1\nSăpt 1–2','PO nominalizat, D01 catalog curent, D02 baseline, 8–10 interviuri, analiză a până la 500 recenzii/tichete disponibile, ADR01–03; PoC căutare vizuală și AI pe date izolate.','Responsabili și surse confirmate; buget/volum fixate; PoC evaluat pe etalon, fără scrieri în producție.'),
('Val 1\nSăpt 1–6','Concepte și sistem vizual; homepage, listare, produs, căutare, 12 familii de colecții, reguli de recomandare, 300 produse prioritare și 10 ghiduri.','D03 design și R01 date, SEO și teste critice trecute; trafic pilot 5% → 20%.'),
('Val 2\nSăpt 7–10','Coș și checkout, wallet eligibil, livrare/lockere, reconciliere stoc și facturare, CMP, evenimente și automatizări de bază.','Contracte și integrare fiscală verificate; zero defecte comerciale critice; pilot controlat.'),
('Val 3\nSăpt 11–14','Asistent, căutare vizuală/semantică, masă completă, serie, pilot AR, Pro minimal, UGC și 20 ghiduri cumulat.','Praguri AI și relevanță îndeplinite; fallback funcțional; validare Pro și media.'),
('Val 4\nSăpt 15–18','Personalizare pilot, liste de eveniment de bază, Club, card cadou, restul catalogului eligibil și 30 ghiduri; pilot precomenzi dacă fabrica este pregătită.','Producție, financiar și juridic validează serviciile; catalogul restant are destinație și plan.'),
('A5\nDupă valuri','90 zile monitorizare și experimente, corecții, raport comercial și predare operare.','Raport cu baseline, segmente, efecte, limite statistice și acțiuni.')],[2.7,9.1,5.7],small=9.8)
p('Designul și contractele API încep în săptămâna 1, dezvoltarea reutilizabilă în săptămâna 2. Sprinturi de două săptămâni, demo și decizie PO în trei zile lucrătoare. „P1” din audit înseamnă cerință obligatoriu tratată în proiect; nu impune activarea tuturor funcțiilor în primul val.')
p('Traficul crește 5% → 20% → 50% → 100%, minimum 48 h de monitorizare la fiecare treaptă și volum suficient. O eroare critică de total, plată, izolare sau stoc oprește imediat extinderea. Prag statistic comercial: limita inferioară a intervalului de încredere pentru variația conversiei trebuie să depășească −5% relativ; fără putere suficientă, PO decide doar o extindere limitată, explicită, pe baza riscului tehnic.')
p('Piața pilot se alege după volum, suport, traduceri și contracte. BG/HU sunt opțiuni, nu o condiție automată; o cohortă mică în RO poate produce dovezi mai relevante. Comutarea înapoi la interfața veche trebuie demonstrată în ≤15 minute, păstrând comenzile și schema compatibilă.')

page('17 Resurse buget și limite de estimare')
p('Estimările sunt de planificare, fără TVA și fără ofertă comercială. Tariful mediu presupus este 400–550 EUR/zi-persoană, 8 ore/zi. Ținta de 160–220 zile sugerată în audit este folosită ca interval de bază, nu ca economie demonstrată. Reestimarea se închide după analiza diferențelor și măsurarea calității catalogului.')
table(['Scenariu','Efort și cost de lucru','Costuri suplimentare și total'],[
('Minim\nValurile 1–2','120–150 zile × 400–550 EUR = 48.000–82.500 EUR.','Media/lingvistic 4.000–7.000; infrastructură/licențe 6 luni 2.000–4.000; rezervă 15%. TOTAL 62.100–107.525 EUR.'),
('Recomandat\nValurile 1–4','190–220 zile × 400–550 EUR = 76.000–121.000 EUR.','Media/lingvistic 10.000–18.000; infrastructură/licențe 6 luni 3.000–6.000; rezervă 15%. TOTAL 102.350–166.750 EUR.'),
('Ambițios\nExtinderi după pilot','260–320 zile × 400–550 EUR = 104.000–176.000 EUR.','Media/lingvistic 20.000–35.000; infrastructură/licențe 6 luni 5.000–10.000; rezervă 20%. TOTAL 154.800–265.200 EUR.')],[3.2,6.1,8.2])
p('Total = (efort × tarif + producție externă de conținut + infrastructură/licențe) × (1 + rezervă). Scenariul minim are domeniu redus și nu echivalează cu îndeplinirea integrală a reviziei. Costurile în lei se calculează la cursul contractual; nu folosim un curs inventat.')
h('Distribuția scenariului recomandat')
table(['Rol și activitate','Zile','Rol și activitate','Zile'],[
('Produs și cercetare','18–20','UX și sistem vizual','24–28'),('Frontend React','38–44','Backend și integrări','32–36'),('Date și localizare','24–28','AI și căutare','18–22'),('QA accesibilitate securitate','22–24','DevOps și lansări','8–10'),('CRM și măsurare','6–8','Total','190–220')],[6.2,2.1,6.9,2.3])
p('Minimum 25% din efortul recomandat, adică 48–55 zile deja incluse în rolurile de mai sus, se alocă funcțiilor diferențiatoare: AI, configurare, personalizare, liste și retenție. Echipa medie de livrare este aproximativ 2,1–2,5 echivalenți normă întreagă pe 90 zile lucrătoare, cu specialiști part-time și vârfuri planificate. PO CESIRO are disponibilitate separată de minimum două zile/săptămână.')
p('Bugetul presupune până la 6.000 înregistrări canonice în flux și șase limbi, fără 36.000 produse distincte. Include ingestie/normalizare pentru toate, editare prioritară 300 și verificări pe restul; nu include rescriere umană integrală a fiecărui text. Lipsurile legale se rezolvă prin documente reale de la deținători, iar produsele fără ele rămân neeligibile.')

page('17 Guvernanță dependențe și riscuri')
table(['Responsabil','Răspundere și decizie'],[
('Sponsor CESIRO','Buget, portofoliu, entitate vânzătoare și promisiuni comerciale.'),
('Product Owner CESIRO','Priorități și acceptare; persoana se nominalizează în A0, cu înlocuitor și termen de decizie.'),
('Lider tehnic și DevOps','ADR, reutilizare, integrări, securitate, restaurare și lansare; minimum două persoane cu acces și instruire.'),
('Responsabil date și merchandising','Inventar, ABC, scor, serii și eligibilitate; aprobă ieșirea loturilor din remediere.'),
('UX content și CRM','Cercetare, media, traduceri, accesibilitate UX, comunicări și experimente.'),
('Fabrică logistică financiar juridic','Producție personalizată, capacitate loturi, spargeri, facturare și conformitate; drept de oprire pe domeniul propriu.')],[5,12.5])
table(['Risc','Măsură și prag','Responsabil'],[
('Cod diferit de producție','Demonstrație a versiunii instalate și contracte API înainte de estimarea fixă.','Lider tehnic'),
('Date slabe sau acte lipsă','Loturi, scor și condiții obligatorii; zero publicări comerciale neeligibile.','Date + juridic'),
('Dependență de o persoană','Documentație, pairing și exercițiu de restaurare condus de a doua persoană.','DevOps'),
('AI greșit sau costisitor','Etalon, plafon lunar, oprire automată la epuizare și fallback; măsurare cost/cerere.','AI + PO'),
('Stoc și plăți divergente','Reconciliere, outbox/idempotentă, tampon și alarme; intervenție umană pentru excepții.','Backend + logistică'),
('Canibalizare marketplace','Marjă și cotă directă pe canal; servicii exclusive măsurabile, fără război automat de preț.','Comercial'),
('Capacitate fabrică sau personalizare','Pilot de 10 produse, fișă aprobată, cantitate și termen confirmate; flag dezactivat până la validare.','Fabrică'),
('Legal sau piață nepregătită','Matrice pe țară și familie; revalidare înainte de val, stop pentru domeniul afectat.','Juridic'),
('Conținut peste buget','Inventar media și rată de editare în A1; variația >10% din efort cere recalcul transparent.','PO + content')],[4.2,10.6,2.7],small=9.6)
p('Nu sunt incluse în costurile de mai sus: buget media plătită, comisioane PSP/marketplace, transport și spargeri, materiale și capacitate de fabricație, personal CESIRO sau achiziție hardware AI. Bugetul media/lingvistic extern nu dublează zilele de orchestrat/editat date; cele două categorii se reconciliază în deviz. Contribuțiile financiare de grup, abonamentul Mystery Box, creditul Pro și AR extins apar în scenariul ambițios, după pilot.')

page('18 Recepție și probe cerute')
table(['Cod','Livrabil și criteriu','Probă de închidere'],[
('R01','100% rânduri și câmpuri sursă contabilizate; praguri de calitate și condiții obligatorii îndeplinite pentru fiecare lot publicat.','D01 semnat, raport diferențe, scoruri și jurnal de aprobare.'),
('R02','24 tipuri, 72 ecrane de bază, stări, tokenuri și bibliotecă; SUS ≥80 în runda finală.','Fișiere editabile, prototip și raport cu sarcini, participanți și rezultate.'),
('R03','≥90% succes pe sarcini critice; mediană până la primul add-to-cart ≤60 s; checkout nou ≤90 s și wallet ≤30 s.','2×8 participanți; timpi măsurați cu datele pregătite, separat de așteptarea PSP/SCA; erori și percentile raportate.'),
('R04','Zero defecte critice deschise în totaluri, stoc, plăți, tenant și facturare.','Teste de contract, integrare izolată și demonstrații umane autorizate; fără anulări automate de AI.'),
('R05','Pragurile din capitolul 8, 20 serii, 12 scene, 10 produse personalizabile și 10 modele AR pilot.','Etaloane, rapoarte de relevanță, fișe de producție și fallbackuri demonstrate.'),
('R06','Toate URL-urile inventariate au decizie; 0 erori critice pe URL-uri prioritare; 6 limbi cu conținut critic validat.','Crawl comparativ, mapare redirect, hreflang și teste monetare/țară.'),
('R07','Criteriile din capitolul 13, accesibilitate AA și lipsa vulnerabilităților critice/înalte.','Rapoarte laborator/RUM, încărcare, accesibilitate manuală și securitate.'),
('R08','Rollback ≤15 min; restaurare RPO/RTO; două persoane instruite și monitorizare.','Exercițiu documentat, runbook, alerte și responsabil de permanență.'),
('R09','Matrice legală pe entitate/piață/familie și aprobarea domeniilor aplicabile.','Politici, documente, CMP, dovada facturării și avize operaționale.'),
('R10','Dashboard și raport la 90 zile, cu baseline, guardrails, atribuiri și incertitudine.','D02, evenimente reconciliate, experimente și rezultate explicate.')],[1.4,8.1,8],small=9.8)
p('Setul critic include: ultima unitate simultană, webhook duplicat și reordonat, plată întârziată, preț schimbat, pierdere sesiune, cont Pro izolat, serie greșită, traducere numerică incorectă, fișier personalizare invalid și lipsa sursei AI. Pentru retur/rambursare și anulare, numai operatorul uman execută probele autorizate în mediul permis.')
p('Nicio acceptare nu este dedusă din simpla existență a unui fișier sau din trecerea testelor automate. Se livrează raportul, data, versiunea și responsabilul. Neconformitățile critice blochează funcția afectată; restul au termen și proprietar. Recepția poate fi parțială pe val, fără a declara întregul proiect finalizat.')

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
h('Cercetarea care închide ipotezele')
p('A1 include 8–10 interviuri: cumpărători recenți, persoane care au abandonat, clienți de cadouri și Pro. Se analizează până la 500 recenzii/tichete anonimizate; dacă există mai puține, se raportează totalul real. Se caută dovezi despre spargeri, completarea seriei, diferențe de culoare, ambalare și termen. Sondajul după comandă se activează numai în implementarea autorizată, cu regulile de confidențialitate.')
p('Raportul diferențiază ce au spus clienții de interpretarea echipei. Ponderea mobilului, conversia și rata de retur CESIRO se extrag din datele proprii; nu sunt înlocuite de medii de piață neverificate. Această revizie nu inventează interviuri, rezultate de sondaj sau benchmarkuri numerice de conversie.')
h('Domeniul acestei revizii')
p('Livrabilele sunt descrierea de proiect V2 și matricea de răspuns la audituri. Nu includ implementare, publicare, modificarea cesiro.com, a codului platformei sau a datelor operaționale. Funcțiile, testele și lansările descrise sunt activități viitoare ale proiectului. Originalul V1 și auditurile se păstrează.')

page('20 Surse interne și tehnice')
p('I1 — Audit.Claude.V1.0.docx: 92 observații și 87 propuneri numerotate; Audit.Gemini.v1.0.pdf: 3 pagini, recomandări fără coduri proprii. Identificatorii G01–G20 din matrice au fost adăugați pentru trasabilitate.')
p('I2 — U:/cesiro1-site/backend/requirements.txt și frontend/package.json: tehnologii declarate. I3 — backend/app/price_reference.py, ai_assistant/guard.py și history.py, api/admin/resources, integrations, payments, feeds.py și database/migrations: citire statică, fără execuție.')
p('I4 — U:/cesiro1-site/wc-product-export-16-9-2026-1789549595309.csv. SHA-256: '+stats['sha256']+'. Rezultatele agregate și selecția sunt păstrate în evidence-v2/catalog-summary.json. I5 — U:/cesiro1-site/REGULI.md: restricții operaționale citite și păstrate în proiect.')
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

page('20 Surse legale și repere comerciale')
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
save('Proiect_CESIRO_Design_React_Python_V2.docx')
print('Proiect V2 salvat')
