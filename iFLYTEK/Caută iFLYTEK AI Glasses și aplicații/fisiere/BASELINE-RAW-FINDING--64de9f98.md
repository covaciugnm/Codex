# Diferență confirmată față de vechea extracție raw

Auditorul a comparat toate intrările APK-ului oficial Translate 1.0.3899, SHA-256 `73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2`, cu vechiul arbore `Software/APK_Reconstituit_2026-10-30/extras/apk`.

- APK-ul are **2.341 intrări de fișier și zero intrări de director**. Numărul nu include directoare fictive.
- Vechea extracție are **2.264 de fișiere**.
- Există **77 de perechi de nume confundate de Windows**, toate cu conținut diferit, de exemplu `res/2F.xml` și `res/2f.xml`.
- În arborele vechi lipsesc **77 de căi logice exacte**; pentru alte **75 de căi prezente**, hashul diferă de intrarea cu acel nume din APK. Conținutul uneia dintre variante a fost suprascris sub o altă capitalizare a numelui.

Dovezile complete sunt în [audit/baseline-case-loss.json](audit/baseline-case-loss.json), iar inventarul tuturor coliziunilor este în [audit/case-collision-inputs.json](audit/case-collision-inputs.json).

Constatarea privește vechiul arbore **raw `extras/apk`**; nu demonstrează automat aceeași problemă în proiectele decodate cu apktool, Smali sau în fiecare artefact istoric. Arhiva istorică este păstrată pentru proveniență.

Noua analiză citește intrările direct din fiecare APK și verifică fiecare conținut după CRC32, SHA-256 și mărime. Inventarul raw păstrează toate cele 2.341 de fișiere ale acestui APK. La materializarea pe Windows, `PATH-MAP.json` menține legătura dintre fiecare nume original și un nume fizic unic, astfel încât ambele resurse rămân accesibile.

Reutilizarea conținutului vechi este bazată pe **hash**, nu pe presupunerea că vechea cale descrie corect numele original. Fiecare fișier materializat este verificat din nou față de intrarea APK curentă. Acest mecanism păstrează conținutul corect și evită încărcarea lui încă o dată.
