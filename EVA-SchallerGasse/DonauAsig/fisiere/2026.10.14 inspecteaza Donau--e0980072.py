from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
idx=json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))
print('INDEX RELEVANT')
for x in idx:
 if ('Memoformat' in x['cale'] or '2026.10.07 Audit juridic.txt' in x['cale']) and 'Istoric' not in x['cale']:print(x['cale'],x['sha256'],x.get('text_cache'))
B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
ats=json.loads((B/'2026.10.14 Registru atasamente.json').read_text(encoding='utf-8-sig'))
print('ATT STRUCT',type(ats).__name__)
if isinstance(ats,dict):print(ats.keys())
else:print(ats[0])
p=R/'05. Asigurari/Asigurare cladire/2026.10.14 Situatie Donau/Surse/2026.10.14 Verificare Eva-Mail.json'
data=json.loads(p.read_text(encoding='utf-8'))
ids={a['id'] for e in data['emails'] for a in e.get('attachments',[]) if not a.get('content_type','').startswith('image/')}
for id in ids:
 ar=[a for a in ats if a.get('id')==id]
 print('ATT',id,[(a.get('cale'),a.get('sha256'),a.get('stare')) for a in ar])
reg=json.loads((B/'2026.10.14 Registru comunicatii.json').read_text(encoding='utf-8-sig'))
print('REG KEYS',list(reg))
for s in reg.get('statusuri',[]):
 if s.get('partener') in ['Donau Versicherung','Maritczak - Commerz Inkasso']:print('STATUS',s)
print('MESSAGES',[(x['data'],x['id'],x['subiect']) for x in reg['comunicatii'] if x['partener']=='Donau Versicherung'])
