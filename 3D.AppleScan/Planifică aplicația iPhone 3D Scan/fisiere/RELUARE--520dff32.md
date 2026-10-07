# Reluarea lucrului și operarea site-ului

## Punctul de pornire

1. Citiți `STATUS.json`, `AUDIT_SITE.md` și `VALIDARE_FINALA.md` din acest folder.
2. Citiți ultimul eveniment din `manager-events.jsonl`, apoi jurnalul specialistului relevant: `backend-events.jsonl`, `translations-events.jsonl`, `auditor-events.jsonl`.
3. Verificați starea reală pe server. Un jurnal descrie ultima verificare; nu înlocuiește verificarea serviciului curent.

Director Windows: `S:\3dscan.eva-org.com\Site`.
Director server: `/home/saga-server/site-uri/3dscan.eva-org.com/Site`.

```sh
docker compose ps
docker compose logs --tail 60 migrate app
curl --fail http://127.0.0.1:4160/readyz
```

## Continuarea unei modificări

- Înregistrați înainte de lucru: ID sarcină, responsabil, obiectiv, fișiere, criteriu de acceptare și starea `in_progress`.
- Editați sursele; nu modificați checksum-ul unei migrări SQL deja aplicate. Adăugați o migrare nouă.
- Rulați verificările relevante. Pentru o schimbare de backend/traduceri: `bash ops/verify.sh` în mediul de test configurat.
- Înregistrați rezultatul concret, comanda, raportul și orice limită. `passed` se folosește numai după rezultat real.
- Actualizați `STATUS.json`, raportul de audit și manifestul fișierelor la închiderea etapei. Nu ștergeți evenimentele vechi.

## Restart și actualizare

`docker compose restart app` repornește numai serverul web. `bash ops/start.sh` reconstruiește imaginea și aplică migrările necesare. Ambele păstrează volumul PostgreSQL și textele editate. Nu utilizați `docker compose down -v` pentru un restart: șterge datele persistente.

Fișierul `.env` existent se păstrează. Este exclus din imagine, manifestul de livrare și documentele publice. Nu copiați parole în loguri.

## Copie a bazei de date

Exemplu de backup administrativ, din directorul Site, pe Linux:

```sh
mkdir -p backups
chmod 700 backups
umask 077
docker compose exec -T db pg_dump -U eva_site -d eva_site -Fc > "backups/eva_site-$(date -u +%Y%m%dT%H%M%SZ).dump"
```

Backupurile trebuie păstrate și în afara acestui server. Procedura de restaurare trebuie probată într-o bază separată înainte de a înlocui datele curente. Nu este declarată o restaurare testată în această livrare.

## Acces public

Site-ul este public la https://3dscan.eva-org.com, verificat prin HTTPS. Aplicația Docker ascultă local pe 4160. Preview-ul Windows poate folosi tunelul SSH existent. Pentru starea actuală a redesignului și cele două selectoare, citiți REDESIGN_CLIENTI_LIVRAT.md și CUSTOMER_FOCUS.md. Verificarea unui serviciu curent se repetă înainte de intervenții.

## Delimitarea livrării

Site-ul prezintă aplicația în dezvoltare. Testele din Site verifică site-ul, PostgreSQL și traducerile. Validarea dimensiunilor, LiDAR, RoomPlan, exporturilor aplicației și imprimării 3D se găsește ca plan în `Aplicație/documentatie`; testele fizice ale aplicației nu au fost executate.
