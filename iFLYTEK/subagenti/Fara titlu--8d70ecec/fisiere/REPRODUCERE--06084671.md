# Repetarea analizei statice

Sunt necesare Node.js, Java 21 și GitHub CLI autentificat cu acces la repository. Nu sunt necesare instalarea APK-urilor sau autentificarea în serviciile iFLYTEK. Pentru viteză și spațiu, folosește un disc local cu câțiva GB disponibili.

```powershell
$env:IFLYTEK_APK_WORK_ROOT='D:/iflytek-analysis-work'
$env:IFLYTEK_APK_CAS_ROOT='D:/iflytek-analysis-work/cas'
$env:IFLYTEK_JAVA='C:/Program Files/Java/jdk-21/bin/java.exe'
node tools/prepare-apk-analysis-20261101.cjs
node tools/analyze-apk-versions-20261101.cjs
node tools/decompile-apk-versions-20261101.cjs --force
node tools/finalize-apk-analysis-20261101.cjs
```

Pregătirea folosește fișierele existente local sau descarcă exact artefactele referite de manifestele acestei analize, apoi verifică dimensiunea și SHA-256. JADX 1.5.6 este preluat din [Release-ul oficial skylot/jadx](https://github.com/skylot/jadx/releases/tag/v1.5.6); arhiva și JAR-ul sunt verificate față de [toolchain.json](toolchain.json). Analiza decompilată rulează explicit clasa `jadx.cli.JadxCLI`, cu un singur proces Java și două fire de lucru. Cache-ul și temporarele sunt direcționate în directorul de lucru.

Scripturile refac manifestele locale; folosește o clonă sau un checkout de lucru separat dacă dorești să păstrezi neatins raportul publicat. JADX poate produce text ușor diferit între rulări/configurații; hashurile fișierelor raw extrase trebuie să fie identice. Nu se pretinde reproducerea unui APK recompilat și semnat de furnizor.

`--force` reexecută decompilările noi chiar dacă rapoartele publicate există deja. Fără acest parametru, un raport este reutilizat numai dacă toate obiectele CAS pe care le cere există local și au hashul și dimensiunea corecte. Într-o clonă nouă, existența raportului JSON singur nu este suficientă pentru a omite decompilarea. Setul DEX de bază, deja decompilat și arhivat anterior, este referit în continuare fără duplicare.

Ultima etapă reutilizează indexul existent [baseline-release-index.json](baseline-release-index.json), al cărui audit păstrează hashurile arhivelor originale. Maparea sa privește aceleași arhive Release imuabile după hash; niciun fișier identic nu trebuie încărcat încă o dată.
