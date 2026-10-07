from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parent.parent;B=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
es={e['id']:e for p in (B/'Surse').glob('*.json') for e in json.loads(p.read_text(encoding='utf-8'))}
q=sys.argv[1] if len(sys.argv)>1 else 'capra|artus'
mode=sys.argv[2] if len(sys.argv)>2 else 'list'
for e in sorted(es.values(),key=lambda e:e.get('received_at')or''):
 hay=e.get('from_address','')+' '+e.get('subject','')+' '+e.get('text','')
 if len(sys.argv)>3:
  if not re.search(sys.argv[3],e.get('from_address',''),re.I):continue
 if len(sys.argv)>4:
  if not e.get('received_at','').startswith(sys.argv[4]):continue
 if re.search(q,hay,re.I):
  print('\nEMAIL',e['id'],e.get('received_at'),e.get('from_address'),e.get('subject'))
  print('ATTACHMENTS',json.dumps([{k:a.get(k) for k in ['id','name','text_chars']} for a in e.get('attachments',[]) if not re.match(r'^(image\d+|inline|smime)',a['name'])],ensure_ascii=False))
  if mode!='list':
   t=e.get('text','').replace('\r','');t=re.split(r'\n(?:Von:|From:|De la:|Am .+schrieb|On .+wrote|Mag. Bogdan Capra)',t)[0];print(t[:int(mode)])
   for a in e.get('attachments',[]):
    if q!='.' and not re.match(r'^(image\d+|inline|smime)',a['name']) and re.search(q,a.get('name','')+' '+(a.get('text')or''),re.I):print('ATTACHMENT TEXT',a['name'],(a.get('text')or'')[:int(mode)])
