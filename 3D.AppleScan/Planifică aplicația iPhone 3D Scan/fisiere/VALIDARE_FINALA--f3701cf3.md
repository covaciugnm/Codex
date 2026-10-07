# Validarea livrării Site

Data: 2 octombrie 2026. Responsabil pentru integrare: managerul echipei.

## Rezultat

Site-ul rulează pe serverul Docker cu PostgreSQL persistent. O structură unică de pagini acoperă limbile en/de/fr/es/ro/hu/bg; `sp` este acceptat ca alias pentru spaniolă. Textele și variabilele sunt citite din PostgreSQL și actualizate în browser prin SSE după commit.

| Verificare executată | Rezultat | Dovezi |
|---|---|---|
| Migrare și pornire pe server | 001, 002 și 003 aplicate; `/readyz` răspunde ready | Jurnal manager; `docker compose logs migrate` |
| Backend, inclusiv PostgreSQL real, după migrarea 003 | 4 teste trecute, 0 eșecuri, 0 omise | `validation/backend-tests.txt` |
| 7 rute × 7 limbi × 2 dimensiuni de ecran | 98 combinații trecute | `validation/browser-report.json` |
| Meniu mobil, limbi fără reload, curse de navigare, unități, filtre, descărcări, căi private, SSE text | 19 verificări suplimentare; total browser 117 | Același raport |
| Modificare variabilă numerică în DB → pagină deschisă | Trecut; documentul nu se reîncarcă; valoarea inițială restaurată | `validation/live-variable.json` |
| Audit independent | 5 constatări concrete remediate | `AUDIT_SITE.md` și `audit-variables-inputs.json` |
| Desktop și mobil | Capturi examinate vizual | `validation/home-1440.png`, `home-390.png`, `measure-desktop.png` |
| Mutarea documentației originale | 59 fișiere urmărite, hashuri neschimbate | `../Aplicație/MUTARE_VERIFICATA.json` față de rădăcina Site |

Suita de 117 verificări a rulat după integrarea variabilelor și înainte de migrarea 003. După 003 au fost reluate toate testele backend cu PostgreSQL și testul browser dedicat variabilei; frontendul a rămas identic. Testele pentru numere extreme verifică respingerea valorilor SQL nefinite în JavaScript, acceptarea limitelor finite și păstrarea datelor la o migrare refuzată.

## Performanță măsurată

Cele două imagini servite însumează 177.658 octeți în WebP, față de 3.889.008 octeți pentru originalele PNG, păstrate pentru editare. Detalii: `asset-optimization.json`.

O probă locală pe server a măsurat API p95 de aproximativ 4,55 ms în 30 de cereri succesive și LCP de 192 ms într-o singură încărcare Chromium. Aceste valori sunt probe locale fără limitare de rețea/procesor; nu sunt rezultate Core Web Vitals din trafic public. Datele brute sunt în `validation/performance.json`.

## Limite și următorul pas

- Domeniul public, DNS, HTTPS și proxy-ul SSE nu au fost configurate sau testate în această livrare. Accesul de previzualizare folosește tunelul local către server.
- Verificările browser sunt Chromium desktop și viewport mobil; Safari pe un iPhone fizic și o revizie lingvistică de către vorbitori nativi nu au fost executate.
- Nu este declarată o conformitate completă de accesibilitate, un pentest sau un test de încărcare la trafic mare.
- Aplicația iPhone este în etapa de documentare/proiectare. Ilustrațiile site-ului sunt conceptuale, iar exemplele de măsurare și fișierele 3D sunt sintetice.

## Probleme întâlnite în integrare

Testul HTTP inițial a cerut spațiu temporar în serviciul content cu filesystem read-only; adăugarea tmpfs a rezolvat eroarea, iar suita a trecut. Invocarea `sh ops/verify.sh` a fost corectată la `bash`, conform scriptului. Primul test al variabilei a comparat textul transformat vizual în majuscule; comparația folosește acum textContent și trece. Aceste evenimente și remedierile auditului sunt consemnate în loguri, fără a fi ascunse de rezultatul final.
