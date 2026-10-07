# -*- coding: utf-8 -*-
"""EVA Learn — traducator in masa cu LLM local (Ollama / vLLM / llama-server).

Comenzi:
  python traducator.py extrage                      # citeste Excel-ul -> segmente unice in tm.sqlite
  python traducator.py traduce --limbi de,bn        # traduce (se poate opri si relua oricand)
        [--foi "Texte fixe,Lecții A1"] [--max 200] [--paralel 4]
  python traducator.py stare                        # progres pe limbi
  python traducator.py exporta --limbi de           # scrie iesire/EVA-traducere-de-<data>.xlsx
  python traducator.py viteza [--paralel 1,4,8]     # masoara viteza serverului
"""
import argparse, concurrent.futures as cf, datetime, json, os, re, sqlite3, sys, threading, time, urllib.request
from collections import Counter, defaultdict

AICI = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(AICI, "config.json"), encoding="utf-8"))
TM = os.path.join(AICI, "tm.sqlite")
IESIRE = os.path.join(AICI, "iesire")
PROMPT = open(os.path.join(AICI, "prompt_sistem.txt"), encoding="utf-8").read()
_lock = threading.Lock()

# ---------------------------------------------------------------- baza de date (memorie de traducere)

def db():
    c = sqlite3.connect(TM, timeout=60, check_same_thread=False)
    c.execute("PRAGMA journal_mode=DELETE")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS seg(id INTEGER PRIMARY KEY, src TEXT, text TEXT, ref_en TEXT, ctx TEXT,
        foaie TEXT, prio INT, ord INT, mod TEXT, UNIQUE(src,text));
    CREATE TABLE IF NOT EXISTS tr(seg INT, limba TEXT, text TEXT, stare TEXT, eroare TEXT, model TEXT, ts TEXT,
        PRIMARY KEY(seg,limba));
    CREATE INDEX IF NOT EXISTS tr_limba ON tr(limba,stare);
    """)
    if "refs" not in [r[1] for r in c.execute("PRAGMA table_info(seg)")]:
        c.execute("ALTER TABLE seg ADD COLUMN refs TEXT")
    return c

# ---------------------------------------------------------------- detectie romana / engleza

RO_DIA = set("ăâîșțşţĂÂÎȘȚŞŢ")
RO_CUV = set("""si și este sunt să sa nu ce care pentru cu pe din la mai cel cea cei cele lui ei eu tu noi voi ai fost sau dar
când cand cum unde foarte acest această aceasta acesta de una unei unui ale alege scrie corectează corecteaza traduce
completează completeaza cuvântul cuvantul propoziția propozitia răspuns raspuns ori iar fiindcă deci""".split())
CUV = re.compile(r"[A-Za-zÀ-ÿĂÂÎȘȚăâîșțşţŞŢ']+")

def are_romana(t):
    if any(ch in RO_DIA for ch in t):
        return True
    return any(w.lower() in RO_CUV for w in CUV.findall(t))

def mod_en(tip, camp, text):
    """Pentru randurile doar cu Text EN: 'llm' daca au parti in romana, 'copie' daca sunt engleza pura, 'sari' la optional."""
    tip = (tip or "").strip()
    if "opțional" in tip:
        return "sari"
    camp = re.sub(r"\[\d+\]", "[]", camp or "").split(".")[-1]
    if (tip == "en-ro" and camp in ("answer", "options[]")) or (tip == "ro-en" and camp == "question") \
            or (tip == "translate-ro-en" and camp == "question"):
        return "llm"
    return "llm" if are_romana(text) else "copie"

# ---------------------------------------------------------------- extragere

def coloane(h):
    g = lambda *n: next((h.index(x) for x in n if x in h), None)
    return dict(ro=g("Text RO"), en=g("Text EN (de învățat)", "Text EN"), camp=g("Câmp", "Câmp EN"),
                tip=g("Tip", "Tip / id"), fis=g("Lecție", "Fișier", "Sursă"),
                out_ro=g("Traducere RO → limba nouă", "Traducere"), out_en=g("Versiune EN → limba nouă"))

def extrage(a):
    import openpyxl
    wb = openpyxl.load_workbook(CFG["fisier_sursa"], read_only=True)
    ordine = CFG["ordine_foi"]
    c = db()
    n_nou = 0; ord_ = 0
    for ws in wb.worksheets:
        if ws.title not in ordine:
            continue
        prio = ordine.index(ws.title)
        it = ws.iter_rows(values_only=True)
        h = [str(x) for x in next(it)]
        k = coloane(h)
        for r in it:
            ord_ += 1
            ro, en = r[k["ro"]], r[k["en"]] if k["en"] is not None else None
            camp = r[k["camp"]] if k["camp"] is not None else None
            tip = r[k["tip"]] if k["tip"] is not None else None
            fis = r[k["fis"]] if k["fis"] is not None else None
            ctx = " / ".join(str(x) for x in (ws.title, fis, camp, tip) if x)
            if ro:
                src, text, mod = "ro", str(ro), "llm"
                ref = str(en) if en and len(str(en)) <= 300 else None
            elif en:
                src, text, ref = "en", str(en), None
                mod = mod_en(tip, camp, text)
            else:
                continue
            cur = c.execute("INSERT OR IGNORE INTO seg(src,text,ref_en,ctx,foaie,prio,ord,mod) VALUES(?,?,?,?,?,?,?,?)",
                            (src, text, ref, ctx, ws.title, prio, ord_, mod))
            n_nou += cur.rowcount
        print(f"  {ws.title}: gata", flush=True)
    incarca_referinte(c)
    for i, foaie in enumerate(ordine):  # prioritatea urmeaza ordinea curenta din config
        c.execute("UPDATE seg SET prio=? WHERE foaie=?", (i, foaie))
    c.commit()
    for row in c.execute("SELECT mod,count(*),sum(length(text)) FROM seg GROUP BY mod"):
        print(f"  mod={row[0]}: {row[1]} segmente, {row[2]} caractere")
    print(f"segmente noi: {n_nou}")

def incarca_referinte(c):
    """Traducerile existente si verificate EN/RO/DE/FR/ES ale aceluiasi text (fisierul TOATE-LIMBILE)."""
    import openpyxl
    p = CFG.get("referinte")
    if not p or not os.path.exists(p):
        print("  (fara fisier de referinte)"); return
    wb = openpyxl.load_workbook(p, read_only=True)
    dupa_ro, dupa_en = {}, {}
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        h = [str(x) for x in next(it)]
        ix = {k: h.index("Text " + k.upper()) for k in ("en", "ro", "de", "fr", "es") if "Text " + k.upper() in h}
        if "en" not in ix or "ro" not in ix:
            continue
        for r in it:
            d = {k: str(r[i]) for k, i in ix.items() if r[i]}
            if d.get("ro"): dupa_ro.setdefault(d["ro"], d)
            if d.get("en"): dupa_en.setdefault(d["en"], d)
    n = 0
    rows = c.execute("SELECT id,src,text FROM seg WHERE mod='llm'").fetchall()
    for sid, src, text in rows:
        d = dupa_ro.get(text) if src == "ro" else (dupa_en.get(text) or dupa_ro.get(text))
        if d:
            c.execute("UPDATE seg SET refs=? WHERE id=?", (json.dumps(d, ensure_ascii=False), sid)); n += 1
    c.commit()
    print(f"  referinte EN/DE/FR/ES: {n} / {len(rows)} segmente")

# ---------------------------------------------------------------- glosar din dictionare

STOP_EN = set("""the a an and or but if then than that this these those there here is are was were be been being am do does did
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

# ---------------------------------------------------------------- verificare automata

SCRIPT = {"bengali": "ঀ-৿", "arabic": "؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿",
          "devanagari": "ऀ-ॿ", "telugu": "ఀ-౿", "tamil": "஀-௿", "kannada": "ಀ-೿",
          "gujarati": "઀-૿", "ethiopic": "ሀ-᎟", "myanmar": "က-႟", "malayalam": "ഀ-ൿ",
          "oriya": "଀-୿", "thai": "฀-๿", "cyrillic": "Ѐ-ӿ", "sinhala": "඀-෿",
          "khmer": "ក-៿", "han": "㐀-鿿豈-﫿", "tifinagh": "ⴰ-⵿"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆↔-⇿]")
GHILIMELE = re.compile(r"[„\"“”«](.+?)[”\"“»]")

def multiset(rx, t):
    return Counter(re.findall(rx, t))

def verifica(sursa, trad, limba, ctx=""):
    """Intoarce lista de probleme (goala = ok)."""
    p = []
    if not isinstance(trad, str) or not trad.strip():
        return ["gol"]
    for nume, rx in (("${…}", r"\$\{[^}]*\}"), ("tag HTML", r"</?[a-zA-Z][^>]*>"), ("___", r"_{2,}"),
                     ("|", r"\|"), ("`cod`", r"`[^`]*`"), ("**", r"\*\*"), ("cifre", r"\d+")):
        if multiset(rx, sursa) != multiset(rx, trad):
            p.append(f"{nume} diferit")
    vocab = bool(re.search(r"vocab|words|srs|\.ro", ctx or ""))
    if sursa.count("/") != trad.count("/") and not (vocab and trad.count("/") < sursa.count("/")):
        p.append("/ diferit")
    if Counter(EMOJI.findall(sursa)) != Counter(EMOJI.findall(trad)):
        p.append("emoji diferit")
    if sursa.count("\n") != trad.count("\n"):
        p.append("randuri diferite")
    for q in GHILIMELE.findall(sursa):  # engleza citata trebuie sa ramana identica
        if len(q) > 2 and not are_romana(q) and re.search(r"[A-Za-z]{2}", q) and q not in trad:
            p.append(f"engleza schimbata: {q[:40]}")
    sc = CFG["limbi"][limba]["script"]
    if sc != "latin":
        if any(ch in RO_DIA for ch in trad):
            p.append("a ramas romana")
        if are_romana(sursa) and not re.search(f"[{SCRIPT[sc]}]", trad):
            p.append("nu e in scrierea limbii")
    elif are_romana(sursa) and len(sursa) > 12 and trad.strip() == sursa.strip():
        p.append("netradus")
    elif limba != "ro" and sum(ch in "ăâîșțşţ" for ch in trad) >= 2 and limba not in ("az", "uz"):
        p.append("a ramas romana")
    return p

# ---------------------------------------------------------------- apel model

def servere():
    """Lista serverelor din config: "servere": [...] (fiecare completat cu "server_implicit")."""
    lst = CFG.get("servere") or [CFG["server"]]
    return [dict(CFG.get("server_implicit", {}), **s) for s in lst]

def cere_model(srv, system, user):
    if srv.get("backend", "ollama") == "ollama":
        opt = {"temperature": srv.get("temperature", 0.2), "num_predict": 12000}
        if srv.get("num_ctx"): opt["num_ctx"] = srv["num_ctx"]
        body = {"model": srv["model"], "stream": False, "think": False, "format": "json",
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "options": opt}
        url = srv["url"].rstrip("/") + "/api/chat"
    else:  # openai-compatibil: vLLM, llama-server
        body = {"model": srv["model"], "temperature": srv.get("temperature", 0.2), "max_tokens": 12000,
                "response_format": {"type": "json_object"}, "chat_template_kwargs": {"enable_thinking": False},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
        url = srv["url"].rstrip("/") + "/v1/chat/completions"
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=srv.get("timeout_s", 3600)))
    if srv.get("backend", "ollama") == "ollama":
        return r["message"]["content"], r.get("eval_count", 0)
    return r["choices"][0]["message"]["content"], r.get("usage", {}).get("completion_tokens", 0)

def prompt_limba(limba):
    L = CFG["limbi"][limba]
    return PROMPT.replace("{LIMBA}", L["nume"]).replace("{ADRESARE}", L["adresare"])

def traduce_lot(srv, lot, limba, glosar, nota=""):
    """Trimite lotul; modelul intoarce {"t": [traducere_0, traducere_1, ...]} in aceeasi ordine."""
    L = CFG["limbi"][limba]
    items = []
    for i, s in enumerate(lot):
        x = {"id": i, "src": s["src"], "text": s["text"], "ctx": s["ctx"]}
        refs = {k: v for k, v in (s.get("refs") or {}).items() if v and v != s["text"] and (k != "ro" or s["src"] == "en")}
        if refs:
            x["ref"] = refs
        elif s.get("ref_en"):
            x["en"] = s["ref_en"]
        g = glosar.pentru(s, limba)
        if g: x["gloss"] = g
        items.append(x)
    user = (nota + "\n" if nota else "") + f"{len(items)} segments -> return exactly {len(items)} strings.\n" \
        + json.dumps(items, ensure_ascii=False)
    raw, tok = cere_model(srv, prompt_limba(limba), user)
    data = json.loads(raw)
    lista = data.get("t", []) if isinstance(data, dict) else data
    out = {}
    if isinstance(lista, list) and len(lista) == len(lot):
        for s, x in zip(lot, lista):
            if isinstance(x, dict): x = x.get("tr")
            if isinstance(x, str): out[s["id"]] = x
    return out, tok

def loturi(segs):
    m, mc = CFG["lot"]["max_segmente"], CFG["lot"]["max_caractere"]
    cur, n = [], 0
    for s in segs:
        if cur and (len(cur) >= m or n + len(s["text"]) > mc):
            yield cur; cur, n = [], 0
        cur.append(s); n += len(s["text"])
    if cur:
        yield cur

# ---------------------------------------------------------------- traducere

def salveaza(c, srv, limba, rezultate):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    with _lock:
        c.executemany("INSERT OR REPLACE INTO tr(seg,limba,text,stare,eroare,model,ts) VALUES(?,?,?,?,?,?,?)",
                      [(sid, limba, t, st, er, srv["model"], ts) for sid, (t, st, er) in rezultate.items()])
        c.commit()

NOTA_REFACERE = ("ATTENTION: a previous attempt broke the rules (placeholders, ___, /, |, emoji, Western digits, line breaks "
                 "and English parts must be kept exactly; everything Romanian must be translated). Be careful.")

def proceseaza(srv, lot, limba, glosar, c, stat):
    rez = {}
    de_refacut = list(lot)
    for incercare in range(3):
        if not de_refacut:
            break
        bucati = [de_refacut] if incercare == 0 else [de_refacut[i:i + 5] for i in range(0, len(de_refacut), 5)]
        urmatoare = []
        for b in bucati:
            try:
                out, tok = traduce_lot(srv, b, limba, glosar, NOTA_REFACERE if incercare else "")
                stat["tok"] += tok
            except Exception as e:  # JSON stricat / timeout -> se reia in loturi mici
                out = {}; stat["erori"] += 1
                print(f"[{limba}] eroare lot ({len(b)} seg): {type(e).__name__}: {str(e)[:120]}", flush=True)
            for s in b:
                t = out.get(s["id"])
                probl = verifica(s["text"], t, limba, s.get("ctx")) if t is not None else ["lipsa din raspuns"]
                vechi = rez.get(s["id"])
                if not probl:
                    rez[s["id"]] = (t, "ok", None)
                    continue
                if t and (not vechi or len(probl) <= len((vechi[2] or "").split("; "))):
                    rez[s["id"]] = (t, "verifica", "; ".join(probl))
                urmatoare.append(s)
        de_refacut = urmatoare
    salveaza(c, srv, limba, rez)
    stat["seg"] += len(lot); stat["ok"] += sum(v[1] == "ok" for v in rez.values())

def de_tradus(c, limba, foi):
    with _lock:
        c.execute("""INSERT OR IGNORE INTO tr(seg,limba,text,stare,model,ts)
                     SELECT id,?,text,'copie','-',datetime('now') FROM seg WHERE mod='copie'""", (limba,))
        c.commit()
        filtru, params = "", [limba]
        if foi:
            filtru = f" AND foaie IN ({','.join('?' * len(foi))})"; params += foi
        rows = c.execute(f"""SELECT id,src,text,ref_en,ctx,refs FROM seg WHERE mod='llm'
                AND id NOT IN (SELECT seg FROM tr WHERE limba=? AND stare IN ('ok','verifica','copie')) {filtru}
                ORDER BY prio, ord""", params).fetchall()
    return [dict(id=r[0], src=r[1], text=r[2], ref_en=r[3], ctx=r[4], refs=json.loads(r[5]) if r[5] else None)
            for r in rows]

def traduce_limba(srv, limba, foi, maxim, c, glosar):
    segs = de_tradus(c, limba, foi)
    if maxim:
        segs = segs[:maxim]
    total = len(segs)
    nume = srv.get("nume", srv["model"])
    print(f"[{limba}] {nume}: de tradus {total} segmente", flush=True)
    stat = defaultdict(int); t0 = time.time()
    with cf.ThreadPoolExecutor(srv.get("paralel", 1)) as ex:
        fut = [ex.submit(proceseaza, srv, lot, limba, glosar, c, stat) for lot in loturi(segs)]
        for f in cf.as_completed(fut):
            f.result()
            dt = time.time() - t0
            rata = stat["seg"] / dt if dt else 0
            rest = (total - stat["seg"]) / rata / 3600 if rata else 0
            print(f"[{limba}] {nume}: {stat['seg']}/{total} seg | ok {stat['ok']} | {stat['tok']/dt:.1f} tok/s | "
                  f"{rata*3600:.0f} seg/h | ramas ~{rest:.1f} h", flush=True)

def traduce(a):
    """Fiecare server ia, pe rand, cate o limba intreaga din coada (terminologie consecventa pe limba)."""
    import queue
    c = db()
    limbi = [l for l, v in CFG["limbi"].items() if not v.get("existent")] if a.limbi == "toate" else a.limbi.split(",")
    for l in limbi:
        if l not in CFG["limbi"]:
            sys.exit(f"limba necunoscuta: {l}")
    foi = a.foi.split(",") if a.foi else None
    srvs = servere()
    if a.server:
        srvs = [s for s in srvs if s.get("nume") in a.server.split(",")]
    q = queue.Queue()
    for l in limbi:
        q.put(l)
    glosar = Glosar()

    def lucrator(srv):
        while True:
            try:
                limba = q.get_nowait()
            except queue.Empty:
                return
            traduce_limba(srv, limba, foi, a.max, c, glosar)

    with cf.ThreadPoolExecutor(len(srvs)) as ex:
        for f in [ex.submit(lucrator, s) for s in srvs]:
            f.result()

# ---------------------------------------------------------------- stare + export

def stare(a):
    c = db()
    tot = dict(c.execute("SELECT mod,count(*) FROM seg GROUP BY mod").fetchall())
    print(f"segmente: {tot}")
    for limba, st, n in c.execute("SELECT limba,stare,count(*) FROM tr GROUP BY 1,2 ORDER BY 1,2"):
        print(f"  {limba:16} {st:9} {n}")

def exporta(a):
    import openpyxl
    from openpyxl.styles import PatternFill
    c = db()
    os.makedirs(IESIRE, exist_ok=True)
    data = datetime.date.today().isoformat()
    for limba in a.limbi.split(","):
        tr = {(s, t): (x, st, er) for s, t, x, st, er in c.execute(
            "SELECT seg.src, seg.text, tr.text, tr.stare, tr.eroare FROM tr JOIN seg ON seg.id=tr.seg WHERE tr.limba=?", (limba,))}
        src = openpyxl.load_workbook(CFG["fisier_sursa"], read_only=True)
        out = openpyxl.Workbook(write_only=True)
        galben = PatternFill("solid", fgColor="FFF2CC")
        de_verificat = []
        n_ok = n_gol = 0
        for ws in src.worksheets:
            wo = out.create_sheet(ws.title)
            it = ws.iter_rows(values_only=True)
            h = list(next(it)); wo.append(h)
            k = coloane([str(x) for x in h]) if ws.title in CFG["ordine_foi"] else None
            for r in it:
                r = list(r)
                if k:
                    ro, en = r[k["ro"]], r[k["en"]] if k["en"] is not None else None
                    if ro:
                        key, col = ("ro", str(ro)), k["out_ro"]
                    elif en and k["out_en"] is not None:
                        key, col = ("en", str(en)), k["out_en"]
                    else:
                        key = None
                    if key:
                        x = tr.get(key)
                        if x and x[0]:
                            r[col] = x[0]; n_ok += 1
                            if x[1] == "verifica":
                                de_verificat.append((ws.title, key[1], x[0], x[2]))
                        else:
                            n_gol += 1
                wo.append(r)
        susp = cuvinte_suspecte(limba, [(k[1], v[0]) for k, v in tr.items() if v[0] and v[1] != "copie"])
        if susp:
            ws_ = out.create_sheet("Cuvinte suspecte")
            ws_.append(["Cuvânt", "Apariții", "Exemplu de traducere"])
            for w, n, ex in susp:
                ws_.append([w, n, ex])
        wv = out.create_sheet("De verificat")
        wv.append(["Foaie", "Text sursă", "Traducere propusă", "Problemă găsită automat"])
        for row in de_verificat:
            wv.append(list(row))
        f = os.path.join(IESIRE, f"EVA-traducere-{limba}-{data}.xlsx")
        out.save(f)
        print(f"{f}: {n_ok} randuri completate, {n_gol} goale, {len(de_verificat)} de verificat")

FARA_SPATII = {"han", "thai", "khmer", "myanmar"}

def lexic(limba):
    """Cuvintele limbii tinta din baza EVA_Learn_Import_35 (source_lang = limba)."""
    L = CFG["limbi"][limba]
    if L["script"] in FARA_SPATII or limba == "kk-Latn":
        return None
    rad = os.path.dirname(os.path.dirname(CFG["dictionare"]["ro"]))
    rad = os.path.dirname(rad)
    meta = json.load(open(os.path.join(rad, "limbi.json"), encoding="utf-8"))
    for m in meta:
        if set(m["codes"]) & set(L["dict"]):
            dbd = os.path.join(rad, m["folder"], "DB")
            cuv = set()
            for f in os.listdir(dbd):
                if f.endswith(".sqlite"):
                    con = sqlite3.connect(f"file:{os.path.join(dbd, f)}?mode=ro", uri=True)
                    q = ",".join("?" * len(L["dict"]))
                    cuv |= {w.lower() for (w,) in con.execute(
                        f"SELECT DISTINCT word FROM entries WHERE source_lang IN ({q})", L["dict"])}
            return cuv or None
    return None

def flexionat(w, cuv):
    """Forma flexionata/aglutinata a unui cuvant cunoscut (radacina de minim 3 litere, sufix de max. 5)."""
    return any(w[:i] in cuv for i in range(len(w) - 1, max(2, len(w) - 6), -1))

def cuvinte_suspecte(limba, traduceri):
    cuv = lexic(limba)
    if not cuv:
        return []
    sc = CFG["limbi"][limba]["script"]
    rx = re.compile(r"[^\W\d_]+") if sc == "latin" else re.compile(f"[{SCRIPT[sc]}]+")
    n, ex = Counter(), {}
    for sursa, t in traduceri:
        din_sursa = {w.lower() for w in rx.findall(sursa)}  # engleza pastrata, nume proprii
        for w in rx.findall(t):
            wl = w.lower()
            if len(wl) < 3 or wl in cuv or wl in din_sursa or flexionat(wl, cuv):
                continue
            n[wl] += 1; ex.setdefault(wl, t[:150])
    return sorted(((w, k, ex[w]) for w, k in n.items()), key=lambda x: (x[1], x[0]))  # cele rare intai

# ---------------------------------------------------------------- viteza

def viteza(a):
    text = "Traduce în germană, doar traducerea: Astăzi mergem la piață să cumpărăm legume proaspete, apoi gătim o supă mare pentru toată familia."
    for srv in servere():
        for k in [int(x) for x in a.paralel_lista.split(",")]:
            t = time.time()
            with cf.ThreadPoolExecutor(k) as ex:
                tok = sum(ex.map(lambda _: cere_model(srv, 'Answer in JSON: {"t": "..."}', text)[1], range(k)))
            dt = time.time() - t
            print(f"{srv.get('nume', srv['model'])} paralel {k}: {tok} tokeni in {dt:.1f}s = {tok/dt:.1f} tok/s total", flush=True)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("extrage")
    t = sp.add_parser("traduce"); t.add_argument("--limbi", required=True, help='coduri separate prin virgula sau "toate"')
    t.add_argument("--foi"); t.add_argument("--max", type=int); t.add_argument("--server", help="numele serverelor de folosit")
    sp.add_parser("stare")
    e = sp.add_parser("exporta"); e.add_argument("--limbi", required=True)
    v = sp.add_parser("viteza"); v.add_argument("--paralel", dest="paralel_lista", default="1,4,8")
    a = p.parse_args()
    {"extrage": extrage, "traduce": traduce, "stare": stare, "exporta": exporta, "viteza": viteza}[a.cmd](a)
