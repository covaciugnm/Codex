# SEL-001 — rezultate de implementare r02_staging

Autor de lucru: P-CANON. Data: 24.09.2026, Europe/Bucharest. Obiect: anexă de selecție preliminară SEL-001 / G00.

**Stare a implementării: REALIZAT ÎN STAGING, în așteptarea integrării și verificării independente.** Finding păstrat: `SEL-001-A-CANON-F01`, major, `open` în auditul `SEL-001-A-CANON-r01`, verdict istoric **RETURN**. Nu atribui scor, verdict r02 ori închidere de autor. Înregistrarea locală a contradicției în selecție este **H-C9**, nu un finding de audit nou.

Rădăcina căilor relative din acest rezultat: `D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/`.

## 1. Mandat, separarea versiunilor și livrabile

Mandatul explicit curent autorizează implementarea numai într-o copie nouă în staging și consemnarea rezultatului în prezentul fișier. Nu autorizează integrarea în originalul de lucru, alegerea numelui canonic, modificarea manuscriselor/site-ului ori actualizarea manifestelor. Staging va fi integrat de Main după metaaudit, conform mandatului.

Au fost create prin `apply_patch` numai:

- [02_DOCUMENTARE/r02_staging/CANON_EXISTENT.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/02_DOCUMENTARE/r02_staging/CANON_EXISTENT.md>) — raportul de selecție corectat, 57.858 octeți, 290 linii fizice; SHA-256 `a695de981533d4a0f27c5a0c9ae867625831951850d72ca6842e8c1bab005c7b`.
- [06_REGISTRU/MASURI/SEL-001-rezultate-r02.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/MASURI/SEL-001-rezultate-r02.md>) — prezentul rezultat de implementare; nu face parte retroactiv din produsul auditat r01.

Cele două destinații nu existau la verificarea prealabilă. Nu au fost create extrageri DOCX, diff-uri, fișiere temporare de probă, audituri ori alte fișiere. Extracția și compararea au fost în memorie. Nu au fost folosiți subagenți și nu au fost citite fișiere `.env`.

[SEL-001-plan-r01.md](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/06_REGISTRU/MASURI/SEL-001-plan-r01.md>) rămâne **PLANIFICAT istoric**, exact în forma arhivată. Afirmația sa „nicio remediere implementată” descrie momentul acelui plan, nu rezultatul mandatului ulterior de față. Planul nu a fost „actualizat” retrospectiv.

## 2. Intrări și legătura probelor cu versiunile

| Intrare | SHA-256 verificat | Rol în implementare |
| --- | --- | --- |
| `02_DOCUMENTARE/CANON_EXISTENT.md` | `0c64e4cc13bed895a0105a582afca2c85905f69cc90e3ce34774446f2e87ad72` | Produs r01 înghețat, 48.900 octeți, 267 linii. Baza corecției; nu a fost editat. |
| `05_AUDIT/SEL-001/A-CANON-r01.json` | `66aa22455424a2f9f361531a472829a8f3aab543f731a0306f6565875c72c1cd` | Auditul conține un singur finding, F01. ID-ul, severitatea și statutul istoric nu sunt schimbate. |
| `05_AUDIT/SEL-001/A-CANON-r01.md` | `c4e491128bebc2d71838a9fae20b2aa47db6e0171a15514ba42af24324579fd6` | Proba auditorului: ancora `proba-identitate`, L33–L54, în special excerptele L44–L48 și numărătoarea L50. |
| `06_REGISTRU/MASURI/SEL-001-plan-r01.md` | `a5f0b9c0ecb1605b562ec3000e3b74eed0a19b7bb1efdd5f3d51837463d5b7c0` | Măsura `SEL-001-A-CANON-F01-M01`; teste F01-T1–T4 și limitele responsabilităților. |
| `08_ARHIVA/SEL-001/r01-primary-complete/index.json` | `3550617abbf65bfaabc787419bf4a62114429e7cb4b0838a1f20a50297516b8f` | Snapshotul indicat de mandat: 121 intrări, `editorial_approval_issued: false`. Digestul coincide exact cu textul din `index.sha256`. Existența lui nu este un verdict de acceptare sau dovada finalizării metaauditului. |
| `06_REGISTRU/deliverables.json` | `f2cd4902b4e5be5fd9a31e6b9f72046785a7799dca365bf17988435719d0e86d` | Amprenta registrului curent la controalele precizate mai jos; nu este schimbată pentru a înscrie staging în manifestul r01. |

Au fost confruntate cu indexul și fișierele efective exact cinci intrări din snapshotul `r01-primary-complete`: copiile raportului r01, auditului JSON, auditului MD, planului r01 și registrului, la aceleași căi prefixate cu `sources/`. Toate cinci corespund hashurilor și dimensiunilor declarate; copiile coincid cu versiunile de lucru controlate. Nu pretind verificarea tuturor celor 121 intrări sau evaluarea metaauditului de către P-CANON.

Sursa primară **H**: [Hotelul_din_Rue_des_Ames_FINAL_v2.docx](<D:/00. Downloads/Dracula Book/AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Hotelul_din_Rue_des_Ames_FINAL_v2.docx>). Copie: [08_ARHIVA/INTRARI_CANON/20260924-r01/H.docx](<D:/00. Downloads/Dracula Book/02. ATELIER EDITORIAL - ROMANE 50000/08_ARHIVA/INTRARI_CANON/20260924-r01/H.docx>). Fiecare: 269.789 octeți, SHA-256 `a9940d5776380cb40b105429f6976219440f3ea74fb8ebc1d1b4481e9da068c3`. Originalul și copia au fost reverificate; numerele de paragraf de mai jos se referă strict la această versiune.

## 3. F01: cauza documentabilă și corecția realizată

| Câmp | Rezultat |
| --- | --- |
| Finding / măsură | `SEL-001-A-CANON-F01` / `SEL-001-A-CANON-F01-M01`. Este tratat singurul finding din auditul A-CANON r01; nu sunt inventate constatări suplimentare. |
| Cauză constatabilă | R01 L111 asocia numele Alexandre Boucher cu H P3538–P3556 ca probă pentru căsătorie, fără să consemneze Alexandre Dubois din chiar P3548/P3550. H-C5 privea tată/bunic, iar H-C8 Antoine Boucher/Mercier; niciunul nu acoperea numele lui Alexandre. Aceasta este omisiunea documentabilă; nu pretind un motiv psihologic sau un istoric al lecturii nedovedit. |
| Corecție concretă | Rândul personajului este acum „Alexandre — Boucher / Dubois, nume de familie nereconciliat”. Sunt consemnate toate cele patru localizări, excerpte literale și H P3553 separat pentru căsătorie. Este adăugat H-C9, legat explicit de F01; concluzia, comparația, starea cuplului, nucleul recomandării și predarea G01 includ rezerva de nume. |
| Limite respectate | Nu s-a înlocuit arbitrar un nume cu celălalt; nu s-a dedus rudenie cu Catherine/Guillaume Dubois, schimbare legală de nume, pseudonim sau un al doilea Alexandre. Nu s-au schimbat masterul H ori celelalte surse. Conflictul numelui nu este confundat cu H-C5/H-C8. |
| Responsabil implementare | P-CANON, autorul acestei corecții documentare. Acesta nu este auditorul independent și nu își atribuie o identitate de auditor. |
| Responsabil integrare și retest | Main / coordonatorul integrează și îngheață versiunea nouă după metaaudit; rolurile independente stabilite de contract verifică exact noua depunere. Prezentul rezultat nu face aceste operații în locul lor. |
| Impact | Omisiunea de clasificare din selecție este corectată. Faptul căsătoriei rămâne probat; numele de familie rămâne contradictoriu. Titlul The Magenta Letters, plicul și pista Margaux nu sunt infirmate de F01. Recomandarea rămâne DRAFT de selecție preliminară G00. |
| Rezultat așteptat al măsurii | Ambele forme sunt vizibile cu sursa exactă, niciuna nu este promovată tacit în canon, iar conflictul este transmis nominal în G01. |
| Rezultat observat | Aceste elemente sunt introduse în copia staging și au fost controlate de producător prin reextragere, citire și comparație. Nu echivalez acest rezultat cu trecerea retestului independent. |
| Stare | **REALIZAT ÎN STAGING; NEREAUDITAT.** F01 rămâne `open` în r01. Nu este emis un status nou de închidere pentru audit. |

### Proba primară reprodusă

Metoda P este cea declarată în raport: `zipfile` și `lxml`, citire în memorie a `word/document.xml`, namespace `w=http://schemas.openxmlformats.org/wordprocessingml/2006/main`, selecție `//w:body//w:p`, concatenare `.//w:t/text()`, eliminarea paragrafelor fără text, numerotare de la 1. Au rezultat **3.984 paragrafe nevide**; P nu reprezintă pagina Word.

| Localizare în H | Excerpt literal reprodus | Interpretare limitată |
| --- | --- | --- |
| P166 | “My specialty is post-war France, particularly social history—how ordinary people lived. Alexandre Boucher.” | Fragment din autoprezentare, forma Boucher. |
| P860 | “My name is Alexandre Boucher. I'm a historian in Paris.” | Fragment din a doua autoprezentare. |
| P3548 | “Do you, Isabella Morgan, take Alexandre Dubois as your spouse?” | Oficiantul folosește Dubois. |
| P3550 | “And do you, Alexandre Dubois, take Isabella Morgan as your spouse?” | A doua formulă folosește tot Dubois. |
| P3553 | “I now pronounce you married. You may kiss.” | Dovada căsătoriei, nu rezolvarea numelui. |

Căutările literale în întregul H au reprodus exact rezultatul auditorului pentru **numele complete**: Alexandre Boucher la P166/P860, Alexandre Dubois la P3548/P3550. Contextul P3538–P3556 a fost citit integral, inclusiv acordurile P3549/P3551 și pronunțarea căsătoriei P3553; în acel interval apar două Dubois și niciun Boucher.

Pentru a delimita acoperirea fără a confunda căutarea cu lectura integrală, au fost citite și paragrafele returnate de căutările mai largi:

- `Boucher`: P166, P364, P552, P860, P1366, P1370, P1536, P1556, P1897, P2007, P2062, P2280.
- `Dubois`: P143, P145, P170, P216, P228, P232, P237, P256, P369, P392, P401, P468, P650, P651, P659, P660, P663, P666, P846, P865, P915, P936, P938, P977, P1055, P1063, P1086, P1486, P1539, P1897, P2060, P3548, P3550.

Aceste rezultate includ adresări „Monsieur Boucher” și alte personaje cu numele Dubois; ele nu sunt o numărătoare a două nume complete și nu justifică o alegere prin majoritate. Nu reprezintă lectură integrală a capitolelor 1–23 sau a celor aproximativ 95k.

## 4. Localizări ale corecției și regresia întregului raport

Localizările de mai jos aparțin **exclusiv raportului r02_staging de 290 linii**, cu hashul din §1. Nu se aplică r01.

| Zonă controlată | Localizare r02 | Schimbare / constatare |
| --- | --- | --- |
| Statut și concluzie | L3–L17 | Proveniență r02, F01, blocaj G01 și rezervă Boucher/Dubois chiar în concluzie și comparație. |
| Metodă / surse / site | L25, L45, L75–L89 | Lecturile și HTTP-ul r01 sunt declarate istorice; r02 adaugă doar verificările executate, nu o nouă certificare a site-ului. |
| Personaje | L112–L126 | Căsătoria Isabellei este separată de nume; rândul Alexandre include ambele forme și toate cele patru paragrafe. Distincțiile față de alte personaje sunt păstrate. |
| Excerpte și sursă exactă | L128–L142 | Proba localizată și identificată prin hash; referință la findingul original, fără închiderea lui. |
| Cuplu / final | L150 | Faptul căsătoriei este păstrat cu P3553; numele și aniversarea rămân două probleme distincte. |
| Contradicții | L175–L187, în special L183 | H-C1–H-C8 și H-N1/H-N2 rămân neschimbate; este adăugat H-C9, legat de F01. Concluzia registrului nu echivalează promisiunea Magenta cu un canon închis. |
| Recomandare | L248–L252 | Nucleul și lista deciziilor rămase menționează numele nereconciliat; recomandarea nu este schimbată în aprobare. |
| Acoperire și G01 | L262–L277, în special L270 | Se disting lectura raportului și lectura romanului; G01 primește nominal Boucher/Dubois, nu numai o cerință generică de verificare a numelor. |
| Limite / predare | L281–L290 | Staging, integrare ulterioară, retest independent; fără scor, închidere de autor sau promovare a G01. |

Regresia a acoperit întregul raport: recitire r01 L1–L267, compararea tuturor blocurilor modificate și a textului final recitit din fișier cu textul pregătit; examinarea semantică a modificărilor împreună cu blocurile păstrate. Comparația a confirmat **27 de linii-sursă r01 modificate/extinse**, cu rezultat de 290 linii; nu s-au făcut înlocuiri globale de nume. Egalitatea textului a fost verificată după uniformizarea sfârșiturilor de linie și ignorarea newline-ului final; digesturile SHA-256 identifică separat octeții reali.

Controale de conservare efectuate:

- Cele nouă secțiuni principale sunt prezente. Secțiunile 5 și 6, despre Alex Damian și Ten Crowns, sunt identice textual cu r01.
- §4.1, despre masterul real și statutul biblei, §4.4, despre promisiunea The Magenta Letters, și tabelul amprentelor surselor sunt identice textual cu r01.
- Toate rândurile H-C1–H-C8 și H-N1/H-N2 sunt identice; există exact un rând H-C9. Nu s-a rescris Antoine Boucher ca Alexandre și nu s-a modificat numele Catherine/Guillaume Dubois.
- Clauza despre banca mecanismelor din orice mediu cu succes, cu accent pe prezentare, este identică. Cerința master EN minimum 50.000, apoi RO/DE, și separarea auditorilor sunt păstrate; nu sunt scoruri acordate de P-CANON.
- Vechea etichetă necalificată `| **Alexandre Boucher** |` nu mai există. Tabelul probei conține P166/P860/P3548/P3550/P3553, iar recomandarea și predarea G01 păstrează ID-ul F01 și rezerva de nume.
- Sunt păstrate explicit DRAFT, neaprobarea scrierii și limita lecturii integrale. Nu este introdus un plot, o rezolvare a scrisorii sau o explicație inventată pentru nume.
- Textul citit după scriere coincide cu textul pregătit; nu conține caracterul de înlocuire Unicode U+FFFD. Controlul liniilor pentru sublinieri Setext formate numai din `=` ori `-` nu a găsit candidați. Acest control punctual al documentului **nu validează parserul sau schema SYS-001**.

## 5. Testele planului: ce s-a executat și ce nu

Acestea sunt verificări de implementare ale producătorului, nu închiderea testelor în numele auditorului.

| Test din planul istoric | Execuție și rezultat observabil r02 | Ce rămâne |
| --- | --- | --- |
| F01-T1 — reproducerea probei | Executat de P-CANON: hash H/copie, 3.984 paragrafe, toate cele patru localizări, lectura contextuală a nunții și dovada separată P3553. Rezultat concordant cu proba auditorului. | A-CANON trebuie să reproducă independent pe versiunea sursei legată de noua depunere. |
| F01-T2 — corecția coerentă | Executat de P-CANON: ambele nume, cele patru localizări, căsătoria separată, H-C9/F01 în tabel, concluzii și G01; regresie pe întregul raport, conform §4. | Retest independent al documentului exact integrat/înghețat. |
| F01-T3 — limitele corecției | Executată partea de control a producătorului: H, copia H, originalul r01, cele cinci intrări arhivate, planul, auditurile, indexul și registrul controlat păstrează amprentele. Diff-ul este limitat la selecție; nu este ales numele. | Verificările A-GOVERNANCE/A-CANON și conservarea versiunilor în circuitul de integrare; nu sunt înlocuite de declarația producătorului. |
| F01-T4 — depunere și retestare independentă | **NEEXECUTAT în acest mandat.** Nu au fost create ori schimbate manifestul, contractul, schema, audituri r02 sau metaaudituri. | Main, P-SYSTEMS și auditorii desemnați trebuie să asigure depunerea nouă, hashurile, contractul/dependențele/probele, audituri reale r02, metaaudit și arhivare. |

Controale de integritate documentate înainte de scriere la **24.09.2026, 04:36:30 +03:00**, apoi după scrierea selecției la **04:40:04 +03:00**: amprentele din §2 au rămas identice. H/copia H și cele cinci intrări arhivate au fost recontrolate imediat după controlul de la 04:40:04. Digestul fișierului `index.sha256` a rămas `5eec41dd985c8aa69cb91cd69a4f1efb833ca0c95e3f5ee584b2291f0c3356af`; acesta este hashul fișierului sidecar, distinct de textul său, care conține digestul indexului `3550617a…`. Nu sunt presupuse neschimbate toate documentele administrative sau sursele nereverificate.

## 6. Limite, dependențe și predare

Corecția rezolvă **omisiunea din selecție**, nu contradicția din master. Boucher și Dubois rămân nereconciliate. Pentru închiderea G01 și trecerea la scriere rămân obligatorii lectura integrală a masterului ales, nomenclatorul complet, reconcilierea explicită a identității și a celorlalte contradicții și evaluarea independentă a versiunii exacte. O decizie editorială viitoare nu va fi prezentată retroactiv drept fapt cert în manuscrisul actual.

Acoperirea integrală a finalului 24, epilogului, teaserului și biblei este declarația păstrată din r01; în această implementare au fost recitite doar pasajele H enumerate în §3, pe lângă raport. Nu am reverificat HTTP-ul, toate edițiile ori întregul corpus și nu certific o lectură integrală a romanului. Regresia întregului raport nu este un audit de canon integral sau de originalitate.

Cerințele de contract/dependențe/probe legate de hashuri, păstrarea RETURN/HASH și compatibilitatea cu rapoartele reale r02 rămân ale circuitului Main/P-SYSTEMS/auditori. `schema_version: 1` din A-CANON r01 este o caracteristică a documentului istoric, nu acceptarea implicită a acelei scheme pentru r02. Nu am implementat și nu am validat schema nouă sau detectorul Setext; nu am convertit verdicturi și nu am „reparat” manifestul r01. Pentru A-CANON r01 proba citită spune RETURN; nu îi atribui un verdict HASH neconsemnat.

Predau cele două fișiere autorizate. Planul r01 rămâne PLANIFICAT istoric, originalele înghețate rămân disponibile pentru QA r01, iar staging așteaptă integrarea de către Main după metaaudit și retestarea independentă. **Fără scor și fără închidere de autor pentru SEL-001-A-CANON-F01; selecția rămâne preliminară, G01 rămâne blocat.**
