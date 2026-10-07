import os
os.chdir(r"Z:\00.Roboti\EVA.Pro\Learn\Traducator")
s = open('traducator.py', encoding='utf-8').read()
a = s.index("class Glosar:")
b = s.index("# ---------------------------------------------------------------- verificare automata")
new = r'''STOP_EN = set("""the a an and or but if then than that this these those there here is are was were be been being am do does did
have has had will would shall should can could may might must not no yes of to in on at by for with from into onto about
as it its it's i you he she we they me him her us them my your his our their what which who whom whose when where why how
all any some each every one two very more most much many such so too also just only own same other another again up down
out over under off then once""".split())

def lemme_en(w):
    """Forme de baza posibile ale unui cuvant englez (fara biblioteci)."""
    f = [w]
    if w.endswith("ies") and len(w) > 4: f.append(w[:-3] + "y")
    if w.endswith("es") and len(w) > 3: f.append(w[:-2])
    if w.endswith("s") and len(w) > 3: f.append(w[:-1])
    if w.endswith("ed") and len(w) > 4: f += [w[:-2], w[:-1]]
    if w.endswith("ing") and len(w) > 5: f += [w[:-3], w[:-3] + "e"]
    return f

class Glosar:
    """Glosar unificat (glosar.py -> glosar.sqlite) + rezerva: dictionarele ro/en directe."""
    MAX_CUVINTE = 10

    def __init__(self):
        p = os.path.join(AICI, "glosar.sqlite")
        self.g = sqlite3.connect(f"file:{p}?mode=ro", uri=True, check_same_thread=False) if os.path.exists(p) else None
        self.cache = {}

    def caut(self, limba, kl, cheie, n=3):
        key = (limba, kl, cheie)
        if key not in self.cache:
            res = []
            if self.g:
                with _lock:
                    res = [r[0] for r in self.g.execute(
                        "SELECT termen FROM g WHERE limba=? AND kl=? AND cheie=? ORDER BY n DESC LIMIT ?",
                        (limba, kl, cheie, n))]
            self.cache[key] = res
        return self.cache[key]

    def pentru(self, s, limba):
        g = {}
        refs = dict(s.get("refs") or {})
        if s.get("ref_en") and "en" not in refs: refs["en"] = s["ref_en"]
        refs[s["src"]] = s["text"]
        # 1) textul intreg, cand e scurt (vocabular), in toate limbile de referinta
        for kl, t in refs.items():
            t = str(t).strip()
            if t and len(t.split()) <= 3 and len(t) <= 40:
                hit = self.caut(limba, kl, glosar_norm(t))
                if hit: g[t] = hit
        # 2) cuvintele de continut din fraza engleza (referinta sau textul sursa englez)
        en = refs.get("en")
        if en and len(en.split()) > 3:
            vazute = 0
            for w in re.findall(r"[A-Za-z][A-Za-z'-]+", en):
                wl = w.lower()
                if wl in STOP_EN or len(wl) < 4 or wl in g:
                    continue
                for f in lemme_en(wl):
                    hit = self.caut(limba, "en", f, 2)
                    if hit:
                        g[wl] = hit; vazute += 1; break
                if vazute >= self.MAX_CUVINTE:
                    break
        return g

def glosar_norm(t):
    t = re.sub(r"\s*[\(\[].*?[\)\]]\s*", " ", str(t)).strip().lower()
    t = re.sub(r"^(to|a|an|the|un|o|der|die|das|le|la|les|el|los|las)\s+", "", t).strip(" .,;:!?\"'„”“")
    return t

'''
s = s[:a] + new + s[b:]
old = '''        g = glosar.pentru(s, L["dict"])'''
assert old in s
s = s.replace(old, '''        g = glosar.pentru(s, limba)''')
open('traducator.py', 'w', encoding='utf-8').write(s)
import ast; ast.parse(s); print("ok")
