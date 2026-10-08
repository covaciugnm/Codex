# Compară 3 programe HR gratuite

ID: `01a11ac9-7ce0-7481-87a6-870f72ae1107`  
Proiect: iDempiere  
Export UTC: 2026-10-08T14:13:28.280906+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Utilizator

Cauta top 3 cele mai dezvoltate si stabile 100% free programde HR de pe github/huginface etc...
justifica ce au unele si altele si de ce sunt cele mai bune
de preferat in Java pentru ca dorim sa il integram cu iDempiere


## Asistent

Voi căuta proiecte HR open-source mature, cu accent pe Java, licențe fără costuri și posibilități de integrare cu iDempiere. Voi compara funcționalitățile disponibile gratuit, mentenanța și limitele fiecăruia.

## Asistent

Axelor este un candidat Java promițător, dar oferta Community are limite față de edițiile comerciale, inclusiv la migrarea între versiuni. Frappe HR pare mai complet ca produs HR gratuit, deși este în Python. Verific și Apache OFBiz, plus pluginurile native iDempiere, pentru a separa maturitatea produsului de ușurința integrării.

## Asistent

**Pentru integrarea cu iDempiere, lista mea scurtă este: Frappe HR, Axelor Open Suite și Apache OFBiz.** Frappe câștigă la funcționalitate HR gratuită; Axelor este prima opțiune pe care aș testa-o dacă Java contează mult; OFBiz este potrivit mai ales pentru dezvoltare proprie.

Am verificat repository-urile, documentația, licențele și versiunile publicate, la **8 octombrie 2026**. Clasamentul reprezintă evaluarea mea pentru cerințele voastre, nu un clasament universal.

Prin „100% free” înțeleg **fără taxe de licență pentru instalarea pe serverele proprii**. Administrarea și integrarea presupun muncă. Stabilitatea o pot evalua prin mentenanță și istoricul versiunilor; nu am testat aceste aplicații în producția voastră.

| Loc | Produs | Tehnologie | Gratuitate | Avantaj decisiv | Principalul compromis |
|---|---|---|---|---|---|
| **1** | **Frappe HR** | Python + JavaScript | HRMS open-source, instalabil gratuit | Cea mai completă alegere HR din această selecție | Introduce un ecosistem tehnic diferit |
| **2** | **Axelor Open Suite – HR** | **Java** | Cod HR public; Community gratuită | Cel mai bun compromis între Java și funcționalitate HR | Unele facilități și servicii sunt comerciale |
| **3** | **Apache OFBiz – HR** | **Java** | Open-source, Apache 2.0 | Bază matură pentru personalizare profundă | Mai multă implementare pentru o experiență HR finisată |

**1. Frappe HR — recomandarea mea pentru un HR complet, gratuit**

[Repository GitHub](https://github.com/frappe/hrms)

Include dosare de angajați, onboarding, promovări și transferuri, concedii, prezență, deconturi și avansuri, evaluări, obiective, structuri salariale și fluturași. Are și aplicație mobilă pentru operațiuni uzuale. Avantajul față de Axelor este că dispune de un **motor de salarizare**, în timp ce Axelor documentează în principal pregătirea datelor pentru salarizare. [Funcționalități oficiale](https://github.com/frappe/hrms#key-features)

Mentenanța este activă: pagina de versiuni arată actualizări și corecții pe ramurile 15 și 16, inclusiv la 7 octombrie 2026. Acesta este un indicator bun de continuitate, fără a demonstra singur absența erorilor. [Versiuni publicate](https://github.com/frappe/hrms/releases)

**Pentru iDempiere:** framework-ul oferă API REST pentru citirea și modificarea documentelor. Prin urmare, un conector scris în Java poate sincroniza datele fără să fie necesară rescrierea HR-ului în Java. [Documentația API](https://docs.frappe.io/framework/user/en/api/rest)

Limita practică este că echipa trebuie să întrețină și platforma Frappe; personalizările interne se fac în ecosistemul Python/JavaScript.

**Licență:** fișierul din repository-ul verificat indică **GPL-3.0**. Site-ul comercial afișează AGPL-3.0, deci există o neconcordanță între surse; pentru implementare trebuie verificată licența versiunii exacte alese. [Licența din cod](https://raw.githubusercontent.com/frappe/hrms/develop/license.txt)

**De ce îl pun primul:** oferă cel mai convingător ansamblu de funcții HR și salarizare, cu dezvoltare activă și o cale clară de integrare prin API.

**2. Axelor Open Suite — prima alegere de evaluat dacă preferați Java**

[Repository GitHub](https://github.com/axelor/axelor-open-suite) · [Modulul HR public](https://github.com/axelor/axelor-open-suite/tree/master/axelor-human-resource)

Acoperă angajați și contracte, concedii, foi de timp, deconturi, ore suplimentare, recrutare, formare, evaluări, prime și pregătirea salarizării. Documentația explică explicit că pregătirea salariilor presupune colectarea datelor și exportul către software de salarizare adecvat. **Nu l-aș considera un înlocuitor complet al unei aplicații de salarii.** [Documentația HR](https://docs.axelor.com/aos/en/5.4/hr/)

Proiectul publică versiuni de mentenanță pentru mai multe ramuri; la verificare, versiunea marcată „Latest” era **9.1.9**, publicată la 1 octombrie. [Versiuni publicate](https://github.com/axelor/axelor-open-suite/releases)

**Pentru iDempiere:** Java ajută echipa la dezvoltare și depanare, iar Axelor oferă servicii REST/JSON. Totuși, modulul Axelor nu devine automat un plugin iDempiere: recomand integrarea între aplicații prin API. [Servicii web Axelor](https://docs.axelor.com/adk/7.4/dev-guide/web-services/index.html)

**Atenție la cerința „100% free”:** codul public este AGPLv3, dar produsul are și ediții Pro/Enterprise. Pagina actuală rezervă anumite funcții edițiilor comerciale; echipa Axelor precizează și că scripturile de migrare între versiuni nu sunt furnizate Community. Codul nou poate fi folosit gratuit, însă migrarea datelor poate rămâne responsabilitatea voastră. [Ediții](https://axelor.com/pricing/) · [Clarificarea oficială privind migrările](https://forum.axelor.com/t/clarifcation-on-community-versions/6243)

**De ce îl pun al doilea:** este foarte relevant pentru echipa voastră Java, însă gratuitatea nu acoperă întregul pachet comercial, iar salarizarea și actualizările necesită atenție suplimentară.

**3. Apache OFBiz — opțiunea Java pentru control și dezvoltare proprie**

[Repository GitHub](https://github.com/apache/ofbiz-framework)

Modulul HR include structuri organizaționale, poziții, angajați, recrutare, competențe, calificări, formare, evaluări, concedii și informații despre remunerație. Este integrat cu celelalte componente OFBiz, inclusiv contabilitatea. [Manualul oficial HR](https://nightlies.apache.org/ofbiz/stable/ofbiz/html5/user-manual.html#_human_resources)

Are un proces de versiuni stabil: **24.09.07**, publicată în iunie 2026, aparține unei ramuri înghețate funcțional din septembrie 2024, care primește corecții. Acesta este un argument concret pentru predictibilitatea mentenanței. [Versiuni și politica de actualizare](https://ofbiz.apache.org/download.html)

Codul este disponibil sub **Apache License 2.0**. [Licență](https://github.com/apache/ofbiz-framework/blob/trunk/LICENSE)

**Pentru iDempiere:** avantajul este Java și posibilitatea de personalizare profundă. Dezavantajul este că introduceți încă o platformă ERP, cu propriul model de date și propriile servicii. Estimez un efort mai mare decât la Frappe pentru a obține un HR comod pentru angajați și administratori.

**De ce îl pun al treilea:** este o bază tehnică matură, dar l-aș alege când vreți să construiți și să adaptați substanțial, nu când prioritatea este folosirea rapidă a unui HR complet.

**Ce aș alege concret pentru voi**

- **HR complet, cu cât mai multe funcții gratuite:** Frappe HR.
- **Echipă predominant Java, accent pe angajați, concedii, pontaj și deconturi:** pilot cu Axelor Community.
- **Java și dezvoltare proprie amplă:** Apache OFBiz.

Arhitectura pe care o recomand este **HR separat + conector Java către iDempiere**. HR-ul gestionează angajații și aprobările, iar iDempiere primește datele necesare contabilității și costurilor. Aș evita scrierea directă în bazele de date ale celor două aplicații.

Mai există o opțiune foarte relevantă: **plugin HR/payroll nativ iDempiere**. De exemplu, CDSoftware Payroll este documentat sub GPLv2, cu contracte, angajați, reguli salariale și împrumuturi. Totuși, pagina declară testare pe iDempiere 10; nu am suficiente dovezi de compatibilitate actuală ca să-l plasez înaintea celor trei. [Pluginul oficial documentat](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_Payroll)

OrangeHRM Starter rămâne o alternativă matură, dar este PHP și are o separare între Starter și Advanced; pentru preferința voastră Java nu aduce un avantaj decisiv. [Comparația edițiilor](https://orangehrm.com/pricing)

**Recomandarea finală: comparați practic Frappe HR cu Axelor pe aceleași fluxuri.** Dacă aveți nevoie și de salarizare românească, nu am confirmat pentru niciunul un pachet complet, întreținut, pentru calculul local și raportările D112/REGES-ONLINE; această cerință poate schimba alegerea.

## Utilizator

aceste programe contin si partea de SSM / ISU necesara firmei conform legislatiei romanesti ?


## Asistent

Voi verifica dacă cele trei au module dedicate SSM și SU/PSI pentru România și ce diferență există între acestea și funcțiile generale de instruire sau evidență a angajaților.

## Asistent

**Nu, nu ca module complete, gata de utilizat conform legislației românești.** Pentru Frappe HR, Axelor și Apache OFBiz **nu am identificat în documentația oficială un pachet dedicat SSM și SU/PSI pentru România**. Recomandarea anterioară privea funcțiile HR generale, nu conformitatea în aceste domenii.

Prin „partea de ISU” mă refer aici la **situații de urgență și prevenirea/stingerea incendiilor — SU/PSI**.

| Program | Ce există și poate ajuta | Ce nu am identificat inclus |
|---|---|---|
| **Frappe HR** | Programe de instruire, sesiuni, rezultate și feedback | Fișe SSM/SU românești, fluxuri legale specifice și documentație completă de prevenire |
| **Axelor** | Instruiri obligatorii, participanți, durată și competențe dobândite | Pachet legislativ românesc SSM/SU și formulare locale gata de folosit |
| **Apache OFBiz** | Evidența instruirilor, calificărilor și angajaților | Modul complet pentru obligațiile SSM/SU din România |

Aceste funcții sunt descrise în documentațiile oficiale: [Frappe Training](https://docs.frappe.io/hr/training-program), [Axelor Training](https://docs.axelor.com/aos/en/aos/RH/training/), [OFBiz HR](https://nightlies.apache.org/ofbiz/stable/ofbiz/html5/user-manual.html).

**Diferența esențială:** înregistrarea unui curs numit „Instruire SSM” nu acoperă automat obligațiile firmei.

Pentru SSM, aplicația ar trebui să susțină, în funcție de activitatea firmei:

- evaluările riscurilor pe locuri de muncă și planul de prevenire și protecție;
- instrucțiunile proprii și responsabilitățile;
- instruirile, verificarea cunoștințelor și documentarea lor;
- evidențele relevante privind echipamentele de protecție și evenimentele de muncă.

Cadrul principal este [Legea nr. 319/2006](https://legislatie.just.ro/Public/DetaliiDocument/73772), împreună cu normele de aplicare aprobate prin HG nr. 1425/2006.

Pentru SU/PSI, necesarul poate include organizarea responsabilităților, instruiri și fișe specifice, documente și planuri aplicabile amplasamentului, exerciții, precum și evidența verificărilor mijloacelor de apărare împotriva incendiilor. Cerințele depind de activitate și de clădiri; nu se reduc la dosarul angajatului. Reperele sunt [Legea nr. 307/2006](https://legislatie.just.ro/Public/DetaliiDocument/243520), [Ordinul nr. 163/2007](https://legislatie.just.ro/Public/DetaliiDocument/80730) și [Ordinul nr. 712/2005](https://legislatie.just.ro/Public/DetaliiDocumentAfis/63056).

**Pentru voi, această cerință schimbă recomandarea:** dacă obiectivul principal este gestionarea SSM/SU alături de iDempiere, aș evalua **un modul dedicat în iDempiere**, înainte de introducerea unui al doilea ERP precum Axelor sau OFBiz.

Modulul ar putea reuni angajații, posturile, punctele de lucru, instruirile, scadențele, documentele și istoricul verificărilor. **Formularele și fluxurile trebuie validate de persoanele competente SSM/SU ale firmei**, inclusiv modul de semnare și păstrare a documentelor. Software-ul ajută la evidență și control; conformitatea presupune și efectuarea activităților și măsurilor cerute.

**Deci: toate trei pot servi drept bază tehnică, dar niciunul dintre ele nu poate fi considerat, pe dovezile verificate, o soluție completă SSM/ISU pentru România fără adaptări.**

## Utilizator

exista programe dedicate SSM ... adaptate legislatiei romanesti 100% pe care sa le integram ?
le putem integra in Frappe ? sau are sens ?


## Asistent

Voi căuta soluții românești dedicate SSM/SU și voi verifica dacă oferă API sau alte metode de integrare. Voi separa acoperirea legislativă declarată de furnizori de ceea ce se poate confirma public și voi evalua dacă Frappe aduce un beneficiu în această arhitectură.

## Asistent

**Da, există platforme românești dedicate SSM/SU, iar integrarea cu Frappe este fezzabilă. Cea mai clară opțiune de integrare pe care am verificat-o este SSM.ro, deoarece are API documentat public.**

Totuși, **„adaptat legislației românești” nu înseamnă că instalarea aplicației garantează 100% conformitatea firmei**. Trebuie verificată acoperirea activităților și punctelor voastre de lucru, nu doar existența fișelor de instruire.

În privința cerinței inițiale: **nu am identificat o soluție matură care să combine gratuitate integrală, cod open-source, acoperire SSM/SU românească și API verificabil.**

**Soluțiile concrete pe care le-aș evalua**

| Soluție | Ce oferă / declară furnizorul | Integrare verificată public | Gratuitate |
|---|---|---|---|
| **SSM.ro** | Gestionare SSM/PSI, instruire, documente și semnare electronică | **Da: API documentat pentru angajați/contacte și anumite rapoarte** | Comercială; tarifarea descrisă este pe salariat |
| **SSMatic.ro** | Documentații, instruiri, fișe de risc, evidența firmelor și angajaților, notificări | **Nu am confirmat un API public** | Pachet gratuit declarat; semnarea electronică se plătește |
| **SafeHub** | Platformă SSM/HSE pentru firme și servicii externe; declară conformitate cu cadrul românesc SSM/SU | **Nu am confirmat un API public** | Costul și condițiile integrării trebuie confirmate |

Surse: [SSM.ro — funcționalități și tarifare](https://www.ssm.ro/intrebari-frecvente), [SSM.ro — API](https://ghid.ssm.ro/docs/03-api), [SSMatic — pachete](https://www.ssmatic.ro/preturi), [SafeHub — prezentare](https://safehub.ro/). Afirmațiile de conformitate ale furnizorilor nu reprezintă o certificare independentă făcută de mine.

**1. SSM.ro — prima opțiune pentru integrare**

Documentația publică confirmă:

- citirea unui angajat/contact după marcă;
- crearea și actualizarea acestuia;
- autentificare prin token;
- preluarea unor rapoarte;
- disponibilitate în variantă SaaS partajată și instalare Enterprise dedicată. [Documentație API](https://ghid.ssm.ro/docs/03-api)

Există și un exemplu oficial de sincronizare cu un sistem HR, inclusiv tratarea angajaților cu contract încetat. [Exemplu de sincronizare](https://ghid.ssm.ro/docs/03-api/exemple-implementare/nodejs)

**Limita importantă:** raportul documentat public este pentru **documente în așteptarea semnării**. Nu am confirmat endpoint-uri pentru exportul tuturor PDF-urilor semnate, istoricul complet al instruirilor, scadențe sau notificări automate către alte sisteme. Acestea trebuie cerute explicit înainte de alegere. [API rapoarte](https://ghid.ssm.ro/docs/03-api/rapoarte)

**2. SSMatic — interesant dacă bugetul este prioritar**

Furnizorul declară gratuită gestionarea firmelor și angajaților, generarea documentelor și notificările, cu plată pentru semnătura electronică. **Gratuitatea serviciului nu înseamnă acces la cod sau instalare pe serverul vostru.** Fără confirmarea API-ului ori a unui export structurat, nu l-aș alege încă pentru automatizare cu Frappe. [Oferta publică](https://www.ssmatic.ro/preturi)

**3. SafeHub — candidat pentru demonstrație funcțională**

Este o platformă dedicată domeniului și declară acoperire legislativă românească. Merită comparată pe fluxurile voastre, dar integrarea rămâne neconfirmată: în pagina publică verificată nu am găsit documentație API. [Prezentarea oficială](https://safehub.ro/)

**Integrarea cu Frappe are sens?**

**Da, dacă doriți Frappe HR și pentru angajați, concedii, pontaj, recrutare și evaluări.** Frappe oferă REST API și webhooks, deci permite construirea unui conector către o platformă SSM. Nu am identificat un conector Frappe–SSM.ro gata făcut; discutăm despre o integrare de dezvoltat. [Capabilități Frappe](https://frappe.io/framework/api-and-integrations)

Aș împărți responsabilitățile astfel:

| Sistem | Rol recomandat |
|---|---|
| **Frappe HR** | Evidența principală a angajaților, structurii organizaționale și proceselor HR |
| **Platforma SSM/SU** | Instruiri specifice, documente, semnare și evidențe de specialitate |
| **iDempiere** | Operațiuni ERP, contabilitate și costuri |

Un flux concret ar fi:

1. Angajatul este introdus sau actualizat în Frappe.
2. Conectorul transmite datele necesare către platforma SSM.
3. Responsabilul SSM stabilește încadrarea în grupa de risc și instruirile aplicabile.
4. În Frappe se afișează situația documentelor și, **dacă API-ul furnizorului permite**, scadențele și linkurile către documentele semnate.

Încadrarea în grupa de risc nu trebuie dedusă automat doar din denumirea funcției. Chiar ghidul SSM.ro explică faptul că acest câmp are un rol specific și nu există de regulă în sistemul HR. [Ghidul de integrare](https://ghid.ssm.ro/docs/03-api/exemple-implementare/nodejs)

**Dacă aveți nevoie doar de SSM/SU, nu aș introduce Frappe ca intermediar.** Integrarea directă **iDempiere ↔ platformă SSM** ar reduce numărul de aplicații și sincronizări.

Înainte de contractare, aș cere furnizorului trei demonstrații concrete:

- acoperirea documentelor și fluxurilor pentru activitatea voastră, validată împreună cu responsabilul SSM/SU;
- sincronizarea unui angajat și citirea situației instruirilor prin API, cu prețul accesului API precizat;
- exportul complet al documentelor semnate și al dovezilor aferente, inclusiv la încetarea abonamentului.

**Recomandarea mea este să evaluați întâi SSM.ro pentru conectivitate. Frappe + platformă SSM are sens dacă Frappe devine sistemul vostru HR; pentru SSM singur, aș integra direct cu iDempiere.**

## Utilizator

realizeaza o analiza completa si complexa cu toate functionalitatile actuale din Idempiere 
ce ofera cele trei programe de HR si ce ofera programele de SSM/SU 
compara tabe;lar clar module/functii documenteaza cu linkuri de download a tuturor documentatiilor pentru fiecare din cele 3 + 3 - de unde se poate vedea clar ce si cum ofera


## Asistent

Voi construi o matrice detaliată pe module și funcții, separând ce există în iDempiere standard, ce necesită pluginuri și ce oferă fiecare dintre cele trei soluții HR și trei platforme SSM/SU. Voi include sursele oficiale, documentațiile și descărcările disponibile, marcând explicit funcțiile sau condițiile de acces pe care nu le pot confirma public.

## Asistent

Documentația iDempiere amestecă uneori funcții standard cu extensii ale comunității, în special la producție și salarizare. Le voi marca separat, pentru a nu atribui instalării de bază funcții disponibile doar prin pluginuri. La platformele SSM voi distinge între funcții descrise în manuale, afirmații comerciale și informații nepublicate.

## Utilizator

Cauta si module de iDempiere suplimentare deja existente oriund ein lume legate de HR - care sa dezvolte ceea ce are deja implicit iDempiere


## Asistent

Includ și o secțiune dedicată extensiilor HR pentru iDempiere: salarizare, dosar de personal, recrutare, pontaj, concedii și instruire. Pentru fiecare voi căuta sursa codului, licența, documentația și versiunile iDempiere pentru care există dovezi de compatibilitate, ca să putem compara extinderea iDempiere cu introducerea Frappe.

## Asistent

Am găsit o familie de extensii CDSoftware pentru iDempiere care acoperă salarizare, pontaj, recrutare, instruire și rapoarte salariale. Paginile verificate declară însă testare pe versiunea 10; AMERPSOFT menționează actualizare pentru versiunea 12. Acestea sunt alternative reale de evaluat, dar compatibilitatea cu versiunea voastră trebuie testată înainte de a le considera echivalente unui HR gata de instalat.

## Asistent

Diferența decisivă este între un motor HR configurabil și o soluție pregătită pentru obligațiile din România. Nici documentația HR, nici cea a extensiilor iDempiere găsite nu confirmă un pachet complet pentru salarizare românească, REGES și SSM/SU. Dintre platformele SSM analizate, SSM.ro publică și documentație API; pentru celelalte două, posibilitatea unei integrări complete rămâne de confirmat.


## Asistent

**Da — există extensii HR pentru iDempiere care merită evaluate înainte să introduceți încă un sistem ERP. Cele mai relevante găsite sunt familia CDSoftware și AMERPSOFT Personnel & Payroll.** Acoperă o parte importantă din diferența dintre iDempiere standard și un HRMS, dar compatibilitatea cu versiunile actuale și adaptarea pentru România nu sunt demonstrate complet.

Am inclus mai jos analiza integrată: iDempiere standard, extensiile existente, trei soluții HR și trei platforme SSM/SU.

**Concluzia pentru situația voastră:** aș compara într-un proiect pilot două variante:

- **iDempiere + extensii HR native + platformă SSM/SU românească**, dacă prioritatea este păstrarea unui singur sistem principal.
- **iDempiere + Frappe HR + platformă SSM/SU românească**, dacă prioritatea este funcționalitatea HR mai bogată și accesul angajaților.

Java ajută la dezvoltarea extensiilor native. Pentru integrarea între aplicații, disponibilitatea și calitatea API-urilor contează mai mult decât folosirea aceluiași limbaj.

**Data verificării: 8 octombrie 2026.** Analiza privește funcțiile documentate public, nu o verificare a instalării voastre. Prin „completă” acopăr modulele și familiile funcționale; inventarul fiecărui câmp, raport și proces depinde de versiunea și pluginurile efectiv instalate.

---

**1. Ce înseamnă, în această comparație, „gratuit”, „stabil” și „compatibil cu România”**

| Criteriu | Ce trebuie să existe pentru a-l considera îndeplinit |
|---|---|
| Gratuit ca licență | Cod disponibil sub o licență care permite utilizarea dorită fără abonament obligatoriu |
| Gratuit în exploatare | Ar presupune inclusiv găzduire, administrare, actualizări, integrare și semnături fără cost; nu rezultă automat din open-source |
| Mentenanță activă | Versiuni, remedieri și documentație actualizate |
| Stabil pentru voi | Testare pe versiunea aleasă, cu datele și fluxurile voastre |
| Salarizare românească | Reguli fiscale și de muncă, documente și raportări locale implementate și întreținute |
| SSM/SU pentru România | Fluxuri, documente, semnături și evidențe potrivite activității și obligațiilor firmei |
| Integrare disponibilă | API documentat sau conector existent, nu doar posibilitatea teoretică de a programa unul |

**Nu am identificat o soluție demonstrabil „100% gratuită + completă HR + salarizare românească + SSM/SU românesc + integrare gata făcută cu iDempiere”.** Există componente care pot forma o astfel de arhitectură, cu efort de implementare și mentenanță.

În tabele:

- **Da** = funcție documentată.
- **Parțial** = acoperire limitată sau alt scop.
- **Extensie** = necesită un modul suplimentar.
- **De construit** = configurare/dezvoltare specifică.
- **NC** = neconfirmat din documentația publică; nu înseamnă obligatoriu că funcția lipsește.
- La platformele comerciale, funcțiile prezentate pe site sunt **declarații ale furnizorului**, nu rezultate ale unui test independent.

---

**2. Ce oferă iDempiere standard**

Documentația oficială delimitează ariile ERP principale, iar manualul de referință descrie ferestrele și procesele. Pentru comparație folosesc versiunea stabilă 13; ramura de dezvoltare nu trebuie confundată cu versiunea de producție. [Structura funcțională](https://docs.idempiere.org/docs/basic-functional/menue_overview), [manualul de referință](https://wiki.idempiere.org/en/Reference), [versiuni și instalatoare](https://wiki.idempiere.org/en/Downloading_Installers).

| Modul / familie | Funcții principale | Situație |
|---|---|---|
| Organizații | Companii, organizații, structuri și acces separat | Standard |
| Utilizatori și securitate | Utilizatori, roluri, drepturi, restricții de acces | Standard |
| Parteneri | Clienți, furnizori, angajați, contacte, adrese | Standard |
| Relații cu partenerii | Solicitări, responsabilități, urmărire activități | Standard |
| Vânzări | Oferte, comenzi, livrări, facturare | Standard |
| Achiziții | Necesar, cereri de ofertă, comenzi, recepții, facturi | Standard |
| Verificare achiziții | Corelare comandă–recepție–factură | Standard |
| Retururi | Retururi comerciale și documente asociate | Standard |
| Produse | Articole, servicii, categorii, unități, atribute | Standard |
| Prețuri | Liste, versiuni de preț, reduceri | Standard |
| Stocuri | Depozite, locații, mișcări, inventariere | Standard |
| Trasabilitate | Loturi/serii și atribute, în funcție de configurare | Standard |
| Reaprovizionare | Reguli și procese de completare a stocului | Standard |
| Contabilitate | Scheme contabile, note, dimensiuni, perioade | Standard |
| Valute și taxe | Valute, cursuri și configurări fiscale | Standard; localizarea rămâne distinctă |
| Încasări și plăți | Plăți, alocări, bancă și casă | Standard |
| Creanțe și datorii | Solduri, scadențe, vechime, urmărire încasări | Standard |
| Costuri | Costuri produse și costuri suplimentare | Standard |
| Raportare financiară | Rapoarte configurabile, analiză contabilă | Standard |
| Active fixe | Evidență și amortizare | Standard |
| Proiecte | Proiecte, faze, activități și costuri | Standard |
| Timp și cheltuieli | Ore pe proiect și deconturi | Standard |
| Resurse | Resurse, disponibilitate și alocări | Standard |
| Producție de bază | BOM, consumuri și producție | Standard |
| Producție avansată | MRP/planificare extinsă și alte funcții industriale | Verificat separat; inclusiv pluginuri |
| Automatizări | Workflow, aprobări, procese programate | Standard |
| Documente și rapoarte | Atașamente, formate de tipărire, rapoarte | Standard |
| Personalizare | Application Dictionary, ferestre, câmpuri, procese | Standard |
| Extensibilitate | Pluginuri Java/OSGi | Standard ca mecanism |
| API REST extins | Acces la modele, procese și alte resurse | Plugin dedicat |

Acest inventar rezultă din [manualul funcțional](https://wiki.idempiere.org/en/Reference) și [catalogul ferestrelor/proceselor](https://wiki.idempiere.org/en/Manual). Funcțiile unui plugin precum Libero Manufacturing nu trebuie atribuite automat instalării standard; catalogul oficial separă explicit extensiile. [Pluginuri disponibile](https://wiki.idempiere.org/en/Category%3AAvailable_Plugins).

**Ce înseamnă asta pentru HR**

| Cerință HR | iDempiere standard | Ce mai trebuie |
|---|---|---|
| Evidență persoană/angajat | Înregistrare de partener, contacte și date asociate | Dosar HR mai bogat |
| Ore lucrate pe proiect | Există | Reguli de pontaj și prezență |
| Deconturi | Există | Eventuale politici specifice firmei |
| Programarea resurselor | Există | Nu echivalează cu planificarea completă a turelor |
| Recrutare | Nu rezultă un ATS complet standard | Extensie sau aplicație HR |
| Contracte și carieră | Acoperire HR completă neconfirmată | Extensie |
| Concedii și solduri | Modul HR complet neconfirmat | Extensie |
| Pontaj de la dispozitive | Nu rezultă ca funcție HR standard | Extensie |
| Salarizare | Motor HR/payroll suplimentar | Extensie și localizare |
| Evaluări și instruiri | Nu rezultă o suită HR completă standard | Extensii |
| Documente SSM/SU România | Pachet dedicat neidentificat | Platformă specializată sau dezvoltare |
| Salarizare și raportări România | Pachet complet neconfirmat | Localizare sau integrare dedicată |

O distincție importantă: **Expense Report înregistrează ore și cheltuieli pentru proiecte/decontare; nu dovedește existența unui sistem complet de pontaj cu ture, întârzieri și concedii.** [Documentația Expense Report](https://wiki.idempiere.org/en/Expense_Report_%28Window_ID-235%29).

---

**3. Extensii HR iDempiere existente, găsite în ecosistemul internațional**

Aceasta este partea care poate reduce cel mai mult dezvoltarea de la zero.

| Extensie | Ce adaugă documentat | Licență / compatibilitate publicată | Evaluarea mea |
|---|---|---|---|
| **CDSoftware Payroll** | Angajați, departamente, poziții, concepte și perioade salariale, reguli, multivalută, împrumuturi cu contabilizare | GPLv2; testat pe **10.0.0** | Candidat principal pentru HR/payroll nativ |
| **CDSoftware Attendance** | Import pontaj TXT, formate HIKVISION, ture rotative, întârzieri, administrarea dispozitivelor | GPLv2; testat pe **10.0.0** | Foarte relevant pentru pontaj |
| **CDSoftware EmployeeTraining** | Planificarea, realizarea și urmărirea instruirilor | GPLv2; testat pe **10.0.0**; depinde de Payroll | Bază pentru formare profesională |
| **CDSoftware EmployeeRecruitment** | Recrutare și selecție | GPLv2; testat pe **10.0.0**; depinde de Payroll și Training | De evaluat; descrierea publică este scurtă |
| **CDSoftware PayrollReport** | Rapoarte salariale cu coloane multiple și exporturi configurabile | GPLv2; testat pe **10.0.0**; depinde de Payroll și Attendance | Util pentru raportare și interfețe |
| **CDSoftware PerformanceEvaluation** | Apare în catalog sub acest nume | Detaliile funcționale și compatibilitatea: NC | Pista există; nu o consider funcție validată |
| **AMERPSOFT Personnel & Payroll** | Evidență personal, concepte și formule salariale, procese și rapoarte | Repository-ul indică actualizare pentru **12**, cu mențiunea **Under Test**; licența trebuie clarificată | Al doilea candidat nativ important |
| **Ingeint Payroll** | Soluție de payroll prezentă în ecosistem | Disponibilitatea actuală a sursei și compatibilitatea: neconfirmate | Necesită verificare cu mentenorul |
| **Ingeint Human Talent** | Repository Java cu acest nume | Documentație, versiuni și acoperire funcțională insuficient confirmate | Punct de cercetare, nu recomandare de producție |
| **Libero Payroll, varianta veche** | Motor HR/payroll extensibil prin reguli | Pagina avertizează explicit: **învechit și neîntreținut** | Nu l-aș alege pentru implementare nouă |
| **Localization Romania** | Traducere și import plan de conturi; alte elemente în lista de intenții | Pagina: „in Progress”, ultima modificare indicată în 2020 | Nu dovedește salarizare sau SSM românesc |
| **HR/Payroll din ADempiere** | Sursă de idei și funcții HR din proiectul înrudit | Alt produs | Portare posibilă ca proiect; nu instalare directă în iDempiere |

Sursele pentru familia CDSoftware sunt paginile proprii din wiki: [Payroll](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_Payroll), [Attendance](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_Attendance), [Training](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_EmployeeTraining), [Recruitment](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_EmployeeRecruitment), [PayrollReport](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_PayrollReport). PerformanceEvaluation este listat în [catalogul oficial](https://wiki.idempiere.org/en/Category%3AAvailable_Plugins).

Celelalte surse: [AMERPSOFT](https://github.com/luisamesty/Amerpsoft-iDempiere-community), [Ingeint Payroll](https://wiki.idempiere.org/en/Plugin%3A_Ingeint_Payroll), [Ingeint Human Talent](https://github.com/ingeint/ingeint-idempiere-humantalent), [avertismentul Libero Payroll](https://wiki.idempiere.org/en/Plugin%3A_Libero_Payroll), [Localization Romania](https://wiki.idempiere.org/en/Plugin%3A_Localization_Romania), [versiuni ADempiere](https://github.com/adempiere/adempiere/releases).

**Ce trebuie observat la cei doi candidați principali**

**CDSoftware** este cea mai interesantă familie prin întinderea funcțională: payroll, pontaj, recrutare și instruire au module distincte și dependențe documentate. Totuși:

- testarea publicată este pentru iDempiere 10, nu dovadă de compatibilitate cu 13;
- exemplele Payroll includ configurări pentru Panama;
- „Payroll Contract” descrie și frecvența salarizării; nu trebuie confundat cu un CIM românesc;
- instruirea profesională generică nu reprezintă automat instruire SSM/SU conformă. [Documentația Payroll](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_Payroll).

**AMERPSOFT** are semnale de adaptare la versiuni iDempiere mai recente. Modulul utilizează tabele proprii `AMN_` și formule configurabile; documentația sa provine dintr-un context de localizare diferit de România. Există și nealiniere între informațiile de versiune din README-ul general și cel al modulului. [Repository](https://github.com/luisamesty/Amerpsoft-iDempiere-community), [documentația Personnel & Payroll](https://github.com/luisamesty/Amerpsoft-iDempiere-community/blob/master/org.amerpsoft.com.idempiere.personnelpayroll/README.md).

**Nu aș instala CDSoftware Payroll și AMERPSOFT Payroll împreună ca soluție implicită.** Le-aș trata drept alternative până când sunt verificate modelele de date, procesele contabile și dependențele. Altfel riscați două evidențe salariale în același ERP.

**Ordinea mea de evaluare pentru extensii native:** familia CDSoftware pentru acoperire HR, AMERPSOFT pentru alternativa de payroll, apoi celelalte doar dacă se confirmă sursele și mentenanța.

---

**4. Comparația celor trei soluții HR independente**

Pentru comparație folosesc **Frappe HR, Axelor Open Suite HR și Apache OFBiz HR**. Sunt trei candidați potriviți criteriilor voastre, nu un clasament universal: Frappe oferă un reper funcțional HR, iar Axelor și OFBiz răspund preferinței pentru Java.

| Criteriu | Frappe HR | Axelor Open Suite HR | Apache OFBiz HR |
|---|---|---|---|
| Tehnologie principală | Python / JavaScript | Java | Java, cu componente și scripting proprii |
| Licență sursă | GPLv3 în fișierul consultat | AGPLv3 | Apache 2.0 |
| Instalare proprie | Da | Da, Community | Da |
| Natura produsului | Aplicație HR pe platforma Frappe | Modul într-o suită ERP | Modul într-o platformă ERP |
| Activitate recentă observată | Release-uri v15 și v16 în octombrie 2026 | Release-uri 9.1.x în octombrie 2026 | 24.09.07, iunie 2026 |
| Principalul avantaj | Acoperire HR și fluxuri pentru angajați | HR în Java, extensibil | Platformă Java și licență permisivă |
| Principalul compromis pentru voi | Încă o platformă tehnică | Suprapunere cu ERP-ul existent | Efort mai mare de adaptare a experienței HR |
| Salarizare românească gata de utilizare | NC | NC | NC |
| SSM/SU România gata de utilizare | NC | NC | NC |

Licențe și activitate: [Frappe — licență](https://raw.githubusercontent.com/frappe/hrms/develop/license.txt), [release-uri](https://github.com/frappe/hrms/releases); [Axelor — licență](https://raw.githubusercontent.com/axelor/axelor-open-suite/master/LICENSE), [release-uri](https://github.com/axelor/axelor-open-suite/releases); [OFBiz — licență](https://github.com/apache/ofbiz-framework/blob/trunk/LICENSE), [descărcări și mentenanță](https://ofbiz.apache.org/download).

**Matrice funcțională HR**

| Funcție | iDempiere standard | Frappe HR | Axelor HR | OFBiz HR |
|---|---|---|---|---|
| Dosar personal dedicat HR | Parțial | Da | Da | Da |
| Departamente și poziții HR | Parțial/configurare | Da | Da | Da |
| Istoric profesional și calificări | Extensie | Da | Da/parțial | Da |
| Evidență relație de muncă | Extensie | Da; adaptare locală | Da; contracte | Da |
| CIM și acte adiționale românești | De construit | De adaptat | De adaptat | De adaptat |
| Recrutare și candidați | Extensie | Da | Da | Da |
| Interviuri și feedback structurat | Extensie | Da | Flux de recrutare; detalii de verificat | NC |
| Onboarding/offboarding | Extensie | Da | Parțial | NC |
| Transferuri și promovări | Extensie | Da | Parțial | Parțial |
| Concedii | Extensie | Da | Da | Da |
| Politici și solduri de concediu | Extensie | Da | Da | Acoperire de verificat |
| Înregistrări de prezență/check-in | Extensie | Da | Acoperire de verificat | NC |
| Conectare dispozitive de pontaj | Extensie | Documentată | NC | NC |
| Ture și repartizarea lor | Extensie | Da | Planificări; echivalența de verificat | NC |
| Ore pe proiect | Da | Da, în configurația corespunzătoare | Da | Prin Project Manager |
| Ore suplimentare | Extensie HR | Da, în funcție de versiune/configurare | Da | NC |
| Deconturi și avansuri | Da/parțial | Da | Da pentru cheltuieli | În ecosistem; fluxul de verificat |
| Evaluarea performanței | Extensie | Da | Da | Da |
| Competențe și instruire | Extensie | Da | Da | Da |
| Acces al angajatului pentru cereri | De configurat/extins | Da | Da | NC pentru experiență comparabilă |
| Utilizare HR mobilă | Extensie | PWA | Aplicație mobilă; ediția de verificat | NC |
| Motor de calcul salarial configurabil | Extensie | Da | Pregătire/export payroll | Componente; flux complet de verificat |
| Fluturași generați din calcul | Extensie | Da | Nu deduc din „Payroll Preparation” | De verificat |
| Bonusuri/beneficii | Extensie | Da, configurabile | Da | Da |
| Contabilizarea salariilor | După extensie | În configurația integrată cu contabilitatea | În funcție de integrarea payroll | De configurat |
| D112 și integrare REGES-ONLINE | NC | NC | NC | NC |
| Documente SSM/SU românești | NC | NC | NC | NC |

Pentru Frappe, acoperirea este descrisă în [manualul HR](https://docs.frappe.io/hr/introduction), [recrutare](https://docs.frappe.io/hr/recruitment), [ture](https://docs.frappe.io/hr/shift-management), [calcul salarial](https://docs.frappe.io/hr/payroll-setup) și [procesarea salariilor](https://docs.frappe.io/hr/payroll-entry). Pentru Axelor: [manualul HR](https://docs.axelor.com/aos/en/category/rh/), [contracte și dosar](https://docs.axelor.com/aos/en/8.0/aos/RH/employe_file/), [instruire/evaluare](https://docs.axelor.com/aos/en/aos/RH/training/). Pentru OFBiz: capitolele HR, Project Manager și integrare din [manualul oficial](https://nightlies.apache.org/ofbiz/stable/ofbiz/html5/user-manual.html).

**Diferența salarială care poate schimba alegerea**

Frappe documentează un circuit efectiv: componente și formule → structură salarială → fluturași → procesare colectivă → înregistrări contabile. Regulile pentru România rămân de implementat și validat. [Payroll Setup](https://docs.frappe.io/hr/payroll-setup), [Salary Slip](https://docs.frappe.io/hr/salary-slip).

Axelor documentează **pregătirea datelor pentru salarizare**, inclusiv concedii, ore suplimentare, bonusuri și tichete, apoi exporturi precum Standard/Nibelis/Silae. Aceasta nu dovedește un motor complet de salarizare românească. [Payroll Preparation](https://docs.axelor.com/aos/en/aos/RH/tickets/).

La Axelor trebuie verificată și delimitarea Community–comercial: existența unei funcții în documentația generală nu garantează că fiecare componentă, serviciu sau instrument de migrare este inclus gratuit în distribuția aleasă. [Ediții](https://axelor.com/pricing/), [clarificare privind Community și migrările](https://forum.axelor.com/t/clarifcation-on-community-versions/6243).

**Clasamentul meu pentru utilizarea alături de iDempiere**

| Loc | Soluție | Justificare |
|---|---|---|
| **1** | **Frappe HR** | Prima de testat dacă doriți o aplicație HR separată: funcții HR bine documentate și un circuit salarial configurabil |
| **2** | **Axelor HR** | Prima alternativă separată în Java; potrivită pentru administrare HR, timp și cheltuieli, cu atenție la payroll și ediții |
| **3** | **OFBiz HR** | Mai potrivit dacă echipa dorește să construiască și să adapteze o soluție Java decât să adopte rapid un HR modern |

Acest clasament este evaluarea mea pentru arhitectura voastră. **Nu este o garanție de stabilitate și nu înlocuiește testarea versiunilor alese.**

---

**5. Comparația platformelor românești SSM/SU**

Am comparat **SSM.ro, SSMatic.ro și SafeHub**. Acestea nu sunt echivalente cu cele trei proiecte HR open-source: sunt servicii comerciale, iar condițiile gratuite, semnăturile și accesul la integrare diferă.

| Funcție / criteriu | SSM.ro | SSMatic.ro | SafeHub |
|---|---|---|---|
| Orientare România | Da | Da | Da |
| Cod sursă public open-source | Neidentificat | Neidentificat | Neidentificat |
| Gratuit integral, inclusiv semnături | Nu rezultă | Nu; semnături contra cost | Nu rezultă |
| Companii și angajați | Da | Declarat | Declarat |
| Departamente/posturi/grupuri | Documentate | Acoperire de verificat | Declarat |
| Instruire SSM | Documentată | Declarată | Declarată |
| Instruire SU | Documentată | Acoperire exactă de verificat | Declarată |
| Instruire periodică/suplimentară | Documentată | De verificat în demo | Declarată |
| Materiale și teste | Documentate | Declarate | Declarate |
| Generare documente | Documentată | Declarată | Șabloane declarate |
| Șabloane proprii | DOCX și variabile | De verificat | Declarate |
| Semnătură electronică | Opțiuni documentate | Serviciu plătit | AES/OTP declarat |
| Scadențe și notificări | Da | Declarate | Declarate |
| Evidență documente nesemnate | Inclusiv raport API | NC | De verificat |
| Evaluare completă de risc | Nu rezultă din simpla generare de fișe | Generare declarată; metodologia de verificat | NC |
| Medicină a muncii / aptitudini | Acoperire exactă de verificat | NC | Declarat |
| Echipament individual de protecție | Acoperire de verificat | NC | Declarat |
| Incidente / near-miss | Acoperire de verificat | NC | Declarat |
| Scadențe PRAM/ISCIR/echipamente PSI | Acoperire de verificat | NC | Declarat |
| Import angajați | Documentat | De verificat | Excel declarat |
| API public documentat | **Da** | **Neidentificat** | **Neidentificat pentru integrare HR generală** |
| Integrare Microsoft 365 | NC | NC | Declarată |
| Instalare proprie cu sursă disponibilă | Nu rezultă | Nu rezultă | Nu rezultă |
| Manual public detaliat | **Da** | Nu am identificat unul comparabil | Nu am identificat unul comparabil |

Pentru SSM.ro, funcțiile sunt susținute de [ghidul de utilizare](https://ghid.ssm.ro/docs), [generatoarele de documente](https://ghid.ssm.ro/docs/02-ghiduri/utilizator/generatoare-documente), [FAQ](https://www.ssm.ro/intrebari-frecvente) și [documentația API](https://ghid.ssm.ro/docs/03-api). Pentru SSMatic, sursele sunt [prezentarea funcțională](https://www.ssmatic.ro/) și [condițiile comerciale](https://www.ssmatic.ro/preturi). Pentru SafeHub, matricea reflectă [funcțiile declarate de furnizor](https://safehub.ro/) și [oferta comercială](https://safehub.ro/preturi/).

**Ce diferențiază efectiv cele trei**

| Platformă | Motiv principal de evaluare | Ce nu este încă demonstrat |
|---|---|---|
| **SSM.ro** | Documentație operațională și API public, utile pentru integrare | Exportul automat complet al tuturor documentelor și stărilor necesare vouă |
| **SSMatic** | Oferta gratuită declarată pentru gestiune/documente | Limitele exacte, costul semnăturilor, API-ul și procedura completă de export |
| **SafeHub** | Acoperire declarată mai largă a activităților HSE și integrare Microsoft | API general de angajați/documente și accesul contractual la acesta |

SSMatic publică o ofertă gratuită pentru anumite utilizări, însă semnăturile sunt tarifate separat. Pagina consultată conține prezentări de preț care merită clarificate contractual înainte de calcularea costului total. [Prețuri SSMatic](https://www.ssmatic.ro/preturi).

**Niciuna nu trebuie considerată automat „100% conformă pentru orice firmă”.** Conformitatea depinde și de riscurile locurilor de muncă, documentele întocmite, instruirea efectivă, responsabilități și măsurile implementate. Software-ul poate administra și documenta aceste procese; nu le îndeplinește singur. Cadrul relevant include [Legea 319/2006](https://legislatie.just.ro/Public/DetaliiDocument/73772), [Ordinul 712/2005](https://legislatie.just.ro/Public/DetaliiDocumentAfis/63056) și [Ordinul 163/2007](https://legislatie.just.ro/Public/DetaliiDocument/80730).

De asemenea, **SU/PSI în aplicație nu înseamnă obținerea automată a unei autorizații ISU**.

---

**6. Comparația documentelor și rezultatelor concrete**

Pentru selecție, este util să verificați documentele produse, nu doar denumirile modulelor.

| Document / rezultat | iDempiere standard | HR independent sau plugin HR | Platformă SSM/SU |
|---|---|---|---|
| Fișă de angajat | Date de bază | Dosar HR extins | Date necesare SSM |
| Contract individual de muncă românesc | De construit | Șablon și logică locală de verificat | Unele platforme generează contracte; tipul exact trebuie verificat |
| Act adițional / decizie HR | De construit | Configurare/localizare | În funcție de șabloane |
| Cerere de concediu | Extensie | Funcție HR | Nu este funcția principală |
| Situație sold concediu | Extensie | Funcție HR | Nu este funcția principală |
| Pontaj lunar | Ore pe proiect, parțial | Attendance + reguli locale | Nu înlocuiește sistemul HR |
| Stat de plată românesc | Extensie/localizare | Motor + localizare | Nu |
| Fluturaș salarial | Extensie | Frappe documentat; ceilalți de verificat | Nu |
| D112 | Neconfirmat | Neconfirmat în candidații analizați | Nu |
| Transmitere REGES-ONLINE | Neconfirmat | Neconfirmat | Nu rezultă din importul de angajați |
| Fișă individuală de instruire SSM | De construit | Nu rezultă gata adaptată | Funcție de verificat pe platformă |
| Fișă de instruire SU | De construit | Nu rezultă gata adaptată | Funcție de verificat pe platformă |
| Tematică de instruire / test | De construit | Instruire generică | Funcție specializată |
| Instrucțiuni proprii SSM | Documente atașate | Documente/configurare | Șabloane sau documente proprii |
| Evaluare de risc | De construit | Nu rezultă modul RO complet | Verificare metodologie și conținut |
| Plan de prevenire și protecție | De construit | Nu rezultă gata adaptat | De verificat pe document concret |
| Fișă de aptitudine | Atașament/configurare | Evidență posibilă | Evidență/scadență în unele platforme |
| Proces-verbal de predare EIP | De construit | Extensie | De verificat; SafeHub declară evidență EIP |
| Dosar de accident de muncă complet | Neconfirmat | Neconfirmat | Nu trebuie dedus din simpla existență a modulului „Incidente” |
| Document semnat + dovadă de semnare | Integrare suplimentară | Integrare suplimentară | Depinde de serviciu și tipul semnăturii |

SSM.ro documentează explicit generatoare pentru decizii, declarații, contracte, tematici, fișe de instruire și testări. Acest lucru susține existența generatorului, dar nu validează automat fiecare șablon pentru situația voastră. [Generatoare de documente](https://ghid.ssm.ro/docs/02-ghiduri/utilizator/generatoare-documente).

**Un import denumit „Revisal” într-un manual nu dovedește o integrare actuală REGES-ONLINE.** Aceasta trebuie demonstrată separat, cu fluxul și interfața efectiv utilizate.

---

**7. Documentații, surse și descărcări pentru toate soluțiile**

Am separat **manualele**, **codul/instalatoarele** și **paginile comerciale**. Nu am identificat un manual PDF integral public pentru fiecare produs; unde există doar HTML, îl indic ca atare.

**iDempiere și extensiile sale**

| Produs | Documentație | Descărcare / sursă | Observație |
|---|---|---|---|
| iDempiere | [Portal documentație](https://docs.idempiere.org/), [manual](https://wiki.idempiere.org/en/Manual), [referință funcțională](https://wiki.idempiere.org/en/Reference) | [GitHub](https://github.com/idempiere/idempiere), [instalatoare](https://wiki.idempiere.org/en/Downloading_Installers), [fișiere SourceForge](https://sourceforge.net/projects/idempiere/files/) | Alegeți release stabil, nu automat cel mai recent fișier „Dev” |
| CDSoftware Payroll | [Ghid funcțional](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_Payroll) | Secțiunea **Sources** din pagină trimite la Bitbucket | Descărcarea/build-ul trebuie reverificate |
| CDSoftware Attendance | [Descriere și surse](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_Attendance) | Link Bitbucket în pagină | Testare publicată pe 10 |
| CDSoftware Training | [Descriere și dependențe](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_EmployeeTraining) | Link Bitbucket în pagină | Nu este un manual SSM românesc |
| CDSoftware Recruitment | [Descriere și dependențe](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_EmployeeRecruitment) | Link Bitbucket în pagină | Documentație publică redusă |
| CDSoftware PayrollReport | [Funcții și configurare](https://wiki.idempiere.org/en/Plugin%3A_CDSoftware_PayrollReport) | Link Bitbucket în pagină | Rapoarte/exporturi |
| AMERPSOFT Payroll | [README modul](https://github.com/luisamesty/Amerpsoft-iDempiere-community/blob/master/org.amerpsoft.com.idempiere.personnelpayroll/README.md) | [Repository](https://github.com/luisamesty/Amerpsoft-iDempiere-community) | Verificați ramura și dependențele |
| AMERPSOFT — PDF | [README în PDF](https://github.com/luisamesty/Amerpsoft-iDempiere-community/blob/master/README.pdf), [prezentare Payroll PDF](https://wiki.idempiere.org/w-en/images/5/53/PayrollPluginNomina_EN_Luis_Amesty.pdf) | PDF disponibil | Prezentarea este istorică, nu garanție pentru versiunea actuală |
| iDempiere REST | [Documentație API](https://bxservice.github.io/idempiere-rest-docs/) | [Plugin GitHub](https://github.com/bxservice/idempiere-rest) | Compatibilitatea se verifică pe ramura aleasă |

Unele pagini wiki au putut fi citite prin indexarea publică, dar accesul direct automatizat a returnat 403. Prin urmare, **nu prezint toate legăturile Bitbucket drept descărcări testate**.

**Cele trei aplicații HR**

| Produs | Manuale funcționale | Documentație tehnică | Descărcare și PDF |
|---|---|---|---|
| **Frappe HR** | [Manual complet navigabil](https://docs.frappe.io/hr/introduction), [angajați](https://docs.frappe.io/hr/employee), [recrutare](https://docs.frappe.io/hr/recruitment), [ture](https://docs.frappe.io/hr/shift-management), [payroll](https://docs.frappe.io/hr/payroll-setup) | [REST API](https://docs.frappe.io/framework/user/en/api/rest), [webhooks](https://docs.frappe.io/framework/v14/user/en/guides/integration/webhooks) | [Cod](https://github.com/frappe/hrms), [release-uri](https://github.com/frappe/hrms/releases). Documentația are **Download this page as a PDF**, pe pagină |
| **Axelor HR** | [Index HR](https://docs.axelor.com/aos/en/category/rh/), [recrutare](https://docs.axelor.com/aos/en/aos/RH/job_offer/), [dosar](https://docs.axelor.com/aos/en/aos/RH/employe_file/), [training](https://docs.axelor.com/aos/en/aos/RH/training/), [pregătire payroll](https://docs.axelor.com/aos/en/aos/RH/tickets/) | [Portal tehnic](https://docs.axelor.com/), [web services](https://docs.axelor.com/adk/7.4/dev-guide/web-services/index.html) | [Cod suită](https://github.com/axelor/axelor-open-suite), [modul HR](https://github.com/axelor/axelor-open-suite/tree/master/axelor-human-resource), [aplicație web](https://github.com/axelor/open-suite-webapp), [release-uri](https://github.com/axelor/axelor-open-suite/releases). PDF integral oficial neidentificat |
| **Apache OFBiz** | [Manual utilizator HTML](https://nightlies.apache.org/ofbiz/stable/ofbiz/html5/user-manual.html) | [Manual dezvoltator PDF](https://nightlies.apache.org/ofbiz/stable/ofbiz/pdf/developer-manual.pdf) | **[Manual utilizator PDF](https://nightlies.apache.org/ofbiz/stable/ofbiz/pdf/user-manual.pdf)**, [software](https://ofbiz.apache.org/download), [cod](https://github.com/apache/ofbiz-framework) |

**Atenție la versiunea documentației:** paginile Axelor consultate includ versiunea 8.5, în timp ce repository-ul are release-uri 9.1.x. Manualele OFBiz de la adresa `stable` sunt actualizate în timp. Pentru implementare, documentația trebuie arhivată împreună cu versiunea exactă aleasă.

**Cele trei platforme SSM/SU**

| Produs | Documentație disponibilă | Integrare | Download / acces |
|---|---|---|---|
| **SSM.ro** | [Portal ghid](https://ghid.ssm.ro/docs), [primii pași](https://ghid.ssm.ro/docs/02-ghiduri/utilizator/primii-pasi), [introducere angajați](https://ghid.ssm.ro/docs/02-ghiduri/utilizator/introducere-date-angajati), [generatoare documente](https://ghid.ssm.ro/docs/02-ghiduri/utilizator/generatoare-documente) | [API](https://ghid.ssm.ro/docs/03-api), [autentificare](https://ghid.ssm.ro/docs/03-api/autentificare), [rapoarte](https://ghid.ssm.ro/docs/03-api/rapoarte), [exemplu Node.js](https://ghid.ssm.ro/docs/03-api/exemple-implementare/nodejs) | Serviciu comercial; [ofertă](https://www.ssm.ro/oferta). Nu am identificat cod sursă sau manual PDF integral public |
| **SSMatic.ro** | [Prezentare funcții](https://www.ssmatic.ro/), [prețuri și limite](https://www.ssmatic.ro/preturi) | API public neidentificat | Aplicație online; nu am identificat instalator, cod sursă sau manual tehnic public complet |
| **SafeHub** | [Prezentare funcții](https://safehub.ro/), [ofertă](https://safehub.ro/preturi/) | Integrări descrise comercial; API general neidentificat | Serviciu online; nu am identificat cod sursă sau manual PDF integral public |

Pentru ultimele două, paginile de prezentare **nu sunt echivalente cu o documentație tehnică**. Accesul la manual, API și exporturile complete trebuie inclus în evaluarea furnizorului.

---

**8. Integrarea în Frappe sau direct în iDempiere: ce are sens**

**Da, integrarea are sens**, dacă fiecare aplicație are un rol clar și nu se întrețin manual aceleași date în trei locuri.

| Date / proces | Sistem principal recomandat | Ce se transmite |
|---|---|---|
| Companii și centre de cost | iDempiere | Identificatori și structură |
| Dosar angajat | Un singur HR: plugin iDempiere **sau** Frappe | Date necesare celorlalte sisteme |
| Concedii, ture, pontaj | Sistemul HR ales | Rezultate validate |
| Calcul salarial | Motorul localizat ales | Înregistrări contabile către iDempiere |
| Instruire SSM/SU | Platforma specializată | Stare, scadență, referință document |
| Documente semnate | Platforma SSM și arhiva stabilită | Documente finale și dovezi disponibile |
| Cheltuieli și contabilitate | iDempiere | Date financiare aprobate |

**Varianta A — păstrați HR în iDempiere**

```text
iDempiere + o familie de extensii HR
                 │
          conector de integrare
                 │
       platformă SSM/SU România
```

Avantaje estimate: mai puține aplicații și mai puține sincronizări. Costul principal se mută în compatibilizarea pluginurilor, completarea funcțiilor lipsă și localizarea românească.

**Varianta B — Frappe HR ca aplicație specializată**

```text
Frappe HR ── conector ── iDempiere
    │
    └────── conector ── platformă SSM/SU
```

Avantaje estimate: funcțiile HR și interacțiunea cu angajații pot fi adoptate mai repede. În schimb, trebuie administrate explicit sincronizarea, erorile, drepturile și versiunea fiecărei aplicații.

Frappe oferă REST și mecanisme de webhook, iar iDempiere are un plugin REST documentat. Acestea sunt elemente pentru construirea integrării; **nu am identificat un conector gata de utilizare pentru întregul circuit propus**. [Frappe REST](https://docs.frappe.io/framework/user/en/api/rest), [webhooks](https://docs.frappe.io/framework/v14/user/en/guides/integration/webhooks), [iDempiere REST](https://github.com/bxservice/idempiere-rest).

**Ce se poate demonstra acum pentru SSM.ro**

| Operațiune | Situație în documentația publică |
|---|---|
| Autentificare API | Documentată, cu token |
| Identificare angajat/contact după marcă | Documentată |
| Creare și actualizare date | Documentate |
| Raport documente în așteptarea semnării | Documentat |
| Descărcare automată a tuturor PDF-urilor semnate | Neconfirmată pentru întregul necesar |
| Istoric complet instruiri și rezultate teste | Acoperirea API trebuie verificată |
| Webhook pentru fiecare document finalizat | Neconfirmat |
| Export integral la încetarea contractului | De verificat contractual și tehnic |

Raportul public documentat include `draft_signatures`; nu rezultă de aici că API-ul oferă automat toate documentele și toate stările. [API SSM.ro](https://ghid.ssm.ro/docs/03-api), [rapoarte API](https://ghid.ssm.ro/docs/03-api/rapoarte).

La SSMatic și SafeHub, integrarea poate fi realizabilă, dar **nu o pot confirma integral din documentația publică găsită**. Importul Excel sau integrarea Microsoft 365 nu demonstrează singure existența unui API HR complet.

---

**9. Ce aș alege și ce aș verifica înainte de decizie**

| Prioritatea voastră | Prima opțiune de evaluat | Motiv |
|---|---|---|
| Totul cât mai aproape de iDempiere | **CDSoftware HR/Payroll** | Cea mai largă familie nativă documentată dintre cele găsite |
| Alternativă nativă de salarizare | **AMERPSOFT Payroll** | Adaptări declarate pentru versiuni mai recente |
| HR separat, cu funcții bogate | **Frappe HR** | Cea mai potrivită primă probă funcțională pentru acest scenariu |
| Aplicație HR separată obligatoriu Java | **Axelor HR** | Funcții HR documentate și platformă Java |
| Dezvoltare amplă pe o bază Java | **OFBiz** | Potrivit când acceptați un proiect mai mare de adaptare |
| SSM/SU cu integrare documentată | **SSM.ro** | API și ghid public |
| SSM cu ofertă de bază gratuită | **SSMatic** | De verificat limitele și costul total |
| SSM/HSE cu evidențe operaționale mai largi | **SafeHub** | De verificat în demo și prin acces la integrare |

Pentru voi, **nu aș decide după numărul de funcții de pe site**. Aș cere fiecărei variante să treacă aceleași probe:

| Probă | Rezultat concret de cerut |
|---|---|
| Instalare și upgrade | Build reproductibil pe versiunea aleasă, fără erori de migrare |
| Angajare | Dosar, organizație, manager, documente și transfer către SSM |
| Schimbare de post | Istoric corect și actualizarea obligațiilor de instruire |
| Pontaj dificil | Tură peste miezul nopții, lipsă pontare, corecție, concediu, ore suplimentare |
| Salarizare | Calcul comparat cu rezultatul validat pentru cazuri românești relevante |
| Decont | Aprobare și înregistrare contabilă fără dubluri |
| Instruire SSM/SU | Material, test, semnături, fișă finală și scadență următoare |
| Export | Dosar complet recuperabil și lizibil în afara platformei |
| Încetare contract | Dezactivare acces și păstrarea istoricului |
| Eroare de integrare | Reluare fără dublarea angajatului sau documentului |

**Recomandarea mea de pornire este un pilot comparativ CDSoftware versus Frappe HR, folosind iDempiere ca sistem financiar și SSM.ro ca prim candidat de integrare documentată.** AMERPSOFT merită evaluat separat pentru payroll. Salarizarea românească și documentele SSM/SU trebuie tratate ca cerințe explicite de acceptanță, nu presupuse din existența unui modul „Payroll” sau „Training”.

## Utilizator

SUB FORMA DE DOCUMENT - si descarca in subfoldere si anexe totul pregatit de utilizare :

realizeaza o analiza completa si complexa cu toate functionalitatile actuale din Idempiere
ce ofera cele trei programe de HR si ce ofera programele de SSM/SU
compara tabe;lar clar module/functii documenteaza cu linkuri de download a tuturor documentatiilor pentru fiecare din cele 3 + 3 - de unde se poate vedea clar ce si cum ofera
Cauta si module de iDempiere suplimentare deja existente oriund ein lume legate de HR - care sa dezvolte ceea ce are deja implicit iDempiere


## Asistent

Voi pregăti un dosar cu raportul comparativ, tabelele, documentațiile publice descărcabile și anexele tehnice, organizate pe produse. Voi marca separat documentele istorice, informațiile neconfirmate și materialele care necesită acces de la furnizor. Folosesc instrucțiunile pentru documente Word și PDF ca să verific și lizibilitatea fișierelor finale.


## Asistent

Le dossier distinguera les fonctions standard, les extensions et les adaptations nécessaires pour la Roumanie. Je préparerai aussi un registre des sources indiquant, pour chaque annexe, son origine, sa date de récupération et son état de téléchargement. Le partage réseau n’est pas accessible depuis la session actuelle ; je construis le dossier localement, puis je retenterai la copie à l’emplacement demandé.


## Utilizator

NU IN FRANCEZA !!

totul trebuie si pe local DAR si push in github documentatie
gasesti cheia intr-un fisier pe c:\... 
am generat cheia intr-o conversatie din acest proiect si a fost salvata local 


## Asistent

Îmi cer scuze pentru mesajul în franceză. Raportul, anexele redactate și indexul dosarului vor fi în română; documentațiile originale descărcate își vor păstra limba sursei.

Voi salva dosarul local și voi publica documentația în repository-ul GitHub al proiectului. Caut mai întâi configurația repository-ului și conversația relevantă pentru a identifica fișierul cheii, fără să afișez sau să includ cheia în documente ori în commit.


## Asistent

Am identificat cheia și repository-ul `cesiroproduction/Eva-Accounting`. Accesul SSH și accesul la folderul local al proiectului funcționează acum. Voi publica dosarul într-un subfolder distinct din `Documentatie`, pe ramura de documentație existentă, păstrând celelalte biblioteci.


## Asistent

Am descărcat 238 de materiale și pagini de documentație. Verificarea codului iDempiere a adus o corecție importantă față de comparația inițială: baza include deja poziții, atribuiri și evidențe de remunerație, precum și modele de date HR. Le voi separa în raport de funcțiile operaționale care necesită extensii. Unele pagini wiki refuză descărcarea; acestea vor fi marcate ca indisponibile, nu ca anexe recuperate.


## Asistent

Raportul include acum comparația pe funcții și documente, plus două variante de integrare: HR nativ în iDempiere sau Frappe HR separat. Pregătesc și anexele de lucru: cerințe de completat, scenarii de test, întrebări pentru furnizorii SSM/SU și un inventar tehnic al bazei iDempiere, cu versiunea de cod verificată.


## Asistent

Raportul PDF este generat și verific tabelele pagină cu pagină. Descărcarea extinsă a ghidului SSM.ro a confirmat și module pentru accidente, audituri, indicatori HSE, arhivare externă și SSO; le-am adăugat în comparație. Urmează verificarea legăturilor locale și a integrității fișierelor, apoi copierea și push-ul.


## Asistent

Raportul final are 28 de pagini, iar biblioteca include 308 surse descărcate. Verific acum fișierele și legăturile, apoi salvez pachetul în folderul proiectului și îl public în GitHub. Cele 20 de încercări de descărcare nereușite vor fi evidențiate separat, cu alternativele găsite.


## Asistent

Verificările au trecut: 482 de legături locale valide, integritatea surselor confirmată și arhiva ZIP verificată. Pachetul conține și fișe de cerințe, scenarii de acceptanță și întrebări pentru furnizori.

Concluzia importantă: există opțiuni HR gratuite și extensii reale pentru iDempiere, dar nu am confirmat o soluție SSM/SU complet gratuită care să acopere demonstrabil toate obligațiile firmei în România.


## Asistent

Pachetul este salvat în folderul local al proiectului; am verificat că toate fișierele copiate sunt identice cu cele pregătite. Public acum aceeași documentație în repository-ul `cesiroproduction/Eva-Accounting`, în subfolderul dedicat din `Documentatie`, pe ramura folosită deja pentru documentațiile ERP.


## Asistent

Am finalizat documentația **în română**, salvată local și publicată în GitHub.

- **Raport de 28 de pagini:** comparații iDempiere, 3 aplicații HR, 3 soluții SSM/SU, extensii HR și opțiuni de integrare.
- **308 surse descărcate**, organizate în subfoldere, plus anexe de evaluare.
- Cele **20 de descărcări nereușite** sunt identificate explicit, cu alternativele disponibile.

**Acces:**

- [Deschide biblioteca locală](Z:/00.Roboti/iDempiere/Analiza_iDempiere_HR_SSM_SU_2026-10-08/INDEX.html)
- [Descarcă pachetul ZIP local](Z:/00.Roboti/iDempiere/Analiza_iDempiere_HR_SSM_SU_2026-10-08.zip)
- [Documentația publicată în GitHub](https://github.com/cesiroproduction/Eva-Accounting/tree/808f976f6904829ab3cbbde7dbd0ac006cef0574/Documentatie/Analiza_iDempiere_HR_SSM_SU_2026-10-08)

Push confirmat: `808f976`. Fișierele publicate sunt identice cu livrarea locală. Documentațiile originale păstrează limba autorilor; analiza și anexele create sunt în română.

:codex-file-citation{path="C:/Users/User/.codex/visualizations/2026/10/08/01a11ac9-7ce0-7481-87a6-870f72ae1107/Analiza_iDempiere_HR_SSM_SU_2026-10-08/01_Raport/Analiza_iDempiere_HR_SSM_SU.pdf" purpose="output"}

## Utilizator

Creaza un tabel excel clar comparativ cu capitole / functii - si coloane cu toate softurile / modulele - versiunile gasite cu bifa au sa nu sau partial  


## Asistent

Voi crea un Excel cu funcțiile grupate pe capitole și câte o coloană pentru fiecare aplicație sau modul analizat, cu versiunea identificată. Voi marca distinct „Da”, „Parțial”, „Nu” și „Neconfirmat”, pentru a nu confunda lipsa documentației cu lipsa funcției. Îl voi salva local și în GitHub, alături de raport.


## Asistent

Folosesc skill-ul Spreadsheets pentru fișierul Excel. Tabelul va păstra distincția dintre funcțiile iDempiere standard, cele adăugate prin module și cele oferite de aplicații separate; această diferență contează pentru alegerea integrării.


## Asistent

Versiunile vor apărea în antetele coloanelor. Pentru serviciile SSM care nu publică un număr de versiune, voi indica data documentației; pentru extensii, voi separa versiunea iDempiere pe care au fost testate de compatibilitatea cu versiunea 13.


## Asistent

Am structurat comparația pe capitole și am inclus separat modulele HR native, aplicațiile externe și platformele SSM/SU. Fiecare evaluare va avea o explicație și sursele folosite într-o foaie de detalii, astfel încât o bifă bazată pe manual să poată fi deosebită de o declarație comercială.


## Asistent

Excelul va avea patru foi: comparația completă, produsele și versiunile, explicațiile cu surse și legenda. Antetul și coloanele cu funcțiile vor rămâne fixe la derulare, iar filtrele vor permite afișarea rapidă a unui capitol sau a funcțiilor disponibile într-un anumit produs.


## Asistent

Tabelul conține **119 funcții și criterii, în 12 capitole, pentru 24 de aplicații, module și dependențe**. Am inclus 1.230 de evaluări cu explicații și surse. Verific acum afișarea, filtrele și corespondența marcajelor înainte de salvarea locală și push-ul în GitHub.


## Asistent

Am păstrat în tabel diferențele de versiune găsite: Frappe HR are release-uri 16.50.0 și 15.64.3, Axelor are release 9.1.9 și documentație HR inclusiv pentru 8.5, iar AMERPSOFT declară iDempiere 12 în testare, deși manualul exemplifică încă un modul 11.0.0. Aceste diferențe sunt evidențiate pentru verificarea compatibilității.


## Asistent

Am verificat vizual toate cele patru foi. Marcajele sunt colorate distinct: verde pentru „Da”, galben pentru „Parțial”, roșu pentru „Nu” și gri pentru „Neconfirmat”. Urmează verificarea fișierului Excel salvat și actualizarea pachetului local și din GitHub.


## Asistent

Verificarea fișierului salvat a detectat o problemă la legăturile către documentații. O corectez înainte de publicare; conținutul comparației și marcajele au trecut verificările.


## Asistent

Verificările finale au trecut: toate cele 2.856 de marcaje corespund datelor comparației, iar cele 48 de legături directe către documentații sunt valide în fișier. Salvez acum Excelul și arhiva actualizată în folderul proiectului și în GitHub.


## Asistent

Am creat :codex-file-citation{path="C:/Users/User/.codex/visualizations/2026/10/08/01a11ac9-7ce0-7481-87a6-870f72ae1107/outputs/01a11ac9-7ce0-7481-87a6-870f72ae1107/Comparativ_iDempiere_HR_SSM_SU_2026-10-08.xlsx" purpose="output"} cu **119 funcții, 12 capitole și 24 de aplicații/module**, cu versiunile identificate în coloane.

Include filtre, antete fixe, explicații și surse. Marcajele sunt **✓ Da · ◐ Parțial · ✕ Nu · ? Neconfirmat · — N/A**.

Salvat și în folderul proiectului, sub `09_Comparativ_Excel`, și [publicat în GitHub](https://github.com/cesiroproduction/Eva-Accounting/commit/5779e2a19056262a980695ba03681969f1737f52). Arhiva ZIP este actualizată.

- :codex-followup[Prioritizează funcțiile]{prompt="Adaugă în Excel priorități configurabile pentru funcții și un clasament care separă funcțiile neconfirmate de cele absente."}
- :codex-followup[Estimează costurile]{prompt="Estimează costurile implementării și integrării pentru variantele recomandate, cu ipoteze explicite și costuri recurente separate."}
- :codex-followup[Detaliază integrarea]{prompt="Transformă diferențele identificate în Excel într-un backlog tehnic pentru integrarea iDempiere, HR și SSM/SU."}
