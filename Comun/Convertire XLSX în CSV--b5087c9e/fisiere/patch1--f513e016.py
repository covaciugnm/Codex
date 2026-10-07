import json, os
os.chdir(r"Z:\00.Roboti\EVA.Pro\Learn\Traducator")
src = open('traducator.py', encoding='utf-8').read()
a = src.index("# ---------------------------------------------------------------- apel model")
b = src.index("# ---------------------------------------------------------------- stare + export")
new = r'''# ---------------------------------------------------------------- apel model

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
        if s.get("ref_en"): x["en"] = s["ref_en"]
        g = glosar.pentru(s, L["dict"])
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
                probl = verifica(s["text"], t, limba) if t is not None else ["lipsa din raspuns"]
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
        rows = c.execute(f"""SELECT id,src,text,ref_en,ctx FROM seg WHERE mod='llm'
                AND id NOT IN (SELECT seg FROM tr WHERE limba=? AND stare IN ('ok','verifica','copie')) {filtru}
                ORDER BY prio, ord""", params).fetchall()
    return [dict(id=r[0], src=r[1], text=r[2], ref_en=r[3], ctx=r[4]) for r in rows]

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
    limbi = list(CFG["limbi"]) if a.limbi == "toate" else a.limbi.split(",")
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

'''
src = src[:a] + new + src[b:]
old_args = '''t = sp.add_parser("traduce"); t.add_argument("--limbi", required=True); t.add_argument("--foi"); t.add_argument("--max", type=int)
    t.add_argument("--paralel", type=int)'''
assert old_args in src
src = src.replace(old_args, '''t = sp.add_parser("traduce"); t.add_argument("--limbi", required=True, help='coduri separate prin virgula sau "toate"')
    t.add_argument("--foi"); t.add_argument("--max", type=int); t.add_argument("--server", help="numele serverelor de folosit")''')
vs = src.index("def viteza(a):"); ve = src.index('if __name__ == "__main__":')
src = src[:vs] + '''def viteza(a):
    text = "Traduce în germană, doar traducerea: Astăzi mergem la piață să cumpărăm legume proaspete, apoi gătim o supă mare pentru toată familia."
    for srv in servere():
        for k in [int(x) for x in a.paralel_lista.split(",")]:
            t = time.time()
            with cf.ThreadPoolExecutor(k) as ex:
                tok = sum(ex.map(lambda _: cere_model(srv, 'Answer in JSON: {"t": "..."}', text)[1], range(k)))
            dt = time.time() - t
            print(f"{srv.get('nume', srv['model'])} paralel {k}: {tok} tokeni in {dt:.1f}s = {tok/dt:.1f} tok/s total", flush=True)

''' + src[ve:]
src = src.replace('if __name__ == "__main__":\n', 'if __name__ == "__main__":\n    sys.stdout.reconfigure(encoding="utf-8", errors="replace")\n', 1)
src = src.replace('python traducator.py traduce --limbi de,bn --foi "Texte fixe,Lecții A1" [--max 200] [--paralel 4]',
                  'python traducator.py traduce --limbi de,bn --foi "Texte fixe,Lecții A1" [--max 200] [--server qwen27b]')
open('traducator.py', 'w', encoding='utf-8').write(src)

p = 'config.json'; c = json.load(open(p, encoding='utf-8'))
c.pop('server', None)
c['server_implicit'] = {"backend": "ollama", "temperature": 0.2, "timeout_s": 3600, "paralel": 1}
c['servere'] = [
    {"nume": "qwen27b", "url": "http://192.168.100.160:11436", "model": "qwen3.8:27b-q4_K_M"},
    {"nume": "qwen35b", "url": "http://192.168.100.160:11438", "model": "batiai/qwen3.6-35b:q6"}]
c = {k: c[k] for k in ['server_implicit', 'servere'] + [k for k in c if k not in ('server_implicit', 'servere')]}
json.dump(c, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
import ast; ast.parse(src); print("ok")
