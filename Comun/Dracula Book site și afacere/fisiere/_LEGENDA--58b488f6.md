# LEGENDA — Structura folder `01. Acte Proprietate`

**Ultima actualizare:** 2026-07-11

Acest folder conține **exclusiv acte de proprietate**: cărți funciare (CF), extrase CF, decizii, planuri cadastrale, autorizații de construcție/demolare — atât ale firmelor, cât și ale persoanelor.

---

## 1. Structură top-level

```
01. Acte Proprietate/
├── _LEGENDA.md                (acest fisier)
├── 00. RAPORT/                (rapoarte + CSV cu documente gasite pe drive)
├── 01. FIRME/
│   └── {NUME FIRMA} SRL - CUI {CUI}/
└── 02. PERSOANE/
    └── {NUME PRENUME} - CNP {CNP}/
```

---

## 2. Denumire folder firmă / persoană

Identică cu convenția din `00. Firme` și `00. Persoane`:

**Firmă:** `{NUME FIRMA} SRL - CUI {CUI}`
**Persoană:** `{NUME PRENUME} - CNP {CNP}`

---

## 3. Sub-structură pentru o firmă / persoană

Fiecare folder de firmă sau persoană conține:

```
{NUME} SRL - CUI {CUI}/
├── CF {numar} - {localitate}/     ← un folder per carte funciara
│   ├── {CUI/CNP} Extras CF {numar} {data}.pdf
│   ├── {CUI/CNP} Decizie {tip} {data}.pdf
│   ├── {CUI/CNP} Plan cadastral {numar} {data}.pdf
│   ├── {CUI/CNP} Autorizatie constructie {numar} {data}.pdf
│   └── 99. Arhiva/                 ← extrase CF vechi/expirate
└── 99. Arhiva/                     ← CF-uri istorice complete
```

**Regulă:** un CF activ → un folder propriu, cu subfolderul `99. Arhiva/` pentru versiuni vechi.

---

## 4. Denumire fișier CF

**Format:**
```
{CUI/CNP} Extras CF {numar CF} {AAAA.LL.ZZ}.pdf
{CUI/CNP} Decizie {tip} {AAAA.LL.ZZ}.pdf
{CUI/CNP} Plan cadastral {numar} {AAAA.LL.ZZ}.pdf
```

Exemple:
- `12445967 Extras CF 75174 AB 2026.03.15.pdf`
- `1721019120687 Extras CF 12345 Ciugud 2025.10.20.pdf`

---

## 5. Reguli de valabilitate

**Extras CF** — este considerat valabil **30 zile** de la emitere pentru tranzacții.
La expirare → mută în `99. Arhiva/` și obține un extras nou de pe [portal.ancpi.ro](https://portal.ancpi.ro).

---

## 6. Ce NU se face

- ❌ NU se pun CF-uri direct în `01. FIRME/` sau `02. PERSOANE/` — MEREU într-un subfolder per CF
- ❌ NU se șterg extrasele CF vechi — se arhivează
- ❌ NU se amestecă CF-urile firmei cu cele personale ale administratorului
