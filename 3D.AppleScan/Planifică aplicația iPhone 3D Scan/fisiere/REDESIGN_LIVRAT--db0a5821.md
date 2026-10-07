# Livrare — identitate și prima pagină EVA-3dScan

2 octombrie 2026. Manager: agentul principal. Specialiști: campaign_assets, site_translations, auditor_final.

## Livrabile

- Iconiță distinctă pentru aplicație: SVG și PNG la 1024, 180 și 32 px. Copie în `Aplicație/Identitate EVA-3dScan`.
- Simbol și siglă orizontală animate pentru site, cu suport pentru preferința de mișcare redusă.
- Cinci imagini originale de campanie, în PNG, plus cinci WebP optimizate. Prompturile și proveniența sunt în `campaign-assets.json`.
- Prima pagină reconstruită: aplicație iPhone, trei funcții, ecuație intrare → proces → ieșire, public vizat. Stil luminos cu albastru, turcoaz și coral.
- Carusel cu cinci imagini, pauză, comenzi manuale, tastatură, păstrarea focusului la actualizare și subtitrări traduse.
- 51 chei noi de traducere în fiecare limbă; 190 chei per dicționar, 1.330 valori în total.

Motto: **Îți capturăm forma. Te lăsăm fără cuvinte.** Replica scenei cu portretul: **„Hei, fața rămâne la mine!”**

## Rezultate verificate

| Verificare | Rezultat | Raport |
|---|---|---|
| Backend și PostgreSQL real, după integrarea funcțiilor existente | 4 teste trecute, niciunul omis | `validation/backend-tests.txt` |
| Rute, limbi, mobil/desktop, descărcări, SSE | 117 verificări trecute | `validation/browser-report.json` |
| Carusel, cinci cadre × șapte limbi, focus, Play/Pause, SVG animat și mișcare redusă | 42 verificări trecute, inclusiv după ultima revizie a textelor | `validation/redesign-report.json` |
| Variabilă numerică modificată în PostgreSQL și actualizată în pagină | Trecut; valoarea inițială restaurată | `validation/live-variable.json` |
| Auth și proiecte existente | Rutele fără autentificare răspund 401, integrarea și granturile sunt păstrate | Inclus în raportul de 42 verificări |
| Audit independent | Zero constatări deschise în domeniul inspectat | `AUDIT_REDESIGN.md` |

Capturile `redesign-desktop.png`, `redesign-mobile.png` și `redesign-face.png` au fost examinate vizual. Cele cinci WebP au în total 837.954 octeți, iar originalele PNG sunt păstrate. Browserul încarcă imaginea cadrului selectat; nu introduce cinci fotografii mari în prima încărcare.

## Integrarea și istoricul corecțiilor

Pe server existau commituri mai recente pentru autentificare și proiecte. Copierea inițială din versiunea locală veche a înlocuit temporar trei fișiere de integrare. Diferența a fost identificată, cele trei fișiere au fost restaurate din versiunea curentă Git, iar politica necesară animației a fost reaplicată numai răspunsurilor SVG. Nu au fost șterse tabele sau date de utilizator. Rutele existente au fost reverificate.

Copia locală a acestor trei fișiere a avut apoi octeți NUL după transferul prin partajarea de rețea. A fost înlocuită prin transfer direct SSH, cu verificare SHA-256 și sintaxă. Auditorul a reverificat remedierea. Detaliile corecțiilor caruselului sunt în raportul independent.

Actualizarea editorială este limitată la `campaign.*`, trei texte hero, numele din footer și variabila `product`. Celelalte texte editate în baza de date sunt păstrate. Migrările SQL existente nu au fost rescrise.

## Continuare

Pentru conținut, editați variabilele și textele în PostgreSQL conform README. Pentru campanie, sursele sunt `public/app.js`, `public/campaign.css` și `public/assets/campaign`. Testul dedicat este `tests/redesign-browser.mjs`, inclus și în `ops/verify.sh`. Consultați `STATUS.json` și jurnalele managerului, traducătorului și auditorului.

Verificările folosesc Chromium pe desktop și viewport mobil. Nu se declară validare pe iPhone fizic, implementarea scanării, precizie măsurată sau audit complet al autentificării. Capturile din campanie sunt ilustrații ale conceptului.
