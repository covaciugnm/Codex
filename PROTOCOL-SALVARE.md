# Protocol de salvare a proiectelor și conversațiilor Codex

Versiunea 1.0 — 7 octombrie 2026

## Scop și structură

Păstrează istoricul local Codex organizat după proiect și titlul conversației, împreună cu răspunsurile, rezultatele instrumentelor și fișierele recuperabile. Fiecare rulare creează o salvare nouă; nu suprascrie salvările precedente și nu modifică istoricul din aplicație.

```text
Codex-Arhiva/
  PROTOCOL-SALVARE.md
  Salveaza-Codex.ps1
  export_codex.py
  verifica_arhiva.py
  salvari/
    AAAA-LL-ZZ_OO-MM-SS/
      README.md
      manifest.json
      SHA256SUMS.txt
      Nume proiect/
        README.md
        index.json
        arhiva-001.zip
        Titlul conversației/
          conversatie.md
          rezultate.md
          istoric.json
          metadate.json
          fisiere-index.json
          fisiere/
        subagenti/
          Titlul sesiunii subagentului/
      _Fara proiect/
```

Titlul original complet și ID-ul conversației sunt păstrate în metadate. Pentru compatibilitate Windows, caracterele interzise sunt înlocuite, titlurile lungi sunt scurtate la 80 de caractere, iar titlurile identice primesc un sufix din ID. În index, titlul complet conduce la subfolderul corespunzător. Proiectele fără conversații primesc un index care menționează explicit acest lucru.

## Procedura de salvare

1. Așteaptă terminarea conversațiilor pe care vrei să le păstrezi integral până la ultimul răspuns. Conectează unitățile și serverele pe care sunt fișierele proiectelor.
2. Deschide PowerShell în directorul `Codex-Arhiva` și rulează:

   ```powershell
   .\Salveaza-Codex.ps1
   ```

   Pentru altă destinație, de exemplu un disc de backup accesibil:

   ```powershell
   .\Salveaza-Codex.ps1 -Destinatie 'D:\Backup-Codex'
   ```

3. Așteaptă mesajul „Salvare verificata”. Scriptul folosește Python 3.11+ disponibil în runtime-ul Codex sau primit prin `-PythonExe`. Nu instalează programe.
4. Deschide `README.md` și `manifest.json`. Verifică numărul proiectelor, conversațiilor, mesajelor, fișierelor salvate și erorilor de citire.
5. Consultă `fisiere-index.json` din conversațiile importante. Starea `copiat` înseamnă fișier salvat, cu mărime și SHA-256. Celelalte stări descriu o referință care nu a fost salvată. Dacă un server devine disponibil, rulează din nou salvarea; rezultatul va fi într-un director nou.
6. Păstrează copia locală și o copie pe un mediu independent. Nu șterge originalele până când copia a fost verificată.

## Conținutul salvat

- `conversatie.md`: mesajele utilizatorului și asistentului, fără scurtare introdusă de export.
- `rezultate.md`: răspunsurile asistentului și evenimentele instrumentelor, inclusiv rezultatele disponibile în istoricul local.
- `istoric.json`: evenimentele structurate pentru procesare ulterioară.
- `fisiere/`: fișierele locale identificabile prin linkuri, atașamente, imagini generate și modificări de fișiere consemnate. Fișierele sunt copiate, nu mutate. Denumirile primesc un sufix pentru a evita suprascrierea fișierelor omonime.
- `fisiere-index.json`: corespondența dintre referințele originale și copiile salvate, plus fișierele indisponibile.
- `arhiva-*.zip`: volume ZIP independente, care conțin împreună copia dezarhivată a proiectului. Pentru restaurare, extrage toate volumele în același director. Fișierele individuale mai mari de 90 MiB pot produce un volum mai mare.
- `SHA256SUMS.txt`: sumele de control ale tuturor fișierelor din salvare.

Exportul nu poate reconstitui fișiere șterse, versiuni istorice nesalvate, rezultate deja trunchiate în istoricul sursă sau conținut disponibil exclusiv în cloud. Linkurile rămân consemnate, dar nu echivalează cu un fișier salvat. Fișierele externe sunt salvate în versiunea lor de la momentul copierii. Instrucțiunile de sistem, raționamentul intern și sesiunile interne de verificare nu sunt conversații ale utilizatorului și nu sunt incluse. Configurațiile de autentificare și cheile private nu sunt copiate ca fișiere; mesajele și rezultatele istorice pot totuși conține informații confidențiale.

## Reguli pentru salvările viitoare

La finalul unui rezultat important, salvează fișierul pe disc și include în răspuns un link către calea sa exactă. Păstrează fișierele finale într-un director stabil al proiectului, de preferință `rezultate/AAAA-LL-ZZ/`. Evită să lași singura copie într-un director temporar sau într-un link care expiră.

Folosește următoarea cerere în Codex:

> Aplică protocolul PROTOCOL-SALVARE.md: exportă proiectele și conversațiile locale, fiecare conversație într-un subfolder cu titlul ei, cu mesajele, rezultatele afișate și fișierele disponibile. Creează o salvare nouă, verifică ZIP-urile și SHA-256 și raportează separat fișierele indisponibile. Nu declara exportul complet dacă există date nerecuperate. Încarcă în depozitul GitHub convenit numai după verificarea destinației și a vizibilității sale.

Automatizarea „Salvare Codex și push la 6 ore” este activă în Codex, cu interval de 6 ore, în această conversație. Ea rulează salvarea, verifică rezultatul și compară amprentele de conținut ale proiectelor înainte de sincronizare. Acest protocol rămâne utilizabil și manual. Rularea depinde de disponibilitatea calculatorului și a aplicației.

## Salvarea în GitHub

Destinația este https://github.com/covaciugnm/Codex. Depozitul este public, iar utilizatorul a autorizat încărcarea după informarea privind vizibilitatea. GitHub CLI este autentificat ca `covaciugnm`, cu drept de scriere verificat. Conexiunea folosește HTTPS și autentificarea securizată GitHub CLI; nu necesită transferul cheii SSH.

La fiecare 6 ore, automatizarea redescoperă proiectele din baza Codex și din setările aplicației, precum și toate conversațiile locale. Sunt incluse automat proiectele noi, proiectele încă fără conversații, conversațiile noi și actualizările celor existente. Nu există o listă fixă de proiecte sau conversații.

`sincronizeaza_github.py DIRECTOR_SALVARE` verifică dreptul de push, integritatea salvării și amprentele proiectelor. Încarcă toate proiectele la prima rulare; ulterior face commit și push numai pentru proiectele noi sau modificate. Folosește Git LFS pentru ZIP-uri și fișiere de cel puțin 5 MiB. `--plan` oferă comparația locală fără publicare. După push, compară SHA-ul commitului local cu cel distant și salvează `ultima-incarcare.json`.

Copia locală rămâne integrală. În copia publicată, `protejeaza_publicarea.py` maschează cheile API, tokenurile și cheile private identificabile, inclusiv în volumele ZIP generate. Raportul `mascari-publicare.json` consemnează fișierele afectate fără a include valorile secrete. `SHA256SUMS-PUBLIC.txt` verifică copia publicată. Nu sunt omise conversații sau fișiere din cauza acestei mascări. Configurația locală `conexiune-github.json` nu se publică.

Dacă autentificarea expiră sau un fișier este indisponibil, automatizarea raportează problema și păstrează copia locală. Nu face force push, nu șterge istoricul și nu creează commituri goale. Nu inițiază achiziții sau modificări de abonament pentru stocare.

## Verificare și restaurare

Rulează verificatorul asupra unui director de salvare:

```powershell
& 'CALE\python.exe' .\verifica_arhiva.py 'CALE\salvari\AAAA-LL-ZZ_OO-MM-SS'
```

Poți citi direct copia dezarhivată sau extrage toate volumele ZIP ale unui proiect. Verifică SHA-256 înainte de a folosi copia restaurată. Exportul este o arhivă portabilă pentru citire și recuperarea fișierelor; nu este un mecanism garantat de reimport în bara laterală Codex.

