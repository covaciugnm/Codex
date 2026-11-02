# HANDOFF — continuare pe Ubuntu

**Data:** 2026-10-31 · **De la:** sesiune Claude Code pe Windows (mașina User) · **Către:** sesiune nouă pe Ubuntu

## 1. De ce mutăm

Pe mașina Windows, volumul **C: este plin (ENOSPC)** — directorul temp al Claude Code (`C:\Users\User\AppData\Local\Temp\claude`) nu mai are spațiu, deci **shell-urile (PowerShell/Bash) nu pornesc**, iar `Glob`/`ripgrep` pe share dau timeout. Scrierea/citirea pe share de rețea (`\\192.168.100.169\Comun`) funcționează (alt volum), așa că livrabilele sunt în siguranță. Implementarea și build-ul oricum au nevoie de un mediu Linux cu unelte (JDK/Android/Docker), de unde mutarea pe Ubuntu.

> Dacă vrei să refolosești mașina Windows: eliberează spațiu pe C: sau setează `CLAUDE_CODE_TMPDIR` pe alt volum. Legat: [memorie „Curatenie Google Drive"].

## 2. Ce este GATA (pe share, neafectat de C:)

Toate în `\\192.168.100.169\Comun\Dep. IT\iFlyGlasses-Companion\`:

- `protocol-core\` — nucleul Kotlin (E0), nerulat/necompilat aici.
- `docs\protocol-catalog.json` — 113 `opt` app→ochelari + 17 upload-uri.
- `docs\proiect-tehnic\` — **proiectul tehnic DRAFT complet**: documentele 00–12 (vezi `00-INDEX.md`) + folderul `knowledge-base\` cu 20 de articole de manual.
- Toate secțiunile sunt scrise negru pe alb, în română, cu elementele TENTATIV marcate.

## 3. Ce NU este făcut

- **Auditul până la 10/10 NU a rulat.** Proiectul e „runda 1 — fundație". Documentele transversale (00/01/10/11) le-am completat manual la checkpoint; trebuie reconciliate la primul audit.
- **Implementarea (cod real) nu a început.**
- **Protocolul e NEVERIFICAT pe hardware** (E2 este poarta critică).

## 4. Pași pe Ubuntu

### 4.1. Montează share-ul
Exemplu (ajustează la infrastructura ta):
```bash
sudo mkdir -p /mnt/comun
sudo mount -t cifs //192.168.100.169/Comun /mnt/comun -o username=USER,uid=$(id -u),iocharset=utf8
```
Atunci rădăcina proiectului devine: `/mnt/comun/Dep. IT/iFlyGlasses-Companion/`

### 4.2. Traducere căi
Peste tot în documente și în scriptul de workflow, înlocuiește baza UNC cu calea montată:
`\\192.168.100.169\Comun\Dep. IT\iFlyGlasses-Companion` → `/mnt/comun/Dep. IT/iFlyGlasses-Companion`

### 4.3. Deschide o sesiune Claude Code nouă
Cu working dir pe `/mnt/comun/Dep. IT/iFlyGlasses-Companion/`. (Workflow-ul de pe Windows NU se poate relua cross-sesiune — repornește bucla pe documentele existente.)

### 4.4. Rulează mai întâi AUDITUL → 10/10
Prompt sugerat de dat sesiunii Ubuntu:
> Pornește echipa de agenți proiectant↔auditor pe proiectul tehnic existent din `docs/proiect-tehnic/` (NU de la zero — citește ce există). Auditorul notează pe dimensiuni, întoarce checklist clar; proiectantul revizuiește. Iterează până la 10/10 pe front-end ȘI backend. Rezolvă întrebările deschise din secțiunea 6 a `HANDOFF-UBUNTU.md`.

### 4.5. Apoi IMPLEMENTAREA → 10/10
După ce proiectarea ia 10/10: pornește al doilea workflow coder↔auditor care scrie codul real (app Android + backend) peste proiectul validat, code-review până la 10/10. Toolchain necesar:
- JDK 17, Android SDK + command-line tools (sau Android Studio), Gradle
- Docker + docker-compose (pentru backend Ktor + PostgreSQL 16 + Redis 7)
- Emulator/dispozitiv Android pentru E1; ochelari reali + telefon cu HCI snoop pentru E2

## 5. Decizii de infrastructură de confirmat cu tine
- Host backend: propus `iflyglasses.eva-org.com` prin Cloudflare Tunnel + port LAN 3490 pe `192.168.100.151`. Postgres/Redis dedicate sau partajate?
- Repo backend: în `covaciugnm/iFLYTEK` sau nou `covaciugnm/iflyglasses-backend`?
- STT pe server: microserviciu Whisper propriu SAU Qwen de pe PGX `.160` prin HTTP (regula „NU umbla la docker pe .160" rămâne).
- Stocare LAN: SMB (jcifs-ng) vs WebDAV vs SAF tree-URI.
- E2EE pe cloud: din start sau amânat (afectează sumarizarea pe server).
- Implicite confidențialitate propuse: `storeAudio=false`, `telemetry=false`, `retentionDays=0`.
- `minSdk`: propus 26 (urcăm la 28 dacă BLE/audio e instabil pe dispozitive vechi).

## 6. Întrebări deschise (consolidat din toți specialiștii) — de rezolvat la audit/E2
1. **Checksum real** (exemplul `0xa4` nu se potrivește cu scheme simple) — harness-ul Python din `docs\proiect-tehnic\12-validare-hardware.md` îl rezolvă pe cadre reale.
2. **Offset câmp lungime**: 12 (din cod) vs 10 (sugerat de APK) și ce numără — blocant pentru reasamblare.
3. **Format audio pe `...A4`**: PCM vs SBC, mono/stereo, dimensiune cadru. `android.speech.SpeechRecognizer` NU acceptă PCM arbitrar → pentru STT pe vocea de pe ochelari e nevoie de Vosk/whisper.cpp (JNI) sau rutare cloud, ori calea HFP SCO. **De decis motorul embedded** (impact pe dimensiunea APK).
4. **Opcode-uri doar în doc, nu în catalog**: teleprompter, `startAstronTakePhoto`, `setWearSwitch`, `72023`/`72019`/`72025`/`72026`/`72018`/`72027` etc. — de confirmat din reconstituirea APK sau la E2 înainte de a activa ecranele respective.
5. **Corelare răspuns**: cheia (SEQ header vs `optNum` payload vs `opt`) — strategie defensivă până la confirmare.
6. **UUID-uri reale**, tip scriere BLE (WithResponse vs NoResponse), eventual bonding/encryption LE — nRF Connect + HCI.
7. **`protocol-core/Commands.kt`**: de adăugat buildere (62010 LED, 62104 mute, 62102 tone, 62305 segment traducere, 62212 dual sound, 62301/62302/62306 playDest, 62130 network state) și corecturi (câmp `value` la `setPickupMode`, numele câmpului la `enableDisplay`, separare `downloadFile` BLE vs WiFi, coliziune valori în `Opt.File`, legătura reasamblare↔offset lungime).
8. Acoperirea limbii **RO** în planul iFLYTEK al userului (altfel RO pe Vosk/ML Kit/DeepL/Azure/Google).
9. **Capcană captură E2**: dacă app-ul oficial nu pornește fără SMS-ul chinezesc, captura pasivă app→ochelari e imposibilă; planul B din doc.12 folosește notificările de la butoanele fizice (cadre reale, fără cont) pentru checksum/lungime.

## 7. Reguli de respectat (din memorie)
- Protocolul rămâne NEVERIFICAT → nimic bazat pe el până la E2; **OTA/flash interzis**.
- „NU umbla la docker pe PGX `.160`".
- Căi complete, fără „..."; texte germane cu diacritice (nu e cazul aici).
- Înainte de a șterge ceva de pe C: pentru spațiu, anunță userul.
