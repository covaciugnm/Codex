from pathlib import Path
import json,re,sys,collections
R=Path(__file__).resolve().parent.parent
ns={'__file__':str(Path(__file__).parent/'2026.09.30 actualizeaza jurnale.py')}
exec((Path(__file__).parent/'2026.09.30 actualizeaza jurnale.py').read_text(encoding='utf-8').split('\ndata={}')[0],ns)
data={}
for p in (R/'08. Corespondenta'/'2026.09.30 Arhiva Eva-Mail'/'Surse').glob('*.json'):
 for e in json.loads(p.read_text(encoding='utf-8')):data[e['id']]=e
groups=collections.defaultdict(list)
for e in sorted(data.values(),key=lambda e:e.get('received_at',''),reverse=True):groups[ns['classify'](e)[0]].append(e)
terms=sys.argv[1:]
for partner,emails in sorted(groups.items()):
 if terms and not any(t.lower() in partner.lower() for t in terms):continue
 incoming=[e for e in emails if not e.get('is_sent') and not e.get('text','').lstrip().startswith('BEGIN:VCALENDAR')]
 print('\nPARTNER',partner,'total',len(emails),'incoming',len(incoming))
 for e in incoming[:2 if terms else 1]:
  body=e.get('text','').replace('\r','')
  body=re.split(r'\n(?:Von:|From:|---------- Ca răspuns la|Am .+schrieb)',body,maxsplit=1)[0]
  print(e['received_at'],e['id'],e['subject'],'\n',body[:6000 if terms else 1400])
