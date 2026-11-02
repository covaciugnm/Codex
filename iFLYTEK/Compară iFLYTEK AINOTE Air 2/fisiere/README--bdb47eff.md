# iFLYTEK Translate 1.0.3899 — proiect reconstruibil

**Varianta nouă pentru România (+40):** [documentație și APK](variants/romania-40/README.md). Are verificări proprii; rezultatele de instalare de mai jos aparțin bazei nemodificate. Varianta +40 este construită și semnată, dar instalarea ei așteaptă reconectarea telefonului prin USB.

Acest proiect reconstruiește APK-ul `com.iflytek.translateapp` din Smali și resurse Android. Cele șase DEX sunt reasamblate, resursele sunt recompilate, arhiva este aliniată și semnată cu o cheie locală. Binarele Flutter și native sunt păstrate integral.

**Starea curentă: APK recompilat, instalat și pornit pe Galaxy A14 cu Android 14.** Interfața în engleză, profilul și ecranul „Password Login” au fost deschise. Autentificarea efectivă și conectarea la ochelari rămân netestate. Fișierele JSON din `reports` sunt dovezile măsurate. Un rezultat static PASS nu înseamnă că funcțiile cloud sau Bluetooth au fost testate.

Conexiunea ADB cu Galaxy A14 SM-A146P a fost autorizată: Android 14, API 34, ARM64. APK-ul oficial instalat a fost verificat prin hash și certificat și afișa interfața în engleză. `reports/device-baseline.json` descrie această verificare a originalului; `reports/device-test.json` consemnează separat testele variantei reconstruite. Amprenta `testedApkSha256` trebuie să coincidă cu APK-ul evaluat.

## Fișiere

- `dist/iflytek-1.0.3899-full-rebuilt.apk`: APK reconstruit, semnat local.
- `dist/iflytek-1.0.3899-editable-source.zip`: proiect Apktool cu 47.219 fișiere Smali, resurse, assets și biblioteci native. Nu include cache-ul de build sau cheia de semnare.
- `Build.ps1`: decodare, recompilare, aliniere, semnare și verificări.
- `Setup-Tools.ps1` și `tools.lock.json`: unelte cu versiuni și SHA-256 fixate.
- `Audit-APK.cjs`, `Compare-Decoded.cjs`, `normalization.cjs`: verificări ale conținutului și echivalenței.
- `Check-Device.ps1`: diagnostic ADB numai prin citire; nu instalează și nu dezinstalează aplicații.
- `reports/full/`: loguri de build, certificat public, manifest, inventar și comparații.
- `index.html`: raport navigabil cu legături către APK, sursele editabile și dovezi; se regenerează cu `node .\Write-Report.cjs`.

## Reconstruire

Necesită Windows, PowerShell 7, Node.js și JDK 21. Uneltele Android și Apktool sunt descărcate automat din surse oficiale și verificate prin SHA-256. Nu este necesară instalarea Android Studio.

Din directorul acestui proiect:

```powershell
.\Build.ps1 -VerifyRoundTrip
.\Export-Source.ps1
.\Check-Device.ps1
node .\Write-Report.cjs
```

APK-ul de intrare este implicit `../Biblioteca_Glasses/Aplicatii/iflytranslate-official.apk`. SHA-256 obligatoriu:

```text
73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2
```

Căile de lucru implicite sunt `D:\CodexWork\iflytek-build-work`, `D:\CodexWork\iflytek-build-tools` și `D:\CodexWork\iflytek-build-private`. Se pot schimba prin parametrii `WorkDirectory`, `ToolDirectory`, `SigningDirectory`, `InputApk` și `Jdk`. Fișierele de lucru existente nu sunt șterse. Un director decodat fără amprenta sursei este refuzat, pentru a nu suprascrie alte modificări.

Pentru o verificare independentă, dintr-un director nou:

```powershell
.\Build.ps1 -WorkDirectory D:\CodexWork\iflytek-clean-build -VerifyRoundTrip
```

Pentru modificări ulterioare, se editează proiectul `decoded-full` din directorul de lucru și se rulează din nou Build. Modificările manifestului și metadatelor sunt oprite de verificările curente până la revizuirea lor explicită. `AllowCodeChanges` permite continuarea după o diferență de recompilare, dar nu transformă rezultatul FAIL din raport în PASS.

Arhiva editabilă se poate extrage într-un director nou `decoded-full`, aflat în `WorkDirectory` ales. Conține și amprenta sursei cerută de Build. APK-ul oficial rămâne necesar pentru comparațiile cu originalul. Scripturile de construire și raportare sunt în acest folder, separat de arhiva editabilă.

Modul `BinaryResources` este prevăzut în script pentru păstrarea resurselor binare. Raportul variantei `full` nu validează automat această variantă; trebuie construită și verificată separat înainte de utilizare.

## Ce verificăm

1. Identitatea APK-ului oficial și a uneltelor descărcate.
2. Construirea celor șase DEX și a resurselor fără erori de compilare.
3. Semnătura APK și alinierea ZIP cu `zipalign -P 16`.
4. Hashurile tuturor bibliotecilor native și fișierelor assets.
5. Numărul claselor, referințelor la metode și câmpuri pentru fiecare DEX.
6. Manifestul și metadatele Android; numerele de linie XML și căile de resurse redenumite sunt comparate separat de valori.
7. Re-decodarea APK-ului reconstruit și compararea tuturor fișierelor Smali și resurselor.

Normalizarea acceptă doar valori statice implicite `false`, `null`, `0x0`, `0x0L`, unificarea intervalelor consecutive cu aceiași handleri de excepții și ordinea declarațiilor enum/flag. Instrucțiunile și acoperirea fiecărei instrucțiuni de către handleri sunt comparate. Testele verificatorului includ modificări deliberate care trebuie respinse. [Formatul DEX, AOSP](https://source.android.com/docs/core/runtime/dex-format).

## Semnare și instalare

APK-ul rezultat are același package name și aceeași versiune ca originalul, dar este semnat cu o cheie locală. Android nu îl poate instala ca actualizare peste aplicația oficială semnată de producător. Scripturile nu dezinstalează aplicația oficială și nu șterg datele telefonului.

Cheia și parola se află exclusiv în directorul privat de semnare, cu acces limitat utilizatorului Windows și SYSTEM. Ele trebuie păstrate local pentru actualizările ulterioare ale acestei variante. Nu sunt incluse în Git, arhiva de surse, pagina HTML sau APK.

Pentru testare este necesar un dispozitiv Android ARM64 cu API 29 sau ulterior și un loc de instalare care nu intră în conflict cu pachetul oficial. Eliminarea aplicației oficiale ar necesita o decizie explicită și protejarea datelor; acest proiect nu execută această operație.

Pentru testul de pe Galaxy A14, utilizatorul a autorizat explicit înlocuirea aplicației oficiale și ștergerea datelor ei locale. APK-ul oficial a fost salvat pentru reinstalare; aceasta nu reprezintă o copie de siguranță a datelor aplicației.

Prima instalare a variantei reconstruite a fost respinsă cu `INSTALL_FAILED_VERIFICATION_FAILURE`. Și reinstalarea originalului a afișat un avertisment Play Protect despre o versiune Android mai veche. Originalul a fost reinstalat după confirmarea specifică pachetului, iar testul variantei reconstruite a fost reluat. Starea efectivă se citește din `device-test.json`. Nu au fost dezactivate protecțiile generale. [Google explică separat avertismentele Play Protect](https://developers.google.com/android/play-protect/warning-dev-guidance); mesajul observat nu stabilește singur de ce clasificarea a fost aplicată acestei configurații.

Autentificarea prin SMS nu a fost eliminată. „Password Login” este accesibil din dreapta sus a ecranului SMS. Ambele ecrane folosesc selectorul cu +86, +852 și +853. Codul păstrează `loginByPassword` și ruta `/login/account/byPwd`, dar prezența lor nu dovedește că un anumit cont este acceptat sau că serverul nu poate cere verificări suplimentare. Aceasta este varianta de bază, fără adăugarea României.

## Limite care rămân deschise

- Exportul Java/JADX cu 301 erori rămâne material de analiză. Nu este prezentat drept proiect Gradle reparat. Calea de build verificată folosește Smali.
- Sursele originale Dart/Flutter și C/C++ nu sunt recuperate. Bibliotecile AOT și JNI sunt binare păstrate; nu sunt recompilate din surse.
- Nu există cheia privată de semnare a producătorului. Serviciile care verifică certificatul sau integritatea aplicației pot respinge varianta reconstruită; acest lucru necesită testare efectivă.
- Autentificarea folosește serviciul original. Eliminarea unui ecran nu poate substitui validarea contului de către server. Suportul pentru numere +40 nu este adăugat de această recompilare.
- Profilurile ART originale din `assets/dexopt` sunt păstrate. Deoarece DEX-urile sunt reconstruite, profilurile pot să nu mai fie aplicabile; optimizarea și pornirea trebuie urmărite în testul pe dispozitiv.
- Alinierea ZIP la 16 KiB nu modifică alinierea ELF a bibliotecilor native și nu certifică singură compatibilitatea cu toate dispozitivele de 16 KiB.
- Instalarea și pornirea au fost testate pe Galaxy A14; funcțiile de cont, audio, traducere și legătura cu XF-AIGlasses-01 / firmware 1.0.01.88 nu sunt încă validate.

## Surse ale uneltelor

- [Apktool — utilizare](https://apktool.org/docs/cli-parameters/)
- [Android — apksigner](https://developer.android.com/tools/apksigner)
- [Android — zipalign](https://developer.android.com/tools/zipalign)
- [Samsung — opțiuni pentru dezvoltatori](https://developer.samsung.com/health/data/guide/phone-developer-options.html)
