from pathlib import Path
from collections import Counter
import json, runpy
O=Path(__file__).parent
v=runpy.run_path(str(O/'build_v4.py'))
init,p,h,head,page,table,save=[v[k] for k in ['init','p','h','head','page','table','save']]
audit=json.loads((O/'evidence-v4/audit-claude-v3.json').read_text(encoding='utf-8'))
byid={a['id']:a for a in audit};groups=[]
def G(ids,topic,where,decision,proof,status='Specificat în V4'):
    groups.append(dict(ids=['A3-'+i for i in ids.split()],topic=topic,where=where,decision=decision,proof=proof,status=status))
G('O0.1','Direcția programului','§0; §22','Se păstrează experiența CESIRO și istoricul separat. Varianta C combină tema cu E0–E7 în același motor, fără sistem API paralel.','PO: domeniu explicit și limite; execuția rămâne viitoare.')
G('O0.2 P0.1','Cadou disponibil și personalizare','§0; §8.2; §11','Diferențiatorul este „Cadou gata de dăruit”: ambalaj și mesaj existente, maximum 300 caractere. E6 adaugă personalizarea pilot, distinct de prima lansare.','Platformă: gift.py și migrația 0079; fabrică: 10 proof-uri înainte de E6.','Fapt verificat și extensie planificată')
G('O1.1 P1.1','Calea actuală a sursei','§1; I2–I6','Referințele active sunt U:/cesiro.com. Vechea cale apare numai în explicația istorică. Existența/noile căi sunt observate la 21 octombrie 2026; data exactă a redenumirii nu este inventată.','Manifest de hashuri pentru 14 fișiere; D01 completează istoricul disponibil.','Fapt verificat cu limită')
G('O1.2 P1.2','Versiunea de cod','§1; §9.1; I6','Accesul GitHub a fost verificat din nou și a rămas 404 prin conexiunea disponibilă. Folderul local nu are .git. Hashurile identifică lectura locală, nu commitul instalat.','Responsabil platformă, S1–2: acces de citire, commit, digest și legătura cu tenantul înainte de ofertarea fermă.','Dependență deschisă identificată')
G('O2.1 P2.1','Calendar juridic actualizat','§2; §13.2; §20.3','Textele oficiale 2025/2439 și 2026/405 sunt citate direct. Calendarul viitor nu suspendă obligațiile actuale CLP, biocide și preț unitar.','Juridic, A0: registru pe familie/piață, articole aplicabile și revizie înainte de lansare.','Surse oficiale incluse')
G('O3.1 P3.1','Capacitate editorială','§3','Se păstrează pilotul cronometrat de 100 fișe, 60 fișe/zi ca ipoteză și pragul de replanificare sub 52. Cei doi editori nu sunt considerați automat traducători/fotografi.','Date + PO, S1–2: jurnal pilot, rată reală, plan de loturi și capacitate.')
G('O4.1 O4.2 P4.1 P4.2','Indicatori separați după livrare','§4; §15; R10','Tema are venit, conversie, AOV și checkout. E4/E5 au utilizare și efectul asistentului; E6 personalizare; E7 retenție. Ferestrele de 90 zile pornesc separat; D02 recalibrează ipotezele după trafic și funcții.','Financiar + analytics, S2: baseline și metodă; R10 nu confundă o țintă cu un rezultat garantat.')
G('O5.1 O5.2 P5.1','Filtre disponibile și E1','§5; §11; E1','Parametrii existenți sunt enumerați din cod. Serie/decor și persoane lipsesc și intră explicit în E1, 4–6 zile. Se validează 100 SKU-uri și 20 serii.','Platformă + fabrică: teste de contract compatibile și zero asocieri greșite publicate.','Fapt verificat și extensie planificată')
G('O6.1 P6.1','Inventarul celor 25 tipuri','§6–6.1; R02; R11','Tabel explicit: 21 tipuri în tema de bază, personalizare prin E6 și Club prin E7; listele de eveniment și cardul cadou rămân concepte ulterioare. Paginile Temă + E# nu sunt numărate dublu.','UX + tehnic: 75 ecrane și mapă tip–rută–limbă–test; manifestul nu declară conceptele funcționale.')
G('O7.1 P7.1','Arhiva media și devizul','§7; §17.2; I8','38.865 fișiere cu extensie de imagine inventariate, cu posibile duplicate. Reutilizarea, asocierea SKU și drepturile se verifică înainte de refotografiere. Devizul de 19.460–35.100 EUR este păstrat.','Editorial: registru media; ipoteza de 150 produse reutilizate se confirmă, nu se transformă în economie pretinsă.','Inventar verificat și activitate planificată')
G('O8.1.1 O8.1.2 P8.1.1 P8.1.2','E4 asistent și E5 căutare','§8.1; §11.1; §16–17; R12','Lipsa publică este explicită. E4 15–25 zile reutilizează clientul LLM sigur, fără ruta OWNER și unelte admin. E5 15–20 zile folosește pgvector în aceeași bază. Ambele au calendar, flag, PoC și plafon comun 600 EUR/lună.','AI + securitate: 300 cereri E4, 150 imagini și 360 interogări E5; praguri R12, zero divulgări/acțiuni interzise.','Extensii incluse în plan')
G('O8.2.1 P8.2.1','Personalizare și funcții ulterioare','§8.2; §17; §17.5','E6 are 20–30 zile și 10 produse pilot; E7 are 15–20 zile. Listele și loturile au ordine de mărime, prioritate ulterioară și condiții de pornire, fără a intra în varianta C.','Fabrică + PO: proof, capacitate și specificații; niciun serviciu absent nu este declarat deja existent.')
G('O8.2.2','Informare despre personalizare','§8.2; §12.1','Se păstrează bifa de informare separată, fără renunțare generală la drepturi. Un set standard configurat nu este automat exceptat; disputa poate fi înregistrată în E0.','Juridic: text, comandă mixtă și drepturi de neconformitate.','Cerință păstrată')
G('O8.3.1 P8.3.1','Reutilizarea CUI din grup','§8.3; §11.1; I9; E3','Logica anaf_lookup din acc-florin a fost identificată static. E3 o adaptează în Flask în 2–4 zile; nu copiază sesiuni/credite fiscale și nu construiește integrare e-Factura.','Platformă: 20 cazuri CUI, timeout și completare manuală; clientul confirmă datele.','Sursă identificată și extensie planificată')
G('O8.3.2 P8.3.2','Pro de bază și Club','§6.1; §8.3; E7','Pro include pagină, firme pe cont, cerere de ofertă și coș actual. Prețul contractual pe client este ulterior. Club devine funcțional prin registrul E7, nu printr-o pagină care pretinde solduri.','Comercial + financiar: reguli puncte, plafon și reconciliere; conturile reutilizează /api/account/companies.')
G('O8.4.1 P8.4.1','Acces fără cont','§8.4; §12.1; E2','E2, 3–5 zile, adaugă grant limitat la comandă/tenant. Numărul comenzii și ruta publică de status nu autorizează acces la factură sau adresă. E0 rămâne utilizabil independent de livrarea linkului.','Securitate: expirare, revocare, replay și enumerare; GET nu consumă tokenul; fără token în jurnale.')
G('O9.1 P9.1','Variante și calendar de teme','§9; §18.1','10 variante noi au parent=cesiro_atelier. theme_schedule păstrează modul manual/automat, fallback și calendarele pascale. marketplace_pro și variantele ei rămân disponibile.','UX + tehnic: manifest, tokenuri, limite de dată și regresie pe tema de rezervă.')
G('O9.2 P9.2','Randare Flask și React','§9–10; §14; §20.1','Referințele Next.js, revalidateTag și arhitectura frontend separată sunt eliminate. Flask/Jinja livrează HTML, React deține insule DOM și Vite produce asseturi statice.','Tehnic: fără runtime Node de storefront în producție și fără handleri dubli.','Documentație corectată')
G('O9.1.1 P9.1.1','Serverul local partajat','§9.1; ADR04','Maparea U: la serverul local, coexistența proiectelor și Compose cu tunnel sunt fapte verificate. Containerele active și HA nu sunt certificate. 99,9%/RPO 15/RTO 60 rămân ținte de probat; 99,5% cere decizie distinctă.','DevOps, S2: versiune instalată, sarcină, backup/restaurare și nivel contractual; costuri separate.','Fapt verificat și decizie operațională deschisă')
G('O9.2.1 P9.2.1','Validarea înainte de comandă','§10; §11; R04','/api/orders/validate există în cod și este inclus în regresie pentru preț schimbat și stoc zero. Comentariul fără efecte nu înlocuiește inspectarea lanțului înainte de test.','QA: mediu izolat, fără secrete și apeluri externe; fluxurile sensibile sunt probate de om.')
G('O10.1 P10.1','R11 recepția temei','§18.1','Se adaugă validator, localizare fără texte fixe, citire fără JavaScript, templates/shared neatins, comutare sub un minut, SEO, variante și bugete de performanță.','Tehnic + QA: rapoarte pe 21 tipuri ×6 limbi, apoi două tipuri E6/E7; două persoane pot opera revenirea.')
G('O11.1 P11.1','Capabilități din cod','§11–11.1','Fiecare funcție are stare: prezentă în cod, UI oprit implicit, lipsă identificată sau funcție nedemonstrată. D01 confirmă configurația și producția, fără a amâna estimarea funcțiilor clar absente.','Platformă: hashuri și citări de modul; probe runtime distincte.','Inventar static actualizat')
G('O12.1 P12.1','Plata găzduită Stripe','§12; §11','Payloadul sesiunii indică flux găzduit. Formularul local poate fi într-o pagină; nu se promite că plata rămâne acolo. Walleturile depind de contul și integrarea Stripe.','Responsabil PSP, D01: confirmă modul activ și eligibilitatea; schimbarea modului se cotează distinct.')
G('O12.1.1 O12.1.2 P12.1.1 P12.1.2','E0 remediere urgentă','§12.1; §16; R09; R12','E0, 6–10 zile în S1–3 pe tema actuală, înregistrează declarația fără cont, motiv ori fotografie și emite dovadă durabilă. Returul din cont se reface în condițiile aprobate. Nu se ascunde lipsa sub blocarea unui segment comercial.','Platformă + juridic + suport: 12 cazuri conduse de om; confirmare fără întârziere, fără pierdere la eroare e-mail.','Remediere planificată prioritar')
G('O13.1 P13.1','Autentificare existentă','§9; §13; E2','Passkeys și autentificare generală prin link nu sunt în domeniu. E2 este un grant limitat pentru o comandă, nu înlocuiește identitatea și sesiunea platformei.','Securitate: izolare și compatibilitate; nicio autentificare paralelă.','Cerință păstrată și delimitată')
G('O13.1.1 P13.1.1','R09 și retragerea','§13.1–13.2; R09','Matricea de conformitate este păstrată și R09 cere recepția E0 înaintea noii teme. Actuala operare și transpunerile naționale sunt analizate de juridic.','Juridic + financiar: dovadă E0 și condiții pe fiecare piață/familie; fără certificare din lectura de cod.')
G('O14.1 P14.1','SEO pe aceleași URL-uri','§14; R06','Crawl comparativ veche/nouă pe aceleași adrese; canonical, hreflang și conținut esențial păstrate. Redirecturile sunt rezervate schimbărilor justificate individual.','SEO: inventar URL, zero erori critice și monitorizare 30 zile.','Documentație simplificată')
G('O15.1 P15.1','Experimente cu putere suficientă','§15','Prioritate pentru 3–4 teste cu efect mare în șase luni: checkout, configurator, decor și E4 după activare. Se păstrează calculul dimensiunii eșantionului și raportarea incertitudinii.','Analytics: D02, MDE și trafic; rezultatul neconcludent nu este prezentat ca succes.')
G('O16.1 P16.1','Calendar comun cu două fluxuri','§16','Tema la S16; E0/E2 urgent S1–3, E1/E3 înaintea temei, E4/E5 apoi E6/E7 până la S24–26. Dependențele și ferestrele de 90 zile sunt separate.','PO: plan nominal și dependențe; ultimul raport comercial poate ajunge în jur de S39.')
G('O17.1 O17.2 P17.1 P17.2','Cost comparabil și timp intern','§17–17.3','Tema 160–200 și E0–E7 80–120 =240–320 zile. WBS pe roluri, două scenarii tarifare, rezervă 15%, AI și mentenanță extensii separate. Timp CESIRO 148–152 zile ×150 EUR ipotetic =22.200–22.800 EUR.','PO + financiar: aritmetică verificată; două oferte pe același domeniu. Infrastructura/fabrica/punctele rămân variabile explicite.')
G('O18.1 P18.1','Regresie pe domeniul livrat','§10; R04; R11–R12','Șase trasee de bază folosesc text, filtre, serii, ambalaj/mesaj, checkout și cerere Pro. Personalizarea, AI, căutarea foto și Club au trasee după activarea extensiei; prețul pe client nu este cerință de temă.','QA: raport separat pe temă/extensie și pe ambele teme; fără operațiuni sensibile executate de AI.')
G('O19.1','Eșantionul de produse','§19; matricea V2','Eșantionul de 50 și cele șase concluzii sunt păstrate. Datele istorice nu sunt stocuri actuale; relațiile și promisiunile trebuie validate.','Date: lista reproductibilă rămâne în anexa V2; D01 reconciliază sursa actuală.','Păstrat')
G('O20.1','Benchmark','§20','Se păstrează delimitarea dintre elemente observabile și ipoteze de cercetare. Nu se pretinde audit tranzacțional complet al concurenților.','UX: cercetare și testare conform planului, fără rezultate fabricate.','Păstrat')
G('O21.1 P21.1','Trei direcții vizuale distincte','§21.1–21.3; I8','Planșele au fotografii din arhivă, trei perechi de fonturi, palete și fragmente de produs: Atelier și glazură, Masa de acasă, Colecția contemporană. Sursele vizuale au hashuri.','UX: fișierul conține planșele; alegerea finală și drepturile de publicare se validează în D03.','Livrat documentar')
G('O21.2','Wireframe-uri de mobil','§21.4–21.6','Se păstrează home, produs și masa completă, cu ierarhie și alternativă de listă accesibilă. Intrările extensiilor sunt delimitate după activare.','UX: testele pe sarcini și criteriile de accesibilitate rămân recepție viitoare.','Livrat documentar')
G('OM.1','Istoricul celor 118 coduri','Matrice V3; §3 din prezenta matrice','Acoperirea A2 rămâne în matricea V3 nemodificată. Puntea de mai jos actualizează deciziile de domeniu pentru V4; nu se șterge istoricul pentru a reduce numărul cerințelor.','Control de documente: V2/V3 și auditurile păstrate; V4 prevalează pentru planul curent.','Trasabilitate păstrată')
G('OM.2 PM.1','Trasabilitatea addendumurilor','§2 din prezenta matrice; §9; R11','Ambele addendumuri au secțiuni de trasabilitate cu identificatori editoriali AD2 și AD3. Sunt incluse explicit variantele, theme_schedule, R11 și revenirea prin comutare.','Control automat: toate cele 80 coduri A3 sunt mapate o singură dată; addendumurile sunt urmărite separat.','Livrat documentar')
G('OM.3','Titlu fără ambiguitate','Titlul documentului','Matricea se numește „Matricea CESIRO V4 pentru auditul V3 și addendumuri”, distinct de versiunea proiectului auditat.','Titlu și proprietăți DOCX actualizate.','Corectat')
G('OM.4 PM.2','Înlocuirea condiționărilor neclare','§11.1; §3 din prezenta matrice','Funcțiile absente au starea „extensie E# planificată” ori „ulterior”. Domeniul actual include E0–E7, astfel că nu se mai spune că lipsa lor se decide abia la D01.','Punte A2 și inventar static; numai producția, costurile ferme și probele rămân de confirmat.','Corectat')
used=[i for g in groups for i in g['ids']]
assert Counter(used)==Counter(byid.keys()),(set(byid)-set(used),[i for i,n in Counter(used).items() if n>1])
(O/'evidence-v4/audit-mapping.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')
init('Matricea CESIRO V4 pentru auditul V3 și addendumuri','Trasabilitate V4')
p('Matricea CESIRO V4 pentru auditul V3 și addendumuri','Title')
p('Decizii de proiect referințe și probe necesare','Subtitle')
p('Însoțește Proiect_CESIRO_Design_React_Python_V4.docx. Acoperă toate cele 80 coduri din Audit.Claude.V3.0.docx, cele două addendumuri și efectul asupra deciziilor istorice A2. Este răspuns documentar, nu raport de implementare sau certificat de conformitate.')
head('Domeniul curent')
p('Tema nouă React funcționează în motorul Python/Flask existent. Varianta C din addendumul V3 planifică și E0–E7 în aceeași aplicație și bază, cu rute și migrări strict necesare, fără sistem API paralel. Tema rămâne la S16; programul complet la S24–26, cu 240–320 zile-persoană. Nicio modificare a site-ului nu este executată prin această revizie.')
head('Cum se citește matricea')
table(['Stare','Semnificație'],[('Specificat sau planificat','Cerință, activitate și probă viitoare. Nu echivalează cu funcție instalată.'),('Fapt verificat','Citire statică ori inventar datat. Configurația și producția se confirmă separat.'),('Livrat documentar','Element prezent în proiect/matrice: tabel, planșă, calcul sau trasabilitate.'),('Dependență deschisă','Intrare încă indisponibilă, cu responsabil și termen. Nu este marcată fictiv închisă.')],[5,12.5])
p('Prioritatea dintre paranteze este copiată din audit. Identificatorii A3 apar o singură dată în secțiunea 1. Referințele § indică proiectul V4; referințele la această matrice sunt numite explicit. AD2 și AD3 sunt identificatori creați aici pentru cerințe fără cod în documentele sursă.')
p('Nota 8,3/10 din audit și estimarea condiționată de 8,8/10 din addendum aparțin auditorului. Acest răspuns nu atribuie o notă nouă și nu promite 10/10. Închiderea operațională cere versiune, probă și semnătură.')
for j,g in enumerate(groups):
    if j%4==0:page('1 Auditul Claude V3'+(' continuare' if j else ''))
    h(f'{j+1} '+g['topic'])
    p('; '.join(i+' ['+byid[i]['priority']+']' for i in g['ids'])).paragraph_format.keep_with_next=True
    table(['Decizie și stare','Probă responsabil și referință'],[(g['status']+'. '+g['decision'],g['where']+'. '+g['proof'])],[10.3,7.2],small=10)

ad2=[
('AD2-01 Temă proprie','§9; R11','cesiro_atelier este numele de lucru; base, parent=null, template atelier. Se înregistrează cu manifest/files/page_contracts/README, fără înlocuirea motorului.'),
('AD2-02 Izolarea șabloanelor','§9–10; R11','Directoare proprii pentru șabloane și asseturi. templates/shared rămâne neatins; fragmentele diferite sunt locale temei.'),
('AD2-03 Motor comun','§9; R00','Coș, checkout, cont, i18n și logică comercială rămân comune. E0–E7 extind motorul cu regresie pe ambele teme, fără catalog sau autentificare paralele.'),
('AD2-04 JavaScript și React','§10','Insule cu proprietate DOM explicită, build Vite și asseturi statice. Nu se dublează handlerii scripturilor vechi și nu se adaugă runtime Node de storefront.'),
('AD2-05 Pagini și limbi','§6–6.1; R02; R11','Inventarul anterior de 24 este înlocuit de 25 tipuri de design; 21 de bază, două prin E6/E7 și două concepte. Șase limbi, zero chei lipsă și texte UI fixe.'),
('AD2-06 Variante derivate','§9','10 variante proprii cu parent=cesiro_atelier, numai tokenuri/imagini/mesaje; variantele marketplace_pro se păstrează.'),
('AD2-07 Calendar','§9; R11','theme_schedule pentru manual/automat, default, date și priorități; test Paște ortodox/catolic. Nu se creează un al doilea calendar.'),
('AD2-08 Preview și revenire','§9.1; R08; R11','Preview autorizat, condițiile reale pentru ?theme= și cookie, revenire prin admin sub un minut. Recuperare completă ≤15 min, cu păstrarea coșurilor/comenzilor și E0.'),
('AD2-09 Validator și predare','§18.1','Validator tenant fără erori, surse/build/licențe/manual și două persoane instruite. Manifestul nu declară pagini desenate ca fiind funcționale.'),
('AD2-10 Randare și performanță','§10; R06–R07; R11','HTML lizibil fără JavaScript, comparație SEO pe aceleași URL-uri, React inițial pe produs ≤120 KB, total JS ≤170 KB; praguri CWV separate.'),
('AD2-11 Contracte și testare','§11.1; R00; R04','Contracte documentate pentru rutele reale. Propunerea de mutare generală în /api/v1 nu se preia; se păstrează compatibilitatea actuală și se adaugă strict operațiile E#.'),
('AD2-12 Estimarea înlocuită','§16–17','Calendarul și efortul vechi din acest addendum nu se cumulează cu noul plan. Se aplică addendumul V3: temă S16, program S24–26, total 240–320 zile.')]
ad3=[
('AD3-01 Varianta C','§0; §9','Temă și extensii esențiale/inovare, în aceeași platformă. „Fără sistem API nou” înseamnă fără sistem paralel; rutele necesare E0–E7 sunt parte din motorul actual.'),
('AD3-02 E0 și E2 urgent','§12.1; §16','E0 6–10 și E2 3–5 zile, S1–3 pe tema existentă. Funcție de retragere fără cont, dovadă durabilă și acces limitat securizat; operator uman pentru probele sensibile.'),
('AD3-03 E1 filtre','§5; §11; §17','4–6 zile pentru serie/decor și persoane pe catalogul canonic; 20 serii și 100 SKU-uri validate, compatibilitate cu cererile vechi.'),
('AD3-04 E3 CUI','§8.3; §11.1','2–4 zile, reutilizare logică din grup; 20 cazuri de test și completare manuală. Nu se confundă cu e-Factura/OAuth fiscal.'),
('AD3-05 E4 public doar citire','§8.1; R12','15–25 zile, reutilizare LLM sigur, fără rol OWNER/unelte admin; date publice și comandă autorizată minimală. 300 cereri, prag ≥90%, zero divulgări/acțiuni interzise.'),
('AD3-06 E5 vizual și semantic','§8.1; §9.1; R12','15–20 zile, pgvector în baza existentă, model/versionare și filtrare eligibilitate. 150 imagini, Recall@5 ≥85%, 360 interogări în șase limbi și nDCG@10 ≥0,80.'),
('AD3-07 E6 personalizare','§8.2; R12','20–30 zile pentru 10 produse, fișiere 1:1, hashuri, 20 comenzi simulate și 10 proof-uri fizice; capacitate și preț aprobate de fabrică.'),
('AD3-08 E7 Club','§8.3; R12','15–20 zile, registru idempotent și reconciliere. Costul punctelor este aprobat de financiar; AI nu declanșează retururi pentru a proba ajustări.'),
('AD3-09 Limitele inovării','§17.5','Liste de eveniment, loturi, preț pe client, card cadou cu sold, AR și abonamente rămân ulterior, cu estimări preliminare unde sunt definite.'),
('AD3-10 Calendar și capacitate','§16–17','160–200 zile temă +80–120 extensii. S16 pentru temă, S24–26 complet; vârf 4–5 FTE rezervat, medii și zile facturabile distincte.'),
('AD3-11 Buget și AI','§17.1','Local 97.589–200.675 EUR; furnizor 138.989–255.875 EUR, cu rezervă. AI 600 EUR/lună comun E4/E5 separat; timpul intern și mentenanța extensiilor sunt cuantificate suplimentar.'),
('AD3-12 Activare și riscuri','§9.1; §17.5; R12','Flag pe tenant, praguri de calitate, capacitate PGX, proof și marjă. Oprirea inovării păstrează cumpărarea standard; E0 are continuitate proprie și nu dispare la rollback.')]
for label,rows in [('Addendumul la auditul V2',ad2),('Addendumul la auditul V3',ad3)]:
    for start in [0,6]:
        page('2 '+label+(' continuare' if start else ''))
        p('Sursa este documentul Addendum1 din folderul Audituri. Codurile de mai jos sunt identificatori ai acestei matrice, nu coduri atribuite de auditor.')
        table(['Cerință urmărită','Decizie și referință V4'],[(a,b+'. '+c) for a,b,c in rows[start:start+6]],[4.7,12.8],small=10)

page('3 Actualizarea deciziilor istorice A2')
p('Matrice_Raspuns_Audituri_CESIRO_V3.docx rămâne registrul complet al celor 118 coduri A2. Matricea V2 păstrează cele 179 coduri Claude V1, 20 teme Gemini și eșantionul de 50 produse. Următoarele decizii curente înlocuiesc condiționările ori excluderile din V3, fără modificarea documentelor istorice.')
table(['Grupa istorică','Starea curentă în V4'],[
('Etaloane inovare și valoarea asistenței','E4/E5 incluse în plan, §8.1, §17 și R12; KPI pornesc după activare.'),
('Asistent după cumpărare','E4 citește exclusiv comanda autorizată prin cont/E2; nu execută operațiuni sensibile.'),
('Capacitate de producție','Registru și proof pentru E6 incluse; motorul de loturi rămâne ulterior, §17.5.'),
('Personalizare și retragere','E6 planificat; E0 înregistrează declarația fără a elimina drepturile pentru neconformitate.'),
('Date de firmă și TVA','E3 inclus, 2–4 zile; fiscalitatea și e-Factura rămân contracte distincte.'),
('Obiective Pro','Pagina, firmele și ofertele de bază plus E3. Prețul pe client este ulterior; Club prin E7.'),
('Buget AI','Plafon 600 EUR/lună pentru E4+E5, separat de baza de investiție; nicio promisiune de 10.000 sesiuni E4 dacă E5 consumă aceeași alocație.'),
('Calendar efort și capacitate','16 săptămâni pentru temă, 24–26 pentru program; total 240–320 zile și contribuții interne separate.'),
('Arhitectură și motor EVA','Flask/Jinja + React; extensii additive în aceeași aplicație. Fără sistem API sau catalog paralel.'),
('Autoservire și R09','E0/E2 urgente pe tema actuală. Recepția legală nu este amânată până la inovare.'),
('Anexa vizuală și recepție','Fotografii, fonturi și fragmente noi; R11 temă și R12 extensii, cu probe distincte.')],[5.2,12.3])
page('4 Registrul de închidere')
counts=Counter(a['priority'] for a in audit)
p('Control automat: 80 identificatori unici, 44 observații și 36 propuneri, fiecare mapat exact o dată, fără omisiuni sau dublări. Distribuție originală: '+', '.join(f'{k} {n}' for k,n in counts.items())+'. Sunt urmărite suplimentar 12 cerințe AD2 și 12 cerințe AD3.')
table(['Element','Responsabil și probă','Termen'],[
('Documentație','Proiect V4, această matrice, trei planșe foto și trei wireframe-uri; verificare de conținut și paginare.','Această livrare'),
('Sursa instalată','Platformă: commit, digest, tenant și imagine; manifestul local nu le substituie.','D01 S1–2'),
('Date și ținte','Date/financiar: inventar actual, reconciliere, ABC, baseline și recalibrare.','D01/D02 S1–2'),
('Cerințe urgente','Platformă/juridic/suport: E0/E2 demonstrate pe tema actuală de operator uman.','S1–3'),
('Design și teme','UX/QA: 25 tipuri, 75 ecrane, 10 variante și mapă de rute; R11.','D03 S1–4; recepție S16'),
('Inovare','AI/fabrică/financiar: rapoarte E4–E7, resurse și costuri; R12.','Pe extensie până la S24–26'),
('Operare','DevOps: nivel disponibilitate acceptat, restaurare, revenire și două persoane instruite.','ADR04 și înainte de lansare'),
('Rezultate comerciale','PO/analytics: raport distinct cu fereastră completă, incertitudine și cost.','90 zile de la fiecare activare')],[3.8,10.1,3.6])
p('Acceptarea documentației și acceptarea sistemului sunt etape diferite. GitHub inaccesibil, configurația live, ofertele ferme și rezultatele operaționale rămân explicit deschise. Niciun element nu este bifat implementat pentru a obține artificial o notă.')
save('Matrice_Raspuns_Audituri_CESIRO_V4.docx')
print(f'Matrice V4: {len(groups)} grupe, {len(used)} coduri A3, 24 cerințe addendum')
