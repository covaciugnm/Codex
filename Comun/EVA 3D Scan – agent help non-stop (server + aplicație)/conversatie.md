# EVA 3D Scan – agent help non-stop (server + aplicație)

ID: `01a1184d-8751-78b3-9d9f-daab8068529e`  
Proiect: Comun  
Export UTC: 2026-10-08T14:13:28.280906+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Utilizator

<scheduled-task name="eva-help-writer" file="C:\Users\User\.claude\scheduled-tasks\eva-help-writer\SKILL.md">
This is an automated run of a scheduled task. The user is not present to answer questions. For implementation details, execute autonomously without asking clarifying questions — make reasonable choices and note them in your output. "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if the task file asks for that specific action. When in doubt, producing a report of what you found is the correct output.

Ești agentul de HELP pentru proiectul EVA 3D Scan (site https://3dscan.eva-org.com, repo GitHub privat covaciugnm/3dscan.eva-org.com). Lucrezi complet autonom: proprietarul a cerut explicit să NU fie întrebat nimic. Scrii în română cu diacritice corecte (ă â î ș ț) și traduci de calitate în en, de, fr, es, hu, bg, cu terminologie consecventă.

ACCES: `ssh -o BatchMode=yes saga-server@192.168.100.151 '<comenzi>'` (Docker fără sudo). Clona ta de lucru: `~/work/3dscan-helpwriter` (dacă nu există: `git clone ~/site-uri/3dscan.eva-org.com ~/work/3dscan-helpwriter` și `git remote set-url origin git@github-3dscan-eva:covaciugnm/3dscan.eva-org.com.git`). Checkout-ul LIVE `~/site-uri/3dscan.eva-org.com` (compose `eva-3d-scan-site` în Site/) nu îl editezi manual; ~120 containere ale altor proiecte nu le atingi.

LOCK: `mkdir ~/work/coord-state/help-lock` — dacă există și are < 60 min, ieși; la final șterge-l.

MISIUNE (la fiecare rulare):
1. `git fetch origin` (main, app, feat/*). Stabilește ce s-a schimbat de la ultima rulare (`~/work/coord-state/help_last_sha_main` și `help_last_sha_app`): pagini/funcții noi pe site (Site/public/**, Site/server/**, documentele Site/docs/*), ecrane noi în aplicația iOS (origin/app: EVA-3DScan/**/ *View.swift, Features/Help/HelpModels.swift, Resources/i18n/*.json), sarcini noi în "Aplicație/Extindere-Robotica/Coordonare-Server-iOS/".
2. Infrastructura de help (construită de echipa feat/help — vezi Site/docs/HELP_ARHITECTURA.md și HELP_INTEGRARE.md pe main sau pe origin/feat/help): conținutul server e în Site/db/help/server/<lang>.json + seed `scripts/seed-help.mjs`; help-ul aplicației se redă din app_i18n (chei help.* și tip.* — PROPRIETATEA echipei iOS, NU modifici Site/db/app-i18n/ sau i18n-ul iOS). Dacă infrastructura nu e încă pe main, lucrezi pe branch-ul origin/feat/help (git pull --rebase, fără force), doar pe fișierele de conținut, fără să intri în conflict cu echipa feat/help.
3. Pentru fiecare funcție/pagină nouă sau schimbată pe server/site: scrie sau actualizează capitolul de help și tips-urile „Ce e asta / Ce face” (tip.<pagina>.<element>, câmpurile what/does) pentru FIECARE element interactiv, în toate 7 limbile; verifică că pagina are butonul „?” (help.js + data-help-page) și data-help pe elemente. Paginile altor echipe (admin, scena, magazie, setari) le atingi DOAR după ce au intrat pe main (atunci adaugi data-help/include-ul help.js pe un branch feat/help-content-<data>).
4. Pentru ecranele/funcțiile noi din aplicația iOS fără help: NU scrii în codul iOS. Creezi/actualizezi sarcina IOS-009 (help în aplicație) în folderul de coordonare conform PROTOCOL.md (append în §Discuție cu ora `TZ=Europe/Bucharest date`, commit `coord(IOS-009): ...` pe main) cu lista exactă de chei propuse (help.<topic>.* și tip.<ecran>.<element>) și textele propuse în 7 limbi, ca echipa iOS să le adauge. Cerința proprietarului pentru aplicație: „?” pe fiecare ecran și „Ce e asta / Ce face” la clic dreapta (pe iOS: apăsare lungă / contextMenu, iar la pointer secundar pe iPad clic dreapta).
5. Rulează scriptul de acoperire (toate elementele interactive au tips în 7 limbi) și testele help; dacă trec: commit (`git -c user.name=saga-server -c user.email=horeca.cesiro@gmail.com commit`, linia finală `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`), pe main doar dacă infrastructura help e deja pe main și schimbarea e doar de conținut (Site/db/help/**, data-help în paginile tale); altfel pe branch.
6. Publicare conținut (doar când infrastructura e pe main și ai comis pe main): în checkout-ul live `./ops/git.sh pull --ff-only origin main` și `cd Site && docker compose run --rm migrate node scripts/seed-help.mjs` (fără rebuild dacă s-a schimbat doar conținutul; dacă s-au schimbat fișiere din public/ care sunt în imagine, `docker compose build app && docker compose up -d app`), apoi verifică `curl -s https://3dscan.eva-org.com/api/help?scope=server&lang=ro` (200) și pagina /ajutor/. La eșec, revino la commit-ul anterior.
7. Actualizează markerii help_last_sha_*, eliberează lock-ul. Fără schimbări: termină tăcut. Cu schimbări: raport de 2–4 rânduri.

Onestitate: nu descrie funcții care nu există; verifică în cod ce face fiecare element înainte să scrii „Ce face”.
</scheduled-task>

## Asistent

You've hit your session limit · resets 6:30am (Europe/Bucharest)

## Asistent

<EXTERNAL SESSION IMPORTED>
