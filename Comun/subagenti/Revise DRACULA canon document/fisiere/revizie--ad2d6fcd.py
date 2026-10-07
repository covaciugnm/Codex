from pathlib import Path
import hashlib, difflib, json, datetime, re
ROOT=Path(r'D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924')
D=ROOT/'00_STUDIO/audit/G0-CANON-v4/REV_IZOLAT_20260924'
P=ROOT/'01_CANON/00_CANON_NUCLEU.md'
baseline=(D/'inainte/00_CANON_NUCLEU.md').read_bytes()
assert hashlib.sha256(baseline).hexdigest()=='eef72462df479ad0d88231aae6b0a9ead3a74df4621c5ceb88cc88961bcabad7'
assert P.read_bytes()==baseline, 'SCRIERE CONCURENTA: oprire fara suprascriere'
s=baseline.decode('utf-8-sig'); changes=[]
def sub(a,b,n=None):
 global s
 count=s.count(a)
 assert count and (n is None or count==n), (a[:90],count,n)
 s=s.replace(a,b); changes.append({'vechi':a,'nou':b,'aparitii':count})
sub('(v4.1, 24.09.2026)','(v4.2, 24.09.2026)',1)
sub('> **Versiunea:** v4.1 · 24.09.2026 · revizia R1 a v4.0', '> **Versiunea:** v4.2 · 24.09.2026 · continuarea izolată a reviziei R1; baza v4.1 (`eef72462…abad7`) și dovezile: `00_STUDIO/audit/G0-CANON-v4/REV_IZOLAT_20260924/`. Nu are încă audit independent. Revizia R1 a v4.0',1)
sub('R7: apele curgătoare mari îi taie zborul și transformarea.','R7: peste apele mari puterile scad la ~50%; scufundat, nu se transformă.',1)
sub('trează ca în fiecare martie (§8)','trează în fereastra obișnuită din martie (§8)',1)
old='Vârsta declarată la începutul unei identități = 45 − durata ei (cel puțin 21 de ani); identitățile de cel mult 12 ani pornesc de la cel mult 33. Vârsta declarată rămâne între 21 și 45; peste 45, numai cu îmbătrânire teatrală completă (tâmple albe, baston, retragere), niciodată peste 50.'
new='Pentru identitățile de peste 12 ani, vârsta inițială = 45 − durata (±1 an calendaristic), minimum 21; cele de cel mult 12 ani pornesc între 21 și 33. Plafonul obișnuit este 45; excepțiile declarate cer tâmple albe, baston și retragere, maximum 50. Durata include retragerea; la identitatea curentă se folosește termenul-limită.'
sub(old,new,2)
sub('Valentin Dragoni (2005–2018, Zürich și Viena)*; 2018–2020: Valentin se retrage, „bolnav”','Valentin Dragoni (2005–2020, Zürich și Viena)*; activ până în 2018, apoi retras, cu tâmple albe și baston',1)
sub('31 → 44 (46 în 2020, retras)','31 → 46 (excepție teatrală; 44 la retragerea din 2018)',1)
sub('Vlad Dragoni (2020–; în acte n. 1993, Viena)','Vlad Dragoni (2020–2038, termen-limită; în acte n. 1993, Viena)*',1)
sub('27 → 33 în 2026 |','27 → 33 în 2026; maximum 45 în 2038 |',1)
sub('revendică baronia adormită din 1679 ca „descendent din colonii”','revendică titlul nerevendicat din 1679 ca „descendent din colonii”; genealogie fictivă, fără a invoca procedura juridică de abeyance',1)
sub('din 1604, cuarțul fumuriu șlefuit la Praga; din 1752, sticla colorată','din 1604, cuarț fumuriu comandat la Praga (invenție BD); din 1752, sticlă colorată aleasă de Casă',1)
sub('din octombrie 1604, ochelari de cuarț fumuriu (precedentul chinezesc *Ai Tai*, secolul al XII-lea), șlefuiți în atelierul de pietre dure al lui Rudolf al II-lea, prinși cu șnur de mătase până la brațele laterale (înainte de 1727), plus pălăria cu boruri largi (vălul, pe drum); din 1752, sticla colorată (Ayscough); din 1929, ochelarii de soare de serie.','din octombrie 1604, ochelari de cuarț fumuriu comandați la Praga: invenție BD, nu produs documentat al unui atelier istoric. Se prind cu șnur; brațele laterale apar în ținutele lui după 1730. Din 1752 Casa alege sticla colorată; din 1929, modele comerciale. Acestea sunt datele garderobei, nu priorități de invenție. Pălăria și vălul completează protecția; §18 separă obiectele atestate de ficțiune.',1)
sub('apoi primii ochelari de cuarț fumuriu, din atelierul lui Ottavio Miseroni (la Praga din 1588), prinși cu șnur de mătase','apoi ochelarii săi de cuarț fumuriu, comandați unui atelier fictiv din Praga, prinși cu șnur de mătase',1)
sub('ochelarii de cuarț fumuriu cu brațe laterale (înainte de 1727)','ochelarii de cuarț fumuriu cu șnur; după 1730, cu brațe laterale',1)
sub('ochelarii cu lentile verzi (Ayscough, 1752)','ochelarii cu lentile verzi (adoptate de Casă în 1752)',1)
sub('din 1929, primii ochelari de soare de serie','din 1929, ochelari de soare comerciali',1)
sub('niciunul: singurul popas fără lux','niciunul: războiul',1)
sub('acceptat: contractul coloanei; cuarț (1604), sticlă colorată (1752), serie (1929)','modificat în v4.2: contract păstrat; anii garderobei nu sunt priorități istorice',1)
sub(' (cuarțul fumuriu *Ai Tai*, secolul al XII-lea)',' (referință secundară; nu atestă comanda fictivă din 1604)',1)
sub(' (Ayscough, 1752; Foster, 1929)',' (cronologia comercială se verifică la muzeul de optică, mai jos)',1)
sub(' (brațele laterale, înainte de 1727)',' (brațele laterale: secolul XVIII)',1)
sub('și nu intră nicăieri fără invitație sau mandat','și nu intră într-o locuință privată fără invitație sau mandat',1)
sub('el nu folosește Privirea și nici Criptele în anchetele ei fără acordul ei (excepția: clipa primejdiei, art. 7)','Privirea asupra altor oameni cere acordul lor și al Ioanei, cu excepția art. 7; asupra Ioanei rămâne interzisă (R3). Criptele pot sprijini legal analiza, cu acordul ei; acordul nu permite acces ilegal la datele anchetei (R9)',1)
sub('Criptele ating numai datele de identitate ale familiei (§4).','Intervențiile ilegale ale Criptelor se limitează la datele de identitate ale familiei (§4); analiza legală a datelor autorizate rămâne permisă.',1)
sub('Criptele nu ating nicio altă bază de date (R9).','Criptele nu modifică și nu accesează ilegal alte baze de date (R9).',1)
sub('Hanzerul ramurii din Viena**, emigrat după Anexarea din 1938, care îl urmează la Hollywood, la Londra și în exil și reaprinde inelul între 1947 și 1989.','însoțitorul din ramura vieneză**, refugiat în 1938, apoi succesorii lui: o succesiune de oameni, nu un singur slujitor presupus activ 51 de ani. Ei asigură reaprinderile din exil; numele și mandatele se aliniază la G1.',1)
sub('Între 1938 și 1989 (războiul, apoi Cortina de Fier), când Hanzerii din Transilvania nu pot ieși din țară, rolul îl are','Între 1938 și 1989, în ficțiunea familiei, rolul îl preia',1)
sub('din 1611, un Hanzer îl însoțește în fiecare popas (§8).','din 1611, un Hanzer îl însoțește, cu excepția frontului din 1915–1916 (§8).',1)
sub('după aniversarea de 550 de ani (§12).','la aniversarea familială (§12). **Intervalul de stingere:** dacă termenul e ratat, puterile de zi scad treptat până la 27 ianuarie 2027; finalul nu îl tratează ca stingere instantanee.',1)
sub('*(Notă pentru pedanți: aniversarea se ține după data din calendarul iulian al epocii, ca în tradiția familiei.)*','Familia păstrează convențional ziua și luna în calendarul civil actual; nu este conversia astronomică a datei iuliene (§3.1).',1)
sub('în noaptea de 26 spre 27 decembrie 2026 se împlinesc 550 de ani de la transformare','în noaptea de 26 spre 27 decembrie 2026 familia celebrează 550 de ani de la transformare',1)
sub('**Regula tranșelor (OBS-7):** povestirea Ep. 1 se publică integral la lansare; de la Ep. 2, povestirea apare în 4 tranșe săptămânale; tranșele 1–3 pot preceda BD-ul, fără vinovat, soluție, răsturnare sau cârlig final; tranșa 4 apare în ziua BD-ului sau după.','**Regula tranșelor (OBS-7, OBS-8):** Ep. 1 se publică integral la lansare; apoi, de regulă, 4 tranșe săptămânale. Ultima apare în ziua BD-ului sau după; cele anterioare nu divulgă vinovatul, soluția, răsturnarea ori finalul. Tranșele Ep. n+1 apărute înaintea BD-ului Ep. n nu divulgă nimic din Ep. n. După pivoturile 1, 5, 10 și 15, prima tranșă următoare apare cel mai devreme în prima zi lucrătoare după BD. Ep. 11 și 16 au 3 tranșe; aceleași restricții se aplică primelor două și ultimei. Ritmul final: Producătorul, 13.11.2026.',1)
sub('sunt compatibile cu toate ipotezele.','cer alinierea documentului C la prezentul canon. Verificarea v4.2 nu confirmă compatibilitatea integrală a versiunii C încă aliniate la v3.0; aceasta nu autorizează abateri de la R3, cronologie sau pivoturi.',1)
sub('reverificată de Showrunner pentru v4.1 (24.09.2026):','nota moștenită din v4.1 este corectată la 24.09.2026:',1)
sub('Statusurile juridice sunt o verificare din 24.09.2026, de confirmat de H1; nu țin loc de aviz juridic.','Reguli editoriale interne. Datele juridice sunt orientative, cu surse în §18; aplicarea pe teritoriu și material cere avizul H1.',1)
start=s.index('2. **Statusul juridic al filmului din 1931**'); end=s.index('\n3. **Galeria Hollywood**',start)
sub(s[start:end],'2. **Filmul din 1931:** calculul SUA de 95 de ani indică 01.01.2027, sub rezerva verificării ediției și drepturilor subiacente (17 USC §§304–305). În UE, H1 aplică art. 2 alin. (2), art. 7 și art. 8 din Directiva 2006/116/CE, inclusiv tratatele relevante; nu există aici o autorizare generală din 2027. California Civil Code §3344.1 stabilește limita de 70 de ani după deces; calculul pentru Lugosi nu înlocuiește verificarea titularilor și a celorlalte jurisdicții. Regula 1 rămâne obligatorie.',1)
sub('riscul: juridic scăzut (personaj pozitiv, unitate fictivă, altă vârstă și profesie), de căutare mediu.','evaluarea editorială preliminară: confuzie de căutare posibilă; nivelul riscului juridic îl stabilește H1.',1)
sub('monumentele se desenează liber în interior.','reprezentarea monumentelor se verifică după teritoriul și utilizarea concretă, inclusiv în interiorul BD-ului.',1)
sub('Producătorul (propunerea: Showrunnerul, raportul S; verificarea: B, apoi H1)','Producătorul (propunerea: raportul separat al reviziei v4.2; verificarea: B, apoi H1)',1)
sub('Corespondența jurnal → registru: E.6 din `00_STUDIO/audit/G0-CANON-v4/R1_plan_masuri.md`.','Dovezile reviziei v4.2: `00_STUDIO/audit/G0-CANON-v4/REV_IZOLAT_20260924/RAPORT_REVIZIE.md`.',1)
sub('| AR-16 | raportul Showrunnerului | acceptat: un singur raport, `S_showrunner.md` | păstrat |','| AR-16 | raportul Showrunnerului | acceptat: un singur raport, `S_showrunner.md` | v4.2: raport separat, conform instrucțiunii utilizatorului; integrarea aparține Studio |',1)
rows='''| V4-83 | OBS-8, jurnal §5.5 | protecția pivoturilor în foileton | acceptat: 3 tranșe la Ep. 11 și 16; ultima după BD | §12 | Studio, D3–D6, F2 | G1 |
| V4-84 | revizia izolată; M1.3–4, M1.37 | datele ochelarilor; vârstele; rezumatele R7/R9; Hanzerii | modificat: ficțiunea separată de istorie; excepții explicite | §2, §4–§9, §19 | B, C, E | G1 |
| V4-85 | M1.24, M1.28, M1.37 | compatibilitate C, aniversare, stingerea inelului | modificat: alinierea C rămâne necesară; calendar civil; stingere progresivă | §6, §10, §12 | C, D1, Studio | G1–G2 |
| V4-86 | M1.5–6, M1.17, M1.34–39; instrucțiunea utilizatorului | drepturi și dovezi | modificat: surse primare; raport separat; copie stabilă pentru audit | §14, §18; dosarul reviziei | H1, Studio, auditori | înaintea publicării |
'''
sub('\n### 16.2 Deciziile anterioare','\n'+rows+'\n### 16.2 Deciziile anterioare',1)
sub('\n## 18. Surse de verificare','\n| **v4.2** | 24.09.2026 | continuare izolată; V4-83…V4-86; fără revendicarea corecturilor v4.1 preexistente | raportul separat din REV_IZOLAT_20260924 | mandatul utilizatorului; audit independent încă necesar |\n\n## 18. Surse de verificare',1)
sub('> Verificate la 24.09.2026. Pentru zona blocată 1431–1476, lucrările academice de mai jos sunt referința primară, iar paginile web, trimiterea secundară, ușor de verificat de echipe.','> Bibliografie de lucru, nu certificare integrală. Lucrările academice sunt studii secundare; sursele contemporane și obiectele digitizate sunt primare. Rezultatele accesării URL-urilor și limitele verificării se arhivează separat.',1)
sources='''
**Verificări punctuale v4.2 (24.09.2026):**
- Optică: muzeul profesional documentează brațele în secolul XVIII și ochelari comercializați înainte de 1929; nu atestă invenția BD din 1604: https://www.college-optometrists.org/the-british-optical-association-museum/the-history-of-spectacles · https://www.college-optometrists.org/the-british-optical-association-museum/history-fashion-sunglasses
- Drepturi, texte oficiale: https://www.copyright.gov/title17/92chap3.html · https://eur-lex.europa.eu/legal-content/RO/TXT/?uri=CELEX:32006L0116 · https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=3344.1.&lawCode=CIV
- Cetățenia din §2 este biografie fictivă: aprobarea austriacă prealabilă nu dovedește singură eligibilitatea română; H1 verifică dosarul și temeiurile: https://www.ris.bka.gv.at/eli/bgbl/1985/311/P28/NOR40205579
'''
sub('\n## 19. Glosar','\n'+sources+'\n## 19. Glosar',1)
# Fără rescrierea regulilor pentru a forța bugetul: scurtăm trimiteri bibliografice redundante.
sub('**Lucrări academice de referință (§3, §3.1, §8, §10):**','**Studii (§3, §3.1, §8, §10):**',1)
sub(' (Leiden: Brill, 2017)',' (2017)',1); sub(' (Iași: Center for Romanian Studies, 2000)',' (2000)',1)
sub(' (Boston: Little, Brown, 1989)',' (1989)',1); sub(' (București: Editura Enciclopedică, 2001)',' (2001)',1)
out=s.encode('utf-8')
assert P.read_bytes()==baseline, 'SCRIERE CONCURENTA la commit'
P.write_bytes(out)
(D/'modificari_proprii.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'diff_propriu.patch').write_text(''.join(difflib.unified_diff(baseline.decode('utf-8-sig').splitlines(True),s.splitlines(True),fromfile='baza_izolata_eef72462',tofile='canon_v4.2')),encoding='utf-8')
print(json.dumps({'modificari':len(changes),'cuvinte':len(s.split()),'sha256':hashlib.sha256(out).hexdigest()},ensure_ascii=False))
