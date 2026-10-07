# Surse și metodă — Dracula Food

Cercetare verificată la 2026-09-25. 19 produse, 57 fișe localizate RO/EN/DE.

Fișierul `food/product-enrichment.json` conține conținut editorial pentru integrarea în DB. Nu modifică produsele, prețurile sau stocurile. `nutrition.product_values` este null pentru toate produsele: lipsesc analizele sau declarațiile furnizorului.

## Nutriție

Valorile USDA au fost citite direct din API FoodData Central, nu deduse din site-uri terțe. Unitățile sunt explicite în chei. Baza este 100 g de parte comestibilă a ingredientului generic. Glucidele „by difference” includ fibrele; nu trebuie redenumite automat drept glucide pe o etichetă UE. Energia kJ este valoarea din înregistrarea USDA, fără recalculare. Nu au fost calculate procente din necesarul zilnic sau beneficii medicale.

Pentru Golden folosim înregistrarea dedicată, iar pentru Corint înregistrarea Zante. Celelalte selecții au referința generică pentru stafide închise fără sâmburi, fără a pretinde o analiză de soi. Pentru cele șapte produse compuse, tabelul descrie exclusiv ingredientul de bază; rețeta finală poate modifica substanțial valorile.

| Referință | FDC | kcal / 100 g |
|---|---:|---:|
| Nuts, walnuts, english | 170187 | 654 |
| Nuts, hazelnuts or filberts | 170581 | 628 |
| Raisins, dark, seedless (Includes foods for USDA's Food Distribution Program) | 168165 | 299 |
| Raisins, golden, seedless | 168164 | 301 |
| Currants, zante, dried | 171724 | 290 |

## Precizări editoriale

- Rose Red este denumire comercială nevalidată; nu i-am inventat genealogie sau origine.
- Manukka nu este echivalat automat cu Monukka. Sultaniye și Thompson pot fi sinonime botanice; diferențierea comercială trebuie documentată.
- Anardana este ingredient din rodie, nu soi de stafide. Paan nu dovedește compoziția, prezența betelului ori efecte digestive.
- Nu afirmăm proveniență din Dracula-Farm, procesare „fără aditivi”, absență de sulfiți, certificări sau gramaje comerciale neconfirmate.
- Istoria factuală are surse separate; poveștile de brand sunt marcate explicit „Poveste editorială”.
- Cele 19 propuneri culinare sunt formulări proprii, cu cantități și pași proprii și surse de inspirație. Nu sunt reproduceri ale rețetelor autorilor și nu implică afiliere. Sunt netestate în bucătărie; timpii sunt orientativi și includ repere de textură.
- Alergenii rețetelor de servire sunt declarați separat de compoziția comercială. Variantele cu rom/vin pot păstra alcool; alternativa cu suc este explicită.
- Temperatura de depozitare, durata de viață, materialele de contact, compoziția și declarația de alergeni necesită fișele furnizorului.

## Registrul surselor

### usda-170187

[USDA FoodData Central: Nuts, walnuts, english](https://fdc.nal.usda.gov/food-details/170187/nutrients) — consultat 2026-09-25.

Generic ingredient composition, not a Dracula Food batch or product analysis.

### usda-170581

[USDA FoodData Central: Nuts, hazelnuts or filberts](https://fdc.nal.usda.gov/food-details/170581/nutrients) — consultat 2026-09-25.

Generic ingredient composition, not a Dracula Food batch or product analysis.

### usda-168165

[USDA FoodData Central: Raisins, dark, seedless (Includes foods for USDA's Food Distribution Program)](https://fdc.nal.usda.gov/food-details/168165/nutrients) — consultat 2026-09-25.

Generic ingredient composition, not a Dracula Food batch or product analysis.

### usda-168164

[USDA FoodData Central: Raisins, golden, seedless](https://fdc.nal.usda.gov/food-details/168164/nutrients) — consultat 2026-09-25.

Generic ingredient composition, not a Dracula Food batch or product analysis.

### usda-171724

[USDA FoodData Central: Currants, zante, dried](https://fdc.nal.usda.gov/food-details/171724/nutrients) — consultat 2026-09-25.

Generic ingredient composition, not a Dracula Food batch or product analysis.

### walnut-history

[California Walnut Board — History](https://walnuts.org/about-walnuts/history/) — consultat 2026-09-25.

Persian/English walnut naming and trade history; no claim about our lot origin.

### hazelnut-history

[Hazelnut Industry Office — About U.S. Hazelnuts](https://oregonhazelnuts.org/about/) — consultat 2026-09-25.

Oregon orchard history; no claim about our lot origin.

### fps-sultanina

[UC Davis Foundation Plant Services — Thompson Seedless (Sultanina)](https://fps.ucdavis.edu/FGRfamilies.cfm?varietyid=1516) — consultat 2026-09-25.

Verified cultivar synonyms, including Sultaniye.

### golden-process

[Sun-Maid — Industrial Ingredients](https://www.sunmaid.com/industrial/ingredients/) — consultat 2026-09-25.

Golden colour and commercial processing examples; no assertion that Dracula Food uses these processes.

### green-study

[Proteomic analyses on the browning of shade-dried Thompson seedless grape](https://link.springer.com/article/10.1186/s13765-021-00612-7) — consultat 2026-09-25.

Primary research on shade drying and green raisin colour; not evidence of this product origin.

### zante-history

[Sun-Maid — Raisins & Dried Fruits, chapter 5](https://www.sunmaid.com/wp-content/uploads/2019/02/US-Edition_Ch5.pdf) — consultat 2026-09-25.

Zante/Black Corinth distinction from currant berries.

### fps-varieties

[UC Davis Foundation Plant Services — Grape Varieties](https://fps.ucdavis.edu/fgrvarieties.cfm) — consultat 2026-09-25.

Muscat of Alexandria and Monukka recorded as table/raisin cultivars.

### fps-flame

[UC Davis Foundation Plant Services — Flame Seedless](https://fps.ucdavis.edu/FGRfamilies.cfm?varietyid=648) — consultat 2026-09-25.

Red grape cultivar released in 1973 in the USA; not product provenance.

### raisin-industry

[California Raisin Marketing Board — The Raisin Industry](https://calraisins.org/about/the-raisin-industry/) — consultat 2026-09-25.

Dried grapes and raisin processing categories; no historical claim for unverified commercial names.

### betel-botany

[Royal Botanic Gardens, Kew — Piper betle](https://powo.science.kew.org/taxon/680605-1) — consultat 2026-09-25.

Botanical identity of betel; no medicinal or health claims.

### anardana

[Spices Board India — Pomegranate](https://www.indianspices.com/spice-catalog/pomegranate.html) — consultat 2026-09-25.

Anardana is dried pomegranate seed with pulp used as a spice; it is not a raisin variety.

### nuts-storage

[University of California — Nuts: Safe Methods for Consumers](https://ucfoodsafety.ucdavis.edu/sites/g/files/dgvnsk7366/files/inline-files/44384.pdf) — consultat 2026-09-25.

Generic cool, sealed storage guidance; not a commercial shelf-life validation.

### recipe-pear

[West Virginia University Extension — Walnut and Honey Baked Pears](https://extension.wvu.edu/food-health/recipes/2021/07/13/walnut-and-honey-baked-pears) — consultat 2026-09-25.

Inspiration limited to the pear/walnut pairing; our quantities, plating and method are original.

### recipe-chocolate

[Andrew Gravett / Great British Chefs — Chocolate and hazelnut tart](https://www.greatbritishchefs.com/recipes/chocolate-hazelnut-tart-andrew-gravett-recipe) — consultat 2026-09-25.

Inspiration limited to dark chocolate with hazelnuts; original dessert cups, not a reproduction of the tart.

### recipe-couscous

[Ottolenghi — Giant couscous with golden raisins, lemon and almonds](https://ottolenghi.co.uk/pages/recipes/giant-couscous-golden-raisins-lemon-almonds) — consultat 2026-09-25.

Inspiration limited to fruit/grain/herb contrast; our recipes use independent ingredients and quantities.

### recipe-carrots

[Ottolenghi — Roasted carrots with curry leaf dukkah](https://ottolenghi.co.uk/pages/recipes/roasted-carrots-curry-leaf-dukkah) — consultat 2026-09-25.

Inspiration limited to roasted vegetables over yoghurt; original raisin versions.

### recipe-scones

[King Arthur Baking — Cream Tea Scones](https://www.kingarthurbaking.com/recipes/cream-tea-scones-recipe) — consultat 2026-09-25.

Inspiration: small teatime pastries. Our butter-based currant rounds are an independent formulation.

### recipe-rice

[Jamie Oliver — Icelandic rice pudding](https://www.jamieoliver.com/recipes/rice/icelandic-rice-pudding/) — consultat 2026-09-25.

Inspiration limited to creamy rice and fruit contrast; original cardamom versions.

### recipe-rum

[Susan Reid / King Arthur Baking — Rum-Raisin Bread](https://www.kingarthurbaking.com/recipes/rum-raisin-bread-recipe) — consultat 2026-09-25.

Inspiration limited to rum and raisins with bread; our baked custard cups use an independent method.

### recipe-oats

[Jamie Oliver — Mothership overnight oats](https://www.jamieoliver.com/recipes/fruit/mothership-overnight-oats/) — consultat 2026-09-25.

Inspiration limited to overnight soaking; independent citrus parfait formulation.

### recipe-aubergine

[Ottolenghi — Bruschetta with aubergine](https://ottolenghi.co.uk/pages/recipes/bruschetta-aubergine) — consultat 2026-09-25.

Inspiration limited to aubergine/pomegranate pairing; original plated recipe.

### recipe-berry

[Ottolenghi — Berry platter with sheep’s labneh and orange oil](https://ottolenghi.co.uk/pages/recipes/berry-platter-sheeps-labneh-orange-oil) — consultat 2026-09-25.

Inspiration limited to fruit against a creamy dairy base; our ricotta cups use their own formulation.

### recipe-rose

[Nigella Lawson — Pear, Pistachio and Rose Cake](https://www.nigella.com/recipes/pear-pistachio-and-rose-cake) — consultat 2026-09-25.

Inspiration limited to the rose/pistachio pairing; our cold dairy cup is not a reproduction of the cake.

### recipe-bark

[Lorraine Elliott / Not Quite Nigella — Easy Easter Chocolate Bark](https://www.notquitenigella.com/2018/04/01/easter-chocolate-bark-recipe/) — consultat 2026-09-25.

Inspiration limited to broken chocolate-sheet presentation; own fruit/nut combination.
