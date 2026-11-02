import json,sqlite3,collections
from pathlib import Path
R=Path.cwd();q=R/'folder map/2026.10.27 QA autorizare';d=json.loads((q/'2026.10.27 Comparatie servieta.json').read_text(encoding='utf-8'))
c=sqlite3.connect(R/'folder map/cautare.sqlite')
for term in ['Rechtskraft','Sichtvermerk','Löschwasser','Brandschutzkonzept']:
 print('\nTERM',term)
 for r in c.execute('SELECT cale FROM documente WHERE documente MATCH ? LIMIT 20',(term,)):print(r[0])
web={x['sha256'] for x in d['files']}
core=[x for x in d['local'] if x['cale'].startswith('00.Proiect/') and '/09. Vertraege/' not in x['cale'] and not x['cale'].endswith('.md')]
print('CORE',len(core),len({x['sha256'] for x in core}),len({x['sha256'] for x in core}-web))
missing=[x for x in core if x['sha256'] not in web];(q/'2026.10.27 Lipsuri nucleu.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2),encoding='utf-8')
for x in missing:print(x['cale'])
