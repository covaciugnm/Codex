# Nume distincte prin litere mari/mici pe Windows

APK-urile Translate conțin resurse distincte precum `res/2F.xml` și `res/2f.xml`. Windows nu le poate păstra sub aceste două nume în același director. Conținuturile originale sunt păstrate separat în CAS și manifestele raw; materializarea trebuie să adapteze numele fizice fără să piardă vreun fișier.

Materializatorul planifică toate căile înainte de scriere. Numele obișnuite rămân neschimbate. Numele care intră în conflict prin litere mari/mici, conflictele fișier/director și numele incompatibile cu Windows primesc un nume determinist din spațiul rezervat `_apkcase_`, cu SHA-256 al căii logice și tipului nodului. Numele originale care încep deja cu acest prefix sunt și ele codificate, astfel încât nu pot imita o cale generată. Sunt verificate atât căile complete, cât și prefixele directoarelor.

Fiecare director materializat primește **PATH-MAP.json**, care enumeră toate fișierele: componenta APK, calea originală, calea logică, calea fizică, dimensiunea și SHA-256. Maparea este reversibilă prin acest index. Se schimbă numai numele fizic necesar Windows; octeții fiecărui fișier sunt verificați față de manifestul original.

Pentru o execuție nouă, folosește un director de ieșire proaspăt. Un director existent fără același PATH-MAP.json este refuzat; fișierele vechi nu sunt șterse sau suprascrise. O execuție parțială care are deja aceeași mapare poate fi reluată, iar fișierele existente sunt verificate înainte de reutilizare.

Verificarea cu fișiere reale pe Windows și cazuri artificiale este în [audit/path-mapping-test-results.json](audit/path-mapping-test-results.json). Script: `node tools/test-apk-materializer-paths-20261101.cjs`.
