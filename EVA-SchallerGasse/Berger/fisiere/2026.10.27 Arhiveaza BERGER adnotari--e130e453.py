from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib
root=Path.cwd();tz=ZoneInfo('Europe/Bucharest')
p=json.loads((root/'folder map/2026.10.27 Dovezi BERGER adnotari.json').read_text(encoding='utf-8'))
out=root/'08. Corespondenta/2026.10.27 BERGER contract adnotat si Teams';out.mkdir(exist_ok=True)
saved=[]
for e in p['emails']:
 dt=datetime.fromisoformat(e['received_at'].replace('Z','+00:00')).astimezone(tz)
 stem=f"{dt.strftime('%Y.%m.%d %H-%M-%S')} PRIMIT BERGER {e['id'][:8]}"
 jp=out/(stem+'.json');tp=out/(stem+'.txt')
 jp.write_bytes(json.dumps(e,ensure_ascii=False,indent=2).encode('utf-8'))
 head=f"Data: {dt.strftime('%Y.%m.%d')}; ora Romania: {dt.strftime('%H:%M:%S')}; data tehnica originala: {e['received_at']}\nStatut: PRIMIT\nID Eva-Mail: {e['id']}\nCont: {e['account_email']}\nExpeditor: {e['from_address']}\nDestinatari: {', '.join(e['to'])}\nCC: {', '.join(e.get('cc',[]))}\nSubiect original: {e['subject']}\nSursa: Eva-Mail; text API integral, nu MIME original\n\nTEXT ORIGINAL NEMODIFICAT\n\n"
 tp.write_bytes((head+e['text']).encode('utf-8'))
 assert tp.read_bytes().decode('utf-8').endswith(e['text'])
 row={'id':e['id'],'json':str(jp.relative_to(root)).replace('\\','/'),'txt':str(tp.relative_to(root)).replace('\\','/')}
 if 'BEGIN:VCALENDAR' in e['text']:
  ics=e['text'][e['text'].index('BEGIN:VCALENDAR'):]
  ip=out/'2026.10.27 Invitatie originala BERGER 2026.10.29 Teams.ics';ip.write_bytes(ics.encode('utf-8'));row['ics']=str(ip.relative_to(root)).replace('\\','/')
 saved.append(row)
original=root/p['original_path'];assert original.stat().st_size==p['download']['size']==6248347
manifest={'data':'2026.10.27','mesaje':saved,'atasament':p['attachment'],'original_pdf':p['original_path'],'sha256_original':hashlib.sha256(original.read_bytes()).hexdigest(),'calendar_din_ICS':{'data':'2026.10.29','ora_Viena':'13:00–13:30','ora_Romania':'14:00–14:30','timezone_original':'W. Europe Standard Time','status_ICS':'CONFIRMED','PARTSTAT':'NEEDS-ACTION','locatie':'Teams','mentiune':'Invitatia nu reprezinta acceptare RSVP. Calendarul EVA contine o interpretare automata eronata la 2026.10.27; nu a fost modificata in aceasta arhivare.'}}
(out/'2026.10.27 Registru surse BERGER.json').write_bytes(json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(manifest,ensure_ascii=False))
