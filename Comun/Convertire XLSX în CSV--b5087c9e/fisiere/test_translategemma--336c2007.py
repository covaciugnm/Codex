# -*- coding: utf-8 -*-
"""Test comparativ TranslateGemma 12B (din engleza verificata) vs Qwen 35B (pipeline complet) pe acelasi esantion.
TranslateGemma ruleaza cu llama-server (~/llamacpp, in afara Docker) pe 192.168.100.160:127.0.0.1:8090, prin tunel SSH:
  ssh -N -L 11441:127.0.0.1:8090 user@192.168.100.160
Rezultat: iesire/test_translategemma_<data>.xlsx
"""
import datetime, json, os, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.argv = sys.argv[:1] + sys.argv[1:]
import traducator as T

TG_URL = "http://127.0.0.1:11441/completion"
TG_LIMBI = {  # cod -> (nume pentru prompt, cod)
    "tzm": ("Central Atlas Tamazight written in Tifinagh script (IRCAM standard)", "tzm-Tfng"),
    "ary": ("Moroccan Arabic (Darija), Arabic script", "ar-MA"),
    "bn": ("Bengali", "bn"),
    "ha": ("Hausa", "ha"),
    "yue": ("Cantonese (Hong Kong, Traditional Chinese characters)", "yue"),
}

def tg(text, limba):
    nume, cod = TG_LIMBI[limba]
    prompt = (f"<start_of_turn>user\nYou are a professional English (en) to {nume} ({cod}) translator. Your goal is to "
              f"accurately convey the meaning and nuances of the original English text while adhering to {nume} grammar, "
              f"vocabulary, and cultural sensitivities.\nProduce only the {nume} translation, without any additional "
              f"explanations or commentary. Please translate the following English text into {nume}:\n\n\n{text}"
              f"<end_of_turn>\n<start_of_turn>model\n")
    body = {"prompt": prompt, "n_predict": 600, "temperature": 0.1, "cache_prompt": True}
    r = json.load(urllib.request.urlopen(urllib.request.Request(TG_URL, json.dumps(body).encode(),
                                                                {"Content-Type": "application/json"}), timeout=900))
    tm = r.get("timings", {})
    return r["content"].strip(), r.get("tokens_predicted", 0), tm.get("predicted_ms", 1) / 1000

def esantion(n=25):
    c = T.db()
    rows = c.execute("""SELECT id,src,text,ref_en,ctx,refs FROM seg WHERE mod='llm' AND src='ro' AND refs IS NOT NULL
        AND foaie IN ('Texte fixe','Lecții A1','Lecții A2') AND length(text) BETWEEN 15 AND 220
        ORDER BY (id*2654435761) % 1000003 LIMIT ?""", (n,)).fetchall()
    return [dict(id=r[0], src=r[1], text=r[2], ref_en=r[3], ctx=r[4], refs=json.loads(r[5])) for r in rows]

if __name__ == "__main__":
    import openpyxl
    limbi = (sys.argv[1] if len(sys.argv) > 1 else "tzm,ary,bn").split(",")
    segs = esantion()
    qwen = [s for s in T.servere() if s["nume"] == "qwen35b"][0]
    gl = T.Glosar()
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    for limba in limbi:
        ws = wb.create_sheet(limba)
        ws.append(["Context", "Text RO", "Text EN (verificat)", "TranslateGemma 12B (din EN)", "Qwen 35B (RO + ref + glosar)",
                   "Verificare automată TG", "Verificare automată Qwen"])
        t0 = time.time(); out_q = {}
        try:
            o, _ = T.traduce_lot(qwen, segs, limba, gl); out_q.update(o)
        except Exception as e:  # JSON stricat -> ca in programul principal: loturi mici
            print(f"{limba}: Qwen lot intreg esuat ({type(e).__name__}), reiau cate 5", flush=True)
            for i in range(0, len(segs), 5):
                try:
                    o, _ = T.traduce_lot(qwen, segs[i:i + 5], limba, gl); out_q.update(o)
                except Exception as e2:
                    print(f"{limba}: Qwen lot {i} esuat: {type(e2).__name__}", flush=True)
        tq = time.time() - t0
        import concurrent.futures as cf
        t0 = time.time()
        with cf.ThreadPoolExecutor(4) as ex:
            rez_tg = list(ex.map(lambda s: tg(s["refs"]["en"], limba), segs))
        dt_tg = time.time() - t0; tok = sum(r[1] for r in rez_tg); dur = dt_tg
        for s, (t, k, d) in zip(segs, rez_tg):
            en = s["refs"]["en"]
            q = out_q.get(s["id"])
            ws.append([s["ctx"], s["text"], en, t, q, "; ".join(T.verifica(en, t, limba, s["ctx"])),
                       "; ".join(T.verifica(s["text"], q, limba, s["ctx"])) if q else "lipsă"])
        print(f"{limba}: TranslateGemma {tok/dt_tg:.1f} tok/s total cu 4 cereri paralele ({dt_tg:.0f}s / {len(segs)} seg), "
              f"Qwen 35B {tq:.0f}s / {len(segs)} seg", flush=True)
    os.makedirs(T.IESIRE, exist_ok=True)
    f = os.path.join(T.IESIRE, f"test_translategemma_{datetime.date.today()}.xlsx")
    wb.save(f); print(f)
