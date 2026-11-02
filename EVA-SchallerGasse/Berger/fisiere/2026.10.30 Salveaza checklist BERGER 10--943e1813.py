from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil,re
root=Path.cwd(); now=datetime.now(ZoneInfo('Europe/Bucharest')); day=now.strftime('%Y.%m.%d');tag=now.strftime('%H-%M-%S');stamp=now.isoformat(timespec='seconds')
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
p=read('folder map/2026.10.30 Dovezi checklist BERGER 10.json');r=read(p['baseline_register']);idx=read('folder map/inventar.json')
out=Path('08. Corespondenta')/(day+' Checklist BERGER');proof=out/(day+' '+tag+' Dovezi checklist BERGER.json');report=out/(day+' '+tag+' Checklist BERGER.txt')
hist=Path('folder map')/(day+' Istoric checklist BERGER '+tag)
def save(path,text):
 path=Path(path)
 if path.exists():
  backup=hist/path;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,backup)
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
def jsave(path,obj):save(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def prepend(path,text):
 path=Path(path);old=path.read_text(encoding='utf-8-sig') if path.exists() else ''
 save(path,text+'\n\nISTORIC PASTRAT\n\n'+old)
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def loc(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Bucharest')).strftime('%Y.%m.%d %H:%M:%S')
known={x['id'] for x in r['comunicatii']};aliases={x['alias_id']:x['canonical_id'] for x in r.get('aliasuri_email_EVA',[])}
canonical_scoped={aliases.get(x,x) for x in p['scoped_email_ids']}
assert not p['errors'] and canonical_scoped<=known
for x in p['searches']:assert x['args']['offset']+len(x['result']['items'])>=x['result']['total']
found={x['id'] for s in p['searches'] for x in s['result']['items']}
assert found==set(p['scoped_email_ids'])|set(p['excluded_unrelated_email_ids'])
assert p['draft_readback']['status']=='sent'
files=[]
for f in idx:
 if '2026.10.29 Werkvertrag R11/' in f['cale'] and f['cale'].endswith('.pdf'):
  sha=hashlib.sha256(Path(f['cale']).read_bytes()).hexdigest()
  files.append({'cale':f['cale'],'index_sha256':f['sha256'],'actual_sha256':sha,'unchanged':sha==f['sha256']})
assert len(files)==2 and all(x['unchanged'] for x in files)
newer=[x['cale'] for x in idx if 'bmberger.at/' in x['cale'] and re.search(r'(Werkvertrag|contract).*R(1[2-9]|[2-9]\d)',Path(x['cale']).name,re.I)]
assert not newer, newer
source={x['id']:x for x in r['comunicatii'] if x['id'] in canonical_scoped};sent=source['96e74e69-7ff6-402c-9959-597c0b472950']
assert sent['sens']=='TRIMIS' and len(sent['atasamente'])==3
ics=Path('08. Corespondenta/2026.10.29 Verificare Berger Pech/2026.10.29 15-03-39 PRIMIT BERGER d5bc6ece.ics')
icst=ics.read_text(encoding='utf-8-sig');assert 'SEQUENCE:2' in icst and 'PARTSTAT=NEEDS-ACTION' in icst
ev=[x for x in p['calendar_readback']['items'] if x.get('title')=='Baubesprechung']
assert len(ev)==1 and ev[0]['id']=='6665664f-bce5-4b47-ae5f-121900bc959c' and ev[0]['start']=='2026-10-29T11:00:00Z'
status=next(x for x in r['statusuri'] if x.get('partener')=='Markus Berger')
before={k:digest(r[k]) for k in ('comunicatii','drafturi','aliasuri_email_EVA')};general=digest(r['acoperire']['verificare_incrementala'])
nq=len({json.dumps({k:v for k,v in s['args'].items() if k!='offset'},sort_keys=True) for s in p['searches']})
coverage=f"{nq} cautari, {len(p['searches'])} pagini complete, {len(found)} ID-uri metadate unice; {len(p['scoped_email_ids'])} ID-uri BERGER = {len(canonical_scoped)} comunicatii canonice deja arhivate si {len(p['scoped_email_ids'])-len(canonical_scoped)} aliasuri cunoscute; 0 mesaje noi."
checks=[
{'punct':1,'criteriu':'Mesaje primite/trimise, cautari globale, nelivrari','rezultat':'FARA NOUTATI','detalii':coverage+' Control integral office/Gmail primit si trimis; control conexiune office secundara. Nicio notificare de nelivrare BERGER identificata.','surse':[x['cale'] for x in source.values()]},
{'punct':2,'criteriu':'Versiune curenta, raspunsuri si contrapropuneri','rezultat':'FARA NOUTATI','detalii':'R11 ramane versiunea curenta documentata. Nicio contrapropunere ori confirmare comerciala noua. Cele doua PDF-uri locale au hash identic indexului; nu s-a identificat o versiune contractuala ulterioara in index.','surse':files},
{'punct':3,'criteriu':'Preturi, servicii si suplimente','rezultat':'FARA NOUTATI','detalii':'Propunere trimisa: 45.000 EUR net baza + 2.500 EUR net Bauwerksbuch = 47.500 EUR net/57.000 EUR brut; 8 vizite incluse, suplimente numai comandate 1.000 EUR net/4 vizite. Bauwerksbuch complet si PI/ZT/includerea in pret asteapta confirmare, fara acceptare comerciala identificata.','surse':sent['atasamente']},
{'punct':4,'criteriu':'Atasamente, ID si continut/hash','rezultat':'FARA NOUTATI','detalii':'Nicio comunicatie sau anexa BERGER noua de descarcat. Se reutilizeaza originalele celor trei PDF-uri Sent descarcate/hash-verificate 2026.10.29. Aliasul Sent are acelasi continut documentar cunoscut, nu constituie o noua oferta.','surse':sent['atasamente']},
{'punct':5,'criteriu':'Draft, Sent, primire si acceptare','rezultat':'FARA MODIFICARE','detalii':'Get_draft reconfirma sent, doua anexe in readback. Mesajul Sent canonic confirma expedierea 2026.10.29 13:06:48 Romania cu trei PDF-uri reale, inclusiv scanul adnotat. Nici confirmarea primirii, nici acceptarea nu sunt deduse din trimitere.','surse':[sent['cale'],sent['json']]},
{'punct':6,'criteriu':'ICS UID/SEQUENCE, calendar si RSVP','rezultat':'PENDING CUNOSCUT, FARA NOUTATI','detalii':'ICS reutilizat SEQUENCE 2: 2026.11.02 14:00–14:30 Viena/15:00–15:30 Romania; acelasi UID, inlocuieste secventele 0 si 1. Participant NEEDS-ACTION. Calendarul EVA ramane la evenimentul vechi 2026.10.29. Neconcordanta si RSVP au fost deja raportate; nicio noua notificare sau modificare de calendar. Invitatia nu confirma o sedinta efectuata.','surse':[ics.as_posix(),'calendar_readback in dovezi']},
{'punct':7,'criteriu':'Termene, calendar valoric si urmatorul pas','rezultat':'FARA ACTIUNE NOUA','detalii':status['urmatorul_pas'],'surse':status.get('sursa_status',[])}
]
sync={x['email']:x.get('last_sync') for x in p['mailboxes']['mailboxes']}
sync2=next(x['last_sync'] for x in p['secondary_mailboxes']['mailboxes'] if x['email']=='office@ac-wohnart.at')
limits=f"Indicatori ultima sincronizare: Primary office {loc(sync['office@ac-wohnart.at'])}; Gmail {loc(sync['covaciu.gnm@gmail.com'])}; conexiunea secundara office {loc(sync2)} Romania. Mesajele ulterioare neindexate pot lipsi; shared/team necautabile excluse. Indicatorii nu demonstreaza exhaustivitatea."
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger'],'mesaje_noi':0,'atasamente_noi_ID':0,'continuturi_documentare_noi':0,'query_count':nq,'page_count':len(p['searches']),'metadate_unice':len(found),'mesaje_BERGER_canonice':len(canonical_scoped),'aliasuri_BERGER_cunoscute':len(p['scoped_email_ids'])-len(canonical_scoped),'perioada':p['period'],'paginare_completa':True,'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'sincronizare_office_secundara':sync2,'decizie_notificare':'DONT_NOTIFY','sursa':proof.as_posix(),'checklist':report.as_posix()}
summary=f"{day} {now.strftime('%H:%M:%S')} | CHECKLIST BERGER\nStatus scurt: FARA NOUTATI fata de verificarea generala 2026.10.30 08:15:47 si checklistul BERGER 2026.10.29 17:02:42. Nicio actiune noua; punctele cunoscute nu se renotifica.\nUltimul raspuns: {status['ultimul_raspuns']}\nUrmatorul pas: {status['urmatorul_pas']}\n\n"
for c in checks:summary+=f"{c['punct']}. {c['criteriu']} — {c['rezultat']}\n{c['detalii']}\nSurse: {c['surse']}\n\n"
summary+=coverage+'\n'+limits+'\nSursa: '+proof.as_posix()+'\nNu s-au trimis emailuri/RSVP, modificat contracte sau calendar, semnat ori efectuat plati. PECH nu face obiectul acestui control.\n'
p['baseline']={'register_count':len(r['comunicatii']),'relevant_current_files':files,'canonical_scoped_email_ids':sorted(canonical_scoped),'aliasuri_BERGER':[x for x in r['aliasuri_email_EVA'] if x['alias_id'] in p['scoped_email_ids']]}
status['checklist_BERGER_ultim']={'checked_at_iso':stamp,'rezultat':'FARA NOUTATI','sursa':proof.as_posix(),'checklist':report.as_posix()}
r['acoperire']['verificare_punctuala_BERGER']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert all(digest(r[k])==v for k,v in before.items()) and digest(r['acoperire']['verificare_incrementala'])==general
jsave(p['baseline_register'],r);save(report,summary)
for name in ('Status proiect','Log progres proiect'):prepend(day+' '+name+'.txt',summary)
prepend(Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri')/(day+' Log discutii - Markus Berger.txt'),summary)
prepend('folder map/README.md',summary+'\nChecklist: ../'+report.as_posix())
jsave(proof,{'verificare':entry,'checklist':checks,'dovezi_originale':p,'general_baseline_preserved':True,'comunicatii_drafturi_aliasuri_nemodificate':True,'excluderi':{'ID':p['excluded_unrelated_email_ids'],'motiv':'Mesaje ale altor parteneri de proiect deja controlate de verificarea generala ori mesaje personale/comerciale/tehnice Gmail fara referinta BERGER; nicio nelivrare catre BERGER.'}})
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'decision':'DONT_NOTIFY','count':len(r['comunicatii'])},ensure_ascii=False))

