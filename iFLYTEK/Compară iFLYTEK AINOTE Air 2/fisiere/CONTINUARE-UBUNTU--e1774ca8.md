# Continuarea proiectului iFLYTEK pe Ubuntu

Actualizare: 31 octombrie 2026. Branch: **`build/reproducible-apk-20261031`**. Citește acest fișier înaintea documentelor istorice: separă testele efectuate de operațiile încă necesare.

## Starea exactă la predare

| Element | Rezultat |
|---|---|
| Telefon | Samsung Galaxy A14 5G, SM-A146P/DSN, Android 14 / API 34, ARM64 |
| Ochelari | XF-AIGlasses-01; firmware **1.0.01.88**, comunicat de proprietar |
| Aplicație | `com.iflytek.translateapp`, 1.0.3899 / 3899, minimum Android 10 / API 29 |
| Baza recompilată | Instalată și pornită pe Galaxy A14; interfață engleză, profil, login SMS și Password Login vizibile |
| Varianta România +40 | Construită, semnată, aliniată; 22 de teste ARM64 trecute; **neinstalată și netestată pe telefon** |
| Autentificare / SMS / cloud | Nu s-au introdus credențiale și nu s-au trimis cereri de autentificare de test; acceptarea +40 de către server este necunoscută |
| Bluetooth / audio / OTA | Niciun test nou pe ochelari; nu există un firmware OTA recuperat |
| Telefon disponibil | Proprietarul îl va conecta mai târziu, posibil la laptopul Ubuntu; nu se mai așteaptă ADB pe PC-ul inițial |

Proiectul reconstruibil se află în `iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31` (mai jos: variabila `PROJECT`). [Raportul HTML](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31/index.html), [dovezile bazei](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31/reports/device-test.json) și [starea variantei +40](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31/variants/romania-40/reports/device-test.json) sunt distincte.

## 1. Copia locală pe Ubuntu

Cu un cont GitHub care are acces la repository-ul privat:

```bash
sudo apt update
sudo apt install git gh nodejs adb unzip
gh auth login
gh repo clone covaciugnm/iFLYTEK -- --branch build/reproducible-apk-20261031
cd iFLYTEK
node --version   # scripturile cer Node.js 18 sau ulterior
node tools/restore-iflytek-apk-assets.cjs --apk-only
PROJECT="$PWD/iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31"
```

`--apk-only` descarcă cele două APK-uri semnate și verifică dimensiunile și SHA-256. Pentru toate fișierele suplimentare (surse editabile, analiză AOT și unelte), rulează fără această opțiune:

```bash
node tools/restore-iflytek-apk-assets.cjs
```

Pentru întregul corpus de cercetare anterior, inclusiv APK-ul oficial, SDK-urile și arhivele mari (~4,95 GB în total, incluzând conținutul din Git):

```bash
node tools/restore-iflytek-assets.cjs
node tools/verify-iflytek-snapshot.cjs
```

Cele două scripturi restaurează **release-uri diferite**. Manifestul istoric nu acoperă noile APK-uri; acestea au propriul [manifest](iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31/release-assets.json). Fișierele existente cu alte hashuri sunt refuzate, nu suprascrise. Cheia SSH de deploy cu drept de citire permite clonarea Git; atașamentele private se descarcă prin autentificarea `gh`.

## 2. Instalarea APK-ului cu +40 când telefonul este conectat la Ubuntu

Deblochează telefonul, activează depanarea USB și acceptă amprenta RSA a **noului laptop**. Comenzile ADB se execută pe laptopul la care este conectat cablul:

```bash
adb devices -l
```

Verifică APK-ul din `dist`, apoi instalează-l:

```bash
(cd "$PROJECT/dist" && sha256sum -c iflytek-1.0.3899-romania40.apk.sha256)
adb install -r "$PROJECT/dist/iflytek-1.0.3899-romania40.apk"
adb shell monkey -p com.iflytek.translateapp -c android.intent.category.LAUNCHER 1
```

La `adb devices`, starea trebuie să fie `device`, nu `unauthorized`. Dacă apar mai multe dispozitive, adaugă `-s SERIALUL_TELEFONULUI` după `adb`. Pentru `no permissions`, configurează regulile udev Android ale distribuției; nu publica identificatorii telefonului.

Varianta +40 folosește **același certificat local** ca baza instalată anterior; `install -r` o poate actualiza. Dacă telefonul conține aplicația oficială sau o variantă semnată cu altă cheie, Android poate raporta `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. Nu dezinstala automat: dezinstalarea șterge datele locale. Înlocuirea originalului pe Galaxy A14 a fost deja autorizată și efectuată în sesiunea anterioară, dar acest lucru nu dovedește ce există pe un alt telefon.

La avertismentul Play Protect, decizia și eventuala confirmare biometrică se fac direct pe telefon. Nu se dezactivează protecțiile generale. Nu transmite parola, PIN-ul, codul SMS sau tokenurile în chat/loguri.

Verificări rămase pe telefon:

1. Pornire și deschiderea ecranului de login fără crash.
2. Selectorul afișează +86, +852, +853 și **Romania +40**; celelalte țări își păstrează traducerile.
3. Pentru +40, introdu **9 cifre începând cu 7**, fără zero inițial și fără a repeta prefixul. Confirmă limitarea lungimii și activarea butonului.
4. Deschide și închide selectorul repetat și testează SMS Login / Password Login. Randarea Flutter și comportamentul GC real nu sunt acoperite integral de emulator.
5. Proprietarul poate testa contul propriu și, separat, trimiterea SMS. Raportează mesajul de eroare fără date de autentificare. Succesul în cloud nu trebuie presupus din prezența butonului.
6. După login, verifică separat asocierea ochelarilor, audio, traducerea și verificarea OTA. Nu instala firmware necunoscut.

SDK-ul existent trimite țara separat: `ccode: "40"` și `phone/loginid: "7xxxxxxxx"`, către `https://account.xfinfr.com`. Verificarea SMS și autentificarea serverului nu au fost eliminate. „Password Login” există deja în interfața originală; serverul poate cere verificări suplimentare.

## 3. Surse și analiză pe Ubuntu

Arhiva `iflytek-1.0.3899-editable-source.zip` conține 49.768 de fișiere, inclusiv 47.219 Smali, resurse, assets și biblioteci native. Arhiva AOT conține ieșirea Blutter, poolul de obiecte, assembly-ul Dart, ajutoare IDA/Frida și patch-ul binar. **Acestea nu reprezintă sursele originale Dart/C++ recuperate.** Exportul JADX cu 301 erori rămâne material de analiză; calea de recompilare verificată este Smali/Apktool.

Pentru reasamblarea și verificarea patch-ului nativ pe Ubuntu, fără acces la telefon sau cloud:

```bash
sudo apt install python3-venv binutils-aarch64-linux-gnu
python3 -m venv .venv-iflytek
.venv-iflytek/bin/pip install pyelftools==0.33 unicorn==2.1.4
mkdir -p "$PROJECT/work/native-ubuntu"
unzip -p "$PROJECT/dist/iflytek-1.0.3899-full-rebuilt.apk" lib/arm64-v8a/libapp.so > "$PROJECT/work/native-ubuntu/original-libapp.so"
.venv-iflytek/bin/python "$PROJECT/variants/romania-40/patch_native.py" "$PROJECT/work/native-ubuntu/original-libapp.so" "$PROJECT/work/native-ubuntu/libapp.so" --work "$PROJECT/work/native-ubuntu/patch"
.venv-iflytek/bin/python "$PROJECT/variants/romania-40/test_native.py" "$PROJECT/work/native-ubuntu/libapp.so" "$PROJECT/work/native-ubuntu/patch/native-tests.json"
.venv-iflytek/bin/python "$PROJECT/variants/romania-40/package_variant.py" "$PROJECT/dist/iflytek-1.0.3899-full-rebuilt.apk" "$PROJECT/work/native-ubuntu/libapp.so" "$PROJECT/work/native-ubuntu/patch/native-patch.json" "$PROJECT/work/native-ubuntu/romania40-unsigned.apk"
```

Ultima comandă produce un APK **nesemnat**, care nu poate fi instalat ca atare. Recompilarea/semnarea completă verificată este implementată în `Build.ps1` și `variants/romania-40/Build-Romania40.ps1` pentru Windows + WSL. Pe Ubuntu sunt necesare separat Android Build Tools pentru Linux, JDK și cheia de semnare. Arhivele Windows din pachetul de unelte nu sunt executabile Linux. Comenzile native de mai sus au aceeași logică, dar întregul pipeline de semnare nu este încă portat și validat pe Ubuntu.

Pentru a păstra posibilitatea actualizării APK-ului deja instalat, cheia locală și fișierul parolei din `D:\CodexWork\iflytek-build-private` trebuie transferate **separat, printr-un canal privat**, dacă semnarea se mută pe alt calculator. Nu se află în GitHub. APK-urile deja semnate se instalează fără această cheie. O cheie nouă produce alt certificat și nu poate actualiza instalarea existentă.

## 4. Codex CLI pe Ubuntu, conectat la acest PC Windows

Verificat local: **Codex CLI 0.153.0** oferă `--remote` și `codex app-server --listen`. PC-ul Windows avea adresa LAN **192.168.100.137**; serverul OpenSSH nu era instalat. Pașii următori sunt instrucțiuni de configurare, **nu servicii pornite de acest ghid**. PC-ul trebuie să rămână pornit, conectat și să nu intre în repaus.

În PowerShell **ca administrator** pe Windows, o singură dată:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Set-Service -Name sshd -StartupType Automatic
if (!(Get-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -RemoteAddress LocalSubnet
}
Set-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -RemoteAddress LocalSubnet
Start-Service sshd
```

În PowerShell normal, sub utilizatorul **User** care are Codex autentificat, pornește serverul numai pe loopback și lasă terminalul deschis:

```powershell
Set-Location 'D:\CodexWork\iFLYTEK-publish-20261031'
codex app-server --listen ws://127.0.0.1:4500
```

Pe Ubuntu, instalează/actualizează Codex CLI conform [instrucțiunilor oficiale](https://learn.chatgpt.com/docs/codex/cli). Cu Node.js/npm deja instalate, comanda este `npm install -g @openai/codex`. Verifică `codex --help` pentru `--remote`; o versiune veche poate să nu ofere această opțiune.

Într-un terminal Ubuntu:

```bash
ssh -N -T -o ExitOnForwardFailure=yes -L 127.0.0.1:4500:127.0.0.1:4500 User@192.168.100.137
```

Confirmă amprenta serverului după verificare. Autentificarea SSH folosește contul Windows/parola lui sau o cheie SSH configurată; PIN-ul Windows Hello nu este parola SSH. În alt terminal Ubuntu:

```bash
codex --remote ws://127.0.0.1:4500 --cd 'D:\CodexWork\iFLYTEK-publish-20261031'
```

Astfel interfața CLI rulează pe Ubuntu, iar comenzile și fișierele Codex sunt pe Windows. Citește `CONTINUARE-UBUNTU.md` pentru context; nu presupune că deschiderea unei sesiuni noi transferă automat întreaga conversație. [Referința oficială CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli) descrie modul remote; [Microsoft](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse) documentează instalarea OpenSSH.

`192.168.100.137` este o adresă privată, valabilă doar în rețeaua accesibilă laptopului; din altă locație ai nevoie de VPN și de o regulă SSH limitată la adresa/subrețeaua VPN. Nu expune portul app-server 4500 pe internet. Tunelul de mai sus protejează conexiunea, iar serverul Codex rămâne pe loopback. `Ctrl+C` închide tunelul sau serverul din terminalul respectiv.

Telefonul conectat prin USB la Ubuntu **nu apare automat** în ADB de pe Windows prin acest tunel. Pentru instalare rulează ADB local pe Ubuntu, ca în secțiunea 2. Pentru Codex care lucrează local pe Ubuntu, pornește simplu `codex` în repository-ul clonat și autentifică-te pe laptop.

## Fișiere private și limite de predare

Sunt publicate în repository-ul privat codul, rapoartele și artefactele tehnice. Cheile SSH, cheia/parola de semnare, datele contului Codex/iFLYTEK, fotografiile cu număr de telefon/IMEI și logurile brute ale dispozitivului rămân în afara GitHub. Sistemul WSL și cache-urile de build nu sunt arhivate; sursele și binarele Blutter necesare analizei sunt incluse. Toate cele cinci artefacte noi au SHA-256 în manifest și în `SHA256SUMS.txt` din release.
