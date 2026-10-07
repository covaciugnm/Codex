# Dracula Food — proiect independent

Site pentru **dracula-food.com**, marca **Dracula Food**, companie **Dracula-Company**, locație de brand **Dracula-Farm**. Sigla existentă este păstrată fără modificare.

Structura și stilul vizual sunt comune cu Dracula Design: negru, roșu discret, auriu, compoziție aerisită. Conținutul și imaginile Food sunt separate. Panoul CESIRO este disponibil la `/admin/`, cu utilizatori administrativi și clienți, produse, comenzi, pagini și traduceri. Frontendul public este cel Dracula, diferit de CESIRO.

## Izolare

| Componentă | Dracula Food |
| --- | --- |
| Proiect Docker Compose | `dracula-food` |
| PostgreSQL | `dracula_food` |
| Volum PostgreSQL | `dracula_food_pgdata` |
| Tenant | `dracula-food` |
| Port local server | `127.0.0.1:4183` |
| Cont inițial admin | `owner@dracula-food.local` |
| Parole și chei | generate independent în `.env` |
| Cookie sesiune/CSRF | prefix `dracula_food_` |
| Preferințe browser | prefix `dracula.food.` |

Nu se copiază baze de date, conturi, parole, comenzi sau `.env` de la alt magazin. Rețelele, volumele și secretele sunt separate. Niciun serviciu runtime Food nu depinde de proiectul Design. Template-ul comun se folosește doar la generarea surselor.

## Conținut și produse

RO/EN/DE sunt inițializate în PostgreSQL. Textele publice, paginile, produsele și traducerile se administrează în DB. Seedul nu resetează textele editate sau parolele existente.

La pregătirea proiectului folderul `S:/dracula-food` conținea numai `dracula-food-logo.jpeg`. Produsele și imaginile provin din materialele furnizate; informațiile comerciale și alimentare complete rămân de confirmat. Catalogul conține acum Nuci Dracula-Farm și Alune de pădure Dracula-Farm, importate din imaginile furnizate ulterior. Prețurile de 49 RON și 59 RON sunt demonstrative, nu prețuri comerciale confirmate. Sigla originală include textul de brand furnizat de utilizator; acesta nu a fost transformat în afirmații de certificare pentru produse.

Cele două produse pot fi adăugate din `/admin/`, cu imaginile lor. Înainte de vânzare completați numele, cantitatea, ingredientele și alergenii, condițiile de păstrare, informațiile nutriționale unde se aplică, datele operatorului, prețul și stocul. Pagina de retur este adaptată pentru produse alimentare și nu promite retur universal pentru mărfuri perisabile.

Pentru seedul inițial reproductibil, `food/catalog.json` acceptă lista produselor cu câmpurile `id`, `sku`, `price`, `category`, `image` (cale locală `/assets/produse/...`), `name`, `description`, `details`. Ultimele trei sunt dicționare cu cheile `ro`, `en`, `de`. Categorii inițiale: `gourmet`, `pantry`, `gifts`. Fișierele originale merg în `food/assets/produse/`. `details` trebuie să conțină informațiile alimentare confirmate.

## Actualizarea codului comun

```sh
python3 food/build_overrides.py
python3 ops/sync-from-design.py ../dracula-design-office
```

Comanda copiază exclusiv sursele, apoi aplică brandingul, catalogul și setările Food. Păstrează `.env`, datele și volumele existente. Nu pornește containere și nu modifică proiectul Design. După inițializarea DB, modificările de conținut se fac din admin, nu prin repetarea seedului.

## Pornire pe server

Sursele sunt destinate folderului `/home/saga-server/site-uri/dracula-food`. După validarea bazei comune:

```sh
sh ops/start.sh
```

Parola admin aleatoare se află numai în `.env`, câmpul `ADMIN_SEED_PASSWORD`. Schimbați parola la prima conectare. Nu folosiți parola SSH ca parolă de magazin. Accesul local prin tunel SSH: `ssh -L 4183:127.0.0.1:4183 saga-server@192.168.100.151`, apoi `http://127.0.0.1:4183/admin/`.

Magazinul este inițial în mod demo, fără plăți și expedieri reale. Configurația Cloudflare Food este pregătită în `docker-compose.cloudflare.yml`, `ops/start-cloudflare.sh` și `ops/CLOUDFLARE.md`. Folosește un tunel dedicat `dracula-food` și un token nou în `.env` Food, cu rute pentru `dracula-food.com` și `www.dracula-food.com` spre `http://admin:80`. Nu au fost create înregistrări DNS și tunelul nu este activat.

Surse folosite pentru adaptarea paginilor: [Comisia Europeană — vânzarea alimentelor la distanță](https://food.ec.europa.eu/food-safety/labelling-and-nutrition/food-information-consumers-legislation/distance-selling_en), [Your Europe — dreptul de retragere](https://europa.eu/youreurope/citizens/consumers/shopping/returns/indexamp_en.htm).

## Acces de test verificat

Stackul rulează pe server. Previzualizare locală prin tunel SSH: http://127.0.0.1:4183/ ; administrare: http://127.0.0.1:4183/admin/ .

Conturile cerute sunt create în DB Food: admin@dracula-food.com (owner) și client@dracula-food.com (client). Parola este cea indicată în conversație, fără a fi salvată în surse. Autentificarea ambelor conturi, catalogul, conținutul trilingv și afișarea mobilă au fost verificate în browser. Contul Design este respins în Food; secretele DB și de autentificare sunt diferite.

Cele două produse furnizate sunt disponibile în RO/EN/DE, cu favorite, coș și pagini individuale. Imaginile originale PNG de 1536 × 1024 sunt păstrate nemodificate. Cloudflare rămâne pregătit, neactivat, până la furnizarea tokenului dedicat și configurarea rutelor domeniului.


## Imagini produse adăugate

- Nuci: https://chatgpt.com/s/m_6ab691ad087c81919ea2c882178b576d
- Alune de pădure: https://chatgpt.com/s/m_6ab6921286f48191b2489c962fbe7245

Originale: food/assets/produse și S:/dracula-food/02-produse. Hashurile și proveniența sunt în inventar-imagini.csv. Panourile de prezentare folosesc fotografiile produselor; logo-ul auriu original rămâne în antet și hero.
