# Audit independent — Dracula Food

**Verdict: prima etapă nu poate fi declarată finalizată global la 10/10.** Fluxurile locale de demonstrație verificate trec auditul după remedierea problemelor găsite. Publicarea Cloudflare, catalogul extins cu imagini și activarea comercială rămân incomplete.

Audit efectuat independent la 25 septembrie 2026 pe `http://127.0.0.1:4183`, cu Playwright/Chromium, cereri HTTP directe, citirea surselor și inspecție SSH proprie a containerelor. Auditorul nu a modificat implementarea. Echipa de implementare a remediat constatările, apoi auditorul a repetat probele relevante pe versiunea desfășurată.

## Scoruri și dovezi

Un scor de 10/10 de mai jos înseamnă că toate probele enumerate pentru acel capitol au trecut în mediul local demo. Nu reprezintă certificare universală de securitate, accesibilitate sau conformitate juridică.

| Capitol | Scor / stare | Dovezi și limite |
|---|---|---|
| Aspect desktop și mobil | **10/10** | Pagina principală, colecția, produsul și contul verificate la 320, 390, 768 și 1440 px; fără depășire orizontală. Imaginile originale ale ambelor produse se încarcă la 1536×1024. |
| Navigare | **10/10** | Pagini produs din colecție și din coș, cont, favorite, checkout și footer funcționale; fără erori JavaScript în 95 de verificări din scriptul principal. |
| Categorii RO / EN / DE | **10/10** | Cele cinci categorii sunt traduse. Filtrele celor două categorii de stafide arată zero produse publicate; selecția generală arată două. Categorie nouă creată prin API admin apare public; după dezactivare dispare. Cămara raportează corect două produse în admin. |
| Catalogul celor două produse publicate | **10/10 pentru demo** | Nuci și alune de pădure, denumiri și descrieri RO/EN/DE, imagini originale, pagini proprii, prețuri marcate demonstrative. Valorile 49 și 59 RON nu sunt prețuri comerciale confirmate. |
| Catalog extins — 17 produse stafide | **4/10, incomplet** | Cele 17 propuneri există numai în fișierul editorial `dracula-food/food/raisin-drafts.json`, împărțite 10 + 7. Nu sunt produse introduse în baza de date; imaginile ambalajelor nu sunt generate. Prețurile, gramajele, stocurile și rețetele nu sunt confirmate. |
| Cont client și autentificare admin | **10/10 pentru accesul testat** | Conturile cerute de utilizator se autentifică; clientul își vede comenzile; logout invalidează accesul la profil. Panoul admin și secțiunile produse, categorii, comenzi, clienți, pagini legale, traduceri, solicitări, setări și utilizatori se deschid. |
| Recuperarea parolei / email | **BLOCAT** | SMTP și workerul de email nu sunt configurate pentru expedierea reală. Livrarea mesajelor de resetare și verificare nu poate primi 10/10. |
| Favorite | **10/10** | Adăugare, persistență după reîncărcare și eliminare verificate pentru clientul de test. Lista inițială de favorite a fost restaurată. |
| Coș | **10/10 în probele funcționale** | Adăugare produs, preț și legătură către produs corecte; cantitățile text, negative, fracționare, bool și obiect sunt respinse cu 400. Sincronizarea cu o linie invalidă respinge întregul set fără adăugări parțiale. Cantitățile întregi foarte mari sunt plafonate de motorul existent la 999 și produc avertisment de stoc. |
| Checkout demo | **10/10** | Comanda de audit `ORD-2026-000001` a fost înregistrată cu un produs de 49 RON și transport demo de 25 RON; total 74 RON. Apare în cont și admin. Stripe este blocat în demo cu 409. Totalul `NaN` este respins cu 400. Nu s-a inițiat nicio plată reală. |
| Admin CRUD și traduceri | **10/10 în operațiile verificate** | Creare/citire/modificare/ștergere produs QA draft; categorie QA și activare/dezactivare; cheie de traducere RO/EN/DE creată, servită în bootstrap DE și ștearsă. Datele QA de catalog au fost șterse definitiv după probe. Nu au fost testate integrările externe inactive. |
| Pagini footer — afișare | **10/10** | Toate cele 14 pagini în fiecare dintre RO/EN/DE: 42 de pagini accesibile, cu titlu și corp, fără variabile `{{…}}` nerezolvate. |
| Date juridice și pregătire comercială | **BLOCAT** | Textele sunt proiecte marcate ca atare. Identitatea juridică completă, adresa legală, datele de contact, prețurile/stocurile reale, condițiile de livrare și datele finale despre alimente lipsesc sau sunt neconfirmate. Nu este un magazin gata de vânzări reale. |
| Accesibilitate funcțională | **10/10 în probele executate** | Primul Tab găsește legătura către conținut; Enter focalizează `main`; câmpurile au etichete; butoanele iconice au nume; dialogul imaginii are numele produsului și se închide cu Escape; filtrele expun corect `aria-pressed`. Nu s-a efectuat un audit WCAG complet cu cititor de ecran. |
| Securitate funcțională | **10/10 în probele executate** | Client/anonim respinși de API admin cu 401; cereri fără CSRF sau cu origine străină respinse cu 403; cookie-ul clientului Food nu acordă acces la Design; cantități invalide și total nenumeric respinse. Este un audit funcțional, nu un test de penetrare exhaustiv. |
| Docker și izolarea celor două site-uri | **10/10** | Inspecție SSH proprie: Food backend/admin/db healthy; singurul port publicat al stackului este `127.0.0.1:4183`; PostgreSQL fără port host. Rețeaua `dracula-food_default` și volumul `dracula_food_pgdata` sunt distincte de `dracula-design_default` și `dracula_design_pgdata`. |
| Cloudflare / domeniu public HTTPS | **BLOCAT** | Overlay și script dedicate există. Conform verificării operative a echipei, tokenul nu este configurat și tunelul nu rulează. Nu există probă de rutare publică HTTPS, DNS sau certificat pe domeniul final. Pregătirea fișierelor nu echivalează cu publicarea. |

## Probleme găsite și reverificate după remediere

1. **Categorii dezactivate rămase publice.** O categorie QA cu `is_active:false` continua să apară în bootstrap. Remediat: după noul deploy, categoria activă apare și aceeași categorie dezactivată dispare.
2. **Contorul produselor din categorii afișa zero.** Cămara avea două produse publicate, dar admin afișa 0. Remediat și verificat: API admin raportează 2.
3. **Cantitate invalidă genera HTTP 500.** `POST /api/cart/items` cu CSRF valid și `qty:"invalid"` genera eroare internă; fracțiile și negativele erau convertite implicit. Remediat: toate tipurile invalide testate sunt respinse cu 400; sincronizarea nu lasă modificări parțiale.
4. **Dialogul imaginii nu avea nume accesibil.** Remediat: `aria-label` conține numele produsului.
5. **Filtrele comunicau selecția doar vizual.** Remediat: `aria-pressed` este adevărat exclusiv pe selecția curentă.
6. **Total nenumeric în checkout.** Verificarea de regresie confirmă respingerea `expected_total_ron:"NaN"` cu 400 înainte de crearea comenzii.

## Date de audit și artefacte

- `dracula-food/audit-evidence.json`: rezultate brute ale probelor inițiale și regresiei. Constatările inițiale sunt păstrate pentru trasabilitate; ultima regresie determină starea tehnică finală.
- `dracula-food/audit-mobile.png`: captură mobilă a colecției, cu ambele imagini încărcate.
- `dracula-food/audit-admin.png`: captură a administrării din audit.
- `VERIFICARE-DOCKER.md`: raportul operațional suplimentar al echipei, inclusiv starea Cloudflare și configurația demo.

Comanda demo rămâne în istoricul clientului, identificată prin observația „QA independent food audit; demo only”. Stocul demo de nuci a scăzut cu o unitate conform fluxului normal. Produsele și categoriile QA și cheia de traducere QA au fost eliminate; nu au fost modificate numele, imaginile sau prețurile celor două produse existente. Probe de coș vizitator pot lăsa în baza de date coșuri anonime necomandate, fără plăți sau rezervări comerciale.

**Condiție pentru acceptarea globală:** finalizarea catalogului extins dacă rămâne în prima etapă, livrarea emailurilor, completarea datelor comerciale/juridice și activarea/testarea independentă a domeniului prin Cloudflare. Auditorul nu acordă 10/10 global cât timp aceste puncte rămân blocate sau incomplete.
