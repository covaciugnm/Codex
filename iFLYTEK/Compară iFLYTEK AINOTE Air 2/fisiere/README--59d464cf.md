# iFLYTEK 1.0.3899 — România (+40)

Varianta adaugă **România (+40)** ca a patra opțiune în componenta comună de introducere a telefonului. Păstrează +86, +852 și +853, inclusiv traducerile existente ale denumirilor lor. Eticheta noii țări este `Romania`.

APK: [iflytek-1.0.3899-romania40.apk](../../dist/iflytek-1.0.3899-romania40.apk). Starea instalării și verificarea interfeței pe telefon se raportează separat de compilare; consultați raportul de dispozitiv când acesta există.

## Introducerea numărului și comunicarea cu serverul

Selectați **+40** și introduceți **9 cifre, începând cu 7**, fără zero-ul inițial și fără a repeta `40`. De exemplu, pentru forma locală `07xx xxx xxx`, câmpul primește `7xxxxxxxx`. Exemplele descriu formatul; nu sunt numere cărora li s-au trimis SMS-uri.

| Etapă | Parametru / valoare | Verificare |
|---|---|---|
| Selector Flutter | `+40`, text `Romania` | Lista are patru valori distincte |
| Limitarea câmpului și activarea butonului | 9 cifre | Ambele utilizări ale hărții de lungimi primesc 9 pentru +40 |
| Validare mobil România | `^7[0-9]{8}$` | Executată de codul ARM64; celelalte țări folosesc validatorul original |
| Apel Flutter către SDK | `countryCode: "40"` | Codul existent aplică `substring(1)` prefixului selectat |
| Trimitere SMS | `phone: "7xxxxxxxx"`, `ccode: "40"` | `u8.m` → `t8.R` → `/login/phone/sendMsgCode` |
| Autentificare cu parolă | `loginid: "7xxxxxxxx"`, `ccode: "40"` | `u8.j` → `t8.C` → `/login/account/byPwd` |

Serverul conturilor din APK este `https://account.xfinfr.com`. SDK-ul transmite țara separat; nu trebuie concatenat `+40` încă o dată în câmpul `phone/loginid`. Criptarea parolei, semnarea cererilor și verificările serverului sunt cele originale. Această modificare a clientului **nu dovedește că serverul acceptă înregistrarea, SMS-ul sau conturile din România**. Nu s-a simulat o autentificare reușită și nu s-au trimis SMS-uri de test.

## Ce s-a modificat

Se pornește de la APK-ul recompilat integral și verificat, SHA-256 `c10d5475f384d433884e44417126f1077478790241ab174bc5987a08a98f038c`. În această variantă se modifică exclusiv `lib/arm64-v8a/libapp.so`. Celelalte 79 de biblioteci, cele 6 DEX, cele 1.046 assets și manifestul sunt identice cu baza. Semnătura este refăcută cu același certificat local, astfel încât varianta poate actualiza baza locală deja instalată.

Analiza AOT cu [Blutter](https://github.com/worawit/blutter) a identificat Dart 3.10.9, snapshot `1ce86630892e2dca9a8543fdb8ed8e22`, ARM64 cu pointeri comprimați. Patch-ul este fixat la amprenta bibliotecii originale `17745c9106afa9fbdf3077ea2d0771437b1435371aec73d8ad13ef5e71ad2f06`; refuză alte versiuni.

| Zonă | Adresă / efect |
|---|---|
| `_PhoneNumberInputer` constructor | `0x156cebc`: literalul hărții crește la 4 perechi; +40 și Romania sunt alocate prin allocatorul Dart existent |
| `_PhoneNumberInputer.build` | `0x1283018`: lista de patru prefixe ajunge la maparea originală a widgeturilor |
| Formatter de lungime | `0x128390c`: +40 → 9; celelalte valori merg la harta originală |
| Listener `LoginProvider` | `0x11184c4`: aceeași regulă de lungime pentru starea butonului |
| `phoneNumberValidate` | `0xfa92d0`: validare mobil românesc, apoi delegare originală pentru celelalte prefixe |

Asamblarea nu reconstruiește sursele originale Dart. Extensia ARM64 este inclusă în spațiul liber al segmentului executabil ELF, cu limitele segmentului actualizate. Alocările păstrează adrese de apel existente și sloturi de stivă deja urmărite de GC. Se folosesc allocatorii și barierele de scriere originale; nu se fabrică antete de obiecte și nu se împarte manual memoria heap. Scalarea originală a interfeței este păstrată.

## Verificare și reproducere

`Build-Romania40.ps1` asamblează patch-ul, execută 22 de teste ARM64 cu Unicorn, înlocuiește strict biblioteca permisă, aliniază APK-ul, îl semnează și verifică întregul conținut ZIP. Testele includ limite de lungime, caractere invalide, zero inițial, delegarea pentru cele trei țări originale, generarea celor patru intrări și păstrarea scalării. Testele de emulator nu înlocuiesc verificările Flutter și GC pe telefon.

```powershell
.\variants\romania-40\Build-Romania40.ps1
```

Necesită mediul de bază documentat în proiect, Python cu `pyelftools` și `unicorn`, plus WSL cu Python/pyelftools și GNU binutils AArch64. Scriptul folosește distribuția locală `Codex-iFLYTEK-Analysis`. Cheia privată rămâne în directorul separat de semnare.

Dovezi: [modificări native](reports/native-patch.json), [teste ARM64](reports/native-tests.json), [dezasamblare patch](reports/patch-disassembly.txt), [audit APK](reports/archive-audit.json), [semnătură](reports/signature.txt). Acceptarea în cloud, autentificarea contului, Bluetooth, audio și OTA necesită verificări separate.
