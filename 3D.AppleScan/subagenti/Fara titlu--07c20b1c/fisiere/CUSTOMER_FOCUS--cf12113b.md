# Clienții și problemele lor pe homepage

Specificație din 2 octombrie 2026, realizată de agentul de marketing la cererea managerului. Cerința finală pune tipurile de clienți în prim-plan, urmate de alegerea problemei. Două selectoare verticale răspund întrebărilor „Cine ești?” și „Ce problemă vrei să rezolvi?”. Activitățile concrete explică apoi cum ar putea fi folosită aplicația.

## Primul ecran

Etichetă: **PROIECTUL TĂU, NEVOILE TALE**

Titlu: **Găsește ce îți este util.**

Introducere: **Pentru profesioniști, proprietari și creatori: alege profilul tău și problema pe care vrei să o rezolvi. Găsește un exemplu util pentru proiectul tău.**

Primul selector oferă șase profiluri și opțiunea **Proiect personal / altă activitate**. Al doilea selector oferă probleme relevante din catalogul existent cu 36 de utilizări, deja tradus în șapte limbi. Opțiunea pentru proiect personal permite explorarea întregului catalog. Alegerea profilului trebuie să ajute orientarea; vizitatorul poate schimba oricând profilul pentru a vedea alte probleme.

Selecția problemei trebuie să conducă la un exemplu identificabil și o explicație a rezultatului. Platforma iPhone și starea „Aplicație în dezvoltare” rămân vizibile. Scenariile sunt utilizări propuse; nu sunt testimoniale sau rezultate validate ale aplicației native.

## Matricea clienților și activităților

| Client | Activitate | Ce încearcă să rezolve | Rezultatul planificat | Acțiunea pe site |
| --- | --- | --- | --- | --- |
| Arhitect | Proiectez un spațiu | Să înțeleagă geometria existentă înaintea modificărilor. | Referință cotată a camerelor, golurilor și legăturilor, de verificat și completat în proiectare. | Vezi fluxul de releveu; deschide planul DXF exemplu. |
| Designer de interior | Amenajez un interior | Să verifice mobilierul și spațiul de trecere înaintea propunerii către client. | Camera și dimensiunile relevante pentru instrumentul de proiectare ales. | Vezi scenariul de amenajare și exemplul dimensional. |
| Meșter sau renovator | Renovez sau repar | Să pregătească lucrarea cu dimensiuni și observații manuale. | Referință cotată pentru discuția despre lucrări și verificarea cotelor de montaj. | Încearcă exemplul de măsurare; vezi scenariul de renovare. |
| Creator 3D sau atelier | Creez un obiect 3D | Să pornească de la o formă existentă pentru o piesă, prototip sau imprimare. | Referință 3D cu dimensiuni, urmată de modelare și verificarea potrivirii și imprimabilității. | Vezi fluxul pentru obiecte; deschide exemplul STL sintetic. |
| Agent, proprietar sau administrator | Prezint o proprietate | Să explice dispunerea camerelor la vizionare, predare sau întreținere. | Plan cu camere conectate și dimensiuni de referință pentru discuții. | Vezi fluxul pentru camere; explorează utilizările imobiliare. |
| Artist, educator sau specialist în patrimoniu | Digitizez persoane sau obiecte | Să arate forma unui obiect, detaliu permis sau portret pentru o lucrare, lecție ori colecție. | Referință 3D pentru creație și învățare, cu verificarea capturii și a drepturilor. | Vezi obiectele și portretele; explorează utilizările creative. |

Profilurile nu limitează cine poate folosi un exemplu. Un proprietar poate amenaja, un profesor poate imprima un obiect, iar un artist poate documenta o cameră. Etichetele de activitate arată aceste posibilități fără să presupună o profesie obligatorie.

## Ordinea explicației după selecție

1. **Problema:** formularea concretă din catalog pe care o recunoaște vizitatorul.
2. **Activitatea:** ce vrea să facă, independent de profesie.
3. **Pașii:** trei acțiuni clare, separate în interfață.
4. **Rezultatul:** ce referință ar putea folosi și în ce etapă a proiectului.
5. **Exemplul:** demonstrație sau fișier sintetic accesibil imediat.
6. **Limita relevantă:** informația care schimbă folosirea rezultatului, lângă acesta.

Pentru atelier, limita relevantă privește potrivirea, toleranțele și imprimabilitatea. Pentru imobiliare, planul nu ține locul unei măsurători certificate. Pentru creator, sunt relevante acordul persoanei și drepturile de reutilizare. Aceste precizări nu trebuie să eclipseze nevoia și exemplul.

## Conținutul livrat

`content/customer-segments.json` conține șapte dicționare — EN, RO, DE, FR, ES, HU și BG — cu câte 27 de chei:

- 15 chei pentru cele trei profiluri noi: denumire, titlu, nevoie, trei pași și rezultat;
- 6 etichete de activitate, una pentru fiecare profil;
- 3 texte comune pentru titlu, introducere și etichetă;
- 3 etichete pentru cele două selectoare și opțiunea proiectului personal.

Sunt 189 de valori localizate. Textele pentru arhitect, designer și meșter rămân în sursa redesignului existent. Catalogul celor 36 de utilizări furnizează problemele. Fișierul nou nu duplică acele conținuturi. Acțiunile din matrice duc către exemple și pagini existente; nu presupun funcții noi de captură sau ofertare.

## Verificări de acceptare

- Selectorul profilului este înaintea selectorului problemei și a prezentării modulelor.
- Există șase profiluri și o alegere pentru proiect personal sau altă activitate.
- Problemele provin din catalogul tradus și se actualizează când profilul se schimbă.
- Selecția nu lasă o problemă incompatibilă ascunsă după schimbarea profilului.
- Rezultatul ales oferă nevoie, pași și exemplu; denumirea profesiei singură nu este suficientă.
- Cele șapte limbi au exact aceleași 27 de chei, fără valori goale.
- Fiecare valoare `Steps` conține trei pași și doi separatori `|`.
- Nu se promite scanare disponibilă acum, precizie certificată, fabricație automată sau calcul imobiliar oficial.
- Fiecare opțiune poate fi folosită cu tastatura, iar schimbarea limbii păstrează sau revalidează selecția prin identificatori stabili.

Verificarea structurală a dicționarelor este automatizabilă. Înțelegerea de către clienți necesită ulterior testare cu persoane reale; organizarea celor șase profiluri este o propunere de navigare a produsului.

## Starea sarcinii

Textele și matricea sunt livrate pentru integrarea de către manager. Au fost păstrate toate imaginile și identitatea aprobate. Agentul de marketing a modificat numai acest document și noul fișier de dicționare; nu a modificat codul site-ului.
