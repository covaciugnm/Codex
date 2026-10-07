# Verificare Docker — Dracula Design și Dracula Food

Verificat în citire pe serverul `192.168.100.151`, 25 septembrie 2026, aproximativ 18:38 EEST. Nu au fost modificate containerele sau configurațiile în cadrul auditului.

| Componentă | Dracula Design | Dracula Food |
|---|---|---|
| Proiect Compose | `dracula-design` | `dracula-food` |
| Backend | pornit, healthy | pornit, healthy |
| Admin / proxy | pornit, healthy | pornit, healthy |
| PostgreSQL 16 | pornit, healthy | pornit, healthy |
| Migrare inițială | terminată, cod 0 | terminată, cod 0 |
| Port de previzualizare | `127.0.0.1:4181` | `127.0.0.1:4183` |
| Rețea Docker | `dracula-design_default` | `dracula-food_default` |
| Volum PostgreSQL | `dracula_design_pgdata` | `dracula_food_pgdata` |
| Bază de date | `dracula_design` | `dracula_food` |
| Director de date | `dracula-design/data` | `dracula-food/data` |
| Cloudflare Tunnel | pregătit, neactivat | pregătit, neactivat |

Izolarea este confirmată prin inspecția containerelor pornite: fiecare aparține propriei rețele și folosește propriile volume/directoare. Cheile aplicației, JWT și criptarea secretelor sunt prezente și diferite între site-uri; valorile nu au fost afișate. Bazele de date și backendurile nu publică porturi pe host. Containerele inspectate aveau zero restarturi automate; backendurile fuseseră recreate pentru actualizarea categoriilor.

Pentru ambele site-uri, `/health`, `/ro/collection` și `/admin/` au răspuns HTTP 200 prin tunelul SSH de previzualizare. Acest audit confirmă disponibilitatea rutelor, nu repetă testele complete de autentificare sau comandă.

## Cloudflare

Ambele proiecte au overlay Compose și script de pornire pentru un tunel dedicat, cu serviciul intern `http://admin:80`, URL public HTTPS și cookie-uri Secure. În starea verificată, `CF_TUNNEL_TOKEN` nu este setat în niciunul dintre cele două fișiere `.env`, iar containerele de tunel pentru Design și Food nu sunt pornite.

Pentru activare sunt necesare două tuneluri Cloudflare independente, tokenul fiecăruia salvat pe server și rutele domeniului principal plus `www` către serviciul intern al proiectului respectiv. Configurația DNS și contul Cloudflare nu au fost inspectate în acest audit. În prezent, site-urile sunt disponibile prin previzualizare SSH; nu este confirmată publicarea pe domeniile externe.

Modul comercial curent este `demo` pentru ambele. Nu au fost inițiate plăți sau solicitări către procesatori.

## Observație privind serverul comun

Serverul deservește și alte aplicații. La verificare, swap-ul folosea aproximativ 8.18 din 8.19 GiB, deși memoria disponibilă era aproximativ 29 GiB. O citire a senzorilor a indicat 100°C, iar citirea următoare a identificat senzorul procesorului `x86_pkg_temp` la 87°C. Aceste valori fluctuante justifică verificarea răcirii și a sarcinii serverului; nu dovedesc o problemă provocată de cele două site-uri. Nu s-au făcut intervenții asupra hostului.
