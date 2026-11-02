# Autentificare SMS, cont și servicii iFLYTEK

Verificare: 1 noiembrie 2026. Acest raport adaugă concluzii noi și referă resursele deja arhivate; nu dublează aplicațiile sau paginile originale.

## Ce confirmă documentația oficială

[Politica aplicației iFLYTEK Translate](https://saas-public.ioss.xfinfr.com/private/config/privacy-policy.html), secțiunea 1.1, descrie înregistrarea/autentificarea prin număr de telefon și cod SMS. Numărul este necesar pentru acest flux. Traducerea de bază poate fi folosită fără cont, dar anumite servicii, inclusiv traducerea imersivă și interpretarea, necesită autentificare. Nu rezultă că toate funcțiile ochelarilor sunt disponibile fără cont.

[Politica contului iFLYTEK](https://saas-public.ioss.xfinfr.com/private/config/account-privacy.html) descrie contul comun mai multor produse, parola opțională, verificarea SMS și verificarea suplimentară dacă este necesară. Mai descrie autentificarea rapidă prin SDK China Mobile; disponibilitatea acestui mecanism pentru SIM-uri străine nu este confirmată. Politica generală amintește și conturi terțe, dar acest lucru nu dovedește că fiecare opțiune este expusă în aplicația pentru ochelari.

Documentul contului din 11 mai 2024 precizează că serviciul descris vizează China și că datele sunt stocate în China continentală, inclusiv prelucrarea acolo a datelor provenite din Hong Kong/Macao. Această constatare privește serviciul descris de document; nu stabilește arhitectura tuturor produselor internaționale iFLYTEK.

## Pagina de logare

Pe [platforma iFLYTEK Translate](https://www.iflytranslate.com/), logarea este implementată ca dialog „登录/注册” / Login/Register. Nu am confirmat o adresă separată și stabilă `/login` pentru acest dialog. Documentația aplicației și autentificarea din aplicație sunt distincte de pagina web.

În JavaScript-ul oficial deja arhivat, selectorul dialogului definește exact:

| Regiune | Prefix | Lungimea numărului local în formular |
|---|---|---|
| China continentală | +86 | 11 cifre |
| Hong Kong | +852 | 8 cifre |
| Macao | +853 | 8 cifre |

România +40, UK +44 și SUA +1 nu apar în această listă a formularului web. Aceasta dovedește o limitare a interfeței analizate, nu un răspuns al serverului despre livrarea SMS către aceste țări. Existența limbii engleze sau a unui APK diferit nu dovedește acceptarea prefixelor internaționale.

Formularul prevede cod de verificare de 6 cifre și parametru `expire:300` la solicitarea codului. Acestea sunt valori trimise/configurate de client, fără confirmarea comportamentului efectiv al serverului. Există și logare prin parolă. Textul interfeței spune că numerele neînregistrate sunt înregistrate automat după logare.

## Servere și API-uri identificate în codul public

| Server / domeniu | Rol demonstrat în client |
|---|---|
| `https://account.xfinfr.com` | Baza SDK-ului de cont și autentificare |
| `https://transsaas.iflytranslate.com` | Baza cererilor pentru serviciile platformei de traducere |
| `https://gw.xftrans.cn` | Gateway al unui alt modul de traducere prezent în client |
| `https://account.xunfei.cn` | Legături către regulile și politica contului; nu trebuie confundat cu baza API SMS de mai sus |
| `https://saas-public.ioss.xfinfr.com` | Documente publice și politici |

SDK-ul include următoarele căi relative; nu au fost apelate pentru această verificare:

| Cale | Rol în SDK |
|---|---|
| `/login/phone/sendMsgCode` | Solicitare cod SMS pentru logare |
| `/login/phone/checkCode` | Verificare cod și logare |
| `/register/phone/sendMsgCode` | Solicitare cod pentru înregistrare |
| `/register/phone/checkCode` | Verificare cod de înregistrare |
| `/register/phone/submit` | Finalizare înregistrare |
| `/login/account/byPwd` | Autentificare prin parolă |
| `/general/query/getCcode` | Metodă SDK pentru codurile de țară; rezultatul serverului nu a fost verificat |

Codul trimite prefixul `ccode` și numărul `phone` la solicitarea codului, apoi `phone`, `mcode` și `msgid` la verificare. Serviciile autentificate folosesc o sesiune/token; în clientul web apar antetele `X-Auth-Token` și `X-Auth-User`. Simpla editare a selectorului sau a prefixului din APK nu confirmă acceptarea de către server.

## Serviciile conectate

Pagina și politica oficială descriu traducere text, documente, audio/video, interpretare, cont, istoric și sincronizare. Politica aplicației conține secțiuni dedicate ochelarilor: asociere Bluetooth, interpretare, traducerea apelurilor și conversațiilor, traducere offline, teleprompter, fotografie/video și importul fișierelor prin Wi-Fi.

Clientul public include și trimiteri către `tongchuan.iflyrec.com` (interpretare), `yizhi.iflyrec.com` (producție/traducere media) și `fanyi.iflyrec.com` (traducere umană). Existența trimiterilor și a mecanismului de transfer al sesiunii nu înseamnă că toate serviciile sunt incluse în abonamentul ochelarilor.

## Dovezi și limite

- Sursa tehnică: [iflytranslate-index-Ca1undxD.js](resources/iflytranslate-index-Ca1undxD.js), descărcată anterior de pe `https://www.iflytranslate.com/assets/index-Ca1undxD.js`. SHA-256 și proveniența sunt în [assets.json](assets.json). Selectorul poate fi găsit după `reigonChinaMainland`, API-urile după `getLoginCode` / `loginByCode`, baza de cont după `https://account.xfinfr.com`.
- Politicile publice au fost reverificate prin căutare web. Reîncercarea descărcării directe a JavaScript-ului live a expirat; constatările tehnice se referă la snapshotul arhivat din aceeași zi.
- Nu s-au trimis SMS-uri, nu s-a creat sau accesat un cont, nu s-au testat numere de telefon și nu s-au accesat date private. Nu s-a verificat funcționarea efectivă a logării cu +40.
- Nu a fost găsit în această verificare un portal de autentificare UE separat, confirmat compatibil cu modelul XF-AIGlasses-01.

Concluzie: cerința SMS este documentată oficial; suportul pentru un număr românesc rămâne neconfirmat și nu poate fi dedus din schimbarea aplicației sau a interfeței.
