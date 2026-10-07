# Plan produse stafide — Dracula Food

Catalogul editorial conține **17 propuneri**, separate în două categorii. Fiecare are nume și descriere RO / EN / DE, identificator stabil și instrucțiuni pentru imagine în `food/raisin-drafts.json`. Toate au statut **draft**, fără preț, gramaj, stoc sau imagine generată. Acest fișier nu publică produse și nu modifică baza de date.

## Stafide naturale și soiuri

Identificator categorie: `stafide-naturale`. Denumirea urmează structura listei primite; procesarea și eventuala prezență a aditivilor se verifică pentru fiecare produs.

1. **Stafide Thompson Seedless** — `stafide-thompson-seedless`
2. **Stafide Sultaniye** — `stafide-sultaniye`
3. **Stafide aurii Golden** — `stafide-golden`
4. **Stafide verzi** — `stafide-verzi`
5. **Stafide de Corint — Zante Currants** — `stafide-corint`
6. **Stafide Muscat de Alexandria** — `stafide-muscat-alexandria`
7. **Stafide roșii Flame Seedless** — `stafide-flame-seedless`
8. **Stafide Black Monukka** — `stafide-black-monukka`
9. **Stafide Rose Red** — `stafide-rose-red`
10. **Stafide Manukka** — `stafide-manukka`

Numele Sultaniye și Manukka sunt păstrate fără afirmarea țării de origine până la confirmarea furnizorului. Denumirile din listă sunt propuneri de sortiment, nu dovada soiului sau a provenienței produsului efectiv.

## Stafide aromatizate și infuzate

Identificator categorie: `stafide-aromatizate`.

1. **Stafide cu rom** — `stafide-rom`
2. **Stafide cu suc de fructe** — `stafide-suc-fructe`
3. **Stafide Paan** — `stafide-paan`
4. **Stafide cu rodie — Anardana** — `stafide-anardana`
5. **Stafide cu ciocolată și scorțișoară** — `stafide-ciocolata-scortisoara`
6. **Stafide macerate în vin** — `stafide-vin`
7. **Stafide glazurate** — `stafide-glazurate`

Aromele reprezintă direcții de produs. Ingrediente precum romul, vinul, fructele, betelul, ciocolata sau condimentele nu sunt tratate drept rețete confirmate. Nu se preiau afirmații de sănătate sau utilizări digestive din materialul inițial.

## Direcția imaginilor

Au fost inspectate cele două imagini originale cu nuci și alune. Referințele pentru ambalaj sunt:

- `food/assets/produse/dracula-food-nuci-dracula-farm.png`
- `food/assets/produse/dracula-food-alune-de-padure-dracula-farm.png`

Păstrăm cutia verticală neagră, textura fină, chenarul, perspectiva de trei sferturi și monograma DF argintie cu elementul roșu din ambalajul existent. Sigla nu se reinventează și nu se recolorează. Atmosfera rămâne cea din fotografii: masă întunecată, lumină caldă controlată, castel defocalizat în fundal. Compozițiile vor avea raport 3:2 și o scară constantă a cutiei.

Pentru fiecare sortiment se schimbă denumirea, stafidele și un accent cromatic discret. Marca rămâne **DRACULA FOOD**. Accentele aurii se folosesc moderat, fără modificarea monogramei. Nu se păstrează nuci sau alune în fotografiile noii colecții.

Machetele nu vor prelua automat gramajul de 500 g, steagurile, originea România, „din propria fermă”, „din Dracula-Farm”, „100% natural”, „fără aditivi” sau insignele de calitate de pe referințe. Acestea descriu imaginile primite, nu informații confirmate despre noile stafide. Numele Dracula-Farm poate rămâne identitatea locației companiei în site; nu se transformă într-o declarație de proveniență a stafidelor.

Detaliile vizuale ale fiecărui sortiment și numele propus al fișierului se află în JSON. În etapa de generare se vor folosi imaginile originale ca referințe de editare. Textul ambalajului va fi verificat separat, pentru consistență și lizibilitate. Imaginile nu au fost generate în această etapă.

## Date necesare înainte de activarea produselor

Pentru fiecare produs: denumirea comercială finală, confirmarea sortimentului și originii, ingrediente și alergeni, gramaj, preț și monedă, stoc, condiții de păstrare și informațiile de etichetare aplicabile. Pentru variantele cu rom sau vin se confirmă și conținutul de alcool. Aceste date rămân `null` în catalogul draft.

Fișierul primit a fost citit ca text. Codul Python din atașament nu a fost executat; afirmațiile sale despre origini, procese sau caracterul exhaustiv al listei nu au fost convertite în garanții comerciale.

