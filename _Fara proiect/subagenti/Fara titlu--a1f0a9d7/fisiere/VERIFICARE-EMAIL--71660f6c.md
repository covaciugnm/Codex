# Verificare email local — 25 septembrie 2026

Ambele site-uri rulează cu serviciu separat Mailpit și worker pentru coada PostgreSQL. Capturarea este forțată de overlay-ul explicit de dezvoltare, inclusiv dacă cineva configurează un alt SMTP în admin. Mesajele nu sunt expediate extern.

| Verificare | Dracula Design | Dracula Food |
|---|---|---|
| Înregistrare și mesaj de verificare în germană | Trecut | Trecut |
| Consum token de verificare prin API | Trecut | Trecut |
| Mesaj resetare parolă în engleză | Trecut | Trecut |
| Formular resetare deschis din link, parolă salvată, autentificare cu parola nouă | Trecut | Trecut |
| Refuz reutilizare token resetare | HTTP 400 | HTTP 400 |
| Logo original inclus în email | Da, inline | Da, inline |
| Dracula-Company și adresa corectă în footer | Dracula-Castel | Dracula-Farm |
| Nicio identitate CESIRO în mesajele noi | Trecut | Trecut |
| Căsuță independentă: mesajele nu ajung în celălalt site | Trecut | Trecut |

Acces local prin tunel SSH: Design http://127.0.0.1:4182 și Food http://127.0.0.1:4184. Portul SMTP nu este publicat; interfața HTTP este publicată doar pe loopback. Datele rămân în volume distincte `dracula_design_mail_capture` și `dracula_food_mail_capture`.

Textele email sunt salvate în PostgreSQL sub cheile `email.*`, cu RO/EN/DE. Brandingul, linkurile pentru cont/resetare/pagini legale și imaginile sunt adaptate fiecărui magazin. Coada fără SMTP configurat nu consumă încercările de trimitere.

SMTP extern rămâne neactivat: lipsesc hostul, portul/securitatea, utilizatorul și parola Dracula, expeditorul verificat și adresa de răspuns. Configurația CESIRO a fost inspectată numai pentru existența setărilor, fără copiere de credențiale. `docker-compose.smtp.yml` și instrucțiunile `ops/EMAIL.md` sunt pregătite pentru activarea separată ulterioară.

Verificarea notificării unei comenzi demo și a consumului linkului de verificare în frontend urmează după integrarea schimbărilor comune de checkout/frontend; nu sunt prezentate aici ca finalizate.
