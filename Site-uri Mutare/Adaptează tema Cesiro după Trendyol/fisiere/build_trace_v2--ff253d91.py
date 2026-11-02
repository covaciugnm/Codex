from build_v2 import *
from collections import Counter

audit=json.loads((OUT/'evidence-v2/audit-claude.json').read_text(encoding='utf-8'))
lookup={x['id']:x for x in audit}
groups=[]
def g(ch,codes,topic,decision,where,proof):
    ids=codes.split()
    assert all(i in lookup for i in ids),codes
    groups.append(dict(ch=ch,ids=ids,topic=topic,decision=decision,where=where,proof=proof))

g(0,'O0.1 O0.2 P0.1','Poziționare și viziune','Adoptat. Brand de ceramică și masă, cu servicii directe măsurabile. Afirmațiile despre fabrică sunt validate înainte de folosire.','0 și 3','Viziune, arhitectură de portofoliu și registru de dovezi de origine; sponsor + juridic.')
g(0,'O0.3 P0.4','Repetarea limitelor','Adoptat. O singură clauză de domeniu în capitolul 20.','20','Control editorial al proiectului; PO.')
g(0,'O0.4 P0.2','Diferențiatori și business','Adoptat cu validare operațională. Origine, masă completă, personalizare și politică de spargere justificată.','0, 4 și 8','Praguri comerciale, serii, scene și pilot; garanția nu este promisă fără proces aprobat.')
g(0,'O0.5','Lansare concentrată','Adoptat. Patru valuri și comutare reversibilă, cu trafic progresiv.','16','Plan de cohorte, probe de rollback și criterii de trecere; lider tehnic.')
g(0,'P0.3','Repere de brand','Adoptat. Opt repere plus Trendyol, cu element observat și adaptare proprie.','20','Matrice comparativă și surse oficiale; nu se pretinde testarea checkouturilor concurente.')

g(1,'O1.1 P1.1','Date interne','Adoptat parțial acum. Export și cod local inspectate; raportul comercial curent rămâne de furnizat în A1.','1 și 16','5.222 înregistrări numărate; D01 și raport 12 luni cerute în 3–5 zile; responsabil date.')
g(1,'O1.2 P1.2','Diluarea catalogului','Adoptat. Vitrină Ceramică și Masă, zonă /pro; restul portofoliului primește decizie de canal, fără eliminări automate.','1 și 5','Matrice SKU–familie–canal–destinație URL, aprobată de comercial.')
g(1,'O1.3 P1.4','Dimensiunea contractuală','Clarificat. 5.221 SKU-uri nenule distincte în exportul istoric; activele curente nu sunt cunoscute.','1 și 17','Hash export și numărători; reconciliere curentă obligatorie înainte de deviz fix.')
g(1,'O1.4 P1.3','ABC și produse prioritare','Adoptat ca activitate, nu rezultat inventat. ABC venit plus marjă/rotație; maximum 300 prioritare.','1','Raport ABC și listă justificată pe 12 luni; comercial + date.')

g(2,'O2.1 P2.1','Atribute pe familii','Adoptat. Model extins pentru serie, rol, componente, persoane, ambalaj, culoare și utilizare.','2','Dicționar, tipuri, unități, câmpuri obligatorii și aplicabilitate pe familie; R01.')
g(2,'O2.2 P2.2','Siguranță și contact alimentar','Adoptat cu aplicabilitate legală. Condițiile obligatorii sunt independente de scorul editorial.','3 și 13','Documente reale și câmpuri GPSR/food contact pentru fiecare produs eligibil; juridic + fabrică.')
g(2,'O2.3','Prețul anterior','Adoptat și aprofundat. Modulul există, dar fallbackul la prețul de catalog nu probează istoricul legal.','11 și 13','Verificare istoric, promoții succesive și istoric absent; comercial + juridic.')
g(2,'O2.4 P2.3 P2.4','Tags și îmbogățire AI','Adoptat în valuri. Drafturi AI și relații/coșuri agregate, cu aprobare și sursă.','3 și 8','Etalon 200 produse; praguri de precizie și zero specificații critice inventate; date + AI.')

g(3,'O3.1','Reguli corecte existente','Păstrat. Necunoscut ≠ zero, capacitate pe componentă și compatibilitate demonstrată.','2 și 19','Teste de normalizare și exemple ceașcă/set; R01.')
g(3,'O3.2 P3.2','Prioritizare în loturi','Adaptat. Arhivarea completă nu așteaptă editarea; prioritare, active și arhivă au livrare separată.','1, 3 și 16','100% înregistrări contabilizate; loturi publicate numai dacă sunt eligibile; date.')
g(3,'O3.3 P3.1 P3.3','Scor și monitorizare','Adoptat. Grilă 100 puncte, prag 90/60 și raport zilnic; condiții obligatorii separate.','3','Algoritm versionat, explicație scor și alertă la regresie; R01.')
g(3,'O3.4 P3.4','Superlative și origine','Adoptat. Revizuire documentară a tuturor promisiunilor de origine, capacitate și superioritate.','3 și 13','Registru afirmație–document–dată–aprobare; juridic + sponsor.')

g(4,'O4.1 P4.1','Baseline comercial','Date încă necesare. V2 oferă definiții și registrul D02; nu poate prezenta drept existente rapoarte de vânzări/analytics neconsultate.','4 și 16','D02 înainte de angajamente comerciale și buget final; financiar + growth.')
g(4,'O4.2 O4.4 P4.2','Venit retenție mobil','Adoptat. Venit net direct, AOV, conversie mobilă, recumpărare și recenzii, cu formule și termene.','4 și 15','Dashboard reconciliat financiar, cohorte mature și guardrails; R10.')
g(4,'O4.3','UX nu dovedește efectul A/B','Păstrat și explicitat. Testele de utilizare și experimentele comerciale au probe distincte.','15 și 18','Raport SUS/sarcini separat de analiza statistică; UX + growth.')
g(4,'P4.3','Măsurarea inovării','Adoptat. Utilizare ≥10% din sesiunile expuse și personalizare ≥5% din comenzile eligibile.','4 și 8','Evenimente de expunere și utilizare; denominatori documentați; R05/R10.')

g(5,'O5.1 P5.1','Meniu hibrid','Adoptat. Tipurile de produs conduc meniul; ocaziile completează descoperirea.','5','Test de găsire farfurii, căni și cadouri; succes ≥90%; UX.')
g(5,'O5.2 P5.2','Colecții dinamice','Adoptat. Reguli, override, stoc, programare și limbă; minimum 8 produse pentru promovare.','5 și 7','Editorul publică o colecție din date pregătite în ≤5 minute; demo CMS.')
g(5,'O5.3 P5.3','Serii și completare','Adoptat. Pagini de decor și „Ce ai deja?”, relații verificate și alternative distincte.','5 și 8','20 serii și 10 scenarii de cantitate/buget; R05.')
g(5,'O5.4','Cadouri pentru el și ea','Adaptat la cererea utilizatorului. Se păstrează opțional, alături de relație, ocazie, stil și buget.','5','Reguli și conținut fără stereotipuri; nu se elimină cererea inițială pentru a urma preferința auditorului.')
g(5,'O5.5 P5.4 P5.5','Culoare persoane și meniu','Adoptat cu date validate. Swatchuri și număr de persoane; meniu vizual desktop și panou mobil accesibil.','5 și 6','Test tastatură și cititor ecran; etichete text; persoanele derivă din componente, nu doar număr de piese.')

g(6,'O6.1 P6.1','Concept creativ','Adoptat ca livrabil. Trei direcții descrise și selecție prin două runde de test.','6','Moodboarduri, homepage/produs la 390 px și raport de decizie; D03.')
g(6,'O6.2 P6.2','Pagini lipsă','Adoptat. 24 tipuri, inclusiv fabrică/showroom, serie, personalizare, eveniment, Pro, Outlet și card cadou.','6','72 ecrane de bază și stări aplicabile; R02.')
g(6,'O6.3','Comparație și recente','Adoptat. Comparare până la 4 produse și vizualizări recente, cu reguli de confidențialitate.','6','Demonstrație pe familii comparabile; fără atribute irelevante sau date între conturi.')
g(6,'O6.4 P6.3','Prioritate mobil','Adoptat. Prototip principal la 390 px, comandă fără cont și checkout pe o pagină.','6 și 18','Timpi și succes de sarcină, plus verificare la 768/1440 px; R02/R03.')
g(6,'O6.5 P6.4','Microinteracțiuni și PWA','Adoptat gradual. Tranziții cu fallback, mișcare redusă, PWA și push cu acord.','6 și 10','Test fără suport API și fără notificări; zero cache de checkout sau date personale.')
g(6,'P6.5','Textură scară și video','Adoptat. Galerie, video scurt, detaliu și scară; fără afirmații tehnice nedovedite.','7','30 clipuri și galerii prioritare; probe de culoare și proporție.')

g(7,'O7.1 O7.2 P7.1','Sistem de design','Adoptat. 60–80 componente estimate; Figma, tokenuri și Storybook cu regresie vizuală.','7 și 10','Acoperirea stărilor folosite și trasabilitate design–cod; R02/R07.')
g(7,'O7.3 P7.2','Media compusă și 3D','Adaptat. Scene/randări permise cu fidelitate, proveniență și simulare marcată unde contează.','7 și 8','12 scene și 10 modele pilot; drepturi și scară verificate; content + fabrică.')
g(7,'O7.4 P7.3','Traducerea integrală','Adoptat în buget. Flux pe toate înregistrările/6 limbi; nu se publică erori critice sub simplu marcaj de calitate.','3, 7 și 17','Revizie umană prioritare și texte critice; eșantionare rest; volum și cost în deviz.')
g(7,'O7.5 P7.4','UGC','Adoptat. Fotografii și recenzii autentice, moderare și permisiune de folosire.','7 și 8','Flux după livrare, retragere și moderare; fără recenzii sintetice sau bonus pentru opinie pozitivă.')
g(7,'P7.5','Ton pe limbi','Adoptat. Ghid și exemple pe șase limbi pentru revizie de vorbitori competenți.','7','Aprobarea conținutului localizat și terminologie consecventă; content.')

g(8,'O8.1 P8.1','Asistent AI','Adoptat. Catalog și politici aprobate, informare AI, voce opțională și control explicit al clientului.','8 și 13','200 cereri, 40 adversariale, ≥90% corect/utile; zero acțiuni neautorizate; R05.')
g(8,'O8.2 P8.3','Personalizare','Adoptat. Pilot 10 produse, preview aprobat și fișă de producție, cu termen și cost.','8','20 comenzi simulate reconciliate și capacitate validată de fabrică înainte de activare.')
g(8,'P8.2','Căutare vizuală și semantică','Adoptat. Distincție între potrivire exactă și produs similar; etaloane pe limbi.','8 și 9','Recall@5 ≥85%, identificări false ≤2%, nDCG@10 ≥0,80 pe seturile definite.')
g(8,'P8.4','Liste de eveniment','Adoptat cu două niveluri. Listă și cumpărare piese în bază; contribuții financiare de grup condiționate de PSP/juridic.','8 și 17','Concurență pe cantitate, protecția adresei, expirare rezervări; pilot financiar în extensie.')
g(8,'P8.5','WebAR','Adoptat ca pilot. 10 modele GLB/USDZ; fallback 2D și imagine.','8','Test pe iOS/Android, scară și SKU corecte; extindere după efect și cost.')
g(8,'P8.6','Recomandări','Adoptat. Reguli în primul val, coșuri agregate și similitudine ulterior; stoc și marjă drept filtre interne.','8 și 16','Relevanță editorială și absența recomandărilor neeligibile; merchandising.')
g(8,'O8.3 O8.4 P8.7 P8.8','Retenție CRM și afiliere','Adoptat. Automatizări, Club, canale eligibile și control al frecvenței/consimțământului.','8, 14 și 15','Trigger, oprire, deduplicare, puncte și atribuire reconciliate; CRM + financiar.')
g(8,'O8.5 P8.9','Mystery Box','Adaptat. Prezentare și dezvăluire accesibilă; abonamentul intră în extensia validată, fără raritate fictivă.','8 și 17','Reguli, cost, marjă și plăți recurente aprobate înainte de activare; PO.')

g(9,'O9.1 O9.2 P9.1','Reutilizare EVA și eliminare Django','Adoptat, susținut de fișiere locale. Flask rămâne motorul comercial; Next.js livrează interfața.','9 și 11','ADR01 și analiza diferențelor cu versiunea instalată; fără duplicarea modelului de date.')
g(9,'O9.3','JavaScript și TypeScript','Clarificat. Cerința utilizatorului rămâne JavaScript/React; TypeScript este strat recomandat compilat în JavaScript.','9 și 10','Documentarea alegerii și compatibilitatea cu adminul existent; lider tehnic.')
g(9,'O9.4 P9.4','Motor de căutare','Adoptat prin PoC. Meilisearch candidat și pgvector pentru similitudine; nu deducem limite PostgreSQL din număr de produse.','8 și 9','ADR02 cu relevanță, limbi, latență, cost, operare și fallback.')
g(9,'O9.5 P9.5','CDN monitorizare și flags','Adoptat. CDN/WAF, Sentry/OTel și GrowthBook, cu confirmarea serviciilor disponibile.','9, 13 și 16','Alerte, expunere stabilă, cache izolat și comutare; DevOps.')
g(9,'P9.2','Migrare graduală','Adoptat. Preluare pe rute/cohorte, sesiuni coerente și schemă compatibilă.','10 și 16','Canary fără cloaking, coș păstrat, rollback ≤15 min.')
g(9,'P9.3','FastAPI','Extensie justificată numai de nevoie. Nu se include o migrare suplimentară de framework în pilot.','9','ADR separat cu cost și beneficii măsurate înainte de o eventuală schimbare.')
g(9,'P9.6','PGX și Qwen','Condiționat. Modelul, licența, capacitatea și costul se verifică; modulul admin nu dovedește infrastructura de inferență.','3 și 9','PoC, cost/1.000 produse și plafon operațional; AI + DevOps.')

g(10,'O10.1 P10.1','Matrice de randare','Adoptat. Conținut public cacheabil, tranzacții no-store și recomandări independente.','10','ADR03, invalidare între instanțe și verificare server înainte de comandă.')
g(10,'O10.2 P10.2','Biblioteci frontend','Adoptat. React/Next, Radix, Tailwind, TanStack, RHF/Zod și validare Python.','10','Catalog de componente și contracte; revizie a versiunilor la execuție.')
g(10,'O10.3','Samsung Internet','Adoptat. Inclus explicit în matricea de browsere și fallbackuri.','10','Rapoarte pe versiunile suportate și dispozitive reprezentative.')
g(10,'O10.4 P10.3','Automatizare testare','Adoptat. Șase trasee Playwright, regresie vizuală și Lighthouse CI; probe sensibile umane.','10 și 18','Rapoarte legate de versiune; fără apeluri AI de anulare/retur/rambursare.')
g(10,'O10.5 P10.4','Prefetch','Adoptat limitat la rute publice sigure. Respectă capabilități, economie de date și efecte comerciale.','10','Teste de fallback și lipsa cererilor cu mutații înainte de acțiunea clientului.')

g(11,'O11.1 O11.4 P11.1','Entități și admin duplicate','Adoptat. Matrice de reutilizare/extindere/nou, bazată pe fișiere; ecranele se integrează în adminul existent.','11','Gap analysis și demonstrație funcțională, fără a confunda prezența fișierului cu recepția.')
g(11,'O11.2','Set comercial și pachet','Păstrat. Setul are identitate și componente; pachetul configurat are componente rezervate individual.','2 și 8','Calcul, cantități, preț și rezervări verificate; R04/R05.')
g(11,'O11.3 P11.2','Entități de inovare','Adoptat. Config/Job, Registry/Item, LoyaltyLedger, embeddings, scor și media UGC.','8 și 11','Relații către ID canonic, fișier producție versionat și jurnal; backend.')
g(11,'P11.3','AI în admin','Adoptat cu restricții. Drafturi și aprobări, păstrând guard/history și politica operațională locală.','3, 11 și 12','Test de refuz, audit de aprobare, zero acțiuni interzise; responsabil platformă.')

g(12,'O12.1 P12.1','Plăți moderne','Adoptat cu eligibilitate. Guest, wallet, tokenizare și opțiuni BNPL evaluate contractual.','12','PSP, țară și dispozitiv validate; test de succes/eșec/fallback; fără promisiuni de furnizor neconfirmate.')
g(12,'O12.2 P12.2','e-Factura','Adoptat și corectat. eva_docs inspectat citește documente de curier; conectorul fiscal nu este confirmat.','11, 12 și 13','Identificare sau extensie SPV, status, retry, deduplicare, termen fiscal și probă contabilă.')
g(12,'O12.3 P12.3','Stoc pe canale','Adoptat cu latență și autorizare. Autoritate comună, tampon și reconciliere; nu promitem atomicitate externă imposibilă.','12','Simulare concurență și degradare; scrierile externe rămân sub regulile proprietarului.')
g(12,'O12.4 P12.5','Prag de transport','Adoptat. Bară configurabilă și recomandări eligibile; 500 lei rămâne valoare publică de reverificat.','12','Aceeași bază și prag pe produs/coș/checkout; teste monedă și promoție.')
g(12,'O12.5 P12.4','Adresă locker și termen','Adoptat. Hartă plus listă accesibilă, autocompletare și introducere manuală.','12','ETA din date reale, test întrerupere API și adresă specială; logistică + QA.')

g(13,'O13.1 P13.1','Accesibilitate legală','Adoptat cu precizare. AA este condiție contractuală; aplicabilitatea Legii 232/2022 și excepțiile se verifică distinct.','13','Audit manual și informații publice de accesibilitate; juridic + UX; R07/R09.')
g(13,'O13.2 P13.2','Autentificare modernă','Adoptat. Passkeys/link magic și social opțional; contul nu se activează tacit.','13','Token unic/expirat, recuperare, alegerea clientului și guest; securitate.')
g(13,'O13.3 P13.3','Anti-boți și fraudă','Adoptat. WAF, rate limit, protecție card testing și alternativă accesibilă.','13','Scenarii de abuz și fals pozitiv; nu se garantează absența verificărilor vizibile.')
g(13,'O13.4 P13.4','Încărcare','Adoptat. Profil 10× vârf observat, 2× catalog și anduranță; coadă doar dacă este necesară.','13','Raport cu cereri/s și comenzi/min; fără echivalarea numărului de utilizatori cu sarcina.')
g(13,'O13.5 P13.5','Consimțământ și măsurare','Adoptat. CMP, Consent Mode v2 și server-side respectă acordul; nu sunt certificat GDPR.','13 și 15','Test accept/refuz/retragere; fără marketing neautorizat, date mascate și retenție.')

g(14,'O14.1 P14.1','Bulgaria și moneda','Clarificat. EUR/BG este explicit; V1 nu specifica BGN ca monedă nouă. Observația nu dovedește o eroare monetară V1.','14','Test limbă–țară–monedă și păstrarea istoricului BGN; financiar.')
g(14,'O14.2 P14.2','Descoperire prin AI','Adaptat. Date și ghiduri utile, JSON-LD corect; llms.txt experimental, fără promisiune de recomandare.','14','Validare schema și măsurarea referințelor; sursa Google nu cere optimizări AI speciale.')
g(14,'O14.3 P14.3','Conținut SEO','Adoptat. 30 ghiduri etapizate, dintre care 10 la primul val, cu produse eligibile.','14 și 16','Calendar editorial, autor, surse, limbă și date de revizie; content.')
g(14,'O14.4','Filtre indexabile selectiv','Păstrat. Numai combinații aprobate și utile; control al spațiului de URL-uri.','14','Crawl, canonical și listă de pagini indexabile; SEO.')
g(14,'O14.5 P14.4','Feeduri','Adoptat cu eligibilitate. Reutilizarea feeds.py; piețele și conturile Google/Meta/TikTok se verifică.','11 și 14','ID, GTIN legitim, preț/stoc/transport coerente; monitorizare respingeri, țintă ≥98% eligibile acceptate.')

g(15,'O15.1 P15.1','Platformă de măsurare','Adoptat. GA4/server-side cu CMP; PostHog alternativ, fără colectare dublă implicită.','15','Plan evenimente, deduplicare și reconciliere financiară; analytics + juridic.')
g(15,'O15.2 P15.2','Cohorte și experiență','Adoptat. Recumpărare, venit și marjă/client, CSAT/NPS, spargeri și costul incidentelor.','4 și 15','Cohorte mature, rate de răspuns și LTV estimat etichetat; R10.')
g(15,'O15.3 P15.3','Experimente','Adoptat cu fezabilitate statistică. 15 ipoteze și țintă 2/lună când traficul permite.','15','Plan predefinit, putere și efect minim, intervale și rezultat neconcludent dacă este cazul.')
g(15,'O15.4','Marjă și retururi','Păstrat și extins. Praguri de analiză pentru marjă, spargeri, plăți și suport.','4 și 15','Guardrails în dashboard și decizie de oprire documentată.')

g(16,'O16.1 O16.3 P16.1','Valuri și pilot real','Adoptat. Patru valuri cu livrabile, trafic progresiv și etape reversibile.','16','Rezultate pe cohortă și flag; primul pilot până la săptămâna 6, dacă intrările sunt pregătite.')
g(16,'O16.2','Pornirea frontend/backend','Adoptat. Design și contracte din săptămâna 1, dezvoltare reutilizabilă din săptămâna 2.','16','Plan de sprinturi și dependențe; lider tehnic + PO.')
g(16,'O16.4 P16.2','Product Owner','Adoptat. Nominalizare în A0, înlocuitor și disponibilitate; nu inventăm numele unei persoane.','16 și 17','Registru responsabilități înainte de pornire; sponsor.')
g(16,'P16.3','Criterii de trecere','Adaptat. Zero erori critice, performanță și prag comercial de non-inferioritate cu incertitudine explicită.','16 și 18','Nu se afirmă „conversia nu scade” din trafic insuficient; raport de gate semnat.')

g(17,'O17.1 P17.1','Efort reutilizare și inovare','Adaptat. 190–220 zile în scenariul complet recomandat; minimum 25% inovare, incluse în total.','17','Deviz refăcut după gap analysis; reutilizarea nu garantează singură economiile.')
g(17,'O17.2 P17.2','Roluri suplimentare','Adoptat. AI, CRM, content/foto, growth, QA și DevOps sunt explicite.','17','Alocare pe roluri și furnizori externi; fără dublarea costurilor de content.')
g(17,'O17.3','Dependență de o persoană','Adoptat. Două persoane instruite, documentație și exercițiu independent de restaurare.','13 și 17','Raport de restaurare condus de a doua persoană; R08.')
g(17,'O17.4 P17.3','Riscuri legale și canal','Adoptat. Registru cu proprietari de rol, măsuri și praguri; numele se fixează la A0.','13 și 17','Revizie periodică și decizie de oprire pe domeniu; PO.')
g(17,'O17.5 P17.4','Buget monetar','Adoptat. Trei scenarii EUR, formule, rezervă și costuri recurente; fără curs RON fictiv.','17','Verificare aritmetică și ipoteze semnate; financiar. Minim ≠ domeniu complet.')

g(18,'O18.1 O18.2 P18.1','Domeniu modern și Pro','Adoptat. Recomandări, Club, personalizare și portal Pro minimal; creditul comercial automat rămâne extensie.','8 și 17','Criterii per funcție, marjă și confidențialitatea prețurilor; R05.')
g(18,'O18.3 P18.2','Criterii de experiență','Adoptat cu protocol. SUS ≥80, succes ≥90%, timpi de add-to-cart și checkout.','18','Mediană, excluderi PSP/SCA și erori raportate separat; UX.')
g(18,'O18.4','Teste critice existente','Păstrat. Ultima unitate, webhook duplicat, plată întârziată și preț schimbat.','12 și 18','Automatizare numai pe operații permise și medii izolate; probe sensibile umane.')

g(19,'O19.1 P19.1','Eșantion prea mic','Rezolvat documentar. 50 înregistrări interne, 10 grupe și raport de lipsuri, cu lista reproductibilă în anexă.','19 și anexa matricei','ID/SKU, familie, selecție deterministă și hash export; nu echivalează cu verificare fizică.')
g(19,'O19.2','Clasificare manuală per produs','Adoptat. Colecții bazate pe reguli și relații; exemplele sunt cazuri de validare.','5 și 19','Test reguli pe catalog, prag de relevanță și timp editor ≤5 min.')
g(19,'P19.2','Machete cu date îmbogățite','Planificat în D03. 10 machete țintă, una/grupă, cu sursa fiecărui atribut nou.','6 și 19','Prototip și aprobare date; nu sunt declarate realizate în revizia documentară.')

g(20,'O20.1 P20.2','Repere comerciale','Adoptat documentar. Opt site-uri oficiale și Trendyol; fără statistici de piață inventate.','20','Matrice observat/adaptare, surse și limite; valorile CESIRO se extrag din D02.')
g(20,'O20.2 P20.1','Vocea clienților','Planificat în A1. 8–10 interviuri și până la 500 recenzii/tichete, raportând baza reală.','16 și 20','Sinteză anonimizată și ipoteze prioritizate; nu pretindem interviuri executate acum.')
g(20,'O20.3 P20.3','Surse legale','Adoptat. Matrice de conformitate și surse primare, cu aplicabilitate pe entitate și piață.','13 și 20','Avize juridic/fiscal și probe înainte de activare; R09.')

seen=[i for x in groups for i in x['ids']]
assert len(seen)==179,(len(seen),set(lookup)-set(seen))
assert set(seen)==set(lookup),set(lookup)-set(seen)
assert len(set(seen))==len(seen),'Duplicate audit IDs'
(OUT/'evidence-v2/audit-mapping.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')

init('Răspuns la auditurile proiectului CESIRO','Trasabilitate V2')
p('Răspuns la auditurile proiectului CESIRO','Title')
p('Matrice de trasabilitate pentru versiunea 2','Subtitle')
p('Documentul însoțește Proiect_CESIRO_Design_React_Python_V2.docx și permite verificarea fiecărei observații, a deciziei adoptate și a probei necesare pentru acceptare. Referințele de capitol urmează proiectul V2; punctele de audit își păstrează identificatorii originali.')
table(['Sursă','Acoperire verificată'],[
('Claude V1.0','92 observații și 87 propuneri, 179 identificatori unici. Fiecare apare exact o dată în matrice. Prioritățile originale sunt păstrate lângă cod.'),
('Gemini V1.0','3 pagini fără coduri proprii. Recomandările și premisele sunt descompuse în 20 puncte G01–G20, definite în acest document.'),
('Rezultat al reviziei','100% dintre punctele numerotate Claude sunt tratate documentar. Aceasta nu înseamnă implementare, recepție, închiderea tuturor dependențelor sau notă acordată de auditori.')],[4,13.5])
h('Cum se citește statusul')
p('Adoptat = cerința este inclusă în proiect. Adaptat = intenția este păstrată, cu o soluție adecvată datelor sau riscului. Păstrat = observația apreciază o regulă deja corectă. Clarificat/Corectat = premisa necesită o corecție probată. Planificat/Condiționat/Date necesare = închiderea cere o activitate viitoare sau o informație care nu există în materialul consultat.')
h('Decizii care rezolvă contradicțiile')
b('Reutilizăm Flask și administrarea React confirmate în fișiere; înlocuirea cu un alt motor comercial nu este justificată de o temă nouă.')
b('31.674 sunt URL-uri de produs în șase limbi. Exportul istoric are 5.222 înregistrări și 5.221 SKU-uri nenule distincte.')
b('eva_docs descrie documente de curier; nu certifică e-Factura. Existența unui modul AI nu certifică infrastructura PGX/Qwen sau un cost marginal redus.')
b('Standardul contractual AA, obligațiile legale aplicabile și condițiile DPP/AI sunt tratate separat. llms.txt nu garantează recomandări în asistenți.')
b('Cerința inițială de cadouri pentru el/ea rămâne opțională în arhitectură; este completată cu relație, stil și buget.')
h('Ce rămâne necesar pentru o reevaluare completă')
p('Baseline comercial curent, demonstrarea versiunii instalate, numirea responsabililor, actele de conformitate și capacitatea fabricii nu pot fi deduse din exportul de produse. Proiectul definește pentru fiecare termen, responsabil și probă. Auditorii pot evalua calitatea specificației acum; o notă privind implementarea cere ulterior probele R01–R10.')

titles=['Viziune și domeniu','Catalog și portofoliu','Atribute și date legale','Calitatea datelor','Obiective comerciale','Navigare și colecții','Design și experiență','Conținut și sistem vizual','Funcții comerciale','Arhitectură','Frontend','Backend și administrare','Checkout și integrări','Accesibilitate și securitate','SEO și piețe','Măsurare','Calendar și lansare','Resurse și buget','Recepție','Eșantion și machete','Cercetare și surse']
for ch,title in enumerate(titles):
    if ch==0:page(f'{ch} {title}')
    else:head(f'{ch} {title}')
    rows=[]
    for x in groups:
        if x['ch']!=ch:continue
        labels='\n'.join(i+' · '+lookup[i]['priority'] for i in x['ids'])
        rows.append((labels,x['topic']+'\n'+x['decision'],'§ '+x['where']+'\n'+x['proof']))
    table(['Cod și prioritate originale','Tratament în versiunea 2','Referință și probă de acceptare'],rows,[3.0,7.4,7.1],small=10)

gemini=[
('G01','p1 sinteză','Identitate emoțională și tactilă','Adoptat: ceramică, glazură, scară și utilizare, cu trei concepte creative.','0, 6, 7','D03 și testare UX; nu adoptăm o clonă vizuală Trendyol.'),
('G02','p1 matrice și p2 cap 1–3','Pipeline AI de îmbogățire','Adoptat: drafturi, surse, aprobare, etalon și scor de calitate.','2, 3','200 produse etalon; precizie și lipsuri măsurate, fără fapte critice inventate.'),
('G03','p1 matrice','Knowledge Graph de stil','Adaptat: graf logic de relații în PostgreSQL înaintea unui motor separat.','8, 11','Relații serie/piesă/stil cu proveniență și relevanță testată.'),
('G04','p1 matrice și p2 cap 4–8','Configurare vizuală a mesei','Adoptat: 2D de bază, configurator React și pilot 3D.','8','12 scene, 20 serii, calcule și stoc validate; R05.'),
('G05','p1 matrice și p2 cap 4–8','WebAR','Adoptat ca pilot pentru 10 modele, cu fallback.','8','Verificare scară, dispozitiv și performanță înainte de extindere.'),
('G06','p1 matrice și p2 cap 9–11','Căutare după fotografie și vectori','Adoptat, cu potrivire similară separată de identificare exactă.','8, 9','Recall@5, fals pozitiv, nDCG și latență din etaloane.'),
('G07','p1 matrice și p2 cap 9–11','Saleor sau Medusa','Neadoptat ca înlocuire implicită. Flask există; Medusa ar schimba backendul Python cerut.','9, 11','ADR01 explică reutilizarea; alternativă numai după dovadă de blocaj și cost total.'),
('G08','p1 matrice','Randare edge sub o secundă','Adaptat. CDN și cache sigur, fără garanție universală sub 1 s.','10, 13','CWV reale și latențe măsurate pe dispozitiv/rețea/sarcină definite.'),
('G09','p1 matrice','Portal B2B cu mostre logo și volum','Adoptat: cont Pro, ofertă, listă SKU, preț pe client, mostre și personalizare.','8','10 scenarii, 100 poziții, izolare prețuri, ofertă tipică ≤10 min.'),
('G10','p1 matrice și p3 cap 14–15','GEO și recomandări AI externe','Adaptat. Conținut verificabil, schema și feeduri; fără garanții de citare.','14','Surse Google, validare structură și monitorizare referințe.'),
('G11','p1 matrice și p2 cap 6–7','Video cumpărabil','Adoptat. Clipuri scurte, subtitrări și produse reale disponibile.','7, 14','30 clipuri; performanță și drepturi; afirmații de rezistență numai cu dovadă.'),
('G12','p2 cap 1–3','Premisa de circa 31.000 SKU-uri','Corectat. Sunt URL-uri pe limbi; exportul istoric arată 5.221 SKU-uri nenule distincte.','1','Numărători și hash; baseline curent se reconciliază înainte de contract.'),
('G13','p2 cap 1–3','Digital Product Passport','Adaptat. Fișă voluntară de trasabilitate pregătită pentru evoluția cadrului.','3, 13','Nu este declarată obligație universală pentru ceramică; actele delegate se verifică.'),
('G14','p2 cap 6–7','Atomic design și blocuri marketing','Adoptat. Tokenuri, componente și 12 blocuri editabile cu preview/programare.','7','Acoperire în Storybook și demo de publicare editorială.'),
('G15','p2 cap 9–11','Complexitate Node/Python și presupus eșec PostgreSQL','Clarificat. Node randează; Python deține comerțul. Numărul de produse nu dovedește degradarea căutării.','9, 10','PoC comparativ, profil de încărcare și ADR cu cost operațional.'),
('G16','p3 cap 12–13','Express checkout și BNPL','Adoptat cu eligibilitate contractuală și geografică.','12','PSP/dispozitive, fallback și cost/marjă; Klarna nu este promis fără verificare.'),
('G17','p3 cap 12–13','Precomenzi pe loturi de ardere','Adoptat ca pilot condiționat de sursa de producție și capacitate.','8, 16','3 loturi validate, cantități rezervate și comunicarea întârzierilor; fabrică.'),
('G18','p3 cap 14–15','A/B continuu cu feature flags','Adoptat cu disciplină statistică și protecția consimțământului.','15, 16','15 ipoteze, 2/lună când traficul permite, guardrails și rollback.'),
('G19','p3 plan de acțiune','PoC în săptămânile 1–2','Adoptat: căutare vizuală și îmbogățire pe date izolate.','3, 8, 16','Set etalon, relevanță, latență și cost măsurate înainte de extindere.'),
('G20','p3 plan de acțiune','Soft launch BG/HU înainte de RO','Adaptat. Piața/cohorta se alege după date și pregătire, nu automat.','14, 16','Suport, monedă, contracte și traduceri; RO 5% poate fi pilot mai relevant.')]
for k in range(0,len(gemini),5):
    if k==0:page('Recomandări Gemini '+str(k+1)+' până la '+str(min(k+5,len(gemini))))
    else:head('Recomandări Gemini '+str(k+1)+' până la '+str(min(k+5,len(gemini))))
    rows=[]
    for id,loc,topic,decision,where,proof in gemini[k:k+5]:
        rows.append((id+'\n'+loc,topic+'\n'+decision,'§ '+where+'\n'+proof))
    table(['Cod adăugat și localizare','Tratament în versiunea 2','Referință și probă'],rows,[3,7.4,7.1],small=10)

page('Anexa eșantionului intern de catalog')
p('Sursă: exportul din 16 septembrie 2026, citit la 21 octombrie 2026. 50 înregistrări, câte 5 din 10 grupe; selecție deterministă după hashul ID-ului, după încadrarea unică în prima grupă potrivită termenilor din denumire. Produsul de tip variable este inclus prioritar în grupa lui. Grupele sunt de analiză, nu o taxonomie comercială validată. Rândurile nu sunt dovezi de stoc curent sau de conformitate.')
p('Coloana „Lipsuri” privește numai câmpurile SKU, GTIN/EAN, descriere, imagini și greutate în export. „Niciuna din cele 5” nu înseamnă fișă completă. Compatibilitățile și siguranța necesită documente de produs.')
sample_rows=[]
short={'GTIN, UPC, EAN sau ISBN':'GTIN/EAN','Descriere':'descriere','Greutate (kg)':'greutate','Imagini':'imagini','SKU':'SKU'}
for i,x in enumerate(stats['samples'],1):
    sample_rows.append((str(i)+'\n'+x['family'],x['id']+'\n'+(x['sku'] or 'SKU lipsă'),x['name'],', '.join(short[k] for k in x['missing']) or 'Niciuna din cele 5'))
table(['Nr și grupă','ID și SKU','Denumire din export','Lipsuri'],sample_rows,[2.5,4.1,7.3,3.6],small=9.5)

page('Fișa de reevaluare independentă')
p('Propunerea de mai jos este o grilă de verificare pentru auditori, nu un punctaj autoacordat. Fiecare domeniu poate primi 0–1 punct după probele cerute. Totalul de 10/10 este posibil numai dacă evaluatorul confirmă toate criteriile și rezolvarea dependențelor relevante scopului evaluării.')
table(['Domeniu','Condiție pentru punctaj integral'],[
('1 Strategie','Motiv de cumpărare directă, portofoliu coerent și diferențiatori verificabili.'),
('2 Date','Dimensiuni reconciliate, câmpuri, proveniență și destinație pentru toate înregistrările.'),
('3 UX și design','Concepte, mobil, stări, accesibilitate și rezultate de utilizare.'),
('4 Inovare','Funcții cu utilitate, date, etalon, cost și criterii de acceptare.'),
('5 Arhitectură','Reutilizare probată, contracte și separarea corectă a responsabilităților.'),
('6 Comerț și integrări','Preț, stoc, plăți, livrare și facturare reconciliate; excepții acoperite.'),
('7 Legal și securitate','Aplicabilitate verificată și dovezi, fără afirmații legale automate.'),
('8 SEO și conținut','Migrare completă, piețe, traduceri și conținut verificabil.'),
('9 Livrare și cost','Valuri, responsabilități, deviz realist, dependențe și rollback.'),
('10 Rezultate și trasabilitate','Baseline, indicatori, experimente și răspuns la toate punctele de audit.')],[4.3,13.2])
h('Dovezi care nu sunt încă produse de această revizie')
p('D01 curent și D02 comercial, interviuri, prototipuri Figma, PoC AI, teste de încărcare, accesibilitate, plăți, documente de conformitate și aprobările operaționale sunt activități viitoare. Matricea precizează unde sunt cerute și cine le furnizează. Dacă auditorul evaluează numai descrierea proiectului, poate aprecia completitudinea specificației; dacă evaluează sistemul livrat, aceste probe sunt obligatorii.')
p('Concluziile auditorilor se atașează ulterior cu dată, versiune și neconformități rămase. Nu se transformă automat statusul „Adoptat în proiect” în „Rezolvat în sistem”.')
save('Matrice_Raspuns_Audituri_CESIRO_V2.docx')
print('Matrice V2 salvată;',len(seen),'puncte Claude;',len(gemini),'puncte Gemini;',len(groups),'grupuri de răspuns')
