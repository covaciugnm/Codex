# Fara titlu

ID: `01a158d9-1156-73e3-9ce3-7d77ee0a3644`  
Proiect: cesiro.com  
Export UTC: 2026-11-02T15:26:35.221418+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Audit încheiat. Manifestul utilizabil pentru corectare este:

`Z:\00.Roboti\cesiro.com\work_nomexp\audit_formule\safe_formula_manifest.json`

Conține 63 corecții verificate în `NOMEXP02`:

- 38 formule externe în coloana I → nomenclator local, aceleași rezultate.
- 24 formule din coloana G → index VLOOKUP corect și interval ancorat.
- `I2747` → codul 9049, confirmat în două nomenclatoare locale.

Alte constatări:

- `GLAZ!K1986:K2015` și `M1986:M2015`: sursă externă lipsă; cache-ul extern nu conține aceste 30 SKU. Nu există bază sigură pentru completare.
- `BISC!B320`: extracția pozițională din `394_4010__B` produce `010_`, provocând trei `#VALUE!`. Se repară prin extragerea segmentului dintre delimitatori.
- 782 formule `LISGL1!Q2:Q783` au sursă eliminată. Reconstrucția beneficiarilor este parțial posibilă, dar în afara focalizării actuale pe SKU.
- Nu am găsit nume definite invalide, autoreferințe sau cicluri în scanarea statică.
- Cele 13.086 rânduri istorice incomplete au articole reale; trebuie păstrate.

Rapoarte suplimentare: `lookup_report.json`, `cycle_report.json`, `external2_cache_match.json`. Originalul nu a fost modificat.

## Asistent

Confirmat: **367 SKU unice cu prefix `5900_`**, exclusiv în `NOMEXP02!A`:

- `A3216:A3469`: 254 SKU.
- `A3503:A3615`: 113 SKU.

Cele 33 rânduri intercalate `A3470:A3502` au prefix `7700_` și trebuie excluse.

Am verificat toate cele 41 foi, toate coloanele și variantele cu spații: nu există alte apariții `5900_` sau surse istorice alternative pentru acest prefix.

Inventar complet: `Z:\00.Roboti\cesiro.com\work_nomexp\audit_formule\prefix5900_inventory.json`.

## Asistent

Nu am identificat altă eroare sintactică în formule: argumentele, virgulele, ghilimelele, referințele și tipurile celulelor sunt corecte. Prefixul XML `x:` este permis de OOXML; normalizarea lui merită testată ca problemă de compatibilitate.

Dacă aceasta nu rezolvă, soluția verificabilă este:

1. Extragi formulele înainte de reparare.
2. Deschizi cu `CorruptLoad=1`.
3. Restabilești formulele prin COM `.Formula`, în blocuri.
4. Salvezi nativ și redeschizi normal.

Aceasta folosește exact mecanismul pentru care testul `IF(1=1,2,3)` a funcționat. Nu am modificat fișierul.
