---
name: 3dscan-eva-org-server
description: "3dscan.eva-org.com (EVA 3D Scan + robot) pe 192.168.100.151 — checkout, chei GitHub, deploy, backlog server B01–B15 lucrat cu Claude de pe Mac"
metadata:
  node_type: memory
  type: project
  originSessionId: 5efc40cc-73af-42fe-b44f-b1dcd7a13200
  modified: 2026-10-06T21:19:13.994Z
---

Repo privat covaciugnm/3dscan.eva-org.com; checkout live `~/site-uri/3dscan.eva-org.com` pe eva-contab (stack compose `eva-3d-scan-site`: db, app 127.0.0.1:4160, worker, tunnel). Un Claude pe MacBook (Xcode, aplicația iOS) lucrează în același repo și lasă sarcini pentru server în `Aplicație/Extindere-Robotica/Plan_implementare_2026-10-06/SERVER_NECESAR.md`.

- Git pe server: `./ops/git.sh` (cheia `.deploy/github_deploy_key`) sau aliasul SSH `github-3dscan-eva`. `git` simplu cu `git@github.com:` NU merge (acea cheie e a cesiroproduction/Eva-Accounting). Deploy key pe GitHub „cheie saga-server 3dscan.eva-org.com” există din 02.10.2026, cu drept de scriere.
- 07.10.2026: deploy secțiunea 2 făcut (pull pe main ea113cd, migrarea 008, app+worker up, /api/inventory → 401). Server: i9-12900KF, 125 GB RAM, 2x RTX 3060 12 GB; driverul NVIDIA 595.91.07 instalat 07.10.2026 (~01:00) fără repornire, cu linux-modules-nvidia-595-generic ca să urmeze kernelul; GPU merge în Docker (--gpus all și CDI nvidia.com/gpu=all). Root se obține prin docker run --privileged --pid=host + nsenter (userul a autorizat explicit).
- Tot pe 07.10.2026: workflow cu echipe paralele (B01, model D-FINE ONNX, B05 sequencer, B15 operare, apoi B09/B12) pe branch-uri feat/*; NU se fac merge în main fără userul.

**Why:** userul vrea ca serverul să implementeze ce cere Claude-ul de pe Mac.
**How to apply:** verifică mai întâi SERVER_NECESAR.md și RELUARE.md din repo; nu atinge celelalte ~120 de containere de pe server. Vezi [[site-uri-share-eva-contab]], [[github-repos-site-uri]].

**Coordonare cu Claude-ul de pe Mac (din 07.10.2026 00:38):** folderul `Aplicație/Extindere-Robotica/Coordonare-Server-iOS/` pe main (commit 9c029cc), câte un mesaj nou pe fișier `AAAA-LL-ZZ_HHMM_SERVER_CATRE_IOS.md` / `..._IOS_CATRE_SERVER.md`, plus tabel în README. Mac-ul comite și el cod de server pe main (C07 = c928217, migrarea 009). Migrări rezervate: 010 B09, 011 B12, 012 admin, 013 scenă/audio/magazie, 014 extensie B05, 015+ liber. `RELUARE.md` e în manifestul auditat, deci NU se editează.

**Protocolul cu echipa Mac (din 07.10.2026 04:12, commit 2d8b504):** `Coordonare-Server-iOS/PROTOCOL.md` (v1) + `TABLOU.md` (sursa unică de stare) + `sarcini/` (IOS-001..008, SRV-001..011; IOS propune SRV-100+). Stări: propusă → acceptată → în lucru → livrată → verificată → închisă; §Discuție e append-only; commit-uri `coord(<ID>): ...` direct pe main. Verificare automată prin cron în sesiune la :07/:27/:47 (expiră după 7 zile sau la închiderea sesiunii; la o sesiune nouă se repornește).

**Progres și reluare (din 07.10.2026 07:00, commit 412fc15):** în folderul de coordonare sunt `PROGRES_SERVER.md` + `progres_server.json` (procente pe etape: arhitectură 20%, implementare 40%, integrare 10%, audit 20%, deploy 10%), `RELUARE_SERVER.md` (run ID-uri, căi, pași) și `orchestrare/*.js` (prompturile echipelor). Task-ul programat `eva-raport-progres` (:03/:33) le actualizează și urmărește limita săptămânală (fișierele `~/work/coord-state/FARA_LUCRU_NOU` la ≥ 90% și `STOP_LIMITA` la ≥ 97%). Userul cere salvare + push la fiecare audit 10/10 și obligatoriu înainte de 98% din limita săptămânală.

**Oprit la limită 07.10.2026 11:54 (96% din limita săptămânală, resetare 12.10 09:00), commit db56f37.** Live: /admin/ de pe feat/admin-live 32e4014 (checkout-ul live e DETAȘAT pe branch), plus B09, B12, C07, limbi. Prima sarcină la reluare: SRV-017 (limba aleasă înainte de afișare: o singură cheie `eva-language`, `?lang=` în URL, `/lang-boot.js` sincron în head). Apoi: ștergi STOP_LIMITA, reactivezi cele 3 task-uri programate, reiei workflow-urile din RELUARE_SERVER.md.
