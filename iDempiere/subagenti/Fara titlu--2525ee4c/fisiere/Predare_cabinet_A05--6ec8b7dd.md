# Predare cabinet A05 către coordonator

Raportul R2 a fost sigilat la SHA-256 `fd871b4a22b753ea42d25ecb6935426d4612f76ed05a531d4aa97b9e189f9a26`. Directorul curent conține numai completări după sigilare.

- Host SSH autorizat: `saga-server@192.168.100.151`. Director exact: `/tmp/eva-contab-codex-a05-r2.uxJmd3`. PID al supervisorului: 387684, fără terminal interactiv. Prima rezervare §61 este `suita~eva-contab-codex-a05r2~P01.T355~387684~1793633538`.
- Proprietar de test `eva-contab-codex-a05r2`, alias tehnic liber `P01.T355`. PG: `eva-test-p01-t355-auditor-pg-20261102173229`. ERP: `eva-test-p01-t355-auditor-app-20261102173240`. Endpoint intern `https://10.250.13.3:8443`, fără port public.
- Cabinetul a devenit gata la 17:35:24 EET. Perioada maximă a supervisorului este 80 minute de la acest moment (aproximativ 18:55 EET). Ordinul §40 are durata 85 minute de la rezervare (aproximativ 18:57 EET). Închideți la confirmarea A09; nu așteptați aceste limite.
- A09 are propriul document 1000023 și cheia terminată în 0021. Înainte de trimitere, documentul este DR, cantitate scriptică 20, numărată 20 și jurnal fără 0021. Starea este imortalizată în `avd21-before.json`. Un token temporar sintetic există exclusiv în `avd21.token` (0600) în directorul privat al hostului. Nu îl afișați, copiați sau înregistrați. A09 poate folosi `lab.py` pentru reautentificare dacă expiră.

După ce A09 confirmă terminarea, salvați observația finală **înainte** de a opri cabinetul. Exemplu PowerShell pe workstation:

```powershell
$hostAudit = 'saga-server@192.168.100.151'
$remoteAudit = '/tmp/eva-contab-codex-a05-r2.uxJmd3'
$evidenceAudit = 'Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R3_zone/A05'
ssh -o BatchMode=yes $hostAudit "cd $remoteAudit && python3 readback21.py" |
    Set-Content -Encoding utf8 -LiteralPath (Join-Path $evidenceAudit 'avd21-after.json')
Get-FileHash -LiteralPath (Join-Path $evidenceAudit 'avd21-after.json')
```

Verificați ID-ul documentului, linia, versiunile, `key_journal`, cantitățile, M_Transaction și Fact_Acct. Corelați-le cu cererile capturate efectiv de A09. În caz de eroare de rețea sau TLS, păstrați numărul real de cereri care au ajuns.

Pentru închidere, verificați întâi ambele etichete de proprietate. Apoi eliminați doar tokenul sintetic și semnalizați supervisorul. Exemplu shell pe hostul autorizat:

```bash
set -eu
w=/tmp/eva-contab-codex-a05-r2.uxJmd3
for name in "$(cat "$w/auditor-app")" "$(cat "$w/auditor-pg")"; do
  test "$(docker inspect -f '{{index .Config.Labels "eva.sesiune"}}' "$name")" = eva-contab-codex-a05r2
  test "$(docker inspect -f '{{index .Config.Labels "eva.task"}}' "$name")" = P01.T355
done
rm -f -- "$w/avd21.token"
touch "$w/finish"
```

Supervisorul verifică din nou proprietatea și eliberează în ordine rezervările containerelor, containerele și volumele lor, rețeaua internă, ocuparea și slotul. În eșantioane la 5–10 secunde citiți `tail -6 "$w/run.log"`; finalul așteptat este `remaining_owned_containers=0` și `CLEANED`. Verificați `$w/release-task`, `$w/release-slot` și `docker ps -a --filter label=eva.sesiune=eva-contab-codex-a05r2 --format '{{.Names}}'` (fără nume). Salvați aceste rezultate distinct sub R3. Nu rulați curățare generală a serverului. Dacă vreuna dintre etichete sau căi diferă, opriți acțiunea și verificați proprietatea.

Baza locală de model `a05_r2` a fost eliminată după reproducerea SQL, cu zero conexiuni active. `p01_garden` și dumpul A07 au rămas intacte.

