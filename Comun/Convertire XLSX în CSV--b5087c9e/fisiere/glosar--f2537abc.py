# -*- coding: utf-8 -*-
"""Glosar unificat din TOATE bazele lexicale din EVA_Learn_Import_35 -> glosar.sqlite

Pentru fiecare limba tinta X (codurile din config.json -> limbi.*.dict) aduna perechi (limba_cheie, cheie, termen_X):
  - eva_en / eva_ro / eva_de / eva_fr / eva_es : cheie -> X           (directia originala)
  - bazele limbii X (toate .sqlite din folderul ei, ex. Alar pt. kn): X -> en/ro/de/fr/es, INVERSAT
  - definitiile scurte X -> en (Kaikki/Alar: "water; liquid") sunt sparte in chei de 1-3 cuvinte
Exclus implicit: bazele din foldere "Drepturi_neconfirmate_*" (pornire cu --cu-drepturi-neconfirmate) si
"Complementar_Punjabi_generic_pa" (Gurmukhi, nu Shahmukhi).
Rulare:  python glosar.py [--limbi bn,ur] [--cu-drepturi-neconfirmate]
"""
import argparse, glob, json, os, re, sqlite3, sys, time
from collections import Counter

AICI = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(AICI, "config.json"), encoding="utf-8"))
RAD = os.path.dirname(os.path.dirname(os.path.dirname(CFG["dictionare"]["ro"])))  # ...\EVA_Learn_Import_35
OUT = os.path.join(AICI, "glosar.sqlite")
CHEI = ("en", "ro", "de", "fr", "es")
ARTICOLE = re.compile(r"^(to|a|an|the|un|o|der|die|das|le|la|les|el|los|las)\s+", re.I)

def norm(t):
    t = re.sub(r"\s*[\(\[].*?[\)\]]\s*", " ", str(t)).strip().lower()
    t = ARTICOLE.sub("", t).strip(" .,;:!?\"'„”“")
    return t

def chei_definitie(text):
    """'water; a liquid' -> ['water', 'liquid']  (doar bucati de 1-3 cuvinte)."""
    out = []
    for p in re.split(r"[;,/]| or ", str(text)):
        p = norm(p)
        if p and 1 <= len(p.split()) <= 3 and len(p) <= 40:
            out.append(p)
    return out

def baze_limba(coduri, cu_neconf):
    meta = json.load(open(os.path.join(RAD, "limbi.json"), encoding="utf-8"))
    for m in meta:
        if set(m["codes"]) & set(coduri):
            for f in glob.glob(os.path.join(RAD, m["folder"], "**", "*.sqlite"), recursive=True):
                if "Complementar_Punjabi_generic_pa" in f: continue
                if "Drepturi_neconfirmate" in f and not cu_neconf: continue
                yield f

SCRIPT = {"bengali": "ঀ-৿", "arabic": "؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿",
          "devanagari": "ऀ-ॿ", "telugu": "ఀ-౿", "tamil": "஀-௿", "kannada": "ಀ-೿",
          "gujarati": "઀-૿", "ethiopic": "ሀ-᎟", "myanmar": "က-႟", "malayalam": "ഀ-ൿ",
          "oriya": "଀-୿", "thai": "฀-๿", "cyrillic": "Ѐ-ӿ", "sinhala": "඀-෿",
          "khmer": "ក-៿", "han": "㐀-鿿豈-﫿", "tifinagh": "ⴰ-⵿"}
IPA = re.compile("[ɐ-˿ʰ-˿ᴀ-ᶿ̀-̃̅-ͯ]|[˥˦˧˨˩]")

def termen_valid(x, script):
    """Doar termeni scrisi in alfabetul limbii tinta; fara transcrieri IPA/fonetice."""
    if IPA.search(x):
        return False
    if script == "latin":
        return not re.search("[Ͱ-῿ⴰ-⵿　-￿]", x)
    return bool(re.search(f"[{SCRIPT[script]}]", x)) and not re.search("[A-Za-z]", x)

def ro_conn(p):
    return sqlite3.connect(f"file:{p}?mode=ro", uri=True)

def construieste(limba, coduri, cu_neconf, out):
    t0 = time.time()
    n = Counter()          # (cheie_lang, cheie, termen) -> numar surse/randuri
    q = ",".join("?" * len(coduri))
    # 1) directia originala: eva_<cheie>.sqlite, word=cheie -> text=X
    for kl in CHEI:
        p = os.path.join(RAD, {"en": "01_Engleza_en", "de": "02_Germana_de", "fr": "03_Franceza_fr",
                               "es": "04_Spaniola_es", "ro": "05_Romana_ro"}[kl], "DB", f"eva_{kl}.sqlite")
        if not os.path.exists(p): continue
        for w, x in ro_conn(p).execute(
                f"SELECT word,text FROM entries WHERE target_lang IN ({q}) AND kind='translation'", coduri):
            k, x = norm(w), str(x).strip()
            if k and x and len(x) <= 60: n[(kl, k, x)] += 1
    # 2) bazele limbii tinta, inversat: word=X -> text=cheie
    for p in baze_limba(coduri, cu_neconf):
        con = ro_conn(p)
        for w, tl, kind, x in con.execute(
                f"SELECT word,target_lang,kind,text FROM entries WHERE source_lang IN ({q}) "
                f"AND target_lang IN ('en','ro','de','fr','es') AND kind IN ('translation','definition')", coduri):
            w = str(w).strip()
            if not w or len(w) > 60: continue
            if kind == "translation":
                k = norm(x)
                if k and len(k) <= 60: n[(tl, k, w)] += 1
            else:
                for k in chei_definitie(x):
                    n[(tl, k, w)] += 1
    sc = CFG["limbi"][limba]["script"]
    n = Counter({k: v for k, v in n.items() if termen_valid(k[2], sc)})
    out.execute("DELETE FROM g WHERE limba=?", (limba,))
    out.executemany("INSERT INTO g(limba,kl,cheie,termen,n) VALUES(?,?,?,?,?)",
                    [(limba, kl, k, x, c) for (kl, k, x), c in n.items()])
    out.commit()
    per = Counter(kl for kl, _, _ in n)
    print(f"{limba:8} {len(n):9} perechi  {dict(per)}  {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--limbi"); ap.add_argument("--cu-drepturi-neconfirmate", action="store_true")
    a = ap.parse_args()
    out = sqlite3.connect(OUT)
    out.executescript("""CREATE TABLE IF NOT EXISTS g(limba TEXT, kl TEXT, cheie TEXT, termen TEXT, n INT);
                         CREATE INDEX IF NOT EXISTS g_cheie ON g(limba, kl, cheie);""")
    limbi = a.limbi.split(",") if a.limbi else [l for l, v in CFG["limbi"].items() if not v.get("existent")]
    for l in limbi:
        if CFG["limbi"][l].get("glosar") is False: continue
        construieste(l, CFG["limbi"][l]["dict"], a.cu_drepturi_neconfirmate, out)
