# Audit preliminar al software-ului propriu

Referință GitHub: `build/reproducible-apk-20261031`, commit `4792f6b38e2c51e8d98c9fbc0b537ef6a521db8f`.

Verdict: păstrarea statică a componentelor este susținută de dovezi; implementarea și funcționarea tuturor funcțiilor NU sunt încă certificate. Proiectul reasamblează aplicația originală din Smali și păstrează binarele Flutter/native. Sursele originale Dart și C/C++ nu sunt recuperate.

| Funcție / verificare | Baza full-rebuilt | România +40 |
|---|---|---|
| Instalare și pornire | Confirmate pe Galaxy A14 / Android 14 | Netestate; WAITING_FOR_USB |
| Interfață profil / SMS / parolă | Ecrane observate | Netestată |
| Cod și resurse Android | Raport roundtrip PASS; 176 diferențe normalizate, fără diferențe nerezolvate | Cele 6 DEX și manifestul identice cu baza |
| Biblioteci native și assets | Raport original–bază: 80 native / 1046 assets identice | Comparație refăcută: 79 native / 1046 assets identice; numai libapp.so schimbat |
| Selector România / validare 9 cifre | Absent | 22 teste ARM64 raportate PASS; randare Flutter și GC pe telefon netestate |
| SMS / parolă / înregistrare în cloud | Netestate | Netestate; prefixul 40 în client nu confirmă acceptarea serverului |
| Asociere și reconectare Bluetooth | Netestate | Netestate |
| Transfer foto / video prin Wi-Fi | Netestat | Netestat |
| Captură / redare / transfer audio | Netestate | Netestate |
| Traducere / limbi / offline / interpretare | Netestate funcțional | Netestate funcțional |
| Teleprompter / apeluri / sincronizare / OTA | Netestate | Netestate |

## Verificări refăcute în această sesiune

- Cele două APK-uri corespund hashurilor publicate: baza `c10d5475f384d433884e44417126f1077478790241ab174bc5987a08a98f038c`; România `82aa11096fbd474f0669b5ca295e325fd0b0c45c2999360859d1bd93821a9aa8`.
- Comparație a conținutului decomprimat: 2337 intrări identice, una modificată (`lib/arm64-v8a/libapp.so`), zero intrări lipsă sau adăugate. Nu compară blocurile de semnătură APK.
- Verificatorul existent: 9 teste de echivalență și regresii deliberate PASS. Aceste teste validează verificatorul; nu testează funcțiile aplicației.
- Cele 8 documente GitHub sunt salvate cu hash și proveniență în snapshot.json. Rapoartele istorice nu au fost prezentate drept teste noi pe telefon.

## Țări

Selectorul original: China continentală (+86), Hong Kong (+852), Macao (+853). Varianta modificată adaugă România (+40). Acestea sunt opțiuni de client, nu o listă de autentificări reușite. Nicio țară nu are în aceste dovezi un test end-to-end de conectare la cont și ochelari.

## Condiții pentru verdict funcțional complet

Testarea trebuie să lege fiecare rezultat de SHA-ul APK, dispozitiv, firmware, cont/regiune și versiunea serverului observată. Sunt necesare verificări reale ale contului, Bluetooth, media, limbilor, istoricului, permisiunilor, reconectării și erorilor. Acceptarea în cloud și comportamentul Flutter/GC nu sunt demonstrate de egalitatea fișierelor sau de emularea ARM64. Nu este atribuit 10/10 funcțional și nu este autorizat niciun commit prin acest document.

Verificare curentă la 2 noiembrie 2026: `adb devices -l` nu afișează niciun dispozitiv conectat. Testele hardware nu pot fi reluate în configurația curentă. Nu s-a instalat sau dezinstalat nicio aplicație.

## Constatări independente ale executantului

- Comparația ZIP și cele 12 intervale native au fost confirmate independent: 527 octeți modificați, fără modificări în afara intervalelor declarate.
- În fixture-ul Unicorn, x28=2, deci x28 >> 32 este zero; calea lentă a barierei GC nu este exercitată. Sunt necesare verificări sub presiune GC și randare reală.
- test_native.py preia hashul bibliotecii din metadate, fără să îl recalculeze direct pentru intrarea testului. Ambalarea îl verifică separat; testul izolat are o lacună de proveniență.
- Verificările Python folosesc assert, care poate fi dezactivat prin optimizare.
- Dovada independentă: D:/Codex-iflytek-own-software-audit-20261102/independent-payload-check.json. Nu s-au rerulat testele Unicorn în această sesiune.
