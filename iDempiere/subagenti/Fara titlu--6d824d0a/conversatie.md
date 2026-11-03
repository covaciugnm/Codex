# Fara titlu

ID: `01a19e2f-f372-7942-bcad-99266d824d0a`  
Proiect: iDempiere  
Export UTC: 2026-11-03T03:30:08.376808+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Verific în sursele magazinului cum sunt separate coșul și comenzile între canale și ce vede un utilizator după reîncărcare. Rulez probele într-o copie locală identificată prin SHA-ul Git, la lățimi de desktop și mobil.

## Asistent

Am urmărit două cazuri din interfață până la datele salvate. În primul, coșul afișa produsul de 12 lei, iar comanda a înregistrat alt produs la 60 de lei. În al doilea, după deconectare, adresa fostului utilizator a rămas vizibilă la checkout. Ambele s-au reprodus pe desktop și mobil. Fișele includ și cazurile de control în care problema nu apare.

## Asistent

A08 a confirmat două probleme pe commitul `2fe90ed3`, în Chromium la 390 și 1280 px.

- **Magazinul poate salva alt produs decât cel ales.** Cumpărătorul a selectat produsul CPP de 12 lei. Când SKU-ul unui articol CPA coincidea cu ID-ul intern al produsului CPP, comanda a salvat articolul CPA de 60 lei. Totalul cu transport a devenit 89,99 lei în loc de 41,99 lei. Eliminarea coliziunii a restabilit rezultatul corect.
- **Adresa clientului rămâne vizibilă după deconectare.** Vizitatorul anonim care folosește același browser și canal vede adresa fostului client la checkout, inclusiv după reîncărcare. Pe un alt canal și într-un profil nou, câmpul a rămas gol.

Am predat către A12 cinci fișe de fișier și dovezile aferente. A11 le-a preluat pentru verificare independentă. Probele au folosit date sintetice și au urmărit efectele până la comanda salvată de magazin. Efectul asupra `C_OrderLine` în iDempiere rămâne de verificat. [Raport A08](<Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R11_fisiere/A08/A08_raport_R11.json>)
