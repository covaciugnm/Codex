# Cloudflare — Dracula Design

Stack separat de CESIRO și Dracula Food. PostgreSQL nu are port public. Cloudflared se conectează din propria rețea Compose la `http://admin:80`.

## Configurare

1. Adaugă domeniul `dracula-design.com` în contul Cloudflare și verifică nameserverele.
2. În Zero Trust → Networks → Tunnels, creează un tunel dedicat `dracula-design`.
3. Salvează tokenul nou în `/home/saga-server/site-uri/dracula-design/.env` ca `CF_TUNNEL_TOKEN=...`. Nu folosi tokenul CESIRO sau Food.
4. În Published application routes, configurează `dracula-design.com` și `www.dracula-design.com`, ambele cu tip HTTP, serviciu `admin:80`, fără restricție Path. Astfel funcționează și `/admin/` și `/api/`.
5. Pornește pe server: `sh ops/start-cloudflare.sh`.
6. Verifică `https://dracula-design.com/`, `/admin/` și `/health`. Serviciul tunnel trebuie să fie Connected. Opțional, redirecționează www către domeniul fără www din Cloudflare.

Overlay-ul setează `PUBLIC_BASE_URL=https://dracula-design.com` și cookie-uri Secure. HTTPS public înlocuiește previzualizarea HTTP pentru autentificare. Commerce rămâne demo până la configurarea prețurilor, stocurilor, livrării, datelor juridice și procesatorului.

Păstrează cache bypass pentru `/api/*`, `/admin/*`, `/account*`, `/checkout*`. Nu activa „Cache Everything” pentru răspunsuri private. Fișierele admin cu hash pot avea cache lung. Administrația are autentificarea și rolurile CESIRO; poate primi suplimentar o regulă Cloudflare Access dedicată numai `/admin*` și `/api/admin/*`.

Pentru revenire la previzualizare locală: `docker compose -f docker-compose.yml -f docker-compose.cloudflare.yml stop tunnel`, apoi `docker compose up -d backend admin`.

Documentație: [Cloudflare Tunnel setup](https://developers.cloudflare.com/tunnel/get-started/), [tokenuri dedicate](https://developers.cloudflare.com/tunnel/reference/tunnel-tokens/).

Starea livrată: configurație pregătită; tokenul și rutele DNS ale acestui domeniu nu au fost furnizate și tunelul nu este pornit.
