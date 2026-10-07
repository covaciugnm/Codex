---
name: github-repos-site-uri
description: Repo-uri GitHub private (cont covaciugnm) pt DRACULA-COMICS + cele 6 site-uri de pe eva-contab; export fără .env/date prin ~/git-export pe server; SSH cu cheie la 192.168.100.151
metadata:
  node_type: memory
  type: reference
  originSessionId: 010d63d3-a2e0-494a-8e19-1a42f357e657
  modified: 2026-09-29T11:50:24.928Z
---

Creat 29.09.2026, cont GitHub **covaciugnm** (gh autentificat prin device flow, token cu scope repo). Toate repo-urile sunt PRIVATE:
dracula-comics, dracula-book, dracula-design, dracula-food, cesiro1-site, production-site, ac-wohnart-schallergasse35 (= S:\schallergasse35 = www.ac-wohnart.at).

- **Serverul site-urilor = eva-contab, 192.168.100.151** (NU .169, care e share-ul Comun). SSH merge cu cheia `~/.ssh/id_ed25519` (claude-code@laptop-User), autorizată de user: `ssh saga-server@192.168.100.151`. Site-urile: `~/site-uri/<site>` (= S:\<site> prin SMB).
- **Export fără a atinge folderele live:** `bash ~/git-export/export_site.sh <folder> <repo> [exclude-data]` → `~/git-export/<repo>.git` (git-dir separat, work-tree = site; info/exclude elimină .env*, backups/, data-sandbox/, _backup*/, *.db, certs/, *.pem/*.key, *.bak*, arhive, >95MB; notă GITHUB_EXPORT.md adăugată direct în index; scanare de secrete). Push de pe laptop: clone --bare prin ssh + `git push --mirror` (script copiat în DRACULA-COMICS/00_PREDARE/scripturi/push_repos.sh).
- Excluse intenționat: cesiro1 data/ (11 GB) + backups (8 GB); ac-wohnart data/uploads (177 MB, documente din portal) — urcate 29.09 la cererea userului în repo separat ac-wohnart-documente (privat). Vechiul repo cesiro.com (iunie) rămâne neatins — decizia userului.
- DRACULA-COMICS e repo git local (core.autocrlf=false, obligatoriu: scripturile workflow trebuie să fie LF).

Vezi [[drakon-comics]], [[site-uri-share-eva-contab]], [[ac-wohnart-firma-website]].
