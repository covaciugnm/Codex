from pathlib import Path
import json,hashlib,datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
O=R/'executie/R12_fisiere/A08_Catalog_paginare_lot05'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
src=O/'Raport_A08_paginare_lot05_lectura_v3.html'
verdict=R/'executie/R12_fisiere/A11/Val05_loturi/Verdict_A11_paginare_lot05_v1.json'
assert sha(src)=='9ade0cb1658144c819ff1915af602563fbcc6d8fb8feb71b6d4e6503a92dbdc3'
assert sha(verdict)=='08a65ade90287c0b2db1bb3e0d2b39130ef7e42705b16e4de7e8d74884e4c70d'
s=src.read_text(encoding='utf-8')
assert 'Recepția independentă A11 este în așteptare.' in s
s=s.replace('Recepția independentă A11 este în așteptare.','A11 a recepționat dovezile limitate de componentă și a confirmat constatarea R12-CATALOG-JSON-PAGINATION-01. Auditul integral rămâne deschis.')
s=s.replace('</style>','table{min-width:720px}th{white-space:nowrap;overflow-wrap:normal}.table{max-width:100%}</style>',1)
s=s.replace('<div class="table">','<p>Pe ecrane înguste, tabelul poate fi derulat orizontal.</p><div class="table" role="region" tabindex="0" aria-label="Cele 16 cazuri de paginare; tabel derulabil orizontal">',1)
s=s.replace('<h2>Calibrări păstrate</h2>','<h2>Verificarea independentă</h2><p>A11 a verificat 183 de artefacte, arhiva și identitățile surselor, a recalculat ieșirile celor 16 cazuri și a reprodus separat mecanismul prin șase apeluri proprii: doi martori conformi și patru contraexemple. Aceste apeluri nu sunt adunate la cazurile executorului ca scenarii distincte. Confirmarea este P2 la nivel de componentă și nu dovedește un răspuns HTTP, un efect DB sau funcționarea întregului site.</p><p><a href="../A11/Val05_loturi/Verdict_A11_paginare_lot05_v1.json">Verdictul A11 și limitele per fișier</a> · <a href="../A11/Val05_loturi/Contraoracol_A11_paginare_v1.json">Reproducerea independentă</a></p><h2>Calibrări păstrate</h2>',1)
s=s.replace('Cele 16 cazuri și oracolele independente','Cele 16 cazuri și rezultatele așteptate')
out=O/'Raport_A08_paginare_lot05_lectura_v4.html';assert not out.exists();out.write_text(s,encoding='utf-8')
manifest={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'Vedere explicativă aditivă; zero execuții de produs','source_reading':ref(src),'independent_receipt':ref(verdict),'files':[ref(out)],'changes':['Statutul actual al recepției A11 și limitele explicite','Tabel derulabil și lizibil pe ecran îngust','Separarea celor șase apeluri A11 de cele 16 cazuri executor'],'signed_sources_unchanged':True,'product_acceptance':False}
m=O/'MANIFEST_lectura_paginare_v4.json';assert not m.exists();m.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'reading':ref(out),'manifest':ref(m)},ensure_ascii=False))
