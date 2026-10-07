# EVA-3dScan — identitate și campanie

## Marca

Nume vizibil: **EVA-3dScan**. Păstrăm litera E construită din trei bare, asociată acum unui volum și unui cadru de captură. Albastrul intens face aplicația ușor de recunoscut; turcoazul sugerează scanarea, iar coralul aduce căldură personajelor.

| Utilizare | Fișier |
|---|---|
| Iconiță aplicație, sursă vectorială | `public/assets/eva-app-icon.svg` |
| Iconiță aplicație, 1024 × 1024 px | `public/assets/eva-app-icon-1024.png` |
| Iconiță web pentru ecranul principal, 180 px | `public/assets/eva-app-icon-180.png` |
| Variantă mică, 32 px | `public/assets/eva-app-icon-32.png` |
| Simbol animat pentru site/interfață | `public/assets/eva-mark-animated.svg` |
| Siglă orizontală animată | `public/assets/eva-logo-animated.svg` |

Iconița de aplicație este livrată static, cu fundal opac. Variantele SVG animate sunt destinate site-ului și interfețelor care pot afișa animația; nu este promisă animarea iconiței de pe ecranul principal iOS. Sigla și simbolul animat opresc mișcarea când utilizatorul solicită mișcare redusă. Animația folosește CSS; documentele SVG nu permit executarea scripturilor.

O copie a identității este în `Aplicație/Identitate EVA-3dScan`. Versiunea anterioară a siglei rămâne păstrată, pentru istoric.

## Motto

**Îți capturăm forma. Te lăsăm fără cuvinte.**

Replica personajului: **„Hei, fața rămâne la mine!”**

Direcția propusă de utilizator — viteză, precizie și fața „furată” în telefon — este exprimată prin transferul vizual al unei copii holografice. Nu se prezintă o precizie sau un timp de scanare netestat drept rezultat măsurat.

## Cinci imagini originale

1. `01-capture.png` — un personaj cu iPhone capturează forma unei vaze; particulele formează modelul din telefon.
2. `02-face.png` — un bărbat indian contemporan, expresiv și amuzat, își păstrează fața; o copie holografică este transpusă în telefon. Replica este HTML tradus, nu text inclus în imagine.
3. `03-objects.png` — obiect și repere dimensionale pentru comunicarea modelului cu dimensiuni.
4. `04-measure.png` — măsurarea mobilierului, în contextul camerei.
5. `05-spaces.png` — camera este reprezentată ca apartament digital.

Toate originalele au 1536 × 1024 px și sunt păstrate în `public/assets/campaign`. Variantele WebP servite de site însumează 837.954 octeți. Fiecare imagine este un concept publicitar; nu reprezintă o captură a unei funcții implementate. Prompturile complete și proveniența sunt în `campaign-assets.json`; s-a folosit instrumentul integrat de generare a imaginilor, câte un apel pentru fiecare imagine. Conversia WebP schimbă numai codificarea, fără retușuri de conținut.

## Prima pagină

Ordinea informației: aplicație iPhone → trei module numerotate → intrare/proces/ieșire → publicul vizat. Caruselul ilustrează povestea; funcțiile aplicației sunt explicate și independent de acesta. Textul, descrierile imaginilor și comenzile sunt disponibile în toate cele șapte limbi.

Caruselul schimbă cadrul la 6,5 secunde și are comenzi manuale. Alegerea unui cadru oprește rotația automată. Hover-ul și focusul suspendă rotația; Play explicit permite reluarea. Preferința pentru mișcare redusă pornește caruselul în pauză. Actualizarea datelor păstrează pauza și focusul unui control activ.
