#!/usr/bin/env python3
"""OCR pe anunțurile oficiale ANABI (PDF scanate) descărcate de prepare.mjs în sources/document-<id>-<n>.pdf.
Scrie sources/anunt-<id>.json cu câmpurile relevante (termen înscriere, vizionare, data licitației, garanție, dosar, pas,
cont trezorerie, plată). Se reface doar dacă PDF-ul e mai nou decât JSON-ul. Rulare: python3 anunt-ocr.py [id ...]
Dependențe: rapidocr-onnxruntime, pymupdf (venv în generator/.venv-ocr pe server)."""
import glob, json, os, re, sys, time, unicodedata

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources')

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', '', s).lower()

def ocr_pdf(path, pages=5):
    import fitz
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    doc = fitz.open(path)
    out = []
    for i, p in enumerate(doc):
        if i >= pages: break
        res, _ = ocr(p.get_pixmap(dpi=200).tobytes('png'))
        out.append('\n'.join(r[1] for r in (res or [])))
    return '\n'.join(out)

def grab(t, pat, flags=0):
    m = re.search(pat, t, flags)
    return m.groups() if m else None

ORD = {'prima': 1, 'adoua': 2, 'atreia': 3, 'apatra': 4, 'acincea': 5, 'asasea': 6, 'asaptea': 7}
D = r'(\d{2}[./]\d{2}[./]\d{4})'
H = r'(\d{1,2}[:.]\d{2})'

def iso(d):  # 08.10.2026 / 08/10/2026 -> 2026-10-08
    return '-'.join(reversed(re.split(r'[./]', d))) if d else None

def hhmm(h):
    return h.replace('.', ':').zfill(5) if h else None

def extract(text):
    t = norm(text)
    r = {}
    g = grab(t, r'datalimita(?:pentru)?inscriere(?:a)?lalicitatie:?' + D + r'(?:ora:?)?' + H + '?')
    if g: r['inscriereLicitatie'] = {'data': iso(g[0]), 'ora': hhmm(g[1])}
    g = grab(t, r'datalimita(?:pentru)?inscriere(?:a)?lavizionare:?' + D + r'(?:ora:?)?' + H + '?')
    if g: r['vizionare'] = {'data': iso(g[0]), 'ora': hhmm(g[1])}
    g = grab(text, r'Locul\s*vizion[aă]rii\s*:?\s*\n?\s*([^\n]{3,80})', re.I)
    if g: r.setdefault('vizionare', {})['loc'] = g[0].strip()
    g = grab(t, r'data(?:desfasurare|organizarii?|organizare)licitatiei?:?' + D + r'(?:ora:?|(?:in)?intervalulorar|intervalorar)?' + H + r'?-?' + H + '?') \
        or grab(t, r'ladatade' + D + r'(?:in)?intervalulorar' + H + r'-' + H)
    if g: r['desfasurare'] = {'data': iso(g[0]), 'de': hhmm(g[1]), 'la': hhmm(g[2])}
    g = grab(t, r'garantie(?:departicipare)?:?([\d.,]+)(?:ron|lei)')
    if g: r['garantie'] = g[0]
    g = grab(t, r'pret:?([\d.,]+)(?:lei|ron)[(/]?([\d.,]+)(?:eur|euro)') or grab(t, r'pret:?([\d.,]+)(?:lei|ron)()')
    if g: r['pret'] = {'lei': g[0], 'eur': g[1] or None}
    g = grab(t, r'nr\.?dosarvalorificare([\d/]+)')
    if g: r['dosar'] = g[0]
    g = grab(t, r'(prima|adoua|atreia|apatra|acincea|asasea|asaptea)licitatiepublica')
    if g: r['licitatiaNr'] = ORD[g[0]]
    g = grab(t, r'pasuldelicitareestede(\d+%)')
    if g: r['pas'] = g[0]
    g = grab(t, r'timpulsuplimentarestede([a-z]+|\d+)minute')
    if g: r['timpSuplimentarMin'] = {'unu': 1, 'doua': 2, 'trei': 3, 'patru': 4, 'cinci': 5, 'zece': 10}.get(g[0], g[0])
    g = grab(t, r'contul(r[o0]\d{2}trez[0-9a-z]{16,24})')
    if g: r['cont'] = 'RO' + g[0][2:].upper()
    g = grab(t, r'seachitaintermendecelmult(\d+)zilelucratoare')
    if g: r['plataZileLucratoare'] = int(g[0])
    g = grab(t, r'cotatva\*?(\d{1,2}%)') or grab(t, r'(\d{1,2}%)\(seaplicala')
    if g: r['tva'] = g[0]
    g = grab(t, r'(?:exclusivprinmijloaceelectronice|licitatie)pentruurmatorulbun:?(.{0,400}?)pretde')
    r['esteAnunt'] = bool(re.search(r'anuntprivindvanzarea', t)) and 'inscriereLicitatie' in r
    return r

def reparse():
    """Reaplică extragerea pe textul OCR deja salvat (după îmbunătățirea expresiilor), fără OCR nou."""
    for f in sorted(glob.glob(os.path.join(SRC, 'anunt-*.json'))):
        j = json.load(open(f, encoding='utf-8'))
        r = extract(j.get('text', ''))
        keep = {k: j[k] for k in ('id', 'pdf', 'pdfMtime', 'ocrAt', 'text') if k in j}
        r.update(keep)
        json.dump(r, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('REPARSE', r.get('id'), 'anunt' if r['esteAnunt'] else 'alt document', r.get('inscriereLicitatie'), r.get('desfasurare'), r.get('garantie'), r.get('licitatiaNr'))

def main(ids):
    if '--reparse' in ids:
        return reparse()
    done = 0
    for pdf in sorted(glob.glob(os.path.join(SRC, 'document-*-*.pdf'))):
        m = re.match(r'document-(\d+)-(\d+)\.pdf', os.path.basename(pdf))
        if not m: continue
        lot, n = m.group(1), m.group(2)
        if ids and lot not in ids: continue
        out = os.path.join(SRC, f'anunt-{lot}.json')
        if os.path.exists(out):
            j = json.load(open(out, encoding='utf-8'))
            if j.get('pdf') == os.path.basename(pdf) and j.get('pdfMtime') == int(os.path.getmtime(pdf)): continue
            if j.get('esteAnunt') and j.get('pdf') != os.path.basename(pdf): continue  # avem deja anunțul din alt PDF
        try:
            text = ocr_pdf(pdf)
        except Exception as e:
            print('EROARE OCR', pdf, e); continue
        r = extract(text)
        if not r.get('esteAnunt') and os.path.exists(out) and json.load(open(out, encoding='utf-8')).get('esteAnunt'):
            continue  # nu suprascrie un anunț valid cu un PDF care nu e anunț
        r.update({'id': int(lot), 'pdf': os.path.basename(pdf), 'pdfMtime': int(os.path.getmtime(pdf)),
                  'ocrAt': time.strftime('%Y-%m-%dT%H:%M:%S'), 'text': text[:20000]})
        json.dump(r, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        done += 1
        print('OK', lot, os.path.basename(pdf), 'anunt' if r['esteAnunt'] else 'alt document',
              r.get('inscriereLicitatie'), r.get('desfasurare'))
    print('ANUNTURI OCR noi:', done)

if __name__ == '__main__':
    main(set(sys.argv[1:]))
