from pathlib import Path
import re,json,hashlib,datetime,csv,difflib,collections
R=Path(r'D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924');D=Path(__file__).resolve().parent;P=R/'01_CANON/00_CANON_NUCLEU.md';s=P.read_text(encoding='utf-8');lines=s.splitlines()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,t): (D/name).write_text(t,encoding='utf-8',newline='\n')
def loc(needle):
 hits=[str(i) for i,l in enumerate(lines,1) if needle in l]
 return 'r. '+', '.join(hits[:8]) if hits else 'NU GĂSIT'
sections={m[1]:loc(m[0]) for m in re.finditer(r'^## (\d+)\. .+$',s,re.M)}
evidence={
1:('închis, bază nouă','inainte/00_CANON_NUCLEU.md; SHA256SUMS.txt'),
2:('închis în canon; aliniere C necesară','§8; '+loc('Trezirile extraordinare canonice')),
3:('corectat','§2, §5.2; VC22; surse optică în §18; anii garderobei nu sunt atestări'),
4:('corectat','§4/§19; VC8/23/24; identitati.json (32 de identități)'),
5:('implementat; H1 deschis','§5.2/§14; VC25; numele trenurilor sunt propuneri fictive, nu mărci declarate disponibile'),
6:('implementat; decizia Producătorului și H1 deschise','§14; cautari_nume.json; propunerea din raport; numele blocat păstrat'),
7:('preexistent, verificat','§5.2/§6; '+loc('R6 ·')),
8:('preexistent, verificat','§6/§7/§19; '+loc('trei săptămâni')),
9:('completat','§5.1/§8; VC28; ramura vieneză și succesorii; excepția 1915–1916'),
10:('preexistent, verificat','§2/§6/§13; VC20'),
11:('preexistent, verificat','§5.1/§8; VC29'),
12:('preexistent, verificat','§5/§5.1/§5.2; V4-54; venituri japoneze donate, portofolii externe păstrate'),
13:('completat','§6 R7 și fișa rapidă; Canalul Mânecii este excepție canonică, nu afirmație hidrologică'),
14:('preexistent, verificat','§2/§7/§8/§15; neutralizare fără ucidere în prezent'),
15:('preexistent, verificat','§8/§11: sicriu fără trup; Oradea: încă un mormânt gol'),
16:('preexistent, verificat','§3/§5/§10/§14/§18: ediții Ayrer/Wagner distincte; Lübeck disputat'),
17:('executat cu excepții de acces','stare_url.json/txt; toate URL-urile încercate; răspunsurile HTTP nu certifică faptele'),
18:('preexistent, verificat','§5/§5.1; VC1/27; identitati.json; Virgilio Dal Drago și Victorin'),
19:('precizat','§4/§5.1: primul/al doilea/al treilea baron; genealogie fictivă, fără echivalarea abeyance cu titlu nerevendicat'),
20:('preexistent, verificat','§5/§5.1: cetățean elvețian în 1914; detaliul opțional al Cisternei neadoptat, V4-62'),
21:('preexistent, verificat','§7 art. 4; §13; VC40'),
22:('completat','clisee_24.md; §5: obiectivul există la data scenei; §14'),
23:('preexistent, verificat','§15; R3; VC38; documentul C necesită aliniere fără divulgarea ipotezelor'),
24:('corectat; aliniere C deschisă','§10: eliminată certificarea nejustificată a compatibilității integrale; pista inelului păstrată'),
25:('preexistent, verificat','§5.2; VC35: cinci vehicule feroviare de lux'),
26:('preexistent plus condensare','§1; VC11: 44 cuvinte; caz/poliție, zi, glamour, antagonist'),
27:('preexistent, verificat','§10: covor respectat, origini multiple, Istanbul luminos'),
28:('precizat','§12: cele trei date; aniversare civilă convențională; R4 păstrează luna de stingere'),
29:('preexistent, verificat','§12: cinci elemente și ancore ale arcului interior'),
30:('completat','§12; VC34; OBS-8/OBS-10; pagina 4 artă nouă, 28/32 pagini'),
31:('preexistent, verificat','antet 15/15; VC31; V4-78'),
32:('completat','§16: V4-83…V4-87; corespondenta_jurnal.md; jurnalul rămâne la Studio'),
33:('livrat separat','avizul de aliniere din RAPORT_REVIZIE.md; VC37'),
34:('livrat separat conform mandatului','RAPORT_REVIZIE.md; tabel 15 decizii și KPI K1–K13; S_showrunner.md neatins'),
35:('închis','VC33; 24.971 cuvinte; fișa rapidă 279; ghid 11 echipe'),
36:('verificări executate','VC3/36; glosar §19; limita verificării lexicale declarată'),
37:('parțial: autoverificare, nu certificare independentă','scan_absolut.csv; cine_stie.md; corecții R7/R9, calendar, vârste; alinierea C și K1 global rămân la AU-C'),
38:('executat, limite declarate','verifica.py; rezultat_verificari.json/txt; verificările semantice nu sunt simulate printr-un PASS automat'),
39:('închis în scopul autorului','predat/; SHA256SUMS.txt; MANIFEST.json; raport separat; registrul central exclus')}
plan=(R/'00_STUDIO/audit/G0-CANON-v4/R1_plan_masuri.md').read_text(encoding='utf-8-sig')
tasks={int(m[1]):m[2] for m in re.finditer(r'^\| \*\*M1\.(\d+)\*\* \| (.*?) \| Showrunner',plan,re.M)}
mt=['# Execuția celor 39 de măsuri','', 'Stările sunt ale autorului; „preexistent” nu înseamnă implementat de această revizie. Coloana dovadă indică versiunea v4.2.','', '| Măsura | Stare | Dovadă |','|---|---|---|']
for n,(status,ev) in evidence.items(): mt.append(f'| M1.{n} | {status} | {ev} |')
write('MASURI_39.md','\n'.join(mt)+'\n')
# Defectele au corespondența din plan, fără reclasificări sau punctaje inventate.
mapping={
'AC-m1':[2,28],'AC-m2':[3],'AC-m3':[7],'AC-m4':[16],'AC-m5':[8],'AC-m6':[8],'AC-m7':[11],'AC-m8':[19],'AC-m9':[21],'AC-m10':[15],'AC-m11':[23],'AC-m12':[5],'AC-m13':[33],
'AC-c1':[36],'AC-c2':[17],'AC-c3':[14],'AC-c4':[13],'AC-c5':[4],'AC-c6':[32],
'AC-O1':[20],'AC-O2':[20],'AC-O3':[24],
'AM-1':[5],'AM-2':[2],'AM-3':[6],'AM-4':[4],'AM-5':[23],'AM-6':[3],'AM-7':[9],'AM-8':[24],'AM-9':[25],'AM-10':[12],'AM-11':[28],'AM-12':[29],'AM-13':[30],'AM-14':[5],'AM-15':[21],'AM-16':[22],'AM-17':[13],'AM-18':[11],'AM-19':[26],'AM-20':[26],'AM-21':[35],'AM-22':[10],'AM-23':[14],'AM-24':[4],'AM-25':[27],
'AK-1':[3],'AK-2':[32],'AK-3':[34],'AK-4':[12],'AK-5':[10],'AK-6':[2],'AK-7':[9],'AK-8':[30],'AK-9':[17],'AK-10':[18],'AK-11':[32],'AK-12':[11],'AK-13':[31,14,36],
'AK-O1':[31],'AK-O2':[39],'AK-O3':[35],'AK-O4':[34]}
out=['# Defect → măsură → dovadă','','57 defecte și 7 observații; nu este o nouă notare.','', '| ID | Măsuri | Rânduri V4 și dovezi |','|---|---|---|']
for id,nums in mapping.items():
 vr=[re.match(r'\| (V4-\d+)',l)[1] for l in lines if re.match(r'\| V4-\d+',l) and re.search(r'(?<![\w-])'+re.escape(id)+r'(?!\d)',l)]
 out.append(f"| {id} | {', '.join('M1.'+str(n) for n in nums)} | {', '.join(vr) or 'Raport separat / măsură de verificare'}; {'; '.join(evidence[n][1] for n in nums)} |")
assert len(mapping)==64
write('DEFECTE_64.md','\n'.join(out)+'\n')
films=[('Dracula',1931,'vampirul și mormântul'),('Casino Royale',2006,'Veneția, identități și urmărire'),('Angels & Demons',2009,'arhive și conspirație romană'),('From Russia with Love',1963,'Istanbul și cisterna'),('The Illusionist',2006,'iluzionistul central-european; nu atestare a Golemului'),('The Three Musketeers',1973,'muschetarii'),('Forever Amber',1947,'Londra, ciuma și incendiul'),('The Lord of the Rings: The Two Towers',2002,'asediul; analogie de mecanism, nu istorie'),('Anastasia',1956,'curtea rusă și identitatea'),('The Scarlet Pimpernel',1934,'salvatorul mascat'),('The Mummy',1999,'egiptologul'),('The Emperor Waltz',1948,'balul imperial'),('Sherlock Holmes',2009,'detectivul londonez'),('Murder on the Orient Express',1974,'crima din tren; fără soluția filmului'),('1917',2019,'misiunea din tranșee'),('The Great Gatsby',2013,'jazz și bogăție'),('Sunset Boulevard',1950,'mitologia Hollywoodului'),('The Longest Day',1962,'Rezistența'),('To Catch a Thief',1955,'hoțul elegant pe Riviera'),('The Spy Who Came in from the Cold',1965,'spionul și Berlinul'),('Interview with the Vampire',1994,'vampirul în sudul american'),('The Bourne Identity',2002,'străinul fără identitate'),('The Thomas Crown Affair',1999,'financiarul misterios'),('Bram Stoker’s Dracula',1992,'castelul transilvănean')]
write('clisee_24.md','# Repere cinematografice interne — 24/24\n\nSelecție editorială, nu surse pentru adevărul istoric al scenelor; nu se preiau personaje, soluții sau cadre. Anul filmului nu este anul popasului. Pentru #5 și #8 se compară mecanismul, nu geografia.\n\n| Popas | Film | An | Mecanism |\n|---|---|---|---|\n'+'\n'.join(f'| {i} | {f} | {y} | {v} |' for i,(f,y,v) in enumerate(films,1))+'\n\nVerificări de catalog punctuale: [Forever Amber](https://catalog.afi.com/Film/25169-FOREVER-AMBER), [The Emperor Waltz](https://catalog.afi.com/Film/25528-THE-EMPEROR-WALTZ). Celelalte sunt repere de lucru pentru AU-M, nu o cercetare filmografică exhaustivă.\n')
write('cine_stie.md','''# Cine știe ce și când — relectură de autor

| Personaj | Înainte de Ep. 10 | După Ep. 10 / limită |
|---|---|---|
| Ioana | identitatea civilă; indiciile nu sunt confirmare | află natura lui; poate dărui pentru R4; R3 nu admite excepție pentru ea |
| Irina | bănuiește din Ep. 1, ADN imposibil și dâre | canonul nu fixează confirmarea; nu se presupune eligibilă pentru R4 |
| Tudor | remarcă dâra înainte de Ep. 10 | nu are revelație fixată; nu devine donator informat prin presupunere |
| Iosif | știe natura lui; reaprinde în 2019 | donator informat; boala propusă rămâne amânată |
| Ilinca | cunoaște Casa și Criptele | nemuritoare; R4 cere sângele unui om |
| Sânziana | cunoaște transformarea și propria judecată | separată din 1794; nu este soția prezentului |
| Mihnea | știe din 1510 | exilat; inel confiscat; nu e donator uman |
| Buna Dochia | cunoaște Sângele și legea Casei | accesul la oracol este limitat de somn și cost |

Vlad află judecata Sânzianei în Ep. 15–20, de la Radu; nu i se atribuie această cunoaștere în Ep. 1. Scenele și răspunsul la stingerea progresivă: D1.
''')
# Inventar literal: nu atribuim unui program capacitatea de a confirma adevărul semantic.
with (D/'scan_absolut.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['rand','sectiune','termen','context','metoda']);section=0
 for i,l in enumerate(lines,1):
  m=re.match(r'## (\d+)\.',l)
  if m:section=int(m[1])
  if section in list(range(1,16))+[19,20]:
   for m in re.finditer(r'\b(?:singur\w*|numai|doar|niciodată|nicăieri|primul|toate)\b|nu .{0,60}?niciun',l,re.I):w.writerow([i,section,m[0],l,'inventar automat; nu verdict semantic'])
# Matricea jurnalului păstrează intrările istorice fără a pretinde modificarea lor.
j=(R/'00_STUDIO/03_JURNAL_PROGRES.md').read_text(encoding='utf-8-sig');j5=j.split('## 5.',1)[1].split('## 6.',1)[0]
jrows=[]
for l in j5.splitlines():
 if not l.startswith('|'):continue
 first=l.split('|')[1].strip()
 if re.fullmatch(r'(?:B-[ABC]\d+|C-P\d+|A-\d+|SR-\d+|DP-\d+|OBS-\d+|AUD-\d+|REG-1)',first):
  refs=re.findall(r'V4-\d+|§16 [A-Z]+-?\d+',l)
  direct=[re.match(r'\| ([^|]+)',x)[1].strip() for x in lines if x.startswith('|') and first in x and 'V4-' in x]
  jrows.append((first, ', '.join(direct or refs) or 'decizie istorică din jurnal; vezi §16.2 și matricea defectelor'))
write('corespondenta_jurnal.md','# Corespondența jurnal → canon\n\nExtracție a rândurilor individuale din §5 al jurnalului citit la predare; nu transformă referințele istorice în decizii noi. OBS-8 → V4-83; OBS-10 → V4-87. Intrările compuse și intervalele necesită lectura auditorului; K5 global nu este declarat 100%.\n\n| ID | Trimitere |\n|---|---|\n'+'\n'.join('| '+a+' | '+b+' |' for a,b in jrows)+'\n')
payload=json.loads((D/'rezultat_verificari.json').read_text(encoding='utf-8'));http=json.loads((D/'stare_url.json').read_text(encoding='utf-8'))
report=f'''# Raport separat de revizie — G0-CANON-v4, v4.2

Data UTC a generării: {now}. Autor: agentul de revizie Codex din această sarcină. Nu este raport de auditor și nu conține o notă. Niciun agent nou nu a fost lansat.

## E.1 Livrabilul și starea auditului

Canon: `{P}`. SHA-256: `{sha(P)}`. Versiune: v4.2. Copie stabilă: `predat/00_CANON_NUCLEU.md`; manifest: `MANIFEST.json`, `SHA256SUMS.txt`. Aceleași octeți trebuie folosiți de toți cei trei auditori. Orice corectură ulterioară cere alt instantaneu; nu se auditează un fișier aflat în scriere.

Ultimele rapoarte independente găsite în dosarul propriu sunt R1: AU-C 9,31, AU-M 8,70, AU-K 8,70, pe v4.0. Nu se transferă la v4.2. Poarta de 9,50 de la fiecare auditor nu este trecută și nu este revendicată.

## E.2 Măsurile și atribuirea

`MASURI_39.md`: 39/39 măsuri inventariate cu stări și dovezi. `DEFECTE_64.md`: 57 defecte + 7 observații. Baza izolată era deja v4.1; majoritatea corecturilor R1 existau înaintea acestei sarcini. Nu le revendic ca implementări proprii. `diff_propriu.patch` este dovada exhaustivă a contribuției mele; `modificari_proprii.json` descrie prima etapă, iar diff-ul final include și condensarea, OBS-10 și corecturile ulterioare.

## E.3 Integritatea bazei

Baza izolată, exactă: `inainte/00_CANON_NUCLEU.md`, SHA-256 `eef72462df479ad0d88231aae6b0a9ead3a74df4621c5ceb88cc88961bcabad7`. Diferă de prima captură din original (`f553eb7d…bfcd8`) și de captura concurentă (`f9c6a3e2…62434`). Copiile acestora se află în dosarul anterior copiat `REV_20260924_120416/inainte/`. Diferențele sunt arhivate separat; nu sunt atribuite acestei revizii. Originalul nu a fost scris. Nu s-a găsit AGENTS.md în proiect ori în directoarele părinte verificate; AGENTS.md din profilul Codex era gol.

## E.4 Verificări reale

`verifica.py` și `verifica_url.py` folosesc numai rădăcina izolată. Nu am rulat scriptul R0 cu rădăcina originală. Scriptul R0 moștenit avea verificări lexicale și un prag vechi de 40 de cuvinte; verificatorul nou păstrează obiectivele structurale și explică limitele, fără a simula audit semantic.

Rezultate: {dict(collections.Counter(x['result'] for x in payload['teste']))}. Erori raportate: {payload['ERORI']}. Textul are {len(s.split())} cuvinte. URL-uri: {len(http)}, distribuție {dict(collections.Counter(str(x['status']) for x in http))}. Accesul 202/302/403 sau o eroare de server nu certifică o sursă. Fișierele `stare_url*` păstrează încercările și excepțiile. Rezultatul structural se rerulează pe copia predată și se compară; HTTP este observație datată, nu rezultat reproductibil garantat.

## E.5 Trasabilitate și decizii blocate

Matricea defectelor: `DEFECTE_64.md`. Deciziile rămân 15; numele Ioana Mureșan rămâne blocat. Titlul DRACULA, eroul de zi, moda și glamourul Bond, burlăcia prezentului și despărțirea Paris 1794 sunt păstrate.

| Decizie | Aplicare în canon | Locație |
|---|---|---|
'''
dec_sections={1:2,2:3,3:8,4:5,5:2,6:19,7:17,8:1,9:13,10:6,11:5,12:20,13:8,14:20,15:8}
for n,k in dec_sections.items():report+=f'| {n} | §{k}; rezumatul deciziei din antet păstrat | {sections[str(k)]} |\n'
report+='''
## E.6 Relectură, cercetare și KPI

32 de identități și vârste calculate: `identitati.json`. Repere cinematografice: `clisee_24.md`. Informația personajelor: `cine_stie.md`. Scanarea tuturor absolutelor: `scan_absolut.csv` (inventar, nu certificare semantică automată). Cuvinte pe secțiuni: `rezultat_verificari.json`.

Corecții proprii: excepția Valentin la 46 de ani, termenul identității curente 2038, formula identică §4/§19; R7 în fișa rapidă; R9 și Protocolul Mureșan; excepția Hanzer 1915–1916 și succesorii ramurii vieneze; ochelarii din 1604 ca invenție BD, fără atestare falsă a atelierului; eliminarea priorității false din 1929; aniversarea civilă, păstrând conversia iuliană în §3.1; stingerea progresivă în R4; OBS-8 și OBS-10 acceptate. Nota confidențială nu mai certifică impropriu compatibilitatea tuturor ipotezelor C.

Surse consultate punctual: [muzeul de optică — ochelari de soare](https://www.college-optometrists.org/the-british-optical-association-museum/history-fashion-sunglasses), [construcția ochelarilor](https://www.college-optometrists.org/the-british-optical-association-museum/the-history-of-spectacles), [17 USC, capitolul 3](https://www.copyright.gov/title17/92chap3.html), [Directiva 2006/116/CE](https://eur-lex.europa.eu/legal-content/RO/TXT/?uri=CELEX:32006L0116), [California §3344.1](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=3344.1.&lawCode=CIV), [hotărârea austriacă din 15.05.2019](https://www.ris.bka.gv.at/Dokumente/Vwgh/JWT_2018010076_20190515L00/JWT_2018010076_20190515L00.pdf). Sursele legale stabilesc reguli generale, nu un aviz pentru fiecare material DRACULA. Muzeul nu confirmă perechea fictivă de ochelari din 1604.

**Propunerea M1.6 către Producător:** păstrarea numelui blocat până la decizia explicită. Dacă dorește redenumire, variante de lucru: Ioana Vetriceanu, Ioana Brădetu, Ioana Sălceanu. Interogări exacte cu domeniile Wikipedia, portal.just.ro și politiaromana.ro: `cautari_nume.json`. Rezultatele vizibile pentru Sălceanu sunt potriviri de termeni separați, nu dovada unei identități exacte; nu declarăm numele liber ori rar statistic. Corbeanu a fost abandonat la prefiltrare după o potrivire nominală în indexul portalului. B și H1 verifică variantele și grafiile fără diacritice înaintea deciziei din 02.10.2026. Pentru tren, căutarea „L’Express des Deux Empires” a produs rezultate lexicale nespecifice; nu dovedește disponibilitatea unei mărci. Numele trenurilor rămân provizorii până la H1.

| KPI S (fișa curentă K1–K13) | Măsurare / limită |
|---|---|
| K1 | Cele 15 decizii păstrate; neconcordanțele interne de mai sus corectate. K1 global nu este declarat 0: documentele B/C/Studio trebuie sincronizate și AU-C măsoară. |
| K2 | Brief-urile nu sunt livrabilul acestei revizii; Studio. |
| K3 | Intrarea pentru jurnal este propusă în E.9; jurnalul nu a fost scris. |
| K4 | Planul R1 existent; fără ședință nouă inventată. |
| K5 | Corespondență în corespondenta_jurnal.md; OBS-8 și OBS-10 decise. Actualizarea jurnalului și termenul global de 48 h: Studio. |
| K6 | Dovezile acestei revizii arhivate; trei rapoarte independente noi încă lipsesc. |
| K7 | Media rundelor nu se calculează pe acest singur livrabil; registrul aparține părintelui. |
| K8 | Mandatul utilizatorului și contrasemnarea generală existente; nu sunt transformate în aprobare editorială nouă. |
| K9 | Căutare normalizată în canon, cu martori pozitivi, VC1/27: 0 urme interzise. Alte documente nu sunt certificate aici. |
| K10 | Buletinele săptămânale: în afara scopului. |
| K11 | Nicio procedură de audit v5 executată; doar verificări de autor. |
| K12 | Mediana AU-M pe livrabile creative nu este încă măsurabilă aici. |
| K13 | Măsurătorile de audiență: etapă ulterioară; nu se inventează date. |

## E.7 Diferențe și aviz de aliniere

`diff_propriu.patch` separă strict contribuția de baza izolată. Condensarea prezentării și a trimiterilor bibliografice redundante păstrează §1–§20 și registrul istoric integrat. Nu au fost modificate documente ale altor autori.

| Destinatar / cale relativă rădăcinii izolate | Măsura concretă |
|---|---|
| Studio: 00_STUDIO/01_ECHIPA_SI_ROADMAP.md; 03_JURNAL_PROGRES.md; rapoarte/S_showrunner.md | Sincronizare numai după această predare; v4.2 și amprenta E.1; OBS-8 → V4-83, OBS-10 → V4-87; fără atribuire retroactivă. |
| C: 04_LUME/02_REGULILE_NOPTII.md | Opt elemente R1: titlul eliminat; antetul vechi; numele galeriei; numele medicului; art. 1; veto după 1794 și sentința incompatibilă; puterile de zi; propunere de nume de fișier. În plus: R7/R9, cele 7 pietre, stingerea și Hanzerii. |
| C: 04_LUME/01_CRONOLOGIE_SECOLE.md; 06_TRASEUL_CAPITALELOR.md | Virgilio Dal Drago, vârstele, Dochia și prețul trezirilor, rolurile Hanzer, mormântul Mihnea, ochelarii și data scenei. |
| C: documentul confidențial | Aliniere la v4.2, R3 și pivoturi; nota de compatibilitate integrală este retrasă. Nicio ipoteză nu este divulgată aici. |
| B: 03_PERSONAJE/02_FAMILIA_DRACULESTI.md | Reconcilierea Konrad/Georg/Andreas, succesorii vienezi, somnul Dochiei, statutul Sânzianei; verificarea numelor. |
| E: 05_ART/ | Ochelarii (ficțiune/atestare), paleta de zi, un accent de culoare, pagina 4 cu artă nouă, trenurile fictive cu H1. |
| A: 02_RESEARCH/; F1: 09_SITE/ | Loglinia de 44 de cuvinte, comparabilele, separarea informației interne de materialul public. |
| D1 și D3–D6 | OBS-8/OBS-10, cele trei date fixe, luna de stingere, arcul interior, pista inelului; fără romantism Ioana în S1. |

## E.8 Abateri explicite și restanțe

Instrucțiunea utilizatorului prevalează asupra planului: nu se editează S_showrunner, jurnalul, registrul central sau alte documente; raportul de față înlocuiește execuția în acele fișiere. Planul R1 și auditurile vechi nu au fost rescrise. M1.1 este reluat pe baza exactă izolată, nu pe hash-ul istoric v4.0. Arhiva R0 rămâne intactă: nota ulterioară de reconstituire bit-cu-bit depășește afirmația mai veche că reconstituirea nu era posibilă; această revizie nu rescrie retrospectiv acele note.

Rămân: trei auditori independenți pe aceeași copie; verificarea semantică integrală a absolutelor și istoriei (M1.37); alinierea documentului C și a celorlalte documente la G1; avizele H1, decizia asupra numelui și confirmarea disponibilității mărcilor; accesul la sursele cu răspuns neconcludent. Aceste limite sunt vizibile și nu primesc închideri sau note fictive. Nu s-au inventat ședințe, date de piață ori rezultate de audit.

## E.9 Predare către părinte

Intrare propusă: „Canon v4.2 revizuit în copia izolată, pe baza eef72462…abad7. OBS-8 și OBS-10 acceptate; raport separat, copie stabilă și manifest în REV_IZOLAT_20260924. Urmează trei auditori independenți; poarta rămâne nepromovată.”

Părintele deține registrul. Studio integrează raportul după sincronizare. Autorul canonului a scris numai 01_CANON/00_CANON_NUCLEU.md și propriul dosar REV_IZOLAT_20260924. Nu va modifica copia predată pe durata auditului.
'''
write('RAPORT_REVIZIE.md',report)
base=(D/'inainte/00_CANON_NUCLEU.md').read_text(encoding='utf-8-sig')
write('diff_propriu.patch',''.join(difflib.unified_diff(base.splitlines(True),s.splitlines(True),fromfile='baza_izolata_eef72462',tofile='canon_v4.2')))
prior=R/'00_STUDIO/audit/G0-CANON-v4/REV_20260924_120416/inainte'
for p in prior.glob('*.md'):
 old=p.read_text(encoding='utf-8-sig');write('diff_baza_vs_'+p.stem+'.patch',''.join(difflib.unified_diff(old.splitlines(True),base.splitlines(True),fromfile=p.name,tofile='baza_izolata')))
print('Dovezi: 39 măsuri, 64 constatări, 24 repere,',len(jrows),'rânduri jurnal individuale.')
