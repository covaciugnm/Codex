---
name: site-uri-share-eva-contab
description: partajare SMB \192.168.100.151\site-uri cu site-urile ac-wohnart.at si dracula-book.com; cum se editeaza si se publica
metadata:
  type: project
---

Serverul `eva-contab` (Ubuntu, LAN 192.168.100.151) gazduieste doua site-uri in
`/home/saga-server/site-uri/`, expuse din Windows ca partajare SMB
`\192.168.100.151\site-uri` (user `saga-server`, parola in Credential Manager;
se monteaza cu `%SystemRoot%\System32\net.exe use` — `net` nu e pe PATH in
sesiunile Claude Code, trebuie calea completa).

- `\192.168.100.151\site-uri\schallergasse35` — www.ac-wohnart.at, FastAPI+Postgres+cloudflared, port local 3480. Vezi [[ac-wohnart-firma-website]].
- `\192.168.100.151\site-uri\dracula-book` — dracula-book.com, Nginx static, port local 3481. Vezi [[dracula-book-editura]].

**Why:** userul vrea sa pot actualiza site-urile la cerere direct din Windows.

**How to apply:** din 21.09.2026 `public/` e montat ca volum in container la
ambele site-uri, deci editarile din partajare sunt **live imediat, fara rebuild**
(la ac-wohnart trebuie incrementat `?v=N` pe js/css; la dracula css/js au cache 1 zi).
Rebuild (`docker compose --profile tunnel up -d --build`, rulat de user pe server)
e necesar doar pentru `backend/`, `Dockerfile`, `nginx.conf` sau `.env`.
Detalii complete in `DOCUMENTATIE.md` din fiecare folder.

**SSH (din 21.09.2026):** `ssh saga-server@192.168.100.151` merge pe port 22 cu
parola (doar din LAN), iar `saga-server` ruleaza Docker fara sudo. In sesiunile
Claude Code (non-interactive) prompt-ul de parola se rezolva cu un script
`SSH_ASKPASS` + `SSH_ASKPASS_REQUIRE=force`. Scripturi gata pe server:
`~/site-uri/stare.sh` (starea containerelor + HTTP 200 pe ambele domenii) si
`~/site-uri/reconstruieste.sh dracula-book|schallergasse35` (rebuild + verificare).
Deci pot rula eu rebuild-ul, nu mai e nevoie sa-l ruleze userul.

**Unitatea S: (22.09.2026):** partajarea e mapata permanent ca `S:\` pe laptopul
userului (`net use S: ... /persistent:yes` + `cmdkey /add:192.168.100.151`), deci
apare in File Explorer la This PC si se reconecteaza la login. Share-ul Samba e
`read only = no`, `force user/group = saga-server`, `create mask 0664`,
`directory mask 0775` — fisierele scrise din Windows ajung cu proprietarul corect
pentru Docker. Testat: creare/editare/redenumire/copiere/stergere de fisiere si foldere.

**Fisiere pe paginile P1–P10 (28.09.2026):** `data/uploads/` NU e scriibil din share
(Permission denied) si nu am cheie SSH (doar parola → nu o introduc eu). Metoda folosita:
pozele puse in `schallergasse35/_import_p3/` cu nume UUID + `import_p3_arhiva.sql`
(INSERT in `page_files`) + `import_p3_arhiva.sh` (docker compose cp in `app:/data/uploads/pages/N/`
+ psql in `db`), rulat de user pe server. Varianta alternativa: upload manual din `/admin`.

**Actualizare 28.09.2026 (seara): SSH cu cheie FUNCTIONEAZA.** `ssh -o BatchMode=yes saga-server@192.168.100.151` intra fara parola (cheia `~/.ssh/id_ed25519` a userului Windows e acceptata). Deci pot rula direct pe server `~/site-uri/stare.sh`, `reconstruieste.sh`, `docker compose cp` / `psql` (ex. importul in `data/uploads/`) fara sa mai ceara userul ceva.
