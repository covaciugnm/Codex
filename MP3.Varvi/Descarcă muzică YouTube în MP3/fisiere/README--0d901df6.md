# MP3 Varvi

Aplicație locală în Python + HTML pentru piese și playlisturi YouTube / YouTube Music.

## Pornire pe Windows

1. Python 3.11+ și Node.js 22+ sau Deno trebuie instalate. JavaScript este necesar pentru provocările playerului YouTube.
2. Dublu clic pe `Porneste.cmd`. Prima pornire instalează dependențele în `.venv`, inclusiv FFmpeg prin imageio-ffmpeg.
3. Deschide http://127.0.0.1:8765 și introdu linkul. Păstrează consola deschisă până la final.

Fișierele sunt salvate în `downloads`, lângă aplicație. Playlisturile au foldere separate; piesele individuale sunt în `Piese individuale`. Copiază folderul dorit pe stick. Pentru player sunt suficiente fișierele MP3; CSV/JSON/JPEG sunt utile pentru arhivă.

## Metadate și denumiri

### Import din Excel

În pagină, alege fișierul `.xlsx` și apasă **Verifică linkurile**. După previzualizare, apasă **Descarcă linkurile importate**. Se utilizează calitatea MP3 selectată sus. Importul citește toate foile, inclusiv cele ascunse, în ordinea lor, apoi rândurile în ordine. Foile fără coloană de linkuri sunt afișate ca omise.

Modelul `outputs/party_20261008/Model_playlist_masa_si_petrecere.xlsx` este recunoscut: antet pe rândul 7, `Link YouTube` în G, date de la rândul 8. Completează linkurile și salvează fișierul înainte de import. Nu este necesar Microsoft Excel instalat pentru citire.

Sunt acceptate URL-uri directe, hyperlinkuri Excel și formule `HYPERLINK` cu un URL literal; alte formule nu sunt evaluate. Antetul este căutat în primele 50 de rânduri: `Link YouTube`, `YouTube`, `YouTube URL`, `URL` sau `Link`. Fișierele `.xls` trebuie salvate ca `.xlsx`.

Linkurile identice după normalizare sunt descărcate o singură dată per import. Videoclipurile care apar în playlisturi diferite pot produce duplicate. Rândurile goale sunt ignorate; cele completate fără link, linkurile invalide și duplicatele apar în raportul previzualizării. Un link indisponibil nu oprește restul importului.

Salvare: `downloads/Excel - nume fișier/număr - foaie/`, cu subfolder pentru fiecare playlist, când există. Același nume de fișier și aceeași ordine a foilor reutilizează folderele la următoarele importuri; fișierele MP3 existente sunt păstrate. Folderele modelului furnizat sunt deja create. Numele MP3 și etichetele muzicale provin în continuare din YouTube. Numele fișierului Excel, foaia, rândul și valorile originale ale rândului se păstrează în CSV și JSON. Fișierul Excel original nu este modificat.

Limite: 10 MB încărcare, 40 MB decomprimat, 20.000 rânduri și 200 coloane per foaie, maximum 2.000 de linkuri distincte. Previzualizările expiră la repornirea serverului sau după încă cinci importuri. Descărcarea rulează în backend, pe rând, chiar dacă pagina este închisă, cât timp serverul rămâne pornit.

- `Artist - Piesă.mp3`: metadate muzicale YouTube dacă există; altfel separare la primul ` - `, ` – ` sau ` — ` din titlul original. Această deducție poate necesita corectare. Canalul nu este presupus artist. Dacă nu există indicii, artistul este `Artist necunoscut`.
- Nu sunt eliminate mențiunile „Official Video” etc. Titlul YouTube complet este păstrat separat în ID3, CSV și JSON. Caracterele incompatibile cu Windows sunt înlocuite, iar numele foarte lungi sunt scurtate.
- ID3v2.3 + ID3v1: artist, titlu, album, artist album, gen, data lansării, număr piesă/disc, licență, descriere, URL și câmpuri suplimentare, dacă sunt disponibile. Data încărcării nu este prezentată drept data lansării. Albumul poate folosi numele playlistului, cu proveniența indicată.
- Copertă JPEG de maximum 600×600 inclusă în MP3 când miniatura poate fi citită. MP3 stereo, 44,1 kHz, bitrate selectabil. 320 kbps nu recuperează informație pierdută în sursă.
- `catalog.csv` în fiecare folder și unul general, UTF-8 cu BOM pentru Excel. Textul cu potențial de formulă este prefixat cu apostrof. Câmpurile necunoscute rămân goale.
- Fișier `.info.json` pentru fiecare MP3: metadate normalizate și informațiile returnate de yt-dlp; poate conține URL-uri media temporare. Nu sunt garantate versuri, compozitor, ISRC sau alte informații pe care YouTube nu le oferă.
- La coliziuni se adaugă ID-ul YouTube și apoi un contor; fișierele existente nu sunt suprascrise. O nouă descărcare poate crea duplicate.

## Funcționare și limite

### Pauze pentru YouTube

Aplicația procesează o singură descărcare și un singur fragment simultan. Așteaptă 20 de secunde între operațiunile de citire/descărcare YouTube (inclusiv între citirea metadatelor și descărcarea aceleiași piese), 2 secunde între cererile extractorului și 8 secunde înaintea descărcării media. Interfața afișează pauza dintre operațiuni. Aceste intervale reduc ritmul; nu garantează că YouTube va permite accesul.

La HTTP 429, CAPTCHA sau mesaje de verificare anti-bot, se oprește întregul import/playlist. Fișierele deja salvate rămân pe disc. Pornirile noi sunt blocate minimum 30 de minute, inclusiv după repornirea aplicației; nu există reluare automată. Nu se fac reîncercări automate la erorile extractorului, fișierelor sau fragmentelor. O eroare obișnuită a unei piese permite continuarea celorlalte după pauză. Aplicația nu simulează identitatea unui utilizator și nu ocolește verificările YouTube.

O singură descărcare activă; playlisturile sunt procesate piesă cu piesă. Erorile unei piese nu opresc restul. Progresul este ținut în memorie și poate fi urmărit după reîncărcarea paginii, dar nu după repornirea serverului. Fișierele finalizate rămân pe disc. Lucrările întrerupte pot lăsa fișiere în subfolderul `.work`.

Aplicația ascultă doar pe `127.0.0.1:8765`. Nu are autentificare pentru acces în rețea și nu trebuie expusă pe internet. Nu importă cookie-uri și nu ocolește restricții de acces; videoclipurile private, restricționate sau blocate de YouTube pot eșua. Descarcă numai conținut pentru care ai drepturile necesare.

Unele mașini nu afișează coperți sau toate câmpurile ID3. Verifică manualul pentru capacitatea/formatul stickului și limitele playerului.

Pentru actualizarea extractorului: `.venv\Scripts\python.exe -m pip install --no-cache-dir -U "yt-dlp[default]"`. Componentele EJS pentru provocările YouTube sunt instalate împreună cu pachetul yt-dlp.

Teste: `.venv\Scripts\python.exe -m unittest discover -s tests -v`.

Referințe: https://github.com/yt-dlp/yt-dlp și https://mutagen.readthedocs.io/en/latest/api/id3.html
