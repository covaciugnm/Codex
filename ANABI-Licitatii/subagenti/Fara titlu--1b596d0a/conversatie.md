# Fara titlu

ID: `01a13066-4b94-79f1-a48e-b0441b596d0a`  
Proiect: ANABI-Licitatii  
Export UTC: 2026-10-13T08:28:59.767902+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Am salvat inventarul complet:

- `sources/insolventa/listings.json`: **2.308 anunțuri**, toate cu detalii.
- `sources/insolventa/coverage.json`: acoperire, număr pe categorii, verificări și limite.
- `sources/insolventa/collect.cjs`: colector reutilizabil cu paginare dinamică.

Categorii: Afaceri 57, Altele 791, Auto 443, Imobiliare 520, Industrial 444, Office 53.

Schema include titlu, sursă, categorie/subcategorie, preț și monedă originale, județ/localitate, fotografie, descriere integrală, publicator, publicare/expirare, data/ora licitației și `attributes`. Auto are marcă/an/combustibil; imobiliarele au suprafețe, camere și tip teren unde sunt publicate.

Validat: ID-uri unice, toate detaliile descărcate, zero erori, 2.059 prețuri numerice. Sursa include și postări vechi din 2018; nu trebuie prezentate automat drept licitații active.
