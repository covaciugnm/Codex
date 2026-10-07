from pathlib import Path
import json, hashlib
import genereaza_documente as g
W=Path(__file__).resolve().parent
t=(W/'AUDIT.md').read_text(encoding='utf-8')
g.word(g.parse(t),W.parent/'05 Audit intern - contract BAU-WERTE.docx','Audit intern - propunere BAU-WERTE')
(W.parent/'05 Audit intern - contract BAU-WERTE.txt').write_text(t,encoding='utf-8-sig')
p=W/'SURSE_JURIDICE.md'
t=p.read_text(encoding='utf-8').replace('o prelungire BAU-WERTE a ofertei după 10.09.2026 a condițiilor financiare.','o prelungire BAU-WERTE a valabilității ofertei după 10.09.2026.')
p.write_text(t,encoding='utf-8')
p=W/'manifest_erzeugung.json';m=json.loads(p.read_text(encoding='utf-8'))
m['artefakte']=[{'datei':x.name,'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(W.parent.iterdir()) if x.is_file()]
p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Audit final si manifest salvate. Contractul auditat nu a fost modificat.')
