# Audit independent — Dracula Design

Data: 25 septembrie 2026. Instanță verificată: `http://127.0.0.1:4181`, prin tunel SSH către serverul `192.168.100.151`. Auditorul nu a modificat implementarea. Au fost create o comandă demonstrativă și o solicitare de contact marcate QA; favoritele au fost restaurate, iar coșul de test a fost golit.

**Verdict intermediar: funcțiile principale ale magazinului demonstrativ sunt operaționale, dar acceptarea fără observații este amânată până la remedierea și retestarea celor trei defecte de mai jos. Publicarea comercială nu poate fi certificată fără configurațiile și datele reale.**

Scorurile reflectă verificările concrete din această rundă. Un 10/10 într-un capitol înseamnă că toate verificările descrise au trecut, nu că orice scenariu posibil a fost testat.

| Capitol | Scor | Dovezi și limite |
|---|---:|---|
| Aspect desktop și mobil | 10/10 | Verificare vizuală la 1440 px; mobil 390 px și tabletă 768 px fără depășire orizontală. Logo și cele cinci imagini existente sunt păstrate. Capturi `dracula-design-office/audit-desktop.png` și `audit-mobile.png`. |
| Navigare, categorii și catalog | 8/10 | Filtrele RO/EN/DE returnează Business 2, Esențiale 1, Feminin 2, Haine 0, Accesorii 5. Căutarea fără rezultat funcționează. Coloana numărului de produse din admin arată incorect 0 pentru toate categoriile. Categoria Haine este intenționat goală până la adăugarea produselor. |
| Limbi și conținut configurabil | 10/10 | RO/EN/DE: cinci produse, cinci categorii, 14 pagini fără corp/titlu gol și 183 chei de interfață. Schimbarea limbii păstrează pagina și actualizează URL-ul, textul și atributul HTML lang. Conținutul este furnizat din bootstrap DB; modulul admin Traduceri se încarcă. Adăugarea unei a patra limbi nu a fost repetată în această rundă. |
| Cont client și favorite | 10/10 | Contul de test se autentifică; favoritele se adaugă, persistă la reîncărcare și se pot elimina. Istoricul și detaliile comenzii proprii se afișează. Un client autentificat primește 401 la API-ul admin. Recuperarea parolei prin email rămâne blocată pentru verificare de livrare fără SMTP. |
| Coș și comandă demonstrativă | 10/10 | Adăugare, cantitate 1→2→1, cumpără acum și curățarea coșului verificate. Comandă `ORD-2026-000003` creată cu HTTP 201, `demo=true`, fără plată, total 1515 RON. Confirmarea și istoricul coincid. Preț diferit respins 409; lipsa acceptării termenilor respinsă 400. Idempotency este prezent în cod, dar nu a fost retrimisă comanda în această rundă. |
| Administrare și formulare | 8/10 | Login administrator reușit; Produse, Categorii, Comenzi, Clienți, Pagini legale, Traduceri, Solicitări, Setări și Utilizatori se încarcă. Contact QA salvat cu HTTP 201. Defectul numărului de produse afectează corectitudinea admin. Nu au fost schimbate roluri sau șterse înregistrări pentru audit. |
| DB, Docker și izolare | 10/10 | db/backend/admin healthy; migrare exit 0; zero restarturi automate. Rețea, volum, director de date și secrete distincte față de Food. PostgreSQL fără port public. Dovezi detaliate în `VERIFICARE-DOCKER.md`. Nu este audit de restaurare backup sau test de sarcină. |
| Securitate funcțională | 8/10 | API admin anonim/client 401; profil anonim 403; mutație fără CSRF 403; origine străină 403; sesiune HttpOnly și SameSite=Lax; Stripe în demo respins 409. Un tip invalid pentru totalul așteptat produce 500, necesitând validare. Cookie Secure este dezactivat doar în previzualizarea HTTP și activat de overlay-ul Cloudflare. Nu este test de penetrare exhaustiv. |
| Accesibilitate de bază | 8/10 | Primul Tab ajunge la skip-link; imaginile vizibile au alt; acțiunile cu pictograme au nume; modalul se închide cu Escape; focus vizibil și mesaje role alert/status. Modalul nu are nume accesibil, iar închiderea detaliilor comenzii are doar simbolul × dacă nu a fost deschisă anterior o imagine. Audit complet WCAG și cititor de ecran neefectuate. |
| Cloudflare, conținut juridic și lansare | BLOCAT | Configurațiile pentru tunel independent și HTTPS sunt pregătite; token absent, tunel nepornit. Cele 14 pagini sunt accesibile și marcate draft, însă firma nu are încă toate datele juridice/contact validate. Prețurile, stocurile, taxele, transportul și încasările sunt demonstrative. Lipsesc și configurația SMTP/validarea livrării email. |

## Defecte g?site ?i remediate ? istoric

1. **Număr incorect de produse în categorii admin.** Autentificare admin → Categorii. Business/Esențiale/Feminin/Accesorii indică 0, deși filtrele publice arată 2/1/2/5. Captură `dracula-design-office/audit-admin.png`. Sursa API citește câmpul `product_count` stocat fără a garanta actualizarea la asocierea produselor.
2. **Nume accesibil absent pentru modal.** Deschidere directă `/ro/account` după autentificare → Vezi detalii. `#image-dialog` are `aria-label=null`, `aria-labelledby=null`; butonul close are `aria-label=null`. Este necesar un nume pentru dialog și un text de închidere tradus în ambele utilizări, imagine și comandă.
3. **Total așteptat cu tip invalid produce HTTP 500.** Cu client autentificat, CSRF valid și un produs în coș, trimiterea unui checkout valid cu `expected_total_ron: {"invalid": true}` produce `internal_error`. Codul convertește direct cu `float(expected)`. Sunt necesare verificarea tipului, finitudinii și un răspuns de validare pentru valori neacceptate, inclusiv NaN/Infinity.

Nu au existat erori JavaScript sau HTTP 5xx în parcursul normal. Singurul HTTP 500 observat a fost cel provocat intenționat de verificarea tipului invalid.

## Limite și date de test

Comanda QA este demonstrativă și conține explicit „fără livrare, fără încasare”. Solicitarea de contact este „QA AUDIT DESIGN” și precizează că nu necesită răspuns. Nu s-au pornit plăți, emailuri sau curieri reali. Condițiile pentru operare publică nu sunt înlocuite cu un scor artificial de 10/10.

Stare retestare: în așteptarea remedierilor.


## Etap? suplimentar? ? fi?e detaliate, email local ?i protec?ia lans?rii

Verificare independent? pe instan?a actualizat?, 25 septembrie 2026, aproximativ 19:50 EEST.

| Verificare | Rezultat | Probe |
|---|---|---|
| Cinci produse ? trei limbi | PASS | Toate cele 15 fi?e RO/EN/DE au 2.7?3.1 mii de caractere, tabel tehnic, ?ngrijire, istorie documentat? cu linkuri, povestea m?rcii ?i dou? propuneri de ?inute/utilizare. Datele sunt primite din bootstrap DB; imaginile produselor coincid ?ntre limbi ?i cu catalogul anterior. |
| Afi?are fi?e | PASS | Layout desktop ?n dou? coloane; la 390 ?i 768 px, documentul nu dep??e?te viewportul, iar tabelele r?m?n ?n container. Capturi `dracula-design-office/audit-dossier-desktop.png` ?i `audit-dossier-mobile.png`, inspectate vizual. |
| Confirmare email din browser | PASS | Email EN capturat ?n Mailpit; linkul `/en/account?verify=...` consum? endpointul cu HTTP 200 ?i elimin? parametrul din URL. Reutilizarea tokenului este respins? cu 400. Tokenurile nu sunt incluse ?n raport. |
| Recuperare parol? din browser | PASS | Email EN capturat; formularul de resetare seteaz? parola nou?, iar loginul cu aceasta r?spunde 200. |
| Notific?ri de comand? | PASS | O singur? comand? nou?, `ORD-2026-000004`, `demo=true`, f?r? expediere sau ?ncasare. Confirmarea clientului EN ?i notificarea administratorului RO au ajuns ?n Mailpit. Ambele con?in Dracula-Company ?i Dracula-Castel; c?te dou? imagini inline; f?r? text CESIRO. |
| Date QA | PASS | Contul nou dedicat auditului a fost dezactivat prin API admin cu HTTP 200 la sf?r?it. Comanda este etichetat? explicit test/f?r? expediere/f?r? ?ncasare. Nu au fost trimise emailuri externe. |
| Servicii email Docker | PASS | Verificat separat prin SSH: backend, admin, db, mailpit ?i mail-worker healthy. Mailpit expune doar `127.0.0.1:4182`; SMTP r?m?ne ?n re?eaua Docker. |
| Validarea lans?rii comerciale | PASS ca protec?ie; lansare BLOCAT? | Executat read-only pe DB server: `ready=false`, cinci produse, f?r? cerere de activare. Sunt enumerate datele ?nc? lips? ?i confirm?rile pentru pre?/stoc/con?inut, fiscalitate, transport, metode de plat? ?i pagini juridice. |
| Regresie validator | PASS | Opt teste sintetice rulate independent pe sursele locale: activarea nu ocole?te datele lips?, schimbarea pre?ului cere reconfirmare, stocul demonstrativ nu este aprobat implicit, cheile de test nu aprob? procesarea live, valorile nefinite/negative sunt respinse, TVA explicit 0 este permis. |

Firma ?i adresa comunicate de utilizator sunt p?strate exact: **Dracula-Company**, **Dracula-Castel (Castelul-Dracula)**. Auditul nu solicit? ?nlocuirea lor. Lipsesc ?nc? CUI/num?r de ?nregistrare/telefon/email comercial ?i confirm?rile necesare oper?rii reale; acestea sunt distincte de identitatea deja aprobat?.

Limite: fi?ele public? explicit informa?iile tehnice ?nc? neconfirmate; linkurile de documentare sunt prezente, dar aceast? rund? nu reface verificarea istoric? a surselor. SMTP extern, livrarea la Gmail/Outlook, DNS, Cloudflare ?i ?ncas?rile reale nu au fost activate sau certificate. Testul email a acoperit EN pentru client ?i RO pentru notificarea administratorului; nu afirm? o reverificare a tuturor combina?iilor de ?abloane ?i limbi.

Nu au existat erori JavaScript sau r?spunsuri 5xx ?n parcursul normal al acestei etape. O indisponibilitate ini?ial? a tunelului local c?tre Mailpit a fost corectat? ?nainte de continuarea testului, f?r? a crea un al doilea cont sau o a doua comand?.

Observa?ie editorial? transmis? implementatorului: titlul RO al istoriei con?inea referire la ingrediente ?i pentru accesorii. Retestarea titlului corectat ?i a navig?rii Back/Forward ?ntre limbi este ?n a?teptarea ultimei public?ri locale.
