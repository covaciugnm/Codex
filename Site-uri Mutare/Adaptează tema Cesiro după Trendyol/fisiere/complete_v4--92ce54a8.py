from pathlib import Path
import re
O=Path(__file__).parent
s=(O/'build_v4.py').read_text(encoding='utf-8')
def section(start,end,body):
    global s
    a=s.index(start);b=s.index(end,a);s=s[:a]+body.strip()+'\n\n\n'+s[b:]
def para(prefix,new):
    global s
    found=re.findall(r"p\('"+re.escape(prefix)+r"[^\n]*\)",s)
    assert len(found)==1,(prefix,len(found))
    s=s.replace(found[0],'p('+repr(new)+')')

s=s.replace('Migrarea graduală servește aceeași experiență utilizatorilor și roboților din aceeași cohortă; nu folosește cloaking. Monitorizăm zilnic în paginile prioritare, erorile și indexării în primele 30 zile.','Tema nouă păstrează URL-urile; se compară vechea și noua randare pe aceleași adrese. Monitorizăm zilnic erorile și indexarea în primele 30 zile.')
s=re.sub(r'Migrarea graduală servește aceeași experiență utilizatorilor și roboților din aceeași cohortă; nu folosește cloaking\.', 'Schimbarea temei păstrează URL-urile; crawlul compară cele două randări pe aceleași adrese.',s)
para('Portofoliu inițial', 'În primele șase luni se prioritizează 3–4 teste cu efect potențial mare: checkout, configurator, intrare după decor și asistent după activarea E4. Restul ipotezelor rămân în backlog. Se testează disponibilitatea funcției, cu un singur obiectiv primar și fără suprapuneri care împiedică atribuirea.')
section("page('16 Activități", "page('17 Efortul",r'''
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
''')
section("page('17 Efortul", "page('17.2 Devizul",r'''
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
''')
s=s.replace('Mentenanța temei de 750–1.500 EUR/lună este distinctă de operarea backendului, de permanența infrastructurii și de dezvoltarea unor capabilități noi.','Mentenanța temei de 750–1.500 EUR/lună și suplimentul estimat pentru extensii din §17.1 sunt distincte de operarea infrastructurii. Cele 90 zile de garanție se aplică separat fiecărui pachet recepționat.')
s=s.replace("('Copii divergente EVA','Versiuni comune, configurare per tenant, compatibilitate API și migrații pe două configurații.','Lider tehnic')","('Copii divergente EVA','Hashuri locale, commit și digest de producție; migrări E0–E7 și regresie pe ambele teme.','Lider tehnic')")
section("page('18 Recepție", "page('19 Eșantionul",r'''
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
('Citire fără JavaScript','Home, categorie, produs și serie rămân lizibile și navigabile cu JavaScript oprit; insulele adaugă interactivitate.'),
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
table(['Extensie','Prag obligatoriu','Probă'],[
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
''')
section("page('20.1 Surse interne", "page('20.2 Surse legale",r'''
page('20.1 Surse interne și probe de referință')
p('I1 — Audit.Claude.V1.0.docx și Audit.Gemini.v1.0.pdf; I7 — Audit.Claude.V2.0.docx, Audit Tehnic si Directii Arhitecturale CESIRO v2.0.pdf, Audit.Claude.V2.0.Addendum1.docx, Audit.Claude.V3.0.docx și Audit.Claude.V3.0.Addendum1.docx. Toate sunt păstrate în folderul Audituri. A3 are 80 coduri unice: 44 observații și 36 propuneri.')
p('I2 — U:/cesiro.com/backend/requirements.txt și frontend/package.json. I3 — backend/app/factory.py, api/storefront.py, cms.py, gift.py, theme_schedule.py, theme_preview.py, payments/stripe_gateway.py, api/admin/resources/assistant.py și templates/themes/generic/account.html. Citire statică, fără apeluri tranzacționale.')
p('I4 — U:/cesiro.com/wc-product-export-16-9-2026-1789549595309.csv. SHA-256: bbbf54a45baa5dc098b40a7765f7c122ff1179162a0b480e055716407843dbe8. Agregatele și eșantionul de 50 produse din evidence-v2 rămân istorice și reproductibile; nu sunt inventar curent.')
p('I5 — U:/cesiro.com/REGULI.md, citit: nicio anulare/retur/rambursare executată de AI, inclusiv în teste; nicio modificare a comenzilor marketplace. I6 — README, themes/README, manifests, page_contracts, Docker Compose și hashurile din evidence-v4/source-hashes.json. U: mapat la \\\\192.168.100.151\\site-uri; GitHub cesiroproduction/site-uri a returnat 404 prin conexiunea disponibilă la 21 octombrie 2026.')
p('I8 — Z:/images și _RAPORT/index.html: 38.872 fișiere, 38.865 cu extensie de imagine la inventariere. Numărul include posibile duplicate și active neeligibile. Fotografiile planșelor au sursă și hash în evidence-v4/visual-sources.json; clasificarea arhivei nu certifică originea, drepturile sau compatibilitatea produsului.')
p('I9 — U:/acc-florin/app/main.py:1206, anaf_lookup; logică de validare CUI și citire ANAF identificată. Nu au fost citite baze de facturi, setări secrete sau date personale și nu s-a apelat serviciul ANAF.')
for x in [('S1 CESIRO pagina principală','https://cesiro.com/'),('S2 CESIRO sitemap','https://cesiro.com/sitemap.xml'),('S5 CESIRO întrebări frecvente','https://cesiro.com/legal/intrebari-frecvente'),('S6 CESIRO termeni și identitatea vânzătorului','https://cesiro.com/legal/termeni-si-conditii'),('T2 Core Web Vitals','https://web.dev/articles/vitals'),('T3 WCAG 2.2','https://www.w3.org/TR/WCAG22/'),('T4 Google Consent Mode','https://developers.google.com/tag-platform/security/guides/consent'),('T5 Google Search și funcțiile AI','https://developers.google.com/search/docs/appearance/ai-features')]:link(*x)
p('Starea sursei, starea configurației și starea producției sunt distincte. Manifestul local permite repetarea lecturii; commitul și digestul instalat sunt livrabile D01. Lipsa accesului GitHub nu este dovadă că repository-ul nu există.')
''')
s=s.replace("page('20.3 Surse suplimentare pentru cerințele V3')","page('20.3 Surse actualizate pentru V4')")
s=s.replace("('T6 Next.js revalidateTag și expirare','https://nextjs.org/docs/app/api-reference/functions/revalidateTag'),\n",'')
s=s.replace("('L11 ECHA calendarul revizuirii CLP','https://echa.europa.eu/regulations/clp/understanding-clp'),","('L11 Regulamentul 2025/2439 calendarul CLP','https://eur-lex.europa.eu/eli/reg/2025/2439/oj/eng'),")
s=s.replace("('L14 Regulamentul 2026/405 și tranziția detergenților','https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32026R0405'),","('L14 Regulamentul 2026/405 articolul 37','https://eur-lex.europa.eu/eli/reg/2026/405/oj/eng'),")
s=s.replace("('L10 Directiva 2023/2673 și funcția de retragere','https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32023L2673'),","('L10 Directiva 2023/2673 funcția de retragere și aplicarea','https://eur-lex.europa.eu/eli/dir/2023/2673/oj/eng'),")
section("for i,ttl in enumerate(['Atelier", "page('22 Istoricul",r'''
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
''')
section("page('22 Istoricul", "save('Proiect_CESIRO",r'''
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
''')
(O/'build_v4.py').write_text(s,encoding='utf-8')
print('V4 complet pregătit')
