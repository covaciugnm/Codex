from pathlib import Path
import json,re
M=Path(__file__).parent
p=M/'2026.09.30 lista mesaje candidate.json';old=json.loads(p.read_text(encoding='utf-8'));d={e['id']:e for e in old};initial=set(d)
excluded=[];restricted=[]
for e in json.loads((M/'2026.09.30 Candidati suplimentari proiect.json').read_text(encoding='utf-8')):
 if e.get('note'):
  restricted.append(e);continue
 if re.search('SOLBIKA|D300|balotat|900 kWp|Arabesque|unsubscribe|Scan 28112025|transport aerian',e.get('subject',''),re.I):excluded.append(e);continue
 x=dict(e,id=e['email_id'],from_address=e['sender'],from_name=e.get('sender_name',''));d.setdefault(x['id'],x)
for e in json.loads((M/'2026.09.30 Cautari financiare.json').read_text(encoding='utf-8')):
 if (e.get('received_at') or '')<'2025-11-01' or re.search('Tableware|Steuerinfo|Webinar|Newsletter',e.get('subject',''),re.I):excluded.append(e);continue
 d.setdefault(e['id'],e)
extra=[e for k,e in d.items() if k not in initial]
extra.sort(key=lambda e:(not bool(re.search('1925|Factura Notar|Honorarnote|Finanzamt|Rechnung|Zahlung',e.get('subject',''),re.I)),e.get('received_at','')),reverse=False)
p.write_text(json.dumps(list(d.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(M/'2026.09.30 Candidati noi de preluat.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2),encoding='utf-8')
(M/'2026.09.30 Limite si excluderi proiecte.json').write_text(json.dumps({'acces_limitat':restricted,'excluse_alte_subiecte':excluded},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total':len(d),'initial':len(old),'noi':len(extra),'ids':[e['id'] for e in extra]}))
